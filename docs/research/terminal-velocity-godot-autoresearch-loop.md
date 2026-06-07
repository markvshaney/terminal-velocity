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


Mission alignment branch delivery scenario contract:

- `RunGodot.ps1 -MissionAlignmentDeliveryLog` / `--tv-mission-alignment-delivery-log`
- Exercises the chapter-one alignment branch delivery scaffold in the Godot fast-eval lane after `frontier_samples_delivered`, without claiming exact EV Classic branch-completion UI.
- Runs both branch choices independently: `federation_report_freeport` delivers to Earth and `freeport_pact_smugglers` delivers to Luna.
- Logs branch acceptance/delivery, cargo release, reward payout, branch completion flags (`alignment_federation` / `alignment_freeport` plus asset flags), incompatible branch blockage after delivery, completed mission ids, and story flags.
- `sourceLabel=terminal-velocity-mission-scaffold`; `oracleStatus=mission_behavior_pending_classic_runtime_trace`; `deliveryBoundary=terminal_velocity_alignment_delivery_scaffold_exact_classic_completion_ui_pending`.

Mission alignment return-contract scenario contract:

- `RunGodot.ps1 -MissionAlignmentReturnLog` / `--tv-mission-alignment-return-log`
- Sets the fast-eval state to Sirius Station after `frontier_sample_hera_freeport`, verifies the non-branch return contract (`freeport_return_earth`) appears alongside both open `chapter_one_alignment` branch offers, applies the Federation branch-completed state and verifies only the return contract remains available, then exercises accept/deliver loops for the return contract after both Federation and Freeport branch completion states. The log records:
  - Sirius Station scan system/body;
  - before-branch offer ids (`offersBeforeBranch`) including `freeport_return_earth`, `federation_report_freeport`, and `freeport_pact_smugglers`;
  - `returnContractVisibleWithBranches=true`;
  - post-Federation offer ids (`offersAfterFederation`) with only `freeport_return_earth`;
  - `returnContractVisibleAfterCompletion=true`;
  - `returnContractAcceptedAfterFederation=true` and `returnContractDeliveredAfterFederation=true`;
  - `returnContractAcceptedAfterFreeport=true` and `returnContractDeliveredAfterFreeport=true`;
  - `returnContractCargoReleased=true` for the 5-ton return-contract cargo release in both branch paths;
  - `returnContractRewardPaid=true` for the 3200-credit return-contract reward in both branch paths;
  - `alignmentReturnHelpVisible=true` for the F10 recovery guidance;
  - completed mission ids and story flags used by the timing scaffold;
  - `sourceLabel=terminal-velocity-observed`;
  - `oracleStatus=terminal_velocity_eval_pending_original_trace`;
  - `returnBoundary=terminal_velocity_return_contract_timing_scaffold_exact_classic_offer_ui_pending`.
  This is a Terminal Velocity return-contract timing/playability probe; exact EV Classic Mission Computer refresh timing, UI wording, and branch-chain behavior remain pending original-runtime/manual/resource evidence.

Mission route-hint scenario contract:

- `RunGodot.ps1 -MissionRouteHintLog` / `--tv-mission-route-hint-log`
- Exercises active mission destination → queued route leg in the Godot fast-eval lane.
- Resets to Levo, route-selects Sol, jumps and lands at Earth, accepts `intro_courier_earth_hera`, buys one 10-ton Food trade lot, launches, clears prior map route state, calls `_route_to_active_mission_destination()`, follows the low-fuel/refuel route through Luna delivery, sells the preserved Food lot at the destination market, and logs:
  - whether the Sol route selection succeeded;
  - accepted mission id and destination system;
  - mission acceptance and route queue booleans (`missionAccepted=true`, `missionRouteQueued=true`);
  - stale-route replacement guard (`staleRouteReplaced=true`) proving the `G` helper clears an unrelated queued/manual route before queuing the active mission destination;
  - queued route and route hop count (`route=[...]`, `routeHops`);
  - player-visible route fuel status from the `G` helper (`routeStatusHasFuelHint=true`) and a low-fuel warning branch (`lowFuelRouteWarningVisible=true`, `refuel before full route`);
  - mission/trade cleanup booleans and counters (`tradeBoughtBeforeRoute=true`, `tradeCargoPreservedAfterDelivery=true`, `tradeCargoSoldAfterDelivery=true`, `heldTradeCargoAfterSale=0`, `cargoUsedAfterSale=0`, destination-sale credit increase);
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

Mission abort/reaccept delivery scenario contract:

- `RunGodot.ps1 -MissionAbortReacceptLog` / `--tv-mission-abort-reaccept-log`
- Exercises the Terminal Velocity mission-abort recovery loop in the Godot fast-eval lane while keeping exact EV Classic abort/reoffer UI pending.
- Resets to Levo, route-selects Sol, lands at Earth, accepts `intro_courier_earth_hera`, aborts it, verifies reserved cargo release and reoffer visibility, reaccepts the same scaffold mission, routes to Centauri/Luna, and completes it.
- Logs first acceptance, abort, cargo release after abort, reoffer visibility, reacceptance, cargo reservation after reaccept, final delivery, final cargo release, reward payment, active/completed/aborted history, `sourceLabel=terminal-velocity-mission-abort-reaccept-scaffold`, and `oracleStatus=mission_abort_reaccept_pending_classic_runtime_or_manual_trace`.
- This is a Terminal Velocity mission-state recovery scaffold, not an EV Classic exact reacceptance/UI fidelity claim.

Mission abort-forbidden return-cleanup scenario contract:

- `RunGodot.ps1 -MissionAbortForbiddenLog` / `--tv-mission-abort-forbidden-log`
- Exercises the EV Classic Resource Bible-backed `CanAbort=0` guardrail in the Godot fast-eval lane while keeping exact Classic UI wording pending.
- Seeds deterministic active mission `canabort_return_gate_probe` with `canAbort=false`, `destinationSystem=Centauri`, `destinationBody=Luna`, `cargoTons=3`, and `reward=1800`; attempts abort; then moves to Luna and completes it.
- Logs blocked abort, preserved reserved cargo after the blocked abort, completion at return/destination body, cargo release, reward payment, active/completed/aborted history, `sourceLabel=ev-classic-resource-bible-backed-canabort-guardrail`, and `oracleStatus=classic_runtime_canabort_return_cleanup_pending`.
- This is a source-backed Terminal Velocity guardrail for mission state cleanup; exact EV Classic runtime dialog/status text remains gated on original-runtime/manual evidence.

Mission abort reputation-penalty scenario contract:

- `RunGodot.ps1 -MissionAbortPenaltyLog` / `--tv-mission-abort-penalty-log`
- Exercises the EV Classic Resource Bible-backed abort reputation reversal field in the Godot fast-eval lane while keeping exact Classic abort UI wording pending.
- Seeds deterministic active mission `abort_penalty_probe` with `completionGovernment=Federation`, `completionReward=6`, `abortReputationMultiplier=5`, and `cargoTons=3`; starts Federation reputation at `5`; aborts the job; and logs:
  - `missionAborted=true` and `reservedCargoReleased=true`;
  - `reputationBeforeAbort`, `reputationAfterAbort`, `reputationDelta`, and `expectedReputationDelta`;
  - `reputationPenaltyApplied=true` when the abort applies `-(completionReward * abortReputationMultiplier)`;
  - active mission ids, abort-history count, and latest abort record;
  - `sourceLabel=ev-classic-resource-bible-backed-mission-abort-penalty-scaffold`;
  - `oracleStatus=classic_runtime_abort_penalty_ui_pending`.
- This is a decoded-resource-backed Terminal Velocity guardrail for reputation state; exact EV Classic player-facing abort dialog/status remains gated on original-runtime/manual evidence.

Mission auto-abort completion-bit scenario contract:

- `RunGodot.ps1 -MissionAutoAbortLog` / `--tv-mission-auto-abort-log`
- Exercises the EV Classic Resource Bible-backed mission flag `0x0001` auto-abort contract in the Godot fast-eval lane while keeping exact Classic runtime timing and UI wording pending.
- Seeds deterministic active mission `auto_abort_completion_bit_probe` with `autoAbort=true`, `completionFlags=["auto_abort_completion_bit_77"]`, and `cargoTons=2`; applies the auto-abort transition immediately after acceptance; and logs:
  - `autoAbortedAfterAcceptance=true` and `reservedCargoReleased=true`;
  - `completionFlagsApplied=true`, active mission ids, abort-history count, and latest abort record;
  - `sourceLabel=ev-classic-resource-bible-backed-auto-abort-guardrail`;
  - `oracleStatus=classic_runtime_auto_abort_ui_pending`.
- This is a decoded-resource-backed Terminal Velocity guardrail for mission state/flag cleanup; exact EV Classic auto-abort dialog/status/timing remains gated on original-runtime/manual evidence.

Mission scan-failure scenario contract:

- `RunGodot.ps1 -MissionScanFailureLog` / `--tv-mission-scan-failure-log`
- Exercises the EV Classic Resource Bible-backed `ScanGovt` / `FailIfScanned` mission-cargo contract in the Godot fast-eval lane while keeping exact Classic scan frequency and UI wording pending.
- Seeds deterministic active mission `scan_failure_probe` with `scanGovernment=Federation`, `failIfScanned=true`, `failureBitSet=44`, and `cargoTons=4`; applies a nonmatching `Independent` scan and then a matching `Federation` scan; and logs:
  - `nonmatchingScanPreservedMission=true` and `matchingScanFailedMission=true`;
  - reserved cargo before/after scan and `reservedCargoReleased=true`;
  - `failureFlagSet=true`, active mission ids, failed-history count, and latest failure record;
  - `sourceLabel=ev-classic-resource-bible-backed-mission-scan-failure-scaffold`;
  - `oracleStatus=classic_runtime_scan_failure_ui_pending`.
- This is a decoded-resource-backed Terminal Velocity guardrail for mission scan state; exact EV Classic scan cadence, dialog/status text, and stock mission mapping remain gated on original-runtime/resource evidence.

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

Mission deadline completed-state scenario contract:

- `RunGodot.ps1 -MissionDeadlineCompletedLog` / `--tv-mission-deadline-completed-log`
- Exercises the Terminal Velocity completed-mission deadline guardrail in the Godot fast-eval lane.
- Seeds deterministic mission `deadline_dispatch_completed_probe`, completes it at Luna before the limit, advances to day 3, then attempts the deadline-failure helper and verifies it remains blocked because the mission is no longer active.
- Logs completion, no-late-failure, cargo-release, reward, and reputation booleans (`deadlineMissionCompleted=true`, `lateFailurePrevented=true`, `reservedCargoReleased=true`, `rewardPreserved=true`, `reputationPreserved=true`), completed mission ids, failed-history count, and latest completion record.
- `sourceLabel=terminal-velocity-mission-deadline-completed-no-late-failure-scaffold`; `oracleStatus=deadline_completed_no_late_failure_pending_classic_runtime_or_manual_trace`.
- This is a Terminal Velocity guardrail scaffold; exact EV Classic completed-mission cleanup/UI remains pending runtime/manual evidence.

Mission deadline recovery scenario contract:

- `RunGodot.ps1 -MissionDeadlineRecoveryLog` / `--tv-mission-deadline-recovery-log`
- Exercises the Terminal Velocity post-deadline recovery guardrail in the Godot fast-eval lane.
- Seeds deterministic active mission `deadline_dispatch_failure_probe`, advances beyond `timeLimitDays`, records the failure, releases reserved cargo, then accepts and delivers follow-up mission `deadline_recovery_followup`.
- Logs failure, cargo-release, follow-up acceptance, follow-up delivery, and failed-history preservation booleans (`deadlineFailureRecorded=true`, `reservedCargoReleased=true`, `followupAccepted=true`, `followupDelivered=true`, `failedHistoryPreserved=true`), mission ids, cargo/credit counters, and latest failure/completion records.
- `sourceLabel=terminal-velocity-mission-deadline-recovery-scaffold`; `oracleStatus=deadline_failure_recovery_pending_classic_runtime_or_manual_trace`.
- This is a Terminal Velocity recovery scaffold; exact EV Classic post-failure mission UI, offer refresh timing, and date wording remain pending runtime/manual evidence.

Mission deadline sequential-failures scenario contract:

- `RunGodot.ps1 -MissionDeadlineSequentialLog` / `--tv-mission-deadline-sequential-log`
- Exercises the Terminal Velocity multi-deadline failure guardrail in the Godot fast-eval lane.
- Seeds deterministic active missions `deadline_dispatch_failure_probe` and `deadline_second_failure_probe`, advances both beyond `timeLimitDays`, then verifies both fail in one deadline pass without leaving reserved cargo or active mission ids behind.
- Logs both-failure, reserved-cargo release, two failure flags, and cumulative reputation-penalty booleans (`bothDeadlineFailuresRecorded=true`, `reservedCargoReleased=true`, `failureFlagsSet=true`, `cumulativeReputationPenaltyApplied=true`), active mission ids, failed-history count, failure ids, and latest failure records.
- `sourceLabel=terminal-velocity-mission-deadline-sequential-failures-scaffold`; `oracleStatus=deadline_sequential_failures_pending_classic_runtime_or_manual_trace`.
- This is a Terminal Velocity guardrail scaffold; exact EV Classic simultaneous/multiple deadline UI, ordering, and date-display behavior remain pending runtime/manual evidence.

Mission deadline last-day delivery scenario contract:

- `RunGodot.ps1 -MissionDeadlineLastDayLog` / `--tv-mission-deadline-last-day-log`
- Exercises the current Terminal Velocity deadline-boundary scaffold through Godot: a deterministic timed mission is accepted on day 0, delivered at Luna exactly on day 2 with `timeLimitDays=2`, then the failure helper is attempted and remains blocked because the mission completed.
- Logs last-day completion, no deadline failure, cargo release, reward payment, and reputation-preservation booleans (`lastDayDeliveryCompleted=true`, `deadlineFailurePrevented=true`, `reservedCargoReleased=true`, `rewardPaid=true`, `reputationPreserved=true`), completed mission ids, failed history count, and latest completion record.
- `sourceLabel=terminal-velocity-mission-deadline-last-day-scaffold`; `oracleStatus=deadline_last_day_delivery_pending_classic_runtime_or_manual_trace`.
- This is a Terminal Velocity deadline-boundary guardrail scaffold; exact EV Classic date inclusivity, deadline UI, and failure timing remain pending runtime/manual evidence.

Mission deadline abort scenario contract:

- `RunGodot.ps1 -MissionDeadlineAbortLog` / `--tv-mission-deadline-abort-log`
- Exercises the Terminal Velocity timed-mission abort guardrail in the Godot fast-eval lane.
- Seeds deterministic mission `deadline_dispatch_failure_probe`, aborts it before the deadline, advances past the former limit, then attempts the deadline-failure helper and verifies it remains blocked because the mission is no longer active.
- Logs abort, no-late-failure, cargo-release, no-failure-flag, and reputation-preservation booleans (`deadlineMissionAborted=true`, `lateFailurePrevented=true`, `reservedCargoReleased=true`, `failureFlagPreserved=true`, `reputationPreserved=true`), aborted history count, failed history count, and latest abort record.
- `sourceLabel=terminal-velocity-mission-deadline-abort-scaffold`; `oracleStatus=deadline_abort_pending_classic_runtime_or_manual_trace`.
- This is a Terminal Velocity guardrail scaffold; exact EV Classic abort/deadline interaction, UI wording, and date inclusivity remain pending runtime/manual evidence.

Mission deadline trade-carryover scenario contract:

- `RunGodot.ps1 -MissionDeadlineTradeCarryoverLog` / `--tv-mission-deadline-trade-carryover-log`
- Exercises the Terminal Velocity deadline-failure cleanup boundary when unrelated commodity cargo shares the hold with reserved mission cargo.
- Seeds deterministic mission `deadline_dispatch_failure_probe`, buys an independent commodity lot, advances beyond `timeLimitDays`, applies deadline failure, then sells the preserved commodity cargo.
- Logs mission failure, mission cargo release, trade cargo preservation, sale, failure-flag, and reputation-penalty booleans (`deadlineFailureRecorded=true`, `missionCargoReleased=true`, `tradeCargoPreserved=true`, `tradeCargoSold=true`, `failureFlagSet=true`, `reputationPenaltyApplied=true`) plus cargo/credit/reputation counters and latest failure history.
- `sourceLabel=terminal-velocity-mission-deadline-trade-carryover-scaffold`; `oracleStatus=deadline_failure_trade_carryover_pending_classic_runtime_or_manual_trace`.
- This is a Terminal Velocity guardrail scaffold; exact EV Classic missed-deadline behavior with mixed mission/trade cargo remains pending Classic runtime or manual trace evidence.

Mission trade destination-sale scenario contract:

- `RunGodot.ps1 -MissionTradeDestinationSaleLog` / `--tv-mission-trade-destination-sale-log`
- Exercises the Terminal Velocity mission/trade hybrid loop where a player accepts the intro courier at Earth, buys one Sol Food lot in spare hold space, delivers at Luna, then sells the preserved trade lot at the destination market.
- Logs `missionAccepted=true`, `tradeBoughtBeforeDelivery=true`, `missionDelivered=true`, `tradeCargoPreservedAfterDelivery=true`, and `tradeCargoSoldAtDestination=true` plus cargo, credit, route, and completed-mission counters.
- `sourceLabel=terminal-velocity-mission-trade-destination-sale-scaffold`; `oracleStatus=mission_trade_destination_sale_pending_classic_runtime_trace`.
- This is a Terminal Velocity mission/trade destination-sale scaffold; exact EV Classic mixed mission/trade UI and market behavior remain pending Classic runtime evidence.

Chapter-one trade carryover scenario contract:

- `RunGodot.ps1 -ChapterOneTradeCarryoverLog` / `--tv-chapter-one-trade-carryover-log`
- Exercises the Terminal Velocity chapter-one mission/trade loop where a player accepts the intro courier at Earth, buys one Sol Food lot in spare hold space, delivers at Luna, accepts the follow-up Frontier Sample Transfer, carries the same trade lot alongside the second mission, delivers at Sirius Station, then sells the preserved trade lot.
- Logs `introMissionDelivered=true`, `secondMissionDelivered=true`, `tradeCargoReservedAlongsideSecondMission=true`, `tradeCargoPreservedThroughSecondDelivery=true`, and `tradeCargoSoldAtSiriusStation=true` plus cargo, credit, route, completed-mission, and story-flag counters.
- `sourceLabel=terminal-velocity-chapter-one-trade-carryover-scaffold`; `oracleStatus=chapter_one_trade_carryover_pending_classic_runtime_trace`.
- This is a Terminal Velocity chapter-one mission/trade carryover scaffold; exact EV Classic story-chain, mixed mission/trade UI, and market behavior remain pending Classic runtime evidence.

Mission trade return-margin scenario contract:

- `RunGodot.ps1 -MissionTradeReturnMarginLog` / `--tv-mission-trade-return-margin-log`
- Exercises the Terminal Velocity chapter-one return-leg guardrail where the player completes the intro courier and Frontier Sample Transfer, sells the preserved outbound Food lot at Sirius Station, evaluates Sirius Equipment for resale back at Sol, skips it when the Sol return margin is not positive, then accepts and completes the Freeport Return Dispatch to Earth.
- Logs `introMissionDelivered=true`, `secondMissionDelivered=true`, `returnTradeSkippedForMargin=true`, `heldReturnTradeAfterMarginEval=0`, `returnMissionAccepted=true`, and `returnMissionDelivered=true` plus return price/margin, cargo, completed-mission, and story-flag counters.
- `sourceLabel=terminal-velocity-mission-trade-return-margin-scaffold`; `oracleStatus=chapter_one_return_trade_margin_pending_classic_runtime_trace`.
- This is a Terminal Velocity return-leg trade-margin scaffold; exact EV Classic story-chain, mixed mission/trade UI, and market behavior remain pending Classic runtime evidence.

Trade margin choice scenario contract:

- `RunGodot.ps1 -TradeMarginChoiceLog` / `--tv-trade-margin-choice-log`
- Exercises the Terminal Velocity trade-margin choice scaffold where a pilot compares a profitable Food option with an Equipment option that has a negative return-leg margin, buys/sells the profitable cargo, and leaves the unprofitable cargo out of the hold.
- Logs `profitableCommodity=food`, `unprofitableCommodity=equipment`, `profitableMarginPerTon=60`, `negativeMarginPerTon=-10`, `negativeMarginSkipped=true`, `profitableTradeBought=true`, `profitableTradeSold=true`, and `finalCargo=0` plus route, cargo, and credit counters.
- `sourceLabel=terminal-velocity-trade-margin-choice-scaffold`; `oracleStatus=trade_margin_choice_pending_classic_runtime_trace`.
- This is a Terminal Velocity scaffold for deterministic autoresearch coverage; exact EV Classic commodity-choice UI, price reasoning, and player-facing margin prompts remain pending Classic runtime evidence.

Light Freighter bulk margin scenario contract:

- `RunGodot.ps1 -LightFreighterBulkMarginLog` / `--tv-light-freighter-bulk-margin-log`
- Exercises the Terminal Velocity Light Freighter bulk margin scaffold where the pilot upgrades at Earth, compares a profitable 150-ton Food fill against a negative-margin Equipment candidate, carries only the positive-margin bulk cargo, and sells it at Levo.
- Logs `boughtLightFreighter=true`, `startingCargoSpace=20`, `upgradedCargoSpace=150`, `profitableCommodity=food`, `unprofitableCommodity=equipment`, `profitableMarginPerTon=78`, `negativeMarginPerTon=-210`, `positiveMarginLotsBought=15`, `positiveMarginTonsBought=150`, `negativeMarginSkipped=true`, `bulkCargoCleared=true`, and `finalCargo=0` plus route, ship-price, cargo, and credit counters.
- `sourceLabel=terminal-velocity-light-freighter-bulk-margin-scaffold`; `oracleStatus=light_freighter_bulk_margin_pending_classic_runtime_trace`.
- This is a Terminal Velocity scaffold for deterministic autoresearch coverage; exact EV Classic bulk-hold price reasoning and commodity-choice UI remain pending Classic runtime evidence.

Mission log history scenario contract:

- `RunGodot.ps1 -MissionLogHistoryLog` / `--tv-mission-log-history-log`
- Verifies the Terminal Velocity mission log helper remains useful after mission state transitions leave no active mission.
- Also verifies Player Info mirrors compact mission-history counts and the latest failed mission/reputation delta so a pilot can recover context without reopening the Mission Log.
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
