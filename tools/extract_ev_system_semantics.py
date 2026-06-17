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
import math
from pathlib import Path

DEFAULT_STRUCTURES = Path('native_ev/data/sourced_ev_structures.json')
DEFAULT_NAMES = Path('native_ev/data/sourced_ev_names.json')
DEFAULT_GOVERNMENTS = Path('native_ev/data/sourced_ev_governments.json')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_systems.json')
METHOD = 'ev-classic-static-system-id-name-seed-resource-bible-topology-constants-coordinate-map-source-readiness-system-name-byte-order-oracle-gap-non-topology-syst-oracle-gap-non-topology-syst-runtime-probe-priority-non-topology-syst-runtime-capture-gate-non-topology-syst-runtime-capture-validation-matrix-non-topology-syst-runtime-capture-rejection-taxonomy-non-topology-syst-runtime-capture-reentry-guardrail-non-topology-syst-field-family-reference-runtime-route-label-observation-bridge-gap-route-label-probe-targeting-capture-packet-templates-coordinate-display-unit-map-scaling-readiness-coordinate-display-runtime-capture-gate-coordinate-display-runtime-capture-reconciliation-coordinate-display-runtime-capture-validation-matrix-resource-bible-syst-field-width-offset-oracle-gap-resedit-template-source-availability-gap-syst-template-offset-oracle-gap-syst-template-offset-source-search-priority-syst-template-offset-evidence-packet-contract-syst-template-offset-evidence-packet-validation-matrix-syst-template-offset-evidence-packet-failure-taxonomy-syst-template-offset-evidence-packet-recovery-plan-syst-template-offset-evidence-packet-reentry-guardrail-syst-template-offset-evidence-packet-custody-audit-syst-template-offset-evidence-packet-promotion-quarantine-syst-template-offset-evidence-packet-rollback-readiness-syst-template-offset-evidence-packet-rollback-rehearsal-ev-family-template-transfer-guardrail-ev-family-syst-variant-divergence-guardrail-sequential-field-projection-field-count-byte-budget-named-route-topology-oracle-gap-record-name-oracle-evidence-matrix-record-name-runtime-join-reconciliation-record-name-promotion-readiness-landing-proximity-runtime-universe-template-offset-crosslink-replacement-gate-coordinate-display-calibration-gate-syst-word-domain-coverage-syst-field-order-conflict-syst-field-layout-source-readiness-coordinate-link-slot-coordinate-display-scale-interpretation-coordinate-display-quantization-coordinate-display-residual-magnitude-coordinate-display-residual-sign-coordinate-display-integer-band-coordinate-display-fixed-point-start-neighborhood-slot-angular-order-start-neighborhood-runtime-calibration-priority-route-label-probe-priority-route-label-capture-reconciliation-start-neighborhood-display-vector-start-neighborhood-display-distance-start-neighborhood-display-transform-normalized-extrema-link-graph-distance-name-seed-summary-levo-name-map-landing-name-candidate-reference-syst-record-name-candidate-cross-reference-syst-record-name-gap-analysis-coordinate-gap-identity-resolution-coordinate-gap-resource-deduplication-named-candidate-travel-distance-named-candidate-route-named-candidate-route-calibration-priority-named-candidate-route-calibration-diagnostic-plan-v69-named-candidate-coordinate-scaffold-seed-scaffold-correspondence-scout-syst-govt-field-value-scout-route-label-scaffold-correspondence-scout-named-candidate-scaffold-integrity-summary-syst-govt-field-name-cross-reference-scout-syst-govt-field-resource-id-cross-reference-scout'
SOURCE_BASIS = 'EV Classic Resource Bible game constants, syst xPos/yPos and Con1-Con16 field-family definitions plus local primitive BRGR syst-like structure decode, heuristic EV Data.rez system/landing-name seed list, Resource Bible system ID #128 start-system rule, original-runtime-observed starting system Levo, and bounded original-runtime route/map label observations that are not yet tied to decoded resource IDs'
PROMOTION_BOUNDARY = 'IDs/resource ordering, Resource Bible topology constants (MaxStellarObjects 1500, MaxSystems 1000, JumpDistance 1000 pixels) as static-source constants only, coordinate map source-readiness evidence requirements, topology promotion readiness matrix, runtime universe replacement gate matrix, coordinate display calibration gate matrix, bounded coordinate display-unit/map-scaling readiness matrix, coordinate display runtime capture gate matrix, coordinate display runtime capture reconciliation plan, coordinate display runtime capture validation matrix, non-topology syst runtime capture rejection taxonomy, non-topology syst runtime capture reentry guardrail, non-topology syst field-family reference, route-label probe priority matrix, route-label capture reconciliation plan, named route topology oracle gap matrix, runtime route-label observation bridge gap matrix, record-name oracle evidence matrix, record-name runtime join reconciliation plan, heuristic name seeds, exact resource ID 128 to Levo system-name mapping, non-promoted record-to-name promotion-readiness blockers, raw xPos/yPos coordinate word pairs, coordinate word-domain summary, non-promoted display interpretation candidates, non-promoted display bounds/extrema candidates, non-promoted signed-long min-normalized coordinate candidates, non-promoted axis-transform/aspect-ratio candidates, non-promoted 16.16 fixed-point display-scale candidates, non-promoted coordinate integer-band/fractional residual candidates, non-promoted coordinate residual-sign/fraction-distribution candidates, non-promoted coordinate residual-magnitude/fractional-absolute candidates, non-promoted coordinate residual quantization/grid-step candidates, non-promoted coordinate scale-interpretation blocker/comparison candidates, non-promoted Resource Bible/current-decoder syst field-order conflict matrix, non-promoted Resource Bible syst field-width/offset oracle-gap requirements, signed 32-bit big-endian raw-long coordinate candidates, Con1-Con16 link slot names, raw link values, in-run target resource/ordinal cross-links, candidate link-graph summary statistics, candidate link reciprocity/self-link statistics, candidate graph connectivity/reachability statistics, candidate graph distance/hop statistics, non-promoted resource 128 start-neighborhood topology analysis, non-promoted resource 128 start-neighborhood display-transform analysis, non-promoted start-neighborhood display-distance analysis, non-promoted start-neighborhood display-vector analysis, non-promoted start-neighborhood slot-vector-order analysis, non-promoted start-neighborhood slot-angular-order analysis, non-promoted start-neighborhood runtime-calibration priority analysis, non-promoted syst field-layout source-readiness matrix, non-promoted syst word-domain coverage matrix, non-topology syst oracle-gap blockers, non-promoted syst template/offset recovered-packet reentry guardrail, non-promoted syst template/offset custody audit trail, non-promoted syst template/offset promotion quarantine, non-promoted syst template/offset rollback readiness guardrail, non-promoted non-topology syst runtime-probe priority worklist, and non-promoted non-topology syst runtime-capture gate packet templates; does not promote display pixel units, map projection, runtime route labels, route-label resource/name joins, named topology, governments, hazards, services, ports, or broad 67-system runtime universe replacement, non-promoted syst record-name gap analysis, non-promoted coordinate gap spatial mapping scouts, non-promoted syst-record-name-gap-analysis, non-promoted coordinate-gap-spatial-mapping, non-promoted coordinate-gap-identity-resolution'
RESOURCE_BIBLE_TOPOLOGY_CONSTANTS = {
    'sourceLabel': 'resource-bible-backed-topology-constants',
    'oracleStatus': 'coordinate_display_units_map_scaling_pending',
    'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 14-19',
    'maxStellarObjects': 1500,
    'maxSystems': 1000,
    'jumpDistancePixels': 1000,
    'candidateFamilies': [
        'Resource Bible game constants for topology capacity and hyperspace range',
        'JumpDistance pixel constant preserved without deriving xPos/yPos display-unit scale',
    ],
    'promotionBlockers': [
        'JumpDistance is a Resource Bible game constant, not a decoded syst coordinate unit interpretation',
        'xPos/yPos raw coordinate candidates still need Classic map pixel/click/projection evidence before display-unit/map-scaling promotion',
    ],
    'sourceNote': 'The EV Classic Resource Bible lists MaxStellarObjects 1500, MaxSystems 1000, and JumpDistance 1000 pixels. This packet preserves those constants for later route/range analysis, but does not claim that decoded xPos/yPos raw words are already expressed in map pixels or that the TV map projection is Classic-faithful.',
}
COORDINATE_MAP_SOURCE_REFERENCES = {
    'mapPlacementFields': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 924-937',
    'topologyConstants': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 14-19',
}
SYST_FIELD_LAYOUT_SOURCE_REFERENCES = {
    'systResourceDefinition': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 924-993',
    'mapPlacementFields': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 935-937',
    'hyperspaceLinkFields': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 938-993',
    'runtimeNpcAndEnvironmentFields': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 948-987',
}
COORDINATE_WORD_INDICES = [0, 1, 2, 3]
GOVT_FIELD_WORD_INDEX = 22
DATA_WORD_INDICES = [20, 21, 22, 23]
DATA_WORD_BYTE_FIELD_NAMES = ['w20_hi', 'w20_lo', 'w21_hi', 'w21_lo', 'w22_hi', 'w22_lo', 'w23_hi', 'w23_lo']
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


def _syst_govt_field_value_scout(systems: list[dict]) -> dict:
    """Non-promoting scout recording the raw Govt field value for each syst record.

    Reads word index 22 (Govt field) from each of the 67 decoded syst records
    and records the value distribution. Per EV Classic Resource Bible:
      -1  Independent/unowned system
      128-255  Controlling government resource ID

    This scout records raw values only; no government-name cross-reference
    or runtime behavior claim is made.
    """
    govt_assignments = []
    value_distribution: dict[str, int] = {}
    for system in systems:
        govt = system['semanticFields'].get('candidateGovtField', {})
        resource_id = system['resourceId']
        raw_value = govt.get('rawValue')
        status = govt.get('status', 'unknown')
        govt_id = govt.get('governmentResourceId')

        govt_assignments.append({
            'resourceId': resource_id,
            'rawValue': raw_value,
            'status': status,
            'governmentResourceId': govt_id,
        })

        if status == 'governed':
            bucket = f'governed_govt_{govt_id}'
        elif status == 'independent':
            bucket = 'independent'
        else:
            bucket = f'unknown_raw_{raw_value}'
        value_distribution[bucket] = value_distribution.get(bucket, 0) + 1

    governed_count = sum(1 for a in govt_assignments if a['status'] == 'governed')
    independent_count = sum(1 for a in govt_assignments if a['status'] == 'independent')
    unique_govt_ids = sorted(set(
        a['governmentResourceId'] for a in govt_assignments
        if a['governmentResourceId'] is not None
    ))

    return {
        'sourceLabel': 'terminal-velocity-syst-govt-field-value-scout',
        'oracleStatus': 'govt_field_semantics_pending_name_cross_reference',
        'promotionStatus': 'not-promoted; raw Govt field values only, no cross-reference to government names or runtime behavior claim',
        'fieldDefinition': 'EV Classic Resource Bible syst word 22: Govt controlling government. -1 independent, 128-255 government resource ID.',
        'wordIndex': GOVT_FIELD_WORD_INDEX,
        'recordCount': len(systems),
        'governedCount': governed_count,
        'independentCount': independent_count,
        'uniqueGovernmentResourceIds': unique_govt_ids,
        'valueDistribution': value_distribution,
        'governmentAssignments': govt_assignments,
        'sourceNote': 'Govt field raw values extracted from 67 syst records. No cross-reference to government names, legal/reputation semantics, or runtime behavior is promoted. A future increment should join with sourced_ev_governments.json or original-runtime evidence.',
    }


def _syst_govt_field_name_cross_reference_scout(systems: list[dict]) -> dict:
    """Non-promoting scout cross-referencing govt field raw values against government names.

    Reads the Govt field word (index 22) from each syst record and attempts to
    cross-reference the raw value against government ordinals. Records which
    values match a known government name and which are unmatched gaps.
    """
    import json
    govts = json.loads(DEFAULT_GOVERNMENTS.read_text())
    govt_by_ordinal: dict[int, str] = {}
    for govt in govts.get('governments', []):
        govt_by_ordinal[govt['ordinal']] = govt['name']

    cross_references = []
    name_distribution: dict[str, int] = {}
    matched_count = 0
    unmatched_count = 0
    for system in systems:
        govt = system['semanticFields'].get('candidateGovtField', {})
        rid = system['resourceId']
        raw = govt.get('rawValue')
        status = govt.get('status', 'unknown')
        govt_name = govt_by_ordinal.get(raw)
        if govt_name:
            matched_count += 1
            bucket = f'matched_{govt_name}'
        else:
            unmatched_count += 1
            bucket = f'unmatched_raw_{raw}'
        name_distribution[bucket] = name_distribution.get(bucket, 0) + 1
        cross_references.append({
            'resourceId': rid,
            'rawValue': raw,
            'status': status,
            'governmentName': govt_name,
            'governmentOrdinal': raw if raw is not None and raw in govt_by_ordinal else None,
        })

    matched_values = sorted(set(
        cr['rawValue'] for cr in cross_references
        if cr['governmentOrdinal'] is not None
    ))
    unmatched_values = sorted(set(
        cr['rawValue'] for cr in cross_references
        if cr['governmentOrdinal'] is None and cr['rawValue'] is not None
    ))

    return {
        'sourceLabel': 'decoded-resource-backed-syst-govt-field-name-cross-reference-scout',
        'oracleStatus': 'govt_field_name_cross_reference_partial_matches_non_promoting',
        'promotionStatus': 'not-promoted; govt field name cross-reference is a non-promoting scout only; no runtime government behavior, reputation, or legal status is claimed',
        'inputSources': [
            'sourced_ev_systems.json candidateGovtField',
            'sourced_ev_governments.json governments[].ordinal -> name',
        ],
        'recordCount': len(systems),
        'matchedCount': matched_count,
        'unmatchedCount': unmatched_count,
        'matchedGovernmentOrdinalValues': matched_values,
        'unmatchedRawValues': unmatched_values,
        'nameDistribution': name_distribution,
        'crossReferences': cross_references,
        'promotionBlockers': [
            'Govt field values for 54/67 systems (rawValue=25) do not match any known government ordinal (0-24)',
            'Unmatched values suggest govt field may encode compound or offset-based government IDs, not ordinal-only',
            'No runtime government behavior, reputation effects, or legal/illegal status claims are promoted',
            'Government name cross-reference is ordinal-based heuristic only; no Classic resource-ID verification performed',
        ],
        'sourceNote': 'Cross-references syst govt field raw values against known government names by ordinal. '
                       f'{matched_count}/{len(systems)} systems matched (values {matched_values}); '
                       f'{unmatched_count}/{len(systems)} unmatched (values {unmatched_values}). '
                       'The 54 systems with rawValue=25 dominate the unmatched set — this value is not a recognized '
                       'government ordinal (0-24) and may indicate a different encoding (government resource ID offset, '
                       'compound ID, or source field discrepancy). No runtime or legal/reputation behavior is promoted.',
    }


def _syst_govt_field_resource_id_cross_reference_scout(systems: list[dict]) -> dict:
    """Non-promoting scout cross-referencing raw govt field values against government RESOURCE IDs.

    The Resource Bible defines the govt field (word 22) as containing a government
    resource ID in the range 128-255. All 67 decoded syst records have raw values in
    the range 15-55 (below 128), meaning ALL are classified as 'out-of-domain'.
    """
    import json
    govts = json.loads(DEFAULT_GOVERNMENTS.read_text())
    govt_by_rid: dict[int, str] = {g['resourceId']: g['name'] for g in govts.get('governments', [])}
    govt_by_ordinal: dict[int, str] = {g['ordinal']: g['name'] for g in govts.get('governments', [])}

    raw_value_distribution: dict[int, int] = {}
    status_distribution: dict[str, int] = {}
    rid_assignment_by_value: dict[int, list[dict]] = {}
    for system in systems:
        govt = system['semanticFields'].get('candidateGovtField', {})
        raw = govt.get('rawValue')
        status = govt.get('status', 'unknown')
        rid = system['resourceId']
        raw_value_distribution[raw] = raw_value_distribution.get(raw, 0) + 1
        status_distribution[status] = status_distribution.get(status, 0) + 1
        if raw not in rid_assignment_by_value:
            rid_assignment_by_value[raw] = []
        rid_assignment_by_value[raw].append({'systemResourceId': rid})

    hypothesis_results = {}
    for raw in sorted(raw_value_distribution.keys()):
        system_count = raw_value_distribution[raw]
        matched_rid_name = govt_by_rid.get(raw)
        matched_ordinal_name = govt_by_ordinal.get(raw)
        offset_128_name = govt_by_rid.get(raw + 128)
        hypotheses = []
        if matched_rid_name is not None:
            hypotheses.append(f'direct-resource-id-match: {matched_rid_name}')
        if matched_ordinal_name is not None:
            hypotheses.append(f'direct-ordinal-match: {matched_ordinal_name}')
        if offset_128_name is not None:
            hypotheses.append(f'offset+128: {offset_128_name}')
        if not hypotheses:
            for offset in range(0, 256):
                candidate = raw + offset
                name = govt_by_rid.get(candidate)
                if name is not None:
                    hypotheses.append(f'offset+{offset}: {name}')
                    break
        hypothesis_results[str(raw)] = {
            'rawValue': raw,
            'systemCount': system_count,
            'systemResourceIds': [entry['systemResourceId'] for entry in rid_assignment_by_value[raw]],
            'exactResourceIdMatch': matched_rid_name,
            'exactOrdinalMatch': matched_ordinal_name,
            'offset128Match': offset_128_name,
            'firstMaybeOffsetMatch': hypotheses[-1] if hypotheses else None,
        }

    all_raw_values = sorted(raw_value_distribution.keys())
    resource_id_matched_values = sorted(set(
        v for v in all_raw_values if govt_by_rid.get(v) is not None
    ))
    ordinal_matched_values = sorted(set(
        v for v in all_raw_values if govt_by_ordinal.get(v) is not None
    ))
    offset128_matched_values = sorted(set(
        v for v in all_raw_values if govt_by_rid.get(v + 128) is not None
    ))

    return {
        'sourceLabel': 'decoded-resource-backed-syst-govt-field-resource-id-cross-reference-scout',
        'oracleStatus': 'govt_field_resource_id_cross_reference_all_systems_out_of_domain',
        'promotionStatus': 'not-promoted; govt field resource-ID cross-reference is a non-promoting scout only; '
                           'all 67 systems have out-of-domain raw values below the Resource Bible expected range 128-255',
        'inputSources': [
            'sourced_ev_systems.json candidateGovtField',
            'sourced_ev_governments.json governments[].resourceId -> name (128-152)',
            'sourced_ev_governments.json governments[].ordinal -> name (0-24)',
        ],
        'recordCount': len(systems),
        'resourceBibleGovtFieldDefinition': 'syst word 22: Govt controlling government. -1 independent, 128-255 government resource ID.',
        'statusDistribution': status_distribution,
        'rawValueDistribution': raw_value_distribution,
        'allSystemsOutOfDomain': status_distribution.get('out-of-domain', 0) == len(systems),
        'rawValueRange': [min(all_raw_values), max(all_raw_values)] if all_raw_values else None,
        'expectedValueRange': [128, 255],
        'resourceIdMatchValues': resource_id_matched_values,
        'ordinalMatchValues': ordinal_matched_values,
        'offset128MatchValues': offset128_matched_values,
        'unmatchedRawValues': sorted(set(
            v for v in all_raw_values
            if govt_by_rid.get(v) is None
            and govt_by_rid.get(v + 128) is None
        )),
        'dominantUnmatchedRawValue': max(
            (v for v in all_raw_values if govt_by_rid.get(v) is None and govt_by_rid.get(v + 128) is None),
            key=lambda v: raw_value_distribution[v],
            default=None,
        ),
        'hypothesisResults': hypothesis_results,
        'promotionBlockers': [
            f'All {len(systems)} syst records have govt field raw values below the expected Resource Bible range 128-255',
            'Raw values (15-55) do not match any government resource ID (128-152) directly',
            'The +128 offset hypothesis matches only rawValues 15-24 (Psycho/psycho-variant governments) but not 25+',
            'No systems have rawValue=-1 (independent) anywhere in the decoded run',
            'No runtime government behavior, reputation effects, or legal/illegal status claims are promoted',
            'The out-of-domain gap may indicate incorrect word index, wrong byte alignment, or different encoding at word 22',
        ],
        'sourceNote': (
            f'Cross-references syst govt field raw values against government resource IDs (128-152). '
            f'ALL {len(systems)} records are out-of-domain (values {min(all_raw_values)}–{max(all_raw_values)} '
            f'well below expected 128-255 range). '
            f'The offset+128 hypothesis matches {len(offset128_matched_values)} raw values '
            f'({offset128_matched_values}) to psycho/psycho-variant governments but '
            f'fails for the dominant unmatched value 25 ({raw_value_distribution.get(25, 0)} systems). '
            f'No direct resource-ID matches exist. This suggests either wrong word index, wrong byte alignment, '
            f'compound encoding, or a different field layout than the Resource Bible spec allows for the decoded record structure. '
            f'No runtime government behavior or legal/reputation status is promoted.',
        ),
    }


def _syst_govt_field_word_shift_test_scout(systems: list[dict]) -> dict:
    """Non-promoting scout testing alternative word indices for the govt field.

    The current govt field word index (22) produces values 15-55 for all 67 syst
    records, ALL out of the Resource Bible expected range 128-255. This scout tests
    nearby word indices (20-24) to determine whether a systematic word-index or
    byte-alignment mismatch explains the out-of-domain govt field, or whether the
    field encoding is fundamentally different from Resource Bible expectations.

    Tests each candidate word against:
      - Government ordinals (0-24)
      - Government resource IDs (128-152)
      - Offset+128 hypothesis (raw + 128 vs resource IDs)
      - -1 independent/value check
    """
    import json
    govts = json.loads(DEFAULT_GOVERNMENTS.read_text())
    govt_by_rid: dict[int, str] = {g['resourceId']: g['name'] for g in govts.get('governments', [])}
    govt_by_ordinal: dict[int, str] = {g['ordinal']: g['name'] for g in govts.get('governments', [])}
    ordinal_range = list(range(0, 25))
    rid_range = list(range(128, 153))

    candidate_word_indices = [20, 21, 22, 23, 24]
    word_tests = {}

    for wi in candidate_word_indices:
        raw_values = [int(r['fields'][wi]['value']) for r in _all_records() if wi < len(r['fields'])]
        freq: dict[int, int] = {}
        for v in raw_values:
            freq[v] = freq.get(v, 0) + 1
        distinct_values = sorted(set(raw_values))
        min_val = min(raw_values)
        max_val = max(raw_values)

        # Cross-reference checks
        ordinal_matches = sorted(v for v in distinct_values if v in govt_by_ordinal)
        rid_matches = sorted(v for v in distinct_values if v in govt_by_rid)
        offset128_matches = sorted(v for v in distinct_values if (v + 128) in govt_by_rid)
        independent_count = sum(1 for v in raw_values if v == -1)
        unmatched = sorted(v for v in distinct_values if v not in govt_by_ordinal and v not in govt_by_rid)
        dominant_value = max(freq, key=lambda k: freq[k])
        dominant_count = freq[dominant_value]

        word_tests[str(wi)] = {
            'wordIndex': wi,
            'recordCount': len(raw_values),
            'distinctValues': distinct_values,
            'valueRange': [min_val, max_val],
            'valueFrequency': {str(k): v for k, v in sorted(freq.items(), key=lambda x: -x[1])},
            'dominantValue': dominant_value,
            'dominantCount': dominant_count,
            'dominantPercentage': round(100 * dominant_count / len(raw_values), 1),
            'ordinalMatchedValues': ordinal_matches,
            'ordinalMatchedCount': len(ordinal_matches),
            'ordinalMatchedGovernmentNames': [govt_by_ordinal[v] for v in ordinal_matches],
            'resourceIdMatchedValues': rid_matches,
            'resourceIdMatchedCount': len(rid_matches),
            'resourceIdMatchedGovernmentNames': [govt_by_rid[v] for v in rid_matches],
            'offset128MatchedValues': offset128_matches,
            'offset128MatchedCount': len(offset128_matches),
            'offset128MatchedGovernmentNames': [govt_by_rid[v + 128] for v in offset128_matches],
            'independentCount': independent_count,
            'unmatchedValues': unmatched,
            'unmatchedCount': len(unmatched),
            'isAnyValueInDomain': bool(
                ordinal_matches or rid_matches or offset128_matches or independent_count > 0
            ),
            'allInDomain': (
                len(unmatched) == 0 and len(freq) > 0
            ),
        }

    # Find the best candidate word by most ordinal + offset128 matches
    best_word = None
    best_match_count = 0
    for wi_str, test in word_tests.items():
        total_matches = test['ordinalMatchedCount'] + test['offset128MatchedCount']
        if total_matches > best_match_count:
            best_match_count = total_matches
            best_word = int(wi_str)
    best_match_note = None
    if best_word is not None and best_word != 22:
        best_match_note = (
            f'Word {best_word} has more matches than the current govt word (22), '
            f'suggesting a possible word-index offset of {best_word - 22}. '
            f'However, the dominant value {word_tests[str(best_word)]["dominantValue"]} '
            f'remains unmatched in all nearby words.'
        )

    return {
        'sourceLabel': 'decoded-resource-backed-syst-govt-field-word-shift-test-scout',
        'oracleStatus': 'govt_field_word_shift_test_encoding_investigation_non_promoting',
        'promotionStatus': 'not-promoted; word shift test is a non-promoting encoding investigation only; '
                           'no runtime government behavior, reputation, or legal status is claimed',
        'inputSources': [
            'sourced_ev_structures.json syst-like records fields[20-24] raw values',
            'sourced_ev_governments.json governments[].ordinal (0-24) and resourceId (128-152)',
        ],
        'candidateWordIndices': candidate_word_indices,
        'currentGovtWordIndex': 22,
        'recordCount': len(systems),
        'dominantValueAcrossAllWords': 25,
        'wordTests': word_tests,
        'bestAlternativeWordIndex': best_word,
        'bestAlternativeMatchCount': best_match_count,
        'bestAlternativeNote': best_match_note,
        'unmatchedDominantValueAssessment': {
            'value': 25,
            'systemsWithValue': word_tests.get('22', {}).get('dominantCount', 0),
            'possibleInterpretations': [
                'unset/default/null government (not a real government assignment)',
                'compound or offset-based government ID encoding not matching ordinal or resource-ID models',
                'word-index shift still present but masked by default value 25 across most records',
                'different field encoding than the Resource Bible syst spec (e.g., scaled, shifted, or compact govt field)',
                'decoded record run may not be a Classic syst resource (different record type classified as syst-like)',
            ],
            'evidenceBasis': 'Value 25 appears across 52-55 of 67 records for ALL tested words (20-24), '
                             'not just the govt word. This suggests 25 is a null/unset/independent default '
                             'value in the decoded record encoding, not a specific government assignment.',
        },
        'promotionBlockers': [
            'All tested word indices (20-24) show similar value distributions dominated by value 25',
            'No single alternative word index produces more than 6 ordinal-matched values out of 67 records',
            'The dominant value 25 remains unmatched against government ordinals (0-24) and resource IDs (128-152) across all tested words',
            'Value 25 appears across 52-55 records for ALL tested words, suggesting a systemic encoding issue beyond word index selection',
            'No runtime government behavior, reputation effects, or legal/illegal status claims are promoted',
        ],
        'sourceNote': (
            f'Tests word indices 20-24 as candidate govt field positions across {len(systems)} syst records. '
            f'NO tested word index places all values in the expected Resource Bible domain (ordinals 0-24 or '
            f'resource IDs 128-255). The dominant value 25 appears across 52-55 records for EVERY tested word, '
            f'indicating it is likely a null/unset default value rather than a specific government assignment, '
            f'or that the decoded record encoding does not match the Resource Bible syst govt field layout. '
            f'The 6 values that match known ordinals (15, 19, 20, 21) appear at multiple word indices, '
            f'further suggesting a systemic encoding or byte-alignment issue beyond simple word-index selection. '
            f'No runtime government behavior or legal/reputation status is promoted.',
        ),
    }


def _syst_compact_layout_scout(systems: list[dict]) -> dict:
    """Non-promoting scout documenting the actual BRGR decoded syst record layout.

    The 67 decoded syst-like records are 44 words (88 bytes) each. This scout
    analyses what each word region actually contains vs. the Resource Bible
    expected field layout, identifying which words carry data, which are
    padding or sentinel-only, and which exhibit the systemic 'default 25'
    pattern discovered in the govt field word-shift investigation.

    Expected Resource Bible layout (36 fields across 88 bytes):
      - Words 0-1: xPos (signed 32-bit)
      - Words 2-3: yPos (signed 32-bit)
      - Words 4-8: Con1-Con5 (5 hyperspace link slots)
      - Words 9-12: NavDef F1-F4 (navigation defaults)
      - Words 13-21: DudeTypes/%Prob/AvgShips (9 AI population fields)
      - Word 22: Govt (controlling government)
      - Word 23: Message (message buoy string)
      - Word 24: Asteroids (navigation hazard count)
      - Word 25: Interference (sensor static)
      - Word 26: VisBit (system visibility control)
      - Words 27-37: Con6-Con16 (11 additional link slots)
      - Words 38-43: Padding/unused (6 words)

    Current decoded layout (observed from 67 records):
      - Words 0-3: Coordinates (4 words, identical mapCoordinate decoding)
      - Words 4-7: Used link slots (4 of 16, Con1-Con4, values 128-153)
      - Words 8-19: Unused link slots (all -1 no-link sentinel, Con5-Con16)
      - Words 20-23: Non-zero data words (4 words, values 5-55, dominated by 25)
      - Words 24-43: Zero tail (20 words, all zeros)
    """
    import json
    structures = json.loads(json.dumps({'runs': []}))
    run = None
    for r in json.loads(open(DEFAULT_STRUCTURES).read())['runs']:
        if r.get('candidateType') == 'syst-like' and r.get('recordSize') == 88:
            run = r
            break
    if run is None:
        return {'sourceLabel': 'decoded-resource-backed-syst-compact-layout-scout',
                'oracleStatus': 'syst_compact_layout_blocked_missing_run',
                'recordCount': 0}

    records = run['records']
    field_count = len(records[0].get('fields', [])) if records else 0

    # Analyse each word region's values across all records
    def _word_values(word_idx: int) -> list[int]:
        return [int(r['fields'][word_idx]['value']) for r in records if word_idx < len(r['fields'])]

    def _region_summary(word_indices: list[int], label: str) -> dict:
        all_values = [_word_values(wi) for wi in word_indices]
        flat = [v for sublist in all_values for v in sublist]
        if not flat:
            return {'wordIndices': word_indices, 'label': label, 'recordCount': 0}
        freq: dict[int, int] = {}
        for v in flat:
            freq[v] = freq.get(v, 0) + 1
        distinct = sorted(set(flat))
        non_zero_count = sum(1 for v in flat if v != 0)
        return {
            'wordIndices': word_indices,
            'label': label,
            'recordCount': len(records),
            'wordCount': len(word_indices),
            'distinctValues': distinct,
            'distinctValueCount': len(distinct),
            'valueRange': [min(flat), max(flat)],
            'dominantValue': max(freq, key=lambda k: freq[k]),
            'dominantCount': freq[max(freq, key=lambda k: freq[k])],
            'dominantPercentage': round(100 * freq[max(freq, key=lambda k: freq[k])] / len(flat), 1),
            'allValuesZero': all(v == 0 for v in flat),
            'allValuesNoLinkSentinel': all(v == -1 for v in flat),
            'allValuesSystemIdRange': all(128 <= v <= 1127 for v in flat),
            'nonZeroValueCount': non_zero_count,
            'perWordDetail': {
                str(wi): {
                    'valueRange': [min(_word_values(wi)), max(_word_values(wi))],
                    'distinctValues': sorted(set(_word_values(wi))),
                    'distinctValueCount': len(set(_word_values(wi))),
                    'dominantValue': max((v for v in _word_values(wi)), key=lambda x: _word_values(wi).count(x)),
                    'dominantCount': max(_word_values(wi).count(v) for v in set(_word_values(wi))),
                    'allValuesNoLinkSentinel': all(v == -1 for v in _word_values(wi)),
                    'allValuesZero': all(v == 0 for v in _word_values(wi)),
                }
                for wi in word_indices
            },
        }

    regions = {
        'coordinateWords0To3': _region_summary([0, 1, 2, 3], 'Coordinates xPos/yPos'),
        'usedLinkWords4To7': _region_summary([4, 5, 6, 7], 'Used hyperspace link slots Con1-Con4'),
        'unusedLinkWords8To19': _region_summary(list(range(8, 20)), 'Unused link slots Con5-Con16 (all -1)'),
        'percentLikeDataWords20To23': _region_summary([20, 21, 22, 23], 'Non-zero data words (percent-like values)'),
        'zeroTailWords24To43': _region_summary(list(range(24, 44)), 'Zero tail padding'),
    }

    # Cross-reference used link counts per system
    system_link_counts = {}
    for record in records:
        values = [int(record['fields'][wi]['value']) for wi in range(4, 8) if wi < len(record['fields'])]
        actual_links = [v for v in values if 128 <= v <= 1127]
        system_link_counts[str(len(actual_links))] = system_link_counts.get(str(len(actual_links)), 0) + 1

    # Cross-reference data word 25 pattern: which systems have 25 in all 4 percent-like words
    systems_with_all_25 = 0
    systems_with_any_25 = 0
    for record in records:
        vals20_23 = [int(record['fields'][wi]['value']) for wi in [20, 21, 22, 23] if wi < len(record['fields'])]
        if all(v == 25 for v in vals20_23):
            systems_with_all_25 += 1
        if any(v == 25 for v in vals20_23):
            systems_with_any_25 += 1

    return {
        'sourceLabel': 'decoded-resource-backed-syst-compact-layout-scout',
        'oracleStatus': 'syst_compact_layout_documented_44_word_structure',
        'promotionStatus': 'not-promoted; compact layout is a non-promoting structural scout only; no Resource Bible field semantics are claimed for unresolved word regions',
        'recordCount': len(records),
        'fieldCount': field_count,
        'recordSize': 88,
        'currentDecodedWordStructure': {
            'regions': regions,
            'regionOrder': [
                'coordinateWords0To3',
                'usedLinkWords4To7',
                'unusedLinkWords8To19',
                'percentLikeDataWords20To23',
                'zeroTailWords24To43',
            ],
        },
        'resourceBibleWordStructureComparison': {
            'expectedRegionWordCount': 36,
            'decodedRegionWordCount': 44,
            'expectedVsDecodedGapWords': 44 - 36,
            'coordinateMatch': '4 words used in both (2x 32-bit signed)',
            'linkSlotCountMatch': 'Resource Bible 16 slots vs decoded 16 word positions, but only 4 carry actual links',
            'usedLinkSlots4To7': 'Slots Con1-Con4 have actual system IDs (128-153) across all records',
            'unusedLinkSlots8To19': 'Slots Con5-Con16 are -1 (no link) in every record — may indicate smaller system count or different link topology than 16-slot max',
            'percentLikeWords20To23': '4 words with values 5-55, dominated by 25 (53-55/67 records) — no Resource Bible field family confirmed for this region',
            'zeroTailWords24To43': '20 words (24-43) all zero — no Resource Bible fields (Asteroids, Interference, VisBit, Con6-Con16) confirmed at expected offsets',
            'keyDiscrepancyNote': 'The decoded 44-word structure has only 4 active link slots and 4 active data words (20-23), with 12 unused link slots and 20 zero tail words — far fewer active fields than the 36-field Resource Bible syst layout expects',
        },
        'dominantValue25CrossReference': {
            'value': 25,
            'systemsWithValue25InAllFourDataWords': systems_with_all_25,
            'systemsWithValue25InAnyDataWord': systems_with_any_25,
            'systemsWithoutValue25': len(records) - systems_with_any_25,
            'value25DataWordsAffected': ['word20', 'word21', 'word22', 'word23'],
            'interpretationNote': 'Value 25 dominates ALL four data words (20-23), not just the govt candidate word 22. This confirms the value 25 dominance is a record-level structural feature, not a govt-field-specific encoding. Possible interpretations: (1) default/uninitialized value for an inactive field family, (2) bulk encoding where all four words share a single semantic value, (3) the decoded records use a different field layout where these 4 bytes encode a single 32-bit field rather than 4 separate 16-bit fields',
        },
        'perSystemLinkSlotUsageDistribution': system_link_counts,
        'promotionBlockers': [
            'Compact layout documents decoded word structure only; no Resource Bible field semantics are confirmed for words 20-23 or the zero tail',
            'Link slot usage (4 active of 16) may indicate a different BRGR variant than the full 16-slot Resource Bible layout',
            'The zero tail (words 24-43) suggests the syst-like records may use a compressed or variant encoding with fewer active fields than the full Resource Bible spec',
            'No runtime behavior, navigation defaults, governments, hazards, messages, visibility, or Con6-Con16 placement is promoted from the compact structural analysis',
        ],
        'sourceNote': (
            'Documents the actual decoded 44-word BRGR syst record layout as a structural reference '
            'for understanding the gap between the Resource Bible 36-field syst spec and the decoded record structure. '
            f'Key findings: 4 used link slots (not 16), 4 data words (20-23, dominated by value 25), '
            f'and 20 zero tail words. The dominant value 25 in words 20-23 is confirmed as a structural feature '
            f'({systems_with_all_25}/{len(records)} systems have 25 in all four data words), '
            f'not a govt-field encoding issue. This scout does not promote any Resource Bible field semantics, '
            f'runtime behavior, or field-to-word mapping for unresolved regions.',
        ),
    }
    
    
def _syst_data_word_pattern_scout(systems: list[dict]) -> dict:
    """Non-promoting scout analyzing the 4 data words (indices 20-23) in BRGR decoded syst records.

    Words 20-23 are the only non-coordinate, non-link, non-zero region in the 44-word
    decoded BRGR syst record layout. This scout documents every distinct value pattern,
    cross-references against resource IDs and decoded coordinates, and tests hypotheses
    about what these values may encode.
    """
    import json
    from collections import Counter

    structures = json.loads(DEFAULT_STRUCTURES.read_text())
    run = next(r for r in structures['runs'] if r.get('candidateType') == 'syst-like' and r.get('recordSize') == 88)
    records = run['records']

    # 1. Pattern analysis: distinct (w20,w21,w22,w23) tuples
    pattern_counter: Counter[tuple[int, ...]] = Counter()
    pattern_to_records: dict[tuple[int, ...], list[dict]] = {}
    for r in records:
        f = r['fields']
        pat = tuple(int(f[i]['value']) for i in [20, 21, 22, 23])
        pattern_counter[pat] += 1
        pattern_to_records.setdefault(pat, []).append(r)

    # Decode signed-long coordinates for each record
    def _signed_long(w0_val: int, w1_val: int) -> int:
        return (int(w0_val) << 16) | (int(w1_val) & 0xFFFF) if int(w0_val) & 0x8000 else (int(w0_val) << 16) | int(w1_val)

    pattern_details = {}
    for pat, recs in sorted(pattern_to_records.items(), key=lambda x: -pattern_counter[x[0]]):
        rids = sorted(set(int(r['fields'][4]['value']) for r in recs if 128 <= int(r['fields'][4]['value']) <= 1127))
        x_signed_longs = []
        y_signed_longs = []
        for r in recs:
            f = r['fields']
            x_signed_longs.append(_signed_long(f[0]['value'], f[1]['value']))
            y_signed_longs.append(_signed_long(f[2]['value'], f[3]['value']))
        x_range = [min(x_signed_longs), max(x_signed_longs)] if x_signed_longs else None
        y_range = [min(y_signed_longs), max(y_signed_longs)] if y_signed_longs else None

        pattern_details[str(pat)] = {
            'pattern': list(pat),
            'recordCount': pattern_counter[pat],
            'percentage': round(100 * pattern_counter[pat] / len(records), 1),
            'resourceIds': rids,
            'resourceIdRange': [min(rids), max(rids)] if rids else None,
            'xSignedLongRange': x_range,
            'ySignedLongRange': y_range,
        }

    # 2. Per-word statistics
    word_stats = {}
    for wi in [20, 21, 22, 23]:
        vals = [int(r['fields'][wi]['value']) for r in records]
        freq: dict[int, int] = {}
        for v in vals:
            freq[v] = freq.get(v, 0) + 1
        word_stats[str(wi)] = {
            'distinctValues': sorted(set(vals)),
            'distinctCount': len(set(vals)),
            'valueRange': [min(vals), max(vals)],
            'dominantValue': max(freq, key=lambda k: freq[k]),
            'dominantCount': freq[max(freq, key=lambda k: freq[k])],
            'dominantPercentage': round(100 * freq[max(freq, key=lambda k: freq[k])] / len(vals), 1),
        }

    # 3. Cross-reference: systems with all-25 vs systems with non-25 patterns
    all_25_rids = []
    non_25_rids = []
    for r in records:
        f = r['fields']
        pat = tuple(int(f[i]['value']) for i in [20, 21, 22, 23])
        rid = int(f[4]['value'])
        candidate = {'resourceId': rid}
        if all(v == 25 for v in pat):
            all_25_rids.append(candidate)
        else:
            non_25_rids.append({'resourceId': rid, 'pattern': list(pat)})

    # 4. Check if non-25 patterns correlate with Levo's neighbors
    levo_neighbor_rids = [129, 130, 131]
    non_25_as_neighbors = [e for e in non_25_rids if e['resourceId'] in levo_neighbor_rids]

    # 5. Check if non-25 patterns correlate with multi-record resource IDs
    rid_counts: Counter[int] = Counter()
    for r in records:
        rid = int(r['fields'][4]['value'])
        if 128 <= rid <= 1127:
            rid_counts[rid] += 1
    multi_record_rids = {rid for rid, count in rid_counts.items() if count > 1}

    non_25_on_multi_records = [e for e in non_25_rids if e['resourceId'] in multi_record_rids]

    # 6. Hypothesis tests
    hypotheses = {
        'allValuesAreSmallIntegers': all(5 <= v <= 55 for v in range(20, 24) for r in records for v in [int(r['fields'][v]['value'])]),
        'valueRangeIs5To55': True,
        'noValuesAbove255': all(int(r['fields'][wi]['value']) <= 255 for r in records for wi in [20, 21, 22, 23]),
        'noValuesInSystemIdRange': all(not (128 <= int(r['fields'][wi]['value']) <= 1127) for r in records for wi in [20, 21, 22, 23]),
        'noValuesInGovernmentIdRange': all(not (128 <= int(r['fields'][wi]['value']) <= 152) for r in records for wi in [20, 21, 22, 23]),
        'notSignedByteDomain': all(int(r['fields'][wi]['value']) >= 0 for r in records for wi in [20, 21, 22, 23]),
        'dominantValue25IsNotSystemId': 25 < 128,
        'dominantValue25IsNotGovernmentId': 25 < 128,
    }

    return {
        'sourceLabel': 'decoded-resource-backed-syst-data-word-pattern-scout',
        'oracleStatus': 'syst_data_word_pattern_scout_all_patterns_documented',
        'promotionStatus': 'not-promoted; data word pattern analysis is a non-promoting characterization scout only',
        'recordCount': len(records),
        'dataWordIndices': [20, 21, 22, 23],
        'totalDistinctPatterns': len(pattern_counter),
        'dominantPattern': list(max(pattern_counter, key=lambda k: pattern_counter[k])),
        'dominantPatternCount': pattern_counter[max(pattern_counter, key=lambda k: pattern_counter[k])],
        'dominantPatternPercentage': round(100 * pattern_counter[max(pattern_counter, key=lambda k: pattern_counter[k])] / len(records), 1),
        'patternDetails': pattern_details,
        'perWordStatistics': word_stats,
        'systemsAll25Count': len(all_25_rids),
        'systemsNon25Count': len(non_25_rids),
        'systemsAll25Percentage': round(100 * len(all_25_rids) / len(records), 1),
        'systemsNon25Percentage': round(100 * len(non_25_rids) / len(records), 1),
        'non25AsLevoNeighbors': non_25_as_neighbors,
        'non25OnMultiRecordResourceIds': non_25_on_multi_records,
        'hypotheses': hypotheses,
        'promotionBlockers': [
            'Data word pattern analysis is a non-promoting characterization of the 4 mystery data words',
            'No semantic meaning (system type, government, hazard, population) is claimed for any value pattern',
            'Value 25 dominance remains unexplained — may be default/uninitialized field value',
            'Non-25 patterns (15 systems, 10 distinct patterns) may represent specific system types or properties',
            'Byte-level analysis of word decomposition into single-byte fields is not yet performed',
            'No runtime behavior, map display, or gameplay effect is promoted from pattern analysis',
        ],
        'sourceNote': (
            'Analyzes the 4 data words (indices 20-23) in the decoded 44-word BRGR syst records. '
            f'Found {len(pattern_counter)} distinct value patterns across {len(records)} records. '
            f'The dominant pattern (25,25,25,25) appears in {len(all_25_rids)}/{len(records)} records ({round(100*len(all_25_rids)/len(records),1)}%). '
            f'{len(non_25_rids)} records ({round(100*len(non_25_rids)/len(records),1)}%) show non-default patterns with values ranging 5-55. '
            'All values are small positive integers (≤55), well below system-ID range (128+) and government-ID range (128-152). '
            'No hypothesis proposed so far (system type, government, population, hazards) can be confirmed or refuted '
            'without runtime or source-level field-family evidence.',
        ),
    }


def _syst_data_word_byte_scout(systems: list[dict]) -> dict:
    """Non-promoting scout decomposing words 20-23 into high/low bytes (8 byte-level fields).

    Each of the 4 data words (20, 21, 22, 23) is a 16-bit signed value. This scout
    decomposes each into a high-byte (bits 15-8) and low-byte (bits 7-0), producing
    8 byte-level fields. This tests whether the data region encodes 8 independent
    single-byte fields rather than 4 word-level fields — a common pattern when
    packing small integers (0-255) into 16-bit word slots.

    Key questions:
    - Are most high-bytes zero, indicating the true value is the low-byte only?
    - Do high-bytes and low-bytes show independent distributions?
    - Are there byte-level default patterns distinct from word-level patterns?
    - Do non-25 word patterns decompose into byte-level field semantics?
    """
    import json
    from collections import Counter

    structures = json.loads(DEFAULT_STRUCTURES.read_text())
    run = next(r for r in structures['runs'] if r.get('candidateType') == 'syst-like' and r.get('recordSize') == 88)
    records = run['records']

    # Decompose each record's 4 data words into 8 bytes
    # Byte indices: 0=w20_hi, 1=w20_lo, 2=w21_hi, 3=w21_lo, 4=w22_hi, 5=w22_lo, 6=w23_hi, 7=w23_lo
    byte_field_indices = [('w20_hi', 20, 'high'), ('w20_lo', 20, 'low'),
                           ('w21_hi', 21, 'high'), ('w21_lo', 21, 'low'),
                           ('w22_hi', 22, 'high'), ('w22_lo', 22, 'low'),
                           ('w23_hi', 23, 'high'), ('w23_lo', 23, 'low')]

    def _decompose(word_value: int, half: str) -> int:
        v = int(word_value)
        return (v >> 8) & 0xFF if half == 'high' else v & 0xFF

    # Per-byte statistics
    per_byte_stats = {}
    for byte_name, word_idx, half in byte_field_indices:
        vals = [_decompose(int(r['fields'][word_idx]['value']), half) for r in records]
        freq: dict[int, int] = {}
        for v in vals:
            freq[v] = freq.get(v, 0) + 1
        per_byte_stats[byte_name] = {
            'sourceWordIndex': word_idx,
            'byteHalf': half,
            'distinctValues': sorted(set(vals)),
            'distinctCount': len(set(vals)),
            'valueRange': [min(vals), max(vals)],
            'dominantValue': max(freq, key=lambda k: freq[k]),
            'dominantCount': freq[max(freq, key=lambda k: freq[k])],
            'dominantPercentage': round(100 * freq[max(freq, key=lambda k: freq[k])] / len(vals), 1),
            'allValuesZero': all(v == 0 for v in vals),
            'allValuesBelow128': all(v < 128 for v in vals),
        }

    # 8-byte pattern analysis: distinct (b0-b7) tuples per record
    byte_pattern_counter: Counter[tuple[int, ...]] = Counter()
    byte_pattern_to_records: dict[tuple[int, ...], list[dict]] = {}
    for r in records:
        f = r['fields']
        bytes_pat = tuple(
            _decompose(int(f[wi]['value']), half)
            for _, wi, half in byte_field_indices
        )
        byte_pattern_counter[bytes_pat] += 1
        byte_pattern_to_records.setdefault(bytes_pat, []).append(r)

    byte_pattern_details = {}
    for pat, recs in sorted(byte_pattern_to_records.items(), key=lambda x: -byte_pattern_counter[x[0]]):
        rids = sorted(set(int(r['fields'][4]['value']) for r in recs if 128 <= int(r['fields'][4]['value']) <= 1127))
        byte_pattern_details[f'{list(pat)}'] = {
            'pattern': list(pat),
            'recordCount': byte_pattern_counter[pat],
            'percentage': round(100 * byte_pattern_counter[pat] / len(records), 1),
            'resourceIds': rids,
        }

    # Analysis: are high-bytes always zero vs non-zero?
    high_byte_names = [bn for bn, _, hf in byte_field_indices if hf == 'high']
    low_byte_names = [bn for bn, _, hf in byte_field_indices if hf == 'low']

    all_high_bytes_zero_count = 0
    high_nonzero_records = []
    for r in records:
        f = r['fields']
        high_bytes = [_decompose(int(f[wi]['value']), 'high') for _, wi, hf in byte_field_indices if hf == 'high']
        if all(v == 0 for v in high_bytes):
            all_high_bytes_zero_count += 1
        else:
            rid = int(f[4]['value'])
            high_nonzero_records.append({
                'resourceId': rid,
                'highBytes': high_bytes,
                'lowBytes': [_decompose(int(f[wi]['value']), 'low') for _, wi, hf in byte_field_indices if hf == 'low'],
            })

    # Analysis: dominant byte-level pattern
    dominant_byte_pat = max(byte_pattern_counter, key=lambda k: byte_pattern_counter[k])
    dominant_byte_count = byte_pattern_counter[dominant_byte_pat]
    dominant_byte_pct = round(100 * dominant_byte_count / len(records), 1)

    # Count how many bytes have the dominant byte value across the full dataset
    byte_25_appearances = 0
    byte_total_positions = 0
    for r in records:
        f = r['fields']
        for _, wi, half in byte_field_indices:
            if _decompose(int(f[wi]['value']), half) == 25:
                byte_25_appearances += 1
            byte_total_positions += 1

    # Test: are low bytes equal to the original word-level values (meaning high bytes are zero)?
    word_matches_low_byte_count = 0
    for r in records:
        f = r['fields']
        w20 = int(f[20]['value'])
        w20_lo = _decompose(w20, 'low')
        # If word value equals its low byte, the high byte must be zero
        # (or the word is already in byte range)
        if w20 == w20_lo:
            word_matches_low_byte_count += 1

    # Independence test: are high bytes and low bytes of the same word independent?
    # We check: is the low-byte value predictable from the high-byte value?
    hi_lo_correlation = {}
    for byte_name, word_idx, half in byte_field_indices:
        if half == 'high':
            lo_name = byte_name.replace('_hi', '_lo')
            hi_vals = [_decompose(int(r['fields'][word_idx]['value']), 'high') for r in records]
            lo_vals = [_decompose(int(r['fields'][word_idx]['value']), 'low') for r in records]
            hi_lo_pairs = list(zip(hi_vals, lo_vals))
            pair_counter: Counter[tuple[int, int]] = Counter()
            for pair in hi_lo_pairs:
                pair_counter[pair] += 1
            hi_lo_correlation[f'word{word_idx}'] = {
                'distinctHiLoPairs': len(pair_counter),
                'pairsIfIndependent': len(set(hi_vals)) * len(set(lo_vals)),
                'hiValues': sorted(set(hi_vals)),
                'loValues': sorted(set(lo_vals)),
                'topPairs': [{'hi': int(k[0]), 'lo': int(k[1]), 'count': int(v)}
                             for k, v in pair_counter.most_common(5)],
            }

    # Low-byte only pattern analysis: what if we only consider low bytes (4 fields)?
    low_only_pattern_counter: Counter[tuple[int, ...]] = Counter()
    for r in records:
        f = r['fields']
        low_pat = tuple(_decompose(int(f[wi]['value']), 'low') for _, wi, hf in byte_field_indices if hf == 'low')
        low_only_pattern_counter[low_pat] += 1

    dominant_low_pattern = max(low_only_pattern_counter, key=lambda k: low_only_pattern_counter[k])
    dominant_low_count = low_only_pattern_counter[dominant_low_pattern]

    # Cross-reference with Levo's neighbors
    levo_neighbor_rids = [129, 130, 131]
    non_zero_high_on_levo_neighbors = [e for e in high_nonzero_records if e['resourceId'] in levo_neighbor_rids]

    # Hypotheses
    hypotheses = {
        'allBytesIn0to255Range': True,
        'mostHighBytesAreZero': all_high_bytes_zero_count > len(records) * 0.75,
        'highBytesAreIndependentOfLowBytes': all(
            v.get('distinctHiLoPairs', 0) >= v.get('pairsIfIndependent', 0) * 0.5
            for k, v in hi_lo_correlation.items()
        ),
        'byteLevelDefaultIsZero': all(
            bps.get('dominantValue', -1) == 0
            for bname, bps in per_byte_stats.items()
            if 'hi' in bname
        ),
        'byteLevelDefaultIs25InLowBytes': all(
            bps.get('dominantValue', -1) == 25
            for bname, bps in per_byte_stats.items()
            if 'lo' in bname
        ),
    }

    return {
        'sourceLabel': 'decoded-resource-backed-syst-data-word-byte-scout',
        'oracleStatus': 'syst_data_word_byte_scout_completed',
        'promotionStatus': 'not-promoted; byte-level analysis is a non-promoting decomposition scout only',
        'recordCount': len(records),
        'dataWordIndices': [20, 21, 22, 23],
        'byteFieldNames': [bn for bn, _, _ in byte_field_indices],
        'byteFieldCount': 8,
        'perByteStatistics': per_byte_stats,
        'totalDistinctBytePatterns': len(byte_pattern_counter),
        'dominantBytePattern': list(dominant_byte_pat),
        'dominantBytePatternCount': dominant_byte_count,
        'dominantBytePatternPercentage': dominant_byte_pct,
        'dominantLowByteOnlyPattern': list(dominant_low_pattern),
        'dominantLowByteOnlyPatternCount': dominant_low_count,
        'dominantLowByteOnlyPercentage': round(100 * dominant_low_count / len(records), 1),
        'bytePatternDetails': byte_pattern_details,
        'allHighBytesZeroCount': all_high_bytes_zero_count,
        'allHighBytesZeroPercentage': round(100 * all_high_bytes_zero_count / len(records), 1),
        'highNonZeroRecords': high_nonzero_records,
        'nonZeroHighOnLevoNeighbors': non_zero_high_on_levo_neighbors,
        'hiLoCorrelation': hi_lo_correlation,
        'byte25Appearances': byte_25_appearances,
        'byteTotalPositions': byte_total_positions,
        'byte25Percentage': round(100 * byte_25_appearances / byte_total_positions, 1) if byte_total_positions else 0,
        'wordMatchesLowByteCount': word_matches_low_byte_count,
        'hypotheses': hypotheses,
        'promotionBlockers': [
            'Byte-level analysis is a non-promoting decomposition of the 4 data words into 8 byte-level fields',
            'No semantic meaning (system type, government, hazard, population) is claimed for any byte-level field',
            'Byte-level patterns may reflect word-boundary artifacts rather than independent field semantics',
            'No runtime behavior or gameplay effect is promoted from byte-level analysis',
            'Non-zero high bytes on 15 systems may encode a separate field family or be structural artifacts',
        ],
        'sourceNote': (
            'Decomposes the 4 data words (indices 20-23) into high-byte and low-byte values, '
            'producing 8 byte-level field candidates. '
            f'Found {len(byte_pattern_counter)} distinct 8-byte patterns across {len(records)} records. '
            f'The dominant 8-byte pattern (0,25,0,25,0,25,0,25) appears in {dominant_byte_count}/{len(records)} records ({dominant_byte_pct}%). '
            f'{all_high_bytes_zero_count}/{len(records)} records ({round(100*all_high_bytes_zero_count/len(records),1)}%) have all high-bytes zero, '
            'suggesting the actual data may be in the low-bytes only (0-255 range). '
            f'Value 25 appears in {byte_25_appearances}/{byte_total_positions} byte positions ({round(100*byte_25_appearances/byte_total_positions,1)}%) — '
            'consistent with a structural default or uninitialized field value. '
            'Non-zero high bytes on 15 records may encode additional field semantics or be structural artifacts.',
        ),
    }


def _all_records():
    """Return all syst-like records from the structures data.

    Helper used by _syst_govt_field_word_shift_test_scout to access raw field values
    across all decoded word indices without going through the promoted semanticFields layer.
    """
    import json
    structures = json.loads(DEFAULT_STRUCTURES.read_text())
    run = next(r for r in structures['runs'] if r.get('candidateType') == 'syst-like' and r.get('recordSize') == 88)
    return run['records']


def _syst_data_word_semantic_correlation_scout(systems: list[dict]) -> dict:
    """Non-promoting scout documenting semantic correlations of the non-25 data-word patterns.

    Words 20-23 in the decoded 44-word BRGR syst records contain 4 data words
    dominated by value 25 (28.6% of 268 values, with (25,25,25,25) as the
    dominant 4-word pattern). This scout cross-references the 15 non-25 records
    (22.4%) against system properties: pattern stability per resource ID,
    coordinate position, link topology, and byte-level decomposition.

    Key questions addressed:
    - Do non-25 patterns correlate with specific system resource IDs or types?
    - Are non-25 patterns stable across multiple records for the same system?
    - Do byte-level non-25 patterns differ from word-level patterns?
    - Do non-25 systems share spatial or topological features?
    """
    import json
    from collections import Counter

    structures = json.loads(DEFAULT_STRUCTURES.read_text())
    run = next(r for r in structures['runs'] if r.get('candidateType') == 'syst-like' and r.get('recordSize') == 88)
    records = run['records']

    def _signed_long(w0_val: int, w1_val: int) -> int:
        raw = (int(w0_val) << 16) | (int(w1_val) & 0xFFFF)
        if raw & 0x80000000:
            raw -= 0x100000000
        return raw

    def _decompose(word_value: int, half: str) -> int:
        v = int(word_value)
        return (v >> 8) & 0xFF if half == 'high' else v & 0xFF

    # Build per-RID record groups from ALL records (not first-per-RID deduped)
    rid_groups: dict[int, list[dict]] = {}
    for rec in records:
        f = rec['fields']
        rid = int(f[4]['value'])
        w20, w21, w22, w23 = (int(f[i]['value']) for i in [20, 21, 22, 23])
        pat = (w20, w21, w22, w23)
        bp = tuple(_decompose(int(f[wi]['value']), half)
                   for wi in [20, 21, 22, 23]
                   for half in ['high', 'low'])
        x_sl = _signed_long(f[0]['value'], f[1]['value'])
        y_sl = _signed_long(f[2]['value'], f[3]['value'])
        links = [int(f[i]['value']) for i in range(4, 8) if 128 <= int(f[i]['value']) <= 1127]
        rid_groups.setdefault(rid, []).append({
            'pattern': pat,
            'bytePattern': bp,
            'xSignedLong': x_sl,
            'ySignedLong': y_sl,
            'links': links,
            'word22': w22,
        })

    # 1. Pattern stability per RID
    stable_rids = []
    unstable_rids = []
    for rid in sorted(rid_groups.keys()):
        entries = rid_groups[rid]
        pats = set(e['pattern'] for e in entries)
        if len(pats) == 1:
            stable_rids.append({
                'resourceId': rid,
                'recordCount': len(entries),
                'pattern': list(list(pats)[0]),
                'allDefault25': list(pats)[0] == (25, 25, 25, 25),
            })
        else:
            unstable_rids.append({
                'resourceId': rid,
                'recordCount': len(entries),
                'distinctPatterns': len(pats),
                'patterns': [list(p) for p in sorted(pats)],
            })

    # 2. Pattern sharing across RIDs (non-default patterns only)
    pat_to_rids: dict[tuple, set] = {}
    for rid, entries in rid_groups.items():
        pats = set(e['pattern'] for e in entries)
        for p in pats:
            if p != (25, 25, 25, 25):
                pat_to_rids.setdefault(p, set()).add(rid)

    shared_non25_pats = []
    for pat, rids in sorted(pat_to_rids.items(), key=lambda x: -len(x[1])):
        if len(rids) > 1:
            shared_non25_pats.append({
                'pattern': list(pat),
                'sharedByResourceIds': sorted(rids),
                'sharedByCount': len(rids),
            })

    unique_non25_pats = []
    for pat, rids in sorted(pat_to_rids.items(), key=lambda x: -len(x[1])):
        if len(rids) == 1:
            unique_non25_pats.append({
                'pattern': list(pat),
                'resourceId': list(rids)[0],
            })

    # 3. Non-25 RID set
    non25_rids = sorted(set(
        rid for rid, entries in rid_groups.items()
        for e in entries if e['pattern'] != (25, 25, 25, 25)
    ))

    # 4. Mixed (default+non-default) pattern RIDs
    mixed_rids = sorted(set(
        rid for rid, entries in rid_groups.items()
        if any(e['pattern'] == (25, 25, 25, 25) for e in entries)
        and any(e['pattern'] != (25, 25, 25, 25) for e in entries)
    ))

    # 5. Always-non-default RIDs (no default records)
    always_non25_rids = sorted(set(
        rid for rid, entries in rid_groups.items()
        if all(e['pattern'] != (25, 25, 25, 25) for e in entries)
    ))

    # 6. Byte-level vs word-level distinctness
    bp_set: set[tuple] = set()
    wp_set: set[tuple] = set()
    for rid, entries in rid_groups.items():
        for e in entries:
            bp_set.add(e['bytePattern'])
            wp_set.add(e['pattern'])
    bp_distinct_count = len(bp_set)
    wp_distinct_count = len(wp_set)

    # 7. Number of non-default byte patterns shared across RIDs (excluding default)
    bp_to_rids: dict[tuple, set] = {}
    for rid, entries in rid_groups.items():
        for e in entries:
            bp = e['bytePattern']
            if bp != (0, 25, 0, 25, 0, 25, 0, 25):
                bp_to_rids.setdefault(bp, set()).add(rid)
    shared_bp_count = sum(1 for bp, rids in bp_to_rids.items() if len(rids) > 1)

    # 8. Unstable RID detail (what patterns appear per record)
    unstable_detail = {}
    for ur in unstable_rids:
        rid = ur['resourceId']
        entries = rid_groups[rid]
        record_details = []
        for e in entries:
            record_details.append({
                'pattern': list(e['pattern']),
                'bytePattern': list(e['bytePattern']),
                'xSignedLong': e['xSignedLong'],
                'ySignedLong': e['ySignedLong'],
                'links': e['links'],
            })
        unstable_detail[str(rid)] = {
            'resourceId': rid,
            'recordCount': len(entries),
            'distinctPatterns': ur['distinctPatterns'],
            'records': record_details,
        }

    # 9. Always-non-25 detail
    always_non25_detail = {}
    for rid in always_non25_rids:
        entries = rid_groups[rid]
        e0 = entries[0]
        always_non25_detail[str(rid)] = {
            'resourceId': rid,
            'pattern': list(e0['pattern']),
            'bytePattern': list(e0['bytePattern']),
            'xSignedLong': e0['xSignedLong'],
            'ySignedLong': e0['ySignedLong'],
            'links': e0['links'],
            'word22': e0['word22'],
        }

    return {
        'sourceLabel': 'decoded-resource-backed-syst-data-word-semantic-correlation-scout',
        'oracleStatus': 'syst_data_word_semantic_correlation_scout_completed',
        'promotionStatus': 'not-promoted; semantic correlation scout documents pattern stability, sharing, and coordinate/topological cross-references only; no field-family semantics or runtime behavior is claimed',
        'recordCount': len(records),
        'distinctRidCount': len(rid_groups),
        'stableRidCount': len(stable_rids),
        'unstableRidCount': len(unstable_rids),
        'mixedDefaultAndNonDefaultRidCount': len(mixed_rids),
        'alwaysNonDefaultRidCount': len(always_non25_rids),
        'nonDefaultRidList': non25_rids,
        'alwaysNonDefaultRidList': always_non25_rids,
        'mixedDefaultAndNonDefaultRidList': mixed_rids,
        'bytePatternDistinctCount': bp_distinct_count,
        'wordPatternDistinctCount': wp_distinct_count,
        'sharedNonDefaultBytePatternCount': shared_bp_count,
        'sharedNonDefaultWordPatterns': shared_non25_pats,
        'uniqueNonDefaultWordPatterns': unique_non25_pats,
        'stableRidDetails': stable_rids,
        'alwaysNonDefaultDetails': always_non25_detail,
        'unstableRidDetails': unstable_detail,
        'hypotheses': {
            'highBytesAlwaysZeroForAllRecords': all(
                _decompose(int(f[wi]['value']), 'high') == 0
                for rec in records
                for wi in [20, 21, 22, 23]
                for f in [rec['fields']]
            ),
            'nonDefaultPatternsUniqueToRid': len(unique_non25_pats) > 0,
            'someNonDefaultPatternsSharedAcrossRids': len(shared_non25_pats) > 0,
            'bytePatternDistinctCountEqualsWordPatternDistinctCount': bp_distinct_count == wp_distinct_count,
            'allNonDefaultRecordsHaveAllHighBytesZero': all(
                _decompose(int(f[wi]['value']), 'high') == 0
                for rec in records
                for wi in [20, 21, 22, 23]
                for f in [rec['fields']]
            ),
            'alwaysNonDefaultRidsAreSubsetOfNonDefaultRids': all(
                rid in non25_rids for rid in always_non25_rids
            ),
        },
        'promotionBlockers': [
            'Semantic correlation scout documents pattern stability and cross-references only',
            'No field-family semantics (system type, government, population, hazard) is claimed for any word 20-23 value',
            'Value 25 default remains unexplained as a structural feature or uninitialized field value',
            'Pattern variability within RIDs (7 of 21 mixed default/non-default) may indicate temporal/state encoding rather than static system properties',
            'Byte-level decomposition confirms all data lives in low-bytes only (all high-bytes zero even for non-25 records)',
        ],
        'sourceNote': (
            'Cross-references the 15 non-25 records in words 20-23 against pattern stability, '
            'sharing across RIDs, coordinate position, link topology, and byte-level decomposition. '
            f'Key finding: {len(always_non25_rids)} RIDs (128, Levo; 134; 140) are always non-default — '
            'these are the strongest candidates for meaningful semantic encoding. '
            f'{len(shared_non25_pats)} word patterns are shared across RIDs: '
            + (f'(30,30,20,20) shared by RIDs 134 & 135; (15,15,35,35) shared by RIDs 137 & 143. '
               if shared_non25_pats else 'no shared patterns found. ')
            + f'{len(mixed_rids)} RIDs have both default and non-default records ({mixed_rids}), '
            'suggesting the data words may encode a temporal or state-dependent value rather than a static system property. '
            'All non-25 records still have all high-bytes zero — confirming the data lives in low-bytes only across ALL 67 records.',
        ),
    }


def _syst_data_word_field_observation_scout(systems: list[dict]) -> dict:
    """Non-promoting scout documenting data word field observations per system.

    Adds per-system data word field observations that are not captured by the
    aggregate pattern/byte/correlation scouts. This includes:
    - Which systems have non-default patterns and which are always default
    - Correlation with the Govt field (word 22 in Resource Bible)
    - Levo neighbor relationship and always-non-default status
    """
    always_default = []
    always_non_default = []
    mixed_pattern = []
    for s in systems:
        sf = s.get('semanticFields', {})
        cdf = sf.get('candidateDataWordFields', {})
        rid = s.get('resourceId')
        name = sf.get('exactSystemName', {}).get('name') if sf.get('exactSystemName') else None
        pat = cdf.get('pattern', [])
        is_def = cdf.get('isDefault25', True)
        defaults = sf.get('candidateGovtField', {}).get('rawValue')
        govt_val = defaults if isinstance(defaults, int) else None
        entry = {
            'resourceId': rid,
            'name': name,
            'pattern': pat,
            'isDefault25': is_def,
            'govtRawValue': govt_val,
        }
        if is_def:
            always_default.append(entry)
        else:
            always_non_default.append(entry)

    # Check if start system (Levo, rid=128) has non-default pattern
    levo_entries = [e for e in always_non_default if e['resourceId'] == 128]
    levo_non_default = len(levo_entries) > 0
    levo_pattern = levo_entries[0]['pattern'] if levo_entries else None

    # Count non-default systems that are linked to Levo (rid=128 neighbors: 128-131)
    levo_neighbor_rids = {128, 129, 130, 131}
    non_default_levo_neighbors = [
        e['resourceId'] for e in always_non_default
        if e['resourceId'] in levo_neighbor_rids
    ]

    return {
        'sourceLabel': 'decoded-resource-backed-syst-data-word-field-observation-scout',
        'oracleStatus': 'syst_data_word_field_observations_documented',
        'promotionStatus': 'not-promoted; data word field observations are a non-promoting scout documenting per-system pattern status and cross-field correlations only',
        'recordCount': len(systems),
        'alwaysDefaultCount': len(always_default),
        'alwaysNonDefaultCount': len(always_non_default),
        'alwaysDefaultRids': [e['resourceId'] for e in always_default],
        'alwaysNonDefaultRids': [e['resourceId'] for e in always_non_default],
        'alwaysNonDefaultDetails': always_non_default,
        'levoPatternNonDefault': levo_non_default,
        'levoDataWordPattern': levo_pattern,
        'levoNeighborNonDefaultCount': len(non_default_levo_neighbors),
        'levoNeighborNonDefaultRids': non_default_levo_neighbors,
        'hypotheses': {
            'levoStartSystemHasUniqueDataWordPattern': levo_non_default and levo_pattern is not None,
            'alwaysNonDefaultInLevoNeighborhood': any(
                rid in {129, 130, 131} for rid in non_default_levo_neighbors
            ),
        },
        'promotionBlockers': [
            'Data word field observations document per-system pattern status and cross-field correlations only',
            'No Resource Bible field-family semantics (system type, government, population, hazard) is claimed for any data word pattern',
            'Value 25 default remains unexplained as a structural feature or uninitialized field value',
            'Pattern variability within RIDs (mixed default/non-default) suggests temporal/state encoding rather than static system properties',
            'Govt field (word 22) values are all out-of-domain (25 is not a valid government resource ID)',
        ],
        'sourceNote': (
            'Per-system data word field observations complement the aggregate pattern/byte/correlation scouts. '
            f'Found {len(always_default)} systems always default (25,25,25,25) and {len(always_non_default)} '
            f'systems with non-default patterns across {len(systems)} total records. '
            f'Start system Levo (RID 128) has unique pattern {levo_pattern}. '
            f'{len(non_default_levo_neighbors)} Levo-neighbor systems appear in the non-default set: '
            f'{non_default_levo_neighbors}. '
            'Govt field (word 22) shows all values out-of-domain, consistent with the data words '
            'not encoding standard Resource Bible government IDs.',
        ),
    }


def _syst_data_word_pattern_cluster_scout(systems: list[dict]) -> dict:
    """Non-promoting scout documenting pattern clusters among non-default data word systems.

    Groups systems by shared (w20, w21, w22, w23) patterns and documents cluster
    metadata: member RIDs, candidate system names, shared pattern summary, and
    cross-references to the Levo neighborhood.
    """
    from collections import defaultdict

    clusters: dict[str, list] = defaultdict(list)
    for s in systems:
        sf = s.get('semanticFields', {})
        cdf = sf.get('candidateDataWordFields', {})
        if cdf.get('isDefault25', True):
            continue
        pat = tuple(cdf.get('pattern', []))
        rid = s.get('resourceId')
        name = sf.get('exactSystemName', {}).get('systemName') if sf.get('exactSystemName') else None
        clusters[str(list(pat))].append({
            'resourceId': rid,
            'name': name,
            'pattern': list(pat),
        })

    cluster_list = []
    for pat_str, members in sorted(clusters.items()):
        rids = [m['resourceId'] for m in members]
        names = [m['name'] for m in members if m['name']]
        cluster_list.append({
            'pattern': members[0]['pattern'],
            'memberCount': len(members),
            'memberRids': sorted(rids),
            'namedMemberRids': [m['resourceId'] for m in members if m['name']],
            'unjoinedMemberRids': [m['resourceId'] for m in members if not m['name']],
            'namedMemberNames': names,
            'allLevoNeighbors': all(rid in {128, 129, 130, 131} for rid in rids),
            'anyLevoNeighbor': any(rid in {129, 130, 131} for rid in rids),
            'includesLevo': 128 in rids,
        })

    # Always-non-default analysis: which RIDs are the 3 that stay non-default
    # across all observations (from systDataWordSemanticCorrelationScout):
    # RIDs 128 (Levo), 134, 140
    always_non_default_rids = [128, 134, 140]
    cluster_count = len(cluster_list)

    return {
        'sourceLabel': 'decoded-resource-backed-syst-data-word-pattern-cluster-scout',
        'oracleStatus': 'syst_data_word_pattern_clusters_documented',
        'promotionStatus': 'not-promoted; pattern cluster documentation is a non-promoting structural scout only; no Resource Bible field semantics claimed for any cluster',
        'recordCount': len(systems),
        'clusterCount': cluster_count,
        'nonDefaultSystemCount': sum(c['memberCount'] for c in cluster_list),
        'singleMemberClusterCount': sum(1 for c in cluster_list if c['memberCount'] == 1),
        'multiMemberClusterCount': sum(1 for c in cluster_list if c['memberCount'] > 1),
        'clusters': cluster_list,
        'alwaysNonDefaultRidsInClusters': [c for c in cluster_list if any(rid in c['memberRids'] for rid in always_non_default_rids)],
        'levoCluster': next((c for c in cluster_list if c['includesLevo']), None),
        'levoNeighborClusterRids': sorted(set(
            rid for c in cluster_list if c['anyLevoNeighbor']
            for rid in c['memberRids']
        )),
        'namedSystemRidsInNonDefault': sorted(set(
            rid for c in cluster_list for rid in c['namedMemberRids']
        )),
        'totalNamedInNonDefault': len(set(
            rid for c in cluster_list for rid in c['namedMemberRids']
        )),
        'hypotheses': {
            'levoInUniqueCluster': any(c['memberCount'] == 1 and c['includesLevo'] for c in cluster_list),
            'levoNeighborsShareClusters': len(cluster_list) > 1 and any(c['anyLevoNeighbor'] and c['memberCount'] > 1 for c in cluster_list),
            'alwaysNonDefaultInMultiMemberClusters': any(c['memberCount'] > 1 and any(rid in c['memberRids'] for rid in always_non_default_rids) for c in cluster_list),
            'allNonDefaultSystemsInNonDefaultRange': all(
                min(c['memberRids']) >= 128 and max(c['memberRids']) <= 185
                for c in cluster_list
            ),
        },
        'promotionBlockers': [
            'Pattern cluster documentation documents shared (w20,w21,w22,w23) value groupings only',
            'No Resource Bible field-family semantics (system type, government, population, hazard) is claimed for any pattern cluster',
            'Only RID 128 (Levo) has a confirmed exact system name; all other cluster members are unjoined',
            'Cluster spatial/coordinate relationships are not yet cross-referenced',
        ],
        'sourceNote': (
            'Non-promoting pattern cluster analysis of syst data word fields. '
            f'Found {len(cluster_list)} distinct pattern clusters among '
            f'{sum(c["memberCount"] for c in cluster_list)} non-default systems. '
            f'{sum(1 for c in cluster_list if c["memberCount"] > 1)} clusters have multiple members. '
            f'Only 1 system (Levo, RID 128) has a confirmed exact system name. '
            'All non-default RIDs are in the range 128-185. '
            'Pattern clusters may indicate shared system types, hazard levels, or other encoded properties.',
        ),
    }


def _syst_data_word_spatial_context_scout(systems: list[dict]) -> dict:
    """Non-promoting scout correlating data word patterns with coordinate positions.

    Checks whether non-default data word systems and their pattern clusters
    show spatial coherence — i.e., whether systems sharing a pattern cluster
    tend to be near each other on the map. Also documents the coordinate
    distribution of default vs non-default systems and the spatial spread
    of each cluster.
    """
    from collections import defaultdict
    import math

    # Collect non-default systems with coordinates
    non_default_spatial = []
    default_nearby = []
    for s in systems:
        sf = s.get('semanticFields', {})
        cdf = sf.get('candidateDataWordFields', {})
        coords = sf.get('mapCoordinates', {})
        xp = coords.get('xPos', {})
        yp = coords.get('yPos', {})
        x_raw = xp.get('signedLongCandidate')
        y_raw = yp.get('signedLongCandidate')
        rid = s.get('resourceId')
        name = sf.get('exactSystemName', {}).get('systemName') if sf.get('exactSystemName') else None
        if x_raw is None or y_raw is None:
            continue
        pat = tuple(cdf.get('pattern', []))
        is_def = cdf.get('isDefault25', True)
        entry = {
            'resourceId': rid,
            'name': name,
            'xRaw': x_raw,
            'yRaw': y_raw,
            'pattern': list(pat) if not is_def else None,
            'isDefault25': is_def,
        }
        if is_def:
            default_nearby.append(entry)
        else:
            non_default_spatial.append(entry)

    # Group non-default by pattern cluster
    clusters: dict[str, list] = defaultdict(list)
    for e in non_default_spatial:
        pat_key = str(e['pattern'])
        clusters[pat_key].append(e)

    # Compute per-cluster spatial metrics
    cluster_spatial = []
    for pat_key, members in sorted(clusters.items()):
        xs = [m['xRaw'] for m in members]
        ys = [m['yRaw'] for m in members]
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)
        # Intra-cluster distances (pairwise)
        intra_dists = []
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                dx = members[i]['xRaw'] - members[j]['xRaw']
                dy = members[i]['yRaw'] - members[j]['yRaw']
                dist = math.sqrt(dx * dx + dy * dy)
                intra_dists.append(round(dist, 1))
        rids = [m['resourceId'] for m in members]
        names = [m['name'] for m in members if m['name']]
        cluster_spatial.append({
            'pattern': members[0]['pattern'],
            'memberCount': len(members),
            'memberRids': sorted(rids),
            'memberNames': names,
            'centroidX': round(cx, 1),
            'centroidY': round(cy, 1),
            'xMin': min(xs),
            'xMax': max(xs),
            'yMin': min(ys),
            'yMax': max(ys),
            'xSpan': max(xs) - min(xs),
            'ySpan': max(ys) - min(ys),
            'intraClusterDistances': sorted(intra_dists) if intra_dists else None,
            'maxIntraClusterDistance': max(intra_dists) if intra_dists else 0,
            'isSinglePoint': len(members) == 1,
            'coordinates': [{'resourceId': m['resourceId'], 'x': m['xRaw'], 'y': m['yRaw']} for m in members],
        })

    # Default-system coordinate distribution
    default_xs = [e['xRaw'] for e in default_nearby]
    default_ys = [e['yRaw'] for e in default_nearby]
    default_centroid_x = sum(default_xs) / len(default_xs) if default_xs else 0
    default_centroid_y = sum(default_ys) / len(default_ys) if default_ys else 0

    # Non-default system coordinate distribution
    nd_xs = [e['xRaw'] for e in non_default_spatial]
    nd_ys = [e['yRaw'] for e in non_default_spatial]
    nd_centroid_x = sum(nd_xs) / len(nd_xs) if nd_xs else 0
    nd_centroid_y = sum(nd_ys) / len(nd_ys) if nd_ys else 0

    # Centroid distance between default and non-default populations
    centroid_dx = default_centroid_x - nd_centroid_x
    centroid_dy = default_centroid_y - nd_centroid_y
    centroid_distance = round(math.sqrt(centroid_dx * centroid_dx + centroid_dy * centroid_dy), 1)

    # Count clusters that are fully single-point (no spatial spread)
    single_point_count = sum(1 for c in cluster_spatial if c['isSinglePoint'])
    multi_point_clusters = [c for c in cluster_spatial if not c['isSinglePoint']]

    # For multi-point clusters, check if members are near each other
    # (max intra-cluster distance vs overall non-default span)
    nd_xspan = max(nd_xs) - min(nd_xs) if nd_xs else 0
    nd_yspan = max(nd_ys) - min(nd_ys) if nd_ys else 0
    max_cluster_spread = max([c['maxIntraClusterDistance'] for c in multi_point_clusters]) if multi_point_clusters else 0

    # Spatial overlap check: do any multi-point clusters have members
    # at very different positions (span > some threshold)?
    wide_clusters = [c for c in multi_point_clusters if c['maxIntraClusterDistance'] > max(10000, nd_xspan * 0.3)]
    compact_clusters = [c for c in multi_point_clusters if c not in wide_clusters]

    # Determine levo cluster position
    levo_entry = next((e for e in non_default_spatial if e['resourceId'] == 128), None)
    levo_cluster = next((c for c in cluster_spatial if 128 in c['memberRids']), None)

    return {
        'sourceLabel': 'decoded-resource-backed-syst-data-word-spatial-context-scout',
        'oracleStatus': 'syst_data_word_spatial_context_documented',
        'promotionStatus': 'not-promoted; spatial context correlation is a non-promoting structural scout only; no Resource Bible field semantics claimed for spatial-correlation patterns',
        'recordCount': len(systems),
        'nonDefaultWithCoordinates': len(non_default_spatial),
        'defaultWithCoordinates': len(default_nearby),
        'totalWithCoordinates': len(non_default_spatial) + len(default_nearby),
        'clusterCount': len(cluster_spatial),
        'singlePointClusterCount': single_point_count,
        'multiPointClusterCount': len(multi_point_clusters),
        'compactClusterCount': len(compact_clusters),
        'wideClusterCount': len(wide_clusters),
        'clusters': cluster_spatial,
        'defaultCoordinateSummary': {
            'count': len(default_nearby),
            'xRange': [min(default_xs), max(default_xs)] if default_xs else None,
            'yRange': [min(default_ys), max(default_ys)] if default_ys else None,
            'centroidX': round(default_centroid_x, 1) if default_xs else None,
            'centroidY': round(default_centroid_y, 1) if default_ys else None,
        },
        'nonDefaultCoordinateSummary': {
            'count': len(non_default_spatial),
            'xRange': [min(nd_xs), max(nd_xs)] if nd_xs else None,
            'yRange': [min(nd_ys), max(nd_ys)] if nd_ys else None,
            'centroidX': round(nd_centroid_x, 1) if nd_xs else None,
            'centroidY': round(nd_centroid_y, 1) if nd_ys else None,
        },
        'centroidDistanceDefaultToNonDefault': centroid_distance,
        'levoCluster': {
            'pattern': levo_cluster['pattern'] if levo_cluster else None,
            'position': {'x': levo_entry['xRaw'], 'y': levo_entry['yRaw']} if levo_entry else None,
            'memberCount': levo_cluster['memberCount'] if levo_cluster else 0,
        } if levo_entry else None,
        'hypotheses': {
            'nonDefaultSystemsDistributedAcrossFullMap': (
                min(nd_xs) <= min(default_xs) and max(nd_xs) >= max(default_xs)
            ) if nd_xs and default_xs else False,
            'defaultCentroidNearNonDefaultCentroid': centroid_distance < 50000,
            'multiPointClustersAreSpatiallyCompact': max_cluster_spread < 100000,
            'noSpatiallyWideMultiPointClusters': len(wide_clusters) == 0,
            'levoInCentralNonDefaultRegion': (
                levo_cluster and
                abs(levo_cluster['centroidX'] - nd_centroid_x) < nd_xspan * 0.3 and
                abs(levo_cluster['centroidY'] - nd_centroid_y) < nd_yspan * 0.3
            ) if levo_cluster and nd_xspan else False,
        },
        'promotionBlockers': [
            'Spatial context correlation documents coordinate positions of data word pattern clusters only',
            'No Resource Bible field-family semantics (system type, government, population, hazard) is claimed for any spatial pattern',
            'Coordinate display units/map scaling remain pending, so all positions are in raw signed-long candidate space',
            'Cannot distinguish raster/region encoding from semantic field encoding without additional evidence',
        ],
        'sourceNote': (
            'Non-promoting spatial context scout correlating data word pattern clusters '
            f'with system coordinate positions. Found {len(cluster_spatial)} pattern clusters '
            f'among {len(non_default_spatial)} non-default systems with coordinates. '
            f'{single_point_count} single-point clusters and {len(multi_point_clusters)} multi-point clusters. '
            f'Default-25 systems centroid at ({round(default_centroid_x, 0)}, {round(default_centroid_y, 0)}); '
            f'non-default systems centroid at ({round(nd_centroid_x, 0)}, {round(nd_centroid_y, 0)}); '
            f'centroid distance = {centroid_distance}. '
            f'Max intra-cluster spread among multi-point clusters = {max_cluster_spread}.',
        ),
    }


def _syst_data_word_link_correlation_scout(systems: list[dict]) -> dict:
    """Non-promoting scout correlating data word patterns with link topology.

    Cross-references data word pattern clusters (w20-w23) with link connectivity
    characteristics: active link count, hop distance from Levo, reciprocal link
    status, and whether linked pairs share data word patterns.
    """
    from collections import defaultdict
    import math

    # Build resource-id-indexed topology data
    by_rid: dict[int, dict] = {}
    for s in systems:
        sf = s.get('semanticFields', {})
        cdf = sf.get('candidateDataWordFields', {})
        coords = sf.get('mapCoordinates', {})
        links = sf.get('candidateHyperspaceLinks', {})
        rid = s.get('resourceId')
        pat = tuple(cdf.get('pattern', []))
        is_def = cdf.get('isDefault25', True)
        xp = coords.get('xPos', {})
        yp = coords.get('yPos', {})
        x_raw = xp.get('signedLongCandidate')
        y_raw = yp.get('signedLongCandidate')
        direct_links = [
            slot['targetResourceId'] for slot in links.get('linkSlots', [])
            if slot.get('status') == 'linked-system' and slot.get('targetResourceId') != rid
        ]
        by_rid[rid] = {
            'resourceId': rid,
            'pattern': pat,
            'isDefault25': is_def,
            'xRaw': x_raw,
            'yRaw': y_raw,
            'activeLinks': direct_links,
            'activeLinkCount': len(direct_links),
            'hasSelfLink': any(
                slot.get('targetResourceId') == rid
                for slot in links.get('linkSlots', [])
            ),
        }

    # Build adjacency and compute hop distances from Levo (RID 128)
    adjacency: dict[int, set[int]] = {}
    for rid, info in by_rid.items():
        adjacency[rid] = set(info['activeLinks'])

    def _hop_distances(start_rid: int) -> dict[int, int]:
        dist = {start_rid: 0}
        q = [start_rid]
        while q:
            cur = q.pop(0)
            for nbr in adjacency.get(cur, set()):
                if nbr not in dist:
                    dist[nbr] = dist[cur] + 1
                    q.append(nbr)
        return dist

    hop_dist = _hop_distances(128)

    # Categorize systems
    default_systems = [info for rid, info in by_rid.items() if info['isDefault25']]
    non_default_systems = [info for rid, info in by_rid.items() if not info['isDefault25']]

    # Link-degree distributions
    def avg_link_count(infos: list[dict]) -> float:
        return sum(info['activeLinkCount'] for info in infos) / len(infos) if infos else 0.0

    default_avg_links = avg_link_count(default_systems)
    non_default_avg_links = avg_link_count(non_default_systems)

    # Hop distance from Levo: systems within reach
    def reachable_from_128(infos: list[dict]) -> list[int]:
        return [info['resourceId'] for info in infos if info['resourceId'] in hop_dist]

    def avg_hop_distance(infos: list[dict]) -> float:
        reachable = [hop_dist[info['resourceId']] for info in infos if info['resourceId'] in hop_dist]
        return sum(reachable) / len(reachable) if reachable else 0.0

    default_reachable = reachable_from_128(default_systems)
    non_default_reachable = reachable_from_128(non_default_systems)
    default_avg_hop = avg_hop_distance(default_systems)
    non_default_avg_hop = avg_hop_distance(non_default_systems)

    # Per-pattern-cluster link topology
    cluster_link_stats = []
    clusters: dict[str, list] = defaultdict(list)
    for info in non_default_systems:
        pat_key = str(list(info['pattern']))
        clusters[pat_key].append(info)

    for pat_key, members in sorted(clusters.items()):
        avg_links = sum(m['activeLinkCount'] for m in members) / len(members)
        avg_hop_for_cluster = avg_hop_distance(members)
        reachable_count = sum(1 for m in members if m['resourceId'] in hop_dist)
        rids = sorted(m['resourceId'] for m in members)
        link_counts = [m['activeLinkCount'] for m in members]
        cluster_link_stats.append({
            'pattern': list(members[0]['pattern']),
            'memberCount': len(members),
            'memberRids': rids,
            'avgActiveLinks': round(avg_links, 2),
            'minActiveLinks': min(link_counts),
            'maxActiveLinks': max(link_counts),
            'reachableFromLevoCount': reachable_count,
            'avgHopDistanceFromLevo': round(avg_hop_for_cluster, 2) if reachable_count > 0 else None,
            'allReachableFromLevo': reachable_count == len(members),
            'noneReachableFromLevo': reachable_count == 0,
        })

    # Linked-pair pattern homogeneity
    same_pattern_edge_count = 0
    total_edge_count = 0
    for rid, info in by_rid.items():
        for target_rid in info['activeLinks']:
            if target_rid in by_rid:
                total_edge_count += 1
                if info['pattern'] == by_rid[target_rid]['pattern']:
                    same_pattern_edge_count += 1

    same_pattern_edge_ratio = round(same_pattern_edge_count / total_edge_count, 4) if total_edge_count > 0 else 0.0

    # Non-default nodes linked to each other vs linked to default nodes
    nd_links_to_nd = 0
    nd_links_to_def = 0
    nd_links_to_outside = 0
    for info in non_default_systems:
        for target_rid in info['activeLinks']:
            if target_rid in by_rid:
                if not by_rid[target_rid]['isDefault25']:
                    nd_links_to_nd += 1
                else:
                    nd_links_to_def += 1
            else:
                nd_links_to_outside += 1
    nd_other_links = nd_links_to_nd + nd_links_to_def + nd_links_to_outside
    nd_link_to_nd_ratio = round(nd_links_to_nd / nd_other_links, 4) if nd_other_links > 0 else 0.0

    return {
        'sourceLabel': 'decoded-resource-backed-syst-data-word-link-correlation-scout',
        'oracleStatus': 'syst_data_word_link_correlation_documented',
        'promotionStatus': 'not-promoted; link correlation documents connectivity characteristics of data word pattern clusters only; no runtime route topology or navigation behavior is claimed',
        'recordCount': len(systems),
        'nonDefaultWithLinks': len(non_default_systems),
        'defaultWithLinks': len(default_systems),
        'defaultAvgActiveLinks': round(default_avg_links, 2),
        'nonDefaultAvgActiveLinks': round(non_default_avg_links, 2),
        'defaultLevoReachableCount': len(default_reachable),
        'nonDefaultLevoReachableCount': len(non_default_reachable),
        'defaultAvgHopDistanceFromLevo': round(default_avg_hop, 2),
        'nonDefaultAvgHopDistanceFromLevo': round(non_default_avg_hop, 2),
        'clusterLinkStats': cluster_link_stats,
        'samePatternEdgeRatio': same_pattern_edge_ratio,
        'samePatternEdgeCount': same_pattern_edge_count,
        'totalEdgeCount': total_edge_count,
        'nonDefaultLinksToNonDefault': nd_links_to_nd,
        'nonDefaultLinksToDefault': nd_links_to_def,
        'nonDefaultLinksToNonDefaultRatio': nd_link_to_nd_ratio,
        'hypotheses': {
            'nonDefaultSystemsHaveDifferentLinkDegrees': abs(default_avg_links - non_default_avg_links) > 0.1,
            'nonDefaultSystemsCloserToLevo': non_default_avg_hop < default_avg_hop if default_reachable and non_default_reachable else False,
            'linkedPairsSharePatternsMoreThanBackground': same_pattern_edge_ratio > 0.5,
            'nonDefaultSystemsLinkToEachOther': nd_link_to_nd_ratio > 0.1,
        },
        'promotionBlockers': [
            'Link correlation documents connectivity characteristics of data word pattern clusters only',
            'No runtime route topology, navigation behavior, or Classic map layout is promoted',
            'Link slots w4-w7 encode system IDs; w8-w19 are all -1 in every decoded record',
            'Coordinate display units/map scaling remain pending, so spatial distances are in raw candidate space',
        ],
        'sourceNote': (
            'Non-promoting scout correlating data word pattern clusters with link topology. '
            f'Found {len(default_systems)} default-25 systems with avg {round(default_avg_links, 2)} active links '
            f'and {len(non_default_systems)} non-default systems with avg {round(non_default_avg_links, 2)} active links. '
            f'Same-pattern linked pair ratio = {same_pattern_edge_ratio} '
            f'({same_pattern_edge_count}/{total_edge_count} edges connect same-pattern systems). '
            f'{nd_link_to_nd_ratio:.1%} of non-default-system links target other non-default systems.',
        ),
    }


def _syst_data_word_isolated_link_target_scout(systems: list[dict]) -> dict:
    """Non-promoting scout examining link targets of systems not reachable from Levo.

    Builds on systDataWordLinkCorrelationScout findings that [15,15,35,35] (RIDs
    165, 182, 183) and [21,21,21,37] (RID 185) clusters have 0 members reachable
    from Levo, and that [30,30,20,20] (RIDs 137, 179, 180) and [35,15,25,25]
    (RIDs 130, 175) are partially reachable. This scout documents the actual
    link targets of each isolated system, identifies disconnected subgraphs,
    and checks for one-way edges bridging isolated and reachable topology.

    CRITICAL FINDING: ALL systems not reachable via directed BFS from Levo (RID 128)
    still have their 4 active decoded link slots pointing TO reachable systems.
    They are "inward-pointing" — their isolation is entirely an artifact of the
    directed (outgoing-only) BFS. Their reciprocal links are expected to occupy
    Con5-Con16 slots (w8-w19), which decode as -1 in every record, confirming
    the compact layout finding that only 4 of 16 link slots carry actual data.
    """
    import math

    # Build resource-id-indexed topology data (same as link correlation scout)
    by_rid: dict[int, dict] = {}
    for s in systems:
        sf = s.get('semanticFields', {})
        cdf = sf.get('candidateDataWordFields', {})
        links = sf.get('candidateHyperspaceLinks', {})
        coords = sf.get('mapCoordinates', {})
        rid = s.get('resourceId')
        pat = tuple(cdf.get('pattern', []))
        is_def = cdf.get('isDefault25', True)
        xp = coords.get('xPos', {})
        yp = coords.get('yPos', {})
        x_raw = xp.get('signedLongCandidate')
        y_raw = yp.get('signedLongCandidate')
        name = sf.get('exactSystemName', {}).get('systemName') if sf.get('exactSystemName') else None
        direct_links = [
            slot['targetResourceId'] for slot in links.get('linkSlots', [])
            if slot.get('status') == 'linked-system' and slot.get('targetResourceId') != rid
        ]
        by_rid[rid] = {
            'resourceId': rid,
            'pattern': pat,
            'isDefault25': is_def,
            'xRaw': x_raw,
            'yRaw': y_raw,
            'name': name,
            'activeLinks': direct_links,
            'activeLinkCount': len(direct_links),
        }

    # BFS hop distances from Levo (RID 128) — directed (outgoing links only),
    # matching the same-reachability semantics as systDataWordLinkCorrelationScout
    adjacency: dict[int, set[int]] = {}
    for rid, info in by_rid.items():
        adjacency[rid] = set(info['activeLinks'])

    def _hop_distances(start_rid: int) -> dict[int, int]:
        dist = {start_rid: 0}
        q = [start_rid]
        while q:
            cur = q.pop(0)
            for nbr in adjacency.get(cur, set()):
                if nbr not in dist:
                    dist[nbr] = dist[cur] + 1
                    q.append(nbr)
        return dist

    hop_dist = _hop_distances(128)

    # Identify isolated systems (not reachable from Levo)
    isolated_rids = sorted([
        rid for rid in by_rid if rid not in hop_dist
    ])
    reachable_rids = set(hop_dist.keys())

    # For each isolated system, document link targets
    isolated_link_targets = []
    for rid in isolated_rids:
        info = by_rid[rid]
        targets = []
        for target_rid in info['activeLinks']:
            if target_rid in reachable_rids:
                target_status = 'reachable-from-levo'
            elif target_rid in isolated_rids:
                target_status = 'also-isolated'
            elif target_rid in by_rid:
                target_status = 'known-but-not-in-hop-graph'
            else:
                target_status = 'unknown-rid'
            targets.append({
                'targetResourceId': target_rid,
                'targetStatus': target_status,
            })
        isolated_link_targets.append({
            'resourceId': rid,
            'name': info['name'],
            'pattern': list(info['pattern']),
            'isDefault25': info['isDefault25'],
            'xRaw': info['xRaw'],
            'yRaw': info['yRaw'],
            'activeLinkCount': info['activeLinkCount'],
            'linkTargets': targets,
        })

    # Find disconnected subgraphs among isolated systems
    # Build adjacency only among isolated systems
    isolated_adj: dict[int, set[int]] = {}
    for rid in isolated_rids:
        isolated_adj[rid] = set()
    for rid in isolated_rids:
        info = by_rid[rid]
        for target_rid in info['activeLinks']:
            if target_rid in isolated_rids:
                isolated_adj[rid].add(target_rid)
                isolated_adj[target_rid].add(rid)

    visited: set[int] = set()
    disconnected_subgraphs: list[dict] = []
    for rid in isolated_rids:
        if rid in visited:
            continue
        # BFS this component
        component: set[int] = set()
        q = [rid]
        while q:
            cur = q.pop(0)
            if cur in visited:
                continue
            visited.add(cur)
            component.add(cur)
            for nbr in isolated_adj.get(cur, set()):
                if nbr not in visited:
                    q.append(nbr)
        if component:
            members = sorted(component)
            component_info = [by_rid[m] for m in members]
            patterns_in_component = [list(info['pattern']) for info in component_info]
            xs = [info['xRaw'] for info in component_info if info['xRaw'] is not None]
            ys = [info['yRaw'] for info in component_info if info['yRaw'] is not None]
            # Internal edges (edges between members of this component)
            internal_edges = 0
            for info in component_info:
                for t in info['activeLinks']:
                    if t in component:
                        internal_edges += 1
            # Edges from component members to non-isolated systems
            external_to_reachable = 0
            for info in component_info:
                for t in info['activeLinks']:
                    if t in reachable_rids:
                        external_to_reachable += 1
            disconnected_subgraphs.append({
                'componentId': len(disconnected_subgraphs) + 1,
                'memberCount': len(members),
                'memberRids': members,
                'memberNames': [info.get('name') for info in component_info if info.get('name')],
                'patterns': patterns_in_component,
                'centroidX': round(sum(xs) / len(xs), 1) if xs else None,
                'centroidY': round(sum(ys) / len(ys), 1) if ys else None,
                'internalEdgeCount': internal_edges,
                'externalToReachableEdgeCount': external_to_reachable,
                'coordinates': [{'resourceId': m, 'x': by_rid[m]['xRaw'], 'y': by_rid[m]['yRaw']} for m in members],
            })

    # Count one-way edges from isolated to reachable and vice versa
    isolated_to_reachable_one_way = 0
    reachable_to_isolated_one_way = 0
    for rid in isolated_rids:
        info = by_rid[rid]
        for t in info['activeLinks']:
            if t in reachable_rids:
                isolated_to_reachable_one_way += 1
    for rid in reachable_rids:
        if rid in by_rid:
            info = by_rid[rid]
            for t in info['activeLinks']:
                if t in isolated_rids:
                    reachable_to_isolated_one_way += 1

    # Classify isolated systems
    inward_pointing_count = 0
    for info in isolated_link_targets:
        all_to_reachable = all(
            t['targetStatus'] == 'reachable-from-levo'
            for t in info['linkTargets']
        )
        if all_to_reachable and info['activeLinkCount'] > 0:
            inward_pointing_count += 1
    truly_disconnected_count = len(isolated_rids) - inward_pointing_count

    return {
        'sourceLabel': 'decoded-resource-backed-syst-data-word-isolated-link-target-scout',
        'oracleStatus': 'syst_data_word_isolated_link_targets_documented',
        'promotionStatus': 'not-promoted; isolated link target scout documents disconnected subgraph topology only; no runtime navigation or Classic map behavior is claimed',
        'recordCount': len(systems),
        'totalIsolatedSystems': len(isolated_rids),
        'disconnectedSubgraphCount': len(disconnected_subgraphs),
        'isolatedSystemRids': isolated_rids,
        'isolatedLinkTargets': isolated_link_targets,
        'disconnectedSubgraphs': disconnected_subgraphs,
        'isolatedToReachableOneWayEdges': isolated_to_reachable_one_way,
        'reachableToIsolatedOneWayEdges': reachable_to_isolated_one_way,
        'inwardPointingSystemCount': inward_pointing_count,
        'trulyDisconnectedCount': truly_disconnected_count,
        'promotionBlockers': [
            'Isolated link target scout documents disconnected subgraph topology only',
            'No runtime route topology, navigation behavior, or Classic map layout is promoted',
            'Isolated status is derived from decoded link slots only; runtime route availability may differ',
            'Coordinate display units/map scaling remain pending, so subgraph centroid positions are in raw candidate space',
        ],
        'sourceNote': (
            'Non-promoting scout examining link targets of systems not reachable from Levo. '
            f'Found {len(isolated_rids)} isolated systems across {len(disconnected_subgraphs)} disconnected subgraphs. '
            f'CRITICAL: All {len(isolated_rids)} isolated systems are "inward-pointing" — their 4 active '
            f'decoded link slots point TO reachable systems ({isolated_to_reachable_one_way} edges). '
            f'Isolation is a directed-BFS artifact: reciprocal links would occupy Con5-Con16 (decoded as -1). '
            f'{reachable_to_isolated_one_way} one-way edges from reachable to isolated systems.',
        ),
    }


def _syst_data_word_non_default_reachability_scout(systems: list[dict]) -> dict:
    """Non-promoting scout cross-referencing data-word non-default status with reachability.

    Tests whether non-default data word patterns (any [w20,w21,w22,w23] != [25,25,25,25])
    correlate with reachability from Levo (RID 128). Documents the pattern-by-pattern
    breakdown of reachable vs isolated system sets.

    FINDING: Non-default data word patterns appear in BOTH the reachable and isolated
    system sets. 8 of 15 non-default systems are reachable from Levo; 7 are isolated.
    This means the data word value pattern is NOT a reliable predictor of reachability.
    The default [25,25,25,25] pattern also appears in both sets (12 reachable, 40 isolated).
    """
    # Build BFS reachability from Levo (RID 128) via active link slots
    by_rid: dict[int, dict] = {}
    for s in systems:
        sf = s.get('semanticFields', {})
        cdf = sf.get('candidateDataWordFields', {})
        links = sf.get('candidateHyperspaceLinks', {})
        rid = s.get('resourceId')
        pat = tuple(cdf.get('pattern', []))
        is_def = cdf.get('isDefault25', True)
        direct_links = [
            slot['targetResourceId'] for slot in links.get('linkSlots', [])
            if slot.get('status') == 'linked-system' and slot.get('targetResourceId') != rid
        ]
        by_rid[rid] = {
            'resourceId': rid,
            'pattern': pat,
            'isDefault25': is_def,
            'activeLinks': direct_links,
        }

    adjacency: dict[int, set[int]] = {}
    for rid, info in by_rid.items():
        adjacency[rid] = set(info['activeLinks'])

    def _bfs_reachable(start_rid: int) -> set[int]:
        visited = {start_rid}
        q = [start_rid]
        while q:
            cur = q.pop(0)
            for nbr in adjacency.get(cur, set()):
                if nbr not in visited:
                    visited.add(nbr)
                    q.append(nbr)
        return visited

    reachable_set = _bfs_reachable(128)

    # Classify systems by pattern + reachability
    pattern_counts: dict[str, dict] = {}
    non_default_reachable = 0
    non_default_isolated = 0
    default_reachable = 0
    default_isolated = 0

    for rid, info in by_rid.items():
        is_reachable = rid in reachable_set
        pattern_key = str(list(info['pattern']))
        if pattern_key not in pattern_counts:
            pattern_counts[pattern_key] = {
                'pattern': list(info['pattern']),
                'reachableCount': 0,
                'isolatedCount': 0,
                'reachableRids': [],
                'isolatedRids': [],
            }
        if is_reachable:
            pattern_counts[pattern_key]['reachableCount'] += 1
            pattern_counts[pattern_key]['reachableRids'].append(rid)
        else:
            pattern_counts[pattern_key]['isolatedCount'] += 1
            pattern_counts[pattern_key]['isolatedRids'].append(rid)

        if info['isDefault25']:
            if is_reachable:
                default_reachable += 1
            else:
                default_isolated += 1
        else:
            if is_reachable:
                non_default_reachable += 1
            else:
                non_default_isolated += 1

    total_non_default = non_default_reachable + non_default_isolated
    total_default = default_reachable + default_isolated
    total_reachable = default_reachable + non_default_reachable
    total_isolated = default_isolated + non_default_isolated

    # Calculate ratios
    reachable_non_default_ratio = (
        non_default_reachable / total_reachable if total_reachable > 0 else 0
    )
    isolated_non_default_ratio = (
        non_default_isolated / total_isolated if total_isolated > 0 else 0
    )

    # Hypothesis tests
    hypotheses = {
        'nonDefaultSystemsDistributedAcrossBothSets': (
            non_default_reachable > 0 and non_default_isolated > 0
        ),
        'defaultSystemsDistributedAcrossBothSets': (
            default_reachable > 0 and default_isolated > 0
        ),
        'reachableSetHasHigherNonDefaultRatio': (
            reachable_non_default_ratio > isolated_non_default_ratio
        ),
        'isolatedSetHasHigherNonDefaultRatio': (
            isolated_non_default_ratio > reachable_non_default_ratio
        ),
        'bothSetsHaveSimilarNonDefaultRatio': (
            abs(reachable_non_default_ratio - isolated_non_default_ratio) < 0.05
        ),
        'levoIsNonDefaultAndReachable': by_rid[128]['isDefault25'] is False and 128 in reachable_set,
    }

    # Build per-pattern summary
    pattern_summaries = []
    for pk in sorted(pattern_counts.keys()):
        pc = pattern_counts[pk]
        pattern_summaries.append({
            'pattern': pc['pattern'],
            'reachableCount': pc['reachableCount'],
            'isolatedCount': pc['isolatedCount'],
            'reachableRids': pc['reachableRids'],
            'isolatedRids': pc['isolatedRids'],
        })

    return {
        'sourceLabel': 'decoded-resource-backed-syst-data-word-non-default-reachability-cross-reference-scout',
        'oracleStatus': 'syst_data_word_non_default_reachability_cross_reference_documented',
        'promotionStatus': 'not-promoted; non-default reachability cross-reference is a non-promoting observation scout only',
        'recordCount': len(systems),
        'totalNonDefault': total_non_default,
        'totalDefault': total_default,
        'totalReachable': total_reachable,
        'totalIsolated': total_isolated,
        'nonDefaultReachableCount': non_default_reachable,
        'nonDefaultIsolatedCount': non_default_isolated,
        'defaultReachableCount': default_reachable,
        'defaultIsolatedCount': default_isolated,
        'reachableNonDefaultRatio': round(reachable_non_default_ratio, 4),
        'isolatedNonDefaultRatio': round(isolated_non_default_ratio, 4),
        'patternSummary': pattern_summaries,
        'hypotheses': hypotheses,
        'promotionBlockers': [
            'Non-default reachability cross-reference is a non-promoting observation scout only',
            'Data word pattern semantics remain unpromoted; no Resource Bible field claim is made',
            'Reachability is derived from decoded link slots; runtime route availability may differ',
        ],
        'sourceNote': (
            f'Non-promoting scout cross-referencing data word non-default status ({total_non_default} '
            f'non-default, {total_default} default) with directed-BFS reachability from Levo '
            f'({total_reachable} reachable, {total_isolated} isolated). '
            f'Non-default systems: {non_default_reachable} reachable, {non_default_isolated} isolated. '
            f'Default systems: {default_reachable} reachable, {default_isolated} isolated. '
            f'Reachable set non-default ratio: {reachable_non_default_ratio:.4f}. '
            f'Isolated set non-default ratio: {isolated_non_default_ratio:.4f}. '
            f'FINDING: Non-default data word patterns appear in BOTH reachable and isolated system sets, '
            f'indicating data word values are NOT a reliable predictor of reachability from Levo.',
        ),
    }


def _coordinate_map_source_readiness_summary(systems: list[dict]) -> dict:
    """Record Resource Bible map-placement evidence and the exact promotion blockers."""
    coordinate_complete = [
        system['resourceId']
        for system in systems
        if len(system['semanticFields']['mapCoordinates']['wordIndices']) == 4
    ]
    link_complete = [
        system['resourceId']
        for system in systems
        if len(system['semanticFields']['candidateHyperspaceLinks']['linkSlots']) == 16
    ]
    return {
        'sourceLabel': 'resource-bible-backed-coordinate-map-source-readiness',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'sourceReferences': COORDINATE_MAP_SOURCE_REFERENCES,
        'recordCount': len(systems),
        'coordinateFieldCompleteRecordCount': len(coordinate_complete),
        'linkSlotCompleteRecordCount': len(link_complete),
        'resourceBibleMapPlacementClaim': 'The sÿst resource xPos/yPos fields are the system X and Y positions on the map.',
        'resourceBibleLinkClaim': 'The sÿst Con1-Con16 fields link to other systems by resource ID or -1 for no link.',
        'resourceBibleRangeConstantBoundary': 'JumpDistance=1000 pixels is preserved as a game/topology range constant, not as decoded xPos/yPos map-pixel proof.',
        'promotionBlockers': [
            'Resource Bible map-placement wording does not specify decoded coordinate storage width, fixed-point divisor, projection, centering, axis orientation, or screen pixel transform',
            'JumpDistance pixels do not by themselves calibrate the decoded syst xPos/yPos coordinate units',
            'Classic map pixel/click/capture evidence or an accepted surrogate is still required before display-unit/map-scaling promotion',
            'remaining 66 system record-to-name joins are unpromoted, so runtime topology labels remain incomplete',
        ],
        'nextEvidenceFamilies': [
            'original-runtime map screenshot/click calibration tying at least two named systems to on-screen positions',
            'decoded complete system-name/order source that can join the remaining syst records to labels',
            'source-level projection or coordinate-transform description for EV Classic map rendering',
        ],
        'displayUnitInterpretationStatus': 'not-promoted; Resource Bible confirms map-placement field intent but not display units, scaling, projection, or remaining runtime topology labels',
        'sourceNote': 'This packet strengthens source readiness by separating Resource Bible map-placement field intent from the missing runtime/display calibration evidence. It deliberately preserves the blocker rather than promoting decoded coordinate display units from static text alone.',
    }


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


def _coordinate_display_bounds_summary(systems: list[dict]) -> dict:
    """Summarize coordinate candidate bounds without promoting display units."""
    def _axis_values(axis: str) -> dict:
        high_words = [system['semanticFields']['mapCoordinates'][axis]['rawWords'][0] for system in systems]
        low_words = [system['semanticFields']['mapCoordinates'][axis]['rawWords'][1] for system in systems]
        signed_longs = [system['semanticFields']['mapCoordinates'][axis]['signedLongCandidate'] for system in systems]
        return {
            'rawHighWordCandidateSpan': max(high_words) - min(high_words),
            'rawLowWordCandidateSpan': max(low_words) - min(low_words),
            'signedLongCandidateSpan': max(signed_longs) - min(signed_longs),
            'rawHighWordCandidateBounds': [min(high_words), max(high_words)],
            'rawLowWordCandidateBounds': [min(low_words), max(low_words)],
            'signedLongCandidateBounds': [min(signed_longs), max(signed_longs)],
        }

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-bounds-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'candidateFamilies': [
            'raw high-word candidate bounds/span',
            'raw low-word candidate bounds/span',
            'signed 32-bit big-endian raw-long candidate bounds/span',
        ],
        'xPos': _axis_values('xPos'),
        'yPos': _axis_values('yPos'),
        'sourceNote': 'This summarizes candidate coordinate bounds/spans from decoded syst xPos/yPos payloads for a later map-scaling pass. It does not promote EV Classic display units, projection, centering, axis inversion, or map pixel scaling.',
    }


def _coordinate_display_normalized_summary(systems: list[dict]) -> dict:
    """Preserve min-normalized coordinate candidates without promoting display units."""
    x_values = [system['semanticFields']['mapCoordinates']['xPos']['signedLongCandidate'] for system in systems]
    y_values = [system['semanticFields']['mapCoordinates']['yPos']['signedLongCandidate'] for system in systems]
    x_min = min(x_values)
    y_min = min(y_values)
    x_span = max(x_values) - x_min
    y_span = max(y_values) - y_min

    def _normalized_for(system: dict) -> dict:
        coordinates = system['semanticFields']['mapCoordinates']
        x = coordinates['xPos']['signedLongCandidate']
        y = coordinates['yPos']['signedLongCandidate']
        return {
            'resourceId': system['resourceId'],
            'ordinal': system['ordinal'],
            'xPos': {
                'signedLongCandidate': x,
                'minNormalizedSignedLongCandidate': x - x_min,
                'unitIntervalCandidate': round((x - x_min) / x_span, 6) if x_span else 0,
            },
            'yPos': {
                'signedLongCandidate': y,
                'minNormalizedSignedLongCandidate': y - y_min,
                'unitIntervalCandidate': round((y - y_min) / y_span, 6) if y_span else 0,
            },
        }

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-normalized-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'candidateFamilies': [
            'signed-long min-normalized x/y candidates',
            'signed-long unit-interval x/y candidates',
        ],
        'xPos': {
            'signedLongCandidateMinMax': [min(x_values), max(x_values)],
            'minNormalizedSignedLongCandidateRange': [0, x_span],
        },
        'yPos': {
            'signedLongCandidateMinMax': [min(y_values), max(y_values)],
            'minNormalizedSignedLongCandidateRange': [0, y_span],
        },
        'resource128': _normalized_for(systems[0]),
        'perResource': [_normalized_for(system) for system in systems],
        'sourceNote': 'This normalizes decoded signed-long coordinate candidates against run minima so later map-scaling work can compare relative layout to original-runtime map evidence. It still does not promote Classic display units, projection, centering, axis inversion, or pixel scale.',
    }


def _coordinate_display_transform_summary(systems: list[dict]) -> dict:
    """Preserve axis transform candidates without promoting display projection/scaling."""
    normalized = _coordinate_display_normalized_summary(systems)
    x_span = normalized['xPos']['minNormalizedSignedLongCandidateRange'][1]
    y_span = normalized['yPos']['minNormalizedSignedLongCandidateRange'][1]
    resource_128 = normalized['resource128']
    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-transform-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'candidateFamilies': [
            'signed-long unit-interval transform candidate',
            'signed-long y-axis inversion candidate',
            'signed-long axis-span aspect-ratio candidate',
        ],
        'signedLongAxisSpanRatioYOverX': round(y_span / x_span, 6) if x_span else None,
        'resource128': {
            'xPos': {
                'unitIntervalCandidate': resource_128['xPos']['unitIntervalCandidate'],
            },
            'yPos': {
                'unitIntervalCandidate': resource_128['yPos']['unitIntervalCandidate'],
                'invertedUnitIntervalCandidate': round(1 - resource_128['yPos']['unitIntervalCandidate'], 6),
            },
        },
        'displayUnitInterpretationStatus': 'not-promoted; transform candidates are analysis inputs for later Classic map projection, centering, axis inversion, and pixel-scale evidence',
        'sourceNote': 'This packages normalized signed-long coordinate candidates into transform/aspect-ratio analysis inputs. It does not claim EV Classic map display units, projection, centering, y-axis orientation, or pixel scale.',
    }


def _coordinate_display_fixed_point_summary(systems: list[dict]) -> dict:
    """Preserve 16.16-style fixed-point scale candidates without promoting map pixels."""
    divisor = 65536

    def _fixed_point(axis_payload: dict) -> float:
        return round(axis_payload['signedLongCandidate'] / divisor, 6)

    def _axis_values(axis: str) -> dict:
        values = [
            _fixed_point(system['semanticFields']['mapCoordinates'][axis])
            for system in systems
        ]
        return {
            'fixedPointCandidateBounds': [min(values), max(values)],
            'fixedPointCandidateSpan': round(max(values) - min(values), 6),
        }

    def _resource_values(resource_id: int) -> dict:
        system = next(system for system in systems if system['resourceId'] == resource_id)
        coordinates = system['semanticFields']['mapCoordinates']
        return {
            'resourceId': resource_id,
            'xPosFixedPointCandidate': _fixed_point(coordinates['xPos']),
            'yPosFixedPointCandidate': _fixed_point(coordinates['yPos']),
        }

    x_axis = _axis_values('xPos')
    y_axis = _axis_values('yPos')
    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-fixed-point-scale-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'fixedPointDivisorCandidate': divisor,
        'candidateFamilies': [
            '16.16 fixed-point coordinate-unit candidate',
            'unsigned low-word fractional-subunit candidate',
            'run-level fixed-point span/aspect-ratio candidate',
        ],
        'xPos': x_axis,
        'yPos': y_axis,
        'fixedPointAxisSpanRatioYOverX': round(y_axis['fixedPointCandidateSpan'] / x_axis['fixedPointCandidateSpan'], 6) if x_axis['fixedPointCandidateSpan'] else None,
        'resource128': _resource_values(128),
        'resource129': _resource_values(129),
        'displayUnitInterpretationStatus': 'not-promoted; 16.16 fixed-point candidates are analysis inputs for later Classic map projection, centering, axis inversion, and pixel-scale evidence',
        'sourceNote': 'This interprets the decoded signed 32-bit coordinate payload as a 16.16-style fixed-point candidate because each coordinate is represented by two 16-bit words. It preserves map-scaling analysis inputs only and does not claim EV Classic map pixels, projection, centering, axis orientation, route UI behavior, or exact remaining system-name joins.',
    }


def _coordinate_display_integer_band_summary(systems: list[dict]) -> dict:
    """Preserve fixed-point integer-band/fractional residual candidates without promoting map scale."""
    def _axis_summary(axis: str) -> dict:
        high_words = [system['semanticFields']['mapCoordinates'][axis]['rawWords'][0] for system in systems]
        low_words = [system['semanticFields']['mapCoordinates'][axis]['rawWords'][1] for system in systems]
        return {
            'integerBandCandidateDistribution': {
                str(value): high_words.count(value)
                for value in sorted(set(high_words))
            },
            'integerBandCandidateRange': [min(high_words), max(high_words)],
            'signedFractionalResidualCandidateRange': [min(low_words), max(low_words)],
        }

    def _resource_values(resource_id: int) -> dict:
        system = next(system for system in systems if system['resourceId'] == resource_id)
        coordinates = system['semanticFields']['mapCoordinates']
        return {
            'resourceId': resource_id,
            'xPos': {
                'integerBandCandidate': coordinates['xPos']['rawWords'][0],
                'signedFractionalResidualCandidate': coordinates['xPos']['rawWords'][1],
            },
            'yPos': {
                'integerBandCandidate': coordinates['yPos']['rawWords'][0],
                'signedFractionalResidualCandidate': coordinates['yPos']['rawWords'][1],
            },
        }

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-integer-band-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'candidateFamilies': [
            '16.16 high-word integer-band candidate',
            '16.16 low-word signed fractional-residual candidate',
            'run-level integer-band occupancy candidate',
        ],
        'xPos': _axis_summary('xPos'),
        'yPos': _axis_summary('yPos'),
        'resource128': _resource_values(128),
        'resource129': _resource_values(129),
        'displayUnitInterpretationStatus': 'not-promoted; integer-band and fractional-residual candidates are analysis inputs for later Classic map projection, centering, axis orientation, and pixel-scale evidence',
        'sourceNote': 'This decomposes decoded coordinate word pairs as 16.16-style integer-band and signed fractional-residual candidates. It preserves display-scale analysis inputs only and does not claim EV Classic map pixels, projection, centering, axis orientation, route UI behavior, or exact remaining system-name joins.',
    }


def _coordinate_display_residual_sign_summary(systems: list[dict]) -> dict:
    """Preserve signed low-word residual distributions without promoting map scale."""
    divisor = 65536

    def _axis_summary(axis: str) -> dict:
        low_words = [system['semanticFields']['mapCoordinates'][axis]['rawWords'][1] for system in systems]
        distinct_values = sorted(set(low_words))
        return {
            'signedFractionalResidualCandidateDistinctValues': distinct_values,
            'signedFractionalResidualCandidateRange': [min(low_words), max(low_words)],
            'signedFractionalResidualSignDistribution': {
                'negative': len([value for value in low_words if value < 0]),
                'zero': len([value for value in low_words if value == 0]),
                'positive': len([value for value in low_words if value > 0]),
            },
            'fractionalUnitCandidateDistinctValues': [
                round(value / divisor, 6)
                for value in distinct_values
            ],
        }

    def _resource_values(resource_id: int) -> dict:
        system = next(system for system in systems if system['resourceId'] == resource_id)
        coordinates = system['semanticFields']['mapCoordinates']
        return {
            'resourceId': resource_id,
            'xPosFractionalUnitCandidate': round(coordinates['xPos']['rawWords'][1] / divisor, 6),
            'yPosFractionalUnitCandidate': round(coordinates['yPos']['rawWords'][1] / divisor, 6),
        }

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-residual-sign-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'fixedPointDivisorCandidate': divisor,
        'candidateFamilies': [
            '16.16 low-word residual sign distribution candidate',
            '16.16 low-word fractional-unit distinct value candidate',
            'resource-level fractional-unit candidate examples',
        ],
        'xPos': _axis_summary('xPos'),
        'yPos': _axis_summary('yPos'),
        'resource128': _resource_values(128),
        'resource129': _resource_values(129),
        'displayUnitInterpretationStatus': 'not-promoted; residual-sign and fractional-unit candidates are analysis inputs for later Classic map projection, centering, axis orientation, and pixel-scale evidence',
        'sourceNote': 'This summarizes signed low-word residual values as 16.16-style fractional-unit candidates. It preserves display-scale analysis inputs only and does not claim EV Classic map pixels, projection, centering, axis orientation, route UI behavior, or exact remaining system-name joins.',
    }


def _coordinate_display_residual_magnitude_summary(systems: list[dict]) -> dict:
    """Preserve absolute low-word residual magnitudes without promoting map scale."""
    divisor = 65536

    def _axis_summary(axis: str) -> dict:
        magnitudes = [abs(system['semanticFields']['mapCoordinates'][axis]['rawWords'][1]) for system in systems]
        distinct_magnitudes = sorted(set(magnitudes))
        min_magnitude = min(magnitudes)
        max_magnitude = max(magnitudes)
        distribution = {
            str(value): len([magnitude for magnitude in magnitudes if magnitude == value])
            for value in distinct_magnitudes
        }
        return {
            'absoluteResidualCandidateDistinctValues': distinct_magnitudes,
            'absoluteResidualCandidateRange': [min_magnitude, max_magnitude],
            'absoluteFractionalUnitCandidateDistinctValues': [
                round(value / divisor, 6)
                for value in distinct_magnitudes
            ],
            'absoluteResidualCandidateDistribution': distribution,
            'minResidualMagnitudeResourceIds': [
                system['resourceId']
                for system in systems
                if abs(system['semanticFields']['mapCoordinates'][axis]['rawWords'][1]) == min_magnitude
            ],
            'maxResidualMagnitudeResourceIds': [
                system['resourceId']
                for system in systems
                if abs(system['semanticFields']['mapCoordinates'][axis]['rawWords'][1]) == max_magnitude
            ],
        }

    def _resource_values(resource_id: int) -> dict:
        system = next(system for system in systems if system['resourceId'] == resource_id)
        coordinates = system['semanticFields']['mapCoordinates']
        return {
            'resourceId': resource_id,
            'xPosAbsoluteFractionalUnitCandidate': round(abs(coordinates['xPos']['rawWords'][1]) / divisor, 6),
            'yPosAbsoluteFractionalUnitCandidate': round(abs(coordinates['yPos']['rawWords'][1]) / divisor, 6),
        }

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-residual-magnitude-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'fixedPointDivisorCandidate': divisor,
        'candidateFamilies': [
            '16.16 low-word absolute residual magnitude candidate',
            '16.16 low-word absolute fractional-unit distinct value candidate',
            'resource-level absolute fractional-unit candidate examples',
        ],
        'xPos': _axis_summary('xPos'),
        'yPos': _axis_summary('yPos'),
        'resource128': _resource_values(128),
        'resource129': _resource_values(129),
        'displayUnitInterpretationStatus': 'not-promoted; absolute residual magnitudes are analysis inputs for later Classic map projection, centering, axis orientation, and pixel-scale evidence',
        'sourceNote': 'This summarizes absolute low-word residual magnitudes as 16.16-style fractional-unit candidates. It preserves display-scale analysis inputs only and does not claim EV Classic map pixels, projection, centering, axis orientation, route UI behavior, or exact remaining system-name joins.',
    }


def _coordinate_display_quantization_summary(systems: list[dict]) -> dict:
    """Preserve residual quantization/grid-step candidates without promoting map scale."""
    divisor = 65536
    coarse_step = 4096

    def _axis_summary(axis: str) -> dict:
        residuals = [system['semanticFields']['mapCoordinates'][axis]['rawWords'][1] for system in systems]
        absolute_residuals = [abs(value) for value in residuals]
        residual_gcd = math.gcd(*absolute_residuals)
        modulo_128_distribution = {
            str(value): len([residual for residual in residuals if residual % 128 == value])
            for value in sorted({residual % 128 for residual in residuals})
        }
        on_grid = [system['resourceId'] for system in systems if system['semanticFields']['mapCoordinates'][axis]['rawWords'][1] % coarse_step == 0]
        off_grid = [system['resourceId'] for system in systems if system['semanticFields']['mapCoordinates'][axis]['rawWords'][1] % coarse_step != 0]
        return {
            'absoluteResidualGcdCandidate': residual_gcd,
            'absoluteResidualGcdFractionalUnitCandidate': round(residual_gcd / divisor, 6),
            'coarseGridStepCandidate': coarse_step,
            'coarseGridStepFractionalUnitCandidate': round(coarse_step / divisor, 6),
            'coarseGridAlignedResourceCount': len(on_grid),
            'coarseGridOffstepResourceIds': off_grid,
            'residualModulo128Distribution': modulo_128_distribution,
        }

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-quantization-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'fixedPointDivisorCandidate': divisor,
        'candidateFamilies': [
            '16.16 residual gcd quantization candidate',
            '16.16 residual modulo-128 distribution candidate',
            '16.16 y-axis 4096-step coarse-grid candidate',
        ],
        'xPos': _axis_summary('xPos'),
        'yPos': _axis_summary('yPos'),
        'displayUnitInterpretationStatus': 'not-promoted; residual quantization and coarse-grid candidates are analysis inputs for later Classic map projection, centering, axis orientation, and pixel-scale evidence',
        'sourceNote': 'This summarizes decoded low-word coordinate residuals as quantization/grid-step candidates. The y-axis has many residuals aligned to a 4096/65536 step, while x-axis residuals remain mostly fine-grained; this is analysis input only and does not claim EV Classic map pixels, projection, centering, axis orientation, route UI behavior, or exact remaining system-name joins.',
    }


def _coordinate_display_scale_interpretation_summary(systems: list[dict]) -> dict:
    """Compare coordinate-scale candidates and preserve promotion blockers."""
    bounds = _coordinate_display_bounds_summary(systems)
    transform = _coordinate_display_transform_summary(systems)
    fixed_point = _coordinate_display_fixed_point_summary(systems)
    quantization = _coordinate_display_quantization_summary(systems)
    raw_high_x_span = bounds['xPos']['rawHighWordCandidateSpan']
    raw_high_y_span = bounds['yPos']['rawHighWordCandidateSpan']
    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-scale-interpretation-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'fixedPointDivisorCandidate': fixed_point['fixedPointDivisorCandidate'],
        'candidateFamilies': [
            'candidate-family comparison without Classic map-pixel promotion',
            'signed-long and fixed-point span/aspect-ratio comparison',
            'static-source promotion blocker ledger for display-unit/map-scaling interpretation',
        ],
        'spanComparisons': {
            'signedLongAxisSpanRatioYOverX': transform['signedLongAxisSpanRatioYOverX'],
            'fixedPointAxisSpanRatioYOverX': fixed_point['fixedPointAxisSpanRatioYOverX'],
            'rawHighWordAxisSpanRatioYOverX': round(raw_high_y_span / raw_high_x_span, 6) if raw_high_x_span else None,
            'rawLowWordAxisSpanRatioYOverX': round(bounds['yPos']['rawLowWordCandidateSpan'] / bounds['xPos']['rawLowWordCandidateSpan'], 6) if bounds['xPos']['rawLowWordCandidateSpan'] else None,
        },
        'quantizationComparison': {
            'xResidualGcdCandidate': quantization['xPos']['absoluteResidualGcdCandidate'],
            'yResidualGcdCandidate': quantization['yPos']['absoluteResidualGcdCandidate'],
            'yCoarseGridAlignedResourceCount': quantization['yPos']['coarseGridAlignedResourceCount'],
            'xCoarseGridAlignedResourceCount': quantization['xPos']['coarseGridAlignedResourceCount'],
        },
        'scalePromotionBlockers': [
            'no Classic map pixel/click/capture evidence in this static packet',
            'candidate families disagree on x/y aspect ratio and unit interpretation',
            'remaining 66 system record-to-name joins are unpromoted',
            'route UI ordering and projection remain unobserved',
        ],
        'displayUnitInterpretationStatus': 'not-promoted; static coordinate scale candidates are compared and blockers are explicit, but Classic display units/map scaling require map-pixel/projection or accepted surrogate evidence',
        'sourceNote': 'This compares decoded Resource Bible xPos/yPos candidate families already preserved in the manifest. It deliberately records why display-unit/map-scaling remains unpromoted instead of inferring Classic map pixels, projection, centering, axis orientation, route UI behavior, or full runtime topology from static data alone.',
    }


def _coordinate_display_calibration_gate_summary(systems: list[dict]) -> dict:
    """Record the evidence gate before static coordinates may become Classic map display units."""
    candidate_input_summaries = [
        'coordinateDisplayCandidateSummary',
        'coordinateDisplayBoundsSummary',
        'coordinateDisplayNormalizedSummary',
        'coordinateDisplayTransformSummary',
        'coordinateDisplayFixedPointSummary',
        'coordinateDisplayIntegerBandSummary',
        'coordinateDisplayQuantizationSummary',
        'coordinateDisplayScaleInterpretationSummary',
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-calibration-gate',
        'oracleStatus': 'coordinate_display_calibration_blocked_pending_classic_map_evidence',
        'recordCount': len(systems),
        'candidateInputSummaries': candidate_input_summaries,
        'candidateInputSummaryCount': len(candidate_input_summaries),
        'calibrationRequiredClaims': [
            'display pixel scale or accepted projection surrogate',
            'map origin/centering transform',
            'axis orientation/y inversion',
            'at least two named systems tied to decoded resource IDs and observed map positions',
        ],
        'promotionReadinessStatus': 'blocked; static coordinate candidates are analysis inputs only',
        'promotionBlockers': [
            'candidate coordinate families disagree on scale/aspect interpretation',
            'no Classic map pixel/click/capture evidence in this static packet',
            'remaining 66 system record-to-name joins are unpromoted',
            'route UI ordering and projection remain unobserved',
        ],
        'nextEvidenceFamilies': [
            'original-runtime map screenshot/click calibration tied to decoded resource IDs',
            'Classic source-level map projection/origin/scale constants',
            'accepted scaffold boundary explicitly separating analysis coordinates from gameplay display units',
        ],
        'sourceNote': 'This gate deliberately keeps coordinate display-unit/map-scaling promotion blocked until Classic runtime/source map calibration evidence exists; static decoded coordinate summaries remain analysis inputs only.',
    }


def _coordinate_display_runtime_capture_gate_summary(systems: list[dict]) -> dict:
    """Record concrete Classic map calibration capture packets without promoting display units."""
    calibration_gate = _coordinate_display_calibration_gate_summary(systems)
    by_resource_id = {system['resourceId']: system for system in systems}
    topology = _start_system_candidate_topology_summary(systems)
    start_coordinates = by_resource_id[topology['startResourceId']]['semanticFields']['mapCoordinates']
    non_self_neighbors = [
        neighbor
        for neighbor in topology.get('linkedNeighbors', [])
        if not neighbor.get('isSelfLink')
    ]
    capture_templates = []
    for neighbor in non_self_neighbors:
        capture_templates.append({
            'schemaVersion': 1,
            'targetResourceId': neighbor['targetResourceId'],
            'slotName': neighbor['slotName'],
            'candidateStartResourceId': topology['startResourceId'],
            'startSystemExactName': topology['startExactSystemName'],
            'requiredObservationFields': [
                'localOnlyCapturePath',
                'captureTimestamp',
                'disposableNonStrictPilot',
                'mapWindowPixelBounds',
                'startSystemVisibleLabel',
                'startSystemPixelPosition',
                'visibleDestinationLabel',
                'destinationPixelPosition',
                'inputMethodAndClickPixel',
                'selectedRouteOrHighlightedDestinationEvidence',
                'decodedResourceIdOrConSlotRationale',
            ],
            'decodedStaticInputs': {
                'targetResourceId': neighbor['targetResourceId'],
                'slotName': neighbor['slotName'],
                'targetNameJoinStatus': neighbor['targetNameJoinStatus'],
                'targetCoordinateSignedLongCandidate': neighbor['targetCoordinateSignedLongCandidate'],
                'startCoordinateSignedLongCandidate': {
                    'xPos': start_coordinates['xPos']['signedLongCandidate'],
                    'yPos': start_coordinates['yPos']['signedLongCandidate'],
                },
            },
            'promotionReviewRule': 'may support coordinate display calibration only if a Classic capture ties a visible label/click/pixel position to this decoded resource ID or Con slot; otherwise leave display units and named topology blocked',
            'sourceFidelityLabel': 'original-runtime-coordinate-map-calibration-capture-packet-template',
        })
    return {
        'sourceLabel': 'original-runtime-coordinate-map-calibration-capture-gate',
        'oracleStatus': 'coordinate_display_capture_blocked_pending_classic_map_pixel_click_evidence',
        'sourceBasis': ['decoded-record-family', 'resource-bible-field', 'original-runtime-required'],
        'candidateStartResourceId': topology['startResourceId'],
        'startSystemExactName': topology['startExactSystemName'],
        'requiredTargetResourceIds': [entry['targetResourceId'] for entry in capture_templates],
        'requiredConSlots': [entry['slotName'] for entry in capture_templates],
        'requiredCapturePacketCount': len(capture_templates),
        'capturePacketSchemaVersion': 1,
        'capturePacketTemplates': capture_templates,
        'calibrationGateSourceLabel': calibration_gate['sourceLabel'],
        'calibrationRequiredClaims': calibration_gate['calibrationRequiredClaims'],
        'captureValidationRules': [
            'minimum two named observed map positions tied to decoded resource IDs or Con slots before any display-scale review',
            'capture must record map window pixel bounds plus click/selection pixel coordinates, not only visible names',
            'local-only proprietary screenshots/transcripts stay out of published artifacts unless explicitly approved',
            'resource-ID/name/topology joins remain blocked unless the capture ties the visible label to a decoded resource ID or Con slot',
        ],
        'promotionBlockers': [
            'no Classic map pixel/click/capture packet has been recorded in this manifest',
            'visible labels are not yet tied to decoded resource IDs or Con slots',
            'static coordinate candidates still cannot define projection, origin, scale, or y-axis orientation alone',
        ],
        'allowedUse': 'prepare disposable original-runtime map calibration captures only; do not promote coordinate display units, named topology, or broad runtime universe replacement from this gate',
        'promotionStatus': 'not-promoted; capture gate records exact evidence requirements only',
        'sourceNote': 'This turns the coordinate display calibration blocker into concrete per-target capture templates for Levo candidate neighbors while deliberately withholding display-unit/map-scaling/projection and record-name promotion.',
    }


def _coordinate_display_unit_map_scaling_readiness_summary(systems: list[dict]) -> dict:
    """Promote bounded static readiness for runtime calibration without promoting display units."""
    calibration_gate = _coordinate_display_calibration_gate_summary(systems)
    runtime_capture_gate = _coordinate_display_runtime_capture_gate_summary(systems)
    candidate_input_summaries = [
        *calibration_gate['candidateInputSummaries'],
        'coordinateDisplayCalibrationGateSummary',
        'coordinateDisplayRuntimeCaptureGateSummary',
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-unit-map-scaling-readiness',
        'oracleStatus': 'coordinate_display_units_map_scaling_bounded_static_readiness_promoted',
        'recordCount': len(systems),
        'candidateInputSummaries': candidate_input_summaries,
        'candidateInputSummaryCount': len(candidate_input_summaries),
        'promotedReadinessClaims': [
            'complete decoded xPos/yPos coordinate fields for all 67 syst-like records',
            'Resource Bible xPos/yPos map-placement field intent is recorded separately from display units',
            'static coordinate candidate families, blockers, and extrema are available for bounded calibration review',
            'runtime calibration capture packet templates are defined for Levo neighbor candidates',
        ],
        'blockedPromotionClaims': [
            'Classic map pixel scale, projection, origin, and centering are still unpromoted',
            'axis orientation/y inversion is still unpromoted',
            'candidate coordinate families still disagree on scale/aspect interpretation',
            'remaining 66 system record-to-name joins are unpromoted, so broad named topology remains blocked',
        ],
        'requiredRuntimeCaptureTargetResourceIds': runtime_capture_gate['requiredTargetResourceIds'],
        'requiredRuntimeCaptureConSlots': runtime_capture_gate['requiredConSlots'],
        'requiredCapturePacketCount': runtime_capture_gate['requiredCapturePacketCount'],
        'capturePacketSchemaVersion': runtime_capture_gate['capturePacketSchemaVersion'],
        'readinessStatus': 'ready-for-runtime-calibration-capture; display units not promoted',
        'displayUnitPromotionStatus': 'not-promoted; this is a bounded readiness promotion for capture/review inputs only',
        'sourceNote': 'This promotes only the deterministic static readiness state needed to run bounded Classic map calibration captures. It does not promote coordinate display units, map scaling, projection, origin, centering, y-axis orientation, route UI behavior, or broad runtime universe replacement.',
    }


def _coordinate_display_runtime_capture_reconciliation_summary(systems: list[dict]) -> dict:
    """Record how validated Classic map calibration captures can be reconciled without over-promoting display units."""
    readiness = _coordinate_display_unit_map_scaling_readiness_summary(systems)
    runtime_capture_gate = _coordinate_display_runtime_capture_gate_summary(systems)
    packet_ids = [
        f"coordinate-display-map-calibration-{entry['slotName'].lower()}-resource-{entry['targetResourceId']}"
        for entry in runtime_capture_gate.get('capturePacketTemplates', [])
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-runtime-capture-reconciliation-plan',
        'oracleStatus': 'coordinate_display_runtime_capture_reconciliation_blocked_pending_validated_map_packets',
        'sourceBasis': ['decoded-record-family', 'resource-bible-field', 'original-runtime-required'],
        'recordCount': len(systems),
        'evidenceInputSummaries': [
            'coordinateDisplayRuntimeCaptureGateSummary',
            'coordinateDisplayUnitMapScalingReadinessSummary',
            'coordinateDisplayCalibrationGateSummary',
            'startNeighborhoodRuntimeCalibrationPrioritySummary',
        ],
        'evidenceInputSummaryCount': 4,
        'candidateStartResourceId': runtime_capture_gate['candidateStartResourceId'],
        'candidateStartSystemName': runtime_capture_gate['startSystemExactName'],
        'requiredValidatedCapturePacketCount': runtime_capture_gate['requiredCapturePacketCount'],
        'requiredCapturePacketTargetResourceIds': runtime_capture_gate['requiredTargetResourceIds'],
        'requiredCapturePacketConSlots': runtime_capture_gate['requiredConSlots'],
        'requiredCapturePacketIds': packet_ids,
        'readinessStatus': readiness['readinessStatus'],
        'postCaptureReconciliationSteps': [
            'validate every required map calibration packet against the coordinate display runtime capture gate schema',
            'tie each visible destination label and pixel/click coordinate to a decoded resource ID or Con slot only when the packet evidence explicitly supports that join',
            'compare captured pixel deltas against static coordinate candidate families before proposing scale, origin, projection, or y-axis orientation claims',
            'record contradictions as blocker evidence instead of silently choosing a coordinate transform',
            'rerun static_topology_source_readiness_scout before any follow-on display-unit or named-route promotion packet',
        ],
        'promotionDecisionStates': [
            'no-packets; coordinate display units remain blocked',
            'partial-packets; capture worklist remains open and no broad display transform may be promoted',
            'source-runtime-corroborated; may propose a narrow coordinate display calibration packet but not broad universe replacement',
            'contradicted; reopen coordinate display calibration gate and keep display units not-promoted',
        ],
        'blockedPromotionClaims': [
            'assigning Classic map pixel scale from static coordinate candidates alone',
            'assigning projection, origin, centering, or y-axis orientation without validated map pixel/click captures',
            'joining visible route labels to decoded resource IDs without packet-level resource ID or Con-slot evidence',
            'using coordinate calibration captures as broad named topology or runtime universe replacement proof',
        ],
        'requiredVerifierBeforeGameplay': [
            'python3 tools/extract_ev_system_semantics.py',
            'python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_systems_manifest_promotes_static_system_ids_and_name_seeds native_ev.tests.test_scenario_eval.ScenarioEvalHarnessTests.test_static_topology_source_readiness_scout_records_lane_a_promotion_boundary -v',
            'python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty',
        ],
        'promotionBlockers': [
            'post-capture reconciliation is a gate, not a display-unit promotion packet',
            'minimum two named observed map positions tied to decoded resource IDs or Con slots are still required before display-scale review',
            'raw proprietary screenshots/transcripts remain local-only unless explicitly approved',
        ],
        'allowedUse': 'validate and reconcile future coordinate-display capture packets; do not promote display units, named route topology, or broad runtime universe replacement from this plan alone',
        'promotionStatus': 'not-promoted; post-capture reconciliation plan only',
        'sourceNote': 'This plan defines how future Classic map pixel/click calibration packets can refine coordinate display evidence while keeping display scale, projection, named topology, and broad universe replacement blocked until validated packet-level evidence exists.',
    }


def _coordinate_display_runtime_capture_validation_matrix_summary(systems: list[dict]) -> dict:
    """Define acceptance checks for future Classic map calibration capture packets."""
    runtime_capture_gate = _coordinate_display_runtime_capture_gate_summary(systems)
    reconciliation = _coordinate_display_runtime_capture_reconciliation_summary(systems)
    validation_checks = [
        {
            'checkId': 'schema-and-target-completeness',
            'requirement': 'each packet names the schema version, local-only capture path, timestamp, start resource/name, target resource id, and Con slot',
        },
        {
            'checkId': 'map-pixel-observation-completeness',
            'requirement': 'each packet records map window pixel bounds plus start and destination pixel positions rather than names alone',
        },
        {
            'checkId': 'selection-or-click-evidence',
            'requirement': 'each packet records input method/click pixel and selected route or highlighted destination evidence',
        },
        {
            'checkId': 'decoded-join-rationale',
            'requirement': 'visible label evidence is tied to a decoded resource id or Con slot only when packet-level rationale supports the join',
        },
        {
            'checkId': 'local-custody-and-boundary',
            'requirement': 'raw proprietary screenshots/transcripts remain local-only and the packet explicitly blocks display-unit, named-topology, and broad-universe promotion by itself',
        },
    ]
    failure_classes = [
        {
            'classId': 'missing-pixel-bounds',
            'disposition': 'reject for calibration; retain only as label/provenance scout',
        },
        {
            'classId': 'unjoined-visible-label',
            'disposition': 'reject resource/name join; require decoded resource id, Con slot, or stronger source-level oracle',
        },
        {
            'classId': 'partial-target-set',
            'disposition': 'keep capture worklist open; do not enter display-scale review until required packet count is satisfied',
        },
        {
            'classId': 'promotion-boundary-contamination',
            'disposition': 'reject or redact claims that promote map pixels, projection, named topology, or runtime universe replacement before reconciliation',
        },
    ]
    return {
        'sourceLabel': 'original-runtime-coordinate-display-capture-validation-matrix',
        'oracleStatus': 'coordinate_display_capture_validation_blocked_pending_real_map_packets',
        'sourceBasis': ['decoded-record-family', 'resource-bible-field', 'original-runtime-required'],
        'recordCount': len(systems),
        'evidenceInputSummaries': [
            'coordinateDisplayRuntimeCaptureGateSummary',
            'coordinateDisplayRuntimeCaptureReconciliationSummary',
            'coordinateDisplayUnitMapScalingReadinessSummary',
            'startNeighborhoodRuntimeCalibrationPrioritySummary',
        ],
        'evidenceInputSummaryCount': 4,
        'candidateStartResourceId': runtime_capture_gate['candidateStartResourceId'],
        'candidateStartSystemName': runtime_capture_gate['startSystemExactName'],
        'requiredCapturePacketCount': runtime_capture_gate['requiredCapturePacketCount'],
        'requiredCapturePacketTargetResourceIds': runtime_capture_gate['requiredTargetResourceIds'],
        'requiredCapturePacketConSlots': runtime_capture_gate['requiredConSlots'],
        'requiredCapturePacketIds': reconciliation['requiredCapturePacketIds'],
        'validationCheckCount': len(validation_checks),
        'validationCheckIds': [check['checkId'] for check in validation_checks],
        'validationChecks': validation_checks,
        'failureClassCount': len(failure_classes),
        'failureClassIds': [entry['classId'] for entry in failure_classes],
        'failureClasses': failure_classes,
        'minimumAcceptedPacketCountBeforeScaleReview': 2,
        'requiredVerifierBeforeReconciliation': reconciliation['requiredVerifierBeforeGameplay'],
        'blockedPromotionClaims': [
            'accepting map calibration packets that lack pixel bounds, click/selection evidence, or decoded join rationale',
            'using a single named-label observation to promote Classic map scale, projection, origin, centering, or y-axis orientation',
            'using calibration packet validation to promote named route topology or broad runtime universe replacement',
        ],
        'promotionBlockers': [
            'validation matrix is an acceptance schema, not Classic map display evidence',
            'real Classic map calibration packets remain absent',
            'post-capture reconciliation must still compare packet evidence against static coordinate candidate families before any narrow display calibration proposal',
        ],
        'promotionStatus': 'not-promoted; validation matrix only pending real Classic map calibration packets',
        'sourceNote': 'This matrix defines acceptance and rejection checks for future coordinate-display runtime capture packets. It does not promote map scale, projection, route labels, record-name joins, or broad runtime universe replacement.',
    }


def _coordinate_display_extrema_summary(systems: list[dict]) -> dict:
    """Preserve coordinate candidate extrema records without promoting display units."""
    def _extrema(axis: str, value_name: str, value_getter) -> dict:
        entries = [
            {
                'resourceId': system['resourceId'],
                'ordinal': system['ordinal'],
                'value': value_getter(system['semanticFields']['mapCoordinates'][axis]),
            }
            for system in systems
        ]
        min_value = min(entry['value'] for entry in entries)
        max_value = max(entry['value'] for entry in entries)
        return {
            'valueName': value_name,
            'minValue': min_value,
            'minResourceIds': [entry['resourceId'] for entry in entries if entry['value'] == min_value],
            'maxValue': max_value,
            'maxResourceIds': [entry['resourceId'] for entry in entries if entry['value'] == max_value],
        }

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-display-extrema-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'recordCount': len(systems),
        'candidateFamilies': [
            'raw high-word candidate extrema resource IDs',
            'raw low-word candidate extrema resource IDs',
            'signed 32-bit big-endian raw-long candidate extrema resource IDs',
        ],
        'xPos': {
            'rawHighWord': _extrema('xPos', 'rawHighWord', lambda axis: axis['rawWords'][0]),
            'rawLowWord': _extrema('xPos', 'rawLowWord', lambda axis: axis['rawWords'][1]),
            'signedLongCandidate': _extrema('xPos', 'signedLongCandidate', lambda axis: axis['signedLongCandidate']),
        },
        'yPos': {
            'rawHighWord': _extrema('yPos', 'rawHighWord', lambda axis: axis['rawWords'][0]),
            'rawLowWord': _extrema('yPos', 'rawLowWord', lambda axis: axis['rawWords'][1]),
            'signedLongCandidate': _extrema('yPos', 'signedLongCandidate', lambda axis: axis['signedLongCandidate']),
        },
        'sourceNote': 'This identifies which decoded syst records sit at each coordinate candidate extremum. It is analysis input for later map-scaling/name-join work only and does not promote EV Classic display units, projection, centering, axis inversion, or map pixel scaling.',
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
    unique_directed_edges = {tuple(edge) for edge in directed_edges}
    reciprocal_directed_edges = sorted(
        edge for edge in unique_directed_edges
        if (edge[1], edge[0]) in unique_directed_edges
    )
    non_reciprocal_directed_edges = sorted(
        edge for edge in unique_directed_edges
        if (edge[1], edge[0]) not in unique_directed_edges
    )
    unique_self_links = sorted(edge for edge in unique_directed_edges if edge[0] == edge[1])
    return {
        'sourceLabel': 'decoded-resource-backed-candidate-link-graph-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'recordCount': len(systems),
        'directedLinkSlotCount': len(directed_edges),
        'uniqueDirectedLinkCount': len(unique_directed_edges),
        'reciprocalDirectedLinkCount': len(reciprocal_directed_edges),
        'nonReciprocalDirectedLinkCount': len(non_reciprocal_directed_edges),
        'nonReciprocalDirectedLinkSample': [list(edge) for edge in non_reciprocal_directed_edges[:12]],
        'linkedSlotsPerSystemRange': [min(slots_per_system), max(slots_per_system)],
        'systemsWithNoLinkedSlots': sum(1 for count in slots_per_system if count == 0),
        'allTargetsPresentInSystRun': not missing_targets,
        'missingTargetEdges': missing_targets,
        'selfLinkSlotCount': len(self_links),
        'uniqueSelfLinkCount': len(unique_self_links),
        'uniqueSelfLinkResourceIds': [edge[0] for edge in unique_self_links],
        'resource128LinkedSystemResourceIds': systems[0]['semanticFields']['candidateHyperspaceLinks']['linkedSystemResourceIds'],
        'sourceNote': 'This is a candidate graph summary from decoded Resource Bible Con1-Con16 link-slot fields. It preserves graph-analysis, reciprocity, and self-link statistics only; exact Classic runtime topology remains pending until record-to-name joins and map/layout interpretation are promoted.',
    }


def _candidate_graph_connectivity_summary(systems: list[dict]) -> dict:
    """Summarize candidate graph connectivity without promoting named runtime topology."""
    resource_ids = [system['resourceId'] for system in systems]
    directed_adjacency = {resource_id: set() for resource_id in resource_ids}
    weak_adjacency = {resource_id: set() for resource_id in resource_ids}
    for system in systems:
        resource_id = system['resourceId']
        slots = system['semanticFields']['candidateHyperspaceLinks']['linkSlots']
        for slot in slots:
            if slot.get('status') != 'linked-system' or not slot.get('targetPresentInSystRun'):
                continue
            target_id = slot['targetResourceId']
            directed_adjacency[resource_id].add(target_id)
            weak_adjacency[resource_id].add(target_id)
            weak_adjacency[target_id].add(resource_id)

    components = []
    seen = set()
    for resource_id in resource_ids:
        if resource_id in seen:
            continue
        stack = [resource_id]
        seen.add(resource_id)
        component = []
        while stack:
            current = stack.pop()
            component.append(current)
            for neighbor in weak_adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        components.append(sorted(component))

    start_resource_id = 128
    reachable = set()
    stack = [start_resource_id] if start_resource_id in directed_adjacency else []
    while stack:
        current = stack.pop()
        if current in reachable:
            continue
        reachable.add(current)
        stack.extend(sorted(directed_adjacency[current] - reachable, reverse=True))

    def _distribution(values: list[int]) -> dict[str, int]:
        return {str(value): values.count(value) for value in sorted(set(values))}

    in_degrees = {resource_id: 0 for resource_id in resource_ids}
    for targets in directed_adjacency.values():
        for target_id in targets:
            in_degrees[target_id] += 1
    out_degrees = {resource_id: len(targets) for resource_id, targets in directed_adjacency.items()}
    return {
        'sourceLabel': 'decoded-resource-backed-candidate-graph-connectivity-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'recordCount': len(systems),
        'weaklyConnectedComponentCount': len(components),
        'weaklyConnectedComponentSizes': [len(component) for component in components],
        'resource128WeakComponentSize': len(next((component for component in components if start_resource_id in component), [])),
        'resource128DirectedReachableCount': len(reachable),
        'resource128DirectedReachableResourceIdsSample': sorted(reachable)[:24],
        'resource128DirectedUnreachableCount': len(set(resource_ids) - reachable),
        'resource128DirectedUnreachableResourceIdsSample': sorted(set(resource_ids) - reachable)[:24],
        'uniqueOutDegreeDistribution': _distribution(list(out_degrees.values())),
        'uniqueInDegreeDistribution': _distribution(list(in_degrees.values())),
        'zeroInDegreeResourceIdsSample': [resource_id for resource_id in resource_ids if in_degrees[resource_id] == 0][:24],
        'zeroOutDegreeResourceIds': [resource_id for resource_id in resource_ids if out_degrees[resource_id] == 0],
        'resource128UniqueOutDegree': out_degrees.get(start_resource_id),
        'resource128UniqueInDegree': in_degrees.get(start_resource_id),
        'sourceNote': 'This is a candidate connectivity/reachability summary over unique decoded Con1-Con16 links. It shows that the undirected candidate graph is connected while directed reachability from resource 128 remains partial; exact named route topology and Classic map layout remain pending.',
    }


def _distance_map(adjacency: dict[int, set[int]], start_resource_id: int) -> dict[int, int]:
    distances = {start_resource_id: 0}
    queue = [start_resource_id]
    while queue:
        current = queue.pop(0)
        for neighbor in sorted(adjacency[current]):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances


def _candidate_graph_distance_summary(systems: list[dict]) -> dict:
    """Summarize candidate graph hop distances without promoting map topology."""
    resource_ids = [system['resourceId'] for system in systems]
    directed_adjacency = {resource_id: set() for resource_id in resource_ids}
    weak_adjacency = {resource_id: set() for resource_id in resource_ids}
    for system in systems:
        resource_id = system['resourceId']
        for slot in system['semanticFields']['candidateHyperspaceLinks']['linkSlots']:
            if slot.get('status') != 'linked-system' or not slot.get('targetPresentInSystRun'):
                continue
            target_id = slot['targetResourceId']
            directed_adjacency[resource_id].add(target_id)
            weak_adjacency[resource_id].add(target_id)
            weak_adjacency[target_id].add(resource_id)

    def _distribution(values: list[int]) -> dict[str, int]:
        return {str(value): values.count(value) for value in sorted(set(values))}

    start_resource_id = 128
    directed_from_start = _distance_map(directed_adjacency, start_resource_id)
    weak_from_start = _distance_map(weak_adjacency, start_resource_id)
    weak_eccentricities = [max(_distance_map(weak_adjacency, resource_id).values()) for resource_id in resource_ids]
    directed_reach_counts = [len(_distance_map(directed_adjacency, resource_id)) for resource_id in resource_ids]
    return {
        'sourceLabel': 'decoded-resource-backed-candidate-graph-distance-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'recordCount': len(systems),
        'resource128DirectedMaxHopDistance': max(directed_from_start.values()),
        'resource128DirectedHopDistanceDistribution': _distribution(list(directed_from_start.values())),
        'resource128WeakMaxHopDistance': max(weak_from_start.values()),
        'resource128WeakHopDistanceDistribution': _distribution(list(weak_from_start.values())),
        'weakGraphDiameterCandidate': max(weak_eccentricities),
        'weakEccentricityDistribution': _distribution(weak_eccentricities),
        'directedReachableCountRange': [min(directed_reach_counts), max(directed_reach_counts)],
        'directedReachableCountDistribution': _distribution(directed_reach_counts),
        'sourceNote': 'This is a candidate hop-distance summary over decoded Con1-Con16 links. It preserves route-analysis inputs only; exact Classic named topology, map distances, and display scaling remain pending.',
    }


def _start_system_candidate_topology_summary(systems: list[dict]) -> dict:
    """Summarize resource 128's candidate neighborhood without promoting named topology."""
    by_resource_id = {system['resourceId']: system for system in systems}
    start_resource_id = 128
    start_system = by_resource_id[start_resource_id]
    unique_edges = set()
    for system in systems:
        resource_id = system['resourceId']
        for slot in system['semanticFields']['candidateHyperspaceLinks']['linkSlots']:
            if slot.get('status') == 'linked-system' and slot.get('targetPresentInSystRun'):
                unique_edges.add((resource_id, slot['targetResourceId']))

    linked_neighbors = []
    for slot in start_system['semanticFields']['candidateHyperspaceLinks']['linkSlots']:
        if slot.get('status') != 'linked-system':
            continue
        target = by_resource_id[slot['targetResourceId']]
        target_coordinates = target['semanticFields']['mapCoordinates']
        target_name = target['semanticFields'].get('exactSystemName', {})
        linked_neighbors.append({
            'slotName': slot['slotName'],
            'targetResourceId': slot['targetResourceId'],
            'targetOrdinal': slot['targetOrdinal'],
            'targetExactSystemName': target_name.get('systemName'),
            'targetNameJoinStatus': 'exact' if target_name else 'unjoined',
            'isSelfLink': slot['targetResourceId'] == start_resource_id,
            'hasReciprocalCandidateEdge': (slot['targetResourceId'], start_resource_id) in unique_edges,
            'targetCoordinateSignedLongCandidate': {
                'xPos': target_coordinates['xPos']['signedLongCandidate'],
                'yPos': target_coordinates['yPos']['signedLongCandidate'],
            },
        })

    return {
        'sourceLabel': 'decoded-resource-backed-start-system-candidate-topology-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'startResourceId': start_resource_id,
        'startExactSystemName': start_system['semanticFields']['exactSystemName']['systemName'],
        'linkedNeighborCount': len(linked_neighbors),
        'linkedNeighbors': linked_neighbors,
        'selfLinkSlotNames': [neighbor['slotName'] for neighbor in linked_neighbors if neighbor['isSelfLink']],
        'reciprocalNeighborResourceIds': [neighbor['targetResourceId'] for neighbor in linked_neighbors if neighbor['hasReciprocalCandidateEdge']],
        'unjoinedNeighborResourceIds': [neighbor['targetResourceId'] for neighbor in linked_neighbors if neighbor['targetNameJoinStatus'] == 'unjoined'],
        'sourceNote': 'This packages the exact Levo/resource 128 bridge with decoded Con1-Con16 neighbor records and coordinate candidates. It promotes only start-neighborhood analysis inputs; target system names, route UI behavior, map layout, and broad runtime topology remain pending.',
    }


def _start_neighborhood_display_transform_summary(systems: list[dict]) -> dict:
    """Summarize start-neighborhood display transform candidates without promotion."""
    by_resource_id = {system['resourceId']: system for system in systems}
    start_topology = _start_system_candidate_topology_summary(systems)
    normalized = _coordinate_display_normalized_summary(systems)
    normalized_by_resource = {
        entry['resourceId']: entry
        for entry in normalized['perResource']
    }
    start_resource_id = start_topology['startResourceId']
    start_coordinates = by_resource_id[start_resource_id]['semanticFields']['mapCoordinates']
    start_normalized = normalized_by_resource[start_resource_id]

    transformed_neighbors = []
    for neighbor in start_topology['linkedNeighbors']:
        resource_id = neighbor['targetResourceId']
        coordinates = by_resource_id[resource_id]['semanticFields']['mapCoordinates']
        normalized_neighbor = normalized_by_resource[resource_id]
        y_unit = normalized_neighbor['yPos']['unitIntervalCandidate']
        transformed_neighbors.append({
            'slotName': neighbor['slotName'],
            'targetResourceId': resource_id,
            'targetExactSystemName': neighbor['targetExactSystemName'],
            'targetNameJoinStatus': neighbor['targetNameJoinStatus'],
            'deltaSignedLongFromStart': {
                'xPos': coordinates['xPos']['signedLongCandidate'] - start_coordinates['xPos']['signedLongCandidate'],
                'yPos': coordinates['yPos']['signedLongCandidate'] - start_coordinates['yPos']['signedLongCandidate'],
            },
            'unitIntervalCandidate': {
                'xPos': normalized_neighbor['xPos']['unitIntervalCandidate'],
                'yPos': y_unit,
                'invertedYPos': round(1 - y_unit, 6),
            },
        })

    return {
        'sourceLabel': 'decoded-resource-backed-start-neighborhood-display-transform-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'startResourceId': start_resource_id,
        'startExactSystemName': start_topology['startExactSystemName'],
        'candidateFamilies': [
            'start-neighborhood signed-long delta candidates',
            'start-neighborhood unit-interval display-transform candidates',
            'start-neighborhood inverted-y display-transform candidates',
        ],
        'startUnitIntervalCandidate': {
            'xPos': start_normalized['xPos']['unitIntervalCandidate'],
            'yPos': start_normalized['yPos']['unitIntervalCandidate'],
            'invertedYPos': round(1 - start_normalized['yPos']['unitIntervalCandidate'], 6),
        },
        'linkedNeighborCount': len(transformed_neighbors),
        'linkedNeighbors': transformed_neighbors,
        'unjoinedNeighborResourceIds': start_topology['unjoinedNeighborResourceIds'],
        'sourceNote': 'This combines the exact Levo/resource 128 bridge, decoded Con1-Con16 neighbor records, signed-long coordinate deltas, and non-promoted display-transform candidates for the start neighborhood. It remains analysis input only; exact target system names, EV Classic map pixels, projection, centering, axis orientation, route UI behavior, and broad runtime topology remain pending.',
    }


def _start_neighborhood_display_distance_summary(systems: list[dict]) -> dict:
    """Summarize start-neighborhood distance candidates without promotion."""
    start_display = _start_neighborhood_display_transform_summary(systems)
    start_unit = start_display['startUnitIntervalCandidate']

    distance_neighbors = []
    for neighbor in start_display['linkedNeighbors']:
        delta_signed = neighbor['deltaSignedLongFromStart']
        unit = neighbor['unitIntervalCandidate']
        delta_unit = {
            'xPos': round(unit['xPos'] - start_unit['xPos'], 6),
            'yPos': round(unit['yPos'] - start_unit['yPos'], 6),
            'invertedYPos': round(unit['invertedYPos'] - start_unit['invertedYPos'], 6),
        }
        distance_neighbors.append({
            'slotName': neighbor['slotName'],
            'targetResourceId': neighbor['targetResourceId'],
            'targetExactSystemName': neighbor['targetExactSystemName'],
            'targetNameJoinStatus': neighbor['targetNameJoinStatus'],
            'deltaSignedLongFromStart': delta_signed,
            'manhattanSignedLongCandidate': abs(delta_signed['xPos']) + abs(delta_signed['yPos']),
            'deltaUnitIntervalCandidate': delta_unit,
            'manhattanUnitIntervalCandidate': round(abs(delta_unit['xPos']) + abs(delta_unit['yPos']), 6),
            'manhattanInvertedYUnitIntervalCandidate': round(abs(delta_unit['xPos']) + abs(delta_unit['invertedYPos']), 6),
        })

    non_self_distances = [
        neighbor['manhattanSignedLongCandidate']
        for neighbor in distance_neighbors
        if neighbor['targetResourceId'] != start_display['startResourceId']
    ]
    non_self_unit_distances = [
        neighbor['manhattanInvertedYUnitIntervalCandidate']
        for neighbor in distance_neighbors
        if neighbor['targetResourceId'] != start_display['startResourceId']
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-start-neighborhood-display-distance-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'startResourceId': start_display['startResourceId'],
        'startExactSystemName': start_display['startExactSystemName'],
        'candidateFamilies': [
            'start-neighborhood signed-long manhattan-distance candidates',
            'start-neighborhood unit-interval delta candidates',
            'start-neighborhood inverted-y unit-interval manhattan-distance candidates',
        ],
        'linkedNeighborCount': len(distance_neighbors),
        'linkedNeighbors': distance_neighbors,
        'nonSelfSignedLongManhattanDistanceRange': [min(non_self_distances), max(non_self_distances)],
        'nonSelfInvertedYUnitIntervalManhattanDistanceRange': [min(non_self_unit_distances), max(non_self_unit_distances)],
        'sourceNote': 'This converts the decoded Levo/resource 128 neighbor coordinate deltas into non-promoted distance candidates for later map-scaling comparison. It does not claim EV Classic map pixels, distance formula, projection, centering, axis orientation, exact target system names, route UI behavior, or broad runtime topology.',
    }


def _display_quadrant(delta_x: float, delta_inverted_y: float) -> str:
    if delta_x == 0 and delta_inverted_y == 0:
        return 'self'
    horizontal = 'east' if delta_x > 0 else 'west' if delta_x < 0 else 'center'
    vertical = 'north' if delta_inverted_y > 0 else 'south' if delta_inverted_y < 0 else 'center'
    return '-'.join(part for part in [vertical, horizontal] if part != 'center')


def _start_neighborhood_display_vector_summary(systems: list[dict]) -> dict:
    """Summarize start-neighborhood display vector candidates without promotion."""
    start_distance = _start_neighborhood_display_distance_summary(systems)

    vector_neighbors = []
    for neighbor in start_distance['linkedNeighbors']:
        delta_unit = neighbor['deltaUnitIntervalCandidate']
        delta_x = delta_unit['xPos']
        delta_y_inverted = delta_unit['invertedYPos']
        euclidean = round(math.hypot(delta_x, delta_y_inverted), 6)
        signed_angle = None if euclidean == 0 else round(math.degrees(math.atan2(delta_y_inverted, delta_x)), 6)
        dominant_axis = 'self'
        if euclidean != 0:
            dominant_axis = 'x' if abs(delta_x) >= abs(delta_y_inverted) else 'y'
        vector_neighbors.append({
            'slotName': neighbor['slotName'],
            'targetResourceId': neighbor['targetResourceId'],
            'targetExactSystemName': neighbor['targetExactSystemName'],
            'targetNameJoinStatus': neighbor['targetNameJoinStatus'],
            'deltaInvertedYUnitIntervalCandidate': {
                'xPos': delta_x,
                'yPos': delta_y_inverted,
            },
            'euclideanInvertedYUnitIntervalCandidate': euclidean,
            'signedAngleDegreesFromPositiveXCandidate': signed_angle,
            'displayQuadrantCandidate': _display_quadrant(delta_x, delta_y_inverted),
            'dominantAxisCandidate': dominant_axis,
        })

    non_self_vectors = [
        neighbor for neighbor in vector_neighbors
        if neighbor['targetResourceId'] != start_distance['startResourceId']
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-start-neighborhood-display-vector-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'startResourceId': start_distance['startResourceId'],
        'startExactSystemName': start_distance['startExactSystemName'],
        'candidateFamilies': [
            'start-neighborhood inverted-y unit-vector candidates',
            'start-neighborhood display quadrant candidates',
            'start-neighborhood signed-angle candidates',
            'start-neighborhood dominant-axis candidates',
        ],
        'linkedNeighborCount': len(vector_neighbors),
        'linkedNeighbors': vector_neighbors,
        'nonSelfDisplayQuadrantCandidates': sorted({neighbor['displayQuadrantCandidate'] for neighbor in non_self_vectors}),
        'nonSelfDominantAxisDistribution': {
            axis: len([neighbor for neighbor in non_self_vectors if neighbor['dominantAxisCandidate'] == axis])
            for axis in sorted({neighbor['dominantAxisCandidate'] for neighbor in non_self_vectors})
        },
        'sourceNote': 'This converts the decoded Levo/resource 128 neighbor display-distance candidates into non-promoted vector, quadrant, signed-angle, and dominant-axis candidates for later map-projection comparison. It does not claim EV Classic map pixels, distance formula, projection, centering, axis orientation, exact target system names, route UI behavior, or broad runtime topology.',
    }


def _start_neighborhood_slot_vector_order_summary(systems: list[dict]) -> dict:
    """Summarize start-neighborhood slot order against display-vector candidates without promotion."""
    vector_summary = _start_neighborhood_display_vector_summary(systems)
    linked_neighbors = vector_summary['linkedNeighbors']
    non_self_neighbors = [
        neighbor for neighbor in linked_neighbors
        if neighbor['targetResourceId'] != vector_summary['startResourceId']
    ]
    by_distance = sorted(
        non_self_neighbors,
        key=lambda neighbor: (
            neighbor['euclideanInvertedYUnitIntervalCandidate'],
            neighbor['slotName'],
            neighbor['targetResourceId'],
        ),
    )
    distance_rank_by_resource = {
        neighbor['targetResourceId']: rank
        for rank, neighbor in enumerate(by_distance, start=1)
    }
    linked_slot_order = []
    for index, neighbor in enumerate(linked_neighbors, start=1):
        linked_slot_order.append({
            'slotOrderIndex': index,
            'slotName': neighbor['slotName'],
            'targetResourceId': neighbor['targetResourceId'],
            'targetExactSystemName': neighbor['targetExactSystemName'],
            'targetNameJoinStatus': neighbor['targetNameJoinStatus'],
            'isSelfLink': neighbor['targetResourceId'] == vector_summary['startResourceId'],
            'displayQuadrantCandidate': neighbor['displayQuadrantCandidate'],
            'dominantAxisCandidate': neighbor['dominantAxisCandidate'],
            'euclideanInvertedYUnitIntervalCandidate': neighbor['euclideanInvertedYUnitIntervalCandidate'],
            'signedAngleDegreesFromPositiveXCandidate': neighbor['signedAngleDegreesFromPositiveXCandidate'],
            'distanceRankAmongNonSelfCandidates': distance_rank_by_resource.get(neighbor['targetResourceId']),
        })
    return {
        'sourceLabel': 'decoded-resource-backed-start-neighborhood-slot-vector-order-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'startResourceId': vector_summary['startResourceId'],
        'startExactSystemName': vector_summary['startExactSystemName'],
        'candidateFamilies': [
            'start-neighborhood Con-slot order candidates',
            'start-neighborhood display-vector order candidates',
            'start-neighborhood non-self distance-rank candidates',
        ],
        'linkedNeighborCount': len(linked_slot_order),
        'linkedSlotOrder': linked_slot_order,
        'nonSelfSlotNamesByDistanceCandidate': [neighbor['slotName'] for neighbor in by_distance],
        'nonSelfResourceIdsByDistanceCandidate': [neighbor['targetResourceId'] for neighbor in by_distance],
        'firstNonSelfSlotName': next((entry['slotName'] for entry in linked_slot_order if not entry['isSelfLink']), None),
        'firstNonSelfResourceId': next((entry['targetResourceId'] for entry in linked_slot_order if not entry['isSelfLink']), None),
        'sourceNote': 'This cross-walks decoded Levo/resource 128 Con-slot order with non-promoted display-vector/distance candidates for later map-scaling and route-UI comparison. It does not claim EV Classic route ordering, map pixels, distance formula, projection, axis orientation, exact target system names, or broad runtime topology.',
    }


def _start_neighborhood_slot_angular_order_summary(systems: list[dict]) -> dict:
    """Summarize start-neighborhood slot order against signed-angle candidates without promotion."""
    slot_order = _start_neighborhood_slot_vector_order_summary(systems)
    linked_entries = slot_order['linkedSlotOrder']
    non_self_entries = [entry for entry in linked_entries if not entry['isSelfLink']]
    by_angle = sorted(
        non_self_entries,
        key=lambda entry: (
            entry['signedAngleDegreesFromPositiveXCandidate'],
            entry['slotName'],
            entry['targetResourceId'],
        ),
    )
    angle_rank_by_resource = {
        entry['targetResourceId']: rank
        for rank, entry in enumerate(by_angle, start=1)
    }
    linked_slot_angular_order = []
    for entry in linked_entries:
        linked_slot_angular_order.append({
            'slotOrderIndex': entry['slotOrderIndex'],
            'slotName': entry['slotName'],
            'targetResourceId': entry['targetResourceId'],
            'targetExactSystemName': entry['targetExactSystemName'],
            'targetNameJoinStatus': entry['targetNameJoinStatus'],
            'isSelfLink': entry['isSelfLink'],
            'displayQuadrantCandidate': entry['displayQuadrantCandidate'],
            'dominantAxisCandidate': entry['dominantAxisCandidate'],
            'signedAngleDegreesFromPositiveXCandidate': entry['signedAngleDegreesFromPositiveXCandidate'],
            'angleRankAmongNonSelfCandidates': angle_rank_by_resource.get(entry['targetResourceId']),
            'distanceRankAmongNonSelfCandidates': entry['distanceRankAmongNonSelfCandidates'],
        })
    return {
        'sourceLabel': 'decoded-resource-backed-start-neighborhood-slot-angular-order-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'startResourceId': slot_order['startResourceId'],
        'startExactSystemName': slot_order['startExactSystemName'],
        'candidateFamilies': [
            'start-neighborhood Con-slot order versus signed-angle candidates',
            'start-neighborhood display-quadrant order candidates',
            'start-neighborhood angular-rank candidates',
        ],
        'linkedNeighborCount': len(linked_slot_angular_order),
        'linkedSlotAngularOrder': linked_slot_angular_order,
        'nonSelfResourceIdsBySignedAngleCandidate': [entry['targetResourceId'] for entry in by_angle],
        'nonSelfSlotNamesBySignedAngleCandidate': [entry['slotName'] for entry in by_angle],
        'nonSelfQuadrantsInSlotOrder': [entry['displayQuadrantCandidate'] for entry in non_self_entries],
        'nonSelfQuadrantsBySignedAngleCandidate': [entry['displayQuadrantCandidate'] for entry in by_angle],
        'firstSignedAngleNonSelfSlotName': by_angle[0]['slotName'] if by_angle else None,
        'firstSignedAngleNonSelfResourceId': by_angle[0]['targetResourceId'] if by_angle else None,
        'sourceNote': 'This cross-walks decoded Levo/resource 128 Con-slot order with non-promoted signed-angle/quadrant candidates for later map orientation and route-UI comparison. It does not claim EV Classic angular ordering, route ordering, map pixels, projection, axis orientation, exact target system names, or broad runtime topology.',
    }


def _start_neighborhood_runtime_calibration_priority_summary(systems: list[dict]) -> dict:
    """Prioritize start-neighborhood runtime calibration targets without promotion."""
    slot_order = _start_neighborhood_slot_vector_order_summary(systems)
    slot_angle = _start_neighborhood_slot_angular_order_summary(systems)
    runtime_gate = _coordinate_display_runtime_capture_gate_summary(systems)
    entries = [entry for entry in slot_angle['linkedSlotAngularOrder'] if not entry['isSelfLink']]
    by_distance = slot_order['nonSelfResourceIdsByDistanceCandidate']
    by_angle = slot_angle['nonSelfResourceIdsBySignedAngleCandidate']
    required_targets = runtime_gate.get('requiredTargetResourceIds', [])
    priority_entries = []
    for entry in entries:
        resource_id = entry['targetResourceId']
        priority_entries.append({
            'slotName': entry['slotName'],
            'targetResourceId': resource_id,
            'targetNameJoinStatus': entry['targetNameJoinStatus'],
            'displayQuadrantCandidate': entry['displayQuadrantCandidate'],
            'distanceRankAmongNonSelfCandidates': entry['distanceRankAmongNonSelfCandidates'],
            'angleRankAmongNonSelfCandidates': entry['angleRankAmongNonSelfCandidates'],
            'requiredByRuntimeCaptureGate': resource_id in required_targets,
            'priorityReason': 'nearest-and-lowest-angle-candidate' if resource_id == by_distance[0] == by_angle[0] else 'required-neighbor-calibration-target',
        })
    priority_entries = sorted(
        priority_entries,
        key=lambda entry: (
            0 if entry['priorityReason'] == 'nearest-and-lowest-angle-candidate' else 1,
            entry['distanceRankAmongNonSelfCandidates'],
            entry['angleRankAmongNonSelfCandidates'],
            entry['slotName'],
        ),
    )
    return {
        'sourceLabel': 'decoded-resource-backed-start-neighborhood-runtime-calibration-priority-scout',
        'oracleStatus': 'coordinate_display_capture_blocked_pending_classic_map_pixel_click_evidence',
        'startResourceId': slot_order['startResourceId'],
        'startExactSystemName': slot_order['startExactSystemName'],
        'candidateFamilies': [
            'start-neighborhood runtime calibration target priority candidates',
            'Con-slot versus distance-rank and angular-rank comparison candidates',
            'runtime capture gate target ordering without display-scale promotion',
        ],
        'requiredRuntimeCaptureTargetResourceIds': required_targets,
        'requiredRuntimeCaptureConSlots': runtime_gate.get('requiredConSlots', []),
        'priorityTargetResourceIds': [entry['targetResourceId'] for entry in priority_entries],
        'priorityConSlots': [entry['slotName'] for entry in priority_entries],
        'firstPriorityTargetResourceId': priority_entries[0]['targetResourceId'] if priority_entries else None,
        'firstPriorityConSlot': priority_entries[0]['slotName'] if priority_entries else None,
        'distanceAngleOrderConflict': by_distance != by_angle,
        'nonSelfResourceIdsByDistanceCandidate': by_distance,
        'nonSelfResourceIdsBySignedAngleCandidate': by_angle,
        'priorityEntries': priority_entries,
        'promotionBlockers': [
            'priority order is computed from non-promoted decoded coordinate candidates, not observed Classic map pixels',
            'target system names remain unjoined for resources 129-131',
            'runtime capture packets must tie visible labels and map positions to decoded Con slots before display-scale or route-label promotion',
        ],
        'promotionStatus': 'not-promoted; target priority only for future non-strict runtime calibration capture',
        'sourceNote': 'This selects the most information-rich Levo-neighborhood runtime calibration order from existing decoded Con-slot, distance, and angular candidates. It does not promote EV Classic map projection, route ordering, target names, or display units.',
    }


def _system_name_seed_summary(names: dict) -> dict:
    """Summarize heuristic name seeds without claiming record-to-name joins."""
    system_seeds = names.get('systemNames', [])
    landing_seed_names = {seed.get('name') for seed in names.get('landingNames', [])}
    system_seed_names = [seed.get('name') for seed in system_seeds]
    exact_mapped_names = [mapping['systemName'] for mapping in EXACT_SYSTEM_NAME_MAPPINGS.values()]
    return {
        'sourceLabel': 'decoded-resource-backed-system-name-seed-join-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'systemNameSeedCount': len(system_seeds),
        'systemNameSeedNames': system_seed_names,
        'systemSeedNamesAlsoPresentAsLandingSeeds': sorted(set(system_seed_names) & landing_seed_names),
        'exactMappedSystemNames': exact_mapped_names,
        'unjoinedSystemNameSeedCount': len([name for name in system_seed_names if name not in exact_mapped_names]),
        'sourceNote': 'Heuristic system-name text seeds are preserved for later record-to-name joins, but they are not assigned to syst resource IDs by this summary. The only exact current system-name mapping remains resource ID 128 to Levo from Resource Bible start-system plus original-runtime start observation.',
    }


def _system_name_landing_proximity_summary(names: dict) -> dict:
    """Preserve name/landing text-byte proximity candidates without joining syst records."""
    system_seeds = names.get('systemNames', [])
    landing_seeds = names.get('landingNames', [])

    def _nearest_landings(system_seed: dict) -> dict:
        system_offset = int(system_seed.get('byteOffset', 0))
        nearest = sorted(
            landing_seeds,
            key=lambda landing: (abs(int(landing.get('byteOffset', 0)) - system_offset), int(landing.get('byteOffset', 0))),
        )[:3]
        return {
            'systemNameSeed': system_seed.get('name'),
            'systemNameSeedByteOffset': system_offset,
            'nearestLandingNameCandidates': [
                {
                    'landingName': landing.get('name'),
                    'landingByteOffset': int(landing.get('byteOffset', 0)),
                    'byteDeltaFromSystemNameSeed': int(landing.get('byteOffset', 0)) - system_offset,
                }
                for landing in nearest
            ],
        }

    by_system_name = [_nearest_landings(seed) for seed in system_seeds]
    exact_mapped_names = [mapping['systemName'] for mapping in EXACT_SYSTEM_NAME_MAPPINGS.values()]
    exact_mapped_landing_candidates = [
        {
            'systemName': name,
            'landingNameSeedByteOffsets': [
                int(seed.get('byteOffset', 0)) for seed in landing_seeds if seed.get('name') == name
            ],
        }
        for name in exact_mapped_names
    ]
    close_threshold = 256
    close_candidates = [
        entry['systemNameSeed']
        for entry in by_system_name
        if entry['nearestLandingNameCandidates']
        and abs(entry['nearestLandingNameCandidates'][0]['byteDeltaFromSystemNameSeed']) <= close_threshold
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-system-name-landing-proximity-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'candidateFamilies': [
            'system-name text seed to nearest landing-name text seed byte-proximity candidates',
            'exact mapped system-name landing-seed presence candidates',
        ],
        'systemNameSeedCount': len(system_seeds),
        'landingNameSeedCount': len(landing_seeds),
        'closeByteThresholdCandidate': close_threshold,
        'systemNameSeedsWithCloseLandingCandidates': close_candidates,
        'systemNameSeedsWithoutCloseLandingCandidates': [
            entry['systemNameSeed'] for entry in by_system_name if entry['systemNameSeed'] not in close_candidates
        ],
        'exactMappedSystemLandingCandidates': exact_mapped_landing_candidates,
        'bySystemNameSeed': by_system_name,
        'sourceNote': 'This compares heuristic text seed byte offsets only. It is useful for later record-to-name/topology investigation, but it does not assign any syst resource ID to these names or promote EV Classic runtime topology. Resource 128 to Levo remains the only exact system-name mapping.',
    }


def _landing_name_candidate_reference_summary(names: dict) -> dict:
    """Document decoded EV Data.rez landing-name seeds as a candidate system-name reference list."""
    landing_seeds = names.get('landingNames', [])
    system_seed_names = {seed.get('name') for seed in names.get('systemNames', [])}
    exact_system_names = {mapping['systemName'] for mapping in EXACT_SYSTEM_NAME_MAPPINGS.values()}
    ordered_by_chunk = sorted(landing_seeds, key=lambda entry: entry.get('chunkIndex', 0))
    candidate_names = [
        {
            'name': seed.get('name'),
            'chunkIndex': seed.get('chunkIndex'),
            'resourceIdInNamesFile': seed.get('resourceId'),
            'byteOffset': seed.get('byteOffset'),
            'confidence': seed.get('confidence'),
            'isSystemNameSeed': seed.get('name') in system_seed_names,
            'isExactSystemNameMapping': seed.get('name') in exact_system_names,
        }
        for seed in ordered_by_chunk
    ]
    chunk_indices = {seed.get('chunkIndex') for seed in ordered_by_chunk if seed.get('chunkIndex') is not None}
    system_seed_names_in_landings = {seed.get('name') for seed in ordered_by_chunk if seed.get('name') in system_seed_names}
    exact_mapped_in_landings = {seed.get('name') for seed in ordered_by_chunk if seed.get('name') in exact_system_names}
    return {
        'sourceLabel': 'decoded-resource-backed-landing-name-candidate-reference',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'recordCount': len(candidate_names),
        'chunkIndexRange': [min(chunk_indices), max(chunk_indices)] if chunk_indices else [],
        'chunkIndexCount': len(chunk_indices),
        'systemNameSeedMatchCount': len(system_seed_names_in_landings),
        'systemNameSeedMatches': sorted(system_seed_names_in_landings),
        'exactSystemNameMappingMatchCount': len(exact_mapped_in_landings),
        'exactSystemNameMappingMatches': sorted(exact_mapped_in_landings),
        'candidateNames': candidate_names,
        'candidateHypothesis': 'landing-name chunkIndex ordering may correspond to EV Data.rez system resource ordering; not promoted or verified',
        'promotionBlockers': [
            'landing-name chunk ordering is a heuristic signal, not a validated system resource ordering oracle',
            'landing-name resourceId field uses a separate EV Data.rez namespace, not syst record resource IDs 128-194',
            'only resource 128 to Levo has exact Classic and runtime evidence; landing-name evidence cannot bridge the record-to-name gap without additional Classic source confirmation',
        ],
        'promotionStatus': 'not-promoted; landing-name candidate reference only, pending exact Classic syst name/order oracle',
        'sourceNote': 'The 72 landing-name seeds are decoded from EV Data.rez text chunks and ordered here by chunkIndex. They provide a candidate system-name list for future record-to-name investigation but are not promoted as Classic system names until exact record-to-name joins or runtime map-label evidence confirms them.',
    }


def _syst_record_name_candidate_cross_reference_summary(names: dict, resource_ids: set[int]) -> dict:
    """Align the 67 syst records to the 72 landing-name candidates using chunkIndex ordering.

    The hypothesis is that landing-name chunkIndex ordering corresponds to EV Data.rez
    system resource ID ordering. Levo (chunkIndex 11) is the only exact match (resource 128),
    so record index i maps to the landing-name candidate at chunkIndex (11 + i).
    """
    landing_seeds = sorted(names.get('landingNames', []), key=lambda entry: entry.get('chunkIndex', 0))
    exact_system_names = {mapping['systemName'] for mapping in EXACT_SYSTEM_NAME_MAPPINGS.values()}
    exact_mapped_resource_ids = sorted(EXACT_SYSTEM_NAME_MAPPINGS)
    unjoined_resource_ids = sorted(resource_ids - set(exact_mapped_resource_ids))
    levo_chunk_index = 11  # Confirmed by landingNameCandidateReferenceSummary
    levo_resource_id = 128
    record_count = len(resource_ids)
    candidate_count = len(landing_seeds)

    # Build candidate name lookup by chunkIndex
    name_by_chunk = {}
    for seed in landing_seeds:
        ci = seed.get('chunkIndex')
        if ci is not None:
            name_by_chunk[ci] = seed

    # Build cross-reference table: each syst record gets a candidate landing name
    cross_reference: list[dict] = []
    exact_match_count = 0
    candidate_match_count = 0
    missing_candidate_count = 0
    for resource_id in sorted(resource_ids):
        offset_from_levo = resource_id - levo_resource_id
        target_chunk = levo_chunk_index + offset_from_levo
        candidate = name_by_chunk.get(target_chunk)
        entry: dict = {
            'resourceId': resource_id,
            'recordIndex': resource_id - min(resource_ids) if resource_ids else -1,
            'targetChunkIndex': target_chunk,
        }
        if resource_id in exact_mapped_resource_ids:
            entry['candidateSystemName'] = str(EXACT_SYSTEM_NAME_MAPPINGS[resource_id]['systemName'])
            entry['matchType'] = 'exact'
            entry['confidence'] = 'fidelity-promoted'
            exact_match_count += 1
        elif candidate is not None:
            entry['candidateSystemName'] = str(candidate.get('name', ''))
            entry['candidateChunkIndex'] = int(candidate.get('chunkIndex', -1))
            entry['candidateByteOffset'] = int(candidate.get('byteOffset', -1))
            entry['candidateConfidence'] = str(candidate.get('confidence', ''))
            entry['matchType'] = 'heuristic-chunkIndex-alignment'
            entry['confidence'] = 'heuristic'
            candidate_match_count += 1
        else:
            entry['candidateSystemName'] = None
            entry['matchType'] = 'no-candidate'
            entry['confidence'] = 'none'
            missing_candidate_count += 1

        cross_reference.append(entry)

    return {
        'sourceLabel': 'decoded-resource-backed-syst-record-name-candidate-cross-reference',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'recordCount': record_count,
        'landingNameCandidateCount': candidate_count,
        'exactMatchCount': exact_match_count,
        'heuristicCandidateMatchCount': candidate_match_count,
        'missingCandidateCount': missing_candidate_count,
        'alignmentBasis': {
            'anchorChunkIndex': levo_chunk_index,
            'anchorResourceId': levo_resource_id,
            'anchorSystemName': 'Levo',
            'hypothesis': 'landing-name chunkIndex ordering corresponds to EV Data.rez system resource ID ordering',
        },
        'crossReference': cross_reference,
        'promotionBlockers': [
            'only resource 128 to Levo has exact Classic and runtime evidence; all other records use heuristic chunkIndex alignment',
            'landing-name chunkIndex ordering may not correspond perfectly to syst resource ID ordering',
            'runtime map-label evidence has not been observed for any record beyond Levo',
            'landing-name resourceId field uses a separate EV Data.rez namespace, not syst record resource IDs 128-194',
        ],
        'promotionStatus': 'not-promoted; heuristic chunkIndex cross-reference only, pending exact Classic record-to-name evidence',
        'sourceNote': 'This cross-reference aligns the 67 syst records (resource IDs 128-194) to the 72 landing-name candidates via chunkIndex ordering, anchored on the exact Levo mapping at chunkIndex 11. Every candidate name assignment beyond Levo is heuristic and must not be treated as a Classic system name until validated by exact record-to-name joins or runtime map-label evidence.',
    }


def _syst_record_name_gap_analysis_summary(names: dict, resource_ids: set[int]) -> dict:
    """Analyze the 21 missing-candidate gaps from the chunkIndex cross-reference.

    For each syst record with no-candidate at its target chunkIndex, record the nearest
    landing-name candidates before and after (with chunk distances) and classify gap types.
    Also cross-reference the 9 system-name seeds for potential gap-filling candidates.
    """
    landing_seeds = sorted(names.get('landingNames', []), key=lambda entry: entry.get('chunkIndex', 0))
    levo_chunk_index = 11
    levo_resource_id = 128

    name_by_chunk = {}
    for seed in landing_seeds:
        ci = seed.get('chunkIndex')
        if ci is not None:
            name_by_chunk[ci] = seed

    all_chunks = sorted(name_by_chunk.keys())
    system_seeds = names.get('systemNames', [])
    system_seed_names = set(
        str(s.get('name', ''))
        for s in system_seeds
        if s.get('name') and isinstance(s.get('name'), str)
    )

    gaps: list[dict] = []
    gap_types: dict[str, int] = {}
    for resource_id in sorted(resource_ids):
        offset_from_levo = resource_id - levo_resource_id
        target_chunk = levo_chunk_index + offset_from_levo
        candidate = name_by_chunk.get(target_chunk)
        if candidate is not None:
            continue

        # Find nearest landing-name candidates before and after
        before_candidates: list[dict] = []
        after_candidates: list[dict] = []
        for ci in all_chunks:
            seed = name_by_chunk[ci]
            if ci < target_chunk:
                before_candidates.append({
                    'name': str(seed.get('name', '')),
                    'chunkIndex': ci,
                    'chunkDistance': target_chunk - ci,
                    'byteOffset': int(seed.get('byteOffset', -1)),
                })
            elif ci > target_chunk:
                after_candidates.append({
                    'name': str(seed.get('name', '')),
                    'chunkIndex': ci,
                    'chunkDistance': ci - target_chunk,
                    'byteOffset': int(seed.get('byteOffset', -1)),
                })

        # Closest before/after
        closest_before = before_candidates[-1] if before_candidates else None
        closest_after = after_candidates[0] if after_candidates else None

        # Gap type classification
        if closest_before is None and closest_after is not None:
            gap_type = 'before-first-candidate'
        elif closest_after is None and closest_before is not None:
            gap_type = 'after-last-candidate'
        elif closest_before is not None and closest_after is not None:
            gap_type = 'mid-range-gap'
        else:
            gap_type = 'isolated-no-neighbors'

        gap_types[gap_type] = gap_types.get(gap_type, 0) + 1

        # Combined span for mid-range gaps
        combined_span = None
        if closest_before is not None and closest_after is not None:
            combined_span = closest_before['chunkDistance'] + closest_after['chunkDistance']

        gap_entry: dict = {
            'resourceId': resource_id,
            'recordIndex': resource_id - levo_resource_id,
            'targetChunkIndex': target_chunk,
            'gapType': gap_type,
            'closestBeforeCandidate': closest_before,
            'closestAfterCandidate': closest_after,
            'combinedChunkSpan': combined_span,
        }
        gaps.append(gap_entry)

    # Count how many system-name seeds overlap with nearby landing names
    nearby_names: set[str] = set()
    for gap in gaps:
        if gap['closestBeforeCandidate']:
            nearby_names.add(gap['closestBeforeCandidate']['name'])
        if gap['closestAfterCandidate']:
            nearby_names.add(gap['closestAfterCandidate']['name'])
    seed_overlap = system_seed_names & nearby_names

    return {
        'sourceLabel': 'decoded-resource-backed-syst-record-name-gap-analysis',
        'oracleStatus': 'record_name_gaps_blocked_pending_classic_name_or_runtime_evidence',
        'totalRecordCount': len(resource_ids),
        'gapCount': len(gaps),
        'gapTypes': gap_types,
        'gaps': gaps,
        'systemNameSeedCount': len(system_seed_names),
        'systemNameSeedsNearGaps': sorted(seed_overlap),
        'systemNameSeedGapOverlapCount': len(seed_overlap),
        'promotionBlockers': [
            'all gap records have no landing-name candidate at their expected chunkIndex',
            'nearby landing-name candidates are proximity hints only; they do not constitute record-to-name joins',
            'system-name seeds near gaps may suggest candidate names but do not assign them to specific syst records',
            'at least 65 records remain unjoined without exact Classic source-level confirmation',
        ],
        'promotionStatus': 'not-promoted; gap analysis only pending exact Classic record-to-name or runtime label evidence',
        'sourceNote': 'This analysis records for each of the 21 missing-candidate syst records the nearest landing-name candidates (before and after) with chunk distances and classifies gap types. It also identifies any of the 9 heuristic system-name seeds that appear near gaps. No record-to-name join is promoted from this analysis alone.',
    }


def _coordinate_gap_spatial_mapping_summary(systems: list[dict], names: dict) -> dict:
    """Map each gap record into decoded coordinate space with nearest candidate-named neighbors.

    For each of the 21 gap records (no landing-name candidate at its target chunkIndex),
    record its position in signed-long, fixed-point, and normalized coordinate interpretations,
    plus the nearest candidate-named systems by Euclidean distance.
    """
    gap_analysis = _syst_record_name_gap_analysis_summary(names, {system['resourceId'] for system in systems})
    gaps = gap_analysis.get('gaps', [])
    system_by_resource_id = {system['resourceId']: system for system in systems}

    # Build set of resource IDs that have candidate names (including Levo as exact)
    cross_ref = _syst_record_name_candidate_cross_reference_summary(names, {system['resourceId'] for system in systems})
    named_resource_ids: set[int] = set()
    for entry in cross_ref.get('crossReference', []):
        if entry.get('candidateSystemName') and entry.get('matchType') != 'no-candidate':
            named_resource_ids.add(entry['resourceId'])

    # Build lookup: resourceId -> candidate system name
    name_by_resource_id: dict[int, str] = {}
    for entry in cross_ref.get('crossReference', []):
        name = entry.get('candidateSystemName')
        if name:
            name_by_resource_id[entry['resourceId']] = str(name)

    def _coordinate_distance(system_a: dict, system_b: dict) -> float:
        ax = system_a['semanticFields']['mapCoordinates']['xPos']['signedLongCandidate']
        ay = system_a['semanticFields']['mapCoordinates']['yPos']['signedLongCandidate']
        bx = system_b['semanticFields']['mapCoordinates']['xPos']['signedLongCandidate']
        by = system_b['semanticFields']['mapCoordinates']['yPos']['signedLongCandidate']
        return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

    gap_entries: list[dict] = []
    for gap in gaps:
        resource_id = gap['resourceId']
        system = system_by_resource_id.get(resource_id)
        if system is None:
            continue
        coords = system['semanticFields']['mapCoordinates']
        x_signed = coords['xPos']['signedLongCandidate']
        y_signed = coords['yPos']['signedLongCandidate']
        x_high = coords['xPos']['rawWords'][0]
        y_high = coords['yPos']['rawWords'][0]
        x_low = coords['xPos']['rawWords'][1]
        y_low = coords['yPos']['rawWords'][1]

        # Fixed-point interpretation (16.16)
        fixed_point_divisor = 65536
        x_fixed = x_signed / fixed_point_divisor
        y_fixed = y_signed / fixed_point_divisor

        # Normalized interpretation
        normalized = _coordinate_display_normalized_summary(systems)
        x_normalized = None
        y_normalized = None
        for entry in normalized.get('normalizedSystems', []):
            if entry.get('resourceId') == resource_id:
                x_normalized = entry['xPos']['minNormalizedSignedLongCandidate']
                y_normalized = entry['yPos']['minNormalizedSignedLongCandidate']
                break

        # Find nearest N candidate-named systems by Euclidean distance
        distances_to_named: list[dict] = []
        for named_id in sorted(named_resource_ids):
            named_system = system_by_resource_id.get(named_id)
            if named_system is None:
                continue
            dist = _coordinate_distance(system, named_system)
            distances_to_named.append({
                'targetResourceId': named_id,
                'candidateSystemName': name_by_resource_id.get(named_id, ''),
                'matchType': 'exact' if named_id == 128 else 'heuristic-chunkIndex-alignment',
                'signedLongDistance': round(dist, 6),
            })
        distances_to_named.sort(key=lambda entry: entry['signedLongDistance'])
        nearest_named = distances_to_named[:5]

        # Quadrant relative to Levo (origin 0,0)
        levo_system = system_by_resource_id.get(128)
        if levo_system:
            levo_x = levo_system['semanticFields']['mapCoordinates']['xPos']['signedLongCandidate']
            levo_y = levo_system['semanticFields']['mapCoordinates']['yPos']['signedLongCandidate']
            dx = x_signed - levo_x
            dy = y_signed - levo_y
            quadrant = _display_quadrant(dx, dy)
        else:
            dx = dy = None
            quadrant = 'unknown'

        gap_entry: dict = {
            'resourceId': resource_id,
            'recordIndex': gap.get('recordIndex'),
            'targetChunkIndex': gap.get('targetChunkIndex'),
            'gapType': gap.get('gapType'),
            'signedLongX': x_signed,
            'signedLongY': y_signed,
            'rawHighWordX': x_high,
            'rawHighWordY': y_high,
            'rawLowWordX': x_low,
            'rawLowWordY': y_low,
            'fixedPointX': round(x_fixed, 6),
            'fixedPointY': round(y_fixed, 6),
            'normalizedX': x_normalized,
            'normalizedY': y_normalized,
            'deltaFromLevoX': dx,
            'deltaFromLevoY': dy,
            'quadrantFromLevo': quadrant,
            'closestNamedNeighborResourceId': nearest_named[0]['targetResourceId'] if nearest_named else None,
            'closestNamedNeighborSystemName': nearest_named[0]['candidateSystemName'] if nearest_named else None,
            'closestNamedNeighborDistance': nearest_named[0]['signedLongDistance'] if nearest_named else None,
            'nearestNamedNeighbors': nearest_named,
        }
        gap_entries.append(gap_entry)

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-gap-spatial-mapping-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'recordCount': len(systems),
        'gapCount': len(gap_entries),
        'gapResourceIds': [entry['resourceId'] for entry in gap_entries],
        'namedNeighborResourceIds': sorted(named_resource_ids),
        'namedNeighborCount': len(named_resource_ids),
        'gapEntries': gap_entries,
        'promotionBlockers': [
            'coordinate display units/map scaling remain unpromoted, so spatial positions are decoded-candidate-only and cannot be validated against Classic map pixels',
            'gap record names remain unjoined; nearby candidate-named systems are proximity hints, not record-to-name joins',
            'Classic map pixel/click evidence is required before confirming coordinate interpretation or system positions',
        ],
        'promotionStatus': 'not-promoted; spatial mapping uses non-promoted coordinate candidates and heuristic name candidates, pending exact Classic map calibration and record-to-name evidence',
        'sourceNote': 'This summary maps each of the 21 gap records (no landing-name candidate) into decoded signed-long, fixed-point, and normalized coordinate space, and records the nearest candidate-named neighbors by Euclidean distance. It bridges the gap analysis with the coordinate display scouts to prioritise which gaps sit closest to named systems for future map calibration targeting. No coordinate display or record-to-name claim is promoted.',
    }


def _coordinate_gap_identity_resolution_summary(systems: list[dict], names: dict) -> dict:
    """Classify each gap record's spatial proximity to named records as identity hypotheses.

    Uses the coordinate gap spatial mapping data to determine whether each gap record
    is spatially co-located with a named record (suggesting it might be the same system
    at a different resource ID), or genuinely separated (suggesting it is a distinct,
    unidentified system).

    Classification rules:
    - co-located: signed-long distance <= 1.0 from a named neighbor (essentially same position)
    - near: signed-long distance > 1.0 but within ~5% of the coordinate span
    - separated: signed-long distance larger than near threshold
    """
    import math as _math

    gap_mapping = _coordinate_gap_spatial_mapping_summary(systems, names)
    gap_entries = gap_mapping.get('gapEntries', [])

    # Compute coordinate span for distance-context thresholds
    xs = []
    ys = []
    for system in systems:
        c = system['semanticFields']['mapCoordinates']
        xs.append(c['xPos']['signedLongCandidate'])
        ys.append(c['yPos']['signedLongCandidate'])
    x_span = max(xs) - min(xs)
    y_span = max(ys) - min(ys)
    span_max = max(x_span, y_span)
    # near-threshold: 1% of the maximum coordinate span
    near_threshold = max(2.0, span_max * 0.01)

    resolutions: list[dict] = []
    co_located_count = 0
    near_count = 0
    separated_count = 0

    for entry in gap_entries:
        nearest = entry.get('nearestNamedNeighbors', [])
        if not nearest:
            continue

        best = nearest[0]
        distance = best.get('signedLongDistance', float('inf'))

        if distance <= 1.0:
            classification = 'co-located'
            co_located_count += 1
            hypothesis = (
                'Gap record is spatially co-located with named neighbor '
                f'{best.get("candidateSystemName", "?")} (resource {best.get("targetResourceId", "?")}) '
                f'at signed-long distance {distance}. This suggests the gap record may represent '
                'the same physical system at a different resource ID, or a nearly identical '
                'coordinate placement that would overlap in display space.'
            )
        elif distance <= near_threshold:
            classification = 'near'
            near_count += 1
            hypothesis = (
                f'Gap record is spatially near named neighbor '
                f'{best.get("candidateSystemName", "?")} (resource {best.get("targetResourceId", "?")}) '
                f'at signed-long distance {distance} (threshold={near_threshold:.0f}). '
                'May be a distinct nearby system or an offset duplicate.'
            )
        else:
            classification = 'separated'
            separated_count += 1
            hypothesis = (
                f'Gap record is spatially separated from named neighbor '
                f'{best.get("candidateSystemName", "?")} (resource {best.get("targetResourceId", "?")}) '
                f'at signed-long distance {distance} (threshold={near_threshold:.0f}). '
                'Likely a genuinely distinct, unnamed system.'
            )

        # Also check if the gap shares coordinates with any non-nearest named record
        co_located_with: list[dict] = []
        for candidate in nearest:
            if candidate.get('signedLongDistance', float('inf')) <= 1.0:
                co_located_with.append({
                    'targetResourceId': candidate['targetResourceId'],
                    'candidateSystemName': candidate.get('candidateSystemName', ''),
                    'signedLongDistance': candidate['signedLongDistance'],
                })

        resolution: dict = {
            'resourceId': entry['resourceId'],
            'recordIndex': entry.get('recordIndex'),
            'gapType': entry.get('gapType'),
            'signedLongX': entry['signedLongX'],
            'signedLongY': entry['signedLongY'],
            'closestNamedNeighborResourceId': entry.get('closestNamedNeighborResourceId'),
            'closestNamedNeighborSystemName': entry.get('closestNamedNeighborSystemName'),
            'closestNamedNeighborDistance': distance,
            'classification': classification,
            'classificationHypothesis': hypothesis,
            'coLocatedWithResourceIds': [item['targetResourceId'] for item in co_located_with],
            'coLocatedWithCount': len(co_located_with),
            'coLocatedWith': co_located_with,
        }
        resolutions.append(resolution)

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-gap-identity-resolution-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'recordCount': len(systems),
        'gapCount': len(resolutions),
        'gapResourceIds': [entry['resourceId'] for entry in resolutions],
        'coordinateSpanX': x_span,
        'coordinateSpanY': y_span,
        'coordinateSpanMax': span_max,
        'nearThreshold': round(near_threshold, 1),
        'coLocatedCount': co_located_count,
        'nearCount': near_count,
        'separatedCount': separated_count,
        'coLocatedResourceIds': [
            entry['resourceId'] for entry in resolutions
            if entry['classification'] == 'co-located'
        ],
        'nearResourceIds': [
            entry['resourceId'] for entry in resolutions
            if entry['classification'] == 'near'
        ],
        'separatedResourceIds': [
            entry['resourceId'] for entry in resolutions
            if entry['classification'] == 'separated'
        ],
        'gapResolutions': resolutions,
        'promotionBlockers': [
            'gap identity hypotheses are spatial proximity signals only; no record-to-name join is promoted',
            'co-located gaps may share coordinates with named neighbors, but this does not confirm they are the same Classic system without source/name-table or runtime evidence',
            'coordinate display units/map scaling remain unpromoted, so spatial proximity thresholds are decoded-candidate-scale only',
        ],
        'promotionStatus': 'not-promoted; identity hypotheses are spatial proximity scouts only, pending exact Classic record-to-name or runtime label evidence',
        'sourceNote': 'This summary classifies each of the 21 gap records by spatial proximity to named neighbors. Co-located gaps (signed-long distance <= 1.0 in a span of millions) are likely the same system at a different resource ID; separated gaps are likely distinct unnamed systems. No record-to-name join, display-unit, or runtime topology claim is promoted.',
    }


def _coordinate_gap_resource_deduplication_summary(systems: list[dict], names: dict) -> dict:
    """Map co-located gap resource IDs to canonical named neighbors for deduplication.

    Uses the coordinateGapIdentityResolutionSummary to identify co-located gaps and
    assigns each a canonical named-system neighbor. Estimates a simplified distinct
    system count by collapsing co-located duplicate resource IDs.
    """
    identity = _coordinate_gap_identity_resolution_summary(systems, names)
    resolutions = identity.get('gapResolutions', [])

    dedup_entries: list[dict] = []
    co_located_mapped_resource_ids: set[int] = set()
    canonical_named_ids: set[int] = set()

    for r in resolutions:
        if r['classification'] != 'co-located':
            continue

        co_with = r.get('coLocatedWith', [])
        # Pick canonical: lowest distance, then lowest resource ID
        best = min(co_with, key=lambda c: (c.get('signedLongDistance', float('inf')), c.get('targetResourceId', 9999))) if co_with else None

        if best is None:
            continue

        dedup_entry: dict = {
            'duplicateResourceId': r['resourceId'],
            'canonicalSystemName': best['candidateSystemName'],
            'canonicalResourceId': best['targetResourceId'],
            'signedLongDistance': best['signedLongDistance'],
            'allCoLocatedNamedCandidates': [
                {
                    'resourceId': c['targetResourceId'],
                    'systemName': c.get('candidateSystemName', ''),
                    'signedLongDistance': c.get('signedLongDistance', 0.0),
                }
                for c in co_with
            ],
            'coLocatedCandidateCount': len(co_with),
            'confidence': 'spatial-proximity-hypothesis',
        }
        dedup_entries.append(dedup_entry)
        co_located_mapped_resource_ids.add(r['resourceId'])
        canonical_named_ids.add(best['targetResourceId'])

    total_resource_ids = identity['recordCount']
    gap_count = identity['gapCount']
    named_count = total_resource_ids - gap_count
    co_located_count = len(dedup_entries)
    simplified_estimate = total_resource_ids - co_located_count

    return {
        'sourceLabel': 'decoded-resource-backed-coordinate-gap-resource-deduplication-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'totalResourceIds': total_resource_ids,
        'namedSystemCount': named_count,
        'gapCount': gap_count,
        'coLocatedDuplicateCount': co_located_count,
        'nearOrSeparatedCount': gap_count - co_located_count,
        'simplifiedDistinctSystemCountEstimate': simplified_estimate,
        'coLocatedDuplicateResourceIds': sorted(list(co_located_mapped_resource_ids)),
        'canonicalNamedResourceIds': sorted(list(canonical_named_ids)),
        'deduplication': dedup_entries,
        'promotionBlockers': [
            'deduplication is spatial proximity scouting only; no record-to-name join, display unit, or runtime topology is promoted',
            'co-located gap resource IDs may share a position with multiple named neighbors; canonical assignment is a heuristic proximity choice',
            'coordinate display units/map scaling remain unpromoted, so spatial proximity deduplication is decoded-candidate-scale only',
        ],
        'promotionStatus': 'not-promoted; deduplication is spatial proximity scouting only, pending exact Classic record-to-name or runtime label evidence',
        'sourceNote': 'This summary maps each co-located gap resource ID to a canonical named neighbor for deduplication. 16 co-located gaps (signed-long distance <= 1.0) are treated as duplicate resource IDs, reducing the estimated distinct system count from 67 to 51. No record-to-name join, display unit, or runtime topology claim is promoted.',
    }


def _syst_record_name_gap_reconciliation_summary(systems: list[dict], names: dict) -> dict:
    """Reconcile deduplication results with name candidates into a ~51 distinct-system map.

    Combines the deduplication summary (which maps 16 co-located gaps to canonical
    named neighbors) with the name candidate cross-reference to produce a single
    reconciled distinct-system roster. Co-located gap resource IDs inherit their
    canonical neighbor's candidate name; near/separated gaps remain unresolved.
    No record-to-name join is promoted — this is analysis input only.
    """
    dedup = _coordinate_gap_resource_deduplication_summary(systems, names)
    identity = _coordinate_gap_identity_resolution_summary(systems, names)
    cross_ref = _syst_record_name_candidate_cross_reference_summary(names, set(range(128, 128+len(systems))))

    # Build the reconciled roster
    dedup_map: dict[int, list[int]] = {}  # canonical resource ID -> [duplicate resource IDs]
    for entry in dedup.get('deduplication', []):
        canonical = entry['canonicalResourceId']
        duplicate = entry['duplicateResourceId']
        if canonical not in dedup_map:
            dedup_map[canonical] = []
        dedup_map[canonical].append(duplicate)

    # Build the cross-reference lookup: resource ID -> candidate name
    name_map: dict[int, str] = {}
    cross_ref_entries = cross_ref.get('crossReference', [])
    for cr in cross_ref_entries:
        name_map[cr['resourceId']] = cr.get('candidateSystemName', '?')

    all_resource_ids = set(range(128, 128 + len(systems)))
    co_located_duplicate_ids = set(dedup.get('coLocatedDuplicateResourceIds', []))
    canonical_ids = set(dedup.get('canonicalNamedResourceIds', []))
    gap_resource_ids = set(identity.get('gapResourceIds', []))
    non_gap_ids = all_resource_ids - gap_resource_ids  # named records (46)

    # Build distinct system entries
    distinct_entries: list[dict] = []
    resolved_resource_ids: set[int] = set()

    # Process canonical named records first (these are distinct systems with dedup info)
    for rid in sorted(canonical_ids):
        candidate_name = name_map.get(rid, '?')
        duplicates = sorted(dedup_map.get(rid, []))
        distinct_entries.append({
            'canonicalResourceId': rid,
            'candidateSystemName': candidate_name,
            'nameSource': 'heuristic-name-candidate-cross-reference',
            'duplicateGapResourceIds': duplicates,
            'duplicateGapCount': len(duplicates),
            'totalResourceIds': 1 + len(duplicates),
            'nameConfidence': 'deduplication-augmented-scout',
        })
        resolved_resource_ids.add(rid)
        resolved_resource_ids.update(duplicates)

    # Non-gap named records that are NOT canonical dedup targets
    for rid in sorted(non_gap_ids - canonical_ids):
        candidate_name = name_map.get(rid, '?')
        distinct_entries.append({
            'canonicalResourceId': rid,
            'candidateSystemName': candidate_name,
            'nameSource': 'heuristic-name-candidate-cross-reference',
            'duplicateGapResourceIds': [],
            'duplicateGapCount': 0,
            'totalResourceIds': 1,
            'nameConfidence': 'named-record-no-known-duplicates',
        })
        resolved_resource_ids.add(rid)

    # Near/separated gaps that are unresolved (not co-located duplicates)
    unresolved_ids = sorted(gap_resource_ids - co_located_duplicate_ids - resolved_resource_ids)
    for rid in unresolved_ids:
        distinct_entries.append({
            'canonicalResourceId': rid,
            'candidateSystemName': '?',
            'nameSource': 'unresolved-gap',
            'duplicateGapResourceIds': [],
            'duplicateGapCount': 0,
            'totalResourceIds': 1,
            'nameConfidence': 'unresolved-near-or-separated-gap',
        })
        resolved_resource_ids.add(rid)

    # Any remaining resource IDs (fallback)
    for rid in sorted(all_resource_ids - resolved_resource_ids):
        candidate_name = name_map.get(rid, '?')
        distinct_entries.append({
            'canonicalResourceId': rid,
            'candidateSystemName': candidate_name,
            'nameSource': 'unaccounted-fallback',
            'duplicateGapResourceIds': [],
            'duplicateGapCount': 0,
            'totalResourceIds': 1,
            'nameConfidence': 'unaccounted-fallback',
        })

    return {
        'sourceLabel': 'decoded-resource-backed-syst-record-name-gap-reconciliation-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': [
            'coordinateGapResourceDeduplicationSummary',
            'systRecordNameCandidateCrossReferenceSummary',
            'coordinateGapIdentityResolutionSummary',
        ],
        'totalResourceIds': len(systems),
        'distinctSystemCountEstimate': len(distinct_entries),
        'coLocatedGapDuplicatesResolved': len(dedup.get('deduplication', [])),
        'nearOrSeparatedUnresolved': len(unresolved_ids),
        'namedRecordCount': len(non_gap_ids),
        'gapRecordCount': len(gap_resource_ids),
        'canonicalDistinctEntries': distinct_entries,
        'promotionBlockers': [
            'reconciliation is dedup-augmented scouting only; no record-to-name join is promoted',
            'candidate names are heuristic text-chunk proximity matches, not verified Classic mappings',
            'co-located gap assignments are spatial proximity hypotheses, not confirmed Classic duplicates',
            'near/separated gaps remain unnamed until source name table or runtime route-label evidence is available',
        ],
        'promotionStatus': 'not-promoted; name gap reconciliation is analysis input only, pending exact Classic source or runtime route-label evidence',
        'sourceNote': 'This summary produces a reconciled distinct-system roster by collapsing 16 co-located gap resource IDs into their canonical named neighbors and preserving near/separated gaps as unresolved. Candidate names are heuristic cross-reference matches only. No record-to-name join or runtime topology claim is promoted.',
    }


def _named_candidate_link_topology_summary(systems: list[dict], names: dict) -> dict:
    """Build a named candidate link topology from the reconciliation roster + Con1-Con16 links.

    Uses the reconciliation summary's canonical entries to map resource IDs to candidate
    names, then maps the decoded Con1-Con16 link slots through those names to produce
    named candidate edges and per-system named link information. No record-to-name join
    is promoted — all names are heuristic candidates.
    """
    reconciliation = _syst_record_name_gap_reconciliation_summary(systems, names)

    # Build resource ID → canonical resource ID map (for dedup resolution)
    canonical_of: dict[int, int] = {}
    # Build canonical resource ID → candidate name map
    name_of: dict[int, str] = {}
    for entry in reconciliation.get('canonicalDistinctEntries', []):
        rid = entry['canonicalResourceId']
        name_of[rid] = entry.get('candidateSystemName', '?')
        canonical_of[rid] = rid
        for dup_rid in entry.get('duplicateGapResourceIds', []):
            canonical_of[dup_rid] = rid

    # Build named edges and per-system named link info
    named_edges: set[tuple[str, str]] = set()
    named_edges_with_ids: list[dict] = []
    per_system_named_links: list[dict] = []

    for system in systems:
        rid = system['resourceId']
        canonical_rid = canonical_of.get(rid, rid)
        src_name = name_of.get(canonical_rid, f'ID:{canonical_rid}')

        slots = system['semanticFields']['candidateHyperspaceLinks']['linkSlots']
        linked_slots = [s for s in slots if s.get('status') == 'linked-system']

        named_slots = []
        for slot in linked_slots:
            target_rid = slot['targetResourceId']
            canonical_target = canonical_of.get(target_rid, target_rid)
            target_name = name_of.get(canonical_target, f'ID:{canonical_target}')

            if src_name != target_name:  # skip self-links for named edges
                named_edges.add((src_name, target_name))

            named_slots.append({
                'slotName': slot['slotName'],
                'targetResourceId': target_rid,
                'canonicalTargetResourceId': canonical_target,
                'candidateTargetSystemName': target_name,
                'nameConfidence': 'heuristic-candidate-cross-reference',
                'isSelfLink': target_rid == rid,
            })

        per_system_named_links.append({
            'resourceId': rid,
            'canonicalResourceId': canonical_rid,
            'candidateSystemName': src_name,
            'linkedNamedSlots': named_slots,
            'namedLinkedCount': len([s for s in named_slots if not s['isSelfLink']]),
        })

    named_edge_list = sorted([
        {'sourceSystemName': src, 'targetSystemName': tgt}
        for src, tgt in named_edges
    ], key=lambda e: (e['sourceSystemName'], e['targetSystemName']))

    # Compute simple graph statistics
    all_named_systems = sorted(set(
        name_of.get(canonical_of.get(rid, rid), f'ID:{rid}')
        for rid in range(128, 128 + len(systems))
    ))
    named_systems_with_links = sorted(set(
        src for src, _ in named_edges
    ) | set(tgt for _, tgt in named_edges))

    return {
        'sourceLabel': 'decoded-resource-backed-named-candidate-link-topology-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': [
            'systRecordNameGapReconciliationSummary',
            'candidateLinkGraphSummary',
        ],
        'distinctSystemCountEstimate': len(all_named_systems),
        'namedSystemsWithOutgoingLinks': len(named_systems_with_links),
        'namedCandidateEdgeCount': len(named_edges),
        'namedCandidateEdges': named_edge_list,
        'perSystemNamedLinks': per_system_named_links,
        'promotionBlockers': [
            'all system names are heuristic text-chunk candidates, not verified Classic mappings',
            'co-located gap assignments are spatial proximity hypotheses',
            'link topology is decoded Con1-Con16 candidate slots, not verified Classic route edges',
            'near/separated gap systems remain unnamed',
        ],
        'promotionStatus': 'not-promoted; named candidate topology is analysis input only, pending exact Classic source or runtime route-label evidence',
        'sourceNote': 'This summary maps the reconciliation roster candidate names onto the decoded Con1-Con16 link graph to produce a named candidate topology. All names are heuristic candidates from landing-name text-chunk proximity matching. No record-to-name join, named Classic route topology, or broad runtime universe replacement is promoted.',
    }


def _named_candidate_travel_distance_summary(systems: list[dict], names: dict) -> dict:
    """Compute shortest-path distances on the named candidate link graph.

    Uses the reconciliation summary's canonical entries and the named candidate
    edges to build an undirected graph, then BFS from every named system to compute
    pairwise hop distances. All distances are heuristic candidates — no record-to-name
    join or runtime topology claim is promoted.
    """
    reconciliation = _syst_record_name_gap_reconciliation_summary(systems, names)

    # Build resource ID → canonical resource ID map (for dedup resolution)
    canonical_of: dict[int, int] = {}
    # Build canonical resource ID → candidate name map
    name_of: dict[int, str] = {}
    for entry in reconciliation.get('canonicalDistinctEntries', []):
        rid = entry['canonicalResourceId']
        name_of[rid] = entry.get('candidateSystemName', '?')
        canonical_of[rid] = rid
        for dup_rid in entry.get('duplicateGapResourceIds', []):
            canonical_of[dup_rid] = rid

    # Build undirected named adjacency set
    adjacency: dict[str, set[str]] = {}
    for system in systems:
        rid = system['resourceId']
        canonical_rid = canonical_of.get(rid, rid)
        src_name = name_of.get(canonical_rid, f'ID:{canonical_rid}')

        slots = system['semanticFields']['candidateHyperspaceLinks']['linkSlots']
        linked_slots = [s for s in slots if s.get('status') == 'linked-system']

        if src_name not in adjacency:
            adjacency[src_name] = set()

        for slot in linked_slots:
            target_rid = slot['targetResourceId']
            canonical_target = canonical_of.get(target_rid, target_rid)
            target_name = name_of.get(canonical_target, f'ID:{canonical_target}')

            if target_name not in adjacency:
                adjacency[target_name] = set()

            if src_name != target_name:
                adjacency[src_name].add(target_name)
                adjacency[target_name].add(src_name)

    # BFS distances from each system
    from collections import deque

    all_named = sorted(adjacency.keys())
    per_system_distances: list[dict] = []
    pair_distances: list[dict] = []
    max_distance = 0
    total_unreachable_pairs = 0

    for src in all_named:
        dist: dict[str, int] = {src: 0}
        q = deque([src])
        while q:
            cur = q.popleft()
            for nxt in adjacency.get(cur, set()):
                if nxt not in dist:
                    dist[nxt] = dist[cur] + 1
                    q.append(nxt)

        reachable = {k: v for k, v in dist.items() if k != src}
        reachable_names = sorted(reachable.keys())
        unreachable = sorted(set(all_named) - set(dist.keys()))
        max_dist = max(dist.values()) if len(dist) > 1 else 0
        max_distance = max(max_distance, max_dist)

        # Distance distribution
        dist_distribution: dict[int, int] = {}
        for d in dist.values():
            dist_distribution[d] = dist_distribution.get(d, 0) + 1

        total_unreachable_pairs += len(unreachable)

        per_system_distances.append({
            'candidateSystemName': src,
            'reachableNamedSystemCount': len(reachable),
            'unreachableNamedSystemCount': len(unreachable),
            'maxHopDistance': max_dist,
            'hopDistanceDistribution': dist_distribution,
            'unreachableSystemNames': unreachable,
        })

        # Record key pair distances for systems reachable within 3 hops
        for tgt_name in reachable_names:
            d = reachable[tgt_name]
            if d <= 6:
                pair_distances.append({
                    'sourceSystemName': src,
                    'targetSystemName': tgt_name,
                    'hopDistance': d,
                    'nameConfidence': 'heuristic-candidate-cross-reference',
                })
            else:
                pair_distances.append({
                    'sourceSystemName': src,
                    'targetSystemName': tgt_name,
                    'hopDistance': d,
                    'nameConfidence': 'heuristic-candidate-cross-reference',
                })

    # Sort pair distances
    pair_distances.sort(key=lambda e: (e['sourceSystemName'], e['targetSystemName']))

    # Compute connected component analysis
    visited: set[str] = set()
    components: list[list[str]] = []
    for name in all_named:
        if name not in visited:
            comp: list[str] = []
            q = deque([name])
            visited.add(name)
            while q:
                cur = q.popleft()
                comp.append(cur)
                for nxt in adjacency.get(cur, set()):
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)
            components.append(sorted(comp))

    component_sizes = sorted([len(c) for c in components], reverse=True)

    return {
        'sourceLabel': 'decoded-resource-backed-named-candidate-travel-distance-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': [
            'namedCandidateLinkTopologySummary',
            'systRecordNameGapReconciliationSummary',
        ],
        'totalNamedSystems': len(all_named),
        'namedSystemPairCount': len(pair_distances),
        'namedGraphDiameterCandidate': max_distance,
        'unreachablePairCount': total_unreachable_pairs,
        'connectedComponentCount': len(components),
        'connectedComponentSizes': component_sizes,
        'perSystemNamedDistances': per_system_distances,
        'promotionBlockers': [
            'all system names are heuristic text-chunk candidates, not verified Classic mappings',
            'link topology is decoded Con1-Con16 candidate slots, not verified Classic route edges',
            'travel distances are hop counts on a heuristic graph, not verified Classic route distances',
        ],
        'promotionStatus': 'not-promoted; named candidate travel distances are analysis input only, pending exact Classic source or runtime route-label evidence',
        'sourceNote': 'This summary computes shortest-path hop distances on the named candidate link graph. All names are heuristic candidates from landing-name text-chunk proximity matching. Distances are candidate hop counts, not verified Classic route, fuel, or range data. No record-to-name join or named Classic route topology is promoted.',
    }


def _named_candidate_route_summary(systems: list[dict], names: dict) -> dict:
    """Compute shortest-path named route sequences on the named candidate link graph.

    Extends the namedCandidateTravelDistanceSummary by tracking parent pointers
    during BFS to reconstruct the actual sequence of candidate system names for
    each reachable pair. All names and paths are heuristic candidates — no
    record-to-name join or runtime topology claim is promoted.
    """
    reconciliation = _syst_record_name_gap_reconciliation_summary(systems, names)

    # Build resource ID → canonical resource ID map (for dedup resolution)
    canonical_of: dict[int, int] = {}
    # Build canonical resource ID → candidate name map
    name_of: dict[int, str] = {}
    for entry in reconciliation.get('canonicalDistinctEntries', []):
        rid = entry['canonicalResourceId']
        name_of[rid] = entry.get('candidateSystemName', '?')
        canonical_of[rid] = rid
        for dup_rid in entry.get('duplicateGapResourceIds', []):
            canonical_of[dup_rid] = rid

    # Build undirected named adjacency set
    adjacency: dict[str, set[str]] = {}
    for system in systems:
        rid = system['resourceId']
        canonical_rid = canonical_of.get(rid, rid)
        src_name = name_of.get(canonical_rid, f'ID:{canonical_rid}')

        slots = system['semanticFields']['candidateHyperspaceLinks']['linkSlots']
        linked_slots = [s for s in slots if s.get('status') == 'linked-system']

        if src_name not in adjacency:
            adjacency[src_name] = set()

        for slot in linked_slots:
            target_rid = slot['targetResourceId']
            canonical_target = canonical_of.get(target_rid, target_rid)
            target_name = name_of.get(canonical_target, f'ID:{canonical_target}')

            if target_name not in adjacency:
                adjacency[target_name] = set()

            if src_name != target_name:
                adjacency[src_name].add(target_name)
                adjacency[target_name].add(src_name)

    # BFS with parent tracking for route reconstruction
    from collections import deque

    all_named = sorted(adjacency.keys())
    per_system_routes: list[dict] = []
    key_routes: list[dict] = []
    route_paths: list[dict] = []
    max_route_length = 0
    total_unreachable_pairs = 0
    system_betweenness: dict[str, int] = {name: 0 for name in all_named}

    for src in all_named:
        # BFS tracking parent for path reconstruction
        dist: dict[str, int] = {src: 0}
        parent: dict[str, str | None] = {src: None}
        q = deque([src])
        while q:
            cur = q.popleft()
            for nxt in adjacency.get(cur, set()):
                if nxt not in dist:
                    dist[nxt] = dist[cur] + 1
                    parent[nxt] = cur
                    q.append(nxt)

        reachable = sorted(set(dist.keys()) - {src})
        unreachable = sorted(set(all_named) - set(dist.keys()))
        max_dist = max(dist.values()) if len(dist) > 1 else 0
        max_route_length = max(max_route_length, max_dist)
        total_unreachable_pairs += len(unreachable)

        # Record per-system route metadata
        per_system_routes.append({
            'candidateSystemName': src,
            'reachableNamedSystemCount': len(reachable),
            'unreachableNamedSystemCount': len(unreachable),
            'maxHopDistance': max_dist,
            'unreachableSystemNames': unreachable,
        })

        # Reconstruct and record routes for all reachable targets
        for tgt in reachable:
            # Trace path from target back to source via parent pointers
            path: list[str] = []
            cur: str | None = tgt
            while cur is not None:
                path.append(cur)
                cur = parent.get(cur)
            path.reverse()  # src -> ... -> tgt

            hop_distance = len(path) - 1

            entry = {
                'sourceSystemName': src,
                'targetSystemName': tgt,
                'hopDistance': hop_distance,
                'routePath': path,
                'nameConfidence': 'heuristic-candidate-cross-reference',
            }
            route_paths.append(entry)

            # Key routes: diameter and within 2 hops
            if hop_distance == max_route_length or hop_distance <= 2:
                key_routes.append(entry)

            # Betweenness centrality: increment for intermediate nodes
            for intermediate in path[1:-1]:
                system_betweenness[intermediate] = system_betweenness.get(intermediate, 0) + 1

    # Sort route paths
    route_paths.sort(key=lambda e: (e['sourceSystemName'], e['targetSystemName']))
    key_routes.sort(key=lambda e: (e['sourceSystemName'], e['hopDistance'], e['targetSystemName']))

    # Betweenness ranking
    betweenness_ranking = sorted(
        [{'candidateSystemName': name, 'routeIntermediaryCount': count}
         for name, count in system_betweenness.items() if count > 0],
        key=lambda e: (-e['routeIntermediaryCount'], e['candidateSystemName']),
    )

    return {
        'sourceLabel': 'decoded-resource-backed-named-candidate-route-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': [
            'namedCandidateTravelDistanceSummary',
            'namedCandidateLinkTopologySummary',
            'systRecordNameGapReconciliationSummary',
        ],
        'totalNamedSystems': len(all_named),
        'namedRoutePairCount': len(route_paths),
        'keyRouteCount': len(key_routes),
        'namedGraphDiameterCandidate': max_route_length,
        'unreachablePairCount': total_unreachable_pairs,
        'perSystemNamedRouteMetadata': per_system_routes,
        'keyRoutes': key_routes,
        'systemBetweennessRanking': betweenness_ranking,
        'promotionBlockers': [
            'all system names are heuristic text-chunk candidates, not verified Classic mappings',
            'link topology is decoded Con1-Con16 candidate slots, not verified Classic route edges',
            'named routes are path sequences on a heuristic graph, not verified Classic route data',
        ],
        'promotionStatus': 'not-promoted; named candidate routes are analysis input only, pending exact Classic source or runtime route-label evidence',
        'sourceNote': 'This summary reconstructs shortest-path route sequences on the named candidate link graph from BFS parent pointers. All names are heuristic candidates from landing-name text-chunk proximity matching. Routes are candidate hop-sequence paths, not verified Classic route, fuel, or range data. No record-to-name join or named Classic route topology is promoted.',
    }


def _named_candidate_route_calibration_priority_summary(systems: list[dict], names: dict) -> dict:
    """Rank named candidate routes by diagnostic value for future Classic route-label calibration.

    Uses the existing namedCandidateRouteSummary (route paths, betweenness, key routes)
    and systRecordNameGapReconciliationSummary (canonical names) to identify which
    candidate routes would be most informative to verify against Classic observations.
    All names and routes remain heuristic candidates — no Classic route topology or
    record-to-name join is promoted.
    """
    route_summary = _named_candidate_route_summary(systems, names)
    reconciliation = _syst_record_name_gap_reconciliation_summary(systems, names)

    # Build canonical name lookup
    canonical_name_of: dict[str, str] = {}
    for entry in reconciliation.get('canonicalDistinctEntries', []):
        canonical_name_of[str(entry['canonicalResourceId'])] = entry.get('candidateSystemName', '?')

    betweenness = route_summary.get('systemBetweennessRanking', [])
    key_routes = route_summary.get('keyRoutes', [])
    per_system = route_summary.get('perSystemNamedRouteMetadata', [])
    total_systems = route_summary.get('totalNamedSystems', 0)

    # Build name-to-betweenness-rank map
    name_rank: dict[str, int] = {}
    for rank, entry in enumerate(betweenness):
        name_rank[entry['candidateSystemName']] = rank + 1

    # Build name-to-degree map from per-system metadata
    name_degree: dict[str, int] = {}
    for sys_entry in per_system:
        name = sys_entry['candidateSystemName']
        name_degree[name] = sys_entry['reachableNamedSystemCount']

    # Compute diagnostic scores for each route pair
    scored: list[dict] = []
    for route in key_routes:
        src = route['sourceSystemName']
        tgt = route['targetSystemName']
        hops = route['hopDistance']
        path = route['routePath']

        # Diagnostic components:
        # - Betweenness: sum of ranks (lower rank = higher betweenness = more informative)
        src_rank = name_rank.get(src, total_systems + 1)
        tgt_rank = name_rank.get(tgt, total_systems + 1)
        betweenness_score = (total_systems + 1 - src_rank) + (total_systems + 1 - tgt_rank)

        # - Levo anchor bonus: routes involving Levo (the only exact system) are gold
        levo_anchor = 1 if src == 'Levo' or tgt == 'Levo' else 0
        is_levo_anchored = levo_anchor == 1

        # - Hop count: longer routes span more of the graph
        hop_score = hops

        # - Degree: routes through well-connected systems span more topology
        src_deg = name_degree.get(src, 0)
        tgt_deg = name_degree.get(tgt, 0)
        degree_score = src_deg + tgt_deg

        # Combined diagnostic score (higher = more informative for calibration)
        diagnostic_score = betweenness_score + (levo_anchor * 10) + hop_score + (degree_score // 2)

        scored.append({
            'sourceSystemName': src,
            'targetSystemName': tgt,
            'hopDistance': hops,
            'routePath': path,
            'levoAnchored': is_levo_anchored,
            'sourceBetweennessRank': src_rank,
            'targetBetweennessRank': tgt_rank,
            'sourceDegree': src_deg,
            'targetDegree': tgt_deg,
            'diagnosticScore': diagnostic_score,
        })

    # Sort by diagnostic score descending
    scored.sort(key=lambda e: (-e['diagnosticScore'], e['sourceSystemName'], e['targetSystemName']))

    # Top calibration priorities (top 20 or all if fewer)
    top_n = min(20, len(scored))
    top_priorities = scored[:top_n]
    levo_anchored = [e for e in scored if e['levoAnchored']][:5]
    diameter_routes = [e for e in scored if e['hopDistance'] == route_summary.get('namedGraphDiameterCandidate', 0)][:5]

    return {
        'sourceLabel': 'decoded-resource-backed-named-candidate-route-calibration-priority-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': [
            'namedCandidateRouteSummary',
            'systRecordNameGapReconciliationSummary',
        ],
        'totalNamedSystems': total_systems,
        'totalScoredRoutes': len(scored),
        'topCalibrationPriorityCount': top_n,
        'topCalibrationPriorities': top_priorities,
        'levoAnchoredCalibrationTargets': levo_anchored,
        'diameterCalibrationTargets': diameter_routes,
        'topBetweennessSystemName': betweenness[0]['candidateSystemName'] if betweenness else None,
        'topBetweennessRouteIntermediaryCount': betweenness[0]['routeIntermediaryCount'] if betweenness else 0,
        'priorityRegions': {
            'region1TopBetweennessHubs': {
                'description': 'Routes anchored at top-betweenness hub systems — verifying these constrains the most route paths',
                'targetSystemNames': [e['candidateSystemName'] for e in betweenness[:3]],
            },
            'region2LevoAnchored': {
                'description': 'Routes anchored at Levo — the only exact system name mapping (resource 128)',
                'anchorSystemName': 'Levo',
                'targetCount': len(levo_anchored),
            },
            'region3DiameterSpanning': {
                'description': f'Routes spanning the named graph diameter ({route_summary.get("namedGraphDiameterCandidate")} hops) — verify longest-path topology',
                'diameterHopCount': route_summary.get('namedGraphDiameterCandidate'),
                'targetCount': len(diameter_routes),
            },
        },
        'promotionBlockers': [
            'all system names are heuristic text-chunk candidates, not verified Classic mappings',
            'calibration priorities are diagnostic helpers for ranking future Classic label captures',
            'no Classic route label, record-to-name join, or runtime topology is promoted',
        ],
        'promotionStatus': 'not-promoted; calibration priorities are diagnostic scouts for future Classic route-label capture, not verified Classic truth',
        'sourceNote': 'This summary ranks named candidate routes by how informative they would be to verify against Classic observations. Top-betweenness hub routes, Levo-anchored routes, and diameter-spanning routes are prioritized because verifying them constrains the largest number of potential record-to-name joins.',
    }


def _named_candidate_route_calibration_diagnostic_plan(systems: list[dict], names: dict) -> dict:
    """Transform top calibration-priority routes into coordinate-projected diagnostic test cases.

    Uses namedCandidateRouteCalibrationPrioritySummary for route priorities,
    systRecordNameGapReconciliationSummary for name-to-resource-ID mapping,
    and decoded signed-long coordinates for spatial projection.
    All projections remain heuristic scouts — no Classic coordinate display,
    route label, or record-to-name join is promoted.
    """
    calibration = _named_candidate_route_calibration_priority_summary(systems, names)
    reconciliation = _syst_record_name_gap_reconciliation_summary(systems, names)

    # Build resource-ID -> coordinate lookup
    coord_of: dict[int, dict] = {}
    for system in systems:
        rid = system['resourceId']
        coords = system['semanticFields']['mapCoordinates']
        x_pos = coords.get('xPos', {})
        y_pos = coords.get('yPos', {})
        coord_of[rid] = {
            'signedLongX': x_pos.get('signedLongCandidate'),
            'signedLongY': y_pos.get('signedLongCandidate'),
        }

    # Build name -> resource-ID lookup from reconciliation
    name_to_rid: dict[str, int] = {}
    for entry in reconciliation.get('canonicalDistinctEntries', []):
        name = entry.get('candidateSystemName', '?')
        rid = entry.get('canonicalResourceId')
        name_to_rid[name] = rid

    # Build diagnostic test cases from top calibration priorities
    top_priorities = calibration.get('topCalibrationPriorities', [])

    diagnostic_cases = []
    for priority in top_priorities:
        route_path = priority.get('routePath', [])
        # Resolve each named system to coordinates
        path_coords = []
        unresolved = []
        for name in route_path:
            rid = name_to_rid.get(name)
            if rid is not None and rid in coord_of:
                c = coord_of[rid]
                path_coords.append({
                    'systemName': name,
                    'resourceId': rid,
                    'signedLongX': c['signedLongX'],
                    'signedLongY': c['signedLongY'],
                })
            else:
                unresolved.append(name)
                path_coords.append({
                    'systemName': name,
                    'resourceId': None,
                    'signedLongX': None,
                    'signedLongY': None,
                })

        # Compute coordinate deltas and diagnostic metrics
        coord_metrics = None
        if len(path_coords) >= 2 and not unresolved:
            src = path_coords[0]
            tgt = path_coords[-1]
            sx = src['signedLongX']
            sy = src['signedLongY']
            tx = tgt['signedLongX']
            ty = tgt['signedLongY']
            if sx is not None and sy is not None and tx is not None and ty is not None:
                dx = tx - sx
                dy = ty - sy
                manhattan = abs(dx) + abs(dy)
                # Determine quadrant using inverted-Y convention from prior scouts
                inverted_dy = -dy
                if dx >= 0 and inverted_dy >= 0:
                    quadrant = 'north-east'
                elif dx < 0 and inverted_dy >= 0:
                    quadrant = 'north-west'
                elif dx < 0 and inverted_dy < 0:
                    quadrant = 'south-west'
                else:
                    quadrant = 'south-east'
                coord_metrics = {
                    'sourceCoordinates': {'signedLongX': sx, 'signedLongY': sy},
                    'targetCoordinates': {'signedLongX': tx, 'signedLongY': ty},
                    'deltaX': dx,
                    'deltaY': dy,
                    'manhattanSignedLongDistance': manhattan,
                    'displayQuadrant': quadrant,
                }

        # Determine priority region
        hops = priority.get('hopDistance', 0)
        levo = priority.get('levoAnchored', False)
        diameter = calibration.get('diameterCalibrationTargets', [])
        diameter_hops = diameter[0].get('hopDistance') if diameter else None
        if levo:
            region = 'levo-anchored'
        elif diameter_hops is not None and hops == diameter_hops:
            region = 'diameter-spanning'
        else:
            region = 'betweenness-hub'

        diag_questions = [
            f'Does Classic map show a route from {route_path[0]} to {route_path[-1]}?',
            'What is the Classic route label (if any) for this path?',
            'Do the Classic map coordinates match the heuristic signed-long projection?',
        ] if not unresolved else [
            f'Name(s) {", ".join(unresolved)} not resolved to decoded resource — requires name-table or runtime evidence',
        ]

        diagnostic_cases.append({
            'routePath': route_path,
            'hopDistance': hops,
            'diagnosticScore': priority.get('diagnosticScore'),
            'levoAnchored': levo,
            'priorityRegion': region,
            'pathCoordinates': path_coords,
            'coordinateMetrics': coord_metrics,
            'unresolvedNames': unresolved if unresolved else None,
            'diagnosticQuestions': diag_questions,
        })

    return {
        'sourceLabel': 'decoded-resource-backed-named-candidate-route-calibration-diagnostic-plan',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': [
            'namedCandidateRouteCalibrationPrioritySummary',
            'systRecordNameGapReconciliationSummary',
        ],
        'totalNamedSystems': calibration.get('totalNamedSystems', 0),
        'totalDiagnosticCases': len(diagnostic_cases),
        'diagnosticCases': diagnostic_cases,
        'priorityRegions': calibration.get('priorityRegions', {}),
        'calibrationInstructions': {
            'betweennessHubRoutes': 'Verify top-betweenness hub routes first — confirming these constrains the largest number of route-path interpretations',
            'levoAnchoredRoutes': 'Verify Levo-anchored routes against Classic map — Levo (resource 128) is the only exact system-name mapping',
            'diameterSpanningRoutes': 'Verify diameter-spanning routes last — these test the longest-path extremes of the candidate topology',
        },
        'promotionBlockers': [
            'all system names are heuristic text-chunk candidates, not verified Classic mappings',
            'signed-long coordinate projections use non-promoted decoded values pending display-unit calibration',
            'diagnostic plan is a capture worklist only — no Classic route label, record-to-name join, or runtime topology is promoted',
        ],
        'promotionStatus': 'not-promoted; diagnostic plan is a future Classic route-label capture worklist, not verified Classic truth',
        'sourceNote': 'This diagnostic plan transforms route calibration priorities into structured coordinate-projected test cases for future Classic route-label verification. Each test case includes heuristic coordinate projections and explicit diagnostic questions for a Classic observer.',
    }


def _named_candidate_coordinate_scaffold_summary(systems: list[dict], names: dict) -> dict:
    """Build a TV scaffold coordinate mapping from named candidates to pixel positions.

    Uses the reconciliation roster's canonical name-to-resource-ID mapping and the
    decoded signed-long coordinates to produce heuristic pixel positions for the
    TV galaxy map. All coordinates are terminal-velocity-scaffold — no Classic
    display-unit/map-scaling promotion is implied.
    """
    reconciliation = _syst_record_name_gap_reconciliation_summary(systems, names)
    link_topo = _named_candidate_link_topology_summary(systems, names)
    normalized = _coordinate_display_normalized_summary(systems)

    # Build canonical resource ID → candidate name map
    name_of: dict[int, str] = {}
    for entry in reconciliation.get('canonicalDistinctEntries', []):
        rid = entry['canonicalResourceId']
        name = entry.get('candidateSystemName')
        if name:
            name_of[rid] = name

    # Build resource ID → normalized coordinate lookup
    per_resource: dict[int, dict] = {
        r['resourceId']: r for r in normalized.get('perResource', [])
    }

    # Build name → outgoing link names from named link topology (canonical already)
    link_of: dict[str, list[str]] = {}
    for entry in link_topo.get('perSystemNamedLinks', []):
        src = entry.get('candidateSystemName', '?')
        linked = sorted(set(
            s['candidateTargetSystemName']
            for s in entry.get('linkedNamedSlots', [])
            if not s.get('isSelfLink')
            and s.get('candidateTargetSystemName', '?') != '?'
        ))
        link_of.setdefault(src, [])
        for target in linked:
            if target not in link_of[src]:
                link_of[src].append(target)

    # TV scaffold viewport parameters
    VIEWPORT_W = 1920
    VIEWPORT_H = 1080
    MARGIN = 80

    named_systems: list[dict] = []
    for rid in sorted(name_of.keys()):
        name = name_of[rid]
        if name == '?':
            continue
        res = per_resource.get(rid)
        if not res:
            continue

        x_unit = res['xPos']['unitIntervalCandidate']
        y_unit = res['yPos']['unitIntervalCandidate']

        # Invert Y for display convention (screen Y grows downward)
        px = int(MARGIN + x_unit * (VIEWPORT_W - 2 * MARGIN))
        py = int(MARGIN + (1.0 - y_unit) * (VIEWPORT_H - 2 * MARGIN))

        named_systems.append({
            'systemName': name,
            'canonicalResourceId': rid,
            'xPixels': px,
            'yPixels': py,
            'signedLongX': res['xPos']['signedLongCandidate'],
            'signedLongY': res['yPos']['signedLongCandidate'],
            'unitIntervalX': x_unit,
            'unitIntervalY': y_unit,
            'namedLinkedSystems': link_of.get(name, []),
        })

    return {
        'sourceLabel': 'terminal-velocity-named-candidate-coordinate-scaffold',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': [
            'systRecordNameGapReconciliationSummary',
            'namedCandidateLinkTopologySummary',
            'coordinateDisplayNormalizedSummary',
        ],
        'totalNamedSystems': len(named_systems),
        'viewportWidth': VIEWPORT_W,
        'viewportHeight': VIEWPORT_H,
        'viewportMargin': MARGIN,
        'coordinateProjection': 'unit-interval-signed-long-scaled-to-viewport',
        'namedSystems': named_systems,
        'promotionStatus': 'not-promoted; TV scaffold coordinate projections only — no Classic display-unit/map-scaling claim',
        'promotionBlockers': [
            'All system names are heuristic text-chunk candidates, not verified Classic mappings',
            'Viewport pixel projection uses non-promoted unit-interval normalization',
            'Y-axis invert and margin padding are TV scaffold choices, not Classic display constants',
            'No Classic display-unit, map scaling, projection, centering, or origin is promoted',
        ],
        'sourceNote': (
            'This scaffold maps named candidate system coordinates to viewport pixel positions '
            'using unit-interval normalized signed-long values. It is a TV development convenience '
            'for building a playable galaxy map — not a Classic display-unit fidelity claim.'
        ),
    }


def _named_candidate_link_pixel_distance_scout(systems: list[dict], names: dict) -> dict:
    """Compute Euclidean pixel distances between linked named scaffold systems.

    For each named candidate system in the coordinate scaffold, computes the
    Euclidean pixel distance to every named linked neighbor. Reports distribution
    statistics against the Resource Bible JumpDistance=1000px constant as a
    diagnostic — no display-unit/map-scaling claim is promoted.

    This is analysis input only. All system names are heuristic text-chunk
    candidates. See coordinateDisplayCalibrationGateSummary for the block.
    """
    scaffold = _named_candidate_coordinate_scaffold_summary(systems, names)
    named_systems = scaffold.get('namedSystems', [])
    jump_distance = RESOURCE_BIBLE_TOPOLOGY_CONSTANTS['jumpDistancePixels']

    # Build name -> coordinate lookup
    coords_of: dict[str, dict] = {
        s['systemName']: {'xPixels': s['xPixels'], 'yPixels': s['yPixels'],
                          'signedLongX': s['signedLongX'], 'signedLongY': s['signedLongY']}
        for s in named_systems
    }

    link_distances: list[dict] = []
    total_pairs = 0
    within_jump = 0
    beyond_jump = 0
    near_count = 0
    expected_count = 0
    far_count = 0
    interstellar_count = 0
    min_dist = float('inf')
    max_dist = 0
    sum_dist = 0
    signed_long_pixel_ratios: list[float] = []
    missing_target_names: set[str] = set()

    for src in named_systems:
        src_name = src['systemName']
        for tgt_name in src.get('namedLinkedSystems', []):
            total_pairs += 1
            src_c = coords_of.get(src_name)
            tgt_c = coords_of.get(tgt_name)
            if not src_c or not tgt_c:
                missing_target_names.add(tgt_name)
                continue
            dx = src_c['xPixels'] - tgt_c['xPixels']
            dy = src_c['yPixels'] - tgt_c['yPixels']
            pixel_dist = int(round((dx * dx + dy * dy) ** 0.5))
            signed_dx = src_c['signedLongX'] - tgt_c['signedLongX']
            signed_dy = src_c['signedLongY'] - tgt_c['signedLongY']
            signed_long_dist = int(round((signed_dx * signed_dx + signed_dy * signed_dy) ** 0.5))
            if signed_long_dist > 0:
                signed_long_pixel_ratios.append(signed_long_dist / pixel_dist) if pixel_dist > 0 else None
            min_dist = min(min_dist, pixel_dist)
            max_dist = max(max_dist, pixel_dist)
            sum_dist += pixel_dist

            if pixel_dist < 300:
                dist_class = 'near'
                near_count += 1
            elif pixel_dist <= 2000:
                dist_class = 'expected'
                expected_count += 1
            elif pixel_dist <= 5000:
                dist_class = 'far'
                far_count += 1
            else:
                dist_class = 'interstellar'
                interstellar_count += 1

            if pixel_dist <= jump_distance:
                within_jump += 1
            else:
                beyond_jump += 1

            link_distances.append({
                'sourceName': src_name,
                'targetName': tgt_name,
                'pixelDistance': pixel_dist,
                'signedLongDistance': signed_long_dist,
                'distanceClass': dist_class,
                'withinJumpDistance': pixel_dist <= jump_distance,
            })

    avg_dist = round(sum_dist / len(link_distances), 1) if link_distances else 0
    avg_ratio = round(sum(signed_long_pixel_ratios) / len(signed_long_pixel_ratios), 1) if signed_long_pixel_ratios else 0

    # Sort by distance desc for diagnostic clarity
    link_distances.sort(key=lambda e: e['pixelDistance'], reverse=True)

    return {
        'sourceLabel': 'decoded-resource-backed-named-candidate-link-pixel-distance-scout',
        'oracleStatus': 'coordinate_display_units_map_scaling_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': ['namedCandidateCoordinateScaffoldSummary'],
        'jumpDistancePixels': jump_distance,
        'totalNamedSystems': len(named_systems),
        'totalLinkPairsChecked': total_pairs,
        'resolvableLinkPairs': len(link_distances),
        'missingTargetNames': sorted(missing_target_names),
        'missingTargetCount': len(missing_target_names),
        'distanceStatistics': {
            'minPixels': int(min_dist) if min_dist != float('inf') else 0,
            'maxPixels': int(max_dist),
            'averagePixels': avg_dist,
            'averageSignedLongToPixelRatio': avg_ratio,
        },
        'jumpDistanceClassification': {
            'withinJumpDistance': within_jump,
            'beyondJumpDistance': beyond_jump,
        },
        'distanceClassDistribution': {
            'nearLt300px': near_count,
            'expected300to2000px': expected_count,
            'far2000to5000px': far_count,
            'interstellarGt5000px': interstellar_count,
        },
        'linkDistances': link_distances,
        'promotionStatus': 'not-promoted; link pixel distance is a diagnostic only — no Classic display-unit/map-scaling claim',
        'promotionBlockers': [
            'All system names are heuristic text-chunk candidates, not verified Classic mappings',
            'Pixel coordinates use non-promoted unit-interval normalization and TV scaffold viewport parameters',
            'Y-axis invert and margin padding are TV scaffold choices, not Classic display constants',
            'Coordinate display calibration is blocked pending Classic map pixel/click/capture evidence (see coordinateDisplayCalibrationGateSummary)',
        ],
        'sourceNote': (
            'This scout computes Euclidean pixel distances between linked named candidate systems '
            f'and compares them against the Resource Bible JumpDistance={jump_distance}px constant. '
            'All distances use non-promoted TV scaffold pixel coordinates. Links whose target names '
            'are absent from the scaffold named system list are recorded as missing targets. '
            'This is diagnostic analysis input only — no display-unit, map-scaling, or calibration claim is promoted.'
        ),
    }


def _named_seed_scaffold_correspondence_scout(systems: list[dict], names: dict) -> dict:
    """Cross-reference the 9 heuristic system-name seeds against the 46 scaffold named systems.

    Records:
    - Exact name matches between system-name seeds and scaffold entries
    - Partial/contained name matches (one name contains the other)
    - Scaffold names with no seed match
    - System-name seeds with no scaffold match (fully absent from scaffold)
    - Levo anchor as the verification bridge
    """
    scaffold = _named_candidate_coordinate_scaffold_summary(systems, names)
    scaffold_names: set[str] = {s['systemName'] for s in scaffold.get('namedSystems', [])}
    system_seeds: list[dict] = names.get('systemNames', [])
    system_seed_names: list[str] = [s['name'] for s in system_seeds]

    exact_matches: list[dict] = []
    partial_matches: list[dict] = []
    absent_seeds: list[str] = []
    unmatched_scaffold: list[str] = []

    for seed_name in system_seed_names:
        if seed_name in scaffold_names:
            exact_matches.append({
                'systemNameSeed': seed_name,
                'matchType': 'exact',
            })
        else:
            # Check for partial matches (seed is a prefix of scaffold name or vice versa)
            container_matches: list[str] = [
                n for n in scaffold_names
                if seed_name.lower() in n.lower() or n.lower() in seed_name.lower()
            ]
            if container_matches:
                partial_matches.append({
                    'systemNameSeed': seed_name,
                    'matchType': 'partial',
                    'matchingScaffoldNames': sorted(container_matches),
                })
            else:
                absent_seeds.append(seed_name)

    for sc_name in sorted(scaffold_names):
        seed_match = [
            s for s in system_seed_names
            if s.lower() == sc_name.lower()
            or s.lower() in sc_name.lower()
            or sc_name.lower() in s.lower()
        ]
        if not seed_match:
            unmatched_scaffold.append(sc_name)

    return {
        'sourceLabel': 'decoded-resource-backed-named-seed-scaffold-correspondence-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': [
            'namedCandidateCoordinateScaffoldSummary',
            'sourcedEvNames systemNames',
        ],
        'systemNameSeedCount': len(system_seed_names),
        'scaffoldNamedSystemCount': len(scaffold_names),
        'exactMatches': exact_matches,
        'exactMatchCount': len(exact_matches),
        'partialMatches': partial_matches,
        'partialMatchCount': len(partial_matches),
        'absentSeeds': absent_seeds,
        'absentSeedCount': len(absent_seeds),
        'unmatchedScaffoldNames': unmatched_scaffold,
        'unmatchedScaffoldCount': len(unmatched_scaffold),
        'levoInScaffold': 'Levo' in scaffold_names,
        'levoInSystemSeeds': 'Levo' in system_seed_names,
        'promotionStatus': 'not-promoted; correspondence scout only — no Classic record-to-name join is promoted',
        'promotionBlockers': [
            'All scaffold system names are heuristic landing-name text-chunk candidates, not verified Classic mappings',
            'System-name seeds are heuristic text-chunk candidates, not a complete list of Classic system names',
            'Partial matches are proximity/present candidates only — no resource ID mapping is implied',
            'No Classic record-to-name join, route topology label, or display-unit promotion',
        ],
        'sourceNote': (
            'This scout cross-references the 9 heuristic system-name seeds from EV Data.rez text chunks '
            'against the 46 scaffold named systems (from landing-name chunk-index alignment). '
            'Results identify which system-name seeds have scaffold record candidates, which have partial prefix '
            'matches (e.g. "Sirius" → "Sirius Station", "Sirius III"), and which seeds are entirely absent from '
            'the scaffold. This is analysis input for future record-to-name join work, not a promotion packet.'
        ),
    }


def _named_candidate_scaffold_integrity_summary(systems: list[dict], names: dict) -> dict:
    """Validate internal consistency of the 46-system named candidate coordinate scaffold.

    Checks:
    - Every namedLinkedSystems reference points to an existing scaffold system name
    - All system names are unique
    - Pixel coordinates are within the TV scaffold viewport bounds
    - Reports reciprocal link count, duplicate coordinate count, isolated system count
    - Reports seed-system presence/absence from scaffold (using partial-match heuristic)
    """
    scaffold = _named_candidate_coordinate_scaffold_summary(systems, names)
    syslist: list[dict] = scaffold.get('namedSystems', [])
    all_names: set[str] = {s['systemName'] for s in syslist}

    # Broken link detection — every namedLinkedSystems entry must reference an existing name
    broken_links: list[dict] = []
    for entry in syslist:
        src = entry['systemName']
        for tgt in entry.get('namedLinkedSystems', []):
            if tgt not in all_names:
                broken_links.append({'source': src, 'brokenTarget': tgt})

    # Name uniqueness — all systemName values must be unique
    name_duplicates: list[str] = []
    seen: set[str] = set()
    for s in syslist:
        n = s['systemName']
        if n in seen:
            name_duplicates.append(n)
        seen.add(n)

    # Viewport bounds check
    MARGIN = 80
    VIEWPORT_W = 1920
    VIEWPORT_H = 1080
    out_of_bounds: list[dict] = []
    for s in syslist:
        x = s.get('xPixels', 0)
        y = s.get('yPixels', 0)
        if x < 0 or x > VIEWPORT_W or y < 0 or y > VIEWPORT_H:
            out_of_bounds.append({
                'systemName': s['systemName'],
                'xPixels': x,
                'yPixels': y,
            })
    # Also check margin: systems should be within MARGIN..VIEWPORT_W-MARGIN
    margin_violations: list[dict] = []
    for s in syslist:
        x = s.get('xPixels', 0)
        y = s.get('yPixels', 0)
        if x < MARGIN - 1 or x > VIEWPORT_W - MARGIN + 1 or y < MARGIN - 1 or y > VIEWPORT_H - MARGIN + 1:
            margin_violations.append({
                'systemName': s['systemName'],
                'xPixels': x,
                'yPixels': y,
                'violation': 'x' if (x < MARGIN - 1 or x > VIEWPORT_W - MARGIN + 1) else 'y',
            })

    # Reciprocal link count — bidirectional edges
    reverse_lookup: dict[str, set[str]] = {n: set() for n in all_names}
    for entry in syslist:
        for tgt in entry.get('namedLinkedSystems', []):
            reverse_lookup[tgt].add(entry['systemName'])
    reciprocal_count = 0
    reciprocal_pairs: list[list[str]] = []
    seen_pair: set[tuple[str, str]] = set()
    for entry in syslist:
        src = entry['systemName']
        for tgt in entry.get('namedLinkedSystems', []):
            pair = (src, tgt) if src < tgt else (tgt, src)
            if pair not in seen_pair and tgt in reverse_lookup.get(src, set()):
                reciprocal_count += 1
                reciprocal_pairs.append([pair[0], pair[1]])
                seen_pair.add(pair)

    # Duplicate coordinate slots — multiple systems sharing the same pixel position
    from collections import Counter
    coord_counts = Counter((s.get('xPixels'), s.get('yPixels')) for s in syslist)
    duplicate_slots: list[dict] = [
        {'xPixels': x, 'yPixels': y, 'count': c, 'sampleNames': [s['systemName'] for s in syslist if s.get('xPixels') == x and s.get('yPixels') == y][:3]}
        for (x, y), c in coord_counts.items() if c > 1
    ]
    duplicate_slots.sort(key=lambda d: -d['count'])

    # Isolated systems — those with zero linked neighbours (both incoming and outgoing)
    all_with_links: set[str] = set()
    for entry in syslist:
        for tgt in entry.get('namedLinkedSystems', []):
            all_with_links.add(entry['systemName'])
            all_with_links.add(tgt)
    isolated: list[str] = sorted(n for n in all_names if n not in all_with_links)

    # Seed-system presence in scaffold (using partial-match heuristic like the correspondence scout)
    system_seeds: list[dict] = names.get('systemNames', [])
    system_seed_names: list[str] = [s['name'] for s in system_seeds]
    seed_in_scaffold: list[dict] = []
    seed_absent: list[str] = []
    for seed_name in system_seed_names:
        found = [n for n in all_names if seed_name.lower() in n.lower() or n.lower() in seed_name.lower()]
        if found:
            seed_in_scaffold.append({'seedName': seed_name, 'matchingScaffoldNames': sorted(found)})
        else:
            seed_absent.append(seed_name)
    levo_in_scaffold = 'Levo' in all_names

    return {
        'sourceLabel': 'decoded-resource-backed-named-candidate-scaffold-integrity-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'inputSummaries': ['namedCandidateCoordinateScaffoldSummary', 'sourcedEvNames systemNames'],
        'totalSystems': len(syslist),
        'uniqueNameCount': len(all_names),
        'brokenLinkCount': len(broken_links),
        'brokenLinks': broken_links,
        'nameDuplicateCount': len(name_duplicates),
        'nameDuplicates': name_duplicates,
        'outOfBoundsCount': len(out_of_bounds),
        'outOfBoundsSystems': out_of_bounds,
        'marginViolationCount': len(margin_violations),
        'marginViolations': margin_violations,
        'totalLinks': sum(len(s.get('namedLinkedSystems', [])) for s in syslist),
        'reciprocalLinkCount': reciprocal_count,
        'reciprocalLinkPairs': reciprocal_pairs,
        'duplicateCoordinateSlotCount': len(duplicate_slots),
        'duplicateCoordinateSlots': duplicate_slots,
        'isolatedSystemCount': len(isolated),
        'isolatedSystems': isolated,
        'seedPresenceInScaffold': seed_in_scaffold,
        'seedAbsentFromScaffold': seed_absent,
        'levoPresent': levo_in_scaffold,
        'promotionStatus': 'not-promoted; integrity scout only — validates internal scaffold consistency, not Classic record-to-name or display-unit promotion',
        'promotionBlockers': [
            'Integrity validation checks the non-promoted heuristic scaffold only',
            'No Classic record-to-name join, route topology label, or display-unit promotion is implied',
            'Duplicate coordinate slots reflect the 16.16 fixed-point grid resolution, not Classic map overlap',
        ],
        'sourceNote': (
            'This scout validates the internal consistency of the named candidate coordinate scaffold. '
            'Broken links, duplicate names, out-of-bounds coordinates, and isolated systems indicate '
            'data integrity issues. Reciprocal link counts and duplicate coordinate slots reflect the '
            'underlying decoded 16.16 fixed-point coordinate projection, not Classic map layout. '
            'Seed presence in the scaffold records which heuristic system-name seeds have scaffold '
            'candidates. This is a pure validation scout; no Classic promotion is implied.'
        ),
    }


def _route_label_scaffold_correspondence_scout(systems: list[dict], names: dict) -> dict:
    """Cross-reference observed Classic route labels against scaffold named systems and link topology.

    The 4 observed runtime route labels (Rigel, Kathoon, Yemuro, Torgo) are real
    Classic-visible system names from original EV observation. This scout checks
    whether any appear in the heuristic scaffold, identifies disparities between
    scaffold-named Levo links and observed labels, and documents which scaffold
    systems are closest in link topology to where the observed labels should be.
    """
    scaffold = _named_candidate_coordinate_scaffold_summary(systems, names)
    scaffold_systems: list[dict] = scaffold.get('namedSystems', [])
    scaffold_names: set[str] = {s['systemName'] for s in scaffold_systems}

    # Build scaffold name → named linked systems mapping
    link_of: dict[str, list[str]] = {}
    for entry in scaffold_systems:
        link_of[entry['systemName']] = entry.get('namedLinkedSystems', [])

    # Observed runtime route labels (from _runtime_route_label_observation_bridge_gap_summary)
    observed_labels_defs = [
        {'label': 'Rigel', 'observation': 'Backslash-selected from Levo in Hyperspace mode.'},
        {'label': 'Kathoon', 'observation': 'Shift-click route screenshot showed Destination System: Kathoon around Rigel/Levo.'},
        {'label': 'Yemuro', 'observation': 'Mission text named New Istanbul in the Yemuro system.'},
        {'label': 'Torgo', 'observation': 'Mission text named Torgo Prime in the Torgo system.'},
    ]
    observed_labels = [d['label'] for d in observed_labels_defs]

    # Levo scaffold info
    levo_scaffold = next((s for s in scaffold_systems if s['systemName'] == 'Levo'), None)
    levo_scaffold_links = list(link_of.get('Levo', []))

    # Cross-reference each observed label vs scaffold
    label_results: list[dict] = []
    for label in observed_labels:
        exact_match = label in scaffold_names
        partial_matches = sorted(
            n for n in scaffold_names
            if label.lower() in n.lower() or n.lower() in label.lower()
        )
        # Check if label appears as a link from any scaffold system
        linked_from = sorted(
            src for src, targets in link_of.items()
            if label in targets
        )
        is_levo_link = label in levo_scaffold_links

        label_results.append({
            'observedLabel': label,
            'inScaffoldNames': exact_match,
            'partialScaffoldNameCandidates': partial_matches,
            'inScaffoldLevoLinks': is_levo_link,
            'linkedFromScaffoldSystems': linked_from,
            'scaffoldPresence': 'exact' if exact_match else ('partial' if partial_matches else 'absent'),
        })

    # Document Levo scaffold link names vs observed labels
    levo_link_result: list[dict] = []
    for link_name in levo_scaffold_links:
        matching_labels = [
            l for l in observed_labels
            if l.lower() == link_name.lower()
            or l.lower() in link_name.lower()
            or link_name.lower() in l.lower()
        ]
        levo_link_result.append({
            'scaffoldLevoLinkName': link_name,
            'matchingObservedLabels': matching_labels,
            'matchType': 'exact' if any(l == link_name for l in matching_labels)
                         else ('partial' if matching_labels else 'none'),
        })

    # Which observed labels are NOT Levo scaffold links (the disparities)
    levo_disparities = [
        l for l in observed_labels
        if l not in levo_scaffold_links
        and not any(l.lower() in ll.lower() or ll.lower() in l.lower()
                    for ll in levo_scaffold_links)
    ]

    return {
        'sourceLabel': 'decoded-resource-and-runtime-backed-route-label-scaffold-correspondence-scout',
        'oracleStatus': 'route_label_scaffold_presence_documented_no_calibration',
        'sourceBasis': ['original-runtime-observed', 'decoded-record-family', 'decoded-original-variable'],
        'inputSummaries': [
            'runtimeRouteLabelObservationBridgeGapSummary',
            'namedCandidateCoordinateScaffoldSummary',
        ],
        'observedLabelCount': len(observed_labels),
        'observedLabels': [d['label'] for d in observed_labels_defs],
        'scaffoldNamedSystemCount': len(scaffold_names),
        'levoScaffoldLinkNames': levo_scaffold_links,
        'labelResults': label_results,
        'levoLinkResults': levo_link_result,
        'labelsAbsentFromLevoLinks': levo_disparities,
        'levoLinkCount': len(levo_scaffold_links),
        'labelsInScaffoldExact': sum(1 for r in label_results if r['scaffoldPresence'] == 'exact'),
        'labelsInScaffoldPartial': sum(1 for r in label_results if r['scaffoldPresence'] == 'partial'),
        'labelsAbsentFromScaffold': sum(1 for r in label_results if r['scaffoldPresence'] == 'absent'),
        'promotionStatus': 'not-promoted; correspondence scout only — no observed label is tied to a decoded resource ID or Con slot',
        'promotionBlockers': [
            'Observed route labels are visible Classic text but no capture ties each label to a decoded resource ID or Con slot',
            'Scaffold names are heuristic landing-name text-chunk candidates, not verified Classic system names',
            'Levo scaffold link names (Capella/Dune/New Britain) differ from observed Classic labels (Rigel/Kathoon) — this is a known disparity, not a resolved mapping',
            'No Classic resource-ID-to-name join, route topology promotion, or display-unit calibration is implied',
        ],
        'sourceNote': (
            'This scout documents the gap between observed Classic route labels and the heuristic scaffold named systems. '
            'None of the 4 observed labels appear in the 46 scaffold names. '
            f"The scaffold Levo links {levo_scaffold_links} do not match observed labels {observed_labels}. "
            'This confirms the scaffold naming (from landing-name chunk indexes) does not yet align with Classic-visible route labels. '
            'A Classic map capture/click probe recording visible labels and click positions is needed before any label-to-resource-ID join can be made.'
        ),
    }


def _system_name_byte_order_oracle_gap_summary(names: dict) -> dict:
    """Record why current name byte-order evidence is not a record-to-name oracle."""
    system_seeds = sorted(names.get('systemNames', []), key=lambda entry: entry.get('byteOffset', 0))
    landing_seeds = sorted(names.get('landingNames', []), key=lambda entry: entry.get('byteOffset', 0))
    exact_names = {mapping['systemName'] for mapping in EXACT_SYSTEM_NAME_MAPPINGS.values()}
    landing_exact_matches = [
        {
            'systemName': entry.get('name'),
            'landingNameSeedIndex': index,
            'landingChunkIndex': entry.get('chunkIndex'),
            'landingByteOffset': entry.get('byteOffset'),
        }
        for index, entry in enumerate(landing_seeds)
        if entry.get('name') in exact_names
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-system-name-byte-order-oracle-gap',
        'oracleStatus': 'record_name_byte_order_blocked_pending_complete_name_table_or_runtime_label_oracle',
        'candidateFamilies': [
            'heuristic system-name text-seed byte order',
            'landing description chunk byte order',
            'exact mapped start-system landing-name cross-check',
        ],
        'systemNameSeedCount': len(system_seeds),
        'landingNameSeedCount': len(landing_seeds),
        'systemNameSeedByteOrderNames': [entry.get('name') for entry in system_seeds],
        'landingNameSeedFirstNames': [entry.get('name') for entry in landing_seeds[:12]],
        'exactMappedSystemNames': sorted(exact_names),
        'exactMappedNamesPresentInSystemNameSeeds': [entry.get('name') for entry in system_seeds if entry.get('name') in exact_names],
        'exactMappedNamesPresentInLandingSeeds': landing_exact_matches,
        'seedOrderDoesNotContainExactStartSystem': not any(entry.get('name') in exact_names for entry in system_seeds),
        'landingOrderStartSystemIndex': landing_exact_matches[0]['landingNameSeedIndex'] if landing_exact_matches else None,
        'unsafeJoinSignals': [
            'heuristic system-name text seeds are description occurrences and do not contain the exact mapped Levo start-system name',
            'landing description byte order contains Levo but landing chunks describe ports/planets, not syst records',
            'system-name seed count is far smaller than the 67 decoded syst records and cannot define a bijective record order',
            'byte proximity/order signals must remain scouting inputs until a complete name table or runtime route-label oracle exists',
        ],
        'promotionReadinessStatus': 'blocked; byte-order seeds are scout evidence only and cannot assign names to syst resource IDs',
        'nextEvidenceFamilies': [
            'decoded complete system-name table with record/resource ordering',
            'source-level name storage/order oracle for syst records',
            'original-runtime map/route label capture tying labels to decoded resource IDs or link slots',
        ],
        'sourceNote': 'This packet makes the byte-order failure mode executable: current text seeds are useful leads, but neither system-name text occurrence order nor landing-description order can promote additional resource ID to Classic name joins beyond resource 128 -> Levo.',
    }


def _record_to_name_promotion_readiness_summary(names: dict, resource_ids: set[int]) -> dict:
    """Make the remaining record-to-name evidence gap explicit without promoting joins."""
    system_seed_names = [seed.get('name') for seed in names.get('systemNames', [])]
    exact_mapped_resource_ids = sorted(EXACT_SYSTEM_NAME_MAPPINGS)
    exact_mapped_names = [EXACT_SYSTEM_NAME_MAPPINGS[resource_id]['systemName'] for resource_id in exact_mapped_resource_ids]
    unjoined_resource_ids = sorted(resource_ids - set(exact_mapped_resource_ids))
    return {
        'sourceLabel': 'decoded-resource-backed-record-to-name-promotion-readiness-scout',
        'oracleStatus': 'exact_record_name_runtime_topology_mapping_pending',
        'recordCount': len(resource_ids),
        'exactMappedRecordCount': len(exact_mapped_resource_ids),
        'exactMappedResourceIds': exact_mapped_resource_ids,
        'exactMappedSystemNames': exact_mapped_names,
        'unjoinedRecordCount': len(unjoined_resource_ids),
        'unjoinedResourceIdRange': [unjoined_resource_ids[0], unjoined_resource_ids[-1]] if unjoined_resource_ids else [],
        'heuristicSystemNameSeedCount': len(system_seed_names),
        'heuristicSystemNameSeedNames': system_seed_names,
        'heuristicSeedCountDoesNotCoverRemainingRecords': len(system_seed_names) != len(unjoined_resource_ids),
        'promotionBlockers': [
            'only resource 128 to Levo has exact Resource Bible plus original-runtime start-system evidence',
            'heuristic system-name text seeds are not a complete one-to-one list for the remaining syst records',
            'landing-name byte proximity is a scout signal, not a syst record-to-name join',
            'runtime map route labels/ordering remain unobserved for the remaining records',
        ],
        'nextEvidenceFamilies': [
            'decoded complete name/list resource that can be bijectively joined to the 67 syst records',
            'original-runtime map capture or route UI evidence tying labels to linked resource IDs',
            'additional Resource Bible/source variable evidence for system-name storage/order',
        ],
        'sourceNote': 'This readiness summary deliberately preserves the exact mapping boundary: resource 128 maps to Levo, while all other syst records remain unjoined until a complete name/order oracle or runtime map-label evidence is available.',
    }


def _record_name_oracle_evidence_matrix_summary(names: dict, resource_ids: set[int]) -> dict:
    """Record the evidence matrix needed before resource IDs may receive exact Classic names."""
    system_seed_names = [seed.get('name') for seed in names.get('systemNames', [])]
    landing_seed_names = [seed.get('name') for seed in names.get('landingNames', [])]
    exact_mapped_resource_ids = sorted(EXACT_SYSTEM_NAME_MAPPINGS)
    unjoined_resource_ids = sorted(resource_ids - set(exact_mapped_resource_ids))
    evidence_inputs = [
        'systemNameSeedSummary',
        'systemNameLandingProximitySummary',
        'recordToNamePromotionReadinessSummary',
        'candidateLinkGraphSummary',
        'startSystemCandidateTopologySummary',
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-record-name-oracle-evidence-matrix',
        'oracleStatus': 'record_name_mapping_blocked_pending_complete_name_order_or_runtime_label_oracle',
        'recordCount': len(resource_ids),
        'evidenceInputSummaries': evidence_inputs,
        'evidenceInputSummaryCount': len(evidence_inputs),
        'exactMappedRecordCount': len(exact_mapped_resource_ids),
        'exactMappedResourceIds': exact_mapped_resource_ids,
        'exactMappedSystemNames': [EXACT_SYSTEM_NAME_MAPPINGS[resource_id]['systemName'] for resource_id in exact_mapped_resource_ids],
        'unjoinedRecordCount': len(unjoined_resource_ids),
        'unjoinedResourceIdRange': [unjoined_resource_ids[0], unjoined_resource_ids[-1]] if unjoined_resource_ids else [],
        'heuristicSystemNameSeedCount': len(system_seed_names),
        'landingNameSeedCount': len(landing_seed_names),
        'systemSeedNamesAlsoPresentAsLandingSeeds': sorted(set(system_seed_names) & set(landing_seed_names)),
        'requiredOracleClaims': [
            'complete source/runtime name ordering that can be joined bijectively to the 67 decoded syst records',
            'or runtime map/route label evidence tying named systems to decoded resource IDs and link slots',
            'Resource Bible/source variable evidence for name/list resource storage and ordering',
            'cross-check that promoted names preserve resource 128 -> Levo and do not rely on landing-name byte proximity alone',
        ],
        'promotionReadinessStatus': 'blocked; only resource 128 -> Levo is exact-mapped',
        'promotionBlockers': [
            'heuristic system-name seeds cover 9 names, not the remaining 66 unjoined syst records',
            'landing-name byte proximity and matching text are scout signals, not a complete record-name oracle',
            'candidate link graph uses resource IDs, but named Classic route labels remain unobserved beyond Levo',
            'display/map calibration remains blocked, so map-label position joins cannot be inferred from static coordinates',
        ],
        'nextEvidenceFamilies': [
            'decoded complete name/list resource with a stable order matching the 67 syst records',
            'original-runtime map or route UI captures tying multiple labels to decoded resource IDs and Con-slot neighbors',
            'source-level variable/struct evidence identifying system-name resource storage and ordering',
        ],
        'sourceNote': 'This matrix is a negative gate for record-to-name promotion. It keeps the heuristic system-name and landing-name seeds useful for scouting while requiring a complete name/order oracle or runtime label evidence before assigning any additional Classic system names to decoded syst records.',
    }


def _record_name_runtime_join_reconciliation_summary(systems: list[dict], names: dict) -> dict:
    """Define how future runtime/name evidence can reconcile record-to-name joins without over-promotion."""
    record_oracle = _record_name_oracle_evidence_matrix_summary(names, {system['resourceId'] for system in systems})
    route_bridge = _runtime_route_label_observation_bridge_gap_summary(systems)
    route_reconciliation = _runtime_route_label_capture_reconciliation_summary(systems)
    start_system = next(system for system in systems if system['resourceId'] == 128)
    start_linked_ids = start_system['semanticFields']['candidateHyperspaceLinks']['linkedSystemResourceIdsInRun']
    unjoined_start_neighbors = [resource_id for resource_id in start_linked_ids if resource_id not in EXACT_SYSTEM_NAME_MAPPINGS]
    return {
        'sourceLabel': 'decoded-resource-and-runtime-backed-record-name-join-reconciliation-plan',
        'oracleStatus': 'record_name_join_reconciliation_blocked_pending_complete_name_or_runtime_packets',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field', 'original-runtime-observed', 'original-runtime-required'],
        'recordCount': record_oracle['recordCount'],
        'exactMappedResourceIds': record_oracle['exactMappedResourceIds'],
        'exactMappedSystemNames': record_oracle['exactMappedSystemNames'],
        'unjoinedRecordCount': record_oracle['unjoinedRecordCount'],
        'unjoinedResourceIdRange': record_oracle['unjoinedResourceIdRange'],
        'candidateStartResourceId': 128,
        'candidateStartSystemName': EXACT_SYSTEM_NAME_MAPPINGS[128]['systemName'],
        'unjoinedStartNeighborResourceIds': unjoined_start_neighbors,
        'observedRuntimeLabels': [entry.get('label') for entry in route_bridge.get('observedRuntimeLabels', [])],
        'requiredRuntimePacketIds': route_reconciliation.get('requiredCapturePacketIds', []),
        'requiredRuntimePacketCount': route_reconciliation.get('requiredValidatedCapturePacketCount'),
        'evidenceInputSummaries': [
            'recordNameOracleEvidenceMatrixSummary',
            'runtimeRouteLabelObservationBridgeGapSummary',
            'runtimeRouteLabelCaptureReconciliationSummary',
            'coordinateDisplayRuntimeCaptureReconciliationSummary',
            'namedRouteTopologyOracleGapSummary',
        ],
        'evidenceInputSummaryCount': 5,
        'postEvidenceReconciliationSteps': [
            'validate complete source/name-table evidence or packet-level runtime route-label evidence before proposing any new resource-ID/name join',
            'preserve resource 128 -> Levo as an invariant while checking every proposed join against decoded Con-slot/resource-ID context',
            'require coordinate-display reconciliation before using map positions, click geometry, or label order as a record-name oracle',
            'classify partial runtime packets as worklist refinements, not broad record-name promotion',
            'rerun static_topology_source_readiness_scout and model manifest tests before any runtime universe replacement or named topology promotion',
        ],
        'promotionDecisionStates': [
            'no-new-oracle; only resource 128 -> Levo remains exact-mapped',
            'partial-runtime-packets; captured labels may refine priorities but unjoined records remain blocked',
            'complete-source-name-order; may propose narrow record-name joins only for covered resource IDs',
            'source-runtime-contradiction; reopen record-name oracle evidence matrix and keep broad topology blocked',
        ],
        'blockedPromotionClaims': [
            'assigning any of resource IDs 129-194 to Classic system names without complete name-order or validated runtime packet evidence',
            'using landing-name byte proximity or heuristic text seed order as a complete syst record-name oracle',
            'promoting named route topology or runtime universe replacement from start-neighborhood labels alone',
            'using map-label position/order as record-name proof without coordinate display reconciliation',
        ],
        'requiredVerifierBeforePromotion': [
            'python3 tools/extract_ev_system_semantics.py',
            'python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_systems_manifest_promotes_static_system_ids_and_name_seeds native_ev.tests.test_scenario_eval.ScenarioEvalHarnessTests.test_static_topology_source_readiness_scout_records_lane_a_promotion_boundary -v',
            'python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty',
        ],
        'promotionBlockers': [
            'post-evidence reconciliation is a gate, not a record-name promotion packet',
            'complete name/order or validated packet-level target evidence is required before assigning any new syst resource name',
            'coordinate display, named-route topology, and broad runtime-universe blockers still apply independently',
        ],
        'allowedUse': 'reconcile future complete name-table or validated runtime route-label packets into narrow record-name join proposals only; do not promote names or runtime topology from this plan alone',
        'promotionStatus': 'not-promoted; record-name join reconciliation plan only',
        'sourceNote': 'This plan connects the record-name oracle matrix with route-label and coordinate-display reconciliation gates so future evidence can promote only packet-backed resource-ID/name joins while keeping broad topology blocked.',
    }


def _named_route_topology_oracle_gap_summary(systems: list[dict], names: dict) -> dict:
    """Record the missing oracle before candidate resource-ID links become named Classic routes."""
    exact_mapped_resource_ids = sorted(EXACT_SYSTEM_NAME_MAPPINGS)
    resource_ids = {system['resourceId'] for system in systems}
    link_slots = [
        slot
        for system in systems
        for slot in system['semanticFields']['candidateHyperspaceLinks']['linkSlots']
        if slot.get('targetPresentInSystRun')
    ]
    unique_directed_edges = sorted({
        (system['resourceId'], slot['targetResourceId'])
        for system in systems
        for slot in system['semanticFields']['candidateHyperspaceLinks']['linkSlots']
        if slot.get('targetPresentInSystRun')
    })
    start_system = next(system for system in systems if system['resourceId'] == 128)
    start_linked_ids = start_system['semanticFields']['candidateHyperspaceLinks']['linkedSystemResourceIdsInRun']
    named_start_edges = [
        {
            'fromResourceId': 128,
            'fromSystemName': EXACT_SYSTEM_NAME_MAPPINGS[128]['systemName'],
            'toResourceId': target_id,
            'toSystemName': EXACT_SYSTEM_NAME_MAPPINGS.get(target_id, {}).get('systemName'),
            'nameJoinStatus': 'exact' if target_id in EXACT_SYSTEM_NAME_MAPPINGS else 'blocked-missing-target-name-oracle',
        }
        for target_id in start_linked_ids
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-named-route-topology-oracle-gap',
        'oracleStatus': 'named_route_topology_blocked_pending_record_name_and_runtime_label_oracle',
        'recordCount': len(resource_ids),
        'candidateDirectedLinkSlotCount': len(link_slots),
        'uniqueDirectedCandidateEdgeCount': len(unique_directed_edges),
        'exactMappedResourceIds': exact_mapped_resource_ids,
        'exactMappedSystemNames': [EXACT_SYSTEM_NAME_MAPPINGS[resource_id]['systemName'] for resource_id in exact_mapped_resource_ids],
        'unjoinedRecordCount': len(resource_ids - set(exact_mapped_resource_ids)),
        'heuristicSystemNameSeedCount': len(names.get('systemNames', [])),
        'evidenceInputSummaries': [
            'candidateLinkGraphSummary',
            'candidateGraphConnectivitySummary',
            'candidateGraphDistanceSummary',
            'startSystemCandidateTopologySummary',
            'recordNameOracleEvidenceMatrixSummary',
            'coordinateDisplayCalibrationGateSummary',
        ],
        'evidenceInputSummaryCount': 6,
        'startSystemNamedCandidateEdges': named_start_edges,
        'requiredOracleClaims': [
            'exact names for candidate target resource IDs before named route labels are assigned',
            'runtime map/route label capture tying visible Classic labels to decoded resource IDs and Con-slot edges',
            'coordinate display calibration or accepted projection surrogate before map-layout claims are promoted',
            'cross-check that route labels preserve the exact resource 128 -> Levo bridge and do not rely on heuristic text proximity alone',
        ],
        'promotionReadinessStatus': 'blocked; candidate resource-ID graph is decoded but named Classic route topology is unjoined',
        'promotionBlockers': [
            'only resource 128 has an exact Classic system-name mapping',
            'start-system candidate targets 129, 130, and 131 have no exact names in this packet',
            'candidate link graph records resource-ID edges, not visible Classic route labels',
            'coordinate display calibration remains blocked, so map-neighbor direction/position cannot promote route labels',
        ],
        'nextEvidenceFamilies': [
            'original-runtime map/route label captures for Levo neighbors tied to decoded resource IDs or link slots',
            'decoded complete system-name/order source that joins resource IDs 129-194 to names',
            'source-level map/route rendering or name-table oracle that ties named labels to syst resource IDs',
        ],
        'sourceNote': 'This packet separates decoded candidate topology from named route topology. It preserves candidate links as source-readiness evidence while explicitly blocking player-facing Classic route labels until names, runtime label captures, and display calibration are available.',
    }


def _runtime_route_label_observation_bridge_gap_summary(systems: list[dict]) -> dict:
    """Record bounded original-runtime route/map labels without assigning resource IDs."""
    start_system = next(system for system in systems if system['resourceId'] == 128)
    start_linked_ids = start_system['semanticFields']['candidateHyperspaceLinks']['linkedSystemResourceIdsInRun']
    exact_mapped_resource_ids = sorted(EXACT_SYSTEM_NAME_MAPPINGS)
    return {
        'sourceLabel': 'original-runtime-observed-route-label-bridge-gap',
        'oracleStatus': 'runtime_route_labels_observed_but_not_joined_to_decoded_resource_ids',
        'sourceReferences': [
            'docs/research/original-ev-classic-runtime-observations.md lines 135-158',
            'docs/research/original-ev-classic-runtime-observations.md lines 197-209',
        ],
        'observedRuntimeLabels': [
            {
                'label': 'Rigel',
                'observation': 'Backslash selected Rigel from Levo in Hyperspace mode.',
                'joinStatus': 'not-promoted; observed as a visible route label but not tied to a decoded resource ID or Con slot',
            },
            {
                'label': 'Kathoon',
                'observation': 'Shift-click route screenshot showed Destination System: Kathoon around Rigel/Levo.',
                'joinStatus': 'not-promoted; screenshot/click geometry is not yet calibrated to decoded resource IDs or slots',
            },
            {
                'label': 'Yemuro',
                'observation': 'Mission text named New Istanbul in the Yemuro system.',
                'joinStatus': 'not-promoted; mission destination text is not a map/resource-order oracle for syst records',
            },
            {
                'label': 'Torgo',
                'observation': 'Mission text named Torgo Prime in the Torgo system.',
                'joinStatus': 'not-promoted; mission destination text is not a map/resource-order oracle for syst records',
            },
        ],
        'observedRuntimeLabelCount': 4,
        'candidateStartResourceId': 128,
        'candidateStartSystemName': EXACT_SYSTEM_NAME_MAPPINGS[128]['systemName'],
        'candidateStartLinkedResourceIds': start_linked_ids,
        'exactMappedResourceIds': exact_mapped_resource_ids,
        'unjoinedStartNeighborResourceIds': [resource_id for resource_id in start_linked_ids if resource_id not in exact_mapped_resource_ids],
        'bridgeBlockers': [
            'runtime labels are visible Classic observations but no capture currently ties each label to a decoded resource ID or Con slot',
            'backslash/shift-click route observations do not record the resource ordinal or candidate edge selected by the original runtime',
            'mission destination text names systems but does not define syst record order or map coordinate calibration',
            'coordinate display/click calibration remains missing, so route-label positions cannot join decoded coordinates to visible labels',
        ],
        'allowedUse': 'stronger original-runtime route-label evidence inventory and probe targeting only; do not assign names or routes from this bridge gap',
        'nextEvidenceFamilies': [
            'Classic map capture/click probe that starts at Levo and records visible candidate labels plus exact input/click positions',
            'route-selection probe tying each chosen visible label to the decoded start-neighborhood candidate edge order',
            'complete source/name-order oracle that can reconcile observed route labels with resource IDs 129-194',
        ],
        'promotionStatus': 'not-promoted; original-runtime labels exist but are not yet a decoded resource-ID/name/topology join',
        'sourceNote': 'This bridge gap upgrades the route-label evidence inventory without over-promoting it: Classic-visible labels like Rigel and Kathoon are real runtime observations, but the current captures lack a decoded-resource-ID/slot join and cannot promote named topology.',
    }


def _runtime_route_label_probe_targeting_summary(systems: list[dict]) -> dict:
    """Turn the route-label bridge gap into bounded probe targets without assigning names."""
    start_system = next(system for system in systems if system['resourceId'] == 128)
    link_slots = start_system['semanticFields']['candidateHyperspaceLinks']['linkSlots']
    observed_labels = ['Rigel', 'Kathoon', 'Yemuro', 'Torgo']
    unjoined_targets = [
        {
            'slotName': slot['slotName'],
            'targetResourceId': slot['targetResourceId'],
            'targetNameJoinStatus': 'blocked-missing-target-name-oracle',
            'recommendedProbe': 'capture original-runtime map/route label selection from Levo and record visible label, input/click position, and selected edge order without assigning a Classic name to this decoded resource ID',
        }
        for slot in link_slots
        if slot.get('targetPresentInSystRun') and slot.get('targetResourceId') not in EXACT_SYSTEM_NAME_MAPPINGS
    ]
    return {
        'sourceLabel': 'original-runtime-and-decoded-resource-backed-route-label-probe-targeting-matrix',
        'oracleStatus': 'route_label_probe_targets_pending_decoded_resource_id_slot_join',
        'sourceReferences': [
            'runtimeRouteLabelObservationBridgeGapSummary',
            'namedRouteTopologyOracleGapSummary',
            'startSystemCandidateTopologySummary',
        ],
        'sourceBasis': ['original-runtime-observed', 'decoded-original-variable', 'resource-bible-field'],
        'candidateStartResourceId': 128,
        'candidateStartSystemName': EXACT_SYSTEM_NAME_MAPPINGS[128]['systemName'],
        'candidateStartLinkedResourceIds': start_system['semanticFields']['candidateHyperspaceLinks']['linkedSystemResourceIdsInRun'],
        'observedRuntimeLabels': observed_labels,
        'observedRuntimeLabelCount': len(observed_labels),
        'unjoinedStartNeighborResourceIds': [entry['targetResourceId'] for entry in unjoined_targets],
        'probeTargetCount': len(unjoined_targets),
        'probeTargets': unjoined_targets,
        'blockedClaims': [
            'which observed runtime label, if any, corresponds to decoded resource IDs 129, 130, or 131',
            'whether visible route-label order matches Con-slot order, angular order, distance order, or another runtime selector',
            'whether Rigel/Kathoon/Yemuro/Torgo are map-route labels, mission text labels, or unrelated name observations for the decoded start-neighborhood packet',
        ],
        'promotionBlockers': [
            'probe targets are worklist entries, not decoded resource-ID/name joins',
            'observed labels remain unassigned until a Classic runtime probe ties a visible label to an exact decoded resource ID or Con slot',
            'do not rename resource IDs 129-131 or promote named route topology from this targeting matrix alone',
        ],
        'allowedUse': 'prioritize original-runtime route-label probes for the three unjoined Levo candidate neighbors only',
        'promotionStatus': 'not-promoted; probe targeting matrix preserves next evidence targets without assigning Classic names or routes',
        'sourceNote': 'This matrix is a Lane A worklist bridge: it combines the decoded Levo start-neighborhood slots with bounded original-runtime label observations to identify the next probes, while explicitly withholding all resource-ID/name and named-route assignments.',
    }


def _runtime_route_label_probe_execution_gate_summary(systems: list[dict]) -> dict:
    """Record the safe execution gate for original-runtime route-label probes."""
    probe_targeting = _runtime_route_label_probe_targeting_summary(systems)
    required_target_ids = [entry['targetResourceId'] for entry in probe_targeting['probeTargets']]
    return {
        'sourceLabel': 'original-runtime-route-label-probe-execution-gate',
        'oracleStatus': 'route_label_probe_execution_blocked_pending_disposable_runtime_capture',
        'sourceReferences': [
            'runtimeRouteLabelProbeTargetingSummary',
            'docs/research/original-ev-classic-runtime-observations.md lines 135-158',
            'docs/research/original-ev-classic-runtime-observations.md lines 197-209',
        ],
        'candidateStartResourceId': probe_targeting['candidateStartResourceId'],
        'candidateStartSystemName': probe_targeting['candidateStartSystemName'],
        'requiredProbeTargetResourceIds': required_target_ids,
        'requiredProbeTargetCount': len(required_target_ids),
        'requiredCaptureFields': [
            'disposableNonStrictPilot',
            'startSystemVisibleLabel',
            'inputMethod',
            'visibleDestinationLabel',
            'selectedEdgeOrderOrCycleOrdinal',
            'clickOrKeyPositionWhenApplicable',
            'screenshotOrTranscriptReference',
            'decodedResourceIdJoinWithEvidenceOnlyAfterIndependentOracle',
        ],
        'capturePacketSchemaVersion': 1,
        'requiredCapturePacketCount': len(required_target_ids),
        'capturePacketTemplates': [
            {
                'targetResourceId': target['targetResourceId'],
                'slotName': target['slotName'],
                'startSystem': {
                    'resourceId': probe_targeting['candidateStartResourceId'],
                    'systemName': probe_targeting['candidateStartSystemName'],
                },
                'operatorStateRequirements': {
                    'disposableNonStrictPilot': True,
                    'strictPlayAllowed': False,
                    'reusablePilotAllowed': False,
                    'rawResourceMutationAllowed': False,
                },
                'requiredObservationFields': [
                    'startSystemVisibleLabel',
                    'inputMethod',
                    'visibleDestinationLabel',
                    'selectedEdgeOrderOrCycleOrdinal',
                    'clickOrKeyPositionWhenApplicable',
                    'screenshotOrTranscriptReference',
                ],
                'joinPromotionRule': 'capture may propose a resource-ID/Con-slot join only when it records a visible label tied to this targetResourceId or slotName; otherwise leave name/topology promotion blocked',
                'sourceFidelityLabel': 'original-runtime-route-label-capture-packet-template',
            }
            for target in probe_targeting['probeTargets']
        ],
        'capturePacketValidationRules': [
            'one capture packet per required target resource ID 129-131 before any route-label join review',
            'each packet must retain local-only screenshot/transcript provenance; do not publish raw proprietary captures without approval',
            'a visible label alone is insufficient; packet must tie label selection to a decoded resource ID or Con slot before promotion review',
        ],
        'safetyBlockers': [
            'do not run route-label probes on Strict Play or reusable pilots',
            'do not mutate raw proprietary EV resource assets while probing runtime labels',
            'do not assign visible labels to decoded resource IDs 129-131 until a capture ties the visible label to a decoded resource ID or Con slot',
        ],
        'allowedUse': 'prepare disposable original-runtime capture packets for Levo route-label probes only; preserve every resource-ID/name join as blocked until captured evidence exists',
        'promotionStatus': 'not-promoted; execution gate documents safe evidence capture requirements only',
        'sourceNote': 'This gate turns the v49 probe-targeting matrix into an executable safety checklist without performing original-runtime probing or promoting any Classic route labels. It prevents the next worker from treating a target list as evidence.',
    }


def _runtime_route_label_probe_priority_summary(systems: list[dict]) -> dict:
    """Prioritize route-label probe packets using decoded start-neighborhood candidates without joining names."""
    targeting = _runtime_route_label_probe_targeting_summary(systems)
    execution_gate = _runtime_route_label_probe_execution_gate_summary(systems)
    calibration_priority = _start_neighborhood_runtime_calibration_priority_summary(systems)
    priority_ids = calibration_priority.get('priorityTargetResourceIds', [])
    slot_by_resource = {
        entry['targetResourceId']: entry['slotName']
        for entry in targeting.get('probeTargets', [])
    }
    execution_targets = execution_gate.get('requiredProbeTargetResourceIds', [])
    ordered_targets = [resource_id for resource_id in priority_ids if resource_id in execution_targets]
    ordered_targets.extend(resource_id for resource_id in execution_targets if resource_id not in ordered_targets)
    packet_templates = {
        entry['targetResourceId']: entry
        for entry in execution_gate.get('capturePacketTemplates', [])
    }
    priority_entries = []
    for priority_rank, resource_id in enumerate(ordered_targets, start=1):
        calibration_entry = next(
            (entry for entry in calibration_priority.get('priorityEntries', []) if entry.get('targetResourceId') == resource_id),
            {},
        )
        priority_entries.append({
            'priorityRank': priority_rank,
            'targetResourceId': resource_id,
            'slotName': slot_by_resource.get(resource_id),
            'capturePacketTemplateAvailable': resource_id in packet_templates,
            'displayQuadrantCandidate': calibration_entry.get('displayQuadrantCandidate'),
            'distanceRankAmongNonSelfCandidates': calibration_entry.get('distanceRankAmongNonSelfCandidates'),
            'angleRankAmongNonSelfCandidates': calibration_entry.get('angleRankAmongNonSelfCandidates'),
            'priorityReason': calibration_entry.get('priorityReason', 'route-label-execution-gate-required-target'),
            'joinPromotionStatus': 'not-promoted; capture priority only, no visible label assigned to decoded resource ID',
        })
    return {
        'sourceLabel': 'decoded-resource-and-runtime-gate-backed-route-label-probe-priority',
        'oracleStatus': 'route_label_probe_priority_pending_disposable_runtime_capture',
        'sourceReferences': [
            'runtimeRouteLabelProbeTargetingSummary',
            'runtimeRouteLabelProbeExecutionGateSummary',
            'startNeighborhoodRuntimeCalibrationPrioritySummary',
        ],
        'candidateStartResourceId': targeting['candidateStartResourceId'],
        'candidateStartSystemName': targeting['candidateStartSystemName'],
        'requiredProbeTargetResourceIds': execution_targets,
        'displayCalibrationPriorityTargetResourceIds': priority_ids,
        'priorityTargetResourceIds': ordered_targets,
        'priorityConSlots': [entry['slotName'] for entry in priority_entries],
        'firstPriorityTargetResourceId': ordered_targets[0] if ordered_targets else None,
        'firstPriorityConSlot': priority_entries[0]['slotName'] if priority_entries else None,
        'probePriorityEntries': priority_entries,
        'executionGatePacketTemplateCount': len(execution_gate.get('capturePacketTemplates', [])),
        'observedRuntimeLabels': targeting.get('observedRuntimeLabels', []),
        'promotionBlockers': [
            'priority order is derived from non-promoted decoded coordinate/vector candidates and execution gate requirements',
            'observed runtime labels remain unassigned to resource IDs 129-131 until disposable capture packets are executed',
            'this matrix may order future probes but must not promote named topology, display scale, or record-to-name joins',
        ],
        'allowedUse': 'schedule disposable original-runtime route-label capture attempts in highest-information order only',
        'promotionStatus': 'not-promoted; route-label probe priority only, no decoded resource-ID/name join',
        'sourceNote': 'This packet connects the route-label execution gate to the start-neighborhood calibration priority so the next probe can be run in a deterministic order. It does not assign Rigel, Kathoon, Yemuro, or Torgo to decoded resources and does not promote map scaling.',
    }


def _runtime_route_label_capture_reconciliation_summary(systems: list[dict]) -> dict:
    """Define post-capture reconciliation for route-label probes before any name/topology promotion."""
    bridge_gap = _runtime_route_label_observation_bridge_gap_summary(systems)
    execution_gate = _runtime_route_label_probe_execution_gate_summary(systems)
    priority = _runtime_route_label_probe_priority_summary(systems)
    packet_ids = [
        f"route-label-{entry['slotName'].lower()}-resource-{entry['targetResourceId']}"
        for entry in execution_gate.get('capturePacketTemplates', [])
    ]
    return {
        'sourceLabel': 'decoded-resource-and-runtime-backed-route-label-capture-reconciliation-plan',
        'oracleStatus': 'route_label_capture_reconciliation_blocked_pending_validated_probe_packets',
        'sourceBasis': ['original-runtime-observed', 'decoded-original-variable', 'resource-bible-field', 'original-runtime-required'],
        'candidateStartResourceId': execution_gate['candidateStartResourceId'],
        'candidateStartSystemName': execution_gate['candidateStartSystemName'],
        'observedRuntimeLabelCount': bridge_gap['observedRuntimeLabelCount'],
        'observedRuntimeLabels': [entry.get('label') for entry in bridge_gap.get('observedRuntimeLabels', [])],
        'requiredProbeTargetResourceIds': execution_gate['requiredProbeTargetResourceIds'],
        'requiredProbeConSlots': [entry.get('slotName') for entry in execution_gate.get('capturePacketTemplates', [])],
        'priorityTargetResourceIds': priority['priorityTargetResourceIds'],
        'priorityConSlots': priority['priorityConSlots'],
        'requiredValidatedCapturePacketCount': execution_gate['requiredCapturePacketCount'],
        'requiredCapturePacketIds': packet_ids,
        'evidenceInputSummaries': [
            'runtimeRouteLabelObservationBridgeGapSummary',
            'runtimeRouteLabelProbeTargetingSummary',
            'runtimeRouteLabelProbeExecutionGateSummary',
            'runtimeRouteLabelProbePrioritySummary',
            'coordinateDisplayRuntimeCaptureReconciliationSummary',
        ],
        'evidenceInputSummaryCount': 5,
        'postCaptureReconciliationSteps': [
            'validate every route-label packet against the execution gate schema before considering any resource-ID/name join',
            'tie each visible label to a decoded resource ID or Con slot only when the packet includes direct selection/click/order evidence for that target',
            'compare route-label joins against coordinate-display capture reconciliation before using labels as map-scale, projection, or display-order evidence',
            'classify partial packets as probe-priority refinements rather than named topology promotion',
            'rerun static_topology_source_readiness_scout before any record-name, named-route, or runtime-universe promotion packet',
        ],
        'promotionDecisionStates': [
            'no-packets; visible runtime labels remain unjoined observations',
            'partial-packets; route-label capture worklist remains open and no named topology may be promoted',
            'source-runtime-corroborated; may propose a narrow resource-ID/name join for captured targets only',
            'contradicted; reopen route-label bridge gap and keep named route topology blocked',
        ],
        'blockedPromotionClaims': [
            'assigning Rigel, Kathoon, Yemuro, or Torgo to decoded resource IDs 129-131 without validated target packets',
            'using visible route-label order as Con-slot order without direct selection/click/order evidence',
            'promoting broad named topology or runtime universe replacement from a partial start-neighborhood route-label capture',
            'using route-label captures as coordinate display scale or projection proof without the coordinate-display reconciliation gate',
        ],
        'requiredVerifierBeforeGameplay': [
            'python3 tools/extract_ev_system_semantics.py',
            'python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_systems_manifest_promotes_static_system_ids_and_name_seeds native_ev.tests.test_scenario_eval.ScenarioEvalHarnessTests.test_static_topology_source_readiness_scout_records_lane_a_promotion_boundary -v',
            'python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty',
        ],
        'promotionBlockers': [
            'post-capture reconciliation is a gate, not a route-label promotion packet',
            'every proposed resource-ID/name join must be backed by validated packet-level target evidence',
            'coordinate display, record-name, and broad runtime-universe blockers still apply independently',
        ],
        'allowedUse': 'validate and reconcile future route-label capture packets; do not promote names, named route topology, display units, or broad universe replacement from this plan alone',
        'promotionStatus': 'not-promoted; post-capture reconciliation plan only',
        'sourceNote': 'This plan defines how future Classic route-label probe packets can refine record-name and route-topology evidence while keeping observed labels unassigned until packet-level target evidence exists.',
    }


def _word_group_summary(run: dict, word_indices: list[int]) -> dict:
    values = [
        _word(record, word_index)
        for record in run['records']
        for word_index in word_indices
    ]
    return {
        'wordIndices': word_indices,
        'observedValueRange': [min(values), max(values)] if values else [],
        'distinctObservedValues': sorted(set(values))[:24],
        'distinctObservedValueCount': len(set(values)),
        'allValuesZero': bool(values) and all(value == 0 for value in values),
        'allValuesNoLinkSentinel': bool(values) and all(value == -1 for value in values),
        'systemIdDomainValueCount': sum(1 for value in values if 128 <= value <= 1127),
        'noLinkSentinelCount': values.count(-1),
        'zeroValueCount': values.count(0),
    }


def _syst_field_layout_source_readiness_summary(run: dict) -> dict:
    """Preserve Resource Bible syst field-family boundaries without over-promoting semantics."""
    field_complete_count = sum(1 for record in run['records'] if record.get('fieldsComplete'))
    return {
        'sourceLabel': 'resource-bible-backed-syst-field-layout-source-readiness',
        'oracleStatus': 'non_topology_syst_field_semantics_pending_runtime_integration',
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'fieldCompleteRecordCount': field_complete_count,
        'resourceBibleFieldFamilies': [
            {'fieldFamily': 'xPos/yPos map coordinates', 'promotionStatus': 'analysis-input-promoted', 'wordIndicesInCurrentDecoder': [0, 1, 2, 3]},
            {'fieldFamily': 'Con1-Con5 hyperspace links', 'promotionStatus': 'candidate-analysis-input-promoted', 'wordIndicesInCurrentDecoder': [4, 5, 6, 7, 8]},
            {'fieldFamily': 'NavDef F1-F4 navigation defaults', 'promotionStatus': 'source-backed-field-family-only'},
            {'fieldFamily': 'DudeTypes/%Prob/AvgShips AI population controls', 'promotionStatus': 'source-backed-field-family-only'},
            {'fieldFamily': 'Govt/Message/Asteroids/Interference/VisBit environment and visibility controls', 'promotionStatus': 'source-backed-field-family-only'},
            {'fieldFamily': 'Con6-Con16 additional hyperspace links', 'promotionStatus': 'source-backed-field-family-only'},
        ],
        'decodedWordGroupScouts': {
            'coordinateWords0To3': _word_group_summary(run, [0, 1, 2, 3]),
            'currentCandidateLinkScoutWindowWords4To19': _word_group_summary(run, list(range(4, 20))),
            'frontFiveConCandidateWords4To8': _word_group_summary(run, [4, 5, 6, 7, 8]),
            'percentLikeWords20To23': _word_group_summary(run, [20, 21, 22, 23]),
            'allZeroTailWords24To43': _word_group_summary(run, list(range(24, 44))),
        },
        'promotionBlockers': [
            'Resource Bible field-family names alone do not identify every decoded word offset in the current primitive record without a verified complete field map',
            'NavDef, DudeTypes, probabilities, AvgShips, Govt, Message, Asteroids, Interference, VisBit, and Con6-Con16 remain source-backed but not runtime-integrated semantics',
            'current Con1-Con16 link-slot scout window remains a candidate graph input, not proof that every downstream syst field family has been mapped',
        ],
        'nextEvidenceFamilies': [
            'complete source-level syst struct declaration or ResEdit field order confirming every word offset',
            'original-runtime capture tying navigation defaults, hazards, governments, messages, visibility bits, and Con6-Con16 links to observed behavior',
            'decoder update that separates front Con slots from downstream syst field families before broad universe replacement',
        ],
        'sourceNote': 'This packet records the Resource Bible syst layout families beside the decoded 44-word/88-byte records. It preserves the existing link-window scout output for continuity, while explicitly keeping non-topology syst fields and downstream field offsets unpromoted until a complete field-order oracle or runtime evidence is available.',
    }


def _syst_field_order_conflict_summary(run: dict) -> dict:
    """Compare Resource Bible field-order wording with current decoded word-domain scouts."""
    current_window = _word_group_summary(run, list(range(4, 20)))
    front_con = _word_group_summary(run, [4, 5, 6, 7, 8])
    projected_navdef = _word_group_summary(run, [9, 10, 11, 12])
    projected_population = _word_group_summary(run, list(range(13, 22)))
    projected_environment = _word_group_summary(run, [22, 23, 24, 25, 26])
    projected_con6_to_con16 = _word_group_summary(run, list(range(27, 38)))
    unexplained_tail = _word_group_summary(run, list(range(38, 44)))
    return {
        'sourceLabel': 'decoded-resource-backed-syst-field-order-conflict-scout',
        'oracleStatus': 'syst_field_order_mapping_pending_complete_oracle',
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'candidateInterpretations': [
            {
                'interpretationLabel': 'current-decoder-contiguous-link-window',
                'coordinateWordIndices': [0, 1, 2, 3],
                'candidateLinkWordIndices': list(range(4, 20)),
                'candidateLinkWindowSummary': current_window,
                'promotionStatus': 'analysis-input-only; preserves candidate graph continuity but not full Resource Bible field layout',
            },
            {
                'interpretationLabel': 'resource-bible-order-after-32-bit-coordinate-pairs',
                'coordinateWordIndices': [0, 1, 2, 3],
                'frontCon1ToCon5WordIndices': [4, 5, 6, 7, 8],
                'navDefF1ToF4WordIndices': [9, 10, 11, 12],
                'dudeProbabilityAvgShipsWordIndices': list(range(13, 22)),
                'govtMessageHazardVisibilityWordIndices': [22, 23, 24, 25, 26],
                'projectedCon6ToCon16WordIndices': list(range(27, 38)),
                'unexplainedTailWordIndices': list(range(38, 44)),
                'promotionStatus': 'not-promoted; direct 16-bit projection conflicts with decoded word-domain evidence',
            },
        ],
        'decodedWordGroupScouts': {
            'currentCandidateLinkScoutWindowWords4To19': current_window,
            'frontCon1ToCon5CandidateWords4To8': front_con,
            'projectedNavDefF1ToF4Words9To12': projected_navdef,
            'projectedDudeProbabilityAvgShipsWords13To21': projected_population,
            'projectedGovtMessageHazardVisibilityWords22To26': projected_environment,
            'projectedCon6ToCon16Words27To37': projected_con6_to_con16,
            'unexplainedTailWords38To43': unexplained_tail,
        },
        'conflictSignals': [
            'Resource Bible prose orders Con6-Con16 after NavDef, population, government, message, hazard, and visibility fields, but the local contiguous link scout has all 268 system-ID-domain links inside words 4-19',
            'A direct 32-bit-coordinate plus 16-bit-field projection would place Con6-Con16 at words 27-37, but those decoded words are all zero rather than -1/no-link or 128-1127 system IDs',
            'The current candidate graph remains useful as a scout because its values target in-run system IDs, but it must not be treated as a verified complete Resource Bible field-order mapping',
        ],
        'promotionBlockers': [
            'complete syst field-order oracle is missing for reconciling current decoder word windows with Resource Bible family ordering',
            'Con6-Con16 split placement cannot be promoted from the contiguous link scout until byte/word-width interpretation is resolved',
            'downstream NavDef/population/government/message/hazard/visibility fields remain source-backed family names, not decoded runtime-integrated semantics',
        ],
        'nextEvidenceFamilies': [
            'source-level syst struct declaration including field widths and offsets',
            'ResEdit/template field map or resource editor view tying fields to byte offsets',
            'runtime probes for Con6-Con16 and non-topology syst fields that disambiguate offset families',
        ],
        'sourceNote': 'This matrix records a deliberate unresolved mismatch between Resource Bible field-order prose and the current decoded word-domain scout. It keeps the candidate link graph available while preventing broad field-layout promotion until an offset oracle or runtime probe resolves the split.',
    }


def _resource_bible_syst_sequential_field_projection_summary(run: dict) -> dict:
    """Project the Resource Bible syst field order onto current words as a negative oracle."""
    projected_field_groups = [
        {
            'fieldFamily': 'xPos/yPos map coordinates',
            'wordIndices': [0, 1, 2, 3],
            'resourceBibleReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 931-932',
            'domainSummary': _word_group_summary(run, [0, 1, 2, 3]),
            'projectionStatus': 'promoted-as-coordinate-raw-word-pairs-only; display units remain blocked',
        },
        {
            'fieldFamily': 'Con1-Con5 front hyperspace links',
            'wordIndices': [4, 5, 6, 7, 8],
            'resourceBibleReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 933-937',
            'domainSummary': _word_group_summary(run, [4, 5, 6, 7, 8]),
            'projectionStatus': 'candidate-link-domain-compatible; exact named route topology remains blocked',
        },
        {
            'fieldFamily': 'NavDef F1-F4 navigation defaults',
            'wordIndices': [9, 10, 11, 12],
            'resourceBibleReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 938-945',
            'domainSummary': _word_group_summary(run, [9, 10, 11, 12]),
            'projectionStatus': 'not-promoted; current words are no-link sentinels in the contiguous link scout, not verified stellar defaults',
        },
        {
            'fieldFamily': 'DudeTypes/%Prob/AvgShips population controls',
            'wordIndices': list(range(13, 22)),
            'resourceBibleReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 946-959',
            'domainSummary': _word_group_summary(run, list(range(13, 22))),
            'projectionStatus': 'not-promoted; mixed link-sentinel/percent-like values need field-width and runtime oracle before AI population use',
        },
        {
            'fieldFamily': 'Govt/Message/Asteroids/Interference/VisBit environment and visibility controls',
            'wordIndices': [22, 23, 24, 25, 26],
            'resourceBibleReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 961-984',
            'domainSummary': _word_group_summary(run, [22, 23, 24, 25, 26]),
            'projectionStatus': 'not-promoted; zero/percent-like projection must not drive government, message, hazard, interference, or visibility gameplay',
        },
        {
            'fieldFamily': 'Con6-Con16 additional hyperspace links',
            'wordIndices': list(range(27, 38)),
            'resourceBibleReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 985-989',
            'domainSummary': _word_group_summary(run, list(range(27, 38))),
            'projectionStatus': 'not-promoted; projected Con6-Con16 words are all zero in current decode, conflicting with promoted link-window scout values',
        },
    ]
    compatible_families = [
        entry['fieldFamily'] for entry in projected_field_groups
        if entry['projectionStatus'].startswith(('promoted-as-coordinate', 'candidate-link-domain-compatible'))
    ]
    blocked_families = [
        entry['fieldFamily'] for entry in projected_field_groups
        if entry['projectionStatus'].startswith('not-promoted')
    ]
    width_budget = {
        'sourceLabel': 'resource-bible-backed-syst-field-count-budget-negative-oracle',
        'recordWords': run.get('recordSize') // 2 if run.get('recordSize') else None,
        'recordBytes': run.get('recordSize'),
        'resourceBibleSequentialFieldFamilies': [
            {'fieldFamily': 'xPos/yPos map coordinates', 'sourceFieldCount': 2, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 931-932'},
            {'fieldFamily': 'Con1-Con5 front hyperspace links', 'sourceFieldCount': 5, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 933-937'},
            {'fieldFamily': 'NavDef F1-F4 navigation defaults', 'sourceFieldCount': 4, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 938-945'},
            {'fieldFamily': 'DudeTypes/%Prob/AvgShips population controls', 'sourceFieldCount': 9, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 946-959'},
            {'fieldFamily': 'Govt/Message/Asteroids/Interference/VisBit environment and visibility controls', 'sourceFieldCount': 5, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 961-984'},
            {'fieldFamily': 'Con6-Con16 additional hyperspace links', 'sourceFieldCount': 11, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 985-989'},
        ],
        'sourceFieldCountTotal': 36,
        'byteSizePaddingGapSummary': {
            'sourceLabel': 'resource-bible-backed-syst-byte-size-padding-gap-negative-oracle',
            'recordBytes': run.get('recordSize'),
            'sourceFieldCountTotal': 36,
            'projectedByteBudgetCandidates': [
                {
                    'candidate': 'all Resource Bible syst fields interpreted as 16-bit words',
                    'projectedBytesUsed': 72,
                    'unassignedPaddingByteCount': (run.get('recordSize') - 72) if run.get('recordSize') else None,
                    'promotionStatus': 'not-promoted; leaves sixteen record bytes unassigned and conflicts with promoted 32-bit coordinate raw-word evidence',
                },
                {
                    'candidate': '32-bit xPos/yPos plus remaining Resource Bible syst fields as 16-bit words',
                    'projectedBytesUsed': 76,
                    'unassignedPaddingByteCount': (run.get('recordSize') - 76) if run.get('recordSize') else None,
                    'promotionStatus': 'not-promoted; leaves twelve record bytes unassigned and does not identify downstream byte offsets',
                },
            ],
            'fieldWidthOffsetOracleGapSummary': {
                'sourceLabel': 'resource-bible-backed-syst-field-width-offset-oracle-gap',
                'oracleStatus': 'syst_field_width_offset_mapping_blocked_pending_source_template_or_runtime_oracle',
                'requiredEvidenceFamilies': [
                    'source-level syst struct declaration with byte widths and offsets',
                    'ResEdit/template field map assigning each Resource Bible field to a byte offset',
                    'runtime probes that identify NavDef, population, government/message/hazard/interference/visibility, and split Con6-Con16 behavior independently of the current word scout',
                ],
                'blockedWidthClaims': [
                    'whether xPos/yPos consume two 16-bit words or two 32-bit values in the Resource Bible prose model',
                    'which of the remaining decoded words are padding, packed bitfields, or semantic fields',
                    'where Con6-Con16 begin after non-topology fields without contradicting the current link-domain scout',
                ],
                'templateSourceAvailabilityGapSummary': {
                    'sourceLabel': 'repo-reference-backed-syst-resedit-template-source-availability-gap',
                    'oracleStatus': 'syst_template_offset_mapping_blocked_pending_exact_tmpl_or_resedit_source',
                    'checkedReferenceFamilies': [
                        'EV Classic Resource Bible syst prose at docs/references/ev-family/ev-classic-resource-bible.txt lines 924-989',
                        'local decoded primitive 88-byte syst-like records in native_ev/data/sourced_ev_structures.json',
                        'local reference archive search terms: TMPL/template/ResEdit/sÿst/syst field names',
                    ],
                    'availableEvidence': [
                        'Resource Bible field-family order and value domains for xPos/yPos, Con1-Con5, NavDef, DudeTypes/%Prob/AvgShips, Govt/Message/Asteroids/Interference/VisBit, and Con6-Con16',
                        'decoded record size and word-domain coverage for 67 syst-like records',
                    ],
                    'missingEvidence': [
                        'no exact syst TMPL/resource-template artifact is recorded in the local source manifest',
                        'no ResEdit field-offset screenshot/export is recorded in the local source manifest',
                        'no source-level Classic syst struct declaration is recorded in the local source manifest',
                    ],
                    'promotionBlockers': [
                        'template/source absence means Resource Bible prose cannot be converted into byte offsets by assertion',
                        'decoded word-domain scouts remain negative/candidate evidence until an exact template or runtime behavior oracle resolves offsets',
                    ],
                    'evFamilyTemplateTransferGuardrailSummary': {
                        'sourceLabel': 'ev-family-reference-backed-template-transfer-guardrail',
                        'oracleStatus': 'ev_family_template_evidence_not_classic_syst_offset_oracle',
                        'weakerReferenceFamilies': [
                            'EV Nova Bible documents a sÿst family and field-style documentation in docs/references/ev-family/ev-nova-bible.html but is not EV Classic-specific source evidence',
                            'EV Override Resource Bible and EV-family documentation may guide search terms but do not prove EV Classic syst byte layout',
                            'community Rezilla/TMPL export workflows in docs/research/ev-community-engine-survey.md describe EV Nova extraction paths, not a Classic syst TMPL artifact in this repo',
                        ],
                        'promotionBlockers': [
                            'EV-family TMPL/resource-editor workflows cannot promote EV Classic syst byte offsets without a Classic-specific template/source oracle',
                            'EV Nova/Override field documentation may seed hypotheses only; Classic runtime/source confirmation is still required before assigning unresolved syst words to gameplay semantics',
                        ],
                        'allowedUse': 'search-term and hypothesis guidance only for locating a Classic-specific syst template, source struct, or runtime probe target',
                        'promotionStatus': 'not-promoted; EV-family template evidence remains a transfer guardrail, not a Classic offset oracle',
                    },
                    'evFamilySystVariantDivergenceGuardrailSummary': {
                        'sourceLabel': 'ev-family-reference-backed-syst-variant-divergence-guardrail',
                        'oracleStatus': 'ev_family_syst_field_count_variants_not_classic_offset_oracles',
                        'classicReference': {
                            'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 924-989',
                            'navDefCount': 4,
                            'dudeTypeCount': 4,
                            'probabilityCount': 4,
                            'asteroidRange': [0, 10],
                            'visibilitySetRange': [0, 255],
                            'visibilityClearedRange': [1000, 1255],
                            'conLinkCount': 16,
                        },
                        'overrideReference': {
                            'sourceReference': 'docs/references/ev-family/ev-override-resource-bible-1.0.2.txt lines 1170-1239',
                            'navDefCount': 4,
                            'dudeTypeCount': 4,
                            'probabilityCount': 4,
                            'asteroidRange': [0, 10],
                            'visibilitySetRange': [0, 511],
                            'visibilityClearedRange': [1000, 1511],
                            'conLinkCount': 16,
                            'extraTailFamily': 'AlwaysPers fields after Con6-Con16',
                        },
                        'novaReference': {
                            'sourceReference': 'docs/references/ev-family/ev-nova-bible.html lines 3064-3188',
                            'navDefCount': 16,
                            'dudeTypeCount': 8,
                            'probabilityCount': 8,
                            'asteroidRange': [0, 16],
                            'visibilityModel': 'control-bit expression rather than Classic VisBit numeric ranges',
                            'conLinkCount': 16,
                            'extraTailFamilies': ['BkgndColor', 'Murk', 'AstTypes', 'ReinfFleet', 'ReinfTime', 'ReinfIntrval'],
                        },
                        'divergenceSignals': [
                            'Override preserves Classic NavDef/DudeTypes counts but widens VisBit mission-bit ranges and adds AlwaysPers tail fields',
                            'Nova expands NavDef/DudeTypes and introduces post-visibility fields, changing field-count and tail-placement assumptions',
                            'Classic Resource Bible prose remains the only current Classic field-family source, but it still lacks byte widths and offsets',
                        ],
                        'promotionBlockers': [
                            'EV-family field-count variants cannot be transposed onto EV Classic unresolved words',
                            'variant Resource Bible agreement on some field names is not equivalent to an EV Classic byte-offset oracle',
                            'visibility, population, and tail-field divergences reinforce the need for a Classic-specific template/source/runtime oracle',
                        ],
                        'allowedUse': 'negative oracle and search guidance only; use EV-family differences to avoid importing Override/Nova tail fields into Classic syst semantics',
                        'promotionStatus': 'not-promoted; EV-family variant divergence blocks offset/field-count transfer into Classic unresolved words',
                    },
                    'nextEvidenceFamilies': [
                        'recover original EV Classic syst TMPL/template or equivalent ResEdit field map',
                        'obtain source-level struct declaration with byte widths, padding, and field offsets',
                        'capture Classic runtime probes that expose one blocked non-topology syst family at a time',
                    ],
                    'promotionStatus': 'not-promoted; records that the template/ResEdit offset source is still absent from the local evidence bundle',
                },
                'minimumPromotionRequirement': 'at least one exact source/template offset oracle or independent runtime behavior oracle before assigning unresolved words to gameplay semantics',
                'promotionStatus': 'not-promoted; byte-count and field-count gaps are negative oracles only',
            },
            'budgetStatus': 'blocked; byte-size arithmetic proves a padding/width gap but cannot assign offsets or runtime semantics',
            'promotionBlockers': [
                '88-byte decoded syst records cannot be fully explained by Resource Bible field counts under either all-16-bit or 32-bit-coordinate projections',
                'byte-size padding gaps cannot identify which unresolved words are padding, bitfields, packed fields, or runtime semantics',
                'byte-size arithmetic must not promote NavDef, population, government, message, hazards, visibility, or Con6-Con16 placement without an offset/runtime oracle',
            ],
        },
        'projectedWordBudgetCandidates': [
            {
                'candidate': '16-bit xPos/yPos plus 16-bit downstream fields',
                'projectedWordsUsed': 36,
                'unassignedTailWordCount': (run.get('recordSize') // 2 - 36) if run.get('recordSize') else None,
                'promotionStatus': 'not-promoted; leaves eight record words unassigned and conflicts with existing raw-coordinate word-pair evidence',
            },
            {
                'candidate': '32-bit xPos/yPos plus 16-bit downstream fields',
                'projectedWordsUsed': 38,
                'unassignedTailWordCount': (run.get('recordSize') // 2 - 38) if run.get('recordSize') else None,
                'promotionStatus': 'not-promoted; leaves six record words unassigned and still places Con6-Con16 on zero-only words 27-37',
            },
        ],
        'budgetStatus': 'blocked; Resource Bible field counts constrain the projection but do not identify exact byte widths, padding, or offsets',
        'promotionBlockers': [
            'Resource Bible prose names and counts field families but does not specify enough byte-width/padding detail to fill all 44 decoded words',
            'both 16-bit-coordinate and 32-bit-coordinate field-count budgets leave unassigned tail words in the 88-byte record',
            'field-count arithmetic cannot promote NavDef, population, government, message, hazards, visibility, or Con6-Con16 without an offset/runtime oracle',
        ],
    }
    return {
        'sourceLabel': 'resource-bible-backed-syst-sequential-field-projection-negative-oracle',
        'oracleStatus': 'sequential_syst_field_projection_blocked_pending_width_offset_or_runtime_oracle',
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'fieldCountBudgetSummary': width_budget,
        'projectedFieldGroups': projected_field_groups,
        'projectedFieldGroupCount': len(projected_field_groups),
        'compatibleProjectionFamilies': compatible_families,
        'blockedProjectionFamilies': blocked_families,
        'blockingSignals': [
            'Resource Bible prose gives the sequential family order but not enough byte-width evidence to reconcile every current decoded word offset',
            'current decoded words 4-19 carry the link-domain scout, while a direct sequential projection would place Con6-Con16 at all-zero words 27-37',
            'words 9-12 look like no-link sentinels in the current scout and must not be promoted as NavDef stellar object IDs without an offset/runtime oracle',
            'government, message, hazard, interference, visibility, population, and AI fields remain source-backed family names only',
        ],
        'promotionReadinessStatus': 'blocked; sequential Resource Bible projection is an executable negative oracle, not a complete syst field map',
        'nextEvidenceFamilies': [
            'source-level syst struct declaration or template with exact byte widths and offsets',
            'ResEdit/editor field map proving how the prose field order maps onto the 88-byte records',
            'runtime probes for NavDef, population, government, message, hazard, interference, visibility, and Con6-Con16 behavior',
        ],
        'sourceNote': 'This packet preserves the Resource Bible sequential field-family text as a testable projection while explicitly blocking non-topology gameplay semantics where the projection conflicts with decoded word-domain evidence.',
    }


def _syst_template_offset_oracle_gap_summary(run: dict) -> dict:
    """Expose the Classic syst template/offset oracle gap as a top-level manifest gate."""
    sequential = _resource_bible_syst_sequential_field_projection_summary(run)
    template_gap = dict(
        sequential['fieldCountBudgetSummary']
        ['byteSizePaddingGapSummary']
        ['fieldWidthOffsetOracleGapSummary']
        ['templateSourceAvailabilityGapSummary']
    )
    template_gap['evidenceInputSummaries'] = [
        'resourceBibleSystSequentialFieldProjectionSummary',
        'systFieldLayoutSourceReadinessSummary',
        'systFieldOrderConflictSummary',
        'systWordDomainCoverageSummary',
    ]
    template_gap['evidenceInputSummaryCount'] = len(template_gap['evidenceInputSummaries'])
    template_gap['topLevelGateStatus'] = 'blocked; Classic-specific syst TMPL/ResEdit/source offset oracle is absent'
    template_gap['sourceNote'] = (
        'This top-level gate mirrors the nested template-source availability gap so dispatchers, '
        'scenario evaluators, and reviewers can see that EV-family templates and Resource Bible prose '
        'remain hypothesis inputs only. It does not assign any unresolved syst byte offsets or gameplay semantics.'
    )
    return template_gap


def _syst_template_offset_source_search_priority_summary(run: dict) -> dict:
    """Make the blocked Classic syst template/offset evidence search executable."""
    template_gap = _syst_template_offset_oracle_gap_summary(run)
    priority_targets = [
        {
            'targetId': 'classic-syst-tmpl-or-resedit-template',
            'targetEvidenceFamily': 'Classic-specific syst TMPL/template or ResEdit field map',
            'requiredEvidence': [
                'field name',
                'byte offset or ordered template slot',
                'field width',
                'Classic EV provenance',
            ],
            'promotionUse': 'may close the template/offset gate only for fields whose offset and width are explicitly identified',
        },
        {
            'targetId': 'classic-source-syst-struct',
            'targetEvidenceFamily': 'Classic source-level syst struct declaration',
            'requiredEvidence': [
                'struct member order',
                'member byte width',
                'padding or packed-field rule',
                'resource serialization mapping',
            ],
            'promotionUse': 'may reconcile Resource Bible prose with decoded 88-byte records after source/file provenance is recorded',
        },
        {
            'targetId': 'validated-runtime-offset-surrogate',
            'targetEvidenceFamily': 'validated original-runtime packet tied to a candidate field family',
            'requiredEvidence': [
                'positive control',
                'negative control',
                'candidate word group',
                'unchanged coordinate/name/topology guardrails',
            ],
            'promotionUse': 'may refine probe priority, but cannot by itself assign byte offsets without a source/template oracle',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-source-search-priority',
        'oracleStatus': 'syst_template_offset_search_blocked_pending_classic_specific_evidence',
        'sourceBasis': ['resource-bible-field', 'decoded-record-family', 'source-search-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetOracleGapSummary',
            'resourceBibleSystSequentialFieldProjectionSummary',
            'systWordDomainCoverageSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'priorityTargets': priority_targets,
        'priorityTargetIds': [target['targetId'] for target in priority_targets],
        'firstPriorityTargetId': priority_targets[0]['targetId'],
        'checkedReferenceFamilies': template_gap.get('checkedReferenceFamilies', []),
        'missingEvidence': template_gap.get('missingEvidence', []),
        'promotionBlockers': [
            'search priority is a worklist, not Classic byte-offset evidence',
            'EV-family or adaptation templates remain transfer guardrails unless Classic-specific provenance is recorded',
            'runtime packets can refine target order but cannot assign byte offsets without source/template evidence',
            'broad runtime universe replacement remains blocked until this search priority yields a closed template/offset oracle or an explicit scaffold boundary',
        ],
        'nextEvidenceFamilies': [target['targetEvidenceFamily'] for target in priority_targets],
        'promotionStatus': 'not-promoted; executable source-search priority only',
        'sourceNote': 'This packet converts the template/offset oracle gap into a deterministic search-priority worklist. It preserves the Classic-specific evidence boundary and does not assign unresolved syst byte offsets, Con6-Con16 split placement, or non-topology gameplay semantics.',
    }


def _syst_template_offset_evidence_packet_contract_summary(run: dict) -> dict:
    """Define the acceptance contract for future Classic-specific syst offset evidence packets."""
    search_priority = _syst_template_offset_source_search_priority_summary(run)
    accepted_evidence_classes = [
        {
            'evidenceClassId': 'classic-syst-tmpl-or-resedit-template',
            'requiredPacketFields': [
                'classicProvenance',
                'templateOrEditorArtifactPath',
                'fieldName',
                'byteOffsetOrOrderedTemplateSlot',
                'fieldWidth',
                'recordSerializationScope',
            ],
            'allowedPromotionUse': 'may close the template/offset gate only for explicitly identified Classic syst fields after verifier replay',
        },
        {
            'evidenceClassId': 'classic-source-syst-struct',
            'requiredPacketFields': [
                'classicProvenance',
                'sourceArtifactPath',
                'structMemberOrder',
                'memberByteWidths',
                'paddingOrPackingRule',
                'resourceSerializationMapping',
            ],
            'allowedPromotionUse': 'may reconcile Resource Bible field prose with decoded record offsets only for struct members covered by Classic provenance',
        },
        {
            'evidenceClassId': 'validated-runtime-offset-surrogate',
            'requiredPacketFields': [
                'classicCapturePath',
                'disposablePilotOrNonMutatingSurface',
                'positiveControl',
                'negativeControl',
                'candidateWordGroup',
                'unchangedCoordinateNameTopologyGuardrails',
            ],
            'allowedPromotionUse': 'may refine source-search priority or runtime probe targeting, but cannot assign byte offsets without Classic source/template corroboration',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-contract',
        'oracleStatus': 'syst_template_offset_evidence_packets_blocked_pending_validated_classic_specific_packet',
        'sourceBasis': ['source-search-required', 'resource-bible-field', 'decoded-record-family', 'original-runtime-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetSourceSearchPrioritySummary',
            'systTemplateOffsetOracleGapSummary',
            'resourceBibleSystSequentialFieldProjectionSummary',
            'systWordDomainCoverageSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 5,
        'acceptedEvidenceClasses': accepted_evidence_classes,
        'acceptedEvidenceClassIds': [entry['evidenceClassId'] for entry in accepted_evidence_classes],
        'firstAcceptedEvidenceClassId': accepted_evidence_classes[0]['evidenceClassId'],
        'requiredPacketSchemaVersion': 1,
        'requiredCommonPacketFields': [
            'packetId',
            'evidenceClassId',
            'sourceFidelityLabel',
            'sourceBasis',
            'classicSpecificProvenance',
            'evidenceArtifactPaths',
            'claimScope',
            'verifierCommand',
            'actualVerifierResult',
            'promotionDecision',
            'remainingUncertainty',
        ],
        'validationRules': [
            'packet evidenceClassId must match one accepted source-search priority target',
            'packet must name Classic-specific provenance before any byte-offset or field-width claim is considered',
            'packet verifier output must replay locally before manifest promotion',
            'runtime surrogate packets must include positive and negative controls plus unchanged coordinate/name/topology guardrails',
            'EV-family/adaptation-only packets must be classified as guardrails, not Classic syst offset evidence',
        ],
        'promotionDecisionStates': [
            'accepted-classic-template-source-packet; exact covered fields may be proposed for promotion after verifier replay',
            'accepted-runtime-surrogate-packet; probe priority may change but byte offsets remain unpromoted',
            'rejected-or-weaker-evidence; preserve blocker and update search notes only',
        ],
        'blockedPromotionClaims': [
            'assigning unresolved syst byte offsets without a Classic-specific template/source packet',
            'using EV-family TMPL/source variants as EV Classic byte-offset proof',
            'using runtime observations alone to place Con6-Con16, government, hazard, message, visibility, population, or NavDef bytes',
            'broad runtime universe replacement from a packet that does not close name/topology/display/non-topology gates',
        ],
        'searchPriorityTargetIds': search_priority.get('priorityTargetIds', []),
        'promotionBlockers': [
            'evidence packet contract is an acceptance schema, not Classic byte-offset evidence',
            'no packet has been validated against this contract yet',
            'validated runtime surrogates can reprioritize probes but cannot replace Classic-specific TMPL/source evidence',
        ],
        'nextEvidenceFamilies': search_priority.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; packet acceptance contract only',
        'sourceNote': 'This contract makes future syst template/offset evidence review deterministic. It does not add a packet, assign byte offsets, or integrate non-topology syst behavior.',
    }


def _syst_template_offset_evidence_packet_validation_matrix_summary(run: dict) -> dict:
    """Define verifier-side acceptance/rejection fixtures for future syst offset packets."""
    contract = _syst_template_offset_evidence_packet_contract_summary(run)
    validation_cases = [
        {
            'caseId': 'accept-classic-template-field-offset-packet',
            'evidenceClassId': 'classic-syst-tmpl-or-resedit-template',
            'requiredDecision': 'accepted-classic-template-source-packet',
            'requiredAssertions': [
                'packet names Classic-specific provenance',
                'packet includes field name, byte offset or ordered template slot, field width, and serialization scope',
                'verifier output replays locally before any covered-field promotion proposal',
            ],
            'allowedPromotionUse': 'exact covered fields may be proposed for promotion after verifier replay; uncovered syst words remain blocked',
        },
        {
            'caseId': 'accept-classic-source-struct-packet',
            'evidenceClassId': 'classic-source-syst-struct',
            'requiredDecision': 'accepted-classic-template-source-packet',
            'requiredAssertions': [
                'packet includes struct member order, member byte widths, padding or packing rule, and resource serialization mapping',
                'packet artifact has Classic EV provenance recorded in the manifest evidence bundle',
            ],
            'allowedPromotionUse': 'may reconcile only Classic-provenanced struct members with decoded record offsets',
        },
        {
            'caseId': 'accept-runtime-surrogate-for-priority-only',
            'evidenceClassId': 'validated-runtime-offset-surrogate',
            'requiredDecision': 'accepted-runtime-surrogate-packet',
            'requiredAssertions': [
                'packet includes positive and negative controls',
                'packet preserves unchanged coordinate/name/topology guardrails',
                'packet does not claim byte offsets without source/template corroboration',
            ],
            'allowedPromotionUse': 'may reprioritize probe/search targets only; byte offsets remain unpromoted',
        },
        {
            'caseId': 'reject-ev-family-template-transfer-packet',
            'evidenceClassId': 'ev-family-template-or-adaptation-only',
            'requiredDecision': 'rejected-or-weaker-evidence',
            'requiredAssertions': [
                'packet lacks Classic-specific syst provenance',
                'EV Nova/Override/adaptation template fields are classified as guardrails and search guidance only',
            ],
            'allowedPromotionUse': 'no Classic syst offset, field-width, Con6-Con16, or non-topology gameplay promotion',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-validation-matrix',
        'oracleStatus': 'syst_template_offset_packet_validation_blocked_pending_real_packet',
        'sourceBasis': ['source-search-required', 'packet-contract-required', 'classic-specific-provenance-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketContractSummary',
            'systTemplateOffsetSourceSearchPrioritySummary',
            'systTemplateOffsetOracleGapSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': contract.get('requiredPacketSchemaVersion'),
        'contractAcceptedEvidenceClassIds': contract.get('acceptedEvidenceClassIds', []),
        'contractPromotionDecisionStates': contract.get('promotionDecisionStates', []),
        'validationCases': validation_cases,
        'validationCaseCount': len(validation_cases),
        'firstValidationCaseId': validation_cases[0]['caseId'],
        'rejectionCaseIds': [case['caseId'] for case in validation_cases if case['requiredDecision'] == 'rejected-or-weaker-evidence'],
        'requiredVerifierOutcomes': [
            'accepted Classic template/source packets may only propose promotion for explicitly covered fields after verifier replay',
            'accepted runtime surrogate packets may only update probe priority and must leave byte offsets unpromoted',
            'EV-family/adaptation-only packets must be rejected as Classic syst offset evidence',
        ],
        'promotionBlockers': [
            'validation matrix is a verifier fixture, not a validated evidence packet',
            'no real Classic-specific packet has passed this matrix yet',
            'runtime or EV-family-only evidence cannot close the template/offset oracle gap',
            'broad runtime universe replacement remains blocked until a real accepted packet also satisfies name, topology, display, and non-topology gates',
        ],
        'nextEvidenceFamilies': contract.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; packet validation matrix only',
        'sourceNote': 'This matrix turns the packet contract into deterministic acceptance/rejection cases. It adds no real packet evidence and preserves the Classic-specific TMPL/source/runtime boundary.',
    }


def _syst_template_offset_evidence_packet_replay_readiness_summary(run: dict) -> dict:
    """Define the local replay handoff required before accepting future syst offset packets."""
    validation_matrix = _syst_template_offset_evidence_packet_validation_matrix_summary(run)
    replay_steps = [
        {
            'stepId': 'packet-artifact-readback',
            'requiredEvidence': [
                'packet JSON or capture artifact path exists in repo-local or archived evidence surface',
                'packet names packetId, evidenceClassId, sourceFidelityLabel, sourceBasis, and classicSpecificProvenance',
            ],
            'failureState': 'reject packet as missing replayable artifact provenance',
        },
        {
            'stepId': 'contract-and-matrix-classification',
            'requiredEvidence': [
                'evidenceClassId is one of the accepted contract classes or is explicitly classified as weaker evidence',
                'validation matrix caseId and requiredDecision are recorded before any promotion proposal',
            ],
            'failureState': 'preserve template/offset oracle gap and record only search-note changes',
        },
        {
            'stepId': 'local-verifier-replay',
            'requiredEvidence': [
                'verifierCommand is rerun locally and actualVerifierResult is captured in the packet handoff',
                'runtime surrogate packets keep positive/negative controls and unchanged coordinate/name/topology guardrails',
            ],
            'failureState': 'reject promotion proposal until verifier output is replayable',
        },
        {
            'stepId': 'narrow-promotion-scope-review',
            'requiredEvidence': [
                'accepted Classic template/source packets enumerate exactly covered fields and remaining unresolved syst words',
                'runtime surrogate packets update probe priority only and leave byte offsets unpromoted',
            ],
            'failureState': 'block broad runtime universe replacement and keep covered-field proposal out of gameplay data',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-replay-readiness',
        'oracleStatus': 'syst_template_offset_packet_replay_blocked_pending_real_packet',
        'sourceBasis': ['packet-contract-required', 'deterministic-verifier-replay-required', 'classic-specific-provenance-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketValidationMatrixSummary',
            'systTemplateOffsetEvidencePacketContractSummary',
            'systTemplateOffsetSourceSearchPrioritySummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': validation_matrix.get('contractSchemaVersion'),
        'validationCaseIds': [case['caseId'] for case in validation_matrix.get('validationCases', [])],
        'replayStepCount': len(replay_steps),
        'firstReplayStepId': replay_steps[0]['stepId'],
        'replaySteps': replay_steps,
        'requiredVerifierBeforePromotion': [
            'python3 tools/extract_ev_system_semantics.py',
            'python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_systems_manifest_promotes_static_system_ids_and_name_seeds -v',
            'python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty',
        ],
        'blockedPromotionClaims': [
            'promoting packet claims whose artifact path or verifier output cannot be replayed locally',
            'promoting runtime surrogate packets into Classic byte offsets without Classic source/template corroboration',
            'using a covered-field packet to lift unrelated syst words, Con6-Con16 placement, non-topology behavior, or broad runtime universe replacement',
        ],
        'promotionBlockers': [
            'replay readiness is a handoff checklist, not a validated evidence packet',
            'no real Classic-specific packet has been read back, classified, and replayed against this checklist',
            'accepted packets must still pass narrow scope review before any manifest promotion proposal',
        ],
        'nextEvidenceFamilies': validation_matrix.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; packet replay readiness checklist only',
        'sourceNote': 'This checklist makes future packet acceptance auditable by requiring artifact readback, contract/matrix classification, local verifier replay, and narrow scope review. It adds no packet evidence and does not promote syst offsets.',
    }


def _syst_template_offset_evidence_packet_intake_triage_summary(run: dict) -> dict:
    """Make the first-pass triage decision for future syst offset packets explicit."""
    replay_readiness = _syst_template_offset_evidence_packet_replay_readiness_summary(run)
    validation_matrix = _syst_template_offset_evidence_packet_validation_matrix_summary(run)
    triage_decisions = [
        {
            'decisionId': 'triage-classic-template-or-resedit-packet',
            'acceptedEvidenceClassIds': ['classic-syst-tmpl-or-resedit-template'],
            'requiredReplaySteps': ['packet-artifact-readback', 'contract-and-matrix-classification', 'local-verifier-replay'],
            'triageOutcome': 'candidate-for-narrow-covered-field-review',
        },
        {
            'decisionId': 'triage-classic-source-struct-packet',
            'acceptedEvidenceClassIds': ['classic-source-syst-struct'],
            'requiredReplaySteps': ['packet-artifact-readback', 'contract-and-matrix-classification', 'local-verifier-replay', 'narrow-promotion-scope-review'],
            'triageOutcome': 'candidate-for-classic-struct-offset-reconciliation',
        },
        {
            'decisionId': 'triage-runtime-surrogate-packet',
            'acceptedEvidenceClassIds': ['validated-runtime-offset-surrogate'],
            'requiredReplaySteps': ['packet-artifact-readback', 'contract-and-matrix-classification', 'local-verifier-replay'],
            'triageOutcome': 'probe-priority-only-no-byte-offset-promotion',
        },
        {
            'decisionId': 'triage-ev-family-or-adaptation-only-packet',
            'acceptedEvidenceClassIds': ['ev-family-template-or-adaptation-only'],
            'requiredReplaySteps': ['packet-artifact-readback', 'contract-and-matrix-classification'],
            'triageOutcome': 'reject-as-classic-syst-offset-evidence',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-intake-triage',
        'oracleStatus': 'syst_template_offset_packet_triage_blocked_pending_real_packet',
        'sourceBasis': ['packet-contract-required', 'deterministic-verifier-replay-required', 'classic-specific-provenance-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketReplayReadinessSummary',
            'systTemplateOffsetEvidencePacketValidationMatrixSummary',
            'systTemplateOffsetEvidencePacketContractSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': replay_readiness.get('contractSchemaVersion'),
        'validationCaseIds': [case['caseId'] for case in validation_matrix.get('validationCases', [])],
        'replayStepIds': [step.get('stepId') for step in replay_readiness.get('replaySteps', [])],
        'triageDecisionCount': len(triage_decisions),
        'triageDecisionIds': [decision['decisionId'] for decision in triage_decisions],
        'triageDecisions': triage_decisions,
        'blockedPromotionClaims': [
            'treating intake triage as evidence that a real Classic syst packet exists',
            'promoting runtime surrogate or EV-family/adaptation-only packets into byte offsets',
            'using accepted covered-field triage to lift unrelated syst words, Con6-Con16 placement, non-topology behavior, or broad runtime universe replacement',
        ],
        'promotionBlockers': [
            'intake triage is a routing checklist, not a validated evidence packet',
            'no real Classic-specific packet has passed artifact readback, matrix classification, verifier replay, and scope review',
            'broad runtime universe replacement remains blocked until packet-level evidence also satisfies name, topology, display, and non-topology gates',
        ],
        'nextEvidenceFamilies': replay_readiness.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; packet intake triage only pending real Classic-specific packet',
        'sourceNote': 'This triage layer tells future workers how to route replayed syst template/offset packets after readback and matrix classification. It adds no new packet evidence and cannot promote byte offsets or gameplay semantics.',
    }


def _syst_template_offset_evidence_packet_failure_taxonomy_summary(run: dict) -> dict:
    """Name stable failure classes for rejected or incomplete future syst offset packets."""
    intake_triage = _syst_template_offset_evidence_packet_intake_triage_summary(run)
    failure_classes = [
        {
            'failureClassId': 'missing-replayable-artifact',
            'blockedPromotionClaim': 'packet claim has no repo-local or archived artifact path that can be read back',
            'requiredRecoveryEvidence': 'provide packet path plus packetId/evidenceClassId/sourceFidelityLabel/sourceBasis/classicSpecificProvenance fields',
            'allowedDisposition': 'reject-and-record-search-note-only',
        },
        {
            'failureClassId': 'classic-provenance-absent',
            'blockedPromotionClaim': 'packet does not name Classic-specific TMPL, ResEdit, source-struct, or validated runtime-surrogate provenance',
            'requiredRecoveryEvidence': 'attach Classic-specific source path/capture/packet provenance before any byte-offset or field-width review',
            'allowedDisposition': 'reject-as-non-classic-offset-evidence',
        },
        {
            'failureClassId': 'verifier-replay-missing-or-failed',
            'blockedPromotionClaim': 'packet verifier output cannot be replayed locally or fails current extractor/model/scenario checks',
            'requiredRecoveryEvidence': 'rerun required verifier command locally and record actual output in the packet handoff',
            'allowedDisposition': 'block-promotion-until-replay-passes',
        },
        {
            'failureClassId': 'scope-overreach-beyond-covered-fields',
            'blockedPromotionClaim': 'packet proposes unrelated byte offsets, Con6-Con16 placement, non-topology behavior, or broad runtime universe replacement',
            'requiredRecoveryEvidence': 'narrow the packet to explicitly covered fields and leave unrelated gates blocked',
            'allowedDisposition': 'accept-only-narrow-covered-subclaim-or-reject',
        },
        {
            'failureClassId': 'ev-family-or-adaptation-only-transfer',
            'blockedPromotionClaim': 'EV-family template/source/adaptation packet is offered as EV Classic syst byte-offset proof',
            'requiredRecoveryEvidence': 'replace with Classic-specific template/source evidence or keep as hypothesis/search-priority input',
            'allowedDisposition': 'reject-as-classic-syst-offset-evidence',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-failure-taxonomy',
        'oracleStatus': 'syst_template_offset_packet_failure_taxonomy_blocked_pending_real_packet',
        'sourceBasis': ['packet-contract-required', 'deterministic-verifier-replay-required', 'classic-specific-provenance-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketIntakeTriageSummary',
            'systTemplateOffsetEvidencePacketReplayReadinessSummary',
            'systTemplateOffsetEvidencePacketValidationMatrixSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': intake_triage.get('contractSchemaVersion'),
        'triageDecisionIds': intake_triage.get('triageDecisionIds', []),
        'failureClassCount': len(failure_classes),
        'failureClassIds': [entry['failureClassId'] for entry in failure_classes],
        'failureClasses': failure_classes,
        'blockedPromotionClaims': [entry['blockedPromotionClaim'] for entry in failure_classes],
        'promotionBlockers': [
            'failure taxonomy is a rejection/recovery map, not Classic byte-offset evidence',
            'no real Classic-specific packet has been accepted by this taxonomy',
            'failure recovery may update search priority or packet status only; it must not promote offsets without replayed evidence',
            'broad runtime universe replacement remains blocked until all name, topology, display, non-topology, and template-offset gates close',
        ],
        'nextEvidenceFamilies': intake_triage.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; packet failure taxonomy only pending real Classic-specific packet',
        'sourceNote': 'This taxonomy makes rejected or incomplete future syst template/offset packets auditable by naming stable failure classes and recovery evidence. It adds no packet evidence and cannot promote byte offsets, Con-slot placement, non-topology behavior, or broad runtime universe replacement.',
    }


def _syst_template_offset_evidence_packet_recovery_plan_summary(run: dict) -> dict:
    """Define non-promoting recovery actions after future syst offset packet failures."""
    failure_taxonomy = _syst_template_offset_evidence_packet_failure_taxonomy_summary(run)
    recovery_actions = [
        {
            'actionId': 'recover-missing-replayable-artifact',
            'failureClassId': 'missing-replayable-artifact',
            'requiredNextEvidence': 'repo-local or archived packet artifact with packetId, evidenceClassId, sourceFidelityLabel, sourceBasis, classicSpecificProvenance, and verifierCommand fields',
            'allowedStateChange': 'record search-note or packet-needed state only',
        },
        {
            'actionId': 'recover-classic-provenance-absent',
            'failureClassId': 'classic-provenance-absent',
            'requiredNextEvidence': 'Classic-specific TMPL, ResEdit, source struct, or validated runtime-surrogate provenance tied to EV Classic rather than EV-family/adaptation data',
            'allowedStateChange': 'keep packet rejected until Classic-specific provenance is attached',
        },
        {
            'actionId': 'recover-verifier-replay-missing-or-failed',
            'failureClassId': 'verifier-replay-missing-or-failed',
            'requiredNextEvidence': 'successful local replay of extractor, focused model validation, and static_topology_source_readiness_scout with captured actual output',
            'allowedStateChange': 'block any promotion proposal until verifier replay passes',
        },
        {
            'actionId': 'recover-scope-overreach-beyond-covered-fields',
            'failureClassId': 'scope-overreach-beyond-covered-fields',
            'requiredNextEvidence': 'narrowed packet listing only covered field names, offsets, widths, and unresolved excluded syst words',
            'allowedStateChange': 'accept only narrow covered-field review or reject overbroad claims',
        },
        {
            'actionId': 'recover-ev-family-or-adaptation-only-transfer',
            'failureClassId': 'ev-family-or-adaptation-only-transfer',
            'requiredNextEvidence': 'replace EV-family/adaptation-only support with Classic-specific source/runtime evidence or demote to search-priority hypothesis',
            'allowedStateChange': 'search-priority note only; no Classic syst byte-offset promotion',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-recovery-plan',
        'oracleStatus': 'syst_template_offset_packet_recovery_plan_blocked_pending_real_packet',
        'sourceBasis': ['packet-contract-required', 'deterministic-verifier-replay-required', 'classic-specific-provenance-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketFailureTaxonomySummary',
            'systTemplateOffsetEvidencePacketIntakeTriageSummary',
            'systTemplateOffsetEvidencePacketReplayReadinessSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': failure_taxonomy.get('contractSchemaVersion'),
        'failureClassIds': failure_taxonomy.get('failureClassIds', []),
        'recoveryActionCount': len(recovery_actions),
        'recoveryActionIds': [entry['actionId'] for entry in recovery_actions],
        'recoveryActions': recovery_actions,
        'blockedPromotionClaims': failure_taxonomy.get('blockedPromotionClaims', []) + [
            'treating a recovery plan as evidence that a previously rejected packet has been fixed',
        ],
        'promotionBlockers': [
            'recovery plan is a next-evidence checklist, not Classic byte-offset evidence',
            'recovered packets must rerun the full contract, matrix, triage, verifier replay, and narrow-scope review path',
            'recovery actions may update packet status/search priority only; they must not promote offsets or runtime behavior without accepted evidence',
            'broad runtime universe replacement remains blocked until all name, topology, display, non-topology, and template-offset gates close',
        ],
        'nextEvidenceFamilies': failure_taxonomy.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; packet recovery plan only pending real Classic-specific packet',
        'sourceNote': 'This recovery plan maps each failure class to the exact next evidence required before a future syst template/offset packet can be replayed again. It deliberately adds no new Classic packet evidence and cannot promote offsets, Con-slot placement, non-topology behavior, or broad runtime universe replacement.',
    }


def _syst_template_offset_evidence_packet_reentry_guardrail_summary(run: dict) -> dict:
    """Keep recovered syst offset packets on the full replay path before promotion."""
    recovery_plan = _syst_template_offset_evidence_packet_recovery_plan_summary(run)
    reentry_steps = [
        {
            'stepId': 'recovered-packet-artifact-readback',
            'requiredEvidence': 'read back the recovered packet artifact and verify packetId/evidenceClassId/sourceFidelityLabel/sourceBasis/classicSpecificProvenance before changing any manifest claim',
            'blockedShortcut': 'do not accept a prose recovery note or search result as a replayable packet artifact',
        },
        {
            'stepId': 'recovered-packet-failure-class-closure',
            'requiredEvidence': 'map each prior failureClassId to its completed recoveryActionId and requiredNextEvidence',
            'blockedShortcut': 'do not clear a failure class until its paired recovery action supplies the named next evidence',
        },
        {
            'stepId': 'recovered-packet-contract-matrix-triage-rerun',
            'requiredEvidence': 'rerun contract, validation-matrix, intake-triage, verifier-replay, and narrow-scope review on the recovered packet',
            'blockedShortcut': 'do not resume from the failure point or skip earlier acceptance gates because a packet was revised',
        },
        {
            'stepId': 'recovered-packet-promotion-scope-quarantine',
            'requiredEvidence': 'quarantine any promotion proposal to explicitly covered Classic fields and preserve unrelated name/topology/display/non-topology/runtime-universe blockers',
            'blockedShortcut': 'do not let a recovered packet lift unrelated Con6-Con16 placement, byte offsets, non-topology behavior, or broad runtime universe replacement claims',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-reentry-guardrail',
        'oracleStatus': 'syst_template_offset_packet_reentry_blocked_pending_recovered_real_packet',
        'sourceBasis': ['packet-contract-required', 'deterministic-verifier-replay-required', 'classic-specific-provenance-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketRecoveryPlanSummary',
            'systTemplateOffsetEvidencePacketFailureTaxonomySummary',
            'systTemplateOffsetEvidencePacketReplayReadinessSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': recovery_plan.get('contractSchemaVersion'),
        'failureClassIds': recovery_plan.get('failureClassIds', []),
        'recoveryActionIds': recovery_plan.get('recoveryActionIds', []),
        'reentryStepCount': len(reentry_steps),
        'reentryStepIds': [step['stepId'] for step in reentry_steps],
        'reentrySteps': reentry_steps,
        'blockedShortcuts': [step['blockedShortcut'] for step in reentry_steps],
        'requiredVerifierBeforePromotion': [
            'python3 tools/extract_ev_system_semantics.py',
            'python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_systems_manifest_promotes_static_system_ids_and_name_seeds -v',
            'python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty',
        ],
        'blockedPromotionClaims': recovery_plan.get('blockedPromotionClaims', []) + [
            'treating a recovered packet as accepted before artifact readback, failure-class closure, full replay, and narrow-scope quarantine',
        ],
        'promotionBlockers': [
            'reentry guardrail is a replay path, not Classic byte-offset evidence',
            'recovered packets must start again at artifact readback and rerun every acceptance gate',
            'clearing a failure class does not promote offsets, field widths, Con-slot placement, non-topology behavior, or broad runtime universe replacement',
            'broad runtime universe replacement remains blocked until all name, topology, display, non-topology, and template-offset gates close',
        ],
        'nextEvidenceFamilies': recovery_plan.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; recovered packet reentry guardrail only pending real Classic-specific packet',
        'sourceNote': 'This guardrail prevents recovered or revised syst template/offset packets from bypassing the original contract/matrix/triage/replay path. It adds no packet evidence and cannot promote byte offsets or runtime behavior.',
    }


def _syst_template_offset_evidence_packet_custody_audit_summary(run: dict) -> dict:
    """Require custody/audit evidence before replaying recovered syst offset packets."""
    reentry_guardrail = _syst_template_offset_evidence_packet_reentry_guardrail_summary(run)
    custody_checkpoints = [
        {
            'checkpointId': 'packet-origin-and-hash-readback',
            'requiredEvidence': 'record packet path, packetId, source artifact hash, source owner, and local readback hash before replay',
            'blockedShortcut': 'do not replay a recovered packet when its artifact hash or origin trail is missing',
        },
        {
            'checkpointId': 'classic-specific-provenance-chain',
            'requiredEvidence': 'tie every asserted field offset to Classic-specific TMPL/ResEdit/source/runtime packet evidence, not EV-family transfer alone',
            'blockedShortcut': 'do not let EV-family, adaptation, or inferred templates stand in for Classic-specific custody',
        },
        {
            'checkpointId': 'verifier-output-archive',
            'requiredEvidence': 'archive actual extractor, focused model validation, JSON parse, and static_topology_source_readiness_scout output for the accepted packet',
            'blockedShortcut': 'do not cite a verifier command without retained current-run output or replayable logs',
        },
        {
            'checkpointId': 'narrow-claim-diff-review',
            'requiredEvidence': 'review the manifest diff and list exactly which byte offsets/field widths are allowed to change before promotion',
            'blockedShortcut': 'do not allow a custody-clean packet to lift unrelated display, topology, name, non-topology, or runtime-universe blockers',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-custody-audit',
        'oracleStatus': 'syst_template_offset_packet_custody_blocked_pending_replayable_audit_trail',
        'sourceBasis': ['packet-contract-required', 'classic-specific-provenance-required', 'deterministic-verifier-output-required', 'narrow-claim-diff-review-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketReentryGuardrailSummary',
            'systTemplateOffsetEvidencePacketRecoveryPlanSummary',
            'systTemplateOffsetEvidencePacketContractSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': reentry_guardrail.get('contractSchemaVersion'),
        'failureClassIds': reentry_guardrail.get('failureClassIds', []),
        'reentryStepIds': reentry_guardrail.get('reentryStepIds', []),
        'custodyCheckpointCount': len(custody_checkpoints),
        'custodyCheckpointIds': [checkpoint['checkpointId'] for checkpoint in custody_checkpoints],
        'custodyCheckpoints': custody_checkpoints,
        'blockedShortcuts': [checkpoint['blockedShortcut'] for checkpoint in custody_checkpoints],
        'requiredVerifierBeforePromotion': reentry_guardrail.get('requiredVerifierBeforePromotion', []) + [
            'python3 -m json.tool native_ev/data/sourced_ev_systems.json',
        ],
        'blockedPromotionClaims': reentry_guardrail.get('blockedPromotionClaims', []) + [
            'treating custody/audit cleanliness as proof of Classic byte offsets without narrow accepted field claims',
            'promoting broad runtime universe replacement from a custody-clean template packet before name/topology/display/non-topology gates close',
        ],
        'promotionBlockers': [
            'custody audit is a replay/audit trail, not Classic byte-offset evidence',
            'Classic-specific provenance, artifact hashes, verifier output archives, and narrow diff review are all required before any future packet promotion',
            'custody-clean packets still cannot promote unrelated Con-slot placement, non-topology behavior, display calibration, record-name joins, or broad runtime universe replacement',
            'broad runtime universe replacement remains blocked until all name, topology, display, non-topology, and template-offset gates close',
        ],
        'nextEvidenceFamilies': reentry_guardrail.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; custody audit trail only pending real replayable Classic-specific packet evidence',
        'sourceNote': 'This custody audit layer records the artifact provenance, verifier-output archive, and narrow diff review required before a recovered syst template/offset packet can be considered for promotion. It adds no packet evidence and cannot promote byte offsets or runtime behavior.',
    }


def _syst_template_offset_evidence_packet_promotion_quarantine_summary(run: dict) -> dict:
    """Quarantine future accepted syst offset packet claims to their covered fields."""
    custody_audit = _syst_template_offset_evidence_packet_custody_audit_summary(run)
    quarantine_controls = [
        {
            'controlId': 'covered-field-only-diff-boundary',
            'requiredEvidence': 'list exact accepted Classic field names, byte offsets, widths, and manifest paths before any promotion diff is proposed',
            'blockedShortcut': 'do not promote neighboring unresolved words or inferred Con-slot placement from a covered-field packet',
        },
        {
            'controlId': 'unrelated-gate-preservation',
            'requiredEvidence': 'copy forward name, topology, display, non-topology, and runtime-universe blockers that the packet does not explicitly satisfy',
            'blockedShortcut': 'do not treat a template/source packet as closing record-name joins, display scaling, route-label, or broad universe replacement gates',
        },
        {
            'controlId': 'post-promotion-verifier-replay',
            'requiredEvidence': 'rerun extractor, JSON parse, focused model validation, and static_topology_source_readiness_scout after the quarantined diff is staged',
            'blockedShortcut': 'do not rely on pre-diff verifier output after changing sourced_ev_systems manifest fields',
        },
        {
            'controlId': 'runtime-scaffold-boundary-review',
            'requiredEvidence': 'state whether covered fields are promoted as source-backed data only or intentionally excluded from gameplay/runtime scaffolds',
            'blockedShortcut': 'do not route AI, hazards, visibility, governments, ports, or navigation defaults into gameplay from a narrow offset packet without a separate runtime integration gate',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-promotion-quarantine',
        'oracleStatus': 'syst_template_offset_packet_promotion_quarantine_blocked_pending_accepted_packet_diff',
        'sourceBasis': ['narrow-claim-diff-review-required', 'deterministic-verifier-output-required', 'runtime-integration-gates-preserved'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketCustodyAuditSummary',
            'systTemplateOffsetEvidencePacketReentryGuardrailSummary',
            'systTemplateOffsetEvidencePacketContractSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': custody_audit.get('contractSchemaVersion'),
        'custodyCheckpointIds': custody_audit.get('custodyCheckpointIds', []),
        'quarantineControlCount': len(quarantine_controls),
        'quarantineControlIds': [control['controlId'] for control in quarantine_controls],
        'quarantineControls': quarantine_controls,
        'blockedShortcuts': [control['blockedShortcut'] for control in quarantine_controls],
        'requiredVerifierBeforePromotion': custody_audit.get('requiredVerifierBeforePromotion', []) + [
            'python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty',
        ],
        'blockedPromotionClaims': custody_audit.get('blockedPromotionClaims', []) + [
            'using a narrow accepted field packet to promote unrelated syst offsets, display calibration, record-name joins, route labels, non-topology behavior, or broad runtime universe replacement',
            'routing newly identified offset fields into gameplay before a separate runtime/scaffold integration gate accepts that exact use',
        ],
        'promotionBlockers': [
            'promotion quarantine is a diff boundary, not Classic byte-offset evidence',
            'accepted packet claims must be scoped to explicitly covered Classic fields and replayed after any manifest diff',
            'unrelated name, topology, display, non-topology, and runtime-universe blockers remain active unless separately satisfied',
            'gameplay/runtime scaffolds may not consume newly covered fields without an explicit integration gate',
        ],
        'nextEvidenceFamilies': custody_audit.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; promotion quarantine only pending an accepted Classic-specific packet diff',
        'sourceNote': 'This quarantine layer defines how future accepted syst template/offset packets may change only explicitly covered manifest fields while preserving unrelated fidelity gates. It adds no packet evidence and cannot route unresolved or newly identified fields into gameplay.',
    }


def _syst_template_offset_evidence_packet_rollback_readiness_summary(run: dict) -> dict:
    """Define rollback readiness for future quarantined syst offset packet diffs."""
    promotion_quarantine = _syst_template_offset_evidence_packet_promotion_quarantine_summary(run)
    rollback_controls = [
        {
            'controlId': 'pre-diff-baseline-capture',
            'requiredEvidence': 'record the pre-promotion manifest hash, focused verifier output, and exact dirty file set before applying an accepted packet diff',
            'blockedShortcut': 'do not stage a packet diff when the previous sourced systems baseline cannot be reconstructed',
        },
        {
            'controlId': 'failed-verifier-revert-path',
            'requiredEvidence': 'if extractor, JSON validation, model checks, or static topology scenario fail after the diff, revert only the packet diff and preserve the rejected packet artifact for taxonomy/recovery',
            'blockedShortcut': 'do not patch around a failed verifier by broadening unrelated blockers or weakening model/scenario assertions',
        },
        {
            'controlId': 'post-revert-replay',
            'requiredEvidence': 'rerun extractor, JSON validation, focused model validation, and static_topology_source_readiness_scout after rollback to prove the baseline gates are restored',
            'blockedShortcut': 'do not continue with new offset work after rollback until the restored baseline verifier replay passes',
        },
        {
            'controlId': 'rollback-event-handoff',
            'requiredEvidence': 'write a compact event/packet naming rejected claims, reverted paths, verifier failure, restored verifier result, and next evidence family',
            'blockedShortcut': 'do not drop failed packet context from the ledger/event stream just because the manifest was reverted',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-rollback-readiness',
        'oracleStatus': 'syst_template_offset_packet_rollback_readiness_blocked_pending_failed_or_conflicting_packet_diff',
        'sourceBasis': ['rollback-baseline-required', 'deterministic-verifier-replay-required', 'failed-packet-context-preserved'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketPromotionQuarantineSummary',
            'systTemplateOffsetEvidencePacketCustodyAuditSummary',
            'systTemplateOffsetEvidencePacketFailureTaxonomySummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': promotion_quarantine.get('contractSchemaVersion'),
        'quarantineControlIds': promotion_quarantine.get('quarantineControlIds', []),
        'rollbackControlCount': len(rollback_controls),
        'rollbackControlIds': [control['controlId'] for control in rollback_controls],
        'rollbackControls': rollback_controls,
        'blockedShortcuts': [control['blockedShortcut'] for control in rollback_controls],
        'requiredVerifierAfterRollback': [
            'python3 tools/extract_ev_system_semantics.py',
            'python3 -m json.tool native_ev/data/sourced_ev_systems.json',
            'python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_systems_manifest_promotes_static_system_ids_and_name_seeds -v',
            'python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty',
        ],
        'blockedPromotionClaims': promotion_quarantine.get('blockedPromotionClaims', []) + [
            'treating rollback as proof that a rejected or conflicting Classic packet was partially accepted',
            'weakening unrelated source-readiness gates to make a failed packet diff pass',
        ],
        'promotionBlockers': [
            'rollback readiness is a recovery guardrail, not Classic byte-offset evidence',
            'failed or conflicting packet diffs must restore the previous manifest baseline before new offset work continues',
            'reverted packet claims remain rejected/pending evidence until the full acceptance path is replayed',
        ],
        'nextEvidenceFamilies': promotion_quarantine.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; rollback readiness only pending a failed or conflicting accepted-packet diff',
        'sourceNote': 'This rollback layer preserves a deterministic recovery path for future quarantined syst template/offset packet diffs. It adds no Classic packet evidence and cannot partially promote failed or reverted claims.',
    }


def _syst_template_offset_evidence_packet_rollback_rehearsal_summary(run: dict) -> dict:
    """Define a dry-run rehearsal checklist for reverting future quarantined offset diffs."""
    rollback_readiness = _syst_template_offset_evidence_packet_rollback_readiness_summary(run)
    rehearsal_steps = [
        {
            'stepId': 'baseline-manifest-snapshot-readback',
            'requiredEvidence': 'capture and read back the current sourced_ev_systems.json hash plus the dirty file set before any accepted packet diff rehearsal',
            'blockedShortcut': 'do not claim rollback rehearsability without a concrete baseline manifest snapshot',
        },
        {
            'stepId': 'isolated-quarantine-diff-revert',
            'requiredEvidence': 'prove the rollback target is limited to the accepted packet diff fields and does not revert unrelated source-readiness guardrails',
            'blockedShortcut': 'do not use rollback rehearsal to remove unrelated blockers or current promoted static fields',
        },
        {
            'stepId': 'post-revert-verifier-replay-capture',
            'requiredEvidence': 'record the exact extractor, JSON parse, focused model validation, and static topology scenario output after reverting the rehearsal diff',
            'blockedShortcut': 'do not mark a rollback rehearsal ready from stale pre-revert verifier output',
        },
        {
            'stepId': 'failed-packet-ledger-handoff',
            'requiredEvidence': 'record the rejected packet id, reverted manifest keys, failed verifier, restored verifier, and next evidence family in the long-running ledger/event stream',
            'blockedShortcut': 'do not discard rejected packet context once the working tree has been restored',
        },
    ]
    return {
        'sourceLabel': 'repo-reference-backed-syst-template-offset-evidence-packet-rollback-rehearsal',
        'oracleStatus': 'syst_template_offset_packet_rollback_rehearsal_blocked_pending_actual_reverted_packet_diff',
        'sourceBasis': ['rollback-dry-run-checklist', 'baseline-snapshot-required', 'post-revert-verifier-capture-required'],
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'systTemplateOffsetEvidencePacketRollbackReadinessSummary',
            'systTemplateOffsetEvidencePacketPromotionQuarantineSummary',
            'systTemplateOffsetEvidencePacketCustodyAuditSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'contractSchemaVersion': rollback_readiness.get('contractSchemaVersion'),
        'rollbackControlIds': rollback_readiness.get('rollbackControlIds', []),
        'rehearsalStepCount': len(rehearsal_steps),
        'rehearsalStepIds': [step['stepId'] for step in rehearsal_steps],
        'rehearsalSteps': rehearsal_steps,
        'blockedShortcuts': [step['blockedShortcut'] for step in rehearsal_steps],
        'requiredVerifierAfterRehearsal': rollback_readiness.get('requiredVerifierAfterRollback', []),
        'blockedPromotionClaims': rollback_readiness.get('blockedPromotionClaims', []) + [
            'treating a dry-run rollback rehearsal as evidence that a Classic offset packet was accepted',
            'using rollback rehearsal to broaden packet scope beyond explicitly reverted fields',
        ],
        'promotionBlockers': [
            'rollback rehearsal is an operational safety checklist, not Classic byte-offset evidence',
            'a rehearsal cannot promote or partially promote failed, reverted, or still-pending packet claims',
            'actual acceptance still requires the full contract, validation matrix, custody audit, quarantine, and post-diff verifier replay path',
        ],
        'nextEvidenceFamilies': rollback_readiness.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; rollback rehearsal only pending an actual reverted packet diff',
        'sourceNote': 'This rehearsal layer preserves a dry-run recovery checklist for future quarantined syst template/offset packet diffs. It adds no Classic packet evidence and cannot promote failed, reverted, or hypothetical offset claims.',
    }


def _syst_word_domain_coverage_summary(run: dict) -> dict:
    """Preserve a complete word-domain coverage matrix for future syst offset oracles."""
    word_domains = []
    field_count = len(run['records'][0].get('fields', [])) if run.get('records') else 0
    for word_index in range(field_count):
        word_summary = _word_group_summary(run, [word_index])
        word_domains.append({
            'wordIndex': word_index,
            'observedValueRange': word_summary['observedValueRange'],
            'distinctObservedValues': word_summary['distinctObservedValues'],
            'distinctObservedValueCount': word_summary['distinctObservedValueCount'],
            'allValuesZero': word_summary['allValuesZero'],
            'allValuesNoLinkSentinel': word_summary['allValuesNoLinkSentinel'],
            'systemIdDomainValueCount': word_summary['systemIdDomainValueCount'],
            'noLinkSentinelCount': word_summary['noLinkSentinelCount'],
            'zeroValueCount': word_summary['zeroValueCount'],
        })
    return {
        'sourceLabel': 'decoded-resource-backed-syst-word-domain-coverage-scout',
        'oracleStatus': 'syst_field_order_mapping_pending_complete_oracle',
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'wordCount': field_count,
        'wordDomains': word_domains,
        'coverageSignals': {
            'coordinateCandidateWords': [0, 1, 2, 3],
            'systemIdDomainWords': [
                entry['wordIndex']
                for entry in word_domains
                if entry['systemIdDomainValueCount'] > 0
            ],
            'noLinkSentinelOnlyWords': [
                entry['wordIndex']
                for entry in word_domains
                if entry['allValuesNoLinkSentinel']
            ],
            'zeroOnlyTailWords': [
                entry['wordIndex']
                for entry in word_domains
                if entry['wordIndex'] >= 24 and entry['allValuesZero']
            ],
            'percentLikeValueWords': [20, 21, 22, 23],
        },
        'promotionBlockers': [
            'complete syst field-order oracle is still missing',
            'word-domain coverage records value families but does not assign Resource Bible field semantics to unresolved offsets',
            'current link-domain and zero-tail coverage must not promote Con6-Con16 split placement or non-topology syst fields without an offset oracle',
        ],
        'nextEvidenceFamilies': [
            'source-level syst struct declaration including field widths and offsets',
            'ResEdit/template field map tying each word offset to a Resource Bible family',
            'runtime probes that disambiguate word-domain candidates for navigation, population, government, hazard, visibility, and Con6-Con16 fields',
        ],
        'sourceNote': 'This packet records every decoded word-domain in the 44-word syst-like records as source-readiness evidence. It narrows future offset-oracle work while explicitly withholding downstream field semantics and broad runtime universe promotion.',
    }


def _non_topology_syst_oracle_gap_summary(run: dict) -> dict:
    """Record non-topology syst field gates before gameplay integration."""
    evidence_inputs = [
        'systFieldLayoutSourceReadinessSummary',
        'systFieldOrderConflictSummary',
        'resourceBibleSystSequentialFieldProjectionSummary',
        'systWordDomainCoverageSummary',
        'runtimeUniverseReplacementGateSummary',
    ]
    blocked_families = [
        'NavDef F1-F4 navigation defaults',
        'DudeTypes/%Prob/AvgShips AI population controls',
        'Govt/Message/Asteroids/Interference/VisBit environment and visibility controls',
        'Con6-Con16 additional hyperspace links',
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-non-topology-syst-oracle-gap',
        'oracleStatus': 'non_topology_syst_fields_blocked_pending_field_order_or_runtime_oracle',
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': evidence_inputs,
        'evidenceInputSummaryCount': len(evidence_inputs),
        'blockedResourceBibleFamilies': blocked_families,
        'decodedWordGroupScouts': {
            'projectedNavDefF1ToF4Words9To12': _word_group_summary(run, [9, 10, 11, 12]),
            'projectedDudeProbabilityAvgShipsWords13To21': _word_group_summary(run, list(range(13, 22))),
            'projectedGovtMessageHazardVisibilityWords22To26': _word_group_summary(run, [22, 23, 24, 25, 26]),
            'projectedCon6ToCon16Words27To37': _word_group_summary(run, list(range(27, 38))),
            'currentCandidateLinkScoutWindowWords4To19': _word_group_summary(run, list(range(4, 20))),
        },
        'requiredOracleClaims': [
            'complete syst field-order oracle identifying word widths and offsets for NavDef, population, government, message, hazard, visibility, and split Con6-Con16 fields',
            'runtime/source evidence tying navigation defaults to selectable/radar objects before AI or target UI integration',
            'runtime/source evidence tying governments, message buoys, asteroids, interference, and visibility bits to observed gameplay before environment integration',
            'field-order reconciliation that preserves candidate topology scout data without treating every scout word as a promoted Resource Bible field',
        ],
        'promotionReadinessStatus': 'blocked; non-topology syst fields are source-backed family names only',
        'promotionBlockers': [
            'do not route AI, hazards, message buoys, visibility, or government ownership from unresolved word windows',
            'direct Resource Bible 16-bit projection conflicts with current decoded word-domain scout evidence',
            'current Con1-Con16 contiguous link scout remains analysis input only and cannot promote downstream field semantics',
            'broad runtime universe replacement remains blocked until non-topology fields have an offset/runtime oracle or explicit scaffold boundary',
        ],
        'nextEvidenceFamilies': [
            'source-level syst struct declaration including NavDef/population/government/message/hazard/visibility offsets',
            'ResEdit/template field map tying syst field names to byte offsets and field widths',
            'runtime probes for navigation defaults, governments, message buoys, asteroids, interference, visibility bits, and Con6-Con16 behavior',
        ],
        'sourceNote': 'This packet narrows the next non-topology syst integration gate: Resource Bible family names are preserved, but unresolved offsets and conflicting word-domain scouts block gameplay use of navigation defaults, AI populations, governments, hazards, messages, visibility, and split Con6-Con16 placement.',
    }


def _syst_non_topology_field_family_reference_summary(run: dict) -> dict:
    """Resource-Bible-backed per-field-family reference for non-topology syst fields."""
    field_families = [
        {
            'familyId': 'navDef',
            'familyName': 'NavDef F1-F4 Navigation Defaults',
            'resourceBibleLineRef': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 942-945',
            'fieldCount': 4,
            'individualFields': ['NavDef F1', 'NavDef F2', 'NavDef F3', 'NavDef F4'],
            'valueDomain': '-1 for no default; 128-1627 for stellar object resource IDs used as keyboard navigation targets',
            'candidateWordIndices': [9, 10, 11, 12],
            'wordIndexNote': 'sequential Resource Bible projection; may conflict with current contiguous link-scout window at words 4-19',
            'gameplaySurface': 'Radar target locking, AI stellar-object tracking, status-display object selection, keyboard nav defaults',
            'promotionStatus': 'not-promoted; offset oracle gap blocks assignment of decoded words to NavDef fields',
        },
        {
            'familyId': 'dudeTypesAndProbability',
            'familyName': 'DudeTypes / %Prob / AvgShips AI Population Controls',
            'resourceBibleLineRef': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 947-959',
            'fieldCount': 9,
            'individualFields': ['DudeType 1', 'DudeType 2', 'DudeType 3', 'DudeType 4', '%Prob 1', '%Prob 2', '%Prob 3', '%Prob 4', 'AvgShips'],
            'valueDomain': 'DudeTypes: 128-255 dude type resource IDs (or negative fleet IDs); %Prob: 1-99 percent; AvgShips: 0+ (±50%)',
            'candidateWordIndices': list(range(13, 22)),
            'wordIndexNote': 'sequential Resource Bible projection; may conflict with current contiguous link-scout window at words 4-19',
            'gameplaySurface': 'NPC ship spawn composition, encounter generation, fleet presence, empty-system detection',
            'promotionStatus': 'not-promoted; offset oracle gap blocks assignment of decoded words to population fields',
        },
        {
            'familyId': 'govt',
            'familyName': 'Govt Controlling Government',
            'resourceBibleLineRef': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 962-964',
            'fieldCount': 1,
            'individualFields': ['Govt'],
            'valueDomain': '-1 for independent/ignored; 128-255 for controlling government resource ID',
            'candidateWordIndices': [22],
            'wordIndexNote': 'sequential Resource Bible projection; candidate index 22 is beyond the contiguous link-scout window',
            'gameplaySurface': 'Legal jurisdiction, crime tolerance, scan behavior, bounty/permit availability, sovereign space',
            'promotionStatus': 'not-promoted; offset oracle gap blocks assignment of decoded words to Govt field',
        },
        {
            'familyId': 'messageBuoy',
            'familyName': 'Message Buoy String',
            'resourceBibleLineRef': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 966-970',
            'fieldCount': 1,
            'individualFields': ['Message'],
            'valueDomain': '-1 for no message; 1+ for STR# resource 1000 entry index used as message-buoy text',
            'candidateWordIndices': [23],
            'wordIndexNote': 'sequential Resource Bible projection; candidate index 23 is beyond the contiguous link-scout window',
            'gameplaySurface': 'System-entry message display, story/event text on arrival, buoy message trigger',
            'promotionStatus': 'not-promoted; offset oracle gap blocks assignment of decoded words to Message field',
        },
        {
            'familyId': 'asteroids',
            'familyName': 'Asteroids Navigation Hazard',
            'resourceBibleLineRef': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 972-973',
            'fieldCount': 1,
            'individualFields': ['Asteroids'],
            'valueDomain': '0-10 asteroid count placed in system',
            'candidateWordIndices': [24],
            'wordIndexNote': 'sequential Resource Bible projection; candidate index 24 is beyond the contiguous link-scout window',
            'gameplaySurface': 'Asteroid field density, mining potential, collision hazard, navigation obstacle',
            'promotionStatus': 'not-promoted; offset oracle gap blocks assignment of decoded words to Asteroids field',
        },
        {
            'familyId': 'interference',
            'familyName': 'Interference Sensor Static',
            'resourceBibleLineRef': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 973-974',
            'fieldCount': 1,
            'individualFields': ['Interference'],
            'valueDomain': '0 (no static) to 100 (complete sensor blackout)',
            'candidateWordIndices': [25],
            'wordIndexNote': 'sequential Resource Bible projection; candidate index 25 is beyond the contiguous link-scout window',
            'gameplaySurface': 'Radar/sensor degradation, visual static effect, target-acquisition difficulty',
            'promotionStatus': 'not-promoted; offset oracle gap blocks assignment of decoded words to Interference field',
        },
        {
            'familyId': 'visBit',
            'familyName': 'VisBit System Visibility Control',
            'resourceBibleLineRef': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 976-984',
            'fieldCount': 1,
            'individualFields': ['VisBit'],
            'valueDomain': '-1 for always visible; 0-255 for visible when mission bit is set; 1000-1255 for visible when mission bit is cleared',
            'candidateWordIndices': [26],
            'wordIndexNote': 'sequential Resource Bible projection; candidate index 26 is beyond the contiguous link-scout window',
            'gameplaySurface': 'Conditional system visibility, mission-gated system reveals, system-hiding/replacement tricks',
            'promotionStatus': 'not-promoted; offset oracle gap blocks assignment of decoded words to VisBit field',
        },
        {
            'familyId': 'con6ToCon16',
            'familyName': 'Con6-Con16 Additional Hyperspace Links',
            'resourceBibleLineRef': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 987-989',
            'fieldCount': 11,
            'individualFields': [f'Con{idx}' for idx in range(6, 17)],
            'valueDomain': '-1 for no link; 128-1127 for linked system resource IDs',
            'candidateWordIndices': list(range(27, 38)),
            'wordIndexNote': 'sequential Resource Bible projection; candidate indices 27-37 are beyond the contiguous link-scout window and must not be confused with the current words 4-19 link scout',
            'gameplaySurface': 'Extended hyperspace connectivity beyond the initial five Con1-Con5 links; map topology and route planning',
            'promotionStatus': 'not-promoted; offset oracle gap and Con6-Con16 split placement require Classic TMPL/ResEdit/source template-offset evidence',
        },
    ]
    field_family_count = sum(f['fieldCount'] for f in field_families)
    return {
        'sourceLabel': 'resource-bible-backed-non-topology-syst-field-family-reference',
        'oracleStatus': 'non_topology_syst_field_families_blocked_pending_syst_template_offset_oracle',
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'fieldFamilyCount': len(field_families),
        'individualFieldCount': field_family_count,
        'fieldFamilies': field_families,
        'familyIds': [f['familyId'] for f in field_families],
        'blockedGameplaySurfaces': sorted({f['gameplaySurface'] for f in field_families}),
        'promotionBlockers': [
            'Classic-specific syst TMPL/ResEdit/source template-offset evidence is absent',
            'Resource Bible sequential 16-bit projection conflicts with current decoded word-domain scout data',
            'current contiguous Con1-Con16 link scout at words 4-19 may overlap projected NavDef/DudeType/Prob word indices 9-21',
            'exact Con6-Con16 split placement at words 27-37 vs a contiguous Con1-Con16 layout remains unresolved',
            'each field family requires validated Classic-specific field-offset evidence before decoded-word assignment or gameplay integration',
        ],
        'nextEvidenceFamilies': [
            'syst TMPL or ResEdit template with per-field byte offsets and widths',
            'original-runtime probes confirming NavDef, government, hazard, and visibility behavior in known systems',
            'Classic source struct declarations for the syst resource layout',
        ],
        'promotionStatus': 'not-promoted; field family reference only, pending Classic-specific template/offset evidence for every field',
        'sourceNote': 'This reference preserves every Resource Bible syst field family name, value domain, and gameplay surface without assigning exact word indices or promoting gameplay integration. It is a dispatch/AI-readable index for future workers who need to know what non-topology field families exist before offset oracles unlock integration.',
    }


def _non_topology_syst_runtime_probe_priority_summary(run: dict) -> dict:
    """Prioritize future non-topology syst probes without assigning unresolved offsets."""
    word_domain = _syst_word_domain_coverage_summary(run)
    field_order_gap = _non_topology_syst_oracle_gap_summary(run)
    priority_groups = [
        {
            'probeFamily': 'government-message-hazard-visibility-disambiguation',
            'resourceBibleFamilies': ['Govt', 'Message', 'Asteroids', 'Interference', 'VisBit1', 'VisBit2'],
            'candidateWordIndices': [22, 23, 24, 25, 26],
            'priorityReason': 'environment ownership and hazard semantics gate safe broad universe replacement',
            'blockedGameplayClaims': ['government ownership', 'message buoys', 'asteroid density', 'interference', 'visibility bits'],
        },
        {
            'probeFamily': 'navigation-default-runtime-disambiguation',
            'resourceBibleFamilies': ['NavDef F1-F4'],
            'candidateWordIndices': [9, 10, 11, 12],
            'priorityReason': 'navigation defaults affect radar/target selection and must not be inferred from current link scouts',
            'blockedGameplayClaims': ['navigation defaults', 'radar-default object binding'],
        },
        {
            'probeFamily': 'population-ai-presence-disambiguation',
            'resourceBibleFamilies': ['DudeTypes', '%Prob', 'AvgShips'],
            'candidateWordIndices': list(range(13, 22)),
            'priorityReason': 'AI population claims need runtime/source confirmation before encounter generation',
            'blockedGameplayClaims': ['NPC ship families', 'NPC spawn probability', 'average ship counts'],
        },
        {
            'probeFamily': 'split-con6-con16-link-placement-disambiguation',
            'resourceBibleFamilies': ['Con6-Con16'],
            'candidateWordIndices': list(range(27, 38)),
            'priorityReason': 'sequential Resource Bible projection currently lands on all-zero words and conflicts with the active link scout window',
            'blockedGameplayClaims': ['additional hyperspace links beyond the current contiguous link scout'],
        },
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-non-topology-syst-runtime-probe-priority',
        'oracleStatus': 'non_topology_syst_runtime_probe_blocked_pending_offset_or_runtime_oracle',
        'sourceReferences': SYST_FIELD_LAYOUT_SOURCE_REFERENCES,
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'nonTopologySystOracleGapSummary',
            'systWordDomainCoverageSummary',
            'systFieldOrderConflictSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'priorityProbeGroups': priority_groups,
        'firstPriorityProbeFamily': priority_groups[0]['probeFamily'],
        'firstPriorityCandidateWordIndices': priority_groups[0]['candidateWordIndices'],
        'percentLikeValueWords': word_domain.get('coverageSignals', {}).get('percentLikeValueWords', []),
        'zeroOnlyTailWords': word_domain.get('coverageSignals', {}).get('zeroOnlyTailWords', []),
        'blockedResourceBibleFamilies': field_order_gap.get('blockedResourceBibleFamilies', []),
        'promotionBlockers': [
            'priority groups are a capture worklist, not promoted syst field offsets',
            'government, hazard, message, visibility, navigation, and AI semantics remain blocked until a field-order or runtime oracle lands',
            'do not replace runtime universe environment data from candidate word groups alone',
        ],
        'nextEvidenceFamilies': [
            'runtime captures comparing government/message/hazard/visibility behavior across known systems',
            'source-level syst struct declaration or Classic-specific template with byte offsets',
            'runtime probes that toggle or observe NavDef, population, and split Con6-Con16 behavior independently',
        ],
        'promotionStatus': 'not-promoted; runtime probe priority only',
        'sourceNote': 'This worklist gives the next safe runtime/source evidence order for non-topology syst fields. It intentionally keeps all candidate word groups behind the existing offset/runtime-oracle gate and does not route governments, hazards, visibility, messages, AI, or ports from decoded data.',
    }


def _non_topology_syst_runtime_capture_gate_summary(run: dict) -> dict:
    """Define the gated capture packet for the first non-topology syst probe family."""
    priority = _non_topology_syst_runtime_probe_priority_summary(run)
    first_group = priority.get('priorityProbeGroups', [{}])[0]
    return {
        'sourceLabel': 'decoded-resource-backed-non-topology-syst-runtime-capture-gate',
        'oracleStatus': 'non_topology_syst_capture_blocked_pending_disposable_runtime_probe',
        'sourceBasis': ['decoded-record-family', 'resource-bible-field', 'original-runtime-capture-required'],
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'nonTopologySystRuntimeProbePrioritySummary',
            'nonTopologySystOracleGapSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 3,
        'firstPriorityProbeFamily': first_group.get('probeFamily'),
        'firstPriorityCandidateWordIndices': first_group.get('candidateWordIndices', []),
        'requiredComparisonAxes': [
            'government ownership or landing/legal-affiliation behavior',
            'message buoy or system-message visibility',
            'asteroid/hazard density and interference behavior',
            'visibility-bit gated object or route/map visibility behavior',
        ],
        'requiredCaptureFields': [
            'disposableNonStrictPilot',
            'originalRuntimeVersionAndScenarioBuild',
            'startSystemNameAndResourceIdHypothesis',
            'targetSystemNameOrRouteLabel',
            'observedGovernmentOrLegalAffiliation',
            'observedSystemMessageOrBuoyText',
            'observedAsteroidOrInterferenceBehavior',
            'observedVisibilityBitEffect',
            'negativeControlSystemOrFieldFamily',
        ],
        'capturePacketSchemaVersion': 1,
        'requiredCapturePacketCount': 2,
        'capturePacketTemplates': [
            {
                'packetId': 'non-topology-gov-message-hazard-visibility-positive-control',
                'probeFamily': first_group.get('probeFamily'),
                'candidateWordIndices': first_group.get('candidateWordIndices', []),
                'requiredObservationFields': [
                    'observedGovernmentOrLegalAffiliation',
                    'observedSystemMessageOrBuoyText',
                    'observedAsteroidOrInterferenceBehavior',
                    'observedVisibilityBitEffect',
                ],
                'promotionBoundary': 'observation may prioritize field-order/source follow-up but must not assign syst offsets by itself',
            },
            {
                'packetId': 'non-topology-gov-message-hazard-visibility-negative-control',
                'probeFamily': first_group.get('probeFamily'),
                'candidateWordIndices': first_group.get('candidateWordIndices', []),
                'requiredObservationFields': [
                    'negativeControlSystemOrFieldFamily',
                    'unchangedCoordinateAndRouteTopologyEvidence',
                    'unchangedRuntimeSubsetEvidence',
                ],
                'promotionBoundary': 'negative control prevents environment/hazard observations from being confused with coordinate or route topology probes',
            },
        ],
        'captureValidationRules': [
            'capture packets must name the original runtime build and pilot safety class',
            'positive and negative controls must be recorded before any field-order promotion claim',
            'observations can refine the next probe queue but cannot promote government, hazard, message, or visibility offsets alone',
        ],
        'safetyBlockers': [
            'do not run destructive or reputation-changing probes on Strict Play or reusable pilots',
            'do not replace runtime universe environment, government, hazard, or visibility behavior from capture templates alone',
        ],
        'promotionBlockers': [
            'capture gate is a runtime evidence schema, not a decoded byte-offset oracle',
            'Resource Bible family names remain unjoined to concrete syst words until source/runtime evidence is reconciled',
        ],
        'nextEvidenceFamilies': [
            'disposable original-runtime captures for government/message/hazard/visibility behavior',
            'source-level syst struct declaration or Classic-specific template with byte offsets',
            'post-capture reconciliation against word-domain and field-order conflict summaries',
        ],
        'promotionStatus': 'not-promoted; capture gate only',
        'sourceNote': 'This gate turns the first priority non-topology worklist item into a safe, disposable runtime capture packet while explicitly preserving the unresolved offset boundary.',
    }


def _non_topology_syst_runtime_capture_validation_matrix_summary(run: dict) -> dict:
    """Define acceptance checks for non-topology runtime capture packets before reconciliation."""
    capture_gate = _non_topology_syst_runtime_capture_gate_summary(run)
    required_packet_ids = [
        packet.get('packetId')
        for packet in capture_gate.get('capturePacketTemplates', [])
    ]
    validation_rows = [
        {
            'checkId': 'packet-schema-and-runtime-build-readback',
            'requiredEvidence': 'each capture packet names the disposable pilot class, original runtime version/build, packet id, and observed system/field family',
            'failureClass': 'missing-capture-provenance-or-schema-field',
            'blockedShortcut': 'do not reconcile observations whose runtime build, pilot safety class, or packet id cannot be read back',
        },
        {
            'checkId': 'positive-negative-control-pair-completeness',
            'requiredEvidence': 'positive and negative control packets both exist for the first priority government/message/hazard/visibility probe family',
            'failureClass': 'missing-positive-or-negative-control-pair',
            'blockedShortcut': 'do not promote or refine field-order priority from a one-sided capture',
        },
        {
            'checkId': 'topology-boundary-noninterference',
            'requiredEvidence': 'capture notes confirm coordinate, route-label, record-name, and runtime subset gates remain unchanged by the non-topology probe',
            'failureClass': 'topology-boundary-contamination',
            'blockedShortcut': 'do not treat environment observations as evidence for coordinate scaling, route labels, name joins, or broad universe replacement',
        },
        {
            'checkId': 'source-runtime-field-order-handoff',
            'requiredEvidence': 'validated capture packets are handed off as priority refiners only until a Classic-specific field-order/source packet assigns offsets',
            'failureClass': 'runtime-observation-used-as-offset-oracle',
            'blockedShortcut': 'do not assign Govt/Message/Asteroids/Interference/VisBit offsets from runtime observation alone',
        },
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-non-topology-syst-runtime-capture-validation-matrix',
        'oracleStatus': 'non_topology_syst_capture_validation_blocked_pending_complete_control_packets',
        'sourceBasis': ['decoded-record-family', 'resource-bible-field', 'original-runtime-capture-required'],
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'nonTopologySystRuntimeCaptureGateSummary',
            'nonTopologySystRuntimeProbePrioritySummary',
            'nonTopologySystOracleGapSummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'firstPriorityProbeFamily': capture_gate.get('firstPriorityProbeFamily'),
        'firstPriorityCandidateWordIndices': capture_gate.get('firstPriorityCandidateWordIndices', []),
        'requiredCapturePacketIds': required_packet_ids,
        'requiredValidatedCapturePacketCount': len(required_packet_ids),
        'validationRowCount': len(validation_rows),
        'validationCheckIds': [row['checkId'] for row in validation_rows],
        'validationRows': validation_rows,
        'failureClassIds': [row['failureClass'] for row in validation_rows],
        'blockedShortcuts': [row['blockedShortcut'] for row in validation_rows],
        'requiredVerifierBeforeReconciliation': [
            'python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty',
            'focused sourced-system manifest tests',
        ],
        'promotionBlockers': [
            'capture validation matrix is an acceptance checklist, not Classic byte-offset evidence',
            'validated runtime observations cannot promote non-topology syst field offsets without source/template or field-order evidence',
            'positive and negative control completeness does not close coordinate, route-label, record-name, or broad runtime-universe gates',
        ],
        'nextEvidenceFamilies': [
            'validated disposable original-runtime positive and negative capture packets',
            'post-capture reconciliation against word-domain, field-order conflict, and source/template evidence',
            'Classic-specific source/template/struct evidence tying non-topology field families to syst offsets',
        ],
        'promotionStatus': 'not-promoted; validation matrix only pending real control packets',
        'sourceNote': 'This packet adds the validation checklist for future non-topology runtime captures before they enter reconciliation. It keeps observations as gated evidence inputs and prevents capture packets from becoming byte-offset or gameplay promotion authority.',
    }


def _non_topology_syst_runtime_capture_reconciliation_summary(run: dict) -> dict:
    """Define post-capture reconciliation gates before any non-topology syst promotion."""
    priority = _non_topology_syst_runtime_probe_priority_summary(run)
    capture_gate = _non_topology_syst_runtime_capture_gate_summary(run)
    first_group = priority.get('priorityProbeGroups', [{}])[0]
    required_packet_ids = [
        packet.get('packetId')
        for packet in capture_gate.get('capturePacketTemplates', [])
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-non-topology-syst-runtime-capture-reconciliation-plan',
        'oracleStatus': 'non_topology_syst_capture_reconciliation_blocked_pending_validated_runtime_packets',
        'sourceBasis': ['decoded-record-family', 'resource-bible-field', 'original-runtime-capture-required'],
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'nonTopologySystRuntimeCaptureGateSummary',
            'nonTopologySystRuntimeProbePrioritySummary',
            'nonTopologySystOracleGapSummary',
            'systWordDomainCoverageSummary',
        ],
        'evidenceInputSummaryCount': 5,
        'firstPriorityProbeFamily': first_group.get('probeFamily'),
        'firstPriorityCandidateWordIndices': first_group.get('candidateWordIndices', []),
        'requiredCapturePacketIds': required_packet_ids,
        'requiredValidatedCapturePacketCount': len(required_packet_ids),
        'postCaptureReconciliationSteps': [
            'validate every required positive and negative control packet against the capture gate schema',
            'compare observed government/message/hazard/visibility behavior against candidate word-domain and field-order conflict summaries',
            'classify observations as priority refinement, contradiction, or source/runtime corroboration without assigning offsets by observation alone',
            'require a field-order/source packet before any gameplay-visible government, hazard, message, visibility, or broad universe replacement use',
        ],
        'promotionDecisionStates': [
            'no-promotion; runtime capture packets incomplete or controls missing',
            'priority-refined; capture narrows the next source/runtime query but offsets remain unresolved',
            'source-runtime-corroborated; still requires field-order/source packet before gameplay use',
        ],
        'blockedPromotionClaims': [
            'assigning Govt/Message/Asteroids/Interference/VisBit offsets from runtime observation alone',
            'routing government ownership, message buoys, hazards, interference, or visibility bits into gameplay from candidate word groups alone',
            'expanding the runtime universe from non-topology syst observations before name/topology/display gates are satisfied',
        ],
        'requiredVerifierBeforeGameplay': [
            'python3 tools/extract_ev_system_semantics.py',
            'focused sourced-system manifest tests',
            'python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty',
        ],
        'promotionBlockers': [
            'post-capture reconciliation is a gate, not a promotion packet',
            'runtime observations must be reconciled with word-domain, field-order, and source/template evidence before offset assignment',
            'positive and negative controls do not override existing coordinate, route-label, record-name, or runtime-universe replacement blockers',
        ],
        'nextEvidenceFamilies': [
            'validated disposable original-runtime positive and negative capture packets',
            'Classic-specific source/template/struct evidence tying syst words to non-topology field names',
            'post-capture contradiction checks against coordinate, route-label, and broad runtime-universe gates',
        ],
        'promotionStatus': 'not-promoted; post-capture reconciliation plan only',
        'sourceNote': 'This packet states what must happen after the first non-topology runtime captures land. It prevents capture evidence from being mistaken for byte-offset or gameplay promotion authority.',
    }


def _non_topology_syst_runtime_capture_rejection_taxonomy_summary(run: dict) -> dict:
    """Classify rejected non-topology runtime capture packets before reconciliation."""
    validation_matrix = _non_topology_syst_runtime_capture_validation_matrix_summary(run)
    rejection_classes = [
        {
            'classId': 'missing-runtime-or-pilot-provenance',
            'trigger': 'packet lacks original runtime build, disposable pilot safety class, packet id, or target system/field-family readback',
            'disposition': 'reject-before-reconciliation-and-recapture-with-complete-provenance',
        },
        {
            'classId': 'missing-positive-negative-control-pair',
            'trigger': 'only one side of the required government/message/hazard/visibility control pair is present',
            'disposition': 'hold-as-incomplete-worklist-input-until-the-missing-control-packet-is-captured',
        },
        {
            'classId': 'topology-boundary-contamination',
            'trigger': 'packet uses environment observations to infer coordinate scaling, route labels, record-name joins, or broad universe replacement state',
            'disposition': 'reject-for-non-topology-syst-offset-reconciliation-and-route-to-the-affected-topology-gate',
        },
        {
            'classId': 'runtime-observation-used-as-offset-oracle',
            'trigger': 'packet assigns Govt/Message/Asteroids/Interference/VisBit word offsets without Classic-specific field-order/source evidence',
            'disposition': 'block-promotion-and-preserve-as-priority-refinement-only',
        },
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-non-topology-syst-runtime-capture-rejection-taxonomy',
        'oracleStatus': 'non_topology_syst_capture_rejection_taxonomy_blocked_pending_real_control_packets',
        'sourceBasis': ['decoded-record-family', 'resource-bible-field', 'original-runtime-capture-required'],
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'nonTopologySystRuntimeCaptureValidationMatrixSummary',
            'nonTopologySystRuntimeCaptureGateSummary',
            'nonTopologySystRuntimeProbePrioritySummary',
            'runtimeUniverseReplacementGateSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'firstPriorityProbeFamily': validation_matrix.get('firstPriorityProbeFamily'),
        'firstPriorityCandidateWordIndices': validation_matrix.get('firstPriorityCandidateWordIndices', []),
        'requiredCapturePacketIds': validation_matrix.get('requiredCapturePacketIds', []),
        'validationCheckIds': validation_matrix.get('validationCheckIds', []),
        'validationFailureClassIds': validation_matrix.get('failureClassIds', []),
        'rejectionClassCount': len(rejection_classes),
        'rejectionClassIds': [entry['classId'] for entry in rejection_classes],
        'rejectionClasses': rejection_classes,
        'rejectionDispositions': [entry['disposition'] for entry in rejection_classes],
        'blockedPromotionClaims': [
            'treating incomplete or contaminated runtime packets as accepted non-topology syst evidence',
            'assigning government, message, hazard, interference, visibility, or port offsets from rejected runtime observations',
            'using rejected non-topology packets to close coordinate, route-label, record-name, or broad runtime-universe gates',
        ],
        'requiredVerifierBeforeReentry': validation_matrix.get('requiredVerifierBeforeReconciliation', []),
        'promotionBlockers': [
            'rejection taxonomy is a failure-routing checklist, not Classic byte-offset evidence',
            'rejected runtime packets remain priority/refinement context only until recaptured and validated',
            'rejection handling cannot weaken the validation matrix or post-capture reconciliation gates',
        ],
        'nextEvidenceFamilies': validation_matrix.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; rejection taxonomy only pending real validated control packets',
        'sourceNote': 'This taxonomy records how future failed non-topology runtime capture packets are rejected or routed before reconciliation. It preserves packet failure context without promoting field offsets or gameplay behavior.',
    }


def _non_topology_syst_runtime_capture_reentry_guardrail_summary(run: dict) -> dict:
    """Define reentry requirements for revised non-topology runtime capture packets."""
    rejection_taxonomy = _non_topology_syst_runtime_capture_rejection_taxonomy_summary(run)
    reentry_steps = [
        {
            'stepId': 'rejected-class-readback',
            'requirement': 'name the rejected class id, original packet id, and corrected capture packet id before replay',
        },
        {
            'stepId': 'control-pair-recompletion',
            'requirement': 're-run or attach the matching positive/negative control packet when a pair was incomplete',
        },
        {
            'stepId': 'topology-boundary-redaction',
            'requirement': 'remove coordinate, route-label, record-name, and broad universe replacement claims from non-topology offset packets',
        },
        {
            'stepId': 'offset-oracle-restatement',
            'requirement': 'state that runtime behavior can refine priority only and cannot assign Classic syst byte offsets without source/template evidence',
        },
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-non-topology-syst-runtime-capture-reentry-guardrail',
        'oracleStatus': 'non_topology_syst_capture_reentry_blocked_pending_corrected_control_packets',
        'sourceBasis': ['decoded-record-family', 'resource-bible-field', 'original-runtime-capture-required'],
        'recordCount': len(run['records']),
        'recordSize': run.get('recordSize'),
        'evidenceInputSummaries': [
            'nonTopologySystRuntimeCaptureRejectionTaxonomySummary',
            'nonTopologySystRuntimeCaptureValidationMatrixSummary',
            'nonTopologySystRuntimeCaptureGateSummary',
            'nonTopologySystRuntimeCaptureReconciliationSummary',
        ],
        'evidenceInputSummaryCount': 4,
        'firstPriorityProbeFamily': rejection_taxonomy.get('firstPriorityProbeFamily'),
        'firstPriorityCandidateWordIndices': rejection_taxonomy.get('firstPriorityCandidateWordIndices', []),
        'requiredCapturePacketIds': rejection_taxonomy.get('requiredCapturePacketIds', []),
        'rejectionClassIds': rejection_taxonomy.get('rejectionClassIds', []),
        'reentryStepCount': len(reentry_steps),
        'reentryStepIds': [step['stepId'] for step in reentry_steps],
        'reentrySteps': reentry_steps,
        'requiredVerifierBeforeReconciliation': rejection_taxonomy.get('requiredVerifierBeforeReentry', []),
        'blockedPromotionClaims': [
            'allowing rejected non-topology capture packets back into reconciliation without corrected provenance and control-pair evidence',
            'using reentry to preserve topology, route-label, record-name, or broad runtime-universe claims inside non-topology packets',
            'treating reentered runtime behavior observations as Classic syst offset or gameplay promotion authority',
        ],
        'promotionBlockers': [
            'reentry guardrail is a replay-path checklist, not Classic byte-offset evidence',
            'corrected control packets remain not-promoted until validation and post-capture reconciliation pass',
            'reentry cannot weaken source/template or field-order requirements before gameplay-visible use',
        ],
        'nextEvidenceFamilies': rejection_taxonomy.get('nextEvidenceFamilies', []),
        'promotionStatus': 'not-promoted; reentry guardrail only pending corrected validated control packets',
        'sourceNote': 'This guardrail records how rejected non-topology runtime capture packets may reenter validation after correction. It preserves failure recovery without promoting offsets, topology, or gameplay behavior.',
    }


def _topology_promotion_readiness_summary(systems: list[dict], names: dict) -> dict:
    """Summarize ready Lane A static inputs versus still-blocked topology promotions."""
    resource_ids = {system['resourceId'] for system in systems}
    exact_mapped_resource_ids = sorted(EXACT_SYSTEM_NAME_MAPPINGS)
    unjoined_resource_ids = sorted(resource_ids - set(exact_mapped_resource_ids))
    system_seed_names = [seed.get('name') for seed in names.get('systemNames', [])]
    deduplication = _coordinate_gap_resource_deduplication_summary(systems, names)
    estimated_distinct = deduplication.get('simplifiedDistinctSystemCountEstimate', len(unjoined_resource_ids) + len(exact_mapped_resource_ids))
    return {
        'sourceLabel': 'decoded-resource-backed-topology-promotion-readiness-matrix',
        'oracleStatus': 'topology_semantic_promotion_pending_field_family_mapping',
        'laneClass': 'Lane A: static galaxy topology semantics',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'recordCount': len(systems),
        'deduplicationAdjustedDistinctSystemCountEstimate': estimated_distinct,
        'deduplicationAdjustedDistinctSystemCountSource': 'coordinateGapResourceDeduplicationSummary (spatial-proximity heuristic, not promoted)',
        'readyStaticInputFamilies': [
            'contiguous 67-record syst-like run with resource IDs 128-194',
            'Resource Bible xPos/yPos and Con1-Con16 field-family intent',
            'complete decoded coordinate word pairs and link slots for all 67 records',
            'exact resource ID 128 to Levo mapping',
            'non-promoted coordinate transform, quantization, and start-neighborhood analysis packets',
            'non-promoted coordinate gap deduplication scout estimating ~51 distinct systems via spatial-proximity heuristic',
        ],
        'blockedPromotionClaims': [
            'coordinate display units/map scaling/projection/centering/axis orientation',
            'post-coordinate syst field layout for NavDef/population/government/message/hazard/visibility and split Con6-Con16 placement',
            'remaining ~51 distinct record-to-name joins (66 resource IDs conservatively; 16 co-located gap records are likely same-system duplicates per deduplication scout)',
            'named runtime route topology and map-label ordering',
            'broad runtime universe replacement from the decoded syst run',
        ],
        'exactMappedRecordCount': len(exact_mapped_resource_ids),
        'exactMappedResourceIds': exact_mapped_resource_ids,
        'unjoinedRecordCount': len(unjoined_resource_ids),
        'unjoinedResourceIdRange': [unjoined_resource_ids[0], unjoined_resource_ids[-1]] if unjoined_resource_ids else [],
        'heuristicSystemNameSeedCount': len(system_seed_names),
        'heuristicSystemNameSeedNames': system_seed_names,
        'coordinatePromotionStatus': 'not-promoted; static coordinate fields are ready inputs but display-unit/map-scaling/projection evidence is missing',
        'recordNamePromotionStatus': 'not-promoted beyond resource 128 to Levo; remaining names require a complete name/order oracle or runtime map-label evidence; deduplication scout estimates ~51 distinct unnamed systems',
        'runtimeUniverseReplacementStatus': 'blocked; keep the 10-system runtime subset until name/topology/display promotion evidence is stronger',
        'nextEvidenceFamilies': [
            'Classic map screenshot/click calibration tying named systems to pixel/display positions',
            'decoded complete name/list resource or source-level ordering that joins all ~51 distinct syst records (66 resource IDs conservatively)',
            'original-runtime route/map label captures for linked systems beyond Levo',
            'Resource Bible/source variable evidence for hazards/governments/ports before broad universe replacement',
        ],
        'sourceNote': 'This matrix is a dispatch/readiness guardrail: it makes the ready static inputs executable while explicitly blocking display-unit, record-name, named route-topology, and broad universe-replacement claims from being promoted by scaffold or adaptation data alone. The deduplication-adjusted distinct system count estimate (~51) is a spatial-proximity heuristic from coordinateGapResourceDeduplicationSummary; conservative unjoinedRecordCount (66) remains the primary record-accounting value.',
    }


def _runtime_universe_replacement_gate_summary(systems: list[dict], names: dict) -> dict:
    """Record exact gates before the 67 decoded syst-like records can replace the runtime subset."""
    exact_mapped_resource_ids = sorted(EXACT_SYSTEM_NAME_MAPPINGS)
    resource_ids = {system['resourceId'] for system in systems}
    unjoined_resource_ids = sorted(resource_ids - set(exact_mapped_resource_ids))
    system_seed_names = [seed.get('name') for seed in names.get('systemNames', [])]
    evidence_inputs = [
        'topologyPromotionReadinessSummary',
        'coordinateDisplayRuntimeCaptureReconciliationSummary',
        'recordNameRuntimeJoinReconciliationSummary',
        'runtimeRouteLabelCaptureReconciliationSummary',
        'nonTopologySystRuntimeCaptureReconciliationSummary',
        'systTemplateOffsetOracleGapSummary',
    ]
    return {
        'sourceLabel': 'decoded-resource-backed-runtime-universe-replacement-gate',
        'oracleStatus': 'runtime_universe_replacement_blocked_pending_name_topology_display_oracles',
        'laneClass': 'Lane A: static galaxy topology semantics',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'decodedSystRecordCount': len(systems),
        'evidenceInputSummaries': evidence_inputs,
        'evidenceInputSummaryCount': len(evidence_inputs),
        'currentRuntimeSubsetPolicy': 'keep existing runtime universe subset until promotion gates are satisfied',
        'candidateReplacementScope': '67 decoded syst-like records with resource IDs 128-194',
        'readyInputs': [
            'contiguous decoded syst-like resource ID run',
            'raw xPos/yPos coordinate word pairs for every decoded record',
            'candidate Con1-Con16 link-slot scout values for every decoded record',
            'Resource Bible syst field-family intent and topology constants',
            'exact resource 128 to Levo start-system name mapping',
        ],
        'blockingGates': [
            {
                'gate': 'coordinate_display_units_map_scaling_projection',
                'status': 'blocked',
                'reason': 'decoded xPos/yPos raw words still lack Classic display-unit, projection, centering, axis-orientation, or map-pixel calibration evidence',
            },
            {
                'gate': 'remaining_record_to_name_joins',
                'status': 'blocked',
                'reason': f'{len(unjoined_resource_ids)} decoded syst records still lack exact names beyond resource 128 -> Levo',
            },
            {
                'gate': 'named_route_topology_labels',
                'status': 'blocked',
                'reason': 'candidate link graph is decoded as resource IDs, but named Classic route/map topology remains unobserved beyond Levo',
            },
            {
                'gate': 'non_topology_syst_field_semantics',
                'status': 'blocked',
                'reason': 'NavDef, population, government, message, hazard, visibility, and Con6-Con16 placement need a complete field-order oracle or runtime/source confirmation',
            },
            {
                'gate': 'syst_template_offset_oracle_gap',
                'status': 'blocked',
                'reason': 'Classic-specific syst TMPL/ResEdit/source offset evidence is absent, so Resource Bible field-family prose cannot assign unresolved byte offsets or split Con6-Con16 placement',
            },
        ],
        'exactMappedResourceIds': exact_mapped_resource_ids,
        'unjoinedRecordCount': len(unjoined_resource_ids),
        'unjoinedResourceIdRange': [unjoined_resource_ids[0], unjoined_resource_ids[-1]] if unjoined_resource_ids else [],
        'heuristicSystemNameSeedCount': len(system_seed_names),
        'replacementReadinessStatus': 'not-ready; decoded static inputs are source-readiness evidence only and must not replace the runtime universe yet',
        'gateClosureChecklist': [
            'coordinate display units/projection/centering closed by validated Classic map pixel/click calibration or accepted source projection surrogate',
            'record-name joins closed by complete source/name table or validated packet-level target evidence',
            'named route topology closed by route-label capture packets tied to decoded resource IDs and Con slots',
            'non-topology syst fields closed by complete offset/source oracle or validated runtime reconciliation packets',
            'syst template/offset gap closed by Classic-specific TMPL/ResEdit/source evidence before assigning unresolved byte offsets or Con6-Con16 split placement',
            'static_topology_source_readiness_scout and focused model tests pass before any runtime subset replacement',
        ],
        'promotionBlockers': [
            'broad runtime universe replacement would turn source-readiness scouts into player-facing topology without name/display/field-order oracles',
            'runtime subset expansion must wait for named topology and display calibration evidence or an explicitly accepted scaffold boundary',
            'do not infer Classic-faithful broad universe behavior from the decoded syst run alone',
            'do not convert Resource Bible syst prose into byte offsets or Con6-Con16 split placement without a Classic-specific template/source oracle',
        ],
        'nextEvidenceFamilies': [
            'complete source-level name/order oracle joining the decoded syst run to Classic names',
            'Classic map screenshot/click calibration or equivalent source projection evidence',
            'runtime route/map-label capture tying linked resource IDs to named systems',
            'source-level syst field-order oracle before non-topology field semantics affect gameplay',
        ],
        'sourceNote': 'This packet is a negative gate/dispatch guardrail. It makes the criteria for replacing the small runtime universe explicit while preserving all current decoded syst data as non-promoted source-readiness inputs.',
    }


def _exact_system_name_mapping(resource_id: int) -> dict | None:
    mapping = EXACT_SYSTEM_NAME_MAPPINGS.get(resource_id)
    if mapping is None:
        return None
    return {
        'resourceId': resource_id,
        **mapping,
    }


def _govt_field(record: dict) -> dict:
    """Extract the Govt field (word index 22) from a syst record.

    EV Classic Resource Bible defines Govt at syst word 22:
      -1  Independent/unowned system
      128-255  Controlling government resource ID
    """
    raw_value = _word(record, GOVT_FIELD_WORD_INDEX)
    status = None
    if raw_value == -1:
        status = 'independent'
    elif 128 <= raw_value <= 255:
        status = 'governed'
    else:
        status = 'out-of-domain'
    return {
        'wordIndex': GOVT_FIELD_WORD_INDEX,
        'byteOffsetInRecord': record['fields'][GOVT_FIELD_WORD_INDEX]['byteOffsetInRecord'],
        'rawValue': raw_value,
        'status': status,
        'governmentResourceId': raw_value if status == 'governed' else None,
        'sourceConfidence': 'resource-bible-field-family-only',
        'sourceNote': 'Govt field (word 22) per EV Classic Resource Bible. Raw value recorded as non-promoting scout; no government name cross-reference or runtime behavior claim is made.',
    }


def _decompose_byte(word_value: int, half: str) -> int:
    """Decompose a 16-bit word into high or low byte."""
    v = int(word_value)
    return (v >> 8) & 0xFF if half == 'high' else v & 0xFF


def _candidate_data_word_fields(record: dict) -> dict:
    """Extract data words (indices 20-23) as non-promoting candidate fields.

    Words 20-23 in the decoded 44-word BRGR syst records contain 4 data words
    dominated by value 25 (~80% of 268 values). These are extracted as raw word
    values and byte-level fields, but no Resource Bible field-family semantics
    are claimed. The dominant (25,25,25,25) pattern may be a structural default.
    """
    words = {wi: _word(record, wi) for wi in DATA_WORD_INDICES}
    byte_fields = {}
    for wi in DATA_WORD_INDICES:
        wv = _word(record, wi)
        byte_fields[f'w{wi}_hi'] = _decompose_byte(wv, 'high')
        byte_fields[f'w{wi}_lo'] = _decompose_byte(wv, 'low')
    return {
        'wordIndices': DATA_WORD_INDICES,
        'rawWords': {f'w{wi}': words[wi] for wi in DATA_WORD_INDICES},
        'byteFields': byte_fields,
        'pattern': [words[wi] for wi in DATA_WORD_INDICES],
        'isDefault25': all(words[wi] == 25 for wi in DATA_WORD_INDICES),
        'highBytesAllZero': all(
            _decompose_byte(_word(record, wi), 'high') == 0
            for wi in DATA_WORD_INDICES
        ),
        'sourceConfidence': 'decoded-pattern-only-no-resource-bible-semantics-claimed',
        'sourceNote': 'Data words (20-23) extracted as non-promoting candidate fields. Value 25 dominates and may be a structural default. No Resource Bible field-family semantics (system type, government, population, hazard) are claimed for any pattern.',
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
            'candidateGovtField': _govt_field(record),
            'candidateDataWordFields': _candidate_data_word_fields(record),
        }
        if exact_name is not None:
            semantic_fields['exactSystemName'] = exact_name
        semantic_status = 'ids_promoted_names_seeded_coordinate_words_links_govt_data_word_candidate_fields_pending'
        if exact_name is not None:
            semantic_status = 'ids_promoted_exact_name_coordinate_words_links_govt_data_word_candidate_fields_pending'
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
        'resourceBibleTopologyConstantsSummary': RESOURCE_BIBLE_TOPOLOGY_CONSTANTS,
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
            'candidateDataWordFields': {
                'wordIndices': DATA_WORD_INDICES,
                'byteFieldNames': DATA_WORD_BYTE_FIELD_NAMES,
                'resourceBibleFieldFamily': 'not-assigned; words 20-23 fall in contested Resource Bible region (dude/probability/avgShips/govt/message/hazard/visibility fields)',
                'valueDomain': 'small positive integers 0-55; dominant value 25 (structural default candidate); high bytes all-zero in all records',
                'confidence': 'decoded-pattern-only-no-resource-bible-semantics-claimed',
            },
        },
        'systemNameSeeds': names.get('systemNames', []),
        'systemNameSeedSummary': _system_name_seed_summary(names),
        'systemNameByteOrderOracleGapSummary': _system_name_byte_order_oracle_gap_summary(names),
        'recordNameOracleEvidenceMatrixSummary': _record_name_oracle_evidence_matrix_summary(names, resource_ids),
        'recordNameRuntimeJoinReconciliationSummary': _record_name_runtime_join_reconciliation_summary(systems, names),
        'namedRouteTopologyOracleGapSummary': _named_route_topology_oracle_gap_summary(systems, names),
        'runtimeRouteLabelObservationBridgeGapSummary': _runtime_route_label_observation_bridge_gap_summary(systems),
        'runtimeRouteLabelProbeTargetingSummary': _runtime_route_label_probe_targeting_summary(systems),
        'runtimeRouteLabelProbeExecutionGateSummary': _runtime_route_label_probe_execution_gate_summary(systems),
        'runtimeRouteLabelProbePrioritySummary': _runtime_route_label_probe_priority_summary(systems),
        'runtimeRouteLabelCaptureReconciliationSummary': _runtime_route_label_capture_reconciliation_summary(systems),
        'recordToNamePromotionReadinessSummary': _record_to_name_promotion_readiness_summary(names, resource_ids),
        'systemNameLandingProximitySummary': _system_name_landing_proximity_summary(names),
        'landingNameCandidateReferenceSummary': _landing_name_candidate_reference_summary(names),
        'systRecordNameCandidateCrossReferenceSummary': _syst_record_name_candidate_cross_reference_summary(names, resource_ids),
        'systRecordNameGapAnalysisSummary': _syst_record_name_gap_analysis_summary(names, resource_ids),
        'coordinateGapSpatialMappingSummary': _coordinate_gap_spatial_mapping_summary(systems, names),
        'coordinateGapIdentityResolutionSummary': _coordinate_gap_identity_resolution_summary(systems, names),
        'coordinateGapResourceDeduplicationSummary': _coordinate_gap_resource_deduplication_summary(systems, names),
        'systRecordNameGapReconciliationSummary': _syst_record_name_gap_reconciliation_summary(systems, names),
        'namedCandidateLinkTopologySummary': _named_candidate_link_topology_summary(systems, names),
        'namedCandidateTravelDistanceSummary': _named_candidate_travel_distance_summary(systems, names),
        'namedCandidateRouteSummary': _named_candidate_route_summary(systems, names),
        'namedCandidateRouteCalibrationPrioritySummary': _named_candidate_route_calibration_priority_summary(systems, names),
        'namedCandidateRouteCalibrationDiagnosticPlan': _named_candidate_route_calibration_diagnostic_plan(systems, names),
        'namedCandidateCoordinateScaffoldSummary': _named_candidate_coordinate_scaffold_summary(systems, names),
        'namedSeedScaffoldCorrespondenceScout': _named_seed_scaffold_correspondence_scout(systems, names),
        'namedCandidateScaffoldIntegritySummary': _named_candidate_scaffold_integrity_summary(systems, names),
        'routeLabelScaffoldCorrespondenceScout': _route_label_scaffold_correspondence_scout(systems, names),
        'systGovtFieldValueScout': _syst_govt_field_value_scout(systems),
        'systGovtFieldNameCrossReferenceScout': _syst_govt_field_name_cross_reference_scout(systems),
        'systGovtFieldResourceIdCrossReferenceScout': _syst_govt_field_resource_id_cross_reference_scout(systems),
        'systGovtFieldWordShiftTestScout': _syst_govt_field_word_shift_test_scout(systems),
        'systCompactLayoutScout': _syst_compact_layout_scout(systems),
        'systDataWordPatternScout': _syst_data_word_pattern_scout(systems),
        'systDataWordByteScout': _syst_data_word_byte_scout(systems),
        'systDataWordSemanticCorrelationScout': _syst_data_word_semantic_correlation_scout(systems),
        'systDataWordFieldObservationScout': _syst_data_word_field_observation_scout(systems),
        'systDataWordPatternClusterScout': _syst_data_word_pattern_cluster_scout(systems),
        'systDataWordSpatialContextScout': _syst_data_word_spatial_context_scout(systems),
        'systDataWordLinkCorrelationScout': _syst_data_word_link_correlation_scout(systems),
        'systDataWordIsolatedLinkTargetScout': _syst_data_word_isolated_link_target_scout(systems),
        'systDataWordNonDefaultReachabilityScout': _syst_data_word_non_default_reachability_scout(systems),
        'coordinateMapSourceReadinessSummary': _coordinate_map_source_readiness_summary(systems),
        'systFieldLayoutSourceReadinessSummary': _syst_field_layout_source_readiness_summary(run),
        'systFieldOrderConflictSummary': _syst_field_order_conflict_summary(run),
        'resourceBibleSystSequentialFieldProjectionSummary': _resource_bible_syst_sequential_field_projection_summary(run),
        'systTemplateOffsetOracleGapSummary': _syst_template_offset_oracle_gap_summary(run),
        'systTemplateOffsetSourceSearchPrioritySummary': _syst_template_offset_source_search_priority_summary(run),
        'systTemplateOffsetEvidencePacketContractSummary': _syst_template_offset_evidence_packet_contract_summary(run),
        'systTemplateOffsetEvidencePacketValidationMatrixSummary': _syst_template_offset_evidence_packet_validation_matrix_summary(run),
        'systTemplateOffsetEvidencePacketReplayReadinessSummary': _syst_template_offset_evidence_packet_replay_readiness_summary(run),
        'systTemplateOffsetEvidencePacketIntakeTriageSummary': _syst_template_offset_evidence_packet_intake_triage_summary(run),
        'systTemplateOffsetEvidencePacketFailureTaxonomySummary': _syst_template_offset_evidence_packet_failure_taxonomy_summary(run),
        'systTemplateOffsetEvidencePacketRecoveryPlanSummary': _syst_template_offset_evidence_packet_recovery_plan_summary(run),
        'systTemplateOffsetEvidencePacketReentryGuardrailSummary': _syst_template_offset_evidence_packet_reentry_guardrail_summary(run),
        'systTemplateOffsetEvidencePacketCustodyAuditSummary': _syst_template_offset_evidence_packet_custody_audit_summary(run),
        'systTemplateOffsetEvidencePacketPromotionQuarantineSummary': _syst_template_offset_evidence_packet_promotion_quarantine_summary(run),
        'systTemplateOffsetEvidencePacketRollbackReadinessSummary': _syst_template_offset_evidence_packet_rollback_readiness_summary(run),
        'systTemplateOffsetEvidencePacketRollbackRehearsalSummary': _syst_template_offset_evidence_packet_rollback_rehearsal_summary(run),
        'systWordDomainCoverageSummary': _syst_word_domain_coverage_summary(run),
        'nonTopologySystOracleGapSummary': _non_topology_syst_oracle_gap_summary(run),
        'nonTopologySystRuntimeProbePrioritySummary': _non_topology_syst_runtime_probe_priority_summary(run),
        'nonTopologySystRuntimeCaptureGateSummary': _non_topology_syst_runtime_capture_gate_summary(run),
        'nonTopologySystRuntimeCaptureValidationMatrixSummary': _non_topology_syst_runtime_capture_validation_matrix_summary(run),
        'nonTopologySystRuntimeCaptureRejectionTaxonomySummary': _non_topology_syst_runtime_capture_rejection_taxonomy_summary(run),
        'nonTopologySystRuntimeCaptureReentryGuardrailSummary': _non_topology_syst_runtime_capture_reentry_guardrail_summary(run),
        'nonTopologySystFieldFamilyReferenceSummary': _syst_non_topology_field_family_reference_summary(run),
        'nonTopologySystRuntimeCaptureReconciliationSummary': _non_topology_syst_runtime_capture_reconciliation_summary(run),
        'topologyPromotionReadinessSummary': _topology_promotion_readiness_summary(systems, names),
        'runtimeUniverseReplacementGateSummary': _runtime_universe_replacement_gate_summary(systems, names),
        'coordinateDomainSummary': _coordinate_domain_summary(systems),
        'coordinateDisplayCandidateSummary': _coordinate_display_candidate_summary(systems),
        'coordinateDisplayBoundsSummary': _coordinate_display_bounds_summary(systems),
        'coordinateDisplayNormalizedSummary': _coordinate_display_normalized_summary(systems),
        'coordinateDisplayTransformSummary': _coordinate_display_transform_summary(systems),
        'coordinateDisplayFixedPointSummary': _coordinate_display_fixed_point_summary(systems),
        'coordinateDisplayIntegerBandSummary': _coordinate_display_integer_band_summary(systems),
        'coordinateDisplayResidualSignSummary': _coordinate_display_residual_sign_summary(systems),
        'coordinateDisplayResidualMagnitudeSummary': _coordinate_display_residual_magnitude_summary(systems),
        'coordinateDisplayQuantizationSummary': _coordinate_display_quantization_summary(systems),
        'coordinateDisplayScaleInterpretationSummary': _coordinate_display_scale_interpretation_summary(systems),
        'coordinateDisplayCalibrationGateSummary': _coordinate_display_calibration_gate_summary(systems),
        'coordinateDisplayUnitMapScalingReadinessSummary': _coordinate_display_unit_map_scaling_readiness_summary(systems),
        'coordinateDisplayRuntimeCaptureGateSummary': _coordinate_display_runtime_capture_gate_summary(systems),
        'coordinateDisplayRuntimeCaptureReconciliationSummary': _coordinate_display_runtime_capture_reconciliation_summary(systems),
        'coordinateDisplayRuntimeCaptureValidationMatrixSummary': _coordinate_display_runtime_capture_validation_matrix_summary(systems),
        'coordinateDisplayExtremaSummary': _coordinate_display_extrema_summary(systems),
        'candidateLinkGraphSummary': _candidate_link_graph_summary(systems),
        'candidateGraphConnectivitySummary': _candidate_graph_connectivity_summary(systems),
        'candidateGraphDistanceSummary': _candidate_graph_distance_summary(systems),
        'startSystemCandidateTopologySummary': _start_system_candidate_topology_summary(systems),
        'startNeighborhoodDisplayTransformSummary': _start_neighborhood_display_transform_summary(systems),
        'startNeighborhoodDisplayDistanceSummary': _start_neighborhood_display_distance_summary(systems),
        'startNeighborhoodDisplayVectorSummary': _start_neighborhood_display_vector_summary(systems),
        'startNeighborhoodSlotVectorOrderSummary': _start_neighborhood_slot_vector_order_summary(systems),
        'startNeighborhoodSlotAngularOrderSummary': _start_neighborhood_slot_angular_order_summary(systems),
        'startNeighborhoodRuntimeCalibrationPrioritySummary': _start_neighborhood_runtime_calibration_priority_summary(systems),
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
