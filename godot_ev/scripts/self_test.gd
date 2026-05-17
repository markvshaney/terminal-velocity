extends SceneTree

const FRAME_COUNT := 36

func _initialize() -> void:
	var root := _repo_root()
	var universe: Dictionary = _json(root + "/native_ev/data/universe.json")
	var ships: Dictionary = _json(root + "/native_ev/data/ships.json")
	var systems: Array = universe.get("systems", [])
	var ship_defs: Array = ships.get("ships", [])
	if systems.is_empty():
		printerr("GODOT SELFTEST FAIL no systems")
		quit(1)
		return
	if ship_defs.is_empty():
		printerr("GODOT SELFTEST FAIL no ships")
		quit(1)
		return
	var player_check_id := "argosy"
	var player_ship := {}
	for ship in ship_defs:
		if ship.get("id", "") == player_check_id:
			player_ship = ship
			break
	if player_ship.is_empty():
		printerr("GODOT SELFTEST FAIL no " + player_check_id)
		quit(1)
		return
	var asset_dir: String = root + "/native_ev/" + str(player_ship.get("assetDir", ""))
	var frame_ok := 0
	for i in range(FRAME_COUNT):
		var frame_path: String = asset_dir + "/frame_%02d.png" % i
		if FileAccess.file_exists(frame_path):
			frame_ok += 1
	if frame_ok != FRAME_COUNT:
		printerr("GODOT SELFTEST FAIL %s frames=%d" % [player_check_id, frame_ok])
		quit(1)
		return
	print("GODOT SELFTEST OK systems=%d ships=%d %sFrames=%d data=native_ev/data/universe.json" % [systems.size(), ship_defs.size(), player_check_id, frame_ok])
	quit(0)

func _repo_root() -> String:
	var base := ProjectSettings.globalize_path("res://").trim_suffix("/")
	return base.get_base_dir()

func _json(path: String) -> Variant:
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		printerr("GODOT SELFTEST FAIL missing " + path)
		quit(1)
		return {}
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed == null:
		printerr("GODOT SELFTEST FAIL invalid JSON " + path)
		quit(1)
		return {}
	return parsed
