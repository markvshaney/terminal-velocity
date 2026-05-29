from pathlib import Path
import json
import re
import struct
import unittest
import wave
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
    sound_manifest,
    sourced_ev_graphics_manifest,
    sourced_ev_names_manifest,
    sourced_ev_sounds_manifest,
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
    def test_godot_prefs_modal_matches_original_ev_classic_observation(self):
        source = Path(__file__).resolve().parents[2] / 'godot_ev' / 'scripts' / 'main.gd'
        text = source.read_text()
        self.assertIn('const PREFS_SAVE_PATH := "user://terminal_velocity_prefs.json"', text)
        for symbol in [
            'Source-backed from original EV Classic title Set Prefs screen observed in Basilisk II',
            'Navigation Controls:',
            'Escort Controls:',
            'Weapon Controls:',
            'Misc. Controls:',
            'Sound Volume:',
            'Intro Music',
            'Game Speed...',
            'Cancel',
            'OK',
            'Backslash',
            'Closest Targ:',
        ]:
            self.assertIn(symbol, text)
        self.assertIn('load_prefs', text)

    def test_godot_self_test_covers_prefs_screenshot_artifact(self):
        source = Path(__file__).resolve().parents[2] / 'godot_ev' / 'scripts' / 'self_test.gd'
        text = source.read_text()
        self.assertIn('prefScreen=original-ev-classic-observed', text)
        self.assertIn('prefsScreenshot=', text)
        self.assertIn('strictPlay=off-by-default', text)
        self.assertIn('user://selftest/title_prefs.png', text)
        self.assertIn('_write_prefs_screenshot_artifact', text)

    def test_godot_self_test_covers_gameplay_scenario_curriculum(self):
        from native_ev.scenario_eval import available_scenarios

        root = Path(__file__).resolve().parents[2]
        manifest_path = root / 'native_ev' / 'data' / 'gameplay_curriculum.json'
        manifest = json.loads(manifest_path.read_text())
        self_test_script = (root / 'godot_ev' / 'scripts' / 'self_test.gd').read_text()

        self.assertEqual(manifest['scenarioOrder'], available_scenarios())
        self.assertIn('native_ev/data/gameplay_curriculum.json', self_test_script)
        self.assertIn('gameplayScenarios=%d', self_test_script)
        self.assertIn('_verify_gameplay_curriculum', self_test_script)
        self.assertIn('low_fuel_jump_recovery', manifest['scenarioOrder'])
        self.assertIn('blocked_reason_curriculum', manifest['scenarioOrder'])
        self.assertIn('disposable_combat_placeholder', manifest['scenarioOrder'])

    def test_wsl_godot_launcher_can_run_selftest_via_windows_binary(self):
        root = Path(__file__).resolve().parents[2]
        launcher = (root / 'run_godot.sh').read_text()
        for symbol in [
            'self-test',
            'powershell.exe',
            'Godot_v4.6.2-stable_win64_console.exe',
            'wslpath -w',
            '--headless --path',
            "--script 'res://scripts/self_test.gd'",
            'tv-movement-log',
            'tv-low-fuel-jump-log',
        ]:
            self.assertIn(symbol, launcher)

    def test_godot_new_pilot_modal_matches_original_ev_strict_play_observation(self):
        source = Path(__file__).resolve().parents[2] / 'godot_ev' / 'scripts' / 'main.gd'
        text = source.read_text()
        for symbol in [
            'var strict_play_selected := false',
            'strict_play_selected = false',
            'Enter your name, pilot:',
            'Strict Play',
            "If you check this box, when you're dead, you're dead. No reincarnation allowed.",
            '_strict_play_checkbox_rect',
            '_strict_play_toggle_rect',
            'Rect2(700, 492, 116, 34), "Cancel"',
            'Rect2(836, 492, 116, 34), "OK"',
            '"strict_play": strict_play_selected',
        ]:
            self.assertIn(symbol, text)

    def test_godot_deterministic_movement_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        self_test_script = (root / 'godot_ev' / 'scripts' / 'self_test.gd').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        checklist = (root / 'docs' / 'checklists' / 'ev-classic-behavior-baseline-checklist.md').read_text()
        for symbol in [
            '--tv-movement-log',
            'func _run_deterministic_movement_log',
            'TV_MOVEMENT_LOG scenario=right_turn ticks=12 ship=',
            'TV_MOVEMENT_LOG scenario=left_turn ticks=12 ship=',
            'TV_MOVEMENT_LOG scenario=thrust ticks=30 ship=',
            'TV_MOVEMENT_LOG scenario=coast ticks=30 ship=',
            'TV_MOVEMENT_LOG scenario=thrust_right_turn ticks=30 ship=',
            'func _movement_scenarios',
            'tickCount=',
            'facingIndex=',
            'angle=',
            'velocity=',
            'position=',
            'acceleration=',
            'maxSpeed=',
            'turning=',
            'turnCellsPerSecond=',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('movementLog=deterministic', self_test_script)
        self.assertIn('[switch]$MovementLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-movement-log', run_script)
        self.assertIn('Deterministic Godot movement log', checklist)
        self.assertIn('Status: `terminal-velocity-observed`', checklist)

    def test_godot_travel_and_landed_ui_logs_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        checklist = (root / 'docs' / 'checklists' / 'ev-classic-behavior-baseline-checklist.md').read_text()
        for symbol in [
            '--tv-travel-event-log',
            '--tv-landed-ui-matrix',
            'func _run_travel_event_log',
            'func _run_landed_ui_matrix',
            'TV_TRAVEL_EVENT',
            'TV_LANDED_UI_MATRIX',
            '"hyper_select"',
            '"jump"',
            'observationGuard=before_after_capture_required',
            '_ev_classic_landing_button_labels',
            'Spaceport Bar',
            'Mission Computer',
            'Commodity Exchange',
            'Outfitter',
            'Shipyard',
            'Leave',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$TravelEventLog', run_script)
        self.assertIn('[switch]$LandedUiMatrix', run_script)
        self.assertIn('--headless --path $Project -- --tv-travel-event-log', run_script)
        self.assertIn('--headless --path $Project -- --tv-landed-ui-matrix', run_script)
        self.assertIn('Event log for landing/takeoff/hyperspace transitions', checklist)
        self.assertIn('Full landed button/option walkthrough by port', checklist)

    def test_godot_map_route_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-map-route-log',
            'func _run_map_route_log',
            'TV_MAP_ROUTE_EVENT',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=user_demonstrated_pending_original_trace',
            '_select_map_route_at_position(click_position)',
            'func _map_linked_stop_at_position',
            'func _map_hovered_link_name',
            'Route selected: %s → %s — press J to jump',
            'Hold Shift and click a linked system',
            'No route from current system',
            'greenLine=true',
            'var selected_route: Array = []',
            'func _map_route_tail_system_name() -> String:',
            'func _append_map_route_at_position(click_position: Vector2) -> bool:',
            'routeHops=%d route=%s',
            'Route appended: %s',
            'draw_line(route_start_point, route_end_point, Color(0.15, 1.0, 0.28, 0.95), 3.0)',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MapRouteLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-map-route-log', run_script)
        self.assertIn('Basilisk source-oracle lane', plan)
        self.assertIn('Godot fast-eval lane', plan)
        self.assertIn('Bridge gate', plan)

    def test_godot_route_jump_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-route-jump-log',
            'func _run_route_jump_log',
            'TV_ROUTE_JUMP_EVENT',
            '_select_first_linked_map_route()',
            '_jump()',
            'jumpSucceeded=true',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=user_demonstrated_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$RouteJumpLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-route-jump-log', run_script)
        self.assertIn('Route-jump scenario contract', plan)
        self.assertIn('select route → jump', plan)

    def test_godot_route_jump_land_refuel_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-route-land-refuel-log',
            'func _run_route_land_refuel_log',
            'TV_ROUTE_LAND_REFUEL_EVENT',
            '_select_first_linked_map_route()',
            '_jump()',
            '_try_land()',
            'landingSucceeded=true',
            'refuelAvailable=true',
            'travelLoopComplete=true',
            'var fuel_before_jump := player_fuel',
            'var fuel_after_jump := player_fuel',
            'var fuel_before_refuel := player_fuel',
            'var fuel_after_refuel := player_fuel',
            '_jump_fuel_cost()',
            '_refuel_current_ship()',
            'fuelBeforeJump=%d fuelAfterJump=%d fuelBeforeRefuel=%d fuelAfterRefuel=%d fuelMax=%d',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=user_demonstrated_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$RouteLandRefuelLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-route-land-refuel-log', run_script)
        self.assertIn('Route-land-refuel scenario contract', plan)
        self.assertIn('select route → jump → land/refuel', plan)

    def test_godot_low_fuel_jump_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-low-fuel-jump-log',
            'func _run_low_fuel_jump_log',
            'TV_LOW_FUEL_JUMP_EVENT',
            '_select_first_linked_map_route()',
            'player_fuel = 0',
            'var fuel_before_jump := player_fuel',
            'var fuel_after_jump := player_fuel',
            '_jump()',
            'jumpBlocked=true',
            'blockReason=insufficient_fuel',
            'fuelBeforeJump=%d fuelAfterJump=%d fuelMax=%d',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=user_demonstrated_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$LowFuelJumpLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-low-fuel-jump-log', run_script)
        self.assertIn('Low-fuel jump scenario contract', plan)
        self.assertIn('blocked low-fuel jump', plan)

    def test_godot_mission_destination_route_hint_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-route-hint-log',
            'func _run_mission_route_hint_log',
            'TV_MISSION_ROUTE_HINT_EVENT',
            'func _route_to_active_mission_destination',
            'missionRouteQueued=true',
            'sourceLabel=terminal-velocity-design-scaffold',
            'oracleStatus=mission_objective_hint_pending_ev_classic_ui_trace',
            'KEY_G: _route_to_active_mission_destination()',
            'G queues active mission route',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionRouteHintLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-route-hint-log', run_script)
        self.assertIn('tv-mission-route-hint-log', wrapper)
        self.assertIn('Mission route-hint scenario contract', plan)
        self.assertIn('active mission destination → queued route leg', plan)

    def test_godot_mission_offer_scan_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        launcher = (root / 'run_godot.sh').read_text()
        for symbol in [
            '--tv-mission-offer-scan-log',
            'func _run_mission_offer_scan_log',
            'TV_MISSION_OFFER_SCAN_EVENT',
            '_select_map_route_to_system("Sol")',
            'offersBySurface=',
            'Mission Computer',
            'totalOffers=%d',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=terminal_velocity_eval_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionOfferScanLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-offer-scan-log', run_script)
        self.assertIn('tv-mission-offer-scan-log', launcher)

    def test_godot_first_mission_delivery_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        launcher = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-first-mission-delivery-log',
            'func _run_first_mission_delivery_log',
            'TV_FIRST_MISSION_DELIVERY_EVENT',
            '_select_map_route_to_system("Sol")',
            '_accept_selected_mission()',
            '_complete_arrived_missions()',
            'acceptedMission=intro_courier_earth_hera',
            'missionDelivered=true',
            'creditsBeforeAccept=%d creditsAfterDelivery=%d reward=%d',
            'cargoBeforeAccept=%d cargoAfterAccept=%d cargoAfterDelivery=%d',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=terminal_velocity_eval_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$FirstMissionDeliveryLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-first-mission-delivery-log', run_script)
        self.assertIn('tv-first-mission-delivery-log', launcher)
        self.assertIn('First mission delivery scenario contract', plan)
        self.assertIn('accept mission → route → jump → land → complete delivery', plan)

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

    def test_start_state_uses_source_backed_levo_system(self):
        universe = load_universe()
        economy = economy_manifest()
        governments = government_manifest()
        first_system = universe['systems'][0]
        self.assertEqual(first_system['name'], 'Levo')
        self.assertIn('Sol', first_system['links'])
        levo_body = next(body for body in first_system['bodies'] if body['name'] == 'Levo Spaceport')
        self.assertEqual(levo_body['sourceLandingName'], 'Levo')
        self.assertEqual(levo_body['evidenceLabel'], 'decoded-resource-backed')
        self.assertIn('tiny but neutral Levo Spaceport', levo_body['sourceEvidence'])
        self.assertIn('Levo', economy['markets'])
        self.assertEqual(governments['systems']['Levo']['government'], 'Independent')
        main_script = (Path(__file__).resolve().parents[2] / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        self.assertIn('const START_SYSTEM_NAME := "Levo"', main_script)
        self.assertIn('_system_index_by_name(START_SYSTEM_NAME, 0)', main_script)

    def test_levo_starting_market_matches_original_runtime_observation(self):
        universe = load_universe()
        economy = economy_manifest()
        levo_body = next(body for body in universe['systems'][0]['bodies'] if body['name'] == 'Levo Spaceport')
        inventory = station_inventory(universe, 'Levo', 'Levo Spaceport')
        self.assertEqual(inventory['outfitsForSale'], [])
        self.assertEqual(inventory['weaponsForSale'], [])
        self.assertNotIn('outfitter', inventory['services'])
        self.assertEqual([commodity['name'] for commodity in economy['commodities']], [
            'Food',
            'Industrial',
            'Medical',
            'Metal',
            'Equipment',
        ])
        levo_market = economy['markets']['Levo']
        self.assertEqual(levo_market['food']['buy'], 120)
        self.assertEqual(levo_market['industrial']['buy'], 192)
        self.assertEqual(levo_market['medical']['buy'], 600)
        self.assertEqual(levo_market['metal']['buy'], 144)
        self.assertEqual(levo_market['equipment']['buy'], 360)
        self.assertEqual(levo_market['food']['sell'], 120)
        self.assertEqual(levo_market['industrial']['sell'], 192)
        self.assertEqual(levo_market['medical']['sell'], 600)
        self.assertEqual(levo_market['metal']['sell'], 144)
        self.assertEqual(levo_market['equipment']['sell'], 360)
        self.assertEqual({prices['evClassicPriceStatus'] for prices in levo_market.values()}, {'Low', 'Med'})

    def test_godot_landing_panel_uses_original_levo_button_and_hold_wording(self):
        source = Path(__file__).resolve().parents[2] / 'godot_ev' / 'scripts' / 'main.gd'
        text = source.read_text()
        for symbol in [
            'Spaceport Bar',
            'Mission Computer',
            'Commodity Exchange',
            'In Hold:',
            'Price:',
            'Buy',
            'Leave',
            '_draw_ev_classic_landing_buttons',
            '_ev_classic_price_status',
        ]:
            self.assertIn(symbol, text)

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
        self.assertEqual(data['method'], 'evnew-opcode-rled-shan-pict-cicn-ppat-spin-boom-roid-v7')
        self.assertEqual(data['resourceCount'], 303)
        resources_by_type = {}
        for resource in data['resources']:
            resources_by_type.setdefault(resource['type'], 0)
            resources_by_type[resource['type']] += 1
        catalog = {entry['type']: entry for entry in data['resourceTypeCatalog']}
        self.assertEqual(catalog['PICT']['decodeStatus'], 'decoded-to-png')
        self.assertEqual(catalog['rlëD']['decodeStatus'], 'decoded-to-png')
        self.assertEqual(catalog['cicn']['decodeStatus'], 'decoded-to-png-with-explicit-errors')
        self.assertEqual(catalog['ppat']['decodeStatus'], 'decoded-to-png-with-explicit-errors')
        self.assertEqual(catalog['spïn']['count'], 58)
        self.assertEqual(catalog['spïn']['decodeStatus'], 'decoded-primitive-fields')
        self.assertEqual(catalog['bööm']['decodeStatus'], 'decoded-primitive-fields')
        self.assertEqual(catalog['röid']['decodeStatus'], 'decoded-primitive-fields')
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
        non_sprite_rled = next(asset for asset in data['rledAssets'] if asset.get('resourceId') == 4004)
        self.assertEqual(non_sprite_rled['status'], 'non-sprite-record')
        self.assertEqual(non_sprite_rled['rled']['decodeStatus'], 'non-sprite-record')
        self.assertEqual(non_sprite_rled['rawWords'][:3], [32767, 40, -1])
        decoded_pict = [asset for asset in data['pictAssets'] if asset.get('status') == 'ok']
        self.assertGreaterEqual(len(decoded_pict), 90)
        shipyard_pic = next(asset for asset in decoded_pict if asset.get('resourceId') == 5000)
        self.assertEqual(shipyard_pic['width'], 100)
        self.assertEqual(shipyard_pic['height'], 100)
        self.assertTrue(shipyard_pic['assetFile'].startswith('assets/graphics/pict/'))
        asteroid_belt_pic = next(asset for asset in decoded_pict if asset.get('resourceId') == 9507)
        self.assertEqual(asteroid_belt_pic['name'], 'Trugati Asteroid Belt')
        self.assertEqual(asteroid_belt_pic['width'], 32)
        self.assertEqual(asteroid_belt_pic['height'], 32)
        self.assertEqual(asteroid_belt_pic['pict']['format'], 'uncompressed-indexed-pixmap-with-color-table')
        self.assertEqual(asteroid_belt_pic['pict']['pixmapOffset'], 32)
        self.assertEqual(asteroid_belt_pic['pict']['pixelSize'], 4)
        self.assertEqual(asteroid_belt_pic['pict']['colorTable']['ctSize'], 10)
        decoded_cicn = [asset for asset in data['cicnAssets'] if asset.get('status') == 'ok']
        self.assertEqual(len(decoded_cicn), 28)
        cicn_1bit = next(asset for asset in decoded_cicn if asset.get('resourceId') == 10000)
        self.assertEqual(cicn_1bit['width'], 16)
        self.assertEqual(cicn_1bit['height'], 16)
        self.assertEqual(cicn_1bit['cicn']['pixelSize'], 1)
        self.assertEqual(cicn_1bit['cicn']['colorTableOffset'], 146)
        cicn_8bit = next(asset for asset in decoded_cicn if asset.get('resourceId') == 18000)
        self.assertEqual(cicn_8bit['width'], 32)
        self.assertEqual(cicn_8bit['height'], 32)
        self.assertEqual(cicn_8bit['cicn']['pixelSize'], 8)
        self.assertEqual(cicn_8bit['cicn']['colorTable']['ctSize'], 19)
        unsupported_cicn = next(asset for asset in data['cicnAssets'] if asset.get('resourceId') == 20000)
        self.assertEqual(unsupported_cicn['status'], 'decode-error: unsupported cicn PixMap header')
        self.assertEqual(unsupported_cicn['rawHeaderBytes'][:6], [0, 0, 0, 0, 0, 0])
        decoded_ppat = [asset for asset in data['ppatAssets'] if asset.get('status') == 'ok']
        self.assertEqual(len(decoded_ppat), 9)
        ppat_128 = next(asset for asset in decoded_ppat if asset.get('resourceId') == 128)
        self.assertEqual(ppat_128['width'], 32)
        self.assertEqual(ppat_128['height'], 32)
        self.assertEqual(ppat_128['ppat']['format'], 'classic-ppat-indexed-pixpat-with-color-table')
        self.assertEqual(ppat_128['ppat']['pixmapOffset'], 32)
        self.assertEqual(ppat_128['ppat']['pixelSize'], 4)
        self.assertEqual(ppat_128['ppat']['colorTable']['ctSize'], 10)
        ppat_133 = next(asset for asset in decoded_ppat if asset.get('resourceId') == 133)
        self.assertEqual(ppat_133['ppat']['colorTable']['ctSize'], 9)
        unsupported_ppat = next(asset for asset in data['ppatAssets'] if asset.get('resourceId') == 137)
        self.assertEqual(unsupported_ppat['status'], 'decode-error: unsupported ppat PixPat/PixMap layout')
        self.assertEqual(unsupported_ppat['rawHeaderBytes'][:4], [0, 8, 0, 8])

    def test_sourced_ev_graphics_manifest_interprets_spin_boom_roid_metadata(self):
        data = sourced_ev_graphics_manifest()
        resources = {(resource['type'], resource['resourceId']): resource for resource in data['resources']}

        small_explosion = resources[('spïn', 400)]['spin']
        self.assertEqual(small_explosion['baseRledResourceId'], 4000)
        self.assertEqual(small_explosion['maskRledResourceId'], 4001)
        self.assertEqual(small_explosion['displayWidth'], 32)
        self.assertEqual(small_explosion['displayHeight'], 26)
        self.assertEqual(small_explosion['frameRows'], 8)
        self.assertEqual(small_explosion['frameColumns'], 1)
        self.assertEqual(small_explosion['linkedRled']['status'], 'ok')
        self.assertEqual(small_explosion['linkedRled']['frames'], 8)

        laser_bolt = resources[('spïn', 3000)]['spin']
        self.assertEqual(laser_bolt['baseRledResourceId'], 200)
        self.assertEqual(laser_bolt['maskRledResourceId'], 201)
        self.assertEqual(laser_bolt['displayWidth'], 8)
        self.assertEqual(laser_bolt['displayHeight'], 8)
        self.assertEqual(laser_bolt['frameRows'], 6)
        self.assertEqual(laser_bolt['frameColumns'], 6)
        self.assertEqual(laser_bolt['linkedRled']['frames'], 36)

        small_fae = resources[('bööm', 128)]['boom']
        self.assertEqual(small_fae['durationTicks'], 100)
        self.assertEqual(small_fae['soundResourceId'], 1)
        self.assertEqual(small_fae['spinResourceId'], 400)
        self.assertEqual(small_fae['linkedSpinName'], 'Small Explosion')

        ship_explodes = resources[('bööm', 132)]['boom']
        self.assertEqual(ship_explodes['variantCount'], 5)
        self.assertEqual(ship_explodes['variantResourceIds'], [128, 129, 130, 131, 132])
        self.assertEqual(ship_explodes['status'], 'forklift-variant-table')

        small_asteroids = resources[('röid', 128)]['roid']
        self.assertEqual(small_asteroids['spinResourceId'], 800)
        self.assertEqual(small_asteroids['linkedSpinName'], 'Small Asteroids')
        self.assertEqual(small_asteroids['rledResourceId'], 800)
        self.assertEqual(small_asteroids['linkedRled']['frames'], 30)

        big_asteroids = resources[('röid', 129)]['roid']
        self.assertEqual(big_asteroids['spinResourceId'], 801)
        self.assertEqual(big_asteroids['linkedSpinName'], 'Big Asteroids')
        self.assertEqual(big_asteroids['rledResourceId'], 802)
        self.assertEqual(big_asteroids['linkedRled']['frames'], 36)

    def test_sourced_ev_sounds_manifest_decodes_classic_mac_snd_resources(self):
        data = sourced_ev_sounds_manifest()
        self.assertEqual(data['sourceFile'], 'source-assets/ev-classic/Nova Files/EV Sounds.rez')
        self.assertEqual(data['sourceSha256'], '36fc306b41bb384e07ea78fe78ede115d02695f9eb01e6b8189b3a1280261f0e')
        self.assertEqual(data['method'], 'classic-mac-snd-wav-v2')
        self.assertEqual(data['chunkCount'], 58)
        self.assertEqual(data['resourceCount'], 57)
        self.assertEqual(data['resourceTypeCatalog'], [{
            'type': 'snd ',
            'count': 57,
            'decodeStatus': 'decoded-to-wav-with-explicit-errors',
            'note': 'classic Mac sound resources cataloged; 56 decoded to 8-bit mono WAV',
        }])
        sounds = data['soundAssets']
        decoded = [sound for sound in sounds if sound['status'] == 'ok']
        self.assertEqual(len(sounds), 57)
        self.assertEqual(len(decoded), 56)
        by_id = {sound['resourceId']: sound for sound in sounds}
        self.assertEqual(by_id[128]['name'], 'Warp Up')
        self.assertEqual(by_id[128]['chunkIndex'], 1)
        self.assertEqual(by_id[128]['size'], 45508)
        self.assertEqual(by_id[128]['status'], 'ok')
        self.assertEqual(by_id[128]['rawHeaderBytes'][:8], [0, 2, 0, 0, 0, 1, 128, 81])
        self.assertEqual(by_id[128]['sound']['sampleCount'], 45472)
        self.assertEqual(by_id[128]['sound']['sampleRateHz'], 11127)
        self.assertEqual(by_id[128]['sound']['encoding'], 0)
        self.assertEqual(by_id[200]['name'], 'Laser')
        self.assertEqual(by_id[223]['name'], 'Engine')
        self.assertEqual(by_id[30003]['name'], 'Transition')
        self.assertEqual(by_id[30003]['status'], 'decode-error: unsupported snd format 0')
        laser_path = Path('native_ev') / by_id[200]['assetFile']
        with wave.open(str(laser_path), 'rb') as wav:
            self.assertEqual(wav.getnchannels(), 1)
            self.assertEqual(wav.getsampwidth(), 1)
            self.assertEqual(wav.getframerate(), 11127)
            self.assertEqual(wav.getnframes(), by_id[200]['sound']['sampleCount'])
        self.assertTrue(all(sound['type'] == 'snd ' for sound in sounds))

    def test_runtime_sound_manifest_maps_source_backed_sounds_to_game_events(self):
        data = sound_manifest()
        sounds = {sound['id']: sound for sound in data['sounds']}
        self.assertEqual(data['source'], 'native_ev/data/sourced_ev_sounds.json')
        self.assertEqual(data['method'], 'ev-classic-runtime-sound-bindings-v1')
        self.assertGreaterEqual(len(sounds), 10)
        self.assertEqual(sounds['weapon_laser']['sourceResourceId'], 200)
        self.assertEqual(sounds['weapon_laser']['name'], 'Laser')
        self.assertEqual(sounds['weapon_laser']['assetFile'], 'assets/sounds/ev_classic/200_laser/sound.wav')
        self.assertEqual(sounds['weapon_cannon']['sourceResourceId'], 205)
        self.assertEqual(sounds['ui_click']['sourceResourceId'], 601)
        self.assertEqual(sounds['engine_loop']['sourceResourceId'], 223)
        self.assertEqual(data['bindings']['weapons']['laser_cannon'], 'weapon_laser')
        self.assertEqual(data['bindings']['weapons']['pulse_cannon'], 'weapon_cannon')
        for sound in sounds.values():
            self.assertTrue((Path('native_ev') / sound['assetFile']).exists())
            self.assertEqual(sound['channels'], 1)
            self.assertEqual(sound['sampleWidthBytes'], 1)

    def test_universe_uses_a_seed_set_of_sourced_ev_names(self):
        universe = load_universe()
        names = {system['name'] for system in universe['systems']}
        body_names = {body['name'] for system in universe['systems'] for body in system['bodies']}
        self.assertTrue({'Sol', 'Centauri', 'Sirius', 'Tau Ceti'}.issubset(names))
        self.assertTrue({'Earth', 'Stardock Alpha', 'Mars', 'Landfall'}.issubset(body_names))

    def test_ship_manifest_loads_player_and_npc_assets(self):
        data = ship_manifest()
        ids = {ship['id'] for ship in data['ships']}
        self.assertIn('shuttlecraft', ids)
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
        self.assertEqual(by_ordinal[0]['id'], 'shuttlecraft')
        self.assertEqual(by_ordinal[5]['id'], 'confed_frigate')
        self.assertEqual(by_ordinal[5]['name'], 'Confed Frigate')
        self.assertEqual(by_ordinal[5]['shipResourceId'], 133)
        self.assertEqual(by_ordinal[5]['assetDir'], 'assets/ships/ev_classic/frigate')
        self.assertEqual(by_ordinal[0]['shipyardPictResourceId'], 5000)
        self.assertEqual(by_ordinal[0]['sourceDataPhysicsFields'], {
            'cargoSpace': 20,
            'shields': 180,
            'acceleration': 979,
            'maxSpeed': 413,
            'turning': 60,
            'fuel': 400,
            'freeMass': 15,
            'armor': 100,
            'shieldRecharge': 42,
        })
        self.assertEqual(by_ordinal[0]['acceleration'], 979)
        self.assertEqual(by_ordinal[0]['maxSpeed'], 413)
        self.assertEqual(by_ordinal[0]['turning'], 60)
        self.assertEqual(by_ordinal[0]['physicsSource'], 'EV Data.rez ship-like record words 0-8 via EVNEW CShipResource field order')
        self.assertEqual(by_ordinal[1]['sourceDataPhysicsFields']['acceleration'], 428)
        self.assertEqual(by_ordinal[1]['sourceDataPhysicsFields']['maxSpeed'], 188)
        self.assertEqual(by_ordinal[1]['sourceDataPhysicsFields']['turning'], 30)
        self.assertEqual(by_ordinal[0]['shipyardPictAssetFile'], 'assets/graphics/pict/5000_shipyard/image.png')
        self.assertTrue((Path('native_ev') / by_ordinal[0]['shipyardPictAssetFile']).exists())
        self.assertEqual(by_ordinal[15]['shipyardPictResourceId'], 5015)
        self.assertNotIn('shipyardPictResourceId', by_ordinal[24])
        self.assertEqual(by_ordinal[6]['id'], 'confed_cruiser')
        self.assertEqual(by_ordinal[6]['name'], 'Confed Cruiser')
        self.assertEqual(by_ordinal[14]['role'], 'npc-hostile')
        self.assertEqual(by_ordinal[22]['role'], 'npc-hostile')
        self.assertEqual(by_ordinal[11]['id'], 'exec_transport')
        self.assertEqual(by_ordinal[12]['id'], 'luxury_liner')
        self.assertEqual(by_ordinal[15]['name'], 'Kestrel')
        self.assertEqual(by_ordinal[15]['id'], 'kestrel')
        self.assertEqual(by_ordinal[15]['shipResourceId'], 143)
        self.assertEqual(by_ordinal[15]['resourceId'], 1030)
        self.assertEqual(by_ordinal[24]['id'], 'kestrel_24')
        self.assertEqual(by_ordinal[24]['shipResourceId'], 152)
        self.assertEqual(by_ordinal[24]['resourceId'], 1002)
        self.assertEqual(by_ordinal[15]['graphicsName'], 'Kestrel')
        self.assertNotIn(26, by_ordinal)
        self.assertEqual(ship_manifest()['ships'], generated['ships'])

    def test_ship_runtime_consumers_reference_data_identity_ship_ids(self):
        ships = ship_manifest()
        outfits = outfit_manifest()
        universe = load_universe()
        ids = {ship['id'] for ship in ships['ships']}
        expected_ids = set()
        seen = set()
        for ship in ships['ships']:
            base_id = re.sub(r'[^a-z0-9]+', '_', ship['name'].lower().replace('ö', 'o').replace('ë', 'e').replace('ï', 'i')).strip('_') or 'unnamed'
            expected_id = base_id if base_id not in seen else f"{base_id}_{ship['sourceDataOrdinal']}"
            seen.add(base_id)
            expected_ids.add(expected_id)
            self.assertEqual(ship['id'], expected_id)
        traffic_ids = {entry['shipId'] for entry in ships['traffic']}
        shipyard_ids = {entry['shipId'] for entry in outfits['shipyard']}
        inventory_ids = {
            ship_id
            for system in universe['systems']
            for body in system.get('bodies', [])
            for ship_id in body.get('inventory', {}).get('shipsForSale', [])
        }
        self.assertTrue(traffic_ids.issubset(ids))
        self.assertEqual(shipyard_ids, expected_ids)
        self.assertTrue(inventory_ids.issubset(ids))
        self.assertNotIn('frigate', ids)
        self.assertNotIn('cruiser', ids)
        self.assertNotIn('gunboat', ids)
        self.assertNotIn('kestrel_152', ids)

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
        self.assertIn('shuttlecraft', ship_ids)
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
        self.assertIn('industrial', commodity_ids)
        self.assertIn('Sol', data['markets'])
        self.assertIn('Sirius', data['markets'])
        self.assertGreater(data['markets']['Sirius']['industrial']['sell'], data['markets']['Sol']['industrial']['buy'])

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
        self.assertIn('equipment', data['contraband']['Federation'])
        self.assertGreater(data['governments']['Federation']['finePerTon'], 0)

    def test_contraband_fine_math(self):
        self.assertEqual(fine_for_contraband({'equipment': 2, 'food': 5}, {'equipment'}, 400), 800)
        self.assertEqual(fine_for_contraband({'food': 5}, {'equipment'}, 400), 0)

    def test_police_outcome_bribes_low_level_contraband_when_config_allows(self):
        governments = government_manifest()
        reputation = reputation_manifest()
        outcome = enforcement_outcome(
            governments,
            reputation,
            government='Independent',
            hold={'medical': 1, 'food': 2},
            credits=2000,
            legal_records={'Independent': 0},
            accept_bribe=True,
        )
        self.assertEqual(outcome['action'], 'bribe')
        self.assertGreater(outcome['creditsDelta'], -1000)
        self.assertEqual(outcome['confiscated'], {'medical': 0})
        self.assertEqual(outcome['legalDelta'], 0)

    def test_police_outcome_fines_and_confiscates_contraband(self):
        governments = government_manifest()
        reputation = reputation_manifest()
        outcome = enforcement_outcome(
            governments,
            reputation,
            government='Federation',
            hold={'equipment': 2, 'food': 3},
            credits=5000,
            legal_records={'Federation': 0},
            accept_bribe=False,
        )
        self.assertEqual(outcome['action'], 'fine')
        self.assertEqual(outcome['creditsDelta'], -800)
        self.assertEqual(outcome['confiscated'], {'equipment': 2})
        self.assertEqual(outcome['legalDelta'], -10)

    def test_police_outcome_escalates_when_player_cannot_pay_fine(self):
        governments = government_manifest()
        reputation = reputation_manifest()
        outcome = enforcement_outcome(
            governments,
            reputation,
            government='Militia Compact',
            hold={'equipment': 1, 'medical': 1},
            credits=100,
            legal_records={'Militia Compact': -40},
            accept_bribe=False,
        )
        self.assertEqual(outcome['action'], 'confiscate')
        self.assertEqual(outcome['confiscated'], {'equipment': 1, 'medical': 1})
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
            commodity_hold={'industrial': {'tons': 3, 'basis': 240}},
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
        self.assertEqual(loaded['commodityHold']['industrial']['tons'], 3)
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
        self.assertEqual(loaded['playerShipId'], 'shuttlecraft')
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
        self.assertIn('native_ev/data/sounds.json', main_script)
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
            'In Hold:',
            'Price:',
            'Buy',
            'B buys selected upgrade',
            'B buys selected ship',
            'func _mission_by_id(mission_id: String) -> Dictionary:',
            'func _mission_summary_lines() -> Array[String]:',
            'Mission Info: %s to %s/%s, %d tons, %d cr',
            'Cargo reserved for missions:',
            'func _cargo_available_tons() -> int:',
            'Cargo: %d/%d (%d mission, %d free)',
            'Mission Info: %d active / %d tons reserved',
            'func _set_status(message: String) -> void:',
            'status_messages.append(message)',
            'Messages:',
            '_set_status("Need %d free cargo tons" % tons)',
            '_set_status("Cargo hold full")',
            'func _ship_comparison_line(ship: Dictionary) -> String:',
            'Δ cargo %+d  Δ hull %+d  Δ speed %+d',
            'func _outfit_effect_summary(item: Dictionary) -> String:',
            'Effect: ',
            'func _draw_help_overlay() -> void:',
            'Terminal Velocity helper/scaffold — not an EV Classic fidelity claim.',
            'Mission route helper: G queues the active mission destination when known.',
            'Shipyard/outfitter: listings show local manifest deltas/effects before buying.',
            'KEY_F10:',
            'Fuel: %d/%d',
            'KEY_F5:',
            'Refuel: F5 available',
            'F5 Refuel',
            '_set_status("Refueled at " + str(body.get("name", "port")))',
        ]:
            self.assertIn(prompt, main_script)

    def test_godot_commodity_trade_uses_ev_classic_ten_ton_lots(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        self.assertIn('const EV_CLASSIC_COMMODITY_LOT_SIZE := 10', main_script)
        self.assertIn('min(EV_CLASSIC_COMMODITY_LOT_SIZE, free_space, affordable_tons)', main_script)
        self.assertIn('price * tons', main_script)
        self.assertIn('Bought %d tons of %s', main_script)
        self.assertIn('Sold %d tons of %s', main_script)

    def test_godot_click_sound_is_wired_to_landing_actions(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for symbol in [
            'AudioStreamPlayer',
            '_load_sound_stream',
            '_play_sound("ui_click")',
            '_sound_by_id("ui_click")',
            'assets/sounds/ev_classic/601_click/sound.wav',
        ]:
            self.assertIn(symbol, main_script)
        for function_name in [
            '_accept_selected_mission',
            '_buy_selected_commodity',
            '_sell_selected_commodity',
            '_buy_selected_outfit_or_weapon',
            '_buy_selected_ship',
        ]:
            function_body = main_script.split(f'func {function_name}', 1)[1].split('\nfunc ', 1)[0]
            self.assertIn('_play_sound("ui_click")', function_body)

    def test_godot_self_test_loads_source_backed_sound_assets(self):
        root = Path(__file__).resolve().parents[2]
        self_test_script = (root / 'godot_ev' / 'scripts' / 'self_test.gd').read_text()
        for symbol in [
            'native_ev/data/sounds.json',
            'ui_click',
            'AudioStreamWAV',
            'GODOT SELFTEST FAIL sound',
            'soundsLoaded=%d',
        ]:
            self.assertIn(symbol, self_test_script)

    def test_godot_title_stubs_are_real_modals(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for symbol in [
            'title_modal = "about"',
            'func _draw_about_modal',
            'About Terminal Velocity',
            'personal-use EV-style Godot reconstruction',
            'title_modal = "prefs"',
            'func _draw_prefs_modal',
            'Navigation Controls:',
            'Intro Music',
            'pref_sound_on',
            'pref_music_on',
            'pref_game_speed_index',
            'Game Speed...',
        ]:
            self.assertIn(symbol, main_script)
        self.assertNotIn('Preferences are not implemented yet.', main_script)

    def test_godot_shipyard_loads_source_backed_pict_art(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        self_test_script = (root / 'godot_ev' / 'scripts' / 'self_test.gd').read_text()
        for symbol in [
            'shipyardPictAssetFile',
            '_load_shipyard_pict_textures',
            '_shipyard_texture_for_listing',
            'draw_texture_rect',
            'assets/graphics/pict/5000_shipyard/image.png',
        ]:
            self.assertIn(symbol, main_script)
        for symbol in [
            'shipyardPictAssetFile',
            'GODOT SELFTEST FAIL pict',
            'pictsLoaded=%d',
        ]:
            self.assertIn(symbol, self_test_script)

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

    def test_godot_defaults_to_observed_ev_classic_keybindings(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for symbol in [
            'KEY_L: _ev_land_or_launch()',
            'KEY_J: _jump()',
            'KEY_H: _toggle_hyper_mode()',
            'KEY_BACKSLASH: _cycle_link(1)',
            'KEY_N: _cycle_target(1)',
            'KEY_R: _select_closest_target()',
            'KEY_P: _show_player_info()',
            'KEY_I: _show_mission_info()',
            'KEY_Z: _afterburner_active()',
            'KEY_TAB: _fire_primary_weapon()',
            'KEY_SPACE: _fire_secondary_weapon()',
            'KEY_S: _change_secondary_weapon()',
            'KEY_A: _toggle_autopilot()',
        ]:
            self.assertIn(symbol, main_script)
        self.assertNotIn('KEY_H:\n\t\t\t\t_jump()', main_script)
        self.assertNotIn('KEY_R:\n\t\t\t\tpos = PLAYER_START', main_script)

    def test_godot_universe_map_screen_is_actionable(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for symbol in [
            'map_visible',
            'KEY_M',
            'func _toggle_universe_map',
            'func _draw_universe_map',
            'GALAXY MAP',
            'Current:',
            'Selected:',
            'linked',
            'system.get("x"',
            'system.get("y"',
            'draw_line(map_point',
            'draw_circle(map_point',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_universe_map_shift_click_sets_green_route(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for symbol in [
            'event.shift_pressed',
            '_select_map_route_at_position(event.position)',
            'func _select_map_route_at_position',
            'func _append_map_route_at_position',
            'func _map_system_points',
            'func _map_route_tail_system_name() -> String:',
            'Shift-click linked stops: green route',
            'Route selected:',
            'Route appended:',
            'Color(0.15, 1.0, 0.28, 0.95)',
            'draw_line(route_start_point, route_end_point',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_ship_sprites_use_center_registered_fixed_cells(self):
        root = Path(__file__).resolve().parents[2]
        main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
        for symbol in [
            'cell-center registration',
            'player_facing_index',
            'turn_cell_progress',
            '_ship_acceleration()',
            '_ship_max_speed()',
            '_ship_turn_cells_per_second()',
            'Source-backed EV Data.rez ship physics',
            '* 0.375',
            'vel = vel.limit_length(_ship_max_speed())',
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
