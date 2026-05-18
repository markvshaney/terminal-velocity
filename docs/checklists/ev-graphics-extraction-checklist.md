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

## Metadata semantics decoded

- [x] Interpret `spïn` spin metadata records beyond cataloging.
  - Current status: standard six-word `spïn` records now decode into base/mask `rlëD` references, display width/height, frame-row/frame-column grids, expected frame counts, and linked `rlëD` header metadata where source-backed.
  - Finding: many source references are direct `rlëD` ids, while some EV Classic records use the same +2 offset pattern already seen in `shän`; the decoder keeps raw words and records inferred links for auditability.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_graphics_manifest_interprets_spin_boom_roid_metadata` asserts representative explosion and weapon spin crosswalks.

- [x] Interpret `bööm` records beyond cataloging.
  - Current status: compact three-word `bööm` records now decode duration/sound/variant primitives and crosswalk to the matching explosion `spïn` resources. The long `Ship Explodes` record is explicitly classified as a table-like/forklift variant record with inferred family ids preserved.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_graphics_manifest_interprets_spin_boom_roid_metadata` asserts `FAE Small` and `Ship Explodes` decoded metadata.

- [x] Interpret `röid` records beyond cataloging.
  - Current status: asteroid `röid` records now preserve raw behavior words and crosswalk to asteroid `spïn`/`rlëD` visual resources where source-backed.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_sourced_ev_graphics_manifest_interprets_spin_boom_roid_metadata` asserts small/big asteroid links and `rlëD` frame counts.

## Runtime integration not yet done

- [x] Choose the first Godot consumer for decoded PICT assets.
  - Current choice: shipyard artwork from `native_ev/assets/graphics/pict/5000_shipyard/` and related `500x` resources, because it is visible in the existing Shipyard landing tab and maps naturally to Data-backed ship identities.
  - Deferred alternatives: outfit artwork from `600x`, target pictures from `300x`, and backdrop/nebula images remain candidates for later runtime consumers.

- [x] Add runtime manifest fields or lookup tables for chosen PICT consumers.
  - Current status: `native_ev/data/ships.json` now carries optional `shipyardPictResourceId`, `shipyardPictAssetFile`, `shipyardPictWidth`, and `shipyardPictHeight` fields for ships whose Data ordinal has a decoded `500x` PICT asset.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_ev_classic_ship_manifest_is_joined_from_data_identity_to_graphics_assets` asserts the Data ordinal to PICT path mapping and keeps unmapped ships explicit by omitting the fields.

- [x] Add Godot-side loading and smoke assertions for any newly consumed PICT assets.
  - Current status: Godot loads source-backed shipyard PICT PNGs from the ship manifest, displays the selected listing's art in the Shipyard tab when available, and self-test validates the loadable PICT set.
  - Verification: `native_ev.tests.test_model.NativeEvModelTests.test_godot_shipyard_loads_source_backed_pict_art` asserts the runtime contract; Windows Godot self-test passed with `pictsLoaded=22`.

- [x] Sync integrated graphics asset directories to the Windows runtime copy.
  - Target: `C:\Users\bh\Games\TerminalVelocity`.
  - Current status: synced `native_ev/data/`, `native_ev/assets/graphics/pict/`, and `godot_ev/scripts/` to the Windows runtime copy after shipyard PICT loading was added.

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
