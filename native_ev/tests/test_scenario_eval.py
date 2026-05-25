import json
import subprocess
import sys
import unittest

from native_ev.scenario_eval import (
    COMMODITY_LOT_SIZE,
    available_scenarios,
    initial_gameplay_state,
    run_scripted_scenario,
)


class ScenarioEvalHarnessTests(unittest.TestCase):
    def test_available_scenarios_exposes_curriculum_order(self):
        self.assertEqual(
            available_scenarios(),
            [
                'levo_merchant_first_hop',
                'mission_runner_first_delivery',
                'route_planner_refuel_loop',
                'blocked_reason_curriculum',
                'disposable_combat_placeholder',
            ],
        )

    def test_initial_gameplay_state_starts_non_strict_at_levo_with_structured_state(self):
        state = initial_gameplay_state()

        self.assertEqual(state['currentSystem'], 'Levo')
        self.assertEqual(state['landedBody'], 'Levo Spaceport')
        self.assertEqual(state['credits'], 10000)
        self.assertEqual(state['cargoCapacity'], 20)
        self.assertEqual(state['cargoUsed'], 0)
        self.assertFalse(state['strictPlay'])
        self.assertEqual(state['cargoHold'], {})
        self.assertEqual(state['activeJobs'], [])
        self.assertIn('Levo', state['knownSystems'])

    def test_levo_merchant_first_hop_scenario_buys_lot_accepts_safe_job_and_lands(self):
        result = run_scripted_scenario('levo_merchant_first_hop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['scenario'], 'levo_merchant_first_hop')
        self.assertEqual(result['checks']['started_at_levo'], 'passed')
        self.assertEqual(result['checks']['bought_commodity_lot'], 'passed')
        self.assertEqual(result['checks']['accepted_safe_cargo_job'], 'passed')
        self.assertEqual(result['checks']['reached_neighbor_and_landed'], 'passed')
        self.assertEqual(result['checks']['completed_safe_cargo_job'], 'passed')
        self.assertEqual(result['metrics']['commodityLotSize'], COMMODITY_LOT_SIZE)
        self.assertEqual(result['metrics']['jumps'], 1)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['cargoHold']['food'], COMMODITY_LOT_SIZE)
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertGreater(result['state']['credits'], 10000 - (120 * COMMODITY_LOT_SIZE))
        self.assertEqual(
            [event['type'] for event in result['trace']],
            [
                'start',
                'buy_commodity_lot',
                'accept_cargo_job',
                'jump',
                'land',
                'complete_cargo_job',
            ],
        )

    def test_scenario_rejects_unlinked_jump_and_records_failed_check(self):
        result = run_scripted_scenario(
            'blocked_unlinked_jump',
            actions=[{'type': 'jump', 'destinationSystem': 'Antares'}],
        )

        self.assertFalse(result['success'])
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['checks']['all_actions_valid'], 'failed')
        self.assertEqual(result['trace'][-1]['type'], 'blocked_jump')
        self.assertIn('not linked', result['trace'][-1]['reason'])
    def test_mission_runner_first_delivery_reserves_cargo_completes_job_and_releases_hold(self):
        result = run_scripted_scenario('mission_runner_first_delivery')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Landfall')
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['completedJobs'], ['levo_landfall_courier'])
        self.assertEqual(result['metrics']['jobsCompleted'], 1)
        self.assertGreater(result['state']['credits'], 10000)
        self.assertEqual(
            [event['type'] for event in result['trace']],
            [
                'start',
                'accept_cargo_job',
                'jump',
                'land',
                'complete_cargo_job',
            ],
        )
        accept = result['trace'][1]
        self.assertEqual(accept['id'], 'levo_landfall_courier')
        self.assertEqual(accept['reservedCargoTons'], 8)

    def test_route_planner_refuel_loop_spends_fuel_blocks_empty_jump_then_refuels(self):
        result = run_scripted_scenario('route_planner_refuel_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['fuel'], 6)
        self.assertEqual(result['metrics']['jumps'], 1)
        self.assertEqual(result['checks']['blocked_empty_fuel_jump'], 'passed')
        self.assertIn(
            {'type': 'blocked_jump', 'originSystem': 'Sol', 'destinationSystem': 'Levo', 'reason': 'insufficient fuel'},
            result['trace'],
        )
        self.assertIn(
            {'type': 'refuel', 'system': 'Sol', 'body': 'Earth', 'fuelAfter': 6},
            result['trace'],
        )

    def test_blocked_reason_curriculum_records_all_safe_blocker_categories(self):
        result = run_scripted_scenario('blocked_reason_curriculum')

        self.assertTrue(result['success'], result)
        reasons_by_type = [(event['type'], event.get('reason')) for event in result['trace']]
        self.assertIn(('blocked_buy_commodity_lot', 'not landed'), reasons_by_type)
        self.assertIn(('blocked_buy_commodity_lot', 'insufficient cargo space'), reasons_by_type)
        self.assertIn(('blocked_buy_commodity_lot', 'insufficient credits'), reasons_by_type)
        self.assertIn(('blocked_jump', 'Antares not linked from Levo'), reasons_by_type)
        self.assertIn(('blocked_complete_cargo_job', 'no deliverable job at current landing'), reasons_by_type)
        self.assertEqual(result['checks']['recorded_not_landed'], 'passed')
        self.assertEqual(result['checks']['recorded_insufficient_cargo'], 'passed')
        self.assertEqual(result['checks']['recorded_insufficient_credits'], 'passed')
        self.assertEqual(result['checks']['recorded_invalid_destination'], 'passed')
        self.assertEqual(result['checks']['recorded_no_deliverable_job'], 'passed')

    def test_disposable_combat_placeholder_defines_guardrails_without_combat_execution(self):
        result = run_scripted_scenario('disposable_combat_placeholder')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['combatExecuted'], False)
        self.assertEqual(result['state']['strictPlay'], False)
        self.assertEqual(result['checks']['strict_play_off'], 'passed')
        self.assertEqual(result['checks']['combat_not_executed'], 'passed')
        self.assertEqual(result['checks']['stop_conditions_recorded'], 'passed')
        guardrail = result['trace'][-1]
        self.assertEqual(guardrail['type'], 'combat_placeholder_guardrail')
        self.assertIn('low shields or hull', guardrail['stopConditions'])
        self.assertIn('unclear save state', guardrail['stopConditions'])
    def test_cli_can_run_entire_curriculum_as_named_results(self):
        completed = subprocess.run(
            [sys.executable, 'tools/run_gameplay_scenarios.py', '--all'],
            check=True,
            capture_output=True,
            text=True,
        )

        payload = json.loads(completed.stdout)
        self.assertEqual([item['scenario'] for item in payload['results']], available_scenarios())
        self.assertTrue(all(item['success'] for item in payload['results']))
        self.assertEqual(payload['summary']['passed'], len(available_scenarios()))
        self.assertEqual(payload['summary']['failed'], 0)


if __name__ == '__main__':
    unittest.main()
