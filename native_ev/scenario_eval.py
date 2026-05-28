"""Small symbolic gameplay scenario/eval harness for Terminal Velocity.

This is a Terminal Velocity automation scaffold, not an EV Classic fidelity claim.
It gives automated controllers a cheap, repeatable state/action/evaluator loop before
we spend more effort on fragile long-running Basilisk observation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from native_ev.model import economy_manifest, load_universe, system_distance

COMMODITY_LOT_SIZE = 10
STARTING_CREDITS = 10000
STARTING_CARGO_CAPACITY = 20
STARTING_FUEL = 6
START_SYSTEM = 'Levo'
START_BODY = 'Levo Spaceport'
SCENARIO_CURRICULUM = [
    'levo_merchant_first_hop',
    'mission_runner_first_delivery',
    'route_planner_refuel_loop',
    'low_fuel_jump_recovery',
    'blocked_reason_curriculum',
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
        'fuel': STARTING_FUEL,
        'combatExecuted': False,
        'strictPlay': False,
        'knownSystems': known_systems,
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
        'id': action.get('id', f"cargo_{state['currentSystem'].lower()}_{destination_system.lower()}"),
        'originSystem': state['currentSystem'],
        'originBody': state['landedBody'],
        'destinationSystem': destination_system,
        'destinationBody': destination_body,
        'tons': tons,
        'reservedCargoTons': tons,
        'pay': pay,
        'risk': action.get('risk', 'safe'),
    }
    state['cargoUsed'] += tons
    state['activeJobs'].append(job)
    trace.append({'type': 'accept_cargo_job', **job, 'cargoUsed': state['cargoUsed']})
    return True


def _jump(state: dict[str, Any], action: dict[str, Any], trace: list[dict[str, Any]]) -> bool:
    universe = load_universe()
    destination = action['destinationSystem']
    origin = state['currentSystem']
    links = set(_system(universe, origin).get('links', []))
    if destination not in links:
        trace.append({'type': 'blocked_jump', 'originSystem': origin, 'destinationSystem': destination, 'reason': f'{destination} not linked from {origin}'})
        return False
    if state['fuel'] <= 0:
        trace.append({'type': 'blocked_jump', 'originSystem': origin, 'destinationSystem': destination, 'reason': 'insufficient fuel'})
        return False
    state['currentSystem'] = destination
    state['landedBody'] = None
    state['fuel'] -= 1
    state['knownSystems'] = sorted(set(state.get('knownSystems', [])) | {destination} | set(_system(universe, destination).get('links', [])))
    trace.append({'type': 'jump', 'originSystem': origin, 'destinationSystem': destination, 'fuelAfter': state['fuel']})
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
    trace.append({'type': 'depart', 'system': state['currentSystem'], 'body': previous_body})
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
