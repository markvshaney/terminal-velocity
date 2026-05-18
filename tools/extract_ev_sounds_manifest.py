#!/usr/bin/env python3
"""Catalog EV Classic sound resources from the local EV Sounds.rez.

This first pass is provenance-first. It does not claim audio decoding yet; each
`snd ` resource is recorded with resource-map identity, source byte location,
size, and a raw header preview so later decoding can be source-backed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path


DEFAULT_SOURCE = Path('source-assets/ev-classic/Nova Files/EV Sounds.rez')
DEFAULT_OUTPUT = Path('native_ev/data/sourced_ev_sounds.json')
METHOD = 'classic-mac-snd-catalog-v1'


def iter_chunks(data: bytes) -> list[tuple[int, int, int]]:
    chunks: list[tuple[int, int, int]] = []
    n = len(data)
    for pos in range(20, 10000, 12):
        if pos + 12 > n:
            break
        resource_id, offset, size = struct.unpack_from('<III', data, pos)
        if offset <= 0 or offset >= n or size <= 0 or offset + size > n:
            break
        chunks.append((resource_id, offset, size))
    return chunks


def _is_resource_type(raw: bytes) -> bool:
    if len(raw) != 4:
        return False
    # Classic Mac resource types are four printable-ish MacRoman bytes; allow the
    # trailing space in `snd `, reject NUL-heavy bogus section records.
    return all(32 <= b <= 255 for b in raw)


def iter_resource_map_entries(data: bytes, chunks: list[tuple[int, int, int]]) -> list[dict]:
    if not chunks:
        return []
    map_offset = chunks[-1][1]
    resources: list[dict] = []
    chunk_count = len(chunks)
    for section_index in range(32):
        record_offset = map_offset + 8 + section_index * 12
        if record_offset + 12 > len(data):
            break
        raw_type = data[record_offset:record_offset + 4]
        if not _is_resource_type(raw_type):
            # The previous graphics parser used a fixed eight-section table. Sound
            # files have fewer real sections; stopping at the first invalid section
            # prevents NUL padding from being misread as millions of resources.
            break
        section_offset = int.from_bytes(data[record_offset + 4:record_offset + 8], 'big')
        count = int.from_bytes(data[record_offset + 8:record_offset + 12], 'big')
        table_start = map_offset + section_offset
        table_end = table_start + count * 266
        if section_offset <= 0 or count < 0 or table_end > len(data):
            break
        resource_type = raw_type.decode('macroman', 'replace')
        for resource_index in range(count):
            entry_offset = table_start + resource_index * 266
            chunk_index = int.from_bytes(data[entry_offset:entry_offset + 4], 'big')
            if chunk_index < 0 or chunk_index >= chunk_count:
                continue
            resource_id = int.from_bytes(data[entry_offset + 8:entry_offset + 10], 'big')
            name = data[entry_offset + 10:entry_offset + 266].split(b'\0', 1)[0].decode('macroman', 'replace').strip()
            resources.append({
                'type': resource_type,
                'resourceId': resource_id,
                'name': name,
                'chunkIndex': chunk_index,
                'resourceMapEntryOffset': entry_offset,
            })
    return resources


def build_manifest(source: Path) -> dict:
    data = source.read_bytes()
    chunks = iter_chunks(data)
    resources = iter_resource_map_entries(data, chunks)
    snd_resources = [resource for resource in resources if resource['type'] == 'snd ']
    sound_assets: list[dict] = []
    for resource in snd_resources:
        _chunk_id, byte_offset, size = chunks[resource['chunkIndex']]
        raw = data[byte_offset:byte_offset + size]
        sound_assets.append({
            'type': resource['type'],
            'resourceId': resource['resourceId'],
            'name': resource['name'],
            'chunkIndex': resource['chunkIndex'],
            'byteOffset': byte_offset,
            'size': size,
            'status': 'catalog-only',
            'rawHeaderBytes': list(raw[:32]),
        })
    sound_assets.sort(key=lambda item: item['resourceId'])
    type_catalog = []
    for resource_type in sorted({resource['type'] for resource in resources}):
        items = [resource for resource in resources if resource['type'] == resource_type]
        type_catalog.append({
            'type': resource_type,
            'count': len(items),
            'decodeStatus': 'catalog-only',
            'note': 'classic Mac sound resources cataloged; audio decoding not yet implemented' if resource_type == 'snd ' else 'catalog-only',
        })
    return {
        'sourceFile': source.as_posix(),
        'sourceSha256': hashlib.sha256(data).hexdigest(),
        'method': METHOD,
        'note': 'Provenance-first catalog of classic Mac `snd ` resources from local EV Sounds.rez; audio decoding is intentionally deferred.',
        'chunkCount': len(chunks),
        'resourceCount': len(resources),
        'resourceTypeCatalog': type_catalog,
        'soundAssets': sound_assets,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    manifest = build_manifest(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + '\n')
    print(f"wrote {args.output} sounds={len(manifest['soundAssets'])} chunks={manifest['chunkCount']}")


if __name__ == '__main__':
    main()
