#!/usr/bin/env python3
"""Promote EV Classic static system resource IDs, coordinates, and link fields.

This intentionally does not map coordinate numeric units, governments, hazards,
services, or exact record-to-name joins yet. It packages the already verified
syst-like primitive run into a stable semantic manifest and promotes the field
families whose values match Resource Bible map coordinate and hyperspace-link
semantics.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_STRUCTURES = Path('native_ev/data/sourced_ev_structures.json')
DEFAULT_NAMES = Path('native_ev/data/sourced_ev_names.json')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_systems.json')
METHOD = 'ev-classic-static-system-id-name-seed-coordinate-link-slot-coordinate-display-candidates-link-graph-levo-name-map-v6'
SOURCE_BASIS = 'EV Classic Resource Bible syst xPos/yPos and Con1-Con16 field-family definitions plus local primitive BRGR syst-like structure decode, heuristic EV Data.rez system/landing-name seed list, Resource Bible system ID #128 start-system rule, and original-runtime-observed starting system Levo'
PROMOTION_BOUNDARY = 'IDs/resource ordering, heuristic name seeds, exact resource ID 128 to Levo system-name mapping, raw xPos/yPos coordinate word pairs, coordinate word-domain summary, non-promoted display interpretation candidates, signed 32-bit big-endian raw-long coordinate candidates, Con1-Con16 link slot names, raw link values, in-run target resource/ordinal cross-links, and candidate link-graph summary statistics are promoted as analysis inputs; coordinate display units/map scaling, services, hazards, governments, and remaining exact record-to-name mapping remain pending.'
COORDINATE_WORD_INDICES = [0, 1, 2, 3]
LINK_WORD_INDICES = list(range(4, 20))
LINK_SLOT_NAMES = [f'Con{index}' for index in range(1, 17)]
EXACT_SYSTEM_NAME_MAPPINGS = {
    128: {
        'systemName': 'Levo',
        'confidence': 'fidelity-promoted-for-resource-128-start-system-name',
        'sourceBasis': [
            'resource-bible-field',
            'manual-doc-backed',
            'original-runtime-observed',
            'decoded-record-family',
        ],
        'sourceNote': 'EV Classic Resource Bible says system ID #128 is the player start/rescue system; original EV Classic runtime observation starts the player in the Levo system; the decoded syst-like resource run is contiguous from resource ID 128, so resource ID 128 maps to Levo. This promotes only that exact record-to-name mapping, not the remaining 66 names or runtime topology.',
    },
}


def _syst_run(structures: dict) -> dict:
    return next(run for run in structures['runs'] if run.get('candidateType') == 'syst-like' and run.get('recordSize') == 88)


def _word(record: dict, index: int) -> int:
    return int(record['fields'][index]['value'])


def _signed_long_from_words(words: list[int]) -> int:
    raw = ((int(words[0]) & 0xFFFF) << 16) | (int(words[1]) & 0xFFFF)
    if raw >= 0x80000000:
        raw -= 0x100000000
    return raw


def _link_slot(record: dict, slot_index: int, resource_ids: set[int]) -> dict:
    word_index = LINK_WORD_INDICES[slot_index]
    raw_value = _word(record, word_index)
    slot = {
        'slotNumber': slot_index + 1,
        'slotName': LINK_SLOT_NAMES[slot_index],
        'wordIndex': word_index,
        'byteOffsetInRecord': record['fields'][word_index]['byteOffsetInRecord'],
        'rawValue': raw_value,
    }
    if raw_value == -1:
        slot['status'] = 'no-link'
    elif 128 <= raw_value <= 1127:
        slot.update({
            'status': 'linked-system',
            'targetResourceId': raw_value,
            'targetOrdinal': raw_value - 128,
            'targetPresentInSystRun': raw_value in resource_ids,
        })
    else:
        slot['status'] = 'out-of-domain'
    return slot


def _candidate_links(record: dict, resource_ids: set[int]) -> dict:
    raw = [_word(record, index) for index in LINK_WORD_INDICES]
    link_slots = [_link_slot(record, slot_index, resource_ids) for slot_index in range(len(LINK_WORD_INDICES))]
    return {
        'wordIndices': LINK_WORD_INDICES,
        'slotNames': LINK_SLOT_NAMES,
        'rawValues': raw,
        'linkSlots': link_slots,
        'linkedSystemResourceIds': [value for value in raw if value != -1],
        'linkedSystemResourceIdsInRun': [slot['targetResourceId'] for slot in link_slots if slot.get('targetPresentInSystRun')],
        'noLinkSentinel': -1,
        'validResourceRange': [128, 1127],
        'sourceConfidence': 'decoded-pattern-plus-resource-bible-field-family-candidate',
        'sourceNote': 'EV Classic Resource Bible defines syst Con1-Con16 as -1/no link or 128-1127 system IDs; these 16 local word slots match that value domain across the syst-like run, so this manifest preserves slot names, raw values, and in-run target resource/ordinal cross-links. Exact record-to-name and runtime route topology mapping remain pending.',
    }


def _raw_coordinate_pair(record: dict, first_word_index: int) -> dict:
    words = [_word(record, first_word_index), _word(record, first_word_index + 1)]
    signed_long = _signed_long_from_words(words)
    return {
        'wordIndices': [first_word_index, first_word_index + 1],
        'rawWords': words,
        'signedLongCandidate': signed_long,
        'rawHex32': f'0x{signed_long & 0xFFFFFFFF:08X}',
        'byteOffsetsInRecord': [
            record['fields'][first_word_index]['byteOffsetInRecord'],
            record['fields'][first_word_index + 1]['byteOffsetInRecord'],
        ],
    }


def _map_coordinates(record: dict) -> dict:
    return {
        'wordIndices': COORDINATE_WORD_INDICES,
        'xPos': _raw_coordinate_pair(record, 0),
        'yPos': _raw_coordinate_pair(record, 2),
        'sourceConfidence': 'resource-bible-field-family-plus-decoded-raw-word-pair-domain-summary-plus-raw-signed-long-candidate',
        'sourceNote': 'EV Classic Resource Bible defines the first two syst fields as xPos/yPos map positions. The local primitive decode is word-based, so this manifest preserves each coordinate as its raw two-word field payload, a signed 32-bit big-endian raw-long candidate, and a run-level component-domain summary. Display units/map scaling remain pending.',
    }


def _axis_range(systems: list[dict], axis: str, key: str) -> list[int]:
    values = [system['semanticFields']['mapCoordinates'][axis][key] for system in systems]
    return [min(values), max(values)]


def _axis_word_range(systems: list[dict], axis: str, word_index: int) -> list[int]:
    values = [system['semanticFields']['mapCoordinates'][axis]['rawWords'][word_index] for system in systems]
    return [min(values), max(values)]


def _coordinate_domain_summary(systems: list[dict]) -> dict:
    x_high_words = sorted({system['semanticFields']['mapCoordinates']['xPos']['rawWords'][0] for system in systems})
    y_high_words = sorted({system['semanticFields']['mapCoordinates']['yPos']['rawWords'][0] for system in systems})
    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-domain-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'xPos': {
            'highWordDistinctValues': x_high_words,
            'highWordRange': _axis_word_range(systems, 'xPos', 0),
            'lowWordRange': _axis_word_range(systems, 'xPos', 1),
            'signedLongCandidateRange': _axis_range(systems, 'xPos', 'signedLongCandidate'),
        },
        'yPos': {
            'highWordDistinctValues': y_high_words,
            'highWordRange': _axis_word_range(systems, 'yPos', 0),
            'lowWordRange': _axis_word_range(systems, 'yPos', 1),
            'signedLongCandidateRange': _axis_range(systems, 'yPos', 'signedLongCandidate'),
        },
        'displayUnitInterpretationStatus': 'not-promoted; raw coordinate component domain is preserved for a later map display scaling/topology pass',
        'sourceNote': 'This summary is computed from the decoded syst-like coordinate payloads and supports the next display-unit/map-scaling interpretation pass. It does not claim EV Classic map pixel units, projection, centering, or route layout fidelity.',
    }


def _coordinate_display_candidate(axis_payload: dict) -> dict:
    """Expose candidate display interpretations without promoting map scaling fidelity."""
    high_word, low_word = axis_payload['rawWords']
    return {
        'rawHighWordAsGridBandCandidate': high_word,
        'rawLowWordAsSubgridOffsetCandidate': low_word,
        'signedLongCandidate': axis_payload['signedLongCandidate'],
        'sourceLabel': 'decoded-resource-backed-coordinate-display-candidate',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'sourceNote': 'This preserves plausible display-analysis components from the decoded raw coordinate payload only. It does not claim EV Classic map pixels, projection, centering, axis inversion, or scaling.',
    }


def _coordinate_display_candidate_summary(systems: list[dict]) -> dict:
    by_resource = {}
    for system in systems:
        coordinates = system['semanticFields']['mapCoordinates']
        by_resource[str(system['resourceId'])] = {
            'xPos': _coordinate_display_candidate(coordinates['xPos']),
            'yPos': _coordinate_display_candidate(coordinates['yPos']),
        }
    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-candidate',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'candidateFamilies': [
            'raw high word as coarse grid/band candidate',
            'raw low word as subgrid/offset candidate',
            'signed 32-bit big-endian raw-long candidate',
        ],
        'resource128': by_resource.get('128'),
        'recordCount': len(systems),
        'sourceNote': 'A later map-scaling pass can compare these per-axis candidates against original-runtime map/click/capture evidence or another promoted source. This manifest still withholds Classic display-unit fidelity.',
    }


def _candidate_link_graph_summary(systems: list[dict]) -> dict:
    """Summarize candidate Con1-Con16 links without promoting named runtime topology."""
    directed_edges = []
    slots_per_system = []
    missing_targets = []
    self_links = []
    for system in systems:
        resource_id = system['resourceId']
        slots = system['semanticFields']['candidateHyperspaceLinks']['linkSlots']
        linked_slots = [slot for slot in slots if slot.get('status') == 'linked-system']
        slots_per_system.append(len(linked_slots))
        for slot in linked_slots:
            target_id = slot['targetResourceId']
            directed_edges.append([resource_id, target_id])
            if target_id == resource_id:
                self_links.append([resource_id, target_id])
            if not slot.get('targetPresentInSystRun'):
                missing_targets.append([resource_id, target_id])
    return {
        'sourceLabel': 'decoded-resource-backed-candidate-link-graph-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'recordCount': len(systems),
        'directedLinkSlotCount': len(directed_edges),
        'uniqueDirectedLinkCount': len({tuple(edge) for edge in directed_edges}),
        'linkedSlotsPerSystemRange': [min(slots_per_system), max(slots_per_system)],
        'systemsWithNoLinkedSlots': sum(1 for count in slots_per_system if count == 0),
        'allTargetsPresentInSystRun': not missing_targets,
        'missingTargetEdges': missing_targets,
        'selfLinkSlotCount': len(self_links),
        'resource128LinkedSystemResourceIds': systems[0]['semanticFields']['candidateHyperspaceLinks']['linkedSystemResourceIds'],
        'sourceNote': 'This is a candidate graph summary from decoded Resource Bible Con1-Con16 link-slot fields. It preserves graph-analysis statistics only; exact Classic runtime topology remains pending until record-to-name joins and map/layout interpretation are promoted.',
    }


def _exact_system_name_mapping(resource_id: int) -> dict | None:
    mapping = EXACT_SYSTEM_NAME_MAPPINGS.get(resource_id)
    if mapping is None:
        return None
    return {
        'resourceId': resource_id,
        **mapping,
    }


def derive(structures_path: Path, names_path: Path) -> dict:
    structures = json.loads(structures_path.read_text())
    names = json.loads(names_path.read_text())
    run = _syst_run(structures)
    resource_ids = {128 + int(record['ordinal']) for record in run['records']}
    systems = []
    for record in run['records']:
        ordinal = int(record['ordinal'])
        resource_id = 128 + ordinal
        exact_name = _exact_system_name_mapping(resource_id)
        semantic_fields = {
            'mapCoordinates': _map_coordinates(record),
            'candidateHyperspaceLinks': _candidate_links(record, resource_ids),
        }
        if exact_name is not None:
            semantic_fields['exactSystemName'] = exact_name
        semantic_status = 'ids_promoted_names_seeded_coordinate_words_links_candidate_fields_pending'
        if exact_name is not None:
            semantic_status = 'ids_promoted_exact_name_coordinate_words_links_candidate_fields_pending'
        systems.append({
            'resourceId': resource_id,
            'ordinal': ordinal,
            'chunkIndex': int(record['chunkIndex']),
            'byteOffset': int(record['byteOffset']),
            'size': int(record['size']),
            'semanticStatus': semantic_status,
            'semanticFields': semantic_fields,
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
            'mapCoordinates': {
                'wordIndices': COORDINATE_WORD_INDICES,
                'resourceBibleFieldFamily': 'syst xPos/yPos',
                'valueDomain': 'map coordinate fields; raw two-word payload, coordinate word-domain summary, and signed 32-bit big-endian raw-long candidate preserved pending display-unit/map-scaling confirmation',
                'confidence': 'resource-bible-field-family-plus-decoded-raw-word-pair-domain-summary-plus-raw-signed-long-candidate',
            },
            'candidateHyperspaceLinks': {
                'wordIndices': LINK_WORD_INDICES,
                'slotNames': LINK_SLOT_NAMES,
                'resourceBibleFieldFamily': 'syst Con1-Con16',
                'valueDomain': '-1 for no link; 128-1127 for linked system resource IDs',
                'confidence': 'decoded-pattern-plus-resource-bible-field-family-candidate',
            },
        },
        'systemNameSeeds': names.get('systemNames', []),
        'coordinateDomainSummary': _coordinate_domain_summary(systems),
        'coordinateDisplayCandidateSummary': _coordinate_display_candidate_summary(systems),
        'candidateLinkGraphSummary': _candidate_link_graph_summary(systems),
        'exactSystemNameMappings': [
            _exact_system_name_mapping(resource_id)
            for resource_id in sorted(EXACT_SYSTEM_NAME_MAPPINGS)
        ],
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
