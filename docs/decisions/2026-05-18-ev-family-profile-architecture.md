# EV-family profile architecture decision

Date: 2026-05-18

Status: proposed direction

Related artifact: `docs/research/ev-community-engine-survey.md`

Related checklist: `docs/checklists/ev-family-profile-architecture-checklist.md`

## Decision

Build **one local Terminal Velocity EV-family runtime** with separate source-data/rules profiles, not two separate game codebases.

Initial profiles:

- `classic` — original Escape Velocity / EV Classic fidelity track.
- `nova` — EV Nova fidelity track, added after Nova resource/data semantics are mapped.

Possible later profile:

- `override` — EV Override, if source data and interest justify it.

This is strictly for personal use, so the project does not need public packaging separation right now. Personal-use scope reduces distribution/legal pressure and makes a shared local player/profile model more attractive.

## Rationale

### Shared engine code should not be duplicated

EV Classic and EV Nova share enough runtime structure that separate codebases would create unnecessary drift:

- top-down 2D ship flight and combat;
- prerendered ship facings;
- systems, spobs, hyperspace links, and landing screens;
- missions, outfits, shipyards, weapons, commodity/cargo loops;
- governments, legal status, NPC traffic, and plug-in-style data replacement.

The differences are real, but they belong primarily in profile-specific source adapters, manifests, rules, and balancing data rather than in forked render/gameplay code.

### Personal-use scope favors a local multi-profile player

Because this is for personal use, Terminal Velocity can behave more like a local EV-family player/source-port workspace:

- original/local assets can remain local and non-redistributed;
- profile-specific extraction provenance can be preserved without designing public asset packaging;
- Classic and Nova behavior can be compared side-by-side;
- shared tooling/tests/debug UI can serve both profiles;
- adding Nova later does not require stopping the Classic vertical slice.

### Current evidence favors Classic first

Current local extraction/runtime state is strongest for EV Classic:

- source-backed graphics manifest from `EV Graphics.rez`;
- decoded ship facings, rlëD frames, PICT/cicn/ppat images;
- source-backed sound manifest and WAV extraction;
- primitive `EV Data.rez` structure manifest;
- runtime-facing ship and sound manifests;
- Godot frontend self-test already loads key assets/data.

So the near-term fidelity path should remain **Classic first**, while keeping the architecture profile-aware so Nova can be added cleanly.

## Recommended target shape

Near-term conceptual structure:

```text
native_ev/
  core/
    model/rules shared across EV-family profiles
    manifest loaders
    runtime validation
  profiles/
    classic/
      source-manifests/
      runtime-manifests/
      rule-overrides/
      extraction-notes/
    nova/
      source-manifests/
      runtime-manifests/
      rule-overrides/
      extraction-notes/
```

Godot should eventually select a profile and load profile-specific manifests through a stable shared data contract.

Do not rename/reorganize everything immediately just for neatness. The next useful move is to introduce a small profile boundary around loaders/manifests, then migrate incrementally.

## What should stay shared

- Godot frontend shell and common HUD/scanner/landing UI contracts.
- Core model tests where behavior is genuinely shared.
- Data loading/validation framework.
- Resource provenance conventions.
- Sprite/audio runtime manifest contracts.
- Debug/self-test/autopilot infrastructure.
- Extraction script patterns when the resource family is structurally similar.

## What should be profile-specific

- Source asset paths and hashes.
- Raw resource manifests.
- Semantic field mappings.
- Mission semantics and text/source relationships.
- Ship/outfit/weapon/economy balance.
- UI text and exact feel where games differ.
- Plugin/TC compatibility expectations.
- Any legal/distribution notes, even for personal use, so local-only boundaries remain clear.

## When to reconsider separate games/repos

Split into separate games only if one of these becomes true:

- EV Nova requires a fundamentally different renderer/runtime.
- The data/rules adapters become more complex than the shared core.
- One track becomes a creative remake while the other stays preservation/fidelity-focused.
- Separate public packaging/distribution becomes a goal.
- License or asset-boundary review says hard repo separation is safer.

None of those conditions currently apply.

## Immediate recommendation

1. Keep shipping the EV Classic vertical slice.
2. Add a lightweight profile abstraction before wiring much more content.
3. Mine these sources from the community-engine survey in order:
   - KestrelEngine for resource/plugin architecture patterns;
   - NovaJS for EV Nova runtime/data behavior;
   - EVNToEndlessSky + evnova-utils for EV Nova semantic mapping cross-checks.
4. Track the work in `docs/checklists/ev-family-profile-architecture-checklist.md` rather than leaving it in chat.

## Non-goals for now

- Do not build two separate codebases.
- Do not stop Classic work to perform a large architecture rewrite.
- Do not promise EV Nova compatibility until a Nova source-data profile exists and is verified.
- Do not redistribute original/extracted assets; keep local personal-use boundaries explicit.
