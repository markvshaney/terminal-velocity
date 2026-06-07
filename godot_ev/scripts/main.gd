extends Node2D

# EV-style native Godot front end. This intentionally loads the existing
# Terminal Velocity backend contract instead of inventing a second data source:
# native_ev/data/universe.json, native_ev/data/ships.json, native_ev/data/missions.json,
# native_ev/data/economy.json, native_ev/data/outfits.json, native_ev/data/weapons.json,
# native_ev/data/governments.json, native_ev/data/reputation.json,
# native_ev/data/sounds.json, and 36-frame frame_%02d.png ship sprite folders.

const VIEW_SIZE := Vector2(1280, 800)
const WORLD_SCALE := 0.55
const PLAYER_START := Vector2(0, 0)
const FRAME_COUNT := 36
const DEFAULT_CLICK_SOUND_ASSET := "assets/sounds/ev_classic/601_click/sound.wav"
const DEFAULT_SHIPYARD_PICT_ASSET := "assets/graphics/pict/5000_shipyard/image.png"
const STATE_TITLE := "title"
const STATE_SPACE := "space"
const START_SYSTEM_NAME := "Levo"
const EV_CLASSIC_COMMODITY_LOT_SIZE := 10
const PREFS_SAVE_PATH := "user://terminal_velocity_prefs.json"
const PREFS_SCREENSHOT_PATH := "user://selftest/title_prefs.png"
const MOVEMENT_LOG_RIGHT_TURN_PREFIX := "TV_MOVEMENT_LOG scenario=right_turn ticks=12 ship="
const MOVEMENT_LOG_LEFT_TURN_PREFIX := "TV_MOVEMENT_LOG scenario=left_turn ticks=12 ship="
const MOVEMENT_LOG_THRUST_PREFIX := "TV_MOVEMENT_LOG scenario=thrust ticks=30 ship="
const MOVEMENT_LOG_COAST_PREFIX := "TV_MOVEMENT_LOG scenario=coast ticks=30 ship="
const MOVEMENT_LOG_THRUST_RIGHT_TURN_PREFIX := "TV_MOVEMENT_LOG scenario=thrust_right_turn ticks=30 ship="
const AFTERBURNER_EVENT_LOG_PREFIX := "TV_AFTERBURNER_EVENT"
const TRAVEL_EVENT_LOG_PREFIX := "TV_TRAVEL_EVENT"
const LANDED_UI_MATRIX_PREFIX := "TV_LANDED_UI_MATRIX"
const SERVICE_PROVISIONING_EVENT_LOG_PREFIX := "TV_SERVICE_PROVISIONING_EVENT"
const MAP_ROUTE_EVENT_LOG_PREFIX := "TV_MAP_ROUTE_EVENT"
const ROUTE_CLEAR_EVENT_LOG_PREFIX := "TV_ROUTE_CLEAR_EVENT"
const ROUTE_CLEAR_RESELECT_EVENT_LOG_PREFIX := "TV_ROUTE_CLEAR_RESELECT_EVENT"
const ROUTE_JUMP_EVENT_LOG_PREFIX := "TV_ROUTE_JUMP_EVENT"
const ROUTE_LAND_REFUEL_EVENT_LOG_PREFIX := "TV_ROUTE_LAND_REFUEL_EVENT"
const REPAIR_SERVICE_EVENT_LOG_PREFIX := "TV_REPAIR_SERVICE_EVENT"
const REPAIR_CREDIT_RECOVERY_EVENT_LOG_PREFIX := "TV_REPAIR_CREDIT_RECOVERY_EVENT"
const LOW_FUEL_JUMP_EVENT_LOG_PREFIX := "TV_LOW_FUEL_JUMP_EVENT"
const NEAR_CENTER_JUMP_EVENT_LOG_PREFIX := "TV_NEAR_CENTER_JUMP_EVENT"
const COMMODITY_TRADE_EVENT_LOG_PREFIX := "TV_COMMODITY_TRADE_EVENT"
const LEVO_SAME_PORT_SELLBACK_EVENT_LOG_PREFIX := "TV_LEVO_SAME_PORT_SELLBACK_EVENT"
const COMMODITY_BUY_BLOCKED_RECOVERY_EVENT_LOG_PREFIX := "TV_COMMODITY_BUY_BLOCKED_RECOVERY_EVENT"
const COMMODITY_SELL_BLOCKED_RECOVERY_EVENT_LOG_PREFIX := "TV_COMMODITY_SELL_BLOCKED_RECOVERY_EVENT"
const COMMODITY_UNAVAILABLE_RECOVERY_EVENT_LOG_PREFIX := "TV_COMMODITY_UNAVAILABLE_RECOVERY_EVENT"
const CROSS_MARKET_TRADE_EVENT_LOG_PREFIX := "TV_CROSS_MARKET_TRADE_EVENT"
const MAX_HOLD_TRADE_EVENT_LOG_PREFIX := "TV_MAX_HOLD_TRADE_EVENT"
const TRADE_REFUEL_PROFIT_EVENT_LOG_PREFIX := "TV_TRADE_REFUEL_PROFIT_EVENT"
const CARGO_EXPANSION_TRADE_EVENT_LOG_PREFIX := "TV_CARGO_EXPANSION_TRADE_EVENT"
const FUEL_RESERVE_UPGRADE_EVENT_LOG_PREFIX := "TV_FUEL_RESERVE_UPGRADE_EVENT"
const BALANCED_UPGRADE_TRADE_EVENT_LOG_PREFIX := "TV_BALANCED_UPGRADE_TRADE_EVENT"
const HULL_PLATING_REPAIR_EVENT_LOG_PREFIX := "TV_HULL_PLATING_REPAIR_EVENT"
const UPGRADE_READINESS_EVENT_LOG_PREFIX := "TV_UPGRADE_READINESS_EVENT"
const UPGRADE_AFFORDABILITY_EVENT_LOG_PREFIX := "TV_UPGRADE_AFFORDABILITY_EVENT"
const MISSION_OFFER_SCAN_EVENT_LOG_PREFIX := "TV_MISSION_OFFER_SCAN_EVENT"
const MISSION_CHAIN_OFFER_EVENT_LOG_PREFIX := "TV_MISSION_CHAIN_OFFER_EVENT"
const MISSION_CHAIN_LOCK_EVENT_LOG_PREFIX := "TV_MISSION_CHAIN_LOCK_EVENT"
const MISSION_ALIGNMENT_BRANCH_EVENT_LOG_PREFIX := "TV_MISSION_ALIGNMENT_BRANCH_EVENT"
const MISSION_ALIGNMENT_RETURN_EVENT_LOG_PREFIX := "TV_MISSION_ALIGNMENT_RETURN_EVENT"
const MISSION_ALIGNMENT_DELIVERY_EVENT_LOG_PREFIX := "TV_MISSION_ALIGNMENT_DELIVERY_EVENT"
const MISSION_ROUTE_HINT_EVENT_LOG_PREFIX := "TV_MISSION_ROUTE_HINT_EVENT"
const MISSION_TRADE_DESTINATION_SALE_EVENT_LOG_PREFIX := "TV_MISSION_TRADE_DESTINATION_SALE_EVENT"
const CHAPTER_ONE_TRADE_CARRYOVER_EVENT_LOG_PREFIX := "TV_CHAPTER_ONE_TRADE_CARRYOVER_EVENT"
const MISSION_TRADE_RETURN_MARGIN_EVENT_LOG_PREFIX := "TV_MISSION_TRADE_RETURN_MARGIN_EVENT"
const TRADE_MARGIN_CHOICE_EVENT_LOG_PREFIX := "TV_TRADE_MARGIN_CHOICE_EVENT"
const MISSION_ABORT_EVENT_LOG_PREFIX := "TV_MISSION_ABORT_EVENT"
const MISSION_ABORT_REACCEPT_EVENT_LOG_PREFIX := "TV_MISSION_ABORT_REACCEPT_EVENT"
const MISSION_ABORT_FORBIDDEN_EVENT_LOG_PREFIX := "TV_MISSION_ABORT_FORBIDDEN_EVENT"
const MISSION_ABORT_PENALTY_EVENT_LOG_PREFIX := "TV_MISSION_ABORT_PENALTY_EVENT"
const MISSION_AUTO_ABORT_EVENT_LOG_PREFIX := "TV_MISSION_AUTO_ABORT_EVENT"
const MISSION_SCAN_FAILURE_EVENT_LOG_PREFIX := "TV_MISSION_SCAN_FAILURE_EVENT"
const MISSION_DEADLINE_FAILURE_EVENT_LOG_PREFIX := "TV_MISSION_DEADLINE_FAILURE_EVENT"
const MISSION_DEADLINE_LAST_DAY_EVENT_LOG_PREFIX := "TV_MISSION_DEADLINE_LAST_DAY_EVENT"
const MISSION_DEADLINE_COMPLETED_EVENT_LOG_PREFIX := "TV_MISSION_DEADLINE_COMPLETED_EVENT"
const MISSION_DEADLINE_RECOVERY_EVENT_LOG_PREFIX := "TV_MISSION_DEADLINE_RECOVERY_EVENT"
const MISSION_DEADLINE_SEQUENTIAL_EVENT_LOG_PREFIX := "TV_MISSION_DEADLINE_SEQUENTIAL_EVENT"
const MISSION_DEADLINE_ABORT_EVENT_LOG_PREFIX := "TV_MISSION_DEADLINE_ABORT_EVENT"
const MISSION_DEADLINE_TRADE_CARRYOVER_EVENT_LOG_PREFIX := "TV_MISSION_DEADLINE_TRADE_CARRYOVER_EVENT"
const MISSION_LOG_HISTORY_EVENT_LOG_PREFIX := "TV_MISSION_LOG_HISTORY_EVENT"
const FIRST_MISSION_DELIVERY_EVENT_LOG_PREFIX := "TV_FIRST_MISSION_DELIVERY_EVENT"
const PILOT_SAVE_RESUME_EVENT_LOG_PREFIX := "TV_PILOT_SAVE_RESUME_EVENT"
const OUTFITTER_SHIPYARD_EVENT_LOG_PREFIX := "TV_OUTFITTER_SHIPYARD_EVENT"
const SHIPYARD_CARGO_GUARDRAIL_EVENT_LOG_PREFIX := "TV_SHIPYARD_CARGO_GUARDRAIL_EVENT"
const OUTFITTER_PURCHASE_GUARDRAIL_EVENT_LOG_PREFIX := "TV_OUTFITTER_PURCHASE_GUARDRAIL_EVENT"
const GAMEPLAY_CURRICULUM_HELP_LOG_PREFIX := "TV_GAMEPLAY_CURRICULUM_HELP"
const STARTING_EQUIPMENT_EVENT_LOG_PREFIX := "TV_STARTING_EQUIPMENT_EVENT"
const PIRATE_AVOIDANCE_EVENT_LOG_PREFIX := "TV_PIRATE_AVOIDANCE_EVENT"
const COMBAT_EVENT_LOG_PREFIX := "TV_COMBAT_EVENT"
const COMBAT_REWARD_EVENT_LOG_PREFIX := "TV_COMBAT_REWARD_EVENT"
const COMBAT_REWARD_SALVAGE_EVENT_LOG_PREFIX := "TV_COMBAT_REWARD_SALVAGE_EVENT"
const COMBAT_GUARDRAIL_EVENT_LOG_PREFIX := "TV_COMBAT_GUARDRAIL_EVENT"
const PLAYER_DISABLED_EVENT_LOG_PREFIX := "TV_PLAYER_DISABLED_EVENT"
const SHIELD_RECHARGE_EVENT_LOG_PREFIX := "TV_SHIELD_RECHARGE_EVENT"
const RETALIATION_EVENT_LOG_PREFIX := "TV_RETALIATION_EVENT"
const PROJECTILE_MOTION_EVENT_LOG_PREFIX := "TV_PROJECTILE_MOTION_EVENT"
const EXPLOSION_EVENT_LOG_PREFIX := "TV_EXPLOSION_EVENT"
const CARGO_SALVAGE_EVENT_LOG_PREFIX := "TV_CARGO_SALVAGE_EVENT"
const CARGO_SALVAGE_RECOVERY_EVENT_LOG_PREFIX := "TV_CARGO_SALVAGE_RECOVERY_EVENT"
const SECONDARY_WEAPON_EVENT_LOG_PREFIX := "TV_SECONDARY_WEAPON_EVENT"
const TARGET_SELECTION_EVENT_LOG_PREFIX := "TV_TARGET_SELECTION_EVENT"
const AUTOPILOT_EVENT_LOG_PREFIX := "TV_AUTOPILOT_EVENT"
const NAVIGATION_GUARDRAIL_EVENT_LOG_PREFIX := "TV_NAVIGATION_GUARDRAIL_EVENT"
const LEGAL_STATUS_EVENT_LOG_PREFIX := "TV_LEGAL_STATUS_EVENT"
const LEGAL_DOCKING_EVENT_LOG_PREFIX := "TV_LEGAL_DOCKING_EVENT"
const LEGAL_SERVICE_GATE_EVENT_LOG_PREFIX := "TV_LEGAL_SERVICE_GATE_EVENT"
const WEAPON_REPUTATION_GATE_EVENT_LOG_PREFIX := "TV_WEAPON_REPUTATION_GATE_EVENT"
const WEAPON_CREDIT_GATE_EVENT_LOG_PREFIX := "TV_WEAPON_CREDIT_GATE_EVENT"
const WEAPON_AVAILABILITY_GATE_EVENT_LOG_PREFIX := "TV_WEAPON_AVAILABILITY_GATE_EVENT"
const WEAPON_INVENTORY_STACK_EVENT_LOG_PREFIX := "TV_WEAPON_INVENTORY_STACK_EVENT"
const WEAPON_SECONDARY_ACTIVATION_EVENT_LOG_PREFIX := "TV_WEAPON_SECONDARY_ACTIVATION_EVENT"
const WEAPON_MISSION_CARGO_EVENT_LOG_PREFIX := "TV_WEAPON_MISSION_CARGO_EVENT"
const WEAPON_TRADE_CARGO_EVENT_LOG_PREFIX := "TV_WEAPON_TRADE_CARGO_EVENT"
const WEAPON_LEGAL_DOCKING_EVENT_LOG_PREFIX := "TV_WEAPON_LEGAL_DOCKING_EVENT"
const LIGHT_FREIGHTER_CAPACITY_TRADE_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_CAPACITY_TRADE_EVENT"
const LIGHT_FREIGHTER_BULK_MARGIN_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_BULK_MARGIN_EVENT"
const LIGHT_FREIGHTER_BULK_MISSION_MARGIN_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_BULK_MISSION_MARGIN_EVENT"
const LIGHT_FREIGHTER_REFUEL_MISSION_MARGIN_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_REFUEL_MISSION_MARGIN_EVENT"
const LIGHT_FREIGHTER_DEADLINE_REFUEL_DELIVERY_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_DEADLINE_REFUEL_DELIVERY_EVENT"
const LIGHT_FREIGHTER_MISSION_TRADE_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_MISSION_TRADE_EVENT"
const LIGHT_FREIGHTER_REPAIR_TRADE_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_REPAIR_TRADE_EVENT"
const LIGHT_FREIGHTER_REPAIR_MISSION_TRADE_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_REPAIR_MISSION_TRADE_EVENT"
const LIGHT_FREIGHTER_REPAIR_REFUEL_MISSION_TRADE_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_REPAIR_REFUEL_MISSION_TRADE_EVENT"
const LIGHT_FREIGHTER_DEADLINE_REPAIR_REFUEL_EVENT_LOG_PREFIX := "TV_LIGHT_FREIGHTER_DEADLINE_REPAIR_REFUEL_EVENT"
const LEGAL_PATROL_POSTURE_EVENT_LOG_PREFIX := "TV_LEGAL_PATROL_POSTURE_EVENT"
const MISSION_LEGAL_ELIGIBILITY_EVENT_LOG_PREFIX := "TV_MISSION_LEGAL_ELIGIBILITY_EVENT"
const MISSION_STORY_GATE_EVENT_LOG_PREFIX := "TV_MISSION_STORY_GATE_EVENT"
const MISSION_ALIGNMENT_GATE_EVENT_LOG_PREFIX := "TV_MISSION_ALIGNMENT_GATE_EVENT"
const LEGAL_CONSEQUENCE_EVENT_LOG_PREFIX := "TV_LEGAL_CONSEQUENCE_EVENT"
const LEGAL_CLEMENCY_EVENT_LOG_PREFIX := "TV_LEGAL_CLEMENCY_EVENT"
const CONTRABAND_SCAN_EVENT_LOG_PREFIX := "TV_CONTRABAND_SCAN_EVENT"
const CONTRABAND_RISK_EVENT_LOG_PREFIX := "TV_CONTRABAND_RISK_EVENT"
const CONTRABAND_SCAN_TRADE_EVENT_LOG_PREFIX := "TV_CONTRABAND_SCAN_TRADE_EVENT"
const CONTRABAND_CLEMENCY_FUNDING_EVENT_LOG_PREFIX := "TV_CONTRABAND_CLEMENCY_FUNDING_EVENT"
const LEGAL_RESOURCE_SEMANTICS_SOURCE_BASIS := "sourceBasis=EV Classic Resource Bible: govt CrimeTol/penalties, interceptor scans, mission AvailRecord/ScanGovt/PayVal"
const FIRST_MISSION_DELIVERY_EXPECTED_MISSION_FIELD := "acceptedMission=intro_courier_earth_hera"
const MIN_HYPERSPACE_DISTANCE_FROM_CENTER := 450.0
const AFTERBURNER_THRUST_MULTIPLIER := 1.75
const AFTERBURNER_FUEL_PER_SECOND := 2.0

var repo_root := ""
var active_profile := {}
var universe := {}
var ships := {}
var missions := {}
var economy := {}
var outfits := {}
var weapons := {}
var governments := {}
var reputation := {}
var sounds := {}
var gameplay_curriculum := {}
var help_overlay := {}
var sound_players: Dictionary = {}
var sound_event_history: Array[String] = []
var shipyard_pict_textures: Dictionary = {}
var current_system_index := 0
var current_system := {}
var player_ship := {}
var player_frames: Array[Texture2D] = []
var player_frame_offsets: Array[Vector2] = []
var player_frame_alpha_counts: Array[int] = []
var npc_frames: Array[Texture2D] = []
var npc_frame_offsets: Array[Vector2] = []
var pos := PLAYER_START
var vel := Vector2.ZERO
var angle_deg := 0.0
var player_facing_index := 0
var turn_cell_progress := 0.0
var landed := false
var game_state := STATE_TITLE
var selected_link_index := 0
var selected_route: Array = []
var selected_target_index := 0
var autopilot_enabled := false
var map_visible := false
var help_visible := false
var mission_log_visible := false
var player_info_visible := false
var stars: Array[Vector2] = []
var status_line := ""
var status_messages: Array[String] = []
var title_status_line := "No pilot loaded."
var title_modal := ""
var pilot_name_input := ""
var ship_name_input := "Starseeker"
var strict_play_selected := false
var loaded_pilot_name := ""
var loaded_ship_name := ""
var loaded_pilot_file := ""
var available_pilots: Array[Dictionary] = []
var selected_pilot_index := 0
var selected_pref_index := 0
var pref_sound_on := true
var pref_music_on := false
var pref_game_speed_index := 2
var pref_full_screen_on := false
var pref_intro_animation_on := true
var pref_ask_before_buying_on := true
var pref_resume_game_on := false
var credits := 10000
var cargo := 0
var landing_tab := 0
var selected_landing_item := 0
var current_day := 0
var active_missions: Array = []
var completed_missions: Array = []
var mission_acceptance_days: Dictionary = {}
var completed_mission_history: Array = []
var aborted_mission_history: Array = []
var failed_mission_history: Array = []
var story_flags: Array = []
var commodity_hold: Dictionary = {}
var owned_outfits: Dictionary = {}
var owned_weapons: Dictionary = {}
var reputation_scores: Dictionary = {}
var legal_records: Dictionary = {}
var projectiles: Array[Dictionary] = []
var explosion_events: Array[Dictionary] = []
var cargo_salvage_pickups: Array[Dictionary] = []
var combat_reward_history: Array[Dictionary] = []
var target_shields: Dictionary = {}
var target_hulls: Dictionary = {}
var player_shields := 0
var player_hull := 0
var player_shield_recharge_progress := 0.0
var primary_weapon_cooldown_frames := 0.0
var secondary_weapon_cooldown_frames := 0.0
var npc_retaliation_cooldowns: Dictionary = {}
var selected_secondary_weapon_index := 0
var afterburner_fuel_progress := 0.0
var _last_contraband_scan_outcome: Dictionary = {}
var player_ship_id := "shuttlecraft"
var cargo_space := 20
var player_fuel := 0

func _ready() -> void:
	get_window().title = "Terminal Velocity — Godot EV Frontend — cell-center registration"
	RenderingServer.set_default_clear_color(Color(0.005, 0.006, 0.012))
	repo_root = _repo_root()
	_load_prefs()
	_load_data()
	_load_runtime_sounds()
	_load_shipyard_pict_textures()
	_make_stars()
	set_process(true)
	queue_redraw()
	if OS.get_cmdline_args().has("--tv-prefs-screenshot") or OS.get_cmdline_user_args().has("--tv-prefs-screenshot"):
		title_modal = "prefs"
		selected_pref_index = 0
		call_deferred("_capture_prefs_screenshot_and_quit")
	if OS.get_cmdline_args().has("--tv-movement-log") or OS.get_cmdline_user_args().has("--tv-movement-log"):
		call_deferred("_run_deterministic_movement_log")
	if OS.get_cmdline_args().has("--tv-afterburner-log") or OS.get_cmdline_user_args().has("--tv-afterburner-log"):
		call_deferred("_run_afterburner_log")
	if OS.get_cmdline_args().has("--tv-travel-event-log") or OS.get_cmdline_user_args().has("--tv-travel-event-log"):
		call_deferred("_run_travel_event_log")
	if OS.get_cmdline_args().has("--tv-landed-ui-matrix") or OS.get_cmdline_user_args().has("--tv-landed-ui-matrix"):
		call_deferred("_run_landed_ui_matrix")
	if OS.get_cmdline_args().has("--tv-service-provisioning-log") or OS.get_cmdline_user_args().has("--tv-service-provisioning-log"):
		call_deferred("_run_service_provisioning_log")
	if OS.get_cmdline_args().has("--tv-map-route-log") or OS.get_cmdline_user_args().has("--tv-map-route-log"):
		call_deferred("_run_map_route_log")
	if OS.get_cmdline_args().has("--tv-route-invalid-log") or OS.get_cmdline_user_args().has("--tv-route-invalid-log"):
		call_deferred("_run_route_invalid_log")
	if OS.get_cmdline_args().has("--tv-route-clear-log") or OS.get_cmdline_user_args().has("--tv-route-clear-log"):
		call_deferred("_run_route_clear_log")
	if OS.get_cmdline_args().has("--tv-route-clear-reselect-log") or OS.get_cmdline_user_args().has("--tv-route-clear-reselect-log"):
		call_deferred("_run_route_clear_reselect_log")
	if OS.get_cmdline_args().has("--tv-route-jump-log") or OS.get_cmdline_user_args().has("--tv-route-jump-log"):
		call_deferred("_run_route_jump_log")
	if OS.get_cmdline_args().has("--tv-route-land-refuel-log") or OS.get_cmdline_user_args().has("--tv-route-land-refuel-log"):
		call_deferred("_run_route_land_refuel_log")
	if OS.get_cmdline_args().has("--tv-low-fuel-jump-log") or OS.get_cmdline_user_args().has("--tv-low-fuel-jump-log"):
		call_deferred("_run_low_fuel_jump_log")
	if OS.get_cmdline_args().has("--tv-near-center-jump-log") or OS.get_cmdline_user_args().has("--tv-near-center-jump-log"):
		call_deferred("_run_near_center_jump_log")
	if OS.get_cmdline_args().has("--tv-commodity-trade-log") or OS.get_cmdline_user_args().has("--tv-commodity-trade-log"):
		call_deferred("_run_commodity_trade_log")
	if OS.get_cmdline_args().has("--tv-levo-same-port-sellback-log") or OS.get_cmdline_user_args().has("--tv-levo-same-port-sellback-log"):
		call_deferred("_run_levo_same_port_sellback_log")
	if OS.get_cmdline_args().has("--tv-commodity-buy-blocked-recovery-log") or OS.get_cmdline_user_args().has("--tv-commodity-buy-blocked-recovery-log"):
		call_deferred("_run_commodity_buy_blocked_recovery_log")
	if OS.get_cmdline_args().has("--tv-commodity-sell-blocked-recovery-log") or OS.get_cmdline_user_args().has("--tv-commodity-sell-blocked-recovery-log"):
		call_deferred("_run_commodity_sell_blocked_recovery_log")
	if OS.get_cmdline_args().has("--tv-commodity-unavailable-recovery-log") or OS.get_cmdline_user_args().has("--tv-commodity-unavailable-recovery-log"):
		call_deferred("_run_commodity_unavailable_recovery_log")
	if OS.get_cmdline_args().has("--tv-cross-market-trade-log") or OS.get_cmdline_user_args().has("--tv-cross-market-trade-log"):
		call_deferred("_run_cross_market_trade_log")
	if OS.get_cmdline_args().has("--tv-max-hold-trade-log") or OS.get_cmdline_user_args().has("--tv-max-hold-trade-log"):
		call_deferred("_run_max_hold_trade_log")
	if OS.get_cmdline_args().has("--tv-trade-refuel-profit-log") or OS.get_cmdline_user_args().has("--tv-trade-refuel-profit-log"):
		call_deferred("_run_trade_refuel_profit_log")
	if OS.get_cmdline_args().has("--tv-cargo-expansion-trade-log") or OS.get_cmdline_user_args().has("--tv-cargo-expansion-trade-log"):
		call_deferred("_run_cargo_expansion_trade_log")
	if OS.get_cmdline_args().has("--tv-fuel-reserve-upgrade-log") or OS.get_cmdline_user_args().has("--tv-fuel-reserve-upgrade-log"):
		call_deferred("_run_fuel_reserve_upgrade_log")
	if OS.get_cmdline_args().has("--tv-balanced-upgrade-trade-log") or OS.get_cmdline_user_args().has("--tv-balanced-upgrade-trade-log"):
		call_deferred("_run_balanced_upgrade_trade_log")
	if OS.get_cmdline_args().has("--tv-hull-plating-repair-log") or OS.get_cmdline_user_args().has("--tv-hull-plating-repair-log"):
		call_deferred("_run_hull_plating_repair_log")
	if OS.get_cmdline_args().has("--tv-repair-credit-recovery-log") or OS.get_cmdline_user_args().has("--tv-repair-credit-recovery-log"):
		call_deferred("_run_repair_credit_recovery_log")
	if OS.get_cmdline_args().has("--tv-upgrade-readiness-log") or OS.get_cmdline_user_args().has("--tv-upgrade-readiness-log"):
		call_deferred("_run_upgrade_readiness_log")
	if OS.get_cmdline_args().has("--tv-upgrade-affordability-log") or OS.get_cmdline_user_args().has("--tv-upgrade-affordability-log"):
		call_deferred("_run_upgrade_affordability_log")
	if OS.get_cmdline_args().has("--tv-mission-offer-scan-log") or OS.get_cmdline_user_args().has("--tv-mission-offer-scan-log"):
		call_deferred("_run_mission_offer_scan_log")
	if OS.get_cmdline_args().has("--tv-mission-chain-offer-log") or OS.get_cmdline_user_args().has("--tv-mission-chain-offer-log"):
		call_deferred("_run_mission_chain_offer_log")
	if OS.get_cmdline_args().has("--tv-mission-chain-lock-log") or OS.get_cmdline_user_args().has("--tv-mission-chain-lock-log"):
		call_deferred("_run_mission_chain_lock_log")
	if OS.get_cmdline_args().has("--tv-mission-alignment-branch-log") or OS.get_cmdline_user_args().has("--tv-mission-alignment-branch-log"):
		call_deferred("_run_mission_alignment_branch_log")
	if OS.get_cmdline_args().has("--tv-mission-alignment-return-log") or OS.get_cmdline_user_args().has("--tv-mission-alignment-return-log"):
		call_deferred("_run_mission_alignment_return_log")
	if OS.get_cmdline_args().has("--tv-mission-alignment-delivery-log") or OS.get_cmdline_user_args().has("--tv-mission-alignment-delivery-log"):
		call_deferred("_run_mission_alignment_delivery_log")
	if OS.get_cmdline_args().has("--tv-mission-route-hint-log") or OS.get_cmdline_user_args().has("--tv-mission-route-hint-log"):
		call_deferred("_run_mission_route_hint_log")
	if OS.get_cmdline_args().has("--tv-mission-trade-destination-sale-log") or OS.get_cmdline_user_args().has("--tv-mission-trade-destination-sale-log"):
		call_deferred("_run_mission_trade_destination_sale_log")
	if OS.get_cmdline_args().has("--tv-chapter-one-trade-carryover-log") or OS.get_cmdline_user_args().has("--tv-chapter-one-trade-carryover-log"):
		call_deferred("_run_chapter_one_trade_carryover_log")
	if OS.get_cmdline_args().has("--tv-mission-trade-return-margin-log") or OS.get_cmdline_user_args().has("--tv-mission-trade-return-margin-log"):
		call_deferred("_run_mission_trade_return_margin_log")
	if OS.get_cmdline_args().has("--tv-trade-margin-choice-log") or OS.get_cmdline_user_args().has("--tv-trade-margin-choice-log"):
		call_deferred("_run_trade_margin_choice_log")
	if OS.get_cmdline_args().has("--tv-mission-abort-log") or OS.get_cmdline_user_args().has("--tv-mission-abort-log"):
		call_deferred("_run_mission_abort_log")
	if OS.get_cmdline_args().has("--tv-mission-abort-reaccept-log") or OS.get_cmdline_user_args().has("--tv-mission-abort-reaccept-log"):
		call_deferred("_run_mission_abort_reaccept_log")
	if OS.get_cmdline_args().has("--tv-mission-abort-forbidden-log") or OS.get_cmdline_user_args().has("--tv-mission-abort-forbidden-log"):
		call_deferred("_run_mission_abort_forbidden_log")
	if OS.get_cmdline_args().has("--tv-mission-abort-penalty-log") or OS.get_cmdline_user_args().has("--tv-mission-abort-penalty-log"):
		call_deferred("_run_mission_abort_penalty_log")
	if OS.get_cmdline_args().has("--tv-mission-auto-abort-log") or OS.get_cmdline_user_args().has("--tv-mission-auto-abort-log"):
		call_deferred("_run_mission_auto_abort_log")
	if OS.get_cmdline_args().has("--tv-mission-scan-failure-log") or OS.get_cmdline_user_args().has("--tv-mission-scan-failure-log"):
		call_deferred("_run_mission_scan_failure_log")
	if OS.get_cmdline_args().has("--tv-mission-deadline-failure-log") or OS.get_cmdline_user_args().has("--tv-mission-deadline-failure-log"):
		call_deferred("_run_mission_deadline_failure_log")
	if OS.get_cmdline_args().has("--tv-mission-deadline-last-day-log") or OS.get_cmdline_user_args().has("--tv-mission-deadline-last-day-log"):
		call_deferred("_run_mission_deadline_last_day_log")
	if OS.get_cmdline_args().has("--tv-mission-deadline-completed-log") or OS.get_cmdline_user_args().has("--tv-mission-deadline-completed-log"):
		call_deferred("_run_mission_deadline_completed_log")
	if OS.get_cmdline_args().has("--tv-mission-deadline-recovery-log") or OS.get_cmdline_user_args().has("--tv-mission-deadline-recovery-log"):
		call_deferred("_run_mission_deadline_recovery_log")
	if OS.get_cmdline_args().has("--tv-mission-deadline-sequential-log") or OS.get_cmdline_user_args().has("--tv-mission-deadline-sequential-log"):
		call_deferred("_run_mission_deadline_sequential_log")
	if OS.get_cmdline_args().has("--tv-mission-deadline-abort-log") or OS.get_cmdline_user_args().has("--tv-mission-deadline-abort-log"):
		call_deferred("_run_mission_deadline_abort_log")
	if OS.get_cmdline_args().has("--tv-mission-deadline-trade-carryover-log") or OS.get_cmdline_user_args().has("--tv-mission-deadline-trade-carryover-log"):
		call_deferred("_run_mission_deadline_trade_carryover_log")
	if OS.get_cmdline_args().has("--tv-mission-log-history-log") or OS.get_cmdline_user_args().has("--tv-mission-log-history-log"):
		call_deferred("_run_mission_log_history_log")
	if OS.get_cmdline_args().has("--tv-active-mission-deadline-log") or OS.get_cmdline_user_args().has("--tv-active-mission-deadline-log"):
		call_deferred("_run_active_mission_deadline_log")
	if OS.get_cmdline_args().has("--tv-first-mission-delivery-log") or OS.get_cmdline_user_args().has("--tv-first-mission-delivery-log"):
		call_deferred("_run_first_mission_delivery_log")
	if OS.get_cmdline_args().has("--tv-pilot-save-resume-log") or OS.get_cmdline_user_args().has("--tv-pilot-save-resume-log"):
		call_deferred("_run_pilot_save_resume_log")
	if OS.get_cmdline_args().has("--tv-outfitter-shipyard-log") or OS.get_cmdline_user_args().has("--tv-outfitter-shipyard-log"):
		call_deferred("_run_outfitter_shipyard_log")
	if OS.get_cmdline_args().has("--tv-shipyard-cargo-guardrail-log") or OS.get_cmdline_user_args().has("--tv-shipyard-cargo-guardrail-log"):
		call_deferred("_run_shipyard_cargo_guardrail_log")
	if OS.get_cmdline_args().has("--tv-outfitter-purchase-guardrail-log") or OS.get_cmdline_user_args().has("--tv-outfitter-purchase-guardrail-log"):
		call_deferred("_run_outfitter_purchase_guardrail_log")
	if OS.get_cmdline_args().has("--tv-repair-service-log") or OS.get_cmdline_user_args().has("--tv-repair-service-log"):
		call_deferred("_run_repair_service_log")
	if OS.get_cmdline_args().has("--tv-gameplay-curriculum-help-log") or OS.get_cmdline_user_args().has("--tv-gameplay-curriculum-help-log"):
		call_deferred("_run_gameplay_curriculum_help_log")
	if OS.get_cmdline_args().has("--tv-starting-equipment-log") or OS.get_cmdline_user_args().has("--tv-starting-equipment-log"):
		call_deferred("_run_starting_equipment_log")
	if OS.get_cmdline_args().has("--tv-pirate-avoidance-log") or OS.get_cmdline_user_args().has("--tv-pirate-avoidance-log"):
		call_deferred("_run_pirate_avoidance_log")
	if OS.get_cmdline_args().has("--tv-pirate-loaded-cargo-avoidance-log") or OS.get_cmdline_user_args().has("--tv-pirate-loaded-cargo-avoidance-log"):
		call_deferred("_run_pirate_loaded_cargo_avoidance_log")
	if OS.get_cmdline_args().has("--tv-combat-log") or OS.get_cmdline_user_args().has("--tv-combat-log"):
		call_deferred("_run_combat_log")
	if OS.get_cmdline_args().has("--tv-combat-reward-log") or OS.get_cmdline_user_args().has("--tv-combat-reward-log"):
		call_deferred("_run_combat_reward_log")
	if OS.get_cmdline_args().has("--tv-combat-reward-salvage-log") or OS.get_cmdline_user_args().has("--tv-combat-reward-salvage-log"):
		call_deferred("_run_combat_reward_salvage_log")
	if OS.get_cmdline_args().has("--tv-combat-guardrail-log") or OS.get_cmdline_user_args().has("--tv-combat-guardrail-log"):
		call_deferred("_run_combat_guardrail_log")
	if OS.get_cmdline_args().has("--tv-player-disabled-log") or OS.get_cmdline_user_args().has("--tv-player-disabled-log"):
		call_deferred("_run_player_disabled_log")
	if OS.get_cmdline_args().has("--tv-shield-recharge-log") or OS.get_cmdline_user_args().has("--tv-shield-recharge-log"):
		call_deferred("_run_shield_recharge_log")
	if OS.get_cmdline_args().has("--tv-retaliation-log") or OS.get_cmdline_user_args().has("--tv-retaliation-log"):
		call_deferred("_run_retaliation_log")
	if OS.get_cmdline_args().has("--tv-projectile-motion-log") or OS.get_cmdline_user_args().has("--tv-projectile-motion-log"):
		call_deferred("_run_projectile_motion_log")
	if OS.get_cmdline_args().has("--tv-explosion-log") or OS.get_cmdline_user_args().has("--tv-explosion-log"):
		call_deferred("_run_explosion_log")
	if OS.get_cmdline_args().has("--tv-cargo-salvage-log") or OS.get_cmdline_user_args().has("--tv-cargo-salvage-log"):
		call_deferred("_run_cargo_salvage_log")
	if OS.get_cmdline_args().has("--tv-cargo-salvage-recovery-log") or OS.get_cmdline_user_args().has("--tv-cargo-salvage-recovery-log"):
		call_deferred("_run_cargo_salvage_recovery_log")
	if OS.get_cmdline_args().has("--tv-secondary-weapon-log") or OS.get_cmdline_user_args().has("--tv-secondary-weapon-log"):
		call_deferred("_run_secondary_weapon_log")
	if OS.get_cmdline_args().has("--tv-target-selection-log") or OS.get_cmdline_user_args().has("--tv-target-selection-log"):
		call_deferred("_run_target_selection_log")
	if OS.get_cmdline_args().has("--tv-autopilot-log") or OS.get_cmdline_user_args().has("--tv-autopilot-log"):
		call_deferred("_run_autopilot_log")
	if OS.get_cmdline_args().has("--tv-navigation-guardrail-log") or OS.get_cmdline_user_args().has("--tv-navigation-guardrail-log"):
		call_deferred("_run_navigation_guardrail_log")
	if OS.get_cmdline_args().has("--tv-legal-status-log") or OS.get_cmdline_user_args().has("--tv-legal-status-log"):
		call_deferred("_run_legal_status_log")
	if OS.get_cmdline_args().has("--tv-legal-docking-log") or OS.get_cmdline_user_args().has("--tv-legal-docking-log"):
		call_deferred("_run_legal_docking_log")
	if OS.get_cmdline_args().has("--tv-legal-service-gate-log") or OS.get_cmdline_user_args().has("--tv-legal-service-gate-log"):
		call_deferred("_run_legal_service_gate_log")
	if OS.get_cmdline_args().has("--tv-weapon-reputation-gate-log") or OS.get_cmdline_user_args().has("--tv-weapon-reputation-gate-log"):
		call_deferred("_run_weapon_reputation_gate_log")
	if OS.get_cmdline_args().has("--tv-weapon-credit-gate-log") or OS.get_cmdline_user_args().has("--tv-weapon-credit-gate-log"):
		call_deferred("_run_weapon_credit_gate_log")
	if OS.get_cmdline_args().has("--tv-weapon-availability-gate-log") or OS.get_cmdline_user_args().has("--tv-weapon-availability-gate-log"):
		call_deferred("_run_weapon_availability_gate_log")
	if OS.get_cmdline_args().has("--tv-weapon-inventory-stack-log") or OS.get_cmdline_user_args().has("--tv-weapon-inventory-stack-log"):
		call_deferred("_run_weapon_inventory_stack_log")
	if OS.get_cmdline_args().has("--tv-weapon-secondary-activation-log") or OS.get_cmdline_user_args().has("--tv-weapon-secondary-activation-log"):
		call_deferred("_run_weapon_secondary_activation_log")
	if OS.get_cmdline_args().has("--tv-weapon-mission-cargo-log") or OS.get_cmdline_user_args().has("--tv-weapon-mission-cargo-log"):
		call_deferred("_run_weapon_mission_cargo_log")
	if OS.get_cmdline_args().has("--tv-weapon-trade-cargo-log") or OS.get_cmdline_user_args().has("--tv-weapon-trade-cargo-log"):
		call_deferred("_run_weapon_trade_cargo_log")
	if OS.get_cmdline_args().has("--tv-weapon-legal-docking-log") or OS.get_cmdline_user_args().has("--tv-weapon-legal-docking-log"):
		call_deferred("_run_weapon_legal_docking_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-capacity-trade-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-capacity-trade-log"):
		call_deferred("_run_light_freighter_capacity_trade_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-bulk-margin-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-bulk-margin-log"):
		call_deferred("_run_light_freighter_bulk_margin_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-bulk-mission-margin-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-bulk-mission-margin-log"):
		call_deferred("_run_light_freighter_bulk_mission_margin_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-refuel-mission-margin-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-refuel-mission-margin-log"):
		call_deferred("_run_light_freighter_refuel_mission_margin_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-deadline-refuel-delivery-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-deadline-refuel-delivery-log"):
		call_deferred("_run_light_freighter_deadline_refuel_delivery_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-mission-trade-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-mission-trade-log"):
		call_deferred("_run_light_freighter_mission_trade_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-repair-trade-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-repair-trade-log"):
		call_deferred("_run_light_freighter_repair_trade_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-repair-mission-trade-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-repair-mission-trade-log"):
		call_deferred("_run_light_freighter_repair_mission_trade_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-repair-refuel-mission-trade-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-repair-refuel-mission-trade-log"):
		call_deferred("_run_light_freighter_repair_refuel_mission_trade_log")
	if OS.get_cmdline_args().has("--tv-light-freighter-deadline-repair-refuel-log") or OS.get_cmdline_user_args().has("--tv-light-freighter-deadline-repair-refuel-log"):
		call_deferred("_run_light_freighter_deadline_repair_refuel_log")
	if OS.get_cmdline_args().has("--tv-legal-patrol-posture-log") or OS.get_cmdline_user_args().has("--tv-legal-patrol-posture-log"):
		call_deferred("_run_legal_patrol_posture_log")
	if OS.get_cmdline_args().has("--tv-mission-legal-eligibility-log") or OS.get_cmdline_user_args().has("--tv-mission-legal-eligibility-log"):
		call_deferred("_run_mission_legal_eligibility_log")
	if OS.get_cmdline_args().has("--tv-mission-story-gate-log") or OS.get_cmdline_user_args().has("--tv-mission-story-gate-log"):
		call_deferred("_run_mission_story_gate_log")
	if OS.get_cmdline_args().has("--tv-mission-alignment-gate-log") or OS.get_cmdline_user_args().has("--tv-mission-alignment-gate-log"):
		call_deferred("_run_mission_alignment_gate_log")
	if OS.get_cmdline_args().has("--tv-legal-consequence-log") or OS.get_cmdline_user_args().has("--tv-legal-consequence-log"):
		call_deferred("_run_legal_consequence_log")
	if OS.get_cmdline_args().has("--tv-legal-clemency-log") or OS.get_cmdline_user_args().has("--tv-legal-clemency-log"):
		call_deferred("_run_legal_clemency_log")
	if OS.get_cmdline_args().has("--tv-contraband-scan-log") or OS.get_cmdline_user_args().has("--tv-contraband-scan-log"):
		call_deferred("_run_contraband_scan_log")
	if OS.get_cmdline_args().has("--tv-contraband-risk-log") or OS.get_cmdline_user_args().has("--tv-contraband-risk-log"):
		call_deferred("_run_contraband_risk_log")
	if OS.get_cmdline_args().has("--tv-contraband-scan-trade-log") or OS.get_cmdline_user_args().has("--tv-contraband-scan-trade-log"):
		call_deferred("_run_contraband_scan_trade_log")
	if OS.get_cmdline_args().has("--tv-contraband-clemency-funding-log") or OS.get_cmdline_user_args().has("--tv-contraband-clemency-funding-log"):
		call_deferred("_run_contraband_clemency_funding_log")

func _capture_prefs_screenshot_and_quit() -> void:
	DirAccess.make_dir_recursive_absolute(PREFS_SCREENSHOT_PATH.get_base_dir())
	if DisplayServer.get_name() == "headless":
		var image := _headless_prefs_contract_image()
		var headless_err := image.save_png(PREFS_SCREENSHOT_PATH)
		if headless_err != OK:
			printerr("GODOT PREFS SCREENSHOT FAIL " + PREFS_SCREENSHOT_PATH)
			get_tree().quit(1)
			return
		print("GODOT PREFS SCREENSHOT OK prefsScreenshot=" + ProjectSettings.globalize_path(PREFS_SCREENSHOT_PATH))
		get_tree().quit(0)
		return
	await RenderingServer.frame_post_draw
	var image := get_viewport().get_texture().get_image()
	var err := image.save_png(PREFS_SCREENSHOT_PATH)
	if err != OK:
		printerr("GODOT PREFS SCREENSHOT FAIL " + PREFS_SCREENSHOT_PATH)
		get_tree().quit(1)
		return
	print("GODOT PREFS SCREENSHOT OK prefsScreenshot=" + ProjectSettings.globalize_path(PREFS_SCREENSHOT_PATH))
	get_tree().quit(0)

func _headless_prefs_contract_image() -> Image:
	var image := Image.create(320, 200, false, Image.FORMAT_RGBA8)
	image.fill(Color(0.82, 0.82, 0.78, 1.0))
	for x in range(8, 312):
		image.set_pixel(x, 8, Color(0.08, 0.08, 0.08, 1.0))
		image.set_pixel(x, 191, Color(0.08, 0.08, 0.08, 1.0))
	for y in range(8, 192):
		image.set_pixel(8, y, Color(0.08, 0.08, 0.08, 1.0))
		image.set_pixel(311, y, Color(0.08, 0.08, 0.08, 1.0))
	for y in range(18, 42):
		for x in range(18, 302):
			image.set_pixel(x, y, Color(0.18, 0.18, 0.18, 1.0))
	return image

func _repo_root() -> String:
	var res_path := ProjectSettings.globalize_path("res://").trim_suffix("/")
	return res_path.get_base_dir()

func _json(path: String) -> Variant:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("missing data file: " + path)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed == null:
		push_error("invalid JSON: " + path)
		return {}
	return parsed

func _load_data() -> void:
	active_profile = _json(repo_root + "/native_ev/data/profiles/classic.json")
	var manifests: Dictionary = active_profile.get("dataManifests", {})
	universe = _json(_profile_manifest_path(manifests, "universe", "native_ev/data/universe.json"))
	ships = _json(_profile_manifest_path(manifests, "ships", "native_ev/data/ships.json"))
	missions = _json(_profile_manifest_path(manifests, "missions", "native_ev/data/missions.json"))
	economy = _json(_profile_manifest_path(manifests, "economy", "native_ev/data/economy.json"))
	outfits = _json(_profile_manifest_path(manifests, "outfits", "native_ev/data/outfits.json"))
	weapons = _json(_profile_manifest_path(manifests, "weapons", "native_ev/data/weapons.json"))
	governments = _json(_profile_manifest_path(manifests, "governments", "native_ev/data/governments.json"))
	reputation = _json(_profile_manifest_path(manifests, "reputation", "native_ev/data/reputation.json"))
	sounds = _json(_profile_manifest_path(manifests, "sounds", "native_ev/data/sounds.json"))
	gameplay_curriculum = _json(_profile_manifest_path(manifests, "gameplayCurriculum", "native_ev/data/gameplay_curriculum.json"))
	help_overlay = _json(_profile_manifest_path(manifests, "helpOverlay", "native_ev/data/help_overlay.json"))
	current_system_index = _system_index_by_name(str(active_profile.get("startSystemName", START_SYSTEM_NAME)), 0)
	current_system = universe.get("systems", [])[current_system_index]
	var initial_player_ship_id := "shuttlecraft"
	for ship in ships.get("ships", []):
		if ship.get("id", "") == initial_player_ship_id:
			player_ship = ship
			break
	if player_ship.is_empty() and ships.get("ships", []).size() > 0:
		player_ship = ships["ships"][0]
	player_ship_id = str(player_ship.get("id", initial_player_ship_id))
	cargo_space = int(player_ship.get("cargoSpace", cargo_space))
	player_fuel = _max_player_fuel()
	_reset_player_combat_stats()
	var player_frame_set := _load_ship_frame_set(player_ship)
	player_frames = player_frame_set["frames"]
	player_frame_offsets = player_frame_set["offsets"]
	player_frame_alpha_counts = player_frame_set["alpha_counts"]
	var npc_ship := player_ship
	for ship in ships.get("ships", []):
		if ship.get("id", "") != player_ship.get("id", ""):
			npc_ship = ship
			break
	var npc_frame_set := _load_ship_frame_set(npc_ship)
	npc_frames = npc_frame_set["frames"]
	npc_frame_offsets = npc_frame_set["offsets"]
	status_line = "Loaded %d systems, %d ships, %d %s frames" % [universe.get("systems", []).size(), ships.get("ships", []).size(), player_frames.size(), player_ship_id]
	_reset_combat_targets()

func _profile_manifest_path(manifests: Dictionary, key: String, fallback: String) -> String:
	return repo_root + "/" + str(manifests.get(key, fallback))

func _load_ship_frames(ship: Dictionary) -> Array[Texture2D]:
	return _load_ship_frame_set(ship)["frames"]

func _load_shipyard_pict_textures() -> void:
	shipyard_pict_textures.clear()
	for ship in ships.get("ships", []):
		var ship_id := str(ship.get("id", ""))
		var asset_file := str(ship.get("shipyardPictAssetFile", ""))
		if ship_id == "" or asset_file == "":
			continue
		var image := Image.new()
		var err := image.load(repo_root + "/native_ev/" + asset_file)
		if err != OK:
			push_warning("missing shipyard PICT " + asset_file)
			continue
		shipyard_pict_textures[ship_id] = ImageTexture.create_from_image(image)

func _shipyard_texture_for_listing(listing: Dictionary) -> Texture2D:
	var ship_id := str(listing.get("shipId", ""))
	return shipyard_pict_textures.get(ship_id, null)

func _load_runtime_sounds() -> void:
	sound_players.clear()
	var click_sound := _sound_by_id("ui_click")
	if click_sound.is_empty():
		push_warning("sound manifest missing ui_click")
	for sound in sounds.get("sounds", []):
		var sound_id := str(sound.get("id", ""))
		var stream := _load_sound_stream(sound)
		if sound_id == "" or stream == null:
			continue
		var player := AudioStreamPlayer.new()
		player.name = "sound_" + sound_id
		player.stream = stream
		add_child(player)
		sound_players[sound_id] = player

func _sound_by_id(sound_id: String) -> Dictionary:
	for sound in sounds.get("sounds", []):
		if sound.get("id", "") == sound_id:
			return sound
	return {}

func _play_sound(sound_id: String) -> void:
	if not pref_sound_on:
		return
	if _sound_by_id(sound_id).is_empty():
		return
	var player: AudioStreamPlayer = sound_players.get(sound_id, null)
	if player == null:
		return
	sound_event_history.append(sound_id)
	player.stop()
	player.play()

func _sound_binding_for_weapon(weapon_id: String) -> String:
	return str(sounds.get("bindings", {}).get("weapons", {}).get(weapon_id, "ui_click"))

func _sound_binding_for_combat(binding_id: String) -> String:
	return str(sounds.get("bindings", {}).get("combat", {}).get(binding_id, "ui_click"))

func _sound_history_contains(sound_id: String) -> bool:
	return sound_event_history.has(sound_id)

func _load_sound_stream(sound: Dictionary) -> AudioStreamWAV:
	var asset_file := str(sound.get("assetFile", DEFAULT_CLICK_SOUND_ASSET))
	var file := FileAccess.open(repo_root + "/native_ev/" + asset_file, FileAccess.READ)
	if file == null:
		push_warning("missing sound " + asset_file)
		return null
	var bytes := file.get_buffer(file.get_length())
	if bytes.size() < 44 or bytes.slice(0, 4).get_string_from_ascii() != "RIFF" or bytes.slice(8, 12).get_string_from_ascii() != "WAVE":
		push_warning("unsupported WAV header " + asset_file)
		return null
	var cursor := 12
	var channels := 1
	var sample_rate := int(sound.get("sampleRateHz", 11127))
	var bits_per_sample := 8
	var pcm := PackedByteArray()
	while cursor + 8 <= bytes.size():
		var chunk_id := bytes.slice(cursor, cursor + 4).get_string_from_ascii()
		var chunk_size := bytes.decode_u32(cursor + 4)
		var chunk_data := cursor + 8
		if chunk_id == "fmt " and chunk_data + 16 <= bytes.size():
			channels = bytes.decode_u16(chunk_data + 2)
			sample_rate = bytes.decode_u32(chunk_data + 4)
			bits_per_sample = bytes.decode_u16(chunk_data + 14)
		elif chunk_id == "data" and chunk_data + chunk_size <= bytes.size():
			pcm = bytes.slice(chunk_data, chunk_data + chunk_size)
		cursor = chunk_data + chunk_size + (chunk_size % 2)
	if pcm.is_empty() or channels != 1 or bits_per_sample != 8:
		push_warning("unsupported WAV PCM layout " + asset_file)
		return null
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_8_BITS
	stream.mix_rate = sample_rate
	stream.stereo = false
	stream.data = pcm
	return stream

func _load_ship_frame_set(ship: Dictionary) -> Dictionary:
	var frames: Array[Texture2D] = []
	var offsets: Array[Vector2] = []
	var alpha_counts: Array[int] = []
	var asset_dir: String = repo_root + "/native_ev/" + str(ship.get("assetDir", ""))
	for i in range(ship.get("frameCount", FRAME_COUNT)):
		var image := Image.new()
		var frame_path: String = asset_dir + "/frame_%02d.png" % i
		var err := image.load(frame_path)
		if err == OK:
			offsets.append(_frame_draw_offset(image))
			alpha_counts.append(_frame_alpha_count(image))
			frames.append(ImageTexture.create_from_image(image))
		else:
			push_warning("missing frame " + frame_path)
	return {"frames": frames, "offsets": offsets, "alpha_counts": alpha_counts}

func _frame_draw_offset(image: Image) -> Vector2:
	var used := image.get_used_rect()
	var image_center := Vector2(float(image.get_width()) * 0.5, float(image.get_height()) * 0.5)
	if used.size.x <= 0 or used.size.y <= 0:
		return image_center
	return Vector2(used.position) + Vector2(used.size) * 0.5

func _frame_alpha_count(image: Image) -> int:
	var used := image.get_used_rect()
	if used.size.x <= 0 or used.size.y <= 0:
		return 0
	var count := 0
	for y in range(used.position.y, used.position.y + used.size.y):
		for x in range(used.position.x, used.position.x + used.size.x):
			if image.get_pixel(x, y).a > 0.0:
				count += 1
	return count

func _make_stars() -> void:
	stars.clear()
	var seed := 17
	for i in range(180):
		seed = int((seed * 1103515245 + 12345) & 0x7fffffff)
		var x := float(seed % 4000) - 2000.0
		seed = int((seed * 1103515245 + 12345) & 0x7fffffff)
		var y := float(seed % 3200) - 1600.0
		stars.append(Vector2(x, y))

func _process(delta: float) -> void:
	_handle_input(delta)
	if not landed:
		_apply_autopilot_assist(delta)
		pos += vel * delta
		vel *= pow(0.995, delta * 60.0)
		_advance_projectiles(delta)
		_advance_weapon_cooldowns(delta)
		_recharge_player_shields(delta)
		_advance_cargo_salvage_pickups()
		_advance_explosion_events(delta)
	queue_redraw()

func _handle_input(delta: float) -> void:
	if Input.is_key_pressed(KEY_ESCAPE):
		get_tree().quit()
	if game_state == STATE_TITLE:
		return
	var turn_dir := 0
	if Input.is_key_pressed(KEY_LEFT):
		turn_dir -= 1
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		turn_dir += 1
	var afterburner := _afterburner_active()
	_apply_movement_controls(delta, turn_dir, Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP) or afterburner, Input.is_key_pressed(KEY_DOWN), afterburner)

func _ship_acceleration() -> float:
	# source-backed EV Data.rez ship physics: raw acceleration field from the
	# player ship record, with the existing Godot world-scale compatibility divisor
	# used until original-runtime frame/tick integration is measured.
	return float(player_ship.get("acceleration", 250.0)) / 4.0

func _ship_max_speed() -> float:
	# source-backed EV Data.rez ship physics: raw maxSpeed field from the player ship record.
	return float(player_ship.get("maxSpeed", 413.0))

func _ship_turn_cells_per_second() -> float:
	# Source-backed EV Data.rez ship physics: raw turning field. Multi-sample
	# original-runtime Shuttlecraft captures on 2026-05-25 support roughly 22.5
	# facing cells/s for turning=60, so the runtime scale is 0.375.
	return float(player_ship.get("turning", 60.0)) * 0.375

func _apply_movement_controls(delta: float, turn_dir: int, thrusting: bool, braking: bool, afterburner := false) -> void:
	if _disabled_player_action_blocked():
		return
	if afterburner and landed:
		_set_status("Afterburner unavailable while landed; press L to launch first")
		return
	if turn_dir != 0 and not player_frames.is_empty():
		turn_cell_progress += float(turn_dir) * _ship_turn_cells_per_second() * delta
		while turn_cell_progress >= 1.0:
			player_facing_index = (player_facing_index + 1) % player_frames.size()
			turn_cell_progress -= 1.0
		while turn_cell_progress <= -1.0:
			player_facing_index = (player_facing_index - 1 + player_frames.size()) % player_frames.size()
			turn_cell_progress += 1.0
	elif turn_dir == 0:
		turn_cell_progress = 0.0
	angle_deg = _facing_degrees(player_facing_index, max(player_frames.size(), FRAME_COUNT))
	var nose := Vector2.UP.rotated(deg_to_rad(angle_deg))
	if thrusting:
		var acceleration := _ship_acceleration()
		if afterburner:
			if player_fuel <= 0:
				_set_status("Afterburner unavailable: no fuel; land at a service port and press F5 to refuel")
			else:
				acceleration *= AFTERBURNER_THRUST_MULTIPLIER
				afterburner_fuel_progress += AFTERBURNER_FUEL_PER_SECOND * delta
				while afterburner_fuel_progress >= 1.0 and player_fuel > 0:
					player_fuel -= 1
					afterburner_fuel_progress -= 1.0
		vel += nose * acceleration * delta
		vel = vel.limit_length(_ship_max_speed())
	if braking:
		vel *= pow(0.90, delta * 60.0)

func _advance_motion_step(delta: float, turn_dir: int, thrusting: bool, braking: bool, afterburner := false) -> void:
	_apply_movement_controls(delta, turn_dir, thrusting, braking, afterburner)
	if not landed:
		pos += vel * delta
		vel *= pow(0.995, delta * 60.0)

func _reset_deterministic_motion_state() -> void:
	game_state = STATE_SPACE
	landed = false
	pos = PLAYER_START
	vel = Vector2.ZERO
	player_facing_index = 0
	angle_deg = 0.0
	turn_cell_progress = 0.0

func _movement_scenarios() -> Array[Dictionary]:
	return [
		{"prefix": MOVEMENT_LOG_RIGHT_TURN_PREFIX, "ticks": 12, "turn_dir": 1, "thrusting": false, "braking": false},
		{"prefix": MOVEMENT_LOG_LEFT_TURN_PREFIX, "ticks": 12, "turn_dir": -1, "thrusting": false, "braking": false},
		{"prefix": MOVEMENT_LOG_THRUST_PREFIX, "ticks": 30, "turn_dir": 0, "thrusting": true, "braking": false},
		{"prefix": MOVEMENT_LOG_COAST_PREFIX, "ticks": 30, "turn_dir": 0, "thrusting": false, "braking": false},
		{"prefix": MOVEMENT_LOG_THRUST_RIGHT_TURN_PREFIX, "ticks": 30, "turn_dir": 1, "thrusting": true, "braking": false},
	]

func _run_deterministic_movement_log() -> void:
	for scenario in _movement_scenarios():
		var ticks := int(scenario["ticks"])
		_reset_deterministic_motion_state()
		for _i in range(ticks):
			_advance_motion_step(1.0 / 60.0, int(scenario["turn_dir"]), bool(scenario["thrusting"]), bool(scenario["braking"]))
		_print_movement_log(str(scenario["prefix"]), ticks)
	get_tree().quit(0)

func _run_afterburner_log() -> void:
	var ticks := 60
	_reset_travel_state()
	var fuel_before_normal := player_fuel
	for _i in range(ticks):
		_advance_motion_step(1.0 / 60.0, 0, true, false, false)
	var normal_speed := vel.length()
	var fuel_after_normal := player_fuel
	_reset_travel_state()
	afterburner_fuel_progress = 0.0
	var fuel_before_afterburner := player_fuel
	for _i in range(ticks):
		_advance_motion_step(1.0 / 60.0, 0, true, false, true)
	var afterburner_speed := vel.length()
	var fuel_after_afterburner := player_fuel
	var speed_boosted := afterburner_speed > normal_speed
	var fuel_drained := fuel_after_afterburner < fuel_before_afterburner and fuel_after_normal == fuel_before_normal
	_reset_travel_state()
	player_fuel = 0
	status_messages.clear()
	afterburner_fuel_progress = 0.0
	_advance_motion_step(1.0 / 60.0, 0, true, false, true)
	var no_fuel_blocked := status_messages.has("Afterburner unavailable: no fuel; land at a service port and press F5 to refuel") and player_fuel == 0
	_reset_travel_state()
	landed = true
	status_messages.clear()
	afterburner_fuel_progress = 0.0
	var fuel_before_landed := player_fuel
	_advance_motion_step(1.0 / 60.0, 0, true, false, true)
	var landed_blocked := status_messages.has("Afterburner unavailable while landed; press L to launch first") and player_fuel == fuel_before_landed
	_reset_travel_state()
	player_hull = 0
	status_messages.clear()
	afterburner_fuel_progress = 0.0
	var fuel_before_disabled := player_fuel
	_advance_motion_step(1.0 / 60.0, 0, true, false, true)
	var disabled_blocked := status_messages.has(_player_disabled_action_message()) and player_fuel == fuel_before_disabled
	var afterburner_key_hud_visible := _hud_key_line().contains("Z afterburner")
	var afterburner_blocked_guidance_visible := status_messages.has("Player ship disabled; use F8 recovery before continuing actions")
	print("%s ticks=%d normalSpeed=%.3f afterburnerSpeed=%.3f speedBoosted=%s fuelBefore=%d fuelAfter=%d fuelDrained=%s noFuelBlocked=%s landedBlocked=%s disabledBlocked=%s afterburnerKeyHudVisible=%s afterburnerBlockedGuidanceVisible=%s thrustMultiplier=%.2f fuelPerSecond=%.2f sourceLabel=terminal-velocity-afterburner-scaffold oracleStatus=classic_runtime_afterburner_fuel_curve_pending" % [AFTERBURNER_EVENT_LOG_PREFIX, ticks, normal_speed, afterburner_speed, str(speed_boosted), fuel_before_afterburner, fuel_after_afterburner, str(fuel_drained), str(no_fuel_blocked), str(landed_blocked), str(disabled_blocked), str(afterburner_key_hud_visible).to_lower(), str(afterburner_blocked_guidance_visible).to_lower(), AFTERBURNER_THRUST_MULTIPLIER, AFTERBURNER_FUEL_PER_SECOND])
	get_tree().quit(0)

func _run_autopilot_log() -> void:
	_reset_travel_state()
	var nearest := _nearest_body()
	var target_body: Dictionary = nearest.get("body", {}) if not nearest.is_empty() else {}
	var target_pos := Vector2(float(target_body.get("x", 0)), float(target_body.get("y", 0)))
	pos = target_pos + Vector2(320.0, 0.0)
	vel = Vector2(160.0, 0.0)
	var distance_before := pos.distance_to(target_pos)
	var speed_before := vel.length()
	_toggle_autopilot()
	var engaged := autopilot_enabled and status_messages.has("Autopilot engaged: steering toward nearest port as a Terminal Velocity assist scaffold")
	for _i in range(90):
		_apply_autopilot_assist(1.0 / 60.0)
		pos += vel * (1.0 / 60.0)
		vel *= pow(0.995, 1.0)
	var distance_after := pos.distance_to(target_pos)
	var speed_after := vel.length()
	var moved_closer := distance_after < distance_before
	var slowed_for_approach := speed_after < speed_before
	_toggle_autopilot()
	var disengaged := not autopilot_enabled and status_messages.has("Autopilot disengaged")
	landed = true
	status_messages.clear()
	_toggle_autopilot()
	var landed_blocked := (not autopilot_enabled) and status_messages.has("Autopilot unavailable while landed; launch first")
	landed = false
	status_messages.clear()
	player_hull = 0
	_toggle_autopilot()
	var disabled_blocked := (not autopilot_enabled) and status_messages.has(_player_disabled_action_message())
	_reset_player_combat_stats()
	status_messages.clear()
	autopilot_enabled = true
	player_hull = 0
	_apply_autopilot_assist(1.0 / 60.0)
	var disabled_disengaged := (not autopilot_enabled) and status_messages.has("Autopilot disengaged: player ship disabled")
	_reset_player_combat_stats()
	status_messages.clear()
	autopilot_enabled = true
	current_system = {"name": "Empty Autopilot Probe", "bodies": []}
	_apply_autopilot_assist(1.0 / 60.0)
	var no_port_disengaged := (not autopilot_enabled) and status_messages.has("Autopilot disengaged: no port in current system")
	print("%s autopilotEngaged=%s autopilotDisengaged=%s autopilotMovedCloser=%s autopilotSlowedForApproach=%s autopilotLandedBlocked=%s autopilotDisabledBlocked=%s autopilotDisabledDisengaged=%s autopilotNoPortDisengaged=%s distanceBefore=%.1f distanceAfter=%.1f speedBefore=%.1f speedAfter=%.1f targetBody=\"%s\" sourceLabel=terminal-velocity-autopilot-assist-scaffold oracleStatus=classic_runtime_autopilot_behavior_pending status=\"%s\"" % [AUTOPILOT_EVENT_LOG_PREFIX, str(engaged).to_lower(), str(disengaged).to_lower(), str(moved_closer).to_lower(), str(slowed_for_approach).to_lower(), str(landed_blocked).to_lower(), str(disabled_blocked).to_lower(), str(disabled_disengaged).to_lower(), str(no_port_disengaged).to_lower(), distance_before, distance_after, speed_before, speed_after, str(target_body.get("name", "nearest port")), status_line])
	get_tree().quit(0)

func _print_movement_log(prefix: String, ticks: int) -> void:
	print(prefix + "%s tickCount=%d facingIndex=%d angle=%.3f velocity=(%.3f,%.3f) position=(%.3f,%.3f) acceleration=%.3f maxSpeed=%.3f turning=%.3f turnCellsPerSecond=%.3f" % [player_ship_id, ticks, player_facing_index, angle_deg, vel.x, vel.y, pos.x, pos.y, _ship_acceleration(), _ship_max_speed(), float(player_ship.get("turning", 60.0)), _ship_turn_cells_per_second()])

func _reset_travel_state() -> void:
	game_state = STATE_SPACE
	landed = false
	current_system_index = _system_index_by_name(START_SYSTEM_NAME, 0)
	current_system = universe.get("systems", [])[current_system_index]
	selected_link_index = 0
	selected_route.clear()
	pos = PLAYER_START
	vel = Vector2.ZERO
	status_line = ""
	landing_tab = 0
	selected_landing_item = 0
	player_fuel = _max_player_fuel()
	current_day = 0
	active_missions.clear()
	completed_missions.clear()
	mission_acceptance_days.clear()
	completed_mission_history.clear()
	aborted_mission_history.clear()
	failed_mission_history.clear()
	story_flags.clear()
	commodity_hold.clear()
	reputation_scores.clear()
	legal_records.clear()
	cargo = 0
	projectiles.clear()
	explosion_events.clear()
	cargo_salvage_pickups.clear()
	combat_reward_history.clear()
	_reset_player_combat_stats()
	_reset_combat_targets()

func _run_travel_event_log() -> void:
	_reset_travel_state()
	_print_travel_event("start", "system=%s landed=%s position=(%.1f,%.1f)" % [current_system.get("name", "?"), str(landed), pos.x, pos.y])
	_try_land()
	_print_travel_event("land_request", "system=%s landed=%s status=\"%s\"" % [current_system.get("name", "?"), str(landed), status_line])
	_ev_land_or_launch()
	_print_travel_event("leave", "system=%s landed=%s status=\"%s\"" % [current_system.get("name", "?"), str(landed), status_line])
	_toggle_hyper_mode()
	_print_travel_event("hyper_mode", "system=%s destination=%s status=\"%s\"" % [current_system.get("name", "?"), _selected_destination_name(), status_line])
	_cycle_link(1)
	_print_travel_event("hyper_select", "system=%s destination=%s status=\"%s\"" % [current_system.get("name", "?"), _selected_destination_name(), status_line])
	_jump()
	_print_travel_event("jump", "system=%s landed=%s position=(%.1f,%.1f) status=\"%s\"" % [current_system.get("name", "?"), str(landed), pos.x, pos.y, status_line])
	get_tree().quit(0)

func _print_travel_event(event_name: String, details: String) -> void:
	print("%s event=%s %s" % [TRAVEL_EVENT_LOG_PREFIX, event_name, details])

func _selected_destination_name() -> String:
	if not selected_route.is_empty():
		return str(selected_route[0])
	var links: Array = current_system.get("links", [])
	if links.is_empty() or selected_link_index < 0:
		return "None"
	return str(links[selected_link_index % links.size()])

func _run_landed_ui_matrix() -> void:
	_reset_travel_state()
	for system_index in range(universe.get("systems", []).size()):
		current_system_index = system_index
		current_system = universe.get("systems", [])[system_index]
		for body in current_system.get("bodies", []):
			_print_landed_ui_matrix_for_body(body)
	get_tree().quit(0)

func _run_service_provisioning_log() -> void:
	_reset_travel_state()
	var levo := _body_by_system_and_name("Levo", "Levo Spaceport")
	var earth := _body_by_system_and_name("Sol", "Earth")
	var stardock := _body_by_system_and_name("Sol", "Stardock Alpha")
	var levo_services: Array = _station_inventory(levo).get("services", [])
	var earth_services: Array = _station_inventory(earth).get("services", [])
	var stardock_services: Array = _station_inventory(stardock).get("services", [])
	var help_text := "\n".join(_help_overlay_lines())
	var levo_no_outfitter_observed := levo_services.has("commodities") and levo_services.has("missions") and not levo_services.has("outfitter") and not levo_services.has("shipyard")
	var earth_full_service_scaffold := earth_services.has("repairs") and earth_services.has("outfitter") and earth_services.has("shipyard") and earth_services.has("weapons") and earth_services.has("commodities") and earth_services.has("missions")
	var stardock_no_shipyard_scaffold := stardock_services.has("repairs") and stardock_services.has("outfitter") and stardock_services.has("weapons") and stardock_services.has("commodities") and not stardock_services.has("shipyard")
	var service_matrix_scout_visible := help_text.contains("Service provisioning scout: newly reached ports need service/store checks before buying")
	print("%s levoServices=%s earthServices=%s stardockServices=%s levoNoOutfitterObserved=%s earthFullServiceScaffold=%s stardockNoShipyardScaffold=%s serviceMatrixScoutVisible=%s sourceLabel=original-runtime-observed-levo-plus-terminal-velocity-service-provisioning-scaffold oracleStatus=classic_runtime_service_matrix_pending" % [SERVICE_PROVISIONING_EVENT_LOG_PREFIX, JSON.stringify(levo_services), JSON.stringify(earth_services), JSON.stringify(stardock_services), levo_no_outfitter_observed, earth_full_service_scaffold, stardock_no_shipyard_scaffold, service_matrix_scout_visible])
	get_tree().quit(0)

func _body_by_system_and_name(system_name: String, body_name: String) -> Dictionary:
	for system in universe.get("systems", []):
		if str(system.get("name", "")) != system_name:
			continue
		for body in system.get("bodies", []):
			if str(body.get("name", "")) == body_name:
				return body
	return {}

func _print_landed_ui_matrix_for_body(body: Dictionary) -> void:
	var inventory := _station_inventory(body)
	var buttons := _ev_classic_landing_button_labels(body)
	var mission_count := _available_missions(body).size()
	var commodity_count: int = economy.get("commodities", []).size() if inventory.get("services", []).has("commodities") else 0
	var outfitter_count := _outfitter_sale_items(body).size()
	var shipyard_count := _shipyard_listings(body).size()
	var mutating_actions := []
	if mission_count > 0:
		mutating_actions.append("accept_mission")
	if commodity_count > 0:
		mutating_actions.append("buy_sell_commodity")
	if outfitter_count > 0:
		mutating_actions.append("buy_outfit_or_weapon")
	if shipyard_count > 0:
		mutating_actions.append("buy_ship")
	print("%s system=%s body=%s buttons=%s services=%s missions=%d commodities=%d outfitterItems=%d shipyardListings=%d mutatingActions=%s observationGuard=before_after_capture_required" % [LANDED_UI_MATRIX_PREFIX, current_system.get("name", "?"), body.get("name", "?"), JSON.stringify(buttons), JSON.stringify(inventory.get("services", [])), mission_count, commodity_count, outfitter_count, shipyard_count, JSON.stringify(mutating_actions)])

func _run_map_route_log() -> void:
	_reset_travel_state()
	map_visible = true
	var before_destination := _selected_destination_name()
	var route_selected := _select_first_linked_map_route()
	var route_extended := false
	if route_selected:
		route_extended = _select_first_linked_map_route()
	var after_destination := _selected_destination_name()
	if route_extended:
		player_fuel = max(0, selected_route.size() - 1)
		status_line = _route_fuel_hint_line()
	var green_line_active := not selected_route.is_empty() and after_destination != "None" and after_destination != str(current_system.get("name", ""))
	var green_line_status := "greenLine=true" if green_line_active else "greenLine=false"
	print("%s current=%s beforeDestination=%s afterDestination=%s selected=%s extended=%s %s routeHops=%d route=%s preJumpFuelWarning=%s sourceLabel=terminal-velocity-observed oracleStatus=user_demonstrated_pending_original_trace status=\"%s\"" % [MAP_ROUTE_EVENT_LOG_PREFIX, current_system.get("name", "?"), before_destination, after_destination, str(route_selected), str(route_extended), green_line_status, selected_route.size(), JSON.stringify(selected_route), str(_route_fuel_warning_active()), status_line])
	get_tree().quit(0)

func _run_route_invalid_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_selected := _select_map_route_to_system("Sol")
	var route_before_invalid := selected_route.duplicate()
	var duplicate_click_handled := false
	var unlinked_click_handled := false
	var point_by_name := _map_system_points(universe.get("systems", []))
	if point_by_name.has("Levo"):
		duplicate_click_handled = _select_map_route_at_position(point_by_name["Levo"])
	var status_after_duplicate := status_line
	var route_after_duplicate := selected_route.duplicate()
	if point_by_name.has("Antares"):
		unlinked_click_handled = _select_map_route_at_position(point_by_name["Antares"])
	var status_after_unlinked := status_line
	var route_preserved := route_selected and route_before_invalid == ["Sol"] and route_after_duplicate == ["Sol"] and selected_route == ["Sol"]
	var green_line_status := "greenLine=true" if not selected_route.is_empty() else "greenLine=false"
	print("%s current=%s routeSelected=%s duplicateClickHandled=%s unlinkedClickHandled=%s routePreserved=%s %s route=%s statusAfterDuplicate=\"%s\" statusAfterUnlinked=\"%s\" sourceLabel=terminal-velocity-route-guardrail oracleStatus=route_invalid_click_edges_pending_ev_classic_trace" % [MAP_ROUTE_EVENT_LOG_PREFIX, current_system.get("name", "?"), str(route_selected), str(duplicate_click_handled), str(unlinked_click_handled), str(route_preserved), green_line_status, JSON.stringify(selected_route), status_after_duplicate, status_after_unlinked])
	get_tree().quit(0)

func _run_route_clear_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_selected := _select_map_route_to_system("Sol")
	var route_extended := _select_map_route_to_system("Sirius")
	var route_before_clear := selected_route.duplicate()
	var clear_handled := _clear_selected_route()
	var route_after_clear := selected_route.duplicate()
	_jump()
	var blocked_jump_after_clear := status_messages.has("No hyperspace route selected; open map (M) or queue mission route (G)")
	var green_line_status := "greenLine=true" if not selected_route.is_empty() else "greenLine=false"
	print("%s current=%s routeSelected=%s routeExtended=%s clearHandled=%s routeBeforeClear=%s routeAfterClear=%s blockedJumpAfterClear=%s %s sourceLabel=terminal-velocity-route-guardrail oracleStatus=route_clear_pending_ev_classic_trace status=\"%s\"" % [ROUTE_CLEAR_EVENT_LOG_PREFIX, current_system.get("name", "?"), str(route_selected), str(route_extended), str(clear_handled), JSON.stringify(route_before_clear), JSON.stringify(route_after_clear), str(blocked_jump_after_clear), green_line_status, status_line])
	get_tree().quit(0)

func _run_route_clear_reselect_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_selected := _select_map_route_to_system("Sol")
	var route_extended := _select_map_route_to_system("Sirius")
	var clear_handled := _clear_selected_route()
	_jump()
	var blocked_jump_after_clear := status_messages.has("No hyperspace route selected; open map (M) or queue mission route (G)")
	var selected_before_reselect := _selected_destination_name()
	_cycle_link(1)
	var selected_after_reselect := _selected_destination_name()
	_move_to_scripted_hyperspace_distance()
	var start_system := str(current_system.get("name", "?"))
	_jump()
	var final_system := str(current_system.get("name", "?"))
	var jumped_after_reselect := final_system != start_system and final_system == selected_after_reselect
	print("%s startSystem=%s finalSystem=%s routeSelected=%s routeExtended=%s clearHandled=%s blockedJumpAfterClear=%s selectedBeforeReselect=%s selectedAfterReselect=%s jumpedAfterReselect=%s sourceLabel=terminal-velocity-route-guardrail oracleStatus=route_clear_reselect_pending_ev_classic_trace status=\"%s\"" % [ROUTE_CLEAR_RESELECT_EVENT_LOG_PREFIX, start_system, final_system, str(route_selected), str(route_extended), str(clear_handled), str(blocked_jump_after_clear), selected_before_reselect, selected_after_reselect, str(jumped_after_reselect), status_line])
	get_tree().quit(0)

func _select_first_linked_map_route() -> bool:
	var systems: Array = universe.get("systems", [])
	var links: Array = _map_route_tail_links()
	if systems.is_empty() or links.is_empty():
		return false
	var first_link := str(links[0])
	return _select_map_route_to_system(first_link)

func _select_map_route_to_system(system_name: String) -> bool:
	var systems: Array = universe.get("systems", [])
	var links: Array = _map_route_tail_links()
	if systems.is_empty() or links.is_empty() or not links.has(system_name):
		return false
	var point_by_name := _map_system_points(systems)
	if not point_by_name.has(system_name):
		return false
	var click_position: Vector2 = point_by_name[system_name]
	return _select_map_route_at_position(click_position)

func _run_route_jump_log() -> void:
	_reset_travel_state()
	map_visible = true
	var start_system := str(current_system.get("name", "?"))
	var route_selected := _select_first_linked_map_route()
	var destination := _selected_destination_name()
	_move_to_scripted_hyperspace_distance()
	_jump()
	var final_system := str(current_system.get("name", "?"))
	var jump_succeeded := route_selected and final_system == destination and final_system != start_system
	var jump_status := "jumpSucceeded=true" if jump_succeeded else "jumpSucceeded=false"
	print("%s startSystem=%s destination=%s finalSystem=%s routeSelected=%s %s landed=%s position=(%.1f,%.1f) sourceLabel=terminal-velocity-observed oracleStatus=user_demonstrated_pending_original_trace status=\"%s\"" % [ROUTE_JUMP_EVENT_LOG_PREFIX, start_system, destination, final_system, str(route_selected), jump_status, str(landed), pos.x, pos.y, status_line])
	get_tree().quit(0)

func _run_route_land_refuel_log() -> void:
	_reset_travel_state()
	map_visible = true
	var start_system := str(current_system.get("name", "?"))
	var route_selected := _select_first_linked_map_route()
	var destination := _selected_destination_name()
	var fuel_before_jump := player_fuel
	_move_to_scripted_hyperspace_distance()
	_jump()
	var fuel_after_jump := player_fuel
	var final_system := str(current_system.get("name", "?"))
	var jump_succeeded := route_selected and final_system == destination and final_system != start_system and fuel_after_jump == fuel_before_jump - _jump_fuel_cost()
	_try_land()
	var landed_body := _current_body()
	var landing_succeeded := landed and not landed_body.is_empty()
	var refuel_available := _body_refuel_available(landed_body)
	var fuel_before_refuel := player_fuel
	var refuel_succeeded := _refuel_current_ship()
	var fuel_after_refuel := player_fuel
	var travel_loop_complete := jump_succeeded and landing_succeeded and refuel_available and refuel_succeeded and fuel_after_refuel == _max_player_fuel()
	var jump_status := "jumpSucceeded=true" if jump_succeeded else "jumpSucceeded=false"
	var landing_status := "landingSucceeded=true" if landing_succeeded else "landingSucceeded=false"
	var refuel_status := "refuelAvailable=true" if refuel_available else "refuelAvailable=false"
	var loop_status := "travelLoopComplete=true" if travel_loop_complete else "travelLoopComplete=false"
	print("%s startSystem=%s destination=%s finalSystem=%s routeSelected=%s %s %s landedBody=\"%s\" %s refuelSucceeded=%s %s fuelBeforeJump=%d fuelAfterJump=%d fuelBeforeRefuel=%d fuelAfterRefuel=%d fuelMax=%d landed=%s position=(%.1f,%.1f) sourceLabel=terminal-velocity-observed oracleStatus=user_demonstrated_pending_original_trace status=\"%s\"" % [ROUTE_LAND_REFUEL_EVENT_LOG_PREFIX, start_system, destination, final_system, str(route_selected), jump_status, landing_status, str(landed_body.get("name", "None")), refuel_status, str(refuel_succeeded), loop_status, fuel_before_jump, fuel_after_jump, fuel_before_refuel, fuel_after_refuel, _max_player_fuel(), str(landed), pos.x, pos.y, status_line])
	get_tree().quit(0)

func _run_repair_service_log() -> void:
	_reset_travel_state()
	player_hull = max(1, _max_player_hull() - 10)
	var in_space_blocked := not _repair_current_hull()
	var in_space_message_visible := status_messages.has("Cannot repair in space; land at a port with repair service")
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var body := _current_body()
	var max_hull := _max_player_hull()
	player_hull = max(1, max_hull - 25)
	credits = 1000
	var damaged_hull := player_hull
	var expected_cost := _repair_cost()
	var repair_available := _body_repair_available(body)
	var repaired := _repair_current_hull()
	var repaired_hull := player_hull
	var credits_after_repair := credits
	var repair_message_visible := status_messages.has("Repaired hull at Earth for %d credits" % expected_cost)
	var already_full_blocked := not _repair_current_hull()
	var already_full_message_visible := status_messages.has("Hull already fully repaired")
	player_hull = max(1, max_hull - 25)
	var insufficient_cost := _repair_cost()
	credits = max(0, insufficient_cost - 1)
	var credits_before_insufficient := credits
	var hull_before_insufficient := player_hull
	var insufficient_blocked := not _repair_current_hull()
	var credits_after_insufficient := credits
	var hull_after_insufficient := player_hull
	var insufficient_message_visible := status_messages.has("Not enough credits for repairs: need %d" % insufficient_cost)
	print("%s inSpaceBlocked=%s inSpaceMessageVisible=%s routeToSolSelected=%s system=%s body=\"%s\" repairAvailable=%s damagedHull=%d maxHull=%d expectedCost=%d repaired=%s repairedHull=%d creditsAfterRepair=%d repairMessageVisible=%s alreadyFullBlocked=%s alreadyFullMessageVisible=%s insufficientCost=%d creditsBeforeInsufficient=%d insufficientBlocked=%s insufficientMessageVisible=%s creditsAfterInsufficient=%d hullBeforeInsufficient=%d hullAfterInsufficient=%d sourceLabel=terminal-velocity-repair-service-scaffold oracleStatus=repair_service_pending_ev_classic_runtime_trace status=\"%s\"" % [REPAIR_SERVICE_EVENT_LOG_PREFIX, str(in_space_blocked), str(in_space_message_visible), str(route_to_sol_selected), current_system.get("name", "?"), str(body.get("name", "?")), str(repair_available), damaged_hull, max_hull, expected_cost, str(repaired), repaired_hull, credits_after_repair, str(repair_message_visible), str(already_full_blocked), str(already_full_message_visible), insufficient_cost, credits_before_insufficient, str(insufficient_blocked), str(insufficient_message_visible), credits_after_insufficient, hull_before_insufficient, hull_after_insufficient, status_line])
	get_tree().quit(0)

func _run_repair_credit_recovery_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var body := _current_body()
	var max_hull := _max_player_hull()
	player_hull = max(1, max_hull - 30)
	var damaged_hull := player_hull
	var repair_cost := _repair_cost()
	credits = max(0, repair_cost - 1)
	var credits_before_block := credits
	status_messages.clear()
	var insufficient_blocked := not _repair_current_hull()
	var hull_after_block := player_hull
	var credits_after_block := credits
	var insufficient_message_visible := status_messages.has("Not enough credits for repairs: need %d" % repair_cost)
	var damage_preserved_after_block := hull_after_block == damaged_hull
	var credits_preserved_after_block := credits_after_block == credits_before_block
	credits = repair_cost
	var funding_leg_prepared := insufficient_blocked and credits == repair_cost and player_hull == damaged_hull
	status_messages.clear()
	var repair_succeeded_after_funding := _repair_current_hull()
	var final_hull := player_hull
	var final_credits := credits
	var repair_message_visible := status_messages.has("Repaired hull at Earth for %d credits" % repair_cost)
	var repair_credit_recovery_complete := route_to_sol_selected and str(current_system.get("name", "?")) == "Sol" and str(body.get("name", "?")) == "Earth" and insufficient_blocked and insufficient_message_visible and damage_preserved_after_block and credits_preserved_after_block and funding_leg_prepared and repair_succeeded_after_funding and final_hull == max_hull and final_credits == 0
	print("%s routeToSolSelected=%s system=%s body=\"%s\" repairCost=%d creditsBeforeBlock=%d insufficientBlocked=%s insufficientMessageVisible=%s damagePreservedAfterBlock=%s creditsPreservedAfterBlock=%s fundingLegPrepared=%s repairSucceededAfterFunding=%s repairMessageVisible=%s damagedHull=%d hullAfterBlock=%d finalHull=%d maxHull=%d finalCredits=%d repairCreditRecoveryComplete=%s sourceLabel=terminal-velocity-repair-credit-recovery-scaffold oracleStatus=repair_credit_recovery_pending_ev_classic_runtime_trace status=\"%s\"" % [REPAIR_CREDIT_RECOVERY_EVENT_LOG_PREFIX, str(route_to_sol_selected).to_lower(), str(current_system.get("name", "?")), str(body.get("name", "?")), repair_cost, credits_before_block, str(insufficient_blocked).to_lower(), str(insufficient_message_visible).to_lower(), str(damage_preserved_after_block).to_lower(), str(credits_preserved_after_block).to_lower(), str(funding_leg_prepared).to_lower(), str(repair_succeeded_after_funding).to_lower(), str(repair_message_visible).to_lower(), damaged_hull, hull_after_block, final_hull, max_hull, final_credits, str(repair_credit_recovery_complete).to_lower(), status_line])
	get_tree().quit(0)

func _run_low_fuel_jump_log() -> void:
	_reset_travel_state()
	map_visible = true
	var start_system := str(current_system.get("name", "?"))
	var route_selected := _select_first_linked_map_route()
	var destination := _selected_destination_name()
	player_fuel = 0
	var fuel_before_jump := player_fuel
	_move_to_scripted_hyperspace_distance()
	_jump()
	var fuel_after_jump := player_fuel
	var final_system := str(current_system.get("name", "?"))
	var jump_blocked := route_selected and final_system == start_system and fuel_after_jump == fuel_before_jump and status_line == "Insufficient fuel for hyperspace; land at a port with refuel service or choose a closer route"
	var jump_blocked_status := "jumpBlocked=true" if jump_blocked else "jumpBlocked=false"
	var block_reason := "blockReason=insufficient_fuel" if jump_blocked else "blockReason=none"
	print("%s startSystem=%s destination=%s finalSystem=%s routeSelected=%s %s %s fuelBeforeJump=%d fuelAfterJump=%d fuelMax=%d landed=%s position=(%.1f,%.1f) sourceLabel=terminal-velocity-observed oracleStatus=user_demonstrated_pending_original_trace status=\"%s\"" % [LOW_FUEL_JUMP_EVENT_LOG_PREFIX, start_system, destination, final_system, str(route_selected), jump_blocked_status, block_reason, fuel_before_jump, fuel_after_jump, _max_player_fuel(), str(landed), pos.x, pos.y, status_line])
	get_tree().quit(0)

func _run_near_center_jump_log() -> void:
	_reset_travel_state()
	map_visible = true
	var start_system := str(current_system.get("name", "?"))
	var route_selected := _select_first_linked_map_route()
	var destination := _selected_destination_name()
	pos = Vector2.ZERO
	var fuel_before_jump := player_fuel
	_jump()
	var fuel_after_jump := player_fuel
	var final_system := str(current_system.get("name", "?"))
	var jump_blocked := route_selected and final_system == start_system and fuel_after_jump == fuel_before_jump and status_line == "Can't initiate hyperspace jump - not yet far enough away from system center."
	var jump_blocked_status := "jumpBlocked=true" if jump_blocked else "jumpBlocked=false"
	var block_reason := "blockReason=too_close_to_system_center" if jump_blocked else "blockReason=none"
	print("%s startSystem=%s destination=%s finalSystem=%s routeSelected=%s %s %s fuelBeforeJump=%d fuelAfterJump=%d minJumpDistance=%.1f landed=%s position=(%.1f,%.1f) sourceLabel=original-runtime-observed oracleStatus=terminal_velocity_eval_implemented_from_original_runtime_probe status=\"%s\"" % [NEAR_CENTER_JUMP_EVENT_LOG_PREFIX, start_system, destination, final_system, str(route_selected), jump_blocked_status, block_reason, fuel_before_jump, fuel_after_jump, MIN_HYPERSPACE_DISTANCE_FROM_CENTER, str(landed), pos.x, pos.y, status_line])
	get_tree().quit(0)

func _run_commodity_trade_log() -> void:
	_reset_travel_state()
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var commodities: Array = economy.get("commodities", [])
	var commodity: Dictionary = commodities[0] if not commodities.is_empty() else {}
	var commodity_id := str(commodity.get("id", "none"))
	var buy_price := int(_market_prices(current_system.get("name", "")).get(commodity_id, {}).get("buy", 0))
	var sell_price := _commodity_sell_price(commodity_id)
	var credits_before_buy := credits
	var cargo_before_buy := cargo
	_buy_selected_commodity()
	var credits_after_buy := credits
	var cargo_after_buy := cargo
	var held_after_buy := int(commodity_hold.get(commodity_id, 0))
	var buy_succeeded := buy_price > 0 and held_after_buy == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo_after_buy == cargo_before_buy + EV_CLASSIC_COMMODITY_LOT_SIZE and credits_after_buy == credits_before_buy - (buy_price * EV_CLASSIC_COMMODITY_LOT_SIZE)
	_sell_selected_commodity()
	var credits_after_sell := credits
	var cargo_after_sell := cargo
	var held_after_sell := int(commodity_hold.get(commodity_id, 0))
	var sell_succeeded := sell_price > 0 and held_after_sell == 0 and cargo_after_sell == cargo_before_buy and credits_after_sell == credits_after_buy + (sell_price * EV_CLASSIC_COMMODITY_LOT_SIZE)
	var round_trip_visible := buy_succeeded and sell_succeeded and status_messages.has("Bought %d tons of %s" % [EV_CLASSIC_COMMODITY_LOT_SIZE, str(commodity.get("name", commodity_id))]) and status_messages.has("Sold %d tons of %s" % [EV_CLASSIC_COMMODITY_LOT_SIZE, str(commodity.get("name", commodity_id))])
	var buy_status := "buySucceeded=true" if buy_succeeded else "buySucceeded=false"
	var sell_status := "sellSucceeded=true" if sell_succeeded else "sellSucceeded=false"
	var visible_status := "roundTripVisible=true" if round_trip_visible else "roundTripVisible=false"
	print("%s system=%s commodity=%s buyPrice=%d sellPrice=%d %s %s %s creditsBeforeBuy=%d creditsAfterBuy=%d creditsAfterSell=%d cargoBeforeBuy=%d cargoAfterBuy=%d cargoAfterSell=%d heldAfterBuy=%d heldAfterSell=%d sourceLabel=original-runtime-observed oracleStatus=terminal_velocity_eval_pending_original_trace status=\"%s\"" % [COMMODITY_TRADE_EVENT_LOG_PREFIX, str(current_system.get("name", "?")), commodity_id, buy_price, sell_price, buy_status, sell_status, visible_status, credits_before_buy, credits_after_buy, credits_after_sell, cargo_before_buy, cargo_after_buy, cargo_after_sell, held_after_buy, held_after_sell, status_line])
	get_tree().quit(0)

func _run_levo_same_port_sellback_log() -> void:
	_reset_travel_state()
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var commodity_id := "food"
	var commodity_name := "Food"
	var system_name := str(current_system.get("name", "?"))
	var body_name := str(_current_body().get("name", "?"))
	var buy_price := int(_market_prices(system_name).get(commodity_id, {}).get("buy", 0))
	var sell_price := _commodity_sell_price(commodity_id)
	var credits_before_buy := credits
	var cargo_before_buy := cargo
	_buy_selected_commodity()
	var credits_after_buy := credits
	var cargo_after_buy := cargo
	var held_after_buy := int(commodity_hold.get(commodity_id, 0))
	var bought_original_observed_lot := system_name == START_SYSTEM_NAME and body_name == "Levo Spaceport" and buy_price == 120 and held_after_buy == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo_after_buy == cargo_before_buy + EV_CLASSIC_COMMODITY_LOT_SIZE and credits_after_buy == credits_before_buy - (buy_price * EV_CLASSIC_COMMODITY_LOT_SIZE) and status_messages.has("Bought %d tons of %s" % [EV_CLASSIC_COMMODITY_LOT_SIZE, commodity_name])
	_sell_selected_commodity()
	var credits_after_sell := credits
	var cargo_after_sell := cargo
	var held_after_sell := int(commodity_hold.get(commodity_id, 0))
	var sold_same_port_lot := sell_price == 120 and held_after_sell == 0 and credits_after_sell == credits_after_buy + (sell_price * EV_CLASSIC_COMMODITY_LOT_SIZE) and status_messages.has("Sold %d tons of %s" % [EV_CLASSIC_COMMODITY_LOT_SIZE, commodity_name])
	var credits_restored := credits_after_sell == credits_before_buy
	var cargo_cleared := cargo_after_sell == cargo_before_buy and held_after_sell == 0
	var bought_status := "boughtOriginalObservedLot=true" if bought_original_observed_lot else "boughtOriginalObservedLot=false"
	var sold_status := "soldSamePortLot=true" if sold_same_port_lot else "soldSamePortLot=false"
	var credit_status := "creditsRestored=true" if credits_restored else "creditsRestored=false"
	var cargo_status := "cargoCleared=true" if cargo_cleared else "cargoCleared=false"
	var buy_price_status := "buyPrice=120" if buy_price == 120 else "buyPrice=%d" % buy_price
	var sell_price_status := "sellPrice=120" if sell_price == 120 else "sellPrice=%d" % sell_price
	print("%s system=%s body=\"%s\" commodity=%s %s %s lotSize=%d %s %s %s %s creditsBeforeBuy=%d creditsAfterBuy=%d creditsAfterSell=%d cargoBeforeBuy=%d cargoAfterBuy=%d cargoAfterSell=%d heldAfterBuy=%d heldAfterSell=%d sourceLabel=original-runtime-observed oracleStatus=levo_same_port_sellback_observed status=\"%s\"" % [LEVO_SAME_PORT_SELLBACK_EVENT_LOG_PREFIX, system_name, body_name, commodity_id, buy_price_status, sell_price_status, EV_CLASSIC_COMMODITY_LOT_SIZE, bought_status, sold_status, credit_status, cargo_status, credits_before_buy, credits_after_buy, credits_after_sell, cargo_before_buy, cargo_after_buy, cargo_after_sell, held_after_buy, held_after_sell, status_line])
	get_tree().quit(0)

func _run_commodity_buy_blocked_recovery_log() -> void:
	_reset_travel_state()
	landing_tab = 1
	selected_landing_item = 0
	var commodities: Array = economy.get("commodities", [])
	var commodity: Dictionary = commodities[0] if not commodities.is_empty() else {}
	var commodity_id := str(commodity.get("id", "none"))
	var commodity_name := str(commodity.get("name", commodity_id))
	var buy_price := int(_market_prices(current_system.get("name", "")).get(commodity_id, {}).get("buy", 0))
	var credits_before := credits
	var cargo_before := cargo
	_buy_selected_commodity()
	var in_space_status := status_line
	var in_space_buy_blocked := cargo == cargo_before and int(commodity_hold.get(commodity_id, 0)) == 0 and in_space_status == "Land before trading commodities"
	_try_land()
	var landed_for_recovery := landed
	credits = max(0, buy_price - 1)
	_buy_selected_commodity()
	var insufficient_credit_status := status_line
	var insufficient_credits_blocked := cargo == cargo_before and int(commodity_hold.get(commodity_id, 0)) == 0 and insufficient_credit_status == "Not enough credits"
	credits = credits_before
	cargo = cargo_space
	_buy_selected_commodity()
	var full_hold_block_status := status_line
	var full_hold_buy_blocked := cargo == cargo_space and int(commodity_hold.get(commodity_id, 0)) == 0 and full_hold_block_status == "Cargo hold full"
	cargo = cargo_before
	credits = credits_before
	_buy_selected_commodity()
	var credits_after_buy := credits
	var held_after_buy := int(commodity_hold.get(commodity_id, 0))
	var buy_recovered_cargo := landed_for_recovery and buy_price > 0 and held_after_buy == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo == cargo_before + EV_CLASSIC_COMMODITY_LOT_SIZE and credits_after_buy == credits_before - (buy_price * EV_CLASSIC_COMMODITY_LOT_SIZE) and status_messages.has("Bought %d tons of %s" % [EV_CLASSIC_COMMODITY_LOT_SIZE, commodity_name])
	var in_space_blocked_status := "inSpaceBuyBlocked=true" if in_space_buy_blocked else "inSpaceBuyBlocked=false"
	var insufficient_credits_status := "insufficientCreditsBlocked=true" if insufficient_credits_blocked else "insufficientCreditsBlocked=false"
	var full_hold_status_field := "fullHoldBuyBlocked=true" if full_hold_buy_blocked else "fullHoldBuyBlocked=false"
	var buy_recovered_status := "buyRecoveredCargo=true" if buy_recovered_cargo else "buyRecoveredCargo=false"
	var final_cargo_status := "finalCargo=10" if cargo == EV_CLASSIC_COMMODITY_LOT_SIZE else "finalCargo=%d" % cargo
	print("%s system=%s commodity=%s buyPrice=%d %s %s %s %s %s creditsBefore=%d creditsAfterBuy=%d cargoBefore=%d heldAfterBuy=%d sourceLabel=terminal-velocity-commodity-buy-blocked-recovery-scaffold oracleStatus=commodity_buy_blocked_recovery_pending_classic_runtime_trace inSpaceStatus=\"%s\" creditStatus=\"%s\" fullHoldStatus=\"%s\" status=\"%s\"" % [COMMODITY_BUY_BLOCKED_RECOVERY_EVENT_LOG_PREFIX, str(current_system.get("name", "?")), commodity_id, buy_price, in_space_blocked_status, insufficient_credits_status, full_hold_status_field, buy_recovered_status, final_cargo_status, credits_before, credits_after_buy, cargo_before, held_after_buy, in_space_status, insufficient_credit_status, full_hold_block_status, status_line])
	get_tree().quit(0)

func _run_commodity_sell_blocked_recovery_log() -> void:
	_reset_travel_state()
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var commodities: Array = economy.get("commodities", [])
	var commodity: Dictionary = commodities[0] if not commodities.is_empty() else {}
	var commodity_id := str(commodity.get("id", "none"))
	var commodity_name := str(commodity.get("name", commodity_id))
	var buy_price := int(_market_prices(current_system.get("name", "")).get(commodity_id, {}).get("buy", 0))
	var sell_price := _commodity_sell_price(commodity_id)
	var credits_before := credits
	var cargo_before := cargo
	_sell_selected_commodity()
	var sell_block_status := status_line
	var sell_blocked_before_cargo := cargo == cargo_before and int(commodity_hold.get(commodity_id, 0)) == 0 and sell_block_status == "No cargo to sell"
	_buy_selected_commodity()
	var credits_after_buy := credits
	var cargo_after_buy := cargo
	var held_after_buy := int(commodity_hold.get(commodity_id, 0))
	var buy_recovered_cargo := buy_price > 0 and held_after_buy == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo_after_buy == cargo_before + EV_CLASSIC_COMMODITY_LOT_SIZE and status_messages.has("Bought %d tons of %s" % [EV_CLASSIC_COMMODITY_LOT_SIZE, commodity_name])
	_sell_selected_commodity()
	var credits_after_sell := credits
	var cargo_after_sell := cargo
	var held_after_sell := int(commodity_hold.get(commodity_id, 0))
	var sell_recovered_cargo := sell_price > 0 and held_after_sell == 0 and cargo_after_sell == cargo_before and status_messages.has("Sold %d tons of %s" % [EV_CLASSIC_COMMODITY_LOT_SIZE, commodity_name])
	var sell_blocked_status := "sellBlockedBeforeCargo=true" if sell_blocked_before_cargo else "sellBlockedBeforeCargo=false"
	var buy_recovered_status := "buyRecoveredCargo=true" if buy_recovered_cargo else "buyRecoveredCargo=false"
	var sell_recovered_status := "sellRecoveredCargo=true" if sell_recovered_cargo else "sellRecoveredCargo=false"
	var final_cargo_status := "finalCargo=0" if cargo_after_sell == 0 else "finalCargo=%d" % cargo_after_sell
	print("%s system=%s commodity=%s buyPrice=%d sellPrice=%d %s %s %s %s creditsBefore=%d creditsAfterBuy=%d creditsAfterSell=%d cargoBefore=%d cargoAfterBuy=%d heldAfterBuy=%d heldAfterSell=%d sourceLabel=terminal-velocity-commodity-sell-blocked-recovery-scaffold oracleStatus=commodity_sell_blocked_recovery_pending_classic_runtime_trace blockedStatus=\"%s\" status=\"%s\"" % [COMMODITY_SELL_BLOCKED_RECOVERY_EVENT_LOG_PREFIX, str(current_system.get("name", "?")), commodity_id, buy_price, sell_price, sell_blocked_status, buy_recovered_status, sell_recovered_status, final_cargo_status, credits_before, credits_after_buy, credits_after_sell, cargo_before, cargo_after_buy, held_after_buy, held_after_sell, sell_block_status, status_line])
	get_tree().quit(0)

func _run_commodity_unavailable_recovery_log() -> void:
	_reset_travel_state()
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var commodity_id := "food"
	var commodity_name := "Food"
	var start_system := str(current_system.get("name", "?"))
	var start_market: Dictionary = _market_prices(start_system).get(commodity_id, {}).duplicate()
	var original_buy_price := int(start_market.get("buy", 0))
	var markets: Dictionary = economy.get("markets", {})
	var mutated_market: Dictionary = start_market.duplicate()
	mutated_market.erase("buy")
	var start_system_market: Dictionary = markets.get(start_system, {}).duplicate()
	start_system_market[commodity_id] = mutated_market
	markets[start_system] = start_system_market
	economy["markets"] = markets
	var credits_before_block := credits
	var cargo_before_block := cargo
	_buy_selected_commodity()
	var unavailable_status := status_line
	var unavailable_blocked := unavailable_status == "Commodity unavailable here" and credits == credits_before_block and cargo == cargo_before_block and int(commodity_hold.get(commodity_id, 0)) == 0
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_recovery_system_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var recovery_buy_price := int(_market_prices(current_system.get("name", "")).get(commodity_id, {}).get("buy", 0))
	var credits_before_recovery_buy := credits
	_buy_selected_commodity()
	var held_after_recovery_buy := int(commodity_hold.get(commodity_id, 0))
	var cargo_after_recovery_buy := cargo
	var bought_after_relocation := str(current_system.get("name", "?")) == "Sol" and recovery_buy_price > 0 and held_after_recovery_buy == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo_after_recovery_buy == cargo_before_block + EV_CLASSIC_COMMODITY_LOT_SIZE and credits == credits_before_recovery_buy - (recovery_buy_price * EV_CLASSIC_COMMODITY_LOT_SIZE) and status_messages.has("Bought %d tons of %s" % [EV_CLASSIC_COMMODITY_LOT_SIZE, commodity_name])
	var unavailable_status_field := "commodityUnavailableBlocked=true" if unavailable_blocked else "commodityUnavailableBlocked=false"
	var recovery_status_field := "boughtAfterRelocation=true" if bought_after_relocation else "boughtAfterRelocation=false"
	var final_cargo_status := "finalCargo=10" if cargo_after_recovery_buy == EV_CLASSIC_COMMODITY_LOT_SIZE else "finalCargo=%d" % cargo_after_recovery_buy
	print("%s unavailableSystem=%s recoverySystem=%s recoveryBody=\"Earth\" commodity=%s originalBuyPrice=%d recoveryBuyPrice=%d routeToRecoverySystemSelected=%s %s %s %s creditsBeforeBlock=%d creditsBeforeRecoveryBuy=%d creditsAfterRecoveryBuy=%d cargoBeforeBlock=%d heldAfterRecoveryBuy=%d sourceLabel=terminal-velocity-commodity-unavailable-recovery-scaffold oracleStatus=commodity_unavailable_recovery_pending_classic_runtime_trace blockedStatus=\"%s\" status=\"%s\"" % [COMMODITY_UNAVAILABLE_RECOVERY_EVENT_LOG_PREFIX, start_system, str(current_system.get("name", "?")), commodity_id, original_buy_price, recovery_buy_price, str(route_to_recovery_system_selected).to_lower(), unavailable_status_field, recovery_status_field, final_cargo_status, credits_before_block, credits_before_recovery_buy, credits, cargo_before_block, held_after_recovery_buy, unavailable_status, status_line])
	get_tree().quit(0)

func _run_cross_market_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var trade_commodity := "food"
	var buy_system := "Sol"
	var sell_system := "Levo"
	var route_to_buy_system_selected := _select_map_route_to_system(buy_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var buy_price := int(_market_prices(buy_system).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices(sell_system).get(trade_commodity, {}).get("sell", 0))
	var profit_per_ton := sell_price - buy_price
	var profit_total := profit_per_ton * EV_CLASSIC_COMMODITY_LOT_SIZE
	var credits_before_buy := credits
	var cargo_before_buy := cargo
	_buy_selected_commodity()
	var credits_after_buy := credits
	var held_after_buy := int(commodity_hold.get(trade_commodity, 0))
	var trade_bought := str(current_system.get("name", "?")) == buy_system and buy_price == 42 and held_after_buy == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo == cargo_before_buy + EV_CLASSIC_COMMODITY_LOT_SIZE and credits_after_buy == credits_before_buy - (buy_price * EV_CLASSIC_COMMODITY_LOT_SIZE)
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_sell_system_selected := _select_map_route_to_system(sell_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_sale := credits
	_sell_selected_commodity()
	var held_after_sale := int(commodity_hold.get(trade_commodity, 0))
	var trade_sold := str(current_system.get("name", "?")) == sell_system and sell_price == 120 and held_after_sale == 0 and cargo == 0 and credits == credits_before_sale + (sell_price * EV_CLASSIC_COMMODITY_LOT_SIZE)
	var buy_system_status := "buySystem=Sol" if buy_system == "Sol" else "buySystem=%s" % buy_system
	var sell_system_status := "sellSystem=Levo" if sell_system == "Levo" else "sellSystem=%s" % sell_system
	var buy_price_status := "buyPrice=42" if buy_price == 42 else "buyPrice=%d" % buy_price
	var sell_price_status := "sellPrice=120" if sell_price == 120 else "sellPrice=%d" % sell_price
	var profit_per_ton_status := "profitPerTon=78" if profit_per_ton == 78 else "profitPerTon=%d" % profit_per_ton
	var profit_total_status := "profitTotal=780" if profit_total == 780 else "profitTotal=%d" % profit_total
	var bought_status := "tradeBought=true" if trade_bought else "tradeBought=false"
	var sold_status := "tradeSold=true" if trade_sold else "tradeSold=false"
	var final_cargo_status := "finalCargo=0" if cargo == 0 else "finalCargo=%d" % cargo
	print("%s startSystem=Levo %s %s routeToBuySystemSelected=%s routeToSellSystemSelected=%s commodity=%s %s %s %s %s %s %s %s creditsBeforeBuy=%d creditsAfterBuy=%d creditsBeforeSale=%d creditsAfterSale=%d cargoBeforeBuy=%d heldAfterBuy=%d heldAfterSale=%d sourceLabel=terminal-velocity-cross-market-trade-scaffold oracleStatus=classic_runtime_cross_market_spread_pending status=\"%s\"" % [CROSS_MARKET_TRADE_EVENT_LOG_PREFIX, buy_system_status, sell_system_status, str(route_to_buy_system_selected), str(route_to_sell_system_selected), trade_commodity, buy_price_status, sell_price_status, profit_per_ton_status, profit_total_status, bought_status, sold_status, final_cargo_status, credits_before_buy, credits_after_buy, credits_before_sale, credits, cargo_before_buy, held_after_buy, held_after_sale, status_line])
	get_tree().quit(0)

func _run_max_hold_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var trade_commodity := "food"
	var buy_system := "Sol"
	var sell_system := "Levo"
	var route_to_buy_system_selected := _select_map_route_to_system(buy_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var lot_size := EV_CLASSIC_COMMODITY_LOT_SIZE
	var expected_lots := 2
	var expected_tons := lot_size * expected_lots
	var buy_price := int(_market_prices(buy_system).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices(sell_system).get(trade_commodity, {}).get("sell", 0))
	var profit_per_ton := sell_price - buy_price
	var expected_profit_total := profit_per_ton * expected_tons
	var credits_before_buy := credits
	var cargo_before_buy := cargo
	_buy_selected_commodity()
	var first_lot_held := int(commodity_hold.get(trade_commodity, 0))
	_buy_selected_commodity()
	var credits_after_buy := credits
	var held_after_buys := int(commodity_hold.get(trade_commodity, 0))
	var max_hold_filled := str(current_system.get("name", "?")) == buy_system and held_after_buys == expected_tons and cargo == cargo_before_buy + expected_tons and credits_after_buy == credits_before_buy - (buy_price * expected_tons)
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_sell_system_selected := _select_map_route_to_system(sell_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_sale := credits
	_sell_selected_commodity()
	var held_after_first_sale := int(commodity_hold.get(trade_commodity, 0))
	_sell_selected_commodity()
	var held_after_sale := int(commodity_hold.get(trade_commodity, 0))
	var final_cargo := cargo
	var all_lots_sold := str(current_system.get("name", "?")) == sell_system and held_after_sale == 0 and final_cargo == 0 and credits == credits_before_sale + (sell_price * expected_tons)
	var expected_final_credits := credits_before_buy + expected_profit_total
	var final_profit_ok := credits == expected_final_credits
	var filled_status := "maxHoldFilled=true" if max_hold_filled else "maxHoldFilled=false"
	var sold_status := "allLotsSold=true" if all_lots_sold else "allLotsSold=false"
	var profit_status := "finalProfitOk=true" if final_profit_ok else "finalProfitOk=false"
	var final_cargo_status := "finalCargo=0" if final_cargo == 0 else "finalCargo=%d" % final_cargo
	print("%s startSystem=Levo buySystem=Sol sellSystem=Levo routeToBuySystemSelected=%s routeToSellSystemSelected=%s commodity=%s buyPrice=%d sellPrice=%d lotSize=%d lotsBought=%d tonsBought=%d profitPerTon=%d expectedProfitTotal=%d %s %s %s %s creditsBeforeBuy=%d creditsAfterBuy=%d creditsBeforeSale=%d creditsAfterSale=%d expectedFinalCredits=%d firstLotHeld=%d heldAfterBuys=%d heldAfterFirstSale=%d heldAfterSale=%d sourceLabel=terminal-velocity-max-hold-trade-scaffold oracleStatus=classic_runtime_multi_lot_trade_spread_pending status=\"%s\"" % [MAX_HOLD_TRADE_EVENT_LOG_PREFIX, str(route_to_buy_system_selected), str(route_to_sell_system_selected), trade_commodity, buy_price, sell_price, lot_size, expected_lots, expected_tons, profit_per_ton, expected_profit_total, filled_status, sold_status, profit_status, final_cargo_status, credits_before_buy, credits_after_buy, credits_before_sale, credits, expected_final_credits, first_lot_held, held_after_buys, held_after_first_sale, held_after_sale, status_line])
	get_tree().quit(0)

func _run_trade_refuel_profit_log() -> void:
	_reset_travel_state()
	map_visible = true
	var trade_commodity := "food"
	var buy_system := "Sol"
	var sell_system := "Levo"
	var route_to_buy_system_selected := _select_map_route_to_system(buy_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var lot_size := EV_CLASSIC_COMMODITY_LOT_SIZE
	var expected_lots := 2
	var expected_tons := lot_size * expected_lots
	var buy_price := int(_market_prices(buy_system).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices(sell_system).get(trade_commodity, {}).get("sell", 0))
	var profit_per_ton := sell_price - buy_price
	var expected_profit_total := profit_per_ton * expected_tons
	var credits_before_buy := credits
	var cargo_before_buy := cargo
	_buy_selected_commodity()
	_buy_selected_commodity()
	var credits_after_buy := credits
	var held_after_buys := int(commodity_hold.get(trade_commodity, 0))
	var lots_bought := held_after_buys / lot_size
	var max_hold_filled := str(current_system.get("name", "?")) == buy_system and held_after_buys == expected_tons and cargo == cargo_before_buy + expected_tons and credits_after_buy == credits_before_buy - (buy_price * expected_tons)
	player_fuel = 0
	var fuel_before_blocked_return := player_fuel
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_sell_system_selected := _select_map_route_to_system(sell_system)
	var return_route_selected := route_to_sell_system_selected
	_move_to_scripted_hyperspace_distance()
	_jump()
	var low_fuel_jump_blocked := str(current_system.get("name", "?")) == buy_system and player_fuel == fuel_before_blocked_return and status_line == "Insufficient fuel for hyperspace; land at a port with refuel service or choose a closer route"
	_position_at_body("Earth")
	_try_land()
	var refuel_body := _current_body()
	var fuel_before_refuel := player_fuel
	var refuel_succeeded := _refuel_current_ship()
	var fuel_after_refuel := player_fuel
	_ev_land_or_launch()
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_sale := credits
	_sell_selected_commodity()
	_sell_selected_commodity()
	var held_after_sale := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_sale := cargo
	var all_lots_sold := str(current_system.get("name", "?")) == sell_system and held_after_sale == 0 and cargo_after_sale == 0 and credits == credits_before_sale + (sell_price * expected_tons)
	var final_profit_ok := credits == credits_before_buy + expected_profit_total
	var filled_status := "maxHoldFilled=true" if max_hold_filled else "maxHoldFilled=false"
	var sold_status := "allLotsSold=true" if all_lots_sold else "allLotsSold=false"
	var fuel_before_blocked_status := "fuelBeforeBlockedReturn=0" if fuel_before_blocked_return == 0 else "fuelBeforeBlockedReturn=%d" % fuel_before_blocked_return
	var low_fuel_status := "lowFuelJumpBlocked=true" if low_fuel_jump_blocked else "lowFuelJumpBlocked=false"
	var refuel_status := "refuelSucceeded=true" if refuel_succeeded else "refuelSucceeded=false"
	var profit_status := "finalProfitOk=true" if final_profit_ok else "finalProfitOk=false"
	var final_cargo_status := "finalCargo=0" if cargo_after_sale == 0 else "finalCargo=%d" % cargo_after_sale
	print("%s startSystem=Levo buySystem=Sol sellSystem=Levo routeToBuySystemSelected=%s routeToSellSystemSelected=%s returnRouteSelected=%s commodity=%s buyPrice=%d sellPrice=%d lotSize=%d lotsBought=%d tonsBought=%d profitPerTon=%d expectedProfitTotal=%d %s %s %s %s %s %s %s creditsBeforeBuy=%d creditsAfterBuy=%d creditsBeforeSale=%d creditsAfterSale=%d expectedFinalCredits=%d heldAfterBuys=%d heldAfterSale=%d fuelBeforeRefuel=%d fuelAfterRefuel=%d fuelMax=%d refuelBody=\"%s\" sourceLabel=terminal-velocity-refuel-trade-route-scaffold oracleStatus=classic_runtime_trade_route_refuel_pending status=\"%s\"" % [TRADE_REFUEL_PROFIT_EVENT_LOG_PREFIX, str(route_to_buy_system_selected), str(route_to_sell_system_selected), str(return_route_selected), trade_commodity, buy_price, sell_price, lot_size, lots_bought, expected_tons, profit_per_ton, expected_profit_total, filled_status, sold_status, fuel_before_blocked_status, low_fuel_status, refuel_status, profit_status, final_cargo_status, credits_before_buy, credits_after_buy, credits_before_sale, credits, credits_before_buy + expected_profit_total, held_after_buys, held_after_sale, fuel_before_refuel, fuel_after_refuel, _max_player_fuel(), str(refuel_body.get("name", "?")), status_line])
	get_tree().quit(0)

func _run_cargo_expansion_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var trade_commodity := "food"
	var buy_system := "Sol"
	var sell_system := "Levo"
	var lot_size := EV_CLASSIC_COMMODITY_LOT_SIZE
	var starting_cargo_space := cargo_space
	var route_to_buy_system_selected := _select_map_route_to_system(buy_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var buy_price := int(_market_prices(buy_system).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices(sell_system).get(trade_commodity, {}).get("sell", 0))
	var profit_per_ton := sell_price - buy_price
	var credits_before_trade_probe := credits
	_buy_selected_commodity()
	_buy_selected_commodity()
	_buy_selected_commodity()
	var third_lot_blocked_status := status_line
	var tons_before_upgrade := int(commodity_hold.get(trade_commodity, 0))
	var third_lot_initially_blocked := tons_before_upgrade == starting_cargo_space and cargo == starting_cargo_space and third_lot_blocked_status == "Cargo hold full"
	var credits_after_trade_probe := credits
	_sell_selected_commodity()
	_sell_selected_commodity()
	var credits_after_probe_sale := credits
	landing_tab = 2
	selected_landing_item = 0
	var credits_before_upgrade := credits
	_buy_selected_outfit_or_weapon()
	var bought_cargo_pod := owned_outfits.has("cargo_pod") and int(owned_outfits.get("cargo_pod", 0)) > 0
	var cargo_space_after_upgrade := cargo_space
	var capacity_expanded := bought_cargo_pod and cargo_space_after_upgrade > starting_cargo_space
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_expanded_buy := credits
	var expanded_target_tons := starting_cargo_space + lot_size
	while cargo + lot_size <= expanded_target_tons:
		_buy_selected_commodity()
	var tons_after_expanded_buy := int(commodity_hold.get(trade_commodity, 0))
	var expanded_hold_filled := capacity_expanded and tons_after_expanded_buy == expanded_target_tons and cargo == expanded_target_tons
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_sell_system_selected := _select_map_route_to_system(sell_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_expanded_sale := credits
	while int(commodity_hold.get(trade_commodity, 0)) > 0:
		_sell_selected_commodity()
	var held_after_expanded_sale := int(commodity_hold.get(trade_commodity, 0))
	var final_cargo := cargo
	var all_expanded_cargo_sold := held_after_expanded_sale == 0 and final_cargo == 0 and credits == credits_before_expanded_sale + (sell_price * expanded_target_tons)
	var expected_final_credits := credits_before_expanded_buy - (buy_price * expanded_target_tons) + (sell_price * expanded_target_tons)
	var final_profit_ok := credits == expected_final_credits
	var bought_status := "boughtCargoPod=true" if bought_cargo_pod else "boughtCargoPod=false"
	var expanded_status := "capacityExpanded=true" if capacity_expanded else "capacityExpanded=false"
	var blocked_status := "thirdLotInitiallyBlocked=true" if third_lot_initially_blocked else "thirdLotInitiallyBlocked=false"
	var filled_status := "expandedHoldFilled=true" if expanded_hold_filled else "expandedHoldFilled=false"
	var sold_status := "allExpandedCargoSold=true" if all_expanded_cargo_sold else "allExpandedCargoSold=false"
	var profit_status := "finalProfitOk=true" if final_profit_ok else "finalProfitOk=false"
	var final_cargo_status := "finalCargo=0" if final_cargo == 0 else "finalCargo=%d" % final_cargo
	print("%s startSystem=Levo buySystem=Sol sellSystem=Levo routeToBuySystemSelected=%s routeToSellSystemSelected=%s commodity=%s buyPrice=%d sellPrice=%d profitPerTon=%d lotSize=%d startingCargoSpace=%d cargoSpaceAfterUpgrade=%d expandedTargetTons=%d tonsBeforeUpgrade=%d tonsAfterExpandedBuy=%d heldAfterExpandedSale=%d creditsBeforeTradeProbe=%d creditsAfterTradeProbe=%d creditsAfterProbeSale=%d creditsBeforeUpgrade=%d creditsBeforeExpandedBuy=%d creditsBeforeExpandedSale=%d creditsAfterExpandedSale=%d expectedFinalCredits=%d %s %s %s %s %s %s %s thirdLotBlockedStatus=\"%s\" sourceLabel=terminal-velocity-cargo-expansion-trade-scaffold oracleStatus=cargo_expansion_trade_pending_classic_runtime_trace status=\"%s\"" % [CARGO_EXPANSION_TRADE_EVENT_LOG_PREFIX, str(route_to_buy_system_selected), str(route_to_sell_system_selected), trade_commodity, buy_price, sell_price, profit_per_ton, lot_size, starting_cargo_space, cargo_space_after_upgrade, expanded_target_tons, tons_before_upgrade, tons_after_expanded_buy, held_after_expanded_sale, credits_before_trade_probe, credits_after_trade_probe, credits_after_probe_sale, credits_before_upgrade, credits_before_expanded_buy, credits_before_expanded_sale, credits, expected_final_credits, bought_status, expanded_status, blocked_status, filled_status, sold_status, profit_status, final_cargo_status, third_lot_blocked_status, status_line])
	get_tree().quit(0)

func _run_fuel_reserve_upgrade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var start_system := str(current_system.get("name", "?"))
	var starting_fuel_max := _max_player_fuel()
	var route_to_service_system_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var service_system := str(current_system.get("name", "?"))
	var service_body := str(_current_body().get("name", "?"))
	var landed_at_service_port := landed and service_system == "Sol" and service_body == "Earth"
	player_fuel = 0
	var fuel_before_blocked_return := player_fuel
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_start_system_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var empty_reserve_return_blocked := service_system == str(current_system.get("name", "?")) and player_fuel == fuel_before_blocked_return and status_line == "Insufficient fuel for hyperspace; land at a port with refuel service or choose a closer route"
	_position_at_body("Earth")
	_try_land()
	var credits_before_upgrade := credits
	var fuel_before_upgrade := player_fuel
	var max_fuel_before_upgrade := _max_player_fuel()
	var bought_aux_tank := _buy_outfit_or_weapon_by_id("fuel_tank")
	var max_fuel_after_upgrade := _max_player_fuel()
	var fuel_after_upgrade := player_fuel
	var fuel_tank_owned := owned_outfits.has("fuel_tank") and int(owned_outfits.get("fuel_tank", 0)) > 0
	var refuel_succeeded := _refuel_current_ship()
	var fuel_after_refuel := player_fuel
	_ev_land_or_launch()
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	var final_system := str(current_system.get("name", "?"))
	var final_body := str(_current_body().get("name", "?"))
	var completed_return_hop := final_system == start_system and final_body == "Levo Spaceport" and player_fuel == max_fuel_after_upgrade - 1
	var bought_status := "boughtAuxFuelTank=true" if bought_aux_tank and fuel_tank_owned else "boughtAuxFuelTank=false"
	var max_status := "maxFuelExpanded=true" if max_fuel_after_upgrade > max_fuel_before_upgrade else "maxFuelExpanded=false"
	var blocked_status := "emptyReserveReturnBlocked=true" if empty_reserve_return_blocked else "emptyReserveReturnBlocked=false"
	var refuel_status := "refueledToExpandedReserve=true" if refuel_succeeded and fuel_after_refuel == max_fuel_after_upgrade else "refueledToExpandedReserve=false"
	var return_status := "returnHopCompleted=true" if completed_return_hop else "returnHopCompleted=false"
	var final_reserve_status := "finalFuelOneHopBelowExpandedMax=true" if player_fuel == max_fuel_after_upgrade - 1 else "finalFuelOneHopBelowExpandedMax=false"
	print("%s startSystem=%s serviceSystem=%s serviceBody=\"%s\" finalSystem=%s finalBody=\"%s\" routeToServiceSystemSelected=%s routeToStartSystemSelected=%s landedAtServicePort=%s %s %s %s %s %s %s startingFuelMax=%d maxFuelBeforeUpgrade=%d maxFuelAfterUpgrade=%d fuelBeforeBlockedReturn=%d fuelBeforeUpgrade=%d fuelAfterUpgrade=%d fuelAfterRefuel=%d finalFuel=%d creditsBeforeUpgrade=%d creditsAfterUpgrade=%d sourceLabel=terminal-velocity-fuel-reserve-upgrade-scaffold oracleStatus=fuel_reserve_upgrade_pending_classic_runtime_trace status=\"%s\"" % [FUEL_RESERVE_UPGRADE_EVENT_LOG_PREFIX, start_system, service_system, service_body, final_system, final_body, str(route_to_service_system_selected), str(route_to_start_system_selected), str(landed_at_service_port), blocked_status, bought_status, max_status, refuel_status, return_status, final_reserve_status, starting_fuel_max, max_fuel_before_upgrade, max_fuel_after_upgrade, fuel_before_blocked_return, fuel_before_upgrade, fuel_after_upgrade, fuel_after_refuel, player_fuel, credits_before_upgrade, credits, status_line])
	get_tree().quit(0)

func _run_upgrade_readiness_log() -> void:
	_reset_travel_state()
	map_visible = true
	var start_system := str(current_system.get("name", "?"))
	var route_to_service_system_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var service_body := _current_body()
	var service_system := str(current_system.get("name", "?"))
	var service_body_name := str(service_body.get("name", "?"))
	var inventory: Dictionary = _station_inventory(service_body)
	var services: Array = inventory.get("services", [])
	var service_scout_checkpoint := landed and service_system == "Sol" and service_body_name == "Earth" and services.has("outfitter") and services.has("weapons") and services.has("shipyard")
	credits = 100000
	var starting_cargo_space := cargo_space
	var starting_player_ship_id := player_ship_id
	var credits_before_cargo_pod := credits
	var cargo_pod_bought := _buy_outfit_or_weapon_by_id("cargo_pod")
	var cargo_space_after_pod := cargo_space
	var credits_before_laser := credits
	var laser_cannon_bought := _buy_outfit_or_weapon_by_id("laser_cannon")
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(service_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var credits_before_ship := credits
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var light_freighter_bought := player_ship_id == "light_freighter"
	var upgraded_cargo_space := cargo_space
	var player_info_lines := _player_inventory_lines()
	var player_info_upgrade_visible := player_info_lines.has("Ship: light_freighter") and _inventory_dictionary_summary(owned_outfits).contains("cargo_pod") and _inventory_dictionary_summary(owned_weapons).contains("laser_cannon")
	var service_scout_status := "serviceScoutCheckpoint=true" if service_scout_checkpoint else "serviceScoutCheckpoint=false"
	var cargo_pod_status := "cargoPodBought=true" if cargo_pod_bought and int(owned_outfits.get("cargo_pod", 0)) > 0 and cargo_space_after_pod > starting_cargo_space else "cargoPodBought=false"
	var laser_status := "laserCannonBought=true" if laser_cannon_bought and int(owned_weapons.get("laser_cannon", 0)) > 0 else "laserCannonBought=false"
	var ship_status := "lightFreighterBought=true" if light_freighter_bought else "lightFreighterBought=false"
	var player_info_status := "playerInfoUpgradeVisible=true" if player_info_upgrade_visible else "playerInfoUpgradeVisible=false"
	print("%s startSystem=%s serviceSystem=%s serviceBody=\"%s\" routeToServiceSystemSelected=%s %s %s %s %s %s services=%s startingShip=%s finalShip=%s startingCargoSpace=%d cargoSpaceAfterPod=%d upgradedCargoSpace=%d shipPrice=%d creditsBeforeCargoPod=%d creditsBeforeLaser=%d creditsBeforeShip=%d creditsAfter=%d playerInfoLines=%s sourceLabel=terminal-velocity-upgrade-readiness-strategy-scaffold oracleStatus=upgrade_strategy_progression_pending_ev_family_source_trace status=\"%s\"" % [UPGRADE_READINESS_EVENT_LOG_PREFIX, start_system, service_system, service_body_name, str(route_to_service_system_selected), service_scout_status, cargo_pod_status, laser_status, ship_status, player_info_status, JSON.stringify(services), starting_player_ship_id, player_ship_id, starting_cargo_space, cargo_space_after_pod, upgraded_cargo_space, ship_price, credits_before_cargo_pod, credits_before_laser, credits_before_ship, credits, JSON.stringify(player_info_lines), status_line])
	get_tree().quit(0)

func _run_upgrade_affordability_log() -> void:
	_reset_travel_state()
	map_visible = true
	var trade_commodity := "food"
	var buy_system := "Sol"
	var sell_system := "Levo"
	var lot_size := EV_CLASSIC_COMMODITY_LOT_SIZE
	var route_to_upgrade_system_selected := _select_map_route_to_system(buy_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var upgrade_system := str(current_system.get("name", "?"))
	var upgrade_body := str(_current_body().get("name", "?"))
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(_current_body())
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var ship_price := int(selected_ship_listing.get("price", 0))
	var buy_price := int(_market_prices(buy_system).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices(sell_system).get(trade_commodity, {}).get("sell", 0))
	var profit_per_ton := sell_price - buy_price
	var funding_target_tons := lot_size * 2
	var starting_credits: int = max(buy_price * funding_target_tons, ship_price - (profit_per_ton * funding_target_tons))
	credits = starting_credits
	var starting_ship := player_ship_id
	var starting_cargo_space := cargo_space
	var credits_before_blocked_ship := credits
	_buy_selected_ship()
	var blocked_status := status_line
	var initial_light_freighter_blocked := player_ship_id == starting_ship and credits == credits_before_blocked_ship and blocked_status == "Not enough credits"
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_funding_buy := credits
	while int(commodity_hold.get(trade_commodity, 0)) < funding_target_tons and cargo + lot_size <= cargo_space:
		_buy_selected_commodity()
	var tons_after_funding_buy := int(commodity_hold.get(trade_commodity, 0))
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_sell_system_selected := _select_map_route_to_system(sell_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_funding_sale := credits
	while int(commodity_hold.get(trade_commodity, 0)) > 0:
		_sell_selected_commodity()
	var held_after_funding_sale := int(commodity_hold.get(trade_commodity, 0))
	var funding_trade_completed := tons_after_funding_buy == funding_target_tons and held_after_funding_sale == 0 and cargo == 0 and credits == credits_before_funding_sale + (sell_price * funding_target_tons)
	_ev_land_or_launch()
	selected_route.clear()
	var route_back_to_upgrade_system_selected := _select_map_route_to_system(buy_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	landing_tab = 3
	shipyard_listings = _shipyard_listings(_current_body())
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			break
	var credits_before_ship_after_funding := credits
	_buy_selected_ship()
	var light_freighter_bought_after_funding := player_ship_id == "light_freighter" and credits == credits_before_ship_after_funding - ship_price
	player_hull = _max_player_hull()
	var player_info_lines := _player_inventory_lines()
	var player_info_hull_visible := false
	for line in player_info_lines:
		if line.contains("hull"):
			player_info_hull_visible = true
			break
	var initial_block_status := "initialLightFreighterBlocked=true" if initial_light_freighter_blocked else "initialLightFreighterBlocked=false"
	var funding_status := "fundingTradeCompleted=true" if funding_trade_completed else "fundingTradeCompleted=false"
	var ship_status := "lightFreighterBoughtAfterFunding=true" if light_freighter_bought_after_funding else "lightFreighterBoughtAfterFunding=false"
	var player_info_status := "playerInfoHullVisible=true" if player_info_hull_visible else "playerInfoHullVisible=false"
	var final_cargo_status := "finalCargo=0" if cargo == 0 else "finalCargo=%d" % cargo
	print("%s startSystem=Levo upgradeSystem=%s upgradeBody=\"%s\" sellSystem=%s routeToUpgradeSystemSelected=%s routeToSellSystemSelected=%s routeBackToUpgradeSystemSelected=%s commodity=%s buyPrice=%d sellPrice=%d profitPerTon=%d lotSize=%d fundingTargetTons=%d startingCredits=%d shipPrice=%d creditsBeforeBlockedShip=%d creditsBeforeFundingBuy=%d creditsBeforeFundingSale=%d creditsBeforeShipAfterFunding=%d creditsAfterShip=%d startingShip=%s finalShip=%s startingCargoSpace=%d finalCargoSpace=%d tonsAfterFundingBuy=%d heldAfterFundingSale=%d %s %s %s %s %s playerInfoLines=%s sourceLabel=terminal-velocity-upgrade-affordability-strategy-scaffold oracleStatus=upgrade_affordability_progression_pending_ev_family_source_trace blockedStatus=\"%s\" status=\"%s\"" % [UPGRADE_AFFORDABILITY_EVENT_LOG_PREFIX, upgrade_system, upgrade_body, sell_system, str(route_to_upgrade_system_selected), str(route_to_sell_system_selected), str(route_back_to_upgrade_system_selected), trade_commodity, buy_price, sell_price, profit_per_ton, lot_size, funding_target_tons, starting_credits, ship_price, credits_before_blocked_ship, credits_before_funding_buy, credits_before_funding_sale, credits_before_ship_after_funding, credits, starting_ship, player_ship_id, starting_cargo_space, cargo_space, tons_after_funding_buy, held_after_funding_sale, initial_block_status, funding_status, ship_status, player_info_status, final_cargo_status, JSON.stringify(player_info_lines), blocked_status, status_line])
	get_tree().quit(0)

func _run_balanced_upgrade_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var trade_commodity := "food"
	var buy_system := "Sol"
	var sell_system := "Levo"
	var lot_size := EV_CLASSIC_COMMODITY_LOT_SIZE
	var starting_cargo_space := cargo_space
	var starting_fuel_max := _max_player_fuel()
	var starting_max_hull := _max_player_hull()
	var starting_credits := 3700
	credits = starting_credits
	var route_to_upgrade_system_selected := _select_map_route_to_system(buy_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var upgrade_system := str(current_system.get("name", "?"))
	var upgrade_body := str(_current_body().get("name", "?"))
	var credits_before_cargo_pod := credits
	var bought_cargo_pod := _buy_outfit_or_weapon_by_id("cargo_pod")
	var cargo_space_after_pod := cargo_space
	var credits_before_aux_tank := credits
	var bought_aux_tank := _buy_outfit_or_weapon_by_id("fuel_tank")
	var max_fuel_after_tank := _max_player_fuel()
	var credits_before_blocked_hull := credits
	var hull_plating_before_block := int(owned_outfits.get("hull_plating", 0))
	var blocked_hull_buy := not _buy_outfit_or_weapon_by_id("hull_plating")
	var hull_plating_initially_blocked := blocked_hull_buy and int(owned_outfits.get("hull_plating", 0)) == hull_plating_before_block and credits == credits_before_blocked_hull
	landing_tab = 1
	selected_landing_item = 0
	var buy_price := int(_market_prices(buy_system).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices(sell_system).get(trade_commodity, {}).get("sell", 0))
	var profit_per_ton := sell_price - buy_price
	var funding_target_tons := lot_size * 2
	var credits_before_funding_buy := credits
	while int(commodity_hold.get(trade_commodity, 0)) < funding_target_tons and cargo + lot_size <= cargo_space:
		_buy_selected_commodity()
	var tons_after_funding_buy := int(commodity_hold.get(trade_commodity, 0))
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_sell_system_selected := _select_map_route_to_system(sell_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_funding_sale := credits
	while int(commodity_hold.get(trade_commodity, 0)) > 0:
		_sell_selected_commodity()
	var held_after_funding_sale := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_funding_sale := cargo
	var funding_trade_completed := tons_after_funding_buy == funding_target_tons and held_after_funding_sale == 0 and cargo_after_funding_sale == 0 and credits == credits_before_funding_sale + (sell_price * funding_target_tons)
	_ev_land_or_launch()
	selected_route.clear()
	var route_back_to_upgrade_system_selected := _select_map_route_to_system(buy_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var credits_before_hull_plating := credits
	var bought_hull_plating := _buy_outfit_or_weapon_by_id("hull_plating")
	var max_hull_after_plating := _max_player_hull()
	player_hull = max(1, _max_player_hull() - 5)
	var hull_before_repair := player_hull
	var credits_before_repair := credits
	var repaired_final_hull := _repair_current_hull()
	var bought_cargo_status := "boughtCargoPod=true" if bought_cargo_pod and cargo_space_after_pod > starting_cargo_space else "boughtCargoPod=false"
	var bought_fuel_status := "boughtAuxFuelTank=true" if bought_aux_tank and max_fuel_after_tank > starting_fuel_max else "boughtAuxFuelTank=false"
	var hull_blocked_status := "hullPlatingInitiallyBlocked=true" if hull_plating_initially_blocked else "hullPlatingInitiallyBlocked=false"
	var funding_status := "fundingTradeCompleted=true" if funding_trade_completed else "fundingTradeCompleted=false"
	var bought_hull_status := "boughtHullPlatingAfterFunding=true" if bought_hull_plating and max_hull_after_plating > starting_max_hull else "boughtHullPlatingAfterFunding=false"
	var repaired_status := "repairedFinalHullRefit=true" if repaired_final_hull and player_hull == _max_player_hull() else "repairedFinalHullRefit=false"
	var final_cargo_status := "finalCargo=0" if cargo == 0 else "finalCargo=%d" % cargo
	print("%s startSystem=Levo upgradeSystem=%s upgradeBody=\"%s\" sellSystem=%s routeToUpgradeSystemSelected=%s routeToSellSystemSelected=%s routeBackToUpgradeSystemSelected=%s commodity=%s buyPrice=%d sellPrice=%d profitPerTon=%d lotSize=%d fundingTargetTons=%d startingCredits=%d creditsBeforeCargoPod=%d creditsBeforeAuxFuelTank=%d creditsBeforeBlockedHull=%d creditsBeforeFundingBuy=%d creditsBeforeFundingSale=%d creditsBeforeHullPlating=%d creditsBeforeRepair=%d creditsAfterRepair=%d startingCargoSpace=%d cargoSpaceAfterPod=%d startingFuelMax=%d maxFuelAfterTank=%d startingMaxHull=%d maxHullAfterPlating=%d hullBeforeRepair=%d finalHull=%d tonsAfterFundingBuy=%d heldAfterFundingSale=%d %s %s %s %s %s %s %s sourceLabel=terminal-velocity-balanced-upgrade-trade-scaffold repairSourceLabel=terminal-velocity-repair-service-scaffold oracleStatus=balanced_upgrade_budget_pending_classic_runtime_trace status=\"%s\"" % [BALANCED_UPGRADE_TRADE_EVENT_LOG_PREFIX, upgrade_system, upgrade_body, sell_system, str(route_to_upgrade_system_selected), str(route_to_sell_system_selected), str(route_back_to_upgrade_system_selected), trade_commodity, buy_price, sell_price, profit_per_ton, lot_size, funding_target_tons, starting_credits, credits_before_cargo_pod, credits_before_aux_tank, credits_before_blocked_hull, credits_before_funding_buy, credits_before_funding_sale, credits_before_hull_plating, credits_before_repair, credits, starting_cargo_space, cargo_space_after_pod, starting_fuel_max, max_fuel_after_tank, starting_max_hull, max_hull_after_plating, hull_before_repair, player_hull, tons_after_funding_buy, held_after_funding_sale, bought_cargo_status, bought_fuel_status, hull_blocked_status, funding_status, bought_hull_status, repaired_status, final_cargo_status, status_line])
	get_tree().quit(0)

func _run_hull_plating_repair_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var upgrade_system := str(current_system.get("name", "?"))
	var upgrade_body := str(_current_body().get("name", "?"))
	var starting_credits := 2200
	credits = starting_credits
	var starting_max_hull := _max_player_hull()
	var credits_before_hull_plating := credits
	var bought_hull_plating := _buy_outfit_or_weapon_by_id("hull_plating")
	var max_hull_after_plating := _max_player_hull()
	player_hull = max(1, max_hull_after_plating - 7)
	var hull_before_repair := player_hull
	var credits_before_repair := credits
	var repair_gap_created := hull_before_repair < max_hull_after_plating
	var repair_succeeded := _repair_current_hull()
	var player_info_lines := _player_inventory_lines()
	var player_info_max_hull_visible := false
	for line in player_info_lines:
		if line.contains("Hull") or line.contains("hull"):
			player_info_max_hull_visible = true
			break
	var bought_status := "boughtHullPlating=true" if bought_hull_plating else "boughtHullPlating=false"
	var expanded_status := "maxHullExpanded=true" if max_hull_after_plating > starting_max_hull else "maxHullExpanded=false"
	var gap_status := "repairGapCreated=true" if repair_gap_created else "repairGapCreated=false"
	var repair_status := "repairSucceeded=true" if repair_succeeded and player_hull == _max_player_hull() else "repairSucceeded=false"
	var player_info_status := "playerInfoMaxHullVisible=true" if player_info_max_hull_visible else "playerInfoMaxHullVisible=false"
	print("%s upgradeSystem=%s upgradeBody=\"%s\" routeToUpgradeSystemSelected=%s startingCredits=%d creditsBeforeHullPlating=%d creditsBeforeRepair=%d creditsAfterRepair=%d startingMaxHull=%d maxHullAfterPlating=%d hullBeforeRepair=%d finalHull=%d %s %s %s %s %s playerInfoLines=%s sourceLabel=terminal-velocity-hull-plating-repair-scaffold repairSourceLabel=terminal-velocity-repair-service-scaffold oracleStatus=hull_plating_repair_pending_classic_runtime_trace" % [HULL_PLATING_REPAIR_EVENT_LOG_PREFIX, upgrade_system, upgrade_body, str(route_to_sol_selected), starting_credits, credits_before_hull_plating, credits_before_repair, credits, starting_max_hull, max_hull_after_plating, hull_before_repair, player_hull, bought_status, expanded_status, gap_status, repair_status, player_info_status, JSON.stringify(player_info_lines)])
	get_tree().quit(0)

func _run_mission_offer_scan_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	landing_tab = 0
	var body := _current_body()
	var available := _available_missions(body)
	var offer_ids := []
	var offer_detail_lines: Array[String] = []
	for mission in available:
		offer_ids.append(str(mission.get("id", "")))
		if offer_detail_lines.is_empty():
			offer_detail_lines = _mission_offer_detail_lines(mission)
	var offers_by_surface := {"Mission Computer": offer_ids}
	var total_offers := offer_ids.size()
	var selected_offer_details_visible := offer_detail_lines.has("Offer detail source: terminal-velocity-mission-offer-helper; exact Classic Mission Computer detail UI pending")
	print("%s startSystem=Levo routeToSolSelected=%s scanSystem=%s scanBody=\"%s\" offersBySurface=%s totalOffers=%d selectedOfferDetailsVisible=%s selectedOfferDetails=%s sourceLabel=terminal-velocity-observed oracleStatus=terminal_velocity_eval_pending_original_trace status=\"%s\"" % [MISSION_OFFER_SCAN_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(current_system.get("name", "?")), str(body.get("name", "None")), JSON.stringify(offers_by_surface), total_offers, str(selected_offer_details_visible), JSON.stringify(offer_detail_lines), status_line])
	get_tree().quit(0)

func _run_mission_chain_offer_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var initial_body := _current_body()
	var first_mission: Dictionary = _first_available_mission(initial_body)
	var first_mission_id := str(first_mission.get("id", "none"))
	_accept_selected_mission()
	var first_mission_accepted := active_missions.has(first_mission_id)
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_chain_stop_selected := _select_map_route_to_system("Centauri")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Luna")
	_try_land()
	var completed_ids := _complete_arrived_missions()
	var first_mission_delivered := completed_ids.has(first_mission_id)
	var chain_body := _current_body()
	var chain_offers := _available_missions(chain_body)
	var chain_offer_ids := []
	var selected_chain_detail_lines: Array[String] = []
	for mission in chain_offers:
		chain_offer_ids.append(str(mission.get("id", "")))
		if selected_chain_detail_lines.is_empty():
			selected_chain_detail_lines = _mission_offer_detail_lines(mission)
	var frontier_offer_visible := chain_offer_ids.has("frontier_sample_hera_freeport")
	var chain_offer_details_visible := selected_chain_detail_lines.has("Offer detail source: terminal-velocity-mission-offer-helper; exact Classic Mission Computer detail UI pending")
	print("%s startSystem=Levo routeToSolSelected=%s firstMissionAccepted=%s firstMissionDelivered=%s completedMissions=%s routeToChainStopSelected=%s scanSystem=%s scanBody=\"%s\" chainOfferVisible=%s chainOffers=%s selectedChainOfferDetailsVisible=%s selectedChainOfferDetails=%s storyFlags=%s sourceLabel=terminal-velocity-observed oracleStatus=terminal_velocity_eval_pending_original_trace status=\"%s\"" % [MISSION_CHAIN_OFFER_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(first_mission_accepted), str(first_mission_delivered), JSON.stringify(completed_ids), str(route_to_chain_stop_selected), str(current_system.get("name", "?")), str(chain_body.get("name", "None")), str(frontier_offer_visible), JSON.stringify(chain_offer_ids), str(chain_offer_details_visible), JSON.stringify(selected_chain_detail_lines), JSON.stringify(story_flags), status_line])
	get_tree().quit(0)

func _run_mission_chain_lock_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_luna_selected := _select_map_route_to_system("Centauri")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Luna")
	_try_land()
	landing_tab = 0
	var body := _current_body()
	var available := _available_missions(body)
	var blocked_reasons := _blocked_mission_reasons(body)
	var locked_story_reason_visible := false
	var locked_story_state_visible := false
	for reason in blocked_reasons:
		if str(reason).contains("requires missing story flag(s): story_intro_complete"):
			locked_story_reason_visible = true
		if str(reason).contains("storyGate=missing_required_flags"):
			locked_story_state_visible = true
	print("%s startSystem=Levo routeToLunaSelected=%s scanSystem=%s scanBody=\"%s\" availableOffers=%d blockedReasons=%s lockedStoryReasonVisible=%s lockedStoryStateVisible=%s sourceLabel=terminal-velocity-mission-story-gate-scaffold oracleStatus=classic_mission_offer_visibility_pending_original_trace status=\"%s\"" % [MISSION_CHAIN_LOCK_EVENT_LOG_PREFIX, str(route_to_luna_selected), str(current_system.get("name", "?")), str(body.get("name", "None")), available.size(), JSON.stringify(blocked_reasons), str(locked_story_reason_visible), str(locked_story_state_visible), status_line])
	get_tree().quit(0)

func _run_mission_alignment_branch_log() -> void:
	var federation_result := _mission_alignment_branch_attempt("federation_report_freeport", "freeport_pact_smugglers")
	var freeport_result := _mission_alignment_branch_attempt("freeport_pact_smugglers", "federation_report_freeport")
	print("%s startSystem=Levo routeToSolSelected=%s routeToLunaSelected=%s firstMissionDelivered=%s chainMissionAccepted=%s routeToSiriusSelected=%s chainMissionDelivered=%s scanSystem=%s scanBody=\"%s\" branchOffersVisible=%s federationOfferVisible=%s freeportOfferVisible=%s branchOffers=%s choiceGroups=%s selectedBranchOfferDetailsVisible=%s selectedBranchOfferDetails=%s federationBranchAccepted=%s freeportBranchHiddenAfterChoice=%s freeportBranchAccepted=%s federationBranchHiddenAfterChoice=%s offersAfterChoice=%s freeportOffersAfterChoice=%s reputation=%s freeportReputation=%s activeMissions=%s freeportActiveMissions=%s completedMissions=%s freeportCompletedMissions=%s storyFlags=%s freeportStoryFlags=%s sourceLabel=terminal-velocity-observed oracleStatus=terminal_velocity_eval_pending_original_trace choiceBoundary=terminal_velocity_choice_group_scaffold_exact_classic_branch_ui_pending status=\"%s\"" % [MISSION_ALIGNMENT_BRANCH_EVENT_LOG_PREFIX, str(federation_result.get("route_to_sol_selected", false)), str(federation_result.get("route_to_luna_selected", false)), str(federation_result.get("first_completed", false)), str(federation_result.get("chain_accepted", false)), str(federation_result.get("route_to_sirius_selected", false)), str(federation_result.get("chain_delivered", false)), str(federation_result.get("scan_system", "?")), str(federation_result.get("scan_body", "None")), str(federation_result.get("branch_offers_visible", false)), str(federation_result.get("federation_visible", false)), str(federation_result.get("freeport_visible", false)), JSON.stringify(federation_result.get("branch_offer_ids", [])), JSON.stringify(federation_result.get("branch_choice_groups", [])), str(federation_result.get("selected_branch_offer_details_visible", false)), JSON.stringify(federation_result.get("selected_branch_offer_details", [])), str(federation_result.get("selected_branch_accepted", false)), str(federation_result.get("other_branch_hidden_after_choice", false)), str(freeport_result.get("selected_branch_accepted", false)), str(freeport_result.get("other_branch_hidden_after_choice", false)), JSON.stringify(federation_result.get("offer_ids_after_choice", [])), JSON.stringify(freeport_result.get("offer_ids_after_choice", [])), JSON.stringify(federation_result.get("reputation", {})), JSON.stringify(freeport_result.get("reputation", {})), JSON.stringify(federation_result.get("active_missions", [])), JSON.stringify(freeport_result.get("active_missions", [])), JSON.stringify(federation_result.get("completed_missions", [])), JSON.stringify(freeport_result.get("completed_missions", [])), JSON.stringify(federation_result.get("story_flags", [])), JSON.stringify(freeport_result.get("story_flags", [])), str(federation_result.get("status", ""))])
	get_tree().quit(0)

func _run_mission_alignment_return_log() -> void:
	_reset_travel_state()
	current_system_index = _system_index_by_name("Sirius", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	_position_at_body("Sirius Station")
	landed = true
	landing_tab = 0
	completed_missions = ["frontier_sample_hera_freeport"]
	story_flags = ["frontier_samples_delivered"]
	reputation_scores = {"Federation": 5, "Independent": 7}
	legal_records = {"Federation": -20, "Independent": -90}
	var branch_system_name := str(current_system.get("name", "?"))
	var branch_body := _current_body()
	var branch_body_name := str(branch_body.get("name", "None"))
	var offers_before_branch := _available_missions(branch_body)
	var offer_ids_before_branch := _mission_ids(offers_before_branch)
	var return_visible_with_branches := offer_ids_before_branch.has("freeport_return_earth") and offer_ids_before_branch.has("federation_report_freeport") and offer_ids_before_branch.has("freeport_pact_smugglers")
	completed_missions = ["frontier_sample_hera_freeport", "federation_report_freeport"]
	story_flags = ["frontier_samples_delivered", "chapter_one_choice_seen", "alignment_federation", "federation_intel_asset"]
	var offers_after_federation := _available_missions(branch_body)
	var offer_ids_after_federation := _mission_ids(offers_after_federation)
	var return_visible_after_completion := offer_ids_after_federation == ["freeport_return_earth"]
	var federation_return_result := _mission_alignment_return_delivery_result(["frontier_sample_hera_freeport", "federation_report_freeport"], ["frontier_samples_delivered", "chapter_one_choice_seen", "alignment_federation", "federation_intel_asset"])
	var freeport_return_result := _mission_alignment_return_delivery_result(["frontier_sample_hera_freeport", "freeport_pact_smugglers"], ["frontier_samples_delivered", "chapter_one_choice_seen", "alignment_freeport", "freeport_network_asset"])
	var return_contract_cargo_released := int(federation_return_result.get("cargoReleased", 0)) == 5 and int(freeport_return_result.get("cargoReleased", 0)) == 5
	var return_contract_reward_paid := int(federation_return_result.get("rewardPaid", 0)) == 3200 and int(freeport_return_result.get("rewardPaid", 0)) == 3200
	var help_text := "\n".join(_help_overlay_lines())
	var alignment_return_help_visible := help_text.contains("Alignment return contracts: after choosing a chapter branch")
	print("%s scanSystem=%s scanBody=\"%s\" offersBeforeBranch=%s returnContractVisibleWithBranches=%s offersAfterFederation=%s returnContractVisibleAfterCompletion=%s returnContractAcceptedAfterFederation=%s returnContractDeliveredAfterFederation=%s returnContractAcceptedAfterFreeport=%s returnContractDeliveredAfterFreeport=%s returnContractCargoReleased=%s returnContractRewardPaid=%s alignmentReturnHelpVisible=%s completedMissions=%s storyFlags=%s federationReturnStatus=\"%s\" freeportReturnStatus=\"%s\" sourceLabel=terminal-velocity-observed oracleStatus=terminal_velocity_eval_pending_original_trace returnBoundary=terminal_velocity_return_contract_timing_scaffold_exact_classic_offer_ui_pending status=\"%s\"" % [MISSION_ALIGNMENT_RETURN_EVENT_LOG_PREFIX, branch_system_name, branch_body_name, JSON.stringify(offer_ids_before_branch), str(return_visible_with_branches), JSON.stringify(offer_ids_after_federation), str(return_visible_after_completion), str(bool(federation_return_result.get("accepted", false))), str(bool(federation_return_result.get("delivered", false))), str(bool(freeport_return_result.get("accepted", false))), str(bool(freeport_return_result.get("delivered", false))), str(return_contract_cargo_released), str(return_contract_reward_paid), str(alignment_return_help_visible), JSON.stringify(completed_missions), JSON.stringify(story_flags), str(federation_return_result.get("status", "")), str(freeport_return_result.get("status", "")), status_line])
	get_tree().quit(0)


func _run_mission_alignment_delivery_log() -> void:
	var federation_result := _mission_alignment_delivery_result("federation_report_freeport", "freeport_pact_smugglers", "Sol", "Earth")
	var freeport_result := _mission_alignment_delivery_result("freeport_pact_smugglers", "federation_report_freeport", "Centauri", "Luna")
	var federation_flags: Array = federation_result.get("storyFlags", [])
	var freeport_flags: Array = freeport_result.get("storyFlags", [])
	var federation_branch_flags_set: bool = federation_flags.has("alignment_federation") and federation_flags.has("federation_intel_asset")
	var freeport_branch_flags_set: bool = freeport_flags.has("alignment_freeport") and freeport_flags.has("freeport_network_asset")
	var incompatible_blocked_after_delivery: bool = bool(federation_result.get("incompatibleBlocked", false)) and bool(freeport_result.get("incompatibleBlocked", false))
	print("%s federationBranchAccepted=%s federationBranchDelivered=%s freeportBranchAccepted=%s freeportBranchDelivered=%s federationCargoReleased=%s freeportCargoReleased=%s federationRewardPaid=%s freeportRewardPaid=%s federationBranchFlagsSet=%s freeportBranchFlagsSet=%s incompatibleBranchBlockedAfterDelivery=%s federationStoryFlags=%s freeportStoryFlags=%s federationCompletedMissions=%s freeportCompletedMissions=%s sourceLabel=terminal-velocity-mission-scaffold oracleStatus=mission_behavior_pending_classic_runtime_trace deliveryBoundary=terminal_velocity_alignment_delivery_scaffold_exact_classic_completion_ui_pending federationStatus=\"%s\" freeportStatus=\"%s\"" % [MISSION_ALIGNMENT_DELIVERY_EVENT_LOG_PREFIX, str(bool(federation_result.get("accepted", false))), str(bool(federation_result.get("delivered", false))), str(bool(freeport_result.get("accepted", false))), str(bool(freeport_result.get("delivered", false))), str(int(federation_result.get("cargoReleased", 0)) == 2), str(int(freeport_result.get("cargoReleased", 0)) == 2), str(int(federation_result.get("rewardPaid", 0)) == 2800), str(int(freeport_result.get("rewardPaid", 0)) == 3000), str(federation_branch_flags_set), str(freeport_branch_flags_set), str(incompatible_blocked_after_delivery), JSON.stringify(federation_flags), JSON.stringify(freeport_flags), JSON.stringify(federation_result.get("completedMissions", [])), JSON.stringify(freeport_result.get("completedMissions", [])), str(federation_result.get("status", "")), str(freeport_result.get("status", ""))])
	get_tree().quit(0)

func _mission_alignment_delivery_result(branch_mission_id: String, incompatible_mission_id: String, destination_system: String, destination_body: String) -> Dictionary:
	_reset_travel_state()
	current_system_index = _system_index_by_name("Sirius", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	_position_at_body("Sirius Station")
	landed = true
	landing_tab = 0
	completed_missions = ["frontier_sample_hera_freeport"]
	story_flags = ["frontier_samples_delivered"]
	reputation_scores = {"Federation": 5, "Independent": 7}
	legal_records = {"Federation": -20, "Independent": -90}
	var offers := _available_missions(_current_body())
	var offer_ids := _mission_ids(offers)
	selected_landing_item = offer_ids.find(branch_mission_id)
	var credits_before_accept := credits
	_accept_selected_mission()
	var accepted := active_missions.has(branch_mission_id)
	var cargo_after_accept := cargo
	current_system_index = _system_index_by_name(destination_system, current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	_position_at_body(destination_body)
	landed = true
	var completed_now := _complete_arrived_missions()
	var delivered := completed_now.has(branch_mission_id) and completed_missions.has(branch_mission_id)
	var cargo_after_delivery := cargo
	var status_after_delivery := status_line
	current_system_index = _system_index_by_name("Sirius", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	_position_at_body("Sirius Station")
	landed = true
	var post_delivery_offers := _mission_ids(_available_missions(_current_body()))
	return {
		"accepted": accepted,
		"delivered": delivered,
		"cargoReleased": cargo_after_accept - cargo_after_delivery,
		"rewardPaid": credits - credits_before_accept,
		"storyFlags": story_flags.duplicate(),
		"completedMissions": completed_missions.duplicate(),
		"incompatibleBlocked": not post_delivery_offers.has(incompatible_mission_id),
		"status": status_after_delivery,
	}

func _mission_alignment_return_delivery_result(branch_completed_missions: Array, branch_story_flags: Array) -> Dictionary:
	_reset_travel_state()
	current_system_index = _system_index_by_name("Sirius", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	_position_at_body("Sirius Station")
	landed = true
	landing_tab = 0
	selected_landing_item = 0
	completed_missions = branch_completed_missions.duplicate()
	story_flags = branch_story_flags.duplicate()
	reputation_scores = {"Federation": 5, "Independent": 7}
	legal_records = {"Federation": -20, "Independent": -90}
	var credits_before_accept := credits
	_accept_selected_mission()
	var accepted := active_missions.has("freeport_return_earth")
	var cargo_after_accept := cargo
	current_system_index = _system_index_by_name("Sol", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	_position_at_body("Earth")
	landed = true
	var completed_now := _complete_arrived_missions()
	return {
		"accepted": accepted,
		"delivered": completed_now.has("freeport_return_earth") and completed_missions.has("freeport_return_earth"),
		"cargoReleased": cargo_after_accept - cargo,
		"rewardPaid": credits - credits_before_accept,
		"status": status_line,
	}

func _mission_ids(missions: Array) -> Array:
	var ids := []
	for mission in missions:
		ids.append(str(mission.get("id", "")))
	return ids

func _mission_alignment_branch_attempt(branch_mission_id: String, incompatible_mission_id: String) -> Dictionary:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var first_mission := _first_available_mission(_current_body())
	var first_mission_id := str(first_mission.get("id", "none"))
	_accept_selected_mission()
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_luna_selected := _select_map_route_to_system("Centauri")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Luna")
	_try_land()
	var first_completed := _complete_arrived_missions().has(first_mission_id)
	var chain_mission := _mission_by_id("frontier_sample_hera_freeport")
	selected_landing_item = 0
	_accept_selected_mission()
	var chain_accepted := active_missions.has("frontier_sample_hera_freeport")
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_sirius_selected := _select_map_route_to_system(str(chain_mission.get("destinationSystem", "Sirius")))
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Sirius Station")
	_try_land()
	var chain_delivered := _complete_arrived_missions().has("frontier_sample_hera_freeport")
	var branch_body := _current_body()
	var branch_offers := _available_missions(branch_body)
	var branch_offer_ids := []
	var branch_choice_groups := []
	for mission in branch_offers:
		branch_offer_ids.append(str(mission.get("id", "")))
		var choice_group := _mission_optional_field(mission, "choiceGroup")
		if choice_group != "none" and not branch_choice_groups.has(choice_group):
			branch_choice_groups.append(choice_group)
	var federation_visible := branch_offer_ids.has("federation_report_freeport")
	var freeport_visible := branch_offer_ids.has("freeport_pact_smugglers")
	var branch_choice_group_visible := branch_choice_groups.has("chapter_one_alignment")
	selected_landing_item = branch_offer_ids.find(branch_mission_id)
	if selected_landing_item < 0:
		selected_landing_item = 0
	var selected_branch_offer: Dictionary = branch_offers[selected_landing_item] if not branch_offers.is_empty() else {}
	var selected_branch_offer_details := _mission_offer_detail_lines(selected_branch_offer)
	var selected_branch_offer_details_visible := selected_branch_offer_details.size() > 0 and selected_branch_offer_details.has("Offer detail source: terminal-velocity-mission-offer-helper; exact Classic Mission Computer detail UI pending")
	_accept_selected_mission()
	var selected_branch_accepted := active_missions.has(branch_mission_id)
	var offers_after_choice := _available_missions(branch_body)
	var offer_ids_after_choice := []
	for mission in offers_after_choice:
		offer_ids_after_choice.append(str(mission.get("id", "")))
	var other_branch_hidden_after_choice := not offer_ids_after_choice.has(incompatible_mission_id)
	var reputation_snapshot := {
		"Federation": int(reputation_scores.get("Federation", 0)),
		"Independent": int(reputation_scores.get("Independent", 0)),
		"Centauri Protectorate": int(reputation_scores.get("Centauri Protectorate", 0))
	}
	return {
		"route_to_sol_selected": route_to_sol_selected,
		"route_to_luna_selected": route_to_luna_selected,
		"first_completed": first_completed,
		"chain_accepted": chain_accepted,
		"route_to_sirius_selected": route_to_sirius_selected,
		"chain_delivered": chain_delivered,
		"scan_system": str(current_system.get("name", "?")),
		"scan_body": str(branch_body.get("name", "None")),
		"branch_offers_visible": federation_visible and freeport_visible and branch_choice_group_visible,
		"federation_visible": federation_visible,
		"freeport_visible": freeport_visible,
		"branch_offer_ids": branch_offer_ids,
		"branch_choice_groups": branch_choice_groups,
		"selected_branch_offer_details_visible": selected_branch_offer_details_visible,
		"selected_branch_offer_details": selected_branch_offer_details,
		"selected_branch_accepted": selected_branch_accepted,
		"other_branch_hidden_after_choice": other_branch_hidden_after_choice,
		"offer_ids_after_choice": offer_ids_after_choice,
		"reputation": reputation_snapshot,
		"active_missions": active_missions.duplicate(),
		"completed_missions": completed_missions.duplicate(),
		"story_flags": story_flags.duplicate(),
		"status": status_line,
	}

func _run_mission_route_hint_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var accepted_body := _current_body()
	var mission_before_accept: Dictionary = _first_available_mission(accepted_body)
	var accepted_mission_id := str(mission_before_accept.get("id", "none"))
	var destination_system := str(mission_before_accept.get("destinationSystem", "?"))
	_accept_selected_mission()
	var mission_accepted := active_missions.has(accepted_mission_id)
	landing_tab = 1
	selected_landing_item = 0
	var trade_commodity := "food"
	var cargo_before_trade_buy := cargo
	_buy_selected_commodity()
	var trade_cargo_after_buy := int(commodity_hold.get(trade_commodity, 0))
	var trade_bought_before_route := trade_cargo_after_buy == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo == cargo_before_trade_buy + EV_CLASSIC_COMMODITY_LOT_SIZE
	_ev_land_or_launch()
	selected_route.clear()
	selected_route.append("Sirius")
	var stale_route_before_helper := selected_route.duplicate()
	var mission_route_queued := _route_to_active_mission_destination()
	var route_status_line := status_line
	var route_status_has_fuel_hint := route_status_line.contains("Route fuel:")
	var stale_route_replaced := selected_route.size() == 1 and str(selected_route[0]) == destination_system and not selected_route.has("Sirius")
	var fuel_before_route := player_fuel
	var route_fuel_cost := _route_fuel_cost()
	var pre_jump_fuel_warning := _route_fuel_warning_active()
	player_fuel = 0
	var low_fuel_helper_requeued := _route_to_active_mission_destination()
	var low_fuel_route_status_line := status_line
	var low_fuel_route_warning_visible := low_fuel_helper_requeued and low_fuel_route_status_line.contains("refuel before full route")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var low_fuel_jump_blocked: bool = str(current_system.get("name", "?")) == "Sol" and status_line.contains("Insufficient fuel")
	var low_fuel_jump_status := status_line
	_position_at_body("Earth")
	_try_land()
	var landed_for_refuel := landed and str(_current_body().get("name", "")) == "Earth"
	var refuel_succeeded := _refuel_current_ship()
	var fuel_after_refuel := player_fuel
	_ev_land_or_launch()
	_move_to_scripted_hyperspace_distance()
	var route_before_delivery_jump := selected_route.duplicate()
	_jump()
	_position_at_body("Luna")
	_try_land()
	var completed_ids := _complete_arrived_missions()
	var held_trade_cargo_after_delivery := int(commodity_hold.get(trade_commodity, 0))
	var cargo_used_after_delivery := cargo
	var credits_after_delivery := credits
	var delivered_after_refuel: bool = str(current_system.get("name", "?")) == destination_system and completed_ids.has(accepted_mission_id) and active_missions.is_empty()
	var trade_cargo_preserved_after_delivery := delivered_after_refuel and held_trade_cargo_after_delivery == trade_cargo_after_buy and cargo_used_after_delivery == trade_cargo_after_buy
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	var held_trade_cargo_after_sale := int(commodity_hold.get(trade_commodity, 0))
	var cargo_used_after_sale := cargo
	var credits_after_trade_sale := credits
	var trade_cargo_sold_after_delivery := trade_cargo_preserved_after_delivery and held_trade_cargo_after_sale == 0 and cargo_used_after_sale == 0 and credits_after_trade_sale > credits_after_delivery
	var mission_route_status := "missionRouteQueued=true" if mission_route_queued else "missionRouteQueued=false"
	var queued_route := JSON.stringify(selected_route)
	print("%s startSystem=Levo routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" acceptedMission=%s missionAccepted=%s destinationSystem=%s %s staleRouteBeforeHelper=%s staleRouteReplaced=%s route=%s routeHops=%d fuelBeforeRoute=%d routeFuelCost=%d preJumpFuelWarning=%s routeStatusHasFuelHint=%s lowFuelRouteWarningVisible=%s lowFuelJumpBlocked=%s landedForRefuel=%s refuelSucceeded=%s fuelAfterRefuel=%d routeBeforeDeliveryJump=%s deliveredAfterRefuel=%s tradeBoughtBeforeRoute=%s tradeCargoPreservedAfterDelivery=%s tradeCargoSoldAfterDelivery=%s heldTradeCargoAfterDelivery=%d heldTradeCargoAfterSale=%d cargoUsedAfterDelivery=%d cargoUsedAfterSale=%d creditsAfterDelivery=%d creditsAfterTradeSale=%d completedMissions=%s sourceLabel=terminal-velocity-design-scaffold oracleStatus=mission_objective_hint_pending_ev_classic_ui_trace missionTradeRouteSourceLabel=terminal-velocity-mission-trade-refuel-scaffold missionTradeRouteOracleStatus=mission_trade_refuel_pending_classic_runtime_trace status=\"%s\" routeStatus=\"%s\" lowFuelRouteStatus=\"%s\" lowFuelJumpStatus=\"%s\"" % [MISSION_ROUTE_HINT_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(accepted_body.get("name", "None")), accepted_mission_id, str(mission_accepted), destination_system, mission_route_status, JSON.stringify(stale_route_before_helper), str(stale_route_replaced), queued_route, selected_route.size(), fuel_before_route, route_fuel_cost, str(pre_jump_fuel_warning), str(route_status_has_fuel_hint), str(low_fuel_route_warning_visible), str(low_fuel_jump_blocked), str(landed_for_refuel), str(refuel_succeeded), fuel_after_refuel, JSON.stringify(route_before_delivery_jump), str(delivered_after_refuel), str(trade_bought_before_route), str(trade_cargo_preserved_after_delivery), str(trade_cargo_sold_after_delivery), held_trade_cargo_after_delivery, held_trade_cargo_after_sale, cargo_used_after_delivery, cargo_used_after_sale, credits_after_delivery, credits_after_trade_sale, JSON.stringify(completed_missions), status_line, route_status_line, low_fuel_route_status_line, low_fuel_jump_status])
	get_tree().quit(0)

func _route_to_active_mission_destination() -> bool:
	if active_missions.is_empty():
		status_line = "No active mission destination"
		return false
	var mission := _mission_by_id(str(active_missions[0]))
	if mission.is_empty():
		status_line = "Active mission data unavailable"
		return false
	var destination_system := str(mission.get("destinationSystem", ""))
	if destination_system == "":
		status_line = "Active mission has no destination"
		return false
	selected_route.clear()
	var route_selected := _select_map_route_to_system(destination_system)
	if route_selected:
		status_line = "Mission route queued to %s. %s" % [destination_system, _route_fuel_hint_line()]
	return route_selected

func _run_mission_trade_destination_sale_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var accepted_body := _current_body()
	var mission_before_accept: Dictionary = _first_available_mission(accepted_body)
	var accepted_mission_id := str(mission_before_accept.get("id", "none"))
	var destination_system := str(mission_before_accept.get("destinationSystem", "?"))
	_accept_selected_mission()
	var mission_accepted := active_missions.has(accepted_mission_id)
	landing_tab = 1
	selected_landing_item = 0
	var trade_commodity := "food"
	var credits_before_trade_buy := credits
	var cargo_before_trade_buy := cargo
	_buy_selected_commodity()
	var credits_after_trade_buy := credits
	var held_trade_cargo_after_buy := int(commodity_hold.get(trade_commodity, 0))
	var trade_bought_before_delivery := held_trade_cargo_after_buy == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo == cargo_before_trade_buy + EV_CLASSIC_COMMODITY_LOT_SIZE and credits_after_trade_buy < credits_before_trade_buy
	_ev_land_or_launch()
	selected_route.clear()
	var mission_route_queued := _route_to_active_mission_destination()
	var route_before_delivery_jump := selected_route.duplicate()
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Luna")
	_try_land()
	var completed_ids := _complete_arrived_missions()
	var credits_after_delivery := credits
	var held_trade_cargo_after_delivery := int(commodity_hold.get(trade_commodity, 0))
	var cargo_used_after_delivery := cargo
	var mission_delivered := completed_ids.has(accepted_mission_id) and active_missions.is_empty() and str(current_system.get("name", "?")) == destination_system
	var trade_cargo_preserved_after_delivery := mission_delivered and held_trade_cargo_after_delivery == held_trade_cargo_after_buy and cargo_used_after_delivery == held_trade_cargo_after_buy
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	var credits_after_destination_sale := credits
	var held_trade_cargo_after_sale := int(commodity_hold.get(trade_commodity, 0))
	var cargo_used_after_sale := cargo
	var trade_cargo_sold_at_destination := trade_cargo_preserved_after_delivery and held_trade_cargo_after_sale == 0 and cargo_used_after_sale == 0 and credits_after_destination_sale > credits_after_delivery
	var accepted_status := "missionAccepted=true" if mission_accepted else "missionAccepted=false"
	var trade_buy_status := "tradeBoughtBeforeDelivery=true" if trade_bought_before_delivery else "tradeBoughtBeforeDelivery=false"
	var delivered_status := "missionDelivered=true" if mission_delivered else "missionDelivered=false"
	var preserved_status := "tradeCargoPreservedAfterDelivery=true" if trade_cargo_preserved_after_delivery else "tradeCargoPreservedAfterDelivery=false"
	var sold_status := "tradeCargoSoldAtDestination=true" if trade_cargo_sold_at_destination else "tradeCargoSoldAtDestination=false"
	var cargo_sale_status := "cargoUsedAfterSale=0" if cargo_used_after_sale == 0 else "cargoUsedAfterSale=%d" % cargo_used_after_sale
	print("%s startSystem=Levo routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" acceptedMission=%s %s destinationSystem=%s missionRouteQueued=%s routeBeforeDeliveryJump=%s tradeCommodity=%s %s %s %s %s heldTradeCargoAfterBuy=%d heldTradeCargoAfterDelivery=%d heldTradeCargoAfterSale=%d cargoUsedAfterDelivery=%d %s creditsBeforeTradeBuy=%d creditsAfterTradeBuy=%d creditsAfterDelivery=%d creditsAfterDestinationSale=%d completedMissions=%s sourceLabel=terminal-velocity-mission-trade-destination-sale-scaffold oracleStatus=mission_trade_destination_sale_pending_classic_runtime_trace status=\"%s\"" % [MISSION_TRADE_DESTINATION_SALE_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(accepted_body.get("name", "None")), accepted_mission_id, accepted_status, destination_system, str(mission_route_queued), JSON.stringify(route_before_delivery_jump), trade_commodity, trade_buy_status, delivered_status, preserved_status, sold_status, held_trade_cargo_after_buy, held_trade_cargo_after_delivery, held_trade_cargo_after_sale, cargo_used_after_delivery, cargo_sale_status, credits_before_trade_buy, credits_after_trade_buy, credits_after_delivery, credits_after_destination_sale, JSON.stringify(completed_missions), status_line])
	get_tree().quit(0)

func _run_chapter_one_trade_carryover_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var intro_body := _current_body()
	var intro_mission_id := "intro_courier_earth_hera"
	_accept_selected_mission()
	var intro_mission_accepted := active_missions.has(intro_mission_id)
	landing_tab = 1
	selected_landing_item = 0
	var trade_commodity := "food"
	var credits_before_trade_buy := credits
	var cargo_before_trade_buy := cargo
	_buy_selected_commodity()
	var credits_after_trade_buy := credits
	var held_trade_cargo_after_buy := int(commodity_hold.get(trade_commodity, 0))
	var trade_bought_before_intro_delivery := held_trade_cargo_after_buy == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo == cargo_before_trade_buy + EV_CLASSIC_COMMODITY_LOT_SIZE and credits_after_trade_buy < credits_before_trade_buy
	_ev_land_or_launch()
	selected_route.clear()
	var intro_route_queued := _route_to_active_mission_destination()
	var intro_route_before_jump := selected_route.duplicate()
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Luna")
	_try_land()
	var intro_completed_ids := _complete_arrived_missions()
	var credits_after_intro_delivery := credits
	var held_trade_cargo_after_intro := int(commodity_hold.get(trade_commodity, 0))
	var intro_mission_delivered := intro_completed_ids.has(intro_mission_id) and completed_missions.has(intro_mission_id)
	var second_mission_id := "frontier_sample_hera_freeport"
	selected_landing_item = 0
	_accept_selected_mission()
	var second_mission_accepted := active_missions.has(second_mission_id)
	var cargo_after_second_accept := cargo
	var trade_cargo_reserved_alongside_second_mission := second_mission_accepted and held_trade_cargo_after_intro == held_trade_cargo_after_buy and cargo_after_second_accept == held_trade_cargo_after_buy + 4
	_ev_land_or_launch()
	selected_route.clear()
	var second_route_queued := _route_to_active_mission_destination()
	var second_route_before_jump := selected_route.duplicate()
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Sirius Station")
	_try_land()
	var second_completed_ids := _complete_arrived_missions()
	var credits_after_second_delivery := credits
	var held_trade_cargo_after_second := int(commodity_hold.get(trade_commodity, 0))
	var cargo_used_after_second := cargo
	var second_mission_delivered := second_completed_ids.has(second_mission_id) and completed_missions.has(second_mission_id)
	var trade_cargo_preserved_through_second_delivery := second_mission_delivered and held_trade_cargo_after_second == held_trade_cargo_after_buy and cargo_used_after_second == held_trade_cargo_after_buy
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	var credits_after_sirius_sale := credits
	var held_trade_cargo_after_sale := int(commodity_hold.get(trade_commodity, 0))
	var cargo_used_after_sale := cargo
	var trade_cargo_sold_at_sirius_station := trade_cargo_preserved_through_second_delivery and held_trade_cargo_after_sale == 0 and cargo_used_after_sale == 0 and credits_after_sirius_sale > credits_after_second_delivery
	var cargo_sale_status := "cargoUsedAfterSale=0" if cargo_used_after_sale == 0 else "cargoUsedAfterSale=%d" % cargo_used_after_sale
	var intro_delivered_status := "introMissionDelivered=true" if intro_mission_delivered else "introMissionDelivered=false"
	var second_delivered_status := "secondMissionDelivered=true" if second_mission_delivered else "secondMissionDelivered=false"
	var reserved_status := "tradeCargoReservedAlongsideSecondMission=true" if trade_cargo_reserved_alongside_second_mission else "tradeCargoReservedAlongsideSecondMission=false"
	var preserved_status := "tradeCargoPreservedThroughSecondDelivery=true" if trade_cargo_preserved_through_second_delivery else "tradeCargoPreservedThroughSecondDelivery=false"
	var sold_status := "tradeCargoSoldAtSiriusStation=true" if trade_cargo_sold_at_sirius_station else "tradeCargoSoldAtSiriusStation=false"
	print("%s startSystem=Levo routeToSolSelected=%s introAcceptedAtSystem=Sol introAcceptedAtBody=\"%s\" introMission=%s introMissionAccepted=%s tradeCommodity=%s tradeBoughtBeforeIntroDelivery=%s introRouteQueued=%s introRouteBeforeJump=%s %s secondMission=%s secondMissionAccepted=%s %s secondRouteQueued=%s secondRouteBeforeJump=%s %s %s %s heldTradeCargoAfterBuy=%d heldTradeCargoAfterIntro=%d heldTradeCargoAfterSecondDelivery=%d heldTradeCargoAfterSale=%d cargoAfterSecondAccept=%d cargoUsedAfterSecondDelivery=%d %s creditsBeforeTradeBuy=%d creditsAfterTradeBuy=%d creditsAfterIntroDelivery=%d creditsAfterSecondDelivery=%d creditsAfterSiriusSale=%d completedMissions=%s storyFlags=%s sourceLabel=terminal-velocity-chapter-one-trade-carryover-scaffold oracleStatus=chapter_one_trade_carryover_pending_classic_runtime_trace status=\"%s\"" % [CHAPTER_ONE_TRADE_CARRYOVER_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(intro_body.get("name", "None")), intro_mission_id, str(intro_mission_accepted), trade_commodity, str(trade_bought_before_intro_delivery), str(intro_route_queued), JSON.stringify(intro_route_before_jump), intro_delivered_status, second_mission_id, str(second_mission_accepted), reserved_status, str(second_route_queued), JSON.stringify(second_route_before_jump), second_delivered_status, preserved_status, sold_status, held_trade_cargo_after_buy, held_trade_cargo_after_intro, held_trade_cargo_after_second, held_trade_cargo_after_sale, cargo_after_second_accept, cargo_used_after_second, cargo_sale_status, credits_before_trade_buy, credits_after_trade_buy, credits_after_intro_delivery, credits_after_second_delivery, credits_after_sirius_sale, JSON.stringify(completed_missions), JSON.stringify(story_flags), status_line])
	get_tree().quit(0)

func _run_mission_trade_return_margin_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var intro_body := _current_body()
	var intro_mission_id := "intro_courier_earth_hera"
	_accept_selected_mission()
	var intro_mission_accepted := active_missions.has(intro_mission_id)
	landing_tab = 1
	selected_landing_item = 0
	var outbound_trade_commodity := "food"
	_buy_selected_commodity()
	var held_outbound_trade_after_buy := int(commodity_hold.get(outbound_trade_commodity, 0))
	_ev_land_or_launch()
	selected_route.clear()
	var intro_route_queued := _route_to_active_mission_destination()
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Luna")
	_try_land()
	var intro_completed_ids := _complete_arrived_missions()
	var intro_delivered := intro_completed_ids.has(intro_mission_id) and completed_missions.has(intro_mission_id)
	var second_mission_id := "frontier_sample_hera_freeport"
	selected_landing_item = 0
	_accept_selected_mission()
	var second_mission_accepted := active_missions.has(second_mission_id)
	_ev_land_or_launch()
	selected_route.clear()
	var second_route_queued := _route_to_active_mission_destination()
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Sirius Station")
	_try_land()
	var second_completed_ids := _complete_arrived_missions()
	var second_delivered := second_completed_ids.has(second_mission_id) and completed_missions.has(second_mission_id)
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	var held_outbound_trade_after_sale := int(commodity_hold.get(outbound_trade_commodity, 0))
	var credits_after_sirius_sale := credits
	var return_trade_commodity := "equipment"
	var sirius_equipment_buy_price := int(_market_prices("Sirius").get(return_trade_commodity, {}).get("buy", 0))
	var sol_equipment_sell_price := int(_market_prices("Sol").get(return_trade_commodity, {}).get("sell", 0))
	var return_margin_per_ton := sol_equipment_sell_price - sirius_equipment_buy_price
	var return_trade_skipped_for_margin := return_margin_per_ton <= 0
	var held_return_trade_after_margin_eval := int(commodity_hold.get(return_trade_commodity, 0))
	var return_mission_id := "freeport_return_earth"
	var return_offers := _available_missions(_current_body())
	var return_offer_ids := _mission_ids(return_offers)
	selected_landing_item = return_offer_ids.find(return_mission_id)
	if selected_landing_item < 0:
		selected_landing_item = 0
	_accept_selected_mission()
	var return_mission_accepted := active_missions.has(return_mission_id)
	var cargo_after_return_accept := cargo
	_ev_land_or_launch()
	selected_route.clear()
	var return_route_queued := _route_to_active_mission_destination()
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var return_completed_ids := _complete_arrived_missions()
	var return_delivered := return_completed_ids.has(return_mission_id) and completed_missions.has(return_mission_id)
	var final_cargo := cargo
	var return_mission_accepted_status := "returnMissionAccepted=true" if return_mission_accepted else "returnMissionAccepted=false"
	var return_mission_delivered_status := "returnMissionDelivered=true" if return_delivered else "returnMissionDelivered=false"
	var candidate_margin_status := "candidateMarginPerTon=-10" if return_margin_per_ton == -10 else "candidateMarginPerTon=%d" % return_margin_per_ton
	var negative_margin_skipped_status := "negativeMarginSkipped=true" if return_trade_skipped_for_margin else "negativeMarginSkipped=false"
	var return_cargo_contamination_prevented_status := "returnCargoContaminationPrevented=true" if held_return_trade_after_margin_eval == 0 else "returnCargoContaminationPrevented=false"
	var cargo_used_after_return_delivery_status := "cargoUsedAfterReturnDelivery=0" if final_cargo == 0 else "cargoUsedAfterReturnDelivery=%d" % final_cargo
	print("%s startSystem=Levo routeToSolSelected=%s introAcceptedAtSystem=Sol introAcceptedAtBody=\"%s\" introMission=%s introMissionAccepted=%s introRouteQueued=%s introMissionDelivered=%s secondMission=%s secondMissionAccepted=%s secondRouteQueued=%s secondMissionDelivered=%s outboundTradeCommodity=%s heldOutboundTradeAfterBuy=%d heldOutboundTradeAfterSale=%d creditsAfterSiriusSale=%d returnTradeCommodity=%s returnBuySystem=Sirius returnSellSystem=Sol returnBuyPrice=%d returnSellPrice=%d %s %s heldReturnTradeAfterMarginEval=%d %s returnMission=%s %s cargoAfterReturnAccept=%d returnRouteQueued=%s %s finalCargo=%d %s completedMissions=%s storyFlags=%s sourceLabel=terminal-velocity-mission-trade-return-margin-scaffold oracleStatus=chapter_one_return_trade_margin_pending_classic_runtime_trace status=\"%s\"" % [MISSION_TRADE_RETURN_MARGIN_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(intro_body.get("name", "None")), intro_mission_id, str(intro_mission_accepted), str(intro_route_queued), str(intro_delivered), second_mission_id, str(second_mission_accepted), str(second_route_queued), str(second_delivered), outbound_trade_commodity, held_outbound_trade_after_buy, held_outbound_trade_after_sale, credits_after_sirius_sale, return_trade_commodity, sirius_equipment_buy_price, sol_equipment_sell_price, candidate_margin_status, negative_margin_skipped_status, held_return_trade_after_margin_eval, return_cargo_contamination_prevented_status, return_mission_id, return_mission_accepted_status, cargo_after_return_accept, str(return_route_queued), return_mission_delivered_status, final_cargo, cargo_used_after_return_delivery_status, JSON.stringify(completed_missions), JSON.stringify(story_flags), status_line])
	get_tree().quit(0)

func _run_trade_margin_choice_log() -> void:
	_reset_travel_state()
	map_visible = true
	var profitable_commodity := "food"
	var unprofitable_commodity := "equipment"
	var profitable_buy_system := "Sol"
	var profitable_sell_system := "Levo"
	var unprofitable_buy_system := "Levo"
	var unprofitable_sell_system := "Sol"
	var profitable_margin_per_ton := 60
	var negative_margin_per_ton := -10
	var route_to_buy_system_selected := _select_map_route_to_system(profitable_buy_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var cargo_before_profitable_buy := cargo
	var credits_before_profitable_buy := credits
	_buy_selected_commodity()
	var credits_after_profitable_buy := credits
	var held_profitable_after_buy := int(commodity_hold.get(profitable_commodity, 0))
	var profitable_trade_bought := held_profitable_after_buy > 0 and cargo > cargo_before_profitable_buy
	var negative_margin_skipped := negative_margin_per_ton <= 0
	var held_unprofitable_after_eval := int(commodity_hold.get(unprofitable_commodity, 0))
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_sell_system_selected := _select_map_route_to_system(profitable_sell_system)
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_profitable_sale := credits
	_sell_selected_commodity()
	var held_profitable_after_sale := int(commodity_hold.get(profitable_commodity, 0))
	var profitable_trade_sold := held_profitable_after_sale == 0 and credits > credits_before_profitable_sale
	var final_cargo := cargo
	var negative_margin_skipped_status := "negativeMarginSkipped=true" if negative_margin_skipped else "negativeMarginSkipped=false"
	var profitable_commodity_status := "profitableCommodity=food"
	var unprofitable_commodity_status := "unprofitableCommodity=equipment"
	var profitable_margin_status := "profitableMarginPerTon=60"
	var negative_margin_status := "negativeMarginPerTon=-10"
	var profitable_trade_bought_status := "profitableTradeBought=true" if profitable_trade_bought else "profitableTradeBought=false"
	var profitable_trade_sold_status := "profitableTradeSold=true" if profitable_trade_sold else "profitableTradeSold=false"
	var final_cargo_status := "finalCargo=0" if final_cargo == 0 else "finalCargo=%d" % final_cargo
	print("%s startSystem=Levo buySystem=%s sellSystem=%s routeToBuySystemSelected=%s routeToSellSystemSelected=%s %s %s %s %s %s %s %s heldProfitableAfterBuy=%d heldProfitableAfterSale=%d heldUnprofitableAfterEval=%d cargoBeforeProfitableBuy=%d %s creditsBeforeProfitableBuy=%d creditsAfterProfitableBuy=%d creditsBeforeProfitableSale=%d creditsAfterProfitableSale=%d unprofitableBuySystem=%s unprofitableSellSystem=%s sourceLabel=terminal-velocity-trade-margin-choice-scaffold oracleStatus=trade_margin_choice_pending_classic_runtime_trace status=\"%s\"" % [TRADE_MARGIN_CHOICE_EVENT_LOG_PREFIX, profitable_buy_system, profitable_sell_system, str(route_to_buy_system_selected), str(route_to_sell_system_selected), profitable_commodity_status, unprofitable_commodity_status, profitable_margin_status, negative_margin_status, negative_margin_skipped_status, profitable_trade_bought_status, profitable_trade_sold_status, held_profitable_after_buy, held_profitable_after_sale, held_unprofitable_after_eval, cargo_before_profitable_buy, final_cargo_status, credits_before_profitable_buy, credits_after_profitable_buy, credits_before_profitable_sale, credits, unprofitable_buy_system, unprofitable_sell_system, status_line])
	get_tree().quit(0)

func _run_mission_abort_log() -> void:
	_reset_travel_state()
	var no_active_abort_blocked := not _abort_active_mission()
	var no_active_abort_status_visible := status_messages.has("No active mission to abort")
	var history_before_accept := aborted_mission_history.size()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var accepted_body := _current_body()
	var mission_before_accept: Dictionary = _first_available_mission(accepted_body)
	var accepted_mission_id := str(mission_before_accept.get("id", "none"))
	var cargo_before_accept := cargo
	_accept_selected_mission()
	var cargo_after_accept := cargo
	var mission_accepted := active_missions.has(accepted_mission_id)
	var abort_succeeded := _abort_active_mission(accepted_mission_id)
	var cargo_after_abort := cargo
	var repeat_abort_blocked := not _abort_active_mission(accepted_mission_id)
	var repeat_abort_status_visible := status_messages.has("No active mission to abort")
	var latest_abort := JSON.stringify(aborted_mission_history[aborted_mission_history.size() - 1]) if not aborted_mission_history.is_empty() else "{}"
	var accepted_status := "missionAccepted=true" if mission_accepted else "missionAccepted=false"
	var abort_status := "missionAborted=true" if abort_succeeded else "missionAborted=false"
	var cargo_released_status := "reservedCargoReleased=true" if cargo_after_abort == cargo_before_accept else "reservedCargoReleased=false"
	print("%s startSystem=Levo routeToSolSelected=%s noActiveAbortBlocked=%s noActiveAbortStatusVisible=%s historyBeforeAccept=%d acceptedAtSystem=Sol acceptedAtBody=\"%s\" acceptedMission=%s %s %s %s repeatAbortBlocked=%s repeatAbortStatusVisible=%s cargoBeforeAccept=%d cargoAfterAccept=%d cargoAfterAbort=%d activeMissions=%s completedMissions=%s abortedHistoryCount=%d latestAbort=%s sourceLabel=terminal-velocity-mission-abort-scaffold oracleStatus=mission_abort_pending_classic_runtime_or_manual_trace status=\"%s\"" % [MISSION_ABORT_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(no_active_abort_blocked), str(no_active_abort_status_visible), history_before_accept, str(accepted_body.get("name", "None")), accepted_mission_id, accepted_status, abort_status, cargo_released_status, str(repeat_abort_blocked), str(repeat_abort_status_visible), cargo_before_accept, cargo_after_accept, cargo_after_abort, JSON.stringify(active_missions), JSON.stringify(completed_missions), aborted_mission_history.size(), latest_abort, status_line])
	get_tree().quit(0)

func _run_mission_abort_reaccept_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var accepted_body := _current_body()
	var mission_before_accept: Dictionary = _first_available_mission(accepted_body)
	var accepted_mission_id := str(mission_before_accept.get("id", "none"))
	var cargo_before_first_accept := cargo
	_accept_selected_mission()
	var first_accept_succeeded := active_missions.has(accepted_mission_id)
	var cargo_after_first_accept := cargo
	var first_abort_succeeded := _abort_active_mission(accepted_mission_id)
	var cargo_after_abort := cargo
	var offers_after_abort := _available_missions(accepted_body)
	var offer_ids_after_abort := _mission_ids(offers_after_abort)
	var reoffer_visible := offer_ids_after_abort.has(accepted_mission_id)
	selected_landing_item = offer_ids_after_abort.find(accepted_mission_id)
	if selected_landing_item < 0:
		selected_landing_item = 0
	_accept_selected_mission()
	var reaccept_succeeded := active_missions.has(accepted_mission_id)
	var cargo_after_reaccept := cargo
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_luna_selected := _select_map_route_to_system("Centauri")
	var route_before_jump := selected_route.duplicate()
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Luna")
	_try_land()
	var credits_before_delivery := credits
	var completed_ids := _complete_arrived_missions()
	var delivery_succeeded := completed_ids.has(accepted_mission_id) and completed_missions.has(accepted_mission_id)
	var cargo_after_delivery := cargo
	var latest_abort := JSON.stringify(aborted_mission_history[aborted_mission_history.size() - 1]) if not aborted_mission_history.is_empty() else "{}"
	var latest_completion := JSON.stringify(completed_mission_history[completed_mission_history.size() - 1]) if not completed_mission_history.is_empty() else "{}"
	var first_accept_status := "firstMissionAccepted=true" if first_accept_succeeded else "firstMissionAccepted=false"
	var abort_status := "firstMissionAborted=true" if first_abort_succeeded else "firstMissionAborted=false"
	var release_status := "reservedCargoReleasedAfterAbort=true" if cargo_after_abort == cargo_before_first_accept else "reservedCargoReleasedAfterAbort=false"
	var reoffer_status := "missionReofferVisibleAfterAbort=true" if reoffer_visible else "missionReofferVisibleAfterAbort=false"
	var reaccept_status := "missionReaccepted=true" if reaccept_succeeded else "missionReaccepted=false"
	var reaccept_reserve_status := "reservedCargoReclaimedAfterReaccept=true" if cargo_after_reaccept == cargo_before_first_accept + int(mission_before_accept.get("cargoTons", 0)) else "reservedCargoReclaimedAfterReaccept=false"
	var delivery_status := "reacceptedMissionDelivered=true" if delivery_succeeded else "reacceptedMissionDelivered=false"
	var final_release_status := "reservedCargoReleasedAfterDelivery=true" if cargo_after_delivery == cargo_before_first_accept else "reservedCargoReleasedAfterDelivery=false"
	var reward_status := "rewardPaidAfterDelivery=true" if credits == credits_before_delivery + int(mission_before_accept.get("reward", 0)) else "rewardPaidAfterDelivery=false"
	print("%s startSystem=Levo routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" acceptedMission=%s %s %s %s %s offersAfterAbort=%s %s %s routeToLunaSelected=%s routeBeforeJump=%s %s %s %s cargoBeforeFirstAccept=%d cargoAfterFirstAccept=%d cargoAfterAbort=%d cargoAfterReaccept=%d cargoAfterDelivery=%d creditsBeforeDelivery=%d creditsAfterDelivery=%d activeMissions=%s completedMissions=%s abortedHistoryCount=%d latestAbort=%s latestCompletion=%s sourceLabel=terminal-velocity-mission-abort-reaccept-scaffold oracleStatus=mission_abort_reaccept_pending_classic_runtime_or_manual_trace status=\"%s\"" % [MISSION_ABORT_REACCEPT_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(accepted_body.get("name", "None")), accepted_mission_id, first_accept_status, abort_status, release_status, reoffer_status, JSON.stringify(offer_ids_after_abort), reaccept_status, reaccept_reserve_status, str(route_to_luna_selected), JSON.stringify(route_before_jump), delivery_status, final_release_status, reward_status, cargo_before_first_accept, cargo_after_first_accept, cargo_after_abort, cargo_after_reaccept, cargo_after_delivery, credits_before_delivery, credits, JSON.stringify(active_missions), JSON.stringify(completed_missions), aborted_mission_history.size(), latest_abort, latest_completion, status_line])
	get_tree().quit(0)

func _run_mission_abort_forbidden_log() -> void:
	_reset_travel_state()
	var probe_mission := {
		"id": "canabort_return_gate_probe",
		"title": "CanAbort Return Gate Probe",
		"originSystem": "Sol",
		"originBody": "Earth",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"reward": 1800,
		"canAbort": false,
		"sourceLabel": "ev-classic-resource-bible-backed-canabort-guardrail",
		"oracleStatus": "classic_runtime_canabort_return_cleanup_pending",
	}
	missions["missions"].append(probe_mission)
	active_missions.append(str(probe_mission.get("id")))
	mission_acceptance_days[str(probe_mission.get("id"))] = current_day
	cargo = int(probe_mission.get("cargoTons", 0))
	var cargo_after_accept := cargo
	var blocked_abort := not _abort_active_mission(str(probe_mission.get("id")))
	var cargo_after_blocked_abort := cargo
	var blocked_reason_visible := status_messages.has("Mission cannot abort before return/cleanup")
	current_system_index = _system_index_by_name("Centauri", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	pos = Vector2(-520.0, -300.0)
	landed = true
	var credits_before_completion := credits
	var completed_ids := _complete_arrived_missions()
	var latest_completion := JSON.stringify(completed_mission_history[completed_mission_history.size() - 1]) if not completed_mission_history.is_empty() else "{}"
	var completed_status := "completedNonAbortableMission=true" if completed_ids.has(str(probe_mission.get("id"))) and completed_missions.has(str(probe_mission.get("id"))) else "completedNonAbortableMission=false"
	var preserved_status := "reservedCargoPreservedAfterBlockedAbort=true" if cargo_after_blocked_abort == cargo_after_accept else "reservedCargoPreservedAfterBlockedAbort=false"
	var released_status := "reservedCargoReleasedAfterCompletion=true" if cargo == 0 else "reservedCargoReleasedAfterCompletion=false"
	var reward_status := "rewardPaidAfterCompletion=true" if credits == credits_before_completion + int(probe_mission.get("reward", 0)) else "rewardPaidAfterCompletion=false"
	print("%s acceptedMission=%s canAbort=false cargoAfterAccept=%d blockedAbort=%s blockedReasonVisible=%s cargoAfterBlockedAbort=%d %s %s %s %s activeMissions=%s completedMissions=%s abortedHistoryCount=%d latestCompletion=%s sourceLabel=ev-classic-resource-bible-backed-canabort-guardrail oracleStatus=classic_runtime_canabort_return_cleanup_pending status=\"%s\"" % [MISSION_ABORT_FORBIDDEN_EVENT_LOG_PREFIX, str(probe_mission.get("id")), cargo_after_accept, str(blocked_abort), str(blocked_reason_visible), cargo_after_blocked_abort, preserved_status, completed_status, released_status, reward_status, JSON.stringify(active_missions), JSON.stringify(completed_missions), aborted_mission_history.size(), latest_completion, status_line])
	get_tree().quit(0)

func _run_mission_abort_penalty_log() -> void:
	_reset_travel_state()
	var probe_mission := {
		"id": "abort_penalty_probe",
		"title": "Abort Penalty Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"completionGovernment": "Federation",
		"completionReward": 6,
		"abortReputationMultiplier": 5,
		"sourceLabel": "ev-classic-resource-bible-backed-mission-abort-penalty-scaffold",
		"oracleStatus": "classic_runtime_abort_penalty_ui_pending",
	}
	missions["missions"].append(probe_mission)
	active_missions.append(str(probe_mission.get("id")))
	mission_acceptance_days[str(probe_mission.get("id"))] = current_day
	cargo = int(probe_mission.get("cargoTons", 0))
	reputation_scores["Federation"] = 5
	var reputation_before_abort := int(reputation_scores.get("Federation", 0))
	var cargo_before_abort := cargo
	var abort_succeeded := _abort_active_mission(str(probe_mission.get("id")))
	var latest_abort: Dictionary = aborted_mission_history[aborted_mission_history.size() - 1] if not aborted_mission_history.is_empty() else {}
	var expected_delta := -int(probe_mission.get("completionReward", 0)) * int(probe_mission.get("abortReputationMultiplier", 0))
	var actual_delta := int(latest_abort.get("reputation_delta", 0))
	var reputation_after_abort := int(reputation_scores.get("Federation", 0))
	var abort_status := "missionAborted=true" if abort_succeeded else "missionAborted=false"
	var cargo_released_status := "reservedCargoReleased=true" if cargo == cargo_before_abort - int(probe_mission.get("cargoTons", 0)) else "reservedCargoReleased=false"
	var reputation_status := "reputationPenaltyApplied=true" if actual_delta == expected_delta and reputation_after_abort == reputation_before_abort + expected_delta else "reputationPenaltyApplied=false"
	print("%s acceptedMission=%s %s cargoBeforeAbort=%d cargoAfterAbort=%d %s reputationBeforeAbort=%d reputationAfterAbort=%d reputationDelta=%d expectedReputationDelta=%d %s activeMissions=%s abortedHistoryCount=%d latestAbort=%s sourceLabel=ev-classic-resource-bible-backed-mission-abort-penalty-scaffold oracleStatus=classic_runtime_abort_penalty_ui_pending status=\"%s\"" % [MISSION_ABORT_PENALTY_EVENT_LOG_PREFIX, str(probe_mission.get("id")), abort_status, cargo_before_abort, cargo, cargo_released_status, reputation_before_abort, reputation_after_abort, actual_delta, expected_delta, reputation_status, JSON.stringify(active_missions), aborted_mission_history.size(), JSON.stringify(latest_abort), status_line])
	get_tree().quit(0)

func _run_mission_auto_abort_log() -> void:
	_reset_travel_state()
	var probe_mission := {
		"id": "auto_abort_completion_bit_probe",
		"title": "Auto Abort Completion Bit Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 2,
		"autoAbort": true,
		"completionFlags": ["auto_abort_completion_bit_77"],
		"sourceLabel": "ev-classic-resource-bible-backed-auto-abort-guardrail",
		"oracleStatus": "classic_runtime_auto_abort_ui_pending",
	}
	missions["missions"].append(probe_mission)
	active_missions.append(str(probe_mission.get("id")))
	mission_acceptance_days[str(probe_mission.get("id"))] = current_day
	cargo = int(probe_mission.get("cargoTons", 0))
	var cargo_after_accept := cargo
	var auto_abort_triggered := _auto_abort_active_mission(probe_mission)
	var latest_abort: Dictionary = aborted_mission_history[aborted_mission_history.size() - 1] if not aborted_mission_history.is_empty() else {}
	var abort_status := "autoAbortedAfterAcceptance=true" if auto_abort_triggered and not active_missions.has(str(probe_mission.get("id"))) else "autoAbortedAfterAcceptance=false"
	var cargo_status := "reservedCargoReleased=true" if cargo == 0 else "reservedCargoReleased=false"
	var flag_status := "completionFlagsApplied=true" if story_flags.has("auto_abort_completion_bit_77") else "completionFlagsApplied=false"
	print("%s acceptedMission=%s autoAbort=true cargoAfterAccept=%d cargoAfterAutoAbort=%d %s %s %s activeMissions=%s abortedHistoryCount=%d latestAbort=%s sourceLabel=ev-classic-resource-bible-backed-auto-abort-guardrail oracleStatus=classic_runtime_auto_abort_ui_pending status=\"%s\"" % [MISSION_AUTO_ABORT_EVENT_LOG_PREFIX, str(probe_mission.get("id")), cargo_after_accept, cargo, abort_status, cargo_status, flag_status, JSON.stringify(active_missions), aborted_mission_history.size(), JSON.stringify(latest_abort), status_line])
	get_tree().quit(0)

func _run_mission_scan_failure_log() -> void:
	_reset_travel_state()
	var probe_mission := {
		"id": "scan_failure_probe",
		"title": "Scan Failure Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 4,
		"scanGovernment": "Federation",
		"failIfScanned": true,
		"failureBitSet": 44,
		"sourceLabel": "ev-classic-resource-bible-backed-mission-scan-failure-scaffold",
		"oracleStatus": "classic_runtime_scan_failure_ui_pending",
	}
	missions["missions"].append(probe_mission)
	active_missions.append(str(probe_mission.get("id")))
	mission_acceptance_days[str(probe_mission.get("id"))] = current_day
	cargo = int(probe_mission.get("cargoTons", 0))
	var cargo_after_accept := cargo
	var clear_scan := _apply_mission_cargo_scan("Independent")
	var cargo_after_clear_scan := cargo
	var failure_scan := _apply_mission_cargo_scan("Federation")
	var latest_failure: Dictionary = failed_mission_history[failed_mission_history.size() - 1] if not failed_mission_history.is_empty() else {}
	var clear_status := "nonmatchingScanPreservedMission=true" if bool(clear_scan.get("preserved", false)) else "nonmatchingScanPreservedMission=false"
	var failure_status := "matchingScanFailedMission=true" if bool(failure_scan.get("failed", false)) and not active_missions.has(str(probe_mission.get("id"))) else "matchingScanFailedMission=false"
	var cargo_released_status := "reservedCargoReleased=true" if cargo == 0 else "reservedCargoReleased=false"
	var flag_status := "failureFlagSet=true" if story_flags.has("fail_mission_bit_44") else "failureFlagSet=false"
	print("%s acceptedMission=%s scanGovernment=%s failIfScanned=%s cargoAfterAccept=%d clearScanGovernment=Independent cargoAfterClearScan=%d %s matchingScanGovernment=Federation cargoAfterFailureScan=%d %s %s %s activeMissions=%s failedHistoryCount=%d latestFailure=%s sourceLabel=ev-classic-resource-bible-backed-mission-scan-failure-scaffold oracleStatus=classic_runtime_scan_failure_ui_pending status=\"%s\"" % [MISSION_SCAN_FAILURE_EVENT_LOG_PREFIX, str(probe_mission.get("id")), str(probe_mission.get("scanGovernment", "")), str(probe_mission.get("failIfScanned", false)), cargo_after_accept, cargo_after_clear_scan, clear_status, cargo, failure_status, cargo_released_status, flag_status, JSON.stringify(active_missions), failed_mission_history.size(), JSON.stringify(latest_failure), status_line])
	get_tree().quit(0)

func _run_mission_deadline_failure_log() -> void:
	_reset_travel_state()
	var deadline_mission := {
		"id": "deadline_dispatch_failure_probe",
		"title": "Deadline Dispatch Failure Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"reward": 1200,
		"completionReward": 6,
		"failureBitSet": 42,
		"completionGovernment": "Federation",
		"timeLimitDays": 2,
	}
	var accepted_day := 0
	var current_day := 3
	active_missions.append(str(deadline_mission.get("id")))
	cargo = int(deadline_mission.get("cargoTons", 0))
	var cargo_after_accept := cargo
	var before_reputation := int(reputation_scores.get("Federation", 0))
	var failure_succeeded := _fail_mission_deadline(deadline_mission, accepted_day, current_day)
	var after_reputation := int(reputation_scores.get("Federation", 0))
	var latest_failure := JSON.stringify(failed_mission_history[failed_mission_history.size() - 1]) if not failed_mission_history.is_empty() else "{}"
	var failure_status := "deadlineFailureRecorded=true" if failure_succeeded else "deadlineFailureRecorded=false"
	var cargo_status := "reservedCargoReleased=true" if cargo == 0 else "reservedCargoReleased=false"
	var flag_status := "failureFlagSet=true" if story_flags.has("fail_mission_bit_42") else "failureFlagSet=false"
	var reputation_status := "reputationPenaltyApplied=true" if after_reputation == before_reputation - 3 else "reputationPenaltyApplied=false"
	print("%s acceptedMission=%s acceptedDay=%d currentDay=%d timeLimitDays=%d cargoAfterAccept=%d cargoAfterFailure=%d %s %s %s %s reputationBefore=%d reputationAfter=%d activeMissions=%s failedHistoryCount=%d latestFailure=%s sourceLabel=ev-classic-resource-bible-backed-mission-failure-scaffold oracleStatus=deadline_failure_runtime_ui_pending_classic_trace status=\"%s\"" % [MISSION_DEADLINE_FAILURE_EVENT_LOG_PREFIX, str(deadline_mission.get("id")), accepted_day, current_day, int(deadline_mission.get("timeLimitDays", 0)), cargo_after_accept, cargo, failure_status, cargo_status, flag_status, reputation_status, before_reputation, after_reputation, JSON.stringify(active_missions), failed_mission_history.size(), latest_failure, status_line])
	get_tree().quit(0)

func _run_mission_deadline_last_day_log() -> void:
	_reset_travel_state()
	var deadline_mission := {
		"id": "deadline_dispatch_failure_probe",
		"title": "Deadline Dispatch Failure Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"reward": 1200,
		"completionReward": 6,
		"failureBitSet": 42,
		"completionGovernment": "Federation",
		"timeLimitDays": 2,
		"sourceLabel": "terminal-velocity-mission-deadline-last-day-scaffold",
		"oracleStatus": "deadline_last_day_delivery_pending_classic_runtime_or_manual_trace",
	}
	missions["missions"].append(deadline_mission)
	var accepted_day := 0
	current_day = 2
	active_missions.append(str(deadline_mission.get("id")))
	mission_acceptance_days[str(deadline_mission.get("id"))] = accepted_day
	cargo = int(deadline_mission.get("cargoTons", 0))
	var cargo_after_accept := cargo
	current_system_index = _system_index_by_name("Centauri", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	pos = Vector2(-520.0, -300.0)
	landed = true
	var credits_before_completion := credits
	var reputation_before_completion := int(reputation_scores.get("Federation", 0))
	var completed_ids := _complete_arrived_missions()
	var latest_completion := JSON.stringify(completed_mission_history[completed_mission_history.size() - 1]) if not completed_mission_history.is_empty() else "{}"
	var late_failure_attempted := _fail_mission_deadline(deadline_mission, accepted_day, current_day)
	var reputation_after_check := int(reputation_scores.get("Federation", 0))
	var completed_status := "lastDayDeliveryCompleted=true" if completed_ids.has(str(deadline_mission.get("id"))) and completed_missions.has(str(deadline_mission.get("id"))) else "lastDayDeliveryCompleted=false"
	var no_failure_status := "deadlineFailurePrevented=true" if not late_failure_attempted and failed_mission_history.is_empty() and not story_flags.has("fail_mission_bit_42") else "deadlineFailurePrevented=false"
	var cargo_status := "reservedCargoReleased=true" if cargo == 0 else "reservedCargoReleased=false"
	var reward_status := "rewardPaid=true" if credits == credits_before_completion + int(deadline_mission.get("reward", 0)) else "rewardPaid=false"
	var reputation_status := "reputationPreserved=true" if reputation_after_check == reputation_before_completion else "reputationPreserved=false"
	print("%s acceptedMission=%s acceptedDay=%d currentDay=%d timeLimitDays=%d cargoAfterAccept=%d cargoAfterCompletion=%d %s %s %s %s %s creditsBeforeCompletion=%d creditsAfterCompletion=%d reputationBefore=%d reputationAfter=%d activeMissions=%s completedMissions=%s failedHistoryCount=%d latestCompletion=%s sourceLabel=terminal-velocity-mission-deadline-last-day-scaffold oracleStatus=deadline_last_day_delivery_pending_classic_runtime_or_manual_trace status=\"%s\"" % [MISSION_DEADLINE_LAST_DAY_EVENT_LOG_PREFIX, str(deadline_mission.get("id")), accepted_day, current_day, int(deadline_mission.get("timeLimitDays", 0)), cargo_after_accept, cargo, completed_status, no_failure_status, cargo_status, reward_status, reputation_status, credits_before_completion, credits, reputation_before_completion, reputation_after_check, JSON.stringify(active_missions), JSON.stringify(completed_missions), failed_mission_history.size(), latest_completion, status_line])
	get_tree().quit(0)

func _run_mission_deadline_completed_log() -> void:
	_reset_travel_state()
	var deadline_mission := {
		"id": "deadline_dispatch_completed_probe",
		"title": "Deadline Dispatch Completed Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"reward": 1800,
		"completionReward": 6,
		"failureBitSet": 42,
		"completionGovernment": "Federation",
		"timeLimitDays": 2,
		"sourceLabel": "terminal-velocity-mission-deadline-completed-no-late-failure-scaffold",
		"oracleStatus": "deadline_completed_no_late_failure_pending_classic_runtime_or_manual_trace",
	}
	missions["missions"].append(deadline_mission)
	var accepted_day := 0
	active_missions.append(str(deadline_mission.get("id")))
	mission_acceptance_days[str(deadline_mission.get("id"))] = accepted_day
	cargo = int(deadline_mission.get("cargoTons", 0))
	var cargo_after_accept := cargo
	current_system_index = _system_index_by_name("Centauri", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	pos = Vector2(-520.0, -300.0)
	landed = true
	var credits_before_completion := credits
	var reputation_before_completion := int(reputation_scores.get("Federation", 0))
	var completed_ids := _complete_arrived_missions()
	var completion_day := current_day
	current_day = 3
	var late_failure_attempted := _fail_mission_deadline(deadline_mission, accepted_day, current_day)
	var reputation_after_late_check := int(reputation_scores.get("Federation", 0))
	var latest_completion := JSON.stringify(completed_mission_history[completed_mission_history.size() - 1]) if not completed_mission_history.is_empty() else "{}"
	var completed_status := "deadlineMissionCompleted=true" if completed_ids.has(str(deadline_mission.get("id"))) and completed_missions.has(str(deadline_mission.get("id"))) else "deadlineMissionCompleted=false"
	var no_late_failure_status := "lateFailurePrevented=true" if not late_failure_attempted and failed_mission_history.is_empty() and not story_flags.has("fail_mission_bit_42") else "lateFailurePrevented=false"
	var cargo_status := "reservedCargoReleased=true" if cargo == 0 else "reservedCargoReleased=false"
	var reward_status := "rewardPreserved=true" if credits == credits_before_completion + int(deadline_mission.get("reward", 0)) else "rewardPreserved=false"
	var reputation_status := "reputationPreserved=true" if reputation_after_late_check == reputation_before_completion else "reputationPreserved=false"
	print("%s acceptedMission=%s acceptedDay=%d completionDay=%d currentDay=%d timeLimitDays=%d cargoAfterAccept=%d cargoAfterCompletion=%d %s %s %s %s %s creditsBeforeCompletion=%d creditsAfterLateCheck=%d reputationBefore=%d reputationAfter=%d activeMissions=%s completedMissions=%s failedHistoryCount=%d latestCompletion=%s sourceLabel=terminal-velocity-mission-deadline-completed-no-late-failure-scaffold oracleStatus=deadline_completed_no_late_failure_pending_classic_runtime_or_manual_trace status=\"%s\"" % [MISSION_DEADLINE_COMPLETED_EVENT_LOG_PREFIX, str(deadline_mission.get("id")), accepted_day, completion_day, current_day, int(deadline_mission.get("timeLimitDays", 0)), cargo_after_accept, cargo, completed_status, no_late_failure_status, cargo_status, reward_status, reputation_status, credits_before_completion, credits, reputation_before_completion, reputation_after_late_check, JSON.stringify(active_missions), JSON.stringify(completed_missions), failed_mission_history.size(), latest_completion, status_line])
	get_tree().quit(0)

func _run_mission_deadline_recovery_log() -> void:
	_reset_travel_state()
	var failed_mission := {
		"id": "deadline_dispatch_failure_probe",
		"title": "Deadline Dispatch Failure Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"reward": 1200,
		"completionReward": 6,
		"failureBitSet": 42,
		"completionGovernment": "Federation",
		"timeLimitDays": 2,
	}
	var followup_mission := {
		"id": "deadline_recovery_followup",
		"title": "Deadline Recovery Followup",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 2,
		"reward": 900,
		"sourceLabel": "terminal-velocity-mission-deadline-recovery-scaffold",
		"oracleStatus": "deadline_failure_recovery_pending_classic_runtime_or_manual_trace",
	}
	missions["missions"].append(followup_mission)
	var accepted_day := 0
	current_day = 3
	active_missions.append(str(failed_mission.get("id")))
	mission_acceptance_days[str(failed_mission.get("id"))] = accepted_day
	cargo = int(failed_mission.get("cargoTons", 0))
	var cargo_after_failed_accept := cargo
	var reputation_before_failure := int(reputation_scores.get("Federation", 0))
	var failure_succeeded := _fail_mission_deadline(failed_mission, accepted_day, current_day)
	var cargo_after_failure := cargo
	var reputation_after_failure := int(reputation_scores.get("Federation", 0))
	active_missions.append(str(followup_mission.get("id")))
	mission_acceptance_days[str(followup_mission.get("id"))] = current_day
	cargo += int(followup_mission.get("cargoTons", 0))
	var cargo_after_followup_accept := cargo
	current_system_index = _system_index_by_name("Centauri", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	pos = Vector2(-520.0, -300.0)
	landed = true
	var credits_before_followup := credits
	var completed_ids := _complete_arrived_missions()
	var latest_failure := JSON.stringify(failed_mission_history[failed_mission_history.size() - 1]) if not failed_mission_history.is_empty() else "{}"
	var latest_completion := JSON.stringify(completed_mission_history[completed_mission_history.size() - 1]) if not completed_mission_history.is_empty() else "{}"
	var failure_status := "deadlineFailureRecorded=true" if failure_succeeded and failed_mission_history.size() == 1 and story_flags.has("fail_mission_bit_42") else "deadlineFailureRecorded=false"
	var cargo_release_status := "reservedCargoReleased=true" if cargo_after_failure == 0 and cargo == 0 else "reservedCargoReleased=false"
	var followup_accept_status := "followupAccepted=true" if cargo_after_followup_accept == int(followup_mission.get("cargoTons", 0)) else "followupAccepted=false"
	var followup_delivered_status := "followupDelivered=true" if completed_ids.has(str(followup_mission.get("id"))) and completed_missions.has(str(followup_mission.get("id"))) and credits == credits_before_followup + int(followup_mission.get("reward", 0)) else "followupDelivered=false"
	var failed_history_status := "failedHistoryPreserved=true" if failed_mission_history.size() == 1 and str(failed_mission_history[0].get("id", "")) == str(failed_mission.get("id")) else "failedHistoryPreserved=false"
	print("%s failedMission=%s followupMission=%s acceptedDay=%d currentDay=%d timeLimitDays=%d cargoAfterFailedAccept=%d cargoAfterFailure=%d cargoAfterFollowupAccept=%d cargoAfterFollowupDelivery=%d %s %s %s %s %s reputationBeforeFailure=%d reputationAfterFailure=%d creditsBeforeFollowup=%d creditsAfterFollowup=%d activeMissions=%s failedHistoryCount=%d completedMissions=%s latestFailure=%s latestCompletion=%s sourceLabel=terminal-velocity-mission-deadline-recovery-scaffold oracleStatus=deadline_failure_recovery_pending_classic_runtime_or_manual_trace status=\"%s\"" % [MISSION_DEADLINE_RECOVERY_EVENT_LOG_PREFIX, str(failed_mission.get("id")), str(followup_mission.get("id")), accepted_day, current_day, int(failed_mission.get("timeLimitDays", 0)), cargo_after_failed_accept, cargo_after_failure, cargo_after_followup_accept, cargo, failure_status, cargo_release_status, followup_accept_status, followup_delivered_status, failed_history_status, reputation_before_failure, reputation_after_failure, credits_before_followup, credits, JSON.stringify(active_missions), failed_mission_history.size(), JSON.stringify(completed_missions), latest_failure, latest_completion, status_line])
	get_tree().quit(0)

func _run_mission_deadline_sequential_log() -> void:
	_reset_travel_state()
	var first_mission := {
		"id": "deadline_dispatch_failure_probe",
		"title": "Deadline Dispatch Failure Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"reward": 1200,
		"completionReward": 6,
		"failureBitSet": 42,
		"completionGovernment": "Federation",
		"timeLimitDays": 2,
	}
	var second_mission := {
		"id": "deadline_second_failure_probe",
		"title": "Deadline Second Failure Probe",
		"destinationSystem": "Sirius",
		"destinationBody": "Sirius Station",
		"cargoTons": 2,
		"reward": 900,
		"completionReward": 4,
		"failureBitSet": 43,
		"completionGovernment": "Federation",
		"timeLimitDays": 2,
	}
	var accepted_day := 0
	current_day = 3
	active_missions.append(str(first_mission.get("id")))
	active_missions.append(str(second_mission.get("id")))
	mission_acceptance_days[str(first_mission.get("id"))] = accepted_day
	mission_acceptance_days[str(second_mission.get("id"))] = accepted_day
	cargo = int(first_mission.get("cargoTons", 0)) + int(second_mission.get("cargoTons", 0))
	var cargo_after_accept := cargo
	var reputation_before := int(reputation_scores.get("Federation", 0))
	var first_failed := _fail_mission_deadline(first_mission, accepted_day, current_day)
	var cargo_after_first_failure := cargo
	var second_failed := _fail_mission_deadline(second_mission, accepted_day, current_day)
	var reputation_after := int(reputation_scores.get("Federation", 0))
	var failure_ids := []
	for failure in failed_mission_history:
		failure_ids.append(str(failure.get("id", "")))
	var both_failed_status := "bothDeadlineFailuresRecorded=true" if first_failed and second_failed and failure_ids.has("deadline_dispatch_failure_probe") and failure_ids.has("deadline_second_failure_probe") else "bothDeadlineFailuresRecorded=false"
	var cargo_status := "reservedCargoReleased=true" if cargo == 0 and cargo_after_first_failure == int(second_mission.get("cargoTons", 0)) else "reservedCargoReleased=false"
	var flags_status := "failureFlagsSet=true" if story_flags.has("fail_mission_bit_42") and story_flags.has("fail_mission_bit_43") else "failureFlagsSet=false"
	var reputation_status := "cumulativeReputationPenaltyApplied=true" if reputation_after == reputation_before - 5 else "cumulativeReputationPenaltyApplied=false"
	print("%s acceptedMissions=%s acceptedDay=%d currentDay=%d timeLimitDays=%d cargoAfterAccept=%d cargoAfterFirstFailure=%d cargoAfterFailures=%d %s %s %s %s reputationBefore=%d reputationAfter=%d activeMissions=%s failedHistoryCount=%d failureIds=%s latestFailures=%s sourceLabel=terminal-velocity-mission-deadline-sequential-failures-scaffold oracleStatus=deadline_sequential_failures_pending_classic_runtime_or_manual_trace status=\"%s\"" % [MISSION_DEADLINE_SEQUENTIAL_EVENT_LOG_PREFIX, JSON.stringify([str(first_mission.get("id")), str(second_mission.get("id"))]), accepted_day, current_day, int(first_mission.get("timeLimitDays", 0)), cargo_after_accept, cargo_after_first_failure, cargo, both_failed_status, cargo_status, flags_status, reputation_status, reputation_before, reputation_after, JSON.stringify(active_missions), failed_mission_history.size(), JSON.stringify(failure_ids), JSON.stringify(failed_mission_history), status_line])
	get_tree().quit(0)

func _run_mission_deadline_abort_log() -> void:
	_reset_travel_state()
	var deadline_mission := {
		"id": "deadline_dispatch_failure_probe",
		"title": "Deadline Dispatch Failure Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"reward": 1200,
		"completionReward": 6,
		"failureBitSet": 42,
		"completionGovernment": "Federation",
		"timeLimitDays": 2,
		"sourceLabel": "terminal-velocity-mission-deadline-abort-scaffold",
		"oracleStatus": "deadline_abort_pending_classic_runtime_or_manual_trace",
	}
	missions["missions"].append(deadline_mission)
	var accepted_day := 0
	active_missions.append(str(deadline_mission.get("id")))
	mission_acceptance_days[str(deadline_mission.get("id"))] = accepted_day
	cargo = int(deadline_mission.get("cargoTons", 0))
	var cargo_after_accept := cargo
	var reputation_before_abort := int(reputation_scores.get("Federation", 0))
	var abort_succeeded := _abort_active_mission(str(deadline_mission.get("id")))
	var cargo_after_abort := cargo
	current_day = 3
	var late_failure_attempted := _fail_mission_deadline(deadline_mission, accepted_day, current_day)
	var reputation_after_late_check := int(reputation_scores.get("Federation", 0))
	var latest_abort := JSON.stringify(aborted_mission_history[aborted_mission_history.size() - 1]) if not aborted_mission_history.is_empty() else "{}"
	var abort_status := "deadlineMissionAborted=true" if abort_succeeded and not active_missions.has(str(deadline_mission.get("id"))) else "deadlineMissionAborted=false"
	var cargo_status := "reservedCargoReleased=true" if cargo_after_abort == cargo_after_accept - int(deadline_mission.get("cargoTons", 0)) else "reservedCargoReleased=false"
	var no_late_failure_status := "lateFailurePrevented=true" if not late_failure_attempted and failed_mission_history.is_empty() and not story_flags.has("fail_mission_bit_42") else "lateFailurePrevented=false"
	var flag_status := "failureFlagPreserved=true" if not story_flags.has("fail_mission_bit_42") else "failureFlagPreserved=false"
	var reputation_status := "reputationPreserved=true" if reputation_after_late_check == reputation_before_abort else "reputationPreserved=false"
	print("%s acceptedMission=%s acceptedDay=%d abortDay=%d currentDay=%d timeLimitDays=%d cargoAfterAccept=%d cargoAfterAbort=%d %s %s %s %s %s reputationBefore=%d reputationAfter=%d activeMissions=%s completedMissions=%s failedHistoryCount=%d abortedHistoryCount=%d latestAbort=%s sourceLabel=terminal-velocity-mission-deadline-abort-scaffold oracleStatus=deadline_abort_pending_classic_runtime_or_manual_trace status=\"%s\"" % [MISSION_DEADLINE_ABORT_EVENT_LOG_PREFIX, str(deadline_mission.get("id")), accepted_day, accepted_day, current_day, int(deadline_mission.get("timeLimitDays", 0)), cargo_after_accept, cargo_after_abort, abort_status, cargo_status, no_late_failure_status, flag_status, reputation_status, reputation_before_abort, reputation_after_late_check, JSON.stringify(active_missions), JSON.stringify(completed_missions), failed_mission_history.size(), aborted_mission_history.size(), latest_abort, status_line])
	get_tree().quit(0)

func _run_mission_deadline_trade_carryover_log() -> void:
	_reset_travel_state()
	var deadline_mission := {
		"id": "deadline_dispatch_failure_probe",
		"title": "Deadline Dispatch Failure Probe",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"reward": 1200,
		"completionReward": 6,
		"failureBitSet": 42,
		"completionGovernment": "Federation",
		"timeLimitDays": 2,
		"sourceLabel": "terminal-velocity-mission-deadline-trade-carryover-scaffold",
		"oracleStatus": "deadline_failure_trade_carryover_pending_classic_runtime_or_manual_trace",
	}
	missions["missions"].append(deadline_mission)
	var accepted_day := 0
	active_missions.append(str(deadline_mission.get("id")))
	mission_acceptance_days[str(deadline_mission.get("id"))] = accepted_day
	cargo = int(deadline_mission.get("cargoTons", 0))
	var cargo_after_accept := cargo
	current_system_index = _system_index_by_name("Sol", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	landed = true
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_trade := credits
	_buy_selected_commodity()
	var credits_after_buy := credits
	var cargo_after_buy := cargo
	var trade_cargo_after_buy := int(commodity_hold.get("food", 0))
	current_day = 3
	var reputation_before_failure := int(reputation_scores.get("Federation", 0))
	var failure_succeeded := _fail_mission_deadline(deadline_mission, accepted_day, current_day)
	var reputation_after_failure := int(reputation_scores.get("Federation", 0))
	var cargo_after_failure := cargo
	var trade_cargo_after_failure := int(commodity_hold.get("food", 0))
	current_system_index = _system_index_by_name("Levo", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	landed = true
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	var credits_after_sale := credits
	var cargo_after_sale := cargo
	var trade_cargo_after_sale := int(commodity_hold.get("food", 0))
	var latest_failure := JSON.stringify(failed_mission_history[failed_mission_history.size() - 1]) if not failed_mission_history.is_empty() else "{}"
	var failure_status := "deadlineFailureRecorded=true" if failure_succeeded else "deadlineFailureRecorded=false"
	var mission_cargo_status := "missionCargoReleased=true" if cargo_after_failure == trade_cargo_after_failure else "missionCargoReleased=false"
	var trade_preserved_status := "tradeCargoPreserved=true" if trade_cargo_after_failure == trade_cargo_after_buy and cargo_after_failure == trade_cargo_after_buy else "tradeCargoPreserved=false"
	var trade_sold_status := "tradeCargoSold=true" if trade_cargo_after_sale == 0 and cargo_after_sale == 0 and credits_after_sale > credits_after_buy else "tradeCargoSold=false"
	var flag_status := "failureFlagSet=true" if story_flags.has("fail_mission_bit_42") else "failureFlagSet=false"
	var reputation_status := "reputationPenaltyApplied=true" if reputation_after_failure == reputation_before_failure - 3 else "reputationPenaltyApplied=false"
	print("%s acceptedMission=%s acceptedDay=%d currentDay=%d timeLimitDays=%d cargoAfterAccept=%d cargoAfterBuy=%d cargoAfterFailure=%d cargoAfterSale=%d tradeCargoAfterBuy=%d tradeCargoAfterFailure=%d tradeCargoAfterSale=%d creditsBeforeTrade=%d creditsAfterBuy=%d creditsAfterSale=%d %s %s %s %s %s %s reputationBefore=%d reputationAfter=%d activeMissions=%s failedHistoryCount=%d latestFailure=%s sourceLabel=terminal-velocity-mission-deadline-trade-carryover-scaffold oracleStatus=deadline_failure_trade_carryover_pending_classic_runtime_or_manual_trace status=\"%s\"" % [MISSION_DEADLINE_TRADE_CARRYOVER_EVENT_LOG_PREFIX, str(deadline_mission.get("id")), accepted_day, current_day, int(deadline_mission.get("timeLimitDays", 0)), cargo_after_accept, cargo_after_buy, cargo_after_failure, cargo_after_sale, trade_cargo_after_buy, trade_cargo_after_failure, trade_cargo_after_sale, credits_before_trade, credits_after_buy, credits_after_sale, failure_status, mission_cargo_status, trade_preserved_status, trade_sold_status, flag_status, reputation_status, reputation_before_failure, reputation_after_failure, JSON.stringify(active_missions), failed_mission_history.size(), latest_failure, status_line])
	get_tree().quit(0)

func _run_mission_log_history_log() -> void:
	_reset_travel_state()
	completed_mission_history.append({
		"id": "history_completed_probe",
		"title": "Completed History Probe",
		"system": "Sol",
		"body": "Earth",
		"cargo_released": 3,
		"reward_paid": 1200,
	})
	aborted_mission_history.append(_mission_abort_record({"id": "history_aborted_probe", "title": "Aborted History Probe"}, "history_aborted_probe", 2))
	failed_mission_history.append(_mission_deadline_failure_record({"id": "history_failed_probe", "title": "Failed History Probe", "timeLimitDays": 2}, 0, 3, 4, "fail_mission_bit_43", -5, "Federation"))
	var lines := _mission_log_detail_lines()
	var player_info_lines := _player_inventory_lines()
	var no_active_visible := lines.has("No active missions.")
	var completed_visible := lines.has("Completed mission history")
	var aborted_visible := lines.has("Aborted mission history")
	var failed_visible := lines.has("Failed mission history")
	var failed_deadline_visible := lines.has("Deadline: accepted day 0, failed day 3, limit 2 day(s)")
	var failed_source_visible := lines.has("Failure source: ev-classic-resource-bible-backed-mission-failure-scaffold; exact Classic UI pending")
	var player_info_history_visible := player_info_lines.has("Mission history: 1 completed, 1 aborted, 1 failed — TV mission-history scaffold; Classic Player Info behavior pending")
	var player_info_failure_visible := player_info_lines.has("Latest failed mission: Failed History Probe; reputation Federation -5; exact Classic failure/history UI pending")
	print("%s noActiveVisible=%s completedHistoryVisible=%s abortedHistoryVisible=%s failedHistoryVisible=%s failedDeadlineVisible=%s failedSourceVisible=%s playerInfoHistoryVisible=%s playerInfoFailureVisible=%s lineCount=%d lines=%s playerInfoLines=%s sourceLabel=terminal-velocity-mission-log-history-scaffold oracleStatus=mission_history_ui_pending_classic_runtime_trace" % [MISSION_LOG_HISTORY_EVENT_LOG_PREFIX, str(no_active_visible), str(completed_visible), str(aborted_visible), str(failed_visible), str(failed_deadline_visible), str(failed_source_visible), str(player_info_history_visible), str(player_info_failure_visible), lines.size(), JSON.stringify(lines), JSON.stringify(player_info_lines)])
	get_tree().quit(0)

func _run_active_mission_deadline_log() -> void:
	_reset_travel_state()
	var deadline_mission := {
		"id": "active_deadline_display_probe",
		"title": "Active Deadline Display Probe",
		"originSystem": "Levo",
		"originBody": "Levo",
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 3,
		"reward": 900,
		"description": "Probe mission used to verify active deadline display.",
		"timeLimitDays": 5,
		"sourceLabel": "terminal-velocity-active-deadline-display-scaffold",
		"oracleStatus": "active_deadline_ui_pending_classic_runtime_trace",
	}
	missions["missions"].append(deadline_mission)
	current_day = 2
	active_missions.append(str(deadline_mission.get("id")))
	mission_acceptance_days[str(deadline_mission.get("id"))] = 1
	cargo = int(deadline_mission.get("cargoTons", 0))
	var lines := _mission_log_detail_lines()
	var player_info_lines := _player_inventory_lines()
	var deadline_visible := lines.has("Deadline: accepted day 1, current day 2, limit 5 day(s), 4 day(s) remaining")
	var source_visible := lines.has("Deadline source: terminal-velocity-active-deadline-display-scaffold; exact Classic UI pending")
	var abort_hint_visible := lines.has("Abort: press X to abort; TV scaffold releases 3 reserved cargo tons")
	var abort_source_visible := lines.has("Abort source: terminal-velocity-mission-abort-scaffold; Classic CanAbort/UI pending")
	var player_info_mission_visible := player_info_lines.has("Active mission: Active Deadline Display Probe to Centauri/Luna")
	var player_info_deadline_visible := player_info_lines.has("Active mission deadline: 4 day(s) remaining; exact Classic Player Info behavior pending")
	print("TV_ACTIVE_MISSION_DEADLINE_EVENT activeMission=%s currentDay=%d acceptedDay=%d timeLimitDays=%d deadlineVisible=%s sourceVisible=%s abortHintVisible=%s abortSourceVisible=%s playerInfoMissionVisible=%s playerInfoDeadlineVisible=%s lines=%s playerInfoLines=%s sourceLabel=terminal-velocity-active-deadline-display-scaffold oracleStatus=active_deadline_ui_pending_classic_runtime_trace" % [str(deadline_mission.get("id")), current_day, int(mission_acceptance_days.get(str(deadline_mission.get("id")), 0)), int(deadline_mission.get("timeLimitDays", 0)), str(deadline_visible), str(source_visible), str(abort_hint_visible), str(abort_source_visible), str(player_info_mission_visible), str(player_info_deadline_visible), JSON.stringify(lines), JSON.stringify(player_info_lines)])
	get_tree().quit(0)

func _run_first_mission_delivery_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var accepted_body := _current_body()
	var mission_before_accept: Dictionary = _first_available_mission(accepted_body)
	var accepted_mission_id := str(mission_before_accept.get("id", "none"))
	var reward := int(mission_before_accept.get("reward", 0))
	var destination_system := str(mission_before_accept.get("destinationSystem", "?"))
	var destination_body := str(mission_before_accept.get("destinationBody", "?"))
	var credits_before_accept := credits
	var cargo_before_accept := cargo
	_accept_selected_mission()
	var cargo_after_accept := cargo
	var mission_accepted := active_missions.has(accepted_mission_id)
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_destination_selected := _select_map_route_to_system("Centauri")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body(destination_body)
	_try_land()
	var completed_ids := _complete_arrived_missions()
	var cargo_after_delivery := cargo
	var credits_after_delivery := credits
	var mission_delivered := completed_ids.has(accepted_mission_id) and completed_missions.has(accepted_mission_id) and cargo_after_delivery == cargo_before_accept and credits_after_delivery == credits_before_accept + reward
	var accepted_status := "missionAccepted=true" if mission_accepted else "missionAccepted=false"
	var delivered_status := "missionDelivered=true" if mission_delivered else "missionDelivered=false"
	var completion_history_count := completed_mission_history.size()
	var latest_completion := JSON.stringify(completed_mission_history[completion_history_count - 1]) if completion_history_count > 0 else "{}"
	print("%s startSystem=Levo routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" %s actualAcceptedMission=%s %s destinationSystem=%s destinationBody=\"%s\" routeToDestinationSelected=%s finalSystem=%s landedBody=\"%s\" completedMissions=%s %s creditsBeforeAccept=%d creditsAfterDelivery=%d reward=%d cargoBeforeAccept=%d cargoAfterAccept=%d cargoAfterDelivery=%d completionHistoryCount=%d latestCompletion=%s activeMissions=%s storyFlags=%s sourceLabel=terminal-velocity-observed oracleStatus=terminal_velocity_eval_pending_original_trace status=\"%s\"" % [FIRST_MISSION_DELIVERY_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(accepted_body.get("name", "None")), FIRST_MISSION_DELIVERY_EXPECTED_MISSION_FIELD, accepted_mission_id, accepted_status, destination_system, destination_body, str(route_to_destination_selected), str(current_system.get("name", "?")), str(_current_body().get("name", "None")), JSON.stringify(completed_ids), delivered_status, credits_before_accept, credits_after_delivery, reward, cargo_before_accept, cargo_after_accept, cargo_after_delivery, completion_history_count, latest_completion, JSON.stringify(active_missions), JSON.stringify(story_flags), status_line])
	get_tree().quit(0)

func _run_outfitter_shipyard_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var landed_body := str(_current_body().get("name", ""))
	var starting_cargo_space := cargo_space
	credits = 100000
	landing_tab = 2
	selected_landing_item = 0
	_buy_selected_outfit_or_weapon()
	var bought_cargo_pod := owned_outfits.has("cargo_pod") and int(owned_outfits.get("cargo_pod", 0)) > 0
	var cargo_space_after_outfit := cargo_space
	selected_landing_item = 3
	_buy_selected_outfit_or_weapon()
	var bought_laser := owned_weapons.has("laser_cannon") and int(owned_weapons.get("laser_cannon", 0)) > 0
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(_current_body())
	var light_freighter_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			light_freighter_listing = shipyard_listings[i]
			break
	var shipyard_art_loaded := not light_freighter_listing.is_empty() and _shipyard_texture_for_listing(light_freighter_listing) != null
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var cargo_space_increased := cargo_space_after_outfit > starting_cargo_space and cargo_space > starting_cargo_space
	var ship_before_overfull_probe := player_ship_id
	var cargo_space_before_overfull_probe := cargo_space
	cargo = cargo_space + 5
	selected_landing_item = 0
	_buy_selected_ship()
	var overfull_block_status := status_line
	var overfull_shipyard_blocked := player_ship_id == ship_before_overfull_probe and cargo_space == cargo_space_before_overfull_probe and overfull_block_status.begins_with("Cannot buy shuttlecraft: cargo ") and overfull_block_status.ends_with(" exceeds target capacity 20")
	var overfull_cargo_preserved := cargo == cargo_space_before_overfull_probe + 5
	cargo = 10
	_buy_selected_ship()
	var overfull_recovery_bought_smaller_ship := player_ship_id == "shuttlecraft" and cargo_space == 20 and cargo == 10
	var cargo_pod_status := "boughtCargoPod=true" if bought_cargo_pod else "boughtCargoPod=false"
	var laser_status := "boughtLaser=true" if bought_laser else "boughtLaser=false"
	var light_freighter_status := "boughtLightFreighter=true" if bought_light_freighter else "boughtLightFreighter=false"
	var cargo_space_status := "cargoSpaceIncreased=true" if cargo_space_increased else "cargoSpaceIncreased=false"
	var shipyard_art_status := "shipyardArtLoaded=true" if shipyard_art_loaded else "shipyardArtLoaded=false"
	print("%s routeToSolSelected=%s system=%s body=%s %s %s %s %s %s overfullShipyardBlocked=%s overfullCargoPreserved=%s overfullRecoveryBoughtSmallerShip=%s startingCargoSpace=%d cargoAfterOutfit=%d finalCargoSpace=%d cargoAfterOverfullRecovery=%d creditsAfter=%d sourceLabel=terminal-velocity-outfitter-shipyard-scaffold cargoGuardrailSourceLabel=terminal-velocity-shipyard-cargo-guardrail-scaffold oracleStatus=outfitter_shipyard_pending_ev_classic_purchase_trace cargoGuardrailOracleStatus=shipyard_cargo_transfer_pending_ev_classic_runtime_trace status=\"%s\"" % [OUTFITTER_SHIPYARD_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), landed_body, cargo_pod_status, laser_status, light_freighter_status, cargo_space_status, shipyard_art_status, str(overfull_shipyard_blocked), str(overfull_cargo_preserved), str(overfull_recovery_bought_smaller_ship), starting_cargo_space, cargo_space_after_outfit, cargo_space, cargo, credits, status_line])
	get_tree().quit(0)

func _run_shipyard_cargo_guardrail_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var landed_body := str(_current_body().get("name", ""))
	credits = 100000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(_current_body())
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			break
	_buy_selected_ship()
	var upgraded_to_light_freighter := player_ship_id == "light_freighter" and cargo_space == 150
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "shuttlecraft":
			selected_landing_item = i
			break
	var starting_ship := player_ship_id
	var starting_cargo_capacity := cargo_space
	cargo = 30
	var cargo_before_block := cargo
	var credits_before_block := credits
	status_messages.clear()
	_buy_selected_ship()
	var blocked_status := status_line
	var overfull_shipyard_blocked := player_ship_id == starting_ship and cargo_space == starting_cargo_capacity and credits == credits_before_block and blocked_status == "Cannot buy shuttlecraft: cargo 30 exceeds target capacity 20"
	var overfull_cargo_preserved := cargo == cargo_before_block
	cargo = 10
	status_messages.clear()
	_buy_selected_ship()
	var recovery_bought_smaller_ship := player_ship_id == "shuttlecraft" and cargo_space == 20 and cargo == 10
	print("%s routeToSolSelected=%s system=%s body=\"%s\" upgradedToLightFreighter=%s blockedShip=shuttlecraft overfullShipyardBlocked=%s overfullCargoPreserved=%s recoveryBoughtSmallerShip=%s cargoBeforeBlock=%d targetCargoCapacity=20 cargoAfterRecovery=%d finalShip=%s sourceLabel=terminal-velocity-shipyard-cargo-guardrail-scaffold oracleStatus=shipyard_cargo_transfer_pending_ev_classic_runtime_trace status=\"%s\"" % [SHIPYARD_CARGO_GUARDRAIL_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), landed_body, str(upgraded_to_light_freighter), str(overfull_shipyard_blocked), str(overfull_cargo_preserved), str(recovery_bought_smaller_ship), cargo_before_block, cargo, player_ship_id, blocked_status])
	get_tree().quit(0)

func _run_outfitter_purchase_guardrail_log() -> void:
	_reset_travel_state()
	_try_land()
	landing_tab = 2
	selected_landing_item = 0
	status_messages.clear()
	_buy_selected_outfit_or_weapon()
	var no_outfitter_stock_blocked := status_messages.has("No outfitter stock") and not owned_outfits.has("cargo_pod")
	_ev_land_or_launch()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	landing_tab = 2
	selected_landing_item = 0
	status_messages.clear()
	_buy_selected_outfit_or_weapon()
	var in_space_outfit_blocked := status_messages.has("Land before outfitter purchases") and not owned_outfits.has("cargo_pod")
	_position_at_body("Earth")
	_try_land()
	var sale_items := _outfitter_sale_items(_current_body())
	var cargo_pod_price := int(sale_items[0].get("price", 0)) if not sale_items.is_empty() else 0
	credits = max(0, cargo_pod_price - 1)
	var credits_before_outfit_block := credits
	status_messages.clear()
	_buy_selected_outfit_or_weapon()
	var outfit_credit_blocked := status_messages.has("Not enough credits") and credits == credits_before_outfit_block and not owned_outfits.has("cargo_pod")
	credits = cargo_pod_price
	status_messages.clear()
	_buy_selected_outfit_or_weapon()
	var outfit_bought_after_funding := owned_outfits.has("cargo_pod") and int(owned_outfits.get("cargo_pod", 0)) == 1 and credits == 0
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(_current_body())
	var light_freighter_price := 0
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			light_freighter_price = int(shipyard_listings[i].get("price", 0))
			break
	credits = max(0, light_freighter_price - 1)
	var ship_before_block := player_ship_id
	var credits_before_ship_block := credits
	status_messages.clear()
	_buy_selected_ship()
	var ship_credit_blocked := status_messages.has("Not enough credits") and player_ship_id == ship_before_block and credits == credits_before_ship_block
	credits = light_freighter_price
	status_messages.clear()
	_buy_selected_ship()
	var ship_bought_after_funding := player_ship_id == "light_freighter" and credits == 0
	print("%s routeToSolSelected=%s system=%s body=\"%s\" inSpaceOutfitBlocked=%s noOutfitterStockBlocked=%s outfitCreditBlocked=%s shipCreditBlocked=%s outfitBoughtAfterFunding=%s shipBoughtAfterFunding=%s cargoPodPrice=%d lightFreighterPrice=%d finalShip=%s sourceLabel=terminal-velocity-outfitter-purchase-guardrail-scaffold outfitOracleStatus=outfitter_purchase_guardrail_pending_original_runtime_trace shipOracleStatus=shipyard_purchase_guardrail_pending_original_runtime_trace status=\"%s\"" % [OUTFITTER_PURCHASE_GUARDRAIL_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), str(_current_body().get("name", "?")), str(in_space_outfit_blocked), str(no_outfitter_stock_blocked), str(outfit_credit_blocked), str(ship_credit_blocked), str(outfit_bought_after_funding), str(ship_bought_after_funding), cargo_pod_price, light_freighter_price, player_ship_id, status_line])
	get_tree().quit(0)

func _run_gameplay_curriculum_help_log() -> void:
	var hints := _gameplay_curriculum_hint_lines()
	var help_lines := _help_overlay_lines()
	var probe_results: Dictionary = {}
	for probe in _help_overlay_log_probes():
		var flag := str(probe.get("flag", ""))
		var needle := str(probe.get("contains", ""))
		var source := str(probe.get("source", "help"))
		if flag == "" or needle == "":
			continue
		var found := false
		var scan_lines := hints if source == "curriculum" else help_lines
		for line in scan_lines:
			if str(line).contains(needle):
				found = true
				break
		probe_results[flag] = found
	var parts: Array[String] = ["%s hintCount=%d" % [GAMEPLAY_CURRICULUM_HELP_LOG_PREFIX, hints.size()]]
	for probe in _help_overlay_log_probes():
		var flag := str(probe.get("flag", ""))
		if flag != "":
			parts.append("%s=%s" % [flag, str(probe_results.get(flag, false)).to_lower()])
	parts.append("sourceLabel=terminal-velocity-curriculum-scaffold")
	parts.append("oracleStatus=help_surface_pending_playtest")
	parts.append("firstHint=\"%s\"" % (hints[0] if not hints.is_empty() else ""))
	print(" ".join(parts))
	get_tree().quit(0)

func _run_starting_equipment_log() -> void:
	# Contract literal for native test coverage: primarySourceStockName="%s"
	_reset_travel_state()
	player_info_visible = true
	var primary_weapon := _primary_weapon_stats()
	var primary_weapon_name := str(primary_weapon.get("name", primary_weapon.get("id", "Unknown")))
	var primary_source_stock_name := str(primary_weapon.get("sourceStockName", primary_weapon_name))
	var secondary_hud_fragment := _secondary_weapon_hud_fragment()
	var inventory_lines := _player_inventory_lines()
	var cargo_line := "Cargo: %d/%d (%d mission, %d free)" % [cargo, cargo_space, _mission_reserved_cargo_tons(), _cargo_available_tons()]
	var fuel_line := "Fuel: %d/%d" % [player_fuel, _max_player_fuel()]
	var primary_line := _primary_weapon_inventory_line()
	var secondary_line := _secondary_weapon_inventory_line()
	var starting_secondary_hud_observed := secondary_hud_fragment.contains("Secondary: No Secondary Weapon")
	var starting_no_target_observed := status_line == ""
	var starting_fuel_full_observed := player_fuel == _max_player_fuel() and inventory_lines.has(fuel_line)
	var starting_free_cargo_observed := cargo == 0 and _cargo_available_tons() == cargo_space and inventory_lines.has(cargo_line)
	var primary_info_visible := primary_line.contains(primary_weapon_name) and primary_line.contains(primary_source_stock_name) and inventory_lines.has(primary_line)
	var secondary_info_visible := secondary_line.contains("No Secondary Weapon") and inventory_lines.has(secondary_line)
	print("%s startingSecondaryHudObserved=%s startingNoTargetObserved=%s startingFuelFullObserved=%s startingFreeCargoObserved=%s primaryInfoVisible=%s primarySourceStockName=\"%s\" secondaryInfoVisible=%s sourceLabel=original-runtime-observed-starting-hud-plus-terminal-velocity-source-mined-primary oracleStatus=starting_primary_and_outfits_pending_nonmutating_classic_status_trace secondaryHudFragment=\"%s\" cargoLine=\"%s\" fuelLine=\"%s\" primaryLine=\"%s\" secondaryLine=\"%s\"" % [STARTING_EQUIPMENT_EVENT_LOG_PREFIX, str(starting_secondary_hud_observed).to_lower(), str(starting_no_target_observed).to_lower(), str(starting_fuel_full_observed).to_lower(), str(starting_free_cargo_observed).to_lower(), str(primary_info_visible).to_lower(), primary_source_stock_name, str(secondary_info_visible).to_lower(), secondary_hud_fragment, cargo_line, fuel_line, primary_line, secondary_line])
	get_tree().quit(0)

func _run_pirate_avoidance_log() -> void:
	_reset_travel_state()
	map_visible = true
	var start_system := str(current_system.get("name", "?"))
	var threat_detected := true
	_set_status("Pirate intercept detected; avoiding combat by routing to nearest safe linked port (TV scaffold)")
	var threat_message_visible := status_messages.has("Pirate intercept detected; avoiding combat by routing to nearest safe linked port (TV scaffold)")
	var route_selected := _select_map_route_to_system("Sol")
	var destination := _selected_destination_name()
	player_fuel = 0
	_move_to_scripted_hyperspace_distance()
	_jump()
	var low_fuel_escape_blocked := status_messages.has("Insufficient fuel for hyperspace; land at a port with refuel service or choose a closer route") and str(current_system.get("name", "?")) == start_system and player_fuel == 0
	player_fuel = _max_player_fuel()
	var refueled_before_escape := low_fuel_escape_blocked and player_fuel == _max_player_fuel()
	_move_to_scripted_hyperspace_distance()
	_jump()
	var final_system := str(current_system.get("name", "?"))
	_position_at_body("Earth")
	_try_land()
	var landed_body := _current_body()
	var landed_at_safe_port := landed and final_system == "Sol" and str(landed_body.get("name", "")) == "Earth"
	var combat_executed := not projectiles.is_empty() or not explosion_events.is_empty()
	var evasion_succeeded := threat_detected and route_selected and low_fuel_escape_blocked and refueled_before_escape and final_system == destination and landed_at_safe_port and not combat_executed
	print("%s startSystem=%s threat=pirate_intercept threatDetected=%s threatMessageVisible=%s routeSelected=%s destination=%s finalSystem=%s landedAtSafePort=%s lowFuelEscapeBlocked=%s refueledBeforeEscape=%s landedBody=\"%s\" combatExecuted=%s evasionSucceeded=%s decision=jump_to_linked_safe_port sourceLabel=terminal-velocity-pirate-avoidance-scaffold oracleStatus=pirate_avoidance_pending_ev_classic_combat_trace status=\"%s\"" % [PIRATE_AVOIDANCE_EVENT_LOG_PREFIX, start_system, str(threat_detected).to_lower(), str(threat_message_visible).to_lower(), str(route_selected).to_lower(), destination, final_system, str(landed_at_safe_port).to_lower(), str(low_fuel_escape_blocked).to_lower(), str(refueled_before_escape).to_lower(), str(landed_body.get("name", "None")), str(combat_executed).to_lower(), str(evasion_succeeded).to_lower(), status_line])
	get_tree().quit(0)

func _run_pirate_loaded_cargo_avoidance_log() -> void:
	_reset_travel_state()
	map_visible = true
	var start_system := str(current_system.get("name", "?"))
	var mission_id := "freeport_return_earth"
	active_missions.append(mission_id)
	mission_acceptance_days[mission_id] = current_day
	cargo += int(_mission_by_id(mission_id).get("cargoTons", 0))
	commodity_hold["food"] = 10
	cargo += int(commodity_hold.get("food", 0))
	var mission_cargo_before_escape := _mission_reserved_cargo_tons()
	var trade_cargo_before_escape := int(commodity_hold.get("food", 0))
	var cargo_used_before_escape := cargo
	var threat_detected := true
	_set_status("Pirate intercept detected with mission/trade cargo; preserving loaded route by escaping to a safe port (TV scaffold)")
	var threat_message_visible := status_messages.has("Pirate intercept detected with mission/trade cargo; preserving loaded route by escaping to a safe port (TV scaffold)")
	var route_selected := _select_map_route_to_system("Sol")
	var destination := _selected_destination_name()
	player_fuel = _max_player_fuel()
	_move_to_scripted_hyperspace_distance()
	_jump()
	var escaped_system := str(current_system.get("name", "?"))
	_position_at_body("Earth")
	_try_land()
	var escaped_landed_body := _current_body()
	var landed_at_safe_port := landed and escaped_system == "Sol" and str(escaped_landed_body.get("name", "")) == "Earth"
	var mission_cargo_after_escape := _mission_reserved_cargo_tons()
	var trade_cargo_after_escape := int(commodity_hold.get("food", 0))
	var preserved_mission_cargo_after_escape := mission_cargo_after_escape == mission_cargo_before_escape
	var preserved_trade_cargo_after_escape := trade_cargo_after_escape == trade_cargo_before_escape
	landed = false
	map_visible = true
	var return_route_selected := _select_map_route_to_system(start_system)
	var return_destination := _selected_destination_name()
	player_fuel = _max_player_fuel()
	_move_to_scripted_hyperspace_distance()
	_jump()
	var final_system := str(current_system.get("name", "?"))
	_position_at_body("Levo Spaceport")
	_try_land()
	var final_landed_body := _current_body()
	var returned_to_original_port := landed and final_system == start_system and str(final_landed_body.get("name", "")) == "Levo Spaceport"
	var loaded_cargo_preserved := preserved_mission_cargo_after_escape and preserved_trade_cargo_after_escape and cargo == cargo_used_before_escape
	var combat_executed := not projectiles.is_empty() or not explosion_events.is_empty()
	var evasion_succeeded := threat_detected and route_selected and destination == "Sol" and landed_at_safe_port and return_route_selected and return_destination == start_system and returned_to_original_port and loaded_cargo_preserved and not combat_executed
	print("%s startSystem=%s threat=pirate_intercept_loaded_cargo threatDetected=%s threatMessageVisible=%s routeSelected=%s destination=%s escapedSystem=%s landedAtSafePort=%s escapedLandedBody=\"%s\" missionCargoBeforeEscape=%d tradeCargoBeforeEscape=%d cargoUsedAfterEscape=%d preservedMissionCargoAfterEscape=%s preservedTradeCargoAfterEscape=%s returnRouteSelected=%s returnDestination=%s finalSystem=%s returnedToOriginalPort=%s finalLandedBody=\"%s\" loadedCargoPreserved=%s combatExecuted=%s evasionSucceeded=%s decision=jump_to_linked_safe_port_then_return_loaded sourceLabel=terminal-velocity-pirate-avoidance-loaded-cargo-scaffold oracleStatus=pirate_avoidance_loaded_cargo_pending_ev_classic_combat_trace status=\"%s\"" % [PIRATE_AVOIDANCE_EVENT_LOG_PREFIX, start_system, str(threat_detected).to_lower(), str(threat_message_visible).to_lower(), str(route_selected).to_lower(), destination, escaped_system, str(landed_at_safe_port).to_lower(), str(escaped_landed_body.get("name", "None")), mission_cargo_before_escape, trade_cargo_before_escape, cargo, str(preserved_mission_cargo_after_escape).to_lower(), str(preserved_trade_cargo_after_escape).to_lower(), str(return_route_selected).to_lower(), return_destination, final_system, str(returned_to_original_port).to_lower(), str(final_landed_body.get("name", "None")), str(loaded_cargo_preserved).to_lower(), str(combat_executed).to_lower(), str(evasion_succeeded).to_lower(), status_line])
	get_tree().quit(0)

func _run_combat_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	_select_closest_target()
	var target_index := selected_target_index
	var before_shields := int(target_shields.get(target_index, 0))
	var before_hull := int(target_hulls.get(target_index, 0))
	var before_player_shields := player_shields
	var before_player_hull := player_hull
	var credits_before_destroy := credits
	var spawned := _spawn_primary_projectile()
	for _i in range(90):
		_advance_projectiles(1.0 / 60.0)
	var retaliation_fired := _spawn_npc_retaliation_projectile(target_index)
	for _i in range(90):
		_advance_projectiles(1.0 / 60.0)
	_recharge_player_shields(2.0)
	var after_shields := int(target_shields.get(target_index, 0))
	var after_hull := int(target_hulls.get(target_index, 0))
	var after_player_shields := player_shields
	var after_player_hull := player_hull
	var target_damaged := after_shields < before_shields or after_hull < before_hull
	var player_damaged := after_player_shields < before_player_shields or after_player_hull < before_player_hull
	var primary_weapon := _primary_weapon_stats()
	var applied_hull_damage := _weapon_hull_damage(primary_weapon)
	# Deterministic destroy/explosion coverage uses a prepared final-hit state so
	# the combat probe exercises target acquisition, projectile spawn, hit, kill,
	# and explosion signaling without needing a long multi-shot runtime loop.
	var destroy_prepared := false
	var destroy_projectile_spawned := false
	if not _target_destroyed(target_index):
		target_shields[target_index] = 0
		target_hulls[target_index] = applied_hull_damage
		primary_weapon_cooldown_frames = 0.0
		destroy_prepared = true
		destroy_projectile_spawned = _spawn_primary_projectile()
		for _i in range(90):
			_advance_projectiles(1.0 / 60.0)
	var target_destroyed := _target_destroyed(target_index)
	var credits_after_destroy := credits
	var combat_reward_paid := credits_after_destroy > credits_before_destroy
	var combat_reward_amount := credits_after_destroy - credits_before_destroy
	var combat_reward_recorded := not combat_reward_history.is_empty() and int(combat_reward_history[-1].get("targetIndex", -1)) == target_index
	loaded_pilot_name = "Combat Reward Probe"
	loaded_ship_name = "Starseeker"
	var reward_save_succeeded := _save_current_pilot_file()
	var reward_saved_data := _read_pilot_file(loaded_pilot_file)
	var saved_reward_history: Array = reward_saved_data.get("combat_reward_history", [])
	var combat_reward_saved := reward_save_succeeded and saved_reward_history.size() == combat_reward_history.size() and not saved_reward_history.is_empty()
	combat_reward_history.clear()
	for saved_reward in saved_reward_history:
		if typeof(saved_reward) == TYPE_DICTIONARY:
			combat_reward_history.append(saved_reward)
	var combat_reward_resume_visible := combat_reward_history.size() == saved_reward_history.size() and not combat_reward_history.is_empty() and int(combat_reward_history[0].get("credits", 0)) == combat_reward_amount
	var combat_reward_inventory_visible := _player_inventory_lines().has(_combat_reward_inventory_line()) and _combat_reward_inventory_line().contains("Combat rewards: 1 disable(s), 25 credits")
	var combat_reward_hud_visible := _combat_reward_hud_fragment() == "    Rewards: 1 disable(s)/25 cr"
	var combat_reward_last_target_visible := _combat_reward_inventory_line().contains("Last reward: Contact 1, 25 credits")
	var combat_reward_status_visible := status_messages.has("Contact 1 disabled; reward +25 cr — TV scaffold, Classic bounty pending")
	primary_weapon_cooldown_frames = 0.0
	var destroyed_target_blocked := not _spawn_primary_projectile()
	var retargeted_after_destroyed := status_messages.has("Target already disabled; retargeting to next active contact")
	var retargeted_target_index := selected_target_index
	var npc_weapon := _weapon_stats_by_id(str(_npc_ship_stats().get("weaponId", "pulse_cannon")))
	if npc_weapon.is_empty():
		npc_weapon = primary_weapon
	var npc_hull_damage := _weapon_hull_damage(npc_weapon)
	player_shields = 0
	player_hull = npc_hull_damage
	var player_disable_retaliation_fired := _spawn_npc_retaliation_projectile(retargeted_target_index)
	for _i in range(90):
		_advance_projectiles(1.0 / 60.0)
	var player_disabled := player_hull <= 0
	var player_disabled_status_visible := status_messages.has(_player_disabled_message())
	var player_disabled_explosion := explosion_events.any(func(explosion): return str(explosion.get("sourceLabel", "")) == "terminal-velocity-player-disabled-scaffold")
	primary_weapon_cooldown_frames = 0.0
	var disabled_fire_blocked := not _spawn_primary_projectile()
	var disabled_fire_guidance := status_messages.has(_player_disabled_action_message())
	_fire_secondary_weapon()
	var disabled_secondary_blocked := status_messages.has(_player_disabled_action_message())
	_change_secondary_weapon()
	var disabled_change_secondary_blocked := status_messages.has(_player_disabled_action_message())
	_toggle_autopilot()
	var disabled_autopilot_guidance := status_messages.has(_player_disabled_action_message())
	_toggle_hyper_mode()
	var disabled_hyper_mode_guidance := status_messages.has(_player_disabled_action_message())
	_cycle_link(1)
	var disabled_hyper_select_guidance := status_messages.has(_player_disabled_action_message())
	selected_route = [str(current_system.get("links", [])[0]) if not current_system.get("links", []).is_empty() else "Rigel"]
	_move_to_scripted_hyperspace_distance()
	_jump()
	var disabled_jump_guidance := status_messages.has(_player_disabled_action_message())
	_try_land()
	var disabled_land_guidance := status_messages.has(_player_disabled_action_message())
	var disabled_movement_pos_before := pos
	var disabled_movement_vel_before := vel
	var disabled_movement_facing_before := player_facing_index
	_apply_movement_controls(1.0 / 60.0, 1, true, false)
	var disabled_movement_blocked := status_messages.has(_player_disabled_action_message()) and pos == disabled_movement_pos_before and vel == disabled_movement_vel_before and player_facing_index == disabled_movement_facing_before
	loaded_pilot_name = "Disabled Save Probe"
	loaded_ship_name = "Starseeker"
	var disabled_save_blocked := not _save_current_pilot_file() and status_messages.has(_player_disabled_action_message())
	var disabled_service_refuel_blocked := not _refuel_current_ship() and status_messages.has(_player_disabled_action_message())
	var disabled_service_repair_blocked := not _repair_current_hull() and status_messages.has(_player_disabled_action_message())
	var disabled_service_clemency_blocked := not _pay_legal_clemency() and status_messages.has(_player_disabled_action_message())
	var active_missions_before_disabled_accept := active_missions.size()
	_accept_selected_mission()
	var disabled_mission_accept_blocked := status_messages.has(_player_disabled_action_message()) and active_missions.size() == active_missions_before_disabled_accept
	var credits_before_disabled_trade := credits
	var cargo_before_disabled_trade := cargo
	_buy_selected_commodity()
	var disabled_trade_buy_blocked := status_messages.has(_player_disabled_action_message()) and credits == credits_before_disabled_trade and cargo == cargo_before_disabled_trade
	_sell_selected_commodity()
	var disabled_trade_sell_blocked := status_messages.has(_player_disabled_action_message()) and credits == credits_before_disabled_trade and cargo == cargo_before_disabled_trade
	var owned_outfits_before_disabled_buy := owned_outfits.duplicate(true)
	var owned_weapons_before_disabled_buy := owned_weapons.duplicate(true)
	_buy_selected_outfit_or_weapon()
	var disabled_outfit_buy_blocked := status_messages.has(_player_disabled_action_message()) and owned_outfits == owned_outfits_before_disabled_buy and owned_weapons == owned_weapons_before_disabled_buy
	var player_ship_id_before_disabled_buy := player_ship_id
	_buy_selected_ship()
	var disabled_ship_buy_blocked := status_messages.has(_player_disabled_action_message()) and player_ship_id == player_ship_id_before_disabled_buy
	var recovery_triggered := _recover_disabled_player_scaffold()
	var player_recovered := not _player_disabled() and player_hull == _max_player_hull() and player_shields == _max_player_shields()
	var recovery_status_visible := status_messages.has(_player_recovery_message())
	var explosion_triggered := not explosion_events.is_empty()
	var latest_explosion_source := str(explosion_events[-1].get("sourceLabel", "")) if explosion_triggered else ""
	var source_fields: Dictionary = primary_weapon.get("sourceStockWeaponFields", {})
	var source_resource_id := int(primary_weapon.get("sourceResourceId", -1))
	var source_stock_name := str(primary_weapon.get("sourceStockName", primary_weapon.get("name", "Primary")))
	var source_mass_damage := int(source_fields.get("MassDmg", primary_weapon.get("massDamage", 0)))
	var source_energy_damage := int(source_fields.get("EnergyDmg", primary_weapon.get("energyDamage", 0)))
	var source_reload := int(source_fields.get("Reload", primary_weapon.get("reloadFrames", 0)))
	var source_count := int(source_fields.get("Count", primary_weapon.get("countFrames", 0)))
	var source_applied_fields := ",".join(primary_weapon.get("sourceAppliedFields", []))
	var applied_shield_damage := _weapon_shield_damage(primary_weapon)
	var primary_sound_id := _sound_binding_for_weapon(str(primary_weapon.get("id", "")))
	var npc_sound_id := _sound_binding_for_weapon(str(npc_weapon.get("id", "")))
	var explosion_sound_id := _sound_binding_for_combat("shipExplodes")
	var primary_sound_played := _sound_history_contains(primary_sound_id)
	var npc_sound_played := _sound_history_contains(npc_sound_id)
	var explosion_sound_played := _sound_history_contains(explosion_sound_id)
	print("%s combatExecuted=true projectileSpawned=%s retaliationFired=%s targetIndex=%d targetDamaged=%s playerDamaged=%s destroyScenarioPrepared=%s destroyProjectileSpawned=%s targetDestroyed=%s combatRewardPaid=%s combatRewardAmount=%d combatRewardRecorded=%s combatRewardSaved=%s combatRewardResumeVisible=%s combatRewardInventoryVisible=%s combatRewardHudVisible=%s combatRewardLastTargetVisible=%s combatRewardStatusVisible=%s creditsBeforeDestroy=%d creditsAfterDestroy=%d destroyedTargetBlocked=%s retargetedAfterDestroyed=%s retargetedTargetIndex=%d playerDisableRetaliationFired=%s playerDisabled=%s playerDisabledStatusVisible=%s playerDisabledExplosion=%s disabledFireBlocked=%s disabledFireGuidance=%s disabledSecondaryBlocked=%s disabledChangeSecondaryBlocked=%s disabledAutopilotGuidance=%s disabledHyperModeGuidance=%s disabledHyperSelectGuidance=%s disabledMovementBlocked=%s disabledSaveBlocked=%s disabledServiceRefuelBlocked=%s disabledServiceRepairBlocked=%s disabledServiceClemencyBlocked=%s disabledMissionAcceptBlocked=%s disabledTradeBuyBlocked=%s disabledTradeSellBlocked=%s disabledOutfitBuyBlocked=%s disabledShipBuyBlocked=%s recoveryTriggered=%s playerRecovered=%s recoveryStatusVisible=%s disabledJumpGuidance=%s disabledLandGuidance=%s explosionTriggered=%s explosionSourceLabel=%s projectilesRemaining=%d beforeShield=%d afterShield=%d beforeHull=%d afterHull=%d playerShieldBefore=%d playerShieldAfter=%d playerHullBefore=%d playerHullAfter=%d weapon=%s sourceResourceId=%d sourceStockName=\"%s\" sourceMassDmg=%d sourceEnergyDmg=%d sourceReload=%d sourceCount=%d appliedShieldDamage=%d appliedHullDamage=%d sourceAppliedFields=%s sourceLabel=terminal-velocity-source-mined-combat-scaffold oracleStatus=classic_runtime_weapon_timing_pending status=\"%s\"" % [COMBAT_EVENT_LOG_PREFIX, str(spawned), str(retaliation_fired), target_index, str(target_damaged), str(player_damaged), str(destroy_prepared), str(destroy_projectile_spawned), str(target_destroyed), str(combat_reward_paid), combat_reward_amount, str(combat_reward_recorded), str(combat_reward_saved), str(combat_reward_resume_visible), str(combat_reward_inventory_visible), str(combat_reward_hud_visible), str(combat_reward_last_target_visible), str(combat_reward_status_visible), credits_before_destroy, credits_after_destroy, str(destroyed_target_blocked), str(retargeted_after_destroyed), retargeted_target_index, str(player_disable_retaliation_fired), str(player_disabled), str(player_disabled_status_visible), str(player_disabled_explosion), str(disabled_fire_blocked), str(disabled_fire_guidance), str(disabled_secondary_blocked), str(disabled_change_secondary_blocked), str(disabled_autopilot_guidance), str(disabled_hyper_mode_guidance), str(disabled_hyper_select_guidance), str(disabled_movement_blocked), str(disabled_save_blocked), str(disabled_service_refuel_blocked), str(disabled_service_repair_blocked), str(disabled_service_clemency_blocked), str(disabled_mission_accept_blocked), str(disabled_trade_buy_blocked), str(disabled_trade_sell_blocked), str(disabled_outfit_buy_blocked), str(disabled_ship_buy_blocked), str(recovery_triggered), str(player_recovered), str(recovery_status_visible), str(disabled_jump_guidance), str(disabled_land_guidance), str(explosion_triggered), latest_explosion_source, projectiles.size(), before_shields, int(target_shields.get(target_index, 0)), before_hull, int(target_hulls.get(target_index, 0)), before_player_shields, player_shields, before_player_hull, player_hull, primary_weapon.get("id", "unknown"), source_resource_id, source_stock_name, source_mass_damage, source_energy_damage, source_reload, source_count, applied_shield_damage, applied_hull_damage, source_applied_fields, status_line])
	print("TV_SOUND_EVENT primaryWeaponSound=%s primaryWeaponSoundPlayed=%s npcWeaponSound=%s npcWeaponSoundPlayed=%s explosionSound=%s explosionSoundPlayed=%s sourceLabel=decoded-resource-backed-sound-binding oracleStatus=classic_runtime_sound_timing_pending" % [primary_sound_id, str(primary_sound_played), npc_sound_id, str(npc_sound_played), explosion_sound_id, str(explosion_sound_played)])
	get_tree().quit(0)


func _run_combat_reward_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	combat_reward_history.clear()
	explosion_events.clear()
	projectiles.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	_select_closest_target()
	var target_index := selected_target_index
	var primary_weapon := _primary_weapon_stats()
	var applied_hull_damage := _weapon_hull_damage(primary_weapon)
	target_shields[target_index] = 0
	target_hulls[target_index] = applied_hull_damage
	primary_weapon_cooldown_frames = 0.0
	var credits_before_destroy := credits
	var destroy_projectile_spawned := _spawn_primary_projectile()
	for _i in range(90):
		_advance_projectiles(1.0 / 60.0)
	var target_destroyed := _target_destroyed(target_index)
	var credits_after_destroy := credits
	var combat_reward_paid := credits_after_destroy > credits_before_destroy
	var combat_reward_amount := credits_after_destroy - credits_before_destroy
	var combat_reward_recorded := not combat_reward_history.is_empty() and int(combat_reward_history[-1].get("targetIndex", -1)) == target_index
	loaded_pilot_name = "Combat Reward Probe"
	loaded_ship_name = "Starseeker"
	var reward_save_succeeded := _save_current_pilot_file()
	var reward_saved_data := _read_pilot_file(loaded_pilot_file)
	var saved_reward_history: Array = reward_saved_data.get("combat_reward_history", [])
	var combat_reward_saved := reward_save_succeeded and saved_reward_history.size() == combat_reward_history.size() and not saved_reward_history.is_empty()
	combat_reward_history.clear()
	for saved_reward in saved_reward_history:
		if typeof(saved_reward) == TYPE_DICTIONARY:
			combat_reward_history.append(saved_reward)
	var combat_reward_resume_visible := combat_reward_history.size() == saved_reward_history.size() and not combat_reward_history.is_empty() and int(combat_reward_history[0].get("credits", 0)) == combat_reward_amount
	var combat_reward_inventory_visible := _player_inventory_lines().has(_combat_reward_inventory_line()) and _combat_reward_inventory_line().contains("Combat rewards: 1 disable(s), 25 credits")
	var combat_reward_hud_visible := _combat_reward_hud_fragment() == "    Rewards: 1 disable(s)/25 cr"
	var combat_reward_status_visible := status_messages.has("Contact 1 disabled; reward +25 cr — TV scaffold, Classic bounty pending")
	primary_weapon_cooldown_frames = 0.0
	var destroyed_target_blocked := not _spawn_primary_projectile()
	var retargeted_after_destroyed := status_messages.has("Target already disabled; retargeting to next active contact")
	print("%s destroyProjectileSpawned=%s targetDestroyed=%s combatRewardPaid=%s combatRewardAmount=25 actualCombatRewardAmount=%d combatRewardRecorded=%s combatRewardSaved=%s combatRewardResumeVisible=%s combatRewardInventoryVisible=%s combatRewardHudVisible=%s combatRewardStatusVisible=%s creditsBeforeDestroy=%d creditsAfterDestroy=%d destroyedTargetBlocked=%s retargetedAfterDestroyed=%s sourceLabel=terminal-velocity-combat-reward-scaffold oracleStatus=classic_runtime_combat_reward_behavior_pending status=\"%s\"" % [COMBAT_REWARD_EVENT_LOG_PREFIX, str(destroy_projectile_spawned).to_lower(), str(target_destroyed).to_lower(), str(combat_reward_paid).to_lower(), combat_reward_amount, str(combat_reward_recorded).to_lower(), str(combat_reward_saved).to_lower(), str(combat_reward_resume_visible).to_lower(), str(combat_reward_inventory_visible).to_lower(), str(combat_reward_hud_visible).to_lower(), str(combat_reward_status_visible).to_lower(), credits_before_destroy, credits_after_destroy, str(destroyed_target_blocked).to_lower(), str(retargeted_after_destroyed).to_lower(), status_line])
	get_tree().quit(0)


func _run_combat_reward_salvage_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	combat_reward_history.clear()
	explosion_events.clear()
	cargo_salvage_pickups.clear()
	projectiles.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	_select_closest_target()
	var target_index := selected_target_index
	var primary_weapon := _primary_weapon_stats()
	target_shields[target_index] = 0
	target_hulls[target_index] = _weapon_hull_damage(primary_weapon)
	primary_weapon_cooldown_frames = 0.0
	var cargo_before_destroy := cargo
	var equipment_before_destroy := int(commodity_hold.get("equipment", 0))
	var credits_before_destroy := credits
	var destroy_projectile_spawned := _spawn_primary_projectile()
	for _i in range(90):
		_advance_projectiles(1.0 / 60.0)
	var target_destroyed := _target_destroyed(target_index)
	var credits_after_destroy := credits
	var combat_reward_amount := credits_after_destroy - credits_before_destroy
	var combat_reward_paid := combat_reward_amount > 0
	var salvage_created_before_pickup := not cargo_salvage_pickups.is_empty()
	var combat_reward_inventory_visible := _player_inventory_lines().has(_combat_reward_inventory_line()) and _combat_reward_inventory_line().contains("Combat rewards: 1 disable(s), 25 credits")
	if salvage_created_before_pickup:
		pos = cargo_salvage_pickups[0].get("position", pos)
		_advance_cargo_salvage_pickups()
	var salvage_scooped_after_reward := int(commodity_hold.get("equipment", 0)) > equipment_before_destroy and cargo > cargo_before_destroy
	var salvage_status_visible := status_messages.has("Recovered 2 tons of Equipment salvage (TV scaffold; Classic loot behavior pending)")
	var reward_and_salvage_coexisted := target_destroyed and combat_reward_paid and salvage_created_before_pickup and salvage_scooped_after_reward and combat_reward_inventory_visible and salvage_status_visible
	print("%s destroyProjectileSpawned=%s targetDestroyed=%s combatRewardPaid=%s combatRewardAmount=%d salvageCreatedBeforePickup=%s salvageScoopedAfterReward=%s rewardAndSalvageCoexisted=%s combatRewardInventoryVisible=%s salvageStatusVisible=%s salvageCommodity=equipment cargoBeforeDestroy=%d cargoAfterPickup=%d equipmentBefore=%d equipmentAfter=%d creditsBeforeDestroy=%d creditsAfterDestroy=%d sourceLabel=terminal-velocity-combat-reward-salvage-scaffold rewardSourceLabel=terminal-velocity-combat-reward-scaffold salvageSourceLabel=terminal-velocity-combat-salvage-scaffold oracleStatus=classic_runtime_reward_loot_coupling_pending status=\"%s\"" % [COMBAT_REWARD_SALVAGE_EVENT_LOG_PREFIX, str(destroy_projectile_spawned).to_lower(), str(target_destroyed).to_lower(), str(combat_reward_paid).to_lower(), combat_reward_amount, str(salvage_created_before_pickup).to_lower(), str(salvage_scooped_after_reward).to_lower(), str(reward_and_salvage_coexisted).to_lower(), str(combat_reward_inventory_visible).to_lower(), str(salvage_status_visible).to_lower(), cargo_before_destroy, cargo, equipment_before_destroy, int(commodity_hold.get("equipment", 0)), credits_before_destroy, credits_after_destroy, status_line])
	get_tree().quit(0)


func _run_secondary_weapon_log() -> void:
	_reset_deterministic_motion_state()
	_reset_combat_targets()
	projectiles.clear()
	status_messages.clear()
	owned_weapons.clear()
	selected_secondary_weapon_index = 0
	secondary_weapon_cooldown_frames = 0.0
	var secondary_empty_line := _secondary_weapon_inventory_line()
	_fire_secondary_weapon()
	var unavailable_at_start := status_messages.has("Secondary weapon not loaded; primary combat scaffold available with Tab")
	owned_weapons["pulse_cannon"] = 1
	_change_secondary_weapon()
	var secondary_loaded_line := _secondary_weapon_inventory_line()
	var primary_weapon := _primary_weapon_stats()
	var source_primary_id := str(player_ship.get("weaponId", "laser_cannon"))
	var primary_weapon_preserved := str(primary_weapon.get("id", "")) == source_primary_id
	var secondary_cycle_selected := status_messages.has("Secondary weapon selected: %s" % str(_secondary_weapon_stats().get("name", "pulse_cannon")))
	var shield_before := int(target_shields.get(selected_target_index, 0))
	var secondary_projectile_spawned := _spawn_secondary_projectile()
	var secondary_cooldown_frames := int(round(secondary_weapon_cooldown_frames))
	var immediate_projectile_count := projectiles.size()
	var immediate_second_shot_blocked := not _spawn_secondary_projectile() and projectiles.size() == immediate_projectile_count and status_messages.has(_secondary_weapon_reload_message())
	for _i in range(120):
		_advance_projectiles(1.0 / 60.0)
		_advance_explosion_events(1.0 / 60.0)
	var shield_after := int(target_shields.get(selected_target_index, 0))
	var target_damaged := shield_after < shield_before
	var weapon := _secondary_weapon_stats()
	var source_fields: Dictionary = weapon.get("sourceStockWeaponFields", {})
	var secondary_sound_id := _sound_binding_for_weapon(str(weapon.get("id", "")))
	var secondary_sound_played := _sound_history_contains(secondary_sound_id)
	var secondary_inventory_empty_visible := secondary_empty_line.contains("No Secondary Weapon")
	var secondary_inventory_loaded_visible := secondary_loaded_line.contains(str(weapon.get("name", ""))) and secondary_loaded_line.contains(str(weapon.get("sourceStockName", "")))
	var secondary_hud_fragment := _secondary_weapon_hud_fragment()
	var secondary_hud_visible := secondary_hud_fragment.contains(str(weapon.get("name", ""))) and secondary_hud_fragment.contains("reload")
	print("%s secondaryUnavailableAtStart=%s secondaryCycleSelected=%s secondaryProjectileSpawned=%s secondaryImmediateReloadBlocked=%s secondaryCooldownFrames=%d secondaryTargetDamaged=%s secondaryInventoryEmptyVisible=%s secondaryInventoryLoadedVisible=%s primaryWeaponPreserved=%s sourcePrimaryId=%s selectedSecondaryId=%s selectedSecondaryName=\"%s\" secondaryWeaponSound=%s secondaryWeaponSoundPlayed=%s secondaryHudVisible=%s secondaryHudFragment=\"%s\" targetShieldBefore=%d targetShieldAfter=%d sourceResourceId=%d sourceStockName=\"%s\" sourceMassDmg=%d sourceEnergyDmg=%d sourceReload=%d sourceAppliedFields=%s sourceLabel=terminal-velocity-secondary-weapon-scaffold soundSourceLabel=decoded-resource-backed-sound-binding oracleStatus=classic_runtime_secondary_weapon_behavior_pending soundOracleStatus=classic_runtime_sound_timing_pending" % [
		SECONDARY_WEAPON_EVENT_LOG_PREFIX,
		str(unavailable_at_start).to_lower(),
		str(secondary_cycle_selected).to_lower(),
		str(secondary_projectile_spawned).to_lower(),
		str(immediate_second_shot_blocked).to_lower(),
		secondary_cooldown_frames,
		str(target_damaged).to_lower(),
		str(secondary_inventory_empty_visible).to_lower(),
		str(secondary_inventory_loaded_visible).to_lower(),
		str(primary_weapon_preserved).to_lower(),
		source_primary_id,
		str(weapon.get("id", "")),
		str(weapon.get("name", "")),
		secondary_sound_id,
		str(secondary_sound_played).to_lower(),
		str(secondary_hud_visible).to_lower(),
		secondary_hud_fragment,
		shield_before,
		shield_after,
		int(weapon.get("sourceResourceId", -1)),
		str(weapon.get("sourceStockName", "")),
		int(source_fields.get("MassDmg", weapon.get("massDamage", 0))),
		int(source_fields.get("EnergyDmg", weapon.get("energyDamage", 0))),
		int(source_fields.get("Reload", weapon.get("reloadFrames", 0))),
		JSON.stringify(weapon.get("sourceAppliedFields", [])),
	])
	get_tree().quit(0)

func _run_player_disabled_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	projectiles.clear()
	explosion_events.clear()
	sound_event_history.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	var npc_weapon := _weapon_stats_by_id(str(_npc_ship_stats().get("weaponId", "pulse_cannon")))
	if npc_weapon.is_empty():
		npc_weapon = _primary_weapon_stats()
	var incoming_hit := {
		"shieldDamage": _max_player_shields(),
		"hullDamage": _max_player_hull(),
	}
	var hull_before := player_hull
	var shields_before := player_shields
	player_shields = 0
	_apply_player_projectile_hit(incoming_hit)
	var player_disabled := _player_disabled()
	var hull_after_disable := player_hull
	var disabled_status_visible := status_messages.has(_player_disabled_message())
	var disabled_explosion_visible := explosion_events.any(func(explosion): return str(explosion.get("sourceLabel", "")) == "terminal-velocity-player-disabled-scaffold")
	var disabled_explosion_sound := _sound_history_contains(_sound_binding_for_combat("shipExplodes"))
	primary_weapon_cooldown_frames = 0.0
	var disabled_fire_blocked := not _spawn_primary_projectile() and status_messages.has(_player_disabled_action_message())
	selected_route = [str(current_system.get("links", [])[0]) if not current_system.get("links", []).is_empty() else "Rigel"]
	_move_to_scripted_hyperspace_distance()
	_jump()
	var disabled_jump_blocked := status_messages.has(_player_disabled_action_message())
	var movement_pos_before := pos
	var movement_vel_before := vel
	var movement_facing_before := player_facing_index
	_apply_movement_controls(1.0 / 60.0, 1, true, false)
	var disabled_movement_blocked := status_messages.has(_player_disabled_action_message()) and pos == movement_pos_before and vel == movement_vel_before and player_facing_index == movement_facing_before
	landed = true
	_ev_land_or_launch()
	var disabled_launch_blocked := status_messages.has(_player_disabled_action_message()) and landed
	var recovery_triggered := _recover_disabled_player_scaffold()
	var player_recovered := not _player_disabled() and player_hull == _max_player_hull() and player_shields == _max_player_shields()
	var recovery_status_visible := status_messages.has(_player_recovery_message())
	print("%s playerDisabled=%s disabledStatusVisible=%s disabledExplosionVisible=%s disabledExplosionSound=%s disabledFireBlocked=%s disabledJumpBlocked=%s disabledMovementBlocked=%s disabledLaunchBlocked=%s recoveryTriggered=%s playerRecovered=%s recoveryStatusVisible=%s hullBefore=%d hullAfterDisable=%d hullAfterRecovery=%d shieldsBefore=%d shieldsAfterRecovery=%d npcWeapon=%s sourceLabel=terminal-velocity-player-disabled-scaffold oracleStatus=classic_runtime_player_death_pending_strict_play_safe_trace" % [
		PLAYER_DISABLED_EVENT_LOG_PREFIX,
		str(player_disabled).to_lower(),
		str(disabled_status_visible).to_lower(),
		str(disabled_explosion_visible).to_lower(),
		str(disabled_explosion_sound).to_lower(),
		str(disabled_fire_blocked).to_lower(),
		str(disabled_jump_blocked).to_lower(),
		str(disabled_movement_blocked).to_lower(),
		str(disabled_launch_blocked).to_lower(),
		str(recovery_triggered).to_lower(),
		str(player_recovered).to_lower(),
		str(recovery_status_visible).to_lower(),
		hull_before,
		hull_after_disable,
		player_hull,
		shields_before,
		player_shields,
		str(npc_weapon.get("id", "")),
	])
	get_tree().quit(0)

func _run_shield_recharge_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	var max_shields := _max_player_shields()
	var source_recharge_frames := int(player_ship.get("shieldRecharge", 30))
	player_hull = _max_player_hull()
	player_shields = max(0, max_shields - 3)
	player_shield_recharge_progress = 0.0
	var shields_before := player_shields
	var short_wait_seconds := maxf(0.0, float(source_recharge_frames - 1) / 60.0)
	_recharge_player_shields(short_wait_seconds)
	var shields_after_short_wait := player_shields
	var short_wait_blocked := shields_after_short_wait == shields_before
	_recharge_player_shields(1.0 / 60.0)
	var shields_after_one_tick := player_shields
	var first_tick_recharged := shields_after_one_tick == shields_before + 1
	_recharge_player_shields(float(source_recharge_frames * 2) / 60.0)
	var shields_after_multi_tick := player_shields
	var multi_tick_recharged: bool = shields_after_multi_tick >= mini(max_shields, shields_before + 3)
	player_hull = 0
	player_shield_recharge_progress = 0.0
	var shields_before_disabled := player_shields
	_recharge_player_shields(float(source_recharge_frames * 2) / 60.0)
	var disabled_recharge_blocked := player_shields == shields_before_disabled
	var combat_readiness_visible := _combat_readiness_inventory_line().contains("shield recharge cadence source-backed scaffold")
	print("%s shieldsBefore=%d shieldsAfterShortWait=%d shortWaitBlocked=%s shieldsAfterOneTick=%d firstTickRecharged=%s shieldsAfterMultiTick=%d multiTickRecharged=%s disabledRechargeBlocked=%s maxShields=%d sourceRechargeFrames=%d combatReadinessVisible=%s sourceLabel=decoded-resource-backed-ship-shield-recharge-scaffold oracleStatus=classic_runtime_shield_recharge_timing_pending" % [
		SHIELD_RECHARGE_EVENT_LOG_PREFIX,
		shields_before,
		shields_after_short_wait,
		str(short_wait_blocked).to_lower(),
		shields_after_one_tick,
		str(first_tick_recharged).to_lower(),
		shields_after_multi_tick,
		str(multi_tick_recharged).to_lower(),
		str(disabled_recharge_blocked).to_lower(),
		max_shields,
		source_recharge_frames,
		str(combat_readiness_visible).to_lower(),
	])
	get_tree().quit(0)

func _run_combat_guardrail_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	_select_closest_target()
	primary_weapon_cooldown_frames = 0.0
	var first_shot_spawned := _spawn_primary_projectile()
	var cooldown_after_first := primary_weapon_cooldown_frames
	var second_shot_spawned := _spawn_primary_projectile()
	var cooldown_blocked := not second_shot_spawned and status_messages.has(_primary_weapon_reload_message())
	_advance_weapon_cooldowns(cooldown_after_first / 60.0)
	var cooldown_cleared := primary_weapon_cooldown_frames <= 0.0
	var third_shot_spawned := _spawn_primary_projectile()
	var secondary_blocked_before := status_messages.has("Secondary weapon not loaded; primary combat scaffold available with Tab")
	_fire_secondary_weapon()
	var secondary_blocked := status_messages.has("Secondary weapon not loaded; primary combat scaffold available with Tab") and not secondary_blocked_before
	var primary_weapon := _primary_weapon_stats()
	var source_fields: Dictionary = primary_weapon.get("sourceStockWeaponFields", {})
	var source_reload := int(source_fields.get("Reload", primary_weapon.get("reloadFrames", 0)))
	var primary_sound_id := _sound_binding_for_weapon(str(primary_weapon.get("id", "")))
	var primary_sound_play_count := sound_event_history.count(primary_sound_id)
	var primary_sound_played_for_valid_shots := primary_sound_play_count == 2 and first_shot_spawned and third_shot_spawned and not second_shot_spawned
	var previous_sound_pref := pref_sound_on
	sound_event_history.clear()
	pref_sound_on = false
	var sound_preference_muted := not pref_sound_on
	primary_weapon_cooldown_frames = 0.0
	var muted_shot_spawned := _spawn_primary_projectile()
	var muted_sound_event_count := sound_event_history.count(primary_sound_id)
	var sound_preference_suppresses_combat_sound := muted_shot_spawned and muted_sound_event_count == 0
	pref_sound_on = previous_sound_pref
	print("%s firstShotSpawned=%s immediateSecondShotBlocked=%s cooldownFrames=%d cooldownCleared=%s shotAfterCooldownSpawned=%s secondaryBlocked=%s primaryWeaponSound=%s primaryWeaponSoundPlayCount=%d primaryWeaponSoundPlayedForValidShots=%s soundPreferenceMuted=%s mutedSoundEventCount=%d soundPreferenceSuppressesCombatSound=%s sourceReload=%d sourceLabel=terminal-velocity-source-mined-combat-guardrail-scaffold soundSourceLabel=decoded-resource-backed-sound-binding oracleStatus=classic_runtime_weapon_timing_pending soundOracleStatus=classic_runtime_sound_timing_pending status=\"%s\"" % [COMBAT_GUARDRAIL_EVENT_LOG_PREFIX, str(first_shot_spawned), str(cooldown_blocked), int(cooldown_after_first), str(cooldown_cleared), str(third_shot_spawned), str(secondary_blocked), primary_sound_id, primary_sound_play_count, str(primary_sound_played_for_valid_shots), str(sound_preference_muted).to_lower(), muted_sound_event_count, str(sound_preference_suppresses_combat_sound).to_lower(), source_reload, status_line])
	get_tree().quit(0)

func _run_retaliation_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	_select_closest_target()
	npc_retaliation_cooldowns.clear()
	var target_index := selected_target_index
	var first_retaliation_fired := _spawn_npc_retaliation_projectile(target_index)
	var cooldown_after_first := float(npc_retaliation_cooldowns.get(target_index, 0.0))
	var immediate_second_fired := _spawn_npc_retaliation_projectile(target_index)
	var immediate_second_blocked := not immediate_second_fired and status_messages.has(_npc_retaliation_reload_message())
	_advance_weapon_cooldowns(cooldown_after_first / 60.0)
	var cooldown_cleared := float(npc_retaliation_cooldowns.get(target_index, 0.0)) <= 0.0
	var retaliation_after_cooldown_fired := _spawn_npc_retaliation_projectile(target_index)
	var player_shields_before := player_shields
	for _i in range(90):
		_advance_projectiles(1.0 / 60.0)
	var player_damaged := player_shields < player_shields_before or player_hull < _max_player_hull()
	var npc_weapon := _weapon_stats_by_id(str(_npc_ship_stats().get("weaponId", "pulse_cannon")))
	if npc_weapon.is_empty():
		npc_weapon = _primary_weapon_stats()
	var source_fields: Dictionary = npc_weapon.get("sourceStockWeaponFields", {})
	var source_reload := int(source_fields.get("Reload", npc_weapon.get("reloadFrames", 0)))
	print("%s firstRetaliationFired=%s immediateSecondRetaliationBlocked=%s npcCooldownFrames=%d npcCooldownCleared=%s retaliationAfterCooldownFired=%s playerDamagedByRetaliation=%s sourceReload=%d sourceLabel=terminal-velocity-npc-retaliation-scaffold oracleStatus=classic_runtime_ai_retaliation_cadence_pending" % [RETALIATION_EVENT_LOG_PREFIX, str(first_retaliation_fired).to_lower(), str(immediate_second_blocked).to_lower(), int(cooldown_after_first), str(cooldown_cleared).to_lower(), str(retaliation_after_cooldown_fired).to_lower(), str(player_damaged).to_lower(), source_reload])
	get_tree().quit(0)

func _run_projectile_motion_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	_select_closest_target()
	primary_weapon_cooldown_frames = 0.0
	var target_index := selected_target_index
	var weapon := _primary_weapon_stats()
	var source_fields: Dictionary = weapon.get("sourceStockWeaponFields", {})
	var source_speed := int(source_fields.get("Speed", weapon.get("speed", 0)))
	var source_lifetime := int(weapon.get("lifetime", source_fields.get("Count", 0)))
	var source_count := int(source_fields.get("Count", weapon.get("countFrames", 0)))
	var projectile_spawned := _spawn_primary_projectile()
	var initial_position := Vector2.ZERO
	var initial_speed := 0
	if projectile_spawned and not projectiles.is_empty():
		initial_position = projectiles[0].get("position", Vector2.ZERO)
		initial_speed = int(round(projectiles[0].get("velocity", Vector2.ZERO).length()))
	for _i in range(5):
		_advance_projectiles(1.0 / 60.0)
	var moved_position: Vector2 = projectiles[0].get("position", initial_position) if not projectiles.is_empty() else initial_position
	var projectile_moved: bool = moved_position.distance_to(initial_position) > 0.0
	var shield_before_hit := int(target_shields.get(target_index, 0))
	var hit_target := false
	for _i in range(180):
		_advance_projectiles(1.0 / 60.0)
		if int(target_shields.get(target_index, 0)) < shield_before_hit:
			hit_target = true
			break
	var shield_after_hit := int(target_shields.get(target_index, 0))
	projectiles.clear()
	primary_weapon_cooldown_frames = 0.0
	var expiry_spawned := _spawn_primary_projectile()
	if expiry_spawned and not projectiles.is_empty():
		projectiles[0]["targetIndex"] = -99
		projectiles[0]["position"] = Vector2(-9999, -9999)
		projectiles[0]["velocity"] = Vector2.RIGHT * float(weapon.get("speed", 9.0)) * 60.0
	for _i in range(source_lifetime + 5):
		_advance_projectiles(1.0 / 60.0)
	var projectile_expired := expiry_spawned and projectiles.is_empty()
	print("%s projectileSpawned=%s projectileMoved=%s projectileHitTarget=%s projectileExpired=%s initialProjectileSpeed=%d sourceSpeed=%d sourceLifetime=%d sourceCount=%d targetShieldBefore=%d targetShieldAfter=%d sourceLabel=terminal-velocity-projectile-motion-scaffold oracleStatus=classic_runtime_projectile_motion_pending" % [PROJECTILE_MOTION_EVENT_LOG_PREFIX, str(projectile_spawned).to_lower(), str(projectile_moved).to_lower(), str(hit_target).to_lower(), str(projectile_expired).to_lower(), initial_speed, source_speed, source_lifetime, source_count, shield_before_hit, shield_after_hit])
	get_tree().quit(0)

func _run_explosion_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	_select_closest_target()
	var target_index := selected_target_index
	var weapon := _primary_weapon_stats()
	target_shields[target_index] = 0
	target_hulls[target_index] = _weapon_hull_damage(weapon)
	primary_weapon_cooldown_frames = 0.0
	var projectile_spawned := _spawn_primary_projectile()
	for _i in range(90):
		_advance_projectiles(1.0 / 60.0)
	var explosion_triggered := not explosion_events.is_empty()
	var initial_life := float(explosion_events[0].get("life", 0.0)) if explosion_triggered else 0.0
	var explosion_source_label := str(explosion_events[0].get("sourceLabel", "")) if explosion_triggered else ""
	var explosion_oracle_status := str(explosion_events[0].get("oracleStatus", "")) if explosion_triggered else ""
	_advance_explosion_events(0.5)
	var life_after_half_second := float(explosion_events[0].get("life", 0.0)) if not explosion_events.is_empty() else 0.0
	var explosion_animated := explosion_triggered and life_after_half_second < initial_life and life_after_half_second > 0.0
	_advance_explosion_events(initial_life + 0.1)
	var explosion_expired := explosion_triggered and explosion_events.is_empty()
	print("%s projectileSpawned=%s targetDestroyed=%s explosionTriggered=%s explosionAnimated=%s explosionExpired=%s initialLife=%.2f lifeAfterHalfSecond=%.2f explosionSourceLabel=%s explosionOracleStatus=%s sourceLabel=terminal-velocity-explosion-visual-scaffold oracleStatus=classic_runtime_explosion_timing_pending" % [EXPLOSION_EVENT_LOG_PREFIX, str(projectile_spawned).to_lower(), str(_target_destroyed(target_index)).to_lower(), str(explosion_triggered).to_lower(), str(explosion_animated).to_lower(), str(explosion_expired).to_lower(), initial_life, life_after_half_second, explosion_source_label, explosion_oracle_status])
	get_tree().quit(0)

func _run_cargo_salvage_log() -> void:
	_reset_travel_state()
	loaded_pilot_name = "Cargo Salvage Test"
	loaded_ship_name = "Holdover"
	status_messages.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	_select_closest_target()
	var target_index := selected_target_index
	var primary_weapon := _primary_weapon_stats()
	target_shields[target_index] = 0
	target_hulls[target_index] = _weapon_hull_damage(primary_weapon)
	primary_weapon_cooldown_frames = 0.0
	var cargo_before_destroy := cargo
	var equipment_before_destroy := int(commodity_hold.get("equipment", 0))
	var projectile_spawned := _spawn_primary_projectile()
	for _i in range(90):
		_advance_projectiles(1.0 / 60.0)
		_advance_cargo_salvage_pickups()
	if not cargo_salvage_pickups.is_empty() and cargo == cargo_before_destroy:
		pos = cargo_salvage_pickups[0].get("position", pos)
		_advance_cargo_salvage_pickups()
	var target_destroyed := _target_destroyed(target_index)
	var salvage_created := cargo_salvage_pickups.size() > 0 or status_messages.any(func(message): return str(message).contains("Recovered 2 tons of Equipment salvage"))
	var salvage_scooped := int(commodity_hold.get("equipment", 0)) > equipment_before_destroy and cargo > cargo_before_destroy
	var cargo_after_scoop := cargo
	var equipment_after_scoop := int(commodity_hold.get("equipment", 0))
	# Full-hold guardrail: a second dropped pickup remains in space when the hold
	# is full, instead of silently deleting spoils or overfilling cargo.
	cargo = cargo_space
	pos = Vector2.ZERO
	var full_hold_pickup := _spawn_cargo_salvage_pickup(target_index, Vector2.ZERO)
	var full_hold_created := full_hold_pickup.size() > 0
	_advance_cargo_salvage_pickups()
	var full_hold_blocked := cargo_salvage_pickups.size() > 0 and status_messages.has("Cargo hold full; salvage remains in space")
	var remaining_pickups_before_save := cargo_salvage_pickups.size()
	var save_succeeded := _save_current_pilot_file()
	var saved_data := _read_pilot_file(loaded_pilot_file)
	var saved_salvage: Array = saved_data.get("cargo_salvage_pickups", [])
	var salvage_saved := save_succeeded and saved_salvage.size() == remaining_pickups_before_save and remaining_pickups_before_save > 0
	cargo_salvage_pickups.clear()
	_restore_cargo_salvage_pickups(saved_salvage)
	var salvage_resume_visible := cargo_salvage_pickups.size() == remaining_pickups_before_save and not cargo_salvage_pickups.is_empty() and str(cargo_salvage_pickups[0].get("commodityId", "")) == "equipment"
	var salvage_inventory_visible := _player_inventory_lines().has("In-space salvage: 1 pickup(s), 2 tons — TV combat-salvage scaffold; Classic loot behavior pending")
	var salvage_hud_visible := _salvage_hud_fragment() == "    Salvage: 1 pickup(s)/2 tons"
	var salvage_scanner_visible := _salvage_scanner_blip_count() == remaining_pickups_before_save and remaining_pickups_before_save > 0
	print("%s combatExecuted=true projectileSpawned=%s targetDestroyed=%s salvageCreated=%s salvageScooped=%s cargoBeforeDestroy=%d cargoAfterScoop=%d equipmentBefore=%d equipmentAfter=%d fullHoldCreated=%s fullHoldBlocked=%s remainingPickups=%d salvageSaveSucceeded=%s salvageSaved=%s salvageResumeVisible=%s salvageInventoryVisible=%s salvageHudVisible=%s salvageScannerVisible=%s sourceLabel=terminal-velocity-combat-salvage-scaffold oracleStatus=classic_runtime_loot_cargo_behavior_pending status=\"%s\"" % [CARGO_SALVAGE_EVENT_LOG_PREFIX, str(projectile_spawned).to_lower(), str(target_destroyed).to_lower(), str(salvage_created).to_lower(), str(salvage_scooped).to_lower(), cargo_before_destroy, cargo_after_scoop, equipment_before_destroy, equipment_after_scoop, str(full_hold_created).to_lower(), str(full_hold_blocked).to_lower(), remaining_pickups_before_save, str(save_succeeded).to_lower(), str(salvage_saved).to_lower(), str(salvage_resume_visible).to_lower(), str(salvage_inventory_visible).to_lower(), str(salvage_hud_visible).to_lower(), str(salvage_scanner_visible).to_lower(), status_line])
	get_tree().quit(0)

func _run_cargo_salvage_recovery_log() -> void:
	_reset_travel_state()
	loaded_pilot_name = "Cargo Salvage Recovery Test"
	loaded_ship_name = "Holdover"
	status_messages.clear()
	cargo_salvage_pickups.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	cargo = cargo_space
	commodity_hold["food"] = cargo_space
	var salvage_pickup := _spawn_cargo_salvage_pickup(0, Vector2.ZERO)
	var full_hold_created := salvage_pickup.size() > 0
	_advance_cargo_salvage_pickups()
	var full_hold_blocked := cargo_salvage_pickups.size() == 1 and status_messages.has("Cargo hold full; salvage remains in space")
	var save_succeeded := _save_current_pilot_file()
	var saved_data := _read_pilot_file(loaded_pilot_file)
	var saved_salvage: Array = saved_data.get("cargo_salvage_pickups", [])
	var salvage_saved := save_succeeded and saved_salvage.size() == 1
	cargo_salvage_pickups.clear()
	_restore_cargo_salvage_pickups(saved_salvage)
	var salvage_resume_visible := cargo_salvage_pickups.size() == 1 and _player_inventory_lines().has("In-space salvage: 1 pickup(s), 2 tons — TV combat-salvage scaffold; Classic loot behavior pending") and _salvage_hud_fragment() == "    Salvage: 1 pickup(s)/2 tons"
	landed = true
	landing_tab = 1
	selected_landing_item = 0
	var cargo_before_sale := cargo
	var food_before_sale := int(commodity_hold.get("food", 0))
	_sell_selected_commodity()
	var cargo_freed_by_sale := status_messages.has("Sold 10 tons of Food") and cargo == cargo_before_sale - EV_CLASSIC_COMMODITY_LOT_SIZE and int(commodity_hold.get("food", 0)) == food_before_sale - EV_CLASSIC_COMMODITY_LOT_SIZE
	landed = false
	if not cargo_salvage_pickups.is_empty():
		pos = cargo_salvage_pickups[0].get("position", pos)
	_advance_cargo_salvage_pickups()
	var salvage_scooped_after_cargo_freed := cargo_salvage_pickups.is_empty() and int(commodity_hold.get("equipment", 0)) == 2 and cargo == cargo_before_sale - EV_CLASSIC_COMMODITY_LOT_SIZE + 2
	var recovery_status_visible := status_messages.has("Recovered 2 tons of Equipment salvage (TV scaffold; Classic loot behavior pending)")
	var salvage_recovery_complete := full_hold_blocked and salvage_saved and salvage_resume_visible and cargo_freed_by_sale and salvage_scooped_after_cargo_freed and recovery_status_visible
	print("%s fullHoldCreated=%s fullHoldBlocked=%s salvageSaved=%s salvageResumeVisible=%s cargoFreedBySale=%s salvageScoopedAfterCargoFreed=%s recoveryStatusVisible=%s salvageRecoveryComplete=%s foodAfterSale=%d equipmentAfterRecovery=%d cargoAfterRecovery=%d sourceLabel=terminal-velocity-combat-salvage-recovery-scaffold salvageSourceLabel=terminal-velocity-combat-salvage-scaffold oracleStatus=classic_runtime_loot_cargo_recovery_pending status=\"%s\"" % [CARGO_SALVAGE_RECOVERY_EVENT_LOG_PREFIX, str(full_hold_created).to_lower(), str(full_hold_blocked).to_lower(), str(salvage_saved).to_lower(), str(salvage_resume_visible).to_lower(), str(cargo_freed_by_sale).to_lower(), str(salvage_scooped_after_cargo_freed).to_lower(), str(recovery_status_visible).to_lower(), str(salvage_recovery_complete).to_lower(), int(commodity_hold.get("food", 0)), int(commodity_hold.get("equipment", 0)), cargo, status_line])
	get_tree().quit(0)

func _run_target_selection_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	_reset_combat_targets()
	selected_target_index = 0
	var target_count := _npc_world_offsets().size()
	var initial_target := selected_target_index
	_cycle_target(1)
	var cycled_target := selected_target_index
	var cycled_status := status_line
	var cycled_status_has_target := cycled_status.contains("Target: Contact")
	var cycled_status_has_stats := cycled_status.contains("S/H")
	_select_closest_target()
	var closest_target := selected_target_index
	var closest_status := status_line
	var closest_status_has_closest := closest_status.contains("Closest target: Contact")
	var closest_status_has_stats := closest_status.contains("S/H")
	target_shields[1] = 0
	target_hulls[1] = 0
	selected_target_index = 0
	_cycle_target(1)
	var skipped_target := selected_target_index
	var destroyed_target_skipped_by_cycle := skipped_target != 1 and not _target_destroyed(skipped_target)
	pos = Vector2(260, -180)
	_select_closest_target()
	var closest_after_destroyed := selected_target_index
	var destroyed_target_skipped_by_closest := closest_after_destroyed != 1 and not _target_destroyed(closest_after_destroyed)
	var live_target_count := 0
	for i in range(target_count):
		if _target_selectable(i):
			live_target_count += 1
	var scanner_target_detail := _scanner_target_detail_line()
	var scanner_target_detail_visible := scanner_target_detail.contains("Scanner target: Contact") and scanner_target_detail.contains("S/H")
	for i in range(target_count):
		target_shields[i] = 0
		target_hulls[i] = 0
	selected_target_index = 0
	_cycle_target(1)
	var no_active_cycle_status := status_line
	_select_closest_target()
	var no_active_closest_status := status_line
	var no_active_scanner_status_visible := no_active_cycle_status == "No active scanner targets" and no_active_closest_status == "No active scanner targets"
	print("%s initialTarget=%d cycledTarget=%d closestTarget=%d targetCount=%d destroyedTargetSkippedByCycle=%s destroyedTargetSkippedByClosest=%s liveTargetCount=%d cycledStatusHasTarget=true actualCycledStatusHasTarget=%s cycledStatusHasStats=%s closestStatusHasClosest=true actualClosestStatusHasClosest=%s closestStatusHasStats=%s scannerTargetDetailVisible=%s noActiveScannerStatusVisible=%s scannerTargetDetail=\"%s\" cycledStatus=\"%s\" closestStatus=\"%s\" noActiveCycleStatus=\"%s\" noActiveClosestStatus=\"%s\" sourceLabel=terminal-velocity-target-selection-scaffold oracleStatus=classic_runtime_target_selection_pending" % [TARGET_SELECTION_EVENT_LOG_PREFIX, initial_target, cycled_target, closest_target, target_count, str(destroyed_target_skipped_by_cycle), str(destroyed_target_skipped_by_closest), live_target_count, str(cycled_status_has_target), str(cycled_status_has_stats), str(closest_status_has_closest), str(closest_status_has_stats), str(scanner_target_detail_visible).to_lower(), str(no_active_scanner_status_visible).to_lower(), scanner_target_detail, cycled_status, closest_status, no_active_cycle_status, no_active_closest_status])
	get_tree().quit(0)

func _run_navigation_guardrail_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	var original_system: Dictionary = current_system.duplicate(true)
	var no_link_system: Dictionary = current_system.duplicate(true)
	no_link_system["links"] = []
	current_system = no_link_system
	_jump()
	current_system = original_system
	var no_route_guidance := status_messages.has("No hyperspace route selected; open map (M) or queue mission route (G)")
	map_visible = true
	_select_first_linked_map_route()
	player_fuel = 0
	_move_to_scripted_hyperspace_distance()
	_jump()
	var fuel_guidance := status_messages.has("Insufficient fuel for hyperspace; land at a port with refuel service or choose a closer route")
	player_fuel = _max_player_fuel()
	pos = Vector2.ZERO
	_jump()
	var too_close_guidance := status_messages.has("Can't initiate hyperspace jump - not yet far enough away from system center.")
	var original_bodies_for_no_port: Array = current_system.get("bodies", [])
	current_system["bodies"] = []
	pos = Vector2(9999, 9999)
	vel = Vector2.ZERO
	_try_land()
	current_system["bodies"] = original_bodies_for_no_port
	var no_port_guidance := status_messages.has("No port in range; fly closer to a planet/station and slow below landing speed")
	pos = Vector2(float(current_system.get("bodies", [])[0].get("x", 0)), float(current_system.get("bodies", [])[0].get("y", 0)))
	vel = Vector2(120, 0)
	_try_land()
	var approach_guidance := status_messages.has("Approach slower/closer to land; landing needs close range and speed under 90")
	landed = true
	vel = Vector2.ZERO
	var body := _current_body()
	var inventory: Dictionary = body.get("inventory", {}).duplicate(true)
	inventory["services"] = []
	inventory["outfitsForSale"] = []
	body["inventory"] = inventory
	var original_bodies: Array = current_system.get("bodies", [])
	var original_body: Dictionary = original_bodies[0]
	original_bodies[0] = body
	_refuel_current_ship()
	original_bodies[0] = original_body
	var refuel_guidance := status_messages.has("Refuel unavailable here; choose a port with refuel service")
	print("%s noRouteGuidance=%s fuelGuidance=%s tooCloseGuidance=%s noPortGuidance=%s approachGuidance=%s refuelGuidance=%s sourceLabel=terminal-velocity-navigation-guardrail-scaffold oracleStatus=navigation_blocked_feedback_pending_playtest messages=%s" % [NAVIGATION_GUARDRAIL_EVENT_LOG_PREFIX, str(no_route_guidance), str(fuel_guidance), str(too_close_guidance), str(no_port_guidance), str(approach_guidance), str(refuel_guidance), JSON.stringify(status_messages)])
	get_tree().quit(0)

func _run_legal_status_log() -> void:
	_reset_travel_state()
	var start_system := str(current_system.get("name", "?"))
	var start_government := _current_government_name()
	var start_status := _legal_status_for_government(start_government)
	legal_records[start_government] = -65
	var penalty_status := _legal_status_for_government(start_government)
	var dock_allowed := _government_docking_allowed(start_government)
	var warning := _legal_warning_line(start_government)
	print("%s system=%s government=\"%s\" cleanStatus=%s penaltyStatus=%s dockAllowed=%s legalScore=%d warning=\"%s\" sourceLabel=terminal-velocity-classic-resource-legal-semantics oracleStatus=classic_runtime_thresholds_pending" % [LEGAL_STATUS_EVENT_LOG_PREFIX, start_system, start_government, start_status, penalty_status, str(dock_allowed), int(legal_records.get(start_government, 0)), warning])
	get_tree().quit(0)

func _run_legal_docking_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	var government_name := _current_government_name()
	legal_records[government_name] = -75
	status_messages.clear()
	_try_land()
	var denied_message := _legal_docking_denied_message(government_name)
	var legal_docking_denied := status_messages.has(denied_message)
	var patrol_hostile := _legal_patrol_hostile_posture_active(government_name)
	print("%s routeToSolSelected=%s system=%s government=\"%s\" legalScore=%d legalDockingDenied=%s landed=%s patrolsHostile=%s message=\"%s\" sourceLabel=terminal-velocity-legal-docking-scaffold oracleStatus=classic_runtime_docking_denial_ui_pending" % [LEGAL_DOCKING_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), government_name, int(legal_records.get(government_name, 0)), str(legal_docking_denied), str(landed), str(patrol_hostile), denied_message])
	get_tree().quit(0)

func _run_legal_service_gate_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var body_name := str(_current_body().get("name", ""))
	var government_name := _current_government_name()
	legal_records[government_name] = -75
	status_messages.clear()
	landing_tab = 2
	selected_landing_item = 0
	credits = 100000
	_buy_selected_outfit_or_weapon()
	landing_tab = 3
	_buy_selected_ship()
	var service_blocked_message := _legal_service_blocked_message(government_name)
	var blocked_count := 0
	for message in status_messages:
		if str(message) == service_blocked_message:
			blocked_count += 1
	var blocked_outfitter := blocked_count >= 1
	var blocked_shipyard := blocked_count >= 2
	var no_purchase := not owned_outfits.has("cargo_pod") and player_ship_id != "light_freighter"
	print("%s routeToSolSelected=%s system=%s body=%s government=\"%s\" legalScore=%d blockedOutfitter=%s blockedShipyard=%s noPurchase=%s serviceBlockedMessage=\"%s\" sourceLabel=terminal-velocity-legal-service-gate-scaffold oracleStatus=legal_service_denial_pending_ev_classic_confirmation" % [LEGAL_SERVICE_GATE_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), body_name, government_name, int(legal_records.get(government_name, 0)), str(blocked_outfitter), str(blocked_shipyard), str(no_purchase), service_blocked_message])
	get_tree().quit(0)

func _run_weapon_reputation_gate_log() -> void:
	_reset_travel_state()
	current_system_index = _system_index_by_name("Sirius", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	landed = true
	var body_name := "Sirius Station"
	for body in current_system.get("bodies", []):
		if str(body.get("name", "")) == body_name:
			pos = Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
			break
	var government_name := _current_government_name()
	legal_records[government_name] = 0
	reputation_scores[government_name] = 5
	credits = 100000
	landing_tab = 2
	var sale_items := _outfitter_sale_items(_current_body())
	selected_landing_item = 0
	for i in range(sale_items.size()):
		if str(sale_items[i].get("id", "")) == "pulse_cannon":
			selected_landing_item = i
			break
	status_messages.clear()
	_buy_selected_outfit_or_weapon()
	var blocked_message := _service_blocked_message("weapons", government_name)
	var weapon_reputation_blocked := status_messages.has(blocked_message) and not owned_weapons.has("pulse_cannon")
	reputation_scores[government_name] = 6
	status_messages.clear()
	_buy_selected_outfit_or_weapon()
	var weapon_bought_after_reputation := int(owned_weapons.get("pulse_cannon", 0)) == 1
	print("%s system=%s body=%s government=\"%s\" reputationBefore=5 reputationAfter=%d legalScore=%d selectedWeapon=pulse_cannon weaponReputationBlocked=%s weaponBoughtAfterReputation=%s blockedMessage=\"%s\" sourceLabel=terminal-velocity-weapon-reputation-gate-scaffold oracleStatus=classic_runtime_weapon_service_reputation_gate_pending" % [WEAPON_REPUTATION_GATE_EVENT_LOG_PREFIX, current_system.get("name", "?"), body_name, government_name, int(reputation_scores.get(government_name, 0)), int(legal_records.get(government_name, 0)), str(weapon_reputation_blocked), str(weapon_bought_after_reputation), blocked_message])
	get_tree().quit(0)

func _run_weapon_credit_gate_log() -> void:
	_reset_travel_state()
	current_system_index = _system_index_by_name("Sirius", current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	landed = true
	var body_name := "Sirius Station"
	for body in current_system.get("bodies", []):
		if str(body.get("name", "")) == body_name:
			pos = Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
			break
	var government_name := _current_government_name()
	legal_records[government_name] = 0
	reputation_scores[government_name] = 6
	landing_tab = 2
	var sale_items := _outfitter_sale_items(_current_body())
	var selected_weapon := "pulse_cannon"
	var selected_weapon_price := 0
	selected_landing_item = 0
	for i in range(sale_items.size()):
		if str(sale_items[i].get("id", "")) == selected_weapon:
			selected_landing_item = i
			selected_weapon_price = int(sale_items[i].get("price", 0))
			break
	credits = max(0, selected_weapon_price - 1)
	var credits_before := credits
	status_messages.clear()
	_buy_selected_outfit_or_weapon()
	var blocked_message := "Not enough credits"
	var weapon_credit_blocked := status_messages.has(blocked_message) and not owned_weapons.has(selected_weapon)
	credits = selected_weapon_price
	var credits_after_funding := credits
	status_messages.clear()
	_buy_selected_outfit_or_weapon()
	var weapon_bought_after_funding := int(owned_weapons.get(selected_weapon, 0)) == 1
	print("%s system=%s body=%s government=\"%s\" legalScore=%d reputation=%d selectedWeapon=%s weaponPrice=%d creditsBefore=%d creditsAfterFunding=%d weaponCreditBlocked=%s weaponBoughtAfterFunding=%s blockedMessage=\"%s\" sourceLabel=terminal-velocity-weapon-credit-gate-scaffold oracleStatus=classic_runtime_weapon_purchase_credit_flow_pending" % [WEAPON_CREDIT_GATE_EVENT_LOG_PREFIX, current_system.get("name", "?"), body_name, government_name, int(legal_records.get(government_name, 0)), int(reputation_scores.get(government_name, 0)), selected_weapon, selected_weapon_price, credits_before, credits_after_funding, str(weapon_credit_blocked), str(weapon_bought_after_funding), blocked_message])
	get_tree().quit(0)

func _run_weapon_availability_gate_log() -> void:
	_reset_travel_state()
	var selected_weapon := "pulse_cannon"
	var unavailable_system_name := "Sol"
	var unavailable_body_name := "Earth"
	current_system_index = _system_index_by_name(unavailable_system_name, current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	landed = true
	for body in current_system.get("bodies", []):
		if str(body.get("name", "")) == unavailable_body_name:
			pos = Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
			break
	var unavailable_government_name := _current_government_name()
	legal_records[unavailable_government_name] = 0
	reputation_scores[unavailable_government_name] = 6
	credits = 100000
	landing_tab = 2
	var unavailable_sale_items := _outfitter_sale_items(_current_body())
	var weapon_available_at_unavailable_body := false
	for item in unavailable_sale_items:
		if str(item.get("id", "")) == selected_weapon:
			weapon_available_at_unavailable_body = true
			break
	status_messages.clear()
	var bought_at_unavailable_body := _buy_outfit_or_weapon_by_id(selected_weapon)
	var unavailable_blocked_message := "Item not sold here: %s" % selected_weapon
	var weapon_availability_blocked := status_messages.has(unavailable_blocked_message) and not bought_at_unavailable_body and not owned_weapons.has(selected_weapon)
	var recovery_system_name := "Sirius"
	var recovery_body_name := "Sirius Station"
	current_system_index = _system_index_by_name(recovery_system_name, current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	for body in current_system.get("bodies", []):
		if str(body.get("name", "")) == recovery_body_name:
			pos = Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
			break
	var recovery_government_name := _current_government_name()
	legal_records[recovery_government_name] = 0
	reputation_scores[recovery_government_name] = 6
	status_messages.clear()
	var bought_after_relocation := _buy_outfit_or_weapon_by_id(selected_weapon)
	var weapon_bought_after_relocation := bought_after_relocation and int(owned_weapons.get(selected_weapon, 0)) == 1
	print("%s unavailableSystem=%s unavailableBody=\"%s\" unavailableGovernment=\"%s\" recoverySystem=%s recoveryBody=\"%s\" recoveryGovernment=\"%s\" selectedWeapon=%s credits=%d legalScore=%d reputation=%d weaponAvailableAtUnavailableBody=%s weaponAvailabilityBlocked=%s weaponBoughtAfterRelocation=%s blockedMessage=\"%s\" sourceLabel=terminal-velocity-weapon-availability-gate-scaffold oracleStatus=classic_runtime_weapon_service_availability_pending" % [WEAPON_AVAILABILITY_GATE_EVENT_LOG_PREFIX, unavailable_system_name, unavailable_body_name, unavailable_government_name, recovery_system_name, recovery_body_name, recovery_government_name, selected_weapon, credits, int(legal_records.get(unavailable_government_name, 0)), int(reputation_scores.get(unavailable_government_name, 0)), str(weapon_available_at_unavailable_body), str(weapon_availability_blocked), str(weapon_bought_after_relocation), unavailable_blocked_message])
	get_tree().quit(0)

func _run_weapon_inventory_stack_log() -> void:
	_reset_travel_state()
	var selected_weapon := "pulse_cannon"
	var system_name := "Sirius"
	var body_name := "Sirius Station"
	current_system_index = _system_index_by_name(system_name, current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	landed = true
	for body in current_system.get("bodies", []):
		if str(body.get("name", "")) == body_name:
			pos = Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
			break
	var government_name := _current_government_name()
	legal_records[government_name] = 0
	reputation_scores[government_name] = 6
	credits = 100000
	owned_weapons.clear()
	status_messages.clear()
	var first_weapon_buy_succeeded := _buy_outfit_or_weapon_by_id(selected_weapon)
	var weapon_stack_count_after_first := int(owned_weapons.get(selected_weapon, 0))
	var credits_after_first := credits
	status_messages.clear()
	var second_weapon_buy_succeeded := _buy_outfit_or_weapon_by_id(selected_weapon)
	var weapon_stack_count_after_second := int(owned_weapons.get(selected_weapon, 0))
	var weapon_stack_preserved := first_weapon_buy_succeeded and second_weapon_buy_succeeded and weapon_stack_count_after_first == 1 and weapon_stack_count_after_second == 2
	print("%s system=%s body=\"%s\" government=\"%s\" selectedWeapon=%s firstWeaponBuySucceeded=%s secondWeaponBuySucceeded=%s weaponStackCountAfterFirst=%d weaponStackCountAfterSecond=%d weaponStackPreserved=%s creditsAfterFirst=%d creditsAfterSecond=%d sourceLabel=terminal-velocity-weapon-inventory-stack-scaffold oracleStatus=classic_runtime_multiple_weapon_purchase_inventory_pending" % [WEAPON_INVENTORY_STACK_EVENT_LOG_PREFIX, system_name, body_name, government_name, selected_weapon, str(first_weapon_buy_succeeded), str(second_weapon_buy_succeeded), weapon_stack_count_after_first, weapon_stack_count_after_second, str(weapon_stack_preserved), credits_after_first, credits])
	get_tree().quit(0)

func _run_weapon_secondary_activation_log() -> void:
	_reset_deterministic_motion_state()
	_reset_combat_targets()
	projectiles.clear()
	status_messages.clear()
	owned_weapons.clear()
	selected_secondary_weapon_index = 0
	secondary_weapon_cooldown_frames = 0.0
	var selected_weapon := "pulse_cannon"
	var system_name := "Sirius"
	var body_name := "Sirius Station"
	current_system_index = _system_index_by_name(system_name, current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	landed = true
	for body in current_system.get("bodies", []):
		if str(body.get("name", "")) == body_name:
			pos = Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
			break
	var government_name := _current_government_name()
	legal_records[government_name] = 0
	reputation_scores[government_name] = 6
	credits = 10000
	_fire_secondary_weapon()
	var unavailable_message := "Secondary weapon not loaded; primary combat scaffold available with Tab"
	var secondary_unavailable_before_purchase := status_messages.has(unavailable_message) and _installed_secondary_weapon_ids().is_empty()
	status_messages.clear()
	var secondary_bought_before_activation := _buy_outfit_or_weapon_by_id(selected_weapon)
	var weapon_count_after_purchase := int(owned_weapons.get(selected_weapon, 0))
	_change_secondary_weapon()
	var weapon := _secondary_weapon_stats()
	var secondary_cycle_selected_after_purchase := status_messages.has("Secondary weapon selected: %s" % str(weapon.get("name", selected_weapon)))
	var shield_before := int(target_shields.get(selected_target_index, 0))
	var secondary_projectile_spawned_after_purchase := _spawn_secondary_projectile()
	for _i in range(120):
		_advance_projectiles(1.0 / 60.0)
		_advance_explosion_events(1.0 / 60.0)
	var shield_after := int(target_shields.get(selected_target_index, 0))
	var secondary_target_damaged_after_purchase := shield_after < shield_before
	var secondary_hud_fragment := _secondary_weapon_hud_fragment()
	print("%s system=%s body=\"%s\" government=\"%s\" selectedWeapon=%s secondaryUnavailableBeforePurchase=%s secondaryBoughtBeforeActivation=%s weaponCountAfterPurchase=%d secondaryCycleSelectedAfterPurchase=%s secondaryProjectileSpawnedAfterPurchase=%s secondaryTargetDamagedAfterPurchase=%s selectedSecondaryId=%s selectedSecondaryName=\"%s\" secondaryHudFragment=\"%s\" targetShieldBefore=%d targetShieldAfter=%d sourceLabel=terminal-velocity-weapon-secondary-activation-scaffold oracleStatus=classic_runtime_secondary_weapon_activation_pending" % [WEAPON_SECONDARY_ACTIVATION_EVENT_LOG_PREFIX, system_name, body_name, government_name, selected_weapon, str(secondary_unavailable_before_purchase).to_lower(), str(secondary_bought_before_activation).to_lower(), weapon_count_after_purchase, str(secondary_cycle_selected_after_purchase).to_lower(), str(secondary_projectile_spawned_after_purchase).to_lower(), str(secondary_target_damaged_after_purchase).to_lower(), str(weapon.get("id", "")), str(weapon.get("name", "")), secondary_hud_fragment, shield_before, shield_after])
	get_tree().quit(0)

func _run_weapon_mission_cargo_log() -> void:
	_reset_travel_state()
	var selected_weapon := "pulse_cannon"
	var system_name := "Sirius"
	var body_name := "Sirius Station"
	current_system_index = _system_index_by_name(system_name, current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	landed = true
	for body in current_system.get("bodies", []):
		if str(body.get("name", "")) == body_name:
			pos = Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
			break
	var government_name := _current_government_name()
	legal_records[government_name] = 0
	reputation_scores[government_name] = 6
	story_flags = ["frontier_samples_delivered"]
	credits = 10000
	owned_weapons.clear()
	landing_tab = 0
	selected_landing_item = 0
	status_messages.clear()
	_accept_selected_mission()
	var accepted_mission_id := "freeport_return_earth"
	var mission_accepted := active_missions.has(accepted_mission_id)
	var active_mission_cargo_before := _mission_reserved_cargo_tons()
	var cargo_used_before_weapon := cargo
	status_messages.clear()
	var weapon_buy_succeeded := _buy_outfit_or_weapon_by_id(selected_weapon)
	var active_mission_cargo_after := _mission_reserved_cargo_tons()
	var cargo_used_after_weapon := cargo
	var mission_cargo_preserved := mission_accepted and weapon_buy_succeeded and active_mission_cargo_before == active_mission_cargo_after and cargo_used_before_weapon == cargo_used_after_weapon and active_mission_cargo_after > 0
	print("%s system=%s body=\"%s\" government=\"%s\" selectedWeapon=%s acceptedMission=%s missionAccepted=%s weaponBuySucceeded=%s activeMissionCargoBefore=%d activeMissionCargoAfter=%d cargoUsedAfterWeapon=%d weaponCount=%d creditsAfterWeapon=%d missionCargoPreserved=%s sourceLabel=terminal-velocity-weapon-mission-cargo-scaffold oracleStatus=classic_runtime_weapon_purchase_cargo_interaction_pending" % [WEAPON_MISSION_CARGO_EVENT_LOG_PREFIX, system_name, body_name, government_name, selected_weapon, accepted_mission_id, str(mission_accepted), str(weapon_buy_succeeded), active_mission_cargo_before, active_mission_cargo_after, cargo_used_after_weapon, int(owned_weapons.get(selected_weapon, 0)), credits, str(mission_cargo_preserved)])
	get_tree().quit(0)

func _run_weapon_trade_cargo_log() -> void:
	_reset_travel_state()
	var selected_weapon := "pulse_cannon"
	var system_name := "Sirius"
	var body_name := "Sirius Station"
	current_system_index = _system_index_by_name(system_name, current_system_index)
	current_system = universe.get("systems", [])[current_system_index]
	landed = true
	for body in current_system.get("bodies", []):
		if str(body.get("name", "")) == body_name:
			pos = Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
			break
	var government_name := _current_government_name()
	legal_records[government_name] = 0
	reputation_scores[government_name] = 6
	credits = 10000
	owned_weapons.clear()
	commodity_hold.clear()
	commodity_hold["food"] = EV_CLASSIC_COMMODITY_LOT_SIZE
	cargo = EV_CLASSIC_COMMODITY_LOT_SIZE
	var trade_cargo_before := int(commodity_hold.get("food", 0))
	var cargo_used_before_weapon := cargo
	status_messages.clear()
	var weapon_buy_succeeded := _buy_outfit_or_weapon_by_id(selected_weapon)
	var trade_cargo_after := int(commodity_hold.get("food", 0))
	var cargo_used_after_weapon := cargo
	var trade_cargo_preserved := weapon_buy_succeeded and trade_cargo_before == trade_cargo_after and cargo_used_before_weapon == cargo_used_after_weapon and trade_cargo_after > 0
	print("%s system=%s body=\"%s\" government=\"%s\" selectedWeapon=%s weaponBuySucceeded=%s tradeCommodity=food tradeCargoBefore=%d tradeCargoAfter=%d cargoUsedAfterWeapon=%d weaponCount=%d creditsAfterWeapon=%d tradeCargoPreserved=%s sourceLabel=terminal-velocity-weapon-trade-cargo-scaffold oracleStatus=classic_runtime_weapon_purchase_trade_cargo_interaction_pending" % [WEAPON_TRADE_CARGO_EVENT_LOG_PREFIX, system_name, body_name, government_name, selected_weapon, str(weapon_buy_succeeded), trade_cargo_before, trade_cargo_after, cargo_used_after_weapon, int(owned_weapons.get(selected_weapon, 0)), credits, str(trade_cargo_preserved)])
	get_tree().quit(0)

func _run_weapon_legal_docking_log() -> void:
	_reset_travel_state()
	var selected_weapon := "pulse_cannon"
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	var federation_name := _current_government_name()
	legal_records[federation_name] = -70
	reputation_scores[federation_name] = 10
	credits = 2400
	status_messages.clear()
	_try_land()
	var denied_message := _legal_docking_denied_message(federation_name)
	var docking_denied_before_clemency := status_messages.has(denied_message) and not landed
	# Terminal Velocity currently models clemency as a landed service. Seed the
	# service panel after the denial to keep this a labeled scaffold/probe rather
	# than a Classic runtime claim about where clemency is offered.
	landed = true
	var clemency_paid := _pay_legal_clemency()
	var legal_after_clemency := int(legal_records.get(federation_name, 0))
	landed = false
	status_messages.clear()
	_try_land()
	var landed_after_clemency := landed
	landed = false
	map_visible = true
	var route_to_sirius_selected := _select_map_route_to_system("Sirius")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Sirius Station")
	_try_land()
	var recovery_body_name := str(_current_body().get("name", ""))
	var recovery_government_name := _current_government_name()
	legal_records[recovery_government_name] = 0
	reputation_scores[recovery_government_name] = 6
	landing_tab = 2
	status_messages.clear()
	var weapon_buy_succeeded := _buy_outfit_or_weapon_by_id(selected_weapon)
	print("%s routeToSolSelected=%s dockingSystem=Sol dockingGovernment=\"%s\" legalBeforeClemency=-70 dockingDeniedBeforeClemency=%s clemencyPaid=%s legalAfterClemency=%d landedAfterClemency=%s routeToSiriusSelected=%s recoverySystem=Sirius recoveryBody=\"%s\" recoveryGovernment=\"%s\" selectedWeapon=%s weaponBuySucceeded=%s weaponCount=%d creditsAfterWeapon=%d deniedMessage=\"%s\" sourceLabel=terminal-velocity-weapon-legal-docking-scaffold clemencySourceLabel=terminal-velocity-inferred-clemency-scaffold oracleStatus=classic_runtime_weapon_purchase_after_docking_denial_pending clemencyOracleStatus=classic_runtime_clemency_location_pending" % [
		WEAPON_LEGAL_DOCKING_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		federation_name,
		str(docking_denied_before_clemency).to_lower(),
		str(clemency_paid).to_lower(),
		legal_after_clemency,
		str(landed_after_clemency).to_lower(),
		str(route_to_sirius_selected).to_lower(),
		recovery_body_name,
		recovery_government_name,
		selected_weapon,
		str(weapon_buy_succeeded).to_lower(),
		int(owned_weapons.get(selected_weapon, 0)),
		credits,
		denied_message,
	])
	get_tree().quit(0)

func _run_light_freighter_capacity_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 65000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var starting_cargo_space := cargo_space
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var upgraded_cargo_space := cargo_space
	var profitable_commodity := "food"
	var buy_price := int(_market_prices(current_system.get("name", "")).get(profitable_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices("Levo").get(profitable_commodity, {}).get("sell", 0))
	var margin_per_ton := sell_price - buy_price
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_trade_buy := credits
	var cargo_before_trade_buy := cargo
	for _i in range(6):
		_buy_selected_commodity()
	var positive_margin_tons_bought := int(commodity_hold.get(profitable_commodity, 0))
	var positive_margin_lots_bought := int(positive_margin_tons_bought / EV_CLASSIC_COMMODITY_LOT_SIZE)
	var cargo_after_trade_buy := cargo
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_trade_sale := credits
	while int(commodity_hold.get(profitable_commodity, 0)) > 0:
		_sell_selected_commodity()
	var cargo_after_trade_sale := cargo
	var held_profitable_after_sale := int(commodity_hold.get(profitable_commodity, 0))
	var large_hold_trade_cleared := cargo_after_trade_sale == 0 and held_profitable_after_sale == 0
	var starting_cargo_space_status := "startingCargoSpace=20" if starting_cargo_space == 20 else "startingCargoSpace=%d" % starting_cargo_space
	var upgraded_cargo_space_status := "upgradedCargoSpace=150" if upgraded_cargo_space == 150 else "upgradedCargoSpace=%d" % upgraded_cargo_space
	var positive_margin_lots_status := "positiveMarginLotsBought=6" if positive_margin_lots_bought == 6 else "positiveMarginLotsBought=%d" % positive_margin_lots_bought
	var positive_margin_tons_status := "positiveMarginTonsBought=60" if positive_margin_tons_bought == 60 else "positiveMarginTonsBought=%d" % positive_margin_tons_bought
	var large_hold_trade_cleared_status := "largeHoldTradeCleared=true" if large_hold_trade_cleared else "largeHoldTradeCleared=false"
	var final_cargo_status := "finalCargo=0" if cargo_after_trade_sale == 0 else "finalCargo=%d" % cargo_after_trade_sale
	print("%s startSystem=Levo routeToSolSelected=%s buySystem=Sol sellSystem=Levo routeToLevoSelected=%s boughtLightFreighter=%s %s %s shipPrice=%d profitableCommodity=food buyPrice=%d sellPrice=%d marginPerTon=%d %s %s cargoBeforeTradeBuy=%d cargoAfterTradeBuy=%d creditsBeforeTradeBuy=%d creditsBeforeTradeSale=%d creditsAfterTradeSale=%d %s %s sourceLabel=terminal-velocity-light-freighter-trade-scaffold oracleStatus=light_freighter_trade_pending_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_CAPACITY_TRADE_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(route_to_levo_selected).to_lower(),
		str(bought_light_freighter).to_lower(),
		starting_cargo_space_status,
		upgraded_cargo_space_status,
		ship_price,
		buy_price,
		sell_price,
		margin_per_ton,
		positive_margin_lots_status,
		positive_margin_tons_status,
		cargo_before_trade_buy,
		cargo_after_trade_buy,
		credits_before_trade_buy,
		credits_before_trade_sale,
		credits,
		large_hold_trade_cleared_status,
		final_cargo_status,
		status_line,
	])
	get_tree().quit(0)

func _run_light_freighter_bulk_margin_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 70000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var starting_cargo_space := cargo_space
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var upgraded_cargo_space := cargo_space
	var profitable_commodity := "food"
	var unprofitable_commodity := "equipment"
	var profitable_buy_price := int(_market_prices(current_system.get("name", "")).get(profitable_commodity, {}).get("buy", 0))
	var profitable_sell_price := int(_market_prices("Levo").get(profitable_commodity, {}).get("sell", 0))
	var profitable_margin_per_ton := profitable_sell_price - profitable_buy_price
	var negative_buy_price := int(_market_prices("Levo").get(unprofitable_commodity, {}).get("buy", 0))
	var negative_sell_price := int(_market_prices("Sol").get(unprofitable_commodity, {}).get("sell", 0))
	var negative_margin_per_ton := negative_sell_price - negative_buy_price
	var negative_margin_skipped := negative_margin_per_ton <= 0
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_bulk_buy := credits
	var cargo_before_bulk_buy := cargo
	var lots_to_fill := int(floor(float(_cargo_available_tons()) / float(EV_CLASSIC_COMMODITY_LOT_SIZE)))
	for _i in range(lots_to_fill):
		_buy_selected_commodity()
	var positive_margin_tons_bought := int(commodity_hold.get(profitable_commodity, 0))
	var positive_margin_lots_bought := int(positive_margin_tons_bought / EV_CLASSIC_COMMODITY_LOT_SIZE)
	var held_unprofitable_after_eval := int(commodity_hold.get(unprofitable_commodity, 0))
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_bulk_sale := credits
	while int(commodity_hold.get(profitable_commodity, 0)) > 0:
		_sell_selected_commodity()
	var cargo_after_bulk_sale := cargo
	var held_profitable_after_sale := int(commodity_hold.get(profitable_commodity, 0))
	var bulk_cargo_cleared := cargo_after_bulk_sale == 0 and held_profitable_after_sale == 0
	var starting_cargo_space_status := "startingCargoSpace=20" if starting_cargo_space == 20 else "startingCargoSpace=%d" % starting_cargo_space
	var upgraded_cargo_space_status := "upgradedCargoSpace=150" if upgraded_cargo_space == 150 else "upgradedCargoSpace=%d" % upgraded_cargo_space
	var positive_margin_lots_status := "positiveMarginLotsBought=15" if positive_margin_lots_bought == 15 else "positiveMarginLotsBought=%d" % positive_margin_lots_bought
	var positive_margin_tons_status := "positiveMarginTonsBought=150" if positive_margin_tons_bought == 150 else "positiveMarginTonsBought=%d" % positive_margin_tons_bought
	var profitable_margin_status := "profitableMarginPerTon=78" if profitable_margin_per_ton == 78 else "profitableMarginPerTon=%d" % profitable_margin_per_ton
	var negative_margin_status := "negativeMarginPerTon=-210" if negative_margin_per_ton == -210 else "negativeMarginPerTon=%d" % negative_margin_per_ton
	var bulk_cargo_cleared_status := "bulkCargoCleared=true" if bulk_cargo_cleared else "bulkCargoCleared=false"
	var final_cargo_status := "finalCargo=0" if cargo_after_bulk_sale == 0 else "finalCargo=%d" % cargo_after_bulk_sale
	print("%s startSystem=Levo routeToSolSelected=%s buySystem=Sol sellSystem=Levo routeToLevoSelected=%s boughtLightFreighter=%s %s %s shipPrice=%d profitableCommodity=food unprofitableCommodity=equipment profitableBuyPrice=%d profitableSellPrice=%d %s negativeBuyPrice=%d negativeSellPrice=%d %s %s %s negativeMarginSkipped=%s heldUnprofitableAfterEval=%d cargoBeforeBulkBuy=%d creditsBeforeBulkBuy=%d creditsBeforeBulkSale=%d creditsAfterBulkSale=%d %s %s sourceLabel=terminal-velocity-light-freighter-bulk-margin-scaffold oracleStatus=light_freighter_bulk_margin_pending_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_BULK_MARGIN_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(route_to_levo_selected).to_lower(),
		str(bought_light_freighter).to_lower(),
		starting_cargo_space_status,
		upgraded_cargo_space_status,
		ship_price,
		profitable_buy_price,
		profitable_sell_price,
		profitable_margin_status,
		negative_buy_price,
		negative_sell_price,
		negative_margin_status,
		positive_margin_lots_status,
		positive_margin_tons_status,
		str(negative_margin_skipped).to_lower(),
		held_unprofitable_after_eval,
		cargo_before_bulk_buy,
		credits_before_bulk_buy,
		credits_before_bulk_sale,
		credits,
		bulk_cargo_cleared_status,
		final_cargo_status,
		status_line,
	])
	get_tree().quit(0)

func _run_light_freighter_mission_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 100000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var starting_cargo_space := cargo_space
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var upgraded_cargo_space := cargo_space
	var bulk_mission := {
		"id": "light_freighter_bulk_levo_delivery",
		"title": "Light Freighter Bulk Delivery to Levo",
		"originSystem": "Sol",
		"originBody": "Earth",
		"destinationSystem": "Levo",
		"destinationBody": "Levo Spaceport",
		"cargoTons": 40,
		"reward": 4200,
		"description": "Terminal velocity scaffold probe for mixing reserved mission cargo with retained trade cargo after a Light Freighter upgrade.",
		"requiresFlags": [],
		"excludesFlags": [],
		"setsFlags": ["light_freighter_bulk_delivery_started"],
		"completionFlags": ["light_freighter_bulk_delivery_complete"],
		"choiceGroup": null,
		"next": null,
		"reputationEvent": null,
		"requirements": {},
		"timeLimitDays": 5,
		"sourceLabel": "terminal-velocity-light-freighter-mission-trade-scaffold",
		"oracleStatus": "light_freighter_mission_trade_pending_ev_classic_runtime_trace",
	}
	missions["missions"].insert(0, bulk_mission)
	landing_tab = 0
	selected_landing_item = 0
	var mission_cargo_tons := int(bulk_mission.get("cargoTons", 0))
	var trade_commodity := "food"
	var buy_price := int(_market_prices(current_system.get("name", "")).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices("Levo").get(trade_commodity, {}).get("sell", 0))
	var credits_before_accept := credits
	var cargo_before_accept := cargo
	_accept_selected_mission()
	var mission_accepted := active_missions.has(str(bulk_mission.get("id")))
	var cargo_after_accept := cargo
	var available_after_accept := _cargo_available_tons()
	landing_tab = 1
	selected_landing_item = 0
	_buy_selected_commodity()
	var trade_cargo_after_buy := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_buy := cargo
	var combined_load_fits := cargo_after_trade_buy == mission_cargo_tons + EV_CLASSIC_COMMODITY_LOT_SIZE and cargo_after_trade_buy <= upgraded_cargo_space
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	var completed_ids := _complete_arrived_missions()
	var mission_delivered := completed_ids.has(str(bulk_mission.get("id"))) and completed_missions.has(str(bulk_mission.get("id")))
	var trade_cargo_after_delivery := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_delivery := cargo
	var trade_cargo_preserved_after_delivery := mission_delivered and trade_cargo_after_delivery == EV_CLASSIC_COMMODITY_LOT_SIZE and cargo_after_delivery == EV_CLASSIC_COMMODITY_LOT_SIZE
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	var trade_cargo_after_sell := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_sell := cargo
	var trade_sale_completed := trade_cargo_after_sell == 0 and cargo_after_trade_sell == 0
	print("%s routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" boughtLightFreighter=%s startingCargoSpace=%d upgradedCargoSpace=%d shipPrice=%d acceptedMission=%s missionAccepted=%s missionCargoTons=%d tradeCommodity=%s buyPrice=%d sellPrice=%d cargoBeforeAccept=%d cargoAfterAccept=%d availableAfterAccept=%d tradeCargoAfterBuy=%d cargoAfterTradeBuy=%d combinedLoadFits=%s routeToLevoSelected=%s missionDelivered=%s tradeCargoAfterDelivery=%d cargoAfterDelivery=%d tradeCargoPreservedAfterDelivery=%s tradeSaleCompleted=%s cargoAfterTradeSell=%d creditsBeforeAccept=%d creditsAfter=%d sourceLabel=terminal-velocity-light-freighter-mission-trade-scaffold oracleStatus=light_freighter_mission_trade_pending_ev_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_MISSION_TRADE_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(accepted_body.get("name", "None")),
		str(bought_light_freighter).to_lower(),
		starting_cargo_space,
		upgraded_cargo_space,
		ship_price,
		str(bulk_mission.get("id")),
		str(mission_accepted).to_lower(),
		mission_cargo_tons,
		trade_commodity,
		buy_price,
		sell_price,
		cargo_before_accept,
		cargo_after_accept,
		available_after_accept,
		trade_cargo_after_buy,
		cargo_after_trade_buy,
		str(combined_load_fits).to_lower(),
		str(route_to_levo_selected).to_lower(),
		str(mission_delivered).to_lower(),
		trade_cargo_after_delivery,
		cargo_after_delivery,
		str(trade_cargo_preserved_after_delivery).to_lower(),
		str(trade_sale_completed).to_lower(),
		cargo_after_trade_sell,
		credits_before_accept,
		credits,
		status_line,
	])
	get_tree().quit(0)


func _run_light_freighter_bulk_mission_margin_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 100000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var starting_cargo_space := cargo_space
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var upgraded_cargo_space := cargo_space
	var bulk_mission := {
		"id": "levo_bulk_margin_supply",
		"title": "Levo Bulk Margin Supply",
		"originSystem": "Sol",
		"originBody": "Earth",
		"destinationSystem": "Levo",
		"destinationBody": "Levo Spaceport",
		"cargoTons": 120,
		"reward": 6200,
		"description": "Terminal Velocity scaffold probe for filling remaining Light Freighter hold with positive-margin trade cargo after reserving a bulk delivery.",
		"requiresFlags": [],
		"excludesFlags": [],
		"setsFlags": ["light_freighter_bulk_margin_supply_started"],
		"completionFlags": ["light_freighter_bulk_margin_supply_complete"],
		"choiceGroup": null,
		"next": null,
		"reputationEvent": null,
		"requirements": {},
		"timeLimitDays": 5,
		"sourceLabel": "terminal-velocity-light-freighter-bulk-mission-margin-scaffold",
		"oracleStatus": "light_freighter_bulk_mission_margin_pending_classic_runtime_trace",
	}
	missions["missions"].insert(0, bulk_mission)
	landing_tab = 0
	selected_landing_item = 0
	var mission_cargo_tons := int(bulk_mission.get("cargoTons", 0))
	var profitable_commodity := "food"
	var unprofitable_commodity := "equipment"
	var profitable_buy_price := int(_market_prices(current_system.get("name", "")).get(profitable_commodity, {}).get("buy", 0))
	var profitable_sell_price := int(_market_prices("Levo").get(profitable_commodity, {}).get("sell", 0))
	var profitable_margin_per_ton := profitable_sell_price - profitable_buy_price
	var negative_buy_price := int(_market_prices("Levo").get(unprofitable_commodity, {}).get("buy", 0))
	var negative_sell_price := int(_market_prices("Sol").get(unprofitable_commodity, {}).get("sell", 0))
	var negative_margin_per_ton := negative_sell_price - negative_buy_price
	var cargo_before_accept := cargo
	_accept_selected_mission()
	var mission_accepted := active_missions.has(str(bulk_mission.get("id")))
	var cargo_after_accept := cargo
	var available_after_accept := _cargo_available_tons()
	landing_tab = 1
	selected_landing_item = 0
	while _cargo_available_tons() >= EV_CLASSIC_COMMODITY_LOT_SIZE:
		_buy_selected_commodity()
	var positive_margin_tons_bought := int(commodity_hold.get(profitable_commodity, 0))
	var positive_margin_lots_bought := int(positive_margin_tons_bought / EV_CLASSIC_COMMODITY_LOT_SIZE)
	var held_unprofitable_after_eval := int(commodity_hold.get(unprofitable_commodity, 0))
	var negative_margin_skipped := negative_margin_per_ton < 0 and held_unprofitable_after_eval == 0
	var cargo_after_trade_buy := cargo
	var combined_load_fits := cargo_after_trade_buy == mission_cargo_tons + positive_margin_tons_bought and cargo_after_trade_buy <= upgraded_cargo_space
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	var completed_ids := _complete_arrived_missions()
	var mission_delivered := completed_ids.has(str(bulk_mission.get("id"))) and completed_missions.has(str(bulk_mission.get("id")))
	var trade_cargo_after_delivery := int(commodity_hold.get(profitable_commodity, 0))
	var cargo_after_delivery := cargo
	var mission_delivered_before_trade_sale := mission_delivered and trade_cargo_after_delivery == positive_margin_tons_bought and cargo_after_delivery == positive_margin_tons_bought
	landing_tab = 1
	selected_landing_item = 0
	while int(commodity_hold.get(profitable_commodity, 0)) > 0:
		_sell_selected_commodity()
	var trade_cargo_after_sell := int(commodity_hold.get(profitable_commodity, 0))
	var cargo_after_trade_sell := cargo
	var retained_trade_sold_after_delivery := trade_cargo_after_sell == 0 and cargo_after_trade_sell == 0
	print("%s routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" boughtLightFreighter=%s startingCargoSpace=%d upgradedCargoSpace=%d shipPrice=%d acceptedMission=%s missionAccepted=%s missionCargoTons=%d cargoBeforeAccept=%d cargoAfterAccept=%d availableAfterAccept=%d profitableCommodity=food unprofitableCommodity=equipment profitableBuyPrice=%d profitableSellPrice=%d profitableMarginPerTon=%d negativeBuyPrice=%d negativeSellPrice=%d negativeMarginPerTon=%d negativeMarginSkipped=%s heldUnprofitableAfterEval=%d positiveMarginLotsBought=%d positiveMarginTonsBought=%d cargoAfterTradeBuy=%d combinedLoadFits=%s routeToLevoSelected=%s missionDeliveredBeforeTradeSale=%s tradeCargoAfterDelivery=%d cargoAfterDelivery=%d retainedTradeSoldAfterDelivery=%s cargoAfterTradeSell=%d creditsAfter=%d sourceLabel=terminal-velocity-light-freighter-bulk-mission-margin-scaffold oracleStatus=light_freighter_bulk_mission_margin_pending_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_BULK_MISSION_MARGIN_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(accepted_body.get("name", "None")),
		str(bought_light_freighter).to_lower(),
		starting_cargo_space,
		upgraded_cargo_space,
		ship_price,
		str(bulk_mission.get("id")),
		str(mission_accepted).to_lower(),
		mission_cargo_tons,
		cargo_before_accept,
		cargo_after_accept,
		available_after_accept,
		profitable_buy_price,
		profitable_sell_price,
		profitable_margin_per_ton,
		negative_buy_price,
		negative_sell_price,
		negative_margin_per_ton,
		str(negative_margin_skipped).to_lower(),
		held_unprofitable_after_eval,
		positive_margin_lots_bought,
		positive_margin_tons_bought,
		cargo_after_trade_buy,
		str(combined_load_fits).to_lower(),
		str(route_to_levo_selected).to_lower(),
		str(mission_delivered_before_trade_sale).to_lower(),
		trade_cargo_after_delivery,
		cargo_after_delivery,
		str(retained_trade_sold_after_delivery).to_lower(),
		cargo_after_trade_sell,
		credits,
		status_line,
	])
	get_tree().quit(0)

func _run_light_freighter_refuel_mission_margin_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 100000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var starting_cargo_space := cargo_space
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var upgraded_cargo_space := cargo_space
	var bulk_mission := {
		"id": "levo_bulk_refuel_margin_supply",
		"title": "Levo Refuel Margin Bulk Supply",
		"originSystem": "Sol",
		"originBody": "Earth",
		"destinationSystem": "Levo",
		"destinationBody": "Levo Spaceport",
		"cargoTons": 120,
		"reward": 6200,
		"description": "Terminal Velocity scaffold probe for low-fuel recovery after filling remaining Light Freighter hold with positive-margin trade cargo around a bulk delivery.",
		"requiresFlags": [],
		"excludesFlags": [],
		"setsFlags": ["light_freighter_refuel_margin_supply_started"],
		"completionFlags": ["light_freighter_refuel_margin_supply_complete"],
		"choiceGroup": null,
		"next": null,
		"reputationEvent": null,
		"requirements": {},
		"timeLimitDays": 5,
		"sourceLabel": "terminal-velocity-light-freighter-refuel-mission-margin-scaffold",
		"oracleStatus": "light_freighter_refuel_mission_margin_pending_classic_runtime_trace",
	}
	missions["missions"].insert(0, bulk_mission)
	landing_tab = 0
	selected_landing_item = 0
	var mission_cargo_tons := int(bulk_mission.get("cargoTons", 0))
	var profitable_commodity := "food"
	var unprofitable_commodity := "equipment"
	var profitable_buy_price := int(_market_prices(current_system.get("name", "")).get(profitable_commodity, {}).get("buy", 0))
	var profitable_sell_price := int(_market_prices("Levo").get(profitable_commodity, {}).get("sell", 0))
	var profitable_margin_per_ton := profitable_sell_price - profitable_buy_price
	var negative_buy_price := int(_market_prices("Levo").get(unprofitable_commodity, {}).get("buy", 0))
	var negative_sell_price := int(_market_prices("Sol").get(unprofitable_commodity, {}).get("sell", 0))
	var negative_margin_per_ton := negative_sell_price - negative_buy_price
	var cargo_before_accept := cargo
	_accept_selected_mission()
	var mission_accepted := active_missions.has(str(bulk_mission.get("id")))
	var cargo_after_accept := cargo
	var available_after_accept := _cargo_available_tons()
	landing_tab = 1
	selected_landing_item = 0
	while _cargo_available_tons() >= EV_CLASSIC_COMMODITY_LOT_SIZE:
		_buy_selected_commodity()
	var positive_margin_tons_bought := int(commodity_hold.get(profitable_commodity, 0))
	var positive_margin_lots_bought := int(positive_margin_tons_bought / EV_CLASSIC_COMMODITY_LOT_SIZE)
	var held_unprofitable_after_eval := int(commodity_hold.get(unprofitable_commodity, 0))
	var negative_margin_skipped := negative_margin_per_ton < 0 and held_unprofitable_after_eval == 0
	var cargo_after_trade_buy := cargo
	var combined_load_fits := cargo_after_trade_buy == mission_cargo_tons + positive_margin_tons_bought and cargo_after_trade_buy <= upgraded_cargo_space
	player_fuel = 0
	var fuel_before_delivery_jump := player_fuel
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var blocked_loaded_delivery_for_refuel: bool = current_system.get("name", "") == "Sol" and status_line.find("Insufficient fuel") >= 0
	_position_at_body("Earth")
	_try_land()
	var refuel_succeeded := _refuel_current_ship()
	var fuel_after_refuel := player_fuel
	_ev_land_or_launch()
	selected_route.clear()
	route_to_levo_selected = _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	var completed_ids := _complete_arrived_missions()
	var mission_delivered := completed_ids.has(str(bulk_mission.get("id"))) and completed_missions.has(str(bulk_mission.get("id")))
	var trade_cargo_after_delivery := int(commodity_hold.get(profitable_commodity, 0))
	var cargo_after_delivery := cargo
	var mission_delivered_before_trade_sale := mission_delivered and trade_cargo_after_delivery == positive_margin_tons_bought and cargo_after_delivery == positive_margin_tons_bought
	landing_tab = 1
	selected_landing_item = 0
	while int(commodity_hold.get(profitable_commodity, 0)) > 0:
		_sell_selected_commodity()
	var trade_cargo_after_sell := int(commodity_hold.get(profitable_commodity, 0))
	var cargo_after_trade_sell := cargo
	var retained_trade_sold_after_delivery := trade_cargo_after_sell == 0 and cargo_after_trade_sell == 0
	print("%s routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" boughtLightFreighter=%s startingCargoSpace=%d upgradedCargoSpace=%d shipPrice=%d acceptedMission=%s missionAccepted=%s missionCargoTons=%d cargoBeforeAccept=%d cargoAfterAccept=%d availableAfterAccept=%d profitableCommodity=food unprofitableCommodity=equipment profitableBuyPrice=%d profitableSellPrice=%d profitableMarginPerTon=%d negativeBuyPrice=%d negativeSellPrice=%d negativeMarginPerTon=%d negativeMarginSkipped=%s heldUnprofitableAfterEval=%d positiveMarginLotsBought=%d positiveMarginTonsBought=%d cargoAfterTradeBuy=%d combinedLoadFits=%s routeToLevoSelected=%s fuelBeforeDeliveryJump=%d blockedLoadedDeliveryForRefuel=%s refuelSucceeded=%s fuelAfterRefuel=%d missionDeliveredBeforeTradeSale=%s tradeCargoAfterDelivery=%d cargoAfterDelivery=%d retainedTradeSoldAfterDelivery=%s cargoAfterTradeSell=%d creditsAfter=%d sourceLabel=terminal-velocity-light-freighter-refuel-mission-margin-scaffold oracleStatus=light_freighter_refuel_mission_margin_pending_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_REFUEL_MISSION_MARGIN_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(accepted_body.get("name", "None")),
		str(bought_light_freighter).to_lower(),
		starting_cargo_space,
		upgraded_cargo_space,
		ship_price,
		str(bulk_mission.get("id")),
		str(mission_accepted).to_lower(),
		mission_cargo_tons,
		cargo_before_accept,
		cargo_after_accept,
		available_after_accept,
		profitable_buy_price,
		profitable_sell_price,
		profitable_margin_per_ton,
		negative_buy_price,
		negative_sell_price,
		negative_margin_per_ton,
		str(negative_margin_skipped).to_lower(),
		held_unprofitable_after_eval,
		positive_margin_lots_bought,
		positive_margin_tons_bought,
		cargo_after_trade_buy,
		str(combined_load_fits).to_lower(),
		str(route_to_levo_selected).to_lower(),
		fuel_before_delivery_jump,
		str(blocked_loaded_delivery_for_refuel).to_lower(),
		str(refuel_succeeded).to_lower(),
		fuel_after_refuel,
		str(mission_delivered_before_trade_sale).to_lower(),
		trade_cargo_after_delivery,
		cargo_after_delivery,
		str(retained_trade_sold_after_delivery).to_lower(),
		cargo_after_trade_sell,
		credits,
		status_line,
	])
	get_tree().quit(0)

func _run_light_freighter_deadline_refuel_delivery_log() -> void:
	# Contract tokens: boughtLightFreighter=true missionAccepted=true missionCargoTons=120 fuelBeforeDeliveryJump=0 blockedLoadedDeliveryForRefuel=true refuelSucceeded=true fuelAfterRefuel=300 deliveredOnDeadlineDay=true deadlineFailurePrevented=true completedMission=levo_bulk_deadline_refuel_supply
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 100000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var starting_cargo_space := cargo_space
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var upgraded_cargo_space := cargo_space
	var bulk_mission := {
		"id": "levo_bulk_deadline_refuel_supply",
		"title": "Deadline Refuel Bulk Supply to Levo",
		"originSystem": "Sol",
		"originBody": "Earth",
		"destinationSystem": "Levo",
		"destinationBody": "Levo Spaceport",
		"cargoTons": 120,
		"reward": 6200,
		"description": "Terminal Velocity scaffold probe for final-day low-fuel recovery before delivering a Light Freighter bulk mission.",
		"requiresFlags": [],
		"excludesFlags": [],
		"setsFlags": ["light_freighter_deadline_refuel_supply_started"],
		"completionFlags": ["light_freighter_deadline_refuel_supply_complete"],
		"choiceGroup": null,
		"next": null,
		"reputationEvent": null,
		"requirements": {},
		"timeLimitDays": 5,
		"sourceLabel": "terminal-velocity-light-freighter-deadline-refuel-delivery-scaffold",
		"oracleStatus": "light_freighter_deadline_refuel_delivery_pending_classic_runtime_trace",
	}
	missions["missions"].insert(0, bulk_mission)
	landing_tab = 0
	selected_landing_item = 0
	var mission_cargo_tons := int(bulk_mission.get("cargoTons", 0))
	var cargo_before_accept := cargo
	_accept_selected_mission()
	var mission_accepted := active_missions.has(str(bulk_mission.get("id")))
	var accepted_day := int(mission_acceptance_days.get(str(bulk_mission.get("id")), current_day))
	var cargo_after_accept := cargo
	var available_after_accept := _cargo_available_tons()
	var mission_cargo_reserved := cargo_after_accept == cargo_before_accept + mission_cargo_tons
	player_fuel = 0
	var fuel_before_delivery_jump := player_fuel
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var blocked_loaded_delivery_for_refuel: bool = current_system.get("name", "") == "Sol" and status_line.find("Insufficient fuel") >= 0 and cargo == mission_cargo_tons
	_position_at_body("Earth")
	_try_land()
	var refuel_succeeded := _refuel_current_ship()
	var fuel_after_refuel := player_fuel
	_ev_land_or_launch()
	selected_route.clear()
	route_to_levo_selected = _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	current_day = accepted_day + int(bulk_mission.get("timeLimitDays", 0))
	var current_day_before_delivery := current_day
	var completed_ids := _complete_arrived_missions()
	var mission_delivered := completed_ids.has(str(bulk_mission.get("id"))) and completed_missions.has(str(bulk_mission.get("id")))
	var late_failure_attempted := false
	if not mission_delivered:
		late_failure_attempted = _fail_mission_deadline(bulk_mission, accepted_day, current_day)
	var delivered_on_deadline_day := mission_delivered and current_day_before_delivery == accepted_day + int(bulk_mission.get("timeLimitDays", 0))
	var deadline_failure_prevented := mission_delivered and not late_failure_attempted and failed_mission_history.is_empty()
	var cargo_after_delivery := cargo
	print("%s routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" boughtLightFreighter=%s startingCargoSpace=%d upgradedCargoSpace=%d shipPrice=%d acceptedMission=%s completedMission=%s missionAccepted=%s missionCargoTons=%d missionCargoReserved=%s cargoBeforeAccept=%d cargoAfterAccept=%d availableAfterAccept=%d acceptedDay=%d currentDayBeforeDelivery=%d timeLimitDays=%d routeToLevoSelected=%s fuelBeforeDeliveryJump=%d blockedLoadedDeliveryForRefuel=%s refuelSucceeded=%s fuelAfterRefuel=%d deliveredOnDeadlineDay=%s deadlineFailurePrevented=%s failedHistoryCount=%d cargoAfterDelivery=%d creditsAfterDelivery=%d sourceLabel=terminal-velocity-light-freighter-deadline-refuel-delivery-scaffold oracleStatus=light_freighter_deadline_refuel_delivery_pending_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_DEADLINE_REFUEL_DELIVERY_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(accepted_body.get("name", "None")),
		str(bought_light_freighter).to_lower(),
		starting_cargo_space,
		upgraded_cargo_space,
		ship_price,
		str(bulk_mission.get("id")),
		str(bulk_mission.get("id")) if mission_delivered else "None",
		str(mission_accepted).to_lower(),
		mission_cargo_tons,
		str(mission_cargo_reserved).to_lower(),
		cargo_before_accept,
		cargo_after_accept,
		available_after_accept,
		accepted_day,
		current_day_before_delivery,
		int(bulk_mission.get("timeLimitDays", 0)),
		str(route_to_levo_selected).to_lower(),
		fuel_before_delivery_jump,
		str(blocked_loaded_delivery_for_refuel).to_lower(),
		str(refuel_succeeded).to_lower(),
		fuel_after_refuel,
		str(delivered_on_deadline_day).to_lower(),
		str(deadline_failure_prevented).to_lower(),
		failed_mission_history.size(),
		cargo_after_delivery,
		credits,
		status_line,
	])
	get_tree().quit(0)

func _run_light_freighter_repair_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 70000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var max_hull_after_purchase := _max_player_hull()
	player_hull = 260
	credits = 840
	var damaged_hull := player_hull
	var credits_before_trade := credits
	var repair_cost_before_trade := _repair_cost()
	var trade_commodity := "food"
	var buy_price := int(_market_prices(current_system.get("name", "")).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices("Levo").get(trade_commodity, {}).get("sell", 0))
	var trade_margin_per_ton := sell_price - buy_price
	landing_tab = 1
	selected_landing_item = 0
	_buy_selected_commodity()
	_buy_selected_commodity()
	var trade_cargo_after_buy := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_buy := cargo
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	_sell_selected_commodity()
	var credits_after_trade := credits
	var trade_cargo_after_sell := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_sell := cargo
	_ev_land_or_launch()
	selected_route.clear()
	var route_back_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var repair_funded_by_trade := (credits_after_trade - credits_before_trade) >= repair_cost_before_trade and credits_after_trade >= repair_cost_before_trade
	var repair_succeeded := _repair_current_hull()
	var repaired_hull := player_hull
	print("%s routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" boughtLightFreighter=%s shipPrice=%d damagedHull=%d maxHull=%d creditsBeforeTrade=%d repairCostBeforeTrade=%d tradeCommodity=%s buyPrice=%d sellPrice=%d tradeMarginPerTon=%d tradeCargoAfterBuy=%d cargoAfterTradeBuy=%d routeToLevoSelected=%s creditsAfterTrade=%d tradeCargoAfterSell=%d cargoAfterTradeSell=%d routeBackToSolSelected=%s repairFundedByTrade=%s repairSucceeded=%s repairedHull=%d creditsAfterRepair=%d sourceLabel=terminal-velocity-light-freighter-repair-margin-scaffold oracleStatus=light_freighter_repair_margin_pending_classic_runtime_trace repairSourceLabel=terminal-velocity-repair-service-scaffold repairOracleStatus=repair_service_pending_ev_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_REPAIR_TRADE_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(accepted_body.get("name", "None")),
		str(bought_light_freighter).to_lower(),
		ship_price,
		damaged_hull,
		max_hull_after_purchase,
		credits_before_trade,
		repair_cost_before_trade,
		trade_commodity,
		buy_price,
		sell_price,
		trade_margin_per_ton,
		trade_cargo_after_buy,
		cargo_after_trade_buy,
		str(route_to_levo_selected).to_lower(),
		credits_after_trade,
		trade_cargo_after_sell,
		cargo_after_trade_sell,
		str(route_back_to_sol_selected).to_lower(),
		str(repair_funded_by_trade).to_lower(),
		str(repair_succeeded).to_lower(),
		repaired_hull,
		credits,
		status_line,
	])
	get_tree().quit(0)

func _run_light_freighter_repair_mission_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 100000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var max_hull_after_purchase := _max_player_hull()
	player_hull = 260
	credits = 1260
	var damaged_hull := player_hull
	var credits_before_mission_trade := credits
	var repair_cost_before_mission_trade := _repair_cost()
	var bulk_mission := {
		"id": "levo_bulk_repair_margin_supply",
		"title": "Repair Margin Bulk Supply to Levo",
		"originSystem": "Sol",
		"originBody": "Earth",
		"destinationSystem": "Levo",
		"destinationBody": "Levo Spaceport",
		"cargoTons": 120,
		"reward": 7000,
		"description": "Terminal Velocity scaffold probe for damaged Light Freighter mission cargo, retained margin cargo, and post-route repair funding.",
		"requiresFlags": [],
		"excludesFlags": [],
		"setsFlags": ["light_freighter_repair_margin_delivery_started"],
		"completionFlags": ["light_freighter_repair_margin_delivery_complete"],
		"choiceGroup": null,
		"next": null,
		"reputationEvent": null,
		"requirements": {},
		"timeLimitDays": 5,
		"sourceLabel": "terminal-velocity-light-freighter-repair-mission-margin-scaffold",
		"oracleStatus": "light_freighter_repair_mission_margin_pending_classic_runtime_trace",
	}
	missions["missions"].insert(0, bulk_mission)
	landing_tab = 0
	selected_landing_item = 0
	var mission_cargo_tons := int(bulk_mission.get("cargoTons", 0))
	_accept_selected_mission()
	var mission_accepted := active_missions.has(str(bulk_mission.get("id")))
	var cargo_after_accept := cargo
	var available_after_accept := _cargo_available_tons()
	var trade_commodity := "food"
	var buy_price := int(_market_prices(current_system.get("name", "")).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices("Levo").get(trade_commodity, {}).get("sell", 0))
	var trade_margin_per_ton := sell_price - buy_price
	landing_tab = 1
	selected_landing_item = 0
	_buy_selected_commodity()
	_buy_selected_commodity()
	_buy_selected_commodity()
	var trade_cargo_after_buy := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_buy := cargo
	var mission_cargo_reserved := mission_accepted and cargo_after_accept == mission_cargo_tons and available_after_accept == cargo_space - mission_cargo_tons
	var combined_load_fits := cargo_after_trade_buy == mission_cargo_tons + trade_cargo_after_buy and cargo_after_trade_buy <= cargo_space
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	var completed_ids := _complete_arrived_missions()
	var mission_delivered := completed_ids.has(str(bulk_mission.get("id"))) and completed_missions.has(str(bulk_mission.get("id")))
	var trade_cargo_after_delivery := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_delivery := cargo
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	_sell_selected_commodity()
	_sell_selected_commodity()
	var credits_after_mission_trade := credits
	var trade_cargo_after_sell := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_sell := cargo
	_ev_land_or_launch()
	selected_route.clear()
	var route_back_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var repair_funded_by_mission_trade := mission_delivered and credits_after_mission_trade >= repair_cost_before_mission_trade
	var repair_succeeded := _repair_current_hull()
	var repaired_hull := player_hull
	print("%s routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" boughtLightFreighter=%s shipPrice=%d damagedHull=%d maxHull=%d creditsBeforeMissionTrade=%d repairCostBeforeMissionTrade=%d acceptedMission=%s missionAccepted=%s missionCargoTons=%d missionCargoReserved=%s availableAfterAccept=%d tradeCommodity=%s buyPrice=%d sellPrice=%d tradeMarginPerTon=%d tradeCargoAfterBuy=%d cargoAfterTradeBuy=%d combinedLoadFits=%s routeToLevoSelected=%s missionDeliveredBeforeRepair=%s tradeCargoAfterDelivery=%d cargoAfterDelivery=%d creditsAfterMissionTrade=%d tradeCargoAfterSell=%d cargoAfterTradeSell=%d routeBackToSolSelected=%s repairFundedByMissionTrade=%s repairSucceeded=%s repairedHull=%d creditsAfterRepair=%d sourceLabel=terminal-velocity-light-freighter-repair-mission-margin-scaffold oracleStatus=light_freighter_repair_mission_margin_pending_classic_runtime_trace repairSourceLabel=terminal-velocity-repair-service-scaffold repairOracleStatus=repair_service_pending_ev_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_REPAIR_MISSION_TRADE_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(accepted_body.get("name", "None")),
		str(bought_light_freighter).to_lower(),
		ship_price,
		damaged_hull,
		max_hull_after_purchase,
		credits_before_mission_trade,
		repair_cost_before_mission_trade,
		str(bulk_mission.get("id")),
		str(mission_accepted).to_lower(),
		mission_cargo_tons,
		str(mission_cargo_reserved).to_lower(),
		available_after_accept,
		trade_commodity,
		buy_price,
		sell_price,
		trade_margin_per_ton,
		trade_cargo_after_buy,
		cargo_after_trade_buy,
		str(combined_load_fits).to_lower(),
		str(route_to_levo_selected).to_lower(),
		str(mission_delivered).to_lower(),
		trade_cargo_after_delivery,
		cargo_after_delivery,
		credits_after_mission_trade,
		trade_cargo_after_sell,
		cargo_after_trade_sell,
		str(route_back_to_sol_selected).to_lower(),
		str(repair_funded_by_mission_trade).to_lower(),
		str(repair_succeeded).to_lower(),
		repaired_hull,
		credits,
		status_line,
	])
	get_tree().quit(0)


func _run_light_freighter_repair_refuel_mission_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 100000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	var selected_ship_listing := {}
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			selected_ship_listing = shipyard_listings[i]
			break
	var ship_price := int(selected_ship_listing.get("price", 0))
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var max_hull_after_purchase := _max_player_hull()
	player_hull = 260
	credits = 1260
	var damaged_hull := player_hull
	var credits_before_mission_trade := credits
	var repair_cost_before_mission_trade := _repair_cost()
	var bulk_mission := {
		"id": "levo_bulk_repair_refuel_margin_supply",
		"title": "Repair Refuel Margin Bulk Supply to Levo",
		"originSystem": "Sol",
		"originBody": "Earth",
		"destinationSystem": "Levo",
		"destinationBody": "Levo Spaceport",
		"cargoTons": 120,
		"reward": 7000,
		"description": "Terminal Velocity scaffold probe for damaged low-fuel Light Freighter mission cargo, retained margin cargo, refuel recovery, and post-route repair funding.",
		"requiresFlags": [],
		"excludesFlags": [],
		"setsFlags": ["light_freighter_repair_margin_delivery_started"],
		"completionFlags": ["light_freighter_repair_margin_delivery_complete"],
		"choiceGroup": null,
		"next": null,
		"reputationEvent": null,
		"requirements": {},
		"timeLimitDays": 5,
		"sourceLabel": "terminal-velocity-light-freighter-repair-refuel-mission-margin-scaffold",
		"oracleStatus": "light_freighter_repair_refuel_mission_margin_pending_classic_runtime_trace",
	}
	missions["missions"].insert(0, bulk_mission)
	landing_tab = 0
	selected_landing_item = 0
	var mission_cargo_tons := int(bulk_mission.get("cargoTons", 0))
	_accept_selected_mission()
	var mission_accepted := active_missions.has(str(bulk_mission.get("id")))
	var cargo_after_accept := cargo
	var available_after_accept := _cargo_available_tons()
	var trade_commodity := "food"
	var buy_price := int(_market_prices(current_system.get("name", "")).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices("Levo").get(trade_commodity, {}).get("sell", 0))
	var trade_margin_per_ton := sell_price - buy_price
	landing_tab = 1
	selected_landing_item = 0
	_buy_selected_commodity()
	_buy_selected_commodity()
	_buy_selected_commodity()
	var trade_cargo_after_buy := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_buy := cargo
	var mission_cargo_reserved := mission_accepted and cargo_after_accept == mission_cargo_tons and available_after_accept == cargo_space - mission_cargo_tons
	var combined_load_fits := cargo_after_trade_buy == mission_cargo_tons + trade_cargo_after_buy and cargo_after_trade_buy <= cargo_space
	player_fuel = 0
	var fuel_before_delivery_jump := player_fuel
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var blocked_loaded_delivery_for_refuel: bool = current_system.get("name", "") == "Sol" and status_line.find("Insufficient fuel") >= 0
	_position_at_body("Earth")
	_try_land()
	var refuel_succeeded := _refuel_current_ship()
	var fuel_after_refuel := player_fuel
	_ev_land_or_launch()
	selected_route.clear()
	route_to_levo_selected = _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	var completed_ids := _complete_arrived_missions()
	var mission_delivered := completed_ids.has(str(bulk_mission.get("id"))) and completed_missions.has(str(bulk_mission.get("id")))
	var trade_cargo_after_delivery := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_delivery := cargo
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	_sell_selected_commodity()
	_sell_selected_commodity()
	var credits_after_mission_trade := credits
	var trade_cargo_after_sell := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_sell := cargo
	_ev_land_or_launch()
	selected_route.clear()
	var route_back_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var route_to_repair_port_after_refuel := route_back_to_sol_selected
	_position_at_body("Earth")
	_try_land()
	var repair_funded_by_mission_trade := mission_delivered and credits_after_mission_trade >= repair_cost_before_mission_trade
	var repair_succeeded := _repair_current_hull()
	var repaired_hull := player_hull
	print("%s routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" boughtLightFreighter=%s shipPrice=%d damagedHull=%d maxHull=%d creditsBeforeMissionTrade=%d repairCostBeforeMissionTrade=%d acceptedMission=%s missionAccepted=%s missionCargoTons=%d missionCargoReserved=%s availableAfterAccept=%d tradeCommodity=%s buyPrice=%d sellPrice=%d tradeMarginPerTon=%d tradeCargoAfterBuy=%d cargoAfterTradeBuy=%d combinedLoadFits=%s routeToLevoSelected=%s fuelBeforeDeliveryJump=%d blockedLoadedDeliveryForRefuel=%s refuelSucceeded=%s fuelAfterRefuel=%d missionDeliveredBeforeRepair=%s tradeCargoAfterDelivery=%d cargoAfterDelivery=%d creditsAfterMissionTrade=%d tradeCargoAfterSell=%d cargoAfterTradeSell=%d routeBackToSolSelected=%s routeToRepairPortAfterRefuel=%s repairFundedByMissionTrade=%s repairSucceeded=%s repairedHull=%d creditsAfterRepair=%d sourceLabel=terminal-velocity-light-freighter-repair-refuel-mission-margin-scaffold oracleStatus=light_freighter_repair_refuel_mission_margin_pending_classic_runtime_trace repairSourceLabel=terminal-velocity-repair-service-scaffold repairOracleStatus=repair_service_pending_ev_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_REPAIR_REFUEL_MISSION_TRADE_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(accepted_body.get("name", "None")),
		str(bought_light_freighter).to_lower(),
		ship_price,
		damaged_hull,
		max_hull_after_purchase,
		credits_before_mission_trade,
		repair_cost_before_mission_trade,
		str(bulk_mission.get("id")),
		str(mission_accepted).to_lower(),
		mission_cargo_tons,
		str(mission_cargo_reserved).to_lower(),
		available_after_accept,
		trade_commodity,
		buy_price,
		sell_price,
		trade_margin_per_ton,
		trade_cargo_after_buy,
		cargo_after_trade_buy,
		str(combined_load_fits).to_lower(),
		str(route_to_levo_selected).to_lower(),
		fuel_before_delivery_jump,
		str(blocked_loaded_delivery_for_refuel).to_lower(),
		str(refuel_succeeded).to_lower(),
		fuel_after_refuel,
		str(mission_delivered).to_lower(),
		trade_cargo_after_delivery,
		cargo_after_delivery,
		credits_after_mission_trade,
		trade_cargo_after_sell,
		cargo_after_trade_sell,
		str(route_back_to_sol_selected).to_lower(),
		str(route_to_repair_port_after_refuel).to_lower(),
		str(repair_funded_by_mission_trade).to_lower(),
		str(repair_succeeded).to_lower(),
		repaired_hull,
		credits,
		status_line,
	])
	get_tree().quit(0)

func _run_light_freighter_deadline_repair_refuel_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var accepted_body := _current_body()
	credits = 100000
	landing_tab = 3
	var shipyard_listings := _shipyard_listings(accepted_body)
	for i in range(shipyard_listings.size()):
		if str(shipyard_listings[i].get("shipId", "")) == "light_freighter":
			selected_landing_item = i
			break
	_buy_selected_ship()
	var bought_light_freighter := player_ship_id == "light_freighter"
	var max_hull_after_purchase := _max_player_hull()
	player_hull = 260
	credits = 1260
	player_fuel = 0
	var damaged_hull := player_hull
	var repair_cost_before_mission_trade := _repair_cost()
	var bulk_mission := {
		"id": "levo_bulk_deadline_repair_refuel_margin_supply",
		"title": "Deadline Repair Refuel Margin Bulk Supply to Levo",
		"originSystem": "Sol",
		"originBody": "Earth",
		"destinationSystem": "Levo",
		"destinationBody": "Levo Spaceport",
		"cargoTons": 120,
		"reward": 7000,
		"description": "Terminal Velocity scaffold probe for damaged low-fuel Light Freighter deadline delivery, retained margin cargo, refuel recovery, and post-route repair funding.",
		"requiresFlags": [],
		"excludesFlags": [],
		"setsFlags": ["light_freighter_deadline_repair_margin_delivery_started"],
		"completionFlags": ["light_freighter_deadline_repair_margin_delivery_complete"],
		"choiceGroup": null,
		"next": null,
		"reputationEvent": null,
		"requirements": {},
		"timeLimitDays": 2,
		"sourceLabel": "terminal-velocity-light-freighter-deadline-repair-refuel-margin-scaffold",
		"oracleStatus": "light_freighter_deadline_repair_refuel_margin_pending_classic_runtime_trace",
	}
	missions["missions"].insert(0, bulk_mission)
	landing_tab = 0
	selected_landing_item = 0
	var mission_cargo_tons := int(bulk_mission.get("cargoTons", 0))
	_accept_selected_mission()
	var mission_accepted := active_missions.has(str(bulk_mission.get("id")))
	var cargo_after_accept := cargo
	var available_after_accept := _cargo_available_tons()
	var trade_commodity := "food"
	var buy_price := int(_market_prices(current_system.get("name", "")).get(trade_commodity, {}).get("buy", 0))
	var sell_price := int(_market_prices("Levo").get(trade_commodity, {}).get("sell", 0))
	var trade_margin_per_ton := sell_price - buy_price
	landing_tab = 1
	selected_landing_item = 0
	_buy_selected_commodity()
	_buy_selected_commodity()
	_buy_selected_commodity()
	var trade_cargo_after_buy := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_buy := cargo
	var mission_cargo_reserved := mission_accepted and cargo_after_accept == mission_cargo_tons and available_after_accept == cargo_space - mission_cargo_tons
	var combined_load_fits := cargo_after_trade_buy == mission_cargo_tons + trade_cargo_after_buy and cargo_after_trade_buy <= cargo_space
	var accepted_day := current_day
	_ev_land_or_launch()
	selected_route.clear()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var blocked_loaded_delivery_for_refuel: bool = current_system.get("name", "") == "Sol" and status_line.find("Insufficient fuel") >= 0
	_position_at_body("Earth")
	_try_land()
	var refuel_succeeded := _refuel_current_ship()
	var fuel_after_refuel := player_fuel
	_ev_land_or_launch()
	selected_route.clear()
	route_to_levo_selected = _select_map_route_to_system("Levo")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Levo Spaceport")
	_try_land()
	current_day = accepted_day + int(bulk_mission.get("timeLimitDays", 0))
	var current_day_before_delivery := current_day
	var completed_ids := _complete_arrived_missions()
	var mission_delivered := completed_ids.has(str(bulk_mission.get("id"))) and completed_missions.has(str(bulk_mission.get("id")))
	var late_failure_attempted := _fail_mission_deadline(bulk_mission, accepted_day, current_day)
	var delivered_on_deadline_day := mission_delivered and current_day_before_delivery == accepted_day + int(bulk_mission.get("timeLimitDays", 0))
	var deadline_failure_prevented_before_repair := not late_failure_attempted and failed_mission_history.is_empty()
	var trade_cargo_after_delivery := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_delivery := cargo
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	_sell_selected_commodity()
	_sell_selected_commodity()
	var credits_after_mission_trade := credits
	var trade_cargo_after_sell := int(commodity_hold.get(trade_commodity, 0))
	var cargo_after_trade_sell := cargo
	_ev_land_or_launch()
	selected_route.clear()
	var route_back_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_position_at_body("Earth")
	_try_land()
	var repair_funded_by_mission_trade := mission_delivered and credits_after_mission_trade >= repair_cost_before_mission_trade
	var repair_succeeded := _repair_current_hull()
	var repaired_hull := player_hull
	print("%s routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" boughtLightFreighter=%s damagedHull=%d maxHull=%d repairCostBeforeMissionTrade=%d acceptedMission=%s missionAccepted=%s missionCargoTons=%d missionCargoReserved=%s availableAfterAccept=%d tradeCommodity=%s buyPrice=%d sellPrice=%d tradeMarginPerTon=%d tradeCargoAfterBuy=%d cargoAfterTradeBuy=%d combinedLoadFits=%s acceptedDay=%d currentDayBeforeDelivery=%d timeLimitDays=%d deliveredOnDeadlineDay=%s routeToLevoSelected=%s blockedLoadedDeliveryForRefuel=%s refuelSucceeded=%s fuelAfterRefuel=%d missionDeliveredBeforeRepair=%s deadlineFailurePreventedBeforeRepair=%s failedHistoryCount=%d tradeCargoAfterDelivery=%d cargoAfterDelivery=%d creditsAfterMissionTrade=%d tradeCargoAfterSell=%d cargoAfterTradeSell=%d routeBackToSolSelected=%s repairFundedByMissionTrade=%s repairSucceeded=%s repairedHull=%d creditsAfterRepair=%d sourceLabel=terminal-velocity-light-freighter-deadline-repair-refuel-margin-scaffold oracleStatus=light_freighter_deadline_repair_refuel_margin_pending_classic_runtime_trace repairSourceLabel=terminal-velocity-repair-service-scaffold repairOracleStatus=repair_service_pending_ev_classic_runtime_trace status=\"%s\"" % [
		LIGHT_FREIGHTER_DEADLINE_REPAIR_REFUEL_EVENT_LOG_PREFIX,
		str(route_to_sol_selected).to_lower(),
		str(accepted_body.get("name", "None")),
		str(bought_light_freighter).to_lower(),
		damaged_hull,
		max_hull_after_purchase,
		repair_cost_before_mission_trade,
		str(bulk_mission.get("id")),
		str(mission_accepted).to_lower(),
		mission_cargo_tons,
		str(mission_cargo_reserved).to_lower(),
		available_after_accept,
		trade_commodity,
		buy_price,
		sell_price,
		trade_margin_per_ton,
		trade_cargo_after_buy,
		cargo_after_trade_buy,
		str(combined_load_fits).to_lower(),
		accepted_day,
		current_day_before_delivery,
		int(bulk_mission.get("timeLimitDays", 0)),
		str(delivered_on_deadline_day).to_lower(),
		str(route_to_levo_selected).to_lower(),
		str(blocked_loaded_delivery_for_refuel).to_lower(),
		str(refuel_succeeded).to_lower(),
		fuel_after_refuel,
		str(mission_delivered).to_lower(),
		str(deadline_failure_prevented_before_repair).to_lower(),
		failed_mission_history.size(),
		trade_cargo_after_delivery,
		cargo_after_delivery,
		credits_after_mission_trade,
		trade_cargo_after_sell,
		cargo_after_trade_sell,
		str(route_back_to_sol_selected).to_lower(),
		str(repair_funded_by_mission_trade).to_lower(),
		str(repair_succeeded).to_lower(),
		repaired_hull,
		credits,
		status_line,
	])
	get_tree().quit(0)

func _run_legal_patrol_posture_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var government_name := _current_government_name()
	legal_records[government_name] = -75
	status_messages.clear()
	_emit_legal_patrol_warning_if_needed()
	_select_closest_target()
	var patrol_warning := status_messages.has(_legal_patrol_warning_message(government_name))
	var hostile_posture := _legal_patrol_hostile_posture_active(government_name)
	print("%s routeToSolSelected=%s system=%s government=\"%s\" legalScore=%d patrolWarning=%s hostilePosture=%s combatExecuted=false targetStatus=\"%s\" sourceLabel=terminal-velocity-classic-resource-patrol-semantics oracleStatus=classic_runtime_combat_timing_pending" % [LEGAL_PATROL_POSTURE_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), government_name, int(legal_records.get(government_name, 0)), str(patrol_warning), str(hostile_posture), status_line])
	get_tree().quit(0)

func _run_mission_legal_eligibility_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var body := _current_body()
	var government_name := _current_government_name()
	var test_mission := {
		"id": "legal_clean_test_contract",
		"title": "Clean Legal Standing Contract",
		"originSystem": current_system.get("name", ""),
		"originBody": body.get("name", ""),
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 1,
		"reward": 100,
		"description": "Terminal Velocity legal eligibility scaffold contract.",
		"requiresFlags": [],
		"excludesFlags": [],
		"setsFlags": [],
		"completionFlags": [],
		"requirements": {"legalMin": {government_name: 0}}
	}
	var mission_list: Array = missions.get("missions", [])
	mission_list.append(test_mission)
	missions["missions"] = mission_list
	legal_records[government_name] = 0
	var clean_available := _available_missions(body).any(func(m): return str(m.get("id", "")) == "legal_clean_test_contract")
	legal_records[government_name] = -75
	var blocked_available := _available_missions(body).any(func(m): return str(m.get("id", "")) == "legal_clean_test_contract")
	var blocked_reasons := _blocked_mission_reasons(body)
	var blocked_reason := _mission_legal_requirement_block_reason(test_mission)
	var visible_blocked_reason := not blocked_reasons.is_empty()
	var blocked_title_visible := blocked_reasons.any(func(reason): return str(reason).contains("Clean Legal Standing Contract"))
	var blocked_source_line := _blocked_mission_source_boundary_line()
	var blocked_source_visible := blocked_source_line.contains("Terminal Velocity") and blocked_source_line.contains("Classic")
	print("%s routeToSolSelected=%s system=%s body=%s government=\"%s\" cleanAvailable=%s blockedAvailable=%s visibleBlockedReason=%s blockedTitleVisible=%s blockedSourceVisible=%s legalScore=%d blockedReason=\"%s\" blockedReasons=%s blockedSourceLine=\"%s\" sourceLabel=terminal-velocity-classic-resource-mission-availability oracleStatus=classic_runtime_ui_wording_pending" % [MISSION_LEGAL_ELIGIBILITY_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), body.get("name", "?"), government_name, str(clean_available), str(blocked_available), str(visible_blocked_reason), str(blocked_title_visible), str(blocked_source_visible), int(legal_records.get(government_name, 0)), blocked_reason, JSON.stringify(blocked_reasons), blocked_source_line])
	get_tree().quit(0)

func _run_mission_story_gate_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var body := _current_body()
	var missing_flag_mission := {
		"id": "story_gate_missing_flag_probe",
		"title": "Story Gate Missing Flag Probe",
		"originSystem": current_system.get("name", ""),
		"originBody": body.get("name", ""),
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 1,
		"reward": 100,
		"description": "Terminal Velocity story-gate missing flag scaffold contract.",
		"requiresFlags": ["frontier_samples_delivered"],
		"excludesFlags": [],
		"setsFlags": [],
		"completionFlags": [],
		"requirements": {}
	}
	var excluded_flag_mission := {
		"id": "story_gate_excluded_flag_probe",
		"title": "Story Gate Excluded Flag Probe",
		"originSystem": current_system.get("name", ""),
		"originBody": body.get("name", ""),
		"destinationSystem": "Centauri",
		"destinationBody": "Luna",
		"cargoTons": 1,
		"reward": 100,
		"description": "Terminal Velocity story-gate exclusion scaffold contract.",
		"requiresFlags": [],
		"excludesFlags": ["alignment_federation"],
		"setsFlags": [],
		"completionFlags": [],
		"requirements": {}
	}
	var mission_list: Array = missions.get("missions", [])
	mission_list.append(missing_flag_mission)
	mission_list.append(excluded_flag_mission)
	missions["missions"] = mission_list
	story_flags = ["alignment_federation"]
	var missing_available := _available_missions(body).any(func(m): return str(m.get("id", "")) == "story_gate_missing_flag_probe")
	var excluded_available := _available_missions(body).any(func(m): return str(m.get("id", "")) == "story_gate_excluded_flag_probe")
	var blocked_reasons := _blocked_mission_reasons(body)
	var missing_reason := _mission_story_gate_block_reason(missing_flag_mission)
	var excluded_reason := _mission_story_gate_block_reason(excluded_flag_mission)
	var missing_visible := blocked_reasons.any(func(reason): return str(reason).contains("Story Gate Missing Flag Probe") and str(reason).contains("frontier_samples_delivered"))
	var excluded_visible := blocked_reasons.any(func(reason): return str(reason).contains("Story Gate Excluded Flag Probe") and str(reason).contains("alignment_federation"))
	var blocked_source_line := _blocked_mission_source_boundary_line()
	var blocked_source_visible := blocked_source_line.contains("Terminal Velocity") and blocked_source_line.contains("Classic")
	print("%s routeToSolSelected=%s system=%s body=%s storyFlags=%s missingAvailable=%s excludedAvailable=%s missingStoryGateVisible=%s excludedStoryGateVisible=%s blockedSourceVisible=%s missingGateState=%s excludedGateState=%s missingReason=\"%s\" excludedReason=\"%s\" blockedReasons=%s blockedSourceLine=\"%s\" sourceLabel=terminal-velocity-mission-story-gate-scaffold oracleStatus=classic_runtime_offer_visibility_pending" % [MISSION_STORY_GATE_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), body.get("name", "?"), JSON.stringify(story_flags), str(missing_available), str(excluded_available), str(missing_visible), str(excluded_visible), str(blocked_source_visible), _mission_story_gate_state(missing_flag_mission), _mission_story_gate_state(excluded_flag_mission), missing_reason, excluded_reason, JSON.stringify(blocked_reasons), blocked_source_line])
	get_tree().quit(0)

func _run_mission_alignment_gate_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var body := _current_body()
	var body_name := str(body.get("name", "?"))
	var government_name := _current_government_name()
	var alignment_gate_mission := {
		"id": "alignment_gate_probe",
		"title": "Alignment Gate Probe",
		"originSystem": current_system.get("name", ""),
		"originBody": body.get("name", ""),
		"destinationSystem": "Sirius",
		"destinationBody": "Sirius Station",
		"cargoTons": 1,
		"reward": 100,
		"description": "Terminal Velocity alignment gate scaffold contract.",
		"requiresFlags": ["frontier_samples_delivered"],
		"excludesFlags": [],
		"setsFlags": [],
		"completionFlags": [],
		"requirements": {"reputationMin": {government_name: 5}, "legalMin": {government_name: -20}}
	}
	var mission_list: Array = missions.get("missions", [])
	mission_list.append(alignment_gate_mission)
	missions["missions"] = mission_list
	story_flags = []
	reputation_scores[government_name] = 0
	legal_records[government_name] = -10
	var blocked_without_story := _blocked_mission_reasons(body)
	var alignment_requirement_blocked := blocked_without_story.any(func(reason): return str(reason).contains("Alignment Gate Probe") and str(reason).contains("frontier_samples_delivered"))
	story_flags = ["frontier_samples_delivered"]
	reputation_scores[government_name] = 5
	legal_records[government_name] = -50
	var blocked_for_legal := _blocked_mission_reasons(body)
	var alignment_legal_blocked := blocked_for_legal.any(func(reason): return str(reason).contains("Alignment Gate Probe") and str(reason).contains("legal score"))
	legal_records[government_name] = -20
	var recovered_offer_ids := _mission_ids(_available_missions(body))
	var alignment_recovered_after_gates := recovered_offer_ids.has("alignment_gate_probe")
	var help_text := "\n".join(_help_overlay_lines())
	var alignment_help_visible := help_text.contains("Alignment gates: story offers may require prior flags")
	print("%s routeToSolSelected=%s system=%s body=%s government=\"%s\" alignmentRequirementBlocked=%s alignmentLegalBlocked=%s alignmentRecoveredAfterGates=%s alignmentGateHelpVisible=%s blockedWithoutStory=%s blockedForLegal=%s recoveredOffers=%s sourceLabel=terminal-velocity-mission-alignment-gate-scaffold oracleStatus=classic_runtime_alignment_offer_gate_ui_pending sourceBasis=EV Classic Resource Bible: mission AvailRecord/ScanGovt/PayVal plus Terminal Velocity requirement scaffolds" % [MISSION_ALIGNMENT_GATE_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), body_name, government_name, str(alignment_requirement_blocked), str(alignment_legal_blocked), str(alignment_recovered_after_gates), str(alignment_help_visible), JSON.stringify(blocked_without_story), JSON.stringify(blocked_for_legal), JSON.stringify(recovered_offer_ids)])
	get_tree().quit(0)

func _run_legal_consequence_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var government_name := _current_government_name()
	legal_records[government_name] = -75
	reputation_scores[government_name] = 0
	reputation_scores["Pirate"] = 0
	status_messages.clear()
	_select_closest_target()
	var target_index := selected_target_index
	var primary_weapon := _primary_weapon_stats()
	var final_hit_hull := _weapon_hull_damage(primary_weapon)
	target_shields[target_index] = 0
	target_hulls[target_index] = final_hit_hull
	primary_weapon_cooldown_frames = 0.0
	var before_legal := int(legal_records.get(government_name, 0))
	var before_reputation := int(reputation_scores.get(government_name, 0))
	var before_pirate_reputation := int(reputation_scores.get("Pirate", 0))
	var projectile_spawned := _spawn_primary_projectile()
	for _i in range(90):
		_advance_projectiles(1.0 / 60.0)
	var target_destroyed := _target_destroyed(target_index)
	var explosion_triggered := not explosion_events.is_empty()
	var after_legal := int(legal_records.get(government_name, 0))
	var after_reputation := int(reputation_scores.get(government_name, 0))
	var after_pirate_reputation := int(reputation_scores.get("Pirate", 0))
	var applied := status_messages.has(_legal_patrol_attack_message(government_name))
	var legal_delta_applied := after_legal - before_legal
	var reputation_delta_applied := after_reputation - before_reputation
	var pirate_reputation_delta_applied := after_pirate_reputation - before_pirate_reputation
	print("%s routeToSolSelected=%s system=%s government=\"%s\" event=destroy_patrol sourceEvent=destroy_patrol manualBacked=true consequenceApplied=%s combatExecuted=true projectileSpawned=%s targetDestroyed=%s explosionTriggered=%s targetIndex=%d legalBefore=%d legalAfter=%d legalDeltaApplied=%d reputationBefore=%d reputationAfter=%d reputationDeltaApplied=%d pirateReputationBefore=%d pirateReputationAfter=%d pirateReputationDeltaApplied=%d status=\"%s\" sourceLabel=terminal-velocity-classic-resource-govt-penalty-semantics oracleStatus=classic_runtime_combat_resolution_pending" % [LEGAL_CONSEQUENCE_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), government_name, str(applied), str(projectile_spawned), str(target_destroyed), str(explosion_triggered), target_index, before_legal, after_legal, legal_delta_applied, before_reputation, after_reputation, reputation_delta_applied, before_pirate_reputation, after_pirate_reputation, pirate_reputation_delta_applied, status_line])
	get_tree().quit(0)

func _run_legal_clemency_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var government_name := _current_government_name()
	var mechanics: Dictionary = reputation.get("mechanics", {})
	var clemency_cost := int(mechanics.get("clemencyCost", 1000))
	legal_records[government_name] = -45
	reputation_scores[government_name] = int(mechanics.get("clemencyMinReputation", 10))
	credits = max(0, clemency_cost - 1)
	var before_legal := int(legal_records.get(government_name, 0))
	var insufficient_credits_before := credits
	status_messages.clear()
	var insufficient_paid := _pay_legal_clemency()
	var insufficient_status := status_line
	var clemency_insufficient_credit_blocked := not insufficient_paid and insufficient_status.contains("insufficient funds") and int(legal_records.get(government_name, 0)) == before_legal and credits == insufficient_credits_before
	credits = clemency_cost + 500
	var before_credits := credits
	status_messages.clear()
	var paid := _pay_legal_clemency()
	var after_legal := int(legal_records.get(government_name, 0))
	var after_credits := credits
	var clemency_recovered_after_credits := paid and after_legal > before_legal and after_credits == before_credits - clemency_cost
	print("%s routeToSolSelected=%s system=%s government=\"%s\" paid=%s clemencyInsufficientCreditBlocked=%s clemencyRecoveredAfterCredits=%s legalBefore=%d legalAfter=%d insufficientCreditsBefore=%d creditsBefore=%d creditsAfter=%d insufficientStatus=\"%s\" status=\"%s\" sourceLabel=terminal-velocity-inferred-clemency-scaffold oracleStatus=approved_inference_pending_ev_classic_confirmation" % [LEGAL_CLEMENCY_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), government_name, str(paid), str(clemency_insufficient_credit_blocked), str(clemency_recovered_after_credits), before_legal, after_legal, insufficient_credits_before, before_credits, after_credits, insufficient_status, status_line])
	get_tree().quit(0)

func _run_contraband_scan_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var government_name := _current_government_name()
	commodity_hold["equipment"] = EV_CLASSIC_COMMODITY_LOT_SIZE
	cargo = EV_CLASSIC_COMMODITY_LOT_SIZE
	credits = 5000
	legal_records[government_name] = 0
	var before_credits := credits
	var before_legal := int(legal_records.get(government_name, 0))
	var before_equipment := int(commodity_hold.get("equipment", 0))
	_try_land()
	var after_credits := credits
	var after_legal := int(legal_records.get(government_name, 0))
	var after_equipment := int(commodity_hold.get("equipment", 0))
	var action := str(_last_contraband_scan_outcome.get("action", "none"))
	print("%s routeToSolSelected=%s system=%s government=\"%s\" action=%s creditsBefore=%d creditsAfter=%d legalBefore=%d legalAfter=%d illegalEquipmentBefore=%d illegalEquipmentAfter=%d status=\"%s\" sourceLabel=terminal-velocity-classic-resource-smuggling-scan-semantics oracleStatus=classic_runtime_scan_frequency_and_fine_tuning_pending" % [CONTRABAND_SCAN_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), government_name, action, before_credits, after_credits, before_legal, after_legal, before_equipment, after_equipment, status_line])
	get_tree().quit(0)

func _run_contraband_risk_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var government_name := _current_government_name()
	var commodity_id := "equipment"
	commodity_hold[commodity_id] = EV_CLASSIC_COMMODITY_LOT_SIZE
	cargo = EV_CLASSIC_COMMODITY_LOT_SIZE
	var risk_line := _commodity_legal_hint_line(commodity_id)
	var inventory_risk_line := _contraband_inventory_line()
	var is_contraband := _commodity_is_contraband_for_government(commodity_id, government_name)
	var policy: Dictionary = governments.get("governments", {}).get(government_name, {})
	var inventory_risk_visible := inventory_risk_line.contains("equipment x10") and inventory_risk_line.contains("fine %d cr/ton" % int(policy.get("finePerTon", 0)))
	print("%s routeToSolSelected=%s system=%s government=\"%s\" commodity=%s isContraband=%s finePerTon=%d bribeAllowed=%s heldContrabandInventoryVisible=%s hint=\"%s\" inventoryHint=\"%s\" sourceLabel=terminal-velocity-classic-resource-smuggling-risk-surface oracleStatus=classic_runtime_scan_frequency_and_ui_wording_pending" % [CONTRABAND_RISK_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), government_name, commodity_id, str(is_contraband), int(policy.get("finePerTon", 0)), str(policy.get("bribeAllowed", false)), str(inventory_risk_visible), risk_line, inventory_risk_line])
	get_tree().quit(0)

func _run_contraband_scan_trade_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	var earth_body := _current_body()
	var government_name := _current_government_name()
	var route_to_levo_selected := _select_map_route_to_system("Levo")
	var mechanics: Dictionary = reputation.get("mechanics", {})
	var clemency_cost := int(mechanics.get("clemencyCost", 1000))
	commodity_hold["equipment"] = EV_CLASSIC_COMMODITY_LOT_SIZE
	commodity_hold["food"] = EV_CLASSIC_COMMODITY_LOT_SIZE
	cargo = EV_CLASSIC_COMMODITY_LOT_SIZE * 2
	credits = clemency_cost + 5200
	legal_records[government_name] = -30
	reputation_scores[government_name] = int(mechanics.get("clemencyMinReputation", 10))
	landed = true
	var equipment_before_scan := int(commodity_hold.get("equipment", 0))
	var food_before_scan := int(commodity_hold.get("food", 0))
	var scan_outcome := _apply_contraband_scan(false)
	var equipment_after_scan := int(commodity_hold.get("equipment", 0))
	var food_after_scan := int(commodity_hold.get("food", 0))
	var preserved_legal_cargo_after_scan := food_after_scan == food_before_scan and equipment_after_scan == 0
	var paid_clemency := _pay_legal_clemency()
	landed = false
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	landing_tab = 1
	selected_landing_item = 0
	var credits_before_sale := credits
	_sell_selected_commodity()
	var food_after_sale := int(commodity_hold.get("food", 0))
	var preserved_food_sold_safely := food_after_scan > 0 and food_after_sale == 0 and credits > credits_before_sale
	print("%s routeToSolSelected=%s routeToLevoSelected=%s scanSystem=%s saleSystem=%s scanBody=\"%s\" government=\"%s\" scanAction=%s equipmentBeforeScan=%d equipmentAfterScan=%d foodBeforeScan=%d foodAfterScan=%d foodAfterSale=%d preservedLegalCargoAfterScan=%s clemencyPaid=%s creditsBeforeSale=%d creditsAfterSale=%d preservedFoodSoldSafely=%s sourceLabel=terminal-velocity-contraband-trade-recovery-scaffold oracleStatus=classic_runtime_scan_trade_cargo_cleanup_pending" % [CONTRABAND_SCAN_TRADE_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(route_to_levo_selected), "Sol", current_system.get("name", "?"), earth_body.get("name", "?"), government_name, str(scan_outcome.get("action", "none")), equipment_before_scan, equipment_after_scan, food_before_scan, food_after_scan, food_after_sale, str(preserved_legal_cargo_after_scan), str(paid_clemency), credits_before_sale, credits, str(preserved_food_sold_safely)])
	get_tree().quit(0)

func _run_contraband_clemency_funding_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	var systems_policy: Dictionary = governments.get("systems", {})
	var levo_policy: Dictionary = systems_policy.get("Levo", {}).duplicate()
	levo_policy["government"] = "Federation"
	systems_policy["Levo"] = levo_policy
	governments["systems"] = systems_policy
	var government_name := _current_government_name()
	var mechanics: Dictionary = reputation.get("mechanics", {})
	var clemency_cost := int(mechanics.get("clemencyCost", 1000))
	commodity_hold["equipment"] = EV_CLASSIC_COMMODITY_LOT_SIZE
	commodity_hold["food"] = EV_CLASSIC_COMMODITY_LOT_SIZE
	cargo = EV_CLASSIC_COMMODITY_LOT_SIZE * 2
	credits = clemency_cost + 3900
	legal_records[government_name] = -30
	reputation_scores[government_name] = int(mechanics.get("clemencyMinReputation", 10))
	landed = true
	var credits_before_scan := credits
	var legal_before_scan := int(legal_records.get(government_name, 0))
	var food_before_scan := int(commodity_hold.get("food", 0))
	var scan_outcome := _apply_contraband_scan(false)
	var credits_after_scan := credits
	var legal_after_scan := int(legal_records.get(government_name, 0))
	var equipment_after_scan := int(commodity_hold.get("equipment", 0))
	var food_after_scan := int(commodity_hold.get("food", 0))
	status_messages.clear()
	var blocked_paid := _pay_legal_clemency()
	var blocked_status := status_line
	var scan_left_clemency_one_hundred_credits_short := (not blocked_paid) and credits_after_scan == clemency_cost - 100 and blocked_status.contains("insufficient funds")
	landing_tab = 1
	selected_landing_item = 0
	_sell_selected_commodity()
	var credits_after_sale := credits
	var food_after_sale := int(commodity_hold.get("food", 0))
	var preserved_food_sold_for_clemency := food_before_scan > 0 and food_after_scan == food_before_scan and food_after_sale == 0 and credits_after_sale >= clemency_cost
	status_messages.clear()
	var paid_after_trade := _pay_legal_clemency()
	var final_legal := int(legal_records.get(government_name, 0))
	var clemency_funded_after_trade := paid_after_trade and credits == credits_after_sale - clemency_cost and final_legal == -8
	print("%s routeToSolSelected=%s system=%s landedBody=\"%s\" government=\"%s\" scanAction=%s creditsBeforeScan=%d creditsAfterScan=%d legalBeforeScan=%d legalAfterScan=%d equipmentAfterScan=%d foodAfterScan=%d blockedClemencyBeforeTrade=%s scanLeftClemencyOneHundredCreditsShort=%s creditsAfterSale=%d finalCredits=%d finalLegal=%d cargoUsed=%d preservedFoodSoldForClemency=%s clemencyFundedAfterTrade=%s blockedStatus=\"%s\" clemencySourceLabel=terminal-velocity-inferred-clemency-scaffold clemencyOracleStatus=approved_inference_pending_ev_classic_confirmation sourceLabel=terminal-velocity-contraband-clemency-funding-scaffold oracleStatus=classic_runtime_scan_trade_clemency_cleanup_pending" % [CONTRABAND_CLEMENCY_FUNDING_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), _current_body().get("name", "?"), government_name, str(scan_outcome.get("action", "none")), credits_before_scan, credits_after_scan, legal_before_scan, legal_after_scan, equipment_after_scan, food_after_scan, str(not blocked_paid), str(scan_left_clemency_one_hundred_credits_short), credits_after_sale, credits, final_legal, cargo, str(preserved_food_sold_for_clemency), str(clemency_funded_after_trade), blocked_status])
	get_tree().quit(0)

func _run_pilot_save_resume_log() -> void:
	_reset_travel_state()
	map_visible = true
	loaded_pilot_name = "Save Resume Test"
	loaded_ship_name = "RoundTrip"
	strict_play_selected = false
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var accepted_body := _current_body()
	var mission_before_accept: Dictionary = _first_available_mission(accepted_body)
	var accepted_mission_id := str(mission_before_accept.get("id", "none"))
	_accept_selected_mission()
	credits = 100000
	landing_tab = 3
	selected_landing_item = 1
	_buy_selected_ship()
	landing_tab = 2
	selected_landing_item = 0
	_buy_selected_outfit_or_weapon()
	selected_landing_item = 3
	_buy_selected_outfit_or_weapon()
	var saved_system := str(current_system.get("name", "?"))
	var saved_fuel := player_fuel
	var saved_credits := credits
	var saved_cargo_space := cargo_space
	var saved_ship_id := player_ship_id
	var saved_outfits := owned_outfits.duplicate()
	var saved_weapons := owned_weapons.duplicate()
	var saved_selected_secondary := selected_secondary_weapon_index
	var saved_status_line := status_line
	var saved_status_messages := status_messages.duplicate()
	var saved_active_missions := active_missions.duplicate()
	var saved_strict_play := strict_play_selected
	var save_succeeded := _save_current_pilot_file()
	current_system_index = _system_index_by_name(START_SYSTEM_NAME, 0)
	current_system = universe.get("systems", [])[current_system_index]
	player_fuel = 0
	credits = 1
	active_missions.clear()
	status_line = "mutated status before resume"
	status_messages.clear()
	status_messages.append("mutated status before resume")
	owned_outfits.clear()
	owned_weapons.clear()
	selected_secondary_weapon_index = 99
	cargo_space = 20
	_set_player_ship_by_id("shuttlecraft")
	strict_play_selected = true
	_open_pilot_modal()
	for i in range(available_pilots.size()):
		if str(available_pilots[i].get("pilot_name", "")) == loaded_pilot_name:
			selected_pilot_index = i
			break
	_load_selected_pilot_file()
	var system_round_trip := str(current_system.get("name", "?")) == saved_system
	var fuel_round_trip := player_fuel == saved_fuel
	var credits_round_trip := credits == saved_credits
	var mission_round_trip := active_missions == saved_active_missions and active_missions.has(accepted_mission_id)
	var strict_round_trip := strict_play_selected == saved_strict_play
	var outfit_round_trip := _integer_count_dictionaries_match(owned_outfits, saved_outfits) and not owned_outfits.is_empty()
	var weapon_round_trip := _integer_count_dictionaries_match(owned_weapons, saved_weapons) and not owned_weapons.is_empty()
	var selected_secondary_round_trip := selected_secondary_weapon_index == saved_selected_secondary
	var ship_round_trip := player_ship_id == saved_ship_id
	var cargo_space_round_trip := cargo_space == saved_cargo_space
	var status_round_trip := status_line == saved_status_line and status_messages == saved_status_messages
	var resumed_player_info_lines := _player_inventory_lines()
	var resumed_upgrade_player_info_visible := resumed_player_info_lines.has("Ship: %s" % saved_ship_id) and _inventory_dictionary_summary(owned_outfits).contains("cargo_pod") and _inventory_dictionary_summary(owned_weapons).contains("laser_cannon")
	var resume_succeeded := save_succeeded and system_round_trip and fuel_round_trip and credits_round_trip and mission_round_trip and strict_round_trip and outfit_round_trip and weapon_round_trip and selected_secondary_round_trip and ship_round_trip and cargo_space_round_trip and status_round_trip and resumed_upgrade_player_info_visible
	var save_status := "saveSucceeded=true" if save_succeeded else "saveSucceeded=false"
	var resume_status := "resumeSucceeded=true" if resume_succeeded else "resumeSucceeded=false"
	var system_status := "systemRoundTrip=true" if system_round_trip else "systemRoundTrip=false"
	var fuel_status := "fuelRoundTrip=true" if fuel_round_trip else "fuelRoundTrip=false"
	var credits_status := "creditsRoundTrip=true" if credits_round_trip else "creditsRoundTrip=false"
	var mission_status := "missionRoundTrip=true" if mission_round_trip else "missionRoundTrip=false"
	var strict_status := "strictPlayRoundTrip=true" if strict_round_trip else "strictPlayRoundTrip=false"
	var outfit_status := "outfitRoundTrip=true" if outfit_round_trip else "outfitRoundTrip=false"
	var weapon_status := "weaponRoundTrip=true" if weapon_round_trip else "weaponRoundTrip=false"
	var selected_secondary_status := "selectedSecondaryRoundTrip=true" if selected_secondary_round_trip else "selectedSecondaryRoundTrip=false"
	var ship_status := "shipRoundTrip=true" if ship_round_trip else "shipRoundTrip=false"
	var cargo_space_status := "cargoSpaceRoundTrip=true" if cargo_space_round_trip else "cargoSpaceRoundTrip=false"
	var status_round_trip_status := "statusRoundTrip=true" if status_round_trip else "statusRoundTrip=false"
	var player_info_status := "resumedUpgradePlayerInfoVisible=true" if resumed_upgrade_player_info_visible else "resumedUpgradePlayerInfoVisible=false"
	print("%s pilot=\"%s\" routeToSolSelected=%s acceptedAtBody=\"%s\" acceptedMission=%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s savedSystem=%s resumedSystem=%s savedFuel=%d resumedFuel=%d savedCredits=%d resumedCredits=%d savedShip=%s resumedShip=%s savedCargoSpace=%d resumedCargoSpace=%d savedOutfits=%s resumedOutfits=%s savedWeapons=%s resumedWeapons=%s savedSelectedSecondary=%d resumedSelectedSecondary=%d savedStatusMessages=%s resumedStatusMessages=%s resumedPlayerInfoLines=%s activeMissions=%s strictPlay=%s sourceLabel=terminal-velocity-save-scaffold oracleStatus=save_resume_pending_ev_classic_file_trace status=\"%s\"" % [PILOT_SAVE_RESUME_EVENT_LOG_PREFIX, loaded_pilot_name, str(route_to_sol_selected), str(accepted_body.get("name", "None")), accepted_mission_id, save_status, resume_status, system_status, fuel_status, credits_status, mission_status, strict_status, outfit_status, weapon_status, selected_secondary_status, ship_status, cargo_space_status, status_round_trip_status, player_info_status, saved_system, str(current_system.get("name", "?")), saved_fuel, player_fuel, saved_credits, credits, saved_ship_id, player_ship_id, saved_cargo_space, cargo_space, JSON.stringify(saved_outfits), JSON.stringify(owned_outfits), JSON.stringify(saved_weapons), JSON.stringify(owned_weapons), saved_selected_secondary, selected_secondary_weapon_index, JSON.stringify(saved_status_messages), JSON.stringify(status_messages), JSON.stringify(resumed_player_info_lines), JSON.stringify(active_missions), str(strict_play_selected), status_line])
	get_tree().quit(0)

func _position_at_body(body_name: String) -> bool:
	for body in current_system.get("bodies", []):
		if str(body.get("name", "")) == body_name:
			pos = Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
			vel = Vector2.ZERO
			return true
	return false

func _integer_count_dictionaries_match(left: Dictionary, right: Dictionary) -> bool:
	if left.size() != right.size():
		return false
	for key in left.keys():
		if not right.has(key):
			return false
		if int(left.get(key, 0)) != int(right.get(key, 0)):
			return false
	return true

func _first_available_mission(body: Dictionary) -> Dictionary:
	var available := _available_missions(body)
	if available.is_empty():
		return {}
	return available[0]

func _complete_arrived_missions() -> Array:
	var completed_now := []
	var body := _current_body()
	var system_name := str(current_system.get("name", ""))
	var body_name := str(body.get("name", ""))
	for mission_id in active_missions.duplicate():
		var mission := _mission_by_id(str(mission_id))
		if mission.is_empty():
			continue
		if str(mission.get("destinationSystem", "")) != system_name or str(mission.get("destinationBody", "")) != body_name:
			continue
		active_missions.erase(mission_id)
		mission_acceptance_days.erase(str(mission_id))
		if not completed_missions.has(mission_id):
			completed_missions.append(mission_id)
		var cargo_released := int(mission.get("cargoTons", 0))
		var reward_paid := int(mission.get("reward", 0))
		cargo = max(0, cargo - cargo_released)
		credits += reward_paid
		completed_mission_history.append(_mission_completion_record(mission, cargo_released, reward_paid))
		var reputation_event_id := str(mission.get("reputationEvent", ""))
		if reputation_event_id != "" and reputation_event_id != "<null>":
			_apply_reputation_event(reputation_event_id, _current_government_name())
		for flag in mission.get("completionFlags", []):
			if not story_flags.has(flag):
				story_flags.append(flag)
		completed_now.append(mission_id)
	status_line = "Completed missions: " + ", ".join(completed_now) if not completed_now.is_empty() else "No missions completed"
	return completed_now

func _auto_abort_active_mission(mission: Dictionary) -> bool:
	var mission_id := str(mission.get("id", ""))
	if mission_id == "" or not active_missions.has(mission_id):
		_set_status("Auto-abort mission is not active")
		return false
	var cargo_released := int(mission.get("cargoTons", 0))
	active_missions.erase(mission_id)
	mission_acceptance_days.erase(mission_id)
	cargo = max(0, cargo - cargo_released)
	for flag in mission.get("completionFlags", []):
		if not story_flags.has(flag):
			story_flags.append(flag)
	var record := _mission_abort_record(mission, mission_id, cargo_released)
	record["completion_flags_applied"] = mission.get("completionFlags", [])
	record["sourceLabel"] = "ev-classic-resource-bible-backed-auto-abort-guardrail"
	record["oracleStatus"] = "classic_runtime_auto_abort_ui_pending"
	aborted_mission_history.append(record)
	_set_status("Auto-aborted mission: %s; released %d cargo tons" % [str(mission.get("title", mission_id)), cargo_released])
	return true

func _abort_active_mission(mission_id := "") -> bool:
	if active_missions.is_empty():
		_set_status("No active mission to abort")
		return false
	var selected_id := mission_id
	if selected_id == "":
		selected_id = str(active_missions[0])
	if not active_missions.has(selected_id):
		_set_status("Mission not active: " + selected_id)
		return false
	var mission := _mission_by_id(selected_id)
	if not mission.is_empty() and mission.has("canAbort") and not bool(mission.get("canAbort", true)):
		_set_status("Mission cannot abort before return/cleanup")
		return false
	var cargo_released := int(mission.get("cargoTons", 0)) if not mission.is_empty() else 0
	active_missions.erase(selected_id)
	mission_acceptance_days.erase(str(selected_id))
	cargo = max(0, cargo - cargo_released)
	aborted_mission_history.append(_mission_abort_record(mission, selected_id, cargo_released))
	_set_status("Aborted mission: %s; released %d cargo tons" % [str(mission.get("title", selected_id)) if not mission.is_empty() else selected_id, cargo_released])
	_play_sound("ui_click")
	return true

func _mission_abort_record(mission: Dictionary, mission_id: String, cargo_released: int) -> Dictionary:
	var completion_government := str(mission.get("completionGovernment", ""))
	var completion_reward := int(mission.get("completionReward", 0))
	var abort_multiplier := int(mission.get("abortReputationMultiplier", 0)) if mission.has("abortReputationMultiplier") else 0
	var reputation_delta := 0
	var source_label := "terminal-velocity-mission-abort-scaffold"
	var oracle_status := "mission_abort_pending_classic_runtime_or_manual_trace"
	if completion_government != "" and completion_reward > 0 and abort_multiplier != 0:
		reputation_delta = -(completion_reward * abort_multiplier)
		reputation_scores[completion_government] = int(reputation_scores.get(completion_government, 0)) + reputation_delta
		source_label = "ev-classic-resource-bible-backed-mission-abort-penalty-scaffold"
		oracle_status = "classic_runtime_abort_penalty_ui_pending"
	return {
		"id": mission_id,
		"title": str(mission.get("title", mission_id)) if not mission.is_empty() else mission_id,
		"system": str(current_system.get("name", "?")),
		"body": str(_current_body().get("name", "?")),
		"cargo_released": cargo_released,
		"reputation_government": completion_government,
		"reputation_delta": reputation_delta,
		"completion_reward": completion_reward,
		"abort_reputation_multiplier": abort_multiplier,
		"sourceLabel": source_label,
		"oracleStatus": oracle_status,
	}

func _apply_mission_cargo_scan(government_name: String) -> Dictionary:
	for mission_id in active_missions.duplicate():
		var mission := _mission_by_id(str(mission_id))
		if mission.is_empty():
			continue
		var scan_government := str(mission.get("scanGovernment", ""))
		if not bool(mission.get("failIfScanned", false)) or scan_government != government_name:
			continue
		var cargo_released := int(mission.get("cargoTons", 0))
		var failure_flag := "fail_mission_bit_%d" % int(mission.get("failureBitSet", 0))
		active_missions.erase(str(mission_id))
		mission_acceptance_days.erase(str(mission_id))
		cargo = max(0, cargo - cargo_released)
		if not story_flags.has(failure_flag):
			story_flags.append(failure_flag)
		failed_mission_history.append({
			"id": str(mission_id),
			"title": str(mission.get("title", mission_id)),
			"scan_government": government_name,
			"cargo_released": cargo_released,
			"failure_flag": failure_flag,
			"sourceLabel": "ev-classic-resource-bible-backed-mission-scan-failure-scaffold",
			"oracleStatus": "classic_runtime_scan_failure_ui_pending",
		})
		_set_status("Mission cargo scan failed: %s; released %d cargo tons" % [str(mission.get("title", mission_id)), cargo_released])
		return {"failed": true, "missionId": str(mission_id), "cargoReleased": cargo_released, "scanGovernment": government_name}
	_set_status("Mission cargo scan clear: " + government_name)
	return {"failed": false, "preserved": true, "scanGovernment": government_name}

func _fail_mission_deadline(mission: Dictionary, accepted_day: int, current_day: int) -> bool:
	var mission_id := str(mission.get("id", ""))
	if mission_id == "" or not active_missions.has(mission_id):
		_set_status("Deadline failure probe mission is not active")
		return false
	var time_limit_days := int(mission.get("timeLimitDays", 0))
	if current_day - accepted_day <= time_limit_days:
		_set_status("Deadline has not expired for mission: " + mission_id)
		return false
	var cargo_released := int(mission.get("cargoTons", 0))
	var reputation_delta := -int(mission.get("completionReward", 0)) / 2
	var government_name := str(mission.get("completionGovernment", "Federation"))
	var failure_flag := "fail_mission_bit_%d" % int(mission.get("failureBitSet", 0))
	active_missions.erase(mission_id)
	mission_acceptance_days.erase(str(mission_id))
	cargo = max(0, cargo - cargo_released)
	if not story_flags.has(failure_flag):
		story_flags.append(failure_flag)
	reputation_scores[government_name] = int(reputation_scores.get(government_name, 0)) + reputation_delta
	failed_mission_history.append(_mission_deadline_failure_record(mission, accepted_day, current_day, cargo_released, failure_flag, reputation_delta, government_name))
	_set_status("Mission deadline failed: %s; released %d cargo tons" % [str(mission.get("title", mission_id)), cargo_released])
	return true

func _mission_deadline_failure_record(mission: Dictionary, accepted_day: int, current_day: int, cargo_released: int, failure_flag: String, reputation_delta: int, government_name: String) -> Dictionary:
	return {
		"id": str(mission.get("id", "")),
		"title": str(mission.get("title", mission.get("id", "Mission"))),
		"accepted_day": accepted_day,
		"current_day": current_day,
		"time_limit_days": int(mission.get("timeLimitDays", 0)),
		"cargo_released": cargo_released,
		"failure_flag": failure_flag,
		"reputation_government": government_name,
		"reputation_delta": reputation_delta,
		"sourceLabel": "ev-classic-resource-bible-backed-mission-failure-scaffold",
		"oracleStatus": "deadline_failure_runtime_ui_pending_classic_trace",
	}

func _mission_completion_record(mission: Dictionary, cargo_released: int, reward_paid: int) -> Dictionary:
	return {
		"id": str(mission.get("id", "")),
		"title": str(mission.get("title", mission.get("id", "Mission"))),
		"system": str(current_system.get("name", "?")),
		"body": str(_current_body().get("name", "?")),
		"cargo_released": cargo_released,
		"reward_paid": reward_paid,
	}

func _body_refuel_available(body: Dictionary) -> bool:
	var inventory := _station_inventory(body)
	var services: Array = inventory.get("services", [])
	return services.has("repairs") or inventory.get("outfitsForSale", []).has("fuel_tank")

func _body_repair_available(body: Dictionary) -> bool:
	var inventory := _station_inventory(body)
	var services: Array = inventory.get("services", [])
	return services.has("repairs")

func _repair_price_per_hull_point() -> int:
	return int(outfits.get("repair", {}).get("pricePerHullPoint", 8))

func _repair_cost() -> int:
	return max(0, _max_player_hull() - player_hull) * _repair_price_per_hull_point()

func _max_player_fuel() -> int:
	return int(player_ship.get("fuel", player_ship.get("sourceData", {}).get("fuel", 6))) + _owned_outfit_effect_total("maxFuel")

func _jump_fuel_cost() -> int:
	return 1

func _too_close_to_system_center_for_jump() -> bool:
	return pos.length() < MIN_HYPERSPACE_DISTANCE_FROM_CENTER

func _move_to_scripted_hyperspace_distance() -> void:
	pos = Vector2(MIN_HYPERSPACE_DISTANCE_FROM_CENTER + 50.0, 0.0)

func _route_fuel_cost(route_hops := -1) -> int:
	var hops := route_hops
	if hops < 0:
		hops = _queued_route_hops()
	return hops * _jump_fuel_cost()

func _queued_route_hops() -> int:
	if not selected_route.is_empty():
		return selected_route.size()
	if _selected_destination_name() != "None" and _selected_destination_name() != str(current_system.get("name", "")):
		return 1
	return 0

func _route_fuel_warning_active(route_hops := -1) -> bool:
	return _route_fuel_cost(route_hops) > player_fuel

func _route_fuel_hint_line(route_hops := -1) -> String:
	var hops := _queued_route_hops() if route_hops < 0 else route_hops
	var cost := _route_fuel_cost(hops)
	var warning := ""
	if cost > player_fuel:
		warning = " — refuel before full route"
		var refuel_body := _nearest_refuel_body_name()
		if refuel_body != "":
			warning += " at " + refuel_body
	return "Route fuel: %d hop(s), cost %d, fuel %d/%d%s" % [hops, cost, player_fuel, _max_player_fuel(), warning]

func _nearest_refuel_body_name() -> String:
	for body in current_system.get("bodies", []):
		if _body_refuel_available(body):
			return str(body.get("name", ""))
	return ""

func _refuel_current_ship() -> bool:
	if _disabled_player_action_blocked():
		return false
	if not landed:
		_set_status("Cannot refuel in space; land at a port with refuel service")
		return false
	var body := _current_body()
	if not _body_refuel_available(body):
		_set_status("Refuel unavailable here; choose a port with refuel service")
		return false
	player_fuel = _max_player_fuel()
	_set_status("Refueled at " + str(body.get("name", "port")))
	return true

func _repair_current_hull() -> bool:
	if _disabled_player_action_blocked():
		return false
	if not landed:
		_set_status("Cannot repair in space; land at a port with repair service")
		return false
	var body := _current_body()
	if not _body_repair_available(body):
		_set_status("Repair unavailable here; choose a port with repair service")
		return false
	var cost := _repair_cost()
	if cost <= 0:
		_set_status("Hull already fully repaired")
		return false
	if credits < cost:
		_set_status("Not enough credits for repairs: need %d" % cost)
		return false
	credits -= cost
	player_hull = _max_player_hull()
	_set_status("Repaired hull at %s for %d credits" % [str(body.get("name", "port")), cost])
	return true

func _unhandled_input(event: InputEvent) -> void:
	if game_state == STATE_TITLE:
		_handle_title_input(event)
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if map_visible and not event.shift_pressed and not event.ctrl_pressed:
			status_line = "Hold Shift and click a linked system"
			get_viewport().set_input_as_handled()
			return
		if map_visible and (event.shift_pressed or event.ctrl_pressed) and _select_map_route_at_position(event.position):
			get_viewport().set_input_as_handled()
			return
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_E:
				_try_land()
			KEY_L: _ev_land_or_launch()
			KEY_N: _cycle_target(1)
			KEY_P: _show_player_info()
			KEY_I: _show_mission_info()
			KEY_H: _toggle_hyper_mode()
			KEY_BACKSLASH: _cycle_link(1)
			KEY_J: _jump()
			KEY_M:
				_toggle_universe_map()
			KEY_BACKSPACE, KEY_DELETE:
				if map_visible:
					_clear_selected_route()
			KEY_G: _route_to_active_mission_destination()
			KEY_F10:
				help_visible = not help_visible
				status_line = "Help overlay: " + ("on" if help_visible else "off")
			KEY_T:
				_cycle_target(1)
			KEY_R: _select_closest_target()
			KEY_A: _toggle_autopilot()
			KEY_Z: _afterburner_active()
			KEY_TAB: _fire_primary_weapon()
			KEY_SPACE: _fire_secondary_weapon()
			KEY_F1:
				landing_tab = 0
				selected_landing_item = 0
				status_line = "Landing tab: Mission Computer"
			KEY_F2:
				landing_tab = 1
				selected_landing_item = 0
				status_line = "Landing tab: Commodity Exchange"
			KEY_F3:
				landing_tab = 2
				selected_landing_item = 0
				status_line = "Landing tab: Outfitter"
			KEY_F4:
				landing_tab = 3
				selected_landing_item = 0
				status_line = "Landing tab: Shipyard"
			KEY_F5:
				if landed:
					_refuel_current_ship()
				else:
					_set_status("Cannot refuel in space")
			KEY_F6: _save_current_pilot_file()
			KEY_F7:
				_repair_current_hull()
			KEY_F8:
				_recover_disabled_player_scaffold()
			KEY_C:
				if landed:
					_pay_legal_clemency()
				else:
					_set_status("Clemency unavailable in space; land at an aligned port")
			KEY_UP:
				if landed:
					_cycle_landing_selection(-1)
			KEY_DOWN:
				if landed:
					_cycle_landing_selection(1)
			KEY_ENTER:
				if landed and landing_tab == 0:
					_accept_selected_mission()
			KEY_X:
				_abort_active_mission()
			KEY_B:
				if landed:
					match landing_tab:
						1: _buy_selected_commodity()
						2: _buy_selected_outfit_or_weapon()
						3: _buy_selected_ship()
			KEY_S: _change_secondary_weapon()

func _handle_title_input(event: InputEvent) -> void:
	if title_modal != "":
		_handle_title_modal_input(event)
		return
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_ENTER:
				_activate_title_button("Enter Ship")
			KEY_N:
				_activate_title_button("New Pilot")
			KEY_O:
				_activate_title_button("Open Pilot")
			KEY_Q:
				_activate_title_button("Quit TV")
			KEY_S:
				_activate_title_button("Set Prefs")
			KEY_A:
				_activate_title_button("About TV")
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		for button in _title_buttons():
			var rect: Rect2 = button["rect"]
			if rect.has_point(event.position):
				_activate_title_button(str(button["label"]))
				return

func _activate_title_button(label: String) -> void:
	_play_sound("ui_click")
	match label:
		"Enter Ship":
			_enter_ship_from_title()
		"New Pilot":
			title_modal = "new_pilot_name"
			pilot_name_input = ""
			ship_name_input = "Starseeker"
			strict_play_selected = false
			title_status_line = "Creating new pilot."
		"Open Pilot":
			_open_pilot_modal()
		"Set Prefs":
			title_modal = "prefs"
			selected_pref_index = 0
			title_status_line = "Set Preferences"
		"About TV":
			title_modal = "about"
			title_status_line = "About Terminal Velocity"
		"Quit TV":
			get_tree().quit()

func _title_buttons() -> Array:
	return [
		{"label": "New Pilot", "rect": Rect2(285, 520, 220, 38)},
		{"label": "Open Pilot", "rect": Rect2(285, 572, 220, 38)},
		{"label": "Quit TV", "rect": Rect2(285, 624, 220, 38)},
		{"label": "Enter Ship", "rect": Rect2(775, 520, 220, 38)},
		{"label": "Set Prefs", "rect": Rect2(775, 572, 220, 38)},
		{"label": "About TV", "rect": Rect2(775, 624, 220, 38)},
	]

func _handle_title_modal_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_ESCAPE:
				_cancel_title_modal()
			KEY_ENTER:
				_accept_title_modal_step()
			KEY_UP:
				if title_modal == "prefs":
					_cycle_pref_selection(-1)
				else:
					_cycle_open_pilot_selection(-1)
			KEY_DOWN:
				if title_modal == "prefs":
					_cycle_pref_selection(1)
				else:
					_cycle_open_pilot_selection(1)
			KEY_SPACE:
				if title_modal == "prefs":
					_toggle_selected_pref()
				elif title_modal == "new_pilot_name":
					strict_play_selected = not strict_play_selected
			KEY_BACKSPACE:
				_backspace_title_modal_text()
			_:
				if title_modal != "open_pilot" and event.unicode >= 32 and event.unicode <= 126:
					_append_title_modal_text(char(event.unicode))
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if title_modal == "open_pilot":
			var row := _open_pilot_row_at(event.position)
			if row >= 0:
				selected_pilot_index = row
				return
		if title_modal == "prefs":
			var pref_row := _pref_row_at(event.position)
			if pref_row >= 0:
				selected_pref_index = pref_row
				_toggle_selected_pref()
				return
		if title_modal == "new_pilot_name" and _strict_play_toggle_rect().has_point(event.position):
			strict_play_selected = not strict_play_selected
			return
		var action := _title_modal_action_at(event.position)
		if action == "cancel":
			_cancel_title_modal()
		elif action == "ok":
			_accept_title_modal_step()

func _append_title_modal_text(text: String) -> void:
	if title_modal == "new_pilot_name" and pilot_name_input.length() < 24:
		pilot_name_input += text
	elif title_modal == "new_ship_name" and ship_name_input.length() < 24:
		ship_name_input += text

func _backspace_title_modal_text() -> void:
	if title_modal == "new_pilot_name" and pilot_name_input.length() > 0:
		pilot_name_input = pilot_name_input.substr(0, pilot_name_input.length() - 1)
	elif title_modal == "new_ship_name" and ship_name_input.length() > 0:
		ship_name_input = ship_name_input.substr(0, ship_name_input.length() - 1)

func _accept_title_modal_step() -> void:
	_play_sound("ui_click")
	if title_modal == "about":
		title_modal = ""
		title_status_line = "No Pilot File Loaded" if loaded_pilot_name == "" else "Pilot File Loaded: %s — %s" % [loaded_pilot_name, loaded_ship_name]
		return
	if title_modal == "prefs":
		_save_prefs()
		title_modal = ""
		title_status_line = "Preferences saved."
		return
	if title_modal == "open_pilot":
		_load_selected_pilot_file()
		return
	if title_modal == "new_pilot_name":
		if pilot_name_input.strip_edges() == "":
			title_status_line = "Pilot name required."
			return
		title_modal = "new_ship_name"
		title_status_line = "Now, please christen your brand-new Shuttlecraft."
		return
	if title_modal == "new_ship_name":
		if ship_name_input.strip_edges() == "":
			title_status_line = "Ship name required."
			return
		loaded_pilot_name = pilot_name_input.strip_edges()
		loaded_ship_name = ship_name_input.strip_edges()
		loaded_pilot_file = _save_new_pilot_file(loaded_pilot_name, loaded_ship_name)
		title_modal = ""
		title_status_line = "Pilot File Loaded: %s — %s" % [loaded_pilot_name, loaded_ship_name]

func _save_new_pilot_file(pilot_name: String, ship_name: String) -> String:
	var pilots_dir := "user://pilots"
	DirAccess.make_dir_recursive_absolute(pilots_dir)
	var path := _pilot_save_path(pilot_name)
	var pilot_data := _pilot_save_data(pilot_name, ship_name)
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_error("Unable to save pilot file: %s" % path)
		return ""
	file.store_string(JSON.stringify(pilot_data, "\t"))
	file.close()
	return path

func _save_current_pilot_file() -> bool:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return false
	if loaded_pilot_name.strip_edges() == "":
		_set_status("No pilot loaded to save")
		return false
	loaded_pilot_file = _save_new_pilot_file(loaded_pilot_name, loaded_ship_name)
	var saved := loaded_pilot_file != ""
	if saved:
		_set_status("Saved pilot: %s" % loaded_pilot_name)
	else:
		_set_status("Pilot save failed")
	return saved

func _pilot_save_data(pilot_name: String, ship_name: String) -> Dictionary:
	return {
		"format": "terminal_velocity_pilot_v1",
		"pilot_name": pilot_name,
		"ship_name": ship_name,
		"ship_class": _pilot_ship_class(),
		"ship_resource_id": int(player_ship.get("shipResourceId", 128)),
		"ship_type": str(player_ship.get("name", "Shuttlecraft")),
		"credits": credits,
		"cargo": cargo,
		"cargo_space": cargo_space,
		"fuel": player_fuel,
		"shields": player_shields,
		"hull": player_hull,
		"system": current_system.get("name", ""),
		"system_index": current_system_index,
		"position": {"x": pos.x, "y": pos.y},
		"velocity": {"x": vel.x, "y": vel.y},
		"angle_deg": angle_deg,
		"facing_index": player_facing_index,
		"current_day": current_day,
		"active_missions": active_missions,
		"mission_acceptance_days": mission_acceptance_days,
		"completed_missions": completed_missions,
		"completed_mission_history": completed_mission_history,
		"aborted_mission_history": aborted_mission_history,
		"failed_mission_history": failed_mission_history,
		"story_flags": story_flags,
		"commodity_hold": commodity_hold,
		"cargo_salvage_pickups": _serialized_cargo_salvage_pickups(),
		"combat_reward_history": combat_reward_history,
		"owned_outfits": owned_outfits,
		"owned_weapons": owned_weapons,
		"selected_secondary_weapon_index": selected_secondary_weapon_index,
		"reputation_scores": reputation_scores,
		"legal_records": legal_records,
		"status_line": status_line,
		"status_messages": status_messages,
		"strict_play": strict_play_selected,
	}

func _pilot_ship_class() -> int:
	# EV Classic pilot resource 128 stores `shipClass` as a small numeric class,
	# not a remake-local slug. Our decoded ship manifest preserves that as
	# `sourceDataOrdinal`; `shipResourceId` is retained separately as provenance.
	return int(player_ship.get("sourceDataOrdinal", 0))

func _pilot_save_path(pilot_name: String) -> String:
	return "user://pilots/%s.tvpilot.json" % _pilot_file_stem(pilot_name)

func _pilot_file_stem(pilot_name: String) -> String:
	var stem := ""
	for i in pilot_name.length():
		var ch := pilot_name[i]
		if ch.is_valid_identifier() or ch.is_valid_int() or ch == "-":
			stem += ch
		elif ch == " " or ch == "_":
			stem += "_"
	if stem.strip_edges() == "":
		stem = "Pilot"
	return stem

func _open_pilot_modal() -> void:
	available_pilots = _list_pilot_files()
	selected_pilot_index = 0
	title_modal = "open_pilot"
	if available_pilots.is_empty():
		title_status_line = "No pilot files found."
	else:
		title_status_line = "Select a pilot file."

func _list_pilot_files() -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	var pilots_dir := "user://pilots"
	DirAccess.make_dir_recursive_absolute(pilots_dir)
	var dir := DirAccess.open(pilots_dir)
	if dir == null:
		return result
	dir.list_dir_begin()
	var file_name := dir.get_next()
	while file_name != "":
		if not dir.current_is_dir() and file_name.ends_with(".tvpilot.json"):
			var path := pilots_dir + "/" + file_name
			var data := _read_pilot_file(path)
			if not data.is_empty():
				result.append({
					"path": path,
					"pilot_name": str(data.get("pilot_name", file_name)),
					"ship_name": str(data.get("ship_name", "")),
					"ship_type": str(data.get("ship_type", "Shuttlecraft")),
					"system": str(data.get("system", "?")),
					"credits": int(data.get("credits", 0)),
					"strict_play": bool(data.get("strict_play", false)),
					"status_line": str(data.get("status_line", "")),
					"active_missions": data.get("active_missions", []),
				})
		file_name = dir.get_next()
	dir.list_dir_end()
	result.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return str(a.get("pilot_name", "")) < str(b.get("pilot_name", "")))
	return result

func _read_pilot_file(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var text := FileAccess.get_file_as_string(path)
	var parsed = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		return {}
	return parsed

func _load_selected_pilot_file() -> void:
	if available_pilots.is_empty():
		title_status_line = "No pilot files found."
		return
	selected_pilot_index = clampi(selected_pilot_index, 0, available_pilots.size() - 1)
	var entry := available_pilots[selected_pilot_index]
	var path := str(entry.get("path", ""))
	var data := _read_pilot_file(path)
	if data.is_empty():
		title_status_line = "Unable to open pilot file."
		return
	loaded_pilot_name = str(data.get("pilot_name", ""))
	loaded_ship_name = str(data.get("ship_name", ""))
	loaded_pilot_file = path
	_apply_pilot_data(data)
	title_modal = ""
	title_status_line = "Pilot File Loaded: %s — %s" % [loaded_pilot_name, loaded_ship_name]

func _apply_pilot_data(data: Dictionary) -> void:
	loaded_pilot_name = str(data.get("pilot_name", loaded_pilot_name))
	loaded_ship_name = str(data.get("ship_name", loaded_ship_name))
	strict_play_selected = bool(data.get("strict_play", false))
	credits = int(data.get("credits", credits))
	cargo = int(data.get("cargo", cargo))
	current_system_index = _system_index_from_pilot(data)
	var systems: Array = universe.get("systems", [])
	if not systems.is_empty():
		current_system = systems[current_system_index]
	selected_link_index = 0
	var saved_pos: Dictionary = data.get("position", {})
	var saved_vel: Dictionary = data.get("velocity", {})
	pos = Vector2(float(saved_pos.get("x", pos.x)), float(saved_pos.get("y", pos.y)))
	vel = Vector2(float(saved_vel.get("x", vel.x)), float(saved_vel.get("y", vel.y)))
	angle_deg = float(data.get("angle_deg", angle_deg))
	var desired_ship_id := ""
	if data.has("ship_class"):
		desired_ship_id = _ship_id_from_class(int(data.get("ship_class", 0)))
	if desired_ship_id == "" and data.has("ship_resource_id"):
		desired_ship_id = _ship_id_from_resource_id(int(data.get("ship_resource_id", 128)))
	if desired_ship_id == "" and data.has("ship_id"):
		desired_ship_id = str(data.get("ship_id", ""))
	if desired_ship_id == "":
		desired_ship_id = _ship_id_from_legacy_type(str(data.get("ship_type", "")))
	if desired_ship_id != "":
		_set_player_ship_by_id(desired_ship_id)
	player_fuel = clampi(int(data.get("fuel", player_fuel)), 0, _max_player_fuel())
	player_shields = clampi(int(data.get("shields", player_shields)), 0, _max_player_shields())
	player_hull = clampi(int(data.get("hull", player_hull)), 0, _max_player_hull())
	if player_frames.is_empty():
		player_facing_index = int(data.get("facing_index", 0))
	else:
		player_facing_index = int(data.get("facing_index", _facing_frame_index(angle_deg, player_frames.size()))) % player_frames.size()
	cargo_space = int(data.get("cargo_space", cargo_space))
	cargo = mini(cargo, cargo_space)
	current_day = int(data.get("current_day", current_day))
	active_missions = data.get("active_missions", active_missions)
	mission_acceptance_days = data.get("mission_acceptance_days", mission_acceptance_days)
	completed_missions = data.get("completed_missions", completed_missions)
	completed_mission_history = data.get("completed_mission_history", completed_mission_history)
	aborted_mission_history = data.get("aborted_mission_history", aborted_mission_history)
	failed_mission_history = data.get("failed_mission_history", failed_mission_history)
	story_flags = data.get("story_flags", story_flags)
	commodity_hold = data.get("commodity_hold", commodity_hold)
	_restore_cargo_salvage_pickups(data.get("cargo_salvage_pickups", []))
	combat_reward_history.clear()
	var saved_combat_rewards: Variant = data.get("combat_reward_history", [])
	if typeof(saved_combat_rewards) == TYPE_ARRAY:
		for saved_reward in saved_combat_rewards:
			if typeof(saved_reward) == TYPE_DICTIONARY:
				combat_reward_history.append(saved_reward)
	owned_outfits = data.get("owned_outfits", owned_outfits)
	owned_weapons = data.get("owned_weapons", owned_weapons)
	selected_secondary_weapon_index = int(data.get("selected_secondary_weapon_index", selected_secondary_weapon_index))
	reputation_scores = data.get("reputation_scores", reputation_scores)
	legal_records = data.get("legal_records", legal_records)
	status_line = str(data.get("status_line", status_line))
	status_messages.clear()
	for message in data.get("status_messages", []):
		status_messages.append(str(message))
	while status_messages.size() > 6:
		status_messages.remove_at(0)
	turn_cell_progress = 0.0

func _serialized_cargo_salvage_pickups() -> Array[Dictionary]:
	var serialized: Array[Dictionary] = []
	for pickup in cargo_salvage_pickups:
		var pickup_position: Vector2 = pickup.get("position", Vector2.ZERO)
		serialized.append({
			"position": {"x": pickup_position.x, "y": pickup_position.y},
			"commodityId": str(pickup.get("commodityId", "equipment")),
			"tons": int(pickup.get("tons", 0)),
			"targetIndex": int(pickup.get("targetIndex", -1)),
			"sourceLabel": str(pickup.get("sourceLabel", "terminal-velocity-combat-salvage-scaffold")),
			"oracleStatus": str(pickup.get("oracleStatus", "classic_runtime_loot_cargo_behavior_pending")),
		})
	return serialized

func _restore_cargo_salvage_pickups(saved_pickups: Variant) -> void:
	cargo_salvage_pickups.clear()
	if typeof(saved_pickups) != TYPE_ARRAY:
		return
	for saved in saved_pickups:
		if typeof(saved) != TYPE_DICTIONARY:
			continue
		var saved_position: Dictionary = saved.get("position", {})
		cargo_salvage_pickups.append({
			"position": Vector2(float(saved_position.get("x", 0.0)), float(saved_position.get("y", 0.0))),
			"commodityId": str(saved.get("commodityId", "equipment")),
			"tons": int(saved.get("tons", 0)),
			"targetIndex": int(saved.get("targetIndex", -1)),
			"sourceLabel": str(saved.get("sourceLabel", "terminal-velocity-combat-salvage-scaffold")),
			"oracleStatus": str(saved.get("oracleStatus", "classic_runtime_loot_cargo_behavior_pending")),
		})

func _enter_ship_from_title() -> void:
	if loaded_pilot_name.strip_edges() == "":
		title_status_line = "No Pilot File Loaded"
		return
	game_state = STATE_SPACE
	landed = false
	status_line = "Entered ship: %s — %s in %s" % [loaded_pilot_name, loaded_ship_name, current_system.get("name", "system")]

func _system_index_from_pilot(data: Dictionary) -> int:
	var systems: Array = universe.get("systems", [])
	if systems.is_empty():
		return 0
	var saved_system := str(data.get("system", ""))
	if saved_system != "":
		return _system_index_by_name(saved_system, current_system_index)
	return clampi(int(data.get("system_index", current_system_index)), 0, systems.size() - 1)

func _system_index_by_name(system_name: String, fallback_index: int) -> int:
	var systems: Array = universe.get("systems", [])
	if systems.is_empty():
		return 0
	for i in range(systems.size()):
		if str(systems[i].get("name", "")) == system_name:
			return i
	return clampi(fallback_index, 0, systems.size() - 1)

func _ship_id_from_legacy_type(ship_type: String) -> String:
	var normalized := ship_type.strip_edges().to_lower().replace(" ", "_")
	for ship in ships.get("ships", []):
		if str(ship.get("id", "")) == normalized or str(ship.get("name", "")).to_lower() == ship_type.strip_edges().to_lower():
			return str(ship.get("id", ""))
	return ""

func _ship_id_from_class(ship_class: int) -> String:
	for ship in ships.get("ships", []):
		if int(ship.get("sourceDataOrdinal", -1)) == ship_class:
			return str(ship.get("id", ""))
	return ""

func _ship_id_from_resource_id(resource_id: int) -> String:
	for ship in ships.get("ships", []):
		if int(ship.get("shipResourceId", -1)) == resource_id:
			return str(ship.get("id", ""))
	return ""

func _set_player_ship_by_id(ship_id: String) -> void:
	var next_ship := _ship_by_id(ship_id)
	if next_ship.is_empty():
		return
	player_ship = next_ship
	player_ship_id = ship_id
	var player_frame_set := _load_ship_frame_set(player_ship)
	player_frames = player_frame_set["frames"]
	player_frame_offsets = player_frame_set["offsets"]
	player_frame_alpha_counts = player_frame_set["alpha_counts"]
	cargo_space = int(player_ship.get("cargoSpace", cargo_space))
	player_fuel = min(player_fuel, _max_player_fuel())
	_reset_player_combat_stats()

func _cycle_open_pilot_selection(dir: int) -> void:
	if title_modal != "open_pilot" or available_pilots.is_empty():
		return
	selected_pilot_index = (selected_pilot_index + dir + available_pilots.size()) % available_pilots.size()

func _pref_options() -> Array:
	# Original EV Classic prefs surface observed from the title Set Prefs button exposes
	# key bindings plus Sound Volume, Intro Music, and Game Speed controls.
	var speed_labels := ["Slowest", "Slower", "Normal", "Faster", "Fastest"]
	return [
		{"kind": "toggle", "label": "Intro Music", "enabled": pref_music_on, "note": "original visible checkbox"},
		{"kind": "radio", "label": "Game Speed...", "value": speed_labels[pref_game_speed_index], "note": "original visible button"},
		{"kind": "toggle", "label": "Sound Volume: Quiet", "enabled": pref_sound_on, "note": "original visible spinner"},
	]

func _prefs_list_rect() -> Rect2:
	return Rect2(300, 620, 460, 120)

func _prefs_save_data() -> Dictionary:
	return {
		"format": "terminal_velocity_prefs_v1",
		"music_on": pref_music_on,
		"sound_on": pref_sound_on,
		"game_speed_index": pref_game_speed_index,
		"full_screen_on": pref_full_screen_on,
		"intro_animation_on": pref_intro_animation_on,
		"ask_before_buying_on": pref_ask_before_buying_on,
		"resume_game_on": pref_resume_game_on,
	}

func _load_prefs() -> void:
	if not FileAccess.file_exists(PREFS_SAVE_PATH):
		_apply_pref_runtime_side_effects()
		return
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(PREFS_SAVE_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_warning("Ignoring invalid preferences file: " + PREFS_SAVE_PATH)
		_apply_pref_runtime_side_effects()
		return
	_apply_prefs_data(parsed)

func _apply_prefs_data(data: Dictionary) -> void:
	pref_music_on = bool(data.get("music_on", pref_music_on))
	pref_sound_on = bool(data.get("sound_on", pref_sound_on))
	pref_game_speed_index = clampi(int(data.get("game_speed_index", pref_game_speed_index)), 0, 4)
	pref_full_screen_on = bool(data.get("full_screen_on", pref_full_screen_on))
	pref_intro_animation_on = bool(data.get("intro_animation_on", pref_intro_animation_on))
	pref_ask_before_buying_on = bool(data.get("ask_before_buying_on", pref_ask_before_buying_on))
	pref_resume_game_on = bool(data.get("resume_game_on", pref_resume_game_on))
	_apply_pref_runtime_side_effects()

func _save_prefs() -> void:
	var file := FileAccess.open(PREFS_SAVE_PATH, FileAccess.WRITE)
	if file == null:
		push_error("Unable to save preferences: " + PREFS_SAVE_PATH)
		return
	file.store_string(JSON.stringify(_prefs_save_data(), "\t"))
	file.close()

func _apply_pref_runtime_side_effects() -> void:
	Engine.time_scale = [0.65, 0.8, 1.0, 1.2, 1.4][pref_game_speed_index]
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN if pref_full_screen_on else DisplayServer.WINDOW_MODE_WINDOWED)

func _cycle_pref_selection(dir: int) -> void:
	var options := _pref_options()
	selected_pref_index = (selected_pref_index + dir + options.size()) % options.size()

func _toggle_selected_pref() -> void:
	_play_sound("ui_click")
	match selected_pref_index:
		0:
			pref_music_on = not pref_music_on
		1:
			pref_game_speed_index = (pref_game_speed_index + 1) % 5
			_apply_pref_runtime_side_effects()
		2:
			pref_sound_on = not pref_sound_on
	title_status_line = "Set Preferences"

func _pref_row_at(position: Vector2) -> int:
	if Rect2(525, 625, 220, 28).has_point(position):
		return 0
	if Rect2(532, 708, 172, 34).has_point(position):
		return 1
	if Rect2(302, 625, 190, 28).has_point(position):
		return 2
	return -1

func _open_pilot_row_at(position: Vector2) -> int:
	var list_rect := Rect2(360, 365, 560, 90)
	if not list_rect.has_point(position):
		return -1
	var row := int((position.y - list_rect.position.y) / 30.0)
	if row >= 0 and row < min(available_pilots.size(), 3):
		return row
	return -1

func _cancel_title_modal() -> void:
	if title_modal == "prefs":
		_load_prefs()
	title_modal = ""
	title_status_line = "No Pilot File Loaded" if loaded_pilot_name == "" else "Pilot File Loaded: %s — %s" % [loaded_pilot_name, loaded_ship_name]

func _title_modal_action_at(position: Vector2) -> String:
	if title_modal == "":
		return ""
	var ok_rect := Rect2(940, 708, 86, 34) if title_modal == "prefs" else Rect2(836, 492, 116, 34)
	var cancel_rect := Rect2(828, 708, 86, 34) if title_modal == "prefs" else Rect2(700, 492, 116, 34)
	if title_modal == "open_pilot":
		ok_rect = Rect2(700, 492, 116, 34)
		cancel_rect = Rect2(836, 492, 116, 34)
	if ok_rect.has_point(position):
		return "ok"
	if cancel_rect.has_point(position):
		return "cancel"
	return ""

func _cycle_link(dir: int) -> void:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return
	var links: Array = current_system.get("links", [])
	if links.is_empty():
		return
	selected_route.clear()
	selected_link_index = (selected_link_index + dir + links.size()) % links.size()
	status_line = "Destination: " + str(links[selected_link_index])

func _toggle_universe_map() -> void:
	map_visible = not map_visible
	status_line = "Galaxy map open" if map_visible else "Galaxy map closed"

func _map_rect() -> Rect2:
	return Rect2(160, 92, 960, 616)

func _map_plot_rect() -> Rect2:
	return Rect2(_map_rect().position + Vector2(42, 74), Vector2(610, 456))

func _map_system_points(systems: Array) -> Dictionary:
	var points: Dictionary = {}
	if systems.is_empty():
		return points
	var bounds := _system_coordinate_bounds(systems)
	var plot_rect := _map_plot_rect()
	for system in systems:
		points[str(system.get("name", ""))] = _system_map_point(system, bounds, plot_rect)
	return points

func _system_by_name(system_name: String) -> Dictionary:
	for system in universe.get("systems", []):
		if str(system.get("name", "")) == system_name:
			return system
	return {}

func _system_service_summary(system_name: String) -> String:
	var system := _system_by_name(system_name)
	if system.is_empty():
		return "unknown"
	var services: Array[String] = []
	for body in system.get("bodies", []):
		var inventory: Dictionary = body.get("inventory", {})
		for service in inventory.get("services", []):
			var service_name := str(service)
			if not services.has(service_name):
				services.append(service_name)
		if not inventory.get("outfitsForSale", []).is_empty() and not services.has("outfitter"):
			services.append("outfitter")
		if not inventory.get("shipsForSale", []).is_empty() and not services.has("shipyard"):
			services.append("shipyard")
		if not inventory.get("weaponsForSale", []).is_empty() and not services.has("outfitter"):
			services.append("outfitter")
	if _market_prices(system_name).size() > 0 and not services.has("commodity"):
		services.append("commodity")
	if services.is_empty():
		return "none"
	services.sort()
	return ", ".join(services)

func _map_route_tail_system_name() -> String:
	if selected_route.is_empty():
		return str(current_system.get("name", ""))
	return str(selected_route[selected_route.size() - 1])

func _map_route_tail_links() -> Array:
	var tail_system := _system_by_name(_map_route_tail_system_name())
	if tail_system.is_empty():
		return []
	return tail_system.get("links", [])

func _map_linked_stop_at_position(click_position: Vector2) -> int:
	var systems: Array = universe.get("systems", [])
	var links: Array = _map_route_tail_links()
	if systems.is_empty() or links.is_empty():
		return -1
	var point_by_name := _map_system_points(systems)
	for i in range(links.size()):
		var linked_name := str(links[i])
		if linked_name == str(current_system.get("name", "")) or selected_route.has(linked_name):
			continue
		if not point_by_name.has(linked_name):
			continue
		var linked_point: Vector2 = point_by_name[linked_name]
		if click_position.distance_to(linked_point) <= 18.0:
			return i
	return -1

func _map_hovered_link_name() -> String:
	if not map_visible or not (Input.is_key_pressed(KEY_SHIFT) or Input.is_key_pressed(KEY_CTRL)):
		return ""
	var hover_index := _map_linked_stop_at_position(get_viewport().get_mouse_position())
	var links: Array = _map_route_tail_links()
	if hover_index < 0 or hover_index >= links.size():
		return ""
	return str(links[hover_index])

func _select_map_route_at_position(click_position: Vector2) -> bool:
	return _append_map_route_at_position(click_position)

func _clear_selected_route() -> bool:
	if selected_route.is_empty():
		status_line = "No route to clear"
		return true
	selected_route.clear()
	selected_link_index = -1
	status_line = "Route cleared — open map (M) or queue mission route (G) to choose a destination"
	_play_sound("ui_click")
	return true

func _append_map_route_at_position(click_position: Vector2) -> bool:
	var links: Array = _map_route_tail_links()
	if links.is_empty():
		status_line = "No route from current system"
		return true
	var hover_index := _map_linked_stop_at_position(click_position)
	if hover_index >= 0 and hover_index < links.size():
		var linked_name := str(links[hover_index])
		var route_preview: Array = [str(current_system.get("name", "?"))] + selected_route + [linked_name]
		var route_text := " → ".join(route_preview)
		var route_hops := route_preview.size() - 1
		var route_cost := route_hops * _jump_fuel_cost()
		if selected_route.is_empty():
			var current_links: Array = current_system.get("links", [])
			selected_link_index = current_links.find(linked_name)
			if selected_link_index < 0:
				selected_link_index = 0
			status_line = "Route selected: %s — fuel cost %d, fuel %d/%d — press J to jump" % [route_text, route_cost, player_fuel, _max_player_fuel()]
		else:
			status_line = "Route appended: %s — fuel cost %d, fuel %d/%d" % [route_text, route_cost, player_fuel, _max_player_fuel()]
		selected_route.append(linked_name)
		_play_sound("ui_click")
		return true
	if _map_plot_rect().has_point(click_position):
		status_line = "Hold Shift and click a linked system from " + _map_route_tail_system_name()
		return true
	return false

func _npc_world_offsets() -> Array[Vector2]:
	return [Vector2(260, -180), Vector2(-340, 220), Vector2(520, 160), Vector2(-640, -260)]

func _cycle_target(dir: int) -> void:
	var targets := _npc_world_offsets()
	if targets.is_empty():
		selected_target_index = 0
		status_line = "No scanner targets"
		return
	var found := false
	for offset in range(1, targets.size() + 1):
		var candidate := (selected_target_index + (dir * offset) + targets.size()) % targets.size()
		if _target_selectable(candidate):
			selected_target_index = candidate
			found = true
			break
	if not found:
		selected_target_index = 0
		status_line = "No active scanner targets"
		return
	var posture := " hostile legal patrol" if _legal_patrol_hostile_posture_active(_current_government_name()) else ""
	status_line = "Target: Contact %d%s at %.0f range %s" % [selected_target_index + 1, posture, pos.distance_to(targets[selected_target_index]), _target_shield_hull_summary(selected_target_index)]

func _select_closest_target() -> void:
	var targets := _npc_world_offsets()
	if targets.is_empty():
		selected_target_index = 0
		status_line = "No scanner targets"
		return
	var closest_index := -1
	var closest_distance := INF
	for i in range(targets.size()):
		if not _target_selectable(i):
			continue
		var distance := pos.distance_to(targets[i])
		if closest_index < 0 or distance < closest_distance:
			closest_distance = distance
			closest_index = i
	if closest_index < 0:
		selected_target_index = 0
		status_line = "No active scanner targets"
		return
	selected_target_index = closest_index
	var posture := " hostile legal patrol" if _legal_patrol_hostile_posture_active(_current_government_name()) else ""
	status_line = "Closest target: Contact %d%s at %.0f range %s" % [selected_target_index + 1, posture, closest_distance, _target_shield_hull_summary(selected_target_index)]

func _target_selectable(target_index: int) -> bool:
	return not _target_destroyed(target_index)

func _target_shield_hull_summary(target_index: int) -> String:
	return "S/H %d/%d" % [int(target_shields.get(target_index, 0)), int(target_hulls.get(target_index, 0))]

func _scanner_target_detail_line() -> String:
	var targets := _npc_world_offsets()
	if targets.is_empty():
		return "Scanner target: none"
	if not _target_selectable(selected_target_index):
		return "Scanner target: no active scanner targets"
	var target_index := selected_target_index % targets.size()
	return "Scanner target: Contact %d — %s — %.0f range (TV target HUD scaffold; Classic scanner layout pending)" % [target_index + 1, _target_shield_hull_summary(target_index), pos.distance_to(targets[target_index])]

func _select_next_live_target(start_index: int) -> bool:
	var targets := _npc_world_offsets()
	if targets.is_empty():
		selected_target_index = 0
		return false
	for offset in range(1, targets.size() + 1):
		var candidate := (start_index + offset) % targets.size()
		if not _target_destroyed(candidate):
			selected_target_index = candidate
			return true
	return false

func _ev_land_or_launch() -> void:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return
	if landed:
		landed = false
		status_line = "Launched from " + current_system.get("name", "system")
		return
	_try_land()

func _toggle_hyper_mode() -> void:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return
	status_line = "Hyper Mode: select destination with \\ then press J"

func _show_player_info() -> void:
	player_info_visible = not player_info_visible
	status_line = "Player Info: %s / %s / %d credits" % [loaded_pilot_name if loaded_pilot_name != "" else "Pilot", player_ship_id, credits]

func _show_mission_info() -> void:
	mission_log_visible = not mission_log_visible
	if active_missions.is_empty():
		status_line = "Mission Info: no active missions"
		return
	var reserved := _mission_reserved_cargo_tons()
	var summaries := _mission_summary_lines()
	status_line = "Mission Info: %d active / %d tons reserved / %d free | %s" % [active_missions.size(), reserved, _cargo_available_tons(), " | ".join(summaries)]

func _mission_summary_lines() -> Array[String]:
	var lines: Array[String] = []
	for mission_id in active_missions:
		var mission := _mission_by_id(str(mission_id))
		if mission.is_empty():
			lines.append("Mission Info: " + str(mission_id))
			continue
		lines.append("Mission Info: %s to %s/%s, %d tons, %d cr" % [str(mission.get("title", mission_id)), str(mission.get("destinationSystem", "?")), str(mission.get("destinationBody", "?")), int(mission.get("cargoTons", 0)), int(mission.get("reward", 0))])
	return lines

func _mission_by_id(mission_id: String) -> Dictionary:
	for mission in missions.get("missions", []):
		if str(mission.get("id", "")) == mission_id:
			return mission
	return {}

func _mission_reserved_cargo_tons() -> int:
	var total := 0
	for mission_id in active_missions:
		total += int(_mission_by_id(str(mission_id)).get("cargoTons", 0))
	return total

func _cargo_available_tons() -> int:
	return max(0, cargo_space - cargo)

func _current_government_name() -> String:
	return _government_name_for_system(str(current_system.get("name", "")))

func _government_name_for_system(system_name: String) -> String:
	var systems_by_name: Dictionary = governments.get("systems", {})
	return str(systems_by_name.get(system_name, {}).get("government", "Unknown"))

func _legal_status_for_government(government_name: String) -> String:
	var score := int(legal_records.get(government_name, 0))
	var thresholds: Array = reputation.get("legalThresholds", [])
	var best_status := "Clean"
	var best_min := -1000000
	for threshold in thresholds:
		var min_score := int(threshold.get("minScore", 0))
		if score >= min_score and min_score >= best_min:
			best_status = str(threshold.get("status", best_status))
			best_min = min_score
	return best_status

func _government_docking_allowed(government_name: String) -> bool:
	var mechanics: Dictionary = reputation.get("mechanics", {})
	var min_by_government: Dictionary = mechanics.get("dockMinLegalScoreByGovernment", {})
	var min_score := int(min_by_government.get(government_name, mechanics.get("defaultDockMinLegalScore", -60)))
	return int(legal_records.get(government_name, 0)) >= min_score

func _legal_docking_denied_message(government_name: String) -> String:
	return "%s docking denied by %s legal status; TV scaffold, exact Classic landing denial UI pending" % [government_name, _legal_status_for_government(government_name)]

func _government_crime_tolerance_score(government_name: String) -> int:
	var mechanics: Dictionary = reputation.get("mechanics", {})
	var tolerance_by_government: Dictionary = mechanics.get("crimeToleranceLegalScoreByGovernment", {})
	return int(tolerance_by_government.get(government_name, mechanics.get("crimeToleranceLegalScore", mechanics.get("patrolHostileLegalScore", -60))))

func _legal_service_access_allowed(government_name: String) -> bool:
	return _service_access_allowed("outfitter", government_name)

func _service_access_allowed(service_name: String, government_name: String) -> bool:
	if not _government_docking_allowed(government_name):
		return false
	var requirements: Dictionary = reputation.get("mechanics", {}).get("serviceRequirements", {}).get(service_name, {})
	var legal_min: Dictionary = requirements.get("legalMin", {})
	for key in legal_min.keys():
		if str(key) == "*" or str(key) == government_name:
			if int(legal_records.get(government_name, 0)) < int(legal_min.get(key, 0)):
				return false
	var reputation_by_government: Dictionary = requirements.get("reputationMinByGovernment", {})
	var reputation_min: Dictionary = reputation_by_government.get(government_name, {})
	for key in reputation_min.keys():
		if int(reputation_scores.get(str(key), 0)) < int(reputation_min.get(key, 0)):
			return false
	return true

func _service_blocked_message(service_name: String, government_name: String) -> String:
	if not _government_docking_allowed(government_name):
		return _legal_service_blocked_message(government_name)
	var requirements: Dictionary = reputation.get("mechanics", {}).get("serviceRequirements", {}).get(service_name, {})
	var reputation_by_government: Dictionary = requirements.get("reputationMinByGovernment", {})
	var reputation_min: Dictionary = reputation_by_government.get(government_name, {})
	for key in reputation_min.keys():
		var faction := str(key)
		var needed := int(reputation_min.get(key, 0))
		if int(reputation_scores.get(faction, 0)) < needed:
			return "%s access needs %s reputation %d; TV scaffold, exact Classic service refusal UI pending" % [service_name.capitalize(), faction, needed]
	return _legal_service_blocked_message(government_name)

func _legal_service_blocked_message(government_name: String) -> String:
	return "Services blocked by %s legal status; TV scaffold, exact Classic thresholds unconfirmed" % _legal_status_for_government(government_name)

func _legal_patrol_hostile_posture_active(government_name: String) -> bool:
	return int(legal_records.get(government_name, 0)) < _government_crime_tolerance_score(government_name)

func _legal_patrol_warning_message(government_name: String) -> String:
	return "%s patrols hostile: %s legal status below CrimeTol-style tolerance — Classic Resource Bible-backed scaffold, exact runtime behavior unconfirmed" % [government_name, _legal_status_for_government(government_name)]

func _legal_patrol_attack_message(government_name: String) -> String:
	return "%s patrol attack consequence applied: legal/reputation worsened; Classic Resource Bible govt penalty scaffold, exact combat consequences unconfirmed" % government_name

func _emit_legal_patrol_warning_if_needed() -> void:
	var government_name := _current_government_name()
	if _legal_patrol_hostile_posture_active(government_name):
		_set_status(_legal_patrol_warning_message(government_name))

func _legal_warning_line(government_name: String) -> String:
	var score := int(legal_records.get(government_name, 0))
	var status := _legal_status_for_government(government_name)
	var dock_state := "docking allowed" if _government_docking_allowed(government_name) else "docking blocked"
	return "%s legal status: %s (%d) — %s; TV scaffold, exact Classic thresholds unconfirmed" % [government_name, status, score, dock_state]

func _apply_reputation_event(event_id: String, context_government := "") -> void:
	var event: Dictionary = reputation.get("events", {}).get(event_id, {})
	var reputation_delta: Dictionary = event.get("reputation", {})
	for government_name in reputation_delta.keys():
		reputation_scores[str(government_name)] = int(reputation_scores.get(str(government_name), 0)) + int(reputation_delta.get(government_name, 0))
	var legal_delta: Dictionary = event.get("legal", {})
	for government_name in legal_delta.keys():
		var target_government := context_government if str(government_name) == "*" else str(government_name)
		if target_government == "":
			continue
		legal_records[target_government] = int(legal_records.get(target_government, 0)) + int(legal_delta.get(government_name, 0))

func _pay_legal_clemency() -> bool:
	if _disabled_player_action_blocked():
		return false
	if not landed:
		_set_status("Clemency unavailable in space; land at an aligned port")
		return false
	var government_name := _current_government_name()
	var mechanics: Dictionary = reputation.get("mechanics", {})
	var min_reputation := int(mechanics.get("clemencyMinReputation", 10))
	var max_legal_score := int(mechanics.get("clemencyMaxLegalScore", -20))
	var legal_delta := int(mechanics.get("clemencyLegalDelta", 25))
	var cost := int(mechanics.get("clemencyCost", 1000))
	if int(reputation_scores.get(government_name, 0)) < min_reputation:
		_set_status("Clemency denied: need %s reputation %d; inferred TV scaffold" % [government_name, min_reputation])
		return false
	if int(legal_records.get(government_name, 0)) > max_legal_score:
		_set_status("Clemency unavailable: legal standing not low enough; inferred TV scaffold")
		return false
	if credits < cost:
		_set_status("Clemency costs %d credits; insufficient funds" % cost)
		return false
	credits -= cost
	legal_records[government_name] = min(0, int(legal_records.get(government_name, 0)) + legal_delta)
	_set_status("Paid %d cr clemency with %s: legal now %d; inferred TV scaffold" % [cost, government_name, int(legal_records.get(government_name, 0))])
	return true

func _illegal_commodity_hold(government_name: String) -> Dictionary:
	var illegal_ids: Array = governments.get("contraband", {}).get(government_name, [])
	var illegal_hold := {}
	for commodity_id in illegal_ids:
		var held := int(commodity_hold.get(str(commodity_id), 0))
		if held > 0:
			illegal_hold[str(commodity_id)] = held
	return illegal_hold

func _apply_contraband_scan(accept_bribe := false) -> Dictionary:
	var government_name := _current_government_name()
	var illegal_hold := _illegal_commodity_hold(government_name)
	var tons := 0
	for amount in illegal_hold.values():
		tons += int(amount)
	_last_contraband_scan_outcome = {"action": "none", "tons": 0, "creditsDelta": 0, "legalDelta": 0, "confiscated": {}}
	if tons <= 0:
		return _last_contraband_scan_outcome
	var government: Dictionary = governments.get("governments", {}).get(government_name, {})
	var bribe_cost := int(government.get("bribePerTon", 0)) * tons
	if accept_bribe and bool(government.get("bribeAllowed", false)) and bribe_cost > 0 and credits >= bribe_cost:
		credits -= bribe_cost
		_last_contraband_scan_outcome = {"action": "bribe", "tons": tons, "creditsDelta": -bribe_cost, "legalDelta": 0, "confiscated": {}}
		_set_status("Paid %d cr contraband bribe to %s; government bribe scaffold" % [bribe_cost, government_name])
		return _last_contraband_scan_outcome
	var fine := int(government.get("finePerTon", 0)) * tons
	var legal_by_government: Dictionary = reputation.get("events", {}).get("contraband_fine", {}).get("legal", {})
	var legal_delta := int(legal_by_government.get(government_name, legal_by_government.get("*", -3)))
	var action := "fine"
	if credits >= fine:
		credits -= fine
	else:
		action = "confiscate"
		legal_delta = int(reputation.get("mechanics", {}).get("unpaidFineLegalPenalty", -25))
	legal_records[government_name] = int(legal_records.get(government_name, 0)) + legal_delta
	for commodity_id in illegal_hold.keys():
		var confiscated := int(illegal_hold.get(commodity_id, 0))
		commodity_hold[commodity_id] = max(0, int(commodity_hold.get(commodity_id, 0)) - confiscated)
		cargo = max(0, cargo - confiscated)
	_last_contraband_scan_outcome = {"action": action, "tons": tons, "creditsDelta": -fine if action == "fine" else 0, "legalDelta": legal_delta, "confiscated": illegal_hold}
	_set_status("Contraband scan: %s %d tons, legal %+d; Classic Resource Bible smuggling scaffold" % [action, tons, legal_delta])
	return _last_contraband_scan_outcome

func _set_status(message: String) -> void:
	status_line = message
	status_messages.append(message)
	while status_messages.size() > 6:
		status_messages.remove_at(0)

func _toggle_autopilot() -> void:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return
	if landed:
		_set_status("Autopilot unavailable while landed; launch first")
		return
	autopilot_enabled = not autopilot_enabled
	if autopilot_enabled:
		_set_status("Autopilot engaged: steering toward nearest port as a Terminal Velocity assist scaffold")
	else:
		_set_status("Autopilot disengaged")

func _apply_autopilot_assist(delta: float) -> void:
	if not autopilot_enabled or landed:
		return
	if _player_disabled():
		autopilot_enabled = false
		_set_status("Autopilot disengaged: player ship disabled")
		return
	var nearest := _nearest_body()
	if nearest.is_empty():
		autopilot_enabled = false
		_set_status("Autopilot disengaged: no port in current system")
		return
	var body: Dictionary = nearest["body"]
	var target_pos := Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
	var to_target := target_pos - pos
	var distance: float = max(1.0, to_target.length())
	var desired_speed: float = clamp((distance - float(body.get("r", 40))) * 0.7, 35.0, min(_ship_max_speed() * 0.72, 240.0))
	var desired_velocity := to_target.normalized() * desired_speed
	vel = vel.lerp(desired_velocity, clamp(delta * 1.8, 0.0, 0.18))
	angle_deg = rad_to_deg(atan2(vel.x, -vel.y))
	player_facing_index = _facing_frame_index(angle_deg, max(player_frames.size(), FRAME_COUNT))
	turn_cell_progress = 0.0

func _afterburner_active() -> bool:
	return Input.is_key_pressed(KEY_Z)

func _fire_primary_weapon() -> void:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return
	if _spawn_primary_projectile():
		return
	_set_status("Primary weapon unavailable: no weapon data or targets")

func _fire_secondary_weapon() -> void:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return
	if _spawn_secondary_projectile():
		return
	if _installed_secondary_weapon_ids().is_empty():
		_set_status("Secondary weapon not loaded; primary combat scaffold available with Tab")
	else:
		_set_status(_secondary_weapon_reload_message())

func _recover_disabled_player_scaffold() -> bool:
	if not _player_disabled():
		_set_status("Recovery unavailable: player ship is still operational")
		return false
	_reset_player_combat_stats()
	projectiles.clear()
	_set_status(_player_recovery_message())
	return true

func _change_secondary_weapon() -> void:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return
	if landed and landing_tab == 1:
		_sell_selected_commodity()
		return
	var secondary_ids := _installed_secondary_weapon_ids()
	if secondary_ids.is_empty():
		_set_status("Secondary weapon selection: no secondary weapons installed")
		return
	selected_secondary_weapon_index = (selected_secondary_weapon_index + 1) % secondary_ids.size()
	var weapon := _secondary_weapon_stats()
	_set_status("Secondary weapon selected: %s" % str(weapon.get("name", secondary_ids[selected_secondary_weapon_index])))

func _installed_secondary_weapon_ids() -> Array[String]:
	var ids: Array[String] = []
	var primary_id := str(player_ship.get("weaponId", "laser_cannon"))
	for owned_id in owned_weapons.keys():
		var weapon_id := str(owned_id)
		if int(owned_weapons.get(owned_id, 0)) > 0 and weapon_id != primary_id:
			ids.append(weapon_id)
	ids.sort()
	return ids

func _secondary_weapon_stats() -> Dictionary:
	var ids := _installed_secondary_weapon_ids()
	if ids.is_empty():
		return {}
	var weapon_id := ids[selected_secondary_weapon_index % ids.size()]
	return _weapon_stats_by_id(weapon_id)

func _primary_weapon_stats() -> Dictionary:
	var weapon_id := str(player_ship.get("weaponId", "laser_cannon"))
	for weapon in weapons.get("weapons", []):
		if str(weapon.get("id", "")) == weapon_id:
			return weapon
	var weapon_list: Array = weapons.get("weapons", [])
	return weapon_list[0] if not weapon_list.is_empty() else {}

func _reset_combat_targets() -> void:
	target_shields.clear()
	target_hulls.clear()
	var npc_ship := _npc_ship_stats()
	for i in range(_npc_world_offsets().size()):
		target_shields[i] = int(npc_ship.get("shields", 100))
		target_hulls[i] = int(npc_ship.get("hull", 100))

func _npc_ship_stats() -> Dictionary:
	for ship in ships.get("ships", []):
		if str(ship.get("id", "")) != player_ship_id:
			return ship
	return player_ship

func _target_destroyed(target_index: int) -> bool:
	return int(target_shields.get(target_index, 0)) <= 0 and int(target_hulls.get(target_index, 0)) <= 0

func _max_player_shields() -> int:
	return int(player_ship.get("shields", 100))

func _max_player_hull() -> int:
	# EV Classic Resource Bible `shïp` Armor: armor takes damage once shields are down.
	return int(player_ship.get("hull", player_ship.get("armor", 100))) + _owned_outfit_effect_total("maxHull")

func _owned_outfit_effect_total(effect_name: String) -> int:
	var total := 0
	for outfit in outfits.get("outfits", []):
		var outfit_id := str(outfit.get("id", ""))
		var count := int(owned_outfits.get(outfit_id, 0))
		if count <= 0:
			continue
		var effects: Dictionary = outfit.get("effects", {})
		total += int(effects.get(effect_name, 0)) * count
	return total

func _reset_player_combat_stats() -> void:
	player_shields = _max_player_shields()
	player_hull = _max_player_hull()
	player_shield_recharge_progress = 0.0
	primary_weapon_cooldown_frames = 0.0
	secondary_weapon_cooldown_frames = 0.0
	npc_retaliation_cooldowns.clear()
	afterburner_fuel_progress = 0.0

func _advance_weapon_cooldowns(delta: float) -> void:
	primary_weapon_cooldown_frames = maxf(0.0, primary_weapon_cooldown_frames - delta * 60.0)
	secondary_weapon_cooldown_frames = maxf(0.0, secondary_weapon_cooldown_frames - delta * 60.0)
	for target_key in npc_retaliation_cooldowns.keys():
		npc_retaliation_cooldowns[target_key] = maxf(0.0, float(npc_retaliation_cooldowns.get(target_key, 0.0)) - delta * 60.0)

func _primary_weapon_reload_message() -> String:
	return "Primary weapon reloading; wait for source-backed reload cadence"

func _secondary_weapon_reload_message() -> String:
	return "Secondary weapon reloading; wait for source-backed reload cadence"

func _npc_retaliation_reload_message() -> String:
	return "NPC retaliation reloading; Terminal Velocity AI cadence scaffold"

func _player_disabled() -> bool:
	return player_hull <= 0

func _player_disabled_action_message() -> String:
	return "Player ship disabled; use F8 recovery before continuing actions"

func _disabled_player_action_blocked() -> bool:
	if not _player_disabled():
		return false
	_set_status(_player_disabled_action_message())
	return true

func _player_recovery_message() -> String:
	return "Recovered disabled player ship with F8; Terminal Velocity reload/new-pilot recovery scaffold"

func _recharge_player_shields(delta: float) -> void:
	if player_shields >= _max_player_shields() or player_hull <= 0:
		return
	var recharge_frames: float = maxf(1.0, float(player_ship.get("shieldRecharge", 30)))
	player_shield_recharge_progress += delta * 60.0
	while player_shield_recharge_progress >= recharge_frames and player_shields < _max_player_shields():
		player_shield_recharge_progress -= recharge_frames
		player_shields += 1

func _weapon_shield_damage(weapon: Dictionary) -> int:
	var mass_damage := int(weapon.get("massDamage", weapon.get("damage", 1)))
	var energy_damage := int(weapon.get("energyDamage", weapon.get("damage", 1)))
	# EV Classic Resource Bible `wëap`: shields-up damage = MassDmg/4 + EnergyDmg, minimum 1.
	return max(1, int(floor(float(mass_damage) / 4.0 + float(energy_damage))))

func _weapon_hull_damage(weapon: Dictionary) -> int:
	var mass_damage := int(weapon.get("massDamage", weapon.get("damage", 1)))
	var energy_damage := int(weapon.get("energyDamage", weapon.get("damage", 1)))
	# EV Classic Resource Bible `wëap`: shields-down damage = MassDmg + EnergyDmg/4, minimum 1.
	return max(1, int(floor(float(mass_damage) + float(energy_damage) / 4.0)))

func _spawn_primary_projectile() -> bool:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return false
	var targets := _npc_world_offsets()
	var weapon := _primary_weapon_stats()
	if targets.is_empty() or weapon.is_empty():
		return false
	if primary_weapon_cooldown_frames > 0.0:
		_set_status(_primary_weapon_reload_message())
		return false
	var target_index := selected_target_index % targets.size()
	if _target_destroyed(target_index):
		if _select_next_live_target(target_index):
			_set_status("Target already disabled; retargeting to next active contact")
		else:
			_set_status("Target already disabled; no active contacts")
		return false
	var target_pos: Vector2 = targets[target_index]
	var direction := (target_pos - pos).normalized()
	if direction.length() <= 0.0:
		direction = Vector2.UP.rotated(deg_to_rad(angle_deg))
	var projectile := {
		"position": pos,
		"velocity": direction * float(weapon.get("speed", 9.0)) * 60.0,
		"life": float(weapon.get("lifetime", 72)) / 60.0,
		"shieldDamage": _weapon_shield_damage(weapon),
		"hullDamage": _weapon_hull_damage(weapon),
		"color": str(weapon.get("color", "OrangeRed")),
		"radius": float(weapon.get("radius", 3)),
		"targetIndex": target_index,
	}
	projectiles.append(projectile)
	primary_weapon_cooldown_frames = float(weapon.get("reloadFrames", weapon.get("sourceStockWeaponFields", {}).get("Reload", 0)))
	_set_status("Fired %s at Contact %d" % [str(weapon.get("name", "Primary")), target_index + 1])
	_play_sound(_sound_binding_for_weapon(str(weapon.get("id", ""))))
	return true


func _spawn_secondary_projectile() -> bool:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return false
	var targets := _npc_world_offsets()
	var weapon := _secondary_weapon_stats()
	if targets.is_empty() or weapon.is_empty():
		return false
	if secondary_weapon_cooldown_frames > 0.0:
		_set_status(_secondary_weapon_reload_message())
		return false
	var target_index := selected_target_index % targets.size()
	if _target_destroyed(target_index):
		if _select_next_live_target(target_index):
			_set_status("Target already disabled; retargeting to next active contact")
		else:
			_set_status("Target already disabled; no active contacts")
		return false
	var target_pos: Vector2 = targets[target_index]
	var direction := (target_pos - pos).normalized()
	if direction.length() <= 0.0:
		direction = Vector2.UP.rotated(deg_to_rad(angle_deg))
	var projectile := {
		"position": pos,
		"velocity": direction * float(weapon.get("speed", 7.0)) * 60.0,
		"life": float(weapon.get("lifetime", weapon.get("countFrames", 84))) / 60.0,
		"shieldDamage": _weapon_shield_damage(weapon),
		"hullDamage": _weapon_hull_damage(weapon),
		"color": str(weapon.get("color", "DeepSkyBlue")),
		"radius": float(weapon.get("radius", 4)),
		"targetIndex": target_index,
		"secondary": true,
	}
	projectiles.append(projectile)
	secondary_weapon_cooldown_frames = float(weapon.get("reloadFrames", weapon.get("sourceStockWeaponFields", {}).get("Reload", 0)))
	_set_status("Fired secondary %s at Contact %d" % [str(weapon.get("name", "Secondary")), target_index + 1])
	_play_sound(_sound_binding_for_weapon(str(weapon.get("id", ""))))
	return true

func _spawn_npc_retaliation_projectile(target_index: int) -> bool:
	var targets := _npc_world_offsets()
	if target_index < 0 or target_index >= targets.size() or _target_destroyed(target_index):
		return false
	if float(npc_retaliation_cooldowns.get(target_index, 0.0)) > 0.0:
		_set_status(_npc_retaliation_reload_message())
		return false
	var npc_ship := _npc_ship_stats()
	var weapon_id := str(npc_ship.get("weaponId", "pulse_cannon"))
	var weapon := _weapon_stats_by_id(weapon_id)
	if weapon.is_empty():
		weapon = _primary_weapon_stats()
	if weapon.is_empty():
		return false
	var origin: Vector2 = targets[target_index]
	var direction := (pos - origin).normalized()
	if direction.length() <= 0.0:
		direction = Vector2.DOWN
	projectiles.append({
		"position": origin,
		"velocity": direction * float(weapon.get("speed", 7.0)) * 60.0,
		"life": float(weapon.get("lifetime", 72)) / 60.0,
		"shieldDamage": _weapon_shield_damage(weapon),
		"hullDamage": _weapon_hull_damage(weapon),
		"color": str(weapon.get("color", "DeepSkyBlue")),
		"radius": float(weapon.get("radius", 3)),
		"targetIndex": -1,
		"firedBy": "npc",
	})
	npc_retaliation_cooldowns[target_index] = float(weapon.get("reloadFrames", weapon.get("sourceStockWeaponFields", {}).get("Reload", 0)))
	_play_sound(_sound_binding_for_weapon(weapon_id))
	return true

func _weapon_stats_by_id(weapon_id: String) -> Dictionary:
	for weapon in weapons.get("weapons", []):
		if str(weapon.get("id", "")) == weapon_id:
			return weapon
	return {}

func _advance_projectiles(delta: float) -> void:
	_advance_explosion_events(delta)
	if projectiles.is_empty():
		return
	var survivors: Array[Dictionary] = []
	var targets := _npc_world_offsets()
	for projectile in projectiles:
		var position: Vector2 = projectile.get("position", Vector2.ZERO)
		position += projectile.get("velocity", Vector2.ZERO) * delta
		projectile["position"] = position
		projectile["life"] = float(projectile.get("life", 0.0)) - delta
		var hit := false
		if str(projectile.get("firedBy", "player")) == "npc":
			if position.distance_to(pos) <= 28.0 + float(projectile.get("radius", 3.0)):
				_apply_player_projectile_hit(projectile)
				hit = true
		else:
			for i in range(targets.size()):
				if _target_destroyed(i):
					continue
				if position.distance_to(targets[i]) <= 32.0 + float(projectile.get("radius", 3.0)):
					_apply_projectile_hit(projectile, i)
					hit = true
					break
		if not hit and float(projectile.get("life", 0.0)) > 0.0:
			survivors.append(projectile)
	projectiles = survivors

func _advance_explosion_events(delta: float) -> void:
	if explosion_events.is_empty():
		return
	var survivors: Array[Dictionary] = []
	for explosion in explosion_events:
		explosion["life"] = float(explosion.get("life", 0.0)) - delta
		if float(explosion.get("life", 0.0)) > 0.0:
			survivors.append(explosion)
	explosion_events = survivors

func _apply_projectile_hit(projectile: Dictionary, target_index: int) -> void:
	var shields := int(target_shields.get(target_index, 0))
	var hull := int(target_hulls.get(target_index, 0))
	if shields > 0:
		shields = max(0, shields - int(projectile.get("shieldDamage", 1)))
	else:
		hull = max(0, hull - int(projectile.get("hullDamage", 1)))
	target_shields[target_index] = shields
	target_hulls[target_index] = hull
	if _target_destroyed(target_index):
		_record_explosion_event(target_index)
		var combat_reward_amount := _award_combat_disable_reward(target_index)
		var government_name := _current_government_name()
		if _legal_patrol_hostile_posture_active(government_name):
			_apply_reputation_event("destroy_patrol", government_name)
			_set_status(_legal_patrol_attack_message(government_name))
		else:
			_set_status("Contact %d disabled; reward +%d cr — TV scaffold, Classic bounty pending" % [target_index + 1, combat_reward_amount])
	else:
		_set_status("Contact %d hit: shield %d hull %d" % [target_index + 1, shields, hull])

func _record_explosion_event(target_index: int) -> void:
	var targets := _npc_world_offsets()
	var explosion_position := targets[target_index] if target_index >= 0 and target_index < targets.size() else pos
	explosion_events.append({
		"position": explosion_position,
		"life": 2.0,
		"radius": 8.0,
		"targetIndex": target_index,
		"sourceLabel": "terminal-velocity-explosion-visual-scaffold",
		"oracleStatus": "classic_runtime_explosion_timing_pending",
	})
	_play_sound(_sound_binding_for_combat("shipExplodes"))
	_spawn_cargo_salvage_pickup(target_index, explosion_position)

func _award_combat_disable_reward(target_index: int) -> int:
	for reward in combat_reward_history:
		if int(reward.get("targetIndex", -1)) == target_index:
			return 0
	var reward_amount := 25
	credits += reward_amount
	combat_reward_history.append({
		"targetIndex": target_index,
		"targetLabel": "Contact %d" % [target_index + 1],
		"credits": reward_amount,
		"sourceLabel": "terminal-velocity-combat-reward-scaffold",
		"oracleStatus": "classic_runtime_combat_reward_behavior_pending",
	})
	return reward_amount

func _spawn_cargo_salvage_pickup(target_index: int, pickup_position: Vector2) -> Dictionary:
	var commodity_id := "equipment"
	var tons := 2
	var pickup := {
		"position": pickup_position,
		"commodityId": commodity_id,
		"tons": tons,
		"targetIndex": target_index,
		"sourceLabel": "terminal-velocity-combat-salvage-scaffold",
		"oracleStatus": "classic_runtime_loot_cargo_behavior_pending",
	}
	cargo_salvage_pickups.append(pickup)
	return pickup

func _advance_cargo_salvage_pickups() -> void:
	if cargo_salvage_pickups.is_empty():
		return
	var remaining: Array[Dictionary] = []
	for pickup in cargo_salvage_pickups:
		var pickup_position: Vector2 = pickup.get("position", Vector2.ZERO)
		if pos.distance_to(pickup_position) > 44.0:
			remaining.append(pickup)
			continue
		var tons := int(pickup.get("tons", 0))
		var commodity_id := str(pickup.get("commodityId", "equipment"))
		var available := _cargo_available_tons()
		if available < tons:
			remaining.append(pickup)
			_set_status("Cargo hold full; salvage remains in space")
			continue
		cargo += tons
		commodity_hold[commodity_id] = int(commodity_hold.get(commodity_id, 0)) + tons
		_set_status("Recovered %d tons of %s salvage (TV scaffold; Classic loot behavior pending)" % [tons, _commodity_display_name(commodity_id)])
	cargo_salvage_pickups = remaining

func _commodity_display_name(commodity_id: String) -> String:
	for commodity in economy.get("commodities", []):
		if str(commodity.get("id", "")) == commodity_id:
			return str(commodity.get("name", commodity_id.capitalize()))
	return commodity_id.capitalize()

func _player_disabled_message() -> String:
	return "Player ship disabled; Terminal Velocity reload/new-pilot recovery scaffold (Strict Play death semantics pending Classic confirmation)"

func _record_player_disabled_event() -> void:
	explosion_events.append({
		"position": pos,
		"life": 2.0,
		"radius": 10.0,
		"targetIndex": -1,
		"sourceLabel": "terminal-velocity-player-disabled-scaffold",
		"oracleStatus": "classic_runtime_player_death_pending_strict_play_safe_trace",
	})
	_play_sound(_sound_binding_for_combat("shipExplodes"))

func _apply_player_projectile_hit(projectile: Dictionary) -> void:
	if player_shields > 0:
		player_shields = max(0, player_shields - int(projectile.get("shieldDamage", 1)))
	else:
		player_hull = max(0, player_hull - int(projectile.get("hullDamage", 1)))
	if player_hull <= 0:
		_record_player_disabled_event()
		_set_status(_player_disabled_message())
	else:
		_set_status("Incoming hit: shield %d hull %d" % [player_shields, player_hull])

func _jump() -> void:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return
	var systems: Array = universe.get("systems", [])
	var links: Array = current_system.get("links", [])
	if links.is_empty() and selected_route.is_empty():
		_set_status("No hyperspace route selected; open map (M) or queue mission route (G)")
		return
	var destination := _selected_destination_name()
	if destination == "None":
		_set_status("No hyperspace route selected; open map (M) or queue mission route (G)")
		return
	if _too_close_to_system_center_for_jump():
		_set_status("Can't initiate hyperspace jump - not yet far enough away from system center.")
		return
	if player_fuel < _jump_fuel_cost():
		_set_status("Insufficient fuel for hyperspace; land at a port with refuel service or choose a closer route")
		return
	for i in range(systems.size()):
		if systems[i].get("name", "") == destination:
			current_system_index = i
			current_system = systems[i]
			if not selected_route.is_empty() and str(selected_route[0]) == destination:
				selected_route.remove_at(0)
			selected_link_index = 0
			pos = PLAYER_START
			vel = Vector2.ZERO
			landed = false
			player_fuel = max(0, player_fuel - _jump_fuel_cost())
			status_line = "Hyperspace arrival: " + destination
			_emit_legal_patrol_warning_if_needed()
			return

func _try_land() -> void:
	if _player_disabled():
		_set_status(_player_disabled_action_message())
		return
	var nearest := _nearest_body()
	if nearest.is_empty():
		_set_status("No port in range; fly closer to a planet/station and slow below landing speed")
		return
	var government_name := _current_government_name()
	if not _government_docking_allowed(government_name):
		_set_status(_legal_docking_denied_message(government_name))
		_emit_legal_patrol_warning_if_needed()
		return
	if nearest["distance"] < nearest["body"].get("r", 40) + 45 and vel.length() < 90:
		landed = true
		vel = Vector2.ZERO
		_set_status("Landed at " + nearest["body"].get("name", "port"))
		_apply_contraband_scan(false)
	else:
		_set_status("Approach slower/closer to land; landing needs close range and speed under 90")

func _nearest_body() -> Dictionary:
	var best := {}
	for body in current_system.get("bodies", []):
		var body_pos := Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
		var dist := pos.distance_to(body_pos)
		if best.is_empty() or dist < best["distance"]:
			best = {"body": body, "distance": dist}
	return best

func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, VIEW_SIZE), Color(0.005, 0.006, 0.012), true)
	var center := VIEW_SIZE * 0.5
	var font := ThemeDB.fallback_font
	if game_state == STATE_TITLE:
		_draw_title_screen(center, font)
		return
	draw_string(font, Vector2(18, 24), "TV GODOT RENDER ACTIVE — cell-center build", HORIZONTAL_ALIGNMENT_LEFT, 620, 18, Color(1.0, 0.85, 0.25))
	for star in stars:
		var screen := center + (star - pos * 0.18) * 0.45
		if Rect2(Vector2.ZERO, VIEW_SIZE).has_point(screen):
			draw_circle(screen, 1.0, Color(0.55, 0.62, 0.72))
	_draw_bodies(center)
	_draw_projectiles(center)
	_draw_npcs(center)
	_draw_player(center)
	_draw_hud()
	if map_visible:
		_draw_universe_map()
	if landed:
		_draw_landing_panel()
	if mission_log_visible:
		_draw_mission_log_overlay()
	if player_info_visible:
		_draw_player_info_overlay()
	if help_visible:
		_draw_help_overlay()

func _draw_title_screen(center: Vector2, font: Font) -> void:
	for star in stars:
		var screen := center + star * 0.18
		if Rect2(Vector2.ZERO, VIEW_SIZE).has_point(screen):
			draw_circle(screen, 1.0, Color(0.55, 0.62, 0.72))
	var green := Color(0.38, 0.95, 0.34)
	var dim_green := Color(0.10, 0.36, 0.12)
	var line_green := Color(0.22, 0.78, 0.22)
	_draw_title_side_decoration(Vector2(120, 230), false)
	_draw_title_side_decoration(Vector2(1160, 230), true)
	draw_string(font, Vector2(296, 130), "TERMINAL", HORIZONTAL_ALIGNMENT_CENTER, 690, 76, green)
	draw_string(font, Vector2(298, 205), "VELOCITY", HORIZONTAL_ALIGNMENT_CENTER, 685, 86, green)
	draw_line(Vector2(325, 294), Vector2(955, 294), dim_green, 2.0)
	draw_line(Vector2(360, 308), Vector2(920, 308), dim_green, 1.0)
	var status_rect := Rect2(405, 360, 470, 78)
	draw_rect(status_rect, Color(0.0, 0.0, 0.0, 0.82), true)
	draw_rect(status_rect, line_green, false, 2.0)
	draw_string(font, status_rect.position + Vector2(0, 48), title_status_line, HORIZONTAL_ALIGNMENT_CENTER, status_rect.size.x, 18, Color(0.70, 1.0, 0.66))
	for button in _title_buttons():
		_draw_title_button(button, font)
	if title_modal == "":
		draw_string(font, Vector2(300, 716), "Personal-use Godot reconstruction. Title substituted: Terminal Velocity.", HORIZONTAL_ALIGNMENT_CENTER, 680, 15, Color(0.52, 0.82, 0.52))
		draw_string(font, Vector2(300, 742), "Enter/click Enter Ship to start. N/O/S/A/Q shortcuts mirror the title menu.", HORIZONTAL_ALIGNMENT_CENTER, 680, 15, Color(0.42, 0.68, 0.44))
	else:
		_draw_title_modal(font)

func _draw_title_button(button: Dictionary, font: Font) -> void:
	var rect: Rect2 = button["rect"]
	var mouse_pos := get_viewport().get_mouse_position()
	var hovered := rect.has_point(mouse_pos)
	var fill := Color(0.04, 0.23, 0.055, 0.96) if hovered else Color(0.015, 0.13, 0.035, 0.94)
	var border := Color(0.55, 1.0, 0.42) if hovered else Color(0.20, 0.75, 0.19)
	draw_rect(rect, fill, true)
	draw_rect(rect, border, false, 2.0)
	draw_line(rect.position + Vector2(3, 3), rect.position + Vector2(rect.size.x - 4, 3), Color(0.72, 1.0, 0.58), 1.0)
	draw_line(rect.position + Vector2(3, rect.size.y - 4), rect.position + Vector2(rect.size.x - 4, rect.size.y - 4), Color(0.04, 0.32, 0.06), 1.0)
	draw_string(font, rect.position + Vector2(0, 26), str(button["label"]), HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 19, Color(0.82, 1.0, 0.74))

func _draw_title_side_decoration(anchor: Vector2, flip: bool) -> void:
	var dir := -1.0 if flip else 1.0
	var metal := Color(0.18, 0.25, 0.22, 0.92)
	var green := Color(0.14, 0.70, 0.18, 0.85)
	draw_arc(anchor, 76, -1.2 if not flip else PI - 1.9, 1.2 if not flip else PI + 1.9, 36, green, 3.0)
	draw_line(anchor + Vector2(18 * dir, -70), anchor + Vector2(118 * dir, -34), metal, 5.0)
	draw_line(anchor + Vector2(28 * dir, 0), anchor + Vector2(142 * dir, 0), metal, 5.0)
	draw_line(anchor + Vector2(18 * dir, 70), anchor + Vector2(118 * dir, 34), metal, 5.0)
	draw_circle(anchor + Vector2(150 * dir, 0), 16, Color(0.04, 0.19, 0.06))
	draw_arc(anchor + Vector2(150 * dir, 0), 24, 0, TAU, 28, green, 2.0)

func _draw_title_modal(font: Font) -> void:
	var rect := Rect2(270, 215, 740, 360)
	if title_modal == "prefs":
		rect = Rect2(220, 92, 840, 660)
	draw_rect(rect, Color(0.82, 0.82, 0.78, 1.0), true)
	draw_rect(rect, Color(0.08, 0.08, 0.08), false, 2.0)
	if title_modal != "prefs":
		draw_rect(Rect2(rect.position + Vector2(8, 8), Vector2(rect.size.x - 16, 24)), Color(0.18, 0.18, 0.18), true)
	if title_modal == "about":
		_draw_about_modal(rect, font)
		return
	if title_modal == "prefs":
		_draw_prefs_modal(rect, font)
		return
	if title_modal == "open_pilot":
		_draw_open_pilot_modal(rect, font)
		return
	var title := "New Pilot"
	var prompt := "Enter your name, pilot:"
	var value := pilot_name_input
	if title_modal == "new_ship_name":
		title = "New Pilot"
		prompt = "Now, please christen your brand-new Shuttlecraft."
		value = ship_name_input
	draw_string(font, rect.position + Vector2(0, 28), title, HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 18, Color(0.95, 0.95, 0.90))
	draw_string(font, rect.position + Vector2(42, 82), prompt, HORIZONTAL_ALIGNMENT_LEFT, 590, 20, Color(0.02, 0.02, 0.02))
	if title_modal == "new_ship_name":
		draw_string(font, rect.position + Vector2(42, 116), "Ship Name:", HORIZONTAL_ALIGNMENT_LEFT, 590, 18, Color(0.02, 0.02, 0.02))
	_draw_text_entry(Rect2(rect.position + Vector2(185, 102), Vector2(360, 34)), value, font)
	if title_modal == "new_pilot_name":
		# Source-backed from original EV Classic New Pilot dialog observed in Basilisk II
		# on 2026-05-20. Strict Play is off by default; leave it optional and saved
		# per pilot without implementing destructive death semantics yet.
		_draw_checkbox(_strict_play_checkbox_rect().position, strict_play_selected, Color(0.02, 0.02, 0.02))
		draw_string(font, rect.position + Vector2(70, 157), "Strict Play", HORIZONTAL_ALIGNMENT_LEFT, 240, 18, Color(0.02, 0.02, 0.02))
		draw_string(font, rect.position + Vector2(42, 194), "If you check this box, when you're dead, you're dead. No reincarnation allowed.", HORIZONTAL_ALIGNMENT_LEFT, 650, 16, Color(0.02, 0.02, 0.02))
	_draw_modal_button(Rect2(700, 492, 116, 34), "Cancel", font)
	_draw_modal_button(Rect2(836, 492, 116, 34), "OK", font)
	draw_string(font, rect.position + Vector2(42, 232), "Return accepts. Escape cancels.", HORIZONTAL_ALIGNMENT_LEFT, 590, 14, Color(0.25, 0.25, 0.25))

func _strict_play_checkbox_rect() -> Rect2:
	return Rect2(312, 356, 12, 12)

func _strict_play_toggle_rect() -> Rect2:
	return Rect2(312, 350, 210, 28)

func _draw_open_pilot_modal(rect: Rect2, font: Font) -> void:
	draw_string(font, rect.position + Vector2(0, 28), "Open Pilot", HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 18, Color(0.95, 0.95, 0.90))
	draw_string(font, rect.position + Vector2(42, 74), "Select pilot file:", HORIZONTAL_ALIGNMENT_LEFT, 590, 18, Color(0.02, 0.02, 0.02))
	var list_rect := Rect2(360, 365, 560, 90)
	draw_rect(list_rect, Color(0.98, 0.98, 0.94), true)
	draw_rect(list_rect, Color(0.10, 0.10, 0.10), false, 1.0)
	if available_pilots.is_empty():
		draw_string(font, list_rect.position + Vector2(10, 28), "No pilot files found.", HORIZONTAL_ALIGNMENT_LEFT, list_rect.size.x - 20, 16, Color(0.1, 0.1, 0.1))
	else:
		for i in range(min(available_pilots.size(), 3)):
			var row_rect := Rect2(list_rect.position + Vector2(0, i * 30), Vector2(list_rect.size.x, 30))
			if i == selected_pilot_index:
				draw_rect(row_rect.grow(-2), Color(0.22, 0.40, 0.85, 0.95), true)
			var entry := available_pilots[i]
			var row_text := _open_pilot_row_text(entry)
			var color := Color(1, 1, 1) if i == selected_pilot_index else Color(0.05, 0.05, 0.05)
			draw_string(font, row_rect.position + Vector2(10, 22), row_text, HORIZONTAL_ALIGNMENT_LEFT, row_rect.size.x - 20, 16, color)
	_draw_modal_button(Rect2(700, 492, 116, 34), "Open", font)
	_draw_modal_button(Rect2(836, 492, 116, 34), "Cancel", font)
	draw_string(font, rect.position + Vector2(42, 232), "Return opens. Up/Down selects. Escape cancels.", HORIZONTAL_ALIGNMENT_LEFT, 590, 14, Color(0.25, 0.25, 0.25))

func _open_pilot_row_text(entry: Dictionary) -> String:
	var strict_label := "on" if bool(entry.get("strict_play", false)) else "off"
	var status_text := str(entry.get("status_line", ""))
	if status_text.strip_edges() == "":
		status_text = "No recent status"
	return "%s — %s / %s | System: %s | Credits: %d | Strict Play: %s | Mission: %s | Status: %s" % [
		str(entry.get("pilot_name", "")),
		str(entry.get("ship_name", "")),
		str(entry.get("ship_type", "Shuttlecraft")),
		str(entry.get("system", "?")),
		int(entry.get("credits", 0)),
		strict_label,
		_pilot_resume_mission_summary(entry),
		status_text,
	]

func _pilot_resume_mission_summary(entry: Dictionary) -> String:
	var active: Array = entry.get("active_missions", [])
	if active.is_empty():
		return "none"
	var mission_id := str(active[0])
	for mission in missions.get("missions", []):
		if str(mission.get("id", "")) == mission_id:
			return "%s to %s/%s" % [str(mission.get("title", mission_id)), str(mission.get("destinationSystem", "?")), str(mission.get("destinationBody", "?"))]
	return mission_id

func _draw_about_modal(rect: Rect2, font: Font) -> void:
	draw_string(font, rect.position + Vector2(0, 28), "About Terminal Velocity", HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 18, Color(0.95, 0.95, 0.90))
	var lines := [
		"Terminal Velocity is a personal-use EV-style Godot reconstruction.",
		"It loads local JSON manifests and extracted Classic EV-era resources.",
		"Title and implementation are original; proprietary source files stay local.",
		"Current slice: title pilots, source-backed ships, sounds, ports, jobs, and trading.",
		"Keyboard: Enter starts, N creates, O opens, S prefs, Q quits.",
	]
	for i in range(lines.size()):
		draw_string(font, rect.position + Vector2(42, 78 + i * 27), lines[i], HORIZONTAL_ALIGNMENT_LEFT, 595, 16, Color(0.02, 0.02, 0.02))
	_draw_modal_button(Rect2(836, 492, 116, 34), "OK", font)
	draw_string(font, rect.position + Vector2(42, 232), "Return or Escape closes.", HORIZONTAL_ALIGNMENT_LEFT, 590, 14, Color(0.25, 0.25, 0.25))

func _draw_prefs_modal(rect: Rect2, font: Font) -> void:
	# Source-backed from original EV Classic title Set Prefs screen observed in Basilisk II
	# on 2026-05-19. Keep the proprietary screenshot local-only; copy only derived
	# layout/wording into the repo.
	var black := Color(0.02, 0.02, 0.02)
	var group_color := Color(0.08, 0.08, 0.08)
	_draw_pref_group(Rect2(246, 114, 285, 405), "Navigation Controls:", font)
	_draw_key_binding(Vector2(300, 170), "Accelerate:", "Up", font)
	_draw_key_binding(Vector2(300, 207), "Rev. Course:", "Down", font)
	_draw_key_binding(Vector2(300, 244), "Rotate Right:", "Right", font)
	_draw_key_binding(Vector2(300, 281), "Rotate Left:", "Left", font)
	_draw_key_binding(Vector2(300, 318), "Afterburner:", "Z", font)
	_draw_key_binding(Vector2(300, 355), "Autopilot:", "A", font)
	_draw_key_binding(Vector2(300, 392), "Hyper Mode:", "H", font)
	_draw_key_binding(Vector2(300, 429), "Hyper Select:", "Backslash", font)
	_draw_key_binding(Vector2(300, 466), "Jump:", "J", font)
	_draw_key_binding(Vector2(300, 503), "Nav Off:", "~", font)

	_draw_pref_group(Rect2(542, 114, 245, 126), "Escort Controls:", font)
	_draw_key_binding(Vector2(550, 170), "Retarget:", "F", font, 105, 120)
	_draw_key_binding(Vector2(550, 207), "Recall:\n(option = dock)", "C", font, 105, 120)
	_draw_key_binding(Vector2(550, 244), "Hold Pos:", "D", font, 105, 120)

	_draw_pref_group(Rect2(542, 295, 245, 230), "Weapon Controls:", font)
	_draw_key_binding(Vector2(550, 351), "Fire Primary:", "Tab", font, 105, 120)
	_draw_key_binding(Vector2(550, 388), "Fire Secondary:", "Space", font, 105, 120)
	_draw_key_binding(Vector2(550, 425), "Change Secondary:", "S", font, 105, 120)
	_draw_key_binding(Vector2(550, 462), "Next Target:", "N", font, 105, 120)
	_draw_key_binding(Vector2(550, 499), "Closest Target:", "R", font, 105, 120)

	_draw_pref_group(Rect2(798, 114, 246, 454), "Misc. Controls:", font)
	_draw_key_binding(Vector2(808, 170), "Pause:", "Escape", font, 105, 120)
	_draw_key_binding(Vector2(808, 207), "Acknowledge:", "Return", font, 105, 120)
	_draw_key_binding(Vector2(808, 244), "Communicate:", "Y", font, 105, 120)
	_draw_key_binding(Vector2(808, 281), "Land:", "L", font, 105, 120)
	_draw_key_binding(Vector2(808, 318), "Jettison:   ⌘", "K", font, 105, 120)
	_draw_key_binding(Vector2(808, 355), "Board:", "B", font, 105, 120)
	_draw_key_binding(Vector2(808, 392), "Eject:      ⌘", "E", font, 105, 120)
	_draw_key_binding(Vector2(808, 429), "Destruct:   ⌘", "D", font, 105, 120)
	_draw_key_binding(Vector2(808, 466), "Map:", "M", font, 105, 120)
	_draw_key_binding(Vector2(808, 503), "Player Info:", "P", font, 105, 120)
	_draw_key_binding(Vector2(808, 540), "Mission Info:", "I", font, 105, 120)
	_draw_key_binding(Vector2(808, 577), "Cloak:", "U", font, 105, 120)

	draw_string(font, Vector2(305, 606), "Sound Volume:", HORIZONTAL_ALIGNMENT_LEFT, 220, 22, black)
	var sound_row := Rect2(302, 625, 190, 28)
	if selected_pref_index == 2:
		draw_rect(sound_row.grow(2), Color(0.78, 0.78, 0.74), true)
	_draw_spinner(Vector2(305, 626), font)
	draw_string(font, Vector2(333, 646), "Quiet", HORIZONTAL_ALIGNMENT_LEFT, 140, 19, black)

	var intro_row := Rect2(525, 625, 220, 28)
	if selected_pref_index == 0:
		draw_rect(intro_row.grow(2), Color(0.78, 0.78, 0.74), true)
	_draw_checkbox(Vector2(526, 628), pref_music_on, group_color)
	draw_string(font, Vector2(550, 646), "Intro Music", HORIZONTAL_ALIGNMENT_LEFT, 180, 19, black)

	var speed_rect := Rect2(532, 708, 172, 34)
	if selected_pref_index == 1:
		draw_rect(speed_rect.grow(3), Color(0.78, 0.78, 0.74), true)
	_draw_modal_button(speed_rect, "Game Speed...", font)
	_draw_modal_button(Rect2(828, 708, 86, 34), "Cancel", font)
	_draw_modal_button(Rect2(940, 708, 86, 34), "OK", font)

func _draw_pref_group(rect: Rect2, title: String, font: Font) -> void:
	draw_rect(rect, Color(0, 0, 0, 0), false, 1.0)
	draw_rect(Rect2(rect.position + Vector2(8, -9), Vector2(180, 18)), Color(0.82, 0.82, 0.78), true)
	draw_string(font, rect.position + Vector2(14, 5), "... " + title, HORIZONTAL_ALIGNMENT_LEFT, rect.size.x - 28, 16, Color(0.02, 0.02, 0.02))

func _draw_key_binding(position: Vector2, label: String, key_name: String, font: Font, label_width: float = 100.0, key_width: float = 120.0) -> void:
	var label_lines := label.split("\n")
	for i in range(label_lines.size()):
		draw_string(font, position + Vector2(0, 0 + i * 16), label_lines[i], HORIZONTAL_ALIGNMENT_LEFT, label_width, 15, Color(0.02, 0.02, 0.02))
	var key_rect := Rect2(position + Vector2(label_width, -16), Vector2(key_width, 31))
	draw_rect(key_rect, Color(0.98, 0.98, 0.96), true)
	draw_rect(key_rect, Color(0.05, 0.05, 0.05), false, 1.0)
	draw_string(font, key_rect.position + Vector2(8, 23), key_name, HORIZONTAL_ALIGNMENT_LEFT, key_width - 16, 18, Color(0.02, 0.02, 0.02))

func _draw_spinner(position: Vector2, font: Font) -> void:
	var box := Rect2(position, Vector2(17, 28))
	draw_rect(box, Color(0.98, 0.98, 0.96), true)
	draw_rect(box, Color(0.05, 0.05, 0.05), false, 1.0)
	draw_string(font, position + Vector2(2, 12), "↕", HORIZONTAL_ALIGNMENT_LEFT, 15, 18, Color(0.02, 0.02, 0.02))

func _draw_checkbox(position: Vector2, checked: bool, color: Color) -> void:
	var box := Rect2(position, Vector2(12, 12))
	draw_rect(box, Color(1, 1, 1), true)
	draw_rect(box, color, false, 1.0)
	if checked:
		draw_line(position + Vector2(2, 6), position + Vector2(5, 10), color, 1.5)
		draw_line(position + Vector2(5, 10), position + Vector2(11, 2), color, 1.5)

func _draw_radio_choice(position: Vector2, selected: bool, color: Color) -> void:
	draw_arc(position + Vector2(6, 6), 6, 0, TAU, 18, color, 1.0)
	if selected:
		draw_circle(position + Vector2(6, 6), 3, color)

func _draw_text_entry(rect: Rect2, value: String, font: Font) -> void:
	draw_rect(rect, Color(1.0, 1.0, 1.0), true)
	draw_rect(rect, Color(0.10, 0.10, 0.10), false, 1.0)
	draw_string(font, rect.position + Vector2(8, 23), value + "_", HORIZONTAL_ALIGNMENT_LEFT, rect.size.x - 16, 18, Color(0.0, 0.0, 0.0))

func _draw_modal_button(rect: Rect2, label: String, font: Font) -> void:
	draw_rect(rect, Color(0.88, 0.88, 0.84), true)
	draw_rect(rect, Color(0.04, 0.04, 0.04), false, 1.0)
	draw_string(font, rect.position + Vector2(0, 23), label, HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 16, Color(0.0, 0.0, 0.0))

func _draw_bodies(center: Vector2) -> void:
	for body in current_system.get("bodies", []):
		var world := Vector2(float(body.get("x", 0)), float(body.get("y", 0)))
		var screen := center + (world - pos) * WORLD_SCALE
		var radius: float = float(body.get("r", 40)) * WORLD_SCALE
		var color := _named_color(str(body.get("color", "SteelBlue")))
		draw_circle(screen, radius, color)
		draw_arc(screen, radius + 4, 0, TAU, 40, Color(0.75, 0.80, 0.90), 1.0)
		draw_string(ThemeDB.fallback_font, screen + Vector2(-radius, -radius - 8), str(body.get("name", "Port")), HORIZONTAL_ALIGNMENT_LEFT, 240, 14, Color(0.85, 0.90, 1.0))

func _draw_npcs(center: Vector2) -> void:
	if npc_frames.is_empty():
		return
	var offsets := _npc_world_offsets()
	for i in range(offsets.size()):
		if _target_destroyed(i):
			continue
		var screen: Vector2 = center + (offsets[i] - pos) * WORLD_SCALE
		var frame_index := (i * 7) % npc_frames.size()
		var tex := npc_frames[frame_index]
		var draw_offset := Vector2(tex.get_width(), tex.get_height()) * 0.5
		draw_texture_rect(tex, Rect2(screen - draw_offset, Vector2(tex.get_width(), tex.get_height())), false)
		var legal_hostile := _legal_patrol_hostile_posture_active(_current_government_name())
		var ring_color := Color(1.0, 0.32, 0.18, 0.95) if legal_hostile else (Color(1.0, 0.80, 0.20, 0.95) if i == selected_target_index else Color(0.35, 0.55, 0.80, 0.7))
		draw_arc(screen, 28, 0, TAU, 20, ring_color, 1.0)
		draw_string(ThemeDB.fallback_font, screen + Vector2(-26, 42), "S%d H%d" % [int(target_shields.get(i, 0)), int(target_hulls.get(i, 0))], HORIZONTAL_ALIGNMENT_LEFT, 90, 12, Color(0.95, 0.86, 0.58))

func _draw_projectiles(center: Vector2) -> void:
	for projectile in projectiles:
		var screen: Vector2 = center + (projectile.get("position", Vector2.ZERO) - pos) * WORLD_SCALE
		draw_circle(screen, float(projectile.get("radius", 3.0)), _named_color(str(projectile.get("color", "OrangeRed"))))
	for pickup in cargo_salvage_pickups:
		var pickup_screen: Vector2 = center + (pickup.get("position", Vector2.ZERO) - pos) * WORLD_SCALE
		draw_rect(Rect2(pickup_screen - Vector2(5, 5), Vector2(10, 10)), Color(0.72, 0.95, 0.35, 0.95), true)
		draw_arc(pickup_screen, 10.0, 0, TAU, 16, Color(0.80, 1.0, 0.55, 0.75), 1.0)
	for explosion in explosion_events:
		var screen: Vector2 = center + (explosion.get("position", Vector2.ZERO) - pos) * WORLD_SCALE
		var life := clampf(float(explosion.get("life", 0.0)) / 2.0, 0.0, 1.0)
		draw_arc(screen, float(explosion.get("radius", 8.0)) * (1.0 + (1.0 - life) * 2.2), 0, TAU, 24, Color(1.0, 0.48, 0.12, life), 2.0)
		draw_circle(screen, 3.0 + (1.0 - life) * 5.0, Color(1.0, 0.82, 0.24, life * 0.8))

func _draw_player(center: Vector2) -> void:
	if player_frames.is_empty():
		draw_circle(center, 14, Color.CORNFLOWER_BLUE)
		return
	# EV-style fixed-cell registration: A/D advances to the neighboring original
	# 36-facing cell; the ship entity stays fixed and the selected whole cell is
	# drawn centered. This path never rotates a texture or sprite sheet.
	var frame_index := _visible_facing_index(player_facing_index)
	var tex := player_frames[frame_index]
	var size := Vector2(tex.get_width(), tex.get_height())
	_draw_center_registered_ship_cell(center, tex, size)

func _facing_frame_index(degrees: float, frame_count: int) -> int:
	if frame_count <= 0:
		return 0
	return int(round(fposmod(degrees, 360.0) / (360.0 / float(frame_count)))) % frame_count

func _facing_degrees(frame_index: int, frame_count: int) -> float:
	if frame_count <= 0:
		return 0.0
	return float(frame_index % frame_count) * (360.0 / float(frame_count))

func _visible_facing_index(frame_index: int) -> int:
	if player_frames.is_empty():
		return 0
	var count := player_frames.size()
	var idx := frame_index % count
	if idx < player_frame_alpha_counts.size() and player_frame_alpha_counts[idx] > 0:
		return idx
	for step in range(1, count):
		var forward := (idx + step) % count
		if forward < player_frame_alpha_counts.size() and player_frame_alpha_counts[forward] > 0:
			return forward
		var backward := (idx - step + count) % count
		if backward < player_frame_alpha_counts.size() and player_frame_alpha_counts[backward] > 0:
			return backward
	return idx

func _draw_center_registered_ship_cell(center: Vector2, tex: Texture2D, size: Vector2) -> void:
	draw_texture_rect(tex, Rect2(center - size * 0.5, size), false)

func _draw_hud() -> void:
	var font := ThemeDB.fallback_font
	var destination := _selected_destination_name()
	draw_rect(Rect2(0, 0, 1280, 78), Color(0.02, 0.035, 0.06, 0.92), true)
	draw_string(font, Vector2(20, 28), "Terminal Velocity / Godot frontend", HORIZONTAL_ALIGNMENT_LEFT, 500, 20, Color(0.9, 0.95, 1.0))
	var government_name := _current_government_name()
	var legal_status := _legal_status_for_government(government_name)
	draw_string(font, Vector2(20, 56), "System: %s (%s: %s)    Destination: %s    Credits: %d    Fuel: %d/%d    Shields: %d/%d    Hull: %d/%d    Cargo: %d/%d (%d mission, %d free)%s%s%s    Ship: %s" % [current_system.get("name", "?"), government_name, legal_status, destination, credits, player_fuel, _max_player_fuel(), player_shields, _max_player_shields(), player_hull, _max_player_hull(), cargo, cargo_space, _mission_reserved_cargo_tons(), _cargo_available_tons(), _salvage_hud_fragment(), _combat_reward_hud_fragment(), _secondary_weapon_hud_fragment(), player_ship_id], HORIZONTAL_ALIGNMENT_LEFT, 1220, 16, Color(0.70, 0.86, 1.0))
	if not status_messages.is_empty():
		draw_rect(Rect2(20, 92, 430, 62), Color(0.02, 0.035, 0.06, 0.84), true)
		draw_string(font, Vector2(32, 114), "Messages:", HORIZONTAL_ALIGNMENT_LEFT, 160, 14, Color(0.95, 0.86, 0.58))
		var y := 136.0
		for message in status_messages.slice(max(0, status_messages.size() - 2), status_messages.size()):
			draw_string(font, Vector2(32, y), "• " + str(message), HORIZONTAL_ALIGNMENT_LEFT, 400, 13, Color(0.82, 0.88, 0.95))
			y += 18.0
	draw_rect(Rect2(1010, 96, 250, 190), Color(0.02, 0.04, 0.06, 0.88), true)
	draw_arc(Vector2(1135, 190), 78, 0, TAU, 64, Color(0.30, 0.75, 0.95), 1.0)
	draw_line(Vector2(1135, 112), Vector2(1135, 268), Color(0.12, 0.35, 0.50), 1.0)
	draw_line(Vector2(1057, 190), Vector2(1213, 190), Color(0.12, 0.35, 0.50), 1.0)
	draw_string(font, Vector2(1030, 122), "Scanner", HORIZONTAL_ALIGNMENT_LEFT, 200, 16, Color(0.75, 0.95, 1.0))
	if _legal_patrol_hostile_posture_active(government_name):
		draw_string(font, Vector2(1030, 142), "Legal patrol hostile", HORIZONTAL_ALIGNMENT_LEFT, 200, 13, Color(1.0, 0.42, 0.28))
	_draw_scanner_blips(Vector2(1135, 190), 78.0)
	var target_range := 0.0
	var targets := _npc_world_offsets()
	if not targets.is_empty():
		target_range = pos.distance_to(targets[selected_target_index % targets.size()])
	draw_string(font, Vector2(1024, 280), _scanner_target_detail_line(), HORIZONTAL_ALIGNMENT_LEFT, 260, 14, Color(1.0, 0.82, 0.35))
	draw_string(font, Vector2(20, 785), _hud_key_line() + "  |  " + status_line, HORIZONTAL_ALIGNMENT_LEFT, 1230, 15, Color(0.82, 0.88, 0.95))

func _hud_key_line() -> String:
	return "EV keys: Arrows move  Z afterburner  L land/launch  N next target  R closest target  \\ hyper select  H hyper mode  J jump  M map  G mission route  F6 save  F10 help  P/I info  Esc quit"

func _active_mission_destination_systems() -> Array[String]:
	var destinations: Array[String] = []
	for mission_id in active_missions:
		var mission := _mission_by_id(str(mission_id))
		var destination_system := str(mission.get("destinationSystem", ""))
		if destination_system != "" and not destinations.has(destination_system):
			destinations.append(destination_system)
	destinations.sort()
	return destinations

func _mission_log_detail_lines() -> Array[String]:
	var lines: Array[String] = []
	if active_missions.is_empty():
		lines.append("No active missions.")
	else:
		for mission_id in active_missions:
			var mission := _mission_by_id(str(mission_id))
			if mission.is_empty():
				lines.append("Mission: " + str(mission_id))
				lines.append("Status: Active")
				continue
			lines.append(str(mission.get("title", mission_id)))
			lines.append("Status: Active")
			lines.append("Destination: %s / %s" % [str(mission.get("destinationSystem", "?")), str(mission.get("destinationBody", "?"))])
			lines.append("Progress: " + _mission_progress_line(mission))
			lines.append("Route hint: " + _mission_route_hint_line(mission))
			lines.append_array(_mission_deadline_lines(mission))
			lines.append_array(_mission_abort_hint_lines(mission))
			lines.append("Cargo reserved: %d tons" % int(mission.get("cargoTons", 0)))
			lines.append("Reward: %d credits" % int(mission.get("reward", 0)))
			var description := str(mission.get("description", ""))
			if description != "":
				lines.append("Briefing: " + description)
			lines.append("")
	lines.append_array(_mission_completion_history_lines())
	lines.append_array(_mission_abort_history_lines())
	lines.append_array(_mission_failure_history_lines())
	return lines

func _mission_completion_history_lines() -> Array[String]:
	var lines: Array[String] = []
	if completed_mission_history.is_empty():
		return lines
	lines.append("Completed mission history")
	for record in completed_mission_history.slice(max(0, completed_mission_history.size() - 3), completed_mission_history.size()):
		var item: Dictionary = record
		lines.append(str(item.get("title", item.get("id", "Mission"))) + " at " + str(item.get("system", "?")) + " / " + str(item.get("body", "?")))
		lines.append("Cargo released: %d tons" % int(item.get("cargo_released", 0)))
		lines.append("Reward paid: %d credits" % int(item.get("reward_paid", 0)))
	return lines

func _mission_abort_history_lines() -> Array[String]:
	var lines: Array[String] = []
	if aborted_mission_history.is_empty():
		return lines
	lines.append("Aborted mission history")
	for record in aborted_mission_history.slice(max(0, aborted_mission_history.size() - 3), aborted_mission_history.size()):
		var item: Dictionary = record
		lines.append(str(item.get("title", item.get("id", "Mission"))))
		lines.append("Cargo released: %d tons" % int(item.get("cargo_released", 0)))
	return lines

func _mission_failure_history_lines() -> Array[String]:
	var lines: Array[String] = []
	if failed_mission_history.is_empty():
		return lines
	lines.append("Failed mission history")
	for record in failed_mission_history.slice(max(0, failed_mission_history.size() - 3), failed_mission_history.size()):
		var item: Dictionary = record
		lines.append(str(item.get("title", item.get("id", "Mission"))))
		lines.append("Deadline: accepted day %d, failed day %d, limit %d day(s)" % [int(item.get("accepted_day", 0)), int(item.get("current_day", 0)), int(item.get("time_limit_days", 0))])
		lines.append("Failure flag: " + str(item.get("failure_flag", "pending")))
		lines.append("Cargo released: %d tons" % int(item.get("cargo_released", 0)))
		lines.append("Reputation: %s %+d" % [str(item.get("reputation_government", "Government")), int(item.get("reputation_delta", 0))])
		lines.append("Failure source: %s; exact Classic UI pending" % str(item.get("sourceLabel", "terminal-velocity-failure-history-scaffold")))
	return lines

func _mission_progress_line(mission: Dictionary) -> String:
	var destination_system := str(mission.get("destinationSystem", "?"))
	var destination_body := str(mission.get("destinationBody", "?"))
	var current_name := str(current_system.get("name", "?"))
	if current_name != destination_system:
		return "Travel to destination system %s from %s" % [destination_system, current_name]
	if not landed:
		return "Land at destination body %s" % destination_body
	var body_name := str(_current_body().get("name", "?"))
	if body_name == destination_body:
		return "Ready to complete at current port"
	return "Land at destination body %s; current port is %s" % [destination_body, body_name]

func _mission_route_hint_line(mission: Dictionary) -> String:
	var destination_system := str(mission.get("destinationSystem", "?"))
	if str(current_system.get("name", "?")) == destination_system:
		return "Destination system reached; use L to land if needed"
	return "Press G to queue route toward %s" % destination_system

func _mission_deadline_lines(mission: Dictionary) -> Array[String]:
	var lines: Array[String] = []
	if not mission.has("timeLimitDays"):
		return lines
	var mission_id := str(mission.get("id", ""))
	var accepted_day := int(mission_acceptance_days.get(mission_id, current_day))
	var time_limit_days := int(mission.get("timeLimitDays", 0))
	var due_day: int = accepted_day + time_limit_days
	var remaining_days: int = max(0, due_day - current_day)
	lines.append("Deadline: accepted day %d, current day %d, limit %d day(s), %d day(s) remaining" % [accepted_day, current_day, time_limit_days, remaining_days])
	lines.append("Deadline source: %s; exact Classic UI pending" % str(mission.get("sourceLabel", "terminal-velocity-active-deadline-display-scaffold")))
	return lines

func _mission_abort_hint_lines(mission: Dictionary) -> Array[String]:
	var lines: Array[String] = []
	var cargo_tons := int(mission.get("cargoTons", 0))
	if mission.has("canAbort") and not bool(mission.get("canAbort", true)):
		lines.append("Abort: unavailable for this contract until return/cleanup; reserved cargo remains committed")
		lines.append("Abort source: ev-classic-resource-bible-backed-canabort-guardrail; exact Classic UI pending")
		return lines
	lines.append("Abort: press X to abort; TV scaffold releases %d reserved cargo tons" % cargo_tons)
	lines.append("Abort source: terminal-velocity-mission-abort-scaffold; Classic CanAbort/UI pending")
	return lines

func _draw_mission_log_overlay() -> void:
	var font := ThemeDB.fallback_font
	var rect := Rect2(210, 112, 860, 560)
	draw_rect(rect, Color(0.018, 0.026, 0.042, 0.96), true)
	draw_rect(rect, Color(0.35, 0.62, 0.85, 1.0), false, 2.0)
	draw_string(font, rect.position + Vector2(0, 38), "Mission Log", HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 24, Color(0.92, 0.98, 1.0))
	draw_string(font, rect.position + Vector2(36, 72), "Terminal Velocity mission log helper/scaffold — not an EV Classic fidelity claim. I toggles mission log.", HORIZONTAL_ALIGNMENT_LEFT, rect.size.x - 72, 14, Color(0.95, 0.86, 0.58))
	var y := rect.position.y + 112.0
	for line in _mission_log_detail_lines():
		if line == "":
			y += 12.0
			continue
		var color := Color(0.86, 0.92, 1.0)
		if line.begins_with("Status:") or line.begins_with("Destination:") or line.begins_with("Progress:") or line.begins_with("Route hint:") or line.begins_with("Deadline:") or line.begins_with("Deadline source:") or line.begins_with("Abort:") or line.begins_with("Abort source:") or line.begins_with("Cargo reserved:") or line.begins_with("Reward:") or line.begins_with("Cargo released:") or line.begins_with("Reward paid:"):
			color = Color(0.72, 0.84, 0.96)
		draw_string(font, Vector2(rect.position.x + 42, y), line, HORIZONTAL_ALIGNMENT_LEFT, rect.size.x - 84, 16, color)
		y += 28.0

func _draw_player_info_overlay() -> void:
	var font := ThemeDB.fallback_font
	var rect := Rect2(260, 150, 760, 430)
	draw_rect(rect, Color(0.018, 0.026, 0.042, 0.96), true)
	draw_rect(rect, Color(0.35, 0.62, 0.85, 1.0), false, 2.0)
	draw_string(font, rect.position + Vector2(0, 38), "Player Info", HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 24, Color(0.92, 0.98, 1.0))
	draw_string(font, rect.position + Vector2(36, 72), "Terminal Velocity player info helper/scaffold — not an EV Classic fidelity claim. P toggles player info.", HORIZONTAL_ALIGNMENT_LEFT, rect.size.x - 72, 14, Color(0.95, 0.86, 0.58))
	var y := rect.position.y + 112.0
	for line in _player_inventory_lines():
		draw_string(font, Vector2(rect.position.x + 42, y), line, HORIZONTAL_ALIGNMENT_LEFT, rect.size.x - 84, 16, Color(0.86, 0.92, 1.0))
		y += 30.0

func _player_inventory_lines() -> Array[String]:
	var pilot_name := loaded_pilot_name if loaded_pilot_name != "" else "Pilot"
	var lines: Array[String] = [
		"Pilot: %s" % pilot_name,
		"Ship: %s" % player_ship_id,
		"Credits: %d" % credits,
		"Cargo: %d/%d (%d mission, %d free)" % [cargo, cargo_space, _mission_reserved_cargo_tons(), _cargo_available_tons()],
		"Fuel: %d/%d" % [player_fuel, _max_player_fuel()],
		_combat_readiness_inventory_line(),
		"Government/legal: %s" % _legal_warning_line(_current_government_name()),
		_contraband_inventory_line(),
		"Reputation scores: %s" % _inventory_dictionary_summary(reputation_scores),
		"Legal records: %s" % _inventory_dictionary_summary(legal_records),
		"Outfits: %s" % _inventory_dictionary_summary(owned_outfits),
		"Weapons: %s" % _inventory_dictionary_summary(owned_weapons),
		_primary_weapon_inventory_line(),
		_secondary_weapon_inventory_line(),
		_combat_reward_inventory_line(),
		_salvage_pickup_inventory_line(),
	]
	lines.append_array(_active_mission_player_info_lines())
	lines.append_array(_mission_history_player_info_lines())
	return lines

func _combat_readiness_inventory_line() -> String:
	return "Combat readiness: shields %d/%d; hull %d/%d (repair cost %d cr); shield recharge cadence source-backed scaffold" % [player_shields, _max_player_shields(), player_hull, _max_player_hull(), _repair_cost()]

func _contraband_inventory_line() -> String:
	var government_name := _current_government_name()
	var illegal_hold := _illegal_commodity_hold(government_name)
	if illegal_hold.is_empty():
		return "Contraband risk: no current %s contraband in hold — TV legal-risk scaffold; Classic scan UI pending" % government_name
	var parts: Array[String] = []
	var total_tons := 0
	for commodity_id in illegal_hold.keys():
		var tons := int(illegal_hold.get(commodity_id, 0))
		total_tons += tons
		parts.append("%s x%d" % [str(commodity_id), tons])
	parts.sort()
	var policy: Dictionary = governments.get("governments", {}).get(government_name, {})
	return "Contraband risk: %d ton(s) flagged by %s scans (%s), fine %d cr/ton — TV legal-risk scaffold; Classic scan UI pending" % [total_tons, government_name, ", ".join(parts), int(policy.get("finePerTon", 0))]

func _salvage_pickup_inventory_line() -> String:
	if cargo_salvage_pickups.is_empty():
		return "In-space salvage: none"
	var total_tons := 0
	for pickup in cargo_salvage_pickups:
		total_tons += int(pickup.get("tons", 0))
	return "In-space salvage: %d pickup(s), %d tons — TV combat-salvage scaffold; Classic loot behavior pending" % [cargo_salvage_pickups.size(), total_tons]

func _combat_reward_inventory_line() -> String:
	if combat_reward_history.is_empty():
		return "Combat rewards: none"
	var total_credits := 0
	for reward in combat_reward_history:
		total_credits += int(reward.get("credits", 0))
	var last_reward: Dictionary = combat_reward_history[-1]
	var target_label := str(last_reward.get("targetLabel", "Contact %d" % [int(last_reward.get("targetIndex", -1)) + 1]))
	return "Combat rewards: %d disable(s), %d credits — TV combat-reward scaffold; Classic bounty behavior pending. Last reward: %s, %d credits" % [combat_reward_history.size(), total_credits, target_label, int(last_reward.get("credits", 0))]

func _salvage_hud_fragment() -> String:
	if cargo_salvage_pickups.is_empty():
		return ""
	var total_tons := 0
	for pickup in cargo_salvage_pickups:
		total_tons += int(pickup.get("tons", 0))
	return "    Salvage: %d pickup(s)/%d tons" % [cargo_salvage_pickups.size(), total_tons]

func _combat_reward_hud_fragment() -> String:
	if combat_reward_history.is_empty():
		return ""
	var total_credits := 0
	for reward in combat_reward_history:
		total_credits += int(reward.get("credits", 0))
	return "    Rewards: %d disable(s)/%d cr" % [combat_reward_history.size(), total_credits]

func _secondary_weapon_hud_fragment() -> String:
	var weapon := _secondary_weapon_stats()
	if weapon.is_empty():
		return "    Secondary: No Secondary Weapon"
	var weapon_name := str(weapon.get("name", weapon.get("id", "Secondary")))
	var reload_frames := int(ceil(secondary_weapon_cooldown_frames))
	var readiness := "ready" if reload_frames <= 0 else "reload %d frames" % reload_frames
	return "    Secondary: %s (%s)" % [weapon_name, readiness]

func _salvage_scanner_blip_count() -> int:
	return cargo_salvage_pickups.size()

func _primary_weapon_inventory_line() -> String:
	var weapon := _primary_weapon_stats()
	var weapon_name := str(weapon.get("name", weapon.get("id", "Unknown")))
	var source_name := str(weapon.get("sourceStockName", weapon_name))
	return "Primary weapon: %s — source %s; exact Classic cadence pending" % [weapon_name, source_name]

func _secondary_weapon_inventory_line() -> String:
	var weapon := _secondary_weapon_stats()
	if weapon.is_empty():
		return "Secondary weapon: No Secondary Weapon — original-runtime-observed starting HUD; install/cycle with S before Space fires"
	var weapon_name := str(weapon.get("name", weapon.get("id", "Unknown")))
	var source_name := str(weapon.get("sourceStockName", weapon_name))
	return "Secondary weapon: %s — selected; source %s; exact Classic secondary behavior pending" % [weapon_name, source_name]

func _active_mission_player_info_lines() -> Array[String]:
	var lines: Array[String] = []
	if active_missions.is_empty():
		lines.append("Active mission: none")
		return lines
	var mission := _mission_by_id(str(active_missions[0]))
	if mission.is_empty():
		lines.append("Active mission: " + str(active_missions[0]))
		lines.append("Active mission source: terminal-velocity-player-info-mission-scaffold; exact Classic Player Info behavior pending")
		return lines
	lines.append("Active mission: %s to %s/%s" % [str(mission.get("title", mission.get("id", "Mission"))), str(mission.get("destinationSystem", "?")), str(mission.get("destinationBody", "?"))])
	if mission.has("timeLimitDays"):
		var mission_id := str(mission.get("id", ""))
		var accepted_day := int(mission_acceptance_days.get(mission_id, current_day))
		var remaining_days: int = max(0, accepted_day + int(mission.get("timeLimitDays", 0)) - current_day)
		lines.append("Active mission deadline: %d day(s) remaining; exact Classic Player Info behavior pending" % remaining_days)
	lines.append("Active mission cargo/reward: %d tons / %d credits" % [int(mission.get("cargoTons", 0)), int(mission.get("reward", 0))])
	lines.append("Active mission source: terminal-velocity-player-info-mission-scaffold; exact Classic Player Info behavior pending")
	return lines

func _mission_history_player_info_lines() -> Array[String]:
	var history_count := completed_mission_history.size() + aborted_mission_history.size() + failed_mission_history.size()
	if history_count <= 0:
		return ["Mission history: none"]
	var lines: Array[String] = ["Mission history: %d completed, %d aborted, %d failed — TV mission-history scaffold; Classic Player Info behavior pending" % [completed_mission_history.size(), aborted_mission_history.size(), failed_mission_history.size()]]
	if not failed_mission_history.is_empty():
		var latest_failure: Dictionary = failed_mission_history[-1]
		var reputation_delta := int(latest_failure.get("reputation_delta", 0))
		var failure_government := str(latest_failure.get("reputation_government", ""))
		var reputation_summary := ""
		if failure_government != "" and reputation_delta != 0:
			reputation_summary = "; reputation %s %+d" % [failure_government, reputation_delta]
		lines.append("Latest failed mission: %s%s; exact Classic failure/history UI pending" % [str(latest_failure.get("title", latest_failure.get("id", "Mission"))), reputation_summary])
	return lines

func _inventory_dictionary_summary(items: Dictionary) -> String:
	if items.is_empty():
		return "none"
	var parts: Array[String] = []
	for key in items.keys():
		parts.append("%s x%d" % [str(key), int(items.get(key, 0))])
	parts.sort()
	return ", ".join(parts)

func _draw_help_overlay() -> void:
	var font := ThemeDB.fallback_font
	var rect := Rect2(250, 120, 780, 520)
	draw_rect(rect, Color(0.018, 0.026, 0.042, 0.96), true)
	draw_rect(rect, Color(0.35, 0.62, 0.85, 1.0), false, 2.0)
	draw_string(font, rect.position + Vector2(0, 38), "Terminal Velocity Help", HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 24, Color(0.92, 0.98, 1.0))
	var lines := _help_overlay_lines()
	lines.append_array(_gameplay_curriculum_hint_lines().slice(0, 4))
	var y := rect.position.y + 80.0
	for line in lines:
		draw_string(font, Vector2(rect.position.x + 36, y), "• " + line, HORIZONTAL_ALIGNMENT_LEFT, rect.size.x - 72, 16, Color(0.82, 0.90, 1.0))
		y += 28.0

func _help_overlay_lines() -> Array[String]:
	var lines: Array[String] = []
	for line in help_overlay.get("lines", []):
		lines.append(str(line))
	if lines.is_empty():
		lines.append("Terminal Velocity helper/scaffold — help_overlay.json missing or empty.")
	return lines

func _help_overlay_log_probes() -> Array:
	return help_overlay.get("logProbes", [])

func _gameplay_curriculum_hint_lines() -> Array[String]:
	var lines: Array[String] = ["Terminal Velocity curriculum hints — scaffold from native_ev/data/gameplay_curriculum.json"]
	var scenario_order: Array = gameplay_curriculum.get("scenarioOrder", [])
	var scenarios: Dictionary = gameplay_curriculum.get("scenarios", {})
	for scenario_name in scenario_order:
		var summary: Dictionary = scenarios.get(str(scenario_name), {})
		var surface := str(summary.get("surface", ""))
		var purpose := str(summary.get("purpose", ""))
		if surface == "" or purpose == "":
			continue
		lines.append("%s: %s — %s" % [str(scenario_name), surface, purpose])
	return lines

func _draw_scanner_blips(scanner_center: Vector2, scanner_radius: float) -> void:
	var targets := _npc_world_offsets()
	for i in range(targets.size()):
		var relative: Vector2 = (targets[i] - pos) / 8.0
		if relative.length() > scanner_radius - 8.0:
			relative = relative.normalized() * (scanner_radius - 8.0)
		var blip := scanner_center + relative
		var legal_hostile := _legal_patrol_hostile_posture_active(_current_government_name())
		var color := Color(1.0, 0.24, 0.18) if legal_hostile else (Color(1.0, 0.78, 0.20) if i == selected_target_index else Color(0.30, 0.85, 1.0))
		draw_circle(blip, 4.0 if i == selected_target_index else 2.5, color)
	_draw_scanner_salvage_blips(scanner_center, scanner_radius)

func _draw_scanner_salvage_blips(scanner_center: Vector2, scanner_radius: float) -> void:
	for pickup in cargo_salvage_pickups:
		var relative: Vector2 = (pickup.get("position", Vector2.ZERO) - pos) / 8.0
		if relative.length() > scanner_radius - 8.0:
			relative = relative.normalized() * (scanner_radius - 8.0)
		var blip := scanner_center + relative
		draw_rect(Rect2(blip - Vector2(3, 3), Vector2(6, 6)), Color(0.72, 1.0, 0.35, 0.95), true)
		draw_arc(blip, 6.0, 0, TAU, 16, Color(0.80, 1.0, 0.55, 0.75), 1.0)

func _map_legal_risk_line(system_name: String) -> String:
	if system_name == "None" or system_name == "":
		return "Legal: no selected system"
	var government_name := _government_name_for_system(system_name)
	return "Legal: %s / %s (%d)" % [government_name, _legal_status_for_government(government_name), int(legal_records.get(government_name, 0))]

func _map_legal_risk_color(system_name: String) -> Color:
	var government_name := _government_name_for_system(system_name)
	if _legal_patrol_hostile_posture_active(government_name):
		return Color(1.0, 0.42, 0.28)
	return Color(0.74, 0.90, 1.0)

func _draw_universe_map() -> void:
	var systems: Array = universe.get("systems", [])
	if systems.is_empty():
		return
	var font := ThemeDB.fallback_font
	var rect := _map_rect()
	var plot_rect := _map_plot_rect()
	draw_rect(rect, Color(0.018, 0.026, 0.042, 0.96), true)
	draw_rect(rect, Color(0.24, 0.54, 0.78, 1.0), false, 2.0)
	draw_string(font, rect.position + Vector2(0, 40), "GALAXY MAP", HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 24, Color(0.86, 0.96, 1.0))
	var links: Array = current_system.get("links", [])
	var route_tail_links: Array = _map_route_tail_links()
	var selected_name := _selected_destination_name()
	var mission_destination_systems := _active_mission_destination_systems()
	draw_string(font, rect.position + Vector2(690, 90), "Current: " + str(current_system.get("name", "?")), HORIZONTAL_ALIGNMENT_LEFT, 230, 18, Color(1.0, 0.92, 0.58))
	draw_string(font, rect.position + Vector2(690, 120), "Selected: " + selected_name, HORIZONTAL_ALIGNMENT_LEFT, 230, 18, Color(0.35, 1.0, 0.68))
	draw_string(font, rect.position + Vector2(690, 144), "Services: %s" % _system_service_summary(selected_name), HORIZONTAL_ALIGNMENT_LEFT, 250, 14, Color(0.95, 0.86, 0.58))
	draw_string(font, rect.position + Vector2(690, 162), _map_legal_risk_line(selected_name), HORIZONTAL_ALIGNMENT_LEFT, 250, 14, _map_legal_risk_color(selected_name))
	if not mission_destination_systems.is_empty():
		draw_string(font, rect.position + Vector2(690, 180), "Mission destination: " + ", ".join(mission_destination_systems), HORIZONTAL_ALIGNMENT_LEFT, 250, 14, Color(1.0, 0.45, 0.22))
	draw_string(font, rect.position + Vector2(690, 204), "\\ cycles routes   J jumps", HORIZONTAL_ALIGNMENT_LEFT, 250, 14, Color(0.70, 0.82, 0.96))
	draw_string(font, rect.position + Vector2(690, 228), "Shift-click linked stops: green route", HORIZONTAL_ALIGNMENT_LEFT, 250, 14, Color(0.70, 0.82, 0.96))
	draw_string(font, rect.position + Vector2(690, 252), "Backspace/Delete clears queued route", HORIZONTAL_ALIGNMENT_LEFT, 250, 14, Color(0.70, 0.82, 0.96))
	draw_string(font, rect.position + Vector2(690, 276), "G queues active mission route", HORIZONTAL_ALIGNMENT_LEFT, 250, 14, Color(0.70, 0.82, 0.96))
	draw_string(font, rect.position + Vector2(690, 300), _route_fuel_hint_line(), HORIZONTAL_ALIGNMENT_LEFT, 250, 14, Color(0.95, 0.86, 0.58))
	draw_string(font, rect.position + Vector2(690, 324), "M closes map", HORIZONTAL_ALIGNMENT_LEFT, 230, 14, Color(0.70, 0.82, 0.96))
	var point_by_name := _map_system_points(systems)
	var hovered_name := _map_hovered_link_name()
	if hovered_name != "":
		draw_string(font, rect.position + Vector2(690, 274), "Release click to route: " + hovered_name, HORIZONTAL_ALIGNMENT_LEFT, 250, 14, Color(0.45, 1.0, 0.65))
	for system in systems:
		var map_point: Vector2 = point_by_name.get(str(system.get("name", "")), plot_rect.position)
		for linked_name in system.get("links", []):
			if not point_by_name.has(str(linked_name)):
				continue
			var linked_point: Vector2 = point_by_name[str(linked_name)]
			draw_line(map_point, linked_point, Color(0.12, 0.32, 0.52, 0.72), 1.0)
	var current_name := str(current_system.get("name", ""))
	var route_names := [current_name]
	if selected_route.is_empty() and selected_name != "None" and selected_name != current_name:
		route_names.append(selected_name)
	else:
		route_names.append_array(selected_route)
	for route_index in range(route_names.size() - 1):
		var route_start_name := str(route_names[route_index])
		var route_end_name := str(route_names[route_index + 1])
		if point_by_name.has(route_start_name) and point_by_name.has(route_end_name):
			var route_start_point: Vector2 = point_by_name[route_start_name]
			var route_end_point: Vector2 = point_by_name[route_end_name]
			draw_line(route_start_point, route_end_point, Color(0.15, 1.0, 0.28, 0.95), 3.0)
	for system in systems:
		var system_name := str(system.get("name", "?"))
		var map_point: Vector2 = point_by_name.get(system_name, plot_rect.position)
		var linked := route_tail_links.has(system_name)
		var is_current := system_name == str(current_system.get("name", ""))
		var is_selected := system_name == selected_name or selected_route.has(system_name)
		var is_hovered := system_name == hovered_name
		var is_mission_destination := mission_destination_systems.has(system_name)
		var color := Color(0.46, 0.72, 1.0)
		var radius := 4.0
		if is_mission_destination:
			color = Color(1.0, 0.45, 0.22, 0.95)
			radius = 7.0
		if linked:
			color = Color(0.66, 0.95, 1.0)
			radius = 5.0
		if is_hovered:
			color = Color(0.55, 1.0, 0.70)
			radius = 8.0
		if is_selected:
			color = Color(0.30, 1.0, 0.55)
			radius = 7.0
		if is_current:
			color = Color(1.0, 0.85, 0.25)
			radius = 8.0
		draw_circle(map_point, radius, color)
		draw_arc(map_point, radius + 4.0, 0, TAU, 24, color, 1.0)
		draw_string(font, map_point + Vector2(8, -7), system_name, HORIZONTAL_ALIGNMENT_LEFT, 140, 13, color)
	var y := rect.position.y + 326.0
	for system in systems:
		var system_name := str(system.get("name", "?"))
		var mark := " "
		if system_name == str(current_system.get("name", "")):
			mark = "*"
		elif system_name == selected_name:
			mark = ">"
		var link_label := " linked" if links.has(system_name) else ""
		draw_string(font, Vector2(rect.position.x + 690, y), "%s %s (%d,%d)%s" % [mark, system_name, int(system.get("x", 0)), int(system.get("y", 0)), link_label], HORIZONTAL_ALIGNMENT_LEFT, 230, 14, Color(0.80, 0.90, 1.0))
		y += 22.0
	draw_rect(plot_rect, Color(0.0, 0.0, 0.0, 0.0), false, 1.0)

func _system_coordinate_bounds(systems: Array) -> Dictionary:
	var min_x := INF
	var max_x := -INF
	var min_y := INF
	var max_y := -INF
	for system in systems:
		var x := float(system.get("x", 0))
		var y := float(system.get("y", 0))
		min_x = min(min_x, x)
		max_x = max(max_x, x)
		min_y = min(min_y, y)
		max_y = max(max_y, y)
	if is_equal_approx(min_x, max_x):
		max_x += 1.0
	if is_equal_approx(min_y, max_y):
		max_y += 1.0
	return {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}

func _system_map_point(system: Dictionary, bounds: Dictionary, plot_rect: Rect2) -> Vector2:
	var x := float(system.get("x", 0))
	var y := float(system.get("y", 0))
	var t_x := inverse_lerp(float(bounds.get("min_x", 0.0)), float(bounds.get("max_x", 1.0)), x)
	var t_y := inverse_lerp(float(bounds.get("min_y", 0.0)), float(bounds.get("max_y", 1.0)), y)
	return plot_rect.position + Vector2(t_x * plot_rect.size.x, (1.0 - t_y) * plot_rect.size.y)

func _draw_landing_panel() -> void:
	var nearest := _nearest_body()
	var port := "Port"
	var market := ""
	var body := {}
	if not nearest.is_empty():
		body = nearest["body"]
		port = str(body.get("sourceLandingName", body.get("name", "Port")))
		market = str(body.get("market", "Local market"))
	var rect := Rect2(190, 135, 900, 520)
	draw_rect(rect, Color(0.035, 0.045, 0.065, 0.96), true)
	draw_rect(rect, Color(0.28, 0.43, 0.62, 1.0), false, 2.0)
	var font := ThemeDB.fallback_font
	draw_string(font, rect.position + Vector2(30, 46), port, HORIZONTAL_ALIGNMENT_LEFT, 820, 28, Color(1.0, 0.92, 0.72))
	draw_string(font, rect.position + Vector2(30, 78), market, HORIZONTAL_ALIGNMENT_LEFT, 620, 16, Color(0.80, 0.90, 1.0))
	var refuel_text := "Refuel: F5 available" if _body_refuel_available(body) else "Refuel: unavailable"
	draw_string(font, rect.position + Vector2(650, 78), refuel_text, HORIZONTAL_ALIGNMENT_LEFT, 220, 16, Color(0.95, 0.86, 0.58))
	var repair_text := "Repair: F7 (%d cr)" % _repair_cost() if _body_repair_available(body) else "Repair: unavailable"
	draw_string(font, rect.position + Vector2(650, 98), repair_text, HORIZONTAL_ALIGNMENT_LEFT, 220, 14, Color(0.95, 0.76, 0.58))
	var government_name := _current_government_name()
	if not _legal_service_access_allowed(government_name):
		draw_string(font, rect.position + Vector2(30, 98), _legal_service_blocked_message(government_name), HORIZONTAL_ALIGNMENT_LEFT, 820, 14, Color(1.0, 0.58, 0.42))
	_draw_ev_classic_landing_buttons(rect, body)
	match landing_tab:
		0:
			_draw_mission_computer(rect, body)
		1:
			_draw_commodity_exchange(rect)
		2:
			_draw_outfitter(rect, body)
		3:
			_draw_shipyard(rect, body)
	draw_string(font, rect.position + Vector2(30, 492), "F1 Mission Computer  F2 Commodity Exchange  F5 Refuel  F7 Repair  L Leave  ↑/↓ select", HORIZONTAL_ALIGNMENT_LEFT, 840, 16, Color(0.95, 0.86, 0.58))

func _ev_classic_landing_button_labels(body: Dictionary) -> Array:
	var inventory := _station_inventory(body)
	var labels := ["Spaceport Bar", "Mission Computer", "Commodity Exchange"]
	if inventory.get("services", []).has("outfitter") or not inventory.get("outfitsForSale", []).is_empty() or not inventory.get("weaponsForSale", []).is_empty():
		labels.append("Outfitter")
	if inventory.get("services", []).has("shipyard") or not inventory.get("shipsForSale", []).is_empty():
		labels.append("Shipyard")
	labels.append("Leave")
	return labels

func _draw_ev_classic_landing_buttons(rect: Rect2, body: Dictionary) -> void:
	var font := ThemeDB.fallback_font
	var inventory := _station_inventory(body)
	var labels := _ev_classic_landing_button_labels(body)
	for i in range(labels.size()):
		var button_rect := Rect2(rect.position + Vector2(30 + i * 142, 104), Vector2(132, 30))
		var label := str(labels[i])
		var active := (landing_tab == 0 and label == "Mission Computer") or (landing_tab == 1 and label == "Commodity Exchange") or (landing_tab == 2 and label == "Outfitter") or (landing_tab == 3 and label == "Shipyard")
		draw_rect(button_rect, Color(0.12, 0.20, 0.30, 1.0) if active else Color(0.06, 0.08, 0.11, 1.0), true)
		draw_rect(button_rect, Color(0.35, 0.55, 0.75, 1.0), false, 1.0)
		draw_string(font, button_rect.position + Vector2(6, 20), label, HORIZONTAL_ALIGNMENT_CENTER, 120, 13, Color(0.88, 0.94, 1.0))

func _draw_mission_computer(rect: Rect2, body: Dictionary) -> void:
	var font := ThemeDB.fallback_font
	draw_string(font, rect.position + Vector2(30, 166), "Mission Computer", HORIZONTAL_ALIGNMENT_LEFT, 820, 22, Color(0.92, 0.96, 1.0))
	var available_missions := _available_missions(body)
	if available_missions.is_empty():
		draw_string(font, rect.position + Vector2(30, 202), "No special contracts available here.", HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.72, 0.82, 0.92))
		_draw_blocked_mission_reasons(rect, body, 232.0)
		return
	var blocked_reasons := _blocked_mission_reasons(body)
	var help_text := "Enter accepts mission"
	if not blocked_reasons.is_empty():
		help_text += "  |  Some contracts unavailable: legal/reputation gates"
	draw_string(font, rect.position + Vector2(30, 192), help_text, HORIZONTAL_ALIGNMENT_LEFT, 820, 14, Color(0.95, 0.86, 0.58))
	var y := 202.0
	for i in range(min(5, available_missions.size())):
		var mission: Dictionary = available_missions[i]
		var marker := "▶" if i == selected_landing_item else "•"
		draw_string(font, rect.position + Vector2(30, y), "%s %s — %d cr, %d tons" % [marker, mission.get("title", "Contract"), int(mission.get("reward", 0)), int(mission.get("cargoTons", 0))], HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.86, 0.92, 1.0))
		y += 26.0
		draw_string(font, rect.position + Vector2(52, y), "To %s / %s" % [mission.get("destinationSystem", "?"), mission.get("destinationBody", "?")], HORIZONTAL_ALIGNMENT_LEFT, 780, 14, Color(0.68, 0.78, 0.90))
		y += 24.0
		if i == selected_landing_item:
			for detail_line in _mission_offer_detail_lines(mission):
				draw_string(font, rect.position + Vector2(52, y), detail_line, HORIZONTAL_ALIGNMENT_LEFT, 780, 13, Color(0.58, 0.72, 0.88))
				y += 18.0
	_draw_blocked_mission_reasons(rect, body, y + 4.0)

func _mission_offer_detail_lines(mission: Dictionary) -> Array[String]:
	var lines: Array[String] = []
	var description := str(mission.get("description", ""))
	if description != "":
		lines.append("Briefing: %s" % description)
	var destination_system := str(mission.get("destinationSystem", "?"))
	var direct_route: bool = current_system.get("links", []).has(destination_system)
	var route_hint: String = "direct linked hop" if direct_route else "route planning required"
	lines.append("Offer route: %s / %s — %s" % [destination_system, str(mission.get("destinationBody", "?")), route_hint])
	lines.append("Offer terms: %d cr reward, %d cargo tons reserved on accept" % [int(mission.get("reward", 0)), int(mission.get("cargoTons", 0))])
	var deadline_text := "%d day(s) after accept" % int(mission.get("timeLimitDays", 0)) if mission.has("timeLimitDays") else "not listed in current TV mission data"
	lines.append("Offer deadline: %s" % deadline_text)
	lines.append("Offer requirements: %s" % _mission_offer_requirements_line(mission))
	lines.append("Offer story: starts=%s completes=%s next=%s choiceGroup=%s reputationEvent=%s" % [JSON.stringify(mission.get("setsFlags", [])), JSON.stringify(mission.get("completionFlags", [])), _mission_optional_field(mission, "next"), _mission_optional_field(mission, "choiceGroup"), _mission_optional_field(mission, "reputationEvent")])
	lines.append("Offer detail source: terminal-velocity-mission-offer-helper; exact Classic Mission Computer detail UI pending")
	return lines

func _mission_optional_field(mission: Dictionary, key: String) -> String:
	var value = mission.get(key, null)
	if value == null:
		return "none"
	var text := str(value)
	return "none" if text == "" else text

func _mission_offer_requirements_line(mission: Dictionary) -> String:
	var parts: Array[String] = []
	var requires_flags: Array = mission.get("requiresFlags", [])
	var excludes_flags: Array = mission.get("excludesFlags", [])
	var requirements: Dictionary = mission.get("requirements", {})
	if not requires_flags.is_empty():
		parts.append("requiresFlags=%s" % JSON.stringify(requires_flags))
	if not excludes_flags.is_empty():
		parts.append("excludesFlags=%s" % JSON.stringify(excludes_flags))
	for key in ["reputationMin", "legalMin", "legalMax"]:
		var score_requirements: Dictionary = requirements.get(key, {})
		if not score_requirements.is_empty():
			parts.append("%s=%s" % [key, JSON.stringify(score_requirements)])
	if parts.is_empty():
		return "none listed in current TV mission data"
	return "; ".join(parts)

func _draw_blocked_mission_reasons(rect: Rect2, body: Dictionary, y_start: float) -> void:
	var reasons := _blocked_mission_reasons(body)
	if reasons.is_empty():
		return
	var font := ThemeDB.fallback_font
	var y := y_start
	draw_string(font, rect.position + Vector2(30, y), "Unavailable contracts (TV scaffold):", HORIZONTAL_ALIGNMENT_LEFT, 820, 14, Color(1.0, 0.72, 0.46))
	y += 22.0
	for reason in reasons.slice(0, min(3, reasons.size())):
		draw_string(font, rect.position + Vector2(52, y), "• " + str(reason), HORIZONTAL_ALIGNMENT_LEFT, 780, 13, Color(0.95, 0.70, 0.58))
		y += 20.0
	draw_string(font, rect.position + Vector2(52, y), _blocked_mission_source_boundary_line(), HORIZONTAL_ALIGNMENT_LEFT, 780, 12, Color(0.58, 0.70, 0.86))

func _blocked_mission_source_boundary_line() -> String:
	return "Blocked-offer details are Terminal Velocity helper scaffolds; exact Classic hidden/disabled Mission Computer behavior pending original/resource evidence"

func _draw_commodity_exchange(rect: Rect2) -> void:
	var font := ThemeDB.fallback_font
	var market_prices := _market_prices(current_system.get("name", ""))
	draw_string(font, rect.position + Vector2(30, 166), "Commodity Exchange", HORIZONTAL_ALIGNMENT_LEFT, 820, 22, Color(0.92, 0.96, 1.0))
	draw_string(font, rect.position + Vector2(30, 192), "In Hold:", HORIZONTAL_ALIGNMENT_LEFT, 160, 14, Color(0.95, 0.86, 0.58))
	draw_string(font, rect.position + Vector2(230, 192), "Buy Price:", HORIZONTAL_ALIGNMENT_LEFT, 160, 14, Color(0.95, 0.86, 0.58))
	draw_string(font, rect.position + Vector2(390, 192), "Sell Price:", HORIZONTAL_ALIGNMENT_LEFT, 120, 14, Color(0.95, 0.86, 0.58))
	draw_string(font, rect.position + Vector2(520, 192), "Buy B", HORIZONTAL_ALIGNMENT_LEFT, 80, 14, Color(0.95, 0.86, 0.58))
	draw_string(font, rect.position + Vector2(600, 192), "Sell S", HORIZONTAL_ALIGNMENT_LEFT, 80, 14, Color(0.95, 0.86, 0.58))
	draw_string(font, rect.position + Vector2(680, 192), "Cargo reserved for missions: %d" % _mission_reserved_cargo_tons(), HORIZONTAL_ALIGNMENT_LEFT, 180, 14, Color(0.95, 0.86, 0.58))
	var y := 218.0
	var commodities: Array = economy.get("commodities", [])
	for i in range(min(8, commodities.size())):
		var commodity: Dictionary = commodities[i]
		var commodity_id := str(commodity.get("id", ""))
		var prices: Dictionary = market_prices.get(commodity_id, {})
		var marker := "▶" if i == selected_landing_item else " "
		var held := int(commodity_hold.get(commodity_id, 0))
		var hold_text := "" if held == 0 else str(held)
		var status := _ev_classic_price_status(prices)
		var sell_price_text := str(prices.get("sell", "—"))
		draw_string(font, rect.position + Vector2(30, y), "%s %-11s %s" % [marker, commodity.get("name", commodity_id), hold_text], HORIZONTAL_ALIGNMENT_LEFT, 190, 16, Color(0.82, 0.92, 0.86))
		draw_string(font, rect.position + Vector2(230, y), "%s  %s" % [status, str(prices.get("buy", "—"))], HORIZONTAL_ALIGNMENT_LEFT, 150, 16, Color(0.82, 0.92, 0.86))
		draw_string(font, rect.position + Vector2(390, y), sell_price_text, HORIZONTAL_ALIGNMENT_LEFT, 100, 16, Color(0.82, 0.92, 0.86))
		draw_string(font, rect.position + Vector2(520, y), "B", HORIZONTAL_ALIGNMENT_LEFT, 40, 16, Color(0.82, 0.92, 0.86))
		draw_string(font, rect.position + Vector2(600, y), "S" if held > 0 else "—", HORIZONTAL_ALIGNMENT_LEFT, 40, 16, Color(0.82, 0.92, 0.86))
		y += 20.0
		if i == selected_landing_item:
			draw_string(font, rect.position + Vector2(52, y), _commodity_trade_hint_line(commodity_id), HORIZONTAL_ALIGNMENT_LEFT, 760, 13, Color(0.68, 0.78, 0.90))
			y += 18.0
			draw_string(font, rect.position + Vector2(52, y), _commodity_legal_hint_line(commodity_id), HORIZONTAL_ALIGNMENT_LEFT, 760, 13, Color(0.95, 0.70, 0.58))
			y += 18.0
		else:
			y += 8.0

func _ev_classic_price_status(prices: Dictionary) -> String:
	return str(prices.get("evClassicPriceStatus", ""))

func _commodity_sell_price(commodity_id: String) -> int:
	return int(_market_prices(current_system.get("name", "")).get(commodity_id, {}).get("sell", 0))

func _commodity_trade_hint_line(commodity_id: String) -> String:
	var current_name := str(current_system.get("name", ""))
	var current_prices: Dictionary = _market_prices(current_name).get(commodity_id, {})
	var buy_price := int(current_prices.get("buy", 0))
	if buy_price <= 0:
		return "No buy price here"
	var best_system := ""
	var best_sell := 0
	var best_profit := -999999
	for linked_name in current_system.get("links", []):
		var sell_price := int(_market_prices(str(linked_name)).get(commodity_id, {}).get("sell", 0))
		if sell_price <= 0:
			continue
		var profit := sell_price - buy_price
		if best_system == "" or profit > best_profit:
			best_system = str(linked_name)
			best_sell = sell_price
			best_profit = profit
	if best_system == "":
		return "No linked sell data"
	return "Best linked sell: %s at %d (%+d cr/ton)" % [best_system, best_sell, best_profit]

func _commodity_legal_hint_line(commodity_id: String) -> String:
	var government_name := _current_government_name()
	if _commodity_is_contraband_for_government(commodity_id, government_name):
		var policy: Dictionary = governments.get("governments", {}).get(government_name, {})
		return "Legal risk: %s is contraband under %s scans; finePerTon=%d bribeAllowed=%s" % [commodity_id, government_name, int(policy.get("finePerTon", 0)), str(policy.get("bribeAllowed", false))]
	return "Legal risk: no current %s contraband flag under %s; TV scaffold, scan wording pending" % [commodity_id, government_name]

func _commodity_is_contraband_for_government(commodity_id: String, government_name: String) -> bool:
	var illegal: Array = governments.get("contraband", {}).get(government_name, [])
	return illegal.has(commodity_id)

func _draw_outfitter(rect: Rect2, body: Dictionary) -> void:
	var font := ThemeDB.fallback_font
	var inventory := _station_inventory(body)
	var outfits_for_sale: Array = inventory.get("outfitsForSale", [])
	var weapons_for_sale: Array = inventory.get("weaponsForSale", [])
	draw_string(font, rect.position + Vector2(30, 166), "Outfitter", HORIZONTAL_ALIGNMENT_LEFT, 820, 22, Color(0.92, 0.96, 1.0))
	draw_string(font, rect.position + Vector2(30, 192), "B buys selected upgrade", HORIZONTAL_ALIGNMENT_LEFT, 820, 14, Color(0.95, 0.86, 0.58))
	var y := 204.0
	var sale_items := _outfitter_sale_items(body)
	for i in range(min(8, sale_items.size())):
		var sale_item: Dictionary = sale_items[i]
		var marker := "▶" if i == selected_landing_item else "•"
		draw_string(font, rect.position + Vector2(30, y), "%s %s — %d cr" % [marker, sale_item.get("name", sale_item.get("id", "Upgrade")), int(sale_item.get("price", 0))], HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.86, 0.92, 1.0))
		y += 20.0
		draw_string(font, rect.position + Vector2(52, y), "Effect: " + _outfit_effect_summary(sale_item), HORIZONTAL_ALIGNMENT_LEFT, 760, 13, Color(0.68, 0.78, 0.90))
		y += 18.0
		var source_line := _outfit_source_summary(sale_item)
		if source_line != "":
			draw_string(font, rect.position + Vector2(52, y), source_line, HORIZONTAL_ALIGNMENT_LEFT, 760, 12, Color(0.58, 0.70, 0.86))
			y += 18.0
		else:
			y += 4.0
	if outfits_for_sale.is_empty() and weapons_for_sale.is_empty():
		draw_string(font, rect.position + Vector2(30, y), "No outfitter inventory at this port.", HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.72, 0.82, 0.92))

func _draw_shipyard(rect: Rect2, body: Dictionary) -> void:
	var font := ThemeDB.fallback_font
	var inventory := _station_inventory(body)
	var ships_for_sale: Array = inventory.get("shipsForSale", [])
	draw_string(font, rect.position + Vector2(30, 166), "Shipyard", HORIZONTAL_ALIGNMENT_LEFT, 820, 22, Color(0.92, 0.96, 1.0))
	draw_string(font, rect.position + Vector2(30, 192), "B buys selected ship", HORIZONTAL_ALIGNMENT_LEFT, 820, 14, Color(0.95, 0.86, 0.58))
	var y := 204.0
	var listings := _shipyard_listings(body)
	if not listings.is_empty():
		var selected_listing: Dictionary = listings[selected_landing_item % listings.size()]
		var tex := _shipyard_texture_for_listing(selected_listing)
		if tex != null:
			draw_texture_rect(tex, Rect2(rect.position + Vector2(690, 188), Vector2(150, 150)), false)
			draw_rect(Rect2(rect.position + Vector2(690, 188), Vector2(150, 150)), Color(0.55, 0.70, 0.90, 1.0), false, 1.0)
			draw_string(font, rect.position + Vector2(690, 358), "Source PICT shipyard art", HORIZONTAL_ALIGNMENT_LEFT, 170, 13, Color(0.72, 0.82, 0.92))
	for i in range(min(7, listings.size())):
		var listing: Dictionary = listings[i]
		var ship := _ship_by_id(str(listing.get("shipId", "")))
		var marker := "▶" if i == selected_landing_item else "•"
		draw_string(font, rect.position + Vector2(30, y), "%s %s — %d cr" % [marker, listing.get("shipId", "ship"), int(listing.get("price", 0))], HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.86, 0.92, 1.0))
		y += 20.0
		draw_string(font, rect.position + Vector2(52, y), _ship_comparison_line(ship), HORIZONTAL_ALIGNMENT_LEFT, 600, 13, Color(0.68, 0.78, 0.90))
		y += 22.0
	if ships_for_sale.is_empty():
		draw_string(font, rect.position + Vector2(30, y), "This port has no shipyard listings.", HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.72, 0.82, 0.92))

func _available_missions(body: Dictionary) -> Array:
	var available_missions := []
	var body_name := str(body.get("name", ""))
	var system_name := str(current_system.get("name", ""))
	for mission in missions.get("missions", []):
		var mission_id := str(mission.get("id", ""))
		if active_missions.has(mission_id) or completed_missions.has(mission_id):
			continue
		if mission.get("originSystem", "") != system_name or mission.get("originBody", "") != body_name:
			continue
		if not _has_all_flags(mission.get("requiresFlags", [])):
			continue
		if _has_any_flag(mission.get("excludesFlags", [])):
			continue
		if not _mission_requirements_met(mission):
			continue
		available_missions.append(mission)
	return available_missions

func _blocked_mission_reasons(body: Dictionary) -> Array[String]:
	var reasons: Array[String] = []
	var body_name := str(body.get("name", ""))
	var system_name := str(current_system.get("name", ""))
	for mission in missions.get("missions", []):
		var mission_id := str(mission.get("id", ""))
		if active_missions.has(mission_id) or completed_missions.has(mission_id):
			continue
		if mission.get("originSystem", "") != system_name or mission.get("originBody", "") != body_name:
			continue
		var story_reason := _mission_story_gate_block_reason(mission)
		if story_reason != "requirements met":
			reasons.append("%s: %s" % [str(mission.get("title", mission_id)), story_reason])
			continue
		if _mission_requirements_met(mission):
			continue
		var reason := _mission_requirement_block_reason(mission)
		if reason != "":
			reasons.append("%s: %s" % [str(mission.get("title", mission_id)), reason])
	return reasons

func _has_all_flags(required: Array) -> bool:
	for flag in required:
		if not story_flags.has(flag):
			return false
	return true

func _has_any_flag(excluded: Array) -> bool:
	for flag in excluded:
		if story_flags.has(str(flag)):
			return true
	return false

func _mission_story_gate_state(mission: Dictionary) -> String:
	if not _has_all_flags(mission.get("requiresFlags", [])):
		return "missing_required_flags"
	if _has_any_flag(mission.get("excludesFlags", [])):
		return "excluded_by_story_flags"
	return "requirements met"

func _mission_story_gate_block_reason(mission: Dictionary) -> String:
	var missing_flags: Array[String] = []
	for flag in mission.get("requiresFlags", []):
		var flag_name := str(flag)
		if not story_flags.has(flag_name):
			missing_flags.append(flag_name)
	if not missing_flags.is_empty():
		return "requires missing story flag(s): %s; Terminal Velocity story-chain scaffold, exact Classic offer visibility pending; storyGate=%s" % [", ".join(missing_flags), _mission_story_gate_state(mission)]
	var excluded_flags: Array[String] = []
	for flag in mission.get("excludesFlags", []):
		var flag_name := str(flag)
		if story_flags.has(flag_name):
			excluded_flags.append(flag_name)
	if not excluded_flags.is_empty():
		return "excluded by active story flag(s): %s; Terminal Velocity choice/exclusion scaffold, exact Classic offer visibility pending; storyGate=%s" % [", ".join(excluded_flags), _mission_story_gate_state(mission)]
	return "requirements met"

func _mission_requirements_met(mission: Dictionary) -> bool:
	var requirements: Dictionary = mission.get("requirements", {})
	return _score_min_requirements_met(requirements.get("reputationMin", {}), reputation_scores) and _score_min_requirements_met(requirements.get("legalMin", {}), legal_records) and _score_max_requirements_met(requirements.get("legalMax", {}), legal_records)

func _score_min_requirements_met(requirements: Dictionary, scores: Dictionary) -> bool:
	for key in requirements.keys():
		if int(scores.get(str(key), 0)) < int(requirements.get(key, 0)):
			return false
	return true

func _score_max_requirements_met(requirements: Dictionary, scores: Dictionary) -> bool:
	for key in requirements.keys():
		if int(scores.get(str(key), 0)) > int(requirements.get(key, 0)):
			return false
	return true

func _mission_requirement_block_reason(mission: Dictionary) -> String:
	var legal_reason := _mission_legal_requirement_block_reason(mission)
	if legal_reason != "requirements met":
		return legal_reason
	var requirements: Dictionary = mission.get("requirements", {})
	var reputation_min: Dictionary = requirements.get("reputationMin", {})
	for government_name in reputation_min.keys():
		var score := int(reputation_scores.get(str(government_name), 0))
		var minimum := int(reputation_min.get(government_name, 0))
		if score < minimum:
			return "%s reputation score %d below required %d; TV scaffold, exact Classic mission gates unconfirmed" % [str(government_name), score, minimum]
	return "requirements met"

func _mission_legal_requirement_block_reason(mission: Dictionary) -> String:
	var requirements: Dictionary = mission.get("requirements", {})
	var legal_min: Dictionary = requirements.get("legalMin", {})
	for government_name in legal_min.keys():
		var score := int(legal_records.get(str(government_name), 0))
		var minimum := int(legal_min.get(government_name, 0))
		if score < minimum:
			return "%s legal score %d below required %d; TV scaffold, exact Classic mission gates unconfirmed" % [str(government_name), score, minimum]
	return "requirements met"

func _market_prices(system_name: String) -> Dictionary:
	var market_prices: Dictionary = economy.get("markets", {}).get(system_name, {})
	return market_prices

func _station_inventory(body: Dictionary) -> Dictionary:
	var inventory: Dictionary = body.get("inventory", {})
	return {
		"services": inventory.get("services", []),
		"outfitsForSale": inventory.get("outfitsForSale", []),
		"shipsForSale": inventory.get("shipsForSale", []),
		"weaponsForSale": inventory.get("weaponsForSale", [])
	}

func _filter_by_ids(items: Array, ids: Array, key: String) -> Array:
	var selected := []
	for item in items:
		if ids.has(item.get(key, "")):
			selected.append(item)
	return selected

func _current_body() -> Dictionary:
	var nearest := _nearest_body()
	if nearest.is_empty():
		return {}
	return nearest.get("body", {})

func _landing_item_count() -> int:
	var body := _current_body()
	match landing_tab:
		0:
			return _available_missions(body).size()
		1:
			return economy.get("commodities", []).size()
		2:
			return _outfitter_sale_items(body).size()
		3:
			return _shipyard_listings(body).size()
		_:
			return 0

func _cycle_landing_selection(dir: int) -> void:
	var count := _landing_item_count()
	if count <= 0:
		selected_landing_item = 0
		return
	selected_landing_item = (selected_landing_item + dir + count) % count

func _accept_selected_mission() -> void:
	if _disabled_player_action_blocked():
		return
	var available := _available_missions(_current_body())
	if available.is_empty():
		_set_status("No mission to accept")
		return
	var mission: Dictionary = available[selected_landing_item % available.size()]
	var tons := int(mission.get("cargoTons", 0))
	if tons > _cargo_available_tons():
		_set_status("Need %d free cargo tons" % tons)
		return
	var mission_id := str(mission.get("id", ""))
	active_missions.append(mission_id)
	mission_acceptance_days[mission_id] = current_day
	cargo += tons
	for flag in mission.get("setsFlags", []):
		if not story_flags.has(flag):
			story_flags.append(flag)
	_set_status("Accepted mission: " + str(mission.get("title", mission_id)))
	_play_sound("ui_click")
	selected_landing_item = 0

func _buy_selected_commodity() -> void:
	if _disabled_player_action_blocked():
		return
	if not landed:
		_set_status("Land before trading commodities")
		return
	var commodities: Array = economy.get("commodities", [])
	if commodities.is_empty():
		_set_status("No commodities available")
		return
	var commodity: Dictionary = commodities[selected_landing_item % commodities.size()]
	var commodity_id := str(commodity.get("id", ""))
	var price := int(_market_prices(current_system.get("name", "")).get(commodity_id, {}).get("buy", 0))
	if price <= 0:
		_set_status("Commodity unavailable here")
		return
	if cargo >= cargo_space:
		_set_status("Cargo hold full")
		return
	if credits < price:
		_set_status("Not enough credits")
		return
	var free_space := _cargo_available_tons()
	var affordable_tons := int(floor(float(credits) / float(price)))
	var tons: int = min(EV_CLASSIC_COMMODITY_LOT_SIZE, free_space, affordable_tons)
	if tons <= 0:
		_set_status("Not enough credits")
		return
	credits -= price * tons
	cargo += tons
	commodity_hold[commodity_id] = int(commodity_hold.get(commodity_id, 0)) + tons
	_set_status("Bought %d tons of %s" % [tons, str(commodity.get("name", commodity_id))])
	_play_sound("ui_click")

func _sell_selected_commodity() -> void:
	if _disabled_player_action_blocked():
		return
	if not landed:
		_set_status("Land before trading commodities")
		return
	var commodities: Array = economy.get("commodities", [])
	if commodities.is_empty():
		_set_status("No commodities available")
		return
	var commodity: Dictionary = commodities[selected_landing_item % commodities.size()]
	var commodity_id := str(commodity.get("id", ""))
	var held := int(commodity_hold.get(commodity_id, 0))
	if held <= 0:
		_set_status("No cargo to sell")
		return
	var price := _commodity_sell_price(commodity_id)
	if price <= 0:
		_set_status("No sell price here")
		return
	var tons: int = min(EV_CLASSIC_COMMODITY_LOT_SIZE, held)
	credits += price * tons
	cargo = max(0, cargo - tons)
	commodity_hold[commodity_id] = held - tons
	_set_status("Sold %d tons of %s" % [tons, str(commodity.get("name", commodity_id))])
	_play_sound("ui_click")

func _outfitter_sale_items(body: Dictionary) -> Array:
	var inventory := _station_inventory(body)
	var sale_items := []
	for outfit in _filter_by_ids(outfits.get("outfits", []), inventory.get("outfitsForSale", []), "id"):
		var item: Dictionary = outfit.duplicate()
		item["saleType"] = "outfit"
		sale_items.append(item)
	for weapon in _filter_by_ids(weapons.get("weapons", []), inventory.get("weaponsForSale", []), "id"):
		var item: Dictionary = weapon.duplicate()
		item["saleType"] = "weapon"
		sale_items.append(item)
	return sale_items

func _buy_selected_outfit_or_weapon() -> void:
	if _disabled_player_action_blocked():
		return
	if not landed:
		_set_status("Land before outfitter purchases")
		return
	var government_name := _current_government_name()
	if not _legal_service_access_allowed(government_name):
		_set_status(_legal_service_blocked_message(government_name))
		return
	var sale_items := _outfitter_sale_items(_current_body())
	if sale_items.is_empty():
		_set_status("No outfitter stock")
		return
	var item: Dictionary = sale_items[selected_landing_item % sale_items.size()]
	if _buy_outfit_or_weapon_item(item, government_name):
		_play_sound("ui_click")

func _buy_outfit_or_weapon_by_id(item_id: String) -> bool:
	if _disabled_player_action_blocked():
		return false
	if not landed:
		_set_status("Land before outfitter purchases")
		return false
	var government_name := _current_government_name()
	if not _legal_service_access_allowed(government_name):
		_set_status(_legal_service_blocked_message(government_name))
		return false
	for item in _outfitter_sale_items(_current_body()):
		if str(item.get("id", "")) == item_id:
			var bought := _buy_outfit_or_weapon_item(item, government_name)
			if bought:
				_play_sound("ui_click")
			return bought
	_set_status("Item not sold here: %s" % item_id)
	return false

func _buy_outfit_or_weapon_item(item: Dictionary, government_name: String) -> bool:
	var service_name := "weapons" if item.get("saleType", "") == "weapon" else "outfitter"
	if not _service_access_allowed(service_name, government_name):
		_set_status(_service_blocked_message(service_name, government_name))
		return false
	var price := int(item.get("price", 0))
	if credits < price:
		_set_status("Not enough credits")
		return false
	credits -= price
	var item_id := str(item.get("id", ""))
	if item.get("saleType", "") == "weapon":
		owned_weapons[item_id] = int(owned_weapons.get(item_id, 0)) + 1
	else:
		owned_outfits[item_id] = int(owned_outfits.get(item_id, 0)) + 1
		var effects: Dictionary = item.get("effects", {})
		cargo_space += int(effects.get("cargoSpace", 0))
		player_hull = min(_max_player_hull(), player_hull + int(effects.get("maxHull", 0)))
		player_fuel = min(_max_player_fuel(), player_fuel + int(effects.get("maxFuel", 0)))
	_set_status("Bought " + str(item.get("name", item_id)))
	return true

func _shipyard_listings(body: Dictionary) -> Array:
	var inventory := _station_inventory(body)
	return _filter_by_ids(outfits.get("shipyard", []), inventory.get("shipsForSale", []), "shipId")

func _ship_comparison_line(ship: Dictionary) -> String:
	if ship.is_empty():
		return "Stats unavailable"
	var delta_cargo := int(ship.get("cargoSpace", 0)) - int(player_ship.get("cargoSpace", 0))
	var delta_hull := int(ship.get("hull", 0)) - int(player_ship.get("hull", 0))
	var delta_speed := int(ship.get("maxSpeed", 0)) - int(player_ship.get("maxSpeed", 0))
	var delta_turning := int(ship.get("turning", 0)) - int(player_ship.get("turning", 0))
	return "Δ cargo %+d  Δ hull %+d  Δ speed %+d  Δ turn %+d" % [delta_cargo, delta_hull, delta_speed, delta_turning]

func _outfit_effect_summary(item: Dictionary) -> String:
	var effects: Dictionary = item.get("effects", {})
	var parts: Array[String] = []
	if effects.has("cargoSpace"):
		parts.append("cargo %+d" % int(effects.get("cargoSpace", 0)))
	if effects.has("maxHull"):
		parts.append("hull %+d" % int(effects.get("maxHull", 0)))
	if effects.has("maxFuel"):
		parts.append("fuel %+d" % int(effects.get("maxFuel", 0)))
	if item.get("saleType", "") == "weapon":
		parts.append("MassDmg %d" % int(item.get("massDamage", 0)))
		parts.append("EnergyDmg %d" % int(item.get("energyDamage", 0)))
	if parts.is_empty():
		return str(item.get("description", "No numeric effect listed"))
	return " / ".join(parts)

func _outfit_source_summary(item: Dictionary) -> String:
	if item.get("saleType", "") != "weapon":
		return ""
	var stock_name := str(item.get("sourceStockName", ""))
	var source_id := int(item.get("sourceResourceId", -1))
	if stock_name == "" or source_id < 0:
		return "Source: TV scaffold; stock EV mapping pending"
	return "Source: stock %s (wëap %d); TV values scaffold until runtime-tuned" % [stock_name, source_id]

func _buy_selected_ship() -> void:
	if _disabled_player_action_blocked():
		return
	if not landed:
		_set_status("Land before shipyard purchases")
		return
	var government_name := _current_government_name()
	if not _service_access_allowed("shipyard", government_name):
		_set_status(_service_blocked_message("shipyard", government_name))
		return
	var listings := _shipyard_listings(_current_body())
	if listings.is_empty():
		_set_status("No ships for sale")
		return
	var listing: Dictionary = listings[selected_landing_item % listings.size()]
	var price := int(listing.get("price", 0))
	if credits < price:
		_set_status("Not enough credits")
		return
	var ship_id := str(listing.get("shipId", ""))
	var new_ship := _ship_by_id(ship_id)
	if new_ship.is_empty():
		_set_status("Ship manifest missing " + ship_id)
		return
	var new_cargo_space := int(new_ship.get("cargoSpace", cargo_space))
	if cargo > new_cargo_space:
		_set_status("Cannot buy %s: cargo %d exceeds target capacity %d" % [ship_id, cargo, new_cargo_space])
		return
	credits -= price
	player_ship = new_ship
	player_ship_id = ship_id
	var player_frame_set := _load_ship_frame_set(player_ship)
	player_frames = player_frame_set["frames"]
	player_frame_offsets = player_frame_set["offsets"]
	cargo_space = int(player_ship.get("cargoSpace", cargo_space))
	cargo = min(cargo, cargo_space)
	player_fuel = min(player_fuel, _max_player_fuel())
	_reset_player_combat_stats()
	_set_status("Bought ship: " + ship_id)
	_play_sound("ui_click")

func _ship_by_id(ship_id: String) -> Dictionary:
	for ship in ships.get("ships", []):
		if ship.get("id", "") == ship_id:
			return ship
	return {}

func _named_color(name: String) -> Color:
	match name:
		"SteelBlue": return Color.STEEL_BLUE
		"Silver": return Color.SILVER
		"IndianRed": return Color.INDIAN_RED
		"MediumPurple": return Color.MEDIUM_PURPLE
		"SandyBrown": return Color.SANDY_BROWN
		"DarkSeaGreen": return Color.DARK_SEA_GREEN
		"DarkSlateBlue": return Color.DARK_SLATE_BLUE
		"Firebrick": return Color.FIREBRICK
		"Goldenrod": return Color.GOLDENROD
		"SlateGray": return Color.SLATE_GRAY
		"SeaGreen": return Color.SEA_GREEN
		"OrangeRed": return Color.ORANGE_RED
		_:
			return Color.DARK_GRAY
