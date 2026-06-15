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
METHOD = 'terminal-velocity-service-matrix-scaffold-plus-source-seeds-v2'
SOURCE_BASIS = 'Terminal Velocity runtime universe service matrix plus Levo original-runtime observation, sourced landing-name seeds, EV Classic Resource Bible spöb service/store fields, and local primitive spob-like structure decode'
PROMOTION_BOUNDARY = 'Current service matrix is Terminal Velocity runtime/scaffold plus Levo original-runtime observation and landing-name/source seeds; Resource Bible spöb service/store flags are recorded as readiness inputs, but Classic-wide decoded service fields remain pending.'

RESOURCE_BIBLE_SPOB_SERVICE_FIELDS = [
    {
        'field': 'Flags bit 0x00000001',
        'meaning': 'can land/dock here',
        'serviceImplication': 'landing/docking availability input',
    },
    {
        'field': 'Flags bit 0x00000002',
        'meaning': 'has commodity exchange',
        'serviceImplication': 'commodity exchange availability input',
    },
    {
        'field': 'Flags bit 0x00000004',
        'meaning': 'can outfit ship here',
        'serviceImplication': 'outfitter availability input',
    },
    {
        'field': 'Flags bit 0x00000008',
        'meaning': 'can buy ships here',
        'serviceImplication': 'shipyard availability input',
    },
    {
        'field': 'Flags bit 0x00000040',
        'meaning': 'has bar',
        'serviceImplication': 'bar availability input',
    },
    {
        'field': 'TechLevel and SpecialTech (x3)',
        'meaning': 'base and exact special tech levels controlling item and ship availability',
        'serviceImplication': 'store stock gate input after spob field offsets and item/ship tech joins are promoted',
    },
    {
        'field': 'Govt and MinCoolness',
        'meaning': 'stellar government affiliation and landing clearance threshold',
        'serviceImplication': 'legal landing/service access input after spob field offsets and government joins are promoted',
    },
]


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


def _service_store_readiness_summary(run: dict, names: dict, matrix: list[dict]) -> dict:
    landing_seeds = names.get('landingNames', [])
    tv_scaffold_rows = [
        row for row in matrix
        if 'terminal-velocity-service-provisioning-scaffold' in row.get('sourceLabels', [])
    ]
    original_observed_rows = [
        row for row in matrix
        if 'original-runtime-observed' in row.get('sourceLabels', [])
    ]
    return {
        'schemaVersion': 1,
        'sourceLabel': 'resource-bible-backed-service-store-provisioning-readiness',
        'oracleStatus': 'service_store_matrix_blocked_pending_spob_field_offset_oracle',
        'sourceBasis': [
            'decoded-record-family',
            'decoded-original-variable',
            'resource-bible-field',
            'original-runtime-observed',
            'tv-scaffold',
        ],
        'inputs': [
            'spobRecordRun',
            'landingNameSeeds',
            'serviceMatrix',
            'EV Classic Resource Bible spöb lines 836-897',
        ],
        'inputSummaryCount': 4,
        'spobRecordCount': run['count'],
        'spobRecordSizeBytes': run['recordSize'],
        'landingNameSeedCount': len(landing_seeds),
        'runtimeServiceMatrixRowCount': len(matrix),
        'originalObservedServiceRows': len(original_observed_rows),
        'terminalVelocityScaffoldRows': len(tv_scaffold_rows),
        'resourceBibleSpobServiceFields': RESOURCE_BIBLE_SPOB_SERVICE_FIELDS,
        'readyStaticInputFamilies': [
            '219 contiguous 400-byte spob-like primitive records from EV Data.rez',
            '72 high-confidence landing/body name seeds from sourced EV names manifest',
            'Resource Bible spöb service/store flag definitions for land/dock, commodities, outfitter, shipyard, bar, tech levels, government, and landing coolness',
            'current Terminal Velocity service matrix plus Levo original-runtime no-outfitter/no-shipyard observation',
        ],
        'nextEvidenceFamilies': [
            'exact Classic spöb field-offset/template or source-struct oracle tying Resource Bible fields to decoded word offsets',
            'record-to-name join between decoded spöb records and landing/body names',
            'validated item/ship TechLevel and SpecialTech joins for outfitter/shipyard stock availability',
            'Basilisk spot checks only for ambiguous UI-sensitive service surfaces after static joins narrow the target',
        ],
        'blockedPromotionClaims': [
            'Classic-wide service/store matrix rows for all landable bodies',
            'decoded commodity/outfitter/shipyard/bar availability from current spob-like words',
            'shipyard/outfitter stock availability from TechLevel or SpecialTech joins',
            'legal landing/service denial behavior from Govt and MinCoolness fields',
        ],
        'promotionBlockers': [
            'spob-like record family is decoded but exact Classic spöb field offsets are not promoted',
            'landing/body name seeds are not a complete record-to-name join for all decoded spöb records',
            'current runtime service rows remain Terminal Velocity scaffold except the narrow Levo original-runtime service boundary',
            'Resource Bible field definitions identify intended semantics but cannot assign decoded offsets without a template/source/validated surrogate packet',
        ],
        'promotionStatus': 'not-promoted; readiness packet only pending spob field-offset and record-name join evidence',
        'requiredVerifiersBeforePromotion': [
            'python3 tools/extract_ev_service_semantics.py',
            'python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_services_manifest_records_current_service_matrix_scaffold -v',
            'python3 tools/run_gameplay_scenarios.py system_service_provisioning_scout --pretty',
        ],
    }


def _service_store_promotion_blocker_matrix_summary() -> dict:
    return {
        'schemaVersion': 1,
        'sourceLabel': 'resource-bible-backed-service-store-promotion-blocker-matrix',
        'oracleStatus': 'service_store_promotion_blocked_pending_spob_offset_name_and_stock_joins',
        'sourceBasis': [
            'decoded-record-family',
            'decoded-original-variable',
            'resource-bible-field',
            'tv-scaffold',
        ],
        'inputSummaries': [
            'serviceStoreProvisioningReadinessSummary',
            'spobRecordRun',
            'landingNameSeeds',
            'serviceMatrix',
        ],
        'blockingQuestions': [
            {
                'question': 'Which exact Classic spöb field offsets carry service flags, TechLevel, SpecialTech, Govt, and MinCoolness?',
                'requiredEvidence': 'Classic-specific TMPL/ResEdit/source-struct packet or validated surrogate tying Resource Bible fields to decoded 400-byte record offsets',
                'blockedClaims': ['decoded service flags', 'decoded stock availability', 'legal landing/service gates'],
            },
            {
                'question': 'Which decoded spöb records join to each Classic landing/body name?',
                'requiredEvidence': 'complete record-to-name join or packet-level original-runtime evidence for named target records',
                'blockedClaims': ['Classic-wide per-port service rows', 'per-port stock matrix rows'],
            },
            {
                'question': 'Which outfit, weapon, and ship records join to TechLevel/SpecialTech store availability at each promoted port?',
                'requiredEvidence': 'item/ship/outfit resource joins plus focused service/store verifier output',
                'blockedClaims': ['outfitter stock availability', 'shipyard stock availability', 'weapon store availability'],
            },
        ],
        'allowedUsesBeforePromotion': [
            'Keep current Terminal Velocity service rows labeled as scaffold except narrow original-runtime-observed Levo service absence.',
            'Use Resource Bible spöb service fields as a routing worklist for future evidence packets.',
            'Run Basilisk spot checks only after static joins narrow the target port/service ambiguity.',
        ],
        'promotionStatus': 'not-promoted; blocker matrix only pending Classic-specific spöb offset, record-name, and stock join evidence',
    }


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
        'serviceStoreProvisioningReadinessSummary': _service_store_readiness_summary(run, names, matrix),
        'serviceStorePromotionBlockerMatrixSummary': _service_store_promotion_blocker_matrix_summary(),
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
