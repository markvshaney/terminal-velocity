#!/usr/bin/env python3
"""Promote EV Classic static system resource IDs and candidate link fields.

This intentionally does not map coordinates, governments, hazards, services,
or exact record-to-name joins yet. It packages the already verified syst-like
primitive run into a stable semantic manifest and promotes the field family
whose values match the EV Classic Resource Bible hyperspace-link domain.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_STRUCTURES = Path('native_ev/data/sourced_ev_structures.json')
DEFAULT_NAMES = Path('native_ev/data/sourced_ev_names.json')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_systems.json')
METHOD = 'ev-classic-static-system-id-name-seed-link-candidate-map-v1'
SOURCE_BASIS = 'EV Classic Resource Bible syst x/y and Con1-Con16 field-family definitions plus local primitive BRGR syst-like structure decode and heuristic EV Data.rez system-name seed list'
PROMOTION_BOUNDARY = 'IDs/resource ordering, heuristic name seeds, and candidate hyperspace link fields are promoted; coordinates, services, hazards, governments, and exact record-to-name mapping remain pending.'
LINK_WORD_INDICES = list(range(4, 20))


def _syst_run(structures: dict) -> dict:
    return next(run for run in structures['runs'] if run.get('candidateType') == 'syst-like' and run.get('recordSize') == 88)


def _word(record: dict, index: int) -> int:
    return int(record['fields'][index]['value'])


def _candidate_links(record: dict) -> dict:
    raw = [_word(record, index) for index in LINK_WORD_INDICES]
    return {
        'wordIndices': LINK_WORD_INDICES,
        'rawValues': raw,
        'linkedSystemResourceIds': [value for value in raw if value != -1],
        'noLinkSentinel': -1,
        'validResourceRange': [128, 1127],
        'sourceConfidence': 'decoded-pattern-plus-resource-bible-field-family-candidate',
        'sourceNote': 'EV Classic Resource Bible defines syst Con1-Con16 as -1/no link or 128-1127 system IDs; these 16 local word slots match that value domain across the syst-like run, but exact coordinate/government/hazard field alignment remains pending.',
    }


def derive(structures_path: Path, names_path: Path) -> dict:
    structures = json.loads(structures_path.read_text())
    names = json.loads(names_path.read_text())
    run = _syst_run(structures)
    systems = []
    for record in run['records']:
        ordinal = int(record['ordinal'])
        systems.append({
            'resourceId': 128 + ordinal,
            'ordinal': ordinal,
            'chunkIndex': int(record['chunkIndex']),
            'byteOffset': int(record['byteOffset']),
            'size': int(record['size']),
            'semanticStatus': 'ids_promoted_names_seeded_links_candidate_fields_pending',
            'semanticFields': {
                'candidateHyperspaceLinks': _candidate_links(record),
            },
            'sourceRecord': {
                'candidateType': run['candidateType'],
                'recordSize': run['recordSize'],
                'fieldCount': len(record.get('fields', [])),
                'fieldsComplete': bool(record.get('fieldsComplete')),
            },
        })
    return {
        'schemaVersion': 1,
        'sourceFile': structures['sourceFile'],
        'sourceSha256': structures['sourceSha256'],
        'sourceManifests': {
            'structures': str(structures_path),
            'names': str(names_path),
        },
        'method': METHOD,
        'sourceBasis': SOURCE_BASIS,
        'resourceIdBase': 128,
        'recordRun': {
            'candidateType': run['candidateType'],
            'recordSize': run['recordSize'],
            'count': run['count'],
            'confidence': 'decoded-resource-backed-id-ordering',
        },
        'fieldFamilies': {
            'candidateHyperspaceLinks': {
                'wordIndices': LINK_WORD_INDICES,
                'resourceBibleFieldFamily': 'syst Con1-Con16',
                'valueDomain': '-1 for no link; 128-1127 for linked system resource IDs',
                'confidence': 'decoded-pattern-plus-resource-bible-field-family-candidate',
            },
        },
        'systemNameSeeds': names.get('systemNames', []),
        'systems': systems,
        'promotionBoundary': PROMOTION_BOUNDARY,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--structures', type=Path, default=DEFAULT_STRUCTURES)
    parser.add_argument('--names', type=Path, default=DEFAULT_NAMES)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    manifest = derive(args.structures, args.names)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f"wrote {args.out} systems={len(manifest['systems'])} method={METHOD}")


if __name__ == '__main__':
    main()
