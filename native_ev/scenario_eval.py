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
        'complete_cargo_jobs': _complete_cargo_jobs,
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
        if not handler(state, action, trace):
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
            'events': len(trace),
            'creditsDelta': state['credits'] - STARTING_CREDITS,
        },
    }
