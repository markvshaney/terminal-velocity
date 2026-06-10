from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
PROFILES_ROOT = ROOT / 'data' / 'profiles'
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
SOURCED_EV_GOVERNMENTS_PATH = ROOT / 'data' / 'sourced_ev_governments.json'
SOURCED_EV_JUNK_PATH = ROOT / 'data' / 'sourced_ev_junk.json'
SOURCED_EV_MISSIONS_PATH = ROOT / 'data' / 'sourced_ev_missions.json'
SOURCED_EV_SYSTEMS_PATH = ROOT / 'data' / 'sourced_ev_systems.json'
SOURCED_EV_SERVICES_PATH = ROOT / 'data' / 'sourced_ev_services.json'
SOURCED_EV_GRAPHICS_PATH = ROOT / 'data' / 'sourced_ev_graphics.json'
SOURCED_EV_SOUNDS_PATH = ROOT / 'data' / 'sourced_ev_sounds.json'
SOURCED_EV_WEAPONS_PATH = ROOT / 'data' / 'sourced_ev_weapons.json'


def profile_manifest(profile_id='classic', profiles_root=PROFILES_ROOT):
    """Return a validated runtime profile descriptor.

    Profiles are a small routing layer: they name the source/fidelity target and
    the manifest paths consumed by Python/Godot without changing the current
    single-Classic data contract yet.
    """
    if not re.fullmatch(r'[a-z0-9_-]+', profile_id):
        raise ValueError(f'invalid profile id {profile_id!r}')
    path = profiles_root / f'{profile_id}.json'
    data = json.loads(path.read_text())
    if data.get('id') != profile_id:
        raise ValueError(f'profile {profile_id} id mismatch')
    if data.get('sourceLabel') != 'ev-classic-profile-descriptor-scaffold':
        raise ValueError(f'profile {profile_id} has unexpected source label')
    manifests = data.get('dataManifests', {})
    for key in ['universe', 'ships', 'missions', 'economy', 'sounds', 'weapons', 'outfits', 'governments', 'reputation', 'gameplayCurriculum', 'helpOverlay']:
        rel = manifests.get(key)
        if not rel:
            raise ValueError(f'profile {profile_id} missing data manifest {key}')
        if not (ROOT.parent / rel).exists():
            raise ValueError(f'profile {profile_id} data manifest {key} missing at {rel}')
    sources = data.get('sourceManifests', {})
    for key in ['sourcedEvStructures', 'sourcedEvMissions', 'sourcedEvSystems', 'sourcedEvServices', 'sourcedEvGovernments', 'sourcedEvJunk', 'sourcedEvGraphics', 'sourcedEvSounds', 'sourcedEvWeapons']:
        rel = sources.get(key)
        if not rel:
            raise ValueError(f'profile {profile_id} missing source manifest {key}')
        if not (ROOT.parent / rel).exists():
            raise ValueError(f'profile {profile_id} source manifest {key} missing at {rel}')
    return data


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


def sourced_ev_systems_manifest(path=SOURCED_EV_SYSTEMS_PATH):
    data = json.loads(path.read_text())
    if data.get('schemaVersion') != 1:
        raise ValueError('sourced EV systems manifest has unexpected schema version')
    if data.get('method') != 'ev-classic-static-system-id-name-seed-resource-bible-topology-constants-coordinate-map-source-readiness-record-name-promotion-readiness-landing-proximity-syst-word-domain-coverage-syst-field-order-conflict-syst-field-layout-source-readiness-coordinate-link-slot-coordinate-display-scale-interpretation-coordinate-display-quantization-coordinate-display-residual-magnitude-coordinate-display-residual-sign-coordinate-display-integer-band-coordinate-display-fixed-point-start-neighborhood-slot-angular-order-start-neighborhood-slot-vector-order-start-neighborhood-display-vector-start-neighborhood-display-distance-start-neighborhood-display-transform-coordinate-display-transform-normalized-extrema-link-graph-distance-name-seed-summary-levo-name-map-v34':
        raise ValueError('sourced EV systems manifest has unexpected extraction method')
    if data.get('sourceBasis') != 'EV Classic Resource Bible game constants, syst xPos/yPos and Con1-Con16 field-family definitions plus local primitive BRGR syst-like structure decode, heuristic EV Data.rez system/landing-name seed list, Resource Bible system ID #128 start-system rule, and original-runtime-observed starting system Levo':
        raise ValueError('sourced EV systems manifest has unexpected source basis')
    run = data.get('recordRun', {})
    if run.get('candidateType') != 'syst-like' or run.get('recordSize') != 88 or run.get('count') != 67:
        raise ValueError('sourced EV systems manifest has unexpected record run')
    systems = data.get('systems', [])
    if len(systems) != 67:
        raise ValueError('sourced EV systems manifest has unexpected system count')
    ids = [system.get('resourceId') for system in systems]
    if ids != list(range(128, 195)):
        raise ValueError('sourced EV systems manifest resource ids are not contiguous Classic system ids')
    for system in systems:
        for key in ['resourceId', 'ordinal', 'chunkIndex', 'byteOffset', 'size', 'semanticStatus', 'semanticFields', 'sourceRecord']:
            if key not in system:
                raise ValueError(f'sourced EV system missing {key}')
        allowed_system_statuses = {
            'ids_promoted_exact_name_coordinate_words_links_candidate_fields_pending',
            'ids_promoted_names_seeded_coordinate_words_links_candidate_fields_pending',
        }
        if system['semanticStatus'] not in allowed_system_statuses:
            raise ValueError(f"sourced EV system {system['resourceId']} has unexpected semantic status")
        coordinates = system['semanticFields'].get('mapCoordinates', {})
        if coordinates.get('wordIndices') != [0, 1, 2, 3]:
            raise ValueError(f"sourced EV system {system['resourceId']} has unexpected coordinate word indices")
        for axis in ['xPos', 'yPos']:
            axis_data = coordinates.get(axis, {})
            if len(axis_data.get('rawWords', [])) != 2:
                raise ValueError(f"sourced EV system {system['resourceId']} has incomplete {axis} raw words")
            if 'signedLongCandidate' not in axis_data or 'rawHex32' not in axis_data:
                raise ValueError(f"sourced EV system {system['resourceId']} missing {axis} raw signed-long coordinate candidate")
        links = system['semanticFields'].get('candidateHyperspaceLinks', {})
        if links.get('wordIndices') != list(range(4, 20)):
            raise ValueError(f"sourced EV system {system['resourceId']} has unexpected link candidate indices")
        if links.get('slotNames') != [f'Con{index}' for index in range(1, 17)]:
            raise ValueError(f"sourced EV system {system['resourceId']} has unexpected link slot names")
        link_slots = links.get('linkSlots', [])
        if len(link_slots) != 16:
            raise ValueError(f"sourced EV system {system['resourceId']} has unexpected link slot count")
        for slot_number, slot in enumerate(link_slots, start=1):
            if slot.get('slotNumber') != slot_number or slot.get('slotName') != f'Con{slot_number}' or slot.get('wordIndex') != slot_number + 3:
                raise ValueError(f"sourced EV system {system['resourceId']} has malformed link slot metadata")
            if slot.get('status') == 'linked-system' and slot.get('targetResourceId') != slot.get('rawValue'):
                raise ValueError(f"sourced EV system {system['resourceId']} has malformed link target metadata")
            if slot.get('status') == 'no-link' and slot.get('rawValue') != -1:
                raise ValueError(f"sourced EV system {system['resourceId']} has malformed no-link slot")
        for link_id in links.get('linkedSystemResourceIds', []):
            if link_id < 128 or link_id > 1127:
                raise ValueError(f"sourced EV system {system['resourceId']} has out-of-range link candidate")
    seeds = data.get('systemNameSeeds', [])
    if len(seeds) < 9 or 'Sol' not in {seed.get('name') for seed in seeds}:
        raise ValueError('sourced EV systems manifest missing expected heuristic name seeds')
    topology_constants = data.get('resourceBibleTopologyConstantsSummary', {})
    if topology_constants.get('sourceLabel') != 'resource-bible-backed-topology-constants':
        raise ValueError('sourced EV systems manifest missing Resource Bible topology constants source label')
    if topology_constants.get('maxStellarObjects') != 1500 or topology_constants.get('maxSystems') != 1000:
        raise ValueError('sourced EV systems manifest has unexpected Resource Bible topology capacities')
    if topology_constants.get('jumpDistancePixels') != 1000:
        raise ValueError('sourced EV systems manifest has unexpected Resource Bible JumpDistance constant')
    if topology_constants.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest must not promote coordinate display units from JumpDistance alone')
    if 'not a decoded syst coordinate unit interpretation' not in ' '.join(topology_constants.get('promotionBlockers', [])):
        raise ValueError('sourced EV systems manifest topology constants must preserve display-unit blocker')
    coordinate_map_source = data.get('coordinateMapSourceReadinessSummary', {})
    if coordinate_map_source.get('sourceLabel') != 'resource-bible-backed-coordinate-map-source-readiness':
        raise ValueError('sourced EV systems manifest missing coordinate map source-readiness label')
    if coordinate_map_source.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate map source-readiness must keep display scaling pending')
    if coordinate_map_source.get('recordCount') != 67 or coordinate_map_source.get('coordinateFieldCompleteRecordCount') != 67 or coordinate_map_source.get('linkSlotCompleteRecordCount') != 67:
        raise ValueError('sourced EV systems manifest coordinate map source-readiness has unexpected coverage counts')
    if 'The sÿst resource xPos/yPos fields are the system X and Y positions on the map.' != coordinate_map_source.get('resourceBibleMapPlacementClaim'):
        raise ValueError('sourced EV systems manifest coordinate map source-readiness changed Resource Bible map-placement claim')
    if 'JumpDistance=1000 pixels is preserved as a game/topology range constant, not as decoded xPos/yPos map-pixel proof.' != coordinate_map_source.get('resourceBibleRangeConstantBoundary'):
        raise ValueError('sourced EV systems manifest coordinate map source-readiness must preserve JumpDistance boundary')
    if 'JumpDistance pixels do not by themselves calibrate the decoded syst xPos/yPos coordinate units' not in coordinate_map_source.get('promotionBlockers', []):
        raise ValueError('sourced EV systems manifest coordinate map source-readiness missing JumpDistance display-unit blocker')
    if 'not-promoted' not in coordinate_map_source.get('displayUnitInterpretationStatus', ''):
        raise ValueError('sourced EV systems manifest coordinate map source-readiness must not promote display units')
    syst_field_layout = data.get('systFieldLayoutSourceReadinessSummary', {})
    syst_field_order_conflict = data.get('systFieldOrderConflictSummary', {})
    if syst_field_layout.get('sourceLabel') != 'resource-bible-backed-syst-field-layout-source-readiness':
        raise ValueError('sourced EV systems manifest missing syst field-layout source-readiness label')
    if syst_field_layout.get('oracleStatus') != 'non_topology_syst_field_semantics_pending_runtime_integration':
        raise ValueError('sourced EV systems manifest syst field-layout summary should keep non-topology semantics pending')
    if syst_field_layout.get('recordCount') != 67 or syst_field_layout.get('recordSize') != 88 or syst_field_layout.get('fieldCompleteRecordCount') != 67:
        raise ValueError('sourced EV systems manifest syst field-layout summary has unexpected record coverage')
    if syst_field_layout.get('sourceReferences', {}).get('systResourceDefinition') != 'docs/references/ev-family/ev-classic-resource-bible.txt lines 924-993':
        raise ValueError('sourced EV systems manifest syst field-layout summary changed Resource Bible source reference')
    field_families = [entry.get('fieldFamily') for entry in syst_field_layout.get('resourceBibleFieldFamilies', [])]
    if 'NavDef F1-F4 navigation defaults' not in field_families or 'Con6-Con16 additional hyperspace links' not in field_families:
        raise ValueError('sourced EV systems manifest syst field-layout summary missing source-backed field families')
    word_scouts = syst_field_layout.get('decodedWordGroupScouts', {})
    if word_scouts.get('frontFiveConCandidateWords4To8', {}).get('systemIdDomainValueCount') != 268:
        raise ValueError('sourced EV systems manifest syst field-layout summary has unexpected front Con scout count')
    if word_scouts.get('percentLikeWords20To23', {}).get('observedValueRange') != [5, 55]:
        raise ValueError('sourced EV systems manifest syst field-layout summary has unexpected percent-like word range')
    if word_scouts.get('allZeroTailWords24To43', {}).get('allValuesZero') is not True:
        raise ValueError('sourced EV systems manifest syst field-layout summary expected zero-only tail scout')
    if 'current Con1-Con16 link-slot scout window remains a candidate graph input' not in ' '.join(syst_field_layout.get('promotionBlockers', [])):
        raise ValueError('sourced EV systems manifest syst field-layout summary missing link-window promotion blocker')
    if syst_field_order_conflict.get('sourceLabel') != 'decoded-resource-backed-syst-field-order-conflict-scout':
        raise ValueError('sourced EV systems manifest missing syst field-order conflict scout')
    if syst_field_order_conflict.get('oracleStatus') != 'syst_field_order_mapping_pending_complete_oracle':
        raise ValueError('sourced EV systems manifest syst field-order conflict scout must keep mapping pending')
    conflict_scouts = syst_field_order_conflict.get('decodedWordGroupScouts', {})
    if conflict_scouts.get('currentCandidateLinkScoutWindowWords4To19', {}).get('systemIdDomainValueCount') != 268:
        raise ValueError('sourced EV systems manifest syst field-order conflict changed current link-domain count')
    if conflict_scouts.get('projectedCon6ToCon16Words27To37', {}).get('allValuesZero') is not True:
        raise ValueError('sourced EV systems manifest syst field-order conflict expected zero-only projected Con6-Con16 window')
    if 'Con6-Con16 split placement cannot be promoted' not in ' '.join(syst_field_order_conflict.get('promotionBlockers', [])):
        raise ValueError('sourced EV systems manifest syst field-order conflict missing Con6-Con16 promotion blocker')
    word_domain = data.get('systWordDomainCoverageSummary', {})
    if word_domain.get('sourceLabel') != 'decoded-resource-backed-syst-word-domain-coverage-scout':
        raise ValueError('sourced EV systems manifest missing syst word-domain coverage scout')
    if word_domain.get('oracleStatus') != 'syst_field_order_mapping_pending_complete_oracle':
        raise ValueError('sourced EV systems manifest word-domain coverage must keep field-order mapping pending')
    if word_domain.get('recordCount') != 67 or word_domain.get('recordSize') != 88 or word_domain.get('wordCount') != 44:
        raise ValueError('sourced EV systems manifest word-domain coverage has unexpected dimensions')
    word_domains = {entry.get('wordIndex'): entry for entry in word_domain.get('wordDomains', [])}
    if len(word_domains) != 44:
        raise ValueError('sourced EV systems manifest word-domain coverage missing word entries')
    if word_domains.get(4, {}).get('systemIdDomainValueCount') != 67:
        raise ValueError('sourced EV systems manifest word-domain coverage changed front link-domain count')
    if word_domains.get(8, {}).get('noLinkSentinelCount') != 67:
        raise ValueError('sourced EV systems manifest word-domain coverage changed no-link sentinel-only word')
    if word_domains.get(20, {}).get('observedValueRange') != [15, 40]:
        raise ValueError('sourced EV systems manifest word-domain coverage changed percent-like word range')
    if word_domains.get(24, {}).get('zeroValueCount') != 67 or word_domains.get(43, {}).get('zeroValueCount') != 67:
        raise ValueError('sourced EV systems manifest word-domain coverage changed zero-tail words')
    coverage = word_domain.get('coverageSignals', {})
    if coverage.get('systemIdDomainWords') != [1, 2, 4, 5, 6, 7]:
        raise ValueError('sourced EV systems manifest word-domain coverage changed system-ID-domain word list')
    if coverage.get('noLinkSentinelOnlyWords') != list(range(8, 20)) or coverage.get('zeroOnlyTailWords') != list(range(24, 44)):
        raise ValueError('sourced EV systems manifest word-domain coverage changed sentinel/zero coverage')
    if 'complete syst field-order oracle is still missing' not in word_domain.get('promotionBlockers', []):
        raise ValueError('sourced EV systems manifest word-domain coverage missing field-order blocker')
    seed_summary = data.get('systemNameSeedSummary', {})
    if seed_summary.get('sourceLabel') != 'decoded-resource-backed-system-name-seed-join-scout':
        raise ValueError('sourced EV systems manifest missing system-name seed summary source label')
    if seed_summary.get('oracleStatus') != 'exact_record_name_runtime_topology_mapping_pending':
        raise ValueError('sourced EV systems manifest system-name seed summary should keep runtime topology pending')
    if seed_summary.get('systemNameSeedCount') != len(seeds) or seed_summary.get('systemNameSeedNames', [])[:3] != ['Sol', 'Centauri', 'Sirius']:
        raise ValueError('sourced EV systems manifest system-name seed summary has unexpected seed coverage')
    if seed_summary.get('exactMappedSystemNames') != ['Levo'] or seed_summary.get('unjoinedSystemNameSeedCount') != len(seeds):
        raise ValueError('sourced EV systems manifest system-name seed summary has unexpected exact mapping boundary')
    record_name_readiness = data.get('recordToNamePromotionReadinessSummary', {})
    if record_name_readiness.get('sourceLabel') != 'decoded-resource-backed-record-to-name-promotion-readiness-scout':
        raise ValueError('sourced EV systems manifest missing record-to-name promotion readiness source label')
    if record_name_readiness.get('oracleStatus') != 'exact_record_name_runtime_topology_mapping_pending':
        raise ValueError('sourced EV systems manifest record-to-name readiness should keep runtime topology pending')
    if record_name_readiness.get('recordCount') != 67 or record_name_readiness.get('exactMappedRecordCount') != 1:
        raise ValueError('sourced EV systems manifest record-to-name readiness has unexpected record counts')
    if record_name_readiness.get('exactMappedResourceIds') != [128] or record_name_readiness.get('exactMappedSystemNames') != ['Levo']:
        raise ValueError('sourced EV systems manifest record-to-name readiness changed exact mapping boundary')
    if record_name_readiness.get('unjoinedRecordCount') != 66 or record_name_readiness.get('unjoinedResourceIdRange') != [129, 194]:
        raise ValueError('sourced EV systems manifest record-to-name readiness has unexpected unjoined records')
    if record_name_readiness.get('heuristicSystemNameSeedCount') != len(seeds) or not record_name_readiness.get('heuristicSeedCountDoesNotCoverRemainingRecords'):
        raise ValueError('sourced EV systems manifest record-to-name readiness has unexpected heuristic seed boundary')
    if 'landing-name byte proximity is a scout signal, not a syst record-to-name join' not in record_name_readiness.get('promotionBlockers', []):
        raise ValueError('sourced EV systems manifest record-to-name readiness must not promote byte-proximity joins')
    topology_readiness = data.get('topologyPromotionReadinessSummary', {})
    if topology_readiness.get('sourceLabel') != 'decoded-resource-backed-topology-promotion-readiness-matrix':
        raise ValueError('sourced EV systems manifest missing topology promotion readiness matrix source label')
    if topology_readiness.get('oracleStatus') != 'topology_semantic_promotion_pending_field_family_mapping':
        raise ValueError('sourced EV systems manifest topology promotion readiness should keep topology mapping pending')
    if topology_readiness.get('recordCount') != 67 or topology_readiness.get('exactMappedRecordCount') != 1:
        raise ValueError('sourced EV systems manifest topology promotion readiness has unexpected record counts')
    if topology_readiness.get('exactMappedResourceIds') != [128] or topology_readiness.get('unjoinedRecordCount') != 66:
        raise ValueError('sourced EV systems manifest topology promotion readiness changed exact mapping boundary')
    if 'complete decoded coordinate word pairs and link slots for all 67 records' not in topology_readiness.get('readyStaticInputFamilies', []):
        raise ValueError('sourced EV systems manifest topology promotion readiness missing ready static input family')
    if 'remaining 66 exact record-to-name joins' not in topology_readiness.get('blockedPromotionClaims', []):
        raise ValueError('sourced EV systems manifest topology promotion readiness must block remaining name joins')
    if 'not-promoted' not in topology_readiness.get('coordinatePromotionStatus', '') or 'not-promoted' not in topology_readiness.get('recordNamePromotionStatus', ''):
        raise ValueError('sourced EV systems manifest topology promotion readiness must not promote coordinates or remaining names')
    if 'blocked' not in topology_readiness.get('runtimeUniverseReplacementStatus', ''):
        raise ValueError('sourced EV systems manifest topology promotion readiness must block broad universe replacement')
    landing_proximity = data.get('systemNameLandingProximitySummary', {})
    if landing_proximity.get('sourceLabel') != 'decoded-resource-backed-system-name-landing-proximity-scout':
        raise ValueError('sourced EV systems manifest missing system-name landing-proximity source label')
    if landing_proximity.get('oracleStatus') != 'exact_record_name_runtime_topology_mapping_pending':
        raise ValueError('sourced EV systems manifest landing-proximity summary should keep runtime topology pending')
    if landing_proximity.get('systemNameSeedCount') != len(seeds) or landing_proximity.get('landingNameSeedCount', 0) < 70:
        raise ValueError('sourced EV systems manifest landing-proximity summary has unexpected seed counts')
    if landing_proximity.get('systemNameSeedsWithCloseLandingCandidates') != ['Centauri', 'Sirius', 'Tau Ceti', 'Alkaid', 'Zaxted', 'Clotho']:
        raise ValueError('sourced EV systems manifest landing-proximity close candidates changed unexpectedly')
    if landing_proximity.get('systemNameSeedsWithoutCloseLandingCandidates') != ['Sol', 'Enyo', 'Antares']:
        raise ValueError('sourced EV systems manifest landing-proximity distant candidates changed unexpectedly')
    exact_landing = landing_proximity.get('exactMappedSystemLandingCandidates', [{}])[0]
    if exact_landing.get('systemName') != 'Levo' or exact_landing.get('landingNameSeedByteOffsets') != [23867]:
        raise ValueError('sourced EV systems manifest landing-proximity exact mapped landing candidate changed unexpectedly')
    if 'not assign any syst resource ID' not in landing_proximity.get('sourceNote', ''):
        raise ValueError('sourced EV systems manifest landing-proximity summary must not promote record-to-name joins')
    domain = data.get('coordinateDomainSummary', {})
    if domain.get('sourceLabel') != 'decoded-resource-backed-coordinate-domain-scout':
        raise ValueError('sourced EV systems manifest missing coordinate domain summary source label')
    if domain.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate domain summary should keep display scaling pending')
    if domain.get('recordCount') != 67:
        raise ValueError('sourced EV systems manifest coordinate domain summary has unexpected record count')
    if domain.get('xPos', {}).get('highWordDistinctValues') != [1, 2, 3, 4]:
        raise ValueError('sourced EV systems manifest coordinate domain summary has unexpected x high-word domain')
    if domain.get('yPos', {}).get('highWordDistinctValues') != [0, 18, 72, 127, 133]:
        raise ValueError('sourced EV systems manifest coordinate domain summary has unexpected y high-word domain')
    if 'not-promoted' not in domain.get('displayUnitInterpretationStatus', ''):
        raise ValueError('sourced EV systems manifest coordinate domain summary must not promote display units')
    display_bounds = data.get('coordinateDisplayBoundsSummary', {})
    if display_bounds.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-bounds-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display-bounds summary source label')
    if display_bounds.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display-bounds summary should keep display scaling pending')
    if display_bounds.get('recordCount') != 67:
        raise ValueError('sourced EV systems manifest coordinate display-bounds summary has unexpected record count')
    if display_bounds.get('xPos', {}).get('rawHighWordCandidateSpan') != 3 or display_bounds.get('xPos', {}).get('rawLowWordCandidateSpan') != 153:
        raise ValueError('sourced EV systems manifest coordinate display-bounds summary has unexpected x spans')
    if display_bounds.get('yPos', {}).get('rawHighWordCandidateSpan') != 133 or display_bounds.get('yPos', {}).get('rawLowWordCandidateSpan') != 61440:
        raise ValueError('sourced EV systems manifest coordinate display-bounds summary has unexpected y spans')
    if display_bounds.get('xPos', {}).get('signedLongCandidateBounds') != [65664, 327679] or display_bounds.get('yPos', {}).get('signedLongCandidateBounds') != [1, 8720384]:
        raise ValueError('sourced EV systems manifest coordinate display-bounds summary has unexpected signed-long bounds')
    display_normalized = data.get('coordinateDisplayNormalizedSummary', {})
    if display_normalized.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-normalized-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display-normalized summary source label')
    if display_normalized.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display-normalized summary should keep display scaling pending')
    if display_normalized.get('xPos', {}).get('minNormalizedSignedLongCandidateRange') != [0, 262015] or display_normalized.get('yPos', {}).get('minNormalizedSignedLongCandidateRange') != [0, 8720383]:
        raise ValueError('sourced EV systems manifest coordinate display-normalized summary has unexpected ranges')
    if display_normalized.get('resource128', {}).get('yPos', {}).get('unitIntervalCandidate') != 0.954908:
        raise ValueError('sourced EV systems manifest coordinate display-normalized summary has unexpected Levo y unit interval')
    display_transform = data.get('coordinateDisplayTransformSummary', {})
    if display_transform.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-transform-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display-transform summary source label')
    if display_transform.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display-transform summary should keep display scaling pending')
    if 'not-promoted' not in display_transform.get('displayUnitInterpretationStatus', ''):
        raise ValueError('sourced EV systems manifest coordinate display-transform summary must not promote display units')
    if display_transform.get('signedLongAxisSpanRatioYOverX') != 33.281999:
        raise ValueError('sourced EV systems manifest coordinate display-transform summary has unexpected axis span ratio')
    if display_transform.get('resource128', {}).get('yPos', {}).get('invertedUnitIntervalCandidate') != 0.045092:
        raise ValueError('sourced EV systems manifest coordinate display-transform summary has unexpected Levo inverted y unit interval')
    display_fixed_point = data.get('coordinateDisplayFixedPointSummary', {})
    if display_fixed_point.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-fixed-point-scale-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display fixed-point scale source label')
    if display_fixed_point.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display fixed-point scale should keep display scaling pending')
    if display_fixed_point.get('fixedPointDivisorCandidate') != 65536:
        raise ValueError('sourced EV systems manifest coordinate display fixed-point scale has unexpected divisor')
    if display_fixed_point.get('xPos', {}).get('fixedPointCandidateBounds') != [1.001953, 4.999985] or display_fixed_point.get('yPos', {}).get('fixedPointCandidateBounds') != [0.000015, 133.0625]:
        raise ValueError('sourced EV systems manifest coordinate display fixed-point scale has unexpected bounds')
    if display_fixed_point.get('fixedPointAxisSpanRatioYOverX') != 33.281996:
        raise ValueError('sourced EV systems manifest coordinate display fixed-point scale has unexpected axis ratio')
    if display_fixed_point.get('resource128', {}).get('yPosFixedPointCandidate') != 127.0625:
        raise ValueError('sourced EV systems manifest coordinate display fixed-point scale has unexpected Levo y fixed-point candidate')
    if 'not-promoted' not in display_fixed_point.get('displayUnitInterpretationStatus', ''):
        raise ValueError('sourced EV systems manifest coordinate display fixed-point scale must not promote display units')
    display_integer_band = data.get('coordinateDisplayIntegerBandSummary', {})
    if display_integer_band.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-integer-band-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display integer-band source label')
    if display_integer_band.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display integer-band should keep display scaling pending')
    if '16.16 high-word integer-band candidate' not in display_integer_band.get('candidateFamilies', []):
        raise ValueError('sourced EV systems manifest coordinate display integer-band missing candidate family')
    if display_integer_band.get('xPos', {}).get('integerBandCandidateDistribution') != {'1': 12, '2': 7, '3': 32, '4': 16}:
        raise ValueError('sourced EV systems manifest coordinate display integer-band has unexpected x band distribution')
    if display_integer_band.get('yPos', {}).get('integerBandCandidateDistribution') != {'0': 42, '18': 1, '72': 4, '127': 19, '133': 1}:
        raise ValueError('sourced EV systems manifest coordinate display integer-band has unexpected y band distribution')
    if display_integer_band.get('resource128', {}).get('yPos', {}).get('integerBandCandidate') != 127:
        raise ValueError('sourced EV systems manifest coordinate display integer-band has unexpected Levo y band')
    if display_integer_band.get('resource129', {}).get('yPos', {}).get('signedFractionalResidualCandidate') != -32768:
        raise ValueError('sourced EV systems manifest coordinate display integer-band has unexpected resource 129 y residual')
    if 'not-promoted' not in display_integer_band.get('displayUnitInterpretationStatus', ''):
        raise ValueError('sourced EV systems manifest coordinate display integer-band must not promote display units')
    display_residual_sign = data.get('coordinateDisplayResidualSignSummary', {})
    if display_residual_sign.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-residual-sign-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display residual-sign source label')
    if display_residual_sign.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display residual-sign should keep display scaling pending')
    if '16.16 low-word residual sign distribution candidate' not in display_residual_sign.get('candidateFamilies', []):
        raise ValueError('sourced EV systems manifest coordinate display residual-sign missing candidate family')
    if display_residual_sign.get('fixedPointDivisorCandidate') != 65536:
        raise ValueError('sourced EV systems manifest coordinate display residual-sign has unexpected divisor')
    if display_residual_sign.get('xPos', {}).get('signedFractionalResidualSignDistribution') != {'negative': 4, 'zero': 0, 'positive': 63}:
        raise ValueError('sourced EV systems manifest coordinate display residual-sign has unexpected x sign distribution')
    if display_residual_sign.get('yPos', {}).get('signedFractionalResidualSignDistribution') != {'negative': 54, 'zero': 0, 'positive': 13}:
        raise ValueError('sourced EV systems manifest coordinate display residual-sign has unexpected y sign distribution')
    if display_residual_sign.get('yPos', {}).get('fractionalUnitCandidateDistinctValues') != [-0.5, 0.000015, 0.0625, 0.125, 0.4375]:
        raise ValueError('sourced EV systems manifest coordinate display residual-sign has unexpected y fractional units')
    if display_residual_sign.get('resource128', {}).get('yPosFractionalUnitCandidate') != 0.0625:
        raise ValueError('sourced EV systems manifest coordinate display residual-sign has unexpected Levo y fractional unit')
    if display_residual_sign.get('resource129', {}).get('yPosFractionalUnitCandidate') != -0.5:
        raise ValueError('sourced EV systems manifest coordinate display residual-sign has unexpected resource 129 y fractional unit')
    if 'not-promoted' not in display_residual_sign.get('displayUnitInterpretationStatus', ''):
        raise ValueError('sourced EV systems manifest coordinate display residual-sign must not promote display units')
    display_residual_magnitude = data.get('coordinateDisplayResidualMagnitudeSummary', {})
    if display_residual_magnitude.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-residual-magnitude-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display residual-magnitude source label')
    if display_residual_magnitude.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude should keep display scaling pending')
    if '16.16 low-word absolute residual magnitude candidate' not in display_residual_magnitude.get('candidateFamilies', []):
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude missing candidate family')
    if display_residual_magnitude.get('fixedPointDivisorCandidate') != 65536:
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude has unexpected divisor')
    if display_residual_magnitude.get('xPos', {}).get('absoluteResidualCandidateRange') != [1, 152]:
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude has unexpected x range')
    if display_residual_magnitude.get('xPos', {}).get('absoluteResidualCandidateDistribution', {}).get('128') != 14:
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude has unexpected x 128 count')
    if display_residual_magnitude.get('yPos', {}).get('absoluteResidualCandidateRange') != [1, 32768]:
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude has unexpected y range')
    if display_residual_magnitude.get('yPos', {}).get('absoluteFractionalUnitCandidateDistinctValues') != [0.000015, 0.0625, 0.125, 0.4375, 0.5]:
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude has unexpected y absolute fractional units')
    if display_residual_magnitude.get('yPos', {}).get('maxResidualMagnitudeResourceIds', [])[:3] != [129, 130, 132]:
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude has unexpected y max residual resources')
    if display_residual_magnitude.get('resource128', {}).get('yPosAbsoluteFractionalUnitCandidate') != 0.0625:
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude has unexpected Levo y absolute fractional unit')
    if display_residual_magnitude.get('resource129', {}).get('yPosAbsoluteFractionalUnitCandidate') != 0.5:
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude has unexpected resource 129 y absolute fractional unit')
    if 'not-promoted' not in display_residual_magnitude.get('displayUnitInterpretationStatus', ''):
        raise ValueError('sourced EV systems manifest coordinate display residual-magnitude must not promote display units')
    display_quantization = data.get('coordinateDisplayQuantizationSummary', {})
    if display_quantization.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-quantization-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display quantization source label')
    if display_quantization.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display quantization should keep display scaling pending')
    if '16.16 residual gcd quantization candidate' not in display_quantization.get('candidateFamilies', []):
        raise ValueError('sourced EV systems manifest coordinate display quantization missing candidate family')
    if display_quantization.get('fixedPointDivisorCandidate') != 65536:
        raise ValueError('sourced EV systems manifest coordinate display quantization has unexpected divisor')
    if display_quantization.get('xPos', {}).get('absoluteResidualGcdCandidate') != 1:
        raise ValueError('sourced EV systems manifest coordinate display quantization has unexpected x gcd')
    if display_quantization.get('xPos', {}).get('residualModulo128Distribution', {}).get('0') != 14:
        raise ValueError('sourced EV systems manifest coordinate display quantization has unexpected x modulo-128 count')
    if display_quantization.get('yPos', {}).get('coarseGridStepCandidate') != 4096:
        raise ValueError('sourced EV systems manifest coordinate display quantization has unexpected y coarse step')
    if display_quantization.get('yPos', {}).get('coarseGridStepFractionalUnitCandidate') != 0.0625:
        raise ValueError('sourced EV systems manifest coordinate display quantization has unexpected y coarse unit')
    if display_quantization.get('yPos', {}).get('coarseGridAlignedResourceCount') != 59:
        raise ValueError('sourced EV systems manifest coordinate display quantization has unexpected y grid alignment count')
    if display_quantization.get('yPos', {}).get('coarseGridOffstepResourceIds') != [166, 167, 168, 169, 170, 172, 183, 186]:
        raise ValueError('sourced EV systems manifest coordinate display quantization has unexpected y offstep resource ids')
    if 'not-promoted' not in display_quantization.get('displayUnitInterpretationStatus', ''):
        raise ValueError('sourced EV systems manifest coordinate display quantization must not promote display units')
    display_scale_interpretation = data.get('coordinateDisplayScaleInterpretationSummary', {})
    if display_scale_interpretation.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-scale-interpretation-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display scale interpretation source label')
    if display_scale_interpretation.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display scale interpretation should keep display scaling pending')
    if 'candidate-family comparison without Classic map-pixel promotion' not in display_scale_interpretation.get('candidateFamilies', []):
        raise ValueError('sourced EV systems manifest coordinate display scale interpretation missing candidate family')
    if display_scale_interpretation.get('fixedPointDivisorCandidate') != 65536:
        raise ValueError('sourced EV systems manifest coordinate display scale interpretation has unexpected divisor')
    scale_spans = display_scale_interpretation.get('spanComparisons', {})
    if scale_spans.get('signedLongAxisSpanRatioYOverX') != 33.281999 or scale_spans.get('fixedPointAxisSpanRatioYOverX') != 33.281996:
        raise ValueError('sourced EV systems manifest coordinate display scale interpretation has unexpected signed/fixed ratio')
    if scale_spans.get('rawHighWordAxisSpanRatioYOverX') != 44.333333:
        raise ValueError('sourced EV systems manifest coordinate display scale interpretation has unexpected raw high-word ratio')
    if 'no Classic map pixel/click/capture evidence in this static packet' not in display_scale_interpretation.get('scalePromotionBlockers', []):
        raise ValueError('sourced EV systems manifest coordinate display scale interpretation missing map evidence blocker')
    if 'not-promoted' not in display_scale_interpretation.get('displayUnitInterpretationStatus', ''):
        raise ValueError('sourced EV systems manifest coordinate display scale interpretation must not promote display units')
    display_extrema = data.get('coordinateDisplayExtremaSummary', {})
    if display_extrema.get('sourceLabel') != 'decoded-resource-backed-coordinate-display-extrema-scout':
        raise ValueError('sourced EV systems manifest missing coordinate display-extrema summary source label')
    if display_extrema.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest coordinate display-extrema summary should keep display scaling pending')
    if display_extrema.get('recordCount') != 67:
        raise ValueError('sourced EV systems manifest coordinate display-extrema summary has unexpected record count')
    x_extrema = display_extrema.get('xPos', {})
    y_extrema = display_extrema.get('yPos', {})
    if x_extrema.get('rawLowWord', {}).get('minResourceIds') != [133, 144, 155, 156] or x_extrema.get('rawLowWord', {}).get('maxResourceIds') != [192]:
        raise ValueError('sourced EV systems manifest coordinate display-extrema summary has unexpected x low-word extrema')
    if x_extrema.get('signedLongCandidate', {}).get('minResourceIds', [])[:3] != [128, 139, 140] or x_extrema.get('signedLongCandidate', {}).get('maxResourceIds') != [155, 156]:
        raise ValueError('sourced EV systems manifest coordinate display-extrema summary has unexpected x signed-long extrema')
    if y_extrema.get('rawHighWord', {}).get('maxResourceIds') != [182] or y_extrema.get('rawLowWord', {}).get('maxResourceIds') != [133, 144]:
        raise ValueError('sourced EV systems manifest coordinate display-extrema summary has unexpected y word extrema')
    if y_extrema.get('signedLongCandidate', {}).get('minResourceIds') != [168, 169, 170, 172, 183, 186] or y_extrema.get('signedLongCandidate', {}).get('maxResourceIds') != [182]:
        raise ValueError('sourced EV systems manifest coordinate display-extrema summary has unexpected y signed-long extrema')
    link_graph = data.get('candidateLinkGraphSummary', {})
    if link_graph.get('sourceLabel') != 'decoded-resource-backed-candidate-link-graph-scout':
        raise ValueError('sourced EV systems manifest missing candidate link-graph summary source label')
    if link_graph.get('oracleStatus') != 'exact_record_name_runtime_topology_mapping_pending':
        raise ValueError('sourced EV systems manifest candidate link-graph summary should keep runtime topology pending')
    if link_graph.get('recordCount') != 67 or link_graph.get('directedLinkSlotCount') != 268:
        raise ValueError('sourced EV systems manifest candidate link-graph summary has unexpected link counts')
    if link_graph.get('reciprocalDirectedLinkCount') != 8 or link_graph.get('nonReciprocalDirectedLinkCount') != 109:
        raise ValueError('sourced EV systems manifest candidate link-graph summary has unexpected reciprocity counts')
    if link_graph.get('uniqueSelfLinkCount') != 4 or link_graph.get('uniqueSelfLinkResourceIds') != [128, 136, 139, 140]:
        raise ValueError('sourced EV systems manifest candidate link-graph summary has unexpected self-link statistics')
    if link_graph.get('linkedSlotsPerSystemRange') != [4, 4] or link_graph.get('systemsWithNoLinkedSlots') != 0:
        raise ValueError('sourced EV systems manifest candidate link-graph summary has unexpected per-system link distribution')
    if link_graph.get('allTargetsPresentInSystRun') is not True or link_graph.get('missingTargetEdges') != []:
        raise ValueError('sourced EV systems manifest candidate link-graph summary has missing targets')
    connectivity = data.get('candidateGraphConnectivitySummary', {})
    if connectivity.get('sourceLabel') != 'decoded-resource-backed-candidate-graph-connectivity-scout':
        raise ValueError('sourced EV systems manifest missing candidate graph connectivity source label')
    if connectivity.get('oracleStatus') != 'exact_record_name_runtime_topology_mapping_pending':
        raise ValueError('sourced EV systems manifest candidate graph connectivity should keep runtime topology pending')
    if connectivity.get('recordCount') != 67 or connectivity.get('weaklyConnectedComponentCount') != 1:
        raise ValueError('sourced EV systems manifest candidate graph connectivity has unexpected component count')
    if connectivity.get('resource128WeakComponentSize') != 67 or connectivity.get('resource128DirectedReachableCount') != 21:
        raise ValueError('sourced EV systems manifest candidate graph connectivity has unexpected resource 128 reachability')
    if connectivity.get('resource128DirectedUnreachableCount') != 46:
        raise ValueError('sourced EV systems manifest candidate graph connectivity has unexpected unreachable count')
    if connectivity.get('uniqueOutDegreeDistribution') != {'1': 39, '2': 14, '3': 6, '4': 8}:
        raise ValueError('sourced EV systems manifest candidate graph connectivity has unexpected out-degree distribution')
    if connectivity.get('zeroOutDegreeResourceIds') != []:
        raise ValueError('sourced EV systems manifest candidate graph connectivity should have no zero-out-degree records')
    distances = data.get('candidateGraphDistanceSummary', {})
    if distances.get('sourceLabel') != 'decoded-resource-backed-candidate-graph-distance-scout':
        raise ValueError('sourced EV systems manifest missing candidate graph distance source label')
    if distances.get('oracleStatus') != 'exact_record_name_runtime_topology_mapping_pending':
        raise ValueError('sourced EV systems manifest candidate graph distance should keep runtime topology pending')
    if distances.get('recordCount') != 67:
        raise ValueError('sourced EV systems manifest candidate graph distance has unexpected record count')
    if distances.get('resource128DirectedMaxHopDistance') != 4 or distances.get('resource128WeakMaxHopDistance') != 4:
        raise ValueError('sourced EV systems manifest candidate graph distance has unexpected resource 128 hop range')
    if distances.get('resource128WeakHopDistanceDistribution') != {'0': 1, '1': 3, '2': 19, '3': 31, '4': 13}:
        raise ValueError('sourced EV systems manifest candidate graph distance has unexpected weak hop distribution')
    if distances.get('weakGraphDiameterCandidate') != 7:
        raise ValueError('sourced EV systems manifest candidate graph distance has unexpected weak diameter candidate')
    if distances.get('directedReachableCountRange') != [2, 22]:
        raise ValueError('sourced EV systems manifest candidate graph distance has unexpected directed reachable count range')
    start_topology = data.get('startSystemCandidateTopologySummary', {})
    if start_topology.get('sourceLabel') != 'decoded-resource-backed-start-system-candidate-topology-scout':
        raise ValueError('sourced EV systems manifest missing start-system candidate topology source label')
    if start_topology.get('oracleStatus') != 'exact_record_name_runtime_topology_mapping_pending':
        raise ValueError('sourced EV systems manifest start-system topology should keep runtime topology pending')
    if start_topology.get('startResourceId') != 128 or start_topology.get('startExactSystemName') != 'Levo':
        raise ValueError('sourced EV systems manifest start-system topology has unexpected start identity')
    if start_topology.get('linkedNeighborCount') != 4:
        raise ValueError('sourced EV systems manifest start-system topology has unexpected neighbor count')
    if start_topology.get('selfLinkSlotNames') != ['Con1'] or start_topology.get('reciprocalNeighborResourceIds') != [128]:
        raise ValueError('sourced EV systems manifest start-system topology has unexpected reciprocal/self-link boundary')
    if start_topology.get('unjoinedNeighborResourceIds') != [129, 130, 131]:
        raise ValueError('sourced EV systems manifest start-system topology should keep target names unjoined')
    start_neighbors = start_topology.get('linkedNeighbors', [])
    if [neighbor.get('targetResourceId') for neighbor in start_neighbors] != [128, 129, 130, 131]:
        raise ValueError('sourced EV systems manifest start-system topology has unexpected target resource order')
    if start_neighbors[1].get('targetCoordinateSignedLongCandidate') != {'xPos': 196736, 'yPos': 32768}:
        raise ValueError('sourced EV systems manifest start-system topology has unexpected neighbor coordinate candidate')
    start_display = data.get('startNeighborhoodDisplayTransformSummary', {})
    if start_display.get('sourceLabel') != 'decoded-resource-backed-start-neighborhood-display-transform-scout':
        raise ValueError('sourced EV systems manifest missing start-neighborhood display-transform source label')
    if start_display.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest start-neighborhood display-transform should keep display scaling pending')
    if start_display.get('startResourceId') != 128 or start_display.get('startExactSystemName') != 'Levo':
        raise ValueError('sourced EV systems manifest start-neighborhood display-transform has unexpected start identity')
    if start_display.get('linkedNeighborCount') != 4 or start_display.get('unjoinedNeighborResourceIds') != [129, 130, 131]:
        raise ValueError('sourced EV systems manifest start-neighborhood display-transform has unexpected neighbor boundary')
    display_neighbors = start_display.get('linkedNeighbors', [])
    if [neighbor.get('targetResourceId') for neighbor in display_neighbors] != [128, 129, 130, 131]:
        raise ValueError('sourced EV systems manifest start-neighborhood display-transform has unexpected target resource order')
    if display_neighbors[1].get('deltaSignedLongFromStart') != {'xPos': 131072, 'yPos': -8294400}:
        raise ValueError('sourced EV systems manifest start-neighborhood display-transform has unexpected resource 129 delta')
    if display_neighbors[1].get('unitIntervalCandidate', {}).get('invertedYPos') != 0.996242:
        raise ValueError('sourced EV systems manifest start-neighborhood display-transform has unexpected resource 129 inverted y')
    start_distance = data.get('startNeighborhoodDisplayDistanceSummary', {})
    if start_distance.get('sourceLabel') != 'decoded-resource-backed-start-neighborhood-display-distance-scout':
        raise ValueError('sourced EV systems manifest missing start-neighborhood display-distance source label')
    if start_distance.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest start-neighborhood display-distance should keep display scaling pending')
    if start_distance.get('startResourceId') != 128 or start_distance.get('startExactSystemName') != 'Levo':
        raise ValueError('sourced EV systems manifest start-neighborhood display-distance has unexpected start identity')
    if start_distance.get('linkedNeighborCount') != 4:
        raise ValueError('sourced EV systems manifest start-neighborhood display-distance has unexpected neighbor count')
    distance_neighbors = start_distance.get('linkedNeighbors', [])
    if [neighbor.get('targetResourceId') for neighbor in distance_neighbors] != [128, 129, 130, 131]:
        raise ValueError('sourced EV systems manifest start-neighborhood display-distance has unexpected target resource order')
    if distance_neighbors[1].get('manhattanSignedLongCandidate') != 8425472:
        raise ValueError('sourced EV systems manifest start-neighborhood display-distance has unexpected resource 129 signed-long distance')
    if distance_neighbors[3].get('manhattanInvertedYUnitIntervalCandidate') != 0.250593:
        raise ValueError('sourced EV systems manifest start-neighborhood display-distance has unexpected resource 131 unit distance')
    if start_distance.get('nonSelfSignedLongManhattanDistanceRange') != [69632, 8425473]:
        raise ValueError('sourced EV systems manifest start-neighborhood display-distance has unexpected signed-long distance range')
    start_vector = data.get('startNeighborhoodDisplayVectorSummary', {})
    if start_vector.get('sourceLabel') != 'decoded-resource-backed-start-neighborhood-display-vector-scout':
        raise ValueError('sourced EV systems manifest missing start-neighborhood display-vector source label')
    if start_vector.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest start-neighborhood display-vector should keep display scaling pending')
    vector_neighbors = start_vector.get('linkedNeighbors', [])
    if [neighbor.get('targetResourceId') for neighbor in vector_neighbors] != [128, 129, 130, 131]:
        raise ValueError('sourced EV systems manifest start-neighborhood display-vector has unexpected target resource order')
    if vector_neighbors[1].get('displayQuadrantCandidate') != 'north-east' or vector_neighbors[1].get('dominantAxisCandidate') != 'y':
        raise ValueError('sourced EV systems manifest start-neighborhood display-vector has unexpected resource 129 quadrant/axis')
    if vector_neighbors[3].get('signedAngleDegreesFromPositiveXCandidate') != -0.107663:
        raise ValueError('sourced EV systems manifest start-neighborhood display-vector has unexpected resource 131 angle')
    if start_vector.get('nonSelfDisplayQuadrantCandidates') != ['north-east', 'south-east']:
        raise ValueError('sourced EV systems manifest start-neighborhood display-vector has unexpected quadrant summary')
    slot_order = data.get('startNeighborhoodSlotVectorOrderSummary', {})
    if slot_order.get('sourceLabel') != 'decoded-resource-backed-start-neighborhood-slot-vector-order-scout':
        raise ValueError('sourced EV systems manifest missing start-neighborhood slot-vector order source label')
    if slot_order.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest start-neighborhood slot-vector order should keep display scaling pending')
    if [entry.get('targetResourceId') for entry in slot_order.get('linkedSlotOrder', [])] != [128, 129, 130, 131]:
        raise ValueError('sourced EV systems manifest start-neighborhood slot-vector order has unexpected target resource order')
    if slot_order.get('nonSelfResourceIdsByDistanceCandidate') != [131, 129, 130]:
        raise ValueError('sourced EV systems manifest start-neighborhood slot-vector order has unexpected distance order')
    if slot_order.get('firstNonSelfSlotName') != 'Con2' or slot_order.get('firstNonSelfResourceId') != 129:
        raise ValueError('sourced EV systems manifest start-neighborhood slot-vector order has unexpected first non-self link')
    slot_angular = data.get('startNeighborhoodSlotAngularOrderSummary', {})
    if slot_angular.get('sourceLabel') != 'decoded-resource-backed-start-neighborhood-slot-angular-order-scout':
        raise ValueError('sourced EV systems manifest missing start-neighborhood slot-angular order source label')
    if slot_angular.get('oracleStatus') != 'coordinate_display_units_map_scaling_pending':
        raise ValueError('sourced EV systems manifest start-neighborhood slot-angular order should keep display scaling pending')
    if [entry.get('targetResourceId') for entry in slot_angular.get('linkedSlotAngularOrder', [])] != [128, 129, 130, 131]:
        raise ValueError('sourced EV systems manifest start-neighborhood slot-angular order has unexpected target resource order')
    if slot_angular.get('nonSelfResourceIdsBySignedAngleCandidate') != [131, 130, 129]:
        raise ValueError('sourced EV systems manifest start-neighborhood slot-angular order has unexpected angle order')
    if slot_angular.get('firstSignedAngleNonSelfSlotName') != 'Con4' or slot_angular.get('firstSignedAngleNonSelfResourceId') != 131:
        raise ValueError('sourced EV systems manifest start-neighborhood slot-angular order has unexpected first angle candidate')
    mappings = data.get('exactSystemNameMappings', [])
    if len(mappings) != 1 or mappings[0].get('resourceId') != 128 or mappings[0].get('systemName') != 'Levo':
        raise ValueError('sourced EV systems manifest missing exact Levo resource mapping')
    first_exact_name = systems[0]['semanticFields'].get('exactSystemName', {})
    if first_exact_name.get('systemName') != 'Levo' or first_exact_name.get('resourceId') != 128:
        raise ValueError('sourced EV systems manifest first system is not mapped to Levo')
    if 'original-runtime-observed' not in first_exact_name.get('sourceBasis', []):
        raise ValueError('sourced EV systems manifest Levo mapping missing runtime source basis')
    boundary = data.get('promotionBoundary', '')
    if (
        'Con1-Con16 link slot names' not in boundary
        or 'resource ID 128 to Levo' not in boundary
        or 'link-slot/display-vector order analysis' not in boundary
        or 'slot/angular order analysis' not in boundary
        or 'integer-band/fractional residual candidates' not in boundary
    ):
        raise ValueError('sourced EV systems manifest missing promotion boundary')
    return data


def sourced_ev_services_manifest(path=SOURCED_EV_SERVICES_PATH):
    data = json.loads(path.read_text())
    if data.get('schemaVersion') != 1:
        raise ValueError('sourced EV services manifest has unexpected schema version')
    if data.get('method') != 'terminal-velocity-service-matrix-scaffold-plus-source-seeds-v1':
        raise ValueError('sourced EV services manifest has unexpected extraction method')
    run = data.get('spobRecordRun', {})
    if run.get('candidateType') != 'spob-like' or run.get('recordSize') != 400 or run.get('count') != 219:
        raise ValueError('sourced EV services manifest has unexpected spob run')
    seeds = data.get('landingNameSeeds', [])
    if len(seeds) < 72 or 'Earth' not in {seed.get('name') for seed in seeds}:
        raise ValueError('sourced EV services manifest missing landing name seeds')
    matrix = data.get('serviceMatrix', [])
    if len(matrix) < 20:
        raise ValueError('sourced EV services manifest has too few service rows')
    by_key = {(entry.get('systemName'), entry.get('bodyName')): entry for entry in matrix}
    if ('Levo', 'Levo') not in by_key or ('Sol', 'Earth') not in by_key:
        raise ValueError('sourced EV services manifest missing representative service rows')
    levo = by_key[('Levo', 'Levo')]
    if 'original-runtime-observed' not in levo.get('sourceLabels', []) or 'outfitter' in levo.get('services', []):
        raise ValueError('Levo service row does not preserve original-runtime no-outfitter boundary')
    earth = by_key[('Sol', 'Earth')]
    if not {'outfitter', 'shipyard', 'commodities', 'missions'}.issubset(set(earth.get('services', []))):
        raise ValueError('Earth service scaffold row missing expected current TV services')
    if 'Classic-wide decoded service fields remain pending' not in data.get('promotionBoundary', ''):
        raise ValueError('sourced EV services manifest missing promotion boundary')
    return data


def sourced_ev_weapons_manifest(path=SOURCED_EV_WEAPONS_PATH):
    data = json.loads(path.read_text())
    if data.get('schemaVersion') != 1:
        raise ValueError('sourced EV weapons manifest has unexpected schema version')
    if data.get('method') != 'ev-classic-resource-bible-weapon-field-map-v1':
        raise ValueError('sourced EV weapons manifest has unexpected extraction method')
    if data.get('sourceBasis') != 'EV Classic Resource Bible wëap/oütf field definitions plus local primitive BRGR structure decode':
        raise ValueError('sourced EV weapons manifest has unexpected source basis')
    weapons = data.get('weapons', [])
    if len(weapons) != 42:
        raise ValueError('sourced EV weapons manifest has unexpected weapon count')
    by_resource_id = {weapon.get('resourceId'): weapon for weapon in weapons}
    for expected_id, expected_name in [(128, 'Laser Cannon'), (129, 'Neutron Blaster'), (131, 'Torp. Launcher'), (132, 'Missile Rack'), (146, 'Fighter Bay')]:
        weapon = by_resource_id.get(expected_id)
        if weapon is None:
            raise ValueError(f'sourced EV weapons manifest missing resource {expected_id}')
        if expected_name not in weapon.get('outfitNames', []):
            raise ValueError(f'sourced EV weapon {expected_id} missing outfit name {expected_name}')
    required_fields = ['Reload', 'Count', 'MassDmg', 'EnergyDmg', 'Guidance', 'Speed', 'AmmoType', 'Graphic', 'Inaccuracy', 'Sound', 'Impact', 'ExplodType', 'ProxRadius', 'BlastRadius', 'Flags']
    for weapon in weapons:
        for key in ['resourceId', 'sourceDataOrdinal', 'chunkIndex', 'byteOffset', 'size', 'semanticFields', 'rawWords0To14', 'sourceBasis', 'sourceConfidence']:
            if key not in weapon:
                raise ValueError(f'sourced EV weapon missing {key}')
        fields = weapon['semanticFields']
        for field_name in required_fields:
            if field_name not in fields:
                raise ValueError(f"sourced EV weapon {weapon['resourceId']} missing {field_name}")
            if 'wordIndex' not in fields[field_name] or 'value' not in fields[field_name]:
                raise ValueError(f"sourced EV weapon {weapon['resourceId']} field {field_name} missing word provenance")
    unresolved = data.get('unresolvedOutfitWeaponLinks', [])
    if not any(link.get('modValWeaponResourceId') == 191 and link.get('outfitDisplayName') == 'Forklift' for link in unresolved):
        raise ValueError('sourced EV weapons manifest should preserve unresolved Forklift weapon link')
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


def sourced_ev_governments_manifest(path=SOURCED_EV_GOVERNMENTS_PATH):
    data = json.loads(path.read_text())
    if data.get('method') != 'ev-classic-resource-bible-govt-field-map-v1':
        raise ValueError('sourced EV governments manifest has unexpected extraction method')
    if data.get('sourceBasis') != 'EV Classic Resource Bible gövt field definitions plus local primitive BRGR structure decode':
        raise ValueError('sourced EV governments manifest has unexpected source basis')
    governments = data.get('governments', [])
    if len(governments) < 20:
        raise ValueError('sourced EV governments manifest has too few governments')
    by_id = {entry.get('resourceId'): entry for entry in governments}
    for expected_id in [128, 129, 130, 133]:
        if expected_id not in by_id:
            raise ValueError(f'sourced EV governments missing resource {expected_id}')
    for entry in governments:
        fields = entry.get('semanticFields', {})
        for key in ['flagsUnsigned', 'flagNames', 'crimeTolerance', 'smugglingPenalty', 'disablePenalty', 'boardPenalty', 'killPenalty', 'shootPenalty', 'initialRecord']:
            if key not in fields:
                raise ValueError(f"sourced EV government {entry.get('resourceId')} missing {key}")
    confed = by_id[128]['semanticFields']
    pirate = by_id[130]['semanticFields']
    if confed['crimeTolerance'] != 50 or confed['killPenalty'] != 25:
        raise ValueError('Confed government semantics do not match Classic Resource Bible field map expectations')
    if pirate['crimeTolerance'] != -20 or 'xenophobicWarshipsAttackNonAllies' not in pirate.get('flagNames', []):
        raise ValueError('Pirate government semantics do not match Classic Resource Bible field map expectations')
    return data


def sourced_ev_junk_manifest(path=SOURCED_EV_JUNK_PATH):
    data = json.loads(path.read_text())
    if data.get('schemaVersion') != 1:
        raise ValueError('sourced EV junk manifest has unexpected schema version')
    if data.get('method') != 'ev-classic-resource-bible-junk-field-map-v1':
        raise ValueError('sourced EV junk manifest has unexpected extraction method')
    if data.get('sourceBasis') != 'EV Classic Resource Bible jünk field definitions plus local primitive BRGR structure decode':
        raise ValueError('sourced EV junk manifest has unexpected source basis')
    run = data.get('recordRun', {})
    if run.get('candidateType') != 'commodity-like' or run.get('recordSize') != 676:
        raise ValueError('sourced EV junk manifest has unexpected record run')
    commodities = data.get('junkCommodities', [])
    if len(commodities) != 19:
        raise ValueError('sourced EV junk manifest has unexpected commodity count')
    by_id = {entry.get('resourceId'): entry for entry in commodities}
    for expected_id in [128, 129, 143]:
        if expected_id not in by_id:
            raise ValueError(f'sourced EV junk manifest missing resource {expected_id}')
    for entry in commodities:
        for key in ['resourceId', 'ordinal', 'chunkIndex', 'byteOffset', 'displayName', 'shortName', 'fieldSource', 'semanticFields']:
            if key not in entry:
                raise ValueError(f'sourced EV junk entry missing {key}')
        fields = entry.get('semanticFields', {})
        for key in ['soldAtStellarId', 'boughtAtStellarId', 'basePrice', 'flagsUnsigned', 'flagNames']:
            if key not in fields:
                raise ValueError(f"sourced EV junk {entry.get('resourceId')} missing {key}")
    if by_id[128]['displayName'] != 'self-sealing stembolts' or by_id[128]['semanticFields']['basePrice'] != 50:
        raise ValueError('sourced EV junk first commodity semantics do not match decoded resource')
    if by_id[143]['semanticFields']['boughtAtStellarId'] is not None or 'tribblesMultiplication' not in by_id[143]['semanticFields']['flagNames']:
        raise ValueError('sourced EV junk tribbles/parrots flag semantics not decoded')
    return data


def sourced_ev_missions_manifest(path=SOURCED_EV_MISSIONS_PATH):
    data = json.loads(path.read_text())
    if data.get('method') != 'ev-classic-resource-bible-misn-field-map-v2':
        raise ValueError('sourced EV missions manifest has unexpected extraction method')
    if data.get('sourceBasis') != 'EV Classic Resource Bible mïsn field definitions through Flags plus local primitive BRGR structure decode':
        raise ValueError('sourced EV missions manifest has unexpected source basis')
    missions = data.get('missions', [])
    if len(missions) < 100:
        raise ValueError('sourced EV missions manifest has too few missions')
    field_index = data.get('fieldIndex', {})
    for key in ['availStel', 'availBitSet', 'availLoc', 'availRecord', 'availRating', 'availRandom', 'travelStel', 'returnStel', 'cargoType', 'cargoQuantity', 'pickupMode', 'dropOffMode', 'scanGovernment', 'failIfScanned', 'unknownFieldBeforePayValue', 'payValue', 'shipCount', 'shipSystem', 'shipDude', 'shipGoal', 'shipBehavior', 'shipNameId', 'completionBitSet', 'completionGovernment', 'completionReward', 'failureBitSet', 'briefText', 'quickBrief', 'loadCargoText', 'dumpCargoText', 'completionText', 'failureText', 'timeLimit', 'canAbort', 'availBitClear', 'auxShipCount', 'auxShipDude', 'auxShipSystem', 'completionBitSet2', 'flags']:
        if key not in field_index:
            raise ValueError(f'sourced EV missions manifest missing field index {key}')
    for mission in missions[:10]:
        semantic = mission.get('semanticFields', {})
        for key in ['availability', 'travel', 'cargo', 'reward', 'specialShips', 'auxiliaryShips', 'completion', 'descriptions', 'lifecycle']:
            if key not in semantic:
                raise ValueError(f"sourced EV mission {mission.get('resourceId')} missing semantic {key}")
    first = missions[0]
    if first['resourceId'] != 128 or first['rawFields']['availStel'] != 20002:
        raise ValueError('sourced EV mission 128 availability fields do not match decoded resource')
    if first['semanticFields']['availability']['stellar']['kind'] != 'notGovernmentStellar':
        raise ValueError('sourced EV mission 128 availability selector not decoded')
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


def _ev_classic_ship_physics_fields(record):
    """Decode source-backed EV Classic ship physics primitives.

    Field order comes from EVNEW's CShipResource::Load/Save for the 1860-byte
    ship resource record: words 0-8 are Cargo, Shields, Acceleration, Max
    Speed, Turning, Fuel, Free Mass, Armor, and Shield Recharge.
    """
    fields = _fields_by_index(record)
    return {
        'cargoSpace': int(fields.get(0, 0)),
        'shields': int(fields.get(1, 0)),
        'acceleration': int(fields.get(2, 0)),
        'maxSpeed': int(fields.get(3, 0)),
        'turning': int(fields.get(4, 0)),
        'fuel': int(fields.get(5, 0)),
        'freeMass': int(fields.get(6, 0)),
        'armor': int(fields.get(7, 0)),
        'shieldRecharge': int(fields.get(8, 0)),
    }


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
        physics = _ev_classic_ship_physics_fields(record)
        stats['cargoSpace'] = physics['cargoSpace']
        stats['hull'] = physics['armor']
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
            'sourceDataPhysicsFields': physics,
            'physicsSource': 'EV Data.rez ship-like record words 0-8 via EVNEW CShipResource field order',
            'acceleration': physics['acceleration'],
            'maxSpeed': physics['maxSpeed'],
            'turning': physics['turning'],
            'shields': physics['shields'],
            'shieldRecharge': physics['shieldRecharge'],
            'fuel': physics['fuel'],
            'freeMass': physics['freeMass'],
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
    threshold_by_gov = mechanics.get('crimeToleranceLegalScoreByGovernment', {})
    hostile_threshold = int(threshold_by_gov.get(government, mechanics.get('crimeToleranceLegalScore', mechanics.get('patrolHostileLegalScore', -60))))
    if score <= hostile_threshold:
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
        legal_by_government = event.get('legal', {})
        legal_delta = int(legal_by_government.get(government, legal_by_government.get('*', 0)))
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
    legal_deltas = event.get('legal', {})
    if government is not None and (government in legal_deltas or '*' in legal_deltas):
        delta = legal_deltas.get(government, legal_deltas.get('*', 0))
        legal_records[government] = int(legal_records.get(government, 0)) + int(delta)
    else:
        for gov, delta in legal_deltas.items():
            if gov == '*':
                continue
            legal_records[gov] = int(legal_records.get(gov, 0)) + int(delta)
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
    current_system = data.get('currentSystem', 'Levo')
    return {
        'schemaVersion': int(data.get('schemaVersion', 1)),
        'credits': int(data.get('credits', 10000)),
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
