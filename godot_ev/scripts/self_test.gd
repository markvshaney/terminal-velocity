extends SceneTree

const FRAME_COUNT := 36

func _initialize() -> void:
	var root := _repo_root()
	var universe: Dictionary = _json(root + "/native_ev/data/universe.json")
	var ships: Dictionary = _json(root + "/native_ev/data/ships.json")
	var sounds: Dictionary = _json(root + "/native_ev/data/sounds.json")
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
	var loaded_sounds := _verify_sound_assets(root, sounds)
	var loaded_picts := _verify_shipyard_picts(root, ship_defs)
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
	print("GODOT SELFTEST OK systems=%d ships=%d %sFrames=%d soundsLoaded=%d pictsLoaded=%d data=native_ev/data/universe.json" % [systems.size(), ship_defs.size(), player_check_id, frame_ok, loaded_sounds, loaded_picts])
	quit(0)

func _verify_shipyard_picts(root: String, ship_defs: Array) -> int:
	var loaded := 0
	for ship in ship_defs:
		var asset_file := str(ship.get("shipyardPictAssetFile", ""))
		if asset_file == "":
			continue
		var image := Image.new()
		var err := image.load(root + "/native_ev/" + asset_file)
		if err != OK:
			printerr("GODOT SELFTEST FAIL pict missing " + asset_file)
			quit(1)
			return loaded
		if image.get_width() <= 0 or image.get_height() <= 0:
			printerr("GODOT SELFTEST FAIL pict invalid dimensions " + asset_file)
			quit(1)
			return loaded
		loaded += 1
	if loaded <= 0:
		printerr("GODOT SELFTEST FAIL pict no shipyardPictAssetFile loaded")
		quit(1)
	return loaded

func _verify_sound_assets(root: String, sounds: Dictionary) -> int:
	var sounds_by_id := {}
	for sound in sounds.get("sounds", []):
		sounds_by_id[str(sound.get("id", ""))] = sound
	if not sounds_by_id.has("ui_click"):
		printerr("GODOT SELFTEST FAIL sound missing ui_click")
		quit(1)
		return 0
	var loaded := 0
	for sound_id in ["ui_click"]:
		var stream := _load_sound_stream(root, sounds_by_id[sound_id])
		if stream == null:
			printerr("GODOT SELFTEST FAIL sound failed to load " + sound_id)
			quit(1)
			return loaded
		loaded += 1
	return loaded

func _load_sound_stream(root: String, sound: Dictionary) -> AudioStreamWAV:
	var asset_file := str(sound.get("assetFile", ""))
	var file := FileAccess.open(root + "/native_ev/" + asset_file, FileAccess.READ)
	if file == null:
		printerr("GODOT SELFTEST FAIL sound missing " + asset_file)
		return null
	var bytes := file.get_buffer(file.get_length())
	if bytes.size() < 44 or bytes.slice(0, 4).get_string_from_ascii() != "RIFF" or bytes.slice(8, 12).get_string_from_ascii() != "WAVE":
		printerr("GODOT SELFTEST FAIL sound unsupported WAV header " + asset_file)
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
		printerr("GODOT SELFTEST FAIL sound unsupported WAV PCM layout " + asset_file)
		return null
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_8_BITS
	stream.mix_rate = sample_rate
	stream.stereo = false
	stream.data = pcm
	return stream

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
