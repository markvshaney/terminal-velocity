#!/usr/bin/env python3
"""Promote EV Classic weapon/outfit cross-links from primitive BRGR records.

This derives a compact, source-provenance-preserving manifest from
native_ev/data/sourced_ev_structures.json. It does not replace the complete raw
field manifest; it only names the Classic Resource Bible fields that are stable
for EV Classic `wëap`/`oütf` records and records outfit-based stock weapon names.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STRUCTURES_PATH = Path('native_ev/data/sourced_ev_structures.json')
OUT_PATH = Path('native_ev/data/sourced_ev_weapons.json')
METHOD = 'ev-classic-resource-bible-weapon-field-map-v1'
SOURCE_BASIS = 'EV Classic Resource Bible wëap/oütf field definitions plus local primitive BRGR structure decode'

WEAP_FIELD_NAMES = [
    'Reload',
    'Count',
    'MassDmg',
    'EnergyDmg',
    'Guidance',
    'Speed',
    'AmmoType',
    'Graphic',
    'Inaccuracy',
    'Sound',
    'Impact',
    'ExplodType',
    'ProxRadius',
    'BlastRadius',
    'Flags',
]

OUTF_FIELD_NAMES = [
    'MissionBit',
    'Mass',
    'TechLevel',
    'ModType',
    'ModVal',
    'Max',
    'Flags',
    'Govt',
    'Cost',
]

MOD_TYPE_LABELS = {
    1: 'weapon',
    2: 'cargo-space',
    3: 'ammunition',
    4: 'shield-capacity',
    5: 'shield-recharge',
    6: 'armor',
    7: 'acceleration-booster',
    8: 'speed-increase',
    9: 'turn-rate-increase',
    10: 'ecm',
    11: 'escape-pod',
    12: 'fuel-capacity',
    13: 'density-scanner',
    14: 'iff',
    15: 'afterburner',
    16: 'map',
    17: 'cloaking-device',
    18: 'fuel-scoop',
    19: 'auto-refueller',
    20: 'auto-eject',
    21: 'clean-legal-record',
    22: 'hyperspace-speed-mod',
    23: 'hyperspace-dist-mod',
}


def _run_by_type(structures: dict[str, Any], candidate_type: str) -> dict[str, Any]:
    for run in structures.get('runs', []):
        if run.get('candidateType') == candidate_type:
            return run
    raise ValueError(f'missing {candidate_type} run')


def _words(record: dict[str, Any]) -> list[int]:
    return [int(field['value']) for field in record.get('fields', [])]


def _named_fields(words: list[int], names: list[str]) -> dict[str, dict[str, int]]:
    mapped: dict[str, dict[str, int]] = {}
    for index, name in enumerate(names):
        mapped[name] = {'wordIndex': index, 'value': words[index]}
    return mapped


def _strings(record: dict[str, Any]) -> list[str]:
    return [slot['text'] for slot in record.get('embeddedStrings', []) if slot.get('text')]


def derive_manifest(structures: dict[str, Any]) -> dict[str, Any]:
    weapon_run = _run_by_type(structures, 'weapon-like')
    outfit_run = _run_by_type(structures, 'outfit-like')

    weapon_records_by_id = {
        128 + int(record['ordinal']): record
        for record in weapon_run.get('records', [])
    }

    outfit_links_by_weapon: dict[int, list[dict[str, Any]]] = {}
    outfit_links: list[dict[str, Any]] = []
    for record in outfit_run.get('records', []):
        words = _words(record)
        if len(words) < len(OUTF_FIELD_NAMES):
            continue
        fields = _named_fields(words, OUTF_FIELD_NAMES)
        mod_type = fields['ModType']['value']
        mod_val = fields['ModVal']['value']
        if mod_type not in (1, 3):
            continue
        names = _strings(record)
        entry = {
            'sourceDataOrdinal': int(record['ordinal']),
            'chunkIndex': int(record['chunkIndex']),
            'byteOffset': int(record['byteOffset']),
            'size': int(record['size']),
            'outfitDisplayName': names[0] if names else None,
            'outfitSingularName': names[1] if len(names) > 1 else None,
            'outfitPluralName': names[2] if len(names) > 2 else None,
            'modType': mod_type,
            'modTypeLabel': MOD_TYPE_LABELS.get(mod_type, 'unknown'),
            'modValWeaponResourceId': mod_val,
            'semanticFields': fields,
            'rawWords0To8': words[:9],
            'sourceBasis': SOURCE_BASIS,
        }
        outfit_links.append(entry)
        outfit_links_by_weapon.setdefault(mod_val, []).append(entry)

    weapons = []
    for weapon_id, record in sorted(weapon_records_by_id.items()):
        words = _words(record)
        links = outfit_links_by_weapon.get(weapon_id, [])
        sale_link = next((link for link in links if link['modType'] == 1), None)
        ammo_links = [link for link in links if link['modType'] == 3]
        weapons.append({
            'resourceId': weapon_id,
            'sourceDataOrdinal': int(record['ordinal']),
            'chunkIndex': int(record['chunkIndex']),
            'byteOffset': int(record['byteOffset']),
            'size': int(record['size']),
            'displayName': sale_link['outfitDisplayName'] if sale_link else None,
            'outfitNames': [link['outfitDisplayName'] for link in links if link.get('outfitDisplayName')],
            'semanticFields': _named_fields(words, WEAP_FIELD_NAMES),
            'rawWords0To14': words[:15],
            'sourceBasis': SOURCE_BASIS,
            'sourceConfidence': 'field-layout-from-resource-bible; stock-name-map-from-oütf-ModType/ModVal; runtime combat timing still pending',
            'outfitLinks': links,
            'ammoOutfitLinks': ammo_links,
        })

    unresolved_outfit_links = [
        link for link in outfit_links
        if link['modValWeaponResourceId'] not in weapon_records_by_id
    ]

    return {
        'schemaVersion': 1,
        'sourceFile': structures['sourceFile'],
        'sourceSha256': structures['sourceSha256'],
        'method': METHOD,
        'sourceBasis': SOURCE_BASIS,
        'note': 'Derived from complete primitive records; preserves raw word indices and labels exact stock names only through oütf ModType/ModVal cross-links. Does not claim runtime fire cadence or combat behavior beyond Resource Bible field semantics.',
        'resourceIdAssumption': 'weapon-like run ordinal 0 corresponds to wëap resource ID 128, matching oütf ModVal references for stock weapons; unresolved oütf links are retained separately.',
        'weaponFieldOrder': WEAP_FIELD_NAMES,
        'outfitFieldOrder': OUTF_FIELD_NAMES,
        'weapons': weapons,
        'outfitWeaponLinks': outfit_links,
        'unresolvedOutfitWeaponLinks': unresolved_outfit_links,
    }


def main() -> None:
    structures = json.loads(STRUCTURES_PATH.read_text())
    manifest = derive_manifest(structures)
    OUT_PATH.write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'wrote {OUT_PATH} weapons={len(manifest["weapons"])} outfitLinks={len(manifest["outfitWeaponLinks"])} unresolved={len(manifest["unresolvedOutfitWeaponLinks"])}')


if __name__ == '__main__':
    main()
