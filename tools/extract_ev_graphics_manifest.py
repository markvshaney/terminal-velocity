#!/usr/bin/env python3
"""Decode EV Graphics.rez resource and sprite metadata for local personal-use builds.

The manifest is provenance-first: it records every resource map entry and decodes
rlëD / shän primitive fields. Optionally extracts every ship sprite referenced by
shän records into native_ev/assets/ships/ev_classic/<slug>/frame_XX.png.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import struct
from pathlib import Path

from extract_ev_rled import decode_rled, iter_chunks, iter_resources, write_png

DEFAULT_SOURCE = Path('source-assets/ev-classic/Nova Files/EV Graphics.rez')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_graphics.json')
DEFAULT_SHIP_OUT = Path('native_ev/assets/ships/ev_classic')
DEFAULT_RLED_OUT = Path('native_ev/assets/graphics/rled')
METHOD = 'brgr-graphics-rled-shan-full-field-v1'


def slugify(text: str) -> str:
    text = text.lower().replace('ö', 'o').replace('ë', 'e').replace('ï', 'i')
    text = re.sub(r'[^a-z0-9]+', '_', text).strip('_')
    return text or 'unnamed'


def words(raw: bytes) -> list[int]:
    return list(struct.unpack('>' + 'h' * (len(raw) // 2), raw[:len(raw) // 2 * 2]))


def fields(raw: bytes) -> list[dict]:
    return [
        {'name': f'word_{i:03d}', 'wordIndex': i, 'byteOffsetInRecord': i * 2, 'value': value}
        for i, value in enumerate(words(raw))
    ]


def rled_header(raw: bytes) -> dict:
    if len(raw) < 16:
        return {'decodeStatus': 'too-short'}
    width = int.from_bytes(raw[0:2], 'big')
    height = int.from_bytes(raw[2:4], 'big')
    depth = int.from_bytes(raw[4:6], 'big')
    reserved = int.from_bytes(raw[6:8], 'big')
    frames = int.from_bytes(raw[8:10], 'big')
    valid = 0 < width <= 512 and 0 < height <= 512 and depth in (8, 16, 32) and 0 < frames <= 256
    return {
        'width': width,
        'height': height,
        'depth': depth,
        'reservedWord3': reserved,
        'frameCount': frames,
        'headerBytes': list(raw[:16]),
        'decodeStatus': 'header-ok' if valid else 'unsupported-header',
    }


def decode_shan(resource: dict, raw: bytes) -> dict:
    ws = words(raw)
    # EV Classic shän records store sprite references offset by +2 relative to rlëD IDs
    # in this BRGR dump: Shuttle has word_000=1002 while the matching 48x48/36-frame
    # rlëD is 1000. Keep both values so the inference is auditable.
    inferred_rled = ws[0] - 2 if ws else None
    return {
        'resourceId': resource['res_id'],
        'name': resource['name'],
        'chunkIndex': resource['chunk_index'],
        'size': len(raw),
        'fieldEncoding': 'big-endian signed 16-bit words',
        'fieldCount': len(ws),
        'fieldsComplete': True,
        'fields': fields(raw),
        'semanticFields': {
            'rawBaseSpriteWord': ws[0] if len(ws) > 0 else None,
            'rawMaskSpriteWord': ws[1] if len(ws) > 1 else None,
            'inferredRledResourceId': inferred_rled,
            'inferredMaskResourceId': (ws[1] - 2) if len(ws) > 1 else None,
            'displayWidth': ws[3] if len(ws) > 3 else None,
            'displayHeight': ws[4] if len(ws) > 4 else None,
            'facings': ws[26] if len(ws) > 26 else None,
        },
    }


def relative_asset_dir(path: Path) -> str:
    try:
        return str(path.relative_to(Path('native_ev')))
    except ValueError:
        return str(path)


def extract_rled_assets(rez: bytes, chunks: list[tuple[int, int, int]], resources: list[dict], out_root: Path) -> list[dict]:
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    extracted = []
    used_slugs: set[str] = set()
    for resource in [r for r in resources if r['type'] == 'rlëD']:
        _, off, size = chunks[resource['chunk_index']]
        raw = rez[off:off + size]
        slug = slugify(resource['name'] or f"rled_{resource['res_id']}")
        slug = f"{resource['res_id']}_{slug}"
        if slug in used_slugs:
            slug = f"{slug}_{resource['chunk_index']}"
        used_slugs.add(slug)
        outdir = out_root / slug
        try:
            width, height, frames_rgba = decode_rled(raw, None)
            outdir.mkdir(parents=True, exist_ok=True)
            for i, img in enumerate(frames_rgba):
                write_png(outdir / f'frame_{i:02d}.png', width, height, img)
            extracted.append({
                'type': resource['type'],
                'resourceId': resource['res_id'],
                'name': resource['name'],
                'chunkIndex': resource['chunk_index'],
                'byteOffset': off,
                'size': size,
                'width': width,
                'height': height,
                'frames': len(frames_rgba),
                'assetDir': relative_asset_dir(outdir),
                'status': 'ok',
            })
        except Exception as exc:
            extracted.append({
                'type': resource['type'],
                'resourceId': resource['res_id'],
                'name': resource['name'],
                'chunkIndex': resource['chunk_index'],
                'byteOffset': off,
                'size': size,
                'status': f'decode-error: {exc}',
            })
    return extracted


def extract_ship_frames(rez: bytes, chunks: list[tuple[int, int, int]], resources: list[dict], shan_entries: list[dict], out_root: Path) -> list[dict]:
    by_type_id = {(r['type'], r['res_id']): r for r in resources}
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    extracted = []
    used_slugs: set[str] = set()
    for shan in shan_entries:
        sem = shan['semanticFields']
        rid = sem.get('inferredRledResourceId')
        rled = by_type_id.get(('rlëD', rid))
        if not rled:
            extracted.append({**sem, 'shipName': shan['name'], 'status': 'missing-rled'})
            continue
        _, off, size = chunks[rled['chunk_index']]
        try:
            width, height, frames_rgba = decode_rled(rez[off:off + size], None)
        except Exception as exc:  # keep provenance instead of aborting whole extraction
            extracted.append({**sem, 'shipName': shan['name'], 'status': f'decode-error: {exc}'})
            continue
        slug = slugify(shan['name'])
        if slug in used_slugs:
            slug = f"{slug}_{shan['resourceId']}"
        used_slugs.add(slug)
        outdir = out_root / slug
        outdir.mkdir(parents=True, exist_ok=True)
        frame_paths = []
        for i, img in enumerate(frames_rgba):
            rel = outdir / f'frame_{i:02d}.png'
            write_png(rel, width, height, img)
            frame_paths.append(str(rel))
        asset_dir = relative_asset_dir(outdir)
        extracted.append({
            'shipResourceId': shan['resourceId'],
            'shipName': shan['name'],
            'slug': slug,
            'rledResourceId': rid,
            'rledChunkIndex': rled['chunk_index'],
            'rledByteOffset': off,
            'rledSize': size,
            'width': width,
            'height': height,
            'frames': len(frames_rgba),
            'assetDir': asset_dir,
            'status': 'ok',
        })
    return extracted


def build_manifest(source: Path, extract_sprites: bool, ship_out: Path, extract_rled: bool, rled_out: Path) -> dict:
    rez = source.read_bytes()
    chunks = iter_chunks(rez)
    resources = iter_resources(rez, chunks)
    decoded_resources = []
    shan_entries = []
    for r in resources:
        _, off, size = chunks[r['chunk_index']]
        raw = rez[off:off + size]
        entry = {
            'type': r['type'],
            'resourceId': r['res_id'],
            'name': r['name'],
            'chunkIndex': r['chunk_index'],
            'byteOffset': off,
            'size': size,
        }
        if r['type'] == 'rlëD':
            entry['rled'] = rled_header(raw)
        elif r['type'] == 'shän':
            entry['shan'] = decode_shan(r, raw)
            shan_entries.append(entry['shan'])
        decoded_resources.append(entry)
    ship_sprites = extract_ship_frames(rez, chunks, resources, shan_entries, ship_out) if extract_sprites else []
    rled_assets = extract_rled_assets(rez, chunks, resources, rled_out) if extract_rled else []
    return {
        'sourceFile': str(source),
        'sourceSha256': hashlib.sha256(rez).hexdigest(),
        'method': METHOD,
        'note': 'Full resource-map manifest plus rlëD headers, decoded rlëD PNG assets, and shän word-field decode. Extracted PNGs are local personal-use assets.',
        'chunkCount': len(chunks),
        'resourceCount': len(resources),
        'resources': decoded_resources,
        'rledAssets': rled_assets,
        'shipSprites': ship_sprites,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('source', nargs='?', type=Path, default=DEFAULT_SOURCE)
    ap.add_argument('--out', type=Path, default=DEFAULT_OUT)
    ap.add_argument('--ship-out', type=Path, default=DEFAULT_SHIP_OUT)
    ap.add_argument('--rled-out', type=Path, default=DEFAULT_RLED_OUT)
    ap.add_argument('--extract-ship-sprites', action='store_true')
    ap.add_argument('--extract-rled-assets', action='store_true')
    args = ap.parse_args()
    manifest = build_manifest(args.source, args.extract_ship_sprites, args.ship_out, args.extract_rled_assets, args.rled_out)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    ok = sum(1 for s in manifest['shipSprites'] if s.get('status') == 'ok')
    rled_ok = sum(1 for s in manifest['rledAssets'] if s.get('status') == 'ok')
    print(f"wrote {args.out} resources={manifest['resourceCount']} shipSprites={ok} rledAssets={rled_ok}")


if __name__ == '__main__':
    main()
