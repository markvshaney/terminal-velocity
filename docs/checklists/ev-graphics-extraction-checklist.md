# EV Graphics Extraction Follow-up Checklist

Purpose: track the things I was **not yet able to finish** in the last graphics extraction pass, so we can continue from a concrete backlog instead of re-discovering them.

## Decode gaps left open

- [x] Investigate `rlëD` resource `4004` / `Large Explosion`.
  - Current status: `non-sprite-record` in `native_ev/data/sourced_ev_graphics.json`.
  - Finding: the resource-map entry is typed `rlëD`, but the 40-byte payload has sentinel-like non-image words beginning `[32767, 40, -1]`, not a normal rlëD sprite header/stream. It closely resembles nearby fixed-field metadata records rather than drawable sprite data.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_graphics_manifest_decodes_resources_and_ship_sprites` asserts this classification and raw-word prefix.

- [x] Investigate `PICT` resource `9507` / `Trugati Asteroid Belt`.
  - Current status: decoded to PNG in `native_ev/assets/graphics/pict/9507_trugati_asteroid_belt/image.png`.
  - Finding: unlike the other decoded PICT resources, this 686-byte record does not contain the supported PackBits opcodes; it contains a compact uncompressed indexed PixMap at byte offset 32 (`rowBytes=16`, `bounds=32x32`, `pixelSize=4`) followed by a color table at byte offset 590 (`ctSize=10`).
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_graphics_manifest_decodes_resources_and_ship_sprites` asserts the decoded dimensions, PixMap offset, pixel size, and color-table size.

- [x] Decode or explicitly defer `cicn` resources.
  - Current status: 28 classic Mac color icon resources decoded to PNG under `native_ev/assets/graphics/cicn/`; resource `20000` remains an explicit `decode-error: unsupported cicn PixMap header` with raw header bytes preserved in the manifest.
  - Finding: the supported records use a classic `cicn` layout: PixMap header, mask BitMap, icon BitMap, mask/bitmap payloads, 4-byte pad, ColorTable, then indexed pixel data. Decoded cases cover 1-, 2-, 4-, and 8-bit indexed PixMaps with mask-derived alpha.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_graphics_manifest_decodes_resources_and_ship_sprites` asserts decoded `cicn` count, representative 1-bit/8-bit dimensions and metadata, and the explicit unsupported `20000` status.

- [x] Decode or explicitly defer `ppat` resources.
  - Current status: 9 classic Mac pixel-pattern resources decoded to PNG under `native_ev/assets/graphics/ppat/`; resource `137` remains an explicit `decode-error: unsupported ppat PixPat/PixMap layout` with raw header bytes preserved in the manifest.
  - Finding: resources `128`–`136` use a compact indexed PixPat/PixMap layout matching the uncompressed indexed PixMap+ColorTable form already observed in PICT `9507`: PixMap at byte offset 32, `32x32`, `rowBytes=16`, `pixelSize=4`, with a color table. Resource `133` uses `ctSize=9`; the others use `ctSize=10`.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_graphics_manifest_decodes_resources_and_ship_sprites` asserts decoded `ppat` count, representative metadata, and explicit unsupported `137` status.

## Deferred metadata semantics to decode later

- [ ] Interpret `spïn` spin metadata records beyond cataloging.
  - Current status: 58 `spïn` records cataloged only.
  - Deferred/later rationale: this likely controls spin/animation metadata, but it is less immediately runtime-visible than wiring already-decoded PICT assets into Godot.
  - Why it remains open: the visual frames are largely in `rlëD`, but `spïn` has not been semantically decoded.
  - Later local step: decode all 16-bit fields and correlate with `rlëD` IDs for planets, stations, asteroids, stars, and main-screen orbs.

- [ ] Interpret `bööm` records beyond cataloging.
  - Current status: 5 `bööm` records cataloged only.
  - Why it remains open: explosion visual frames are mostly `rlëD`, but behavior/animation semantics were not decoded.
  - Next local step: decode primitive fields and crosswalk to explosion `rlëD` resources.

- [ ] Interpret `röid` records beyond cataloging.
  - Current status: 2 `röid` records cataloged only.
  - Why it remains open: asteroid visual frames are in `rlëD`, but asteroid behavior/variant metadata was not decoded.
  - Next local step: decode primitive fields and crosswalk to asteroid `rlëD` resources.

## Runtime integration not yet done

- [ ] Choose the first Godot consumer for decoded PICT assets.
  - Candidate: shipyard artwork from `native_ev/assets/graphics/pict/5000_shipyard/` and related `500x` resources.
  - Candidate: outfit artwork from `native_ev/assets/graphics/pict/6000_outfit/` and related `600x` resources.
  - Candidate: target pictures from `native_ev/assets/graphics/pict/3000_target_pics/` and related `300x` resources.
  - Candidate: backdrop/nebula image from `native_ev/assets/graphics/pict/9500_serpens_nebula/`.

- [ ] Add runtime manifest fields or lookup tables for chosen PICT consumers.
  - Why it remains open: extraction is present, but the game runtime does not yet consume these new PICT PNGs.
  - Next local step: design the smallest manifest shape that maps Data identities to extracted PICT asset paths.

- [ ] Add Godot-side loading and smoke assertions for any newly consumed PICT assets.
  - Why it remains open: Godot self-test still verifies systems/ships/Argosy frames, not the new PICT asset families.
  - Next local step: extend `godot_ev/scripts/self_test.gd` after adding runtime asset references.

- [ ] Sync integrated graphics asset directories to the Windows runtime copy.
  - Why it remains open: the previous sync covered data/scripts for self-test; broad asset-directory runtime sync should happen once a Godot consumer exists.
  - Target: `C:\Users\bh\Games\TerminalVelocity`.

## Verification commands for the next pass

```bash
python3 tools/extract_ev_graphics_manifest.py --extract-ship-sprites --extract-rled-assets --extract-pict-assets --extract-cicn-assets --extract-ppat-assets
python3 -m unittest native_ev.tests.test_model
rsync -a --delete native_ev/data/ /mnt/c/Users/bh/Games/TerminalVelocity/native_ev/data/
rsync -a godot_ev/scripts/ /mnt/c/Users/bh/Games/TerminalVelocity/godot_ev/scripts/
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Users\bh\Games\TerminalVelocity\godot_ev\windows\RunGodot.ps1" -SelfTest
git status --short --branch
```

## Guardrails

- Do not commit proprietary source `.rez` files.
- Keep every generated graphics manifest provenance-first: source path, source SHA-256, resource ID, type, chunk index, byte offset, size, and decode status.
- Record unsupported or uncertain formats as catalog-only or decode-error; do not guess labels or silently drop resources.
- Commit only to `markvshaney/terminal-velocity` unless explicitly told otherwise.
