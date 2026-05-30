#!/usr/bin/env python3
"""Derive Classic Resource Bible-backed government semantics from sourced EV structures.

This does not copy raw proprietary records. It maps the existing primitive
`native_ev/data/sourced_ev_structures.json` government-like run to named fields
from the EV Classic Resource Bible and emits compact legal/faction semantics.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_SOURCE = Path('native_ev/data/sourced_ev_structures.json')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_governments.json')
METHOD = 'ev-classic-resource-bible-govt-field-map-v1'

FIELD_INDEX = {
    'unused': 0,
    'flags': 1,
    'ally': 2,
    'enemy': 3,
    'crimeTolerance': 4,
    'smugglingPenalty': 5,
    'disablePenalty': 6,
    'boardPenalty': 7,
    'killPenalty': 8,
    'shootPenalty': 9,
    'initialRecord': 10,
}

FLAG_BITS = {
    0x0001: 'xenophobicWarshipsAttackNonAllies',
    0x0002: 'attackCriminalInNonAlliedSystems',
    0x0004: 'alwaysAttacksPlayer',
    0x0008: 'neverAttacksPlayer',
    0x0010: 'warshipsRetreatBelowQuarterShields',
    0x0020: 'ignoreInGoodSamaritan',
    0x0100: 'persShipsActAsEscapePodUsed',
    0x0200: 'warshipsTakeBribes',
    0x0400: 'cannotHailShips',
    0x0800: 'shipsStartDisabled',
    0x1000: 'warshipsPlunderBeforeDestroying',
    0x2000: 'freightersTakeBribes',
    0x4000: 'planetsTakeBribes',
    0x8000: 'largeBribesOrAlwaysPlanetBribe',
}


def _word(record: dict, index: int) -> int:
    return int(record['fields'][index]['value'])


def _unsigned_16(value: int) -> int:
    return value & 0xFFFF


def _flag_names(flags: int) -> list[str]:
    unsigned = _unsigned_16(flags)
    return [name for bit, name in sorted(FLAG_BITS.items()) if unsigned & bit]


def _name(record: dict) -> str:
    strings = [slot['text'] for slot in record.get('embeddedStrings', [])]
    return strings[-1] if strings else f"govt_{128 + int(record['ordinal'])}"


def derive(source: Path) -> dict:
    data = json.loads(source.read_text())
    run = next(
        run for run in data['runs']
        if run.get('candidateType') == 'government-or-status-like' and run.get('recordSize') == 192
    )
    governments = []
    for record in run['records']:
        resource_id = 128 + int(record['ordinal'])
        flags = _word(record, FIELD_INDEX['flags'])
        entry = {
            'resourceId': resource_id,
            'ordinal': int(record['ordinal']),
            'chunkIndex': int(record['chunkIndex']),
            'byteOffset': int(record['byteOffset']),
            'name': _name(record),
            'shortName': record.get('embeddedStrings', [{}])[0].get('text') if record.get('embeddedStrings') else None,
            'fieldSource': 'EV Classic Resource Bible gövt fields, lines 179-229 of extracted text',
            'semanticFields': {
                'flagsSigned': flags,
                'flagsUnsigned': _unsigned_16(flags),
                'flagNames': _flag_names(flags),
                'allyGovernmentId': resource_id if _word(record, FIELD_INDEX['ally']) in (-1, resource_id) else _word(record, FIELD_INDEX['ally']),
                'enemyGovernmentId': None if _word(record, FIELD_INDEX['enemy']) == -1 else _word(record, FIELD_INDEX['enemy']),
                'crimeTolerance': _word(record, FIELD_INDEX['crimeTolerance']),
                'smugglingPenalty': _word(record, FIELD_INDEX['smugglingPenalty']),
                'disablePenalty': _word(record, FIELD_INDEX['disablePenalty']),
                'boardPenalty': _word(record, FIELD_INDEX['boardPenalty']),
                'killPenalty': _word(record, FIELD_INDEX['killPenalty']),
                'shootPenalty': _word(record, FIELD_INDEX['shootPenalty']),
                'shootPenaltyRuntimeNote': 'EV Classic Resource Bible says ShootPenalty is currently ignored',
                'initialRecord': _word(record, FIELD_INDEX['initialRecord']),
            },
        }
        governments.append(entry)
    return {
        'schemaVersion': 1,
        'sourceFile': data['sourceFile'],
        'sourceSha256': data['sourceSha256'],
        'sourceManifest': str(source),
        'method': METHOD,
        'sourceBasis': 'EV Classic Resource Bible gövt field definitions plus local primitive BRGR structure decode',
        'resourceIdBase': 128,
        'recordRun': {
            'candidateType': run['candidateType'],
            'recordSize': run['recordSize'],
            'count': run['count'],
            'confidence': 'manual-backed-field-map',
        },
        'fieldIndex': FIELD_INDEX,
        'flagBits': {f'0x{bit:04X}': name for bit, name in sorted(FLAG_BITS.items())},
        'governments': governments,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    manifest = derive(args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f"wrote {args.out} governments={len(manifest['governments'])} method={METHOD}")


if __name__ == '__main__':
    main()
