import json
import subprocess
import sys
import unittest

from native_ev.scenario_eval import (
    COMMODITY_LOT_SIZE,
    START_SYSTEM,
    START_BODY,
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
                'commodity_partial_hold_recovery_loop',
                'commodity_exact_credit_sellback_rebuy_loop',
                'commodity_exact_credit_full_hold_sellback_loop',
                'cross_market_trade_spread_scout',
                'cross_market_exact_credit_profit_loop',
                'cross_market_exact_credit_full_hold_profit_loop',
                'max_hold_trade_route_scout',
                'trade_route_refuel_profit_loop',
                'trade_route_margin_choice_loop',
                'strategy_skill_rotation_loop',
                'upgrade_readiness_strategy_loop',
                'upgrade_affordability_trade_loop',
                'cargo_expansion_trade_loop',
                'fuel_reserve_upgrade_loop',
                'hull_plating_repair_loop',
                'balanced_upgrade_trade_loop',
                'light_freighter_capacity_trade_loop',
                'light_freighter_mission_trade_loop',
                'light_freighter_refuel_delivery_loop',
                'light_freighter_deadline_refuel_delivery_loop',
                'light_freighter_bulk_margin_choice_loop',
                'light_freighter_bulk_mission_margin_loop',
                'light_freighter_refuel_mission_margin_loop',
                'light_freighter_repair_margin_loop',
                'light_freighter_repair_mission_margin_loop',
                'light_freighter_repair_refuel_mission_margin_loop',
                'light_freighter_deadline_repair_refuel_margin_loop',
                'mission_runner_first_delivery',
                'scan_intro_mission_offers',
                'intro_courier_mission_delivery',
                'chapter_one_courier_chain',
                'alignment_choice_guardrail',
                'alignment_story_prereq_recovery',
                'alignment_offer_requirement_recovery',
                'federation_alignment_delivery_loop',
                'freeport_alignment_delivery_loop',
                'alignment_completion_offer_scan_guardrail',
                'alignment_return_contract_offer_timing_guardrail',
                'alignment_completion_return_contract_loop',
                'mission_destination_route_hint',
                'mission_destination_low_fuel_route_hint',
                'mission_route_refuel_delivery_loop',
                'mission_trade_hybrid_capacity_planning',
                'mission_trade_refuel_delivery_loop',
                'mission_trade_destination_sale_loop',
                'chapter_one_trade_carryover_loop',
                'mission_trade_return_margin_guardrail',
                'mission_abort_releases_reserved_cargo',
                'mission_abort_reaccept_delivery_loop',
                'mission_abort_forbidden_return_gate',
                'mission_abort_forbidden_return_completion_loop',
                'mission_abort_reputation_penalty_guardrail',
                'mission_auto_abort_completion_flags_guardrail',
                'mission_deadline_failure_scaffold',
                'mission_deadline_last_day_delivery_loop',
                'mission_deadline_completed_no_late_failure_loop',
                'mission_deadline_abort_prevents_failure_loop',
                'mission_deadline_failure_recovery_loop',
                'mission_deadline_trade_carryover_loop',
                'mission_deadline_sequential_failures_loop',
                'mission_scan_failure_guardrail',
                'mission_scan_failure_recovery_loop',
                'outfitter_ship_ladder_intro',
                'outfitter_purchase_guardrail_recovery_loop',
                'shipyard_overfull_cargo_guardrail',
                'repair_service_recovery_loop',
                'repair_insufficient_credit_guardrail',
                'disabled_player_recovery_loop',
                'static_topology_source_readiness_scout',
                'system_service_provisioning_scout',
                'shift_click_multi_stop_route_queue',
                'route_queue_invalid_stop_guardrail',
                'route_queue_clear_guardrail',
                'route_queue_clear_reselect_guardrail',
                'near_center_jump_block',
                'route_planner_refuel_loop',
                'manual_route_low_fuel_recovery_landing_loop',
                'low_fuel_jump_recovery',
                'blocked_reason_curriculum',
                'legal_docking_service_gate_recovery',
                'weapon_reputation_gate_recovery',
                'weapon_credit_recovery_loop',
                'weapon_availability_recovery_loop',
                'weapon_purchase_mission_cargo_reservation_loop',
                'weapon_purchase_trade_cargo_reservation_loop',
                'weapon_purchase_secondary_activation_loop',
                'weapon_legal_docking_recovery_loop',
                'weapon_inventory_stack_recovery_loop',
                'contraband_scan_clemency_recovery',
                'contraband_scan_trade_recovery_loop',
                'contraband_trade_funds_clemency_loop',
                'legal_clemency_insufficient_credit_guardrail',
                'pirate_avoidance_escape_route',
                'pirate_avoidance_mission_trade_escape_loop',
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

    def test_commodity_partial_hold_recovery_loop_frees_space_then_buys_lot(self):
        result = run_scripted_scenario('commodity_partial_hold_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['cargoUsed'], 15)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 10)
        self.assertEqual(result['state']['cargoHold'].get('equipment', 0), 5)
        self.assertEqual(result['checks']['blocked_buy_with_only_partial_lot_space'], 'passed')
        self.assertEqual(result['checks']['freed_hold_space_by_selling_lot'], 'passed')
        self.assertEqual(result['checks']['recovered_by_buying_after_freeing_hold'], 'passed')
        self.assertEqual(result['checks']['recorded_partial_hold_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_commodity_lot']
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual([event['reason'] for event in blocked], ['insufficient cargo space'])
        self.assertEqual([event['type'] for event in trade_events], ['sell_commodity_lot', 'buy_commodity_lot'])
        self.assertEqual([event['commodity'] for event in trade_events], ['equipment', 'food'])
        self.assertEqual([event['cargoUsed'] for event in trade_events], [5, 15])
        labeled_events = blocked + trade_events
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-commodity-partial-hold-recovery-scaffold' for event in labeled_events))
        self.assertTrue(all(event['oracleStatus'] == 'commodity_partial_hold_recovery_pending_classic_runtime_trace' for event in labeled_events))

    def test_commodity_exact_credit_sellback_rebuy_loop_recovers_after_sellback(self):
        result = run_scripted_scenario('commodity_exact_credit_sellback_rebuy_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 0)
        self.assertEqual(result['state']['cargoUsed'], 10)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 10)
        self.assertEqual(result['checks']['exact_credit_buy_left_zero_credits'], 'passed')
        self.assertEqual(result['checks']['blocked_second_buy_without_credits'], 'passed')
        self.assertEqual(result['checks']['sellback_restored_exact_lot_budget'], 'passed')
        self.assertEqual(result['checks']['recovered_by_rebuying_after_sellback'], 'passed')
        self.assertEqual(result['checks']['recorded_exact_credit_rebuy_source_boundary'], 'passed')
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_commodity_lot']
        self.assertEqual([event['type'] for event in trade_events], ['buy_commodity_lot', 'sell_commodity_lot', 'buy_commodity_lot'])
        self.assertEqual([event['commodity'] for event in trade_events], ['food', 'food', 'food'])
        self.assertEqual([event['creditsAfter'] for event in trade_events], [0, 1200, 0])
        self.assertEqual([event['cargoUsed'] for event in trade_events], [10, 0, 10])
        self.assertEqual([event['reason'] for event in blocked], ['insufficient credits'])
        labeled_events = trade_events + blocked
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-commodity-exact-credit-sellback-rebuy-scaffold' for event in labeled_events))
        self.assertTrue(all(event['oracleStatus'] == 'commodity_exact_credit_rebuy_pending_classic_runtime_trace' for event in labeled_events))

    def test_commodity_exact_credit_full_hold_sellback_loop_recovers_after_sellback(self):
        result = run_scripted_scenario('commodity_exact_credit_full_hold_sellback_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 0)
        self.assertEqual(result['state']['cargoUsed'], 20)
        self.assertEqual(result['state']['cargoHold'].get('food', 0), 20)
        self.assertEqual(result['checks']['exact_credit_two_lots_filled_hold'], 'passed')
        self.assertEqual(result['checks']['blocked_third_buy_with_full_hold'], 'passed')
        self.assertEqual(result['checks']['sellback_freed_one_lot_and_budget'], 'passed')
        self.assertEqual(result['checks']['recovered_by_rebuying_to_full_hold'], 'passed')
        self.assertEqual(result['checks']['recorded_exact_credit_full_hold_source_boundary'], 'passed')
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_commodity_lot']
        self.assertEqual([event['type'] for event in trade_events], ['buy_commodity_lot', 'buy_commodity_lot', 'sell_commodity_lot', 'buy_commodity_lot'])
        self.assertEqual([event['creditsAfter'] for event in trade_events], [1200, 0, 1200, 0])
        self.assertEqual([event['cargoUsed'] for event in trade_events], [10, 20, 10, 20])
        self.assertEqual([event['reason'] for event in blocked], ['insufficient cargo space'])
        labeled_events = trade_events + blocked
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-commodity-exact-credit-full-hold-sellback-scaffold' for event in labeled_events))
        self.assertTrue(all(event['oracleStatus'] == 'commodity_exact_credit_full_hold_rebuy_pending_classic_runtime_trace' for event in labeled_events))

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

    def test_cross_market_exact_credit_profit_loop_sells_out_of_zero_credit_state(self):
        result = run_scripted_scenario('cross_market_exact_credit_profit_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 1200)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['checks']['exact_credit_sol_buy_left_zero_credits'], 'passed')
        self.assertEqual(result['checks']['blocked_second_sol_buy_without_credits'], 'passed')
        self.assertEqual(result['checks']['sold_profitable_lot_after_zero_credit_return'], 'passed')
        self.assertEqual(result['checks']['recorded_cross_market_exact_credit_source_boundary'], 'passed')
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_commodity_lot']
        self.assertEqual([event['type'] for event in trade_events], ['buy_commodity_lot', 'sell_commodity_lot'])
        self.assertEqual([event['system'] for event in trade_events], ['Sol', 'Levo'])
        self.assertEqual([event['creditsAfter'] for event in trade_events], [0, 1200])
        self.assertEqual([event['reason'] for event in blocked], ['insufficient credits'])
        labeled_events = trade_events + blocked
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-cross-market-exact-credit-profit-scaffold' for event in labeled_events))
        self.assertTrue(all(event['oracleStatus'] == 'cross_market_exact_credit_profit_pending_classic_runtime_trace' for event in labeled_events))

    def test_cross_market_exact_credit_full_hold_profit_loop_sells_full_hold_out_of_zero_credit_state(self):
        result = run_scripted_scenario('cross_market_exact_credit_full_hold_profit_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 2400)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['checks']['exact_credit_sol_buys_filled_hold'], 'passed')
        self.assertEqual(result['checks']['blocked_third_sol_buy_with_full_hold'], 'passed')
        self.assertEqual(result['checks']['sold_full_hold_after_zero_credit_return'], 'passed')
        self.assertEqual(result['checks']['recorded_cross_market_exact_credit_full_hold_source_boundary'], 'passed')
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_commodity_lot']
        self.assertEqual([event['type'] for event in trade_events], ['buy_commodity_lot', 'buy_commodity_lot', 'sell_commodity_lot', 'sell_commodity_lot'])
        self.assertEqual([event['system'] for event in trade_events], ['Sol', 'Sol', 'Levo', 'Levo'])
        self.assertEqual([event['creditsAfter'] for event in trade_events], [420, 0, 1200, 2400])
        self.assertEqual([event['cargoUsed'] for event in trade_events], [10, 20, 10, 0])
        self.assertEqual([event['reason'] for event in blocked], ['insufficient cargo space'])
        labeled_events = trade_events + blocked
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-cross-market-exact-credit-full-hold-profit-scaffold' for event in labeled_events))
        self.assertTrue(all(event['oracleStatus'] == 'cross_market_exact_credit_full_hold_profit_pending_classic_runtime_trace' for event in labeled_events))

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

    def test_trade_route_margin_choice_loop_carries_positive_margin_and_skips_bad_cargo(self):
        result = run_scripted_scenario('trade_route_margin_choice_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['credits'], 10780)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['checks']['identified_profitable_food_margin'], 'passed')
        self.assertEqual(result['checks']['skipped_negative_equipment_margin'], 'passed')
        self.assertEqual(result['checks']['carried_only_profitable_food_lot'], 'passed')
        self.assertEqual(result['checks']['recorded_margin_choice_source_boundary'], 'passed')
        decisions = [event for event in result['trace'] if event['type'] == 'trade_margin_decision']
        self.assertEqual([event['commodity'] for event in decisions], ['food', 'equipment'])
        self.assertEqual([event['decision'] for event in decisions], ['carry', 'skip'])
        self.assertEqual([event['marginPerTon'] for event in decisions], [78, -210])
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual([event['commodity'] for event in trade_events], ['food', 'food'])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-trade-margin-choice-scaffold' for event in decisions + trade_events))
        self.assertTrue(all(event['oracleStatus'] == 'trade_margin_choice_pending_classic_runtime_trace' for event in decisions + trade_events))

    def test_strategy_skill_rotation_loop_records_distinct_playstyle_checkpoints(self):
        result = run_scripted_scenario('strategy_skill_rotation_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['recorded_strategy_skill_rotation'], 'passed')
        self.assertEqual(result['checks']['completed_strategy_trade_leg'], 'passed')
        self.assertEqual(result['checks']['completed_strategy_mission_leg'], 'passed')
        self.assertEqual(result['checks']['recorded_strategy_source_boundary'], 'passed')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['merchant', 'mission_runner', 'route_planner'])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-strategy-skill-rotation-scaffold' for event in checkpoints))
        self.assertTrue(all(event['oracleStatus'] == 'strategy_skill_progression_pending_ev_family_source_trace' for event in checkpoints))
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertIn('intro_courier_earth_hera', result['state']['completedJobs'])

    def test_upgrade_readiness_strategy_loop_records_service_outfit_weapon_and_ship_checkpoints(self):
        result = run_scripted_scenario('upgrade_readiness_strategy_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['scanned_upgrade_service_matrix'], 'passed')
        self.assertEqual(result['checks']['bought_outfit_weapon_and_ship_upgrade'], 'passed')
        self.assertEqual(result['checks']['recorded_upgrade_readiness_strategy_checkpoints'], 'passed')
        self.assertEqual(result['checks']['recorded_upgrade_readiness_source_boundary'], 'passed')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['service_scout', 'outfitter', 'weapons', 'ship_buyer'])
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['ownedOutfits'].get('cargo_pod'), 1)
        self.assertEqual(result['state']['ownedWeapons'].get('laser_cannon'), 1)
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-upgrade-readiness-strategy-scaffold' for event in checkpoints))
        self.assertTrue(all(event['oracleStatus'] == 'upgrade_strategy_progression_pending_ev_family_source_trace' for event in checkpoints))

    def test_upgrade_affordability_trade_loop_funds_upgrade_after_initial_credit_gate(self):
        result = run_scripted_scenario('upgrade_affordability_trade_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['blocked_initial_light_freighter_purchase'], 'passed')
        self.assertEqual(result['checks']['completed_upgrade_funding_trade_run'], 'passed')
        self.assertEqual(result['checks']['bought_affordable_light_freighter_upgrade'], 'passed')
        self.assertEqual(result['checks']['recorded_upgrade_affordability_source_boundary'], 'passed')
        blocked_ship_events = [event for event in result['trace'] if event['type'] == 'blocked_buy_ship']
        self.assertEqual(blocked_ship_events[0]['reason'], 'insufficient credits')
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertGreaterEqual(len(trade_events), 2)
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['affordability_gap', 'trade_funding_run', 'ship_buyer'])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-upgrade-affordability-strategy-scaffold' for event in checkpoints))
        self.assertTrue(all(event['oracleStatus'] == 'upgrade_affordability_progression_pending_ev_family_source_trace' for event in checkpoints))
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertGreaterEqual(result['state']['credits'], 0)

    def test_cargo_expansion_trade_loop_uses_cargo_pod_for_third_trade_lot(self):
        result = run_scripted_scenario('cargo_expansion_trade_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['blocked_third_lot_before_cargo_pod'], 'passed')
        self.assertEqual(result['checks']['bought_cargo_pod_capacity_upgrade'], 'passed')
        self.assertEqual(result['checks']['completed_expanded_three_lot_trade_run'], 'passed')
        self.assertEqual(result['checks']['recorded_cargo_expansion_source_boundary'], 'passed')
        blocked_buy_events = [event for event in result['trace'] if event['type'] == 'blocked_buy_commodity_lot']
        self.assertEqual(blocked_buy_events[0]['reason'], 'insufficient cargo space')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['capacity_gap', 'cargo_pod_upgrade', 'expanded_trade_run'])
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual([event['commodity'] for event in trade_events], ['food', 'food', 'food', 'food', 'food', 'food'])
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['cargoCapacity'], 30)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['credits'], 11140)
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-cargo-expansion-trade-scaffold' for event in checkpoints + trade_events))
        self.assertTrue(all(event['oracleStatus'] == 'cargo_expansion_trade_pending_classic_runtime_trace' for event in checkpoints + trade_events))

    def test_fuel_reserve_upgrade_loop_buys_aux_tank_and_refuels_expanded_reserve(self):
        result = run_scripted_scenario('fuel_reserve_upgrade_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_auxiliary_fuel_tank_upgrade'], 'passed')
        self.assertEqual(result['checks']['refueled_to_expanded_reserve'], 'passed')
        self.assertEqual(result['checks']['completed_fuel_reserve_return_hop'], 'passed')
        self.assertEqual(result['checks']['recorded_fuel_reserve_source_boundary'], 'passed')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['fuel_range_gap', 'fuel_tank_upgrade', 'expanded_reserve_return'])
        refuel_events = [event for event in result['trace'] if event['type'] == 'refuel']
        self.assertEqual(refuel_events[-1]['fuelAfter'], 31)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['maxFuel'], 31)
        self.assertEqual(result['state']['fuel'], 30)
        self.assertEqual(result['state']['ownedOutfits'].get('fuel_tank'), 1)
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-fuel-reserve-upgrade-scaffold' for event in checkpoints))
        self.assertTrue(all(event['oracleStatus'] == 'fuel_reserve_upgrade_pending_classic_runtime_trace' for event in checkpoints))

    def test_hull_plating_repair_loop_buys_armor_and_repairs_added_hull(self):
        result = run_scripted_scenario('hull_plating_repair_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_hull_plating_upgrade'], 'passed')
        self.assertEqual(result['checks']['repaired_added_hull_capacity'], 'passed')
        self.assertEqual(result['checks']['recorded_hull_refit_source_boundary'], 'passed')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['armor_refit_gap', 'hull_plating_upgrade', 'repair_service_fill'])
        outfit_events = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon' and event['itemId'] == 'hull_plating']
        repair_events = [event for event in result['trace'] if event['type'] == 'repair_hull']
        self.assertEqual(outfit_events[-1]['maxHull'], 125)
        self.assertEqual(repair_events[-1]['hullBefore'], 100)
        self.assertEqual(repair_events[-1]['hullAfter'], 125)
        self.assertEqual(repair_events[-1]['cost'], 200)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['ownedOutfits'].get('hull_plating'), 1)
        self.assertEqual(result['state']['maxHull'], 125)
        self.assertEqual(result['state']['currentHull'], 125)
        self.assertEqual(result['state']['credits'], 8000)
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-hull-plating-repair-scaffold' for event in checkpoints + outfit_events))
        self.assertTrue(all(event['oracleStatus'] == 'hull_plating_repair_pending_classic_runtime_trace' for event in checkpoints + outfit_events))

    def test_balanced_upgrade_trade_loop_funds_final_refit_with_trade_run(self):
        result = run_scripted_scenario('balanced_upgrade_trade_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['blocked_hull_plating_until_trade_funding'], 'passed')
        self.assertEqual(result['checks']['completed_balanced_upgrade_trade_run'], 'passed')
        self.assertEqual(result['checks']['bought_cargo_fuel_and_hull_upgrades'], 'passed')
        self.assertEqual(result['checks']['repaired_final_hull_refit'], 'passed')
        self.assertEqual(result['checks']['recorded_balanced_upgrade_source_boundary'], 'passed')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['budget_gap_after_cargo_and_fuel', 'trade_funded_final_refit', 'balanced_refit_complete'])
        blocked_outfit_events = [event for event in result['trace'] if event['type'] == 'blocked_buy_outfit_or_weapon']
        self.assertEqual(blocked_outfit_events[0]['itemId'], 'hull_plating')
        self.assertEqual(blocked_outfit_events[0]['reason'], 'insufficient credits')
        self.assertEqual(blocked_outfit_events[0]['credits'], 900)
        outfit_events = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon']
        self.assertEqual([event['itemId'] for event in outfit_events], ['cargo_pod', 'fuel_tank', 'hull_plating'])
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual([event['commodity'] for event in trade_events], ['food', 'food', 'food', 'food'])
        repair_events = [event for event in result['trace'] if event['type'] == 'repair_hull']
        self.assertEqual(repair_events[-1]['cost'], 200)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['ownedOutfits'].get('cargo_pod'), 1)
        self.assertEqual(result['state']['ownedOutfits'].get('fuel_tank'), 1)
        self.assertEqual(result['state']['ownedOutfits'].get('hull_plating'), 1)
        self.assertEqual(result['state']['cargoCapacity'], 30)
        self.assertEqual(result['state']['maxFuel'], 31)
        self.assertEqual(result['state']['maxHull'], 125)
        self.assertEqual(result['state']['currentHull'], 125)
        self.assertEqual(result['state']['credits'], 460)
        source_events = checkpoints + outfit_events + blocked_outfit_events + trade_events
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-balanced-upgrade-trade-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'balanced_upgrade_budget_pending_classic_runtime_trace' for event in source_events))

    def test_light_freighter_capacity_trade_loop_uses_ship_capacity_for_large_return_load(self):
        result = run_scripted_scenario('light_freighter_capacity_trade_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_capacity_upgrade'], 'passed')
        self.assertEqual(result['checks']['completed_large_freighter_trade_run'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_trade_source_boundary'], 'passed')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['ship_capacity_upgrade', 'large_hold_trade_run'])
        buy_ship_events = [event for event in result['trace'] if event['type'] == 'buy_ship']
        self.assertEqual(buy_ship_events[-1]['shipId'], 'light_freighter')
        self.assertEqual(buy_ship_events[-1]['cargoCapacityAfter'], 150)
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual(len([event for event in trade_events if event['type'] == 'buy_commodity_lot']), 6)
        self.assertEqual(len([event for event in trade_events if event['type'] == 'sell_commodity_lot']), 6)
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['cargoCapacity'], 150)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['currentSystem'], START_SYSTEM)
        self.assertEqual(result['state']['landedBody'], START_BODY)
        self.assertEqual(result['state']['credits'], 10858)
        source_events = checkpoints + buy_ship_events + trade_events
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-trade-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_trade_pending_classic_runtime_trace' for event in source_events))

    def test_light_freighter_mission_trade_loop_reserves_mission_cargo_alongside_bulk_trade(self):
        result = run_scripted_scenario('light_freighter_mission_trade_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_mission_trade_capacity'], 'passed')
        self.assertEqual(result['checks']['accepted_bulk_mission_and_trade_load'], 'passed')
        self.assertEqual(result['checks']['delivered_bulk_mission_before_trade_sale'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_mission_trade_source_boundary'], 'passed')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['bulk_mission_capacity', 'mission_trade_cargo_recovery'])
        mission_accepts = [event for event in result['trace'] if event['type'] == 'accept_cargo_job']
        self.assertEqual(mission_accepts[-1]['tons'], 80)
        self.assertEqual(mission_accepts[-1]['cargoUsed'], 80)
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual(len([event for event in trade_events if event['type'] == 'buy_commodity_lot']), 6)
        self.assertEqual(len([event for event in trade_events if event['type'] == 'sell_commodity_lot']), 6)
        self.assertEqual(max(event['cargoUsed'] for event in trade_events), 140)
        complete_events = [event for event in result['trace'] if event['type'] == 'complete_cargo_job']
        self.assertEqual(complete_events[-1]['cargoUsed'], 60)
        self.assertEqual(result['state']['currentSystem'], START_SYSTEM)
        self.assertEqual(result['state']['landedBody'], START_BODY)
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['cargoCapacity'], 150)
        self.assertEqual(result['state']['completedJobs'], ['levo_bulk_freighter_supply'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['credits'], 16880)
        source_events = checkpoints + mission_accepts + complete_events + trade_events + [event for event in result['trace'] if event['type'] == 'buy_ship']
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-mission-trade-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_mission_trade_pending_classic_runtime_trace' for event in source_events))

    def test_light_freighter_refuel_delivery_loop_recovers_low_fuel_bulk_delivery(self):
        result = run_scripted_scenario('light_freighter_refuel_delivery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_refuel_delivery'], 'passed')
        self.assertEqual(result['checks']['blocked_bulk_delivery_on_low_fuel'], 'passed')
        self.assertEqual(result['checks']['delivered_bulk_mission_after_refuel'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_refuel_delivery_source_boundary'], 'passed')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['bulk_delivery_refuel_gap', 'refueled_bulk_delivery_recovery'])
        blocked_jumps = [event for event in result['trace'] if event['type'] == 'blocked_jump']
        self.assertEqual(blocked_jumps[-1]['reason'], 'insufficient fuel')
        refuels = [event for event in result['trace'] if event['type'] == 'refuel']
        self.assertEqual(refuels[-1]['fuelAfter'], 300)
        complete_events = [event for event in result['trace'] if event['type'] == 'complete_cargo_job']
        self.assertEqual(complete_events[-1]['id'], 'levo_bulk_refuel_supply')
        self.assertEqual(result['state']['currentSystem'], START_SYSTEM)
        self.assertEqual(result['state']['landedBody'], START_BODY)
        self.assertEqual(result['state']['completedJobs'], ['levo_bulk_refuel_supply'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['fuel'], 299)
        self.assertEqual(result['state']['credits'], 12200)
        source_events = checkpoints + [event for event in result['trace'] if event['type'] in {'buy_ship', 'accept_cargo_job', 'complete_cargo_job'}]
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-refuel-delivery-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_refuel_delivery_pending_classic_runtime_trace' for event in source_events))

    def test_light_freighter_deadline_refuel_delivery_loop_completes_last_day_after_refuel(self):
        result = run_scripted_scenario('light_freighter_deadline_refuel_delivery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_deadline_refuel_delivery'], 'passed')
        self.assertEqual(result['checks']['reserved_timed_bulk_delivery_before_low_fuel_block'], 'passed')
        self.assertEqual(result['checks']['blocked_timed_bulk_delivery_on_low_fuel'], 'passed')
        self.assertEqual(result['checks']['completed_last_day_bulk_delivery_after_refuel'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_deadline_refuel_delivery_source_boundary'], 'passed')
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['timed_bulk_delivery_refuel_gap', 'last_day_refueled_bulk_delivery_recovery'])
        blocked_jumps = [event for event in result['trace'] if event['type'] == 'blocked_jump']
        self.assertEqual(blocked_jumps[-1]['reason'], 'insufficient fuel')
        refuels = [event for event in result['trace'] if event['type'] == 'refuel']
        self.assertEqual(refuels[-1]['fuelAfter'], 300)
        complete_events = [event for event in result['trace'] if event['type'] == 'complete_cargo_job']
        self.assertEqual(complete_events[-1]['id'], 'levo_bulk_deadline_refuel_supply')
        self.assertEqual(result['state']['currentDay'], 2)
        self.assertEqual(result['state'].get('failedJobs', []), [])
        self.assertNotIn('fail_mission_bit_46', result['state']['storyFlags'])
        self.assertEqual(result['state']['currentSystem'], START_SYSTEM)
        self.assertEqual(result['state']['landedBody'], START_BODY)
        self.assertEqual(result['state']['completedJobs'], ['levo_bulk_deadline_refuel_supply'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['fuel'], 299)
        self.assertEqual(result['state']['credits'], 12200)
        source_events = checkpoints + [event for event in result['trace'] if event['type'] in {'buy_ship', 'accept_cargo_job', 'complete_cargo_job'}]
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-deadline-refuel-delivery-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_deadline_refuel_delivery_pending_classic_runtime_trace' for event in source_events))

    def test_light_freighter_bulk_margin_choice_loop_fills_hold_with_positive_margin(self):
        result = run_scripted_scenario('light_freighter_bulk_margin_choice_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_bulk_margin_choice'], 'passed')
        self.assertEqual(result['checks']['identified_profitable_bulk_food_margin'], 'passed')
        self.assertEqual(result['checks']['skipped_negative_bulk_equipment_margin'], 'passed')
        self.assertEqual(result['checks']['filled_freighter_with_profitable_food_only'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_bulk_margin_source_boundary'], 'passed')
        decisions = [event for event in result['trace'] if event['type'] == 'trade_margin_decision']
        self.assertEqual([(event['commodity'], event['marginPerTon'], event['decision']) for event in decisions], [('food', 78, 'carry'), ('equipment', -210, 'skip')])
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual(len([event for event in trade_events if event['type'] == 'buy_commodity_lot']), 15)
        self.assertEqual(len([event for event in trade_events if event['type'] == 'sell_commodity_lot']), 15)
        self.assertEqual(max(event['cargoUsed'] for event in trade_events), 150)
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['bulk_margin_choice', 'full_hold_margin_sale'])
        self.assertEqual(result['state']['currentSystem'], START_SYSTEM)
        self.assertEqual(result['state']['landedBody'], START_BODY)
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['cargoCapacity'], 150)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['credits'], 22878)
        source_events = decisions + trade_events + checkpoints + [event for event in result['trace'] if event['type'] == 'buy_ship']
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-bulk-margin-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_bulk_margin_pending_classic_runtime_trace' for event in source_events))

    def test_light_freighter_bulk_mission_margin_loop_fills_remaining_hold_after_reservation(self):
        result = run_scripted_scenario('light_freighter_bulk_mission_margin_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_bulk_mission_margin'], 'passed')
        self.assertEqual(result['checks']['reserved_bulk_delivery_before_margin_choice'], 'passed')
        self.assertEqual(result['checks']['identified_remaining_hold_profitable_food_margin'], 'passed')
        self.assertEqual(result['checks']['skipped_negative_return_equipment_with_reserved_cargo'], 'passed')
        self.assertEqual(result['checks']['filled_remaining_hold_with_profitable_food'], 'passed')
        self.assertEqual(result['checks']['completed_bulk_mission_then_sold_margin_cargo'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_bulk_mission_margin_source_boundary'], 'passed')
        decisions = [event for event in result['trace'] if event['type'] == 'trade_margin_decision']
        self.assertEqual([(event['commodity'], event['marginPerTon'], event['decision']) for event in decisions], [('food', 78, 'carry'), ('equipment', -210, 'skip')])
        mission_accepts = [event for event in result['trace'] if event['type'] == 'accept_cargo_job']
        self.assertEqual(mission_accepts[-1]['id'], 'levo_bulk_margin_supply')
        self.assertEqual(mission_accepts[-1]['cargoUsed'], 120)
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual(len([event for event in trade_events if event['type'] == 'buy_commodity_lot']), 3)
        self.assertEqual(len([event for event in trade_events if event['type'] == 'sell_commodity_lot']), 3)
        self.assertEqual(max(event['cargoUsed'] for event in trade_events), 150)
        complete_events = [event for event in result['trace'] if event['type'] == 'complete_cargo_job']
        self.assertEqual(complete_events[-1]['cargoUsed'], 30)
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['reserved_bulk_margin_choice', 'bulk_mission_margin_sale'])
        self.assertEqual(result['state']['currentSystem'], START_SYSTEM)
        self.assertEqual(result['state']['landedBody'], START_BODY)
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['cargoCapacity'], 150)
        self.assertEqual(result['state']['completedJobs'], ['levo_bulk_margin_supply'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['credits'], 19540)
        source_events = decisions + trade_events + checkpoints + mission_accepts + complete_events + [event for event in result['trace'] if event['type'] == 'buy_ship']
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-bulk-mission-margin-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_bulk_mission_margin_pending_classic_runtime_trace' for event in source_events))

    def test_light_freighter_refuel_mission_margin_loop_refuels_before_margin_delivery(self):
        result = run_scripted_scenario('light_freighter_refuel_mission_margin_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_refuel_mission_margin'], 'passed')
        self.assertEqual(result['checks']['reserved_bulk_delivery_before_refuel_margin_choice'], 'passed')
        self.assertEqual(result['checks']['picked_profitable_margin_cargo_before_low_fuel_block'], 'passed')
        self.assertEqual(result['checks']['blocked_loaded_margin_delivery_on_low_fuel'], 'passed')
        self.assertEqual(result['checks']['refueled_then_completed_bulk_mission_margin_sale'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_refuel_mission_margin_source_boundary'], 'passed')
        decisions = [event for event in result['trace'] if event['type'] == 'trade_margin_decision']
        self.assertEqual([(event['commodity'], event['marginPerTon'], event['decision']) for event in decisions], [('food', 78, 'carry'), ('equipment', -210, 'skip')])
        blocked_jumps = [event for event in result['trace'] if event['type'] == 'blocked_jump']
        self.assertEqual(blocked_jumps[-1]['reason'], 'insufficient fuel')
        refuels = [event for event in result['trace'] if event['type'] == 'refuel']
        self.assertEqual(refuels[-1]['fuelAfter'], 300)
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual(len([event for event in trade_events if event['type'] == 'buy_commodity_lot']), 3)
        self.assertEqual(len([event for event in trade_events if event['type'] == 'sell_commodity_lot']), 3)
        self.assertEqual(max(event['cargoUsed'] for event in trade_events), 150)
        complete_events = [event for event in result['trace'] if event['type'] == 'complete_cargo_job']
        self.assertEqual(complete_events[-1]['id'], 'levo_bulk_refuel_margin_supply')
        self.assertEqual(complete_events[-1]['cargoUsed'], 30)
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['reserved_bulk_refuel_margin_choice', 'refueled_bulk_mission_margin_sale'])
        self.assertEqual(result['state']['currentSystem'], START_SYSTEM)
        self.assertEqual(result['state']['landedBody'], START_BODY)
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['cargoCapacity'], 150)
        self.assertEqual(result['state']['completedJobs'], ['levo_bulk_refuel_margin_supply'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['fuel'], 299)
        self.assertEqual(result['state']['credits'], 19540)
        source_events = decisions + trade_events + checkpoints + [event for event in result['trace'] if event['type'] in {'buy_ship', 'accept_cargo_job', 'complete_cargo_job'}]
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-refuel-mission-margin-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_refuel_mission_margin_pending_classic_runtime_trace' for event in source_events))

    def test_light_freighter_repair_margin_loop_funds_hull_repair_after_margin_sale(self):
        result = run_scripted_scenario('light_freighter_repair_margin_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_repair_margin'], 'passed')
        self.assertEqual(result['checks']['identified_profitable_repair_margin_food'], 'passed')
        self.assertEqual(result['checks']['funded_repair_with_margin_sale'], 'passed')
        self.assertEqual(result['checks']['repaired_light_freighter_hull_after_trade'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_repair_margin_source_boundary'], 'passed')
        decisions = [event for event in result['trace'] if event['type'] == 'trade_margin_decision']
        self.assertEqual([(event['commodity'], event['marginPerTon'], event['decision']) for event in decisions], [('food', 78, 'carry')])
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual(len([event for event in trade_events if event['type'] == 'buy_commodity_lot']), 2)
        self.assertEqual(len([event for event in trade_events if event['type'] == 'sell_commodity_lot']), 2)
        repair_events = [event for event in result['trace'] if event['type'] == 'repair_hull']
        self.assertEqual(repair_events[-1]['hullBefore'], 260)
        self.assertEqual(repair_events[-1]['hullAfter'], 300)
        self.assertEqual(repair_events[-1]['cost'], 320)
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['repair_margin_gap', 'margin_sale_repair_budget', 'light_freighter_repaired'])
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['cargoCapacity'], 150)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['currentHull'], 300)
        self.assertEqual(result['state']['credits'], 2080)
        source_events = decisions + trade_events + checkpoints + [event for event in result['trace'] if event['type'] == 'buy_ship']
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-repair-margin-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_repair_margin_pending_classic_runtime_trace' for event in source_events))
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-repair-service-scaffold' for event in repair_events))
        self.assertTrue(all(event['oracleStatus'] == 'repair_service_pending_ev_classic_runtime_trace' for event in repair_events))


    def test_light_freighter_repair_mission_margin_loop_repairs_after_bulk_delivery_and_margin_sale(self):
        result = run_scripted_scenario('light_freighter_repair_mission_margin_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_repair_mission_margin'], 'passed')
        self.assertEqual(result['checks']['reserved_bulk_delivery_while_damaged'], 'passed')
        self.assertEqual(result['checks']['filled_remaining_hold_with_profitable_repair_cargo'], 'passed')
        self.assertEqual(result['checks']['completed_bulk_mission_and_sold_repair_margin_cargo'], 'passed')
        self.assertEqual(result['checks']['repaired_light_freighter_after_bulk_mission_margin'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_repair_mission_margin_source_boundary'], 'passed')
        decisions = [event for event in result['trace'] if event['type'] == 'trade_margin_decision']
        self.assertEqual([(event['commodity'], event['marginPerTon'], event['decision']) for event in decisions], [('food', 78, 'carry'), ('equipment', -210, 'skip')])
        trade_events = [event for event in result['trace'] if event['type'] in {'buy_commodity_lot', 'sell_commodity_lot'}]
        self.assertEqual(len([event for event in trade_events if event['type'] == 'buy_commodity_lot']), 3)
        self.assertEqual(len([event for event in trade_events if event['type'] == 'sell_commodity_lot']), 3)
        self.assertEqual(max(event['cargoUsed'] for event in trade_events), 150)
        complete_events = [event for event in result['trace'] if event['type'] == 'complete_cargo_job']
        self.assertEqual(complete_events[-1]['id'], 'levo_bulk_repair_margin_supply')
        self.assertEqual(complete_events[-1]['cargoUsed'], 30)
        repair_events = [event for event in result['trace'] if event['type'] == 'repair_hull']
        self.assertEqual(repair_events[-1]['hullBefore'], 260)
        self.assertEqual(repair_events[-1]['hullAfter'], 300)
        self.assertEqual(repair_events[-1]['cost'], 320)
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['damaged_freighter_mission_margin_choice', 'mission_margin_repair_budget', 'mission_margin_light_freighter_repaired'])
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['cargoCapacity'], 150)
        self.assertEqual(result['state']['completedJobs'], ['levo_bulk_repair_margin_supply'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['currentHull'], 300)
        self.assertEqual(result['state']['credits'], 9302)
        source_events = decisions + trade_events + checkpoints + [event for event in result['trace'] if event['type'] in {'buy_ship', 'accept_cargo_job', 'complete_cargo_job'}]
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-repair-mission-margin-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_repair_mission_margin_pending_classic_runtime_trace' for event in source_events))
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-repair-service-scaffold' for event in repair_events))
        self.assertTrue(all(event['oracleStatus'] == 'repair_service_pending_ev_classic_runtime_trace' for event in repair_events))

    def test_light_freighter_repair_refuel_mission_margin_loop_refuels_before_repair_return(self):
        result = run_scripted_scenario('light_freighter_repair_refuel_mission_margin_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_repair_refuel_mission_margin'], 'passed')
        self.assertEqual(result['checks']['reserved_bulk_delivery_while_damaged_and_low_fuel'], 'passed')
        self.assertEqual(result['checks']['blocked_empty_fuel_repair_return_after_delivery'], 'passed')
        self.assertEqual(result['checks']['refueled_before_repair_port_return'], 'passed')
        self.assertEqual(result['checks']['repaired_light_freighter_after_refueled_bulk_mission_margin'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_repair_refuel_mission_margin_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_jump']
        self.assertTrue(any(event.get('reason') == 'insufficient fuel' and event.get('destinationSystem') == 'Sol' for event in blocked))
        refuel_events = [event for event in result['trace'] if event['type'] == 'refuel']
        self.assertEqual(refuel_events[-1]['system'], 'Levo')
        self.assertEqual(refuel_events[-1]['body'], 'Levo Spaceport')
        self.assertEqual(refuel_events[-1]['fuelAfter'], 300)
        repair_events = [event for event in result['trace'] if event['type'] == 'repair_hull']
        self.assertEqual(repair_events[-1]['hullBefore'], 260)
        self.assertEqual(repair_events[-1]['hullAfter'], 300)
        self.assertEqual(repair_events[-1]['cost'], 320)
        checkpoints = [event for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual([event['skill'] for event in checkpoints], ['damaged_freighter_refuel_repair_margin_choice', 'refueled_repair_return_budget', 'refueled_mission_margin_light_freighter_repaired'])
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['completedJobs'], ['levo_bulk_repair_refuel_margin_supply'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['currentHull'], 300)
        self.assertEqual(result['state']['fuel'], 299)
        self.assertEqual(result['state']['credits'], 9302)
        source_events = [event for event in result['trace'] if event['type'] in {'buy_ship', 'accept_cargo_job', 'complete_cargo_job', 'trade_margin_decision', 'buy_commodity_lot', 'sell_commodity_lot', 'strategy_skill_checkpoint'}]
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-repair-refuel-mission-margin-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_repair_refuel_mission_margin_pending_classic_runtime_trace' for event in source_events))
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-repair-service-scaffold' for event in repair_events))
        self.assertTrue(all(event['oracleStatus'] == 'repair_service_pending_ev_classic_runtime_trace' for event in repair_events))

    def test_light_freighter_deadline_repair_refuel_margin_loop_delivers_before_repair(self):
        result = run_scripted_scenario('light_freighter_deadline_repair_refuel_margin_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['bought_light_freighter_for_deadline_repair_refuel_margin'], 'passed')
        self.assertEqual(result['checks']['reserved_timed_bulk_delivery_while_damaged_and_low_fuel'], 'passed')
        self.assertEqual(result['checks']['delivered_timed_bulk_before_repair_return'], 'passed')
        self.assertEqual(result['checks']['blocked_empty_fuel_deadline_repair_return_after_delivery'], 'passed')
        self.assertEqual(result['checks']['refueled_before_deadline_repair_port_return'], 'passed')
        self.assertEqual(result['checks']['repaired_light_freighter_after_deadline_refuel_margin'], 'passed')
        self.assertEqual(result['checks']['recorded_light_freighter_deadline_repair_refuel_margin_source_boundary'], 'passed')
        self.assertEqual(result['state']['currentDay'], 2)
        self.assertEqual(result['state'].get('failedJobs', []), [])
        self.assertNotIn('fail_mission_bit_45', result['state']['storyFlags'])
        self.assertEqual(result['state']['reputation']['Federation'], 5)
        self.assertEqual(result['state']['completedJobs'], ['levo_bulk_deadline_repair_refuel_margin_supply'])
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['currentHull'], 300)
        source_events = [event for event in result['trace'] if event['type'] in {'buy_ship', 'accept_cargo_job', 'complete_cargo_job', 'trade_margin_decision', 'buy_commodity_lot', 'sell_commodity_lot', 'strategy_skill_checkpoint'}]
        repair_events = [event for event in result['trace'] if event['type'] == 'repair_hull']
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-light-freighter-deadline-repair-refuel-margin-scaffold' for event in source_events))
        self.assertTrue(all(event['oracleStatus'] == 'light_freighter_deadline_repair_refuel_margin_pending_classic_runtime_trace' for event in source_events))
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-repair-service-scaffold' for event in repair_events))
        self.assertTrue(all(event['oracleStatus'] == 'repair_service_pending_ev_classic_runtime_trace' for event in repair_events))

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

    def test_alignment_completion_offer_scan_hides_closed_branch_offers(self):
        result = run_scripted_scenario('alignment_completion_offer_scan_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['checks']['fed_completion_hides_alignment_offers'], 'passed')
        self.assertEqual(result['checks']['freeport_completion_hides_alignment_offers'], 'passed')
        self.assertEqual(result['checks']['recorded_completion_scan_source_boundary'], 'passed')
        scans = [event for event in result['trace'] if event['type'] == 'scan_mission_offers']
        self.assertEqual(len(scans), 2)
        for scan in scans:
            mission_offers = scan['offersBySurface']['Mission Computer']
            self.assertNotIn('federation_report_freeport', mission_offers)
            self.assertNotIn('freeport_pact_smugglers', mission_offers)
            self.assertEqual(mission_offers, ['freeport_return_earth'])
        self.assertEqual(scans[0]['sourceLabel'], 'terminal-velocity-observed')
        self.assertEqual(scans[0]['oracleStatus'], 'terminal_velocity_eval_pending_original_trace')

    def test_alignment_return_contract_offer_timing_guardrail_spans_branch_states(self):
        result = run_scripted_scenario('alignment_return_contract_offer_timing_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['checks']['return_contract_visible_with_alignment_offers'], 'passed')
        self.assertEqual(result['checks']['return_contract_visible_after_alignment_completion'], 'passed')
        self.assertEqual(result['checks']['recorded_return_offer_timing_source_boundary'], 'passed')
        scans = [event for event in result['trace'] if event['type'] == 'scan_mission_offers']
        self.assertEqual(len(scans), 2)
        self.assertEqual(
            scans[0]['offersBySurface']['Mission Computer'],
            ['freeport_return_earth', 'federation_report_freeport', 'freeport_pact_smugglers'],
        )
        self.assertEqual(scans[1]['offersBySurface']['Mission Computer'], ['freeport_return_earth'])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-observed' for event in scans))

    def test_alignment_completion_return_contract_accepts_after_either_branch(self):
        result = run_scripted_scenario('alignment_completion_return_contract_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['checks']['accepted_return_contract_after_each_alignment'], 'passed')
        self.assertEqual(result['checks']['completed_return_contract_after_each_alignment'], 'passed')
        self.assertEqual(result['checks']['recorded_return_contract_source_boundary'], 'passed')
        accepts = [event for event in result['trace'] if event.get('type') == 'accept_cargo_job' and event.get('id') == 'freeport_return_earth']
        completions = [event for event in result['trace'] if event.get('type') == 'complete_cargo_job' and event.get('id') == 'freeport_return_earth']
        self.assertEqual(len(accepts), 2)
        self.assertEqual(len(completions), 2)
        self.assertEqual([event['reservedCargoTons'] for event in accepts], [5, 5])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-mission-scaffold' for event in accepts))

    def test_mission_destination_route_hint_sets_route_to_active_contract_destination(self):
        result = run_scripted_scenario('mission_destination_route_hint')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['routeQueue'], ['Centauri'])
        self.assertEqual(result['checks']['queued_active_mission_destination'], 'passed')
        self.assertEqual(result['trace'][-1]['destinationSystem'], 'Centauri')
        self.assertEqual(result['trace'][-1]['fuelRequired'], 1)
        self.assertEqual(result['trace'][-1]['fuelAvailable'], 5)
        self.assertFalse(result['trace'][-1]['fuelWarning'])
        self.assertIn('1 jump(s), fuel 5/6', result['trace'][-1]['objectiveHint'])
        self.assertIsNone(result['trace'][-1]['refuelRecoveryBody'])
        self.assertEqual(result['trace'][-1]['sourceLabel'], 'terminal-velocity-design-scaffold')

    def test_mission_destination_low_fuel_route_hint_names_refuel_recovery_body(self):
        result = run_scripted_scenario('mission_destination_low_fuel_route_hint')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['routeQueue'], ['Centauri'])
        self.assertEqual(result['checks']['queued_active_mission_destination'], 'passed')
        self.assertEqual(result['checks']['warned_low_fuel_before_mission_route'], 'passed')
        route_event = result['trace'][-1]
        self.assertEqual(route_event['fuelRequired'], 1)
        self.assertEqual(route_event['fuelAvailable'], 0)
        self.assertTrue(route_event['fuelWarning'])
        self.assertEqual(route_event['refuelRecoveryBody'], 'Earth')
        self.assertIn('refuel before full route; nearest refuel: Earth', route_event['objectiveHint'])
        self.assertEqual(route_event['sourceLabel'], 'terminal-velocity-design-scaffold')

    def test_mission_route_refuel_delivery_loop_recovers_and_delivers(self):
        result = run_scripted_scenario('mission_route_refuel_delivery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['queued_active_mission_destination'], 'passed')
        self.assertEqual(result['checks']['warned_low_fuel_before_mission_route'], 'passed')
        self.assertEqual(result['checks']['blocked_jump_before_refuel'], 'passed')
        self.assertEqual(result['checks']['refueled_at_recovery_body'], 'passed')
        self.assertEqual(result['checks']['delivered_mission_after_route_refuel'], 'passed')
        self.assertEqual(result['checks']['recorded_route_refuel_source_boundary'], 'passed')
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['completedJobs'], ['intro_courier_earth_hera'])
        self.assertEqual(result['state']['routeQueue'], [])
        self.assertEqual(result['state']['credits'], 11800)
        self.assertTrue(any(event.get('type') == 'blocked_jump' and event.get('reason') == 'insufficient fuel' for event in result['trace']))
        self.assertTrue(any(event.get('type') == 'refuel' and event.get('body') == 'Earth' for event in result['trace']))
        route_events = [event for event in result['trace'] if event.get('type') == 'route_to_active_mission_destination']
        self.assertTrue(route_events)
        self.assertEqual(route_events[-1]['sourceLabel'], 'terminal-velocity-design-scaffold')
        self.assertEqual(route_events[-1]['oracleStatus'], 'mission_objective_hint_pending_ev_classic_ui_trace')

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

    def test_mission_abort_forbidden_return_gate_preserves_active_job(self):
        result = run_scripted_scenario('mission_abort_forbidden_return_gate')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual([job['id'] for job in result['state']['activeJobs']], ['canabort_return_gate_probe'])
        self.assertEqual(result['state']['cargoUsed'], 3)
        self.assertEqual(result['state'].get('abortedJobs', []), [])
        self.assertEqual(result['checks']['accepted_non_abortable_mission'], 'passed')
        self.assertEqual(result['checks']['blocked_abort_for_return_gated_mission'], 'passed')
        self.assertEqual(result['checks']['preserved_active_job_and_reserved_cargo'], 'passed')
        self.assertEqual(result['checks']['recorded_canabort_source_boundary'], 'passed')
        blocked_abort = [event for event in result['trace'] if event.get('type') == 'blocked_abort_mission'][-1]
        self.assertEqual(blocked_abort['missionId'], 'canabort_return_gate_probe')
        self.assertEqual(blocked_abort['reason'], 'mission cannot abort before return/cleanup')
        self.assertEqual(blocked_abort['sourceLabel'], 'ev-classic-resource-bible-backed-canabort-guardrail')
        self.assertEqual(blocked_abort['oracleStatus'], 'classic_runtime_canabort_ui_pending')

    def test_mission_abort_forbidden_return_completion_loop_completes_after_blocked_abort(self):
        result = run_scripted_scenario('mission_abort_forbidden_return_completion_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['completedJobs'], ['canabort_return_gate_probe'])
        self.assertEqual(result['state'].get('abortedJobs', []), [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['credits'], 11800)
        self.assertEqual(result['checks']['blocked_abort_before_return'], 'passed')
        self.assertEqual(result['checks']['completed_non_abortable_return_job'], 'passed')
        self.assertEqual(result['checks']['released_return_gate_cargo_and_reward'], 'passed')
        self.assertEqual(result['checks']['recorded_canabort_return_cleanup_boundary'], 'passed')
        blocked_abort = [event for event in result['trace'] if event.get('type') == 'blocked_abort_mission'][-1]
        self.assertEqual(blocked_abort['reason'], 'mission cannot abort before return/cleanup')
        completion = [event for event in result['trace'] if event.get('type') == 'complete_cargo_job'][-1]
        self.assertEqual(completion['id'], 'canabort_return_gate_probe')
        self.assertEqual(completion['reservedCargoTons'], 3)
        self.assertEqual(completion['sourceLabel'], 'ev-classic-resource-bible-backed-canabort-guardrail')
        self.assertEqual(completion['oracleStatus'], 'classic_runtime_canabort_return_cleanup_pending')

    def test_mission_abort_reputation_penalty_guardrail_applies_resource_bible_reversal(self):
        result = run_scripted_scenario('mission_abort_reputation_penalty_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['aborted_penalty_mission'], 'passed')
        self.assertEqual(result['checks']['released_abort_penalty_cargo'], 'passed')
        self.assertEqual(result['checks']['applied_abort_reputation_reversal'], 'passed')
        self.assertEqual(result['checks']['recorded_abort_penalty_source_boundary'], 'passed')
        self.assertEqual(result['state']['abortedJobs'], ['abort_penalty_probe'])
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['reputation']['Federation'], -25)
        abort = [event for event in result['trace'] if event.get('type') == 'abort_mission'][-1]
        self.assertEqual(abort['missionId'], 'abort_penalty_probe')
        self.assertEqual(abort['completionReward'], 6)
        self.assertEqual(abort['abortReputationMultiplier'], 5)
        self.assertEqual(abort['reputationDelta'], -30)
        self.assertEqual(abort['sourceLabel'], 'ev-classic-resource-bible-backed-mission-abort-penalty-scaffold')
        self.assertEqual(abort['oracleStatus'], 'classic_runtime_abort_penalty_ui_pending')

    def test_mission_auto_abort_completion_flags_guardrail_applies_resource_bible_contract(self):
        result = run_scripted_scenario('mission_auto_abort_completion_flags_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['accepted_auto_abort_mission'], 'passed')
        self.assertEqual(result['checks']['auto_aborted_after_acceptance'], 'passed')
        self.assertEqual(result['checks']['released_auto_abort_cargo'], 'passed')
        self.assertEqual(result['checks']['applied_auto_abort_completion_flags'], 'passed')
        self.assertEqual(result['checks']['recorded_auto_abort_source_boundary'], 'passed')
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['abortedJobs'], ['auto_abort_completion_bit_probe'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertIn('auto_abort_completion_bit_77', result['state']['storyFlags'])
        events = [event for event in result['trace'] if event.get('type') in {'accept_cargo_job', 'mission_auto_abort'}]
        self.assertEqual([event['type'] for event in events], ['accept_cargo_job', 'mission_auto_abort'])
        auto_abort = events[-1]
        self.assertEqual(auto_abort['missionId'], 'auto_abort_completion_bit_probe')
        self.assertEqual(auto_abort['releasedCargoTons'], 2)
        self.assertEqual(auto_abort['completionFlagsApplied'], ['auto_abort_completion_bit_77'])
        self.assertEqual(auto_abort['sourceLabel'], 'ev-classic-resource-bible-backed-auto-abort-guardrail')
        self.assertEqual(auto_abort['oracleStatus'], 'classic_runtime_auto_abort_ui_pending')

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

    def test_mission_deadline_last_day_delivery_loop_completes_without_failure(self):
        result = run_scripted_scenario('mission_deadline_last_day_delivery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['advanced_to_last_allowed_day'], 'passed')
        self.assertEqual(result['checks']['delivered_before_failure_on_limit_day'], 'passed')
        self.assertEqual(result['checks']['no_deadline_failure_or_penalty_on_limit_day'], 'passed')
        self.assertEqual(result['checks']['recorded_last_day_delivery_source_boundary'], 'passed')
        self.assertEqual(result['state']['completedJobs'], ['deadline_dispatch_failure_probe'])
        self.assertEqual(result['state'].get('failedJobs', []), [])
        self.assertNotIn('fail_mission_bit_42', result['state']['storyFlags'])
        completion = [event for event in result['trace'] if event.get('type') == 'complete_cargo_job'][-1]
        self.assertEqual(completion['acceptedDay'], 0)
        self.assertEqual(completion['timeLimitDays'], 2)
        self.assertEqual(completion['sourceLabel'], 'terminal-velocity-mission-deadline-last-day-scaffold')
        self.assertEqual(completion['oracleStatus'], 'deadline_last_day_delivery_pending_classic_runtime_or_manual_trace')

    def test_mission_deadline_completed_no_late_failure_loop_stays_completed_after_deadline(self):
        result = run_scripted_scenario('mission_deadline_completed_no_late_failure_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['completed_deadline_mission_before_late_advance'], 'passed')
        self.assertEqual(result['checks']['advanced_after_completion_without_late_failure'], 'passed')
        self.assertEqual(result['checks']['preserved_completion_rewards_and_reputation'], 'passed')
        self.assertEqual(result['checks']['recorded_completed_no_late_failure_source_boundary'], 'passed')
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['currentDay'], 3)
        self.assertEqual(result['state']['completedJobs'], ['deadline_dispatch_failure_probe'])
        self.assertEqual(result['state'].get('failedJobs', []), [])
        self.assertNotIn('fail_mission_bit_42', result['state']['storyFlags'])
        self.assertFalse(any(event.get('type') == 'mission_deadline_failure' for event in result['trace']))
        completion = [event for event in result['trace'] if event.get('type') == 'complete_cargo_job'][-1]
        self.assertEqual(completion['sourceLabel'], 'terminal-velocity-mission-deadline-completed-no-late-failure-scaffold')
        self.assertEqual(completion['oracleStatus'], 'deadline_completed_no_late_failure_pending_classic_runtime_or_manual_trace')

    def test_mission_deadline_abort_prevents_failure_loop_releases_cargo_without_penalty(self):
        result = run_scripted_scenario('mission_deadline_abort_prevents_failure_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['currentDay'], 3)
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['completedJobs'], [])
        self.assertEqual(result['state'].get('failedJobs', []), [])
        self.assertEqual(result['state']['abortedJobs'], ['deadline_dispatch_failure_probe'])
        self.assertNotIn('fail_mission_bit_42', result['state']['storyFlags'])
        self.assertEqual(result['state']['reputation']['Federation'], 5)
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['checks']['aborted_deadline_mission_before_expiry'], 'passed')
        self.assertEqual(result['checks']['advanced_beyond_deadline_without_failure'], 'passed')
        self.assertEqual(result['checks']['released_abort_cargo_without_penalty'], 'passed')
        self.assertEqual(result['checks']['recorded_deadline_abort_source_boundary'], 'passed')
        abort = [event for event in result['trace'] if event.get('type') == 'abort_mission'][-1]
        self.assertEqual(abort['missionId'], 'deadline_dispatch_failure_probe')
        self.assertEqual(abort['releasedCargoTons'], 3)
        self.assertEqual(abort['sourceLabel'], 'terminal-velocity-mission-abort-scaffold')
        self.assertEqual(abort['oracleStatus'], 'mission_abort_pending_classic_runtime_or_manual_trace')
        self.assertFalse(any(event.get('type') == 'mission_deadline_failure' for event in result['trace']))

    def test_mission_deadline_failure_recovery_loop_fails_then_completes_followup(self):
        result = run_scripted_scenario('mission_deadline_failure_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['completedJobs'], ['deadline_recovery_followup'])
        self.assertEqual(result['state']['failedJobs'], ['deadline_dispatch_failure_probe'])
        self.assertIn('fail_mission_bit_42', result['state']['storyFlags'])
        self.assertEqual(result['state']['reputation']['Federation'], 2)
        self.assertEqual(result['state']['credits'], 10900)
        self.assertEqual(result['checks']['failed_first_deadline_mission'], 'passed')
        self.assertEqual(result['checks']['accepted_followup_after_failure'], 'passed')
        self.assertEqual(result['checks']['delivered_followup_after_failure'], 'passed')
        self.assertEqual(result['checks']['preserved_failure_history_and_source_boundaries'], 'passed')
        mission_events = [event for event in result['trace'] if event.get('type') in {'mission_deadline_failure', 'accept_cargo_job', 'complete_cargo_job'}]
        self.assertTrue(any(event.get('sourceLabel') == 'ev-classic-resource-bible-backed-mission-failure-scaffold' for event in mission_events))
        self.assertTrue(any(event.get('sourceLabel') == 'terminal-velocity-mission-deadline-recovery-scaffold' for event in mission_events))

    def test_mission_deadline_trade_carryover_loop_sells_trade_after_failure(self):
        result = run_scripted_scenario('mission_deadline_trade_carryover_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['completedJobs'], [])
        self.assertEqual(result['state']['failedJobs'], ['deadline_dispatch_failure_probe'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['credits'], 10780)
        self.assertEqual(result['state']['reputation']['Federation'], 2)
        self.assertEqual(result['checks']['failed_deadline_mission_preserved_trade_cargo'], 'passed')
        self.assertEqual(result['checks']['sold_trade_cargo_after_mission_failure'], 'passed')
        self.assertEqual(result['checks']['recorded_trade_carryover_failure_history'], 'passed')
        self.assertEqual(result['checks']['recorded_trade_carryover_source_boundaries'], 'passed')
        buy = [event for event in result['trace'] if event.get('type') == 'buy_commodity_lot'][-1]
        failure = [event for event in result['trace'] if event.get('type') == 'mission_deadline_failure'][-1]
        sell = [event for event in result['trace'] if event.get('type') == 'sell_commodity_lot'][-1]
        self.assertEqual(buy['cargoUsed'], 13)
        self.assertEqual(failure['releasedCargoTons'], 3)
        self.assertEqual(sell['unitPrice'], 120)
        self.assertEqual(sell['sourceLabel'], 'terminal-velocity-mission-deadline-trade-carryover-scaffold')

    def test_mission_deadline_sequential_failures_loop_expires_multiple_active_jobs(self):
        result = run_scripted_scenario('mission_deadline_sequential_failures_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['currentDay'], 3)
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['completedJobs'], [])
        self.assertEqual(result['state']['failedJobs'], ['deadline_dispatch_failure_probe', 'deadline_second_failure_probe'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['reputation']['Federation'], 0)
        self.assertIn('fail_mission_bit_42', result['state']['storyFlags'])
        self.assertIn('fail_mission_bit_43', result['state']['storyFlags'])
        self.assertEqual(result['checks']['accepted_two_deadline_missions'], 'passed')
        self.assertEqual(result['checks']['expired_both_deadline_missions'], 'passed')
        self.assertEqual(result['checks']['released_all_reserved_deadline_cargo'], 'passed')
        self.assertEqual(result['checks']['recorded_sequential_failure_flags_and_penalties'], 'passed')
        self.assertEqual(result['checks']['recorded_sequential_failure_source_boundary'], 'passed')
        failures = [event for event in result['trace'] if event.get('type') == 'mission_deadline_failure']
        self.assertEqual([event['releasedCargoTons'] for event in failures], [3, 2])
        self.assertEqual([event['failureFlag'] for event in failures], ['fail_mission_bit_42', 'fail_mission_bit_43'])
        self.assertEqual([event['reputationDelta'] for event in failures], [-3, -2])
        self.assertTrue(all(event['sourceLabel'] == 'ev-classic-resource-bible-backed-mission-failure-scaffold' for event in failures))

    def test_mission_scan_failure_guardrail_fails_only_on_matching_government_scan(self):
        result = run_scripted_scenario('mission_scan_failure_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['activeJobs'], [])
        self.assertEqual(result['state']['failedJobs'], ['scan_sensitive_dispatch_probe'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertIn('fail_mission_bit_44', result['state']['storyFlags'])
        self.assertEqual(result['checks']['preserved_job_after_nonmatching_scan'], 'passed')
        self.assertEqual(result['checks']['failed_job_after_matching_scan'], 'passed')
        self.assertEqual(result['checks']['released_scan_sensitive_cargo'], 'passed')
        self.assertEqual(result['checks']['recorded_scan_failure_flag_and_boundary'], 'passed')
        scans = [event for event in result['trace'] if event['type'] in {'mission_scan_clear', 'mission_scan_failure'}]
        self.assertEqual([event['type'] for event in scans], ['mission_scan_clear', 'mission_scan_failure'])
        self.assertEqual(scans[0]['government'], 'Independent')
        self.assertEqual(scans[1]['government'], 'Federation')
        self.assertEqual(scans[1]['releasedCargoTons'], 4)
        self.assertTrue(all(event['sourceLabel'] == 'ev-classic-resource-bible-backed-mission-scan-failure-scaffold' for event in scans))

    def test_mission_scan_failure_recovery_loop_accepts_followup_after_scan_failure(self):
        result = run_scripted_scenario('mission_scan_failure_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['failed_scan_sensitive_mission'], 'passed')
        self.assertEqual(result['checks']['accepted_followup_after_scan_failure'], 'passed')
        self.assertEqual(result['checks']['delivered_followup_after_scan_failure'], 'passed')
        self.assertEqual(result['checks']['preserved_scan_failure_history_and_source_boundaries'], 'passed')
        self.assertEqual(result['state']['currentSystem'], 'Centauri')
        self.assertEqual(result['state']['landedBody'], 'Luna')
        self.assertEqual(result['state']['failedJobs'], ['scan_sensitive_dispatch_probe'])
        self.assertEqual(result['state']['completedJobs'], ['scan_recovery_followup'])
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['credits'], 10900)
        self.assertIn('fail_mission_bit_44', result['state']['storyFlags'])
        recovery_events = [event for event in result['trace'] if event.get('id') == 'scan_recovery_followup']
        self.assertEqual([event['type'] for event in recovery_events], ['accept_cargo_job', 'complete_cargo_job'])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-mission-scan-recovery-scaffold' for event in recovery_events))
        self.assertTrue(all(event['oracleStatus'] == 'scan_failure_recovery_pending_classic_runtime_or_manual_trace' for event in recovery_events))

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

    def test_outfitter_purchase_guardrail_recovery_loop_blocks_then_buys(self):
        result = run_scripted_scenario('outfitter_purchase_guardrail_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['ownedOutfits']['cargo_pod'], 1)
        self.assertEqual(result['state']['playerShipId'], 'light_freighter')
        self.assertEqual(result['checks']['blocked_outfit_not_landed'], 'passed')
        self.assertEqual(result['checks']['blocked_outfit_no_service'], 'passed')
        self.assertEqual(result['checks']['blocked_outfit_insufficient_credits'], 'passed')
        self.assertEqual(result['checks']['blocked_ship_insufficient_credits'], 'passed')
        self.assertEqual(result['checks']['recovered_by_buying_outfit_and_ship'], 'passed')
        self.assertEqual(result['checks']['recorded_outfitter_guardrail_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] in {'blocked_buy_outfit_or_weapon', 'blocked_buy_ship'}]
        self.assertEqual([event['reason'] for event in blocked], ['not landed', 'outfit not for sale here', 'insufficient credits', 'insufficient credits'])
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-outfitter-purchase-guardrail-scaffold' for event in blocked))

    def test_shipyard_overfull_cargo_guardrail_blocks_downsize_until_cargo_fits(self):
        result = run_scripted_scenario('shipyard_overfull_cargo_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['checks']['blocked_overfull_ship_transfer'], 'passed')
        self.assertEqual(result['checks']['preserved_overfull_cargo_before_recovery'], 'passed')
        self.assertEqual(result['checks']['recovered_after_freeing_cargo'], 'passed')
        self.assertEqual(result['checks']['recorded_shipyard_cargo_guardrail_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_ship'][-1]
        self.assertEqual(blocked['reason'], 'cargo exceeds target ship capacity')
        self.assertEqual(blocked['cargoUsed'], 30)
        self.assertEqual(blocked['targetCargoCapacity'], 20)
        self.assertEqual(result['state']['playerShipId'], 'shuttlecraft')
        self.assertEqual(result['state']['cargoUsed'], 10)
        self.assertEqual(result['state']['cargoHold']['food'], 10)

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

    def test_repair_insufficient_credit_guardrail_preserves_damage_then_recovers(self):
        result = run_scripted_scenario('repair_insufficient_credit_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['currentHull'], result['state']['maxHull'])
        self.assertEqual(result['state']['credits'], 0)
        self.assertEqual(result['checks']['blocked_repair_without_enough_credits'], 'passed')
        self.assertEqual(result['checks']['preserved_damage_after_credit_block'], 'passed')
        self.assertEqual(result['checks']['recovered_after_earning_repair_cost'], 'passed')
        self.assertEqual(result['checks']['recorded_repair_credit_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_repair_hull'][-1]
        self.assertEqual(blocked['reason'], 'insufficient credits')
        self.assertEqual(blocked['cost'], 200)
        self.assertEqual(blocked['credits'], 199)
        repair = [event for event in result['trace'] if event['type'] == 'repair_hull'][-1]
        self.assertEqual(repair['hullBefore'], 75)
        self.assertEqual(repair['hullAfter'], 100)
        self.assertEqual(repair['creditsAfter'], 0)
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

    def test_static_topology_source_readiness_scout_records_lane_a_promotion_boundary(self):
        result = run_scripted_scenario('static_topology_source_readiness_scout')

        self.assertTrue(result['success'], result)
        for check in [
            'found_67_syst_like_primitive_records',
            'kept_runtime_universe_subset_unchanged',
            'recorded_name_seed_inputs',
            'recorded_system_name_seed_summary',
            'recorded_coordinate_raw_long_candidate',
            'recorded_coordinate_domain_summary',
            'recorded_coordinate_display_candidate_summary',
            'recorded_coordinate_display_bounds_summary',
            'recorded_coordinate_display_normalized_summary',
            'recorded_coordinate_display_transform_summary',
            'recorded_coordinate_display_fixed_point_summary',
            'recorded_coordinate_display_integer_band_summary',
            'recorded_coordinate_display_residual_sign_summary',
            'recorded_coordinate_display_residual_magnitude_summary',
            'recorded_coordinate_display_extrema_summary',
            'recorded_candidate_link_family',
            'recorded_candidate_link_graph_summary',
            'recorded_candidate_graph_connectivity_summary',
            'recorded_candidate_graph_distance_summary',
            'recorded_start_system_candidate_topology_summary',
            'recorded_start_neighborhood_display_transform_summary',
            'recorded_start_neighborhood_display_distance_summary',
            'recorded_start_neighborhood_display_vector_summary',
            'recorded_start_neighborhood_slot_vector_order_summary',
            'recorded_start_neighborhood_slot_angular_order_summary',
            'recorded_exact_start_system_mapping',
            'recorded_static_topology_source_boundary',
        ]:
            self.assertEqual(result['checks'][check], 'passed')
        readiness = [event for event in result['trace'] if event['type'] == 'static_topology_source_readiness'][-1]
        self.assertEqual(readiness['systLikeRecords'], 67)
        self.assertEqual(readiness['recordSize'], 88)
        self.assertEqual(readiness['runtimeSystemSubsetCount'], 10)
        self.assertEqual(readiness['systemNameSeedSummarySourceLabel'], 'decoded-resource-backed-system-name-seed-join-scout')
        self.assertEqual(readiness['systemNameSeedSummaryOracleStatus'], 'exact_record_name_runtime_topology_mapping_pending')
        self.assertEqual(readiness['systemNameSeedSummarySeedCount'], 9)
        self.assertEqual(readiness['systemNameSeedSummarySeedNames'][:3], ['Sol', 'Centauri', 'Sirius'])
        self.assertEqual(readiness['systemNameSeedSummaryExactMappedNames'], ['Levo'])
        self.assertEqual(readiness['systemNameSeedSummaryUnjoinedSeedCount'], 9)
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['systemNameSeedSummarySourceLabel'], 'decoded-resource-backed-system-name-seed-join-scout')
        self.assertEqual(readiness['candidateCoordinateWordIndices'], [0, 1, 2, 3])
        self.assertEqual(readiness['candidateCoordinateXRawLongResource128'], 65664)
        self.assertEqual(readiness['candidateCoordinateYRawLongResource128'], 8327168)
        self.assertEqual(readiness['candidateCoordinateSourceConfidence'], 'resource-bible-field-family-plus-decoded-raw-word-pair-domain-summary-plus-raw-signed-long-candidate')
        self.assertEqual(readiness['coordinateDomainSourceLabel'], 'decoded-resource-backed-coordinate-domain-scout')
        self.assertEqual(readiness['coordinateDisplayUnitOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertEqual(readiness['coordinateDisplayCandidateSourceLabel'], 'decoded-resource-backed-coordinate-display-candidate')
        self.assertIn('raw high word as coarse grid/band candidate', readiness['coordinateDisplayCandidateFamilies'])
        self.assertEqual(readiness['coordinateDisplayCandidateResource128']['xPos']['rawHighWordAsGridBandCandidate'], 1)
        self.assertEqual(readiness['coordinateDisplayCandidateResource128']['yPos']['rawLowWordAsSubgridOffsetCandidate'], 4096)
        self.assertEqual(readiness['coordinateDisplayBoundsSourceLabel'], 'decoded-resource-backed-coordinate-display-bounds-scout')
        self.assertIn('raw high-word candidate bounds/span', readiness['coordinateDisplayBoundsCandidateFamilies'])
        self.assertEqual(readiness['coordinateDisplayBoundsXSpanHighLowLong'], [3, 153, 262015])
        self.assertEqual(readiness['coordinateDisplayBoundsYSpanHighLowLong'], [133, 61440, 8720383])
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayBoundsSourceLabel'], 'decoded-resource-backed-coordinate-display-bounds-scout')
        self.assertEqual(readiness['coordinateDisplayNormalizedSourceLabel'], 'decoded-resource-backed-coordinate-display-normalized-scout')
        self.assertIn('signed-long min-normalized x/y candidates', readiness['coordinateDisplayNormalizedCandidateFamilies'])
        self.assertEqual(readiness['coordinateDisplayNormalizedXRange'], [0, 262015])
        self.assertEqual(readiness['coordinateDisplayNormalizedYRange'], [0, 8720383])
        self.assertEqual(readiness['coordinateDisplayNormalizedResource128']['xPos']['minNormalizedSignedLongCandidate'], 0)
        self.assertEqual(readiness['coordinateDisplayNormalizedResource128']['yPos']['minNormalizedSignedLongCandidate'], 8327167)
        self.assertEqual(readiness['coordinateDisplayNormalizedResource128']['yPos']['unitIntervalCandidate'], 0.954908)
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayNormalizedSourceLabel'], 'decoded-resource-backed-coordinate-display-normalized-scout')
        self.assertEqual(readiness['coordinateDisplayTransformSourceLabel'], 'decoded-resource-backed-coordinate-display-transform-scout')
        self.assertIn('signed-long y-axis inversion candidate', readiness['coordinateDisplayTransformCandidateFamilies'])
        self.assertEqual(readiness['coordinateDisplayTransformAxisSpanRatioYOverX'], 33.281999)
        self.assertEqual(readiness['coordinateDisplayTransformResource128']['yPos']['invertedUnitIntervalCandidate'], 0.045092)
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayTransformSourceLabel'], 'decoded-resource-backed-coordinate-display-transform-scout')
        self.assertEqual(readiness['coordinateDisplayFixedPointSourceLabel'], 'decoded-resource-backed-coordinate-display-fixed-point-scale-scout')
        self.assertEqual(readiness['coordinateDisplayFixedPointOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertIn('16.16 fixed-point coordinate-unit candidate', readiness['coordinateDisplayFixedPointCandidateFamilies'])
        self.assertEqual(readiness['coordinateDisplayFixedPointDivisor'], 65536)
        self.assertEqual(readiness['coordinateDisplayFixedPointXSpan'], 3.998032)
        self.assertEqual(readiness['coordinateDisplayFixedPointYSpan'], 133.062485)
        self.assertEqual(readiness['coordinateDisplayFixedPointAxisSpanRatioYOverX'], 33.281996)
        self.assertEqual(readiness['coordinateDisplayFixedPointResource128']['yPosFixedPointCandidate'], 127.0625)
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayFixedPointSourceLabel'], 'decoded-resource-backed-coordinate-display-fixed-point-scale-scout')
        self.assertEqual(readiness['coordinateDisplayIntegerBandSourceLabel'], 'decoded-resource-backed-coordinate-display-integer-band-scout')
        self.assertEqual(readiness['coordinateDisplayIntegerBandOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertIn('16.16 high-word integer-band candidate', readiness['coordinateDisplayIntegerBandCandidateFamilies'])
        self.assertEqual(readiness['coordinateDisplayIntegerBandXDistribution'], {'1': 12, '2': 7, '3': 32, '4': 16})
        self.assertEqual(readiness['coordinateDisplayIntegerBandYDistribution'], {'0': 42, '18': 1, '72': 4, '127': 19, '133': 1})
        self.assertEqual(readiness['coordinateDisplayIntegerBandResource128']['yPos']['integerBandCandidate'], 127)
        self.assertEqual(readiness['coordinateDisplayIntegerBandResource129']['yPos']['signedFractionalResidualCandidate'], -32768)
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayIntegerBandSourceLabel'], 'decoded-resource-backed-coordinate-display-integer-band-scout')
        self.assertEqual(readiness['coordinateDisplayResidualSignSourceLabel'], 'decoded-resource-backed-coordinate-display-residual-sign-scout')
        self.assertEqual(readiness['coordinateDisplayResidualSignOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertIn('16.16 low-word residual sign distribution candidate', readiness['coordinateDisplayResidualSignCandidateFamilies'])
        self.assertEqual(readiness['coordinateDisplayResidualSignXDistribution'], {'negative': 4, 'zero': 0, 'positive': 63})
        self.assertEqual(readiness['coordinateDisplayResidualSignYDistribution'], {'negative': 54, 'zero': 0, 'positive': 13})
        self.assertEqual(readiness['coordinateDisplayResidualSignYDistinctFractionalUnits'], [-0.5, 1.5e-05, 0.0625, 0.125, 0.4375])
        self.assertEqual(readiness['coordinateDisplayResidualSignResource128']['yPosFractionalUnitCandidate'], 0.0625)
        self.assertEqual(readiness['coordinateDisplayResidualSignResource129']['yPosFractionalUnitCandidate'], -0.5)
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayResidualSignSourceLabel'], 'decoded-resource-backed-coordinate-display-residual-sign-scout')
        self.assertEqual(readiness['coordinateDisplayResidualMagnitudeSourceLabel'], 'decoded-resource-backed-coordinate-display-residual-magnitude-scout')
        self.assertEqual(readiness['coordinateDisplayResidualMagnitudeOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertIn('16.16 low-word absolute residual magnitude candidate', readiness['coordinateDisplayResidualMagnitudeCandidateFamilies'])
        self.assertEqual(readiness['coordinateDisplayResidualMagnitudeXRange'], [1, 152])
        self.assertEqual(readiness['coordinateDisplayResidualMagnitudeXDistribution']['128'], 14)
        self.assertEqual(readiness['coordinateDisplayResidualMagnitudeYRange'], [1, 32768])
        self.assertEqual(readiness['coordinateDisplayResidualMagnitudeYDistinctAbsoluteFractionalUnits'], [1.5e-05, 0.0625, 0.125, 0.4375, 0.5])
        self.assertEqual(readiness['coordinateDisplayResidualMagnitudeYMaxResourceIds'][:3], [129, 130, 132])
        self.assertEqual(readiness['coordinateDisplayResidualMagnitudeResource128']['yPosAbsoluteFractionalUnitCandidate'], 0.0625)
        self.assertEqual(readiness['coordinateDisplayResidualMagnitudeResource129']['yPosAbsoluteFractionalUnitCandidate'], 0.5)
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayResidualMagnitudeSourceLabel'], 'decoded-resource-backed-coordinate-display-residual-magnitude-scout')
        self.assertEqual(readiness['coordinateDisplayExtremaSourceLabel'], 'decoded-resource-backed-coordinate-display-extrema-scout')
        self.assertEqual(readiness['coordinateDisplayExtremaXLowWordMinMaxResourceIds'], [[133, 144, 155, 156], [192]])
        self.assertEqual(readiness['coordinateDisplayExtremaYSignedLongMinMaxResourceIds'], [[168, 169, 170, 172, 183, 186], [182]])
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayExtremaSourceLabel'], 'decoded-resource-backed-coordinate-display-extrema-scout')
        self.assertEqual(readiness['coordinateXHighWordDistinctValues'], [1, 2, 3, 4])
        self.assertEqual(readiness['coordinateYHighWordDistinctValues'], [0, 18, 72, 127, 133])
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDomainSourceLabel'], 'decoded-resource-backed-coordinate-domain-scout')
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayUnitOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['coordinateDisplayCandidateSourceLabel'], 'decoded-resource-backed-coordinate-display-candidate')
        self.assertEqual(readiness['candidateLinkWordIndices'], list(range(4, 20)))
        self.assertEqual(readiness['candidateLinkedSystemIdsForResource128'][:4], [128, 129, 130, 131])
        self.assertEqual(readiness['candidateLinkGraphSourceLabel'], 'decoded-resource-backed-candidate-link-graph-scout')
        self.assertEqual(readiness['candidateLinkGraphOracleStatus'], 'exact_record_name_runtime_topology_mapping_pending')
        self.assertEqual(readiness['candidateLinkGraphDirectedSlotCount'], 268)
        self.assertEqual(readiness['candidateLinkGraphUniqueDirectedLinkCount'], 117)
        self.assertEqual(readiness['candidateLinkGraphReciprocalDirectedLinkCount'], 8)
        self.assertEqual(readiness['candidateLinkGraphNonReciprocalDirectedLinkCount'], 109)
        self.assertEqual(readiness['candidateLinkGraphUniqueSelfLinkCount'], 4)
        self.assertEqual(readiness['candidateLinkGraphUniqueSelfLinkResourceIds'], [128, 136, 139, 140])
        self.assertTrue(readiness['candidateLinkGraphTargetsInRun'])
        self.assertEqual(readiness['candidateGraphConnectivitySourceLabel'], 'decoded-resource-backed-candidate-graph-connectivity-scout')
        self.assertEqual(readiness['candidateGraphWeaklyConnectedComponentCount'], 1)
        self.assertEqual(readiness['candidateGraphResource128WeakComponentSize'], 67)
        self.assertEqual(readiness['candidateGraphResource128DirectedReachableCount'], 21)
        self.assertEqual(readiness['candidateGraphResource128DirectedUnreachableCount'], 46)
        self.assertEqual(readiness['candidateGraphUniqueOutDegreeDistribution'], {'1': 39, '2': 14, '3': 6, '4': 8})
        self.assertEqual(readiness['candidateGraphDistanceSourceLabel'], 'decoded-resource-backed-candidate-graph-distance-scout')
        self.assertEqual(readiness['candidateGraphResource128DirectedMaxHopDistance'], 4)
        self.assertEqual(readiness['candidateGraphResource128WeakMaxHopDistance'], 4)
        self.assertEqual(readiness['candidateGraphResource128WeakHopDistanceDistribution'], {'0': 1, '1': 3, '2': 19, '3': 31, '4': 13})
        self.assertEqual(readiness['candidateGraphWeakDiameterCandidate'], 7)
        self.assertEqual(readiness['candidateGraphDirectedReachableCountRange'], [2, 22])
        self.assertEqual(readiness['startSystemCandidateTopologySourceLabel'], 'decoded-resource-backed-start-system-candidate-topology-scout')
        self.assertEqual(readiness['startSystemCandidateTopologyOracleStatus'], 'exact_record_name_runtime_topology_mapping_pending')
        self.assertEqual(readiness['startSystemCandidateTopologyStartName'], 'Levo')
        self.assertEqual(readiness['startSystemCandidateTopologyLinkedNeighborCount'], 4)
        self.assertEqual(readiness['startSystemCandidateTopologyNeighborResourceIds'], [128, 129, 130, 131])
        self.assertEqual(readiness['startSystemCandidateTopologyUnjoinedNeighborResourceIds'], [129, 130, 131])
        self.assertEqual(readiness['startSystemCandidateTopologySelfLinkSlotNames'], ['Con1'])
        self.assertEqual(readiness['startSystemCandidateTopologyReciprocalNeighborResourceIds'], [128])
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['startSystemCandidateTopologySourceLabel'], 'decoded-resource-backed-start-system-candidate-topology-scout')
        self.assertEqual(readiness['startNeighborhoodDisplayTransformSourceLabel'], 'decoded-resource-backed-start-neighborhood-display-transform-scout')
        self.assertEqual(readiness['startNeighborhoodDisplayTransformOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertIn('start-neighborhood inverted-y display-transform candidates', readiness['startNeighborhoodDisplayTransformCandidateFamilies'])
        self.assertEqual(readiness['startNeighborhoodDisplayTransformStartUnitInterval'], {'xPos': 0, 'yPos': 0.954908, 'invertedYPos': 0.045092})
        self.assertEqual(readiness['startNeighborhoodDisplayTransformNeighborResourceIds'], [128, 129, 130, 131])
        self.assertEqual(readiness['startNeighborhoodDisplayTransformNeighbor129Delta'], {'xPos': 131072, 'yPos': -8294400})
        self.assertEqual(readiness['startNeighborhoodDisplayTransformNeighbor129UnitInterval'], {'xPos': 0.500246, 'yPos': 0.003758, 'invertedYPos': 0.996242})
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['startNeighborhoodDisplayTransformSourceLabel'], 'decoded-resource-backed-start-neighborhood-display-transform-scout')
        self.assertEqual(readiness['startNeighborhoodDisplayDistanceSourceLabel'], 'decoded-resource-backed-start-neighborhood-display-distance-scout')
        self.assertEqual(readiness['startNeighborhoodDisplayDistanceOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertIn('start-neighborhood inverted-y unit-interval manhattan-distance candidates', readiness['startNeighborhoodDisplayDistanceCandidateFamilies'])
        self.assertEqual(readiness['startNeighborhoodDisplayDistanceNeighborResourceIds'], [128, 129, 130, 131])
        self.assertEqual(readiness['startNeighborhoodDisplayDistanceNeighbor129ManhattanSignedLong'], 8425472)
        self.assertEqual(readiness['startNeighborhoodDisplayDistanceNeighbor131ManhattanInvertedYUnit'], 0.250593)
        self.assertEqual(readiness['startNeighborhoodDisplayDistanceNonSelfSignedLongRange'], [69632, 8425473])
        self.assertEqual(readiness['startNeighborhoodDisplayDistanceNonSelfInvertedYUnitRange'], [0.250593, 1.4514])
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['startNeighborhoodDisplayDistanceSourceLabel'], 'decoded-resource-backed-start-neighborhood-display-distance-scout')
        self.assertEqual(readiness['startNeighborhoodDisplayVectorSourceLabel'], 'decoded-resource-backed-start-neighborhood-display-vector-scout')
        self.assertEqual(readiness['startNeighborhoodDisplayVectorOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertIn('start-neighborhood display quadrant candidates', readiness['startNeighborhoodDisplayVectorCandidateFamilies'])
        self.assertEqual(readiness['startNeighborhoodDisplayVectorNeighborResourceIds'], [128, 129, 130, 131])
        self.assertEqual(readiness['startNeighborhoodDisplayVectorNeighbor129Quadrant'], 'north-east')
        self.assertEqual(readiness['startNeighborhoodDisplayVectorNeighbor129DominantAxis'], 'y')
        self.assertEqual(readiness['startNeighborhoodDisplayVectorNeighbor131Angle'], -0.107663)
        self.assertEqual(readiness['startNeighborhoodDisplayVectorNonSelfQuadrants'], ['north-east', 'south-east'])
        self.assertEqual(readiness['startNeighborhoodDisplayVectorNonSelfDominantAxisDistribution'], {'x': 1, 'y': 2})
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['startNeighborhoodDisplayVectorSourceLabel'], 'decoded-resource-backed-start-neighborhood-display-vector-scout')
        self.assertEqual(readiness['startNeighborhoodSlotVectorOrderSourceLabel'], 'decoded-resource-backed-start-neighborhood-slot-vector-order-scout')
        self.assertEqual(readiness['startNeighborhoodSlotVectorOrderOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertIn('start-neighborhood Con-slot order candidates', readiness['startNeighborhoodSlotVectorOrderCandidateFamilies'])
        self.assertEqual(readiness['startNeighborhoodSlotVectorOrderNeighborResourceIds'], [128, 129, 130, 131])
        self.assertEqual(readiness['startNeighborhoodSlotVectorOrderFirstNonSelfSlotName'], 'Con2')
        self.assertEqual(readiness['startNeighborhoodSlotVectorOrderFirstNonSelfResourceId'], 129)
        self.assertEqual(readiness['startNeighborhoodSlotVectorOrderNonSelfResourceIdsByDistance'], [131, 129, 130])
        self.assertEqual(readiness['startNeighborhoodSlotVectorOrderCon4DistanceRank'], 1)
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['startNeighborhoodSlotVectorOrderSourceLabel'], 'decoded-resource-backed-start-neighborhood-slot-vector-order-scout')
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['startNeighborhoodSlotVectorOrderFirstNonSelfResourceId'], 129)
        self.assertEqual(readiness['startNeighborhoodSlotAngularOrderSourceLabel'], 'decoded-resource-backed-start-neighborhood-slot-angular-order-scout')
        self.assertEqual(readiness['startNeighborhoodSlotAngularOrderOracleStatus'], 'coordinate_display_units_map_scaling_pending')
        self.assertIn('start-neighborhood angular-rank candidates', readiness['startNeighborhoodSlotAngularOrderCandidateFamilies'])
        self.assertEqual(readiness['startNeighborhoodSlotAngularOrderNeighborResourceIds'], [128, 129, 130, 131])
        self.assertEqual(readiness['startNeighborhoodSlotAngularOrderNonSelfResourceIdsByAngle'], [131, 130, 129])
        self.assertEqual(readiness['startNeighborhoodSlotAngularOrderNonSelfQuadrantsByAngle'], ['south-east', 'north-east', 'north-east'])
        self.assertEqual(readiness['startNeighborhoodSlotAngularOrderFirstAngleSlotName'], 'Con4')
        self.assertEqual(readiness['startNeighborhoodSlotAngularOrderFirstAngleResourceId'], 131)
        self.assertEqual(readiness['startNeighborhoodSlotAngularOrderCon4AngleRank'], 1)
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['startNeighborhoodSlotAngularOrderSourceLabel'], 'decoded-resource-backed-start-neighborhood-slot-angular-order-scout')
        self.assertEqual(result['state']['sourceReadiness']['staticTopology']['startNeighborhoodSlotAngularOrderFirstAngleResourceId'], 131)
        self.assertEqual(readiness['exactSystemNameResource128'], 'Levo')
        self.assertIn('original-runtime-observed', readiness['exactSystemNameSourceBasis'])
        self.assertEqual(readiness['sourceLabel'], 'decoded-resource-backed-static-readiness')
        self.assertEqual(readiness['oracleStatus'], 'topology_semantic_promotion_pending_field_family_mapping')
        self.assertTrue(result['state']['sourceReadiness']['staticTopology']['promotionSafeNext'])

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

    def test_manual_route_low_fuel_recovery_landing_loop_keeps_route_and_recovers(self):
        result = run_scripted_scenario('manual_route_low_fuel_recovery_landing_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['fuel'], 4)
        self.assertEqual(result['state']['routeQueue'], [])
        self.assertEqual(result['metrics']['jumps'], 2)
        self.assertEqual(result['checks']['drew_manual_green_route_with_fuel_hint'], 'passed')
        self.assertEqual(result['checks']['blocked_without_consuming_route_or_fuel'], 'passed')
        self.assertEqual(result['checks']['recovered_by_refueling_and_reselecting_route'], 'passed')
        self.assertEqual(result['checks']['landed_after_recovery'], 'passed')
        route_status = [event for event in result['trace'] if event['type'] == 'route_fuel_status']
        self.assertEqual(route_status[-1]['routeQueue'], ['Sol', 'Sirius'])
        self.assertEqual(route_status[-1]['fuelStatus'], 'insufficient fuel for full route')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_jump']
        self.assertEqual(blocked[-1]['reason'], 'insufficient fuel')
        self.assertEqual(blocked[-1]['routeQueue'], ['Sol', 'Sirius'])

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

    def test_legal_docking_service_gate_recovery_blocks_then_recovers_with_clemency(self):
        result = run_scripted_scenario('legal_docking_service_gate_recovery')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['blocked_fugitive_docking'], 'passed')
        self.assertEqual(result['checks']['blocked_legal_service_access'], 'passed')
        self.assertEqual(result['checks']['clemency_restored_dock_and_outfitter_access'], 'passed')
        self.assertEqual(result['checks']['recorded_legal_gate_source_boundary'], 'passed')
        self.assertEqual(result['state']['currentSystem'], 'Sol')
        self.assertEqual(result['state']['landedBody'], 'Earth')
        self.assertEqual(result['state']['legalRecords']['Federation'], -45)
        self.assertEqual(result['state']['ownedOutfits']['cargo_pod'], 1)
        blocked_landing = [event for event in result['trace'] if event['type'] == 'blocked_land'][-1]
        self.assertEqual(blocked_landing['reason'], 'legal docking denied')
        self.assertEqual(blocked_landing['sourceLabel'], 'terminal-velocity-legal-docking-scaffold')
        service_block = [event for event in result['trace'] if event['type'] == 'blocked_buy_outfit_or_weapon'][-1]
        self.assertEqual(service_block['reason'], 'legal/reputation service restricted')
        self.assertEqual(service_block['sourceLabel'], 'terminal-velocity-legal-service-gate-scaffold')

    def test_weapon_reputation_gate_recovery_blocks_then_buys_at_threshold(self):
        result = run_scripted_scenario('weapon_reputation_gate_recovery')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['reputation']['Independent'], 6)
        self.assertEqual(result['state']['ownedWeapons']['pulse_cannon'], 1)
        self.assertEqual(result['checks']['blocked_weapon_service_below_reputation'], 'passed')
        self.assertEqual(result['checks']['recovered_weapon_purchase_at_reputation_threshold'], 'passed')
        self.assertEqual(result['checks']['recorded_weapon_gate_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_outfit_or_weapon'][-1]
        self.assertEqual(blocked['service'], 'weapons')
        self.assertEqual(blocked['government'], 'Independent')
        self.assertEqual(blocked['sourceLabel'], 'terminal-velocity-legal-service-gate-scaffold')
        bought = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon'][-1]
        self.assertEqual(bought['saleType'], 'weapon')
        self.assertEqual(bought['sourceLabel'], 'terminal-velocity-weapon-reputation-gate-scaffold')

    def test_weapon_credit_recovery_loop_blocks_then_buys_at_exact_price(self):
        result = run_scripted_scenario('weapon_credit_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['ownedWeapons']['pulse_cannon'], 1)
        self.assertEqual(result['state']['credits'], 0)
        self.assertEqual(result['checks']['blocked_weapon_purchase_one_credit_short'], 'passed')
        self.assertEqual(result['checks']['recovered_weapon_purchase_at_exact_price'], 'passed')
        self.assertEqual(result['checks']['recorded_weapon_credit_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_outfit_or_weapon'][-1]
        self.assertEqual(blocked['reason'], 'insufficient credits')
        self.assertEqual(blocked['price'], 1400)
        self.assertEqual(blocked['credits'], 1399)
        bought = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon'][-1]
        self.assertEqual(bought['saleType'], 'weapon')
        self.assertEqual(bought['itemId'], 'pulse_cannon')
        self.assertEqual(bought['sourceLabel'], 'terminal-velocity-weapon-credit-gate-scaffold')
        self.assertEqual(bought['oracleStatus'], 'classic_runtime_weapon_purchase_credit_ui_pending')

    def test_weapon_availability_recovery_loop_routes_to_local_weapon_service(self):
        result = run_scripted_scenario('weapon_availability_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['ownedWeapons']['pulse_cannon'], 1)
        self.assertEqual(result['checks']['blocked_weapon_not_for_sale_at_earth'], 'passed')
        self.assertEqual(result['checks']['recovered_at_sirius_weapon_service'], 'passed')
        self.assertEqual(result['checks']['recorded_weapon_availability_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_buy_outfit_or_weapon'][-1]
        self.assertEqual(blocked['reason'], 'weapon not for sale here')
        self.assertEqual(blocked['system'], 'Sol')
        self.assertEqual(blocked['body'], 'Earth')
        self.assertEqual(blocked['sourceLabel'], 'terminal-velocity-weapon-availability-scaffold')
        bought = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon'][-1]
        self.assertEqual(bought['saleType'], 'weapon')
        self.assertEqual(bought['itemId'], 'pulse_cannon')
        self.assertEqual(bought['sourceLabel'], 'terminal-velocity-weapon-availability-scaffold')
        self.assertEqual(bought['oracleStatus'], 'classic_runtime_weapon_store_inventory_pending')

    def test_weapon_purchase_mission_cargo_reservation_loop_preserves_active_job_space(self):
        result = run_scripted_scenario('weapon_purchase_mission_cargo_reservation_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['ownedWeapons']['pulse_cannon'], 1)
        self.assertEqual(result['state']['cargoUsed'], 3)
        self.assertEqual(result['state']['credits'], 8600)
        self.assertEqual(result['checks']['accepted_mission_before_weapon_purchase'], 'passed')
        self.assertEqual(result['checks']['weapon_purchase_preserved_reserved_cargo'], 'passed')
        self.assertEqual(result['checks']['recorded_weapon_purchase_mission_cargo_source_boundary'], 'passed')
        accept = [event for event in result['trace'] if event['type'] == 'accept_cargo_job'][-1]
        bought = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon'][-1]
        self.assertEqual(accept['cargoUsed'], 3)
        self.assertEqual(bought['saleType'], 'weapon')
        self.assertEqual(bought['itemId'], 'pulse_cannon')
        self.assertEqual(bought['cargoUsed'], 3)
        self.assertEqual(bought['sourceLabel'], 'terminal-velocity-weapon-mission-cargo-scaffold')
        self.assertEqual(bought['oracleStatus'], 'classic_runtime_weapon_purchase_cargo_interaction_pending')

    def test_weapon_purchase_trade_cargo_reservation_loop_preserves_held_lot(self):
        result = run_scripted_scenario('weapon_purchase_trade_cargo_reservation_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['ownedWeapons']['pulse_cannon'], 1)
        self.assertEqual(result['state']['cargoUsed'], 10)
        self.assertEqual(result['state']['cargoHold'], {'food': 10})
        self.assertEqual(result['state']['credits'], 7860)
        self.assertEqual(result['checks']['bought_trade_lot_before_weapon_purchase'], 'passed')
        self.assertEqual(result['checks']['weapon_purchase_preserved_trade_cargo'], 'passed')
        self.assertEqual(result['checks']['recorded_weapon_purchase_trade_cargo_source_boundary'], 'passed')
        trade = [event for event in result['trace'] if event['type'] == 'buy_commodity_lot'][-1]
        bought = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon'][-1]
        self.assertEqual(trade['commodity'], 'food')
        self.assertEqual(trade['cargoUsed'], 10)
        self.assertEqual(bought['saleType'], 'weapon')
        self.assertEqual(bought['itemId'], 'pulse_cannon')
        self.assertEqual(bought['cargoUsed'], 10)
        self.assertEqual(bought['cargoHold'], {'food': 10})
        self.assertEqual(bought['activeMissionCargo'], 0)
        self.assertEqual(bought['sourceLabel'], 'terminal-velocity-weapon-trade-cargo-scaffold')
        self.assertEqual(bought['oracleStatus'], 'classic_runtime_weapon_purchase_cargo_interaction_pending')

    def test_weapon_purchase_secondary_activation_loop_buys_and_surfaces_secondary_steps(self):
        result = run_scripted_scenario('weapon_purchase_secondary_activation_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['ownedWeapons']['pulse_cannon'], 1)
        self.assertEqual(result['state']['credits'], 8600)
        self.assertEqual(result['checks']['bought_secondary_weapon_for_activation'], 'passed')
        self.assertEqual(result['checks']['recorded_secondary_activation_steps'], 'passed')
        self.assertEqual(result['checks']['recorded_weapon_secondary_source_boundary'], 'passed')
        bought = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon'][-1]
        self.assertEqual(bought['saleType'], 'weapon')
        self.assertEqual(bought['itemId'], 'pulse_cannon')
        self.assertEqual(bought['sourceLabel'], 'terminal-velocity-weapon-secondary-activation-scaffold')
        self.assertEqual(bought['oracleStatus'], 'classic_runtime_secondary_weapon_activation_pending')
        checkpoints = [event['skill'] for event in result['trace'] if event['type'] == 'strategy_skill_checkpoint']
        self.assertEqual(checkpoints, ['secondary_weapon_unloaded', 'secondary_weapon_loaded'])

    def test_weapon_legal_docking_recovery_loop_repairs_legal_record_then_buys_weapon(self):
        result = run_scripted_scenario('weapon_legal_docking_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['legalRecords']['Federation'], -45)
        self.assertEqual(result['state']['ownedWeapons']['pulse_cannon'], 1)
        self.assertEqual(result['state']['credits'], 0)
        self.assertEqual(result['checks']['blocked_weapon_service_docking_on_bad_legal'], 'passed')
        self.assertEqual(result['checks']['clemency_restored_weapon_port_docking'], 'passed')
        self.assertEqual(result['checks']['bought_weapon_after_legal_docking_recovery'], 'passed')
        self.assertEqual(result['checks']['recorded_weapon_legal_docking_source_boundary'], 'passed')
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_land'][-1]
        self.assertEqual(blocked['government'], 'Federation')
        self.assertEqual(blocked['body'], 'Earth')
        self.assertEqual(blocked['sourceLabel'], 'terminal-velocity-legal-docking-scaffold')
        bought = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon'][-1]
        self.assertEqual(bought['saleType'], 'weapon')
        self.assertEqual(bought['itemId'], 'pulse_cannon')
        self.assertEqual(bought['sourceLabel'], 'terminal-velocity-weapon-legal-docking-scaffold')
        self.assertEqual(bought['oracleStatus'], 'classic_runtime_weapon_purchase_after_docking_denial_pending')

    def test_weapon_inventory_stack_recovery_loop_records_multiple_purchases(self):
        result = run_scripted_scenario('weapon_inventory_stack_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['currentSystem'], 'Sirius')
        self.assertEqual(result['state']['landedBody'], 'Sirius Station')
        self.assertEqual(result['state']['ownedWeapons']['pulse_cannon'], 2)
        self.assertEqual(result['state']['credits'], 7200)
        self.assertEqual(result['checks']['bought_first_secondary_weapon'], 'passed')
        self.assertEqual(result['checks']['bought_second_secondary_weapon_stack'], 'passed')
        self.assertEqual(result['checks']['recorded_weapon_inventory_stack_source_boundary'], 'passed')
        buys = [event for event in result['trace'] if event['type'] == 'buy_outfit_or_weapon' and event['itemId'] == 'pulse_cannon']
        self.assertEqual(len(buys), 2)
        self.assertEqual([event['creditsAfter'] for event in buys], [8600, 7200])
        self.assertTrue(all(event['saleType'] == 'weapon' for event in buys))
        self.assertTrue(all(event['sourceLabel'] == 'terminal-velocity-weapon-inventory-stack-scaffold' for event in buys))
        self.assertTrue(all(event['oracleStatus'] == 'classic_runtime_multiple_weapon_purchase_inventory_pending' for event in buys))

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

    def test_contraband_scan_trade_recovery_loop_preserves_legal_trade_cargo(self):
        result = run_scripted_scenario('contraband_scan_trade_recovery_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['credits'], 5400)
        self.assertEqual(result['state']['legalRecords']['Federation'], -8)
        self.assertEqual(result['checks']['confiscated_only_contraband_cargo'], 'passed')
        self.assertEqual(result['checks']['preserved_legal_food_trade_lot'], 'passed')
        self.assertEqual(result['checks']['recovered_scan_penalty_with_clemency_and_trade_sale'], 'passed')
        self.assertEqual(result['checks']['recorded_contraband_trade_source_boundary'], 'passed')
        scan = [event for event in result['trace'] if event['type'] == 'contraband_scan'][-1]
        self.assertEqual(scan['cargoHoldAfter'], {'food': 10})
        sale = [event for event in result['trace'] if event['type'] == 'sell_commodity_lot'][-1]
        self.assertEqual(sale['sourceLabel'], 'terminal-velocity-contraband-trade-recovery-scaffold')
        self.assertEqual(sale['oracleStatus'], 'classic_runtime_scan_trade_cargo_cleanup_pending')

    def test_contraband_trade_funds_clemency_loop_sells_preserved_cargo_before_clemency(self):
        result = run_scripted_scenario('contraband_trade_funds_clemency_loop')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['scan_left_clemency_one_hundred_credits_short'], 'passed')
        self.assertEqual(result['checks']['preserved_trade_lot_funded_clemency'], 'passed')
        self.assertEqual(result['checks']['recorded_contraband_clemency_funding_boundaries'], 'passed')
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['cargoHold'], {})
        self.assertEqual(result['state']['cargoUsed'], 0)
        self.assertEqual(result['state']['credits'], 1100)
        self.assertEqual(result['state']['legalRecords']['Federation'], -8)
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_legal_clemency']
        sale = [event for event in result['trace'] if event['type'] == 'sell_commodity_lot'][-1]
        self.assertEqual(blocked[-1]['credits'], 900)
        self.assertEqual(sale['creditsAfter'], 2100)
        self.assertEqual(sale['sourceLabel'], 'terminal-velocity-contraband-clemency-funding-scaffold')
        self.assertEqual(sale['oracleStatus'], 'classic_runtime_scan_trade_clemency_cleanup_pending')

    def test_legal_clemency_insufficient_credit_guardrail_blocks_then_recovers(self):
        result = run_scripted_scenario('legal_clemency_insufficient_credit_guardrail')

        self.assertTrue(result['success'], result)
        self.assertEqual(result['checks']['blocked_clemency_one_credit_short'], 'passed')
        self.assertEqual(result['checks']['recovered_clemency_at_exact_cost'], 'passed')
        self.assertEqual(result['checks']['recorded_clemency_source_boundary'], 'passed')
        self.assertEqual(result['state']['credits'], 0)
        self.assertEqual(result['state']['legalRecords']['Federation'], -5)
        blocked = [event for event in result['trace'] if event['type'] == 'blocked_legal_clemency'][-1]
        self.assertEqual(blocked['reason'], 'insufficient credits')
        self.assertEqual(blocked['cost'], 1000)
        self.assertEqual(blocked['credits'], 999)
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

    def test_pirate_avoidance_mission_trade_escape_loop_preserves_loaded_cargo(self):
        result = run_scripted_scenario('pirate_avoidance_mission_trade_escape_loop')

        self.assertTrue(result['success'], result)
        self.assertFalse(result['state']['combatExecuted'])
        self.assertEqual(result['state']['currentSystem'], 'Levo')
        self.assertEqual(result['state']['landedBody'], 'Levo Spaceport')
        self.assertEqual(result['state']['cargoHold'].get('food'), 10)
        self.assertEqual(result['state']['cargoUsed'], 15)
        self.assertEqual(result['checks']['escaped_loaded_route_without_combat'], 'passed')
        self.assertEqual(result['checks']['preserved_mission_and_trade_cargo_after_evasion'], 'passed')
        self.assertEqual(result['checks']['recorded_pirate_loaded_cargo_source_boundary'], 'passed')
        avoidance = [event for event in result['trace'] if event['type'] == 'avoid_pirate_contact'][-1]
        self.assertEqual(avoidance['missionCargoBeforeEscape'], 5)
        self.assertEqual(avoidance['tradeCargoBeforeEscape'], 10)
        self.assertEqual(avoidance['cargoUsedAfterEscape'], 15)
        self.assertEqual(avoidance['sourceLabel'], 'terminal-velocity-pirate-avoidance-loaded-cargo-scaffold')
        self.assertEqual(avoidance['oracleStatus'], 'pirate_avoidance_loaded_cargo_pending_ev_classic_combat_trace')

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
