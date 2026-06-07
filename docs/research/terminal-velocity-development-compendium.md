# Terminal Velocity development compendium

Date: 2026-06-07

Purpose: provide the canonical entry point for Terminal Velocity development method, acceleration, and worker coordination. This is a process artifact, not an EV Classic behavior source.

This compendium summarizes the current operating doctrine. Detailed rationale and provenance remain in:

- `docs/research/source-aligned-game-development-method.md` — source hierarchy and gameplay-development method.
- `docs/research/terminal-velocity-coordination-topology.md` — worker/resource topology, manifest, Kanban/worktree rules.
- `docs/research/2026-06-07-terminal-velocity-acceleration-plan.md` — acceleration synthesis and source-cross-check improvement candidates.
- `docs/checklists/ev-classic-fidelity-implementation-backlog.md` — execution surface for concrete work items.

## Operating doctrine

The default Terminal Velocity loop is **source-aligned vertical slices + cheap evaluators + one-writer coordination**.

1. Pick one player-visible or symbolic behavior.
2. Find and label source truth.
3. Implement the smallest useful slice.
4. Add or update a scenario/evaluator/regression.
5. Run cheap verification.
6. Update backlog/docs/provenance when future behavior is affected.
7. Commit and normally continue unless a real gate appears.

Do not treat “more workers” as the first acceleration move. First make work executable, verifiable, and non-colliding.

## Source hierarchy

Use external workflow/game-agent sources for process improvement only. They do not justify EV Classic behavior claims.

1. **EV Classic fidelity truth**
   - original EV runtime/Basilisk observation;
   - decoded EV Classic resources;
   - EV Classic manuals/docs or local source artifacts.
2. **Transferable EV-family structure**
   - EV Override/Nova walkthroughs, Bible/data-derived mission records, and EV-family guides;
   - use for mission/economy/UI hypotheses, not exact Classic behavior.
3. **Automation/game-agent method**
   - Voyager, Go-Explore, GVGAI, VPT, BrowserGym/WebArena/OSWorld-style harness patterns;
   - use for scenario/evaluator/trace/checkpoint design, not game behavior truth.
4. **General game-development process**
   - Godot docs and practitioner game-production sources;
   - use for workflow, organization, playtesting, vertical-slice/backlog discipline.

Required labels include `original-runtime-observed`, `decoded-resource-backed`, `manual/docs-backed`, `source-grounded EV-family`, `community-guide`, `automation-design`, `terminal-velocity-observed`, `scaffold`, and `needs original confirmation`.

## Definition of Done

A Terminal Velocity slice is done only when:

- a player-visible Godot behavior or explicit symbolic surrogate exists;
- source/fidelity label is attached;
- scenario/evaluator/regression or other cheap verifier passes;
- docs/backlog/provenance are updated if future behavior is affected;
- `git diff` is reviewed for unrelated/proprietary/unsafe changes;
- commit/push gate is satisfied or the remaining gate is explicitly named.

A verified slice is a checkpoint, not necessarily a stop.

## Backlog executability rule

Before adding more worker lanes, audit candidate backlog items for:

- status;
- source/evidence label;
- concrete next action;
- verifier or scenario/evaluator;
- expected touched files/resources;
- gates/blockers.

Prefer grooming existing `ready` / `needs evidence` items before adding fresh ideas. The fidelity backlog remains the execution surface; process docs explain method and rationale.

## Worker and coordination rules

Default mode:

- one serial implementer/coordinator owns repo mutation, verification, commit, and push;
- parallel agents are used first for read-only scouting, source mining, code inspection, review, and test design;
- subagent output is evidence, not proof; coordinator verifies returned paths/claims with live files, diffs, and tests;
- one writer per file/resource surface unless isolated worktrees and a merge plan are explicitly assigned.

Use Kanban only when work has durable independent lanes, must survive context resets, or needs dependency tracking across evidence → implementation → review → docs. Do not use Kanban for line-level patches or a single failing test.

Use isolated worktrees only for true parallel coding. Record each branch/worktree path, file/resource claim, merge order, cleanup plan, and final integrated verification.

## WIP and fan-in defaults

Default conservative limits until a manifest says otherwise:

- active mutation slice: 1;
- read-only scouts: up to 2;
- read-only reviewer/test-design lane: up to 1;
- Basilisk/original-runtime input-driving operator: 1 unless isolation is proven;
- unresolved scout/reviewer reports awaiting coordinator verification: up to 2.

If fan-in exceeds the limit, stop spawning and verify/integrate existing outputs first.

## Scenario/evaluator schema

Cheap TV scenarios are the velocity lane. Each scenario or evaluator should record:

- scenario id/name;
- source/fidelity label;
- starting state, fixture, pilot, or restore method;
- action sequence or macro source;
- expected predicate / success metric;
- blocked reason enum when not successful;
- verification command;
- failure packet path when available;
- artifacts such as logs, screenshots, traces, or JSON events;
- promotion rule from finding → regression/backlog entry.

Semantic Godot probes should produce stable JSON/event outputs when possible. Basilisk/EV Classic capture-driven observations need screenshots/logs and uncertainty labels.

## Basilisk/original-runtime policy

Basilisk is a bounded source oracle and inline blocker surface, not the main velocity loop.

If Basilisk freezes, stalls, foreground/input wedges, or behaves ambiguously:

1. preserve evidence before poking;
2. capture, wait briefly, capture again when useful;
3. classify process responsiveness, guest/display state, EV app state, and input/modal/coordinate failure;
4. use the safe recovery ladder;
5. resume the original slice once usable.

Split Basilisk debugging into a separate lane only when the failure class repeats, the fix is larger than the current slice, TV-side development can proceed without new original-runtime evidence, or all useful Basilisk observation is blocked.

Multiple Basilisk processes proving host capacity is not enough to prove evidence safety. Guest disk, input, window, capture, and state isolation must be verified before parallel original-runtime observations support fidelity claims.

## Watchdog and automation acceptance criteria

Watchdogs should reduce stale-state toil without adding coordination noise.

A TV watchdog should be:

- report-only unless explicitly approved otherwise;
- quiet on no change;
- script-only/no-agent by default;
- no repo mutation;
- specific about the changed file/card/gate/test;
- bounded by an owner, disable path, and noise threshold.

Mutation-heavy exploration, autoresearch, RL/evolutionary loops, or scheduled LLM mutation require a manifest with goal, metric, baseline, mutable surface, trusted surface, budget, experiment log, keep/revert rule, and human gates.

## Acceleration metrics

Use metrics to tell whether process changes actually improve throughput:

- slice lead time: selected → verified/committed;
- backlog executability rate: candidate items with all required fields;
- verifier pass rate: first-pass success vs fixup needed;
- source-gap rate: items blocked by missing EV evidence;
- fan-in load: scout/reviewer outputs awaiting coordinator verification;
- rework rate: reopened slices, reverted commits, docs/test/source-label mismatch.

These are process indicators, not EV fidelity evidence.

## Which artifact to read

- Read this compendium first for current doctrine.
- Read `source-aligned-game-development-method.md` when source hierarchy, vertical-slice method, or playtest/evidence labels matter.
- Read `terminal-velocity-coordination-topology.md` before multi-worker work, Kanban, worktrees, cron/watchdogs, or any coordination manifest.
- Read `2026-06-07-terminal-velocity-acceleration-plan.md` when evaluating acceleration tradeoffs, metrics, and deficiencies/improvements.
- Use `ev-classic-fidelity-implementation-backlog.md` for concrete executable tasks.

## Coordination manifest pointer

Before bigger/multi-worker work, use the manifest template in `docs/research/terminal-velocity-coordination-topology.md` and include at minimum:

- objective;
- source/fidelity boundary;
- live-state preflight;
- worker lanes;
- resource claims;
- workspaces for mutating workers;
- required verification;
- human gates;
- fan-in/integration owner;
- done condition;
- do-not-redo notes.
