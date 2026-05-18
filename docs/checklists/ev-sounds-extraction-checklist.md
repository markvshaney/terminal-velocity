# EV Sounds Extraction Follow-up Checklist

Purpose: track source-backed extraction and runtime integration of EV Classic sound resources from the local `EV Sounds.rez`, without committing proprietary source files or guessing unsupported formats.

## Source catalog and decode

- [x] Catalog `snd ` resources from `EV Sounds.rez`.
  - Current status: `native_ev/data/sourced_ev_sounds.json` records 57 `snd ` resources from `source-assets/ev-classic/Nova Files/EV Sounds.rez` using method `classic-mac-snd-wav-v2`.
  - Finding: the local sound source has SHA-256 `36fc306b41bb384e07ea78fe78ede115d02695f9eb01e6b8189b3a1280261f0e`, 58 BRGR chunks, and 57 cataloged sound resources with provenance fields and raw header bytes preserved.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_sounds_manifest_decodes_classic_mac_snd_resources` asserts manifest provenance, count, status, and representative resources including Warp Up, Laser, Engine, and Transition.

- [x] Decode supported classic Mac `snd ` resources to WAV.
  - Current status: 56 of 57 `snd ` records decoded to 8-bit mono WAV under `native_ev/assets/sounds/ev_classic/`; resource `30003` / `Transition` remains explicit `decode-error: unsupported snd format 0`.
  - Finding: supported records are classic Mac format 1 or 2 sound resources with a single sampledSynth buffer command (`0x8051`) pointing to an uncompressed SoundHeader (`encode=0`, `baseFrequency=60`) followed by 8-bit sample bytes. WAV 8-bit PCM is also unsigned, so the sample payload is copied directly with the source 16.16 sample rate rounded to 11127 Hz.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_sounds_manifest_decodes_classic_mac_snd_resources` asserts decoded count, representative SoundHeader metadata, a valid Laser WAV header, and the explicit Transition decode error.

- [x] Add representative decoded sound tests.
  - Current status: unit coverage verifies decoded WAV headers, sample rate/sample count where source-backed, and explicit unsupported classifications.

## Runtime integration not yet done

- [ ] Add a sound manifest consumed by runtime systems.
  - Candidate mappings: `Laser`, `Torp`, `Missile`, `Cannon`, `Engine`, `Warp Up`, `Warp Out`, `HeavyExplosion`, `MedExplosion`, `ShipExplodes`, UI `Beep*`, and `Click`.

- [ ] Wire Godot playback for the smallest useful sound surface.
  - Recommended first runtime consumer: UI/shipyard/mission `Click` or weapon `Laser`, because they are easy to trigger and verify.

- [ ] Extend Godot self-test for sound asset loading.
  - Done condition: self-test loads the committed sound manifest and at least one decoded audio stream once decoding exists.

- [ ] Sync integrated sound asset directories to the Windows runtime copy.
  - Target: `C:\Users\bh\Games\TerminalVelocity`.

## Verification commands for the next pass

```bash
python3 tools/extract_ev_sounds_manifest.py
python3 -m unittest native_ev.tests.test_model
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\bh\Games\TerminalVelocity\godot_ev\windows\RunGodot.ps1" -SelfTest
git status --short --branch
```

## Guardrails

- Do not commit proprietary source `.rez` files.
- Keep generated sound manifests provenance-first: source path, source SHA-256, resource ID, type, chunk index, byte offset, size, and decode status.
- Record unsupported or uncertain sound formats as catalog-only or decode-error; do not synthesize labels or silently drop resources.
- Commit only to `markvshaney/terminal-velocity` unless explicitly told otherwise.
