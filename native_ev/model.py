from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
SHUTTLE_DIR = ROOT / 'assets' / 'ships' / 'shuttle'
UNIVERSE_PATH = ROOT / 'data' / 'universe.json'
SHIPS_PATH = ROOT / 'data' / 'ships.json'
WEAPONS_PATH = ROOT / 'data' / 'weapons.json'
SOUNDS_PATH = ROOT / 'data' / 'sounds.json'
MISSIONS_PATH = ROOT / 'data' / 'missions.json'
OUTFITS_PATH = ROOT / 'data' / 'outfits.json'
ECONOMY_PATH = ROOT / 'data' / 'economy.json'
GOVERNMENTS_PATH = ROOT / 'data' / 'governments.json'
REPUTATION_PATH = ROOT / 'data' / 'reputation.json'
SOURCED_EV_NAMES_PATH = ROOT / 'data' / 'sourced_ev_names.json'
SOURCED_EV_STRUCTURES_PATH = ROOT / 'data' / 'sourced_ev_structures.json'
SOURCED_EV_GRAPHICS_PATH = ROOT / 'data' / 'sourced_ev_graphics.json'
SOURCED_EV_SOUNDS_PATH = ROOT / 'data' / 'sourced_ev_sounds.json'


def shuttle_frame_paths():
    return [SHUTTLE_DIR / f'frame_{i:02d}.png' for i in range(36)]


def facing_index(degrees):
    return round((degrees % 360) / 10) % 36


def load_universe(path=UNIVERSE_PATH):
    data = json.loads(path.read_text())
    systems = data.get('systems', [])
    if not systems:
        raise ValueError('universe contains no systems')
    names = {system.get('name') for system in systems}
    for system in systems:
        if not system.get('name'):
            raise ValueError('system missing name')
        if not system.get('bodies'):
            raise ValueError(f"system {system.get('name')} has no bodies")
        if 'x' not in system or 'y' not in system:
            raise ValueError(f"system {system.get('name')} missing map coordinates")
        links = system.get('links') or []
        if not links:
            raise ValueError(f"system {system.get('name')} has no hyperspace links")
        missing = [link for link in links if link not in names]
        if missing:
            raise ValueError(f"system {system.get('name')} links to unknown systems: {missing}")
    return data


def ship_manifest(path=SHIPS_PATH):
    data = json.loads(path.read_text())
    ships = data.get('ships', [])
    if not ships:
        raise ValueError('ships manifest contains no ships')
    for ship in ships:
        asset_dir = ROOT / ship['assetDir']
        frames = list(asset_dir.glob('frame_*.png'))
        if len(frames) != ship['frameCount']:
            raise ValueError(f"ship {ship['id']} expected {ship['frameCount']} frames, got {len(frames)}")
        pict_asset = ship.get('shipyardPictAssetFile')
        if pict_asset and not (ROOT / pict_asset).exists():
            raise ValueError(f"ship {ship['id']} missing shipyard PICT {pict_asset}")
    return data


def weapon_manifest(path=WEAPONS_PATH):
    data = json.loads(path.read_text())
    weapons = data.get('weapons', [])
    if not weapons:
        raise ValueError('weapons manifest contains no weapons')
    for weapon in weapons:
        for key in ['id', 'speed', 'lifetime', 'damage', 'cooldownTicks', 'price']:
            if key not in weapon:
                raise ValueError(f'weapon missing {key}')
        if weapon['price'] <= 0:
            raise ValueError(f"weapon {weapon['id']} must have positive price")
    return data


def sound_manifest(path=SOUNDS_PATH):
    data = json.loads(path.read_text())
    if data.get('schemaVersion') != 1:
        raise ValueError('sounds manifest has unexpected schema version')
    if data.get('source') != 'native_ev/data/sourced_ev_sounds.json':
        raise ValueError('sounds manifest has unexpected source')
    if data.get('method') != 'ev-classic-runtime-sound-bindings-v1':
        raise ValueError('sounds manifest has unexpected method')
    sounds = data.get('sounds', [])
    if not sounds:
        raise ValueError('sounds manifest contains no sounds')
    ids = set()
    source_ids = set()
    for sound in sounds:
        for key in ['id', 'name', 'sourceResourceId', 'assetFile', 'sampleRateHz', 'sampleCount', 'channels', 'sampleWidthBytes', 'tags']:
            if key not in sound:
                raise ValueError(f'sound missing {key}')
        if sound['id'] in ids:
            raise ValueError(f"duplicate sound id {sound['id']}")
        ids.add(sound['id'])
        source_ids.add(sound['sourceResourceId'])
        asset_file = ROOT / sound['assetFile']
        if not asset_file.exists():
            raise ValueError(f"sound {sound['id']} missing WAV {asset_file}")
        if sound['channels'] != 1 or sound['sampleWidthBytes'] != 1:
            raise ValueError(f"sound {sound['id']} has unexpected PCM layout")
        if sound['sampleRateHz'] <= 0 or sound['sampleCount'] <= 0:
            raise ValueError(f"sound {sound['id']} has invalid sample metadata")
    bindings = data.get('bindings', {})
    for group_name, group in bindings.items():
        if not isinstance(group, dict):
            raise ValueError(f'sound binding group {group_name} must be a mapping')
        for binding_name, sound_id in group.items():
            if sound_id not in ids:
                raise ValueError(f'sound binding {group_name}.{binding_name} references unknown sound {sound_id}')
    if not {200, 205, 601}.issubset(source_ids):
        raise ValueError('sounds manifest missing representative runtime sounds')
    return data


def station_inventory(universe, system_name, body_name):
    for system in universe.get('systems', []):
        if system.get('name') != system_name:
            continue
        for body in system.get('bodies', []):
            if body.get('name') == body_name:
                inventory = body.get('inventory')
                if inventory is None:
                    return {
                        'services': ['repairs', 'commodities', 'jobs'],
                        'outfitsForSale': [],
                        'shipsForSale': [],
                        'weaponsForSale': [],
                    }
                return {
                    'services': list(inventory.get('services', [])),
                    'outfitsForSale': list(inventory.get('outfitsForSale', [])),
                    'shipsForSale': list(inventory.get('shipsForSale', [])),
                    'weaponsForSale': list(inventory.get('weaponsForSale', [])),
                }
    raise ValueError(f'unknown station {system_name}/{body_name}')


def mission_manifest(path=MISSIONS_PATH):
    data = json.loads(path.read_text())
    missions = data.get('missions', [])
    if not missions:
        raise ValueError('missions manifest contains no missions')
    ids = {mission.get('id') for mission in missions}
    for mission in missions:
        for key in ['id', 'title', 'originSystem', 'originBody', 'destinationSystem', 'destinationBody', 'cargoTons', 'reward']:
            if key not in mission:
                raise ValueError(f'mission missing {key}')
        for list_key in ['requiresFlags', 'excludesFlags', 'setsFlags', 'completionFlags']:
            if list_key not in mission:
                raise ValueError(f"mission {mission['id']} missing {list_key}")
            if not isinstance(mission[list_key], list):
                raise ValueError(f"mission {mission['id']} {list_key} must be a list")
        nxt = mission.get('next')
        if nxt is not None and nxt not in ids:
            raise ValueError(f"mission {mission['id']} points to unknown next mission {nxt}")
        requirements = mission.get('requirements', {})
        for requirement_key in ['reputationMin', 'legalMin', 'legalMax']:
            if requirement_key in requirements and not isinstance(requirements[requirement_key], dict):
                raise ValueError(f"mission {mission['id']} {requirement_key} must be a mapping")
    return data


def sourced_ev_names_manifest(path=SOURCED_EV_NAMES_PATH):
    data = json.loads(path.read_text())
    if data.get('sourceFile') != 'source-assets/ev-classic/Nova Files/EV Data.rez':
        raise ValueError('sourced EV names manifest has unexpected source file')
    if data.get('method') != 'brgr-text-chunk-heuristic-v1':
        raise ValueError('sourced EV names manifest has unexpected extraction method')
    landing_names = data.get('landingNames', [])
    if not landing_names:
        raise ValueError('sourced EV names manifest contains no landing names')
    for entry in landing_names:
        for key in ['name', 'chunkIndex', 'byteOffset', 'evidence', 'confidence']:
            if key not in entry:
                raise ValueError(f'sourced EV landing name missing {key}')
    return data


def sourced_ev_structures_manifest(path=SOURCED_EV_STRUCTURES_PATH):
    data = json.loads(path.read_text())
    if data.get('sourceFile') != 'source-assets/ev-classic/Nova Files/EV Data.rez':
        raise ValueError('sourced EV structures manifest has unexpected source file')
    if data.get('method') != 'brgr-full-field-decode-v2':
        raise ValueError('sourced EV structures manifest has unexpected extraction method')
    if data.get('chunkCount', 0) < 1000:
        raise ValueError('sourced EV structures manifest has too few chunks')
    runs = data.get('runs', [])
    if not runs:
        raise ValueError('sourced EV structures manifest contains no decoded runs')
    by_type = {run.get('candidateType'): run for run in runs}
    for candidate, expected_size, min_count in [
        ('syst-like', 88, 60),
        ('spob-like', 400, 200),
        ('ship-like', 1860, 20),
        ('weapon-like', 282, 30),
        ('outfit-like', 1028, 40),
    ]:
        run = by_type.get(candidate)
        if run is None:
            raise ValueError(f'sourced EV structures missing {candidate} run')
        if run.get('recordSize') != expected_size:
            raise ValueError(f'sourced EV structures {candidate} has unexpected record size')
        if run.get('count', 0) < min_count:
            raise ValueError(f'sourced EV structures {candidate} has too few records')
        records = run.get('records', [])
        if len(records) != run.get('count'):
            raise ValueError(f'sourced EV structures {candidate} count does not match records')
        for record in records[:3]:
            for key in ['ordinal', 'chunkIndex', 'byteOffset', 'size', 'fields', 'fieldEncoding']:
                if key not in record:
                    raise ValueError(f'sourced EV structures {candidate} record missing {key}')
            if not record['fields']:
                raise ValueError(f'sourced EV structures {candidate} record has no decoded fields')
            if record.get('fieldsComplete') is not True:
                raise ValueError(f'sourced EV structures {candidate} record is not fully decoded')
    return data


def sourced_ev_sounds_manifest(path=SOURCED_EV_SOUNDS_PATH):
    data = json.loads(path.read_text())
    if data.get('sourceFile') != 'source-assets/ev-classic/Nova Files/EV Sounds.rez':
        raise ValueError('sourced EV sounds manifest has unexpected source file')
    if data.get('method') != 'classic-mac-snd-wav-v2':
        raise ValueError('sourced EV sounds manifest has unexpected extraction method')
    sounds = data.get('soundAssets', [])
    if len(sounds) != 57:
        raise ValueError('sourced EV sounds manifest has unexpected sound count')
    decoded = [sound for sound in sounds if sound.get('status') == 'ok']
    if len(decoded) != 56:
        raise ValueError('sourced EV sounds manifest has unexpected decoded sound count')
    ids = {sound.get('resourceId') for sound in sounds}
    for expected in [128, 200, 223, 30003]:
        if expected not in ids:
            raise ValueError(f'sourced EV sounds manifest missing resource {expected}')
    for sound in sounds:
        for key in ['type', 'resourceId', 'name', 'chunkIndex', 'byteOffset', 'size', 'status', 'rawHeaderBytes']:
            if key not in sound:
                raise ValueError(f'sourced EV sound resource missing {key}')
        if sound['type'] != 'snd ':
            raise ValueError('sourced EV sounds manifest contains non-snd resource')
        if sound['status'] == 'ok':
            if 'assetFile' not in sound or 'sound' not in sound:
                raise ValueError(f"sourced EV sound resource {sound['resourceId']} missing decoded metadata")
            asset_file = ROOT / sound['assetFile']
            if not asset_file.exists():
                raise ValueError(f"sourced EV sound resource {sound['resourceId']} missing WAV {asset_file}")
        elif not sound['status'].startswith('decode-error:'):
            raise ValueError('sourced EV sound resource should be decoded or explicit decode-error')
        if sound['size'] <= 0 or not sound['rawHeaderBytes']:
            raise ValueError(f"sourced EV sound resource {sound['resourceId']} has invalid byte metadata")
    return data


def sourced_ev_graphics_manifest(path=SOURCED_EV_GRAPHICS_PATH):
    data = json.loads(path.read_text())
    if data.get('sourceFile') != 'source-assets/ev-classic/Nova Files/EV Graphics.rez':
        raise ValueError('sourced EV graphics manifest has unexpected source file')
    if data.get('method') != 'evnew-opcode-rled-shan-pict-cicn-ppat-spin-boom-roid-v7':
        raise ValueError('sourced EV graphics manifest has unexpected extraction method')
    resources = data.get('resources', [])
    if len(resources) < 300:
        raise ValueError('sourced EV graphics manifest has too few resources')
    ship_sprites = data.get('shipSprites', [])
    ok_sprites = [sprite for sprite in ship_sprites if sprite.get('status') == 'ok']
    if len(ok_sprites) < 20:
        raise ValueError('sourced EV graphics manifest has too few extracted ship sprite sets')
    rled_assets = data.get('rledAssets', [])
    ok_rled_assets = [asset for asset in rled_assets if asset.get('status') == 'ok']
    if len(ok_rled_assets) < 70:
        raise ValueError('sourced EV graphics manifest has too few decoded rlëD graphic assets')
    for asset in ok_rled_assets[:5]:
        asset_dir = ROOT / asset['assetDir']
        frames = list(asset_dir.glob('frame_*.png'))
        if len(frames) != asset['frames']:
            raise ValueError(f"sourced EV rlëD asset {asset['resourceId']} expected {asset['frames']} frames, got {len(frames)}")
    for sprite in ok_sprites:
        asset_dir = ROOT / sprite['assetDir']
        frames = list(asset_dir.glob('frame_*.png'))
        if len(frames) != sprite['frames']:
            raise ValueError(f"sourced EV sprite {sprite['shipName']} expected {sprite['frames']} frames, got {len(frames)}")
    cicn_assets = data.get('cicnAssets', [])
    ok_cicn_assets = [asset for asset in cicn_assets if asset.get('status') == 'ok']
    if len(ok_cicn_assets) < 28:
        raise ValueError('sourced EV graphics manifest has too few decoded cicn icon assets')
    for asset in ok_cicn_assets[:5]:
        asset_file = ROOT / asset['assetFile']
        if not asset_file.exists():
            raise ValueError(f"sourced EV cicn asset {asset['resourceId']} missing PNG {asset_file}")
    ppat_assets = data.get('ppatAssets', [])
    ok_ppat_assets = [asset for asset in ppat_assets if asset.get('status') == 'ok']
    if len(ok_ppat_assets) < 9:
        raise ValueError('sourced EV graphics manifest has too few decoded ppat pattern assets')
    for asset in ok_ppat_assets[:5]:
        asset_file = ROOT / asset['assetFile']
        if not asset_file.exists():
            raise ValueError(f"sourced EV ppat asset {asset['resourceId']} missing PNG {asset_file}")
    return data


def _first_embedded_string(record, fallback):
    strings = record.get('embeddedStrings') or []
    if strings:
        return strings[0].get('text') or fallback
    return fallback


def _slugify_identifier(text):
    text = text.lower().replace('ö', 'o').replace('ë', 'e').replace('ï', 'i')
    text = re.sub(r'[^a-z0-9]+', '_', text).strip('_')
    return text or 'unnamed'


def _fields_by_index(record):
    return {field['wordIndex']: field['value'] for field in record.get('fields', [])}


def ship_graphics_crosswalk(structures_path=SOURCED_EV_STRUCTURES_PATH, graphics_path=SOURCED_EV_GRAPHICS_PATH):
    """Return a diagnostic Data.rez ship-record to Graphics.rez shän crosswalk.

    This is intentionally not the final ship manifest generator. It preserves the
    authoritative ship-like Data.rez record identity, then lists every candidate
    field whose value points at a decoded Graphics.rez shän resource. The report
    makes graphics-name mismatches visible instead of silently promoting shän
    names to ship identities.
    """
    structures = sourced_ev_structures_manifest(structures_path)
    graphics = sourced_ev_graphics_manifest(graphics_path)
    ship_run = next(run for run in structures['runs'] if run.get('candidateType') == 'ship-like')
    shan_by_id = {
        resource['resourceId']: resource['shan']
        for resource in graphics['resources']
        if resource.get('type') == 'shän' and 'shan' in resource
    }
    crosswalk = []
    for record in ship_run.get('records', []):
        fields = _fields_by_index(record)
        candidate_refs = []
        for word_index, value in sorted(fields.items()):
            shan = shan_by_id.get(value)
            if shan is None:
                continue
            sem = shan.get('semanticFields', {})
            candidate_refs.append({
                'wordIndex': word_index,
                'shanResourceId': value,
                'shanName': shan.get('name'),
                'inferredRledResourceId': sem.get('inferredRledResourceId'),
                'displayWidth': sem.get('displayWidth'),
                'displayHeight': sem.get('displayHeight'),
                'facings': sem.get('facings'),
            })
        crosswalk.append({
            'dataOrdinal': record['ordinal'],
            'dataChunkIndex': record['chunkIndex'],
            'dataShipName': _first_embedded_string(record, f"ship_{record['ordinal']}"),
            'candidateShanRefs': candidate_refs,
        })
    return crosswalk


def _ship_shan_id_for_data_ordinal(ordinal):
    # EV Classic Data ship records are ordered to Graphics shän resources 128-153;
    # Escape Pod is the only out-of-band ship graphic in this local decode.
    return 895 if ordinal == 26 else 128 + ordinal


def _role_for_ship_name(name):
    lowered = name.lower()
    if 'shuttle' in lowered:
        return 'player'
    if any(token in lowered for token in ['freighter', 'liner', 'transport', 'clipper']):
        return 'npc-trader'
    if any(token in lowered for token in ['alien', 'rebel', 'manta', 'rapier', 'hawk']):
        return 'npc-hostile'
    if any(token in lowered for token in ['frigate', 'cruiser', 'patrol', 'defender', 'corvette', 'gunboat']):
        return 'npc-patrol'
    return 'npc-fast'


def _ship_combat_stats(ship_name, width, height):
    area = int(width or 0) * int(height or 0)
    if 'shuttle' in ship_name.lower():
        return {'cargoSpace': 20, 'hull': 100, 'weaponId': 'laser_cannon'}
    if area >= 5000:
        return {'cargoSpace': 58, 'hull': 370, 'weaponId': 'pulse_cannon'}
    if area >= 4000:
        return {'cargoSpace': 46, 'hull': 293, 'weaponId': 'pulse_cannon'}
    if area >= 2300:
        return {'cargoSpace': 26, 'hull': 165, 'weaponId': 'pulse_cannon'}
    if _role_for_ship_name(ship_name) == 'npc-patrol':
        return {'cargoSpace': 25, 'hull': 180, 'weaponId': 'pulse_cannon'}
    return {'cargoSpace': 11, 'hull': 120 if _role_for_ship_name(ship_name) == 'npc-hostile' else 85, 'weaponId': 'laser_cannon'}


def ev_classic_data_ship_manifest(structures_path=SOURCED_EV_STRUCTURES_PATH, graphics_path=SOURCED_EV_GRAPHICS_PATH):
    """Build runtime ship definitions from Data.rez ship identity joined to Graphics.rez assets."""
    structures = sourced_ev_structures_manifest(structures_path)
    graphics = sourced_ev_graphics_manifest(graphics_path)
    ship_run = next(run for run in structures['runs'] if run.get('candidateType') == 'ship-like')
    sprites_by_shan_id = {
        sprite.get('shipResourceId'): sprite
        for sprite in graphics.get('shipSprites', [])
        if sprite.get('status') == 'ok' and sprite.get('shipResourceId') is not None
    }
    shipyard_picts_by_ordinal = {
        pict.get('resourceId') - 5000: pict
        for pict in graphics.get('pictAssets', [])
        if pict.get('status') == 'ok'
        and isinstance(pict.get('resourceId'), int)
        and 5000 <= pict.get('resourceId') < 6000
        and pict.get('assetFile')
    }
    ships = []
    used_ids = set()
    for record in ship_run.get('records', []):
        name = _first_embedded_string(record, f"ship_{record['ordinal']}")
        shan_id = _ship_shan_id_for_data_ordinal(record['ordinal'])
        sprite = sprites_by_shan_id.get(shan_id)
        if sprite is None:
            continue
        ship_id = _slugify_identifier(name)
        if ship_id in used_ids:
            ship_id = f"{ship_id}_{record['ordinal']}"
        used_ids.add(ship_id)
        stats = _ship_combat_stats(name, sprite['width'], sprite['height'])
        ship = {
            'id': ship_id,
            'name': name,
            'sourceDataOrdinal': record['ordinal'],
            'sourceDataChunkIndex': record['chunkIndex'],
            'shipResourceId': shan_id,
            'graphicsName': sprite['shipName'],
            'resourceId': sprite['rledResourceId'],
            'assetDir': sprite['assetDir'],
            'frameCount': sprite['frames'],
            'width': sprite['width'],
            'height': sprite['height'],
            'role': _role_for_ship_name(name),
            **stats,
        }
        shipyard_pict = shipyard_picts_by_ordinal.get(record['ordinal'])
        if shipyard_pict is not None:
            ship.update({
                'shipyardPictResourceId': shipyard_pict['resourceId'],
                'shipyardPictAssetFile': shipyard_pict['assetFile'],
                'shipyardPictWidth': shipyard_pict['width'],
                'shipyardPictHeight': shipyard_pict['height'],
            })
        ships.append(ship)
    return {'ships': ships}


def _mission_ids(collection):
    return {item['id'] if isinstance(item, dict) else item for item in collection}


def _has_flags(required, flags):
    return all(flag in flags for flag in required)


def _has_excluded_flag(excluded, flags):
    return any(flag in flags for flag in excluded)


def _meets_score_requirements(requirements, scores, default=0):
    for key, minimum in (requirements or {}).items():
        if int((scores or {}).get(key, default)) < int(minimum):
            return False
    return True


def _meets_score_maximums(requirements, scores, default=0):
    for key, maximum in (requirements or {}).items():
        if int((scores or {}).get(key, default)) > int(maximum):
            return False
    return True


def mission_requirements_met(mission, reputation=None, legal_records=None):
    requirements = mission.get('requirements') or {}
    return (
        _meets_score_requirements(requirements.get('reputationMin', {}), reputation)
        and _meets_score_requirements(requirements.get('legalMin', {}), legal_records)
        and _meets_score_maximums(requirements.get('legalMax', {}), legal_records)
    )


def branch_choice_groups(data):
    groups = {}
    for mission in data.get('missions', []):
        group = mission.get('choiceGroup')
        if not group:
            continue
        groups.setdefault(group, []).append(mission['id'])
    return groups


def available_mission_ids(data, system, body, completed_ids=None, active_ids=None, flags=None, reputation=None, legal_records=None):
    completed_ids = set(completed_ids or set())
    active_ids = set(active_ids or set())
    flags = set(flags or set())
    available = []
    for mission in data.get('missions', []):
        mid = mission['id']
        if mid in completed_ids or mid in active_ids:
            continue
        if mission['originSystem'] != system or mission['originBody'] != body:
            continue
        if not _has_flags(mission.get('requiresFlags', []), flags):
            continue
        if _has_excluded_flag(mission.get('excludesFlags', []), flags):
            continue
        if not mission_requirements_met(mission, reputation, legal_records):
            continue
        available.append(mid)
    return available


def mission_unlock_flags(data, mission_id, flags=None, accepted=False):
    flags = set(flags or set())
    mission = next((m for m in data.get('missions', []) if m.get('id') == mission_id), None)
    if mission is None:
        raise ValueError(f'unknown mission {mission_id}')
    for flag in mission.get('completionFlags', []):
        flags.add(flag)
    if accepted:
        for flag in mission.get('setsFlags', []):
            flags.add(flag)
    return flags


def mission_accept_flags(data, mission_id, flags=None):
    flags = set(flags or set())
    mission = next((m for m in data.get('missions', []) if m.get('id') == mission_id), None)
    if mission is None:
        raise ValueError(f'unknown mission {mission_id}')
    for flag in mission.get('setsFlags', []):
        flags.add(flag)
    return flags


def outfit_manifest(path=OUTFITS_PATH):
    data = json.loads(path.read_text())
    outfits = data.get('outfits', [])
    shipyard = data.get('shipyard', [])
    if not outfits:
        raise ValueError('outfit manifest contains no outfits')
    if not shipyard:
        raise ValueError('outfit manifest contains no shipyard entries')
    for outfit in outfits:
        for key in ['id', 'name', 'price', 'effects']:
            if key not in outfit:
                raise ValueError(f'outfit missing {key}')
        if outfit['price'] <= 0:
            raise ValueError(f"outfit {outfit['id']} must have positive price")
    for listing in shipyard:
        for key in ['shipId', 'price']:
            if key not in listing:
                raise ValueError(f'shipyard listing missing {key}')
        if listing['price'] <= 0:
            raise ValueError(f"shipyard listing {listing['shipId']} must have positive price")
    return data


def repair_cost(current_hull, max_hull, per_point):
    missing = max(0, max_hull - current_hull)
    return int(missing * per_point)


def can_buy(credits, price):
    return credits >= price


def economy_manifest(path=ECONOMY_PATH):
    data = json.loads(path.read_text())
    commodities = data.get('commodities', [])
    markets = data.get('markets', {})
    if not commodities:
        raise ValueError('economy manifest contains no commodities')
    if not markets:
        raise ValueError('economy manifest contains no markets')
    commodity_ids = {commodity.get('id') for commodity in commodities}
    for commodity in commodities:
        for key in ['id', 'name']:
            if key not in commodity:
                raise ValueError(f'commodity missing {key}')
    for system, market in markets.items():
        for cid, prices in market.items():
            if cid not in commodity_ids:
                raise ValueError(f'market {system} references unknown commodity {cid}')
            for key in ['buy', 'sell']:
                if key not in prices:
                    raise ValueError(f'market {system}/{cid} missing {key}')
                if prices[key] <= 0:
                    raise ValueError(f'market {system}/{cid} {key} must be positive')
    return data


def trade_profit(buy_price, sell_price, quantity):
    return int((sell_price - buy_price) * quantity)


def _system_by_name(universe, name):
    for system in universe.get('systems', []):
        if system.get('name') == name:
            return system
    raise ValueError(f'unknown system {name}')


def system_distance(universe, origin, destination):
    start = _system_by_name(universe, origin)
    end = _system_by_name(universe, destination)
    dx = float(end['x']) - float(start['x'])
    dy = float(end['y']) - float(start['y'])
    return int(round((dx * dx + dy * dy) ** 0.5))


def route_risk_score(governments, ships, destination):
    mapping = governments.get('systems', {}).get(destination, {})
    gov_name = mapping.get('government')
    gov = governments.get('governments', {}).get(gov_name, {})
    risk = 1
    if gov.get('scanRange', 0) < 250:
        risk += 1
    if gov.get('finePerTon', 0) >= 250:
        risk += 1
    for traffic in ships.get('traffic', []):
        if traffic.get('system') == destination and traffic.get('disposition') == 'hostile':
            risk += 2
    return risk


def cargo_job_pay(tons, distance, risk_score, base=350):
    return int(base + (int(tons) * 120) + (int(distance) * 2) + (int(risk_score) * 250))


def government_manifest(path=GOVERNMENTS_PATH):
    data = json.loads(path.read_text())
    governments = data.get('governments', {})
    systems = data.get('systems', {})
    contraband = data.get('contraband', {})
    if not governments:
        raise ValueError('government manifest contains no governments')
    if not systems:
        raise ValueError('government manifest contains no system mappings')
    for name, government in governments.items():
        for key in ['scanRange', 'finePerTon', 'patrolFaction', 'bribeAllowed', 'bribePerTon']:
            if key not in government:
                raise ValueError(f'government {name} missing {key}')
        if government['finePerTon'] <= 0:
            raise ValueError(f"government {name} finePerTon must be positive")
        if government['bribePerTon'] < 0:
            raise ValueError(f"government {name} bribePerTon cannot be negative")
    for system, mapping in systems.items():
        gov = mapping.get('government')
        if gov not in governments:
            raise ValueError(f'system {system} references unknown government {gov}')
    for gov in contraband.keys():
        if gov not in governments:
            raise ValueError(f'contraband references unknown government {gov}')
    return data


def fine_for_contraband(hold, illegal_ids, fine_per_ton):
    tons = 0
    for cid in illegal_ids:
        tons += int(hold.get(cid, 0))
    return int(tons * fine_per_ton)


def _illegal_hold(hold, illegal_ids):
    return {cid: int((hold or {}).get(cid, 0)) for cid in illegal_ids if int((hold or {}).get(cid, 0)) > 0}


def government_patrol_posture(reputation_data, legal_records, government):
    mechanics = reputation_data.get('mechanics', {})
    score = int((legal_records or {}).get(government, 0))
    if score <= int(mechanics.get('patrolHostileLegalScore', -60)):
        return 'hostile'
    if score <= int(mechanics.get('patrolWarningLegalScore', -20)):
        return 'warning'
    return 'normal'


def enforcement_outcome(governments, reputation_data, *, government, hold, credits, legal_records=None, accept_bribe=False):
    gov = governments.get('governments', {}).get(government)
    if gov is None:
        raise ValueError(f'unknown government {government}')
    illegal_ids = set(governments.get('contraband', {}).get(government, []))
    illegal_hold = _illegal_hold(hold, illegal_ids)
    tons = sum(illegal_hold.values())
    if tons <= 0:
        return {
            'action': 'none',
            'creditsDelta': 0,
            'legalDelta': 0,
            'confiscated': {},
            'posture': government_patrol_posture(reputation_data, legal_records, government),
        }
    if accept_bribe and bool(gov.get('bribeAllowed', False)):
        bribe = int(tons * int(gov.get('bribePerTon', 0)))
        if bribe > 0 and int(credits) >= bribe:
            return {
                'action': 'bribe',
                'creditsDelta': -bribe,
                'legalDelta': 0,
                'confiscated': {cid: 0 for cid in illegal_hold},
                'posture': government_patrol_posture(reputation_data, legal_records, government),
            }
    fine = fine_for_contraband(hold, illegal_ids, int(gov.get('finePerTon', 0)))
    if int(credits) >= fine:
        event = reputation_data.get('events', {}).get('contraband_fine', {})
        legal_delta = int(event.get('legal', {}).get('*', 0))
        return {
            'action': 'fine',
            'creditsDelta': -fine,
            'legalDelta': legal_delta,
            'confiscated': illegal_hold,
            'posture': government_patrol_posture(reputation_data, legal_records, government),
        }
    penalty = int(reputation_data.get('mechanics', {}).get('unpaidFineLegalPenalty', -25))
    return {
        'action': 'confiscate',
        'creditsDelta': 0,
        'legalDelta': penalty,
        'confiscated': illegal_hold,
        'posture': government_patrol_posture(reputation_data, legal_records, government),
    }


def clemency_offer(reputation_data, *, reputation_scores, legal_records, government):
    mechanics = reputation_data.get('mechanics', {})
    rep = int((reputation_scores or {}).get(government, 0))
    legal = int((legal_records or {}).get(government, 0))
    min_rep = int(mechanics.get('clemencyMinReputation', 10))
    max_legal = int(mechanics.get('clemencyMaxLegalScore', -20))
    available = rep >= min_rep and legal <= max_legal
    return {
        'available': available,
        'cost': int(mechanics.get('clemencyCost', 1000)) if available else 0,
        'legalDelta': int(mechanics.get('clemencyLegalDelta', 25)) if available else 0,
    }


def patrol_spawn_specs(governments, ships, universe):
    """Return deterministic patrol spawns for every mapped system.

    This keeps patrol visibility data-backed: governments select factions,
    systems select governments, and the ship manifest supplies patrol hulls.
    """
    ship_defs = {ship['id']: ship for ship in ships.get('ships', [])}
    traffic = ships.get('traffic', [])
    patrol_role_ids = [ship['id'] for ship in ships.get('ships', []) if 'patrol' in str(ship.get('role', '')).lower()]
    if not patrol_role_ids:
        raise ValueError('ships manifest contains no patrol-capable ships')
    specs = []
    system_defs = {system['name']: system for system in universe.get('systems', [])}
    for system_name, mapping in sorted(governments.get('systems', {}).items()):
        if system_name not in system_defs:
            raise ValueError(f'government mapping references unknown system {system_name}')
        government_name = mapping.get('government')
        government = governments.get('governments', {}).get(government_name)
        if government is None:
            raise ValueError(f'system {system_name} references unknown government {government_name}')
        faction = government['patrolFaction']
        candidates = [entry['shipId'] for entry in traffic if entry.get('faction') == faction and entry.get('shipId') in ship_defs]
        if not candidates:
            candidates = patrol_role_ids
        system = system_defs[system_name]
        seed = sum(ord(ch) for ch in system_name)
        specs.append({
            'system': system_name,
            'government': government_name,
            'faction': faction,
            'shipId': candidates[seed % len(candidates)],
            'name': f'{government_name} Patrol',
            'x': int((seed % 900) - 450),
            'y': int(((seed * 7) % 700) - 350),
            'heading': int(seed % 360),
            'speed': 0.55 + ((seed % 5) * 0.08),
            'scanRange': int(government['scanRange']),
            'disposition': 'friendly',
        })
    return specs


def fugitive_docking_consequence(reputation_data, legal_records, government):
    posture = government_patrol_posture(reputation_data, legal_records, government)
    legal = int((legal_records or {}).get(government, 0))
    if posture == 'hostile':
        return {
            'action': 'deny_and_attack',
            'patrolsHostile': True,
            'legal': legal,
            'posture': posture,
            'message': f'{government} patrols are hostile: docking denied and patrols will attack.',
        }
    if posture == 'warning':
        return {
            'action': 'deny',
            'patrolsHostile': False,
            'legal': legal,
            'posture': posture,
            'message': f'{government} port authority denies docking until your legal record improves.',
        }
    return {
        'action': 'allow',
        'patrolsHostile': False,
        'legal': legal,
        'posture': posture,
        'message': f'{government} port authority clears you to land.',
    }


def reputation_manifest(path=REPUTATION_PATH):
    data = json.loads(path.read_text())
    factions = data.get('factions', {})
    events = data.get('events', {})
    thresholds = data.get('legalThresholds', [])
    if not factions:
        raise ValueError('reputation manifest contains no factions')
    if not events:
        raise ValueError('reputation manifest contains no events')
    if not thresholds:
        raise ValueError('reputation manifest contains no legal thresholds')
    for event_name, event in events.items():
        for faction in event.get('reputation', {}).keys():
            if faction not in factions:
                raise ValueError(f'reputation event {event_name} references unknown faction {faction}')
        for government in event.get('legal', {}).keys():
            if government != '*' and government not in factions:
                raise ValueError(f'reputation event {event_name} references unknown legal record {government}')
    for raw_faction, faction in data.get('npcFactionMap', {}).items():
        if faction not in factions:
            raise ValueError(f'npc faction map {raw_faction} references unknown faction {faction}')
    return data


def legal_status_for_score(data, score):
    ordered = sorted(data.get('legalThresholds', []), key=lambda item: int(item['minScore']), reverse=True)
    score = int(score)
    for threshold in ordered:
        if score >= int(threshold['minScore']):
            return threshold['status']
    return ordered[-1]['status'] if ordered else 'Clean'


def apply_reputation_event(data, reputation, legal_records, event_id, government=None):
    if event_id not in data.get('events', {}):
        raise ValueError(f'unknown reputation event {event_id}')
    event = data['events'][event_id]
    reputation = dict(reputation or {})
    legal_records = dict(legal_records or {})
    for faction, delta in event.get('reputation', {}).items():
        reputation[faction] = int(reputation.get(faction, 0)) + int(delta)
    for gov, delta in event.get('legal', {}).items():
        target = government if gov == '*' else gov
        if target is None:
            continue
        legal_records[target] = int(legal_records.get(target, 0)) + int(delta)
    return reputation, legal_records


def _mapped_npc_faction(data, npc_faction):
    return data.get('npcFactionMap', {}).get(npc_faction, npc_faction)


def can_dock_with_government(data, legal_records, government):
    mechanics = data.get('mechanics', {})
    min_by_gov = mechanics.get('dockMinLegalScoreByGovernment', {})
    minimum = int(min_by_gov.get(government, mechanics.get('defaultDockMinLegalScore', -60)))
    return int((legal_records or {}).get(government, 0)) >= minimum


def _score_map_requirement_met(requirements, scores, government=None):
    for key, minimum in (requirements or {}).items():
        target_key = government if key == '*' else key
        if target_key is None:
            continue
        if int((scores or {}).get(target_key, 0)) < int(minimum):
            return False
    return True


def _service_requirement_met(requirement, reputation, legal_records, government):
    if not _score_map_requirement_met((requirement or {}).get('legalMin', {}), legal_records, government):
        return False
    if not _score_map_requirement_met((requirement or {}).get('reputationMin', {}), reputation, government):
        return False
    by_government = (requirement or {}).get('reputationMinByGovernment', {})
    if government in by_government:
        return _score_map_requirement_met(by_government[government], reputation, government)
    return True


def available_station_services(inventory, reputation_data, reputation=None, legal_records=None, government=None):
    services = list((inventory or {}).get('services', []))
    service_requirements = reputation_data.get('mechanics', {}).get('serviceRequirements', {})
    return [
        service
        for service in services
        if _service_requirement_met(service_requirements.get(service, {}), reputation, legal_records, government)
    ]


def effective_npc_disposition(data, base_disposition, npc_faction, reputation, legal_records, government):
    mechanics = data.get('mechanics', {})
    mapped = _mapped_npc_faction(data, npc_faction)
    rep = int((reputation or {}).get(mapped, 0))
    legal_score = int((legal_records or {}).get(government, 0))
    if npc_faction == 'pirate':
        if rep >= int(mechanics.get('pirateFriendlyReputation', 5)):
            return 'neutral'
        if rep <= int(mechanics.get('pirateHostileReputation', -5)):
            return 'hostile'
    patrol_score = int(mechanics.get('patrolHostileLegalScore', -60))
    if npc_faction in {'confed', 'independent'} and legal_score <= patrol_score:
        return 'hostile'
    return base_disposition


def cargo_can_accept(current, add, capacity=20):
    return current + add <= capacity


def serialize_save_data(
    *,
    credits,
    current_system,
    selected_system,
    player_ship_id,
    player_hull,
    player_fuel,
    cargo_used,
    cargo_space,
    owned_outfits=None,
    commodity_hold=None,
    active_mission_ids=None,
    completed_mission_ids=None,
    story_flags=None,
    legal_status='Clean',
    reputation=None,
    legal_records=None,
):
    return {
        'schemaVersion': 1,
        'credits': int(credits),
        'currentSystem': current_system,
        'selectedSystem': selected_system,
        'playerShipId': player_ship_id,
        'playerHull': float(player_hull),
        'playerFuel': float(player_fuel),
        'cargoUsed': int(cargo_used),
        'cargoSpace': int(cargo_space),
        'ownedOutfits': dict(owned_outfits or {}),
        'commodityHold': dict(commodity_hold or {}),
        'activeMissionIds': list(active_mission_ids or []),
        'completedMissionIds': list(completed_mission_ids or []),
        'storyFlags': sorted(set(story_flags or [])),
        'legalStatus': legal_status,
        'reputation': dict(reputation or {}),
        'legalRecords': dict(legal_records or {}),
    }


def normalize_save_data(data):
    current_system = data.get('currentSystem', 'Sol')
    return {
        'schemaVersion': int(data.get('schemaVersion', 1)),
        'credits': int(data.get('credits', 5000)),
        'currentSystem': current_system,
        'selectedSystem': data.get('selectedSystem', current_system),
        'playerShipId': data.get('playerShipId', 'shuttlecraft'),
        'playerHull': float(data.get('playerHull', 100.0)),
        'playerFuel': float(data.get('playerFuel', 100.0)),
        'cargoUsed': int(data.get('cargoUsed', 0)),
        'cargoSpace': int(data.get('cargoSpace', 20)),
        'ownedOutfits': dict(data.get('ownedOutfits', {})),
        'commodityHold': dict(data.get('commodityHold', {})),
        'activeMissionIds': list(data.get('activeMissionIds', [])),
        'completedMissionIds': list(data.get('completedMissionIds', [])),
        'storyFlags': sorted(set(data.get('storyFlags', []))),
        'legalStatus': data.get('legalStatus', 'Clean'),
        'reputation': dict(data.get('reputation', {})),
        'legalRecords': dict(data.get('legalRecords', {})),
    }
