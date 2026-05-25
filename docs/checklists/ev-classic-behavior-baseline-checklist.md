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
  - Strict Play note: the observed Set Prefs screen does not show a `Strict Play` control; 2026-05-20 external/pilot-file evidence indicates Strict Play is per-pilot state, so its UI should be investigated in the new-pilot flow rather than added to Set Prefs.
  - Terminal Velocity current behavior: 2026-05-19 Godot modal in `godot_ev/scripts/main.gd` copies the observed prefs layout/wording and keeps saved mappings for Intro Music, Sound Volume, and Game Speed; self-test emits `prefScreen=original-ev-classic-observed` plus `user://selftest/title_prefs.png`.
  - Status: `match` for visible prefs screen wording/layout target; confidence `medium` because the raw screenshot remains local-only and font/spacing are approximated in Godot.

- [x] Strict Play / permadeath pilot option
  - Evidence label: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat, plus `local-manual-string-backed` and `pilot-file-structure-backed`.
  - Primary evidence: original EV Classic New Pilot dialog capture, local-only path `C:\Games\BasiliskII\ev-new-pilot-strict-play-unchecked.png`; local `System7_5_3.img` string/manual text says the `New Pilot` dialog lets the player name the pilot and decide whether to play by Strict rules. The same manual text says Strict death is final, while not playing by Strict rules lets the player use `Open Pilot` to resume from the last landed planet. Ambrosia forum archive pilot-file notes identify a per-pilot `strictPlayFlag` in resource `129` (`MpďL`) with `0 = strict play off`.
  - Observed original EV Classic behavior: Set Prefs, Levo landed, and commodity screens do not expose the control. The New Pilot dialog shows `Enter your name, pilot:`, default name `Rick Hardslab`, an unchecked `Strict Play` checkbox, explanatory text `If you check this box, when you're dead, you're dead. No reincarnation allowed.`, and `Cancel` / `OK` buttons. The dialog was cancelled after capture; no destructive strict-play test was performed.
  - Terminal Velocity current behavior: `godot_ev/scripts/main.gd` now places `Strict Play` in the New Pilot name dialog, defaults it unchecked/off, lets the player toggle it before naming the pilot, stores it per pilot as `strict_play`, and reloads that per-pilot flag. `godot_ev/scripts/self_test.gd` reports `strictPlay=off-by-default`.
  - Status: `implemented-default-off`; source-backed off semantics are `Strict Play` unchecked / `strictPlayFlag = 0`. Exact destructive death behavior remains intentionally untested and is not implemented yet.

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
  - Primary evidence: original EV Classic first playable in-space HUD; local-only captures `C:\Games\BasiliskII\ev-new-pilot-after-intro-wait2.png`, `C:\Games\BasiliskII\ev-start-equipment-landing-postmessage-l.png`, `C:\Games\BasiliskII\ev-start-equipment-landed-levo.png`, and `C:\Games\BasiliskII\ev-start-equipment-levo-commodity-screen.png`.
  - Observed original EV Classic behavior: HUD shows full Shield/Fuel bars, `No Secondary Weapon`, `No Target`, and `Free: 20`; first landing clearance says `Cleared to land, Starseeker. Commence final approach.`; Levo landed screen has `Spaceport Bar`, `Mission Computer`, `Commodity Exchange`, and `Leave`, with no visible outfitter button; Levo Commodity Exchange `In Hold:` column is blank for `Food`, `Industrial`, `Medical`, `Metal`, and `Equipment`.
  - Status: `partial`; verification still needed: open a player/ship info screen or an outfitter/status screen at a port that exposes one, without changing inventory, to record exact starting primary weapons/outfits.

- [x] Levo Commodity Exchange buy/sell prices
  - Evidence label: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat.
  - Primary evidence: original EV Classic running in Basilisk II; local-only captures `C:\Games\BasiliskII\ev-start-equipment-levo-commodity-screen.png`, `C:\Games\BasiliskII\ev-levo-food-after-buy.png`, `C:\Games\BasiliskII\ev-levo-food-after-sell.png`, `C:\Games\BasiliskII\ev-levo-industrial-after-buy.png`, `C:\Games\BasiliskII\ev-levo-industrial-after-sell.png`, `C:\Games\BasiliskII\ev-levo-medical-after-buy.png`, `C:\Games\BasiliskII\ev-levo-medical-after-sell.png`, `C:\Games\BasiliskII\ev-levo-metal-after-buy.png`, `C:\Games\BasiliskII\ev-levo-metal-after-sell.png`, `C:\Games\BasiliskII\ev-levo-equipment-after-buy.png`, and `C:\Games\BasiliskII\ev-levo-equipment-after-sell.png`.
  - Observed original EV Classic behavior: `Buy` purchases 10 tons at a time from the starting shuttle state. Buying 10 tons of each Levo commodity reduced credits by exactly 10 times the displayed price; selling the lot restored credits to `10,000`. Levo same-port sale prices therefore equal displayed buy prices: Food `120`, Industrial `192`, Medical `600`, Metal `144`, Equipment `360`.
  - Terminal Velocity current behavior: `native_ev/data/economy.json` now uses those source-backed Levo sell prices, and `native_ev/tests/test_model.py` asserts the buy and sell prices.
  - Status: `match`; confidence `medium-high` because the observation is direct runtime behavior, while captures remain local-only and only Levo was tested.

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

- [x] Turning rate
  - Evidence label: `decoded-resource-backed` for source field, `terminal-velocity-observed` for current deterministic Godot mapping, and `original-runtime-observed` for bounded arrow-key responsiveness plus candidate template-matched facing deltas.
  - Primary evidence: EV Classic `Data.rez` ship-like record primitive words decoded from `native_ev/data/sourced_ev_structures.json`; EVNEW `CShipResource::Load` reads words 0-8 as cargo, shields, acceleration, max speed, turning, fuel, free mass, armor, shield recharge. Shuttlecraft word 4 is `60`. Original-runtime captures on 2026-05-25 held Right Arrow for `250`, `500`, `1000`, and `2000 ms`, with full-capture diffs staying localized to the ship sprite area. Candidate frame matches from a common `frame_19` baseline were `+5`, `+12`, `+23`, and `+45` cells modulo 36, supporting roughly `22.5` facing cells/sec for Shuttlecraft `turning=60`; local-only captures are under `C:\Games\BasiliskII\ev-turn-multisample-20260525-152121-*`.
  - Terminal Velocity current behavior: `godot_ev/scripts/main.gd` reads `player_ship.turning` and maps Shuttlecraft `60` to `22.5` facing-cells/sec via `turning * 0.375`; deterministic Godot movement log records facing index after N ticks.
  - Status: `partial but implemented`; source field is decoded and wired, runtime turn responsiveness and multi-sample timing are observed, but a frame-aligned or independent timing check is still desirable before treating the constant as final.

- [x] Acceleration curve
  - Evidence label: `decoded-resource-backed` for source field, `terminal-velocity-observed` for current deterministic Godot mapping.
  - Primary evidence: EV Classic `Data.rez` ship-like record word 2. Shuttlecraft acceleration is `979`; Light Freighter acceleration is `428`.
  - Terminal Velocity current behavior: `native_ev/data/ships.json` now carries per-ship `acceleration`; Godot uses the selected ship's value with a compatibility scale for current world units and deterministic thrust logs.
  - Status: `partial`; source field is decoded and wired, but exact EV Classic acceleration integration/friction curve remains unmeasured.

- [x] Max speed and inertial drift
  - Evidence label: `decoded-resource-backed` for source field, `terminal-velocity-observed` for current deterministic Godot mapping.
  - Primary evidence: EV Classic `Data.rez` ship-like record word 3. Shuttlecraft max speed is `413`; Light Freighter max speed is `188`.
  - Terminal Velocity current behavior: `native_ev/data/ships.json` now carries per-ship `maxSpeed`; Godot clamps thrusting velocity to `_ship_max_speed()` and keeps the existing drift damping.
  - Status: `partial`; max-speed field is decoded and wired, but exact original-runtime velocity cap/friction behavior still needs fixed-frame observation.

### Landing and hyperspace loop

- [ ] Land/takeoff state transitions
  - Evidence label: `original-runtime-observed` with archive-sourced ROM/boot-disk provenance caveat.
  - Primary evidence: local-only captures from 2026-05-20 non-strict gameplay learning pass under `C:\Games\BasiliskII\ev-gameplay-learning-*`, plus previous Levo landing captures.
  - Observed original EV Classic behavior: `L` requests landing clearance near Levo; a second `L` lands. Clicking `Leave` from the Levo landing panel launches and shows `Leaving Levo on May 22nd, 2276.` after the passenger-mission acceptance pass.
  - Terminal Velocity current behavior: current Godot landing state should be logged and compared.
  - Status: `partial`; takeoff/landing text is observed, but exact timing and transition animation/sound still need capture.

- [ ] Hyperspace availability and destination selection
  - Evidence label: `original-runtime-observed` for Levo UI/control behavior plus `decoded-resource-backed` for map links where decoded.
  - Primary evidence: preferences capture `C:\Games\BasiliskII\ev-prefs-correct-coords-2.png`, local-only runtime capture `C:\Games\BasiliskII\ev-gameplay-learning-hyperselect-rigel-20260520.png`, and human-takeover landed-state capture `C:\Games\BasiliskII\ev-kathoon-landed-user-demonstrated-2026-05-20.png`.
  - Observed original EV Classic behavior: nav keys are `H` for Hyper Mode, Backslash for Hyper Select, and `J` for Jump. In Hyper Mode from Levo, Backslash selected `Rigel`; jumping too near Levo failed with `Can't initiate hyperspace jump - not yet far enough away from system center.` User demonstrated successful hyperspace to Kathoon and landing; the resulting landed panel at Maxwell's Purchase is screenshot-confirmed with `Free: 2`, `Special: Multiple`, and `Credits: 10,000`.
  - Terminal Velocity current behavior: uses `links` from `native_ev/data/universe.json`; source-backed EV Classic default keys are now the primary Godot controls for this loop (`H` Hyper Mode, Backslash Hyper Select, `J` Jump, `L` land/launch), with former scaffold reset/hyperspace shortcuts removed from those keys.
  - Status: partial; destination selection and near-center failure are screenshot-observed, and successful travel to Kathoon is user-demonstrated with a screenshot-confirmed landed state. Exact route-selection/jump inputs and hyperspace timing still need step-by-step capture.

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
  - Status: `terminal-velocity-observed` 2026-05-19 via `--tv-movement-log` in `godot_ev/scripts/main.gd`; `godot_ev/windows/RunGodot.ps1 -MovementLog` runs it headlessly for repeatable comparison work.
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
