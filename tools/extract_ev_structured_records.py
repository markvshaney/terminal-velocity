#!/usr/bin/env python3
"""Decode fixed-size structured record families from local EV Data.rez.

This is a bounded first pass, not a full EV resource schema. It preserves source
provenance and decodes records into typed numeric fields so later slices can map
specific offsets to systems, stellar objects, governments, ships, outfits, etc.

The source .rez remains local-only and ignored by git. The generated manifest is
small enough to commit and deliberately avoids copying long text resources or raw
binary payloads.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from collections import Counter
from pathlib import Path

DEFAULT_SOURCE = Path('source-assets/ev-classic/Nova Files/EV Data.rez')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_structures.json')
METHOD = 'brgr-full-field-decode-v2'

# Fixed-size runs observed in the local EV Classic Data.rez. Names are confidence-
# labeled candidates until individual fields are verified against independent EV
# resource docs or in-game behavior.
RUN_LABELS = {
    88: {
        'candidateType': 'syst-like',
        'confidence': 'medium',
        'reason': '67 contiguous 88-byte binary records; plausible EV Classic system-count scale.',
    },
    306: {
        'candidateType': 'government-like',
        'confidence': 'low',
        'reason': '19 contiguous records with visible faction names embedded after numeric headers.',
    },
    192: {
        'candidateType': 'government-or-status-like',
        'confidence': 'low',
        'reason': '25 contiguous records with faction labels and scan/fine-looking numeric ranges.',
    },
    676: {
        'candidateType': 'commodity-like',
        'confidence': 'medium',
        'reason': '19 contiguous records with commodity names embedded in fixed-width string slots.',
    },
    1970: {
        'candidateType': 'mission-like',
        'confidence': 'low',
        'reason': '116 large fixed records in the mission-text region; likely mission/job logic records.',
    },
    282: {
        'candidateType': 'weapon-like',
        'confidence': 'medium',
        'reason': '42 contiguous compact numeric records following weapon/outfit descriptions.',
    },
    1028: {
        'candidateType': 'outfit-like',
        'confidence': 'medium',
        'reason': '54 contiguous records after weapon records; price-like fields and outfit-scale count.',
    },
    400: {
        'candidateType': 'spob-like',
        'confidence': 'medium',
        'reason': '219 contiguous 400-byte records; plausible stellar-object/port record count.',
    },
    1860: {
        'candidateType': 'ship-like',
        'confidence': 'medium',
        'reason': '27 contiguous large records after spob-like records; plausible ship definition count.',
    },
    1118: {
        'candidateType': 'outfit-or-fleet-like',
        'confidence': 'low',
        'reason': '107 contiguous fixed records; binary structure not field-mapped yet.',
    },
    428: {
        'candidateType': 'fleet/dude-like',
        'confidence': 'low',
        'reason': '108 contiguous fixed records with repeated ship-id-like short arrays.',
    },
    134: {
        'candidateType': 'pers-like',
        'confidence': 'low',
        'reason': '26 contiguous fixed records near end of structured data.',
    },
}

# Decode every 16-bit field in every structured record. Semantic field names are
# candidate mappings; the authoritative layer is the offset-indexed word list.
PREFIX_WORD_LIMIT = 0
STRING_SLOT_LIMIT = 12
MAX_STRING_LEN = 48


def iter_brgr_chunks(data: bytes) -> list[dict]:
    if not data.startswith(b'BRGR'):
        raise ValueError('not a BRGR-style .rez file')
    chunks: list[dict] = []
    for pos in range(20, min(len(data) - 12, 20000), 12):
        resource_id, offset, size = struct.unpack_from('<III', data, pos)
        if offset <= 0 or offset >= len(data) or size <= 0 or offset + size > len(data):
            break
        chunks.append({
            'chunkIndex': len(chunks),
            'tableOffset': pos,
            'resourceId': resource_id,
            'byteOffset': offset,
            'size': size,
        })
    return chunks


def fixed_size_runs(chunks: list[dict], min_count: int = 3) -> list[dict]:
    runs: list[dict] = []
    start = 0
    while start < len(chunks):
        size = chunks[start]['size']
        end = start + 1
        while end < len(chunks) and chunks[end]['size'] == size:
            end += 1
        count = end - start
        if count >= min_count:
            label = RUN_LABELS.get(size, {
                'candidateType': 'unknown-fixed-record',
                'confidence': 'low',
                'reason': 'contiguous same-size record run; schema not identified yet.',
            })
            runs.append({
                'runIndex': len(runs),
                'startChunkIndex': chunks[start]['chunkIndex'],
                'endChunkIndex': chunks[end - 1]['chunkIndex'],
                'count': count,
                'recordSize': size,
                'byteOffset': chunks[start]['byteOffset'],
                **label,
            })
        start = end
    return runs


def decode_c_string_slots(raw: bytes) -> list[dict]:
    slots: list[dict] = []
    i = 0
    while i < len(raw):
        b = raw[i]
        if 32 <= b <= 126 and (i == 0 or raw[i - 1] in (0, 255)):
            start = i
            while i < len(raw) and 32 <= raw[i] <= 126:
                i += 1
            if i - start >= 4:
                text = raw[start:i].decode('macroman', 'ignore').strip()
                if text and len(slots) < STRING_SLOT_LIMIT:
                    slots.append({'offset': start, 'text': text[:MAX_STRING_LEN]})
            continue
        i += 1
    return slots


def decode_record(raw: bytes, size: int) -> dict:
    word_count = len(raw) // 2
    words_be = list(struct.unpack('>' + 'h' * word_count, raw[:word_count * 2]))
    fields = [
        {
            'name': f'word_{idx:03d}',
            'wordIndex': idx,
            'byteOffsetInRecord': idx * 2,
            'value': value,
        }
        for idx, value in enumerate(words_be)
    ]
    return {
        'fieldEncoding': 'big-endian signed 16-bit words',
        'fieldCount': word_count,
        'fieldsComplete': True,
        'fields': fields,
        'embeddedStrings': decode_c_string_slots(raw),
    }


def extract_structures(source: Path) -> dict:
    data = source.read_bytes()
    chunks = iter_brgr_chunks(data)
    size_counts = Counter(chunk['size'] for chunk in chunks)
    runs = fixed_size_runs(chunks)
    by_start = {run['startChunkIndex']: run for run in runs}

    decoded_runs = []
    for run in runs:
        if run['recordSize'] not in RUN_LABELS:
            continue
        records = []
        for ordinal, chunk_index in enumerate(range(run['startChunkIndex'], run['endChunkIndex'] + 1)):
            chunk = chunks[chunk_index]
            raw = data[chunk['byteOffset']:chunk['byteOffset'] + chunk['size']]
            records.append({
                'ordinal': ordinal,
                'chunkIndex': chunk['chunkIndex'],
                'sourceResourceId': chunk['resourceId'],
                'byteOffset': chunk['byteOffset'],
                'size': chunk['size'],
                **decode_record(raw, chunk['size']),
            })
        decoded_runs.append({**run, 'records': records})

    return {
        'sourceFile': str(source),
        'sourceSha256': hashlib.sha256(data).hexdigest(),
        'method': METHOD,
        'note': (
            'Fixed-size BRGR resource-record run decode from local EV Data.rez. '
            'candidateType labels are provisional; field-level semantics require later verification.'
        ),
        'chunkCount': len(chunks),
        'sizeHistogram': [{'size': size, 'count': count} for size, count in size_counts.most_common()],
        'runs': decoded_runs,
        'runDirectory': [
            {k: v for k, v in run.items() if k != 'records'}
            for run in runs
            if run['startChunkIndex'] in by_start
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    manifest = extract_structures(args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(
        f"wrote {args.out} chunks={manifest['chunkCount']} "
        f"structuredRuns={len(manifest['runs'])}"
    )


if __name__ == '__main__':
    main()
