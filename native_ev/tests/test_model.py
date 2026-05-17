from pathlib import Path
import struct
import unittest
import zlib

from native_ev.model import (
    available_mission_ids,
    available_station_services,
    branch_choice_groups,
    cargo_can_accept,
    cargo_job_pay,
    can_buy,
    can_dock_with_government,
    effective_npc_disposition,
    economy_manifest,
    fine_for_contraband,
    government_patrol_posture,
    enforcement_outcome,
    clemency_offer,
    patrol_spawn_specs,
    fugitive_docking_consequence,
    facing_index,
    government_manifest,
    load_universe,
    mission_manifest,
    mission_unlock_flags,
    normalize_save_data,
    apply_reputation_event,
    legal_status_for_score,
    outfit_manifest,
    reputation_manifest,
    route_risk_score,
    serialize_save_data,
    repair_cost,
    ship_manifest,
    sourced_ev_graphics_manifest,
    sourced_ev_names_manifest,
    sourced_ev_structures_manifest,
    ship_graphics_crosswalk,
    ev_classic_data_ship_manifest,
    shuttle_frame_paths,
    station_inventory,
    system_distance,
    trade_profit,
    weapon_manifest,
)



def _png_alpha_pixel_count(path: Path) -> int:
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    pos = 8
    raw = b''
    width = height = color_type = None
    while pos < len(data):
        size = struct.unpack('>I', data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + size]
        pos += 12 + size
        if kind == b'IHDR':
            width, height, _depth, color_type, _compression, _filter, _interlace = struct.unpack('>IIBBBBB', chunk)
        elif kind == b'IDAT':
            raw += chunk
        elif kind == b'IEND':
            break
    assert width is not None and height is not None
    bytes_per_pixel = 4 if color_type == 6 else 3
    decoded = zlib.decompress(raw)
    previous = [0] * (width * bytes_per_pixel)
    index = 0
    count = 0

    def paeth(left: int, above: int, upper_left: int) -> int:
        p = left + above - upper_left
        pa = abs(p - left)
        pb = abs(p - above)
        pc = abs(p - upper_left)
        if pa <= pb and pa <= pc:
            return left
        if pb <= pc:
            return above
        return upper_left

    for _y in range(height):
        filter_type = decoded[index]
        index += 1
        row = list(decoded[index:index + width * bytes_per_pixel])
        index += width * bytes_per_pixel
        for i in range(len(row)):
            left = row[i - bytes_per_pixel] if i >= bytes_per_pixel else 0
            above = previous[i]
            upper_left = previous[i - bytes_per_pixel] if i >= bytes_per_pixel else 0
            if filter_type == 1:
                row[i] = (row[i] + left) & 0xFF
            elif filter_type == 2:
                row[i] = (row[i] + above) & 0xFF
            elif filter_type == 3:
                row[i] = (row[i] + ((left + above) // 2)) & 0xFF
            elif filter_type == 4:
                row[i] = (row[i] + paeth(left, above, upper_left)) & 0xFF
        if color_type == 6:
            count += sum(1 for x in range(width) if row[x * bytes_per_pixel + 3] > 0)
        else:
            count += width
        previous = row
    return count


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
        self.assertEqual(data['method'], 'evnew-opcode-rled-shan-full-field-v2')
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

    def test_ship_graphics_crosswalk_preserves_data_ship_identity_before_sprite_mapping(self):
        crosswalk = ship_graphics_crosswalk()
        kestrels = [entry for entry in crosswalk if entry['dataShipName'] == 'Kestrel']
        self.assertGreaterEqual(len(kestrels), 2)
        kestrel = next(entry for entry in kestrels if entry['dataOrdinal'] == 15)
        self.assertEqual(kestrel['candidateShanRefs'][0]['wordIndex'], 9)
        self.assertEqual(kestrel['candidateShanRefs'][0]['shanResourceId'], 131)
        self.assertEqual(kestrel['candidateShanRefs'][0]['shanName'], 'Courier')
        self.assertNotEqual(kestrel['dataShipName'], kestrel['candidateShanRefs'][0]['shanName'])
        self.assertGreaterEqual(len(kestrel['candidateShanRefs']), 4)

    def test_ev_classic_ship_manifest_is_joined_from_data_identity_to_graphics_assets(self):
        generated = ev_classic_data_ship_manifest()
        by_ordinal = {ship['sourceDataOrdinal']: ship for ship in generated['ships']}
        self.assertEqual(by_ordinal[5]['name'], 'Confed Frigate')
        self.assertEqual(by_ordinal[5]['shipResourceId'], 133)
        self.assertEqual(by_ordinal[5]['assetDir'], 'assets/ships/ev_classic/frigate')
        self.assertEqual(by_ordinal[6]['name'], 'Confed Cruiser')
        self.assertEqual(by_ordinal[15]['name'], 'Kestrel')
        self.assertEqual(by_ordinal[15]['shipResourceId'], 143)
        self.assertEqual(by_ordinal[15]['resourceId'], 1030)
        self.assertEqual(by_ordinal[24]['shipResourceId'], 152)
        self.assertEqual(by_ordinal[24]['resourceId'], 1002)
        self.assertEqual(by_ordinal[15]['graphicsName'], 'Kestrel')
        self.assertNotIn(26, by_ordinal)
        self.assertEqual(ship_manifest()['ships'], generated['ships'])

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
            set(available_mission_ids(
                data,
                'Sirius',
                'Sirius Station',
                completed_ids={'frontier_sample_hera_freeport'},
                active_ids=set(),
                flags=choice_flags,
                reputation={'Federation': 4, 'Independent': 6, 'Pirate': 0},
                legal_records={'Federation': 0, 'Independent': 0},
            )),
            {'freeport_return_earth', 'federation_report_freeport', 'freeport_pact_smugglers'},
        )
        self.assertEqual(
            set(available_mission_ids(
                data,
                'Sirius',
                'Sirius Station',
                completed_ids={'frontier_sample_hera_freeport'},
                active_ids=set(),
                flags=choice_flags,
                reputation={'Federation': 4, 'Independent': 6, 'Pirate': 0},
                legal_records={'Federation': -65, 'Independent': 0},
            )),
            {'freeport_return_earth', 'freeport_pact_smugglers'},
        )
        self.assertEqual(
            set(available_mission_ids(
                data,
                'Sirius',
                'Sirius Station',
                completed_ids={'frontier_sample_hera_freeport'},
                active_ids=set(),
                flags=choice_flags,
                reputation={'Federation': 4, 'Independent': 0, 'Pirate': 0},
                legal_records={'Federation': 0, 'Independent': 0},
            )),
            {'freeport_return_earth', 'federation_report_freeport'},
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

    def test_station_inventories_are_selective_and_reference_valid_products(self):
        universe = load_universe()
        outfits = outfit_manifest()
        weapons = weapon_manifest()
        ship_ids = {listing['shipId'] for listing in outfits['shipyard']}
        outfit_ids = {outfit['id'] for outfit in outfits['outfits']}
        weapon_ids = {weapon['id'] for weapon in weapons['weapons']}
        earth = station_inventory(universe, 'Sol', 'Earth')
        luna = station_inventory(universe, 'Centauri', 'Luna')
        freeport = station_inventory(universe, 'Sirius', 'Sirius Station')
        self.assertIn('shipyard', earth['services'])
        self.assertIn('outfitter', earth['services'])
        self.assertIn('laser_cannon', earth['weaponsForSale'])
        self.assertIn('fuel_tank', luna['outfitsForSale'])
        self.assertNotIn('shipyard', luna['services'])
        self.assertIn('pulse_cannon', freeport['weaponsForSale'])
        self.assertNotEqual(set(earth['shipsForSale']), set(freeport['shipsForSale']))
        for system in universe['systems']:
            for body in system['bodies']:
                inventory = station_inventory(universe, system['name'], body['name'])
                self.assertTrue(set(inventory['outfitsForSale']).issubset(outfit_ids))
                self.assertTrue(set(inventory['shipsForSale']).issubset(ship_ids))
                self.assertTrue(set(inventory['weaponsForSale']).issubset(weapon_ids))

    def test_reputation_and_legal_status_gate_station_services(self):
        universe = load_universe()
        reputation_rules = reputation_manifest()
        earth = station_inventory(universe, 'Sol', 'Earth')
        clean_services = available_station_services(
            earth,
            reputation_rules,
            reputation={'Federation': 4, 'Independent': 0},
            legal_records={'Federation': 0},
            government='Federation',
        )
        fugitive_services = available_station_services(
            earth,
            reputation_rules,
            reputation={'Federation': 4, 'Independent': 0},
            legal_records={'Federation': -65},
            government='Federation',
        )
        self.assertIn('shipyard', clean_services)
        self.assertIn('outfitter', clean_services)
        self.assertNotIn('shipyard', fugitive_services)
        self.assertNotIn('outfitter', fugitive_services)
        self.assertIn('repairs', fugitive_services)

        freeport = station_inventory(universe, 'Sirius', 'Sirius Station')
        low_rep_services = available_station_services(
            freeport,
            reputation_rules,
            reputation={'Independent': 0},
            legal_records={'Independent': 0},
            government='Independent',
        )
        trusted_services = available_station_services(
            freeport,
            reputation_rules,
            reputation={'Independent': 6},
            legal_records={'Independent': 0},
            government='Independent',
        )
        self.assertNotIn('weapons', low_rep_services)
        self.assertIn('weapons', trusted_services)

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

    def test_police_outcome_bribes_low_level_contraband_when_config_allows(self):
        governments = government_manifest()
        reputation = reputation_manifest()
        outcome = enforcement_outcome(
            governments,
            reputation,
            government='Independent',
            hold={'medical_supplies': 1, 'food': 2},
            credits=2000,
            legal_records={'Independent': 0},
            accept_bribe=True,
        )
        self.assertEqual(outcome['action'], 'bribe')
        self.assertGreater(outcome['creditsDelta'], -1000)
        self.assertEqual(outcome['confiscated'], {'medical_supplies': 0})
        self.assertEqual(outcome['legalDelta'], 0)

    def test_police_outcome_fines_and_confiscates_contraband(self):
        governments = government_manifest()
        reputation = reputation_manifest()
        outcome = enforcement_outcome(
            governments,
            reputation,
            government='Federation',
            hold={'luxuries': 2, 'food': 3},
            credits=5000,
            legal_records={'Federation': 0},
            accept_bribe=False,
        )
        self.assertEqual(outcome['action'], 'fine')
        self.assertEqual(outcome['creditsDelta'], -800)
        self.assertEqual(outcome['confiscated'], {'luxuries': 2})
        self.assertEqual(outcome['legalDelta'], -10)

    def test_police_outcome_escalates_when_player_cannot_pay_fine(self):
        governments = government_manifest()
        reputation = reputation_manifest()
        outcome = enforcement_outcome(
            governments,
            reputation,
            government='Militia Compact',
            hold={'luxuries': 1, 'medical_supplies': 1},
            credits=100,
            legal_records={'Militia Compact': -40},
            accept_bribe=False,
        )
        self.assertEqual(outcome['action'], 'confiscate')
        self.assertEqual(outcome['confiscated'], {'luxuries': 1, 'medical_supplies': 1})
        self.assertLessEqual(outcome['legalDelta'], -25)
        self.assertEqual(government_patrol_posture(reputation, {'Militia Compact': -70}, 'Militia Compact'), 'hostile')

    def test_clemency_offer_reduces_legal_record_for_clean_faction_reputation(self):
        reputation = reputation_manifest()
        offer = clemency_offer(reputation, reputation_scores={'Federation': 15}, legal_records={'Federation': -45}, government='Federation')
        self.assertTrue(offer['available'])
        self.assertEqual(offer['legalDelta'], 25)
        self.assertEqual(offer['cost'], 1000)
        denied = clemency_offer(reputation, reputation_scores={'Federation': -5}, legal_records={'Federation': -45}, government='Federation')
        self.assertFalse(denied['available'])

    def test_government_patrol_specs_cover_every_mapped_system(self):
        universe = load_universe()
        governments = government_manifest()
        ships = ship_manifest()
        specs = patrol_spawn_specs(governments, ships, universe)
        systems = {system['name'] for system in universe['systems']}
        self.assertEqual({spec['system'] for spec in specs}, systems)
        self.assertTrue(all(spec['shipId'] in {ship['id'] for ship in ships['ships']} for spec in specs))
        self.assertTrue(all(spec['faction'] == governments['governments'][governments['systems'][spec['system']]['government']]['patrolFaction'] for spec in specs))
        self.assertGreaterEqual(min(spec['scanRange'] for spec in specs), 180)

    def test_fugitive_docking_consequence_names_patrol_attack(self):
        reputation = reputation_manifest()
        warning = fugitive_docking_consequence(reputation, {'Federation': -25}, 'Federation')
        self.assertEqual(warning['action'], 'deny')
        self.assertFalse(warning['patrolsHostile'])
        hostile = fugitive_docking_consequence(reputation, {'Federation': -70}, 'Federation')
        self.assertEqual(hostile['action'], 'deny_and_attack')
        self.assertTrue(hostile['patrolsHostile'])
        self.assertIn('hostile', hostile['message'].lower())

    def test_reputation_manifest_loads_factions_events_and_legal_thresholds(self):
        data = reputation_manifest()
        self.assertIn('Federation', data['factions'])
        self.assertIn('Independent', data['factions'])
        self.assertIn('mission_federation_report', data['events'])
        self.assertIn('destroy_pirate', data['events'])
        self.assertEqual(legal_status_for_score(data, 0), 'Clean')
        self.assertEqual(legal_status_for_score(data, -30), 'Offender')
        self.assertEqual(legal_status_for_score(data, -90), 'Fugitive')

    def test_reputation_events_adjust_faction_and_legal_records(self):
        data = reputation_manifest()
        reputation = {'Federation': 0, 'Independent': 0, 'Pirate': 0}
        legal = {'Federation': 0, 'Independent': 0}
        reputation, legal = apply_reputation_event(data, reputation, legal, 'mission_federation_report')
        self.assertGreater(reputation['Federation'], 0)
        self.assertLess(reputation['Pirate'], 0)
        reputation, legal = apply_reputation_event(data, reputation, legal, 'destroy_pirate')
        self.assertGreater(reputation['Federation'], 10)
        reputation, legal = apply_reputation_event(data, reputation, legal, 'contraband_fine', government='Federation')
        self.assertLess(legal['Federation'], 0)
        self.assertEqual(legal_status_for_score(data, legal['Federation']), 'Suspicious')

    def test_reputation_changes_effective_npc_disposition(self):
        data = reputation_manifest()
        self.assertEqual(
            effective_npc_disposition(data, 'neutral', 'confed', {'Federation': 10}, {'Federation': -90}, 'Federation'),
            'hostile',
        )
        self.assertEqual(
            effective_npc_disposition(data, 'hostile', 'pirate', {'Pirate': 8}, {}, 'Rim Freehold'),
            'neutral',
        )
        self.assertEqual(
            effective_npc_disposition(data, 'neutral', 'pirate', {'Pirate': -6}, {}, 'Rim Freehold'),
            'hostile',
        )

    def test_bad_legal_records_block_docking_at_strict_governments(self):
        data = reputation_manifest()
        self.assertTrue(can_dock_with_government(data, {'Federation': -20}, 'Federation'))
        self.assertFalse(can_dock_with_government(data, {'Federation': -65}, 'Federation'))
        self.assertTrue(can_dock_with_government(data, {'Rim Freehold': -65}, 'Rim Freehold'))

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
            reputation={'Federation': 12, 'Independent': 4, 'Pirate': -5},
            legal_records={'Federation': -12, 'Independent': 0},
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
        self.assertEqual(loaded['reputation']['Federation'], 12)
        self.assertEqual(loaded['legalRecords']['Federation'], -12)

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
        self.assertEqual(loaded['reputation'], {})
        self.assertEqual(loaded['legalRecords'], {})

    def test_godot_frontend_project_loads_existing_data_contract(self):
        root = Path(__file__).resolve().parents[2]
        project = root / 'godot_ev'
        self.assertTrue((project / 'project.godot').exists())
        self.assertTrue((project / 'scenes' / 'Main.tscn').exists())
        self.assertTrue((project / 'scripts' / 'main.gd').exists())
        self.assertTrue((project / 'scripts' / 'self_test.gd').exists())
        main_script = (project / 'scripts' / 'main.gd').read_text()
        self.assertIn('native_ev/data/universe.json', main_script)
        self.assertIn('native_ev/data/ships.json', main_script)
        self.assertIn('frame_%02d.png', main_script)
        self.assertIn('EV-style', main_script)

    def test_godot_landing_ui_exposes_core_ev_panels_from_file_backed_manifests(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for data_file in [
            'native_ev/data/missions.json',
            'native_ev/data/economy.json',
            'native_ev/data/outfits.json',
            'native_ev/data/weapons.json',
        ]:
            self.assertIn(data_file, main_script)
        for panel in ['Mission Computer', 'Commodity Exchange', 'Outfitter', 'Shipyard']:
            self.assertIn(panel, main_script)
        for tab_key in ['KEY_F1', 'KEY_F2', 'KEY_F3', 'KEY_F4']:
            self.assertIn(tab_key, main_script)
        self.assertIn('available_missions', main_script)
        self.assertIn('market_prices', main_script)
        self.assertIn('outfits_for_sale', main_script)
        self.assertIn('ships_for_sale', main_script)
        self.assertIn('weapons_for_sale', main_script)

    def test_godot_landing_panels_are_actionable(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for function_name in [
            '_accept_selected_mission',
            '_buy_selected_commodity',
            '_sell_selected_commodity',
            '_buy_selected_outfit_or_weapon',
            '_buy_selected_ship',
        ]:
            self.assertIn(f'func {function_name}', main_script)
        for state_name in [
            'active_missions',
            'completed_missions',
            'story_flags',
            'commodity_hold',
            'owned_outfits',
            'owned_weapons',
            'player_ship_id',
        ]:
            self.assertIn(state_name, main_script)
        for key_name in ['KEY_ENTER', 'KEY_B', 'KEY_S']:
            self.assertIn(key_name, main_script)
        for prompt in [
            'Enter accepts mission',
            'B buys one ton',
            'S sells one ton',
            'B buys selected upgrade',
            'B buys selected ship',
        ]:
            self.assertIn(prompt, main_script)

    def test_godot_scanner_has_target_lock_feedback(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for symbol in [
            'selected_target_index',
            '_cycle_target',
            '_draw_scanner_blips',
            'KEY_T',
            'Target:',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_ship_sprites_use_center_registered_fixed_cells(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for symbol in [
            'cell-center registration',
            'player_facing_index',
            'turn_cell_progress',
            '_visible_facing_index(player_facing_index)',
            '_draw_center_registered_ship_cell',
            'center - size * 0.5',
            'never rotates a texture or sprite sheet',
        ]:
            self.assertIn(symbol, main_script)
        self.assertNotIn('_draw_front_registered_ship_cell', main_script)
        self.assertNotIn('_front_cell_registration_point', main_script)
        self.assertNotIn('_draw_rotated_ship_texture', main_script)
        self.assertNotIn('draw_set_transform(center, deg_to_rad(angle_deg), Vector2.ONE)', main_script)
        self.assertNotIn('draw_arc(center,', main_script)

    def test_extracted_shuttle_rotation_frames_are_all_decoded(self):
        root = Path(__file__).resolve().parents[2]
        shuttle_dirs = [
            root / 'native_ev' / 'assets' / 'ships' / 'shuttle',
            root / 'native_ev' / 'assets' / 'ships' / 'ev_classic' / 'shuttle',
        ]
        for shuttle_dir in shuttle_dirs:
            frames = sorted(shuttle_dir.glob('frame_*.png'))
            self.assertEqual(len(frames), 36)
            alpha_counts = [_png_alpha_pixel_count(frame) for frame in frames]
            self.assertTrue(all(count > 0 for count in alpha_counts), alpha_counts)


if __name__ == '__main__':
    unittest.main()
