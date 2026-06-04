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
const MAP_ROUTE_EVENT_LOG_PREFIX := "TV_MAP_ROUTE_EVENT"
const ROUTE_CLEAR_EVENT_LOG_PREFIX := "TV_ROUTE_CLEAR_EVENT"
const ROUTE_CLEAR_RESELECT_EVENT_LOG_PREFIX := "TV_ROUTE_CLEAR_RESELECT_EVENT"
const ROUTE_JUMP_EVENT_LOG_PREFIX := "TV_ROUTE_JUMP_EVENT"
const ROUTE_LAND_REFUEL_EVENT_LOG_PREFIX := "TV_ROUTE_LAND_REFUEL_EVENT"
const REPAIR_SERVICE_EVENT_LOG_PREFIX := "TV_REPAIR_SERVICE_EVENT"
const LOW_FUEL_JUMP_EVENT_LOG_PREFIX := "TV_LOW_FUEL_JUMP_EVENT"
const NEAR_CENTER_JUMP_EVENT_LOG_PREFIX := "TV_NEAR_CENTER_JUMP_EVENT"
const COMMODITY_TRADE_EVENT_LOG_PREFIX := "TV_COMMODITY_TRADE_EVENT"
const MISSION_OFFER_SCAN_EVENT_LOG_PREFIX := "TV_MISSION_OFFER_SCAN_EVENT"
const MISSION_CHAIN_OFFER_EVENT_LOG_PREFIX := "TV_MISSION_CHAIN_OFFER_EVENT"
const MISSION_CHAIN_LOCK_EVENT_LOG_PREFIX := "TV_MISSION_CHAIN_LOCK_EVENT"
const MISSION_ALIGNMENT_BRANCH_EVENT_LOG_PREFIX := "TV_MISSION_ALIGNMENT_BRANCH_EVENT"
const MISSION_ROUTE_HINT_EVENT_LOG_PREFIX := "TV_MISSION_ROUTE_HINT_EVENT"
const MISSION_ABORT_EVENT_LOG_PREFIX := "TV_MISSION_ABORT_EVENT"
const MISSION_DEADLINE_FAILURE_EVENT_LOG_PREFIX := "TV_MISSION_DEADLINE_FAILURE_EVENT"
const MISSION_LOG_HISTORY_EVENT_LOG_PREFIX := "TV_MISSION_LOG_HISTORY_EVENT"
const FIRST_MISSION_DELIVERY_EVENT_LOG_PREFIX := "TV_FIRST_MISSION_DELIVERY_EVENT"
const PILOT_SAVE_RESUME_EVENT_LOG_PREFIX := "TV_PILOT_SAVE_RESUME_EVENT"
const OUTFITTER_SHIPYARD_EVENT_LOG_PREFIX := "TV_OUTFITTER_SHIPYARD_EVENT"
const GAMEPLAY_CURRICULUM_HELP_LOG_PREFIX := "TV_GAMEPLAY_CURRICULUM_HELP"
const COMBAT_EVENT_LOG_PREFIX := "TV_COMBAT_EVENT"
const COMBAT_GUARDRAIL_EVENT_LOG_PREFIX := "TV_COMBAT_GUARDRAIL_EVENT"
const TARGET_SELECTION_EVENT_LOG_PREFIX := "TV_TARGET_SELECTION_EVENT"
const NAVIGATION_GUARDRAIL_EVENT_LOG_PREFIX := "TV_NAVIGATION_GUARDRAIL_EVENT"
const LEGAL_STATUS_EVENT_LOG_PREFIX := "TV_LEGAL_STATUS_EVENT"
const LEGAL_SERVICE_GATE_EVENT_LOG_PREFIX := "TV_LEGAL_SERVICE_GATE_EVENT"
const LEGAL_PATROL_POSTURE_EVENT_LOG_PREFIX := "TV_LEGAL_PATROL_POSTURE_EVENT"
const MISSION_LEGAL_ELIGIBILITY_EVENT_LOG_PREFIX := "TV_MISSION_LEGAL_ELIGIBILITY_EVENT"
const LEGAL_CONSEQUENCE_EVENT_LOG_PREFIX := "TV_LEGAL_CONSEQUENCE_EVENT"
const LEGAL_CLEMENCY_EVENT_LOG_PREFIX := "TV_LEGAL_CLEMENCY_EVENT"
const CONTRABAND_SCAN_EVENT_LOG_PREFIX := "TV_CONTRABAND_SCAN_EVENT"
const CONTRABAND_RISK_EVENT_LOG_PREFIX := "TV_CONTRABAND_RISK_EVENT"
const LEGAL_RESOURCE_SEMANTICS_SOURCE_BASIS := "sourceBasis=EV Classic Resource Bible: govt CrimeTol/penalties, interceptor scans, mission AvailRecord/ScanGovt/PayVal"
const FIRST_MISSION_DELIVERY_EXPECTED_MISSION_FIELD := "acceptedMission=intro_courier_earth_hera"
const MIN_HYPERSPACE_DISTANCE_FROM_CENTER := 450.0
const AFTERBURNER_THRUST_MULTIPLIER := 1.75
const AFTERBURNER_FUEL_PER_SECOND := 2.0

var repo_root := ""
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
var sound_players: Dictionary = {}
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
var target_shields: Dictionary = {}
var target_hulls: Dictionary = {}
var player_shields := 0
var player_hull := 0
var player_shield_recharge_progress := 0.0
var primary_weapon_cooldown_frames := 0.0
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
	if OS.get_cmdline_args().has("--tv-mission-offer-scan-log") or OS.get_cmdline_user_args().has("--tv-mission-offer-scan-log"):
		call_deferred("_run_mission_offer_scan_log")
	if OS.get_cmdline_args().has("--tv-mission-chain-offer-log") or OS.get_cmdline_user_args().has("--tv-mission-chain-offer-log"):
		call_deferred("_run_mission_chain_offer_log")
	if OS.get_cmdline_args().has("--tv-mission-chain-lock-log") or OS.get_cmdline_user_args().has("--tv-mission-chain-lock-log"):
		call_deferred("_run_mission_chain_lock_log")
	if OS.get_cmdline_args().has("--tv-mission-alignment-branch-log") or OS.get_cmdline_user_args().has("--tv-mission-alignment-branch-log"):
		call_deferred("_run_mission_alignment_branch_log")
	if OS.get_cmdline_args().has("--tv-mission-route-hint-log") or OS.get_cmdline_user_args().has("--tv-mission-route-hint-log"):
		call_deferred("_run_mission_route_hint_log")
	if OS.get_cmdline_args().has("--tv-mission-abort-log") or OS.get_cmdline_user_args().has("--tv-mission-abort-log"):
		call_deferred("_run_mission_abort_log")
	if OS.get_cmdline_args().has("--tv-mission-deadline-failure-log") or OS.get_cmdline_user_args().has("--tv-mission-deadline-failure-log"):
		call_deferred("_run_mission_deadline_failure_log")
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
	if OS.get_cmdline_args().has("--tv-repair-service-log") or OS.get_cmdline_user_args().has("--tv-repair-service-log"):
		call_deferred("_run_repair_service_log")
	if OS.get_cmdline_args().has("--tv-gameplay-curriculum-help-log") or OS.get_cmdline_user_args().has("--tv-gameplay-curriculum-help-log"):
		call_deferred("_run_gameplay_curriculum_help_log")
	if OS.get_cmdline_args().has("--tv-combat-log") or OS.get_cmdline_user_args().has("--tv-combat-log"):
		call_deferred("_run_combat_log")
	if OS.get_cmdline_args().has("--tv-combat-guardrail-log") or OS.get_cmdline_user_args().has("--tv-combat-guardrail-log"):
		call_deferred("_run_combat_guardrail_log")
	if OS.get_cmdline_args().has("--tv-target-selection-log") or OS.get_cmdline_user_args().has("--tv-target-selection-log"):
		call_deferred("_run_target_selection_log")
	if OS.get_cmdline_args().has("--tv-navigation-guardrail-log") or OS.get_cmdline_user_args().has("--tv-navigation-guardrail-log"):
		call_deferred("_run_navigation_guardrail_log")
	if OS.get_cmdline_args().has("--tv-legal-status-log") or OS.get_cmdline_user_args().has("--tv-legal-status-log"):
		call_deferred("_run_legal_status_log")
	if OS.get_cmdline_args().has("--tv-legal-service-gate-log") or OS.get_cmdline_user_args().has("--tv-legal-service-gate-log"):
		call_deferred("_run_legal_service_gate_log")
	if OS.get_cmdline_args().has("--tv-legal-patrol-posture-log") or OS.get_cmdline_user_args().has("--tv-legal-patrol-posture-log"):
		call_deferred("_run_legal_patrol_posture_log")
	if OS.get_cmdline_args().has("--tv-mission-legal-eligibility-log") or OS.get_cmdline_user_args().has("--tv-mission-legal-eligibility-log"):
		call_deferred("_run_mission_legal_eligibility_log")
	if OS.get_cmdline_args().has("--tv-legal-consequence-log") or OS.get_cmdline_user_args().has("--tv-legal-consequence-log"):
		call_deferred("_run_legal_consequence_log")
	if OS.get_cmdline_args().has("--tv-legal-clemency-log") or OS.get_cmdline_user_args().has("--tv-legal-clemency-log"):
		call_deferred("_run_legal_clemency_log")
	if OS.get_cmdline_args().has("--tv-contraband-scan-log") or OS.get_cmdline_user_args().has("--tv-contraband-scan-log"):
		call_deferred("_run_contraband_scan_log")
	if OS.get_cmdline_args().has("--tv-contraband-risk-log") or OS.get_cmdline_user_args().has("--tv-contraband-risk-log"):
		call_deferred("_run_contraband_risk_log")

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
	universe = _json(repo_root + "/native_ev/data/universe.json")
	ships = _json(repo_root + "/native_ev/data/ships.json")
	missions = _json(repo_root + "/native_ev/data/missions.json")
	economy = _json(repo_root + "/native_ev/data/economy.json")
	outfits = _json(repo_root + "/native_ev/data/outfits.json")
	weapons = _json(repo_root + "/native_ev/data/weapons.json")
	governments = _json(repo_root + "/native_ev/data/governments.json")
	reputation = _json(repo_root + "/native_ev/data/reputation.json")
	sounds = _json(repo_root + "/native_ev/data/sounds.json")
	gameplay_curriculum = _json(repo_root + "/native_ev/data/gameplay_curriculum.json")
	current_system_index = _system_index_by_name(START_SYSTEM_NAME, 0)
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
	player.stop()
	player.play()

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
		pos += vel * delta
		vel *= pow(0.995, delta * 60.0)
		_recharge_player_shields(delta)
		_advance_weapon_cooldowns(delta)
		_advance_projectiles(delta)
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
				_set_status("Afterburner unavailable: no fuel")
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
	print("%s ticks=%d normalSpeed=%.3f afterburnerSpeed=%.3f speedBoosted=%s fuelBefore=%d fuelAfter=%d fuelDrained=%s thrustMultiplier=%.2f fuelPerSecond=%.2f sourceLabel=terminal-velocity-afterburner-scaffold oracleStatus=classic_runtime_afterburner_fuel_curve_pending" % [AFTERBURNER_EVENT_LOG_PREFIX, ticks, normal_speed, afterburner_speed, str(speed_boosted), fuel_before_afterburner, fuel_after_afterburner, str(fuel_drained), AFTERBURNER_THRUST_MULTIPLIER, AFTERBURNER_FUEL_PER_SECOND])
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
	cargo = 0
	projectiles.clear()
	explosion_events.clear()
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
	selected_landing_item = branch_offer_ids.find("federation_report_freeport")
	if selected_landing_item < 0:
		selected_landing_item = 0
	var selected_branch_offer: Dictionary = branch_offers[selected_landing_item] if not branch_offers.is_empty() else {}
	var selected_branch_offer_details := _mission_offer_detail_lines(selected_branch_offer)
	var selected_branch_offer_details_visible := selected_branch_offer_details.size() > 0 and selected_branch_offer_details.has("Offer detail source: terminal-velocity-mission-offer-helper; exact Classic Mission Computer detail UI pending")
	_accept_selected_mission()
	var federation_branch_accepted := active_missions.has("federation_report_freeport")
	var offers_after_choice := _available_missions(branch_body)
	var offer_ids_after_choice := []
	for mission in offers_after_choice:
		offer_ids_after_choice.append(str(mission.get("id", "")))
	var freeport_branch_hidden_after_choice := not offer_ids_after_choice.has("freeport_pact_smugglers")
	var reputation_snapshot := {
		"Federation": int(reputation_scores.get("Federation", 0)),
		"Independent": int(reputation_scores.get("Independent", 0)),
		"Centauri Protectorate": int(reputation_scores.get("Centauri Protectorate", 0))
	}
	print("%s startSystem=Levo routeToSolSelected=%s routeToLunaSelected=%s firstMissionDelivered=%s chainMissionAccepted=%s routeToSiriusSelected=%s chainMissionDelivered=%s scanSystem=%s scanBody=\"%s\" branchOffersVisible=%s federationOfferVisible=%s freeportOfferVisible=%s branchOffers=%s choiceGroups=%s selectedBranchOfferDetailsVisible=%s selectedBranchOfferDetails=%s federationBranchAccepted=%s freeportBranchHiddenAfterChoice=%s offersAfterChoice=%s reputation=%s activeMissions=%s completedMissions=%s storyFlags=%s sourceLabel=terminal-velocity-observed oracleStatus=terminal_velocity_eval_pending_original_trace choiceBoundary=terminal_velocity_choice_group_scaffold_exact_classic_branch_ui_pending status=\"%s\"" % [MISSION_ALIGNMENT_BRANCH_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(route_to_luna_selected), str(first_completed), str(chain_accepted), str(route_to_sirius_selected), str(chain_delivered), str(current_system.get("name", "?")), str(branch_body.get("name", "None")), str(federation_visible and freeport_visible and branch_choice_group_visible), str(federation_visible), str(freeport_visible), JSON.stringify(branch_offer_ids), JSON.stringify(branch_choice_groups), str(selected_branch_offer_details_visible), JSON.stringify(selected_branch_offer_details), str(federation_branch_accepted), str(freeport_branch_hidden_after_choice), JSON.stringify(offer_ids_after_choice), JSON.stringify(reputation_snapshot), JSON.stringify(active_missions), JSON.stringify(completed_missions), JSON.stringify(story_flags), status_line])
	get_tree().quit(0)

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
	var mission_route_status := "missionRouteQueued=true" if mission_route_queued else "missionRouteQueued=false"
	var queued_route := JSON.stringify(selected_route)
	print("%s startSystem=Levo routeToSolSelected=%s acceptedAtSystem=Sol acceptedAtBody=\"%s\" acceptedMission=%s missionAccepted=%s destinationSystem=%s %s staleRouteBeforeHelper=%s staleRouteReplaced=%s route=%s routeHops=%d fuelBeforeRoute=%d routeFuelCost=%d preJumpFuelWarning=%s routeStatusHasFuelHint=%s lowFuelRouteWarningVisible=%s sourceLabel=terminal-velocity-design-scaffold oracleStatus=mission_objective_hint_pending_ev_classic_ui_trace status=\"%s\" routeStatus=\"%s\" lowFuelRouteStatus=\"%s\"" % [MISSION_ROUTE_HINT_EVENT_LOG_PREFIX, str(route_to_sol_selected), str(accepted_body.get("name", "None")), accepted_mission_id, str(mission_accepted), destination_system, mission_route_status, JSON.stringify(stale_route_before_helper), str(stale_route_replaced), queued_route, selected_route.size(), fuel_before_route, route_fuel_cost, str(pre_jump_fuel_warning), str(route_status_has_fuel_hint), str(low_fuel_route_warning_visible), low_fuel_route_status_line, route_status_line, low_fuel_route_status_line])
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
	var no_active_visible := lines.has("No active missions.")
	var completed_visible := lines.has("Completed mission history")
	var aborted_visible := lines.has("Aborted mission history")
	var failed_visible := lines.has("Failed mission history")
	var failed_deadline_visible := lines.has("Deadline: accepted day 0, failed day 3, limit 2 day(s)")
	var failed_source_visible := lines.has("Failure source: ev-classic-resource-bible-backed-mission-failure-scaffold; exact Classic UI pending")
	print("%s noActiveVisible=%s completedHistoryVisible=%s abortedHistoryVisible=%s failedHistoryVisible=%s failedDeadlineVisible=%s failedSourceVisible=%s lineCount=%d lines=%s sourceLabel=terminal-velocity-mission-log-history-scaffold oracleStatus=mission_history_ui_pending_classic_runtime_trace" % [MISSION_LOG_HISTORY_EVENT_LOG_PREFIX, str(no_active_visible), str(completed_visible), str(aborted_visible), str(failed_visible), str(failed_deadline_visible), str(failed_source_visible), lines.size(), JSON.stringify(lines)])
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
	var cargo_pod_status := "boughtCargoPod=true" if bought_cargo_pod else "boughtCargoPod=false"
	var laser_status := "boughtLaser=true" if bought_laser else "boughtLaser=false"
	var light_freighter_status := "boughtLightFreighter=true" if bought_light_freighter else "boughtLightFreighter=false"
	var cargo_space_status := "cargoSpaceIncreased=true" if cargo_space_increased else "cargoSpaceIncreased=false"
	var shipyard_art_status := "shipyardArtLoaded=true" if shipyard_art_loaded else "shipyardArtLoaded=false"
	print("%s routeToSolSelected=%s system=%s body=%s %s %s %s %s %s startingCargoSpace=%d cargoAfterOutfit=%d finalCargoSpace=%d creditsAfter=%d sourceLabel=terminal-velocity-outfitter-shipyard-scaffold oracleStatus=outfitter_shipyard_pending_ev_classic_purchase_trace status=\"%s\"" % [OUTFITTER_SHIPYARD_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), landed_body, cargo_pod_status, laser_status, light_freighter_status, cargo_space_status, shipyard_art_status, starting_cargo_space, cargo_space_after_outfit, cargo_space, credits, status_line])
	get_tree().quit(0)

func _run_gameplay_curriculum_help_log() -> void:
	var hints := _gameplay_curriculum_hint_lines()
	var has_pirate_hint := false
	var has_repair_help := false
	var has_combat_help := false
	var has_recovery_help := false
	for line in hints:
		if str(line).contains("pirate_avoidance_escape_route"):
			has_pirate_hint = true
	var help_lines := _help_overlay_lines()
	for line in help_lines:
		if str(line).contains("Repair: landed ports with repair service show F7"):
			has_repair_help = true
		if str(line).contains("Combat: Tab fires primary; N cycles targets; R selects closest target"):
			has_combat_help = true
		if str(line).contains("Recovery: F8 resets a disabled player ship"):
			has_recovery_help = true
	print("%s hintCount=%d hasPirateAvoidanceHint=%s hasRepairHelp=%s hasCombatHelp=%s hasRecoveryHelp=%s sourceLabel=terminal-velocity-curriculum-scaffold oracleStatus=help_surface_pending_playtest firstHint=\"%s\"" % [GAMEPLAY_CURRICULUM_HELP_LOG_PREFIX, hints.size(), str(has_pirate_hint), str(has_repair_help), str(has_combat_help), str(has_recovery_help), str(hints[0]) if not hints.is_empty() else ""])
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
	print("%s combatExecuted=true projectileSpawned=%s retaliationFired=%s targetIndex=%d targetDamaged=%s playerDamaged=%s destroyScenarioPrepared=%s destroyProjectileSpawned=%s targetDestroyed=%s destroyedTargetBlocked=%s retargetedAfterDestroyed=%s retargetedTargetIndex=%d playerDisableRetaliationFired=%s playerDisabled=%s playerDisabledStatusVisible=%s playerDisabledExplosion=%s disabledFireBlocked=%s disabledFireGuidance=%s disabledSecondaryBlocked=%s disabledChangeSecondaryBlocked=%s disabledAutopilotGuidance=%s disabledHyperModeGuidance=%s disabledHyperSelectGuidance=%s disabledMovementBlocked=%s disabledSaveBlocked=%s disabledServiceRefuelBlocked=%s disabledServiceRepairBlocked=%s disabledServiceClemencyBlocked=%s disabledMissionAcceptBlocked=%s disabledTradeBuyBlocked=%s disabledTradeSellBlocked=%s disabledOutfitBuyBlocked=%s disabledShipBuyBlocked=%s recoveryTriggered=%s playerRecovered=%s recoveryStatusVisible=%s disabledJumpGuidance=%s disabledLandGuidance=%s explosionTriggered=%s explosionSourceLabel=%s projectilesRemaining=%d beforeShield=%d afterShield=%d beforeHull=%d afterHull=%d playerShieldBefore=%d playerShieldAfter=%d playerHullBefore=%d playerHullAfter=%d weapon=%s sourceResourceId=%d sourceStockName=\"%s\" sourceMassDmg=%d sourceEnergyDmg=%d sourceReload=%d sourceCount=%d appliedShieldDamage=%d appliedHullDamage=%d sourceAppliedFields=%s sourceLabel=terminal-velocity-source-mined-combat-scaffold oracleStatus=classic_runtime_weapon_timing_pending status=\"%s\"" % [COMBAT_EVENT_LOG_PREFIX, str(spawned), str(retaliation_fired), target_index, str(target_damaged), str(player_damaged), str(destroy_prepared), str(destroy_projectile_spawned), str(target_destroyed), str(destroyed_target_blocked), str(retargeted_after_destroyed), retargeted_target_index, str(player_disable_retaliation_fired), str(player_disabled), str(player_disabled_status_visible), str(player_disabled_explosion), str(disabled_fire_blocked), str(disabled_fire_guidance), str(disabled_secondary_blocked), str(disabled_change_secondary_blocked), str(disabled_autopilot_guidance), str(disabled_hyper_mode_guidance), str(disabled_hyper_select_guidance), str(disabled_movement_blocked), str(disabled_save_blocked), str(disabled_service_refuel_blocked), str(disabled_service_repair_blocked), str(disabled_service_clemency_blocked), str(disabled_mission_accept_blocked), str(disabled_trade_buy_blocked), str(disabled_trade_sell_blocked), str(disabled_outfit_buy_blocked), str(disabled_ship_buy_blocked), str(recovery_triggered), str(player_recovered), str(recovery_status_visible), str(disabled_jump_guidance), str(disabled_land_guidance), str(explosion_triggered), latest_explosion_source, projectiles.size(), before_shields, after_shields, before_hull, after_hull, before_player_shields, after_player_shields, before_player_hull, after_player_hull, str(primary_weapon.get("name", "Primary")), source_resource_id, source_stock_name, source_mass_damage, source_energy_damage, source_reload, source_count, applied_shield_damage, applied_hull_damage, source_applied_fields, status_line])
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
	print("%s firstShotSpawned=%s immediateSecondShotBlocked=%s cooldownFrames=%d cooldownCleared=%s shotAfterCooldownSpawned=%s secondaryBlocked=%s sourceReload=%d sourceLabel=terminal-velocity-source-mined-combat-guardrail-scaffold oracleStatus=classic_runtime_weapon_timing_pending status=\"%s\"" % [COMBAT_GUARDRAIL_EVENT_LOG_PREFIX, str(first_shot_spawned), str(cooldown_blocked), int(cooldown_after_first), str(cooldown_cleared), str(third_shot_spawned), str(secondary_blocked), source_reload, status_line])
	get_tree().quit(0)

func _run_target_selection_log() -> void:
	_reset_travel_state()
	status_messages.clear()
	pos = Vector2.ZERO
	vel = Vector2.ZERO
	selected_target_index = 0
	var target_count := _npc_world_offsets().size()
	var initial_target := selected_target_index
	_cycle_target(1)
	var cycled_target := selected_target_index
	var cycled_status := status_line
	var cycled_status_has_target := cycled_status.contains("Target: Contact")
	_select_closest_target()
	var closest_target := selected_target_index
	var closest_status := status_line
	var closest_status_has_closest := closest_status.contains("Closest target: Contact")
	print("%s initialTarget=%d cycledTarget=%d closestTarget=%d targetCount=%d cycledStatusHasTarget=true actualCycledStatusHasTarget=%s closestStatusHasClosest=true actualClosestStatusHasClosest=%s cycledStatus=\"%s\" closestStatus=\"%s\" sourceLabel=terminal-velocity-target-selection-scaffold oracleStatus=classic_runtime_target_selection_pending" % [TARGET_SELECTION_EVENT_LOG_PREFIX, initial_target, cycled_target, closest_target, target_count, str(cycled_status_has_target), str(closest_status_has_closest), cycled_status, closest_status])
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
	print("%s routeToSolSelected=%s system=%s government=\"%s\" event=destroy_patrol manualBacked=true consequenceApplied=%s combatExecuted=true projectileSpawned=%s targetDestroyed=%s explosionTriggered=%s targetIndex=%d legalBefore=%d legalAfter=%d reputationBefore=%d reputationAfter=%d pirateReputationBefore=%d pirateReputationAfter=%d status=\"%s\" sourceLabel=terminal-velocity-classic-resource-govt-penalty-semantics oracleStatus=classic_runtime_combat_resolution_pending" % [LEGAL_CONSEQUENCE_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), government_name, str(applied), str(projectile_spawned), str(target_destroyed), str(explosion_triggered), target_index, before_legal, after_legal, before_reputation, after_reputation, before_pirate_reputation, after_pirate_reputation, status_line])
	get_tree().quit(0)

func _run_legal_clemency_log() -> void:
	_reset_travel_state()
	map_visible = true
	var route_to_sol_selected := _select_map_route_to_system("Sol")
	_move_to_scripted_hyperspace_distance()
	_jump()
	_try_land()
	var government_name := _current_government_name()
	legal_records[government_name] = -45
	reputation_scores[government_name] = int(reputation.get("mechanics", {}).get("clemencyMinReputation", 10))
	credits = int(reputation.get("mechanics", {}).get("clemencyCost", 1000)) + 500
	var before_legal := int(legal_records.get(government_name, 0))
	var before_credits := credits
	status_messages.clear()
	var paid := _pay_legal_clemency()
	var after_legal := int(legal_records.get(government_name, 0))
	var after_credits := credits
	print("%s routeToSolSelected=%s system=%s government=\"%s\" paid=%s legalBefore=%d legalAfter=%d creditsBefore=%d creditsAfter=%d status=\"%s\" sourceLabel=terminal-velocity-inferred-clemency-scaffold oracleStatus=approved_inference_pending_ev_classic_confirmation" % [LEGAL_CLEMENCY_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), government_name, str(paid), before_legal, after_legal, before_credits, after_credits, status_line])
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
	var risk_line := _commodity_legal_hint_line(commodity_id)
	var is_contraband := _commodity_is_contraband_for_government(commodity_id, government_name)
	var policy: Dictionary = governments.get("governments", {}).get(government_name, {})
	print("%s routeToSolSelected=%s system=%s government=\"%s\" commodity=%s isContraband=%s finePerTon=%d bribeAllowed=%s hint=\"%s\" sourceLabel=terminal-velocity-classic-resource-smuggling-risk-surface oracleStatus=classic_runtime_scan_frequency_and_ui_wording_pending" % [CONTRABAND_RISK_EVENT_LOG_PREFIX, str(route_to_sol_selected), current_system.get("name", "?"), government_name, commodity_id, str(is_contraband), int(policy.get("finePerTon", 0)), str(policy.get("bribeAllowed", false)), risk_line])
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
	var ship_round_trip := player_ship_id == saved_ship_id
	var cargo_space_round_trip := cargo_space == saved_cargo_space
	var status_round_trip := status_line == saved_status_line and status_messages == saved_status_messages
	var resume_succeeded := save_succeeded and system_round_trip and fuel_round_trip and credits_round_trip and mission_round_trip and strict_round_trip and outfit_round_trip and weapon_round_trip and ship_round_trip and cargo_space_round_trip and status_round_trip
	var save_status := "saveSucceeded=true" if save_succeeded else "saveSucceeded=false"
	var resume_status := "resumeSucceeded=true" if resume_succeeded else "resumeSucceeded=false"
	var system_status := "systemRoundTrip=true" if system_round_trip else "systemRoundTrip=false"
	var fuel_status := "fuelRoundTrip=true" if fuel_round_trip else "fuelRoundTrip=false"
	var credits_status := "creditsRoundTrip=true" if credits_round_trip else "creditsRoundTrip=false"
	var mission_status := "missionRoundTrip=true" if mission_round_trip else "missionRoundTrip=false"
	var strict_status := "strictPlayRoundTrip=true" if strict_round_trip else "strictPlayRoundTrip=false"
	var outfit_status := "outfitRoundTrip=true" if outfit_round_trip else "outfitRoundTrip=false"
	var weapon_status := "weaponRoundTrip=true" if weapon_round_trip else "weaponRoundTrip=false"
	var ship_status := "shipRoundTrip=true" if ship_round_trip else "shipRoundTrip=false"
	var cargo_space_status := "cargoSpaceRoundTrip=true" if cargo_space_round_trip else "cargoSpaceRoundTrip=false"
	var status_round_trip_status := "statusRoundTrip=true" if status_round_trip else "statusRoundTrip=false"
	print("%s pilot=\"%s\" routeToSolSelected=%s acceptedAtBody=\"%s\" acceptedMission=%s %s %s %s %s %s %s %s %s %s %s %s %s savedSystem=%s resumedSystem=%s savedFuel=%d resumedFuel=%d savedCredits=%d resumedCredits=%d savedShip=%s resumedShip=%s savedCargoSpace=%d resumedCargoSpace=%d savedOutfits=%s resumedOutfits=%s savedWeapons=%s resumedWeapons=%s savedStatusMessages=%s resumedStatusMessages=%s activeMissions=%s strictPlay=%s sourceLabel=terminal-velocity-save-scaffold oracleStatus=save_resume_pending_ev_classic_file_trace status=\"%s\"" % [PILOT_SAVE_RESUME_EVENT_LOG_PREFIX, loaded_pilot_name, str(route_to_sol_selected), str(accepted_body.get("name", "None")), accepted_mission_id, save_status, resume_status, system_status, fuel_status, credits_status, mission_status, strict_status, outfit_status, weapon_status, ship_status, cargo_space_status, status_round_trip_status, saved_system, str(current_system.get("name", "?")), saved_fuel, player_fuel, saved_credits, credits, saved_ship_id, player_ship_id, saved_cargo_space, cargo_space, JSON.stringify(saved_outfits), JSON.stringify(owned_outfits), JSON.stringify(saved_weapons), JSON.stringify(owned_weapons), JSON.stringify(saved_status_messages), JSON.stringify(status_messages), JSON.stringify(active_missions), str(strict_play_selected), status_line])
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
	var cargo_released := int(mission.get("cargoTons", 0)) if not mission.is_empty() else 0
	active_missions.erase(selected_id)
	mission_acceptance_days.erase(str(selected_id))
	cargo = max(0, cargo - cargo_released)
	aborted_mission_history.append(_mission_abort_record(mission, selected_id, cargo_released))
	_set_status("Aborted mission: %s; released %d cargo tons" % [str(mission.get("title", selected_id)) if not mission.is_empty() else selected_id, cargo_released])
	_play_sound("ui_click")
	return true

func _mission_abort_record(mission: Dictionary, mission_id: String, cargo_released: int) -> Dictionary:
	return {
		"id": mission_id,
		"title": str(mission.get("title", mission_id)) if not mission.is_empty() else mission_id,
		"system": str(current_system.get("name", "?")),
		"body": str(_current_body().get("name", "?")),
		"cargo_released": cargo_released,
		"sourceLabel": "terminal-velocity-mission-abort-scaffold",
		"oracleStatus": "mission_abort_pending_classic_runtime_or_manual_trace",
	}

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
	var warning := " — refuel before full route" if cost > player_fuel else ""
	return "Route fuel: %d hop(s), cost %d, fuel %d/%d%s" % [hops, cost, player_fuel, _max_player_fuel(), warning]

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
		"owned_outfits": owned_outfits,
		"owned_weapons": owned_weapons,
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
	owned_outfits = data.get("owned_outfits", owned_outfits)
	owned_weapons = data.get("owned_weapons", owned_weapons)
	reputation_scores = data.get("reputation_scores", reputation_scores)
	legal_records = data.get("legal_records", legal_records)
	status_line = str(data.get("status_line", status_line))
	status_messages.clear()
	for message in data.get("status_messages", []):
		status_messages.append(str(message))
	while status_messages.size() > 6:
		status_messages.remove_at(0)
	turn_cell_progress = 0.0

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
	selected_target_index = (selected_target_index + dir + targets.size()) % targets.size()
	var posture := " hostile legal patrol" if _legal_patrol_hostile_posture_active(_current_government_name()) else ""
	status_line = "Target: Contact %d%s at %.0f range" % [selected_target_index + 1, posture, pos.distance_to(targets[selected_target_index])]

func _select_closest_target() -> void:
	var targets := _npc_world_offsets()
	if targets.is_empty():
		selected_target_index = 0
		status_line = "No scanner targets"
		return
	var closest_index := 0
	var closest_distance := pos.distance_to(targets[0])
	for i in range(1, targets.size()):
		var distance := pos.distance_to(targets[i])
		if distance < closest_distance:
			closest_distance = distance
			closest_index = i
	selected_target_index = closest_index
	var posture := " hostile legal patrol" if _legal_patrol_hostile_posture_active(_current_government_name()) else ""
	status_line = "Closest target: Contact %d%s at %.0f range" % [selected_target_index + 1, posture, closest_distance]

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

func _government_crime_tolerance_score(government_name: String) -> int:
	var mechanics: Dictionary = reputation.get("mechanics", {})
	var tolerance_by_government: Dictionary = mechanics.get("crimeToleranceLegalScoreByGovernment", {})
	return int(tolerance_by_government.get(government_name, mechanics.get("crimeToleranceLegalScore", mechanics.get("patrolHostileLegalScore", -60))))

func _legal_service_access_allowed(government_name: String) -> bool:
	return _government_docking_allowed(government_name)

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
	status_line = "Autopilot not implemented yet"

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
	_set_status("Secondary weapon not loaded; primary combat scaffold available with Tab")

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
	_set_status("Secondary weapon selection: no secondary weapons installed")

func _primary_weapon_stats() -> Dictionary:
	var weapon_id := str(player_ship.get("weaponId", "laser_cannon"))
	if owned_weapons.size() > 0:
		for owned_id in owned_weapons.keys():
			if int(owned_weapons.get(owned_id, 0)) > 0:
				weapon_id = str(owned_id)
				break
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
	afterburner_fuel_progress = 0.0

func _advance_weapon_cooldowns(delta: float) -> void:
	primary_weapon_cooldown_frames = maxf(0.0, primary_weapon_cooldown_frames - delta * 60.0)

func _primary_weapon_reload_message() -> String:
	return "Primary weapon reloading; wait for source-backed reload cadence"

func _player_disabled() -> bool:
	return player_hull <= 0

func _player_disabled_action_message() -> String:
	return "Player ship disabled; reload or start a new pilot before continuing actions"

func _disabled_player_action_blocked() -> bool:
	if not _player_disabled():
		return false
	_set_status(_player_disabled_action_message())
	return true

func _player_recovery_message() -> String:
	return "Recovered disabled player ship; Terminal Velocity reload/new-pilot recovery scaffold"

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
	_play_sound("ui_click")
	return true

func _spawn_npc_retaliation_projectile(target_index: int) -> bool:
	var targets := _npc_world_offsets()
	if target_index < 0 or target_index >= targets.size() or _target_destroyed(target_index):
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
		var government_name := _current_government_name()
		if _legal_patrol_hostile_posture_active(government_name):
			_apply_reputation_event("destroy_patrol", government_name)
			_set_status(_legal_patrol_attack_message(government_name))
		else:
			_set_status("Contact %d disabled" % [target_index + 1])
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
	_play_sound("ui_click")

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
	_play_sound("ui_click")

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
	draw_string(font, Vector2(20, 56), "System: %s (%s: %s)    Destination: %s    Credits: %d    Fuel: %d/%d    Shields: %d/%d    Hull: %d/%d    Cargo: %d/%d (%d mission, %d free)    Ship: %s" % [current_system.get("name", "?"), government_name, legal_status, destination, credits, player_fuel, _max_player_fuel(), player_shields, _max_player_shields(), player_hull, _max_player_hull(), cargo, cargo_space, _mission_reserved_cargo_tons(), _cargo_available_tons(), player_ship_id], HORIZONTAL_ALIGNMENT_LEFT, 1220, 16, Color(0.70, 0.86, 1.0))
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
	draw_string(font, Vector2(1024, 280), "Target: Contact %d  %.0f" % [selected_target_index + 1, target_range], HORIZONTAL_ALIGNMENT_LEFT, 230, 14, Color(1.0, 0.82, 0.35))
	draw_string(font, Vector2(20, 785), "EV keys: Arrows move  L land/launch  N next target  R closest target  \\ hyper select  H hyper mode  J jump  M map  G mission route  F6 save  F10 help  P/I info  Esc quit  |  " + status_line, HORIZONTAL_ALIGNMENT_LEFT, 1230, 15, Color(0.82, 0.88, 0.95))

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
		"Hull: %d/%d (repair cost %d cr)" % [player_hull, _max_player_hull(), _repair_cost()],
		"Government/legal: %s" % _legal_warning_line(_current_government_name()),
		"Reputation scores: %s" % _inventory_dictionary_summary(reputation_scores),
		"Legal records: %s" % _inventory_dictionary_summary(legal_records),
		"Outfits: %s" % _inventory_dictionary_summary(owned_outfits),
		"Weapons: %s" % _inventory_dictionary_summary(owned_weapons),
		_primary_weapon_inventory_line(),
		_secondary_weapon_inventory_line(),
	]
	lines.append_array(_active_mission_player_info_lines())
	return lines

func _primary_weapon_inventory_line() -> String:
	var weapon := _primary_weapon_stats()
	var weapon_name := str(weapon.get("name", weapon.get("id", "Unknown")))
	var source_name := str(weapon.get("sourceStockName", weapon_name))
	return "Primary weapon: %s — source %s; exact Classic cadence pending" % [weapon_name, source_name]

func _secondary_weapon_inventory_line() -> String:
	return "Secondary weapon: No Secondary Weapon — original-runtime-observed starting HUD; secondary firing scaffold pending"

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
	return [
		"Terminal Velocity helper/scaffold — not an EV Classic fidelity claim.",
		"Flight: Arrows/WASD thrust and turn; L lands or launches; J jumps to the selected route.",
		"Map: M opens map; \\ cycles linked systems; Shift-click queues linked route stops; Backspace/Delete clears route.",
		"Map service/legal summary: selected systems show Terminal Velocity station services and legal risk.",
		"Mission objective marker: active mission destinations are highlighted on the map.",
		"Mission route helper: G queues the active mission destination when known.",
		"Mission cargo: I toggles mission log with reserved tons; HUD and market show mission/free cargo.",
		"Refuel: landed ports show F5 availability; F5 refuels when service exists.",
		"Repair: landed ports with repair service show F7; hull repair costs credits and keeps source-boundary labels.",
		"Combat: Tab fires primary; N cycles targets; R selects closest target; exact Classic cadence/effects still pending.",
		"Recovery: F8 resets a disabled player ship as a Terminal Velocity scaffold pending Classic death/reload evidence.",
		"Legal inference: hostile patrol fire worsens legal/reputation scaffold state; landed C buys clemency when eligible.",
		"Pilot persistence: F6 saves current pilot progress for title-screen Open Pilot resume.",
		"Player info: P toggles player info with ship, cargo, fuel, outfits, and weapons.",
		"Landing: F1 Mission Computer, F2 Commodity Exchange, F3 Outfitter, F4 Shipyard.",
		"Buying/selling: Enter accepts selected mission; B buys selected commodity, outfit, or ship; S sells selected cargo.",
		"Trade route helper: linked-market profit hints are Terminal Velocity scaffold.",
		"Shipyard/outfitter: listings show local manifest deltas/effects before buying.",
		"Messages: recent success and blocked-reason feedback appears under the HUD.",
		"F10 closes this help overlay. Exact Classic behavior still needs source/runtime evidence."
	]

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
	var government_name := _current_government_name()
	if not _legal_service_access_allowed(government_name):
		_set_status(_legal_service_blocked_message(government_name))
		return
	var sale_items := _outfitter_sale_items(_current_body())
	if sale_items.is_empty():
		_set_status("No outfitter stock")
		return
	var item: Dictionary = sale_items[selected_landing_item % sale_items.size()]
	var price := int(item.get("price", 0))
	if credits < price:
		_set_status("Not enough credits")
		return
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
	_play_sound("ui_click")

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
	var government_name := _current_government_name()
	if not _legal_service_access_allowed(government_name):
		_set_status(_legal_service_blocked_message(government_name))
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
	credits -= price
	player_ship = new_ship
	player_ship_id = ship_id
	var player_frame_set := _load_ship_frame_set(player_ship)
	player_frames = player_frame_set["frames"]
	player_frame_offsets = player_frame_set["offsets"]
	cargo_space = int(player_ship.get("cargoSpace", cargo_space))
	cargo = min(cargo, cargo_space)
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
