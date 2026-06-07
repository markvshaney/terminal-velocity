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
    profile_manifest,
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
    sourced_ev_governments_manifest,
    sourced_ev_missions_manifest,
    sourced_ev_names_manifest,
    sourced_ev_sounds_manifest,
    sourced_ev_structures_manifest,
    sourced_ev_weapons_manifest,
    ship_graphics_crosswalk,
    ev_classic_data_ship_manifest,
    shuttle_frame_paths,
    station_inventory,
    system_distance,
    trade_profit,
    weapon_manifest,
)



def _godot_contract_text(root: Path) -> str:
    """Godot script plus data-driven UI contract manifests."""
    main_script = (root / 'godot_ev' / 'scripts' / 'main.gd').read_text()
    help_overlay_path = root / 'native_ev' / 'data' / 'help_overlay.json'
    help_overlay_text = help_overlay_path.read_text() if help_overlay_path.exists() else ''
    return main_script + '\n' + help_overlay_text


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
    def test_classic_profile_descriptor_validates_runtime_and_source_manifests(self):
        profile = profile_manifest('classic')

        self.assertEqual(profile['id'], 'classic')
        self.assertEqual(profile['startSystemName'], 'Levo')
        self.assertEqual(profile['sourceLabel'], 'ev-classic-profile-descriptor-scaffold')
        self.assertEqual(
            profile['oracleStatus'],
            'profile_manifest_paths_source_backed_runtime_profile_switching_pending',
        )
        for key in [
            'universe',
            'ships',
            'missions',
            'economy',
            'sounds',
            'weapons',
            'outfits',
            'governments',
            'reputation',
            'gameplayCurriculum',
            'helpOverlay',
        ]:
            self.assertIn(key, profile['dataManifests'])
        for key in [
            'sourcedEvStructures',
            'sourcedEvMissions',
            'sourcedEvGovernments',
            'sourcedEvGraphics',
            'sourcedEvSounds',
            'sourcedEvWeapons',
        ]:
            self.assertIn(key, profile['sourceManifests'])

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
            'Closest Target:',
        ]:
            self.assertIn(symbol, text)
        for label, expected_key in [
            ('Fire Primary:', 'Tab'),
            ('Fire Secondary:', 'Space'),
            ('Change Secondary:', 'S'),
            ('Next Target:', 'N'),
            ('Closest Target:', 'R'),
        ]:
            self.assertIn(f'_draw_key_binding(Vector2(550, ', text)
            self.assertIn(f'"{label}", "{expected_key}"', text)
        self.assertNotIn('"Target Select:", "Tab"', text)
        self.assertIn('load_prefs', text)

    def test_godot_runtime_weapon_keybindings_match_original_ev_classic_observation(self):
        source = Path(__file__).resolve().parents[2] / 'godot_ev' / 'scripts' / 'main.gd'
        text = source.read_text()
        observed_runtime_bindings = {
            'KEY_TAB': '_fire_primary_weapon()',
            'KEY_SPACE': '_fire_secondary_weapon()',
            'KEY_S': '_change_secondary_weapon()',
            'KEY_N': '_cycle_target(1)',
            'KEY_R': '_select_closest_target()',
        }
        for keycode, handler in observed_runtime_bindings.items():
            self.assertRegex(text, rf'{keycode}:\s*{re.escape(handler)}')
        self.assertNotRegex(text, r'KEY_SPACE:\s*_fire_primary_weapon\(\)')
        self.assertNotRegex(text, r'KEY_TAB:\s*_cycle_target\(1\)')

    def test_godot_self_test_covers_prefs_screenshot_artifact(self):
        source = Path(__file__).resolve().parents[2] / 'godot_ev' / 'scripts' / 'self_test.gd'
        text = source.read_text()
        self.assertIn('prefScreen=original-ev-classic-observed', text)
        self.assertIn('prefsScreenshot=', text)
        self.assertIn('strictPlay=off-by-default', text)
        self.assertIn('profile=classic', text)
        self.assertIn('profileManifests=%d', text)
        self.assertIn('native_ev/data/profiles/classic.json', text)
        self.assertIn('_verify_classic_profile', text)
        self.assertIn('user://selftest/title_prefs.png', text)
        self.assertIn('_write_prefs_screenshot_artifact', text)

    def test_godot_self_test_covers_gameplay_scenario_curriculum(self):
        from native_ev.scenario_eval import available_scenarios

        root = Path(__file__).resolve().parents[2]
        manifest_path = root / 'native_ev' / 'data' / 'gameplay_curriculum.json'
        manifest = json.loads(manifest_path.read_text())
        self_test_script = (root / 'godot_ev' / 'scripts' / 'self_test.gd').read_text()

        self.assertEqual(manifest['scenarioOrder'], available_scenarios())
        self.assertEqual(set(manifest['scenarios']), set(manifest['scenarioOrder']))
        self.assertIn('native_ev/data/gameplay_curriculum.json', self_test_script)
        self.assertIn('gameplayScenarios=%d', self_test_script)
        self.assertIn('_verify_gameplay_curriculum', self_test_script)
        self.assertIn('low_fuel_jump_recovery', manifest['scenarioOrder'])
        self.assertIn('blocked_reason_curriculum', manifest['scenarioOrder'])
        self.assertIn('mission_deadline_failure_scaffold', manifest['scenarioOrder'])
        self.assertIn('mission_trade_hybrid_capacity_planning', manifest['scenarioOrder'])
        self.assertIn('federation_alignment_delivery_loop', manifest['scenarioOrder'])
        self.assertIn('disabled_player_recovery_loop', manifest['scenarioOrder'])
        self.assertIn('pirate_avoidance_escape_route', manifest['scenarioOrder'])
        self.assertIn('disposable_combat_placeholder', manifest['scenarioOrder'])

    def test_godot_help_exposes_gameplay_curriculum_hints_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        help_manifest = json.loads((root / 'native_ev' / 'data' / 'help_overlay.json').read_text())
        help_lines = help_manifest['lines']
        help_probes = {probe['flag']: probe for probe in help_manifest['logProbes']}

        for symbol in [
            'var gameplay_curriculum := {}',
            'var help_overlay := {}',
            'native_ev/data/gameplay_curriculum.json',
            'native_ev/data/help_overlay.json',
            'func _gameplay_curriculum_hint_lines',
            'func _help_overlay_lines',
            'func _help_overlay_log_probes',
            'Terminal Velocity curriculum hints — scaffold',
            'TV_GAMEPLAY_CURRICULUM_HELP',
            '--tv-gameplay-curriculum-help-log',
        ]:
            self.assertIn(symbol, main_script)
        for expected_line in [
            'Map service/legal summary: selected systems show Terminal Velocity station services and legal risk.',
            'Service provisioning scout: newly reached ports need service/store checks before buying; Levo no-outfitter evidence is Classic-observed, other service matrices stay TV scaffold until confirmed.',
            'Route/fuel planning: G and Shift-click route status show hop cost and refuel-before-full-route warnings before J jumps.',
            'Route planner refuel recovery: if a planned return jump blocks after fuel is spent, keep the route state stable, land at the service port, refuel, and verify fuel before retrying. TV route-planner scaffold; exact Classic refuel UI pending.',
            'Travel timing recovery: after L launch/leave or H/\\ hyper-select, wait for the HUD travel event state before retrying J or landing; TV event-log scaffold, exact Classic transition timing/sound pending.',
            'Navigation guardrail recovery: if J/L/F5 blocks, read the HUD reason for no route, low fuel, too-close hyperspace, no nearby port, fast approach, or missing refuel service before changing destinations. TV scaffold; Classic wording pending.',
            'Hyperspace distance recovery: if J reports you are not far enough away from the system center, keep your route selected, fly outward, then retry J before changing destination. Original-runtime-observed guardrail; exact Classic distance pending.',
            'Route clearing: Backspace/Delete clears queued green routes; choose a fresh linked stop before retrying J.',
            'Mission objective marker: active mission destinations are highlighted on the map.',
            'Mission route helper: G queues the active mission destination when known.',
            'Mission route recovery: if G replaces a stale route or J blocks for low fuel after queuing an active mission, keep the mission destination selected, land/refuel at a linked service port, then jump/deliver before buying more cargo. TV scaffold; Classic route UI pending.',
            'Mission/trade hybrid: accept cargo jobs first, then buy only commodity lots that fit remaining free hold; carry trade through delivery chains only when fuel, deadline, and hold margins stay safe.',
            'Strategy skill rotation recovery: after combining route planning, a courier job, and a safe trade lot, verify Mission Log/Player Info checkpoints before specializing the pilot further. TV strategy scaffold; Classic progression loop pending.',
            'Upgrade readiness recovery: before spending upgrade savings, scout service availability, buy capacity and defensive gear intentionally, then verify Player Info ship/outfit/weapon checkpoints after trading up. TV upgrade-readiness scaffold; Classic upgrade progression loop pending.',
            'Upgrade affordability recovery: if a target ship is one funding leg out of reach, preserve the blocked purchase goal, run a safe profitable trade loop, then return to the same shipyard and verify the new hull in Player Info. TV upgrade-affordability scaffold; Classic progression loop pending.',
            'Cargo expansion recovery: if a third trade lot is blocked by shuttle hold limits, preserve the profitable route, buy a Cargo Pod at the outfitter, then fill the expanded hold and verify the larger run in Player Info. TV cargo-expansion scaffold; Classic cargo pod progression loop pending.',
            'Fuel reserve upgrade recovery: if a route leaves no reserve margin, buy an Auxiliary Fuel Tank, refuel to the expanded reserve, then verify the return hop before taking tighter jobs. TV fuel-reserve scaffold; Classic fuel tank progression loop pending.',
            'Balanced upgrade recovery: if hull plating is blocked after cargo and fuel upgrades, run a safe funding trade leg, return to the outfitter, buy the final armor refit, and repair at the service port. TV balanced-upgrade scaffold; Classic refit budgeting loop pending.',
            'Hull plating repair recovery: after buying Hull Plating, verify Player Info max hull increased, then use F7 at a repair-service port to fill the added armor before taking riskier jobs. TV hull-plating scaffold; Classic armor refit UI pending.',
            'Mission route trade sale: after delivering a mission with preserved trade cargo, check the destination market and sell recoverable cargo before leaving the route. TV scaffold; Classic behavior pending.',
            'First mission delivery recovery: after accepting the intro courier, keep the route/mission log aligned through Sol to Luna, land before completing, and verify cargo/reward/history before taking the chain offer. TV scaffold; exact Classic first-job UI pending.',
            'Mission scan failure recovery: scan-sensitive cargo missions can fail when the matching government scans you; watch Mission Log/Player Info failure history, free released cargo, and seek follow-up contracts. Resource Bible-backed scaffold; exact Classic scan UI pending.',
            'Mission scan follow-up recovery: after a scan-sensitive dispatch fails, preserve the failure history, accept only a safe follow-up contract, complete it, then verify failed and completed Mission Log/Player Info history before reusing the route. TV scan-recovery scaffold; Classic reoffer UI pending.',
            'Mission deadline follow-up recovery: after a timed mission fails and releases cargo, use Mission Computer to accept a safe recovery follow-up, then verify Mission Log/Player Info failed and completed history before reusing the route. TV deadline-recovery scaffold; exact Classic reoffer UI pending.',
            'Mission legal eligibility recovery: if Mission Computer hides or blocks a contract for legal standing, check the visible requirement reason, repair legal score or route to a qualifying government, then re-scan offers. Resource Bible-backed scaffold; exact Classic offer UI pending.',
            'Mission story-gate recovery: if a chain offer is locked or excluded, read the Mission Computer reason for missing story flags or active exclusions before hauling more cargo. TV scaffold; exact Classic offer visibility pending.',
            'Mission abort penalty recovery: aborting some cargo missions can apply Resource Bible-backed reputation reversal; check Player Info abort history/legal standing, rebuild reputation, and re-scan Mission Computer gates before retrying. Exact Classic abort UI pending.',
            'Mission auto-abort recovery: some Resource Bible-backed auto-abort probes remove themselves immediately after acceptance and may set completion flags; check Mission Log/Player Info history before assuming cargo is still active. Exact Classic auto-abort UI pending.',
            'Sequential deadline recovery: if multiple timed missions expire together, Mission Log/Player Info failure history should show each released-cargo job and reputation penalty before you re-plan cargo or follow-up contracts. Resource Bible-backed scaffold; exact Classic multi-failure UI pending.',
            'Timed abort recovery: aborting a timed TV mission before expiry should release its reserved cargo and prevent late failure flags or reputation penalties; verify Mission Log/Player Info before accepting follow-ups. Classic abort/deadline UI pending.',
            'Last-day delivery recovery: timed TV missions can still deliver on the current scaffold deadline day; verify Mission Log/Player Info shows reward paid, cargo released, and no failure flag before waiting longer. Classic date inclusivity/UI pending.',
            'Completed deadline recovery: after delivering a timed TV mission, waiting past the former deadline should not create a late failure; verify Mission Log/Player Info shows completed/rewarded and no failure flag before re-planning. Classic cleanup UI pending.',
            'Active deadline recovery: before waiting or rerouting, check Mission Log/Player Info days remaining and complete timed deliveries before the TV deadline scaffold expires. Exact Classic date UI pending.',
            'Mission return trade margin: before buying return-leg cargo after a delivery, compare destination and linked-market prices; skip negative-margin cargo and finish the contract chain. TV scaffold; Classic behavior pending.',
            'Trade margin choice recovery: before filling a hold for a return leg, compare per-ton margins across linked markets, carry only positive-margin cargo, and skip negative-margin candidates. TV scaffold; Classic market spread pending.',
            'Light Freighter bulk margin choice recovery: after upgrading cargo capacity, compare linked-market per-ton margins before filling all 150 tons, carry only positive-margin bulk cargo, and skip negative-margin candidates. TV scaffold; Classic Light Freighter market spread pending.',
            'Light Freighter bulk mission margin recovery: when a bulk delivery reserves most of the freighter, compare spare-hold trade margins before launch, carry only positive-margin cargo, deliver first, then sell retained cargo. TV scaffold; Classic Light Freighter bulk mission/trade UI pending.',
            'Full-hold trade route recovery: when a profitable cargo route fills the shuttle, keep a service-port refuel margin before the return jump and sell both lots before taking another cargo job. TV scaffold; Classic market spread pending.',
            'Light Freighter repair trade funding recovery: when a damaged freighter cannot afford full repair, use only positive-margin cargo runs to fund the service bill, then return to a repair port before taking higher-risk jobs. TV scaffold; Classic damaged freighter trade/repair UI pending.',
            'Light Freighter mission/trade capacity recovery: after upgrading to a Light Freighter, reserve bulk mission cargo first, fill only remaining hold with profitable trade cargo, deliver the job, then sell retained cargo before accepting another bulk contract. TV scaffold; Classic Light Freighter mission/trade UI pending.',
            'Light Freighter deadline/refuel delivery recovery: if a timed bulk delivery reaches its scaffold deadline day after a zero-fuel launch block, refuel first, deliver before waiting longer, then verify no late failure history appears. TV scaffold; Classic Light Freighter deadline/refuel UI pending.',
            'Light Freighter refuel margin recovery: after reserving a bulk delivery, fill only remaining hold with positive-margin cargo, preserve a service-port refuel plan, then deliver and sell retained cargo. TV scaffold; Classic Light Freighter/trade UI pending.',
            'Light Freighter repair mission margin recovery: when a damaged freighter carries a bulk delivery, reserve repair credits, fill only spare hold with positive-margin cargo, deliver, sell retained cargo, then return to a repair port before taking another risky job. TV scaffold; Classic damaged freighter mission/trade/repair UI pending.',
            'Light Freighter repair/refuel margin recovery: when a damaged, low-fuel freighter carries a bulk delivery, reserve repair credits, buy only positive-margin spare cargo, deliver and sell at Levo, refuel before the empty return, then repair at Earth. TV scaffold; Classic damaged freighter fuel/repair UI pending.',
            'Light Freighter deadline repair/refuel margin recovery: on the final allowed day, deliver the timed bulk job before waiting or returning for repairs, then sell retained cargo, refuel at the service port, and repair at Earth. TV scaffold; Classic deadline/damaged freighter UI pending.',
            'Alignment return contracts: after choosing a chapter branch, scan Mission Computer for remaining non-branch return contracts before assuming the story chain is complete. TV timing scaffold pending Classic UI evidence.',
            'Alignment return completion recovery: after finishing either chapter branch, re-scan Mission Computer for leftover return contracts, accept only after free cargo is confirmed, complete the cleanup haul, and verify Mission Log/Player Info cargo release before treating the branch hub as cleared. TV mission scaffold; Classic branch cleanup UI pending.',
            'Repair credit recovery: if F7 reports insufficient credits, keep the damage state stable, run a safe funding leg until the quoted repair bill is covered, then return to the repair-service port before taking another risky job. TV scaffold; Classic repair credit UI pending.',
            'Movement tuning: arrows/WASD use the current Terminal Velocity inertial flight scaffold; coast, turn, and thrust deliberately drift, while exact EV Classic acceleration/facing frame order remains pending runtime comparison.',
            'Afterburner: Z gives a Terminal Velocity thrust boost and drains fuel; if it is blocked, refuel at a landed service port before retrying. Exact Classic curve pending.',
            'Afterburner fuel recovery: if Z is blocked for empty fuel, land at a service port and refuel with F5 before retrying; TV scaffold, exact Classic fuel thresholds pending.',
            'Afterburner launch recovery: if Z is blocked while landed, launch first with L, then boost only after clearing port; TV scaffold, exact Classic landed afterburner behavior pending.',
            'Afterburner disabled recovery: if Z is blocked because the player ship is disabled, use F8 recovery before retrying afterburner; TV scaffold, exact Classic death/afterburner behavior pending.',
            'Autopilot launch recovery: if A is blocked while landed, launch first with L before retrying the port-assist scaffold; exact Classic landed autopilot behavior pending.',
            'Autopilot no-port recovery: if A disengages with no port in the current system, pick a linked system with landable services on the map before retrying; TV scaffold, exact Classic target selection pending.',
            'Autopilot disabled recovery: if A blocks or disengages because the player ship is disabled, use F8 recovery before retrying autopilot; TV scaffold, exact Classic death/autopilot behavior pending.',
            'Combat: Tab fires primary; Space fires selected secondary; S cycles secondary; N/R target contacts; disabled contacts can drop TV-scaffold cargo salvage; exact Classic cadence/effects/loot still pending.',
            'Combat cadence recovery: immediate fire attempts can be blocked by source-mined reload timing; wait for the HUD message/cooldown before treating weapons as broken. Classic timing pending.',
            'NPC retaliation recovery: hostile contacts can fire back under source-mined reload cadence; watch Player Info shields/hull, break off to repair, and use F8 only if disabled. Classic AI cadence pending.',
            'Projectile motion: fired weapons travel with source-mined Speed/Count/lifetime scaffolds; keep target selected and watch scanner damage before firing again. Exact Classic projectile timing pending.',
            'Explosion timing: disabled contacts show a short TV explosion scaffold before cleanup/reward; wait for scanner/HUD update before retargeting. Exact Classic explosion frames pending.',
            'Salvage recovery: if the hold is full when a green salvage marker appears, sell or deliver cargo, then return to the HUD/Player Info marker before leaving the system. TV scaffold; Classic loot behavior pending.',
            'Shield recharge recovery: after taking retaliation damage, break off and wait for the Player Info shield-recharge cadence before re-engaging; disabled hulls still need F8 recovery. Classic timing pending.',
            'Pirate avoidance: if an intercept warning appears, use map/route/refuel guidance to jump to a linked safe port before fighting; TV scaffold pending Classic trace.',
            'Pirate low-fuel recovery: if a pirate-avoidance jump is blocked for empty fuel, stay on the safe route, refuel at a service port, then escape before engaging. TV scaffold; exact Classic pirate/fuel behavior pending.',
            'Pirate cargo avoidance recovery: if a loaded mission/trade route gets an intercept warning, preserve reserved mission cargo and legal trade cargo, escape without combat, then deliver/sell before accepting more risk. TV scaffold; Classic pirate/cargo behavior pending.',
            'Disposable combat evidence gate: before any pirate/combat Classic-runtime trace, use a disposable non-Strict pilot, verify controls/save state, avoid reusable pilots, and stop if hull/shields are unsafe. TV guardrail; Classic combat evidence pending.',
            'Contraband recovery: if Player Info flags cargo as illegal for the current government, sell or reroute before landing scans, or budget clemency after confiscation. TV scaffold; exact Classic scan/bribe UI pending.',
            'Contraband trade recovery: after a scan removes illegal cargo from a mixed hold, check preserved legal cargo in Player Info, pay clemency only when needed, then sell the legal lot at a safe market. TV scaffold; Classic scan/cargo cleanup UI pending.',
            'Legal consequence recovery: after destroying a hostile patrol or other government target, check Player Info legal/reputation deltas, route to a safer port, and use clemency only when eligible. TV scaffold; exact Classic combat/legal resolution pending.',
            'Legal patrol posture recovery: if scanner or target status marks patrols hostile, legal standing is below the CrimeTol-style TV scaffold; route to a safer government or repair legal standing before fighting. Exact Classic patrol AI/UI pending.',
            'Legal clemency recovery: if C is blocked, verify you are landed, your government reputation meets the TV scaffold threshold, legal standing is low enough, and credits cover the clemency cost before retrying. Exact Classic bribe/clemency UI pending.',
            'Legal clemency credit recovery: if C reports insufficient funds, sell safe cargo or run a low-risk contract until the exact clemency cost is covered, then retry before provoking more scans. TV scaffold; Classic bribe/clemency UI pending.',
            'Legal service gates: poor standing can block outfitter/shipyard buying even at a landed port; improve legal standing or use an eligible port before retrying. Exact Classic refusal UI pending.',
            'Weapon credit recovery: if a landed weapon purchase is blocked for insufficient credits, run a safe trade/mission funding leg, return to the same service port, and retry only once the price is covered. TV scaffold; Classic purchase UI pending.',
            'Weapon availability recovery: if a weapon is not sold at the current landed port, keep the purchase goal but scout the service matrix for a port that lists it, then retry there. TV scaffold; Classic store inventory UI pending.',
            'Weapon legal-docking recovery: if legal standing blocks a weapon run before you can land, repair clemency or choose a safer port, then continue to the weapon-service station and verify the purchase. TV scaffold; Classic docking/refusal UI pending.',
            'Weapon mission cargo recovery: buying a landed weapon should preserve active mission-reserved cargo; verify Mission Log/Player Info cargo before rerouting or accepting more freight. TV scaffold; Classic weapon/cargo UI pending.',
            'Weapon trade cargo recovery: buying a landed weapon should preserve held trade cargo; verify Player Info/commodity hold before selling, rerouting, or taking more freight. TV scaffold; Classic weapon/cargo UI pending.',
            'Combat sound prefs: Set Prefs Sound Volume gates decoded combat sounds; if combat is silent, reopen Set Prefs before treating weapons as broken. Exact Classic volume behavior pending.',
            'Secondary weapon recovery: starting Shuttle shows No Secondary Weapon; install a secondary, press S to select it, then Space fires after the source-backed reload cadence.',
            'Weapon secondary activation: after buying a secondary weapon, press S until it is selected, verify Player Info/secondary HUD, then Space fires after reload. TV scaffold; Classic secondary install UI pending.',
            'Starting equipment uncertainty: original EV Classic HUD proves No Secondary Weapon, No Target, full shield/fuel, and Free: 20; check Player Info or an outfitter/status screen before treating primary weapons/outfits as exact Classic data.',
            'Target retarget recovery: if N/R reports no active scanner targets, all disabled/destroyed contacts are skipped; find live contacts or leave the route before retrying. TV scaffold; exact Classic retarget UI pending.',
            'Combat reward recovery: after a target is disabled, verify Player Info/HUD reward history and legal deltas before assuming a Classic bounty payout. TV scaffold; exact Classic bounty behavior pending.',
            'Blocked actions: when a jump, buy, land, fire, repair, or mission action fails, read the HUD Messages line before retrying; TV scaffold feedback, not Classic wording.',
            'Route clear/reselect recovery: after Backspace/Delete clears a multi-stop green route, J should stay blocked until you choose a fresh linked stop; then retry the new route instead of assuming the old path survived. TV route-clear scaffold; exact Classic clear/reselect UI pending.',
            'Route invalid stop recovery: if Shift-click refuses the current system, a duplicate stop, or an unlinked tail stop, keep the preserved green route and choose a linked stop from the current route tail before retrying J. TV route-guardrail scaffold; exact Classic map refusal UI pending.',
        ]:
            self.assertIn(expected_line, help_lines)
        for flag in [
            'hasAfterburnerHelp',
            'hasMovementTuningHelp',
            'hasAfterburnerFuelRecoveryHelp',
            'hasAfterburnerLaunchRecoveryHelp',
            'hasAfterburnerDisabledRecoveryHelp',
            'hasAutopilotHelp',
            'hasAutopilotLaunchRecoveryHelp',
            'hasAutopilotNoPortRecoveryHelp',
            'hasAutopilotDisabledRecoveryHelp',
            'hasRepairHelp',
            'hasRepairRecoveryHelp',
            'hasRepairCreditRecoveryHelp',
            'hasCombatHelp',
            'hasCombatCadenceHelp',
            'hasNpcRetaliationRecoveryHelp',
            'hasProjectileMotionHelp',
            'hasExplosionTimingHelp',
            'hasCombatSoundPrefsHelp',
            'hasStartingEquipmentUncertaintyHelp',
            'hasTargetDetailHelp',
            'hasTargetRetargetRecoveryHelp',
            'hasCombatRewardsHelp',
            'hasCombatRewardRecoveryHelp',
            'hasSalvageHelp',
            'hasSalvageRecoveryHelp',
            'hasShieldRechargeHelp',
            'hasShieldRechargeRecoveryHelp',
            'hasRecoveryHelp',
            'hasDisabledRecoveryHelp',
            'hasPirateAvoidanceHelp',
            'hasPirateLowFuelRecoveryHelp',
            'hasPirateCargoAvoidanceRecoveryHelp',
            'hasDisposableCombatEvidenceGateHelp',
            'hasContrabandHelp',
            'hasContrabandRecoveryHelp',
            'hasContrabandTradeRecoveryHelp',
            'hasLegalStatusHelp',
            'hasLegalClemencyHelp',
            'hasLegalConsequenceRecoveryHelp',
            'hasLegalPatrolPostureRecoveryHelp',
            'hasLegalClemencyRecoveryHelp',
            'hasLegalClemencyCreditRecoveryHelp',
            'hasLegalDockingHelp',
            'hasLegalServiceHelp',
            'hasWeaponReputationHelp',
            'hasWeaponCreditRecoveryHelp',
            'hasWeaponAvailabilityRecoveryHelp',
            'hasWeaponLegalDockingRecoveryHelp',
            'hasWeaponMissionCargoRecoveryHelp',
            'hasWeaponTradeCargoRecoveryHelp',
            'hasWeaponInventoryStackRecoveryHelp',
            'hasWeaponSecondaryActivationHelp',
            'hasAlignmentGateHelp',
            'hasAlignmentReturnHelp',
            'hasAlignmentReturnCompletionHelp',
            'hasMissionDeadlineHelp',
            'hasMissionDeadlineRecoveryHelp',
            'hasMissionAbortHistoryHelp',
            'hasCanAbortReturnHelp',
            'hasMissionOfferHelp',
            'hasMissionObjectiveHelp',
            'hasMissionRouteHelp',
            'hasMissionRouteRecoveryHelp',
            'hasMissionRouteTradeSaleHelp',
            'hasFirstMissionDeliveryRecoveryHelp',
            'hasMissionScanFailureRecoveryHelp',
            'hasMissionScanFollowupRecoveryHelp',
            'hasMissionDeadlineFollowupRecoveryHelp',
            'hasMissionLegalEligibilityRecoveryHelp',
            'hasMissionStoryGateRecoveryHelp',
            'hasMissionAbortPenaltyRecoveryHelp',
            'hasMissionAutoAbortRecoveryHelp',
            'hasMissionSequentialDeadlineRecoveryHelp',
            'hasMissionTimedAbortRecoveryHelp',
            'hasMissionLastDayDeliveryRecoveryHelp',
            'hasMissionCompletedNoLateFailureHelp',
            'hasActiveDeadlineRecoveryHelp',
            'hasMissionTradeReturnMarginHelp',
            'hasTradeMarginChoiceRecoveryHelp',
            'hasLightFreighterBulkMarginChoiceRecoveryHelp',
            'hasLightFreighterBulkMissionMarginRecoveryHelp',
            'hasFullHoldTradeRouteRecoveryHelp',
            'hasLightFreighterCapacityTradeRecoveryHelp',
            'hasLightFreighterRepairTradeFundingHelp',
            'hasLightFreighterMissionTradeCapacityHelp',
            'hasLightFreighterRefuelDeliveryRecoveryHelp',
            'hasLightFreighterDeadlineRefuelDeliveryRecoveryHelp',
            'hasLightFreighterRefuelMarginRecoveryHelp',
            'hasLightFreighterRefuelMissionMarginRecoveryHelp',
            'hasLightFreighterRepairMissionMarginRecoveryHelp',
            'hasLightFreighterRepairRefuelMarginRecoveryHelp',
            'hasLightFreighterDeadlineRepairRefuelMarginRecoveryHelp',
            'hasMissionTradeHybridHelp',
            'hasStrategySkillRotationRecoveryHelp',
            'hasUpgradeReadinessRecoveryHelp',
            'hasUpgradeAffordabilityRecoveryHelp',
            'hasCargoExpansionRecoveryHelp',
            'hasFuelReserveUpgradeRecoveryHelp',
            'hasBalancedUpgradeRecoveryHelp',
            'hasHullPlatingRepairRecoveryHelp',
            'hasCommodityRecoveryHelp',
            'hasTradeRouteHelp',
            'hasMapServiceHelp',
            'hasServiceProvisioningHelp',
            'hasRouteRefuelHelp',
            'hasRoutePlannerRefuelRecoveryHelp',
            'hasTravelTimingRecoveryHelp',
            'hasNavigationGuardrailRecoveryHelp',
            'hasNearCenterJumpRecoveryHelp',
            'hasShipyardDeltaHelp',
            'hasOutfitterGuardrailHelp',
            'hasShipyardCargoTransferHelp',
            'hasShipLadderHelp',
            'hasPilotPersistenceHelp',
            'hasPlayerInfoHelp',
            'hasRecentMessagesHelp',
            'hasBlockedActionHelp',
            'hasRouteClearHelp',
            'hasRouteClearReselectRecoveryHelp',
            'hasRouteInvalidStopRecoveryHelp',
        ]:
            self.assertIn(flag, help_probes)
        self.assertEqual(help_probes['hasPirateAvoidanceHint']['source'], 'curriculum')
        self.assertEqual(help_probes['hasAfterburnerHelp']['source'], 'help')
        self.assertIn('tv-gameplay-curriculum-help-log', run_script)
        self.assertIn('[switch]$GameplayCurriculumHelpLog', windows_script)

    def test_godot_starting_equipment_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_STARTING_EQUIPMENT_EVENT',
            '--tv-starting-equipment-log',
            'func _run_starting_equipment_log() -> void:',
            'startingSecondaryHudObserved=%s',
            'startingNoTargetObserved=%s',
            'startingFuelFullObserved=%s',
            'startingFreeCargoObserved=%s',
            'primaryInfoVisible=%s',
            'primarySourceStockName="%s"',
            'secondaryInfoVisible=%s',
            'sourceLabel=original-runtime-observed-starting-hud-plus-terminal-velocity-source-mined-primary',
            'oracleStatus=starting_primary_and_outfits_pending_nonmutating_classic_status_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-starting-equipment-log', run_script)
        self.assertIn('[switch]$StartingEquipmentLog', windows_script)

    def test_godot_service_provisioning_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_SERVICE_PROVISIONING_EVENT',
            '--tv-service-provisioning-log',
            'func _run_service_provisioning_log() -> void:',
            'levoNoOutfitterObserved=%s',
            'earthFullServiceScaffold=%s',
            'stardockNoShipyardScaffold=%s',
            'serviceMatrixScoutVisible=%s',
            'sourceLabel=original-runtime-observed-levo-plus-terminal-velocity-service-provisioning-scaffold',
            'oracleStatus=classic_runtime_service_matrix_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-service-provisioning-log', run_script)
        self.assertIn('[switch]$ServiceProvisioningLog', windows_script)

    def test_godot_pirate_avoidance_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_PIRATE_AVOIDANCE_EVENT',
            '--tv-pirate-avoidance-log',
            'func _run_pirate_avoidance_log() -> void:',
            'Pirate intercept detected; avoiding combat by routing to nearest safe linked port (TV scaffold)',
            'threat=pirate_intercept',
            'landedAtSafePort=%s',
            'lowFuelEscapeBlocked=%s',
            'refueledBeforeEscape=%s',
            'combatExecuted=%s',
            'evasionSucceeded=%s',
            'decision=jump_to_linked_safe_port',
            'sourceLabel=terminal-velocity-pirate-avoidance-scaffold',
            'oracleStatus=pirate_avoidance_pending_ev_classic_combat_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-pirate-avoidance-log', run_script)
        self.assertIn('[switch]$PirateAvoidanceLog', windows_script)

    def test_godot_primary_combat_is_playable_scaffold_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_COMBAT_EVENT',
            '--tv-combat-log',
            'func _run_combat_log',
            'var projectiles: Array[Dictionary] = []',
            'var explosion_events: Array[Dictionary] = []',
            'var combat_reward_history: Array[Dictionary] = []',
            'var primary_weapon_cooldown_frames := 0.0',
            'var target_shields: Dictionary = {}',
            'var target_hulls: Dictionary = {}',
            'func _primary_weapon_stats() -> Dictionary:',
            'func _spawn_primary_projectile() -> bool:',
            'func _advance_projectiles(delta: float) -> void:',
            'func _advance_weapon_cooldowns(delta: float) -> void:',
            'func _primary_weapon_reload_message() -> String:',
            'func _advance_explosion_events(delta: float) -> void:',
            'func _apply_projectile_hit(projectile: Dictionary, target_index: int) -> void:',
            'func _record_explosion_event(target_index: int) -> void:',
            'func _sound_binding_for_weapon(weapon_id: String) -> String:',
            'func _sound_binding_for_combat(binding_id: String) -> String:',
            'func _sound_history_contains(sound_id: String) -> bool:',
            'func _player_disabled_message() -> String:',
            'func _record_player_disabled_event() -> void:',
            'func _apply_player_projectile_hit(projectile: Dictionary) -> void:',
            'func _spawn_npc_retaliation_projectile(target_index: int) -> bool:',
            'func _weapon_shield_damage(weapon: Dictionary) -> int:',
            'func _weapon_hull_damage(weapon: Dictionary) -> int:',
            'combatExecuted=true',
            'projectileSpawned=%s',
            'retaliationFired=%s',
            'targetDamaged=%s',
            'playerDamaged=%s',
            'destroyScenarioPrepared=%s',
            'destroyProjectileSpawned=%s',
            'playerShieldBefore=%d',
            'playerHullAfter=%d',
            'targetDestroyed=%s',
            'combatRewardPaid=%s',
            'combatRewardAmount=%d',
            'combatRewardRecorded=%s',
            'combatRewardSaved=%s',
            'combatRewardResumeVisible=%s',
            'combatRewardInventoryVisible=%s',
            'combatRewardHudVisible=%s',
            'combatRewardLastTargetVisible=%s',
            'combatRewardStatusVisible=%s',
            'Contact %d disabled; reward +%d cr — TV scaffold, Classic bounty pending',
            'Last reward: Contact 1, 25 credits',
            'func _combat_reward_inventory_line() -> String:',
            'func _combat_reward_hud_fragment() -> String:',
            'Combat rewards: none',
            'targetLabel',
            'Combat rewards: %d disable(s), %d credits — TV combat-reward scaffold; Classic bounty behavior pending',
            '    Rewards: %d disable(s)/%d cr',
            'creditsBeforeDestroy=%d',
            'creditsAfterDestroy=%d',
            'explosionTriggered=%s',
            'explosionSourceLabel=%s',
            'TV_SOUND_EVENT',
            'primaryWeaponSound=%s',
            'primaryWeaponSoundPlayed=%s',
            'npcWeaponSound=%s',
            'npcWeaponSoundPlayed=%s',
            'explosionSound=%s',
            'explosionSoundPlayed=%s',
            'sourceLabel=decoded-resource-backed-sound-binding',
            'oracleStatus=classic_runtime_sound_timing_pending',
            'retargetedAfterDestroyed=%s',
            'destroyedTargetBlocked=%s',
            'retargetedTargetIndex=%d',
            'playerDisableRetaliationFired=%s',
            'playerDisabled=%s',
            'playerDisabledStatusVisible=%s',
            'playerDisabledExplosion=%s',
            'disabledFireBlocked=%s',
            'disabledSecondaryBlocked=%s',
            'disabledChangeSecondaryBlocked=%s',
            'disabledAutopilotGuidance=%s',
            'disabledHyperModeGuidance=%s',
            'disabledHyperSelectGuidance=%s',
            'disabledMovementBlocked=%s',
            'disabledSaveBlocked=%s',
            'disabledServiceRefuelBlocked=%s',
            'disabledServiceRepairBlocked=%s',
            'disabledServiceClemencyBlocked=%s',
            'disabledMissionAcceptBlocked=%s',
            'disabledTradeBuyBlocked=%s',
            'disabledTradeSellBlocked=%s',
            'disabledOutfitBuyBlocked=%s',
            'disabledShipBuyBlocked=%s',
            'func _disabled_player_action_blocked() -> bool:',
            'recoveryTriggered=%s',
            'playerRecovered=%s',
            'recoveryStatusVisible=%s',
            'disabledJumpGuidance=%s',
            'disabledLandGuidance=%s',
            'func _player_disabled() -> bool:',
            'Player ship disabled; Terminal Velocity reload/new-pilot recovery scaffold',
            'Player ship disabled; use F8 recovery before continuing actions',
            'func _recover_disabled_player_scaffold() -> bool:',
            'Recovered disabled player ship with F8; Terminal Velocity reload/new-pilot recovery scaffold',
            'func _fire_secondary_weapon() -> void:',
            'func _change_secondary_weapon() -> void:',
            'func _toggle_autopilot() -> void:',
            'terminal-velocity-player-disabled-scaffold',
            'classic_runtime_player_death_pending_strict_play_safe_trace',
            'Target already disabled; retargeting to next active contact',
            'func _select_next_live_target(start_index: int) -> bool:',
            'terminal-velocity-explosion-visual-scaffold',
            'classic_runtime_explosion_timing_pending',
            'func _award_combat_disable_reward(target_index: int) -> int:',
            'terminal-velocity-combat-reward-scaffold',
            'classic_runtime_combat_reward_behavior_pending',
            'sourceResourceId=%d',
            r'sourceStockName=\"%s\"',
            'sourceMassDmg=%d',
            'sourceEnergyDmg=%d',
            'sourceReload=%d',
            'Primary weapon reloading; wait for source-backed reload cadence',
            'sourceCount=%d',
            'appliedShieldDamage=%d',
            'appliedHullDamage=%d',
            'sourceAppliedFields=%s',
            'sourceLabel=terminal-velocity-source-mined-combat-scaffold',
            'EV Classic Resource Bible `wëap`: shields-up damage = MassDmg/4 + EnergyDmg',
            'EV Classic Resource Bible `shïp` Armor: armor takes damage once shields are down.',
            'oracleStatus=classic_runtime_weapon_timing_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('Combat: Tab fires primary; Space fires selected secondary; S cycles secondary; N/R target contacts', main_script)
        self.assertIn('Recovery: F8 resets a disabled player ship as a Terminal Velocity scaffold', main_script)
        self.assertIn('tv-combat-log', run_script)
        self.assertIn('[switch]$CombatLog', windows_script)

    def test_godot_combat_reward_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_COMBAT_REWARD_EVENT',
            '--tv-combat-reward-log',
            'func _run_combat_reward_log',
            'combatRewardPaid=%s',
            'combatRewardAmount=25',
            'combatRewardRecorded=%s',
            'combatRewardSaved=%s',
            'combatRewardResumeVisible=%s',
            'combatRewardInventoryVisible=%s',
            'combatRewardHudVisible=%s',
            'combatRewardStatusVisible=%s',
            'destroyedTargetBlocked=%s',
            'retargetedAfterDestroyed=%s',
            'sourceLabel=terminal-velocity-combat-reward-scaffold',
            'oracleStatus=classic_runtime_combat_reward_behavior_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-combat-reward-log', run_script)
        self.assertIn('[switch]$CombatRewardLog', windows_script)

    def test_godot_player_disabled_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_PLAYER_DISABLED_EVENT',
            '--tv-player-disabled-log',
            'func _run_player_disabled_log() -> void:',
            'playerDisabled=%s',
            'disabledStatusVisible=%s',
            'disabledExplosionVisible=%s',
            'disabledExplosionSound=%s',
            'disabledFireBlocked=%s',
            'disabledJumpBlocked=%s',
            'disabledMovementBlocked=%s',
            'disabledLaunchBlocked=%s',
            'recoveryTriggered=%s',
            'playerRecovered=%s',
            'recoveryStatusVisible=%s',
            'sourceLabel=terminal-velocity-player-disabled-scaffold',
            'oracleStatus=classic_runtime_player_death_pending_strict_play_safe_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-player-disabled-log', run_script)
        self.assertIn('[switch]$PlayerDisabledLog', windows_script)

    def test_godot_shield_recharge_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_SHIELD_RECHARGE_EVENT',
            '--tv-shield-recharge-log',
            'func _run_shield_recharge_log() -> void:',
            'player_shield_recharge_progress',
            'func _recharge_player_shields(delta: float) -> void:',
            'func _combat_readiness_inventory_line() -> String:',
            'Combat readiness: shields %d/%d; hull %d/%d (repair cost %d cr); shield recharge cadence source-backed scaffold',
            'shieldsAfterShortWait=%d',
            'shortWaitBlocked=%s',
            'shieldsAfterOneTick=%d',
            'firstTickRecharged=%s',
            'shieldsAfterMultiTick=%d',
            'multiTickRecharged=%s',
            'disabledRechargeBlocked=%s',
            'sourceRechargeFrames=%d',
            'combatReadinessVisible=%s',
            'sourceLabel=decoded-resource-backed-ship-shield-recharge-scaffold',
            'oracleStatus=classic_runtime_shield_recharge_timing_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-shield-recharge-log', run_script)
        self.assertIn('[switch]$ShieldRechargeLog', windows_script)

    def test_godot_projectile_motion_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_PROJECTILE_MOTION_EVENT',
            '--tv-projectile-motion-log',
            'func _run_projectile_motion_log() -> void:',
            'projectileMoved=%s',
            'projectileExpired=%s',
            'projectileHitTarget=%s',
            'initialProjectileSpeed=%d',
            'sourceSpeed=%d',
            'sourceLifetime=%d',
            'sourceCount=%d',
            'sourceLabel=terminal-velocity-projectile-motion-scaffold',
            'oracleStatus=classic_runtime_projectile_motion_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-projectile-motion-log', run_script)
        self.assertIn('[switch]$ProjectileMotionLog', windows_script)

    def test_godot_explosion_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_EXPLOSION_EVENT',
            '--tv-explosion-log',
            'func _run_explosion_log() -> void:',
            'explosionTriggered=%s',
            'explosionAnimated=%s',
            'explosionExpired=%s',
            'explosionSourceLabel=%s',
            'sourceLabel=terminal-velocity-explosion-visual-scaffold',
            'oracleStatus=classic_runtime_explosion_timing_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-explosion-log', run_script)
        self.assertIn('[switch]$ExplosionLog', windows_script)

    def test_godot_target_selection_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_TARGET_SELECTION_EVENT',
            '--tv-target-selection-log',
            'func _run_target_selection_log',
            'initialTarget=%d',
            'cycledTarget=%d',
            'closestTarget=%d',
            'cycledStatusHasTarget=true',
            'closestStatusHasClosest=true',
            'targetCount=%d',
            'destroyedTargetSkippedByCycle=%s',
            'destroyedTargetSkippedByClosest=%s',
            'liveTargetCount=%d',
            'func _target_shield_hull_summary(target_index: int) -> String:',
            'func _target_selectable(target_index: int) -> bool:',
            'S/H %d/%d',
            'cycledStatusHasStats=%s',
            'closestStatusHasStats=%s',
            'scannerTargetDetailVisible=%s',
            'noActiveScannerStatusVisible=%s',
            'func _scanner_target_detail_line() -> String:',
            'Scanner target: Contact %d — %s',
            'No active scanner targets',
            'sourceLabel=terminal-velocity-target-selection-scaffold',
            'oracleStatus=classic_runtime_target_selection_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-target-selection-log', run_script)
        self.assertIn('[switch]$TargetSelectionLog', windows_script)

    def test_godot_autopilot_assist_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_AUTOPILOT_EVENT',
            '--tv-autopilot-log',
            'func _run_autopilot_log',
            'var autopilot_enabled := false',
            'func _apply_autopilot_assist(delta: float) -> void:',
            'Autopilot engaged: steering toward nearest port as a Terminal Velocity assist scaffold',
            'Autopilot disengaged',
            'autopilotMovedCloser=%s',
            'autopilotSlowedForApproach=%s',
            'autopilotLandedBlocked=%s',
            'autopilotDisabledBlocked=%s',
            'autopilotDisabledDisengaged=%s',
            'autopilotNoPortDisengaged=%s',
            'Autopilot unavailable while landed; launch first',
            'Player ship disabled; use F8 recovery before continuing actions',
            'Autopilot disengaged: player ship disabled',
            'Autopilot disengaged: no port in current system',
            'sourceLabel=terminal-velocity-autopilot-assist-scaffold',
            'oracleStatus=classic_runtime_autopilot_behavior_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-autopilot-log', run_script)
        self.assertIn('[switch]$AutopilotLog', windows_script)

    def test_godot_secondary_weapon_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_SECONDARY_WEAPON_EVENT',
            '--tv-secondary-weapon-log',
            'func _run_secondary_weapon_log',
            'var secondary_weapon_cooldown_frames := 0.0',
            'var selected_secondary_weapon_index := 0',
            'func _installed_secondary_weapon_ids() -> Array[String]:',
            'func _secondary_weapon_stats() -> Dictionary:',
            'func _spawn_secondary_projectile() -> bool:',
            'func _secondary_weapon_reload_message() -> String:',
            'secondaryUnavailableAtStart=%s',
            'secondaryCycleSelected=%s',
            'secondaryProjectileSpawned=%s',
            'secondaryImmediateReloadBlocked=%s',
            'secondaryCooldownFrames=%d',
            'secondaryTargetDamaged=%s',
            'secondaryInventoryEmptyVisible=%s',
            'secondaryInventoryLoadedVisible=%s',
            'primaryWeaponPreserved=%s',
            'sourcePrimaryId=%s',
            'secondaryWeaponSound=%s',
            'secondaryWeaponSoundPlayed=%s',
            'secondaryHudVisible=%s',
            r'secondaryHudFragment=\"%s\"',
            'func _secondary_weapon_hud_fragment() -> String:',
            'Secondary: No Secondary Weapon',
            'Secondary: %s (%s)',
            'reload %d frames',
            'soundSourceLabel=decoded-resource-backed-sound-binding',
            'soundOracleStatus=classic_runtime_sound_timing_pending',
            'Secondary weapon: %s — selected; source %s; exact Classic secondary behavior pending',
            'Secondary weapon: No Secondary Weapon — original-runtime-observed starting HUD; install/cycle with S before Space fires',
            'Combat: Tab fires primary; Space fires selected secondary; S cycles secondary; N/R target contacts; disabled contacts can drop TV-scaffold cargo salvage; exact Classic cadence/effects/loot still pending.',
            'sourceLabel=terminal-velocity-secondary-weapon-scaffold',
            'oracleStatus=classic_runtime_secondary_weapon_behavior_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-secondary-weapon-log', run_script)
        self.assertIn('[switch]$SecondaryWeaponLog', windows_script)

    def test_godot_combat_guardrail_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_COMBAT_GUARDRAIL_EVENT',
            '--tv-combat-guardrail-log',
            'func _run_combat_guardrail_log',
            'firstShotSpawned=%s',
            'immediateSecondShotBlocked=%s',
            'cooldownFrames=%d',
            'cooldownCleared=%s',
            'shotAfterCooldownSpawned=%s',
            'secondaryBlocked=%s',
            'primaryWeaponSound=%s',
            'primaryWeaponSoundPlayCount=%d',
            'primaryWeaponSoundPlayedForValidShots=%s',
            'soundPreferenceMuted=%s',
            'mutedSoundEventCount=%d',
            'soundPreferenceSuppressesCombatSound=%s',
            'sourceLabel=terminal-velocity-source-mined-combat-guardrail-scaffold',
            'soundSourceLabel=decoded-resource-backed-sound-binding',
            'oracleStatus=classic_runtime_weapon_timing_pending',
            'soundOracleStatus=classic_runtime_sound_timing_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-combat-guardrail-log', run_script)
        self.assertIn('[switch]$CombatGuardrailLog', windows_script)

    def test_godot_retaliation_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_RETALIATION_EVENT',
            '--tv-retaliation-log',
            'var npc_retaliation_cooldowns: Dictionary = {}',
            'func _run_retaliation_log() -> void:',
            'func _npc_retaliation_reload_message() -> String:',
            'firstRetaliationFired=%s',
            'immediateSecondRetaliationBlocked=%s',
            'npcCooldownFrames=%d',
            'npcCooldownCleared=%s',
            'retaliationAfterCooldownFired=%s',
            'playerDamagedByRetaliation=%s',
            'sourceLabel=terminal-velocity-npc-retaliation-scaffold',
            'oracleStatus=classic_runtime_ai_retaliation_cadence_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-retaliation-log', run_script)
        self.assertIn('[switch]$RetaliationLog', windows_script)

    def test_godot_cargo_salvage_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_CARGO_SALVAGE_EVENT',
            '--tv-cargo-salvage-log',
            'func _run_cargo_salvage_log',
            'var cargo_salvage_pickups: Array[Dictionary] = []',
            'func _spawn_cargo_salvage_pickup(target_index: int, pickup_position: Vector2) -> Dictionary:',
            'func _advance_cargo_salvage_pickups() -> void:',
            'func _serialized_cargo_salvage_pickups() -> Array[Dictionary]:',
            'func _restore_cargo_salvage_pickups(saved_pickups: Variant) -> void:',
            '"cargo_salvage_pickups": _serialized_cargo_salvage_pickups(),',
            'Recovered %d tons of %s salvage (TV scaffold; Classic loot behavior pending)',
            'Cargo hold full; salvage remains in space',
            'salvageCreated=%s',
            'salvageScooped=%s',
            'fullHoldBlocked=%s',
            'salvageSaved=%s',
            'salvageResumeVisible=%s',
            'salvageInventoryVisible=%s',
            'salvageHudVisible=%s',
            'salvageScannerVisible=%s',
            'func _salvage_pickup_inventory_line() -> String:',
            'func _salvage_hud_fragment() -> String:',
            'func _salvage_scanner_blip_count() -> int:',
            'func _draw_scanner_salvage_blips(scanner_center: Vector2, scanner_radius: float) -> void:',
            'In-space salvage: none',
            'In-space salvage: %d pickup(s), %d tons — TV combat-salvage scaffold; Classic loot behavior pending',
            'Salvage: %d pickup(s)/%d tons',
            'sourceLabel=terminal-velocity-combat-salvage-scaffold',
            'oracleStatus=classic_runtime_loot_cargo_behavior_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-cargo-salvage-log', run_script)
        self.assertIn('[switch]$CargoSalvageLog', windows_script)

    def test_godot_combat_reward_salvage_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_COMBAT_REWARD_SALVAGE_EVENT',
            '--tv-combat-reward-salvage-log',
            'func _run_combat_reward_salvage_log() -> void:',
            'combatRewardPaid=%s',
            'combatRewardAmount=%d',
            'salvageCreatedBeforePickup=%s',
            'salvageScoopedAfterReward=%s',
            'rewardAndSalvageCoexisted=%s',
            'combatRewardInventoryVisible=%s',
            'salvageStatusVisible=%s',
            'salvageCommodity=equipment',
            'sourceLabel=terminal-velocity-combat-reward-salvage-scaffold',
            'rewardSourceLabel=terminal-velocity-combat-reward-scaffold',
            'salvageSourceLabel=terminal-velocity-combat-salvage-scaffold',
            'oracleStatus=classic_runtime_reward_loot_coupling_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-combat-reward-salvage-log', run_script)
        self.assertIn('[switch]$CombatRewardSalvageLog', windows_script)

    def test_godot_navigation_blocked_reasons_are_player_guidance_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()

        for symbol in [
            'TV_NAVIGATION_GUARDRAIL_EVENT',
            '--tv-navigation-guardrail-log',
            'func _run_navigation_guardrail_log',
            'No hyperspace route selected; open map (M) or queue mission route (G)',
            'Insufficient fuel for hyperspace; land at a port with refuel service or choose a closer route',
            'Can\'t initiate hyperspace jump - not yet far enough away from system center.',
            'No port in range; fly closer to a planet/station and slow below landing speed',
            'Approach slower/closer to land; landing needs close range and speed under 90',
            'Refuel unavailable here; choose a port with refuel service',
            'func _route_fuel_hint_line',
            'Route fuel: %d hop(s), cost %d, fuel %d/%d',
            'func _nearest_refuel_body_name',
            'warning += " at "',
            'preJumpFuelWarning=%s',
            'tooCloseGuidance=%s',
            'Route selected: %s — fuel cost %d, fuel %d/%d — press J to jump',
            'sourceLabel=terminal-velocity-navigation-guardrail-scaffold',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-navigation-guardrail-log', run_script)
        self.assertIn('[switch]$NavigationGuardrailLog', windows_script)

    def test_godot_legal_status_surface_is_scaffold_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        for symbol in [
            'var governments := {}',
            'var reputation := {}',
            'var reputation_scores: Dictionary = {}',
            'var legal_records: Dictionary = {}',
            'native_ev/data/governments.json',
            'native_ev/data/reputation.json',
            'TV_LEGAL_STATUS_EVENT',
            'TV_LEGAL_DOCKING_EVENT',
            'TV_LEGAL_SERVICE_GATE_EVENT',
            'TV_WEAPON_REPUTATION_GATE_EVENT',
            'TV_WEAPON_CREDIT_GATE_EVENT',
            'TV_WEAPON_AVAILABILITY_GATE_EVENT',
            'TV_WEAPON_INVENTORY_STACK_EVENT',
            'TV_WEAPON_SECONDARY_ACTIVATION_EVENT',
            'TV_WEAPON_MISSION_CARGO_EVENT',
            'TV_WEAPON_TRADE_CARGO_EVENT',
            'TV_WEAPON_LEGAL_DOCKING_EVENT',
            'TV_LIGHT_FREIGHTER_BULK_MARGIN_EVENT',
            'TV_LIGHT_FREIGHTER_BULK_MISSION_MARGIN_EVENT',
            'TV_LIGHT_FREIGHTER_REFUEL_MISSION_MARGIN_EVENT',
            'TV_LIGHT_FREIGHTER_MISSION_TRADE_EVENT',
            'TV_LIGHT_FREIGHTER_REPAIR_TRADE_EVENT',
            'TV_LIGHT_FREIGHTER_REPAIR_MISSION_TRADE_EVENT',
            'TV_LIGHT_FREIGHTER_REPAIR_REFUEL_MISSION_TRADE_EVENT',
            'TV_LIGHT_FREIGHTER_DEADLINE_REPAIR_REFUEL_EVENT',
            'TV_LEGAL_PATROL_POSTURE_EVENT',
            'TV_MISSION_LEGAL_ELIGIBILITY_EVENT',
            'TV_MISSION_STORY_GATE_EVENT',
            'TV_MISSION_ALIGNMENT_GATE_EVENT',
            'TV_CONTRABAND_CLEMENCY_FUNDING_EVENT',
            '--tv-legal-status-log',
            '--tv-mission-alignment-gate-log',
            '--tv-contraband-clemency-funding-log',
            '--tv-legal-docking-log',
            '--tv-legal-service-gate-log',
            '--tv-weapon-reputation-gate-log',
            '--tv-weapon-credit-gate-log',
            '--tv-weapon-availability-gate-log',
            '--tv-weapon-inventory-stack-log',
            '--tv-weapon-secondary-activation-log',
            '--tv-weapon-mission-cargo-log',
            '--tv-weapon-trade-cargo-log',
            '--tv-weapon-legal-docking-log',
            '--tv-light-freighter-bulk-margin-log',
            '--tv-light-freighter-bulk-mission-margin-log',
            '--tv-light-freighter-refuel-mission-margin-log',
            '--tv-light-freighter-mission-trade-log',
            '--tv-light-freighter-repair-trade-log',
            '--tv-light-freighter-repair-mission-trade-log',
            '--tv-light-freighter-repair-refuel-mission-trade-log',
            '--tv-light-freighter-deadline-repair-refuel-log',
            '--tv-legal-patrol-posture-log',
            '--tv-mission-legal-eligibility-log',
            '--tv-mission-story-gate-log',
            'func _run_legal_status_log',
            'func _run_legal_docking_log',
            'func _run_legal_service_gate_log',
            'func _run_weapon_reputation_gate_log',
            'func _run_weapon_credit_gate_log',
            'func _run_weapon_availability_gate_log',
            'func _run_weapon_inventory_stack_log',
            'func _run_weapon_secondary_activation_log',
            'func _run_weapon_mission_cargo_log',
            'func _run_weapon_trade_cargo_log',
            'func _run_weapon_legal_docking_log',
            'func _run_light_freighter_bulk_margin_log',
            'func _run_light_freighter_bulk_mission_margin_log',
            'func _run_light_freighter_refuel_mission_margin_log',
            'func _run_light_freighter_mission_trade_log',
            'func _run_light_freighter_repair_trade_log',
            'func _run_light_freighter_repair_mission_trade_log',
            'func _run_light_freighter_repair_refuel_mission_trade_log',
            'func _run_light_freighter_deadline_repair_refuel_log',
            'func _run_legal_patrol_posture_log',
            'func _run_mission_legal_eligibility_log',
            'func _run_mission_story_gate_log',
            'func _run_mission_alignment_gate_log',
            'func _run_contraband_clemency_funding_log',
            'func _current_government_name() -> String:',
            'func _legal_status_for_government(government_name: String) -> String:',
            'func _government_docking_allowed(government_name: String) -> bool:',
            'func _legal_docking_denied_message(government_name: String) -> String:',
            'func _government_name_for_system(system_name: String) -> String:',
            'func _legal_service_access_allowed(government_name: String) -> bool:',
            'func _service_access_allowed(service_name: String, government_name: String) -> bool:',
            'func _service_blocked_message(service_name: String, government_name: String) -> String:',
            'func _legal_service_blocked_message(government_name: String) -> String:',
            'func _legal_patrol_hostile_posture_active(government_name: String) -> bool:',
            'func _legal_patrol_warning_message(government_name: String) -> String:',
            'func _emit_legal_patrol_warning_if_needed() -> void:',
            'func _mission_requirements_met(mission: Dictionary) -> bool:',
            'func _blocked_mission_reasons(body: Dictionary) -> Array[String]:',
            'func _draw_blocked_mission_reasons(rect: Rect2, body: Dictionary, y_start: float) -> void:',
            'func _mission_requirement_block_reason(mission: Dictionary) -> String:',
            'func _map_legal_risk_line(system_name: String) -> String:',
            'func _map_legal_risk_color(system_name: String) -> Color:',
            'func _legal_warning_line(government_name: String) -> String:',
            'func _apply_reputation_event(event_id: String, context_government := "") -> void:',
            'func _pay_legal_clemency() -> bool:',
            'func _illegal_commodity_hold(government_name: String) -> Dictionary:',
            'func _apply_contraband_scan(accept_bribe := false) -> Dictionary:',
            'func _legal_patrol_attack_message(government_name: String) -> String:',
            'Government/legal: %s',
            'reputation_scores',
            'legal_records',
            'sourceBasis',
            'crimeToleranceLegalScore',
            'func _government_crime_tolerance_score(government_name: String) -> int:',
            'sourceLabel=terminal-velocity-classic-resource-legal-semantics',
            'oracleStatus=classic_runtime_thresholds_pending',
            'exact Classic thresholds unconfirmed',
            'sourceLabel=terminal-velocity-classic-resource-patrol-semantics',
            'oracleStatus=classic_runtime_combat_timing_pending',
            'combatExecuted=true',
            'projectileSpawned=%s',
            'targetDestroyed=%s',
            'explosionTriggered=%s',
            'sourceLabel=terminal-velocity-classic-resource-mission-availability',
            'oracleStatus=classic_runtime_ui_wording_pending',
            'visibleBlockedReason=%s',
            'blockedTitleVisible=%s',
            'blockedSourceVisible=%s',
            'blockedReasons=%s',
            'func _blocked_mission_source_boundary_line() -> String:',
            'Blocked-offer details are Terminal Velocity helper scaffolds; exact Classic hidden/disabled Mission Computer behavior pending original/resource evidence',
            'Unavailable contracts (TV scaffold):',
            'Legal: %s / %s (%d)',
            'Map service/legal summary: selected systems show Terminal Velocity station services and legal risk.',
            'sourceLabel=terminal-velocity-classic-resource-govt-penalty-semantics',
            'sourceEvent=destroy_patrol',
            'legalDeltaApplied=%d',
            'reputationDeltaApplied=%d',
            'pirateReputationDeltaApplied=%d',
            'sourceLabel=terminal-velocity-inferred-clemency-scaffold',
            'clemencyInsufficientCreditBlocked=%s',
            'clemencyRecoveredAfterCredits=%s',
            'Clemency costs %d credits; insufficient funds',
            'sourceLabel=terminal-velocity-classic-resource-smuggling-scan-semantics',
            'oracleStatus=classic_runtime_scan_frequency_and_fine_tuning_pending',
            'oracleStatus=approved_inference_pending_ev_classic_confirmation',
            'Legal status: Player Info shows current government/legal stance; hostile patrol fire worsens the TV scaffold and landed C buys clemency when eligible.',
            'legalDockingDenied=%s',
            'sourceLabel=terminal-velocity-legal-docking-scaffold',
            'weaponReputationBlocked=%s',
            'weaponBoughtAfterReputation=%s',
            'sourceLabel=terminal-velocity-contraband-clemency-funding-scaffold',
            'sourceLabel=terminal-velocity-mission-alignment-gate-scaffold',
            'alignmentRequirementBlocked=%s',
            'alignmentLegalBlocked=%s',
            'alignmentRecoveredAfterGates=%s',
            'oracleStatus=classic_runtime_alignment_offer_gate_ui_pending',
            'preservedFoodSoldForClemency=%s',
            'clemencyFundedAfterTrade=%s',
            'sourceLabel=terminal-velocity-weapon-reputation-gate-scaffold',
            'sourceLabel=terminal-velocity-weapon-credit-gate-scaffold',
            'sourceLabel=terminal-velocity-weapon-availability-gate-scaffold',
            'sourceLabel=terminal-velocity-weapon-inventory-stack-scaffold',
            'sourceLabel=terminal-velocity-weapon-secondary-activation-scaffold',
            'sourceLabel=terminal-velocity-weapon-mission-cargo-scaffold',
            'sourceLabel=terminal-velocity-weapon-trade-cargo-scaffold',
            'sourceLabel=terminal-velocity-weapon-legal-docking-scaffold',
            'oracleStatus=classic_runtime_weapon_purchase_credit_flow_pending',
            'oracleStatus=classic_runtime_weapon_service_availability_pending',
            'oracleStatus=classic_runtime_weapon_purchase_trade_cargo_interaction_pending',
            'weaponCreditBlocked=%s',
            'weaponBoughtAfterFunding=%s',
            'weaponAvailableAtUnavailableBody=%s',
            'weaponAvailabilityBlocked=%s',
            'weaponBoughtAfterRelocation=%s',
            'firstWeaponBuySucceeded=%s',
            'secondWeaponBuySucceeded=%s',
            'weaponStackCountAfterFirst=%d',
            'weaponStackCountAfterSecond=%d',
            'secondaryUnavailableBeforePurchase=%s',
            'secondaryBoughtBeforeActivation=%s',
            'secondaryCycleSelectedAfterPurchase=%s',
            'secondaryProjectileSpawnedAfterPurchase=%s',
            'activeMissionCargoBefore=%d',
            'activeMissionCargoAfter=%d',
            'cargoUsedAfterWeapon=%d',
            'missionCargoPreserved=%s',
            'tradeCargoBefore=%d',
            'tradeCargoAfter=%d',
            'tradeCargoPreserved=%s',
            'dockingDeniedBeforeClemency=%s',
            'clemencyPaid=%s',
            'landedAfterClemency=%s',
            'weaponBuySucceeded=%s',
            'oracleStatus=classic_runtime_weapon_purchase_after_docking_denial_pending',
            'clemencyOracleStatus=classic_runtime_clemency_location_pending',
            'sourceLabel=terminal-velocity-light-freighter-repair-margin-scaffold',
            'oracleStatus=light_freighter_repair_margin_pending_classic_runtime_trace',
            'sourceLabel=terminal-velocity-light-freighter-bulk-mission-margin-scaffold',
            'oracleStatus=light_freighter_bulk_mission_margin_pending_classic_runtime_trace',
            'sourceLabel=terminal-velocity-light-freighter-refuel-mission-margin-scaffold',
            'oracleStatus=light_freighter_refuel_mission_margin_pending_classic_runtime_trace',
            'positiveMarginLotsBought=%d',
            'missionDeliveredBeforeTradeSale=%s',
            'retainedTradeSoldAfterDelivery=%s',
            'blockedLoadedDeliveryForRefuel=%s',
            'refuelSucceeded=%s',
            'sourceLabel=terminal-velocity-light-freighter-repair-mission-margin-scaffold',
            'oracleStatus=light_freighter_repair_mission_margin_pending_classic_runtime_trace',
            'repairSourceLabel=terminal-velocity-repair-service-scaffold',
            'repairOracleStatus=repair_service_pending_ev_classic_runtime_trace',
            'damagedHull=%d',
            'repairedHull=%d',
            'repairFundedByTrade=%s',
            'missionCargoReserved=%s',
            'missionDeliveredBeforeRepair=%s',
            'repairFundedByMissionTrade=%s',
            'sourceLabel=terminal-velocity-light-freighter-deadline-repair-refuel-margin-scaffold',
            'oracleStatus=light_freighter_deadline_repair_refuel_margin_pending_classic_runtime_trace',
            'deliveredOnDeadlineDay=%s',
            'deadlineFailurePreventedBeforeRepair=%s',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-legal-status-log', run_script)
        self.assertIn('tv-legal-docking-log', run_script)
        self.assertIn('tv-legal-service-gate-log', run_script)
        self.assertIn('tv-weapon-reputation-gate-log', run_script)
        self.assertIn('tv-weapon-credit-gate-log', run_script)
        self.assertIn('tv-weapon-availability-gate-log', run_script)
        self.assertIn('tv-weapon-inventory-stack-log', run_script)
        self.assertIn('tv-weapon-secondary-activation-log', run_script)
        self.assertIn('tv-weapon-mission-cargo-log', run_script)
        self.assertIn('tv-weapon-trade-cargo-log', run_script)
        self.assertIn('tv-weapon-legal-docking-log', run_script)
        self.assertIn('tv-light-freighter-mission-trade-log', run_script)
        self.assertIn('tv-light-freighter-bulk-mission-margin-log', run_script)
        self.assertIn('tv-light-freighter-refuel-mission-margin-log', run_script)
        self.assertIn('tv-light-freighter-repair-trade-log', run_script)
        self.assertIn('tv-light-freighter-repair-mission-trade-log', run_script)
        self.assertIn('tv-light-freighter-repair-refuel-mission-trade-log', run_script)
        self.assertIn('tv-light-freighter-deadline-repair-refuel-log', run_script)
        self.assertIn('tv-legal-patrol-posture-log', run_script)
        self.assertIn('tv-mission-legal-eligibility-log', run_script)
        self.assertIn('tv-mission-alignment-gate-log', run_script)
        self.assertIn('tv-legal-consequence-log', run_script)
        self.assertIn('tv-legal-clemency-log', run_script)
        self.assertIn('tv-contraband-scan-log', run_script)
        self.assertIn('tv-contraband-risk-log', run_script)
        self.assertIn('tv-contraband-clemency-funding-log', run_script)
        self.assertIn('[switch]$LegalStatusLog', windows_script)
        self.assertIn('[switch]$LegalDockingLog', windows_script)
        self.assertIn('[switch]$LegalServiceGateLog', windows_script)
        self.assertIn('[switch]$WeaponReputationGateLog', windows_script)
        self.assertIn('[switch]$WeaponCreditGateLog', windows_script)
        self.assertIn('[switch]$WeaponAvailabilityGateLog', windows_script)
        self.assertIn('[switch]$WeaponInventoryStackLog', windows_script)
        self.assertIn('[switch]$WeaponSecondaryActivationLog', windows_script)
        self.assertIn('[switch]$WeaponMissionCargoLog', windows_script)
        self.assertIn('[switch]$WeaponTradeCargoLog', windows_script)
        self.assertIn('[switch]$WeaponLegalDockingLog', windows_script)
        self.assertIn('[switch]$LightFreighterMissionTradeLog', windows_script)
        self.assertIn('[switch]$LightFreighterBulkMissionMarginLog', windows_script)
        self.assertIn('[switch]$LightFreighterRefuelMissionMarginLog', windows_script)
        self.assertIn('[switch]$LightFreighterRepairTradeLog', windows_script)
        self.assertIn('[switch]$LightFreighterRepairMissionTradeLog', windows_script)
        self.assertIn('[switch]$LightFreighterRepairRefuelMissionTradeLog', windows_script)
        self.assertIn('[switch]$LightFreighterDeadlineRepairRefuelLog', windows_script)
        self.assertIn('[switch]$LegalPatrolPostureLog', windows_script)
        self.assertIn('[switch]$MissionLegalEligibilityLog', windows_script)
        self.assertIn('[switch]$MissionAlignmentGateLog', windows_script)
        self.assertIn('[switch]$LegalConsequenceLog', windows_script)
        self.assertIn('[switch]$LegalClemencyLog', windows_script)
        self.assertIn('[switch]$ContrabandScanLog', windows_script)
        self.assertIn('[switch]$ContrabandRiskLog', windows_script)
        self.assertIn('[switch]$ContrabandClemencyFundingLog', windows_script)

    def test_godot_contraband_risk_surface_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            'TV_CONTRABAND_RISK_EVENT',
            '--tv-contraband-risk-log',
            'func _run_contraband_risk_log',
            'func _commodity_legal_hint_line(commodity_id: String) -> String:',
            'func _commodity_is_contraband_for_government(commodity_id: String, government_name: String) -> bool:',
            'func _contraband_inventory_line() -> String:',
            'Contraband risk: %d ton(s) flagged by %s scans',
            'heldContrabandInventoryVisible=%s',
            'inventoryHint=\\"%s\\"',
            'Legal risk: %s is contraband under %s scans',
            'Legal risk: no current %s contraband flag',
            'finePerTon=%d',
            'bribeAllowed=%s',
            'sourceLabel=terminal-velocity-classic-resource-smuggling-risk-surface',
            'oracleStatus=classic_runtime_scan_frequency_and_ui_wording_pending',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_contraband_scan_trade_recovery_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        for symbol in [
            'TV_CONTRABAND_SCAN_TRADE_EVENT',
            '--tv-contraband-scan-trade-log',
            'func _run_contraband_scan_trade_log',
            'equipmentAfterScan=%d',
            'foodAfterScan=%d',
            'preservedLegalCargoAfterScan=%s',
            'preservedFoodSoldSafely=%s',
            'sourceLabel=terminal-velocity-contraband-trade-recovery-scaffold',
            'oracleStatus=classic_runtime_scan_trade_cargo_cleanup_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-contraband-scan-trade-log', run_script)
        self.assertIn('[switch]$ContrabandScanTradeLog', windows_script)

    def test_godot_contraband_clemency_funding_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'run_godot.sh').read_text()
        windows_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        for symbol in [
            'TV_CONTRABAND_CLEMENCY_FUNDING_EVENT',
            '--tv-contraband-clemency-funding-log',
            'func _run_contraband_clemency_funding_log',
            'scanLeftClemencyOneHundredCreditsShort=%s',
            'preservedFoodSoldForClemency=%s',
            'clemencyFundedAfterTrade=%s',
            'clemencySourceLabel=terminal-velocity-inferred-clemency-scaffold',
            'clemencyOracleStatus=approved_inference_pending_ev_classic_confirmation',
            'sourceLabel=terminal-velocity-contraband-clemency-funding-scaffold',
            'oracleStatus=classic_runtime_scan_trade_clemency_cleanup_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-contraband-clemency-funding-log', run_script)
        self.assertIn('[switch]$ContrabandClemencyFundingLog', windows_script)

    def test_godot_outfitter_shipyard_purchases_feed_recent_messages_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            '_set_status(_legal_service_blocked_message(government_name))',
            '_set_status("No outfitter stock")',
            '_set_status("Not enough credits")',
            '_set_status("Bought " + str(item.get("name", item_id)))',
            '_set_status("No ships for sale")',
            '_set_status("Ship manifest missing " + ship_id)',
            '_set_status("Bought ship: " + ship_id)',
        ]:
            self.assertIn(symbol, main_script)

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
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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

    def test_godot_afterburner_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        launcher = (root / 'run_godot.sh').read_text()
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        checklist = (root / 'docs' / 'checklists' / 'ev-classic-behavior-baseline-checklist.md').read_text()
        for symbol in [
            '--tv-afterburner-log',
            'func _run_afterburner_log',
            'TV_AFTERBURNER_EVENT',
            'AFTERBURNER_THRUST_MULTIPLIER',
            'AFTERBURNER_FUEL_PER_SECOND',
            'speedBoosted=%s',
            'fuelDrained=%s',
            'noFuelBlocked=%s',
            'landedBlocked=%s',
            'disabledBlocked=%s',
            'afterburnerKeyHudVisible=%s',
            'afterburnerBlockedGuidanceVisible=%s',
            'Z afterburner',
            'Afterburner unavailable: no fuel; land at a service port and press F5 to refuel',
            'Afterburner unavailable while landed; press L to launch first',
            'sourceLabel=terminal-velocity-afterburner-scaffold',
            'oracleStatus=classic_runtime_afterburner_fuel_curve_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('tv-afterburner-log', launcher)
        self.assertIn('[switch]$AfterburnerLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-afterburner-log', run_script)
        self.assertIn('Afterburner acceleration/fuel scaffold', checklist)

    def test_godot_map_route_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
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
            'Route selected: %s — fuel cost %d, fuel %d/%d — press J to jump',
            'Hold Shift and click a linked system',
            'No route from current system',
            'greenLine=true',
            'var selected_route: Array = []',
            'func _map_route_tail_system_name() -> String:',
            'func _append_map_route_at_position(click_position: Vector2) -> bool:',
            'routeHops=%d route=%s',
            'preJumpFuelWarning=%s',
            'Route appended: %s — fuel cost %d, fuel %d/%d',
            'draw_line(route_start_point, route_end_point, Color(0.15, 1.0, 0.28, 0.95), 3.0)',
            '--tv-route-invalid-log',
            'func _run_route_invalid_log',
            'routePreserved=%s',
            'sourceLabel=terminal-velocity-route-guardrail',
            'oracleStatus=route_invalid_click_edges_pending_ev_classic_trace',
            '--tv-route-clear-log',
            'func _run_route_clear_log',
            'TV_ROUTE_CLEAR_EVENT',
            'func _clear_selected_route() -> bool:',
            'Backspace/Delete clears queued route',
            'clearHandled=%s',
            'routeAfterClear=%s',
            'blockedJumpAfterClear=%s',
            'oracleStatus=route_clear_pending_ev_classic_trace',
            '--tv-route-clear-reselect-log',
            'func _run_route_clear_reselect_log',
            'TV_ROUTE_CLEAR_RESELECT_EVENT',
            'selectedBeforeReselect=%s',
            'selectedAfterReselect=%s',
            'jumpedAfterReselect=%s',
            'oracleStatus=route_clear_reselect_pending_ev_classic_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MapRouteLog', run_script)
        self.assertIn('[switch]$RouteInvalidLog', run_script)
        self.assertIn('[switch]$RouteClearLog', run_script)
        self.assertIn('[switch]$RouteClearReselectLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-map-route-log', run_script)
        self.assertIn('--headless --path $Project -- --tv-route-invalid-log', run_script)
        self.assertIn('--headless --path $Project -- --tv-route-clear-log', run_script)
        self.assertIn('--headless --path $Project -- --tv-route-clear-reselect-log', run_script)
        self.assertIn('Basilisk source-oracle lane', plan)
        self.assertIn('Godot fast-eval lane', plan)
        self.assertIn('Bridge gate', plan)

    def test_godot_route_jump_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-route-hint-log',
            'func _run_mission_route_hint_log',
            'TV_MISSION_ROUTE_HINT_EVENT',
            'func _route_to_active_mission_destination',
            'missionRouteQueued=true',
            'staleRouteReplaced=%s',
            'var route_selected := _select_map_route_to_system(destination_system)',
            'status_line = "Mission route queued to %s. %s"',
            'fuelBeforeRoute=%d',
            'routeFuelCost=%d',
            'preJumpFuelWarning=%s',
            'routeStatusHasFuelHint=%s',
            'lowFuelRouteWarningVisible=%s',
            'lowFuelJumpBlocked=%s',
            'landedForRefuel=%s',
            'refuelSucceeded=%s',
            'deliveredAfterRefuel=%s',
            'tradeBoughtBeforeRoute=%s',
            'tradeCargoPreservedAfterDelivery=%s',
            'tradeCargoSoldAfterDelivery=%s',
            'heldTradeCargoAfterDelivery=%d',
            'heldTradeCargoAfterSale=%d',
            'cargoUsedAfterDelivery=%d',
            'cargoUsedAfterSale=%d',
            'creditsAfterDelivery=%d',
            'creditsAfterTradeSale=%d',
            'missionTradeRouteSourceLabel=terminal-velocity-mission-trade-refuel-scaffold',
            'missionTradeRouteOracleStatus=mission_trade_refuel_pending_classic_runtime_trace',
            'completedMissions=%s',
            'Mission route queued to %s. %s',
            'Route fuel: %d hop(s), cost %d, fuel %d/%d%s',
            'warning += " at "',
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

    def test_godot_mission_abort_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-abort-log',
            'func _run_mission_abort_log',
            'TV_MISSION_ABORT_EVENT',
            'func _abort_active_mission',
            'var aborted_mission_history: Array = []',
            'missionAccepted=true',
            'missionAborted=true',
            'reservedCargoReleased=true',
            'noActiveAbortBlocked=%s',
            'noActiveAbortStatusVisible=%s',
            'repeatAbortBlocked=%s',
            'repeatAbortStatusVisible=%s',
            'No active mission to abort',
            'abortedHistoryCount=%d',
            'sourceLabel=terminal-velocity-mission-abort-scaffold',
            'oracleStatus=mission_abort_pending_classic_runtime_or_manual_trace',
            'KEY_X:',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionAbortLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-abort-log', run_script)
        self.assertIn('tv-mission-abort-log', wrapper)
        self.assertIn('Mission abort scenario contract', plan)
        self.assertIn('reserved cargo release', plan)

    def test_godot_mission_abort_reaccept_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-abort-reaccept-log',
            'func _run_mission_abort_reaccept_log',
            'TV_MISSION_ABORT_REACCEPT_EVENT',
            'firstMissionAccepted=true',
            'firstMissionAborted=true',
            'reservedCargoReleasedAfterAbort=true',
            'missionReofferVisibleAfterAbort=true',
            'missionReaccepted=true',
            'reservedCargoReclaimedAfterReaccept=true',
            'reacceptedMissionDelivered=true',
            'reservedCargoReleasedAfterDelivery=true',
            'rewardPaidAfterDelivery=true',
            'sourceLabel=terminal-velocity-mission-abort-reaccept-scaffold',
            'oracleStatus=mission_abort_reaccept_pending_classic_runtime_or_manual_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionAbortReacceptLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-abort-reaccept-log', run_script)
        self.assertIn('tv-mission-abort-reaccept-log', wrapper)
        self.assertIn('Mission abort/reaccept delivery scenario contract', plan)

    def test_godot_mission_abort_forbidden_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-abort-forbidden-log',
            'func _run_mission_abort_forbidden_log',
            'TV_MISSION_ABORT_FORBIDDEN_EVENT',
            'canAbort=false',
            'Mission cannot abort before return/cleanup',
            'blockedAbort=%s',
            'reservedCargoPreservedAfterBlockedAbort=true',
            'completedNonAbortableMission=true',
            'reservedCargoReleasedAfterCompletion=true',
            'rewardPaidAfterCompletion=true',
            'sourceLabel=ev-classic-resource-bible-backed-canabort-guardrail',
            'oracleStatus=classic_runtime_canabort_return_cleanup_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionAbortForbiddenLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-abort-forbidden-log', run_script)
        self.assertIn('tv-mission-abort-forbidden-log', wrapper)
        self.assertIn('Mission abort-forbidden return-cleanup scenario contract', plan)

    def test_godot_mission_abort_penalty_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-abort-penalty-log',
            'func _run_mission_abort_penalty_log',
            'TV_MISSION_ABORT_PENALTY_EVENT',
            'abortReputationMultiplier',
            'reputationDelta=%d',
            'expectedReputationDelta=%d',
            'reputationPenaltyApplied=true',
            'reputation_scores[completion_government]',
            'sourceLabel=ev-classic-resource-bible-backed-mission-abort-penalty-scaffold',
            'oracleStatus=classic_runtime_abort_penalty_ui_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionAbortPenaltyLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-abort-penalty-log', run_script)
        self.assertIn('tv-mission-abort-penalty-log', wrapper)
        self.assertIn('Mission abort reputation-penalty scenario contract', plan)

    def test_godot_mission_auto_abort_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-auto-abort-log',
            'func _run_mission_auto_abort_log',
            'TV_MISSION_AUTO_ABORT_EVENT',
            'autoAbort=true',
            'autoAbortedAfterAcceptance=true',
            'reservedCargoReleased=true',
            'completionFlagsApplied=true',
            'sourceLabel=ev-classic-resource-bible-backed-auto-abort-guardrail',
            'oracleStatus=classic_runtime_auto_abort_ui_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionAutoAbortLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-auto-abort-log', run_script)
        self.assertIn('tv-mission-auto-abort-log', wrapper)
        self.assertIn('Mission auto-abort completion-bit scenario contract', plan)

    def test_godot_mission_scan_failure_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-scan-failure-log',
            'func _run_mission_scan_failure_log',
            'TV_MISSION_SCAN_FAILURE_EVENT',
            'scanGovernment',
            'failIfScanned',
            'nonmatchingScanPreservedMission=true',
            'matchingScanFailedMission=true',
            'reservedCargoReleased=true',
            'failureFlagSet=true',
            'sourceLabel=ev-classic-resource-bible-backed-mission-scan-failure-scaffold',
            'oracleStatus=classic_runtime_scan_failure_ui_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionScanFailureLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-scan-failure-log', run_script)
        self.assertIn('tv-mission-scan-failure-log', wrapper)
        self.assertIn('Mission scan-failure scenario contract', plan)

    def test_godot_mission_deadline_failure_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        for symbol in [
            '--tv-mission-deadline-failure-log',
            'func _run_mission_deadline_failure_log',
            'TV_MISSION_DEADLINE_FAILURE_EVENT',
            'func _fail_mission_deadline',
            'var failed_mission_history: Array = []',
            'deadlineFailureRecorded=true',
            'reservedCargoReleased=true',
            'failureFlagSet=true',
            'reputationPenaltyApplied=true',
            'failedHistoryCount=%d',
            'sourceLabel=ev-classic-resource-bible-backed-mission-failure-scaffold',
            'oracleStatus=deadline_failure_runtime_ui_pending_classic_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionDeadlineFailureLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-deadline-failure-log', run_script)
        self.assertIn('tv-mission-deadline-failure-log', wrapper)

    def test_godot_mission_deadline_completed_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        for symbol in [
            '--tv-mission-deadline-completed-log',
            'func _run_mission_deadline_completed_log',
            'TV_MISSION_DEADLINE_COMPLETED_EVENT',
            'deadlineMissionCompleted=true',
            'lateFailurePrevented=true',
            'reservedCargoReleased=true',
            'rewardPreserved=true',
            'reputationPreserved=true',
            'failedHistoryCount=%d',
            'sourceLabel=terminal-velocity-mission-deadline-completed-no-late-failure-scaffold',
            'oracleStatus=deadline_completed_no_late_failure_pending_classic_runtime_or_manual_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionDeadlineCompletedLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-deadline-completed-log', run_script)
        self.assertIn('tv-mission-deadline-completed-log', wrapper)

    def test_godot_mission_deadline_recovery_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-deadline-recovery-log',
            'func _run_mission_deadline_recovery_log',
            'TV_MISSION_DEADLINE_RECOVERY_EVENT',
            'deadlineFailureRecorded=true',
            'followupAccepted=true',
            'followupDelivered=true',
            'failedHistoryPreserved=true',
            'reservedCargoReleased=true',
            'sourceLabel=terminal-velocity-mission-deadline-recovery-scaffold',
            'oracleStatus=deadline_failure_recovery_pending_classic_runtime_or_manual_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionDeadlineRecoveryLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-deadline-recovery-log', run_script)
        self.assertIn('tv-mission-deadline-recovery-log', wrapper)
        self.assertIn('Mission deadline recovery scenario contract', plan)

    def test_godot_mission_deadline_sequential_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-deadline-sequential-log',
            'func _run_mission_deadline_sequential_log',
            'TV_MISSION_DEADLINE_SEQUENTIAL_EVENT',
            'bothDeadlineFailuresRecorded=true',
            'reservedCargoReleased=true',
            'failureFlagsSet=true',
            'cumulativeReputationPenaltyApplied=true',
            'failedHistoryCount=%d',
            'sourceLabel=terminal-velocity-mission-deadline-sequential-failures-scaffold',
            'oracleStatus=deadline_sequential_failures_pending_classic_runtime_or_manual_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionDeadlineSequentialLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-deadline-sequential-log', run_script)
        self.assertIn('tv-mission-deadline-sequential-log', wrapper)
        self.assertIn('Mission deadline sequential-failures scenario contract', plan)

    def test_godot_mission_deadline_last_day_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-deadline-last-day-log',
            'func _run_mission_deadline_last_day_log',
            'TV_MISSION_DEADLINE_LAST_DAY_EVENT',
            'lastDayDeliveryCompleted=true',
            'deadlineFailurePrevented=true',
            'reservedCargoReleased=true',
            'rewardPaid=true',
            'reputationPreserved=true',
            'failedHistoryCount=%d',
            'sourceLabel=terminal-velocity-mission-deadline-last-day-scaffold',
            'oracleStatus=deadline_last_day_delivery_pending_classic_runtime_or_manual_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionDeadlineLastDayLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-deadline-last-day-log', run_script)
        self.assertIn('tv-mission-deadline-last-day-log', wrapper)
        self.assertIn('Mission deadline last-day delivery scenario contract', plan)

    def test_godot_mission_deadline_abort_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-deadline-abort-log',
            'func _run_mission_deadline_abort_log',
            'TV_MISSION_DEADLINE_ABORT_EVENT',
            'deadlineMissionAborted=true',
            'lateFailurePrevented=true',
            'reservedCargoReleased=true',
            'failureFlagPreserved=true',
            'reputationPreserved=true',
            'abortedHistoryCount=%d',
            'sourceLabel=terminal-velocity-mission-deadline-abort-scaffold',
            'oracleStatus=deadline_abort_pending_classic_runtime_or_manual_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionDeadlineAbortLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-deadline-abort-log', run_script)
        self.assertIn('tv-mission-deadline-abort-log', wrapper)
        self.assertIn('Mission deadline abort scenario contract', plan)

    def test_godot_mission_deadline_trade_carryover_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-deadline-trade-carryover-log',
            'func _run_mission_deadline_trade_carryover_log',
            'TV_MISSION_DEADLINE_TRADE_CARRYOVER_EVENT',
            'deadlineFailureRecorded=true',
            'missionCargoReleased=true',
            'tradeCargoPreserved=true',
            'tradeCargoSold=true',
            'failureFlagSet=true',
            'reputationPenaltyApplied=true',
            'sourceLabel=terminal-velocity-mission-deadline-trade-carryover-scaffold',
            'oracleStatus=deadline_failure_trade_carryover_pending_classic_runtime_or_manual_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionDeadlineTradeCarryoverLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-deadline-trade-carryover-log', run_script)
        self.assertIn('tv-mission-deadline-trade-carryover-log', wrapper)
        self.assertIn('Mission deadline trade-carryover scenario contract', plan)

    def test_godot_mission_trade_destination_sale_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-trade-destination-sale-log',
            'func _run_mission_trade_destination_sale_log',
            'TV_MISSION_TRADE_DESTINATION_SALE_EVENT',
            'missionAccepted=true',
            'tradeBoughtBeforeDelivery=true',
            'missionDelivered=true',
            'tradeCargoPreservedAfterDelivery=true',
            'tradeCargoSoldAtDestination=true',
            'cargoUsedAfterSale=0',
            'sourceLabel=terminal-velocity-mission-trade-destination-sale-scaffold',
            'oracleStatus=mission_trade_destination_sale_pending_classic_runtime_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionTradeDestinationSaleLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-trade-destination-sale-log', run_script)
        self.assertIn('tv-mission-trade-destination-sale-log', wrapper)
        self.assertIn('Mission trade destination-sale scenario contract', plan)

    def test_godot_chapter_one_trade_carryover_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-chapter-one-trade-carryover-log',
            'func _run_chapter_one_trade_carryover_log',
            'TV_CHAPTER_ONE_TRADE_CARRYOVER_EVENT',
            'introMissionDelivered=true',
            'secondMissionDelivered=true',
            'tradeCargoReservedAlongsideSecondMission=true',
            'tradeCargoPreservedThroughSecondDelivery=true',
            'tradeCargoSoldAtSiriusStation=true',
            'cargoUsedAfterSale=0',
            'sourceLabel=terminal-velocity-chapter-one-trade-carryover-scaffold',
            'oracleStatus=chapter_one_trade_carryover_pending_classic_runtime_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$ChapterOneTradeCarryoverLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-chapter-one-trade-carryover-log', run_script)
        self.assertIn('tv-chapter-one-trade-carryover-log', wrapper)
        self.assertIn('Chapter-one trade carryover scenario contract', plan)

    def test_godot_mission_trade_return_margin_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-trade-return-margin-log',
            'func _run_mission_trade_return_margin_log',
            'TV_MISSION_TRADE_RETURN_MARGIN_EVENT',
            'returnMissionAccepted=true',
            'negativeMarginSkipped=true',
            'candidateMarginPerTon=-10',
            'returnMissionDelivered=true',
            'returnCargoContaminationPrevented=true',
            'cargoUsedAfterReturnDelivery=0',
            'sourceLabel=terminal-velocity-mission-trade-return-margin-scaffold',
            'oracleStatus=chapter_one_return_trade_margin_pending_classic_runtime_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionTradeReturnMarginLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-trade-return-margin-log', run_script)
        self.assertIn('tv-mission-trade-return-margin-log', wrapper)
        self.assertIn('Mission trade return-margin scenario contract', plan)

    def test_godot_trade_margin_choice_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-trade-margin-choice-log',
            'func _run_trade_margin_choice_log',
            'TV_TRADE_MARGIN_CHOICE_EVENT',
            'profitableCommodity=food',
            'unprofitableCommodity=equipment',
            'profitableMarginPerTon=60',
            'negativeMarginPerTon=-10',
            'negativeMarginSkipped=true',
            'profitableTradeBought=true',
            'profitableTradeSold=true',
            'finalCargo=0',
            'sourceLabel=terminal-velocity-trade-margin-choice-scaffold',
            'oracleStatus=trade_margin_choice_pending_classic_runtime_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$TradeMarginChoiceLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-trade-margin-choice-log', run_script)
        self.assertIn('tv-trade-margin-choice-log', wrapper)
        self.assertIn('Trade margin choice scenario contract', plan)

    def test_godot_light_freighter_bulk_margin_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-light-freighter-bulk-margin-log',
            'func _run_light_freighter_bulk_margin_log',
            'TV_LIGHT_FREIGHTER_BULK_MARGIN_EVENT',
            'boughtLightFreighter=true',
            'startingCargoSpace=20',
            'upgradedCargoSpace=150',
            'profitableCommodity=food',
            'unprofitableCommodity=equipment',
            'profitableMarginPerTon=78',
            'negativeMarginPerTon=-210',
            'positiveMarginLotsBought=15',
            'positiveMarginTonsBought=150',
            'negativeMarginSkipped=true',
            'bulkCargoCleared=true',
            'finalCargo=0',
            'sourceLabel=terminal-velocity-light-freighter-bulk-margin-scaffold',
            'oracleStatus=light_freighter_bulk_margin_pending_classic_runtime_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$LightFreighterBulkMarginLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-light-freighter-bulk-margin-log', run_script)
        self.assertIn('tv-light-freighter-bulk-margin-log', wrapper)
        self.assertIn('Light Freighter bulk margin scenario contract', plan)

    def test_godot_mission_log_history_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        for symbol in [
            '--tv-mission-log-history-log',
            'func _run_mission_log_history_log',
            'TV_MISSION_LOG_HISTORY_EVENT',
            'func _mission_abort_history_lines',
            'func _mission_failure_history_lines',
            'No active missions.',
            'Completed mission history',
            'Aborted mission history',
            'Failed mission history',
            'completedHistoryVisible=%s',
            'abortedHistoryVisible=%s',
            'failedHistoryVisible=%s',
            'failedDeadlineVisible=%s',
            'failedSourceVisible=%s',
            'func _mission_history_player_info_lines',
            'Mission history: %d completed, %d aborted, %d failed — TV mission-history scaffold; Classic Player Info behavior pending',
            'Latest failed mission: %s%s; exact Classic failure/history UI pending',
            'playerInfoHistoryVisible=%s',
            'playerInfoFailureVisible=%s',
            'Deadline: accepted day %d, failed day %d, limit %d day(s)',
            'Failure source: %s; exact Classic UI pending',
            'sourceLabel=terminal-velocity-mission-log-history-scaffold',
            'oracleStatus=mission_history_ui_pending_classic_runtime_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionLogHistoryLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-log-history-log', run_script)
        self.assertIn('tv-mission-log-history-log', wrapper)

    def test_godot_active_mission_deadline_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()

        for symbol in [
            '--tv-active-mission-deadline-log',
            'func _run_active_mission_deadline_log',
            'TV_ACTIVE_MISSION_DEADLINE_EVENT',
            'var current_day := 0',
            'var mission_acceptance_days: Dictionary = {}',
            'func _mission_abort_hint_lines',
            'Abort: press X to abort; TV scaffold releases %d reserved cargo tons',
            'Abort source: terminal-velocity-mission-abort-scaffold; Classic CanAbort/UI pending',
            'func _mission_deadline_lines',
            'Deadline: accepted day %d, current day %d, limit %d day(s), %d day(s) remaining',
            'Deadline source: %s; exact Classic UI pending',
            'deadlineVisible=%s',
            'sourceVisible=%s',
            'abortHintVisible=%s',
            'abortSourceVisible=%s',
            'func _active_mission_player_info_lines',
            'Active mission: %s to %s/%s',
            'Active mission deadline: %d day(s) remaining; exact Classic Player Info behavior pending',
            'Active mission source: terminal-velocity-player-info-mission-scaffold; exact Classic Player Info behavior pending',
            'playerInfoMissionVisible=%s',
            'playerInfoDeadlineVisible=%s',
            'sourceLabel=terminal-velocity-active-deadline-display-scaffold',
            'oracleStatus=active_deadline_ui_pending_classic_runtime_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$ActiveMissionDeadlineLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-active-mission-deadline-log', run_script)
        self.assertIn('tv-active-mission-deadline-log', wrapper)
        self.assertIn('Active mission deadline display scenario contract', plan)
        self.assertIn('4 day(s) remaining', main_script)

    def test_godot_mission_chain_lock_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-chain-lock-log',
            'func _run_mission_chain_lock_log',
            'TV_MISSION_CHAIN_LOCK_EVENT',
            'func _mission_story_gate_block_reason(mission: Dictionary) -> String:',
            'func _mission_story_gate_state(mission: Dictionary) -> String:',
            'lockedStoryReasonVisible=%s',
            'requires missing story flag(s): %s; Terminal Velocity story-chain scaffold, exact Classic offer visibility pending',
            'excluded by active story flag(s): %s; Terminal Velocity choice/exclusion scaffold, exact Classic offer visibility pending',
            'sourceLabel=terminal-velocity-mission-story-gate-scaffold',
            'oracleStatus=classic_mission_offer_visibility_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionChainLockLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-chain-lock-log', run_script)
        self.assertIn('tv-mission-chain-lock-log', wrapper)
        self.assertIn('Mission chain lock scenario contract', plan)
        self.assertIn('lockedStoryReasonVisible=true', plan)

    def test_godot_outfitter_shipyard_progression_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        for symbol in [
            '--tv-outfitter-shipyard-log',
            'func _run_outfitter_shipyard_log',
            'TV_OUTFITTER_SHIPYARD_EVENT',
            'boughtCargoPod=true',
            'boughtLaser=true',
            'boughtLightFreighter=true',
            'cargoSpaceIncreased=true',
            'shipyardArtLoaded=true',
            'overfullShipyardBlocked=%s',
            'overfullCargoPreserved=%s',
            'overfullRecoveryBoughtSmallerShip=%s',
            'Cannot buy %s: cargo %d exceeds target capacity %d',
            'cargoGuardrailSourceLabel=terminal-velocity-shipyard-cargo-guardrail-scaffold',
            'cargoGuardrailOracleStatus=shipyard_cargo_transfer_pending_ev_classic_runtime_trace',
            'sourceLabel=terminal-velocity-outfitter-shipyard-scaffold',
            'oracleStatus=outfitter_shipyard_pending_ev_classic_purchase_trace',
            'func _outfit_source_summary',
            'Source: stock %s (wëap %d); TV values scaffold until runtime-tuned',
            'MassDmg %d',
            'EnergyDmg %d',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$OutfitterShipyardLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-outfitter-shipyard-log', run_script)
        self.assertIn('tv-outfitter-shipyard-log', wrapper)

    def test_godot_repair_service_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        for symbol in [
            '--tv-repair-service-log',
            'func _run_repair_service_log',
            'TV_REPAIR_SERVICE_EVENT',
            'func _repair_current_hull() -> bool:',
            'func _repair_cost() -> int:',
            'Repair: F7',
            'KEY_F7:',
            'Repaired hull at %s for %d credits',
            'repairAvailable=%s',
            'repaired=%s',
            'alreadyFullBlocked=%s',
            'insufficientBlocked=%s',
            'insufficientMessageVisible=%s',
            'inSpaceBlocked=%s',
            'inSpaceMessageVisible=%s',
            'Cannot repair in space; land at a port with repair service',
            'Not enough credits for repairs: need %d',
            'sourceLabel=terminal-velocity-repair-service-scaffold',
            'oracleStatus=repair_service_pending_ev_classic_runtime_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$RepairServiceLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-repair-service-log', run_script)
        self.assertIn('tv-repair-service-log', wrapper)

    def test_godot_pilot_save_resume_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        wrapper = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-pilot-save-resume-log',
            'func _run_pilot_save_resume_log',
            'TV_PILOT_SAVE_RESUME_EVENT',
            'KEY_F6: _save_current_pilot_file()',
            'func _save_current_pilot_file',
            '_save_new_pilot_file(loaded_pilot_name, loaded_ship_name)',
            '_load_selected_pilot_file()',
            'saveSucceeded=true',
            'resumeSucceeded=true',
            'systemRoundTrip=true',
            'fuelRoundTrip=true',
            'creditsRoundTrip=true',
            'missionRoundTrip=true',
            'strictPlayRoundTrip=true',
            'outfitRoundTrip=true',
            'weaponRoundTrip=true',
            'selectedSecondaryRoundTrip=true',
            '"selected_secondary_weapon_index": selected_secondary_weapon_index,',
            'selected_secondary_weapon_index = int(data.get("selected_secondary_weapon_index", selected_secondary_weapon_index))',
            'shipRoundTrip=true',
            'cargoSpaceRoundTrip=true',
            'statusRoundTrip=true',
            '_buy_selected_outfit_or_weapon()',
            '_buy_selected_ship()',
            'savedOutfits=%s resumedOutfits=%s',
            'savedStatusMessages=%s resumedStatusMessages=%s',
            'sourceLabel=terminal-velocity-save-scaffold',
            'oracleStatus=save_resume_pending_ev_classic_file_trace',
            'F6 saves current pilot',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$PilotSaveResumeLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-pilot-save-resume-log', run_script)
        self.assertIn('tv-pilot-save-resume-log', wrapper)
        self.assertIn('Pilot save/resume scenario contract', plan)
        self.assertIn('save → mutate → reopen pilot', plan)

    def test_godot_player_inventory_overlay_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            'var player_info_visible := false',
            'func _draw_player_info_overlay',
            'func _player_inventory_lines',
            'player_info_visible = not player_info_visible',
            'Terminal Velocity player info helper/scaffold',
            'Ship:',
            'Credits:',
            'Cargo:',
            'Fuel:',
            'Hull:',
            'repair cost',
            'Outfits:',
            'Weapons:',
            'Primary weapon: %s — source %s; exact Classic cadence pending',
            'Secondary weapon: No Secondary Weapon — original-runtime-observed starting HUD; install/cycle with S before Space fires',
            'Secondary weapon: %s — selected; source %s; exact Classic secondary behavior pending',
            'func _primary_weapon_inventory_line() -> String:',
            'func _secondary_weapon_inventory_line() -> String:',
            'P toggles player info',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_open_pilot_list_shows_resume_context_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            'func _open_pilot_row_text(entry: Dictionary) -> String:',
            'System: %s',
            'Credits: %d',
            'Strict Play: %s',
            'str(data.get("system", "?"))',
            'int(data.get("credits", 0))',
            'bool(data.get("strict_play", false))',
            'str(data.get("status_line", ""))',
            'Status: %s',
            'data.get("active_missions", [])',
            '_pilot_resume_mission_summary(entry)',
            'Mission: %s',
            '_open_pilot_row_text(entry)',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_map_service_summary_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            'func _system_service_summary(system_name: String) -> String:',
            'Services: %s',
            'refuel',
            'outfitter',
            'shipyard',
            'commodity',
            '_system_service_summary(selected_name)',
            '_map_legal_risk_line(selected_name)',
            'Map service/legal summary: selected systems show Terminal Velocity station services and legal risk.',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_map_mission_destination_marker_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            'func _active_mission_destination_systems() -> Array[String]:',
            'Mission destination:',
            'Mission objective marker: active mission destinations are highlighted on the map.',
            '_active_mission_destination_systems()',
            'is_mission_destination',
            'Color(1.0, 0.45, 0.22',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_mission_log_overlay_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            'var mission_log_visible := false',
            'func _draw_mission_log_overlay',
            'func _mission_log_detail_lines',
            'mission_log_visible = not mission_log_visible',
            'Terminal Velocity mission log helper/scaffold',
            'Status: Active',
            'Destination:',
            'Cargo reserved:',
            'Reward:',
            'I toggles mission log',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_mission_log_route_progress_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            'Progress:',
            'Route hint:',
            'Press G to queue route',
            'Ready to complete at current port',
            'Travel to destination system',
            'Land at destination body',
            'func _mission_progress_line',
            'func _mission_route_hint_line',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_mission_completion_history_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            'var completed_mission_history: Array = []',
            'func _mission_completion_history_lines',
            'Completed mission history',
            'Cargo released:',
            'Reward paid:',
            'completed_mission_history.append',
            '"completed_mission_history": completed_mission_history',
            'completed_mission_history = data.get("completed_mission_history", completed_mission_history)',
            '_mission_completion_record',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_mission_offer_scan_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
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
            'func _mission_offer_detail_lines',
            'selectedOfferDetailsVisible=%s',
            'Briefing: %s',
            'Offer route: %s / %s — %s',
            'Offer terms: %d cr reward, %d cargo tons reserved on accept',
            'Offer deadline: %s',
            'Offer requirements: %s',
            'func _mission_offer_requirements_line(mission: Dictionary) -> String:',
            'Offer story: starts=%s completes=%s next=%s choiceGroup=%s reputationEvent=%s',
            'func _mission_optional_field(mission: Dictionary, key: String) -> String:',
            'Offer detail source: terminal-velocity-mission-offer-helper; exact Classic Mission Computer detail UI pending',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=terminal_velocity_eval_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionOfferScanLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-offer-scan-log', run_script)
        self.assertIn('tv-mission-offer-scan-log', launcher)

    def test_godot_mission_chain_offer_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        launcher = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-chain-offer-log',
            'func _run_mission_chain_offer_log',
            'TV_MISSION_CHAIN_OFFER_EVENT',
            'firstMissionDelivered=%s',
            'chainOfferVisible=%s',
            'frontier_sample_hera_freeport',
            'selectedChainOfferDetailsVisible=%s',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=terminal_velocity_eval_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionChainOfferLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-chain-offer-log', run_script)
        self.assertIn('tv-mission-chain-offer-log', launcher)
        self.assertIn('Mission chain offer scenario contract', plan)
        self.assertIn('frontier_sample_hera_freeport', plan)

    def test_godot_mission_alignment_branch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        launcher = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-alignment-branch-log',
            'func _run_mission_alignment_branch_log',
            'TV_MISSION_ALIGNMENT_BRANCH_EVENT',
            'branchOffersVisible=%s',
            'federation_report_freeport',
            'freeport_pact_smugglers',
            'chapter_one_alignment',
            'federationBranchAccepted=%s',
            'freeportBranchHiddenAfterChoice=%s',
            'freeportBranchAccepted=%s',
            'federationBranchHiddenAfterChoice=%s',
            'offersAfterChoice=%s',
            'selectedBranchOfferDetailsVisible=%s',
            'selectedBranchOfferDetails=%s',
            'var choice_group := _mission_optional_field(mission, "choiceGroup")',
            'if choice_group != "none" and not branch_choice_groups.has(choice_group):',
            'var selected_branch_offer_details := _mission_offer_detail_lines(selected_branch_offer)',
            'choiceBoundary=terminal_velocity_choice_group_scaffold_exact_classic_branch_ui_pending',
            'reputation_event_id',
            '_apply_reputation_event(reputation_event_id',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=terminal_velocity_eval_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionAlignmentBranchLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-alignment-branch-log', run_script)
        self.assertIn('tv-mission-alignment-branch-log', launcher)
        self.assertIn('Mission alignment branch scenario contract', plan)
        self.assertIn('chapter_one_alignment', plan)

    def test_godot_mission_alignment_return_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        launcher = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-alignment-return-log',
            'func _run_mission_alignment_return_log',
            'TV_MISSION_ALIGNMENT_RETURN_EVENT',
            'offersBeforeBranch=%s',
            'returnContractVisibleWithBranches=%s',
            'offersAfterFederation=%s',
            'returnContractVisibleAfterCompletion=%s',
            'returnContractAcceptedAfterFederation=%s',
            'returnContractDeliveredAfterFederation=%s',
            'returnContractAcceptedAfterFreeport=%s',
            'returnContractDeliveredAfterFreeport=%s',
            'returnContractCargoReleased=%s',
            'returnContractRewardPaid=%s',
            'alignmentReturnHelpVisible=%s',
            'freeport_return_earth',
            'federation_report_freeport',
            'freeport_pact_smugglers',
            'returnBoundary=terminal_velocity_return_contract_timing_scaffold_exact_classic_offer_ui_pending',
            'sourceLabel=terminal-velocity-observed',
            'oracleStatus=terminal_velocity_eval_pending_original_trace',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionAlignmentReturnLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-alignment-return-log', run_script)
        self.assertIn('tv-mission-alignment-return-log', launcher)
        self.assertIn('Mission alignment return-contract scenario contract', plan)
        self.assertIn('freeport_return_earth', plan)

    def test_godot_mission_alignment_delivery_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        launcher = (root / 'run_godot.sh').read_text()
        plan = (root / 'docs' / 'research' / 'terminal-velocity-godot-autoresearch-loop.md').read_text()
        for symbol in [
            '--tv-mission-alignment-delivery-log',
            'func _run_mission_alignment_delivery_log',
            'TV_MISSION_ALIGNMENT_DELIVERY_EVENT',
            'federationBranchAccepted=%s',
            'federationBranchDelivered=%s',
            'freeportBranchAccepted=%s',
            'freeportBranchDelivered=%s',
            'federationCargoReleased=%s',
            'freeportCargoReleased=%s',
            'federationRewardPaid=%s',
            'freeportRewardPaid=%s',
            'federationBranchFlagsSet=%s',
            'freeportBranchFlagsSet=%s',
            'incompatibleBranchBlockedAfterDelivery=%s',
            'federation_report_freeport',
            'freeport_pact_smugglers',
            'alignment_federation',
            'alignment_freeport',
            'sourceLabel=terminal-velocity-mission-scaffold',
            'oracleStatus=mission_behavior_pending_classic_runtime_trace',
            'deliveryBoundary=terminal_velocity_alignment_delivery_scaffold_exact_classic_completion_ui_pending',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$MissionAlignmentDeliveryLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-mission-alignment-delivery-log', run_script)
        self.assertIn('tv-mission-alignment-delivery-log', launcher)
        self.assertIn('Mission alignment branch delivery scenario contract', plan)
        self.assertIn('alignment_federation', plan)

    def test_godot_first_mission_delivery_autoresearch_log_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
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
            'completionHistoryCount=%d latestCompletion=%s',
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
        main_script = _godot_contract_text(Path(__file__).resolve().parents[2])
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

    def test_sourced_ev_weapons_manifest_maps_stock_outfits_to_weapon_records(self):
        data = sourced_ev_weapons_manifest()
        self.assertEqual(data['method'], 'ev-classic-resource-bible-weapon-field-map-v1')
        self.assertEqual(data['sourceBasis'], 'EV Classic Resource Bible wëap/oütf field definitions plus local primitive BRGR structure decode')
        self.assertEqual(data['weaponFieldOrder'][:6], ['Reload', 'Count', 'MassDmg', 'EnergyDmg', 'Guidance', 'Speed'])
        self.assertEqual(len(data['weapons']), 42)
        by_id = {weapon['resourceId']: weapon for weapon in data['weapons']}
        laser = by_id[128]
        self.assertEqual(laser['displayName'], 'Laser Cannon')
        self.assertEqual(laser['semanticFields']['Reload']['wordIndex'], 0)
        self.assertEqual(laser['semanticFields']['MassDmg']['wordIndex'], 2)
        self.assertEqual(laser['semanticFields']['EnergyDmg']['wordIndex'], 3)
        self.assertEqual(laser['semanticFields']['Guidance']['wordIndex'], 4)
        self.assertEqual(laser['sourceDataOrdinal'], 0)
        self.assertEqual(laser['outfitLinks'][0]['semanticFields']['ModType']['value'], 1)
        self.assertEqual(laser['outfitLinks'][0]['semanticFields']['ModVal']['value'], 128)
        self.assertEqual(by_id[131]['displayName'], 'Torp. Launcher')
        self.assertEqual(by_id[131]['ammoOutfitLinks'][0]['outfitDisplayName'], 'Torpedo')
        self.assertIn('Fighter Bay', by_id[146]['outfitNames'])
        self.assertEqual(data['unresolvedOutfitWeaponLinks'][0]['outfitDisplayName'], 'Forklift')
        self.assertEqual(data['unresolvedOutfitWeaponLinks'][0]['modValWeaponResourceId'], 191)

    def test_sourced_ev_governments_manifest_maps_classic_resource_bible_fields(self):
        data = sourced_ev_governments_manifest()
        by_id = {entry['resourceId']: entry for entry in data['governments']}
        confed = by_id[128]['semanticFields']
        rebel = by_id[129]['semanticFields']
        pirate = by_id[130]['semanticFields']
        militia = by_id[133]['semanticFields']
        self.assertEqual(confed['crimeTolerance'], 50)
        self.assertEqual(confed['smugglingPenalty'], 3)
        self.assertEqual(confed['killPenalty'], 25)
        self.assertEqual(rebel['crimeTolerance'], 75)
        self.assertEqual(pirate['crimeTolerance'], -20)
        self.assertIn('xenophobicWarshipsAttackNonAllies', pirate['flagNames'])
        self.assertEqual(militia['smugglingPenalty'], 5)
        self.assertEqual(militia['killPenalty'], 20)
        self.assertIn('EV Classic Resource Bible gövt fields', by_id[128]['fieldSource'])
        self.assertEqual(confed['shootPenaltyRuntimeNote'], 'EV Classic Resource Bible says ShootPenalty is currently ignored')

    def test_sourced_ev_missions_manifest_maps_classic_resource_bible_fields(self):
        data = sourced_ev_missions_manifest()
        self.assertEqual(data['recordRun']['recordSize'], 1970)
        self.assertEqual(len(data['missions']), 116)
        first = data['missions'][0]
        self.assertEqual(first['resourceId'], 128)
        self.assertEqual(first['fieldSource'], 'EV Classic Resource Bible mïsn fields through Flags, lines 249-519 of extracted text')
        self.assertEqual(first['rawFields']['availStel'], 20002)
        self.assertEqual(first['semanticFields']['availability']['stellar'], {'kind': 'notGovernmentStellar', 'governmentIndex': 2})
        self.assertEqual(first['semanticFields']['availability']['missionBitClear'], {'kind': 'mustBeClear', 'bit': 0})
        self.assertEqual(first['semanticFields']['availability']['location'], 'missionComputer')
        self.assertEqual(first['semanticFields']['availability']['randomPercent'], 50)
        self.assertEqual(first['semanticFields']['cargo']['type'], {'kind': 'specificCargoType', 'cargoType': 6})
        self.assertEqual(first['semanticFields']['cargo']['quantity'], {'kind': 'fixedTons', 'tons': 0})
        self.assertEqual(first['semanticFields']['reward'], {'kind': 'credits', 'credits': 10000})
        self.assertEqual(first['semanticFields']['descriptions']['quickBrief'], {'kind': 'descResource', 'resourceId': 6000})
        self.assertEqual(first['semanticFields']['descriptions']['completionText'], {'kind': 'descResource', 'resourceId': 7000})
        self.assertEqual(first['semanticFields']['lifecycle']['timeLimit'], {'kind': 'none'})
        self.assertTrue(first['semanticFields']['lifecycle']['canAbort']['canAbort'])
        self.assertEqual(first['semanticFields']['lifecycle']['flags']['flagNames'], ['globalPenaltyWhenJettisoningMissionCargoIgnored', 'showGreenArrowOnMapInInitialBriefing'])
        self.assertTrue(any(mission['semanticFields']['reward']['kind'] == 'cleanLegalRecord' for mission in data['missions']))
        special_ship_mission = data['missions'][6]
        self.assertEqual(special_ship_mission['semanticFields']['specialShips']['count'], {'kind': 'count', 'count': 3})
        self.assertEqual(special_ship_mission['semanticFields']['specialShips']['system'], {'kind': 'initialSystem'})
        self.assertEqual(special_ship_mission['semanticFields']['specialShips']['dude'], {'kind': 'specificDude', 'dudeId': 142})
        self.assertEqual(special_ship_mission['semanticFields']['specialShips']['goal'], {'kind': 'board'})
        self.assertEqual(special_ship_mission['semanticFields']['completion']['government'], {'kind': 'governmentId', 'governmentId': 129, 'governmentIndex': 1})
        self.assertEqual(special_ship_mission['semanticFields']['completion']['reward'], 50)
        self.assertEqual(special_ship_mission['semanticFields']['completion']['failureRecordPenalty'], -25)
        self.assertEqual(special_ship_mission['semanticFields']['lifecycle']['flags']['flagNames'], ['removePrepaidOutfitOnFailureOrAbort'])
        nonabortable_ids = [
            mission['resourceId']
            for mission in data['missions']
            if not mission['semanticFields']['lifecycle']['canAbort']['canAbort']
        ]
        self.assertEqual(len(nonabortable_ids), 15)
        self.assertEqual(nonabortable_ids[:5], [161, 164, 165, 167, 168])
        self.assertEqual(sum(1 for mission in data['missions'] if mission['semanticFields']['lifecycle']['timeLimit']['kind'] == 'days'), 29)
        self.assertEqual(sum(1 for mission in data['missions'] if mission['semanticFields']['lifecycle']['flags']['flagNames']), 99)
        self.assertEqual(sum(1 for mission in data['missions'] if mission['semanticFields']['auxiliaryShips']['count']['kind'] != 'ignored'), 54)
        flag_names = [
            name
            for mission in data['missions']
            for name in mission['semanticFields']['lifecycle']['flags']['flagNames']
        ]
        self.assertEqual(flag_names.count('showGreenArrowOnMapInInitialBriefing'), 82)
        self.assertEqual(flag_names.count('applyFiveTimesCompletionRewardReversalOnAbort'), 13)

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
        laser = next(weapon for weapon in data['weapons'] if weapon['id'] == 'laser_cannon')
        for key in ['massDamage', 'energyDamage', 'reloadFrames', 'countFrames', 'guidanceMode', 'sourceBasis', 'decodedCandidateWeaponLikeRecord', 'sourceResourceId', 'sourceStockName', 'sourceStockWeaponFields']:
            self.assertIn(key, laser)
        self.assertEqual(laser['sourceResourceId'], 128)
        self.assertEqual(laser['sourceStockName'], 'Laser Cannon')
        self.assertEqual(laser['sourceStockWeaponFields']['Reload'], 146)
        self.assertEqual(laser['sourceStockWeaponFields']['MassDmg'], 100)
        self.assertEqual(laser['sourceStockWeaponFields']['EnergyDmg'], 7)
        self.assertEqual(laser['massDamage'], laser['sourceStockWeaponFields']['MassDmg'])
        self.assertEqual(laser['energyDamage'], laser['sourceStockWeaponFields']['EnergyDmg'])
        self.assertEqual(laser['reloadFrames'], laser['sourceStockWeaponFields']['Reload'])
        self.assertEqual(laser['cooldownTicks'], laser['sourceStockWeaponFields']['Reload'])
        self.assertEqual(laser['sourceAppliedFields'], ['MassDmg', 'EnergyDmg', 'Reload'])
        self.assertIn('projectile speed/lifetime/count semantics remain TV-tuned', laser['sourceApplicationBoundary'])
        self.assertEqual(laser['massDamage'] // 4 + laser['energyDamage'], 32)
        self.assertEqual(laser['massDamage'] + laser['energyDamage'] // 4, 101)
        pulse = next(weapon for weapon in data['weapons'] if weapon['id'] == 'pulse_cannon')
        self.assertEqual(pulse['sourceResourceId'], 129)
        self.assertEqual(pulse['sourceStockName'], 'Neutron Blaster')
        self.assertEqual(pulse['massDamage'], pulse['sourceStockWeaponFields']['MassDmg'])
        self.assertEqual(pulse['energyDamage'], pulse['sourceStockWeaponFields']['EnergyDmg'])
        self.assertEqual(pulse['reloadFrames'], pulse['sourceStockWeaponFields']['Reload'])
        self.assertIn('MassDmg', laser['sourceBasis'])
        self.assertEqual(laser['decodedCandidateWeaponLikeRecord']['sourceDataWeaponResourceId'], 128)

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
        self.assertEqual(outcome['legalDelta'], -3)

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
        self.assertEqual(legal['Federation'], 2)
        self.assertEqual(legal_status_for_score(data, legal['Federation']), 'Clean')
        legal = {'Federation': -20, 'Independent': 0}
        _reputation, legal = apply_reputation_event(data, reputation, legal, 'contraband_fine', government='Federation')
        self.assertEqual(legal['Federation'], -23)
        self.assertEqual(legal_status_for_score(data, legal['Federation']), 'Offender')

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
        self.assertIn('var active_profile := {}', main_script)
        self.assertIn('native_ev/data/profiles/classic.json', main_script)
        self.assertIn('_profile_manifest_path', main_script)
        self.assertIn('active_profile.get("startSystemName", START_SYSTEM_NAME)', main_script)
        self.assertIn('native_ev/data/universe.json', main_script)
        self.assertIn('native_ev/data/ships.json', main_script)
        self.assertIn('native_ev/data/sounds.json', main_script)
        self.assertIn('frame_%02d.png', main_script)
        self.assertIn('EV-style', main_script)

    def test_godot_self_test_loads_runtime_data_through_classic_profile(self):
        root = Path(__file__).resolve().parents[2]
        self_test_script = (root / 'godot_ev' / 'scripts' / 'self_test.gd').read_text()

        self.assertIn('native_ev/data/profiles/classic.json', self_test_script)
        self.assertIn('var manifests: Dictionary = profile.get("dataManifests", {})', self_test_script)
        self.assertIn('_profile_manifest_path(root, manifests, "universe", "native_ev/data/universe.json")', self_test_script)
        self.assertIn('_profile_manifest_path(root, manifests, "ships", "native_ev/data/ships.json")', self_test_script)
        self.assertIn('_profile_manifest_path(root, manifests, "sounds", "native_ev/data/sounds.json")', self_test_script)
        self.assertIn('_profile_manifest_path(root, manifests, "gameplayCurriculum", "native_ev/data/gameplay_curriculum.json")', self_test_script)
        self.assertIn('func _profile_manifest_path(root: String, manifests: Dictionary, key: String, fallback: String) -> String', self_test_script)

    def test_godot_landing_ui_exposes_core_ev_panels_from_file_backed_manifests(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
            'func _help_overlay_lines() -> Array[String]:',
            'help_overlay.get("lines", [])',
            'KEY_F10:',
            'Fuel: %d/%d',
            'KEY_F5:',
            'Refuel: F5 available',
            'F5 Refuel',
            '_set_status("Refueled at " + str(body.get("name", "port")))',
        ]:
            self.assertIn(prompt, main_script)
        help_overlay = json.loads((root / 'native_ev' / 'data' / 'help_overlay.json').read_text())
        help_lines = help_overlay['lines']
        for prompt in [
            'Terminal Velocity helper/scaffold — not an EV Classic fidelity claim.',
            'Mission route helper: G queues the active mission destination when known.',
            'Shipyard/outfitter: listings show local manifest deltas/effects before buying.',
        ]:
            self.assertIn(prompt, help_lines)

    def test_godot_commodity_trade_uses_ev_classic_ten_ton_lots(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        self.assertIn('const EV_CLASSIC_COMMODITY_LOT_SIZE := 10', main_script)
        self.assertIn('min(EV_CLASSIC_COMMODITY_LOT_SIZE, free_space, affordable_tons)', main_script)
        self.assertIn('price * tons', main_script)
        self.assertIn('Bought %d tons of %s', main_script)
        self.assertIn('Sold %d tons of %s', main_script)

    def test_godot_commodity_buy_sell_affordance_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        run_script = (root / 'godot_ev' / 'windows' / 'RunGodot.ps1').read_text()
        launcher = (root / 'run_godot.sh').read_text()
        for symbol in [
            'const COMMODITY_TRADE_EVENT_LOG_PREFIX := "TV_COMMODITY_TRADE_EVENT"',
            '--tv-commodity-trade-log',
            'func _run_commodity_trade_log() -> void:',
            'buySucceeded=true',
            'sellSucceeded=true',
            'roundTripVisible=true',
            'Buy B',
            'Sell S',
            'Sell Price:',
            'S sells selected cargo',
            'No sell price here',
            'func _commodity_sell_price(commodity_id: String) -> int:',
        ]:
            self.assertIn(symbol, main_script)
        self.assertIn('[switch]$CommodityTradeLog', run_script)
        self.assertIn('--headless --path $Project -- --tv-commodity-trade-log', run_script)
        self.assertIn('tv-commodity-trade-log', launcher)

    def test_godot_commodity_route_hint_contract(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
        for symbol in [
            'func _commodity_trade_hint_line(commodity_id: String) -> String:',
            'Best linked sell:',
            '%+d cr/ton',
            'No linked sell data',
            '_commodity_trade_hint_line(commodity_id)',
            'Trade route helper: linked-market profit hints are Terminal Velocity scaffold.',
        ]:
            self.assertIn(symbol, main_script)

    def test_godot_click_sound_is_wired_to_landing_actions(self):
        root = Path(__file__).resolve().parents[2]
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
        main_script = _godot_contract_text(root)
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
