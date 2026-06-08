#!/usr/bin/env python3
"""Record current Terminal Velocity service matrix with EV Classic source seeds.

This is a scaffold/readiness manifest, not a Classic-wide decoded service field
promotion. It combines the verified spob-like primitive record run and landing
name seeds with the current runtime service matrix so Lane B has a durable
manifest surface and an explicit promotion boundary.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_STRUCTURES = Path('native_ev/data/sourced_ev_structures.json')
DEFAULT_NAMES = Path('native_ev/data/sourced_ev_names.json')
DEFAULT_UNIVERSE = Path('native_ev/data/universe.json')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_services.json')
METHOD = 'terminal-velocity-service-matrix-scaffold-plus-source-seeds-v1'
SOURCE_BASIS = 'Terminal Velocity runtime universe service matrix plus Levo original-runtime observation, sourced landing-name seeds, and local primitive spob-like structure decode'
PROMOTION_BOUNDARY = 'Current service matrix is Terminal Velocity runtime/scaffold plus Levo original-runtime observation and landing-name/source seeds; Classic-wide decoded service fields remain pending.'


def _spob_run(structures: dict) -> dict:
    return next(run for run in structures['runs'] if run.get('candidateType') == 'spob-like' and run.get('recordSize') == 400)


def _source_labels(system_name: str, body: dict, inventory: dict) -> list[str]:
    labels = []
    evidence_label = inventory.get('sourceEvidenceLabel')
    if evidence_label:
        labels.append(evidence_label)
    if system_name == 'Levo' and body.get('name') == 'Levo Spaceport':
        labels.append('original-runtime-observed')
    labels.append('terminal-velocity-service-provisioning-scaffold')
    # Preserve order while removing duplicates.
    return list(dict.fromkeys(labels))


def derive(structures_path: Path, names_path: Path, universe_path: Path) -> dict:
    structures = json.loads(structures_path.read_text())
    names = json.loads(names_path.read_text())
    universe = json.loads(universe_path.read_text())
    run = _spob_run(structures)
    matrix = []
    for system in universe.get('systems', []):
        for body in system.get('bodies', []):
            inventory = body.get('inventory') or {
                'services': ['repairs', 'commodities', 'jobs'],
                'outfitsForSale': [],
                'shipsForSale': [],
                'weaponsForSale': [],
            }
            body_name = body.get('displayName') or body.get('name')
            if system['name'] == 'Levo' and body_name == 'Levo Spaceport':
                body_name = 'Levo'
            matrix.append({
                'systemName': system['name'],
                'bodyName': body_name,
                'runtimeBodyId': body.get('name'),
                'services': list(inventory.get('services', [])),
                'outfitsForSale': list(inventory.get('outfitsForSale', [])),
                'shipsForSale': list(inventory.get('shipsForSale', [])),
                'weaponsForSale': list(inventory.get('weaponsForSale', [])),
                'sourceLabels': _source_labels(system['name'], body, inventory),
                'sourceEvidence': inventory.get('sourceEvidence'),
                'oracleStatus': 'classic_runtime_service_matrix_pending',
            })
    return {
        'schemaVersion': 1,
        'sourceFile': structures['sourceFile'],
        'sourceSha256': structures['sourceSha256'],
        'sourceManifests': {
            'structures': str(structures_path),
            'names': str(names_path),
            'runtimeUniverse': str(universe_path),
        },
        'method': METHOD,
        'sourceBasis': SOURCE_BASIS,
        'spobRecordRun': {
            'candidateType': run['candidateType'],
            'recordSize': run['recordSize'],
            'count': run['count'],
            'confidence': 'decoded-resource-backed-record-family-readiness',
        },
        'landingNameSeeds': names.get('landingNames', []),
        'serviceMatrix': matrix,
        'promotionBoundary': PROMOTION_BOUNDARY,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--structures', type=Path, default=DEFAULT_STRUCTURES)
    parser.add_argument('--names', type=Path, default=DEFAULT_NAMES)
    parser.add_argument('--universe', type=Path, default=DEFAULT_UNIVERSE)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    manifest = derive(args.structures, args.names, args.universe)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f"wrote {args.out} serviceMatrix={len(manifest['serviceMatrix'])} method={METHOD}")


if __name__ == '__main__':
    main()
