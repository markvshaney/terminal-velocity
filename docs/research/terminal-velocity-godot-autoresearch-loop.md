# Terminal Velocity Godot autoresearch loop

Date: 2026-05-28

## Decision

Apply bounded autoresearch to both the original EV Classic runtime and the Godot Terminal Velocity runtime, but keep their authority separate.

- **Basilisk source-oracle lane**: answers what original EV Classic actually does.
- **Godot fast-eval lane**: answers whether Terminal Velocity can reproduce, test, and iterate on that behavior quickly.
- **Bridge gate**: promotes Godot findings only when their premise is source-backed or explicitly labeled as scaffold/hypothesis.

## Basilisk source-oracle lane

Goal: collect narrow, source-of-truth observations from original EV Classic without turning emulator operation into the primary iteration surface.

Trusted surface:

- Local Basilisk/original EV Classic screenshots, traces, and user demonstrations.
- Decoded EV Classic resources and original/manual evidence.

Mutable/output surface:

- `docs/research/original-ev-classic-runtime-observations.md`
- `docs/checklists/ev-classic-behavior-baseline-checklist.md`
- `docs/checklists/ev-classic-fidelity-implementation-backlog.md`
- local-only captures under `C:\Games\BasiliskII\`

Metric/rubric:

- one concrete behavior observed or refuted;
- evidence label assigned (`original-runtime-observed`, `user-demonstrated`, `decoded-resource-backed`, `secondary-hypothesis`, or `unknown`);
- next verification question narrowed if evidence remains partial.

Approval/safety gates:

- no Strict Play;
- no destructive or combat-risk testing on reusable pilots without approval;
- no unattended long-running original-EV play;
- local-only captures remain local.

## Godot fast-eval lane

Goal: use Godot as the cheap structured sandbox for repeated navigation, landing, refuel, mission, trade, and combat-scenario checks.

Trusted/read-only surface:

- Source-backed Basilisk/decoded-resource observations and bridge-gate labels.
- Existing test suite and deterministic Godot logs.

Mutable/output surface:

- Godot scenario log hooks in `godot_ev/scripts/main.gd`.
- Windows launcher switches in `godot_ev/windows/RunGodot.ps1`.
- Contract tests in `native_ev/tests/test_model.py`.
- Local results in `docs/research/ev-gameplay-autoresearch-results.jsonl` and future Godot scenario logs.

Metric/rubric:

- scenario produces structured state/action log;
- scenario objective passes/fails mechanically;
- safety/source label is present;
- regression tests and Godot self-test pass.

First Godot scenario contract:

- `RunGodot.ps1 -MapRouteLog` / `--tv-map-route-log`
- Resets to Levo, opens map-equivalent route state, simulates clicking the first linked destination through the same `_select_map_route_at_position(click_position)` path used by Shift-click input, and logs:
  - current system;
  - selected destination before and after;
  - whether route selection succeeded;
  - whether the green current-to-selected route-line contract is active;
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=user_demonstrated_pending_original_trace`.

Route-jump scenario contract:

- `RunGodot.ps1 -RouteJumpLog` / `--tv-route-jump-log`
- Executes the next select route → jump primitive in the Godot fast-eval lane.
- Resets to Levo, selects the first linked destination through `_select_first_linked_map_route()`, calls `_jump()`, and logs:
  - starting system;
  - selected destination;
  - final system after jump;
  - whether route selection succeeded;
  - whether jump succeeded (`jumpSucceeded=true`/`false`);
  - landed state and reset position;
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=user_demonstrated_pending_original_trace`.

Route-land-refuel scenario contract:

- `RunGodot.ps1 -RouteLandRefuelLog` / `--tv-route-land-refuel-log`
- Executes the first complete select route → jump → land/refuel travel-loop primitive in the Godot fast-eval lane.
- Resets to Levo, selects the first linked destination through `_select_first_linked_map_route()`, records fuel before jump, calls `_jump()`, records fuel after jump, calls `_try_land()` at the arrival spawn, checks whether the landed body exposes refuel-capable service scaffolding, calls `_refuel_current_ship()`, and logs:
  - starting system;
  - selected destination;
  - final system after jump;
  - whether route selection and jump succeeded;
  - landed body and whether landing succeeded (`landingSucceeded=true`/`false`);
  - whether refuel-capable service scaffolding is available (`refuelAvailable=true`/`false`);
  - whether refuel action succeeded (`refuelSucceeded=true`/`false`);
  - fuel quantities before/after jump and before/after refuel (`fuelBeforeJump`, `fuelAfterJump`, `fuelBeforeRefuel`, `fuelAfterRefuel`, `fuelMax`);
  - whether the complete travel loop passed (`travelLoopComplete=true`/`false`);
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=user_demonstrated_pending_original_trace`.

Low-fuel jump scenario contract:

- `RunGodot.ps1 -LowFuelJumpLog` / `--tv-low-fuel-jump-log`
- Exercises a blocked low-fuel jump in the Godot fast-eval lane.
- Resets to Levo, selects the first linked destination through `_select_first_linked_map_route()`, sets player fuel to zero, records fuel before jump, calls `_jump()`, records fuel after jump, and logs:
  - starting system;
  - selected destination;
  - final system after the blocked jump attempt;
  - whether route selection succeeded;
  - whether the jump was blocked (`jumpBlocked=true`/`false`);
  - block reason (`blockReason=insufficient_fuel`);
  - fuel quantities before/after the blocked jump (`fuelBeforeJump`, `fuelAfterJump`, `fuelMax`);
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=user_demonstrated_pending_original_trace`.

Mission offer scan scenario contract:

- `RunGodot.ps1 -MissionOfferScanLog` / `--tv-mission-offer-scan-log`
- Exercises landed mission-offer discovery without accepting a mission in the Godot fast-eval lane.
- Resets to Levo, route-selects Sol with `_select_map_route_to_system("Sol")`, jumps and lands at Earth, reads `_available_missions()` from the Mission Computer surface, and logs:
  - whether route selection succeeded;
  - scan system/body;
  - mission offers grouped by surface (`offersBySurface={"Mission Computer":[...]}`);
  - total offer count (`totalOffers`);
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=terminal_velocity_eval_pending_original_trace`.

Mission route-hint scenario contract:

- `RunGodot.ps1 -MissionRouteHintLog` / `--tv-mission-route-hint-log`
- Exercises active mission destination → queued route leg in the Godot fast-eval lane.
- Resets to Levo, route-selects Sol, jumps and lands at Earth, accepts `intro_courier_earth_hera`, launches, clears prior map route state, calls `_route_to_active_mission_destination()`, and logs:
  - whether the Sol route selection succeeded;
  - accepted mission id and destination system;
  - mission acceptance and route queue booleans (`missionAccepted=true`, `missionRouteQueued=true`);
  - queued route and route hop count (`route=[...]`, `routeHops`);
  - `sourceLabel=terminal-velocity-design-scaffold`;
  - `oracleStatus=mission_objective_hint_pending_ev_classic_ui_trace`.

First mission delivery scenario contract:

- `RunGodot.ps1 -FirstMissionDeliveryLog` / `--tv-first-mission-delivery-log`
- Exercises the first deterministic accept mission → route → jump → land → complete delivery loop in the Godot fast-eval lane.
- Resets to Levo, route-selects Sol with `_select_map_route_to_system("Sol")`, jumps and lands at Earth, accepts the first available mission (`intro_courier_earth_hera`), launches, route-selects Centauri, jumps, positions at Luna, lands, completes arrived missions, and logs:
  - whether each route selection succeeded;
  - accepted mission id and destination system/body;
  - mission acceptance and delivery booleans (`missionAccepted=true`, `missionDelivered=true`);
  - completed mission ids;
  - credits before accept, credits after delivery, and reward (`creditsBeforeAccept`, `creditsAfterDelivery`, `reward`);
  - cargo before accept, after accept, and after delivery (`cargoBeforeAccept`, `cargoAfterAccept`, `cargoAfterDelivery`);
  - remaining active missions and story flags;
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=terminal_velocity_eval_pending_original_trace`.

Pilot save/resume scenario contract:

- `RunGodot.ps1 -PilotSaveResumeLog` / `--tv-pilot-save-resume-log`
- Exercises save → mutate → reopen pilot in the Godot fast-eval lane as a Terminal Velocity persistence scaffold, not an EV Classic pilot-file fidelity claim.
- Creates/overwrites a deterministic non-strict, non-player test pilot, accepts the intro courier mission, saves current pilot state with `F6`-equivalent `_save_current_pilot_file()`, mutates live state including the Strict Play flag, reopens the saved pilot through the title-screen pilot-file path, and logs:
  - save and resume booleans (`saveSucceeded=true`, `resumeSucceeded=true`);
  - round-trip checks for system, fuel, credits, active mission ids, and Strict Play flag;
  - active mission ids after resume;
  - `sourceLabel=terminal-velocity-save-scaffold`;
  - `oracleStatus=save_resume_pending_ev_classic_file_trace`.

## Bridge gate

A Godot behavior can be optimized freely only when one of these is true:

1. It is backed by original-runtime, decoded-resource, or user-demonstrated evidence.
2. It is explicitly marked `scaffold` or `hypothesis` and cannot be cited as EV Classic fidelity proof.
3. It is a pure Terminal Velocity instrumentation/test helper with no fidelity claim.

If Godot exploration exposes ambiguity, route back to Basilisk with a narrow source-oracle question rather than treating the Godot result as truth.

## Current bridge state

Shift-click map routing is approved for the first Godot fast-eval scenario because the user demonstrated the original behavior: holding Shift and clicking the next available map stop draws a green route line connecting current system to the next system. Exact original-runtime timing/input trace remains pending, so the Godot log must retain `oracleStatus=user_demonstrated_pending_original_trace` until a captured Basilisk trace confirms it.

## Verification commands

```bash
python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_map_route_autoresearch_log_contract
python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_route_jump_autoresearch_log_contract
python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_route_jump_land_refuel_autoresearch_log_contract
python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_low_fuel_jump_autoresearch_log_contract
python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_mission_offer_scan_autoresearch_log_contract
python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_mission_destination_route_hint_log_contract
python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_first_mission_delivery_autoresearch_log_contract
python3 -m unittest native_ev.tests.test_model.NativeEvModelTests.test_godot_pilot_save_resume_log_contract
python3 -m unittest native_ev.tests.test_model -q
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w godot_ev/windows/RunGodot.ps1)" -MapRouteLog
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w godot_ev/windows/RunGodot.ps1)" -RouteJumpLog
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w godot_ev/windows/RunGodot.ps1)" -RouteLandRefuelLog
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w godot_ev/windows/RunGodot.ps1)" -LowFuelJumpLog
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w godot_ev/windows/RunGodot.ps1)" -MissionOfferScanLog
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w godot_ev/windows/RunGodot.ps1)" -MissionRouteHintLog
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w godot_ev/windows/RunGodot.ps1)" -FirstMissionDeliveryLog
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w godot_ev/windows/RunGodot.ps1)" -PilotSaveResumeLog
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(wslpath -w godot_ev/windows/RunGodot.ps1)" -SelfTest
```
