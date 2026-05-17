# EV Graphics Extraction Follow-up Checklist

Purpose: track the things I was **not yet able to finish** in the last graphics extraction pass, so we can continue from a concrete backlog instead of re-discovering them.

## Decode gaps left open

- [ ] Investigate `rlëD` resource `4004` / `Large Explosion`.
  - Current status: `decode-error: unsupported rleD header width=32767 height=40 depth=65535 frames=0`.
  - Why it remains open: it does not match the normal rlëD sprite header decoder used for the other 77 decoded rlëD resources.
  - Next local step: inspect raw bytes and determine whether this is a special-case sprite, metadata-like resource, or unsupported header variant.
  - Verification target: either decode it to PNG with a test, or document why it is not a normal drawable asset.

- [ ] Investigate `PICT` resource `9507` / `Trugati Asteroid Belt`.
  - Current status: `decode-error: no supported PackBits PICT opcode found`.
  - Why it remains open: the new PICT decoder supports the direct-color PackBits subset used by the other 93 decoded PICT resources, but this one did not expose a supported opcode in the searched range.
  - Next local step: inspect its PICT opcode stream and add only source-backed support for the observed format.
  - Verification target: either decode it to PNG with a test, or record its unsupported format explicitly in the manifest.

- [ ] Decode or explicitly defer `cicn` resources.
  - Current status: `catalog-only-unsupported-raster` for 29 classic Mac color icon resources.
  - Why it remains open: they are raster/icon resources, but no `cicn` PNG decoder was implemented in the pass.
  - Next local step: inspect representative `cicn` raw records and identify the icon/pixmap layout.
  - Verification target: decoded PNGs under a stable asset directory, plus manifest/test coverage; or a documented defer decision.

- [ ] Decode or explicitly defer `ppat` resources.
  - Current status: `catalog-only-unsupported-raster` for 10 classic Mac pixel-pattern resources.
  - Why it remains open: they are raster/pattern resources, but no `ppat` PNG decoder was implemented in the pass.
  - Next local step: inspect representative `ppat` raw records and identify the pattern/pixmap layout.
  - Verification target: decoded PNGs under a stable asset directory, plus manifest/test coverage; or a documented defer decision.

## Metadata families not yet semantically integrated

- [ ] Interpret `spïn` records beyond cataloging.
  - Current status: 58 `spïn` records cataloged only.
  - Why it remains open: the visual frames are largely in `rlëD`, but `spïn` likely controls spin/animation metadata and has not been semantically decoded.
  - Next local step: decode all 16-bit fields and correlate with `rlëD` IDs for planets, stations, asteroids, stars, and main-screen orbs.

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
python3 tools/extract_ev_graphics_manifest.py --extract-ship-sprites --extract-rled-assets --extract-pict-assets
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
