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

    def test_intro_courier_mission_delivery_matches_godot_fast_eval_contract(self):
        result = run_scripted_scenario('intro_courier_mission_delivery')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['completedJobs'], ['intro_courier_earth_hera'])
        self.assertEqual(result['state']['credits'], 11800)
        self.assertIn('story_intro_started', result['state']['storyFlags'])
        self.assertIn('story_intro_complete', result['state']['storyFlags'])
        self.assertIn('federation_trusted_courier', result['state']['storyFlags'])
        self.assertEqual(result['checks']['accepted_intro_courier'], 'passed')
        self.assertEqual(result['checks']['completed_intro_courier'], 'passed')
        self.assertEqual(result['checks']['released_intro_cargo'], 'passed')
        self.assertEqual(result['checks']['applied_story_flags'], 'passed')
        self.assertEqual(result['metrics']['jobsCompleted'], 1)
        self.assertEqual(result['metrics']['creditsDelta'], 1800)
        self.assertEqual(
            [event['type'] for event in result['trace']],
            [
                'start',
                'jump',
                'land',
                'accept_cargo_job',
                'depart',
                'jump',
                'land',
                'complete_cargo_job',
            ],
        )
        accept = result['trace'][3]
        self.assertEqual(accept['id'], 'intro_courier_earth_hera')
        self.assertEqual(accept['originSystem'], 'Sol')
        self.assertEqual(accept['originBody'], 'Earth')
        self.assertEqual(accept['destinationSystem'], 'Centauri')
        self.assertEqual(accept['destinationBody'], 'Luna')
        self.assertEqual(accept['reservedCargoTons'], 3)
        complete = result['trace'][-1]
        self.assertEqual(complete['pay'], 1800)

    def test_chapter_one_courier_chain_completes_three_story_deliveries(self):
        result = run_scripted_scenario('chapter_one_courier_chain')

        self.assertTrue(result['success'], result)
        self.assertEqual(
            result['state']['completedJobs'],
            ['intro_courier_earth_hera', 'frontier_sample_hera_freeport', 'freeport_return_earth'],
        )
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['credits'], 17400)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        for flag in [
            'story_intro_complete',
            'frontier_samples_delivered',
            'chapter_one_complete',
            'federation_independent_bridge',
        ]:
            self.assertIn(flag, result['state']['storyFlags'])
        self.assertEqual(result['checks']['completed_intro_frontier_return_chain'], 'passed')
        self.assertEqual(result['metrics']['jobsCompleted'], 3)
        self.assertEqual(result['metrics']['jumps'], 4)

    def test_scan_mission_offers_archives_available_jobs_by_landed_surface(self):
        result = run_scripted_scenario(
            'scan_intro_mission_offers',
            actions=[
                {'type': 'jump', 'destinationSystem': 'Sol'},
                {'type': 'land', 'body': 'Earth'},
                {'type': 'scan_mission_offers'},
            ],
        )

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['checks']['archived_mission_offers'], 'passed')
        self.assertEqual(result['state']['missionOfferArchive']['Sol/Earth']['Mission Computer'], ['intro_courier_earth_hera'])
        scan = result['trace'][-1]
        self.assertEqual(scan['type'], 'scan_mission_offers')
        self.assertEqual(scan['system'], 'Sol')
        self.assertEqual(scan['body'], 'Earth')
        self.assertEqual(scan['offersBySurface']['Mission Computer'], ['intro_courier_earth_hera'])
        self.assertEqual(scan['totalOffers'], 1)
        self.assertEqual(scan['sourceLabel'], 'terminal-velocity-observed')
        self.assertEqual(scan['oracleStatus'], 'terminal_velocity_eval_pending_original_trace')

    def test_alignment_choice_blocks_mutually_exclusive_branch_after_accept(self):
        result = run_scripted_scenario('alignment_choice_guardrail')

        self.assertTrue(result['success'], result)
        self.assertIn('federation_report_freeport', [job['id'] for job in result['state']['activeJobs']])
        self.assertNotIn('freeport_pact_smugglers', [job['id'] for job in result['state']['activeJobs']])
        self.assertIn('alignment_federation', result['state']['storyFlags'])
        self.assertNotIn('alignment_freeport', result['state']['storyFlags'])
        blocked = [event for event in result['trace'] if event.get('type') == 'blocked_manifest_mission']
        self.assertEqual(blocked[-1]['missionId'], 'freeport_pact_smugglers')
        self.assertEqual(blocked[-1]['reason'], 'not available at current landing')
        self.assertEqual(result['checks']['blocked_mutually_exclusive_alignment'], 'passed')

    def test_mission_destination_route_hint_sets_route_to_active_contract_destination(self):
        result = run_scripted_scenario('mission_destination_route_hint')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['routeQueue'], ['Centauri'])
        self.assertEqual(result['checks']['queued_active_mission_destination'], 'passed')
        self.assertEqual(result['trace'][-1]['destinationSystem'], 'Centauri')
        self.assertEqual(result['trace'][-1]['sourceLabel'], 'terminal-velocity-design-scaffold')

    def test_outfitter_ship_ladder_intro_buys_upgrade_weapon_and_bigger_ship(self):
        result = run_scripted_scenario('outfitter_ship_ladder_intro')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['ownedOutfits']['cargo_pod'], 1)
        self.assertEqual(result['state']['ownedWeapons']['laser_cannon'], 1)
        self.assertGreater(result['state']['cargoCapacity'], 20)
        self.assertEqual(result['checks']['bought_first_outfit'], 'passed')
        self.assertEqual(result['checks']['bought_first_weapon'], 'passed')
        self.assertEqual(result['checks']['upgraded_to_larger_ship'], 'passed')
        self.assertEqual(result['checks']['recorded_outfitter_ship_ladder_source_boundary'], 'passed')
        self.assertIn('terminal-velocity-outfitter-ship-ladder-scaffold', {event.get('sourceLabel') for event in result['trace']})

    def test_shift_click_multi_stop_route_queue_draws_green_path_and_consumes_first_leg(self):
        result = run_scripted_scenario('shift_click_multi_stop_route_queue')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['routeQueue'], ['Sirius'])
        self.assertEqual(result['checks']['green_multi_stop_route'], 'passed')
        self.assertEqual(result['checks']['consumed_first_leg_only'], 'passed')
        self.assertEqual(result['trace'][-1]['remainingRoute'], ['Sirius'])

    def test_route_queue_invalid_stop_guardrail_preserves_valid_route(self):
        result = run_scripted_scenario('route_queue_invalid_stop_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['routeQueue'], ['Sol'])
        self.assertEqual(result['checks']['preserved_valid_route_after_invalid_clicks'], 'passed')
        self.assertEqual(result['checks']['blocked_duplicate_or_current_system'], 'passed')
        self.assertEqual(result['checks']['blocked_unlinked_route_tail_stop'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_append_route_stop']
        self.assertEqual([event['destinationSystem'] for event in blocked], ['Levo', 'Antares'])
        self.assertTrue(all(event['routeQueue'] == ['Sol'] for event in blocked))

    def test_route_queue_clear_guardrail_clears_route_and_blocks_unselected_jump(self):
        result = run_scripted_scenario('route_queue_clear_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['routeQueue'], [])
        self.assertEqual(result['checks']['cleared_multi_stop_route'], 'passed')
        self.assertEqual(result['checks']['blocked_jump_after_clear'], 'passed')
        self.assertEqual(result['checks']['recorded_clear_source_boundary'], 'passed')
        clear_event = [event for event in result['trace'] if event['type'] == 'clear_route_queue'][-1]
        self.assertEqual(clear_event['previousRoute'], ['Sol', 'Sirius'])
        self.assertEqual(clear_event['sourceLabel'], 'terminal-velocity-route-guardrail')
        blocked_jump = [event for event in result['trace'] if event['type'] == 'blocked_jump'][-1]
        self.assertIsNone(blocked_jump['destinationSystem'])
        self.assertEqual(blocked_jump['reason'], 'no destination selected')

    def test_route_queue_clear_reselect_guardrail_recovers_after_new_route_selection(self):
        result = run_scripted_scenario('route_queue_clear_reselect_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['routeQueue'], [])
        self.assertEqual(result['checks']['blocked_jump_after_clear'], 'passed')
        self.assertEqual(result['checks']['reselected_after_clear'], 'passed')
        self.assertEqual(result['checks']['jumped_after_reselect'], 'passed')
        event_types = [event['type'] for event in result['trace']]
        self.assertEqual(event_types[-3:], ['blocked_jump', 'append_route_stop', 'jump'])

    def test_near_center_jump_block_preserves_state_with_original_runtime_label(self):
        result = run_scripted_scenario('near_center_jump_block')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['fuel'], 6)
        self.assertEqual(result['checks']['blocked_near_center_jump'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_jump'][-1]
        self.assertEqual(blocked['destinationSystem'], 'Sol')
        self.assertEqual(blocked['reason'], 'too close to system center')
        self.assertEqual(blocked['sourceLabel'], 'original-runtime-observed')
        self.assertEqual(blocked['oracleStatus'], 'near_center_jump_failure_observed_exact_distance_pending')

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

    def test_low_fuel_jump_recovery_blocks_jump_preserves_state_then_refuels(self):
        result = run_scripted_scenario('low_fuel_jump_recovery')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['fuel'], 6)
        self.assertEqual(result['metrics']['jumps'], 0)
        self.assertEqual(result['checks']['started_with_empty_fuel'], 'passed')
        self.assertEqual(result['checks']['blocked_low_fuel_jump'], 'passed')
        self.assertEqual(result['checks']['preserved_system_after_block'], 'passed')
        self.assertEqual(result['checks']['refueled_after_block'], 'passed')
        self.assertIn(
            {'type': 'blocked_jump', 'originSystem': 'Levo', 'destinationSystem': 'Sol', 'reason': 'insufficient fuel'},
            result['trace'],
        )
        self.assertIn(
            {'type': 'refuel', 'system': 'Levo', 'body': 'Levo Spaceport', 'fuelAfter': 6},
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

    def test_pirate_avoidance_escape_route_records_noncombat_evasion(self):
        result = run_scripted_scenario('pirate_avoidance_escape_route')

        self.assertTrue(result['success'], result)
        self.assertFalse(result['state']['combatExecuted'])
        self.assertEqual(result['state']['threatPosture'], 'evaded')
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['checks']['detected_pirate_threat'], 'passed')
        self.assertEqual(result['checks']['escaped_without_combat'], 'passed')
        self.assertEqual(result['checks']['landed_at_safe_port'], 'passed')
        avoidance = [event for event in result['trace'] if event['type'] == 'avoid_pirate_contact'][-1]
        self.assertEqual(avoidance['sourceLabel'], 'terminal-velocity-pirate-avoidance-scaffold')
        self.assertEqual(avoidance['oracleStatus'], 'pirate_avoidance_pending_ev_classic_combat_trace')
        self.assertEqual(avoidance['decision'], 'jump_to_linked_safe_port')

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
