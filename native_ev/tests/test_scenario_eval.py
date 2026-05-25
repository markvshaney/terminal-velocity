import unittest

from native_ev.scenario_eval import (
    COMMODITY_LOT_SIZE,
    initial_gameplay_state,
    run_scripted_scenario,
)


class ScenarioEvalHarnessTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
