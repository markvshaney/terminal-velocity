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
                'alignment_story_prereq_recovery',
                'alignment_offer_requirement_recovery',
                'federation_alignment_delivery_loop',
                'freeport_alignment_delivery_loop',
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

    def test_levo_same_port_sellback_loop_restores_credits_and_cargo(self):
        result = run_scripted_scenario('levo_same_port_sellback_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 10000)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 0)
        self.assertEqual(result['checks']['bought_original_observed_levo_lot'], 'passed')
        self.assertEqual(result['checks']['sold_same_port_lot_back'], 'passed')
        self.assertEqual(result['checks']['restored_starting_trade_state'], 'passed')
        sell = [event for event in result['trace'] if event['type'] == 'sell_commodity_lot'][-1]
        self.assertEqual(sell['commodity'], 'food')
        self.assertEqual(sell['tons'], 10)
        self.assertEqual(sell['unitPrice'], 120)
        self.assertEqual(sell['creditsAfter'], 10000)
        self.assertEqual(sell['sourceLabel'], 'original-runtime-observed')
        self.assertEqual(sell['oracleStatus'], 'levo_same_port_sellback_observed')

    def test_commodity_sell_blocked_recovery_loop_labels_blockers_and_recovers(self):
        result = run_scripted_scenario('commodity_sell_blocked_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 10000)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 0)
        self.assertEqual(result['checks']['blocked_sell_without_hold'], 'passed')
        self.assertEqual(result['checks']['blocked_sell_while_in_space'], 'passed')
        self.assertEqual(result['checks']['recovered_by_landing_and_selling'], 'passed')
        self.assertEqual(result['checks']['recorded_sell_guardrail_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_sell_commodity_lot']
        self.assertEqual([event['reason'] for event in blocked], ['insufficient commodity in hold', 'not landed'])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-trade-scaffold' for event in blocked))
        self.assertTrue(all(event['oracleStatus'] == 'commodity_sell_guardrail_pending_original_runtime_trace' for event in blocked))

    def test_commodity_buy_blocked_recovery_loop_labels_blockers_and_recovers(self):
        result = run_scripted_scenario('commodity_buy_blocked_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 8800)
        self.assertEqual(result['state']['cargoUsed'], 10)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 10)
        self.assertEqual(result['checks']['blocked_buy_while_in_space'], 'passed')
        self.assertEqual(result['checks']['blocked_buy_without_credits'], 'passed')
        self.assertEqual(result['checks']['blocked_buy_without_capacity'], 'passed')
        self.assertEqual(result['checks']['recovered_by_landing_and_buying'], 'passed')
        self.assertEqual(result['checks']['recorded_buy_guardrail_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_commodity_lot']
        self.assertEqual([event['reason'] for event in blocked], ['not landed', 'insufficient credits', 'insufficient cargo space'])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-trade-scaffold' for event in blocked))
        self.assertTrue(all(event['oracleStatus'] == 'commodity_buy_guardrail_pending_original_runtime_trace' for event in blocked))

    def test_cross_market_trade_spread_scout_buys_sol_food_and_sells_at_levo(self):
        result = run_scripted_scenario('cross_market_trade_spread_scout')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 10780)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 0)
        self.assertEqual(result['checks']['bought_low_at_sol'], 'passed')
        self.assertEqual(result['checks']['sold_high_at_levo'], 'passed')
        self.assertEqual(result['checks']['recorded_cross_market_source_boundary'], 'passed')
        self.assertEqual(result['checks']['returned_to_levo_with_profit'], 'passed')
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual([event['system'] for event in trade_events], ['Sol', 'Levo'])
        self.assertEqual([event['unitPrice'] for event in trade_events], [42, 120])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-cross-market-trade-scaffold' for event in trade_events))
        self.assertTrue(all(event['oracleStatus'] == 'classic_runtime_cross_market_spread_pending' for event in trade_events))

    def test_max_hold_trade_route_scout_fills_hold_and_sells_two_lots(self):
        result = run_scripted_scenario('max_hold_trade_route_scout')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 11560)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 0)
        self.assertEqual(result['checks']['filled_hold_with_two_sol_lots'], 'passed')
        self.assertEqual(result['checks']['sold_two_lots_at_levo'], 'passed')
        self.assertEqual(result['checks']['returned_to_levo_with_full_hold_profit'], 'passed')
        self.assertEqual(result['checks']['recorded_max_hold_trade_source_boundary'], 'passed')
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual([event['type'] for event in trade_events], ['buy_commodity_lot', 'buy_commodity_lot', 'sell_commodity_lot', 'sell_commodity_lot'])
        self.assertEqual([event['system'] for event in trade_events], ['Sol', 'Sol', 'Levo', 'Levo'])
        self.assertEqual([event['cargoUsed'] for event in trade_events], [10, 20, 10, 0])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-max-hold-trade-scaffold' for event in trade_events))
        self.assertTrue(all(event['oracleStatus'] == 'classic_runtime_multi_lot_trade_spread_pending' for event in trade_events))

    def test_trade_route_refuel_profit_loop_blocks_low_fuel_then_recovers(self):
        result = run_scripted_scenario('trade_route_refuel_profit_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 11560)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 0)
        self.assertEqual(result['checks']['blocked_profit_route_on_low_fuel'], 'passed')
        self.assertEqual(result['checks']['refueled_before_return_leg'], 'passed')
        self.assertEqual(result['checks']['completed_refueled_trade_profit'], 'passed')
        self.assertEqual(result['checks']['recorded_refuel_trade_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_jump']
        self.assertTrue(any(event.get('reason') == 'insufficient fuel' and event.get('destinationSystem') == 'Levo' for event in blocked))
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual([event['system'] for event in trade_events], ['Sol', 'Sol', 'Levo', 'Levo'])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-refuel-trade-route-scaffold' for event in trade_events))
        self.assertTrue(all(event['oracleStatus'] == 'classic_runtime_refuel_trade_route_pending' for event in trade_events))

    def test_mission_trade_destination_sale_loop_sells_cargo_after_delivery(self):
        result = run_scripted_scenario('mission_trade_destination_sale_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['completedJobs'], ['intro_courier_earth_hera'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 0)
        self.assertEqual(result['state']['credits'], 11870)
        self.assertEqual(result['checks']['accepted_intro_mission_and_trade_lot'], 'passed')
        self.assertEqual(result['checks']['delivered_mission_before_trade_sale'], 'passed')
        self.assertEqual(result['checks']['sold_trade_cargo_at_destination_market'], 'passed')
        self.assertEqual(result['checks']['recorded_destination_sale_source_boundary'], 'passed')
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual([event['system'] for event in trade_events], ['Sol', 'Centauri'])
        self.assertEqual([event['unitPrice'] for event in trade_events], [42, 49])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-mission-trade-destination-sale-scaffold' for event in trade_events))
        self.assertTrue(all(event['oracleStatus'] == 'mission_trade_destination_sale_pending_classic_runtime_trace' for event in trade_events))

    def test_chapter_one_trade_carryover_loop_sells_cargo_after_second_delivery(self):
        result = run_scripted_scenario('chapter_one_trade_carryover_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['completedJobs'], ['intro_courier_earth_hera', 'frontier_sample_hera_freeport'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 0)
        self.assertEqual(result['state']['credits'], 14400)
        self.assertEqual(result['checks']['completed_two_missions_with_trade_cargo_reserved_alongside'], 'passed')
        self.assertEqual(result['checks']['carried_trade_lot_across_story_chain'], 'passed')
        self.assertEqual(result['checks']['sold_carried_trade_cargo_after_second_delivery'], 'passed')
        self.assertEqual(result['checks']['recorded_chapter_trade_carryover_source_boundary'], 'passed')
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual([event['system'] for event in trade_events], ['Sol', 'Sirius'])
        self.assertEqual([event['unitPrice'] for event in trade_events], [42, 62])
        frontier_accept = [event for event in result['trace'] if event['type'] == 'accept_cargo_job' and event['id'] == 'frontier_sample_hera_freeport'][-1]
        self.assertEqual(frontier_accept['cargoUsed'], 14)
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-chapter-one-trade-carryover-scaffold' for event in result['trace'] if event['type'] in {'accept_cargo_job', 'buy_commodity_lot', 'sell_commodity_lot', 'complete_cargo_job'}))
        self.assertTrue(all(event['oracleStatus'] == 'chapter_one_trade_carryover_pending_classic_runtime_trace' for event in result['trace'] if event['type'] in {'accept_cargo_job', 'buy_commodity_lot', 'sell_commodity_lot', 'complete_cargo_job'}))

    def test_mission_trade_return_margin_guardrail_skips_bad_return_cargo_and_finishes_chain(self):
        result = run_scripted_scenario('mission_trade_return_margin_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['completedJobs'], ['intro_courier_earth_hera', 'frontier_sample_hera_freeport', 'freeport_return_earth'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['credits'], 17600)
        self.assertIn('chapter_one_complete', result['state']['storyFlags'])
        self.assertEqual(result['checks']['completed_return_contract_after_trade_sale'], 'passed')
        self.assertEqual(result['checks']['blocked_negative_margin_return_trade'], 'passed')
        self.assertEqual(result['checks']['recorded_return_margin_source_boundary'], 'passed')
        rejected = [event for event in result['trace'] if event['type'] == 'trade_margin_decision' and event['decision'] == 'skip'][-1]
        self.assertEqual(rejected['commodity'], 'equipment')
        self.assertEqual(rejected['originSystem'], 'Sirius')
        self.assertEqual(rejected['destinationSystem'], 'Sol')
        self.assertEqual(rejected['buyPrice'], 160)
        self.assertEqual(rejected['sellPrice'], 150)
        self.assertEqual(rejected['marginPerTon'], -10)
        self.assertEqual(rejected['sourceLabel'], 'terminal-velocity-mission-trade-return-margin-scaffold')
        self.assertEqual(rejected['oracleStatus'], 'chapter_one_return_trade_margin_pending_classic_runtime_trace')

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

    def test_alignment_offer_requirement_recovery_blocks_and_restores_branch_offers(self):
        result = run_scripted_scenario('alignment_offer_requirement_recovery')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['checks']['blocked_alignment_offers_below_requirements'], 'passed')
        self.assertEqual(result['checks']['recovered_alignment_offers_at_thresholds'], 'passed')
        self.assertEqual(result['checks']['recorded_requirement_gate_source_boundary'], 'passed')
        scans = [event for event in result['trace'] if event['type'] == 'scan_mission_offers']
        self.assertEqual(scans[0]['offersBySurface']['Mission Computer'], [])
        self.assertEqual(scans[-1]['offersBySurface']['Mission Computer'], ['federation_report_freeport', 'freeport_pact_smugglers'])

    def test_alignment_story_prereq_recovery_blocks_and_restores_branch_offers(self):
        result = run_scripted_scenario('alignment_story_prereq_recovery')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['storyFlags'], ['frontier_samples_delivered'])
        self.assertEqual(result['checks']['blocked_alignment_offers_without_story_prereq'], 'passed')
        self.assertEqual(result['checks']['recovered_alignment_offers_after_story_prereq'], 'passed')
        self.assertEqual(result['checks']['recorded_story_gate_source_boundary'], 'passed')
        scans = [event for event in result['trace'] if event['type'] == 'scan_mission_offers']
        self.assertEqual(scans[0]['offersBySurface']['Mission Computer'], [])
        self.assertEqual(scans[-1]['offersBySurface']['Mission Computer'], ['federation_report_freeport', 'freeport_pact_smugglers'])

    def test_federation_alignment_delivery_loop_completes_branch_and_preserves_choice(self):
        result = run_scripted_scenario('federation_alignment_delivery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['completedJobs'], ['federation_report_freeport'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['credits'], 12800)
        self.assertIn('alignment_federation', result['state']['storyFlags'])
        self.assertIn('federation_intel_asset', result['state']['storyFlags'])
        self.assertNotIn('alignment_freeport', result['state']['storyFlags'])
        self.assertEqual(result['checks']['completed_federation_alignment_delivery'], 'passed')
        self.assertEqual(result['checks']['preserved_federation_alignment_flags'], 'passed')
        self.assertEqual(result['checks']['blocked_freeport_branch_after_federation_completion'], 'passed')
        blocked = [event for event in result['trace'] if event.get('type') == 'blocked_manifest_mission'][-1]
        self.assertEqual(blocked['missionId'], 'freeport_pact_smugglers')
        accept = [event for event in result['trace'] if event.get('type') == 'accept_cargo_job' and event.get('id') == 'federation_report_freeport'][-1]
        self.assertEqual(accept['reservedCargoTons'], 2)
        self.assertEqual(accept['sourceLabel'], 'terminal-velocity-mission-scaffold')
        self.assertEqual(accept['oracleStatus'], 'mission_behavior_pending_classic_runtime_trace')

    def test_freeport_alignment_delivery_loop_completes_branch_and_preserves_choice(self):
        result = run_scripted_scenario('freeport_alignment_delivery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['completedJobs'], ['freeport_pact_smugglers'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['credits'], 13000)
        self.assertIn('alignment_freeport', result['state']['storyFlags'])
        self.assertIn('freeport_network_asset', result['state']['storyFlags'])
        self.assertNotIn('alignment_federation', result['state']['storyFlags'])
        self.assertEqual(result['checks']['completed_freeport_alignment_delivery'], 'passed')
        self.assertEqual(result['checks']['preserved_freeport_alignment_flags'], 'passed')
        self.assertEqual(result['checks']['blocked_federation_branch_after_freeport_completion'], 'passed')
        self.assertEqual(result['checks']['recorded_freeport_alignment_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event.get('type') == 'blocked_manifest_mission'][-1]
        self.assertEqual(blocked['missionId'], 'federation_report_freeport')
        accept = [event for event in result['trace'] if event.get('type') == 'accept_cargo_job' and event.get('id') == 'freeport_pact_smugglers'][-1]
        self.assertEqual(accept['reservedCargoTons'], 2)
        self.assertEqual(accept['sourceLabel'], 'terminal-velocity-mission-scaffold')
        self.assertEqual(accept['oracleStatus'], 'mission_behavior_pending_classic_runtime_trace')

    def test_mission_destination_route_hint_sets_route_to_active_contract_destination(self):
        result = run_scripted_scenario('mission_destination_route_hint')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['routeQueue'], ['Centauri'])
        self.assertEqual(result['checks']['queued_active_mission_destination'], 'passed')
        self.assertEqual(result['trace'][-1]['destinationSystem'], 'Centauri')
        self.assertEqual(result['trace'][-1]['sourceLabel'], 'terminal-velocity-design-scaffold')

    def test_mission_trade_hybrid_capacity_planning_preserves_trade_cargo(self):
        result = run_scripted_scenario('mission_trade_hybrid_capacity_planning')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['accepted_trade_aligned_mission'], 'passed')
        self.assertEqual(result['checks']['bought_one_trade_lot_with_remaining_capacity'], 'passed')
        self.assertEqual(result['checks']['blocked_second_lot_to_preserve_capacity_rule'], 'passed')
        self.assertEqual(result['checks']['completed_mission_with_trade_cargo_still_held'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_commodity_lot'][-1]
        self.assertEqual(blocked['reason'], 'insufficient cargo space')
        self.assertEqual(result['state']['completedJobs'], ['levo_trade_aligned_courier'])
        self.assertEqual(result['state']['cargoHold']['food'], 10)
        self.assertEqual(result['state']['cargoUsed'], 10)

    def test_mission_trade_refuel_delivery_loop_blocks_low_fuel_then_delivers_with_trade_cargo(self):
        result = run_scripted_scenario('mission_trade_refuel_delivery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['accepted_intro_mission_and_trade_lot'], 'passed')
        self.assertEqual(result['checks']['blocked_delivery_leg_on_low_fuel'], 'passed')
        self.assertEqual(result['checks']['refueled_before_delivery_leg'], 'passed')
        self.assertEqual(result['checks']['completed_delivery_with_trade_cargo_held'], 'passed')
        self.assertEqual(result['checks']['recorded_mission_trade_refuel_source_boundary'], 'passed')
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['completedJobs'], ['intro_courier_earth_hera'])
        self.assertEqual(result['state']['cargoHold']['food'], COMMODITY_LOT_SIZE)
        self.assertEqual(result['state']['cargoUsed'], COMMODITY_LOT_SIZE)
        self.assertEqual(result['state']['credits'], 11380)
        blocked = [event for event in result['trace'] if event.get('type') == 'blocked_jump'][-1]
        self.assertEqual(blocked['reason'], 'insufficient fuel')
        self.assertEqual(blocked['destinationSystem'], 'Centauri')
        labeled_events = [event for event in result['trace'] if event.get('type') in {'buy_commodity_lot', 'complete_cargo_job'}]
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-mission-trade-refuel-scaffold' for event in labeled_events))
        self.assertTrue(all(event['oracleStatus'] == 'mission_trade_refuel_pending_classic_runtime_trace' for event in labeled_events))

    def test_mission_abort_releases_reserved_cargo_without_completion(self):
        result = run_scripted_scenario('mission_abort_releases_reserved_cargo')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['completedJobs'], [])
        self.assertEqual(result['state']['abortedJobs'], ['intro_courier_earth_hera'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['checks']['aborted_active_mission'], 'passed')
        self.assertEqual(result['checks']['released_aborted_mission_cargo'], 'passed')
        abort_event = [event for event in result['trace'] if event['type'] == 'abort_mission'][-1]
        self.assertEqual(abort_event['missionId'], 'intro_courier_earth_hera')
        self.assertEqual(abort_event['releasedCargoTons'], 3)
        self.assertEqual(abort_event['sourceLabel'], 'terminal-velocity-mission-abort-scaffold')
        self.assertEqual(abort_event['oracleStatus'], 'mission_abort_pending_classic_runtime_or_manual_trace')

    def test_mission_abort_reaccept_delivery_loop_recovers_after_abort(self):
        result = run_scripted_scenario('mission_abort_reaccept_delivery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['completedJobs'], ['intro_courier_earth_hera'])
        self.assertEqual(result['state']['abortedJobs'], ['intro_courier_earth_hera'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['credits'], 11800)
        self.assertIn('story_intro_started', result['state']['storyFlags'])
        self.assertIn('story_intro_complete', result['state']['storyFlags'])
        self.assertEqual(result['checks']['aborted_first_attempt'], 'passed')
        self.assertEqual(result['checks']['reaccepted_after_abort'], 'passed')
        self.assertEqual(result['checks']['delivered_reaccepted_mission'], 'passed')
        self.assertEqual(result['checks']['recorded_abort_reaccept_source_boundary'], 'passed')
        accepts = [event for event in result['trace'] if event['type'] == 'accept_cargo_job' and event.get('id') == 'intro_courier_earth_hera']
        self.assertEqual(len(accepts), 2)
        self.assertEqual(accepts[-1]['reservedCargoTons'], 3)
        abort = [event for event in result['trace'] if event['type'] == 'abort_mission'][-1]
        self.assertEqual(abort['releasedCargoTons'], 3)

    def test_mission_deadline_failure_scaffold_releases_cargo_and_records_penalty(self):
        result = run_scripted_scenario('mission_deadline_failure_scaffold')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['currentDay'], 3)
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['failedJobs'], ['deadline_dispatch_failure_probe'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['reputation']['Federation'], 2)
        self.assertIn('fail_mission_bit_42', result['state']['storyFlags'])
        self.assertEqual(result['checks']['expired_after_deadline'], 'passed')
        self.assertEqual(result['checks']['recorded_deadline_source_boundary'], 'passed')
        failure = [event for event in result['trace'] if event['type'] == 'mission_deadline_failure'][-1]
        self.assertEqual(failure['releasedCargoTons'], 3)
        self.assertEqual(failure['failureFlag'], 'fail_mission_bit_42')
        self.assertEqual(failure['reputationDelta'], -3)
        self.assertEqual(failure['sourceLabel'], 'ev-classic-resource-bible-backed-mission-failure-scaffold')
        self.assertEqual(failure['oracleStatus'], 'deadline_failure_runtime_ui_pending_classic_trace')

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

    def test_repair_service_recovery_loop_repairs_hull_and_blocks_bad_contexts(self):
        result = run_scripted_scenario('repair_service_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['currentHull'], result['state']['maxHull'])
        self.assertEqual(result['checks']['blocked_in_space_repair'], 'passed')
        self.assertEqual(result['checks']['blocked_no_service_repair'], 'passed')
        self.assertEqual(result['checks']['repaired_hull_at_service_port'], 'passed')
        self.assertEqual(result['checks']['recorded_repair_source_boundary'], 'passed')
        events = [event for event in result['trace'] if event['type'] in {'blocked_repair_hull', 'repair_hull'}]
        self.assertEqual(events[0]['reason'], 'not landed')
        self.assertEqual(events[1]['reason'], 'repair service unavailable')
        repair = [event for event in events if event['type'] == 'repair_hull'][-1]
        self.assertEqual(repair['hullBefore'], 65)
        self.assertEqual(repair['hullAfter'], 100)
        self.assertEqual(repair['cost'], 280)
        self.assertEqual(repair['sourceLabel'], 'terminal-velocity-repair-service-scaffold')
        self.assertEqual(repair['oracleStatus'], 'repair_service_pending_ev_classic_runtime_trace')

    def test_disabled_player_recovery_loop_blocks_actions_then_recovers(self):
        result = run_scripted_scenario('disabled_player_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['disabled_player_recorded'], 'passed')
        self.assertEqual(result['checks']['blocked_disabled_actions'], 'passed')
        self.assertEqual(result['checks']['recovered_player_scaffold'], 'passed')
        self.assertEqual(result['checks']['recorded_disabled_recovery_source_boundary'], 'passed')
        self.assertFalse(result['state']['playerDisabled'])
        self.assertEqual(result['state']['currentHull'], result['state']['maxHull'])
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_disabled_action']
        self.assertEqual([event['action'] for event in blocked], ['jump', 'fire_primary', 'accept_mission'])
        recovery = [event for event in result['trace'] if event['type'] == 'recover_disabled_player'][-1]
        self.assertEqual(recovery['hullAfter'], 100)
        self.assertEqual(recovery['sourceLabel'], 'terminal-velocity-player-disabled-scaffold')
        self.assertEqual(recovery['oracleStatus'], 'classic_runtime_player_death_pending_strict_play_safe_trace')

    def test_system_service_provisioning_scout_records_service_matrix_boundaries(self):
        result = run_scripted_scenario('system_service_provisioning_scout')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['checks']['confirmed_levo_original_service_boundary'], 'passed')
        self.assertEqual(result['checks']['scouted_earth_full_service_scaffold'], 'passed')
        self.assertEqual(result['checks']['scouted_station_without_shipyard'], 'passed')
        self.assertEqual(result['checks']['recorded_service_matrix_source_boundary'], 'passed')
        scans = {(event['system'], event['body']): event for event in result['trace'] if event['type'] == 'scan_station_services'}
        self.assertFalse(scans[('Levo', 'Levo Spaceport')]['hasOutfitter'])
        self.assertFalse(scans[('Levo', 'Levo Spaceport')]['hasShipyard'])
        self.assertTrue(scans[('Sol', 'Earth')]['hasShipyard'])
        self.assertIn('light_freighter', scans[('Sol', 'Earth')]['shipsForSale'])
        self.assertFalse(scans[('Sol', 'Stardock Alpha')]['hasShipyard'])
        self.assertEqual(scans[('Sol', 'Stardock Alpha')]['sourceLabel'], 'terminal-velocity-service-provisioning-scaffold')

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

    def test_contraband_scan_clemency_recovery_confiscates_and_repairs_legal_record(self):
        result = run_scripted_scenario('contraband_scan_clemency_recovery')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['confiscated_federation_contraband'], 'passed')
        self.assertEqual(result['checks']['applied_federation_fine_and_legal_penalty'], 'passed')
        self.assertEqual(result['checks']['paid_clemency_after_scan'], 'passed')
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['credits'], 3200)
        self.assertEqual(result['state']['legalRecords']['Federation'], -8)
        scan = [event for event in result['trace'] if event['type'] == 'contraband_scan'][-1]
        self.assertEqual(scan['sourceLabel'], 'terminal-velocity-classic-resource-smuggling-scan-semantics')
        self.assertEqual(scan['oracleStatus'], 'classic_runtime_scan_frequency_and_ui_wording_pending')
        self.assertEqual(scan['confiscated'], {'equipment': 2})
        clemency = [event for event in result['trace'] if event['type'] == 'pay_legal_clemency'][-1]
        self.assertEqual(clemency['sourceLabel'], 'terminal-velocity-inferred-clemency-scaffold')
        self.assertEqual(clemency['oracleStatus'], 'approved_inference_pending_ev_classic_confirmation')

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
