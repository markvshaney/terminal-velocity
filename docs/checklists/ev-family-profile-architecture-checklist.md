# EV-family profile architecture checklist

Date: 2026-05-18

Decision artifact: `docs/decisions/2026-05-18-ev-family-profile-architecture.md`

Research artifact: `docs/research/ev-community-engine-survey.md`

Behavior baseline checklist: `docs/checklists/ev-classic-behavior-baseline-checklist.md`

Purpose: live execution surface for moving Terminal Velocity toward one shared EV-family runtime with separate Classic/Nova source-data profiles.

## Current verdict

Use **artifact + checklist**:

- The decision artifact preserves the rationale, constraints, and tradeoffs.
- This checklist tracks the concrete next actions and prevents the profile-architecture work from being lost in chat.

## Checklist

- [x] Define the smallest profile descriptor shape.
  - Status: implemented 2026-06-04 as `native_ev/data/profiles/classic.json`.
  - Current shape: profile ID/display name, start system, source/fidelity labels, runtime manifest paths, source manifest paths, and explicit profile-switching boundaries.
  - Verification: `python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_classic_profile_descriptor_validates_runtime_and_source_manifests -v`; `./run_godot.sh self-test` reports `profile=classic profileManifests=17`.

- [x] Inventory current hard-coded Classic assumptions.
  - Status: completed 2026-05-18
  - Evidence: searched Python, Godot, and JSON surfaces under `native_ev/`, `godot_ev/`, and `tools/` for direct data paths, Classic resource names, `ev_classic` asset roots, and sourced manifest assumptions.
  - Result: see "Hard-coded Classic assumptions inventory" below.

- [x] Introduce profile-aware manifest loading without a broad rewrite.
  - Status: implemented initial Classic descriptor validation; broader runtime switching remains pending.
  - Implementation: `native_ev.model.profile_manifest('classic')` validates descriptor IDs/source label and all listed runtime/source manifest paths; Godot self-test loads the same descriptor and fails fast on missing listed files while keeping the current `native_ev/data/*.json` contract intact.
  - Done when: existing Classic self-tests still pass through the profile path.

- [ ] Keep Classic as the first fidelity vertical slice.
  - Status: active direction
  - Next action: continue integrating extracted Classic resources while avoiding new global assumptions that would block a Nova profile.
  - Done when: Classic remains playable and all new manifests/assets are profile-addressable or explicitly marked Classic-only.

- [x] Add tests for profile descriptor and asset path integrity.
  - Status: implemented 2026-06-04.
  - Verification: `NativeEvModelTests.test_classic_profile_descriptor_validates_runtime_and_source_manifests` fails fast if required Classic data/source manifest keys or paths disappear.

- [x] Add Godot self-test coverage for selected profile.
  - Status: implemented 2026-06-04.
  - Verification: `./run_godot.sh self-test` loads `native_ev/data/profiles/classic.json`, validates 17 profile-listed manifests, and reports `profile=classic profileManifests=17`.

- [ ] Mine KestrelEngine for architecture ideas only.
  - Status: pending
  - Source: `docs/research/ev-community-engine-survey.md`
  - Next action: inspect Kestrel resource/plugin architecture and summarize transferable patterns before touching Terminal Velocity code.
  - Done when: useful patterns are written to a research note or applied as small code changes with verification.

- [ ] Mine NovaJS for Nova runtime/data behavior.
  - Status: pending
  - Source: `docs/research/ev-community-engine-survey.md`
  - Next action: inspect data loading, plugin assumptions, and gameplay loops; do not copy assets/data.
  - Done when: Nova-specific semantic questions are listed for future profile extraction.

- [ ] Mine EVNToEndlessSky and evnova-utils for EV Nova semantic mapping cross-checks.
  - Status: pending
  - Source: `docs/research/ev-community-engine-survey.md`
  - Next action: compare their EVN parsing assumptions against our manifest/extraction patterns.
  - Done when: candidate Nova field mappings are recorded with source provenance and confidence labels.

- [ ] Create the first empty/stub Nova profile only after the loader boundary exists.
  - Status: deferred
  - Trigger: Classic loads through profile-aware path and tests cover descriptor integrity.
  - Done when: `nova` exists as a clearly incomplete profile with no false compatibility claims.

- [ ] Reassess separate-game split only if a real trigger appears.
  - Status: watching
  - Triggers:
    - Nova requires a fundamentally different renderer/runtime;
    - adapters become more complex than the shared core;
    - public distribution/packaging becomes a goal;
    - legal/asset-boundary review recommends hard separation;
    - one track becomes creative-remake while another stays fidelity-preservation.
  - Done when: decision artifact is updated if any trigger fires.

## Hard-coded Classic assumptions inventory

Completed: 2026-05-18

Scope searched:

- Python: `tools/*.py`, `native_ev/*.py`, `native_ev/tests/*.py`
- Godot: `godot_ev/scripts/*.gd`
- Runtime JSON: `native_ev/data/*.json`

Findings:

- `native_ev/model.py` top-level manifest constants point directly at `native_ev/data/*.json`, including sourced EV manifests.
  - Owner files: `native_ev/model.py`, `native_ev/tests/test_model.py`
  - Migration choice: **parameterize** behind a profile descriptor, but keep these default paths as the Classic compatibility contract during the first loader slice.

- `native_ev/model.py` validates source provenance against exact EV Classic source paths and extraction methods:
  - `source-assets/ev-classic/Nova Files/EV Data.rez`
  - `source-assets/ev-classic/Nova Files/EV Graphics.rez`
  - `source-assets/ev-classic/Nova Files/EV Sounds.rez`
  - Owner files: `native_ev/model.py`, `native_ev/tests/test_model.py`
  - Migration choice: **profile-specific**. These should move into `classic` descriptor/source manifest metadata or profile-specific validators.

- Python runtime sound validation assumes the Classic sound runtime binding source and method.
  - Owner file: `native_ev/model.py`
  - Current assumptions: `source == native_ev/data/sourced_ev_sounds.json`, `method == ev-classic-runtime-sound-bindings-v1`, representative resource IDs `{200, 205, 601}`.
  - Migration choice: **profile-specific rule flags / validation expectations**.

- Python ship generation is explicitly EV Classic Data/Graphics join logic.
  - Owner file: `native_ev/model.py`
  - Current assumptions: `ev_classic_data_ship_manifest`, Data ship ordinals map to Graphics `shän` resources `128 + ordinal`, Escape Pod special case `895`, 36-facing centered sprite assets.
  - Migration choice: **profile-specific generator/adapter**. Do not generalize to Nova until Nova source semantics are mapped.

- Tool defaults point directly at local EV Classic source files and output paths.
  - Owner files: `tools/extract_ev_data_names.py`, `tools/extract_ev_structured_records.py`, `tools/extract_ev_graphics_manifest.py`, `tools/extract_ev_sounds_manifest.py`, `tools/extract_ev_rled.py`
  - Migration choice: **parameterize by profile**, with current defaults retained for Classic CLI compatibility.

- Extracted runtime asset roots encode `ev_classic` in path names.
  - Owner files/data: `native_ev/data/ships.json`, `native_ev/data/sounds.json`, `native_ev/data/sourced_ev_graphics.json`, `native_ev/data/sourced_ev_sounds.json`, extracted assets under `native_ev/assets/ships/ev_classic/` and `native_ev/assets/sounds/ev_classic/`.
  - Migration choice: **keep** for existing extracted assets; profile descriptor should define asset roots so future Nova assets use their own roots without renaming Classic assets now.

- Godot frontend loads fixed runtime manifests from `repo_root + "/native_ev/data/*.json"`.
  - Owner files: `godot_ev/scripts/main.gd`, `godot_ev/scripts/self_test.gd`
  - Migration choice: **parameterize** through a selected profile while preserving the same runtime file contract for `classic` initially.

- Godot frontend has a Classic-specific default click sound asset path.
  - Owner file: `godot_ev/scripts/main.gd`
  - Current assumption: `assets/sounds/ev_classic/601_click/sound.wav`
  - Migration choice: **profile-specific fallback** or remove once sound manifest/profile descriptor supplies the binding.

- Godot self-test output hard-codes the data path and does not report selected profile.
  - Owner file: `godot_ev/scripts/self_test.gd`
  - Migration choice: **parameterize** and update self-test to print `profile=classic` once descriptor loading exists.

Immediate next implementation target:

1. Add a minimal Classic profile descriptor file that names current manifest paths and asset roots.
2. Add a small Python profile loader/validator that resolves those paths.
3. Route existing Python manifest-load tests through `profile=classic` without moving assets or broad-renaming directories.
4. Then mirror the same selected-profile reporting in Godot self-test.

## Guardrails

- Do not build two separate codebases now.
- Do not perform a broad architecture rewrite before a small profile descriptor/loader is proven.
- Do not rename the project or major directories purely for neatness.
- Do not call Nova supported until a Nova source-data profile is extracted, mapped, tested, and loaded.
- Keep original/extracted assets local for personal use and non-redistributed.
