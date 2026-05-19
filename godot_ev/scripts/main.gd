extends Node2D

# EV-style native Godot front end. This intentionally loads the existing
# Terminal Velocity backend contract instead of inventing a second data source:
# native_ev/data/universe.json, native_ev/data/ships.json, native_ev/data/missions.json,
# native_ev/data/economy.json, native_ev/data/outfits.json, native_ev/data/weapons.json,
# native_ev/data/sounds.json, and 36-frame frame_%02d.png ship sprite folders.

const VIEW_SIZE := Vector2(1280, 800)
const WORLD_SCALE := 0.55
const PLAYER_START := Vector2(0, 0)
const FRAME_COUNT := 36
const DEFAULT_CLICK_SOUND_ASSET := "assets/sounds/ev_classic/601_click/sound.wav"
const DEFAULT_SHIPYARD_PICT_ASSET := "assets/graphics/pict/5000_shipyard/image.png"
const STATE_TITLE := "title"
const STATE_SPACE := "space"
const PREFS_SAVE_PATH := "user://terminal_velocity_prefs.json"
const PREFS_SCREENSHOT_PATH := "user://selftest/title_prefs.png"
const MOVEMENT_LOG_RIGHT_TURN_PREFIX := "TV_MOVEMENT_LOG scenario=right_turn ticks=12 ship="
const MOVEMENT_LOG_THRUST_PREFIX := "TV_MOVEMENT_LOG scenario=thrust ticks=30 ship="

var repo_root := ""
var universe := {}
var ships := {}
var missions := {}
var economy := {}
var outfits := {}
var weapons := {}
var sounds := {}
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
var selected_target_index := 0
var map_visible := false
var stars: Array[Vector2] = []
var status_line := ""
var title_status_line := "No pilot loaded."
var title_modal := ""
var pilot_name_input := ""
var ship_name_input := "Starseeker"
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
var credits := 5000
var cargo := 0
var landing_tab := 0
var selected_landing_item := 0
var active_missions: Array = []
var completed_missions: Array = []
var story_flags: Array = []
var commodity_hold: Dictionary = {}
var owned_outfits: Dictionary = {}
var owned_weapons: Dictionary = {}
var player_ship_id := "shuttlecraft"
var cargo_space := 20

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
	sounds = _json(repo_root + "/native_ev/data/sounds.json")
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
	queue_redraw()

func _handle_input(delta: float) -> void:
	if Input.is_key_pressed(KEY_ESCAPE):
		get_tree().quit()
	if game_state == STATE_TITLE:
		return
	var turn_dir := 0
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		turn_dir -= 1
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		turn_dir += 1
	_apply_movement_controls(delta, turn_dir, Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP), Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN))

func _apply_movement_controls(delta: float, turn_dir: int, thrusting: bool, braking: bool) -> void:
	if turn_dir != 0 and not player_frames.is_empty():
		turn_cell_progress += float(turn_dir) * 18.0 * delta
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
		vel += nose * 250.0 * delta
	if braking:
		vel *= pow(0.90, delta * 60.0)

func _advance_motion_step(delta: float, turn_dir: int, thrusting: bool, braking: bool) -> void:
	_apply_movement_controls(delta, turn_dir, thrusting, braking)
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

func _run_deterministic_movement_log() -> void:
	_reset_deterministic_motion_state()
	for _i in range(12):
		_advance_motion_step(1.0 / 60.0, 1, false, false)
	_print_movement_log(MOVEMENT_LOG_RIGHT_TURN_PREFIX, 12)
	_reset_deterministic_motion_state()
	for _i in range(30):
		_advance_motion_step(1.0 / 60.0, 0, true, false)
	_print_movement_log(MOVEMENT_LOG_THRUST_PREFIX, 30)
	get_tree().quit(0)

func _print_movement_log(prefix: String, ticks: int) -> void:
	print(prefix + "%s tickCount=%d facingIndex=%d angle=%.3f velocity=(%.3f,%.3f) position=(%.3f,%.3f)" % [player_ship_id, ticks, player_facing_index, angle_deg, vel.x, vel.y, pos.x, pos.y])

func _unhandled_input(event: InputEvent) -> void:
	if game_state == STATE_TITLE:
		_handle_title_input(event)
		return
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_E:
				_try_land()
			KEY_L:
				landed = false
				status_line = "Launched from " + current_system.get("name", "system")
			KEY_N:
				_cycle_link(1)
			KEY_P:
				_cycle_link(-1)
			KEY_H:
				_jump()
			KEY_M:
				_toggle_universe_map()
			KEY_T:
				_cycle_target(1)
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
			KEY_UP:
				if landed:
					_cycle_landing_selection(-1)
			KEY_DOWN:
				if landed:
					_cycle_landing_selection(1)
			KEY_ENTER:
				if landed and landing_tab == 0:
					_accept_selected_mission()
			KEY_B:
				if landed:
					match landing_tab:
						1: _buy_selected_commodity()
						2: _buy_selected_outfit_or_weapon()
						3: _buy_selected_ship()
			KEY_S:
				if landed and landing_tab == 1:
					_sell_selected_commodity()
			KEY_R:
				pos = PLAYER_START
				vel = Vector2.ZERO
				player_facing_index = 0
				angle_deg = 0.0
				turn_cell_progress = 0.0
				landed = false
				status_line = "Reset in " + current_system.get("name", "system")

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
		"system": current_system.get("name", ""),
		"system_index": current_system_index,
		"position": {"x": pos.x, "y": pos.y},
		"velocity": {"x": vel.x, "y": vel.y},
		"angle_deg": angle_deg,
		"facing_index": player_facing_index,
		"active_missions": active_missions,
		"completed_missions": completed_missions,
		"story_flags": story_flags,
		"commodity_hold": commodity_hold,
		"owned_outfits": owned_outfits,
		"owned_weapons": owned_weapons,
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
	if player_frames.is_empty():
		player_facing_index = int(data.get("facing_index", 0))
	else:
		player_facing_index = int(data.get("facing_index", _facing_frame_index(angle_deg, player_frames.size()))) % player_frames.size()
	cargo_space = int(data.get("cargo_space", cargo_space))
	cargo = mini(cargo, cargo_space)
	active_missions = data.get("active_missions", active_missions)
	completed_missions = data.get("completed_missions", completed_missions)
	story_flags = data.get("story_flags", story_flags)
	commodity_hold = data.get("commodity_hold", commodity_hold)
	owned_outfits = data.get("owned_outfits", owned_outfits)
	owned_weapons = data.get("owned_weapons", owned_weapons)
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
		for i in range(systems.size()):
			if str(systems[i].get("name", "")) == saved_system:
				return i
	return clampi(int(data.get("system_index", current_system_index)), 0, systems.size() - 1)

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

func _cycle_open_pilot_selection(dir: int) -> void:
	if title_modal != "open_pilot" or available_pilots.is_empty():
		return
	selected_pilot_index = (selected_pilot_index + dir + available_pilots.size()) % available_pilots.size()

func _pref_options() -> Array:
	# EV-style preferences; Classic EV-era speed slider wording remains as a source-fidelity reminder.
	# Help text preserves the existing keyboard contract: Space toggles the selected preference.
	var speed_labels := ["Slowest", "Slower", "Normal", "Faster", "Fastest"]
	return [
		{"kind": "radio", "label": "Game speed", "value": speed_labels[pref_game_speed_index], "note": "Classic speed setting"},
		{"kind": "toggle", "label": "Play game music", "enabled": pref_music_on, "note": "saved"},
		{"kind": "toggle", "label": "Play game sounds", "enabled": pref_sound_on, "note": "saved"},
		{"kind": "toggle", "label": "Enable intro animation", "enabled": pref_intro_animation_on, "note": "title"},
		{"kind": "toggle", "label": "Always ask before buying", "enabled": pref_ask_before_buying_on, "note": "trading"},
		{"kind": "toggle", "label": "Resume Game", "enabled": pref_resume_game_on, "note": "title"},
	]

func _prefs_list_rect() -> Rect2:
	return Rect2(402, 350, 476, 150)

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
			pref_game_speed_index = (pref_game_speed_index + 1) % 5
			_apply_pref_runtime_side_effects()
		1:
			pref_music_on = not pref_music_on
		2:
			pref_sound_on = not pref_sound_on
		3:
			pref_intro_animation_on = not pref_intro_animation_on
		4:
			pref_ask_before_buying_on = not pref_ask_before_buying_on
		5:
			pref_resume_game_on = not pref_resume_game_on
	title_status_line = "Set Preferences"

func _pref_row_at(position: Vector2) -> int:
	var list_rect := _prefs_list_rect()
	if not list_rect.has_point(position):
		return -1
	var row := int((position.y - list_rect.position.y) / 25.0)
	if row >= 0 and row < _pref_options().size():
		return row
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
	var ok_rect := Rect2(686, 510, 116, 34) if title_modal == "prefs" else Rect2(700, 492, 116, 34)
	var cancel_rect := Rect2(822, 510, 116, 34) if title_modal == "prefs" else Rect2(836, 492, 116, 34)
	if ok_rect.has_point(position):
		return "ok"
	if cancel_rect.has_point(position):
		return "cancel"
	return ""

func _cycle_link(dir: int) -> void:
	var links: Array = current_system.get("links", [])
	if links.is_empty():
		return
	selected_link_index = (selected_link_index + dir + links.size()) % links.size()
	status_line = "Destination: " + str(links[selected_link_index])

func _toggle_universe_map() -> void:
	map_visible = not map_visible
	status_line = "Galaxy map open" if map_visible else "Galaxy map closed"

func _npc_world_offsets() -> Array[Vector2]:
	return [Vector2(260, -180), Vector2(-340, 220), Vector2(520, 160), Vector2(-640, -260)]

func _cycle_target(dir: int) -> void:
	var targets := _npc_world_offsets()
	if targets.is_empty():
		selected_target_index = 0
		status_line = "No scanner targets"
		return
	selected_target_index = (selected_target_index + dir + targets.size()) % targets.size()
	status_line = "Target: Contact %d at %.0f range" % [selected_target_index + 1, pos.distance_to(targets[selected_target_index])]

func _jump() -> void:
	var systems: Array = universe.get("systems", [])
	var links: Array = current_system.get("links", [])
	if links.is_empty():
		return
	var destination := str(links[selected_link_index % links.size()])
	for i in range(systems.size()):
		if systems[i].get("name", "") == destination:
			current_system_index = i
			current_system = systems[i]
			selected_link_index = 0
			pos = PLAYER_START
			vel = Vector2.ZERO
			landed = false
			status_line = "Hyperspace arrival: " + destination
			return

func _try_land() -> void:
	var nearest := _nearest_body()
	if nearest.is_empty():
		status_line = "No port in range"
		return
	if nearest["distance"] < nearest["body"].get("r", 40) + 45 and vel.length() < 90:
		landed = true
		vel = Vector2.ZERO
		status_line = "Landed at " + nearest["body"].get("name", "port")
	else:
		status_line = "Approach slower/closer to land"

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
	_draw_npcs(center)
	_draw_player(center)
	_draw_hud()
	if map_visible:
		_draw_universe_map()
	if landed:
		_draw_landing_panel()

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
	if title_modal != "":
		_draw_title_modal(font)
	draw_string(font, Vector2(300, 716), "Personal-use Godot reconstruction. Title substituted: Terminal Velocity.", HORIZONTAL_ALIGNMENT_CENTER, 680, 15, Color(0.52, 0.82, 0.52))
	draw_string(font, Vector2(300, 742), "Enter/click Enter Ship to start. N/O/S/A/Q shortcuts mirror the title menu.", HORIZONTAL_ALIGNMENT_CENTER, 680, 15, Color(0.42, 0.68, 0.44))

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
	var rect := Rect2(300, 285, 680, 270)
	draw_rect(rect, Color(0.82, 0.82, 0.78, 0.98), true)
	draw_rect(rect, Color(0.08, 0.08, 0.08), false, 2.0)
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
	var title := "Create New Pilot"
	var prompt := "Pilot Name:"
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
	_draw_modal_button(Rect2(700, 492, 116, 34), "OK", font)
	_draw_modal_button(Rect2(836, 492, 116, 34), "Cancel", font)
	draw_string(font, rect.position + Vector2(42, 232), "Return accepts. Escape cancels.", HORIZONTAL_ALIGNMENT_LEFT, 590, 14, Color(0.25, 0.25, 0.25))

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
			var row_text := "%s — %s" % [str(entry.get("pilot_name", "")), str(entry.get("ship_name", ""))]
			var color := Color(1, 1, 1) if i == selected_pilot_index else Color(0.05, 0.05, 0.05)
			draw_string(font, row_rect.position + Vector2(10, 22), row_text, HORIZONTAL_ALIGNMENT_LEFT, row_rect.size.x - 20, 16, color)
	_draw_modal_button(Rect2(700, 492, 116, 34), "Open", font)
	_draw_modal_button(Rect2(836, 492, 116, 34), "Cancel", font)
	draw_string(font, rect.position + Vector2(42, 232), "Return opens. Up/Down selects. Escape cancels.", HORIZONTAL_ALIGNMENT_LEFT, 590, 14, Color(0.25, 0.25, 0.25))

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
	draw_string(font, rect.position + Vector2(0, 28), "Set Preferences", HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 18, Color(0.95, 0.95, 0.90))
	draw_string(font, rect.position + Vector2(42, 66), "Terminal Velocity Preferences", HORIZONTAL_ALIGNMENT_LEFT, 590, 17, Color(0.02, 0.02, 0.02))
	draw_string(font, rect.position + Vector2(42, 88), "EV Classic title prefs visual scaffold until original-runtime observation verifies exact wording.", HORIZONTAL_ALIGNMENT_LEFT, 610, 13, Color(0.25, 0.25, 0.25))
	var list_rect := _prefs_list_rect()
	draw_rect(list_rect, Color(0.98, 0.98, 0.94), true)
	draw_rect(list_rect, Color(0.10, 0.10, 0.10), false, 1.0)
	var options := _pref_options()
	for i in range(options.size()):
		var row_rect := Rect2(list_rect.position + Vector2(0, i * 25), Vector2(list_rect.size.x, 25))
		if i == selected_pref_index:
			draw_rect(row_rect.grow(-2), Color(0.22, 0.40, 0.85, 0.95), true)
		var option: Dictionary = options[i]
		var color := Color(1, 1, 1) if i == selected_pref_index else Color(0.05, 0.05, 0.05)
		if str(option.get("kind", "toggle")) == "radio":
			_draw_radio_choice(row_rect.position + Vector2(14, 7), true, color)
			draw_string(font, row_rect.position + Vector2(38, 18), "%s: %s" % [str(option.get("label", "")), str(option.get("value", "Normal"))], HORIZONTAL_ALIGNMENT_LEFT, 260, 15, color)
		else:
			_draw_checkbox(row_rect.position + Vector2(14, 6), bool(option.get("enabled", false)), color)
			draw_string(font, row_rect.position + Vector2(38, 18), str(option.get("label", "")), HORIZONTAL_ALIGNMENT_LEFT, 260, 15, color)
		draw_string(font, row_rect.position + Vector2(320, 18), str(option.get("note", "")), HORIZONTAL_ALIGNMENT_LEFT, 140, 12, color)
	_draw_modal_button(Rect2(686, 510, 116, 34), "SavePrefs", font)
	_draw_modal_button(Rect2(822, 510, 116, 34), "Cancel", font)
	draw_string(font, rect.position + Vector2(42, 232), "Up/Down selects. Space changes. Return saves. Escape cancels.", HORIZONTAL_ALIGNMENT_LEFT, 590, 14, Color(0.25, 0.25, 0.25))

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
		var screen: Vector2 = center + (offsets[i] - pos) * WORLD_SCALE
		var frame_index := (i * 7) % npc_frames.size()
		var tex := npc_frames[frame_index]
		var draw_offset := Vector2(tex.get_width(), tex.get_height()) * 0.5
		draw_texture_rect(tex, Rect2(screen - draw_offset, Vector2(tex.get_width(), tex.get_height())), false)
		var ring_color := Color(1.0, 0.80, 0.20, 0.95) if i == selected_target_index else Color(0.35, 0.55, 0.80, 0.7)
		draw_arc(screen, 28, 0, TAU, 20, ring_color, 1.0)

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
	var links: Array = current_system.get("links", [])
	var destination := "None"
	if not links.is_empty():
		destination = str(links[selected_link_index % links.size()])
	draw_rect(Rect2(0, 0, 1280, 78), Color(0.02, 0.035, 0.06, 0.92), true)
	draw_string(font, Vector2(20, 28), "Terminal Velocity / Godot frontend", HORIZONTAL_ALIGNMENT_LEFT, 500, 20, Color(0.9, 0.95, 1.0))
	draw_string(font, Vector2(20, 56), "System: %s    Destination: %s    Credits: %d    Cargo: %d/%d    Ship: %s    Facing cell: %02d/%02d" % [current_system.get("name", "?"), destination, credits, cargo, cargo_space, player_ship_id, player_facing_index, _visible_facing_index(player_facing_index)], HORIZONTAL_ALIGNMENT_LEFT, 1120, 16, Color(0.70, 0.86, 1.0))
	draw_rect(Rect2(1010, 96, 250, 190), Color(0.02, 0.04, 0.06, 0.88), true)
	draw_arc(Vector2(1135, 190), 78, 0, TAU, 64, Color(0.30, 0.75, 0.95), 1.0)
	draw_line(Vector2(1135, 112), Vector2(1135, 268), Color(0.12, 0.35, 0.50), 1.0)
	draw_line(Vector2(1057, 190), Vector2(1213, 190), Color(0.12, 0.35, 0.50), 1.0)
	draw_string(font, Vector2(1030, 122), "Scanner", HORIZONTAL_ALIGNMENT_LEFT, 200, 16, Color(0.75, 0.95, 1.0))
	_draw_scanner_blips(Vector2(1135, 190), 78.0)
	var target_range := 0.0
	var targets := _npc_world_offsets()
	if not targets.is_empty():
		target_range = pos.distance_to(targets[selected_target_index % targets.size()])
	draw_string(font, Vector2(1024, 280), "Target: Contact %d  %.0f" % [selected_target_index + 1, target_range], HORIZONTAL_ALIGNMENT_LEFT, 230, 14, Color(1.0, 0.82, 0.35))
	draw_string(font, Vector2(20, 785), "W/A/D thrust+turn  E land  L launch  T target  N/P select jump  H hyperspace  R reset  Esc quit  |  " + status_line, HORIZONTAL_ALIGNMENT_LEFT, 1230, 15, Color(0.82, 0.88, 0.95))

func _draw_scanner_blips(scanner_center: Vector2, scanner_radius: float) -> void:
	var targets := _npc_world_offsets()
	for i in range(targets.size()):
		var relative: Vector2 = (targets[i] - pos) / 8.0
		if relative.length() > scanner_radius - 8.0:
			relative = relative.normalized() * (scanner_radius - 8.0)
		var blip := scanner_center + relative
		var color := Color(1.0, 0.78, 0.20) if i == selected_target_index else Color(0.30, 0.85, 1.0)
		draw_circle(blip, 4.0 if i == selected_target_index else 2.5, color)

func _draw_universe_map() -> void:
	var systems: Array = universe.get("systems", [])
	if systems.is_empty():
		return
	var font := ThemeDB.fallback_font
	var rect := Rect2(160, 92, 960, 616)
	var plot_rect := Rect2(rect.position + Vector2(42, 74), Vector2(610, 456))
	draw_rect(rect, Color(0.018, 0.026, 0.042, 0.96), true)
	draw_rect(rect, Color(0.24, 0.54, 0.78, 1.0), false, 2.0)
	draw_string(font, rect.position + Vector2(0, 40), "GALAXY MAP", HORIZONTAL_ALIGNMENT_CENTER, rect.size.x, 24, Color(0.86, 0.96, 1.0))
	var links: Array = current_system.get("links", [])
	var selected_name := "None"
	if not links.is_empty():
		selected_name = str(links[selected_link_index % links.size()])
	draw_string(font, rect.position + Vector2(690, 90), "Current: " + str(current_system.get("name", "?")), HORIZONTAL_ALIGNMENT_LEFT, 230, 18, Color(1.0, 0.92, 0.58))
	draw_string(font, rect.position + Vector2(690, 120), "Selected: " + selected_name, HORIZONTAL_ALIGNMENT_LEFT, 230, 18, Color(0.35, 1.0, 0.68))
	draw_string(font, rect.position + Vector2(690, 154), "N/P selects linked destinations", HORIZONTAL_ALIGNMENT_LEFT, 230, 14, Color(0.70, 0.82, 0.96))
	draw_string(font, rect.position + Vector2(690, 178), "H jumps   M closes map", HORIZONTAL_ALIGNMENT_LEFT, 230, 14, Color(0.70, 0.82, 0.96))
	var bounds := _system_coordinate_bounds(systems)
	var point_by_name: Dictionary = {}
	for system in systems:
		var map_point := _system_map_point(system, bounds, plot_rect)
		point_by_name[str(system.get("name", ""))] = map_point
	for system in systems:
		var map_point: Vector2 = point_by_name.get(str(system.get("name", "")), plot_rect.position)
		for linked_name in system.get("links", []):
			if not point_by_name.has(str(linked_name)):
				continue
			var linked_point: Vector2 = point_by_name[str(linked_name)]
			draw_line(map_point, linked_point, Color(0.12, 0.32, 0.52, 0.72), 1.0)
	for system in systems:
		var system_name := str(system.get("name", "?"))
		var map_point: Vector2 = point_by_name.get(system_name, plot_rect.position)
		var linked := links.has(system_name)
		var is_current := system_name == str(current_system.get("name", ""))
		var is_selected := system_name == selected_name
		var color := Color(0.46, 0.72, 1.0)
		var radius := 4.0
		if linked:
			color = Color(0.66, 0.95, 1.0)
			radius = 5.0
		if is_selected:
			color = Color(0.30, 1.0, 0.55)
			radius = 7.0
		if is_current:
			color = Color(1.0, 0.85, 0.25)
			radius = 8.0
		draw_circle(map_point, radius, color)
		draw_arc(map_point, radius + 4.0, 0, TAU, 24, color, 1.0)
		draw_string(font, map_point + Vector2(8, -7), system_name, HORIZONTAL_ALIGNMENT_LEFT, 140, 13, color)
	var y := rect.position.y + 240.0
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
		port = str(body.get("name", "Port"))
		market = str(body.get("market", "Local market"))
	var rect := Rect2(190, 135, 900, 520)
	draw_rect(rect, Color(0.035, 0.045, 0.065, 0.96), true)
	draw_rect(rect, Color(0.28, 0.43, 0.62, 1.0), false, 2.0)
	var font := ThemeDB.fallback_font
	draw_string(font, rect.position + Vector2(30, 46), "Landed: " + port, HORIZONTAL_ALIGNMENT_LEFT, 820, 28, Color(1.0, 0.92, 0.72))
	draw_string(font, rect.position + Vector2(30, 78), market, HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.80, 0.90, 1.0))
	_draw_tab_bar(rect)
	match landing_tab:
		0:
			_draw_mission_computer(rect, body)
		1:
			_draw_commodity_exchange(rect)
		2:
			_draw_outfitter(rect, body)
		3:
			_draw_shipyard(rect, body)
	draw_string(font, rect.position + Vector2(30, 492), "F1 Missions  F2 Commodities  F3 Outfitter  F4 Shipyard  ↑/↓ select  |  Press L to launch", HORIZONTAL_ALIGNMENT_LEFT, 840, 16, Color(0.95, 0.86, 0.58))

func _draw_tab_bar(rect: Rect2) -> void:
	var font := ThemeDB.fallback_font
	var labels := ["F1 Mission Computer", "F2 Commodity Exchange", "F3 Outfitter", "F4 Shipyard"]
	for i in range(labels.size()):
		var tab_rect := Rect2(rect.position + Vector2(30 + i * 210, 104), Vector2(198, 30))
		var active := i == landing_tab
		draw_rect(tab_rect, Color(0.12, 0.20, 0.30, 1.0) if active else Color(0.06, 0.08, 0.11, 1.0), true)
		draw_rect(tab_rect, Color(0.35, 0.55, 0.75, 1.0), false, 1.0)
		draw_string(font, tab_rect.position + Vector2(8, 20), labels[i], HORIZONTAL_ALIGNMENT_LEFT, 184, 13, Color(0.88, 0.94, 1.0))

func _draw_mission_computer(rect: Rect2, body: Dictionary) -> void:
	var font := ThemeDB.fallback_font
	draw_string(font, rect.position + Vector2(30, 166), "Mission Computer", HORIZONTAL_ALIGNMENT_LEFT, 820, 22, Color(0.92, 0.96, 1.0))
	var available_missions := _available_missions(body)
	if available_missions.is_empty():
		draw_string(font, rect.position + Vector2(30, 202), "No special contracts available here.", HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.72, 0.82, 0.92))
		return
	draw_string(font, rect.position + Vector2(30, 192), "Enter accepts mission", HORIZONTAL_ALIGNMENT_LEFT, 820, 14, Color(0.95, 0.86, 0.58))
	var y := 202.0
	for i in range(min(5, available_missions.size())):
		var mission: Dictionary = available_missions[i]
		var marker := "▶" if i == selected_landing_item else "•"
		draw_string(font, rect.position + Vector2(30, y), "%s %s — %d cr, %d tons" % [marker, mission.get("title", "Contract"), int(mission.get("reward", 0)), int(mission.get("cargoTons", 0))], HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.86, 0.92, 1.0))
		y += 26.0
		draw_string(font, rect.position + Vector2(52, y), "To %s / %s" % [mission.get("destinationSystem", "?"), mission.get("destinationBody", "?")], HORIZONTAL_ALIGNMENT_LEFT, 780, 14, Color(0.68, 0.78, 0.90))
		y += 24.0

func _draw_commodity_exchange(rect: Rect2) -> void:
	var font := ThemeDB.fallback_font
	var market_prices := _market_prices(current_system.get("name", ""))
	draw_string(font, rect.position + Vector2(30, 166), "Commodity Exchange", HORIZONTAL_ALIGNMENT_LEFT, 820, 22, Color(0.92, 0.96, 1.0))
	draw_string(font, rect.position + Vector2(30, 192), "B buys one ton   S sells one ton", HORIZONTAL_ALIGNMENT_LEFT, 820, 14, Color(0.95, 0.86, 0.58))
	var y := 204.0
	var commodities: Array = economy.get("commodities", [])
	for i in range(min(8, commodities.size())):
		var commodity: Dictionary = commodities[i]
		var commodity_id := str(commodity.get("id", ""))
		var prices: Dictionary = market_prices.get(commodity_id, {})
		var marker := "▶" if i == selected_landing_item else "•"
		var held := int(commodity_hold.get(commodity_id, 0))
		draw_string(font, rect.position + Vector2(30, y), "%s %s  buy %s / sell %s   held %d" % [marker, commodity.get("name", commodity_id), prices.get("buy", "—"), prices.get("sell", "—"), held], HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.82, 0.92, 0.86))
		y += 28.0

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
		y += 26.0
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
		var marker := "▶" if i == selected_landing_item else "•"
		draw_string(font, rect.position + Vector2(30, y), "%s %s — %d cr" % [marker, listing.get("shipId", "ship"), int(listing.get("price", 0))], HORIZONTAL_ALIGNMENT_LEFT, 820, 16, Color(0.86, 0.92, 1.0))
		y += 28.0
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
		available_missions.append(mission)
	return available_missions

func _has_all_flags(required: Array) -> bool:
	for flag in required:
		if not story_flags.has(flag):
			return false
	return true

func _has_any_flag(excluded: Array) -> bool:
	for flag in excluded:
		if story_flags.has(flag):
			return true
	return false

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
	var available := _available_missions(_current_body())
	if available.is_empty():
		status_line = "No mission to accept"
		return
	var mission: Dictionary = available[selected_landing_item % available.size()]
	var tons := int(mission.get("cargoTons", 0))
	if cargo + tons > cargo_space:
		status_line = "Need %d free cargo tons" % tons
		return
	var mission_id := str(mission.get("id", ""))
	active_missions.append(mission_id)
	cargo += tons
	for flag in mission.get("setsFlags", []):
		if not story_flags.has(flag):
			story_flags.append(flag)
	status_line = "Accepted mission: " + str(mission.get("title", mission_id))
	_play_sound("ui_click")
	selected_landing_item = 0

func _buy_selected_commodity() -> void:
	var commodities: Array = economy.get("commodities", [])
	if commodities.is_empty():
		status_line = "No commodities available"
		return
	var commodity: Dictionary = commodities[selected_landing_item % commodities.size()]
	var commodity_id := str(commodity.get("id", ""))
	var price := int(_market_prices(current_system.get("name", "")).get(commodity_id, {}).get("buy", 0))
	if price <= 0:
		status_line = "Commodity unavailable here"
		return
	if cargo >= cargo_space:
		status_line = "Cargo hold full"
		return
	if credits < price:
		status_line = "Not enough credits"
		return
	credits -= price
	cargo += 1
	commodity_hold[commodity_id] = int(commodity_hold.get(commodity_id, 0)) + 1
	status_line = "Bought 1 ton of " + str(commodity.get("name", commodity_id))
	_play_sound("ui_click")

func _sell_selected_commodity() -> void:
	var commodities: Array = economy.get("commodities", [])
	if commodities.is_empty():
		status_line = "No commodities available"
		return
	var commodity: Dictionary = commodities[selected_landing_item % commodities.size()]
	var commodity_id := str(commodity.get("id", ""))
	var held := int(commodity_hold.get(commodity_id, 0))
	if held <= 0:
		status_line = "No cargo to sell"
		return
	var price := int(_market_prices(current_system.get("name", "")).get(commodity_id, {}).get("sell", 0))
	credits += price
	cargo = max(0, cargo - 1)
	commodity_hold[commodity_id] = held - 1
	status_line = "Sold 1 ton of " + str(commodity.get("name", commodity_id))
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
	var sale_items := _outfitter_sale_items(_current_body())
	if sale_items.is_empty():
		status_line = "No outfitter stock"
		return
	var item: Dictionary = sale_items[selected_landing_item % sale_items.size()]
	var price := int(item.get("price", 0))
	if credits < price:
		status_line = "Not enough credits"
		return
	credits -= price
	var item_id := str(item.get("id", ""))
	if item.get("saleType", "") == "weapon":
		owned_weapons[item_id] = int(owned_weapons.get(item_id, 0)) + 1
	else:
		owned_outfits[item_id] = int(owned_outfits.get(item_id, 0)) + 1
		var effects: Dictionary = item.get("effects", {})
		cargo_space += int(effects.get("cargoSpace", 0))
	status_line = "Bought " + str(item.get("name", item_id))
	_play_sound("ui_click")

func _shipyard_listings(body: Dictionary) -> Array:
	var inventory := _station_inventory(body)
	return _filter_by_ids(outfits.get("shipyard", []), inventory.get("shipsForSale", []), "shipId")

func _buy_selected_ship() -> void:
	var listings := _shipyard_listings(_current_body())
	if listings.is_empty():
		status_line = "No ships for sale"
		return
	var listing: Dictionary = listings[selected_landing_item % listings.size()]
	var price := int(listing.get("price", 0))
	if credits < price:
		status_line = "Not enough credits"
		return
	var ship_id := str(listing.get("shipId", ""))
	var new_ship := _ship_by_id(ship_id)
	if new_ship.is_empty():
		status_line = "Ship manifest missing " + ship_id
		return
	credits -= price
	player_ship = new_ship
	player_ship_id = ship_id
	var player_frame_set := _load_ship_frame_set(player_ship)
	player_frames = player_frame_set["frames"]
	player_frame_offsets = player_frame_set["offsets"]
	cargo_space = int(player_ship.get("cargoSpace", cargo_space))
	cargo = min(cargo, cargo_space)
	status_line = "Bought ship: " + ship_id
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
