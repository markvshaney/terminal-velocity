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
    economy_manifest,
    load_universe,
    mission_manifest,
    outfit_manifest,
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
    'mission_runner_first_delivery',
    'scan_intro_mission_offers',
    'intro_courier_mission_delivery',
    'chapter_one_courier_chain',
    'alignment_choice_guardrail',
    'mission_destination_route_hint',
    'outfitter_ship_ladder_intro',
    'shift_click_multi_stop_route_queue',
    'route_queue_invalid_stop_guardrail',
    'route_queue_clear_guardrail',
    'route_queue_clear_reselect_guardrail',
    'near_center_jump_block',
    'route_planner_refuel_loop',
    'low_fuel_jump_recovery',
    'blocked_reason_curriculum',
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
        'combatExecuted': False,
        'threatPosture': 'clear',
        'strictPlay': False,
        'knownSystems': known_systems,
        'playerShipId': 'shuttlecraft',
        'ownedOutfits': {},
        'ownedWeapons': {},
        'maxHull': 100,
        'maxFuel': STARTING_FUEL,
        'distanceFromSystemCenter': MIN_JUMP_DISTANCE + 50,
    }


def _buy_commodity_lot(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    commodity = action['commodity']
    system_name = state['currentSystem']
    economy = economy_manifest()
    price = int(economy['markets'][system_name][commodity]['buy'])
    total = price * COMMODITY_LOT_SIZE
    if state['landedBody'] is None:
        trace.append({'type': 'blocked_buy_commodity_lot', 'reason': 'not landed', 'commodity': commodity})
        return False
    if state['cargoUsed'] + COMMODITY_LOT_SIZE > state['cargoCapacity']:
        trace.append({'type': 'blocked_buy_commodity_lot', 'reason': 'insufficient cargo space', 'commodity': commodity})
        return False
    if state['credits'] < total:
        trace.append({'type': 'blocked_buy_commodity_lot', 'reason': 'insufficient credits', 'commodity': commodity})
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
        'setsFlags': list(action.get('setsFlags', [])),
        'completionFlags': list(action.get('completionFlags', [])),
    }
    state['cargoUsed'] += tons
    state['activeJobs'].append(job)
    for flag in job['setsFlags']:
        if flag not in state['storyFlags']:
            state['storyFlags'].append(flag)
    trace.append({'type': 'accept_cargo_job', **job, 'cargoUsed': state['cargoUsed']})
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


def default_actions_for_scenario(name: str) -> list[dict[str, Any]]:
    if name == 'levo_merchant_first_hop':
        return [
            {'type': 'buy_commodity_lot', 'commodity': 'food'},
            {'type': 'accept_cargo_job', 'destinationSystem': 'Sol', 'destinationBody': 'Earth', 'tons': 5, 'risk': 'safe'},
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'complete_cargo_jobs'},
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
    if name == 'mission_destination_route_hint':
        return [
            {'type': 'jump', 'destinationSystem': 'Sol'},
            {'type': 'land', 'body': 'Earth'},
            {'type': 'accept_manifest_mission', 'missionId': 'intro_courier_earth_hera'},
            {'type': 'depart'},
            {'type': 'route_to_active_mission_destination'},
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
    elif name == 'mission_destination_route_hint':
        checks.update({
            'queued_active_mission_destination': 'passed' if state.get('currentSystem') == 'Sol' and state.get('routeQueue') == ['Centauri'] and any(event.get('type') == 'route_to_active_mission_destination' and event.get('missionId') == 'intro_courier_earth_hera' and event.get('destinationSystem') == 'Centauri' and event.get('routeQueued') for event in trace) else 'failed',
        })
    elif name == 'outfitter_ship_ladder_intro':
        checks.update({
            'bought_first_outfit': 'passed' if state.get('ownedOutfits', {}).get('cargo_pod') == 1 and any(event.get('type') == 'buy_outfit_or_weapon' and event.get('saleType') == 'outfit' and event.get('itemId') == 'cargo_pod' for event in trace) else 'failed',
            'bought_first_weapon': 'passed' if state.get('ownedWeapons', {}).get('laser_cannon') == 1 and any(event.get('type') == 'buy_outfit_or_weapon' and event.get('saleType') == 'weapon' and event.get('itemId') == 'laser_cannon' for event in trace) else 'failed',
            'upgraded_to_larger_ship': 'passed' if state.get('playerShipId') == 'light_freighter' and any(event.get('type') == 'buy_ship' and event.get('previousShipId') == 'shuttlecraft' and int(event.get('cargoCapacityAfter', 0)) > int(event.get('cargoCapacityBefore', 0)) for event in trace) else 'failed',
            'recorded_outfitter_ship_ladder_source_boundary': 'passed' if all(event.get('sourceLabel') == 'terminal-velocity-outfitter-ship-ladder-scaffold' and 'pending_original' in event.get('oracleStatus', '') for event in trace if event.get('type') in {'buy_outfit_or_weapon', 'buy_ship'}) else 'failed',
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
        'accept_cargo_job': _accept_cargo_job,
        'jump': _jump,
        'land': _land,
        'depart': _depart,
        'refuel': _refuel,
        'set_state': _set_state,
        'append_route_stop': _append_route_stop,
        'clear_route_queue': _clear_route_queue,
        'route_to_active_mission_destination': _route_to_active_mission_destination,
        'scan_mission_offers': _scan_mission_offers,
        'accept_manifest_mission': _accept_manifest_mission,
        'buy_outfit_or_weapon': _buy_outfit_or_weapon,
        'buy_ship': _buy_ship,
        'avoid_pirate_contact': _avoid_pirate_contact,
        'complete_cargo_jobs': _complete_cargo_jobs,
        'combat_placeholder_guardrail': _combat_placeholder_guardrail,
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
