#!/usr/bin/env python3
"""Experimental EV Classic rlëD decoder.

This is intentionally local/project tooling for authorized assets. The format is inferred
from the EV Classic TC resource data enough to extract preview PNGs for browser prototyping.
"""
from __future__ import annotations

import argparse
import json
import struct
import zlib
from pathlib import Path


def rgb555_to_rgba(word: int, alpha: int = 255) -> tuple[int, int, int, int]:
    # Classic Mac 16-bit color resources appear as RGB555-ish big-endian values.
    r = (word >> 10) & 0x1F
    g = (word >> 5) & 0x1F
    b = word & 0x1F
    return ((r << 3) | (r >> 2), (g << 3) | (g >> 2), (b << 3) | (b >> 2), alpha)


def iter_chunks(rez: bytes) -> list[tuple[int, int, int]]:
    chunks: list[tuple[int, int, int]] = []
    n = len(rez)
    for pos in range(20, 10000, 12):
        rid, off, size = struct.unpack_from('<III', rez, pos)
        if off <= 0 or off >= n or size <= 0 or off + size > n:
            break
        chunks.append((rid, off, size))
    return chunks


def iter_resources(rez: bytes, chunks: list[tuple[int, int, int]]) -> list[dict]:
    map_off = chunks[-1][1]
    resources: list[dict] = []
    for i in range(8):
        rec = map_off + 8 + i * 12
        typ = rez[rec:rec + 4]
        sec = int.from_bytes(rez[rec + 4:rec + 8], 'big')
        cnt = int.from_bytes(rez[rec + 8:rec + 12], 'big')
        for j in range(cnt):
            off = map_off + sec + j * 266
            idx = int.from_bytes(rez[off:off + 4], 'big')
            res_id = int.from_bytes(rez[off + 8:off + 10], 'big')
            name = rez[off + 10:off + 266].split(b'\0', 1)[0].decode('macroman', 'replace').strip()
            resources.append({
                'type': typ.decode('macroman', 'replace'),
                'chunk_index': idx,
                'res_id': res_id,
                'name': name,
            })
    return resources


def make_blank(width: int, height: int) -> bytearray:
    return bytearray(width * height * 4)


def set_px(buf: bytearray, width: int, x: int, y: int, rgba: tuple[int, int, int, int]) -> None:
    i = (y * width + x) * 4
    buf[i:i + 4] = bytes(rgba)


def write_png(path: Path, width: int, height: int, rgba: bytes | bytearray) -> None:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return len(payload).to_bytes(4, 'big') + kind + payload + zlib.crc32(kind + payload).to_bytes(4, 'big')

    scanlines = bytearray()
    row_bytes = width * 4
    for y in range(height):
        scanlines.append(0)  # no filter
        start = y * row_bytes
        scanlines.extend(rgba[start:start + row_bytes])
    ihdr = width.to_bytes(4, 'big') + height.to_bytes(4, 'big') + bytes([8, 6, 0, 0, 0])
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(bytes(scanlines), 9)) + chunk(b'IEND', b''))


def decode_rled(data: bytes, max_frames: int | None = None) -> tuple[int, int, list[bytearray]]:
    width = int.from_bytes(data[0:2], 'big')
    height = int.from_bytes(data[2:4], 'big')
    depth = int.from_bytes(data[4:6], 'big')
    frame_count = int.from_bytes(data[8:10], 'big')
    if not (0 < width <= 256 and 0 < height <= 256 and depth in (8, 16, 32) and 0 < frame_count <= 256):
        raise ValueError(f'unsupported rleD header width={width} height={height} depth={depth} frames={frame_count}')

    frames: list[bytearray] = []
    pos = 16
    wanted = min(frame_count, max_frames or frame_count)
    for _frame in range(wanted):
        img = make_blank(width, height)
        for y in range(height):
            if pos + 4 > len(data):
                break
            marker = data[pos]
            row_len = int.from_bytes(data[pos + 2:pos + 4], 'big')
            if marker == 0x00 and row_len == 0:
                pos += 4
                continue
            if marker != 0x01 or row_len < 0 or pos + 4 + row_len > len(data):
                return width, height, frames
            row = data[pos + 4:pos + 4 + row_len]
            pos += 4 + row_len
            x = 0
            rp = 0
            while rp + 4 <= len(row):
                cmd = row[rp]
                count = int.from_bytes(row[rp + 2:rp + 4], 'big')
                rp += 4
                if cmd in (0x01, 0x03):
                    # Counts in rlëD drawing commands are byte counts; 16-bit sprites use 2 bytes/pixel.
                    x += count // 2
                elif cmd == 0x02:
                    for _ in range(count // 2):
                        if rp + 2 > len(row):
                            break
                        word = int.from_bytes(row[rp:rp + 2], 'big')
                        rp += 2
                        if 0 <= x < width and word != 0:
                            set_px(img, width, x, y, rgb555_to_rgba(word))
                        x += 1
                else:
                    break
        frames.append(img)
    return width, height, frames


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('rez', type=Path)
    ap.add_argument('--out', type=Path, default=Path('source-assets/ev-classic/extracted/rled'))
    ap.add_argument('--resource-id', type=int, default=1000)
    ap.add_argument('--max-frames', type=int, default=36)
    args = ap.parse_args()

    rez = args.rez.read_bytes()
    chunks = iter_chunks(rez)
    resources = iter_resources(rez, chunks)
    target = next(r for r in resources if r['type'] == 'rlëD' and r['res_id'] == args.resource_id)
    _, off, size = chunks[target['chunk_index']]
    width, height, frames = decode_rled(rez[off:off + size], args.max_frames)

    safe_name = target['name'] or f'id{args.resource_id}'
    outdir = args.out / f"rled_{args.resource_id}_{safe_name.replace(' ', '_')}"
    outdir.mkdir(parents=True, exist_ok=True)
    for i, img in enumerate(frames):
        write_png(outdir / f'frame_{i:02d}.png', width, height, img)
    cols = min(6, len(frames)) or 1
    rows = (len(frames) + cols - 1) // cols
    contact = bytearray(cols * width * rows * height * 4)
    # opaque black background for visibility
    for i in range(0, len(contact), 4):
        contact[i:i + 4] = b'\x00\x00\x00\xff'
    contact_width = cols * width
    for fi, img in enumerate(frames):
        ox = (fi % cols) * width
        oy = (fi // cols) * height
        for y in range(height):
            for x in range(width):
                src = (y * width + x) * 4
                if img[src + 3]:
                    dst = ((oy + y) * contact_width + ox + x) * 4
                    contact[dst:dst + 4] = img[src:src + 4]
    write_png(outdir / 'contact.png', contact_width, rows * height, contact)
    (outdir / 'manifest.json').write_text(json.dumps({'resource': target, 'frames': len(frames), 'width': width, 'height': height}, indent=2))
    print(outdir)


if __name__ == '__main__':
    main()
