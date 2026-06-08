#!/usr/bin/env python3
"""Derive Classic Resource Bible-backed jünk/specialized commodity semantics.

This maps the existing primitive `native_ev/data/sourced_ev_structures.json`
commodity-like run to named fields from the EV Classic Resource Bible jünk
section. It emits compact semantics and provenance only, not raw records.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_SOURCE = Path('native_ev/data/sourced_ev_structures.json')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_junk.json')
METHOD = 'ev-classic-resource-bible-junk-field-map-v1'
SOURCE_BASIS = 'EV Classic Resource Bible jünk field definitions plus local primitive BRGR structure decode'

# The primitive decoder records every 16-bit word in the 676-byte record. The
# Resource Bible fields are stored as long-aligned values in this local record
# family: SoldAt at word 0, BoughtAt at word 8, BasePrice at word 16, and Flags
# at word 17. Embedded strings begin at byte offset 38 and are intentionally kept
# as display/short names only.
FIELD_INDEX = {
    'soldAt': 0,
    'boughtAt': 8,
    'basePrice': 16,
    'flags': 17,
}

FLAG_BITS = {
    0x0001: 'tribblesMultiplication',
}


def _word(record: dict, index: int) -> int:
    return int(record['fields'][index]['value'])


def _nullable_stellar(value: int) -> int | None:
    return None if value == -1 else value


def _unsigned_16(value: int) -> int:
    return value & 0xFFFF


def _flag_names(flags: int) -> list[str]:
    unsigned = _unsigned_16(flags)
    return [name for bit, name in sorted(FLAG_BITS.items()) if unsigned & bit]


def derive(source: Path) -> dict:
    data = json.loads(source.read_text())
    run = next(
        run for run in data['runs']
        if run.get('candidateType') == 'commodity-like' and run.get('recordSize') == 676
    )
    commodities = []
    for record in run['records']:
        strings = [slot['text'] for slot in record.get('embeddedStrings', [])]
        resource_id = 128 + int(record['ordinal'])
        flags = _word(record, FIELD_INDEX['flags'])
        commodities.append({
            'resourceId': resource_id,
            'ordinal': int(record['ordinal']),
            'chunkIndex': int(record['chunkIndex']),
            'byteOffset': int(record['byteOffset']),
            'displayName': strings[0] if strings else f'junk_{resource_id}',
            'shortName': strings[1] if len(strings) > 1 else None,
            'fieldSource': 'EV Classic Resource Bible jünk fields, lines 237-247 of extracted text',
            'semanticFields': {
                'soldAtStellarId': _nullable_stellar(_word(record, FIELD_INDEX['soldAt'])),
                'boughtAtStellarId': _nullable_stellar(_word(record, FIELD_INDEX['boughtAt'])),
                'basePrice': _word(record, FIELD_INDEX['basePrice']),
                'flagsSigned': flags,
                'flagsUnsigned': _unsigned_16(flags),
                'flagNames': _flag_names(flags),
            },
        })
    return {
        'schemaVersion': 1,
        'sourceFile': data['sourceFile'],
        'sourceSha256': data['sourceSha256'],
        'sourceManifest': str(source),
        'method': METHOD,
        'sourceBasis': SOURCE_BASIS,
        'resourceIdBase': 128,
        'recordRun': {
            'candidateType': run['candidateType'],
            'recordSize': run['recordSize'],
            'count': run['count'],
            'confidence': 'manual-backed-field-map',
        },
        'fieldIndex': FIELD_INDEX,
        'flagBits': {f'0x{bit:04X}': name for bit, name in sorted(FLAG_BITS.items())},
        'junkCommodities': commodities,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    manifest = derive(args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f"wrote {args.out} junkCommodities={len(manifest['junkCommodities'])} method={METHOD}")


if __name__ == '__main__':
    main()
