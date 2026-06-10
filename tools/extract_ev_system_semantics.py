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
DEFAULT_OUT = Path('native_ev/data/sourced_ev_systems.json')
METHOD = 'ev-classic-static-system-id-name-seed-resource-bible-topology-constants-coordinate-map-source-readiness-system-name-byte-order-oracle-gap-non-topology-syst-oracle-gap-resource-bible-syst-sequential-field-projection-field-count-budget-named-route-topology-oracle-gap-record-name-oracle-evidence-matrix-record-name-promotion-readiness-landing-proximity-runtime-universe-replacement-gate-coordinate-display-calibration-gate-syst-word-domain-coverage-syst-field-order-conflict-syst-field-layout-source-readiness-coordinate-link-slot-coordinate-display-scale-interpretation-coordinate-display-quantization-coordinate-display-residual-magnitude-coordinate-display-residual-sign-coordinate-display-integer-band-coordinate-display-fixed-point-start-neighborhood-slot-angular-order-start-neighborhood-slot-vector-order-start-neighborhood-display-vector-start-neighborhood-display-distance-start-neighborhood-display-transform-normalized-extrema-link-graph-distance-name-seed-summary-levo-name-map-v42'
SOURCE_BASIS = 'EV Classic Resource Bible game constants, syst xPos/yPos and Con1-Con16 field-family definitions plus local primitive BRGR syst-like structure decode, heuristic EV Data.rez system/landing-name seed list, Resource Bible system ID #128 start-system rule, and original-runtime-observed starting system Levo'
PROMOTION_BOUNDARY = 'IDs/resource ordering, Resource Bible topology constants (MaxStellarObjects 1500, MaxSystems 1000, JumpDistance 1000 pixels) as static-source constants only, coordinate map source-readiness evidence requirements, topology promotion readiness matrix, runtime universe replacement gate matrix, coordinate display calibration gate matrix, named route topology oracle gap matrix, record-name oracle evidence matrix, heuristic name seeds, exact resource ID 128 to Levo system-name mapping, non-promoted record-to-name promotion-readiness blockers, raw xPos/yPos coordinate word pairs, coordinate word-domain summary, non-promoted display interpretation candidates, non-promoted display bounds/extrema candidates, non-promoted signed-long min-normalized coordinate candidates, non-promoted axis-transform/aspect-ratio candidates, non-promoted 16.16 fixed-point display-scale candidates, non-promoted coordinate integer-band/fractional residual candidates, non-promoted coordinate residual-sign/fraction-distribution candidates, non-promoted coordinate residual-magnitude/fractional-absolute candidates, non-promoted coordinate residual quantization/grid-step candidates, non-promoted coordinate scale-interpretation blocker/comparison candidates, non-promoted Resource Bible/current-decoder syst field-order conflict matrix, signed 32-bit big-endian raw-long coordinate candidates, Con1-Con16 link slot names, raw link values, in-run target resource/ordinal cross-links, candidate link-graph summary statistics, candidate link reciprocity/self-link statistics, candidate graph connectivity/reachability statistics, candidate graph distance/hop statistics, non-promoted resource 128 start-neighborhood topology analysis, non-promoted start-neighborhood display-transform analysis, non-promoted start-neighborhood display-distance analysis, non-promoted start-neighborhood display-vector/quadrant analysis, non-promoted start-neighborhood link-slot/display-vector order analysis, non-promoted start-neighborhood slot/angular order analysis, and source provenance are promoted; coordinate display units/map scaling/projection, remaining exact system names, named route topology, services, hazards, governments, ports, and broad runtime universe replacement are explicitly not promoted yet'
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
        'resourceBibleSequentialFieldFamilies': [
            {'fieldFamily': 'xPos/yPos map coordinates', 'sourceFieldCount': 2, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 931-932'},
            {'fieldFamily': 'Con1-Con5 front hyperspace links', 'sourceFieldCount': 5, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 933-937'},
            {'fieldFamily': 'NavDef F1-F4 navigation defaults', 'sourceFieldCount': 4, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 938-945'},
            {'fieldFamily': 'DudeTypes/%Prob/AvgShips population controls', 'sourceFieldCount': 9, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 946-959'},
            {'fieldFamily': 'Govt/Message/Asteroids/Interference/VisBit environment and visibility controls', 'sourceFieldCount': 5, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 961-984'},
            {'fieldFamily': 'Con6-Con16 additional hyperspace links', 'sourceFieldCount': 11, 'sourceReference': 'docs/references/ev-family/ev-classic-resource-bible.txt lines 985-989'},
        ],
        'sourceFieldCountTotal': 36,
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


def _topology_promotion_readiness_summary(systems: list[dict], names: dict) -> dict:
    """Summarize ready Lane A static inputs versus still-blocked topology promotions."""
    resource_ids = {system['resourceId'] for system in systems}
    exact_mapped_resource_ids = sorted(EXACT_SYSTEM_NAME_MAPPINGS)
    unjoined_resource_ids = sorted(resource_ids - set(exact_mapped_resource_ids))
    system_seed_names = [seed.get('name') for seed in names.get('systemNames', [])]
    return {
        'sourceLabel': 'decoded-resource-backed-topology-promotion-readiness-matrix',
        'oracleStatus': 'topology_semantic_promotion_pending_field_family_mapping',
        'laneClass': 'Lane A: static galaxy topology semantics',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'recordCount': len(systems),
        'readyStaticInputFamilies': [
            'contiguous 67-record syst-like run with resource IDs 128-194',
            'Resource Bible xPos/yPos and Con1-Con16 field-family intent',
            'complete decoded coordinate word pairs and link slots for all 67 records',
            'exact resource ID 128 to Levo mapping',
            'non-promoted coordinate transform, quantization, and start-neighborhood analysis packets',
        ],
        'blockedPromotionClaims': [
            'coordinate display units/map scaling/projection/centering/axis orientation',
            'post-coordinate syst field layout for NavDef/population/government/message/hazard/visibility and split Con6-Con16 placement',
            'remaining 66 exact record-to-name joins',
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
        'recordNamePromotionStatus': 'not-promoted beyond resource 128 to Levo; remaining names require a complete name/order oracle or runtime map-label evidence',
        'runtimeUniverseReplacementStatus': 'blocked; keep the 10-system runtime subset until name/topology/display promotion evidence is stronger',
        'nextEvidenceFamilies': [
            'Classic map screenshot/click calibration tying named systems to pixel/display positions',
            'decoded complete name/list resource or source-level ordering that joins all 67 syst records',
            'original-runtime route/map label captures for linked systems beyond Levo',
            'Resource Bible/source variable evidence for hazards/governments/ports before broad universe replacement',
        ],
        'sourceNote': 'This matrix is a dispatch/readiness guardrail: it makes the ready static inputs executable while explicitly blocking display-unit, record-name, named route-topology, and broad universe-replacement claims from being promoted by scaffold or adaptation data alone.',
    }


def _runtime_universe_replacement_gate_summary(systems: list[dict], names: dict) -> dict:
    """Record exact gates before the 67 decoded syst-like records can replace the runtime subset."""
    exact_mapped_resource_ids = sorted(EXACT_SYSTEM_NAME_MAPPINGS)
    resource_ids = {system['resourceId'] for system in systems}
    unjoined_resource_ids = sorted(resource_ids - set(exact_mapped_resource_ids))
    system_seed_names = [seed.get('name') for seed in names.get('systemNames', [])]
    return {
        'sourceLabel': 'decoded-resource-backed-runtime-universe-replacement-gate',
        'oracleStatus': 'runtime_universe_replacement_blocked_pending_name_topology_display_oracles',
        'laneClass': 'Lane A: static galaxy topology semantics',
        'sourceBasis': ['decoded-record-family', 'decoded-original-variable', 'resource-bible-field'],
        'decodedSystRecordCount': len(systems),
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
        ],
        'exactMappedResourceIds': exact_mapped_resource_ids,
        'unjoinedRecordCount': len(unjoined_resource_ids),
        'unjoinedResourceIdRange': [unjoined_resource_ids[0], unjoined_resource_ids[-1]] if unjoined_resource_ids else [],
        'heuristicSystemNameSeedCount': len(system_seed_names),
        'replacementReadinessStatus': 'not-ready; decoded static inputs are source-readiness evidence only and must not replace the runtime universe yet',
        'promotionBlockers': [
            'broad runtime universe replacement would turn source-readiness scouts into player-facing topology without name/display/field-order oracles',
            'runtime subset expansion must wait for named topology and display calibration evidence or an explicitly accepted scaffold boundary',
            'do not infer Classic-faithful broad universe behavior from the decoded syst run alone',
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
        },
        'systemNameSeeds': names.get('systemNames', []),
        'systemNameSeedSummary': _system_name_seed_summary(names),
        'systemNameByteOrderOracleGapSummary': _system_name_byte_order_oracle_gap_summary(names),
        'recordNameOracleEvidenceMatrixSummary': _record_name_oracle_evidence_matrix_summary(names, resource_ids),
        'namedRouteTopologyOracleGapSummary': _named_route_topology_oracle_gap_summary(systems, names),
        'recordToNamePromotionReadinessSummary': _record_to_name_promotion_readiness_summary(names, resource_ids),
        'systemNameLandingProximitySummary': _system_name_landing_proximity_summary(names),
        'coordinateMapSourceReadinessSummary': _coordinate_map_source_readiness_summary(systems),
        'systFieldLayoutSourceReadinessSummary': _syst_field_layout_source_readiness_summary(run),
        'systFieldOrderConflictSummary': _syst_field_order_conflict_summary(run),
        'resourceBibleSystSequentialFieldProjectionSummary': _resource_bible_syst_sequential_field_projection_summary(run),
        'systWordDomainCoverageSummary': _syst_word_domain_coverage_summary(run),
        'nonTopologySystOracleGapSummary': _non_topology_syst_oracle_gap_summary(run),
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
