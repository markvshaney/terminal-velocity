import unittest

from native_ev.model import (
    available_mission_ids,
    branch_choice_groups,
    cargo_can_accept,
    cargo_job_pay,
    can_buy,
    economy_manifest,
    fine_for_contraband,
    facing_index,
    government_manifest,
    load_universe,
    mission_manifest,
    mission_unlock_flags,
    normalize_save_data,
    outfit_manifest,
    route_risk_score,
    serialize_save_data,
    repair_cost,
    ship_manifest,
    sourced_ev_graphics_manifest,
    sourced_ev_names_manifest,
    sourced_ev_structures_manifest,
    shuttle_frame_paths,
    system_distance,
    trade_profit,
    weapon_manifest,
)


class NativeEvModelTests(unittest.TestCase):
    def test_all_36_shuttle_frames_exist(self):
        paths = shuttle_frame_paths()
        self.assertEqual(len(paths), 36)
        self.assertTrue(all(path.exists() for path in paths))

    def test_facing_index_wraps_to_36_original_facings(self):
        self.assertEqual(facing_index(0), 0)
        self.assertEqual(facing_index(9), 1)
        self.assertEqual(facing_index(359), 0)
        self.assertEqual(facing_index(-10), 35)

    def test_cargo_capacity(self):
        self.assertTrue(cargo_can_accept(12, 8))
        self.assertFalse(cargo_can_accept(12, 9))

    def test_universe_is_file_backed_and_playable(self):
        data = load_universe()
        self.assertGreaterEqual(len(data['systems']), 1)
        self.assertTrue(all(system['bodies'] for system in data['systems']))
        self.assertTrue(all('x' in system and 'y' in system for system in data['systems']))
        self.assertTrue(all(system['links'] for system in data['systems']))

    def test_universe_has_ev_style_route_density(self):
        universe = load_universe()
        economy = economy_manifest()
        governments = government_manifest()
        ships = ship_manifest()
        system_names = {system['name'] for system in universe['systems']}
        self.assertGreaterEqual(len(system_names), 8)
        self.assertTrue(system_names.issubset(set(economy['markets'])))
        self.assertTrue(system_names.issubset(set(governments['systems'])))
        self.assertGreaterEqual(sum(len(system['links']) for system in universe['systems']), 18)
        traffic_systems = {traffic['system'] for traffic in ships['traffic']}
        self.assertGreaterEqual(len(traffic_systems & system_names), 6)
        self.assertGreaterEqual(len(ships['traffic']), 12)

    def test_sourced_ev_names_manifest_has_local_resource_provenance(self):
        data = sourced_ev_names_manifest()
        self.assertEqual(data['sourceFile'], 'source-assets/ev-classic/Nova Files/EV Data.rez')
        self.assertEqual(data['method'], 'brgr-text-chunk-heuristic-v1')
        names = {entry['name'] for entry in data['landingNames']}
        self.assertTrue({'Earth', 'Stardock Alpha', 'Mars', 'Landfall'}.issubset(names))
        for entry in data['landingNames'][:12]:
            self.assertIn('chunkIndex', entry)
            self.assertGreater(entry['byteOffset'], 0)
            self.assertTrue(entry['evidence'])
            self.assertIn(entry['confidence'], {'high', 'medium'})

    def test_sourced_ev_structures_manifest_decodes_fixed_record_runs(self):
        data = sourced_ev_structures_manifest()
        self.assertEqual(data['sourceFile'], 'source-assets/ev-classic/Nova Files/EV Data.rez')
        self.assertEqual(data['method'], 'brgr-full-field-decode-v2')
        self.assertEqual(data['chunkCount'], 1544)
        by_type = {run['candidateType']: run for run in data['runs']}
        self.assertEqual(by_type['syst-like']['recordSize'], 88)
        self.assertEqual(by_type['syst-like']['count'], 67)
        self.assertEqual(by_type['spob-like']['recordSize'], 400)
        self.assertGreaterEqual(by_type['spob-like']['count'], 200)
        self.assertEqual(by_type['ship-like']['recordSize'], 1860)
        first_system = by_type['syst-like']['records'][0]
        first_spob = by_type['spob-like']['records'][0]
        self.assertTrue(first_system['fieldsComplete'])
        self.assertTrue(first_spob['fieldsComplete'])
        self.assertGreaterEqual(len(first_system['fields']), 44)
        self.assertGreaterEqual(len(first_spob['fields']), 200)
        self.assertEqual(first_system['fields'][0]['byteOffsetInRecord'], 0)
        self.assertEqual(first_spob['fields'][0]['byteOffsetInRecord'], 0)
        self.assertGreater(first_system['byteOffset'], 0)
        self.assertGreater(first_spob['byteOffset'], first_system['byteOffset'])

    def test_sourced_ev_graphics_manifest_decodes_resources_and_ship_sprites(self):
        data = sourced_ev_graphics_manifest()
        self.assertEqual(data['sourceFile'], 'source-assets/ev-classic/Nova Files/EV Graphics.rez')
        self.assertEqual(data['method'], 'brgr-graphics-rled-shan-full-field-v1')
        self.assertEqual(data['resourceCount'], 303)
        resources_by_type = {}
        for resource in data['resources']:
            resources_by_type.setdefault(resource['type'], 0)
            resources_by_type[resource['type']] += 1
        self.assertGreaterEqual(resources_by_type['rlëD'], 70)
        self.assertGreaterEqual(resources_by_type['shän'], 25)
        shuttle = next(sprite for sprite in data['shipSprites'] if sprite.get('shipName') == 'Shuttle')
        self.assertEqual(shuttle['rledResourceId'], 1000)
        self.assertEqual(shuttle['frames'], 36)
        self.assertEqual(shuttle['width'], 48)
        self.assertEqual(shuttle['height'], 48)
        ok_sprites = [sprite for sprite in data['shipSprites'] if sprite.get('status') == 'ok']
        self.assertGreaterEqual(len(ok_sprites), 20)
        decoded_rled = [asset for asset in data['rledAssets'] if asset.get('status') == 'ok']
        self.assertGreaterEqual(len(decoded_rled), 70)
        weaponry = next(asset for asset in decoded_rled if asset.get('resourceId') == 200)
        self.assertGreaterEqual(weaponry['frames'], 1)
        self.assertTrue(weaponry['assetDir'].startswith('assets/graphics/rled/'))

    def test_universe_uses_a_seed_set_of_sourced_ev_names(self):
        universe = load_universe()
        names = {system['name'] for system in universe['systems']}
        body_names = {body['name'] for system in universe['systems'] for body in system['bodies']}
        self.assertTrue({'Sol', 'Centauri', 'Sirius', 'Tau Ceti'}.issubset(names))
        self.assertTrue({'Earth', 'Stardock Alpha', 'Mars', 'Landfall'}.issubset(body_names))

    def test_ship_manifest_loads_player_and_npc_assets(self):
        data = ship_manifest()
        ids = {ship['id'] for ship in data['ships']}
        self.assertIn('shuttle', ids)
        self.assertIn('light_freighter', ids)
        self.assertGreaterEqual(len(data['traffic']), 1)

    def test_all_extracted_ev_classic_ship_graphics_are_in_game_manifest(self):
        graphics = sourced_ev_graphics_manifest()
        ships = ship_manifest()
        manifest_asset_dirs = {ship['assetDir'] for ship in ships['ships']}
        ok_sprites = [sprite for sprite in graphics['shipSprites'] if sprite.get('status') == 'ok']
        self.assertGreaterEqual(len(ok_sprites), 26)
        missing = [sprite['shipName'] for sprite in ok_sprites if sprite['assetDir'] not in manifest_asset_dirs]
        self.assertEqual(missing, [])
        traffic_ids = {traffic['shipId'] for traffic in ships['traffic']}
        manifest_ids = {ship['id'] for ship in ships['ships']}
        self.assertTrue(traffic_ids.issubset(manifest_ids))
        self.assertGreaterEqual(len(traffic_ids), 20)
        shipyard_ids = {entry['shipId'] for entry in outfit_manifest()['shipyard']}
        self.assertTrue(manifest_ids.issubset(shipyard_ids))

    def test_weapon_manifest_loads_combat_data(self):
        data = weapon_manifest()
        ids = {weapon['id'] for weapon in data['weapons']}
        self.assertIn('laser_cannon', ids)
        self.assertIn('pulse_cannon', ids)

    def test_mission_manifest_loads_story_chain(self):
        data = mission_manifest()
        ids = {mission['id'] for mission in data['missions']}
        self.assertIn('intro_courier_earth_hera', ids)
        self.assertTrue(all(mission['reward'] > 0 for mission in data['missions']))
        intro = next(mission for mission in data['missions'] if mission['id'] == 'intro_courier_earth_hera')
        followup = next(mission for mission in data['missions'] if mission['id'] == 'frontier_sample_hera_freeport')
        self.assertIn('story_intro_started', intro['setsFlags'])
        self.assertIn('story_intro_complete', intro['completionFlags'])
        self.assertIn('story_intro_complete', followup['requiresFlags'])

    def test_mission_flags_gate_followup_missions(self):
        data = mission_manifest()
        self.assertEqual(
            available_mission_ids(data, 'Sol', 'Earth', completed_ids=set(), active_ids=set(), flags=set()),
            ['intro_courier_earth_hera'],
        )
        self.assertEqual(
            available_mission_ids(data, 'Centauri', 'Luna', completed_ids=set(), active_ids=set(), flags=set()),
            [],
        )
        flags = mission_unlock_flags(data, 'intro_courier_earth_hera', set())
        self.assertIn('story_intro_complete', flags)
        self.assertEqual(
            available_mission_ids(data, 'Centauri', 'Luna', completed_ids={'intro_courier_earth_hera'}, active_ids=set(), flags=flags),
            ['frontier_sample_hera_freeport'],
        )

    def test_mission_effects_apply_reputation_and_legal_status(self):
        data = mission_manifest()
        flags = mission_unlock_flags(data, 'frontier_sample_hera_freeport', {'story_intro_complete'})
        self.assertIn('reputation_independent_positive', flags)

    def test_branching_missions_offer_mutually_exclusive_choices(self):
        data = mission_manifest()
        groups = branch_choice_groups(data)
        self.assertIn('chapter_one_alignment', groups)
        self.assertEqual(
            set(groups['chapter_one_alignment']),
            {'federation_report_freeport', 'freeport_pact_smugglers'},
        )
        choice_flags = {'story_intro_complete', 'frontier_samples_delivered'}
        self.assertEqual(
            set(available_mission_ids(data, 'Sirius', 'Sirius Station', completed_ids={'frontier_sample_hera_freeport'}, active_ids=set(), flags=choice_flags)),
            {'freeport_return_earth', 'federation_report_freeport', 'freeport_pact_smugglers'},
        )
        fed_flags = mission_unlock_flags(data, 'federation_report_freeport', choice_flags)
        self.assertIn('alignment_federation', fed_flags)
        self.assertNotIn(
            'freeport_pact_smugglers',
            available_mission_ids(data, 'Sirius', 'Sirius Station', completed_ids={'frontier_sample_hera_freeport', 'federation_report_freeport'}, active_ids=set(), flags=fed_flags),
        )
        freeport_flags = mission_unlock_flags(data, 'freeport_pact_smugglers', choice_flags)
        self.assertIn('alignment_freeport', freeport_flags)
        self.assertNotIn(
            'federation_report_freeport',
            available_mission_ids(data, 'Sirius', 'Sirius Station', completed_ids={'frontier_sample_hera_freeport', 'freeport_pact_smugglers'}, active_ids=set(), flags=freeport_flags),
        )

    def test_outfit_manifest_loads_upgrade_and_shipyard_data(self):
        data = outfit_manifest()
        outfit_ids = {outfit['id'] for outfit in data['outfits']}
        ship_ids = {ship['shipId'] for ship in data['shipyard']}
        self.assertIn('cargo_pod', outfit_ids)
        self.assertIn('hull_plating', outfit_ids)
        self.assertIn('shuttle', ship_ids)
        self.assertIn('light_freighter', ship_ids)
        self.assertTrue(all(outfit['price'] > 0 for outfit in data['outfits']))

    def test_repair_and_purchase_rules(self):
        self.assertEqual(repair_cost(current_hull=75, max_hull=100, per_point=8), 200)
        self.assertTrue(can_buy(credits=5000, price=4500))
        self.assertFalse(can_buy(credits=1000, price=4500))

    def test_economy_manifest_loads_commodities_and_market_prices(self):
        data = economy_manifest()
        commodity_ids = {commodity['id'] for commodity in data['commodities']}
        self.assertIn('food', commodity_ids)
        self.assertIn('industrial_goods', commodity_ids)
        self.assertIn('Sol', data['markets'])
        self.assertIn('Sirius', data['markets'])
        self.assertGreater(data['markets']['Sirius']['industrial_goods']['sell'], data['markets']['Sol']['industrial_goods']['buy'])

    def test_trade_profit_math(self):
        self.assertEqual(trade_profit(buy_price=80, sell_price=125, quantity=4), 180)

    def test_route_based_jobs_pay_for_distance_and_risk(self):
        universe = load_universe()
        governments = government_manifest()
        ships = ship_manifest()
        short_distance = system_distance(universe, 'Sol', 'Centauri')
        long_distance = system_distance(universe, 'Sol', 'Alkaid')
        self.assertGreater(long_distance, short_distance)
        safe_risk = route_risk_score(governments, ships, 'Tau Ceti')
        hostile_risk = route_risk_score(governments, ships, 'Alkaid')
        self.assertGreater(hostile_risk, safe_risk)
        safe_pay = cargo_job_pay(tons=3, distance=short_distance, risk_score=safe_risk)
        risky_pay = cargo_job_pay(tons=3, distance=long_distance, risk_score=hostile_risk)
        self.assertGreater(risky_pay, safe_pay)

    def test_government_manifest_loads_law_and_contraband(self):
        data = government_manifest()
        self.assertIn('Sol', data['systems'])
        self.assertEqual(data['systems']['Sol']['government'], 'Federation')
        self.assertIn('luxuries', data['contraband']['Federation'])
        self.assertGreater(data['governments']['Federation']['finePerTon'], 0)

    def test_contraband_fine_math(self):
        self.assertEqual(fine_for_contraband({'luxuries': 2, 'food': 5}, {'luxuries'}, 400), 800)
        self.assertEqual(fine_for_contraband({'food': 5}, {'luxuries'}, 400), 0)
    def test_save_data_round_trips_progression_and_ship_state(self):
        save = serialize_save_data(
            credits=7425,
            current_system='Centauri',
            selected_system='Sirius',
            player_ship_id='light_freighter',
            player_hull=135,
            player_fuel=82,
            cargo_used=7,
            cargo_space=45,
            owned_outfits={'cargo_pod': 2, 'fuel_tank': 1},
            commodity_hold={'industrial_goods': {'tons': 3, 'basis': 240}},
            active_mission_ids=['frontier_sample_hera_freeport'],
            completed_mission_ids=['intro_courier_earth_hera'],
            story_flags=['story_intro_complete', 'frontier_chain_started'],
            legal_status='Clean',
        )
        loaded = normalize_save_data(save)
        self.assertEqual(loaded['schemaVersion'], 1)
        self.assertEqual(loaded['credits'], 7425)
        self.assertEqual(loaded['currentSystem'], 'Centauri')
        self.assertEqual(loaded['playerShipId'], 'light_freighter')
        self.assertEqual(loaded['ownedOutfits']['cargo_pod'], 2)
        self.assertEqual(loaded['commodityHold']['industrial_goods']['tons'], 3)
        self.assertEqual(loaded['activeMissionIds'], ['frontier_sample_hera_freeport'])
        self.assertEqual(loaded['completedMissionIds'], ['intro_courier_earth_hera'])
        self.assertIn('story_intro_complete', loaded['storyFlags'])

    def test_save_data_defaults_missing_optional_fields(self):
        loaded = normalize_save_data({'credits': 6000, 'currentSystem': 'Sol'})
        self.assertEqual(loaded['schemaVersion'], 1)
        self.assertEqual(loaded['credits'], 6000)
        self.assertEqual(loaded['currentSystem'], 'Sol')
        self.assertEqual(loaded['selectedSystem'], 'Sol')
        self.assertEqual(loaded['playerShipId'], 'shuttle')
        self.assertEqual(loaded['activeMissionIds'], [])
        self.assertEqual(loaded['completedMissionIds'], [])
        self.assertEqual(loaded['storyFlags'], [])
        self.assertEqual(loaded['commodityHold'], {})


if __name__ == '__main__':
    unittest.main()
