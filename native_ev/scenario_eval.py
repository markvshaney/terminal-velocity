"""Small symbolic gameplay scenario/eval harness for Terminal Velocity.

This is a Terminal Velocity automation scaffold, not an EV Classic fidelity claim.
It gives automated controllers a cheap, repeatable state/action/evaluator loop before
we spend more effort on fragile long-running Basilisk observation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from native_ev.model import (
    available_mission_ids,
    clemency_offer,
    economy_manifest,
    enforcement_outcome,
    government_manifest,
    load_universe,
    mission_manifest,
    outfit_manifest,
    reputation_manifest,
    ship_manifest,
    station_inventory,
    weapon_manifest,
    system_distance,
)

COMMODITY_LOT_SIZE = 10
STARTING_CREDITS = 10000
STARTING_CARGO_CAPACITY = 20
STARTING_FUEL = 6
START_SYSTEM = 'Levo'
START_BODY = 'Levo Spaceport'
MIN_JUMP_DISTANCE = 450
SCENARIO_CURRICULUM = [
    'levo_merchant_first_hop',
    'levo_same_port_sellback_loop',
    'commodity_sell_blocked_recovery_loop',
    'commodity_buy_blocked_recovery_loop',
    'cross_market_trade_spread_scout',
    'max_hold_trade_route_scout',
    'trade_route_refuel_profit_loop',
    'mission_runner_first_delivery',
    'scan_intro_mission_offers',
    'intro_courier_mission_delivery',
    'chapter_one_courier_chain',
    'alignment_choice_guardrail',
    'federation_alignment_delivery_loop',
    'mission_destination_route_hint',
    'mission_trade_hybrid_capacity_planning',
    'mission_trade_refuel_delivery_loop',
    'mission_trade_destination_sale_loop',
    'chapter_one_trade_carryover_loop',
    'mission_trade_return_margin_guardrail',
    'mission_abort_releases_reserved_cargo',
    'mission_abort_reaccept_delivery_loop',
    'mission_deadline_failure_scaffold',
    'outfitter_ship_ladder_intro',
    'repair_service_recovery_loop',
    'disabled_player_recovery_loop',
    'system_service_provisioning_scout',
    'shift_click_multi_stop_route_queue',
    'route_queue_invalid_stop_guardrail',
    'route_queue_clear_guardrail',
    'route_queue_clear_reselect_guardrail',
    'near_center_jump_block',
    'route_planner_refuel_loop',
    'low_fuel_jump_recovery',
    'blocked_reason_curriculum',
    'contraband_scan_clemency_recovery',
    'pirate_avoidance_escape_route',
    'disposable_combat_placeholder',
]


def available_scenarios() -> list[str]:
    """Return the symbolic gameplay curriculum in intended execution order."""
    return list(SCENARIO_CURRICULUM)


def _system(universe: dict[str, Any], name: str) -> dict[str, Any]:
    for system in universe.get('systems', []):
        if system.get('name') == name:
            return system
    raise ValueError(f'unknown system {name}')


def _body(universe: dict[str, Any], system_name: str, body_name: str) -> dict[str, Any]:
    system = _system(universe, system_name)
    for body in system.get('bodies', []):
        if body.get('name') == body_name:
            return body
    raise ValueError(f'unknown body {system_name}/{body_name}')


def initial_gameplay_state() -> dict[str, Any]:
    """Return a structured new-pilot state for scripted symbolic scenarios."""
    universe = load_universe()
    known_systems = sorted({START_SYSTEM, *_system(universe, START_SYSTEM).get('links', [])})
    return {
        'currentSystem': START_SYSTEM,
        'landedBody': START_BODY,
        'credits': STARTING_CREDITS,
        'cargoCapacity': STARTING_CARGO_CAPACITY,
        'cargoUsed': 0,
        'cargoHold': {},
        'activeJobs': [],
        'completedJobs': [],
        'storyFlags': [],
        'missionOfferArchive': {},
        'routeQueue': [],
        'routeSourceLabel': None,
        'reputation': {'Federation': 5, 'Independent': 7},
        'legalRecords': {'Federation': 0, 'Independent': 0},
        'fuel': STARTING_FUEL,
        'currentDay': 0,
        'combatExecuted': False,
        'threatPosture': 'clear',
        'strictPlay': False,
        'knownSystems': known_systems,
        'playerShipId': 'shuttlecraft',
        'ownedOutfits': {},
        'ownedWeapons': {},
        'maxHull': 100,
        'currentHull': 100,
        'playerDisabled': False,
        'maxFuel': STARTING_FUEL,
        'distanceFromSystemCenter': MIN_JUMP_DISTANCE + 50,
    }


def _buy_commodity_lot(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    commodity = action['commodity']
    system_name = state['currentSystem']
    economy = economy_manifest()
    price = int(economy['markets'][system_name][commodity]['buy'])
    total = price * COMMODITY_LOT_SIZE
    source_label = action.get('sourceLabel', 'terminal-velocity-trade-scaffold')
    oracle_status = action.get('oracleStatus', 'commodity_buy_guardrail_pending_original_runtime_trace')
    if state['landedBody'] is None:
        trace.append({'type': 'blocked_buy_commodity_lot', 'reason': 'not landed', 'commodity': commodity, 'sourceLabel': source_label, 'oracleStatus': oracle_status})
        return False
    if state['cargoUsed'] + COMMODITY_LOT_SIZE > state['cargoCapacity']:
        trace.append({'type': 'blocked_buy_commodity_lot', 'reason': 'insufficient cargo space', 'commodity': commodity, 'sourceLabel': source_label, 'oracleStatus': oracle_status})
        return False
    if state['credits'] < total:
        trace.append({'type': 'blocked_buy_commodity_lot', 'reason': 'insufficient credits', 'commodity': commodity, 'sourceLabel': source_label, 'oracleStatus': oracle_status})
        return False
    state['credits'] -= total
    state['cargoUsed'] += COMMODITY_LOT_SIZE
    state['cargoHold'][commodity] = int(state['cargoHold'].get(commodity, 0)) + COMMODITY_LOT_SIZE
    trace.append({
        'type': 'buy_commodity_lot',
        'system': system_name,
        'body': state['landedBody'],
        'commodity': commodity,
        'tons': COMMODITY_LOT_SIZE,
        'unitPrice': price,
        'creditsAfter': state['credits'],
        'cargoUsed': state['cargoUsed'],
        'sourceLabel': source_label,
        'oracleStatus': oracle_status,
    })
    return True


def _sell_commodity_lot(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    commodity = action['commodity']
    system_name = state['currentSystem']
    economy = economy_manifest()
    price = int(economy['markets'][system_name][commodity]['sell'])
    held = int(state['cargoHold'].get(commodity, 0))
    source_label = action.get('sourceLabel', 'terminal-velocity-trade-scaffold')
    oracle_status = action.get('oracleStatus', 'commodity_sell_guardrail_pending_original_runtime_trace')
    if state['landedBody'] is None:
        trace.append({'type': 'blocked_sell_commodity_lot', 'reason': 'not landed', 'commodity': commodity, 'held': held, 'sourceLabel': source_label, 'oracleStatus': oracle_status})
        return False
    if held < COMMODITY_LOT_SIZE:
        trace.append({'type': 'blocked_sell_commodity_lot', 'reason': 'insufficient commodity in hold', 'commodity': commodity, 'held': held, 'sourceLabel': source_label, 'oracleStatus': oracle_status})
        return False
    state['credits'] += price * COMMODITY_LOT_SIZE
    state['cargoUsed'] = max(0, int(state['cargoUsed']) - COMMODITY_LOT_SIZE)
    remaining = held - COMMODITY_LOT_SIZE
    if remaining:
        state['cargoHold'][commodity] = remaining
    else:
        state['cargoHold'].pop(commodity, None)
    trace.append({
        'type': 'sell_commodity_lot',
        'system': system_name,
        'body': state['landedBody'],
        'commodity': commodity,
        'tons': COMMODITY_LOT_SIZE,
        'unitPrice': price,
        'creditsAfter': state['credits'],
        'cargoUsed': state['cargoUsed'],
        'sourceLabel': source_label,
        'oracleStatus': action.get('oracleStatus', 'same_port_sellback_pending_original_runtime_trace'),
    })
    return True


def _evaluate_trade_margin(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    commodity = str(action['commodity'])
    origin = str(action.get('originSystem', state['currentSystem']))
    destination = str(action['destinationSystem'])
    economy = economy_manifest()
    buy_price = int(economy['markets'][origin][commodity]['buy'])
    sell_price = int(economy['markets'][destination][commodity]['sell'])
    margin = sell_price - buy_price
    decision = 'carry' if margin > 0 else 'skip'
    trace.append({
        'type': 'trade_margin_decision',
        'commodity': commodity,
        'originSystem': origin,
        'destinationSystem': destination,
        'buyPrice': buy_price,
        'sellPrice': sell_price,
        'marginPerTon': margin,
        'decision': decision,
        'reason': 'positive margin' if margin > 0 else 'non-positive margin',
        'sourceLabel': action.get('sourceLabel', 'terminal-velocity-trade-margin-scaffold'),
        'oracleStatus': action.get('oracleStatus', 'trade_margin_pending_classic_runtime_trace'),
    })
    return True


def _route_tail_system(state: dict[str, Any]) -> str:
    route_queue = state.get('routeQueue', [])
    if route_queue:
        return str(route_queue[-1])
    return str(state['currentSystem'])


def _append_route_stop(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    destination = str(action['destinationSystem'])
    universe = load_universe()
    tail_name = _route_tail_system(state)
    tail_system = next((system for system in universe.get('systems', []) if system.get('name') == tail_name), None)
    if not tail_system or destination not in tail_system.get('links', []):
        trace.append({'type': 'blocked_append_route_stop', 'destinationSystem': destination, 'tailSystem': tail_name, 'reason': 'not linked from route tail', 'routeQueue': list(state.get('routeQueue', []))})
        return True
    if destination == state['currentSystem'] or destination in state.get('routeQueue', []):
        trace.append({'type': 'blocked_append_route_stop', 'destinationSystem': destination, 'tailSystem': tail_name, 'reason': 'duplicate or current system', 'routeQueue': list(state.get('routeQueue', []))})
        return True
    state.setdefault('routeQueue', []).append(destination)
    state['routeSourceLabel'] = action.get('sourceLabel', 'original-runtime-observed')
    trace.append({
        'type': 'append_route_stop',
        'destinationSystem': destination,
        'tailSystem': tail_name,
        'routeQueue': list(state['routeQueue']),
        'greenRoutePath': [state['currentSystem']] + list(state['routeQueue']),
        'sourceLabel': state['routeSourceLabel'],
        'oracleStatus': action.get('oracleStatus', 'user_demonstrated_pending_original_trace'),
    })
    return True


def _clear_route_queue(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    previous_route = list(state.get('routeQueue', []))
    state['routeQueue'] = []
    state['routeSourceLabel'] = None
    trace.append({
        'type': 'clear_route_queue',
        'previousRoute': previous_route,
        'routeQueue': [],
        'sourceLabel': action.get('sourceLabel', 'terminal-velocity-route-guardrail'),
        'oracleStatus': action.get('oracleStatus', 'route_clear_pending_ev_classic_trace'),
    })
    return True


def _scan_station_services(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    universe = load_universe()
    system_name = str(action.get('system', state['currentSystem']))
    body_name = str(action.get('body', state.get('landedBody') or ''))
    if not body_name:
        trace.append({'type': 'blocked_scan_station_services', 'reason': 'no body selected', 'system': system_name})
        return False
    inventory = station_inventory(universe, system_name, body_name)
    services = list(inventory.get('services', []))
    trace.append({
        'type': 'scan_station_services',
        'system': system_name,
        'body': body_name,
        'services': services,
        'hasCommodities': 'commodities' in services,
        'hasMissionComputer': 'missions' in services,
        'hasOutfitter': 'outfitter' in services,
        'hasShipyard': 'shipyard' in services,
        'hasWeapons': 'weapons' in services,
        'hasRepairs': 'repairs' in services,
        'outfitsForSale': list(inventory.get('outfitsForSale', [])),
        'shipsForSale': list(inventory.get('shipsForSale', [])),
        'weaponsForSale': list(inventory.get('weaponsForSale', [])),
        'sourceLabel': action.get('sourceLabel', 'terminal-velocity-service-provisioning-scaffold'),
        'oracleStatus': action.get('oracleStatus', 'classic_runtime_service_matrix_pending'),
    })
    return True


def _accept_cargo_job(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    universe = load_universe()
    destination_system = action['destinationSystem']
    destination_body = action['destinationBody']
    _body(universe, destination_system, destination_body)
    tons = int(action.get('tons', 5))
    if state['landedBody'] is None:
        trace.append({'type': 'blocked_cargo_job', 'reason': 'not landed', 'destinationSystem': destination_system})
        return False
    if state['cargoUsed'] + tons > state['cargoCapacity']:
        trace.append({'type': 'blocked_cargo_job', 'reason': 'insufficient cargo space', 'destinationSystem': destination_system})
        return False
    distance = system_distance(universe, state['currentSystem'], destination_system)
    pay = int(action.get('pay', 350 + tons * 120 + distance * 2))
    job = {
        'id': action.get('id', action.get('missionId', f"cargo_{state['currentSystem'].lower()}_{destination_system.lower()}")),
        'originSystem': state['currentSystem'],
        'originBody': state['landedBody'],
        'destinationSystem': destination_system,
        'destinationBody': destination_body,
        'tons': tons,
        'reservedCargoTons': tons,
        'pay': pay,
        'risk': action.get('risk', 'safe'),
        'acceptedDay': int(state.get('currentDay', 0)),
        'timeLimitDays': action.get('timeLimitDays'),
        'completionGovernment': action.get('completionGovernment'),
        'completionReward': action.get('completionReward'),
        'failureBitSet': action.get('failureBitSet'),
        'setsFlags': list(action.get('setsFlags', [])),
        'completionFlags': list(action.get('completionFlags', [])),
        'sourceLabel': action.get('sourceLabel', 'terminal-velocity-mission-scaffold'),
        'oracleStatus': action.get('oracleStatus', 'mission_behavior_pending_classic_runtime_trace'),
    }
    state['cargoUsed'] += tons
    state['activeJobs'].append(job)
    for flag in job['setsFlags']:
        if flag not in state['storyFlags']:
            state['storyFlags'].append(flag)
    trace.append({'type': 'accept_cargo_job', **job, 'cargoUsed': state['cargoUsed']})
    return True


def _mission_failure_flag(failure_bit: Any) -> str | None:
    if failure_bit is None or int(failure_bit) < 0:
        return None
    value = int(failure_bit)
    if value >= 1000:
        return f'clear_mission_bit_{value - 1000}'
    return f'fail_mission_bit_{value}'


def _advance_days(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    days = int(action.get('days', 1))
    if days < 0:
        trace.append({'type': 'blocked_advance_days', 'reason': 'negative days', 'days': days})
        return False
    before_day = int(state.get('currentDay', 0))
    state['currentDay'] = before_day + days
    trace.append({'type': 'advance_days', 'days': days, 'currentDay': state['currentDay']})
    remaining_jobs = []
    for job in state.get('activeJobs', []):
        time_limit = job.get('timeLimitDays')
        accepted_day = int(job.get('acceptedDay', 0))
        if time_limit is not None and state['currentDay'] > accepted_day + int(time_limit):
            released = int(job.get('reservedCargoTons', job.get('tons', 0)))
            state['cargoUsed'] = max(0, int(state.get('cargoUsed', 0)) - released)
            mission_id = job.get('id')
            state.setdefault('failedJobs', []).append(mission_id)
            failure_flag = _mission_failure_flag(job.get('failureBitSet'))
            if failure_flag and failure_flag not in state.get('storyFlags', []):
                state.setdefault('storyFlags', []).append(failure_flag)
            completion_government = job.get('completionGovernment')
            completion_reward = int(job.get('completionReward') or 0)
            reputation_delta = 0
            if completion_government and completion_reward:
                reputation_delta = -(completion_reward // 2)
                state.setdefault('reputation', {})[completion_government] = int(state.get('reputation', {}).get(completion_government, 0)) + reputation_delta
            trace.append({
                'type': 'mission_deadline_failure',
                'missionId': mission_id,
                'acceptedDay': accepted_day,
                'currentDay': state['currentDay'],
                'timeLimitDays': int(time_limit),
                'releasedCargoTons': released,
                'failureFlag': failure_flag,
                'completionGovernment': completion_government,
                'completionReward': completion_reward,
                'reputationDelta': reputation_delta,
                'sourceLabel': 'ev-classic-resource-bible-backed-mission-failure-scaffold',
                'oracleStatus': 'deadline_failure_runtime_ui_pending_classic_trace',
            })
        else:
            remaining_jobs.append(job)
    state['activeJobs'] = remaining_jobs
    return True


def _blocked_jump_event(origin: str, destination: str | None, reason: str, route_queue: list[str]) -> dict[str, Any]:
    event: dict[str, Any] = {'type': 'blocked_jump', 'originSystem': origin, 'destinationSystem': destination, 'reason': reason}
    if route_queue:
        event['routeQueue'] = list(route_queue)
    return event


def _jump(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    universe = load_universe()
    destination = action.get('destinationSystem')
    if destination is None and state.get('routeQueue'):
        destination = state['routeQueue'][0]
    if destination is None:
        trace.append(_blocked_jump_event(state['currentSystem'], None, 'no destination selected', list(state.get('routeQueue', []))))
        return False
    destination = str(destination)
    origin = state['currentSystem']
    links = set(_system(universe, origin).get('links', []))
    if destination not in links:
        trace.append(_blocked_jump_event(origin, destination, f'{destination} not linked from {origin}', list(state.get('routeQueue', []))))
        return False
    if state['fuel'] <= 0:
        trace.append(_blocked_jump_event(origin, destination, 'insufficient fuel', list(state.get('routeQueue', []))))
        return False
    distance_from_center = float(action.get('distanceFromSystemCenter', state.get('distanceFromSystemCenter', MIN_JUMP_DISTANCE + 50)))
    if distance_from_center < MIN_JUMP_DISTANCE:
        event = _blocked_jump_event(origin, destination, 'too close to system center', list(state.get('routeQueue', [])))
        event['distanceFromSystemCenter'] = distance_from_center
        event['minJumpDistance'] = MIN_JUMP_DISTANCE
        event['sourceLabel'] = 'original-runtime-observed'
        event['oracleStatus'] = 'near_center_jump_failure_observed_exact_distance_pending'
        trace.append(event)
        return False
    previous_route = list(state.get('routeQueue', []))
    state['currentSystem'] = destination
    state['landedBody'] = None
    state['fuel'] -= 1
    state['distanceFromSystemCenter'] = 0
    if previous_route and previous_route[0] == destination:
        state['routeQueue'].pop(0)
    state['knownSystems'] = sorted(set(state.get('knownSystems', [])) | {destination} | set(_system(universe, destination).get('links', [])))
    trace.append({'type': 'jump', 'originSystem': origin, 'destinationSystem': destination, 'fuelAfter': state['fuel'], 'previousRoute': previous_route, 'remainingRoute': list(state.get('routeQueue', []))})
    return True


def _land(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    universe = load_universe()
    body_name = action['body']
    _body(universe, state['currentSystem'], body_name)
    state['landedBody'] = body_name
    trace.append({'type': 'land', 'system': state['currentSystem'], 'body': body_name})
    return True


def _depart(state: dict[str, Any], _action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    previous_body = state['landedBody']
    state['landedBody'] = None
    state['distanceFromSystemCenter'] = MIN_JUMP_DISTANCE + 50
    trace.append({'type': 'depart', 'system': state['currentSystem'], 'body': previous_body, 'distanceFromSystemCenter': state['distanceFromSystemCenter']})
    return True


def _refuel(state: dict[str, Any], _action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    if state['landedBody'] is None:
        trace.append({'type': 'blocked_refuel', 'reason': 'not landed', 'system': state['currentSystem']})
        return False
    state['fuel'] = STARTING_FUEL
    trace.append({'type': 'refuel', 'system': state['currentSystem'], 'body': state['landedBody'], 'fuelAfter': state['fuel']})
    return True


def _repair_hull(state: dict[str, Any], _action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    if state['landedBody'] is None:
        trace.append({'type': 'blocked_repair_hull', 'reason': 'not landed', 'system': state['currentSystem'], 'sourceLabel': 'terminal-velocity-repair-service-scaffold', 'oracleStatus': 'repair_service_pending_ev_classic_runtime_trace'})
        return False
    universe = load_universe()
    inventory = station_inventory(universe, state['currentSystem'], state['landedBody'])
    if 'repairs' not in inventory.get('services', []):
        trace.append({'type': 'blocked_repair_hull', 'reason': 'repair service unavailable', 'system': state['currentSystem'], 'body': state['landedBody'], 'sourceLabel': 'terminal-velocity-repair-service-scaffold', 'oracleStatus': 'repair_service_pending_ev_classic_runtime_trace'})
        return False
    max_hull = int(state.get('maxHull', 100))
    hull_before = int(state.get('currentHull', max_hull))
    missing = max(0, max_hull - hull_before)
    if missing <= 0:
        trace.append({'type': 'blocked_repair_hull', 'reason': 'no repairs needed', 'system': state['currentSystem'], 'body': state['landedBody'], 'currentHull': hull_before, 'maxHull': max_hull, 'sourceLabel': 'terminal-velocity-repair-service-scaffold', 'oracleStatus': 'repair_service_pending_ev_classic_runtime_trace'})
        return False
    repair_price = int(outfit_manifest().get('repair', {}).get('pricePerHullPoint', 8))
    cost = missing * repair_price
    if int(state.get('credits', 0)) < cost:
        trace.append({'type': 'blocked_repair_hull', 'reason': 'insufficient credits', 'system': state['currentSystem'], 'body': state['landedBody'], 'cost': cost, 'credits': state.get('credits', 0), 'sourceLabel': 'terminal-velocity-repair-service-scaffold', 'oracleStatus': 'repair_service_pending_ev_classic_runtime_trace'})
        return False
    state['credits'] = int(state.get('credits', 0)) - cost
    state['currentHull'] = max_hull
    trace.append({'type': 'repair_hull', 'system': state['currentSystem'], 'body': state['landedBody'], 'hullBefore': hull_before, 'hullAfter': state['currentHull'], 'maxHull': max_hull, 'pricePerHullPoint': repair_price, 'cost': cost, 'creditsAfter': state['credits'], 'sourceLabel': 'terminal-velocity-repair-service-scaffold', 'oracleStatus': 'repair_service_pending_ev_classic_runtime_trace'})
    return True


def _disable_player(state: dict[str, Any], _action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    state['currentHull'] = 0
    state['playerDisabled'] = True
    trace.append({
        'type': 'disable_player',
        'currentHull': state['currentHull'],
        'playerDisabled': state['playerDisabled'],
        'sourceLabel': 'terminal-velocity-player-disabled-scaffold',
        'oracleStatus': 'classic_runtime_player_death_pending_strict_play_safe_trace',
    })
    return True


def _attempt_disabled_action(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    attempted = action.get('action', 'unknown')
    if state.get('playerDisabled') is True:
        trace.append({
            'type': 'blocked_disabled_action',
            'action': attempted,
            'reason': 'player ship disabled',
            'sourceLabel': 'terminal-velocity-player-disabled-scaffold',
            'oracleStatus': 'classic_runtime_player_death_pending_strict_play_safe_trace',
        })
        return False
    trace.append({'type': 'disabled_action_not_blocked', 'action': attempted})
    return True


def _recover_disabled_player(state: dict[str, Any], _action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    if state.get('playerDisabled') is not True:
        trace.append({'type': 'blocked_disabled_recovery', 'reason': 'player not disabled'})
        return False
    max_hull = int(state.get('maxHull', 100))
    hull_before = int(state.get('currentHull', 0))
    state['currentHull'] = max_hull
    state['playerDisabled'] = False
    trace.append({
        'type': 'recover_disabled_player',
        'hullBefore': hull_before,
        'hullAfter': state['currentHull'],
        'playerDisabled': state['playerDisabled'],
        'sourceLabel': 'terminal-velocity-player-disabled-scaffold',
        'oracleStatus': 'classic_runtime_player_death_pending_strict_play_safe_trace',
    })
    return True


def _set_state(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    for key, value in action.get('values', {}).items():
        state[key] = value
    trace.append({'type': 'state_adjustment', 'values': deepcopy(action.get('values', {}))})
    return True


def _route_to_active_mission_destination(state: dict[str, Any], _action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    if not state.get('activeJobs'):
        trace.append({'type': 'blocked_route_to_active_mission_destination', 'reason': 'no active mission', 'routeQueue': list(state.get('routeQueue', []))})
        return True
    job = state['activeJobs'][0]
    destination = str(job.get('destinationSystem', ''))
    before_size = len(state.get('routeQueue', []))
    appended = _append_route_stop(state, {'destinationSystem': destination, 'sourceLabel': 'terminal-velocity-design-scaffold', 'oracleStatus': 'mission_objective_hint_pending_ev_classic_ui_trace'}, trace)
    trace.append({
        'type': 'route_to_active_mission_destination',
        'missionId': job.get('id'),
        'destinationSystem': destination,
        'routeQueued': appended and len(state.get('routeQueue', [])) > before_size,
        'routeQueue': list(state.get('routeQueue', [])),
        'sourceLabel': 'terminal-velocity-design-scaffold',
        'oracleStatus': 'mission_objective_hint_pending_ev_classic_ui_trace',
    })
    return True


def _scan_mission_offers(state: dict[str, Any], _action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    if state['landedBody'] is None:
        trace.append({'type': 'blocked_scan_mission_offers', 'reason': 'not landed', 'system': state['currentSystem']})
        return False
    missions = mission_manifest()
    mission_ids = available_mission_ids(
        missions,
        state['currentSystem'],
        state['landedBody'],
        completed_ids=state.get('completedJobs', []),
        active_ids=[job['id'] for job in state.get('activeJobs', [])],
        flags=state.get('storyFlags', []),
        reputation=state.get('reputation', {}),
        legal_records=state.get('legalRecords', {}),
    )
    offers_by_surface: dict[str, list[str]] = {'Mission Computer': mission_ids}
    archive_key = f"{state['currentSystem']}/{state['landedBody']}"
    state['missionOfferArchive'][archive_key] = deepcopy(offers_by_surface)
    trace.append({
        'type': 'scan_mission_offers',
        'system': state['currentSystem'],
        'body': state['landedBody'],
        'offersBySurface': offers_by_surface,
        'totalOffers': sum(len(offers) for offers in offers_by_surface.values()),
        'sourceLabel': 'terminal-velocity-observed',
        'oracleStatus': 'terminal_velocity_eval_pending_original_trace',
    })
    return True


def _accept_manifest_mission(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    mission_id = action['missionId']
    missions = mission_manifest()
    available_ids = available_mission_ids(
        missions,
        state['currentSystem'],
        state['landedBody'],
        completed_ids=state.get('completedJobs', []),
        active_ids=[job['id'] for job in state.get('activeJobs', [])],
        flags=state.get('storyFlags', []),
        reputation=state.get('reputation', {}),
        legal_records=state.get('legalRecords', {}),
    )
    if mission_id not in available_ids:
        trace.append({'type': 'blocked_manifest_mission', 'missionId': mission_id, 'reason': 'not available at current landing', 'system': state['currentSystem'], 'body': state['landedBody']})
        return True
    mission = next(item for item in missions.get('missions', []) if item.get('id') == mission_id)
    return _accept_cargo_job(state, {
        'id': mission['id'],
        'destinationSystem': mission['destinationSystem'],
        'destinationBody': mission['destinationBody'],
        'tons': mission.get('cargoTons', 0),
        'pay': mission.get('reward', 0),
        'setsFlags': mission.get('setsFlags', []),
        'completionFlags': mission.get('completionFlags', []),
        'timeLimitDays': mission.get('timeLimitDays'),
        'completionGovernment': mission.get('completionGovernment'),
        'completionReward': mission.get('completionReward'),
        'failureBitSet': mission.get('failureBitSet'),
    }, trace)


def _buy_outfit_or_weapon(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    if state['landedBody'] is None:
        trace.append({'type': 'blocked_buy_outfit_or_weapon', 'reason': 'not landed', 'system': state['currentSystem']})
        return False
    universe = load_universe()
    inventory = station_inventory(universe, state['currentSystem'], state['landedBody'])
    item_id = str(action['itemId'])
    outfit_by_id = {item['id']: item for item in outfit_manifest().get('outfits', [])}
    weapon_by_id = {item['id']: item for item in weapon_manifest().get('weapons', [])}
    if item_id in outfit_by_id:
        if item_id not in inventory.get('outfitsForSale', []):
            trace.append({'type': 'blocked_buy_outfit_or_weapon', 'reason': 'outfit not for sale here', 'itemId': item_id, 'system': state['currentSystem'], 'body': state['landedBody']})
            return False
        item = outfit_by_id[item_id]
        sale_type = 'outfit'
    elif item_id in weapon_by_id:
        if item_id not in inventory.get('weaponsForSale', []):
            trace.append({'type': 'blocked_buy_outfit_or_weapon', 'reason': 'weapon not for sale here', 'itemId': item_id, 'system': state['currentSystem'], 'body': state['landedBody']})
            return False
        item = weapon_by_id[item_id]
        sale_type = 'weapon'
    else:
        trace.append({'type': 'blocked_buy_outfit_or_weapon', 'reason': 'unknown item', 'itemId': item_id})
        return False
    price = int(item.get('price', 0))
    if state['credits'] < price:
        trace.append({'type': 'blocked_buy_outfit_or_weapon', 'reason': 'insufficient credits', 'itemId': item_id, 'price': price, 'credits': state['credits']})
        return False
    state['credits'] -= price
    if sale_type == 'weapon':
        state['ownedWeapons'][item_id] = int(state['ownedWeapons'].get(item_id, 0)) + 1
    else:
        state['ownedOutfits'][item_id] = int(state['ownedOutfits'].get(item_id, 0)) + 1
        effects = item.get('effects', {})
        state['cargoCapacity'] += int(effects.get('cargoSpace', 0))
        state['maxHull'] += int(effects.get('maxHull', 0))
        state['maxFuel'] += int(effects.get('maxFuel', 0))
    trace.append({
        'type': 'buy_outfit_or_weapon',
        'saleType': sale_type,
        'itemId': item_id,
        'name': item.get('name', item_id),
        'price': price,
        'creditsAfter': state['credits'],
        'cargoCapacity': state['cargoCapacity'],
        'maxHull': state['maxHull'],
        'maxFuel': state['maxFuel'],
        'sourceLabel': 'terminal-velocity-outfitter-ship-ladder-scaffold',
        'oracleStatus': 'manifest_scaffold_pending_original_outfitter_trace',
    })
    return True


def _buy_ship(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    if state['landedBody'] is None:
        trace.append({'type': 'blocked_buy_ship', 'reason': 'not landed', 'system': state['currentSystem']})
        return False
    universe = load_universe()
    inventory = station_inventory(universe, state['currentSystem'], state['landedBody'])
    ship_id = str(action['shipId'])
    listings = {item['shipId']: item for item in outfit_manifest().get('shipyard', [])}
    ships = {item['id']: item for item in ship_manifest().get('ships', [])}
    if ship_id not in inventory.get('shipsForSale', []):
        trace.append({'type': 'blocked_buy_ship', 'reason': 'ship not for sale here', 'shipId': ship_id, 'system': state['currentSystem'], 'body': state['landedBody']})
        return False
    if ship_id not in listings or ship_id not in ships:
        trace.append({'type': 'blocked_buy_ship', 'reason': 'ship manifest missing', 'shipId': ship_id})
        return False
    listing = listings[ship_id]
    price = int(listing.get('price', 0))
    if state['credits'] < price:
        trace.append({'type': 'blocked_buy_ship', 'reason': 'insufficient credits', 'shipId': ship_id, 'price': price, 'credits': state['credits']})
        return False
    previous_ship = state['playerShipId']
    previous_cargo = state['cargoCapacity']
    ship = ships[ship_id]
    state['credits'] -= price
    state['playerShipId'] = ship_id
    state['cargoCapacity'] = int(ship.get('cargoSpace', state['cargoCapacity']))
    state['cargoUsed'] = min(int(state['cargoUsed']), int(state['cargoCapacity']))
    state['maxHull'] = int(ship.get('hull', state.get('maxHull', 100)))
    state['maxFuel'] = int(ship.get('fuel', state.get('maxFuel', STARTING_FUEL)))
    trace.append({
        'type': 'buy_ship',
        'shipId': ship_id,
        'previousShipId': previous_ship,
        'price': price,
        'creditsAfter': state['credits'],
        'cargoCapacityBefore': previous_cargo,
        'cargoCapacityAfter': state['cargoCapacity'],
        'sourceLabel': 'terminal-velocity-outfitter-ship-ladder-scaffold',
        'oracleStatus': 'manifest_scaffold_pending_original_shipyard_trace',
    })
    return True


def _avoid_pirate_contact(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    state['combatExecuted'] = False
    state['threatPosture'] = 'evaded'
    destination = str(action.get('safeDestinationSystem', 'Sol'))
    trace.append({
        'type': 'avoid_pirate_contact',
        'threat': action.get('threat', 'pirate_intercept'),
        'originSystem': state['currentSystem'],
        'safeDestinationSystem': destination,
        'decision': 'jump_to_linked_safe_port',
        'combatExecuted': False,
        'sourceLabel': 'terminal-velocity-pirate-avoidance-scaffold',
        'oracleStatus': 'pirate_avoidance_pending_ev_classic_combat_trace',
    })
    return _jump(state, {'destinationSystem': destination}, trace)


def _combat_placeholder_guardrail(state: dict[str, Any], _action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    state['combatExecuted'] = False
    trace.append({
        'type': 'combat_placeholder_guardrail',
        'purpose': 'define disposable non-strict combat/piracy scaffold without executing destructive tests',
        'stopConditions': [
            'Strict Play enabled',
            'low shields or hull',
            'mission/trade pilot contamination',
            'unclear save state',
            'unverified input delivery',
        ],
    })
    return True


def _current_government_name(state: dict[str, Any]) -> str:
    governments = government_manifest()
    mapping = governments.get('systems', {}).get(state['currentSystem'], {})
    government = mapping.get('government')
    if not government:
        raise ValueError(f"system {state['currentSystem']} has no government mapping")
    return str(government)


def _apply_contraband_scan(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    government = str(action.get('government') or _current_government_name(state))
    governments = government_manifest()
    reputation = reputation_manifest()
    outcome = enforcement_outcome(
        governments,
        reputation,
        government=government,
        hold=state.get('cargoHold', {}),
        credits=state.get('credits', 0),
        legal_records=state.get('legalRecords', {}),
        accept_bribe=bool(action.get('acceptBribe', False)),
    )
    state['credits'] = int(state.get('credits', 0)) + int(outcome.get('creditsDelta', 0))
    state.setdefault('legalRecords', {})[government] = int(state.get('legalRecords', {}).get(government, 0)) + int(outcome.get('legalDelta', 0))
    confiscated = dict(outcome.get('confiscated', {}))
    for commodity, tons in confiscated.items():
        removed = int(tons)
        if removed <= 0:
            continue
        before = int(state.get('cargoHold', {}).get(commodity, 0))
        after = max(0, before - removed)
        if after:
            state.setdefault('cargoHold', {})[commodity] = after
        else:
            state.setdefault('cargoHold', {}).pop(commodity, None)
        state['cargoUsed'] = max(0, int(state.get('cargoUsed', 0)) - min(before, removed))
    trace.append({
        'type': 'contraband_scan',
        'government': government,
        'action': outcome.get('action'),
        'creditsDelta': int(outcome.get('creditsDelta', 0)),
        'legalDelta': int(outcome.get('legalDelta', 0)),
        'creditsAfter': state['credits'],
        'legalAfter': state['legalRecords'][government],
        'confiscated': confiscated,
        'cargoHold': dict(state.get('cargoHold', {})),
        'sourceLabel': 'terminal-velocity-classic-resource-smuggling-scan-semantics',
        'oracleStatus': 'classic_runtime_scan_frequency_and_ui_wording_pending',
    })
    return True


def _pay_legal_clemency(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    government = str(action.get('government') or _current_government_name(state))
    offer = clemency_offer(
        reputation_manifest(),
        reputation_scores=state.get('reputation', {}),
        legal_records=state.get('legalRecords', {}),
        government=government,
    )
    if not offer.get('available'):
        trace.append({'type': 'blocked_legal_clemency', 'government': government, 'reason': 'clemency unavailable', 'sourceLabel': 'terminal-velocity-inferred-clemency-scaffold', 'oracleStatus': 'approved_inference_pending_ev_classic_confirmation'})
        return False
    cost = int(offer.get('cost', 0))
    if int(state.get('credits', 0)) < cost:
        trace.append({'type': 'blocked_legal_clemency', 'government': government, 'reason': 'insufficient credits', 'cost': cost, 'credits': state.get('credits', 0), 'sourceLabel': 'terminal-velocity-inferred-clemency-scaffold', 'oracleStatus': 'approved_inference_pending_ev_classic_confirmation'})
        return False
    state['credits'] = int(state.get('credits', 0)) - cost
    state.setdefault('legalRecords', {})[government] = int(state.get('legalRecords', {}).get(government, 0)) + int(offer.get('legalDelta', 0))
    trace.append({
        'type': 'pay_legal_clemency',
        'government': government,
        'cost': cost,
        'legalDelta': int(offer.get('legalDelta', 0)),
        'creditsAfter': state['credits'],
        'legalAfter': state['legalRecords'][government],
        'sourceLabel': 'terminal-velocity-inferred-clemency-scaffold',
        'oracleStatus': 'approved_inference_pending_ev_classic_confirmation',
    })
    return True


def _complete_cargo_jobs(state: dict[str, Any], _action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    remaining = []
    completed_any = False
    for job in state['activeJobs']:
        if job['destinationSystem'] == state['currentSystem'] and job['destinationBody'] == state['landedBody']:
            state['credits'] += int(job['pay'])
            state['cargoUsed'] -= int(job['tons'])
            state['completedJobs'].append(job['id'])
            for flag in job.get('completionFlags', []):
                if flag not in state['storyFlags']:
                    state['storyFlags'].append(flag)
            trace.append({'type': 'complete_cargo_job', **job, 'creditsAfter': state['credits'], 'cargoUsed': state['cargoUsed']})
            completed_any = True
        else:
            remaining.append(job)
    state['activeJobs'] = remaining
    if not completed_any:
        trace.append({'type': 'blocked_complete_cargo_job', 'reason': 'no deliverable job at current landing'})
    return completed_any


def _abort_active_mission(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    mission_id = action.get('missionId')
    active_jobs = state.get('activeJobs', [])
    if not active_jobs:
        trace.append({'type': 'blocked_abort_mission', 'reason': 'no active mission', 'sourceLabel': 'terminal-velocity-mission-abort-scaffold', 'oracleStatus': 'mission_abort_pending_classic_runtime_or_manual_trace'})
        return False
    job = None
    for candidate in active_jobs:
        if mission_id is None or candidate.get('id') == mission_id:
            job = candidate
            break
    if job is None:
        trace.append({'type': 'blocked_abort_mission', 'missionId': mission_id, 'reason': 'mission not active', 'sourceLabel': 'terminal-velocity-mission-abort-scaffold', 'oracleStatus': 'mission_abort_pending_classic_runtime_or_manual_trace'})
        return False
    state['activeJobs'] = [candidate for candidate in active_jobs if candidate.get('id') != job.get('id')]
    released = int(job.get('reservedCargoTons', job.get('tons', 0)))
    state['cargoUsed'] = max(0, int(state.get('cargoUsed', 0)) - released)
    state.setdefault('abortedJobs', []).append(job.get('id'))
    trace.append({
        'type': 'abort_mission',
        'missionId': job.get('id'),
        'releasedCargoTons': released,
        'cargoUsed': state['cargoUsed'],
        'activeJobs': [candidate.get('id') for candidate in state.get('activeJobs', [])],
        'sourceLabel': 'terminal-velocity-mission-abort-scaffold',
        'oracleStatus': 'mission_abort_pending_classic_runtime_or_manual_trace',
    })
    return True


def default_actions_for_scenario(name: str) -> list[dict[str, Any]]:
    if name == 'levo_merchant_first_hop':
        return [
            {'type': 'buy_commodity_lot', 'commodity': 'food'},
            {'type': 'accept_cargo_job', 'destinationSystem': 'Sol', 'destinationBody': 'Earth', 'tons': 5, 'risk': 'safe'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'complete_cargo_jobs'},
        ]
    if name == 'levo_same_port_sellback_loop':
        return [
            {'type': 'buy_commodity_lot', 'commodity': 'food'},
            {
                'type': 'sell_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'original-runtime-observed',
                'oracleStatus': 'levo_same_port_sellback_observed',
            },
        ]
    if name == 'commodity_sell_blocked_recovery_loop':
        return [
            {'type': 'sell_commodity_lot', 'commodity': 'food', 'expectBlocked': True},
            {'type': 'buy_commodity_lot', 'commodity': 'food'},
            {'type': 'depart'},
            {'type': 'sell_commodity_lot', 'commodity': 'food', 'expectBlocked': True},
            {'type': 'land', 'body': START_BODY},
            {'type': 'sell_commodity_lot', 'commodity': 'food'},
        ]
    if name == 'commodity_buy_blocked_recovery_loop':
        return [
            {'type': 'depart'},
            {'type': 'buy_commodity_lot', 'commodity': 'food', 'expectBlocked': True},
            {'type': 'land', 'body': START_BODY},
            {'type': 'set_state', 'values': {'credits': 0}},
            {'type': 'buy_commodity_lot', 'commodity': 'food', 'expectBlocked': True},
            {'type': 'set_state', 'values': {'credits': STARTING_CREDITS, 'cargoUsed': 15}},
            {'type': 'buy_commodity_lot', 'commodity': 'food', 'expectBlocked': True},
            {'type': 'set_state', 'values': {'cargoUsed': 0}},
            {'type': 'buy_commodity_lot', 'commodity': 'food'},
        ]
    if name == 'cross_market_trade_spread_scout':
        return [
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {
                'type': 'buy_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-cross-market-trade-scaffold',
                'oracleStatus': 'classic_runtime_cross_market_spread_pending',
            },
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': START_SYSTEM},
            {'type': 'land', 'body': START_BODY},
            {
                'type': 'sell_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-cross-market-trade-scaffold',
                'oracleStatus': 'classic_runtime_cross_market_spread_pending',
            },
        ]
    if name == 'max_hold_trade_route_scout':
        return [
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {
                'type': 'buy_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-max-hold-trade-scaffold',
                'oracleStatus': 'classic_runtime_multi_lot_trade_spread_pending',
            },
            {
                'type': 'buy_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-max-hold-trade-scaffold',
                'oracleStatus': 'classic_runtime_multi_lot_trade_spread_pending',
            },
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': START_SYSTEM},
            {'type': 'land', 'body': START_BODY},
            {
                'type': 'sell_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-max-hold-trade-scaffold',
                'oracleStatus': 'classic_runtime_multi_lot_trade_spread_pending',
            },
            {
                'type': 'sell_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-max-hold-trade-scaffold',
                'oracleStatus': 'classic_runtime_multi_lot_trade_spread_pending',
            },
        ]
    if name == 'trade_route_refuel_profit_loop':
        return [
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {
                'type': 'buy_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-refuel-trade-route-scaffold',
                'oracleStatus': 'classic_runtime_refuel_trade_route_pending',
            },
            {
                'type': 'buy_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-refuel-trade-route-scaffold',
                'oracleStatus': 'classic_runtime_refuel_trade_route_pending',
            },
            {'type': 'set_state', 'values': {'fuel': 0}},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': START_SYSTEM, 'expectBlocked': True},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'refuel'},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': START_SYSTEM},
            {'type': 'land', 'body': START_BODY},
            {
                'type': 'sell_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-refuel-trade-route-scaffold',
                'oracleStatus': 'classic_runtime_refuel_trade_route_pending',
            },
            {
                'type': 'sell_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-refuel-trade-route-scaffold',
                'oracleStatus': 'classic_runtime_refuel_trade_route_pending',
            },
        ]
    if name == 'mission_runner_first_delivery':
        return [
            {
                'type': 'accept_cargo_job',
                'id': 'levo_landfall_courier',
                'destinationSystem': 'Centauri',
                'destinationBody': 'Landfall',
                'tons': 8,
                'pay': 900,
                'risk': 'safe',
            },
            {'type': 'jump', 'destinationSystem': 'Centauri'},
            {'type': 'land', 'body': 'Landfall'},
            {'type': 'complete_cargo_jobs'},
        ]
    if name == 'chapter_one_courier_chain':
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'accept_cargo_job', 'missionId': 'intro_courier_earth_hera', 'originSystem': 'Sol', 'originBody': 'Earth', 'destinationSystem': 'Centauri', 'destinationBody': 'Luna', 'tons': 3, 'pay': 1800, 'setsFlags': ['story_intro_started'], 'completionFlags': ['story_intro_complete', 'federation_trusted_courier']},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Centauri'},
            {'type': 'land', 'body': 'Luna'},
            {'type': 'complete_cargo_jobs'},
            {'type': 'accept_cargo_job', 'missionId': 'frontier_sample_hera_freeport', 'originSystem': 'Centauri', 'originBody': 'Luna', 'destinationSystem': 'Sirius', 'destinationBody': 'Sirius Station', 'tons': 4, 'pay': 2400, 'setsFlags': ['frontier_chain_started'], 'completionFlags': ['frontier_samples_delivered', 'reputation_independent_positive']},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sirius'},
            {'type': 'land', 'body': 'Sirius Station'},
            {'type': 'complete_cargo_jobs'},
            {'type': 'accept_cargo_job', 'missionId': 'freeport_return_earth', 'originSystem': 'Sirius', 'originBody': 'Sirius Station', 'destinationSystem': 'Sol', 'destinationBody': 'Earth', 'tons': 5, 'pay': 3200, 'setsFlags': ['return_contract_started'], 'completionFlags': ['chapter_one_complete', 'federation_independent_bridge']},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'complete_cargo_jobs'},
        ]
    if name == 'scan_intro_mission_offers':
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'scan_mission_offers'},
        ]
    if name == 'intro_courier_mission_delivery':
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {
                'type': 'accept_cargo_job',
                'id': 'intro_courier_earth_hera',
                'destinationSystem': 'Centauri',
                'destinationBody': 'Luna',
                'tons': 3,
                'pay': 1800,
                'risk': 'safe',
                'setsFlags': ['story_intro_started'],
                'completionFlags': ['story_intro_complete', 'federation_trusted_courier'],
            },
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Centauri'},
            {'type': 'land', 'body': 'Luna'},
            {'type': 'complete_cargo_jobs'},
        ]
    if name == 'alignment_choice_guardrail':
        return [
            {'type': 'set_state', 'values': {'currentSystem': 'Sirius', 'landedBody': 'Sirius Station', 'storyFlags': ['frontier_samples_delivered']}},
            {'type': 'accept_manifest_mission', 'missionId': 'federation_report_freeport'},
            {'type': 'accept_manifest_mission', 'missionId': 'freeport_pact_smugglers'},
        ]
    if name == 'federation_alignment_delivery_loop':
        return [
            {'type': 'set_state', 'values': {'currentSystem': 'Sirius', 'landedBody': 'Sirius Station', 'storyFlags': ['frontier_samples_delivered']}},
            {'type': 'accept_manifest_mission', 'missionId': 'federation_report_freeport'},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'complete_cargo_jobs'},
            {'type': 'set_state', 'values': {'currentSystem': 'Sirius', 'landedBody': 'Sirius Station'}},
            {'type': 'accept_manifest_mission', 'missionId': 'freeport_pact_smugglers'},
        ]
    if name == 'mission_destination_route_hint':
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'accept_manifest_mission', 'missionId': 'intro_courier_earth_hera'},
            {'type': 'depart'},
            {'type': 'route_to_active_mission_destination'},
        ]
    if name == 'mission_trade_hybrid_capacity_planning':
        return [
            {'type': 'accept_cargo_job', 'id': 'levo_trade_aligned_courier', 'destinationSystem': 'Sol', 'destinationBody': 'Earth', 'tons': 8, 'pay': 900, 'risk': 'safe'},
            {'type': 'buy_commodity_lot', 'commodity': 'food'},
            {'type': 'buy_commodity_lot', 'commodity': 'industrial', 'expectBlocked': True},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'complete_cargo_jobs'},
        ]
    if name == 'mission_trade_refuel_delivery_loop':
        return [
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {
                'type': 'accept_cargo_job',
                'id': 'intro_courier_earth_hera',
                'destinationSystem': 'Centauri',
                'destinationBody': 'Luna',
                'tons': 3,
                'pay': 1800,
                'setsFlags': ['story_intro_started'],
                'completionFlags': ['story_intro_complete', 'federation_trusted_courier'],
                'sourceLabel': 'terminal-velocity-mission-trade-refuel-scaffold',
                'oracleStatus': 'mission_trade_refuel_pending_classic_runtime_trace',
            },
            {
                'type': 'buy_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-mission-trade-refuel-scaffold',
                'oracleStatus': 'mission_trade_refuel_pending_classic_runtime_trace',
            },
            {'type': 'set_state', 'values': {'fuel': 0}},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Centauri', 'expectBlocked': True},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'refuel'},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Centauri'},
            {'type': 'land', 'body': 'Luna'},
            {'type': 'complete_cargo_jobs'},
        ]
    if name == 'mission_trade_destination_sale_loop':
        return [
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {
                'type': 'accept_cargo_job',
                'id': 'intro_courier_earth_hera',
                'destinationSystem': 'Centauri',
                'destinationBody': 'Luna',
                'tons': 3,
                'pay': 1800,
                'setsFlags': ['story_intro_started'],
                'completionFlags': ['story_intro_complete', 'federation_trusted_courier'],
                'sourceLabel': 'terminal-velocity-mission-trade-destination-sale-scaffold',
                'oracleStatus': 'mission_trade_destination_sale_pending_classic_runtime_trace',
            },
            {
                'type': 'buy_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-mission-trade-destination-sale-scaffold',
                'oracleStatus': 'mission_trade_destination_sale_pending_classic_runtime_trace',
            },
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Centauri'},
            {'type': 'land', 'body': 'Luna'},
            {'type': 'complete_cargo_jobs'},
            {
                'type': 'sell_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-mission-trade-destination-sale-scaffold',
                'oracleStatus': 'mission_trade_destination_sale_pending_classic_runtime_trace',
            },
        ]
    if name == 'chapter_one_trade_carryover_loop':
        return [
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {
                'type': 'accept_cargo_job',
                'id': 'intro_courier_earth_hera',
                'destinationSystem': 'Centauri',
                'destinationBody': 'Luna',
                'tons': 3,
                'pay': 1800,
                'setsFlags': ['story_intro_started'],
                'completionFlags': ['story_intro_complete', 'federation_trusted_courier'],
                'sourceLabel': 'terminal-velocity-chapter-one-trade-carryover-scaffold',
                'oracleStatus': 'chapter_one_trade_carryover_pending_classic_runtime_trace',
            },
            {
                'type': 'buy_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-chapter-one-trade-carryover-scaffold',
                'oracleStatus': 'chapter_one_trade_carryover_pending_classic_runtime_trace',
            },
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Centauri'},
            {'type': 'land', 'body': 'Luna'},
            {'type': 'complete_cargo_jobs'},
            {
                'type': 'accept_cargo_job',
                'id': 'frontier_sample_hera_freeport',
                'destinationSystem': 'Sirius',
                'destinationBody': 'Sirius Station',
                'tons': 4,
                'pay': 2400,
                'setsFlags': ['frontier_chain_started'],
                'completionFlags': ['frontier_samples_delivered', 'reputation_independent_positive'],
                'sourceLabel': 'terminal-velocity-chapter-one-trade-carryover-scaffold',
                'oracleStatus': 'chapter_one_trade_carryover_pending_classic_runtime_trace',
            },
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sirius'},
            {'type': 'land', 'body': 'Sirius Station'},
            {'type': 'complete_cargo_jobs'},
            {
                'type': 'sell_commodity_lot',
                'commodity': 'food',
                'sourceLabel': 'terminal-velocity-chapter-one-trade-carryover-scaffold',
                'oracleStatus': 'chapter_one_trade_carryover_pending_classic_runtime_trace',
            },
        ]
    if name == 'mission_trade_return_margin_guardrail':
        source_label = 'terminal-velocity-mission-trade-return-margin-scaffold'
        oracle_status = 'chapter_one_return_trade_margin_pending_classic_runtime_trace'
        return [
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'accept_cargo_job', 'id': 'intro_courier_earth_hera', 'destinationSystem': 'Centauri', 'destinationBody': 'Luna', 'tons': 3, 'pay': 1800, 'setsFlags': ['story_intro_started'], 'completionFlags': ['story_intro_complete', 'federation_trusted_courier'], 'sourceLabel': source_label, 'oracleStatus': oracle_status},
            {'type': 'buy_commodity_lot', 'commodity': 'food', 'sourceLabel': source_label, 'oracleStatus': oracle_status},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Centauri'},
            {'type': 'land', 'body': 'Luna'},
            {'type': 'complete_cargo_jobs'},
            {'type': 'accept_cargo_job', 'id': 'frontier_sample_hera_freeport', 'destinationSystem': 'Sirius', 'destinationBody': 'Sirius Station', 'tons': 4, 'pay': 2400, 'setsFlags': ['frontier_chain_started'], 'completionFlags': ['frontier_samples_delivered', 'reputation_independent_positive'], 'sourceLabel': source_label, 'oracleStatus': oracle_status},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sirius'},
            {'type': 'land', 'body': 'Sirius Station'},
            {'type': 'complete_cargo_jobs'},
            {'type': 'sell_commodity_lot', 'commodity': 'food', 'sourceLabel': source_label, 'oracleStatus': oracle_status},
            {'type': 'evaluate_trade_margin', 'commodity': 'equipment', 'destinationSystem': 'Sol', 'sourceLabel': source_label, 'oracleStatus': oracle_status},
            {'type': 'accept_cargo_job', 'id': 'freeport_return_earth', 'destinationSystem': 'Sol', 'destinationBody': 'Earth', 'tons': 5, 'pay': 3200, 'setsFlags': ['return_contract_started'], 'completionFlags': ['chapter_one_complete', 'federation_independent_bridge'], 'sourceLabel': source_label, 'oracleStatus': oracle_status},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'complete_cargo_jobs'},
        ]
    if name == 'mission_abort_releases_reserved_cargo':
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'accept_manifest_mission', 'missionId': 'intro_courier_earth_hera'},
            {'type': 'abort_active_mission', 'missionId': 'intro_courier_earth_hera'},
        ]
    if name == 'mission_abort_reaccept_delivery_loop':
        source_label = 'terminal-velocity-mission-abort-reaccept-scaffold'
        oracle_status = 'mission_abort_reaccept_pending_classic_runtime_or_manual_trace'
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'accept_cargo_job', 'id': 'intro_courier_earth_hera', 'destinationSystem': 'Centauri', 'destinationBody': 'Luna', 'tons': 3, 'pay': 1800, 'setsFlags': ['story_intro_started'], 'completionFlags': ['story_intro_complete', 'federation_trusted_courier'], 'sourceLabel': source_label, 'oracleStatus': oracle_status},
            {'type': 'abort_active_mission', 'missionId': 'intro_courier_earth_hera'},
            {'type': 'accept_cargo_job', 'id': 'intro_courier_earth_hera', 'destinationSystem': 'Centauri', 'destinationBody': 'Luna', 'tons': 3, 'pay': 1800, 'setsFlags': ['story_intro_started'], 'completionFlags': ['story_intro_complete', 'federation_trusted_courier'], 'sourceLabel': source_label, 'oracleStatus': oracle_status},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Centauri'},
            {'type': 'land', 'body': 'Luna'},
            {'type': 'complete_cargo_jobs'},
        ]
    if name == 'mission_deadline_failure_scaffold':
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {
                'type': 'accept_cargo_job',
                'id': 'deadline_dispatch_failure_probe',
                'destinationSystem': 'Centauri',
                'destinationBody': 'Luna',
                'tons': 3,
                'pay': 1800,
                'timeLimitDays': 2,
                'completionGovernment': 'Federation',
                'completionReward': 6,
                'failureBitSet': 42,
                'risk': 'deadline',
            },
            {'type': 'advance_days', 'days': 3},
        ]
    if name == 'outfitter_ship_ladder_intro':
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'buy_outfit_or_weapon', 'itemId': 'cargo_pod'},
            {'type': 'buy_outfit_or_weapon', 'itemId': 'laser_cannon'},
            {'type': 'set_state', 'values': {'credits': 60000}},
            {'type': 'buy_ship', 'shipId': 'light_freighter'},
        ]
    if name == 'repair_service_recovery_loop':
        return [
            {'type': 'depart'},
            {'type': 'set_state', 'values': {'currentHull': 65}},
            {'type': 'repair_hull', 'expectBlocked': True},
            {'type': 'land', 'body': START_BODY},
            {'type': 'repair_hull', 'expectBlocked': True},
            {'type': 'depart'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'repair_hull'},
        ]
    if name == 'disabled_player_recovery_loop':
        return [
            {'type': 'depart'},
            {'type': 'disable_player'},
            {'type': 'attempt_disabled_action', 'action': 'jump', 'expectBlocked': True},
            {'type': 'attempt_disabled_action', 'action': 'fire_primary', 'expectBlocked': True},
            {'type': 'attempt_disabled_action', 'action': 'accept_mission', 'expectBlocked': True},
            {'type': 'recover_disabled_player'},
        ]
    if name == 'system_service_provisioning_scout':
        return [
            {'type': 'scan_station_services', 'system': 'Levo', 'body': 'Levo Spaceport', 'sourceLabel': 'original-runtime-observed'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'scan_station_services', 'system': 'Sol', 'body': 'Earth'},
            {'type': 'scan_station_services', 'system': 'Sol', 'body': 'Stardock Alpha'},
        ]
    if name == 'shift_click_multi_stop_route_queue':
        return [
            {'type': 'append_route_stop', 'destinationSystem': 'Sol', 'sourceLabel': 'original-runtime-observed'},
            {'type': 'append_route_stop', 'destinationSystem': 'Sirius', 'sourceLabel': 'original-runtime-observed'},
            {'type': 'jump'},
        ]
    if name == 'route_queue_invalid_stop_guardrail':
        return [
            {'type': 'append_route_stop', 'destinationSystem': 'Sol', 'sourceLabel': 'original-runtime-observed'},
            {'type': 'append_route_stop', 'destinationSystem': 'Levo', 'sourceLabel': 'terminal-velocity-route-guardrail'},
            {'type': 'append_route_stop', 'destinationSystem': 'Antares', 'sourceLabel': 'terminal-velocity-route-guardrail'},
        ]
    if name == 'route_queue_clear_guardrail':
        return [
            {'type': 'append_route_stop', 'destinationSystem': 'Sol', 'sourceLabel': 'original-runtime-observed'},
            {'type': 'append_route_stop', 'destinationSystem': 'Sirius', 'sourceLabel': 'original-runtime-observed'},
            {'type': 'clear_route_queue', 'sourceLabel': 'terminal-velocity-route-guardrail'},
            {'type': 'jump', 'expectBlocked': True},
        ]
    if name == 'route_queue_clear_reselect_guardrail':
        return [
            {'type': 'append_route_stop', 'destinationSystem': 'Sol', 'sourceLabel': 'original-runtime-observed'},
            {'type': 'append_route_stop', 'destinationSystem': 'Sirius', 'sourceLabel': 'original-runtime-observed'},
            {'type': 'clear_route_queue', 'sourceLabel': 'terminal-velocity-route-guardrail'},
            {'type': 'jump', 'expectBlocked': True},
            {'type': 'append_route_stop', 'destinationSystem': 'Sol', 'sourceLabel': 'terminal-velocity-route-guardrail'},
            {'type': 'jump'},
        ]
    if name == 'near_center_jump_block':
        return [
            {'type': 'append_route_stop', 'destinationSystem': 'Sol', 'sourceLabel': 'original-runtime-observed'},
            {'type': 'set_state', 'values': {'distanceFromSystemCenter': 0}},
            {'type': 'jump', 'expectBlocked': True},
        ]
    if name == 'route_planner_refuel_loop':
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'set_state', 'values': {'fuel': 0}},
            {'type': 'jump', 'destinationSystem': 'Levo', 'expectBlocked': True},
            {'type': 'refuel'},
        ]
    if name == 'low_fuel_jump_recovery':
        return [
            {'type': 'set_state', 'values': {'fuel': 0}},
            {'type': 'jump', 'destinationSystem': 'Sol', 'expectBlocked': True},
            {'type': 'refuel'},
        ]
    if name == 'blocked_reason_curriculum':
        return [
            {'type': 'depart'},
            {'type': 'buy_commodity_lot', 'commodity': 'food', 'expectBlocked': True},
            {'type': 'land', 'body': START_BODY},
            {'type': 'set_state', 'values': {'cargoUsed': 15}},
            {'type': 'buy_commodity_lot', 'commodity': 'food', 'expectBlocked': True},
            {'type': 'set_state', 'values': {'cargoUsed': 0, 'credits': 0}},
            {'type': 'buy_commodity_lot', 'commodity': 'medical', 'expectBlocked': True},
            {'type': 'set_state', 'values': {'credits': STARTING_CREDITS}},
            {'type': 'jump', 'destinationSystem': 'Antares', 'expectBlocked': True},
            {'type': 'complete_cargo_jobs', 'expectBlocked': True},
        ]
    if name == 'contraband_scan_clemency_recovery':
        return [
            {'type': 'set_state', 'values': {'currentSystem': 'Sol', 'landedBody': 'Earth', 'cargoHold': {'equipment': 2}, 'cargoUsed': 2, 'credits': 5000, 'reputation': {'Federation': 15, 'Independent': 7}, 'legalRecords': {'Federation': -30, 'Independent': 0}}},
            {'type': 'apply_contraband_scan', 'government': 'Federation'},
            {'type': 'pay_legal_clemency', 'government': 'Federation'},
        ]
    if name == 'pirate_avoidance_escape_route':
        return [
            {'type': 'depart'},
            {'type': 'avoid_pirate_contact', 'threat': 'pirate_intercept', 'safeDestinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
        ]
    if name == 'disposable_combat_placeholder':
        return [
            {'type': 'combat_placeholder_guardrail'},
        ]
    raise ValueError(f'unknown scenario {name}')


def _scenario_checks(name: str, state: dict[str, Any], trace: list[dict[str, Any]], all_actions_valid: bool) -> dict[str, str]:
    event_types = [event['type'] for event in trace]
    checks = {'all_actions_valid': 'passed' if all_actions_valid else 'failed'}
    if name == 'levo_merchant_first_hop':
        checks.update({
            'started_at_levo': 'passed' if trace and trace[0].get('currentSystem') == START_SYSTEM else 'failed',
            'bought_commodity_lot': 'passed' if 'buy_commodity_lot' in event_types else 'failed',
            'accepted_safe_cargo_job': 'passed' if any(event.get('type') == 'accept_cargo_job' and event.get('risk') == 'safe' for event in trace) else 'failed',
            'reached_neighbor_and_landed': 'passed' if state.get('currentSystem') == 'Sol' and state.get('landedBody') == 'Earth' else 'failed',
            'completed_safe_cargo_job': 'passed' if 'complete_cargo_job' in event_types and not state.get('activeJobs') else 'failed',
        })
    elif name == 'levo_same_port_sellback_loop':
        checks.update({
            'bought_original_observed_levo_lot': 'passed' if any(event.get('type') == 'buy_commodity_lot' and event.get('system') == START_SYSTEM and event.get('body') == START_BODY and event.get('commodity') == 'food' and event.get('tons') == COMMODITY_LOT_SIZE and event.get('unitPrice') == 120 for event in trace) else 'failed',
            'sold_same_port_lot_back': 'passed' if any(event.get('type') == 'sell_commodity_lot' and event.get('system') == START_SYSTEM and event.get('body') == START_BODY and event.get('commodity') == 'food' and event.get('tons') == COMMODITY_LOT_SIZE and event.get('unitPrice') == 120 and event.get('sourceLabel') == 'original-runtime-observed' for event in trace) else 'failed',
            'restored_starting_trade_state': 'passed' if state.get('credits') == STARTING_CREDITS and state.get('cargoUsed') == 0 and int(state.get('cargoHold', {}).get('food', 0)) == 0 else 'failed',
        })
    elif name == 'commodity_sell_blocked_recovery_loop':
        blocked_reasons = [event.get('reason') for event in trace if event.get('type') == 'blocked_sell_commodity_lot']
        blocked_sell_events = [event for event in trace if event.get('type') == 'blocked_sell_commodity_lot']
        checks.update({
            'blocked_sell_without_hold': 'passed' if 'insufficient commodity in hold' in blocked_reasons else 'failed',
            'blocked_sell_while_in_space': 'passed' if 'not landed' in blocked_reasons else 'failed',
            'recovered_by_landing_and_selling': 'passed' if any(event.get('type') == 'sell_commodity_lot' and event.get('commodity') == 'food' and event.get('tons') == COMMODITY_LOT_SIZE for event in trace) and state.get('credits') == STARTING_CREDITS and state.get('cargoUsed') == 0 and int(state.get('cargoHold', {}).get('food', 0)) == 0 else 'failed',
            'recorded_sell_guardrail_source_boundary': 'passed' if blocked_sell_events and all(event.get('sourceLabel') == 'terminal-velocity-trade-scaffold' and event.get('oracleStatus') == 'commodity_sell_guardrail_pending_original_runtime_trace' for event in blocked_sell_events) else 'failed',
        })
    elif name == 'commodity_buy_blocked_recovery_loop':
        blocked_reasons = [event.get('reason') for event in trace if event.get('type') == 'blocked_buy_commodity_lot']
        blocked_buy_events = [event for event in trace if event.get('type') == 'blocked_buy_commodity_lot']
        checks.update({
            'blocked_buy_while_in_space': 'passed' if 'not landed' in blocked_reasons else 'failed',
            'blocked_buy_without_credits': 'passed' if 'insufficient credits' in blocked_reasons else 'failed',
            'blocked_buy_without_capacity': 'passed' if 'insufficient cargo space' in blocked_reasons else 'failed',
            'recovered_by_landing_and_buying': 'passed' if any(event.get('type') == 'buy_commodity_lot' and event.get('commodity') == 'food' and event.get('tons') == COMMODITY_LOT_SIZE for event in trace) and state.get('credits') == STARTING_CREDITS - (120 * COMMODITY_LOT_SIZE) and state.get('cargoUsed') == COMMODITY_LOT_SIZE and int(state.get('cargoHold', {}).get('food', 0)) == COMMODITY_LOT_SIZE else 'failed',
            'recorded_buy_guardrail_source_boundary': 'passed' if blocked_buy_events and all(event.get('sourceLabel') == 'terminal-velocity-trade-scaffold' and event.get('oracleStatus') == 'commodity_buy_guardrail_pending_original_runtime_trace' for event in blocked_buy_events) else 'failed',
        })
    elif name == 'cross_market_trade_spread_scout':
        trade_events = [event for event in trace if event.get('type') in {'buy_commodity_lot', 'sell_commodity_lot'}]
        checks.update({
            'bought_low_at_sol': 'passed' if any(event.get('type') == 'buy_commodity_lot' and event.get('system') == 'Sol' and event.get('body') == 'Earth' and event.get('commodity') == 'food' and event.get('unitPrice') == 42 for event in trade_events) else 'failed',
            'sold_high_at_levo': 'passed' if any(event.get('type') == 'sell_commodity_lot' and event.get('system') == START_SYSTEM and event.get('body') == START_BODY and event.get('commodity') == 'food' and event.get('unitPrice') == 120 for event in trade_events) else 'failed',
            'returned_to_levo_with_profit': 'passed' if state.get('currentSystem') == START_SYSTEM and state.get('landedBody') == START_BODY and state.get('credits') == STARTING_CREDITS + ((120 - 42) * COMMODITY_LOT_SIZE) and state.get('cargoUsed') == 0 and int(state.get('cargoHold', {}).get('food', 0)) == 0 else 'failed',
            'recorded_cross_market_source_boundary': 'passed' if trade_events and all(event.get('sourceLabel') == 'terminal-velocity-cross-market-trade-scaffold' and event.get('oracleStatus') == 'classic_runtime_cross_market_spread_pending' for event in trade_events) else 'failed',
        })
    elif name == 'max_hold_trade_route_scout':
        trade_events = [event for event in trace if event.get('type') in {'buy_commodity_lot', 'sell_commodity_lot'}]
        buy_events = [event for event in trade_events if event.get('type') == 'buy_commodity_lot']
        sell_events = [event for event in trade_events if event.get('type') == 'sell_commodity_lot']
        checks.update({
            'filled_hold_with_two_sol_lots': 'passed' if len(buy_events) == 2 and all(event.get('system') == 'Sol' and event.get('body') == 'Earth' and event.get('commodity') == 'food' and event.get('unitPrice') == 42 for event in buy_events) and max(int(event.get('cargoUsed', 0)) for event in buy_events) == STARTING_CARGO_CAPACITY else 'failed',
            'sold_two_lots_at_levo': 'passed' if len(sell_events) == 2 and all(event.get('system') == START_SYSTEM and event.get('body') == START_BODY and event.get('commodity') == 'food' and event.get('unitPrice') == 120 for event in sell_events) else 'failed',
            'returned_to_levo_with_full_hold_profit': 'passed' if state.get('currentSystem') == START_SYSTEM and state.get('landedBody') == START_BODY and state.get('credits') == STARTING_CREDITS + (2 * (120 - 42) * COMMODITY_LOT_SIZE) and state.get('cargoUsed') == 0 and int(state.get('cargoHold', {}).get('food', 0)) == 0 else 'failed',
            'recorded_max_hold_trade_source_boundary': 'passed' if trade_events and all(event.get('sourceLabel') == 'terminal-velocity-max-hold-trade-scaffold' and event.get('oracleStatus') == 'classic_runtime_multi_lot_trade_spread_pending' for event in trade_events) else 'failed',
        })
    elif name == 'trade_route_refuel_profit_loop':
        trade_events = [event for event in trace if event.get('type') in {'buy_commodity_lot', 'sell_commodity_lot'}]
        blocked_jumps = [event for event in trace if event.get('type') == 'blocked_jump']
        checks.update({
            'blocked_profit_route_on_low_fuel': 'passed' if any(event.get('destinationSystem') == START_SYSTEM and event.get('reason') == 'insufficient fuel' for event in blocked_jumps) else 'failed',
            'refueled_before_return_leg': 'passed' if any(event.get('type') == 'refuel' and event.get('system') == 'Sol' and event.get('body') == 'Earth' and event.get('fuelAfter') == STARTING_FUEL for event in trace) else 'failed',
            'completed_refueled_trade_profit': 'passed' if state.get('currentSystem') == START_SYSTEM and state.get('landedBody') == START_BODY and state.get('credits') == STARTING_CREDITS + (2 * (120 - 42) * COMMODITY_LOT_SIZE) and state.get('cargoUsed') == 0 and int(state.get('cargoHold', {}).get('food', 0)) == 0 else 'failed',
            'recorded_refuel_trade_source_boundary': 'passed' if trade_events and all(event.get('sourceLabel') == 'terminal-velocity-refuel-trade-route-scaffold' and event.get('oracleStatus') == 'classic_runtime_refuel_trade_route_pending' for event in trade_events) else 'failed',
        })
    elif name == 'mission_runner_first_delivery':
        checks.update({
            'accepted_reserved_cargo_job': 'passed' if any(event.get('type') == 'accept_cargo_job' and event.get('reservedCargoTons') == 8 for event in trace) else 'failed',
            'reached_destination': 'passed' if state.get('currentSystem') == 'Centauri' and state.get('landedBody') == 'Landfall' else 'failed',
            'completed_delivery': 'passed' if state.get('completedJobs') == ['levo_landfall_courier'] and not state.get('activeJobs') else 'failed',
            'released_reserved_cargo': 'passed' if state.get('cargoUsed') == 0 else 'failed',
        })
    elif name == 'intro_courier_mission_delivery':
        checks.update({
            'accepted_intro_courier': 'passed' if any(event.get('type') == 'accept_cargo_job' and event.get('id') == 'intro_courier_earth_hera' and event.get('originSystem') == 'Sol' and event.get('originBody') == 'Earth' and event.get('reservedCargoTons') == 3 for event in trace) else 'failed',
            'reached_intro_destination': 'passed' if state.get('currentSystem') == 'Centauri' and state.get('landedBody') == 'Luna' else 'failed',
            'completed_intro_courier': 'passed' if state.get('completedJobs') == ['intro_courier_earth_hera'] and not state.get('activeJobs') and state.get('credits') == STARTING_CREDITS + 1800 else 'failed',
            'released_intro_cargo': 'passed' if state.get('cargoUsed') == 0 else 'failed',
            'applied_story_flags': 'passed' if {'story_intro_started', 'story_intro_complete', 'federation_trusted_courier'}.issubset(set(state.get('storyFlags', []))) else 'failed',
        })
    elif name == 'scan_intro_mission_offers':
        checks.update({
            'archived_mission_offers': 'passed' if state.get('missionOfferArchive', {}).get('Sol/Earth', {}).get('Mission Computer') == ['intro_courier_earth_hera'] else 'failed',
        })
    elif name == 'chapter_one_courier_chain':
        expected_jobs = ['intro_courier_earth_hera', 'frontier_sample_hera_freeport', 'freeport_return_earth']
        expected_flags = {'story_intro_complete', 'frontier_samples_delivered', 'chapter_one_complete', 'federation_independent_bridge'}
        checks.update({
            'completed_intro_frontier_return_chain': 'passed' if state.get('completedJobs') == expected_jobs and not state.get('activeJobs') and state.get('cargoUsed') == 0 and state.get('credits') == STARTING_CREDITS + 1800 + 2400 + 3200 and expected_flags.issubset(set(state.get('storyFlags', []))) else 'failed',
        })
    elif name == 'alignment_choice_guardrail':
        active_ids = [job['id'] for job in state.get('activeJobs', [])]
        checks.update({
            'blocked_mutually_exclusive_alignment': 'passed' if 'federation_report_freeport' in active_ids and 'freeport_pact_smugglers' not in active_ids and 'alignment_federation' in state.get('storyFlags', []) and 'alignment_freeport' not in state.get('storyFlags', []) and any(event.get('type') == 'blocked_manifest_mission' and event.get('missionId') == 'freeport_pact_smugglers' for event in trace) else 'failed',
        })
    elif name == 'federation_alignment_delivery_loop':
        checks.update({
            'completed_federation_alignment_delivery': 'passed' if state.get('completedJobs') == ['federation_report_freeport'] and not state.get('activeJobs') and state.get('credits') == STARTING_CREDITS + 2800 and state.get('cargoUsed') == 0 else 'failed',
            'preserved_federation_alignment_flags': 'passed' if {'frontier_samples_delivered', 'chapter_one_choice_seen', 'alignment_federation', 'federation_intel_asset'}.issubset(set(state.get('storyFlags', []))) and 'alignment_freeport' not in state.get('storyFlags', []) else 'failed',
            'blocked_freeport_branch_after_federation_completion': 'passed' if any(event.get('type') == 'blocked_manifest_mission' and event.get('missionId') == 'freeport_pact_smugglers' for event in trace) else 'failed',
            'recorded_alignment_delivery_source_boundary': 'passed' if any(event.get('type') == 'accept_cargo_job' and event.get('id') == 'federation_report_freeport' and event.get('sourceLabel') == 'terminal-velocity-mission-scaffold' and event.get('oracleStatus') == 'mission_behavior_pending_classic_runtime_trace' for event in trace) else 'failed',
        })
    elif name == 'mission_destination_route_hint':
        checks.update({
            'queued_active_mission_destination': 'passed' if state.get('currentSystem') == 'Sol' and state.get('routeQueue') == ['Centauri'] and any(event.get('type') == 'route_to_active_mission_destination' and event.get('missionId') == 'intro_courier_earth_hera' and event.get('destinationSystem') == 'Centauri' and event.get('routeQueued') for event in trace) else 'failed',
        })
    elif name == 'mission_trade_hybrid_capacity_planning':
        checks.update({
            'accepted_trade_aligned_mission': 'passed' if any(event.get('type') == 'accept_cargo_job' and event.get('id') == 'levo_trade_aligned_courier' and event.get('reservedCargoTons') == 8 for event in trace) else 'failed',
            'bought_one_trade_lot_with_remaining_capacity': 'passed' if any(event.get('type') == 'buy_commodity_lot' and event.get('commodity') == 'food' and event.get('cargoUsed') == 18 for event in trace) else 'failed',
            'blocked_second_lot_to_preserve_capacity_rule': 'passed' if any(event.get('type') == 'blocked_buy_commodity_lot' and event.get('commodity') == 'industrial' and event.get('reason') == 'insufficient cargo space' for event in trace) else 'failed',
            'completed_mission_with_trade_cargo_still_held': 'passed' if state.get('completedJobs') == ['levo_trade_aligned_courier'] and state.get('cargoUsed') == 10 and state.get('cargoHold', {}).get('food') == 10 else 'failed',
        })
    elif name == 'mission_trade_refuel_delivery_loop':
        mission_trade_events = [event for event in trace if event.get('type') in {'buy_commodity_lot', 'complete_cargo_job'}]
        checks.update({
            'accepted_intro_mission_and_trade_lot': 'passed' if any(event.get('type') == 'accept_cargo_job' and event.get('id') == 'intro_courier_earth_hera' and event.get('reservedCargoTons') == 3 for event in trace) and any(event.get('type') == 'buy_commodity_lot' and event.get('system') == 'Sol' and event.get('commodity') == 'food' and event.get('cargoUsed') == 13 for event in trace) else 'failed',
            'blocked_delivery_leg_on_low_fuel': 'passed' if any(event.get('type') == 'blocked_jump' and event.get('destinationSystem') == 'Centauri' and event.get('reason') == 'insufficient fuel' for event in trace) else 'failed',
            'refueled_before_delivery_leg': 'passed' if any(event.get('type') == 'refuel' and event.get('system') == 'Sol' and event.get('body') == 'Earth' and event.get('fuelAfter') == STARTING_FUEL for event in trace) else 'failed',
            'completed_delivery_with_trade_cargo_held': 'passed' if state.get('currentSystem') == 'Centauri' and state.get('landedBody') == 'Luna' and state.get('completedJobs') == ['intro_courier_earth_hera'] and state.get('cargoUsed') == COMMODITY_LOT_SIZE and int(state.get('cargoHold', {}).get('food', 0)) == COMMODITY_LOT_SIZE and state.get('credits') == STARTING_CREDITS - (42 * COMMODITY_LOT_SIZE) + 1800 else 'failed',
            'recorded_mission_trade_refuel_source_boundary': 'passed' if mission_trade_events and all(event.get('sourceLabel') == 'terminal-velocity-mission-trade-refuel-scaffold' and event.get('oracleStatus') == 'mission_trade_refuel_pending_classic_runtime_trace' for event in mission_trade_events) else 'failed',
        })
    elif name == 'mission_trade_destination_sale_loop':
        mission_trade_events = [event for event in trace if event.get('type') in {'buy_commodity_lot', 'sell_commodity_lot', 'complete_cargo_job'}]
        checks.update({
            'accepted_intro_mission_and_trade_lot': 'passed' if any(event.get('type') == 'accept_cargo_job' and event.get('id') == 'intro_courier_earth_hera' and event.get('reservedCargoTons') == 3 for event in trace) and any(event.get('type') == 'buy_commodity_lot' and event.get('system') == 'Sol' and event.get('commodity') == 'food' and event.get('cargoUsed') == 13 for event in trace) else 'failed',
            'delivered_mission_before_trade_sale': 'passed' if any(event.get('type') == 'complete_cargo_job' and event.get('id') == 'intro_courier_earth_hera' for event in trace) and state.get('completedJobs') == ['intro_courier_earth_hera'] else 'failed',
            'sold_trade_cargo_at_destination_market': 'passed' if any(event.get('type') == 'sell_commodity_lot' and event.get('system') == 'Centauri' and event.get('body') == 'Luna' and event.get('commodity') == 'food' and event.get('unitPrice') == 49 and event.get('cargoUsed') == 0 for event in trace) and state.get('cargoUsed') == 0 and int(state.get('cargoHold', {}).get('food', 0)) == 0 and state.get('credits') == STARTING_CREDITS - (42 * COMMODITY_LOT_SIZE) + 1800 + (49 * COMMODITY_LOT_SIZE) else 'failed',
            'recorded_destination_sale_source_boundary': 'passed' if mission_trade_events and all(event.get('sourceLabel') == 'terminal-velocity-mission-trade-destination-sale-scaffold' and event.get('oracleStatus') == 'mission_trade_destination_sale_pending_classic_runtime_trace' for event in mission_trade_events) else 'failed',
        })
    elif name == 'chapter_one_trade_carryover_loop':
        mission_trade_events = [event for event in trace if event.get('type') in {'accept_cargo_job', 'buy_commodity_lot', 'sell_commodity_lot', 'complete_cargo_job'}]
        checks.update({
            'completed_two_missions_with_trade_cargo_reserved_alongside': 'passed' if state.get('completedJobs') == ['intro_courier_earth_hera', 'frontier_sample_hera_freeport'] and any(event.get('type') == 'accept_cargo_job' and event.get('id') == 'frontier_sample_hera_freeport' and event.get('cargoUsed') == 14 for event in trace) else 'failed',
            'carried_trade_lot_across_story_chain': 'passed' if any(event.get('type') == 'complete_cargo_job' and event.get('id') == 'frontier_sample_hera_freeport' for event in trace) and any(event.get('type') == 'sell_commodity_lot' and event.get('system') == 'Sirius' and event.get('body') == 'Sirius Station' and event.get('commodity') == 'food' and event.get('unitPrice') == 62 for event in trace) else 'failed',
            'sold_carried_trade_cargo_after_second_delivery': 'passed' if state.get('currentSystem') == 'Sirius' and state.get('landedBody') == 'Sirius Station' and state.get('cargoUsed') == 0 and int(state.get('cargoHold', {}).get('food', 0)) == 0 and state.get('credits') == STARTING_CREDITS - (42 * COMMODITY_LOT_SIZE) + 1800 + 2400 + (62 * COMMODITY_LOT_SIZE) else 'failed',
            'recorded_chapter_trade_carryover_source_boundary': 'passed' if mission_trade_events and all(event.get('sourceLabel') == 'terminal-velocity-chapter-one-trade-carryover-scaffold' and event.get('oracleStatus') == 'chapter_one_trade_carryover_pending_classic_runtime_trace' for event in mission_trade_events) else 'failed',
        })
    elif name == 'mission_trade_return_margin_guardrail':
        source_events = [event for event in trace if event.get('type') in {'accept_cargo_job', 'buy_commodity_lot', 'sell_commodity_lot', 'complete_cargo_job', 'trade_margin_decision'}]
        checks.update({
            'completed_return_contract_after_trade_sale': 'passed' if state.get('currentSystem') == 'Sol' and state.get('landedBody') == 'Earth' and state.get('completedJobs') == ['intro_courier_earth_hera', 'frontier_sample_hera_freeport', 'freeport_return_earth'] and state.get('cargoUsed') == 0 and state.get('credits') == STARTING_CREDITS - (42 * COMMODITY_LOT_SIZE) + 1800 + 2400 + (62 * COMMODITY_LOT_SIZE) + 3200 else 'failed',
            'blocked_negative_margin_return_trade': 'passed' if any(event.get('type') == 'trade_margin_decision' and event.get('commodity') == 'equipment' and event.get('originSystem') == 'Sirius' and event.get('destinationSystem') == 'Sol' and event.get('marginPerTon') == -10 and event.get('decision') == 'skip' for event in trace) else 'failed',
            'recorded_return_margin_source_boundary': 'passed' if source_events and all(event.get('sourceLabel') == 'terminal-velocity-mission-trade-return-margin-scaffold' and event.get('oracleStatus') == 'chapter_one_return_trade_margin_pending_classic_runtime_trace' for event in source_events) else 'failed',
        })
    elif name == 'mission_abort_releases_reserved_cargo':
        checks.update({
            'accepted_abort_test_mission': 'passed' if any(event.get('type') == 'accept_cargo_job' and event.get('id') == 'intro_courier_earth_hera' and event.get('reservedCargoTons') == 3 for event in trace) else 'failed',
            'aborted_active_mission': 'passed' if any(event.get('type') == 'abort_mission' and event.get('missionId') == 'intro_courier_earth_hera' for event in trace) and not state.get('activeJobs') else 'failed',
            'released_aborted_mission_cargo': 'passed' if state.get('cargoUsed') == 0 else 'failed',
            'recorded_abort_source_boundary': 'passed' if any(event.get('type') == 'abort_mission' and event.get('sourceLabel') == 'terminal-velocity-mission-abort-scaffold' and 'pending_classic' in event.get('oracleStatus', '') for event in trace) else 'failed',
        })
    elif name == 'mission_abort_reaccept_delivery_loop':
        mission_events = [event for event in trace if event.get('type') in {'accept_cargo_job', 'abort_mission', 'complete_cargo_job'}]
        accepts = [event for event in trace if event.get('type') == 'accept_cargo_job' and event.get('id') == 'intro_courier_earth_hera']
        checks.update({
            'aborted_first_attempt': 'passed' if any(event.get('type') == 'abort_mission' and event.get('missionId') == 'intro_courier_earth_hera' and event.get('releasedCargoTons') == 3 for event in trace) and state.get('abortedJobs') == ['intro_courier_earth_hera'] else 'failed',
            'reaccepted_after_abort': 'passed' if len(accepts) == 2 and accepts[-1].get('reservedCargoTons') == 3 else 'failed',
            'delivered_reaccepted_mission': 'passed' if state.get('currentSystem') == 'Centauri' and state.get('landedBody') == 'Luna' and state.get('completedJobs') == ['intro_courier_earth_hera'] and state.get('activeJobs') == [] and state.get('cargoUsed') == 0 and state.get('credits') == STARTING_CREDITS + 1800 else 'failed',
            'recorded_abort_reaccept_source_boundary': 'passed' if mission_events and all(event.get('sourceLabel') in {'terminal-velocity-mission-abort-reaccept-scaffold', 'terminal-velocity-mission-abort-scaffold'} and 'pending_classic' in event.get('oracleStatus', '') for event in mission_events) else 'failed',
        })
    elif name == 'mission_deadline_failure_scaffold':
        checks.update({
            'accepted_deadline_mission': 'passed' if any(event.get('type') == 'accept_cargo_job' and event.get('id') == 'deadline_dispatch_failure_probe' and event.get('timeLimitDays') == 2 for event in trace) else 'failed',
            'expired_after_deadline': 'passed' if any(event.get('type') == 'mission_deadline_failure' and event.get('missionId') == 'deadline_dispatch_failure_probe' and event.get('currentDay') == 3 for event in trace) else 'failed',
            'released_failed_mission_cargo': 'passed' if state.get('cargoUsed') == 0 and not state.get('activeJobs') else 'failed',
            'recorded_failure_bit_and_reputation_penalty': 'passed' if 'fail_mission_bit_42' in state.get('storyFlags', []) and state.get('reputation', {}).get('Federation') == 2 else 'failed',
            'recorded_deadline_source_boundary': 'passed' if any(event.get('type') == 'mission_deadline_failure' and event.get('sourceLabel') == 'ev-classic-resource-bible-backed-mission-failure-scaffold' and event.get('oracleStatus') == 'deadline_failure_runtime_ui_pending_classic_trace' for event in trace) else 'failed',
        })
    elif name == 'outfitter_ship_ladder_intro':
        checks.update({
            'bought_first_outfit': 'passed' if state.get('ownedOutfits', {}).get('cargo_pod') == 1 and any(event.get('type') == 'buy_outfit_or_weapon' and event.get('saleType') == 'outfit' and event.get('itemId') == 'cargo_pod' for event in trace) else 'failed',
            'bought_first_weapon': 'passed' if state.get('ownedWeapons', {}).get('laser_cannon') == 1 and any(event.get('type') == 'buy_outfit_or_weapon' and event.get('saleType') == 'weapon' and event.get('itemId') == 'laser_cannon' for event in trace) else 'failed',
            'upgraded_to_larger_ship': 'passed' if state.get('playerShipId') == 'light_freighter' and any(event.get('type') == 'buy_ship' and event.get('previousShipId') == 'shuttlecraft' and int(event.get('cargoCapacityAfter', 0)) > int(event.get('cargoCapacityBefore', 0)) for event in trace) else 'failed',
            'recorded_outfitter_ship_ladder_source_boundary': 'passed' if all(event.get('sourceLabel') == 'terminal-velocity-outfitter-ship-ladder-scaffold' and 'pending_original' in event.get('oracleStatus', '') for event in trace if event.get('type') in {'buy_outfit_or_weapon', 'buy_ship'}) else 'failed',
        })
    elif name == 'repair_service_recovery_loop':
        checks.update({
            'blocked_in_space_repair': 'passed' if any(event.get('type') == 'blocked_repair_hull' and event.get('reason') == 'not landed' for event in trace) else 'failed',
            'blocked_no_service_repair': 'passed' if any(event.get('type') == 'blocked_repair_hull' and event.get('reason') == 'repair service unavailable' and event.get('body') == START_BODY for event in trace) else 'failed',
            'repaired_hull_at_service_port': 'passed' if state.get('currentSystem') == 'Sol' and state.get('landedBody') == 'Earth' and state.get('currentHull') == state.get('maxHull') and any(event.get('type') == 'repair_hull' and event.get('body') == 'Earth' and event.get('hullBefore') == 65 and event.get('hullAfter') == event.get('maxHull') for event in trace) else 'failed',
            'recorded_repair_source_boundary': 'passed' if all(event.get('sourceLabel') == 'terminal-velocity-repair-service-scaffold' and event.get('oracleStatus') == 'repair_service_pending_ev_classic_runtime_trace' for event in trace if event.get('type') in {'blocked_repair_hull', 'repair_hull'}) else 'failed',
        })
    elif name == 'disabled_player_recovery_loop':
        disabled_events = [event for event in trace if event.get('type') in {'disable_player', 'blocked_disabled_action', 'recover_disabled_player'}]
        checks.update({
            'disabled_player_recorded': 'passed' if any(event.get('type') == 'disable_player' and event.get('currentHull') == 0 and event.get('playerDisabled') is True for event in trace) else 'failed',
            'blocked_disabled_actions': 'passed' if [event.get('action') for event in trace if event.get('type') == 'blocked_disabled_action'] == ['jump', 'fire_primary', 'accept_mission'] else 'failed',
            'recovered_player_scaffold': 'passed' if state.get('playerDisabled') is False and state.get('currentHull') == state.get('maxHull') and any(event.get('type') == 'recover_disabled_player' and event.get('hullAfter') == state.get('maxHull') for event in trace) else 'failed',
            'recorded_disabled_recovery_source_boundary': 'passed' if disabled_events and all(event.get('sourceLabel') == 'terminal-velocity-player-disabled-scaffold' and event.get('oracleStatus') == 'classic_runtime_player_death_pending_strict_play_safe_trace' for event in disabled_events) else 'failed',
        })
    elif name == 'system_service_provisioning_scout':
        scans = {(event.get('system'), event.get('body')): event for event in trace if event.get('type') == 'scan_station_services'}
        levo = scans.get(('Levo', 'Levo Spaceport'), {})
        earth = scans.get(('Sol', 'Earth'), {})
        stardock = scans.get(('Sol', 'Stardock Alpha'), {})
        checks.update({
            'confirmed_levo_original_service_boundary': 'passed' if levo.get('hasCommodities') is True and levo.get('hasMissionComputer') is True and levo.get('hasOutfitter') is False and levo.get('hasShipyard') is False and levo.get('sourceLabel') == 'original-runtime-observed' else 'failed',
            'scouted_earth_full_service_scaffold': 'passed' if earth.get('hasRepairs') is True and earth.get('hasOutfitter') is True and earth.get('hasShipyard') is True and earth.get('hasWeapons') is True and bool(earth.get('shipsForSale')) else 'failed',
            'scouted_station_without_shipyard': 'passed' if stardock.get('hasOutfitter') is True and stardock.get('hasWeapons') is True and stardock.get('hasShipyard') is False else 'failed',
            'recorded_service_matrix_source_boundary': 'passed' if all(event.get('sourceLabel') in {'original-runtime-observed', 'terminal-velocity-service-provisioning-scaffold'} and 'pending' in event.get('oracleStatus', '') for event in trace if event.get('type') == 'scan_station_services') else 'failed',
        })
    elif name == 'shift_click_multi_stop_route_queue':
        appended_paths = [event.get('greenRoutePath') for event in trace if event.get('type') == 'append_route_stop']
        checks.update({
            'green_multi_stop_route': 'passed' if appended_paths and appended_paths[-1] == ['Levo', 'Sol', 'Sirius'] and state.get('routeSourceLabel') == 'original-runtime-observed' else 'failed',
            'consumed_first_leg_only': 'passed' if state.get('currentSystem') == 'Sol' and state.get('routeQueue') == ['Sirius'] and any(event.get('type') == 'jump' and event.get('previousRoute') == ['Sol', 'Sirius'] and event.get('remainingRoute') == ['Sirius'] for event in trace) else 'failed',
        })
    elif name == 'route_queue_invalid_stop_guardrail':
        blocked_reasons = [event.get('reason') for event in trace if event.get('type') == 'blocked_append_route_stop']
        checks.update({
            'preserved_valid_route_after_invalid_clicks': 'passed' if state.get('currentSystem') == START_SYSTEM and state.get('routeQueue') == ['Sol'] else 'failed',
            'blocked_duplicate_or_current_system': 'passed' if 'duplicate or current system' in blocked_reasons else 'failed',
            'blocked_unlinked_route_tail_stop': 'passed' if 'not linked from route tail' in blocked_reasons else 'failed',
        })
    elif name == 'route_queue_clear_guardrail':
        checks.update({
            'cleared_multi_stop_route': 'passed' if any(event.get('type') == 'clear_route_queue' and event.get('previousRoute') == ['Sol', 'Sirius'] and event.get('routeQueue') == [] for event in trace) and state.get('routeQueue') == [] else 'failed',
            'blocked_jump_after_clear': 'passed' if any(event.get('type') == 'blocked_jump' and event.get('reason') == 'no destination selected' for event in trace) else 'failed',
            'recorded_clear_source_boundary': 'passed' if any(event.get('type') == 'clear_route_queue' and event.get('sourceLabel') == 'terminal-velocity-route-guardrail' and 'pending_ev_classic_trace' in event.get('oracleStatus', '') for event in trace) else 'failed',
        })
    elif name == 'route_queue_clear_reselect_guardrail':
        checks.update({
            'blocked_jump_after_clear': 'passed' if any(event.get('type') == 'blocked_jump' and event.get('reason') == 'no destination selected' for event in trace) else 'failed',
            'reselected_after_clear': 'passed' if any(event.get('type') == 'append_route_stop' and event.get('destinationSystem') == 'Sol' and event.get('sourceLabel') == 'terminal-velocity-route-guardrail' for event in trace) else 'failed',
            'jumped_after_reselect': 'passed' if state.get('currentSystem') == 'Sol' and state.get('routeQueue') == [] and any(event.get('type') == 'jump' and event.get('previousRoute') == ['Sol'] and event.get('remainingRoute') == [] for event in trace) else 'failed',
        })
    elif name == 'near_center_jump_block':
        checks.update({
            'blocked_near_center_jump': 'passed' if any(event.get('type') == 'blocked_jump' and event.get('reason') == 'too close to system center' and event.get('sourceLabel') == 'original-runtime-observed' for event in trace) else 'failed',
            'preserved_system_after_center_block': 'passed' if state.get('currentSystem') == START_SYSTEM else 'failed',
            'preserved_fuel_after_center_block': 'passed' if state.get('fuel') == STARTING_FUEL else 'failed',
        })
    elif name == 'route_planner_refuel_loop':
        checks.update({
            'spent_fuel_on_jump': 'passed' if any(event.get('type') == 'jump' and event.get('fuelAfter') == STARTING_FUEL - 1 for event in trace) else 'failed',
            'blocked_empty_fuel_jump': 'passed' if any(event.get('type') == 'blocked_jump' and event.get('reason') == 'insufficient fuel' for event in trace) else 'failed',
            'refueled_while_landed': 'passed' if any(event.get('type') == 'refuel' and event.get('fuelAfter') == STARTING_FUEL for event in trace) else 'failed',
        })
    elif name == 'low_fuel_jump_recovery':
        checks.update({
            'started_with_empty_fuel': 'passed' if any(event.get('type') == 'state_adjustment' and event.get('values', {}).get('fuel') == 0 for event in trace) else 'failed',
            'blocked_low_fuel_jump': 'passed' if any(event.get('type') == 'blocked_jump' and event.get('originSystem') == START_SYSTEM and event.get('destinationSystem') == 'Sol' and event.get('reason') == 'insufficient fuel' for event in trace) else 'failed',
            'preserved_system_after_block': 'passed' if state.get('currentSystem') == START_SYSTEM else 'failed',
            'refueled_after_block': 'passed' if any(event.get('type') == 'refuel' and event.get('system') == START_SYSTEM and event.get('fuelAfter') == STARTING_FUEL for event in trace) else 'failed',
        })
    elif name == 'blocked_reason_curriculum':
        checks.update({
            'recorded_not_landed': 'passed' if any(event.get('type') == 'blocked_buy_commodity_lot' and event.get('reason') == 'not landed' for event in trace) else 'failed',
            'recorded_insufficient_cargo': 'passed' if any(event.get('type') == 'blocked_buy_commodity_lot' and event.get('reason') == 'insufficient cargo space' for event in trace) else 'failed',
            'recorded_insufficient_credits': 'passed' if any(event.get('type') == 'blocked_buy_commodity_lot' and event.get('reason') == 'insufficient credits' for event in trace) else 'failed',
            'recorded_invalid_destination': 'passed' if any(event.get('type') == 'blocked_jump' and 'not linked' in event.get('reason', '') for event in trace) else 'failed',
            'recorded_no_deliverable_job': 'passed' if any(event.get('type') == 'blocked_complete_cargo_job' and event.get('reason') == 'no deliverable job at current landing' for event in trace) else 'failed',
        })
    elif name == 'contraband_scan_clemency_recovery':
        scan = next((event for event in trace if event.get('type') == 'contraband_scan'), {})
        clemency = next((event for event in trace if event.get('type') == 'pay_legal_clemency'), {})
        checks.update({
            'confiscated_federation_contraband': 'passed' if scan.get('government') == 'Federation' and scan.get('action') == 'fine' and scan.get('confiscated') == {'equipment': 2} and state.get('cargoHold') == {} and state.get('cargoUsed') == 0 else 'failed',
            'applied_federation_fine_and_legal_penalty': 'passed' if scan.get('creditsDelta') == -800 and scan.get('legalDelta') == -3 else 'failed',
            'paid_clemency_after_scan': 'passed' if clemency.get('government') == 'Federation' and clemency.get('cost') == 1000 and clemency.get('legalDelta') == 25 and state.get('credits') == 3200 and state.get('legalRecords', {}).get('Federation') == -8 else 'failed',
        })
    elif name == 'pirate_avoidance_escape_route':
        checks.update({
            'detected_pirate_threat': 'passed' if any(event.get('type') == 'avoid_pirate_contact' and event.get('threat') == 'pirate_intercept' for event in trace) else 'failed',
            'escaped_without_combat': 'passed' if state.get('combatExecuted') is False and state.get('threatPosture') == 'evaded' and any(event.get('type') == 'jump' and event.get('destinationSystem') == 'Sol' for event in trace) else 'failed',
            'landed_at_safe_port': 'passed' if state.get('currentSystem') == 'Sol' and state.get('landedBody') == 'Earth' else 'failed',
        })
    elif name == 'disposable_combat_placeholder':
        stop_conditions = next((event.get('stopConditions', []) for event in trace if event.get('type') == 'combat_placeholder_guardrail'), [])
        checks.update({
            'strict_play_off': 'passed' if state.get('strictPlay') is False else 'failed',
            'combat_not_executed': 'passed' if state.get('combatExecuted') is False else 'failed',
            'stop_conditions_recorded': 'passed' if {'Strict Play enabled', 'low shields or hull', 'unclear save state'}.issubset(set(stop_conditions)) else 'failed',
        })
    return checks


def run_scripted_scenario(name: str, actions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Run a bounded symbolic scenario and return state, trace, metrics, and checks."""
    state = initial_gameplay_state()
    trace: list[dict[str, Any]] = [{
        'type': 'start',
        'currentSystem': state['currentSystem'],
        'landedBody': state['landedBody'],
        'credits': state['credits'],
        'cargoCapacity': state['cargoCapacity'],
        'strictPlay': state['strictPlay'],
    }]
    handlers = {
        'buy_commodity_lot': _buy_commodity_lot,
        'sell_commodity_lot': _sell_commodity_lot,
        'evaluate_trade_margin': _evaluate_trade_margin,
        'accept_cargo_job': _accept_cargo_job,
        'jump': _jump,
        'land': _land,
        'depart': _depart,
        'refuel': _refuel,
        'repair_hull': _repair_hull,
        'disable_player': _disable_player,
        'attempt_disabled_action': _attempt_disabled_action,
        'recover_disabled_player': _recover_disabled_player,
        'set_state': _set_state,
        'append_route_stop': _append_route_stop,
        'clear_route_queue': _clear_route_queue,
        'scan_station_services': _scan_station_services,
        'route_to_active_mission_destination': _route_to_active_mission_destination,
        'scan_mission_offers': _scan_mission_offers,
        'accept_manifest_mission': _accept_manifest_mission,
        'buy_outfit_or_weapon': _buy_outfit_or_weapon,
        'buy_ship': _buy_ship,
        'avoid_pirate_contact': _avoid_pirate_contact,
        'advance_days': _advance_days,
        'complete_cargo_jobs': _complete_cargo_jobs,
        'abort_active_mission': _abort_active_mission,
        'combat_placeholder_guardrail': _combat_placeholder_guardrail,
        'apply_contraband_scan': _apply_contraband_scan,
        'pay_legal_clemency': _pay_legal_clemency,
    }
    all_actions_valid = True
    for action in actions if actions is not None else default_actions_for_scenario(name):
        action_type = action.get('type')
        if not isinstance(action_type, str):
            trace.append({'type': 'blocked_action', 'reason': f'unknown action {action_type}'})
            all_actions_valid = False
            break
        handler = handlers.get(action_type)
        if handler is None:
            trace.append({'type': 'blocked_action', 'reason': f'unknown action {action_type}'})
            all_actions_valid = False
            break
        action_ok = handler(state, action, trace)
        if not action_ok:
            if action.get('expectBlocked') is True:
                continue
            all_actions_valid = False
            break
    checks = _scenario_checks(name, state, trace, all_actions_valid)
    success = all(value == 'passed' for value in checks.values())
    return {
        'scenario': name,
        'success': success,
        'state': deepcopy(state),
        'trace': deepcopy(trace),
        'checks': checks,
        'metrics': {
            'commodityLotSize': COMMODITY_LOT_SIZE,
            'jumps': sum(1 for event in trace if event.get('type') == 'jump'),
            'jobsCompleted': len(state.get('completedJobs', [])),
            'events': len(trace),
            'creditsDelta': state['credits'] - STARTING_CREDITS,
        },
    }
