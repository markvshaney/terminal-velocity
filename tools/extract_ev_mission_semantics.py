#!/usr/bin/env python3
"""Derive Classic Resource Bible-backed mission semantics from sourced EV structures."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_SOURCE = Path('native_ev/data/sourced_ev_structures.json')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_missions.json')
METHOD = 'ev-classic-resource-bible-misn-field-map-v2'

# Field order follows the EV Classic Resource Bible mïsn definitions through
# the late-added Flags word. Desc fields are resource IDs/pointers; keep them
# compactly decoded as selectors rather than trying to expand proprietary text.
FIELD_INDEX = {
    'availStel': 0,
    'availBitSet': 1,
    'availLoc': 2,
    'availRecord': 3,
    'availRating': 4,
    'availRandom': 5,
    'travelStel': 6,
    'returnStel': 7,
    'cargoType': 8,
    'cargoQuantity': 9,
    'pickupMode': 10,
    'dropOffMode': 11,
    'scanGovernment': 12,
    'failIfScanned': 13,
    'unknownFieldBeforePayValue': 14,
    'payValue': 15,
    'shipCount': 16,
    'shipSystem': 17,
    'shipDude': 18,
    'shipGoal': 19,
    'shipBehavior': 20,
    'shipNameId': 21,
    'completionBitSet': 22,
    'completionGovernment': 23,
    'completionReward': 24,
    'failureBitSet': 25,
    'briefText': 26,
    'quickBrief': 27,
    'loadCargoText': 28,
    'dumpCargoText': 29,
    'completionText': 30,
    'failureText': 31,
    'timeLimit': 32,
    'canAbort': 33,
    'unusedAfterCanAbort': 34,
    'availBitClear': 35,
    'auxShipCount': 36,
    'auxShipDude': 37,
    'auxShipSystem': 38,
    'completionBitSet2': 39,
    'flags': 40,
}

AVAIL_LOC = {
    0: 'missionComputer',
    1: 'bar',
    2: 'missionComputerAndBar',
}

MISSION_FLAGS = {
    0x0001: 'autoAbortAfterAccept',
    0x0002: 'hideRedDestinationArrowsOnMap',
    0x0004: 'cannotRefuse',
    0x0010: 'infiniteAuxShips',
    0x0020: 'removePrepaidOutfitOnFailureOrAbort',
    0x0040: 'applyFiveTimesCompletionRewardReversalOnAbort',
    0x0080: 'globalPenaltyWhenJettisoningMissionCargoIgnored',
    0x0100: 'showGreenArrowOnMapInInitialBriefing',
    0x1000: 'criticalMissionOfferedBeforeOthersInBar',
}


def _word(record: dict, index: int) -> int:
    return int(record['fields'][index]['value'])


def _stel_selector(value: int) -> dict:
    if value == -1:
        return {'kind': 'anyInhabitedStellar'}
    if value == -2:
        return {'kind': 'randomInhabitedStellar'}
    if value == -3:
        return {'kind': 'randomUninhabitedStellar'}
    if value == -4:
        return {'kind': 'initialStellar'}
    if 128 <= value <= 1627:
        return {'kind': 'specificStellar', 'resourceId': value}
    if 5000 <= value <= 5999:
        return {'kind': 'adjacentToSystem', 'systemIndex': value - 5000}
    if 9999 <= value <= 10127:
        return {'kind': 'specificGovernmentStellar', 'governmentIndex': value - 9999}
    if 15000 <= value <= 15127:
        return {'kind': 'governmentAllyStellar', 'governmentIndex': value - 15000}
    if 20000 <= value <= 20127:
        return {'kind': 'notGovernmentStellar', 'governmentIndex': value - 20000}
    if 25000 <= value <= 25127:
        return {'kind': 'governmentEnemyStellar', 'governmentIndex': value - 25000}
    return {'kind': 'raw', 'value': value}


def _bit_selector(value: int) -> dict:
    if value == -1:
        return {'kind': 'ignored'}
    if 0 <= value <= 255:
        return {'kind': 'mustBeSet', 'bit': value}
    if 1000 <= value <= 1255:
        return {'kind': 'mustBeClear', 'bit': value - 1000}
    return {'kind': 'raw', 'value': value}


def _bit_clear_selector(value: int) -> dict:
    if value == -1:
        return {'kind': 'ignored'}
    if 0 <= value <= 255:
        return {'kind': 'mustBeClear', 'bit': value}
    return {'kind': 'raw', 'value': value}


def _record_requirement(value: int) -> dict:
    if value == 0:
        return {'kind': 'ignored'}
    if value == -32000:
        return {'kind': 'dominatedCurrentStellar'}
    if value == -32001:
        return {'kind': 'dominatedAnyStellar'}
    return {'kind': 'minimumLegalRecord', 'value': value}


def _cargo_type(value: int) -> dict:
    if value == -1:
        return {'kind': 'none'}
    if 0 <= value <= 63:
        return {'kind': 'specificCargoType', 'cargoType': value}
    if value == 1000:
        return {'kind': 'randomStandardCargo'}
    return {'kind': 'raw', 'value': value}


def _cargo_quantity(value: int) -> dict:
    if value == -1:
        return {'kind': 'ignored'}
    if value >= 0:
        return {'kind': 'fixedTons', 'tons': value}
    return {'kind': 'variableTonsPlusMinusHalf', 'baseTons': abs(value)}


def _scan_government(value: int) -> dict:
    if value == -1:
        return {'kind': 'ignored'}
    if 128 <= value <= 255:
        return {'kind': 'specificGovernmentCargoIllegal', 'governmentId': value}
    return {'kind': 'raw', 'value': value}


def _pay_value(value: int) -> dict:
    if value == 0:
        return {'kind': 'noPay'}
    if value > 0:
        return {'kind': 'credits', 'credits': value}
    if -10255 <= value <= -10128:
        return {'kind': 'cleanLegalRecord', 'governmentId': abs(value) - 10000}
    if -20255 <= value <= -20128:
        return {'kind': 'grantOutfitOnCompletion', 'outfitId': abs(value) - 20000}
    if -30255 <= value <= -30128:
        return {'kind': 'grantOutfitAtStart', 'outfitId': abs(value) - 30000}
    return {'kind': 'raw', 'value': value}


def _desc_selector(value: int) -> dict:
    if value == -1:
        return {'kind': 'none'}
    if value >= 128:
        return {'kind': 'descResource', 'resourceId': value}
    return {'kind': 'raw', 'value': value}


def _time_limit(value: int) -> dict:
    if value == -1:
        return {'kind': 'none'}
    if value >= 1:
        return {'kind': 'days', 'days': value}
    return {'kind': 'raw', 'value': value}


def _can_abort(value: int) -> dict:
    return {
        'raw': value,
        'canAbort': value != 0,
        'sourceNote': 'CanAbort 0 requires ReturnStel cleanup; nonzero can be aborted and failed missions go inactive',
    }


def _mission_flags(value: int) -> dict:
    unsigned = value & 0xffff
    known_mask = 0
    for bit in MISSION_FLAGS:
        known_mask |= bit
    return {
        'rawSigned': value,
        'rawUnsigned': unsigned,
        'flagNames': [name for bit, name in MISSION_FLAGS.items() if unsigned & bit],
        'unknownMask': unsigned & ~known_mask,
    }


def _dude_selector(value: int) -> dict:
    if value == -1:
        return {'kind': 'ignored'}
    if 128 <= value <= 255:
        return {'kind': 'specificDude', 'dudeId': value}
    return {'kind': 'raw', 'value': value}


def _ship_count(value: int) -> dict:
    if value == -1:
        return {'kind': 'ignored'}
    if 0 <= value <= 31:
        return {'kind': 'count', 'count': value}
    return {'kind': 'raw', 'value': value}


def _ship_goal(value: int) -> dict:
    names = {
        -1: 'ignored',
        0: 'destroyAll',
        1: 'disableDontDestroy',
        2: 'board',
        3: 'escort',
        4: 'observe',
        5: 'rescue',
        6: 'chaseOff',
    }
    return {'kind': names.get(value, 'raw'), **({} if value in names else {'value': value})}


def _ship_behavior(value: int) -> dict:
    names = {
        -1: 'standardAI',
        0: 'alwaysAttackPlayer',
        1: 'protectPlayer',
        9: 'hyperInTogetherAfterDelay',
        10: 'hyperInAndAttackPlayer',
        11: 'hyperInAndProtectPlayer',
    }
    return {'kind': names.get(value, 'raw'), **({} if value in names else {'value': value})}


def _ship_system_selector(value: int) -> dict:
    if value == -1:
        return {'kind': 'initialSystem'}
    if value == -2:
        return {'kind': 'anyRandomSystem'}
    if value == -3:
        return {'kind': 'travelStelSystem'}
    if value == -4:
        return {'kind': 'returnStelSystem'}
    if value == -5:
        return {'kind': 'adjacentToInitialSystem'}
    if value == -6:
        return {'kind': 'currentPlayerSystem'}
    if 128 <= value <= 1127:
        return {'kind': 'specificSystem', 'systemId': value}
    if 9999 <= value <= 10127:
        return {'kind': 'specificGovernmentSystem', 'governmentIndex': value - 9999}
    if 15000 <= value <= 15127:
        return {'kind': 'governmentAllySystem', 'governmentIndex': value - 15000}
    if 20000 <= value <= 20127:
        return {'kind': 'notGovernmentSystem', 'governmentIndex': value - 20000}
    if 25000 <= value <= 25127:
        return {'kind': 'governmentEnemySystem', 'governmentIndex': value - 25000}
    return {'kind': 'raw', 'value': value}


def _completion_government(value: int) -> dict:
    if value == -1:
        return {'kind': 'ignored'}
    if 0 <= value <= 127:
        return {'kind': 'governmentIndex', 'governmentIndex': value, 'governmentId': value + 128}
    if 128 <= value <= 255:
        return {'kind': 'governmentId', 'governmentId': value, 'governmentIndex': value - 128}
    return {'kind': 'raw', 'value': value}


def derive(source: Path) -> dict:
    data = json.loads(source.read_text())
    run = next(run for run in data['runs'] if run.get('candidateType') == 'mission-like' and run.get('recordSize') == 1970)
    missions = []
    for record in run['records']:
        raw = {name: _word(record, index) for name, index in FIELD_INDEX.items()}
        missions.append({
            'resourceId': 128 + int(record['ordinal']),
            'ordinal': int(record['ordinal']),
            'chunkIndex': int(record['chunkIndex']),
            'byteOffset': int(record['byteOffset']),
            'fieldSource': 'EV Classic Resource Bible mïsn fields through Flags, lines 249-519 of extracted text',
            'rawFields': raw,
            'semanticFields': {
                'availability': {
                    'stellar': _stel_selector(raw['availStel']),
                    'missionBitSet': _bit_selector(raw['availBitSet']),
                    'missionBitClear': _bit_clear_selector(raw['availBitClear']),
                    'location': AVAIL_LOC.get(raw['availLoc'], 'raw:%s' % raw['availLoc']),
                    'legalRecord': _record_requirement(raw['availRecord']),
                    'combatRatingMinimum': None if raw['availRating'] == -1 else raw['availRating'],
                    'randomPercent': raw['availRandom'],
                },
                'travel': {
                    'destination': _stel_selector(raw['travelStel']),
                    'return': _stel_selector(raw['returnStel']),
                },
                'cargo': {
                    'type': _cargo_type(raw['cargoType']),
                    'quantity': _cargo_quantity(raw['cargoQuantity']),
                    'pickupMode': raw['pickupMode'],
                    'dropOffMode': raw['dropOffMode'],
                    'scanGovernment': _scan_government(raw['scanGovernment']),
                    'failIfScanned': raw['failIfScanned'] != 0,
                },
                'reward': _pay_value(raw['payValue']),
                'specialShips': {
                    'count': _ship_count(raw['shipCount']),
                    'system': _ship_system_selector(raw['shipSystem']),
                    'dude': _dude_selector(raw['shipDude']),
                    'goal': _ship_goal(raw['shipGoal']),
                    'behavior': _ship_behavior(raw['shipBehavior']),
                    'nameId': None if raw['shipNameId'] == -1 else raw['shipNameId'],
                },
                'auxiliaryShips': {
                    'count': _ship_count(raw['auxShipCount']),
                    'system': _ship_system_selector(raw['auxShipSystem']),
                    'dude': _dude_selector(raw['auxShipDude']),
                },
                'completion': {
                    'bitSet': _bit_selector(raw['completionBitSet']),
                    'bitSet2': _bit_selector(raw['completionBitSet2']),
                    'government': _completion_government(raw['completionGovernment']),
                    'reward': raw['completionReward'],
                    'failureRecordPenalty': -int(raw['completionReward'] / 2) if raw['completionGovernment'] != -1 else 0,
                    'failureBitSet': _bit_selector(raw['failureBitSet']),
                },
                'descriptions': {
                    'briefText': _desc_selector(raw['briefText']),
                    'quickBrief': _desc_selector(raw['quickBrief']),
                    'loadCargoText': _desc_selector(raw['loadCargoText']),
                    'dumpCargoText': _desc_selector(raw['dumpCargoText']),
                    'completionText': _desc_selector(raw['completionText']),
                    'failureText': _desc_selector(raw['failureText']),
                    'wildcardSourceNote': 'Resource Bible supports <DSY>, <DST>, <RSY>, <RST>, <CT>, <CQ>, <DL>, <PN>, <PSN>, <OSN>, and <SN> substitution in mission desc text',
                },
                'lifecycle': {
                    'timeLimit': _time_limit(raw['timeLimit']),
                    'canAbort': _can_abort(raw['canAbort']),
                    'flags': _mission_flags(raw['flags']),
                },
            },
        })
    return {
        'schemaVersion': 1,
        'sourceFile': data['sourceFile'],
        'sourceSha256': data['sourceSha256'],
        'sourceManifest': str(source),
        'method': METHOD,
        'sourceBasis': 'EV Classic Resource Bible mïsn field definitions through Flags plus local primitive BRGR structure decode',
        'recordRun': {'candidateType': run['candidateType'], 'recordSize': run['recordSize'], 'count': run['count'], 'confidence': 'manual-backed-field-map-through-flags'},
        'fieldIndex': FIELD_INDEX,
        'missions': missions,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('source', nargs='?', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--out', type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    manifest = derive(args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f"wrote {args.out} missions={len(manifest['missions'])} method={METHOD}")


if __name__ == '__main__':
    main()
