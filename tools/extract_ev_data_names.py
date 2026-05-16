#!/usr/bin/env python3
"""Extract a bounded, provenance-preserving name seed list from EV Data.rez.

This does not claim full EV resource decoding. It reads the local BRGR chunk table,
finds readable text chunks, and derives likely landing names from the opening clause
of each planet/station description. The output is intentionally a manifest with
byte offsets and evidence snippets so later iterations can replace this heuristic
with full resource-typed parsing without losing provenance.
"""
from __future__ import annotations

import argparse
import json
import re
import struct
from pathlib import Path

DEFAULT_SOURCE = Path('source-assets/ev-classic/Nova Files/EV Data.rez')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_names.json')
METHOD = 'brgr-text-chunk-heuristic-v1'

SYSTEM_SEEDS = [
    'Sol',
    'Centauri',
    'Sirius',
    'Tau Ceti',
    'Enyo',
    'Antares',
    'Alkaid',
    'Zaxted',
    'Clotho',
]

NAME_PATTERNS = [
    re.compile(r'^(?:As every schoolkid knows,\s+)?(?P<name>[A-Z][A-Za-z0-9 .\'’\-]+?)\s+(?:is|was|features|has|used to|serves|makes|produces|attracts|exports|contains|provides)\b'),
    re.compile(r'^(?P<name>[A-Z][A-Za-z0-9 .\'’\-]+?)\s+-\s+'),
]

STOP_PHRASES = (
    'The Centauri Munitions laser cannon',
    'The neutron blaster',
    'Proton bolt cannons',
    'Torpedo launchers',
    'Missile racks',
    'This auxilliary cargo hold',
)


def iter_brgr_chunks(data: bytes) -> list[dict]:
    if not data.startswith(b'BRGR'):
        raise ValueError('not a BRGR-style .rez file')
    chunks = []
    for pos in range(20, min(len(data) - 12, 20000), 12):
        resource_id, offset, size = struct.unpack_from('<III', data, pos)
        if offset <= 0 or offset >= len(data) or size <= 0 or offset + size > len(data):
            break
        chunks.append({
            'chunkIndex': len(chunks),
            'resourceId': resource_id,
            'byteOffset': offset,
            'size': size,
        })
    return chunks


def clean_text(raw: bytes) -> str:
    text = raw.decode('macroman', 'ignore')
    text = text.replace('\x00', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\ufffd', ' ')
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]+', ' ', text)
    text = text.replace('ˇ', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def readable_score(text: str) -> float:
    if not text:
        return 0.0
    good = sum(1 for ch in text if ch.isalnum() or ch in " .,;:'’\"!?()-<>/")
    return good / max(1, len(text))


def likely_name(text: str) -> tuple[str | None, str]:
    evidence = text[:220].strip()
    for pattern in NAME_PATTERNS:
        match = pattern.search(text)
        if match:
            name = match.group('name').strip(" .,-'’\"")
            name = re.sub(r'\s+', ' ', name)
            if 2 <= len(name) <= 40 and not name.startswith(('The ', 'This ', 'Many ', 'Much ', 'Due ', 'A ', 'An ')):
                return name, evidence
    # A few original landing names appear as a standalone first line before the description.
    first_sentence = re.split(r'[.!?]', text, 1)[0].strip()
    if '\n' in first_sentence:
        first_sentence = first_sentence.split('\n', 1)[0].strip()
    if 2 <= len(first_sentence) <= 24 and first_sentence.count(' ') <= 3:
        return first_sentence, evidence
    return None, evidence


def extract_names(source: Path) -> dict:
    data = source.read_bytes()
    chunks = iter_brgr_chunks(data)
    landing_names = []
    seen = set()
    for chunk in chunks:
        text = clean_text(data[chunk['byteOffset']:chunk['byteOffset'] + chunk['size']])
        if len(text) < 20 or readable_score(text) < 0.82:
            continue
        if any(text.startswith(stop) for stop in STOP_PHRASES):
            break
        name, evidence = likely_name(text)
        if not name or name in seen:
            continue
        seen.add(name)
        confidence = 'high' if re.match(rf'^(?:As every schoolkid knows,\s+)?{re.escape(name)}\b', text) else 'medium'
        landing_names.append({
            'name': name,
            'chunkIndex': chunk['chunkIndex'],
            'resourceId': chunk['resourceId'],
            'byteOffset': chunk['byteOffset'],
            'size': chunk['size'],
            'confidence': confidence,
            'evidence': evidence,
        })
    system_names = []
    for name in SYSTEM_SEEDS:
        encoded = name.encode('macroman')
        offset = data.find(encoded)
        if offset >= 0:
            system_names.append({
                'name': name,
                'byteOffset': offset,
                'confidence': 'medium',
                'evidence': clean_text(data[offset:offset + 160]),
            })
    return {
        'sourceFile': str(source),
        'method': METHOD,
        'note': 'Heuristic name seed list from local EV Data.rez text chunks; not a full resource map decode.',
        'systemNames': system_names,
        'landingNames': landing_names,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    manifest = extract_names(args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f"wrote {args.out} landingNames={len(manifest['landingNames'])} systemNames={len(manifest['systemNames'])}")


if __name__ == '__main__':
    main()
