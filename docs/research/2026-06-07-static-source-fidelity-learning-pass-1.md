# Static source fidelity learning pass 1

Date: 2026-06-07

## Scope

This is the completed first static/source-mined fidelity learning pass for Terminal Velocity. It covers the static sources already present locally and the manifests already decoded in the repo. It does **not** claim that every EV Classic field has final semantics. It separates learned static facts, integrated runtime surfaces, and remaining source-decoding gaps.

Basilisk/original-runtime speed is not a blocker for this pass. Basilisk remains useful for spot checks, ambiguity resolution, UI/state-transition behavior, and timing/feel claims.

## Verified source assets

- `EV Data.rez`
  - Path: `source-assets/ev-classic/Nova Files/EV Data.rez`
  - Size: `1263215` bytes
  - SHA256: `e5e8b5c667409b1c950a49e6aeb3a771609126e205959ef81e9328beabf2ba2f`
  - Repo manifests: `native_ev/data/sourced_ev_structures.json`, `native_ev/data/sourced_ev_names.json`, `native_ev/data/sourced_ev_governments.json`, `native_ev/data/sourced_ev_junk.json`, `native_ev/data/sourced_ev_missions.json`, `native_ev/data/sourced_ev_weapons.json`
- `EV Graphics.rez`
  - Path: `source-assets/ev-classic/Nova Files/EV Graphics.rez`
  - Size: `2403167` bytes
  - SHA256: `640f7698dcedc5faab86220284802b07a2a6fe719b3f988f5c4a4bcd4c3f89ad`
  - Repo manifests: `native_ev/data/sourced_ev_graphics.json`
- `EV Sounds.rez`
  - Path: `source-assets/ev-classic/Nova Files/EV Sounds.rez`
  - Size: `1015014` bytes
  - SHA256: `36fc306b41bb384e07ea78fe78ede115d02695f9eb01e6b8189b3a1280261f0e`
  - Repo manifests: `native_ev/data/sourced_ev_sounds.json`

## Static-source learning inventory

- Primitive EV Data structure decode:
  - `brgr-full-field-decode-v2` over `source-assets/ev-classic/Nova Files/EV Data.rez`.
  - Chunk count: `1544`.
  - Fixed-record runs: `12`.
  - Run directory entries: `15`.
    - run 0: unknown-fixed-record / count `5` / record size `822` / confidence `low`.
    - run 1: unknown-fixed-record / count `5` / record size `109` / confidence `low`.
    - run 2: unknown-fixed-record / count `5` / record size `112` / confidence `low`.
    - run 3: syst-like / count `67` / record size `88` / confidence `medium`.
    - run 4: government-like / count `19` / record size `306` / confidence `low`.
    - run 5: government-or-status-like / count `25` / record size `192` / confidence `low`.
    - run 6: commodity-like / count `19` / record size `676` / confidence `medium`.
    - run 7: mission-like / count `116` / record size `1970` / confidence `low`.
  - Learning status: primitive record inventory is complete enough for source-mined lane work; many record-family semantic maps remain partial/provisional.

- Names/text:
  - Method: `brgr-text-chunk-heuristic-v1`.
  - System-name seeds: `9`.
  - Landing/body names and descriptions: `72`.
  - High-confidence landing/body examples: `Earth`, `Stardock Alpha`, `Mars`, `Landfall`, `Luna`, `Levo`, `New Britain`, `Capella`, `Dune`, `Spica`, `Maxwell’s Purchase`, `Hodgson’s World`.
  - Learning status: landing descriptions are strong static text evidence; system-name seeds are heuristic unless cross-linked to decoded topology records.

- Governments/legal:
  - Method: `ev-classic-resource-bible-govt-field-map-v1`.
  - Source basis: `EV Classic Resource Bible gövt field definitions plus local primitive BRGR structure decode`.
  - Runtime-facing data currently exposes `5` governments, `10` system government entries, and `5` contraband entries.
  - Learning status: Resource Bible-backed field semantics can support data-model claims; exact runtime enforcement remains behavior/timing/UI evidence work.

- Missions:
  - Method: `ev-classic-resource-bible-misn-field-map-v2`.
  - Source basis: `EV Classic Resource Bible mïsn field definitions through Flags plus local primitive BRGR structure decode`.
  - Runtime-facing mission scaffold currently exposes `5` missions.
  - Learning status: decoded mission fields through flags support field-level semantics; exact offer generation/UI/deadline behavior still needs runtime or stronger semantic decoding per mission family.

- Economy / specialized commodities:
  - Method: `ev-classic-resource-bible-junk-field-map-v1` for specialized `jünk` commodity records.
  - Source basis: `EV Classic Resource Bible jünk field definitions plus local primitive BRGR structure decode`.
  - Promoted static-source manifest: `native_ev/data/sourced_ev_junk.json` with `19` specialized commodities, sold-at stellar IDs, bought-at stellar IDs or `none`, base prices, and the `tribblesMultiplication` flag where present.
  - Runtime-facing economy still exposes the current 5-commodity playable market subset; broad specialized-commodity UI/import behavior remains a future promotion, not a runtime behavior claim from this static pass.

- Weapons / outfits / ships:
  - Weapon method: `ev-classic-resource-bible-weapon-field-map-v1`.
  - Weapon source basis: `EV Classic Resource Bible wëap/oütf field definitions plus local primitive BRGR structure decode`.
  - Runtime-facing data currently exposes `26` ships, `28` traffic entries, `3` base outfits, `26` shipyard entries, and `2` weapons.
  - Learning status: source-backed stock names/field semantics are usable for data contracts; exact combat cadence, facing, firing behavior, and purchase UI remain runtime/behavior gates.

- Graphics:
  - Method: `evnew-opcode-rled-shan-pict-cicn-ppat-spin-boom-roid-v7`.
  - Resource count: `303` across `8` resource-type catalog entries.
    - `PICT`: count `94`, status `decoded-to-png`.
    - `bööm`: count `5`, status `decoded-primitive-fields`.
    - `cicn`: count `29`, status `decoded-to-png-with-explicit-errors`.
    - `ppat`: count `10`, status `decoded-to-png-with-explicit-errors`.
    - `rlëD`: count `78`, status `decoded-to-png`.
    - `röid`: count `2`, status `decoded-primitive-fields`.
    - `shän`: count `27`, status `decoded-metadata-and-ship-pngs`.
    - `spïn`: count `58`, status `decoded-primitive-fields`.
  - Learning status: decoded PNG/local asset manifests support static visual inventory and runtime asset mapping, but publishing raw proprietary assets remains out of scope.

- Sounds:
  - Method: `classic-mac-snd-wav-v2`.
  - Resource count: `57`; decoded runtime-facing sound entries: `13`; binding groups: `4`.
    - `snd `: count `57`, status `decoded-to-wav-with-explicit-errors`.
  - Learning status: source-backed sound catalog and decoded WAV assets support runtime bindings already present for representative UI/flight/weapon/combat surfaces.

## Runtime-facing coverage from static sources

- Universe data currently contains `10` systems: `Levo`, `Sol`, `Centauri`, `Sirius`, `Tau Ceti`, `Enyo`, `Antares`, `Alkaid`, `Zaxted`, `Clotho`.
- Economy data contains `5` commodities and `10` markets.
- Ships data contains `26` ship records and `28` traffic records.
- Outfits/shipyard data contains `3` base outfit records and `26` shipyard sale records.
- Governments data contains `5` governments and `10` system-government mappings.
- Missions data contains `5` runtime-facing missions.
- Sounds data contains `13` runtime-facing sound aliases and `4` binding groups.

## Static-source claims promoted by this pass

- `decoded-resource-backed`: EV Data.rez, EV Graphics.rez, and EV Sounds.rez are present locally and their SHA256 hashes match the checked-in sourced manifests.
- `decoded-resource-backed`: Static landing/body text extraction has high-confidence entries for 72 landable/station description chunks; these are stronger static text evidence than Basilisk speed-limited observation.
- `decoded-resource-backed / manual/docs-backed`: Government, mission, weapon, and specialized `jünk` commodity semantic manifests combine local primitive records with EV Classic Resource Bible field definitions; they can support field-level data-model semantics, not exact runtime UI/timing by themselves.
- `decoded-resource-backed`: Graphics and sounds have broad source manifests with decoded local assets; runtime use must keep proprietary asset boundaries and provenance labels.
- `terminal-velocity-observed / scaffold where not fully decoded`: Runtime-facing universe/economy/ships/outfits/governments/missions data is intentionally a partial playable subset; not all static source data has been semantically integrated.

## Remaining static-source work

- **Full galaxy topology and coordinates**: 67 `syst-like` primitive records are present, but semantic field mapping/cross-links need promotion before replacing the 10-system runtime subset.
- **System-by-system service/store provisioning**: 72 landing/body text entries exist, but service matrices, outfitter/shipyard/weapon availability, absent services, and planet/station graphics need structured compare/import coverage.
- **Economy-wide market formula/spreads**: Current runtime data has 5 commodities and 10 markets; Levo same-port sellback is runtime-observed, and specialized `jünk` commodity fields are now semantically promoted, while broad regular-commodity buy/sell rules and specialized-commodity runtime availability/import behavior remain partial.
- **Ship/outfit/weapon exact semantics**: Source-backed fields and names exist for representative data, but combat cadence, purchase UI, starting primary/outfit inventory, and frame-order remain runtime/behavior gates.
- **Mission families**: Mission field manifests exist through flags, but exact generation/offer/completion/failure/UI behavior needs family-by-family promotion.
- **Asset/runtime mapping completeness**: Graphics/sound manifests are broad, but every decoded playable resource is not necessarily wired into TV runtime surfaces yet.

## Next lane contract

- Track: `fidelity-gate / static-source-mined`.
- Owner: integration owner or assigned static-source worker lane.
- Writable surfaces: generated semantic manifests under `native_ev/data/`, focused extractor scripts under `tools/`, tests under `native_ev/tests/`, and this research/checklist surface.
- Verifier: JSON parse/hash match, extractor unit tests, focused model/scenario tests for each promoted data surface, and no raw proprietary assets committed beyond existing project policy.
- Merge contract: promote one resource family at a time from primitive/source manifest → semantic manifest → runtime-facing data → tests/docs/backlog.
- Gate: do not claim exact Classic behavior for UI/timing/state transitions from static sources alone.

## Verification performed for this pass

- Parsed all `native_ev/data/*.json` files.
- Verified local source asset existence, sizes, and SHA256 for EV Data, Graphics, and Sounds against sourced manifest hashes.
- Read live backlog and process docs to keep this as a static fidelity learning pass rather than a Basilisk/runtime observation pass.
