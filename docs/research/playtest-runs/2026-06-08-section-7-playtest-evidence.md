# Section 7 playtest evidence records

Date: 2026-06-08T00:49:37-04:00
Source method: safe local no-human Terminal Velocity runs from WSL.
Controlling workflow: `docs/research/tv-spec.md`, especially the Scenario/evaluator contract and Increment packet contract.

Purpose: apply the section-7 playtest record shape to current safe local runs. These records are Terminal Velocity evidence only; they are not EV Classic fidelity claims.

## Kanban assessment

Kanban decision: not needed for this section-7 execution pass.

Evidence:

- Live branch/status checked: `main`; only the four current compendium-doc edits were dirty before this pass.
- Active TV worker/process check found no Godot/Basilisk/Kanban/Terminal Velocity worker processes.
- `hermes profile list` showed multiple profiles, but this task was one local integration-owner lane: inspect section 7, run safe local probes, record evidence, and update docs.
- `git worktree list` showed only the main checkout.

Reason: no independent durable lanes, no dependency graph, no parallel writable surfaces, and no need for context-survival board state. Per the canonical TV spec rule, Kanban is for durable multi-lane work, not this single-writer local record/update pass.

## Run record: symbolic scenario curriculum

- Goal: exercise the current safe Terminal Velocity symbolic gameplay curriculum and record whether broad automated scenarios pass before treating current behavior as useful playtest evidence.
- Initial state / pilot safety: no original EV Classic runtime or pilot was touched; run used Terminal Velocity scenario fixtures through `tools/run_gameplay_scenarios.py`.
- Player action sequence or macro: `python3 tools/run_gameplay_scenarios.py --all --pretty`.
- Resulting state changes: scenario harness executed 97 scenarios; summary reported `passed=97`, `failed=0`, `total=97`.
- Representative successful loops:
  - `levo_merchant_first_hop`: accepted safe cargo job, bought commodity lot, reached neighbor and landed, completed job.
  - `mission_runner_first_delivery`: accepted reserved cargo job, reached destination, completed delivery, released reserved cargo.
  - `route_planner_refuel_loop`: spent fuel on jump, blocked empty-fuel jump, refueled while landed.
- Problems: none from this run; exact EV Classic fidelity remains pending wherever each scenario’s own labels say original/runtime confirmation is needed.
- Bright spots: broad scenario curriculum remains executable as a speed-layer playtest surrogate and records blocked reasons/checks rather than only success/failure.
- Evidence classification: `terminal-velocity-observed` / scenario-specific scaffold labels; not EV Classic source truth.

## Run record: Godot curriculum help probe

- Goal: verify that current player-facing recovery/help guidance is present as a stable Godot event output rather than only implied by docs or scenario code.
- Initial state / pilot safety: no original EV Classic runtime or pilot was touched; run used the Terminal Velocity Godot no-human probe.
- Player action sequence or macro: `./run_godot.sh tv-gameplay-curriculum-help-log`.
- Resulting state changes: Godot emitted `TV_GAMEPLAY_CURRICULUM_HELP` with `hintCount=98`, `sourceLabel=terminal-velocity-curriculum-scaffold`, and `oracleStatus=help_surface_pending_playtest`.
- Representative observed flags:
  - `hasServiceProvisioningHelp=true`
  - `hasNavigationGuardrailRecoveryHelp=true`
  - `hasCommodityBuyBlockedRecoveryHelp=true`
  - `hasRouteClearReselectRecoveryHelp=true`
- Problems: help surface is explicitly `help_surface_pending_playtest`; this verifies presence/contract, not player comprehension or Classic accuracy.
- Bright spots: the help event preserves source/oracle labels and exposes many recovery loops as machine-checkable player guidance.
- Evidence classification: `terminal-velocity-curriculum-scaffold`; not EV Classic source truth.

## Section-7 compliance check

- Goal recorded: yes.
- Initial state/pilot safety recorded: yes.
- Player action sequence or macro recorded: yes.
- Resulting state changes recorded: yes.
- Problems and bright spots recorded: yes.
- Source-truth classification recorded: yes.

## Next safe follow-up

Use this file as the durable local run-record surface for future manual Godot sessions and no-human probes. Add one dated section per run, keeping Terminal Velocity observations separate from original-runtime, decoded-resource, manual/docs-backed, and EV-family hypothesis claims.
