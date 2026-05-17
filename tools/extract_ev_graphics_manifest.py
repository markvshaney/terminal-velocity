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

from extract_ev_rled import decode_rled, iter_chunks, iter_resources, rgb555_to_rgba, write_png

DEFAULT_SOURCE = Path('source-assets/ev-classic/Nova Files/EV Graphics.rez')
DEFAULT_OUT = Path('native_ev/data/sourced_ev_graphics.json')
DEFAULT_SHIP_OUT = Path('native_ev/assets/ships/ev_classic')
DEFAULT_RLED_OUT = Path('native_ev/assets/graphics/rled')
DEFAULT_PICT_OUT = Path('native_ev/assets/graphics/pict')
METHOD = 'evnew-opcode-rled-shan-pict-v4'


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
    sentinel_record = width == 0x7fff and depth == 0xffff and frames == 0
    return {
        'width': width,
        'height': height,
        'depth': depth,
        'reservedWord3': reserved,
        'frameCount': frames,
        'headerBytes': list(raw[:16]),
        'decodeStatus': 'header-ok' if valid else ('non-sprite-record' if sentinel_record else 'unsupported-header'),
    }


def _unpack_word(raw: bytes, pos: int) -> tuple[int, int]:
    return int.from_bytes(raw[pos:pos + 2], 'big'), pos + 2


def _unpack_long(raw: bytes, pos: int) -> tuple[int, int]:
    return int.from_bytes(raw[pos:pos + 4], 'big'), pos + 4


def _unpack_rect(raw: bytes, pos: int) -> tuple[tuple[int, int, int, int], int]:
    top, left, bottom, right = struct.unpack_from('>hhhh', raw, pos)
    return (top, left, bottom, right), pos + 8


def _packbits_decode(raw: bytes, expected: int) -> tuple[bytes, int]:
    out = bytearray()
    pos = 0
    while len(out) < expected and pos < len(raw):
        n = struct.unpack('b', raw[pos:pos + 1])[0]
        pos += 1
        if 0 <= n <= 127:
            count = n + 1
            out.extend(raw[pos:pos + count])
            pos += count
        elif -127 <= n <= -1:
            count = 1 - n
            if pos >= len(raw):
                break
            out.extend(raw[pos:pos + 1] * count)
            pos += 1
    return bytes(out[:expected]), pos


def _decode_color_table(raw: bytes, pos: int) -> tuple[list[tuple[int, int, int]], int, dict]:
    seed, pos = _unpack_long(raw, pos)
    flags, pos = _unpack_word(raw, pos)
    ct_size, pos = _unpack_word(raw, pos)
    colors: dict[int, tuple[int, int, int]] = {}
    for _ in range(ct_size + 1):
        value, pos = _unpack_word(raw, pos)
        red, pos = _unpack_word(raw, pos)
        green, pos = _unpack_word(raw, pos)
        blue, pos = _unpack_word(raw, pos)
        colors[value] = (red >> 8, green >> 8, blue >> 8)
    palette = [colors.get(i, (0, 0, 0)) for i in range(max(colors.keys(), default=-1) + 1)]
    return palette, pos, {'seed': seed, 'flags': flags, 'ctSize': ct_size}


def _decode_indexed_pixmap_pict(raw: bytes) -> tuple[int, int, bytearray, dict] | None:
    # PICT 9507 / Trugati Asteroid Belt is stored as a compact uncompressed
    # indexed PixMap plus color table, without the PackBits PICT opcode used by
    # the other decoded EV Classic PICT resources.
    for pixmap_pos in range(0, min(128, len(raw) - 64), 2):
        row_word = int.from_bytes(raw[pixmap_pos:pixmap_pos + 2], 'big')
        if not (row_word & 0x8000):
            continue
        row_bytes = row_word & 0x3fff
        if row_bytes <= 0:
            continue
        try:
            bounds, pos = _unpack_rect(raw, pixmap_pos + 2)
            top, left, bottom, right = bounds
            width = right - left
            height = bottom - top
            if width <= 0 or height <= 0:
                continue
            pm_version, pos = _unpack_word(raw, pos)
            pack_type, pos = _unpack_word(raw, pos)
            pack_size, pos = _unpack_long(raw, pos)
            h_res, pos = _unpack_long(raw, pos)
            v_res, pos = _unpack_long(raw, pos)
            pixel_type, pos = _unpack_word(raw, pos)
            pixel_size, pos = _unpack_word(raw, pos)
            cmp_count, pos = _unpack_word(raw, pos)
            cmp_size, pos = _unpack_word(raw, pos)
            plane_bytes, pos = _unpack_long(raw, pos)
            pm_table, pos = _unpack_long(raw, pos)
            pm_reserved, pos = _unpack_long(raw, pos)
        except struct.error:
            continue
        if pixel_size not in (1, 2, 4, 8) or cmp_count != 1 or cmp_size != pixel_size:
            continue
        data_bytes = row_bytes * height
        table_pos = pos + data_bytes
        if table_pos + 8 > len(raw):
            continue
        try:
            palette, end_pos, color_table = _decode_color_table(raw, table_pos)
        except (struct.error, ValueError):
            continue
        if not palette or end_pos > len(raw):
            continue
        rgba = bytearray(width * height * 4)
        pixels_per_byte = 8 // pixel_size
        mask = (1 << pixel_size) - 1
        for y in range(height):
            row = raw[pos + y * row_bytes:pos + (y + 1) * row_bytes]
            for x in range(width):
                packed = row[x // pixels_per_byte]
                shift = (pixels_per_byte - 1 - (x % pixels_per_byte)) * pixel_size
                index = (packed >> shift) & mask
                red, green, blue = palette[index] if index < len(palette) else (0, 0, 0)
                out_pos = (y * width + x) * 4
                rgba[out_pos:out_pos + 4] = bytes((red, green, blue, 255))
        return width, height, rgba, {
            'format': 'uncompressed-indexed-pixmap-with-color-table',
            'pixmapOffset': pixmap_pos,
            'rowBytes': row_bytes,
            'bounds': {'top': top, 'left': left, 'bottom': bottom, 'right': right},
            'pmVersion': pm_version,
            'packType': pack_type,
            'packSize': pack_size,
            'hRes': h_res,
            'vRes': v_res,
            'pixelType': pixel_type,
            'pixelSize': pixel_size,
            'cmpCount': cmp_count,
            'cmpSize': cmp_size,
            'planeBytes': plane_bytes,
            'pmTable': pm_table,
            'pmReserved': pm_reserved,
            'colorTable': color_table,
        }
    return None


def decode_pict(raw: bytes) -> tuple[int, int, bytearray, dict]:
    pos = None
    opcode = None
    for candidate in range(10, min(128, len(raw) - 2), 2):
        op = int.from_bytes(raw[candidate:candidate + 2], 'big')
        if op in (0x0098, 0x0099, 0x009a, 0x009b):
            opcode = op
            pos = candidate + 2
            break
    if pos is None or opcode is None:
        indexed = _decode_indexed_pixmap_pict(raw)
        if indexed is not None:
            return indexed
        raise ValueError('no supported PackBits PICT opcode or indexed PixMap found')
    _base_addr, pos = _unpack_long(raw, pos)
    row_word, pos = _unpack_word(raw, pos)
    row_bytes = row_word & 0x3fff
    bounds, pos = _unpack_rect(raw, pos)
    top, left, bottom, right = bounds
    width = right - left
    height = bottom - top
    if width <= 0 or height <= 0 or row_bytes <= 0:
        raise ValueError(f'invalid PICT bounds={bounds} rowBytes={row_bytes}')
    pm_version, pos = _unpack_word(raw, pos)
    pack_type, pos = _unpack_word(raw, pos)
    pack_size, pos = _unpack_long(raw, pos)
    h_res, pos = _unpack_long(raw, pos)
    v_res, pos = _unpack_long(raw, pos)
    pixel_type, pos = _unpack_word(raw, pos)
    pixel_size, pos = _unpack_word(raw, pos)
    cmp_count, pos = _unpack_word(raw, pos)
    cmp_size, pos = _unpack_word(raw, pos)
    plane_bytes, pos = _unpack_long(raw, pos)
    pm_table, pos = _unpack_long(raw, pos)
    pm_reserved, pos = _unpack_long(raw, pos)
    src_rect, pos = _unpack_rect(raw, pos)
    dst_rect, pos = _unpack_rect(raw, pos)
    mode, pos = _unpack_word(raw, pos)
    if opcode in (0x0099, 0x009b):
        region_size, pos = _unpack_word(raw, pos)
        pos += max(0, region_size - 2)
    if pixel_size not in (16, 32):
        raise ValueError(f'unsupported PICT pixel size {pixel_size}')
    rows = []
    for _y in range(height):
        if row_bytes > 250:
            row_size, pos = _unpack_word(raw, pos)
        else:
            row_size = raw[pos]
            pos += 1
        if pos + row_size > len(raw):
            raise ValueError('early end in PICT row data')
        row, _used = _packbits_decode(raw[pos:pos + row_size], row_bytes)
        pos += row_size
        rows.append(row + b'\x00' * max(0, row_bytes - len(row)))
    rgba = bytearray(width * height * 4)
    for y, row in enumerate(rows):
        for x in range(width):
            if pixel_size == 32:
                _pad, red, green, blue = row[x * 4:x * 4 + 4]
            else:
                word = int.from_bytes(row[x * 2:x * 2 + 2], 'big')
                red, green, blue, _alpha = rgb555_to_rgba(word)
            out_pos = (y * width + x) * 4
            rgba[out_pos:out_pos + 4] = bytes((red, green, blue, 255))
    return width, height, rgba, {
        'opcode': f'0x{opcode:04x}',
        'rowBytes': row_bytes,
        'bounds': {'top': top, 'left': left, 'bottom': bottom, 'right': right},
        'pmVersion': pm_version,
        'packType': pack_type,
        'packSize': pack_size,
        'hRes': h_res,
        'vRes': v_res,
        'pixelType': pixel_type,
        'pixelSize': pixel_size,
        'cmpCount': cmp_count,
        'cmpSize': cmp_size,
        'planeBytes': plane_bytes,
        'pmTable': pm_table,
        'pmReserved': pm_reserved,
        'srcRect': {'top': src_rect[0], 'left': src_rect[1], 'bottom': src_rect[2], 'right': src_rect[3]},
        'dstRect': {'top': dst_rect[0], 'left': dst_rect[1], 'bottom': dst_rect[2], 'right': dst_rect[3]},
        'mode': mode,
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
            header = rled_header(raw)
            if header.get('decodeStatus') == 'non-sprite-record':
                status = 'non-sprite-record'
                note = 'rlëD resource-map entry contains sentinel-like non-image record bytes, not a normal sprite stream'
            else:
                status = f'decode-error: {exc}'
                note = None
            entry = {
                'type': resource['type'],
                'resourceId': resource['res_id'],
                'name': resource['name'],
                'chunkIndex': resource['chunk_index'],
                'byteOffset': off,
                'size': size,
                'rled': header,
                'rawWords': words(raw),
                'status': status,
            }
            if note:
                entry['note'] = note
            extracted.append(entry)
    return extracted


def extract_pict_assets(rez: bytes, chunks: list[tuple[int, int, int]], resources: list[dict], out_root: Path) -> list[dict]:
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    extracted = []
    used_slugs: set[str] = set()
    for resource in [r for r in resources if r['type'] == 'PICT']:
        _, off, size = chunks[resource['chunk_index']]
        raw = rez[off:off + size]
        slug = f"{resource['res_id']}_{slugify(resource['name'] or 'pict')}"
        if slug in used_slugs:
            slug = f"{slug}_{resource['chunk_index']}"
        used_slugs.add(slug)
        outdir = out_root / slug
        try:
            width, height, rgba, pict = decode_pict(raw)
            outdir.mkdir(parents=True, exist_ok=True)
            png_path = outdir / 'image.png'
            write_png(png_path, width, height, rgba)
            extracted.append({
                'type': resource['type'],
                'resourceId': resource['res_id'],
                'name': resource['name'],
                'chunkIndex': resource['chunk_index'],
                'byteOffset': off,
                'size': size,
                'width': width,
                'height': height,
                'assetFile': relative_asset_dir(png_path),
                'pict': pict,
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


def resource_type_catalog(resources: list[dict], extract_rled: bool, extract_pict: bool, extract_sprites: bool) -> list[dict]:
    counts: dict[str, int] = {}
    for resource in resources:
        counts[resource['type']] = counts.get(resource['type'], 0) + 1
    notes = {
        'PICT': 'direct-color PackBits PICT raster resources; includes target, shipyard, outfit, and large backdrop images where supported',
        'rlëD': 'EV/Nova opcode RLE sprite resources; includes weapons, explosions, cargo boxes, stars, asteroids, ships, planets, stations, and main-screen orbs',
        'shän': 'ship animation metadata decoded into word fields and joined to rlëD ship sprites',
        'spïn': 'spin metadata records cataloged; referenced visual frames are in rlëD sprite resources',
        'cicn': 'classic Mac color icon resources cataloged; PNG decoder not implemented yet',
        'ppat': 'classic Mac pixel-pattern resources cataloged; PNG decoder not implemented yet',
        'bööm': 'explosion behavior metadata cataloged; referenced visual frames are in rlëD sprite resources',
        'röid': 'asteroid behavior metadata cataloged; referenced visual frames are in rlëD sprite resources',
    }
    status = {
        'PICT': 'decoded-to-png' if extract_pict else 'catalog-only',
        'rlëD': 'decoded-to-png' if extract_rled else 'catalog-only',
        'shän': 'decoded-metadata-and-ship-pngs' if extract_sprites else 'decoded-metadata-only',
        'spïn': 'catalog-only',
        'cicn': 'catalog-only-unsupported-raster',
        'ppat': 'catalog-only-unsupported-raster',
        'bööm': 'catalog-only',
        'röid': 'catalog-only',
    }
    return [
        {'type': resource_type, 'count': counts[resource_type], 'decodeStatus': status.get(resource_type, 'catalog-only'), 'note': notes.get(resource_type, '')}
        for resource_type in sorted(counts)
    ]


def build_manifest(source: Path, extract_sprites: bool, ship_out: Path, extract_rled: bool, rled_out: Path, extract_pict: bool, pict_out: Path) -> dict:
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
    pict_assets = extract_pict_assets(rez, chunks, resources, pict_out) if extract_pict else []
    return {
        'sourceFile': str(source),
        'sourceSha256': hashlib.sha256(rez).hexdigest(),
        'method': METHOD,
        'note': 'Full resource-map manifest plus rlëD headers, decoded rlëD PNG assets, decoded supported PICT PNG assets, and shän word-field decode. Extracted PNGs are local personal-use assets.',
        'chunkCount': len(chunks),
        'resourceCount': len(resources),
        'resourceTypeCatalog': resource_type_catalog(resources, extract_rled, extract_pict, extract_sprites),
        'resources': decoded_resources,
        'rledAssets': rled_assets,
        'pictAssets': pict_assets,
        'shipSprites': ship_sprites,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('source', nargs='?', type=Path, default=DEFAULT_SOURCE)
    ap.add_argument('--out', type=Path, default=DEFAULT_OUT)
    ap.add_argument('--ship-out', type=Path, default=DEFAULT_SHIP_OUT)
    ap.add_argument('--rled-out', type=Path, default=DEFAULT_RLED_OUT)
    ap.add_argument('--pict-out', type=Path, default=DEFAULT_PICT_OUT)
    ap.add_argument('--extract-ship-sprites', action='store_true')
    ap.add_argument('--extract-rled-assets', action='store_true')
    ap.add_argument('--extract-pict-assets', action='store_true')
    args = ap.parse_args()
    manifest = build_manifest(args.source, args.extract_ship_sprites, args.ship_out, args.extract_rled_assets, args.rled_out, args.extract_pict_assets, args.pict_out)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    ok = sum(1 for s in manifest['shipSprites'] if s.get('status') == 'ok')
    rled_ok = sum(1 for s in manifest['rledAssets'] if s.get('status') == 'ok')
    pict_ok = sum(1 for s in manifest['pictAssets'] if s.get('status') == 'ok')
    print(f"wrote {args.out} resources={manifest['resourceCount']} shipSprites={ok} rledAssets={rled_ok} pictAssets={pict_ok}")


if __name__ == '__main__':
    main()
