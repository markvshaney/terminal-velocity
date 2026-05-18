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

var repo_root := ""
var universe := {}
var ships := {}
var missions := {}
var economy := {}
var outfits := {}
var weapons := {}
var sounds := {}
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
var selected_link_index := 0
var selected_target_index := 0
var stars: Array[Vector2] = []
var status_line := ""
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
	_load_data()
	_make_stars()
	set_process(true)
	queue_redraw()

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
	var initial_player_ship_id := "argosy"
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
	var turn_dir := 0
	if Input.is_key_pressed(KEY_A) or Input.is_key_pressed(KEY_LEFT):
		turn_dir -= 1
	if Input.is_key_pressed(KEY_D) or Input.is_key_pressed(KEY_RIGHT):
		turn_dir += 1
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
	if Input.is_key_pressed(KEY_W) or Input.is_key_pressed(KEY_UP):
		vel += nose * 250.0 * delta
	if Input.is_key_pressed(KEY_S) or Input.is_key_pressed(KEY_DOWN):
		vel *= pow(0.90, delta * 60.0)

func _unhandled_input(event: InputEvent) -> void:
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

func _cycle_link(dir: int) -> void:
	var links: Array = current_system.get("links", [])
	if links.is_empty():
		return
	selected_link_index = (selected_link_index + dir + links.size()) % links.size()
	status_line = "Destination: " + str(links[selected_link_index])

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
	draw_string(font, Vector2(18, 24), "TV GODOT RENDER ACTIVE — cell-center build", HORIZONTAL_ALIGNMENT_LEFT, 620, 18, Color(1.0, 0.85, 0.25))
	for star in stars:
		var screen := center + (star - pos * 0.18) * 0.45
		if Rect2(Vector2.ZERO, VIEW_SIZE).has_point(screen):
			draw_circle(screen, 1.0, Color(0.55, 0.62, 0.72))
	_draw_bodies(center)
	_draw_npcs(center)
	_draw_player(center)
	_draw_hud()
	if landed:
		_draw_landing_panel()

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
