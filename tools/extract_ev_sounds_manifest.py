#!/usr/bin/env python3
"""Catalog and decode supported EV Classic sound resources.

The manifest is provenance-first: every `snd ` resource is recorded with
resource-map identity and byte provenance. Supported classic Mac uncompressed
sampled-sound records are also decoded to WAV for local personal-use builds;
unsupported variants remain explicit decode errors with raw header bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import wave
from pathlib import Path


DEFAULT_SOURCE = Path('source-assets/ev-classic/Nova Files/EV Sounds.rez')
DEFAULT_OUTPUT = Path('native_ev/data/sourced_ev_sounds.json')
DEFAULT_ASSET_ROOT = Path('native_ev/assets/sounds/ev_classic')
METHOD = 'classic-mac-snd-wav-v2'


def slugify(value: str) -> str:
    value = value.lower().replace('ö', 'o').replace('ë', 'e').replace('ï', 'i')
    value = re.sub(r'[^a-z0-9]+', '_', value).strip('_')
    return value or 'sound'


def iter_chunks(data: bytes) -> list[tuple[int, int, int]]:
    chunks: list[tuple[int, int, int]] = []
    n = len(data)
    for pos in range(20, 10000, 12):
        if pos + 12 > n:
            break
        resource_id, offset, size = struct.unpack_from('<III', data, pos)
        if offset <= 0 or offset >= n or size <= 0 or offset + size > n:
            break
        chunks.append((resource_id, offset, size))
    return chunks


def _is_resource_type(raw: bytes) -> bool:
    if len(raw) != 4:
        return False
    # Classic Mac resource types are four printable-ish MacRoman bytes; allow the
    # trailing space in `snd `, reject NUL-heavy bogus section records.
    return all(32 <= b <= 255 for b in raw)


def iter_resource_map_entries(data: bytes, chunks: list[tuple[int, int, int]]) -> list[dict]:
    if not chunks:
        return []
    map_offset = chunks[-1][1]
    resources: list[dict] = []
    chunk_count = len(chunks)
    for section_index in range(32):
        record_offset = map_offset + 8 + section_index * 12
        if record_offset + 12 > len(data):
            break
        raw_type = data[record_offset:record_offset + 4]
        if not _is_resource_type(raw_type):
            break
        section_offset = int.from_bytes(data[record_offset + 4:record_offset + 8], 'big')
        count = int.from_bytes(data[record_offset + 8:record_offset + 12], 'big')
        table_start = map_offset + section_offset
        table_end = table_start + count * 266
        if section_offset <= 0 or count < 0 or table_end > len(data):
            break
        resource_type = raw_type.decode('macroman', 'replace')
        for resource_index in range(count):
            entry_offset = table_start + resource_index * 266
            chunk_index = int.from_bytes(data[entry_offset:entry_offset + 4], 'big')
            if chunk_index < 0 or chunk_index >= chunk_count:
                continue
            resource_id = int.from_bytes(data[entry_offset + 8:entry_offset + 10], 'big')
            name = data[entry_offset + 10:entry_offset + 266].split(b'\0', 1)[0].decode('macroman', 'replace').strip()
            resources.append({
                'type': resource_type,
                'resourceId': resource_id,
                'name': name,
                'chunkIndex': chunk_index,
                'resourceMapEntryOffset': entry_offset,
            })
    return resources


def _read_u16(raw: bytes, offset: int) -> int:
    return int.from_bytes(raw[offset:offset + 2], 'big')


def _read_u32(raw: bytes, offset: int) -> int:
    return int.from_bytes(raw[offset:offset + 4], 'big')


def parse_snd_sample(raw: bytes) -> dict:
    """Return decoded sampled-sound metadata and PCM bytes.

    Supported records observed in EV Sounds.rez are format 1 or 2 sound
    resources with one sampledSynth buffer command (`0x8051`), whose param2
    points to a standard uncompressed SoundHeader: samplePtr, length,
    unsigned-16.16 sampleRate, loopStart, loopEnd, encode=0, baseFrequency,
    followed immediately by 8-bit sample bytes. WAV PCM 8-bit is also unsigned,
    so the source sample payload can be copied directly.
    """
    if len(raw) < 22:
        raise ValueError('unsupported snd resource: too short')
    sound_format = _read_u16(raw, 0)
    commands: list[dict] = []
    if sound_format == 1:
        modifier_count = _read_u16(raw, 2)
        command_count_offset = 4 + modifier_count * 6
        if command_count_offset + 2 > len(raw):
            raise ValueError('unsupported snd format 1 command table')
        command_count = _read_u16(raw, command_count_offset)
        command_offset = command_count_offset + 2
    elif sound_format == 2:
        modifier_count = None
        command_count = _read_u16(raw, 4)
        command_offset = 6
    else:
        raise ValueError(f'unsupported snd format {sound_format}')
    if command_count != 1:
        raise ValueError(f'unsupported snd command count {command_count}')
    if command_offset + 8 > len(raw):
        raise ValueError('unsupported snd command table bounds')
    command = _read_u16(raw, command_offset)
    param1 = _read_u16(raw, command_offset + 2)
    param2 = _read_u32(raw, command_offset + 4)
    commands.append({'command': command, 'param1': param1, 'param2': param2})
    if command != 0x8051:
        raise ValueError(f'unsupported snd command 0x{command:04x}')
    header_offset = param2
    if header_offset + 22 > len(raw):
        raise ValueError('unsupported snd SoundHeader bounds')
    sample_pointer = _read_u32(raw, header_offset)
    sample_count = _read_u32(raw, header_offset + 4)
    sample_rate_fixed = _read_u32(raw, header_offset + 8)
    loop_start = _read_u32(raw, header_offset + 12)
    loop_end = _read_u32(raw, header_offset + 16)
    encode = raw[header_offset + 20]
    base_frequency = raw[header_offset + 21]
    data_offset = header_offset + 22
    data_end = data_offset + sample_count
    if sample_pointer != 0:
        raise ValueError('unsupported snd nonzero sample pointer')
    if encode != 0:
        raise ValueError(f'unsupported snd encoding {encode}')
    if data_end > len(raw):
        raise ValueError('unsupported snd sample data bounds')
    if data_end != len(raw):
        raise ValueError('unsupported snd trailing bytes after sample data')
    sample_rate = sample_rate_fixed / 65536.0
    return {
        'soundFormat': sound_format,
        'modifierCount': modifier_count,
        'commandCount': command_count,
        'commands': commands,
        'soundHeaderOffset': header_offset,
        'samplePointer': sample_pointer,
        'sampleCount': sample_count,
        'sampleRateFixed': sample_rate_fixed,
        'sampleRate': sample_rate,
        'sampleRateHz': round(sample_rate),
        'loopStart': loop_start,
        'loopEnd': loop_end,
        'encoding': encode,
        'baseFrequency': base_frequency,
        'sampleDataOffset': data_offset,
        'pcm8': raw[data_offset:data_end],
    }


def write_wav(path: Path, sample_rate_hz: int, pcm8: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(1)
        wav.setframerate(sample_rate_hz)
        wav.writeframes(pcm8)


def build_manifest(source: Path, asset_root: Path) -> dict:
    data = source.read_bytes()
    chunks = iter_chunks(data)
    resources = iter_resource_map_entries(data, chunks)
    snd_resources = [resource for resource in resources if resource['type'] == 'snd ']
    sound_assets: list[dict] = []
    for resource in snd_resources:
        _chunk_id, byte_offset, size = chunks[resource['chunkIndex']]
        raw = data[byte_offset:byte_offset + size]
        entry = {
            'type': resource['type'],
            'resourceId': resource['resourceId'],
            'name': resource['name'],
            'chunkIndex': resource['chunkIndex'],
            'byteOffset': byte_offset,
            'size': size,
            'rawHeaderBytes': list(raw[:32]),
        }
        try:
            decoded = parse_snd_sample(raw)
            slug = f"{resource['resourceId']}_{slugify(resource['name'] or 'snd')}"
            asset_file = asset_root / slug / 'sound.wav'
            write_wav(asset_file, decoded['sampleRateHz'], decoded.pop('pcm8'))
            entry.update({
                'status': 'ok',
                'assetFile': asset_file.as_posix().removeprefix('native_ev/'),
                'sound': decoded,
            })
        except ValueError as exc:
            entry.update({
                'status': f'decode-error: {exc}',
            })
        sound_assets.append(entry)
    sound_assets.sort(key=lambda item: item['resourceId'])
    ok_count = len([asset for asset in sound_assets if asset.get('status') == 'ok'])
    type_catalog = []
    for resource_type in sorted({resource['type'] for resource in resources}):
        items = [resource for resource in resources if resource['type'] == resource_type]
        type_catalog.append({
            'type': resource_type,
            'count': len(items),
            'decodeStatus': 'decoded-to-wav-with-explicit-errors' if resource_type == 'snd ' else 'catalog-only',
            'note': f'classic Mac sound resources cataloged; {ok_count} decoded to 8-bit mono WAV' if resource_type == 'snd ' else 'catalog-only',
        })
    return {
        'sourceFile': source.as_posix(),
        'sourceSha256': hashlib.sha256(data).hexdigest(),
        'method': METHOD,
        'note': 'Provenance-first catalog of classic Mac `snd ` resources from local EV Sounds.rez; supported uncompressed sampled-sound records decode to WAV.',
        'chunkCount': len(chunks),
        'resourceCount': len(resources),
        'resourceTypeCatalog': type_catalog,
        'soundAssets': sound_assets,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--asset-root', type=Path, default=DEFAULT_ASSET_ROOT)
    args = parser.parse_args()

    manifest = build_manifest(args.source, args.asset_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + '\n')
    ok_count = len([asset for asset in manifest['soundAssets'] if asset.get('status') == 'ok'])
    print(f"wrote {args.output} sounds={len(manifest['soundAssets'])} decoded={ok_count} chunks={manifest['chunkCount']}")


if __name__ == '__main__':
    main()
