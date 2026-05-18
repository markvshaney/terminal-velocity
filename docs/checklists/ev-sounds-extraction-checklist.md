# EV Sounds Extraction Follow-up Checklist

Purpose: track source-backed extraction and runtime integration of EV Classic sound resources from the local `EV Sounds.rez`, without committing proprietary source files or guessing unsupported formats.

## Source catalog and decode

- [x] Catalog `snd ` resources from `EV Sounds.rez`.
  - Current status: `native_ev/data/sourced_ev_sounds.json` records 57 `snd ` resources from `source-assets/ev-classic/Nova Files/EV Sounds.rez` using method `classic-mac-snd-catalog-v1`.
  - Finding: the local sound source has SHA-256 `36fc306b41bb384e07ea78fe78ede115d02695f9eb01e6b8189b3a1280261f0e`, 58 BRGR chunks, and 57 cataloged sound resources with provenance fields and raw header bytes preserved. Audio decoding remains deliberately deferred.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_sounds_manifest_catalogs_classic_mac_snd_resources` asserts manifest provenance, count, catalog-only status, and representative resources including Warp Up, Laser, Engine, and Transition.

- [ ] Decode supported classic Mac `snd ` resources to WAV.
  - Why it remains open: the raw records show at least two `snd ` header variants; decoding should inspect each structure before assuming one PCM layout.
  - Next local step: implement a bounded parser for standard sampled-sound command records and preserve unsupported variants as explicit decode errors.

- [ ] Add representative decoded sound tests.
  - Done condition: tests verify decoded WAV headers, sample rate/sample count where source-backed, and explicit unsupported classifications.

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
