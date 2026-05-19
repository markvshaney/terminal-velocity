# EV Classic behavior baseline checklist

Date: 2026-05-18

Purpose: durable execution surface for comparing Terminal Velocity behavior against original Escape Velocity Classic without letting external adaptations become accidental sources of truth.

Related decision: `docs/decisions/2026-05-18-ev-family-profile-architecture.md`

Related profile checklist: `docs/checklists/ev-family-profile-architecture-checklist.md`

Related runtime setup checklist: `docs/checklists/ev-classic-original-runtime-observation-checklist.md`

## Source hierarchy

1. **Primary truth sources**
   - Original EV Classic runtime observation from authorized local copies.
   - Decoded EV Classic source resources with provenance: Data, Graphics, Sounds, and related manifests.
   - Original/manual documentation when available.

2. **Project evidence**
   - Terminal Velocity manifests, tests, Godot self-tests, deterministic logs, and generated artifacts.
   - These describe current implementation state; they do not prove original-game fidelity by themselves.

3. **External adaptations / community engines**
   - Examples: NovaJS, KestrelEngine/Cosmic Frontier, OpenNova, EVNToEndlessSky, evnova-utils, and similar projects.
   - Status: **source of ideas, not necessarily source of truth**.
   - Allowed use: hypothesis generation, edge-case discovery, engineering pattern discovery, comparison prompts, and questions to verify against primary sources.
   - Disallowed use: justifying Terminal Velocity gameplay behavior solely because another adaptation behaves that way.

## Evidence labels

Use one of these labels for each behavior claim:

- `original-runtime-observed` — observed directly in original EV Classic.
- `decoded-resource-backed` — derived from decoded EV Classic resources with source path/hash/resource provenance.
- `manual-backed` — derived from original/manual documentation.
- `terminal-velocity-observed` — observed in current TV runtime/test logs.
- `external-adaptation-observed` — observed in another implementation; idea/hypothesis only.
- `inferred-scaffold` — local implementation guess or temporary scaffold.
- `unknown` — not yet source-backed.

## Comparison matrix template

For every behavior row, record:

- Behavior:
- Primary evidence:
- Evidence label:
- Observed original EV Classic behavior:
- Terminal Velocity current behavior:
- Status: `match` / `mismatch` / `unknown` / `scaffold`
- Confidence: `high` / `medium` / `low`
- Verification needed:
- Notes/provenance:

## Baseline targets

### Start state / new pilot flow

- [x] Title preferences screen visual/wording pass
  - Evidence label: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat.
  - Primary evidence: original EV Classic running in Basilisk II; local-only capture path `C:\Games\BasiliskII\ev-prefs-correct-coords-2.png`.
  - Observed visible groups/controls: `Navigation Controls:`, `Escort Controls:`, `Weapon Controls:`, `Misc. Controls:`, `Sound Volume: Quiet`, `Intro Music`, `Game Speed...`, `Cancel`, `OK`.
  - Terminal Velocity current behavior: 2026-05-19 Godot modal in `godot_ev/scripts/main.gd` copies the observed prefs layout/wording and keeps saved mappings for Intro Music, Sound Volume, and Game Speed; self-test emits `prefScreen=original-ev-classic-observed` plus `user://selftest/title_prefs.png`.
  - Status: `match` for visible prefs screen wording/layout target; confidence `medium` because the raw screenshot remains local-only and font/spacing are approximated in Godot.

- [x] Starting ship
  - Evidence label: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat.
  - Primary evidence: original EV Classic running in Basilisk II; local-only captures `C:\Games\BasiliskII\ev-new-pilot-after-ship-name.png` and `C:\Games\BasiliskII\ev-new-pilot-enter-ship.png`.
  - Observed original EV Classic behavior: new pilot defaults to pilot name `Rick Hardslab`, ship name `Starseeker`, and prompt text `Now, please christen your brand-new Rendell StarDrive 805R cargo shuttle:`; title status panel reports `Ship Type: Shuttlecraft`.
  - Terminal Velocity current behavior: Godot frontend selects `shuttlecraft` in `godot_ev/scripts/main.gd`.
  - Status: `match`; confidence `medium` because captures remain local-only and the exact `805R cargo shuttle` resource meaning still needs static resource cross-check.

- [x] Starting credits
  - Evidence label: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat.
  - Primary evidence: original EV Classic running in Basilisk II; local-only capture `C:\Games\BasiliskII\ev-new-pilot-enter-ship-5s.png` / later in-space captures.
  - Observed original EV Classic behavior: first playable space HUD shows `Credits: 10,000`.
  - Terminal Velocity current behavior: `credits := 10000` in `godot_ev/scripts/main.gd` after 2026-05-19 correction from earlier scaffold value `5000`.
  - Status: `match`; confidence `medium`.

- [x] Starting location / system / landed-or-space state
  - Evidence label: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat plus `decoded-resource-backed` Levo landing text.
  - Primary evidence: original EV Classic running in Basilisk II; local-only captures `C:\Games\BasiliskII\ev-new-pilot-after-ship-name.png`, `C:\Games\BasiliskII\ev-new-pilot-enter-ship-5s.png`, and `C:\Games\BasiliskII\ev-new-pilot-after-intro-wait2.png`; decoded landing entry in `native_ev/data/sourced_ev_names.json` for `Levo`.
  - Observed original EV Classic behavior: title status panel reports `Levo system: Clean`; first playable state is in space near Levo, with message `Welcome to Escape Velocity - it would be a good idea to start by landing on Levo and checking out the prices. Hit ‘L’ to request landing clearance, then hit it again to land.`
  - Terminal Velocity current behavior: `native_ev/data/universe.json` now starts with a Levo system containing source-backed `Levo Spaceport`; `godot_ev/scripts/main.gd` resolves `START_SYSTEM_NAME := "Levo"` by name; live frontend state remains space.
  - Status: `match` for starting system/location and starting in space; confidence `medium` because Levo routing/coordinates are minimal integration scaffolding pending fuller decoded system topology.

- [ ] Starting equipment/outfits/weapons
  - Evidence label: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat.
  - Primary evidence: original EV Classic first playable in-space HUD; local-only capture `C:\Games\BasiliskII\ev-new-pilot-after-intro-wait2.png`.
  - Observed original EV Classic behavior: HUD shows full Shield/Fuel bars, `No Secondary Weapon`, `No Target`, and `Free: 20`; detailed outfits/weapons inventory was not opened successfully during automation.
  - Status: `partial`; verification needed: open player/ship info or landed outfitter/status screen without changing inventory.

### Ship facing and rendering

- [ ] 36-facing ship sprite contract
  - Evidence label: `decoded-resource-backed`
  - Primary evidence: decoded EV Classic graphics manifests and extracted frame sets.
  - Terminal Velocity current behavior: ship manifests expect `frameCount` and tests assert extracted frame counts.
  - Status: partially source-backed; needs original runtime frame-order/facing confirmation.

- [ ] Sprite registration / centering
  - Evidence label: `terminal-velocity-observed`
  - Terminal Velocity current behavior: centered cell/frame handling is an explicit project convention.
  - Primary evidence needed: original runtime observation or decoded sprite metadata if available.
  - Status: `unknown`

- [ ] No runtime rotation for EV Classic ship sprites
  - Evidence label: `decoded-resource-backed`
  - Primary evidence: EV Classic extracted 36-facing sprite sheets/frames.
  - Terminal Velocity current behavior: should select discrete facing frames rather than rotate sprites.
  - Status: source-backed direction; continue testing.

### Movement feel

- [ ] Turning rate
  - Evidence label: `unknown`
  - Primary evidence needed: original runtime capture at fixed time/frame interval.
  - Terminal Velocity current behavior: needs deterministic Godot log of facing index after N ticks.
  - Status: `unknown`

- [ ] Acceleration curve
  - Evidence label: `unknown`
  - Primary evidence needed: original runtime measurement or decoded physics fields if found.
  - Terminal Velocity current behavior: needs deterministic log of velocity after N thrust ticks.
  - Status: `unknown`

- [ ] Max speed and inertial drift
  - Evidence label: `unknown`
  - Primary evidence needed: original runtime measurement or decoded ship/physics fields.
  - Terminal Velocity current behavior: needs deterministic logs.
  - Status: `unknown`

### Landing and hyperspace loop

- [ ] Land/takeoff state transitions
  - Evidence label: `unknown`
  - Primary evidence needed: original runtime observation.
  - Terminal Velocity current behavior: current Godot landing state should be logged and compared.
  - Status: `unknown`

- [ ] Hyperspace availability and destination selection
  - Evidence label: `decoded-resource-backed` for map links where decoded; runtime behavior still needs observation.
  - Primary evidence needed: decoded topology plus original runtime behavior.
  - Terminal Velocity current behavior: uses `links` from `native_ev/data/universe.json`.
  - Status: partial.

- [ ] Hyperspace timing / animation / sound
  - Evidence label: `unknown`
  - Primary evidence needed: original runtime capture.
  - Terminal Velocity current behavior: needs deterministic event log and sound binding check.
  - Status: `unknown`

### Basic combat

- [ ] Weapon fire rate / cooldown
  - Evidence label: `unknown`
  - Primary evidence needed: original runtime measurement or decoded weapon fields.
  - Terminal Velocity current behavior: current `native_ev/data/weapons.json` values are implementation state.
  - Status: `unknown`

- [ ] Projectile speed / lifetime / damage
  - Evidence label: `unknown`
  - Primary evidence needed: decoded weapon fields or original runtime measurement.
  - Terminal Velocity current behavior: current values in `native_ev/data/weapons.json` may be scaffold unless source-backed separately.
  - Status: `unknown`

- [ ] Target selection behavior
  - Evidence label: `unknown`
  - Primary evidence needed: original runtime observation.
  - Terminal Velocity current behavior: needs Godot log/self-test coverage.
  - Status: `unknown`

- [ ] Explosion and sound bindings
  - Evidence label: `decoded-resource-backed` for extracted assets/sound resources; runtime behavior still needs confirmation.
  - Primary evidence needed: decoded resource references and original runtime observation.
  - Terminal Velocity current behavior: sound manifest has source-backed WAVs and local bindings.
  - Status: partial.

## Instrumentation needed in Terminal Velocity

- [x] Deterministic Godot movement log: selected ship, tick count, facing index, angle, velocity, and position.
  - Status: `terminal-velocity-observed` 2026-05-19 via `--tv-movement-log` in `godot_ev/scripts/main.gd`; emits right-turn and thrust scenarios for remote/headless comparison work.
- [ ] Deterministic turn/thrust scenarios: after N ticks of left/right/thrust/no-input.
- [ ] Event log for landing/takeoff/hyperspace transitions.
- [ ] Event log for target acquisition, weapon firing, projectile spawn, hit, and explosion.
- [ ] Self-test output should include selected profile once profile loading exists: `profile=classic`.

## Contamination guardrail for external adaptations

External adaptations may be tested only with this note attached:

```text
Observation source: <project>
Status: source of ideas, not necessarily source of truth
Observed behavior: <specific observation>
Possible use for Terminal Velocity: <question/hypothesis/pattern>
Do not infer: original EV Classic behavior or exact gameplay fidelity
Primary-source verification needed: <what would confirm/refute it>
```

## Immediate next actions

1. Use `docs/checklists/ev-classic-original-runtime-observation-checklist.md` to finish original-runtime setup prerequisites.
2. Create the local-only emulator workspace outside the repo.
3. Locate/provide authorized Classic Mac ROM and compatible Mac OS install/media.
4. Finish profile descriptor work so future behavior logs are profile-addressed.
5. Add `profile=classic` to Godot self-test output.
6. Add deterministic movement/facing logs for Terminal Velocity.
7. Populate this checklist only with evidence-labeled behavior claims; avoid using adaptation observations as truth.
