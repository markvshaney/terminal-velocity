# EV-family profile architecture checklist

Date: 2026-05-18

Decision artifact: `docs/decisions/2026-05-18-ev-family-profile-architecture.md`

Research artifact: `docs/research/ev-community-engine-survey.md`

Purpose: live execution surface for moving Terminal Velocity toward one shared EV-family runtime with separate Classic/Nova source-data profiles.

## Current verdict

Use **artifact + checklist**:

- The decision artifact preserves the rationale, constraints, and tradeoffs.
- This checklist tracks the concrete next actions and prevents the profile-architecture work from being lost in chat.

## Checklist

- [ ] Define the smallest profile descriptor shape.
  - Status: pending
  - Next action: identify current hard-coded manifest/data paths in Python and Godot.
  - Done when: there is a documented minimal descriptor with profile ID, display name, source family, manifest paths, asset roots, and rule flags.

- [ ] Inventory current hard-coded Classic assumptions.
  - Status: pending
  - Next action: search `native_ev/`, `godot_ev/`, and `tools/` for direct paths to Classic manifests/assets and EV Classic-specific naming.
  - Done when: assumptions are listed with owner file and migration choice: keep, parameterize, or profile-specific.

- [ ] Introduce profile-aware manifest loading without a broad rewrite.
  - Status: pending
  - Next action: add the smallest loader indirection so the current Classic data loads through `classic` profile selection.
  - Done when: existing Classic self-tests still pass through the profile path.

- [ ] Keep Classic as the first fidelity vertical slice.
  - Status: active direction
  - Next action: continue integrating extracted Classic resources while avoiding new global assumptions that would block a Nova profile.
  - Done when: Classic remains playable and all new manifests/assets are profile-addressable or explicitly marked Classic-only.

- [ ] Add tests for profile descriptor and asset path integrity.
  - Status: pending
  - Next action: extend existing `native_ev.tests.test_model` or nearby tests to validate the Classic profile descriptor and manifest existence.
  - Done when: profile config errors fail fast in unit tests before Godot launch.

- [ ] Add Godot self-test coverage for selected profile.
  - Status: pending
  - Next action: make the self-test print the selected profile ID and validate profile-loaded assets/data.
  - Done when: Godot self-test clearly reports `profile=classic` and catches missing profile files.

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

## Guardrails

- Do not build two separate codebases now.
- Do not perform a broad architecture rewrite before a small profile descriptor/loader is proven.
- Do not rename the project or major directories purely for neatness.
- Do not call Nova supported until a Nova source-data profile is extracted, mapped, tested, and loaded.
- Keep original/extracted assets local for personal use and non-redistributed.
