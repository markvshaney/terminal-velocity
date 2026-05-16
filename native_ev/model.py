from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
SHUTTLE_DIR = ROOT / 'assets' / 'ships' / 'shuttle'
UNIVERSE_PATH = ROOT / 'data' / 'universe.json'
SHIPS_PATH = ROOT / 'data' / 'ships.json'
WEAPONS_PATH = ROOT / 'data' / 'weapons.json'
MISSIONS_PATH = ROOT / 'data' / 'missions.json'
OUTFITS_PATH = ROOT / 'data' / 'outfits.json'
ECONOMY_PATH = ROOT / 'data' / 'economy.json'
GOVERNMENTS_PATH = ROOT / 'data' / 'governments.json'
SOURCED_EV_NAMES_PATH = ROOT / 'data' / 'sourced_ev_names.json'
SOURCED_EV_STRUCTURES_PATH = ROOT / 'data' / 'sourced_ev_structures.json'
SOURCED_EV_GRAPHICS_PATH = ROOT / 'data' / 'sourced_ev_graphics.json'


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


def sourced_ev_graphics_manifest(path=SOURCED_EV_GRAPHICS_PATH):
    data = json.loads(path.read_text())
    if data.get('sourceFile') != 'source-assets/ev-classic/Nova Files/EV Graphics.rez':
        raise ValueError('sourced EV graphics manifest has unexpected source file')
    if data.get('method') != 'brgr-graphics-rled-shan-full-field-v1':
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
    return data


def _mission_ids(collection):
    return {item['id'] if isinstance(item, dict) else item for item in collection}


def _has_flags(required, flags):
    return all(flag in flags for flag in required)


def _has_excluded_flag(excluded, flags):
    return any(flag in flags for flag in excluded)


def branch_choice_groups(data):
    groups = {}
    for mission in data.get('missions', []):
        group = mission.get('choiceGroup')
        if not group:
            continue
        groups.setdefault(group, []).append(mission['id'])
    return groups


def available_mission_ids(data, system, body, completed_ids=None, active_ids=None, flags=None):
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
        for key in ['scanRange', 'finePerTon', 'patrolFaction']:
            if key not in government:
                raise ValueError(f'government {name} missing {key}')
        if government['finePerTon'] <= 0:
            raise ValueError(f'government {name} finePerTon must be positive')
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
    }


def normalize_save_data(data):
    current_system = data.get('currentSystem', 'Sol')
    return {
        'schemaVersion': int(data.get('schemaVersion', 1)),
        'credits': int(data.get('credits', 5000)),
        'currentSystem': current_system,
        'selectedSystem': data.get('selectedSystem', current_system),
        'playerShipId': data.get('playerShipId', 'shuttle'),
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
    }
