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
  - selected-offer detail visibility (`selectedOfferDetailsVisible=true`) with generated Mission Computer helper lines for briefing text, destination/route hint, reward, reserved cargo, offer deadline status, visible story/legal/reputation requirement summaries, choice-group/reputation-event/next-contract flags, and source boundary;
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=terminal_velocity_eval_pending_original_trace`.
  The selected-offer detail lines are Terminal Velocity helper scaffolding for player clarity; exact Classic Mission Computer detail UI remains pending original-runtime/manual evidence.

Mission chain offer scenario contract:

- `RunGodot.ps1 -MissionChainOfferLog` / `--tv-mission-chain-offer-log`
- Exercises offer continuity after a completed courier job in the Godot fast-eval lane.
- Resets to Levo, route-selects Sol, accepts and delivers `intro_courier_earth_hera` at Luna, then scans Luna's Mission Computer for the newly unlocked `frontier_sample_hera_freeport` offer and logs:
  - first-mission acceptance and delivery booleans (`firstMissionAccepted=true`, `firstMissionDelivered=true`);
  - completion ids and story flags;
  - chain scan system/body;
  - chain-offer visibility (`chainOfferVisible=true`) and offer ids;
  - selected-chain-offer detail visibility (`selectedChainOfferDetailsVisible=true`) using the same Terminal Velocity helper lines/source boundary as the base offer scan;
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=terminal_velocity_eval_pending_original_trace`.
  This is a Terminal Velocity chain-continuity/playability probe; exact EV Classic Mission Computer offer refresh and detail UI remain pending original-runtime/manual evidence.

Mission chain lock scenario contract:

- `RunGodot.ps1 -MissionChainLockLog` / `--tv-mission-chain-lock-log`
- Exercises blocked story-chain offer reasons before a prerequisite courier job is complete in the Godot fast-eval lane.
- Resets to Levo, route-selects Centauri, jumps and lands at Luna without completing `intro_courier_earth_hera`, then scans Luna's Mission Computer for blocked story-gate reasons around `frontier_sample_hera_freeport` and logs:
  - route and scan context;
  - available-offer count and blocked reason text;
  - `lockedStoryReasonVisible=true` when missing `story_intro_complete` is surfaced to the Mission Computer/log contract;
  - `sourceLabel=terminal-velocity-mission-story-gate-scaffold`;
  - `oracleStatus=classic_mission_offer_visibility_pending_original_trace`.
  This is a Terminal Velocity story-gate visibility scaffold; exact EV Classic behavior for hidden vs disabled/unavailable story-chain offers remains pending original-runtime/manual/resource trace.

Mission alignment branch scenario contract:

- `RunGodot.ps1 -MissionAlignmentBranchLog` / `--tv-mission-alignment-branch-log`
- Continues the intro courier chain through Sirius Station, verifies that both `chapter_one_alignment` branch offers (`federation_report_freeport`, `freeport_pact_smugglers`) become visible, then accepts the Federation branch and verifies the Freeport branch disappears from available offers through the Terminal Velocity choice-group scaffold. The log records:
  - first and chain mission delivery booleans;
  - Sirius Station scan system/body;
  - branch-offer visibility (`branchOffersVisible=true`) for both `federation_report_freeport` and `freeport_pact_smugglers`;
  - shared choice group (`chapter_one_alignment`);
  - selected Federation branch helper details (`selectedBranchOfferDetailsVisible=true`) including route/terms/deadline/requirements/story/source-boundary lines before accepting the branch;
  - `federationBranchAccepted=true` and `freeportBranchHiddenAfterChoice=true`;
  - `choiceBoundary=terminal_velocity_choice_group_scaffold_exact_classic_branch_ui_pending`;
  - reputation snapshot needed by the current Terminal Velocity legal/reputation gates;
  - active/completed mission ids and story flags;
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=terminal_velocity_eval_pending_original_trace`.
  This is a Terminal Velocity story-branch/playability probe; exact EV Classic branch offer UI, random refresh timing, and legal/reputation thresholds remain pending original-runtime/manual/resource evidence.

Mission route-hint scenario contract:

- `RunGodot.ps1 -MissionRouteHintLog` / `--tv-mission-route-hint-log`
- Exercises active mission destination → queued route leg in the Godot fast-eval lane.
- Resets to Levo, route-selects Sol, jumps and lands at Earth, accepts `intro_courier_earth_hera`, launches, clears prior map route state, calls `_route_to_active_mission_destination()`, and logs:
  - whether the Sol route selection succeeded;
  - accepted mission id and destination system;
  - mission acceptance and route queue booleans (`missionAccepted=true`, `missionRouteQueued=true`);
  - stale-route replacement guard (`staleRouteReplaced=true`) proving the `G` helper clears an unrelated queued/manual route before queuing the active mission destination;
  - queued route and route hop count (`route=[...]`, `routeHops`);
  - `sourceLabel=terminal-velocity-design-scaffold`;
  - `oracleStatus=mission_objective_hint_pending_ev_classic_ui_trace`.

Mission abort scenario contract:

- `RunGodot.ps1 -MissionAbortLog` / `--tv-mission-abort-log`
- Exercises active mission abort and reserved cargo release in the Godot fast-eval lane.
- Resets to Levo, route-selects Sol, moves to scripted hyperspace distance, jumps and lands at Earth, accepts `intro_courier_earth_hera`, aborts it without completion, and logs:
  - blocked abort guidance before any mission is active (`noActiveAbortBlocked=true`, `noActiveAbortStatusVisible=true`, `historyBeforeAccept=0`), and blocked repeat-abort guidance after the mission has already been removed (`repeatAbortBlocked=true`, `repeatAbortStatusVisible=true`);
  - whether route selection, mission acceptance, and mission abort succeeded;
  - cargo before accept, after accept, and after abort (`cargoBeforeAccept`, `cargoAfterAccept`, `cargoAfterAbort`);
  - active/completed mission ids plus `abortedHistoryCount` and latest abort record;
  - `reservedCargoReleased=true` when the abort returns reserved cargo to the available hold;
  - `sourceLabel=terminal-velocity-mission-abort-scaffold`;
  - `oracleStatus=mission_abort_pending_classic_runtime_or_manual_trace`.
  This is a Terminal Velocity mission-state scaffold, not an EV Classic abort-semantics fidelity claim.

Mission deadline failure scenario contract:

- `RunGodot.ps1 -MissionDeadlineFailureLog` / `--tv-mission-deadline-failure-log`
- Exercises the EV Classic Resource Bible-backed timed-mission failure scaffold in the Godot fast-eval lane.
- Seeds a deterministic active `deadline_dispatch_failure_probe`, advances beyond its `timeLimitDays`, releases reserved cargo, records `fail_mission_bit_42`, applies the half-`completionReward` Federation reputation penalty, and logs:
  - accepted/current day and time limit (`acceptedDay`, `currentDay`, `timeLimitDays`);
  - reserved cargo before and after failure (`cargoAfterAccept`, `cargoAfterFailure`, `reservedCargoReleased=true`);
  - failure, flag, and reputation booleans (`deadlineFailureRecorded=true`, `failureFlagSet=true`, `reputationPenaltyApplied=true`);
  - active mission ids plus `failedHistoryCount` and latest failure record;
  - `sourceLabel=ev-classic-resource-bible-backed-mission-failure-scaffold`;
  - `oracleStatus=deadline_failure_runtime_ui_pending_classic_trace`.
  This remains a scaffold for exact EV Classic runtime/UI timing until a Basilisk/manual trace confirms player-facing wording and date behavior.

Mission log history scenario contract:

- `RunGodot.ps1 -MissionLogHistoryLog` / `--tv-mission-log-history-log`
- Verifies the Terminal Velocity mission log helper remains useful after mission state transitions leave no active mission.
- Seeds completed, aborted, and failed mission-history records with no active missions, then logs `noActiveVisible=true`, `completedHistoryVisible=true`, `abortedHistoryVisible=true`, and `failedHistoryVisible=true` plus the generated line list.
- Failed mission history lines include the scaffolded deadline counters (`accepted day`, `failed day`, `limit`) and source-boundary line (`Failure source: ev-classic-resource-bible-backed-mission-failure-scaffold; exact Classic UI pending`) so the player can see why the job failed without treating the wording/date display as Classic-confirmed.
- `sourceLabel=terminal-velocity-mission-log-history-scaffold`; `oracleStatus=mission_history_ui_pending_classic_runtime_trace`.
- This is a player-facing helper scaffold, not an EV Classic claim about exact mission-history UI.

Active mission deadline display scenario contract:

- `RunGodot.ps1 -ActiveMissionDeadlineLog` / `--tv-active-mission-deadline-log`
- Verifies the active mission-detail overlay exposes deadline counters before the mission has completed, failed, or been aborted.
- Seeds deterministic mission `active_deadline_display_probe` with `timeLimitDays=5`, `cargoTons=3`, sets `acceptedDay=1` and `currentDay=2`, then logs `deadlineVisible=true` when the generated detail lines include `Deadline: accepted day 1, current day 2, limit 5 day(s), 4 day(s) remaining`.
- The same detail-line contract logs `abortHintVisible=true` and `abortSourceVisible=true` when the active mission explains `X` abort behavior, reserved-cargo release, and the Classic `CanAbort`/UI evidence boundary.
- The probe also verifies the Player Info helper exposes active mission title/destination plus remaining deadline (`playerInfoMissionVisible=true`, `playerInfoDeadlineVisible=true`) under `terminal-velocity-player-info-mission-scaffold` so `P` is useful during mission runs without making a Classic Player Info layout claim.
- Deadline lines also include `Deadline source: terminal-velocity-active-deadline-display-scaffold; exact Classic UI pending`, with `sourceLabel=terminal-velocity-active-deadline-display-scaffold` and `oracleStatus=active_deadline_ui_pending_classic_runtime_trace`.
- This is a Terminal Velocity helper scaffold for player clarity; exact EV Classic date/deadline wording remains pending runtime/manual evidence.

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
- Creates/overwrites a deterministic non-strict, non-player test pilot, accepts the intro courier mission, buys a ship plus outfitter/weapon inventory, saves current pilot state with `F6`-equivalent `_save_current_pilot_file()`, mutates live state including inventory/ship/cargo-space and the Strict Play flag, reopens the saved pilot through the title-screen pilot-file path, and logs:
  - save and resume booleans (`saveSucceeded=true`, `resumeSucceeded=true`);
  - round-trip checks for system, fuel, credits, active mission ids, Strict Play flag, owned outfits, owned weapons, ship id, and cargo-space;
  - active mission ids plus saved/resumed outfit and weapon dictionaries after resume;
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
