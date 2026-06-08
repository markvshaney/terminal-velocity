# Terminal Velocity development compendium

Date: 2026-06-07

Purpose: provide the canonical entry point for Terminal Velocity development method, acceleration, and worker coordination. This is a process artifact, not an EV Classic behavior source.

This compendium summarizes the current operating doctrine. Detailed rationale and provenance remain in:

- `docs/research/source-aligned-game-development-method.md` — source hierarchy and gameplay-development method.
- `docs/research/terminal-velocity-coordination-topology.md` — worker/resource topology, manifest, Kanban/worktree rules.
- `docs/research/2026-06-07-terminal-velocity-acceleration-plan.md` — acceleration synthesis and source-cross-check improvement candidates.
- `docs/checklists/ev-classic-fidelity-implementation-backlog.md` — execution surface for concrete work items.

## Operating doctrine

The default Terminal Velocity development system is **parallel executable lanes + fast evaluators + batched integration + fidelity gates**.

Use two coordinated tracks:

1. **Build track** — finish a broad playable Terminal Velocity implementation quickly. Multiple Kanban workers may write in isolated worktrees when each lane has an owner, writable surface, verifier, source/fidelity label policy, and merge contract. Build-track work may be labeled `scaffold`, `terminal-velocity-observed`, `source-grounded EV-family`, or `needs original confirmation` without blocking implementation.
2. **Fidelity gate track** — decide what can be called EV Classic faithful. Strict evidence remains required for original-runtime claims, decoded-resource constants, exact UI text, mission behavior, economy values, movement/physics tuning, and Classic quirk/intentional-TV-divergence decisions.

Vertical slices remain the unit of quality: each worker should still produce player-visible or symbolic behavior with a cheap verifier and source/fidelity label. They are not the global speed limit. Do not serialize all development merely because a fidelity question remains open; label the uncertainty, keep the scaffold moving, and promote only when evidence supports promotion.

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

## Fidelity-learning classes

Do not treat all fidelity learning as emulator-speed limited.

1. **Static/source-mined fidelity** is source/data limited, not Basilisk-speed limited. Map topology, planets/systems, stations, landing services, commodities, ships, outfits, weapons, descriptions/text resources, and decoded mission/resource data should primarily move through decoded-resource/manual/local-source lanes and structured import/compare pipelines. Basilisk is a spot-check and ambiguity-resolution oracle for these surfaces, not the main data source.
2. **UI/state-transition fidelity** is partly runtime-speed limited. Mission board flow, spaceport bar offers, commodity buy/sell semantics, landing/refueling, shipyard/outfitter availability, route setting, hyperspace outcomes, and dialog progression can use Basilisk, including accelerated runs after lane-specific reliability checks.
3. **Timing/feel fidelity** is speed-sensitive. Acceleration, turn rate, weapon cadence, projectile speed, combat feel, animation timing, input responsiveness, and frame/tick-linked recharge/drain claims require 1x confirmation or explicit 1x-vs-accelerated comparison before promotion.

## Definition of Done

A **build-track increment** is done when:

- it implements a player-visible or system-visible behavior, or an explicit symbolic surrogate;
- source/fidelity label is attached;
- a scenario/evaluator/regression/probe or other cheap verifier passes;
- lane artifacts are recorded when work was parallelized;
- docs/backlog/provenance are updated if future behavior is affected;
- the increment is mergeable without colliding with another lane.

A **fidelity-track promotion** is done when:

- the evidence source is original-runtime, decoded-resource, manual/docs, or explicitly weaker;
- uncertainty is labeled;
- TV behavior is compared against the evidence;
- relevant docs/checklists/backlog entries are updated;
- the integration owner verifies the change before canonical promotion.

A verified increment is a checkpoint, not necessarily a stop.

## Backlog executability rule

Before assigning a worker lane, make the candidate executable enough to avoid collision and drift:

- status;
- source/evidence label;
- concrete next action;
- verifier or scenario/evaluator;
- expected touched files/resources;
- owner/lane;
- merge contract;
- gates/blockers.

Backlog grooming is a lane-contract tool, not a reason to fall back to serial development. Prefer grooming existing `ready` / `needs evidence` items into worker-ready lane contracts before adding fresh ideas. The fidelity backlog remains the execution surface; process docs explain method and rationale.

## Worker and coordination rules

Default accelerated mode:

- one integration owner owns final fan-in, diff review, integrated verification, commit, and normal non-force push;
- multiple mutating workers may run in isolated worktrees when a manifest assigns non-overlapping surfaces;
- each worker lane owns a subsystem, worktree, emulator lane, artifact surface, or verifier surface;
- workers may write code/tests/docs inside assigned boundaries;
- subagent/worker output is evidence, not proof; the integration owner verifies returned paths/claims with live files, diffs, and tests;
- one writer per file/resource surface remains mandatory, but it is enforced by lane ownership rather than by banning parallel writing.

Use Kanban when work has durable independent lanes, must survive context resets, or needs dependency tracking across evidence → implementation → review → docs. Do not use Kanban for line-level patches or a single failing test.

Use isolated worktrees for parallel coding. Record each branch/worktree path, file/resource claim, merge order, cleanup plan, and final integrated verification.

## WIP and fan-in defaults

Default accelerated limits until a manifest says otherwise:

- integration owner: 1;
- active mutating worker lanes: 3 initially, scale to 5 after clean integration flow is proven;
- read-only scouts/reviewers: 1-2 when they produce structured evidence packets;
- Basilisk/original-runtime emulator lanes: 4;
- unresolved worker/scout/reviewer reports awaiting integration-owner verification: up to 3.

For Basilisk work, do not write vague capacity language such as “up to 4” or “probably supports four.” The local operating fact is **4 Basilisk emulator lanes**. If a specific lane lacks disk/prefs/window/input/capture/state isolation, mark that lane blocked and fix the lane setup; do not lower the documented emulator count.

If fan-in exceeds the limit, stop spawning and integrate/verify existing outputs first.

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

Basilisk is the original-runtime evidence surface. The local runtime setup has **4 Basilisk emulator lanes**.

Each Basilisk lane needs an unambiguous lane record:

- emulator/lane ID;
- worker/card owner;
- guest disk, prefs file, pilot/save state, and restore method;
- window/process/input target;
- capture directory;
- assigned evidence question;
- allowed mutations;
- status: `ready`, `blocked`, `dirty`, or `needs reset`.

If Basilisk freezes, stalls, foreground/input wedges, or behaves ambiguously:

1. preserve evidence before poking;
2. capture, wait briefly, capture again when useful;
3. classify process responsiveness, guest/display state, EV app state, and input/modal/coordinate failure;
4. use the safe recovery ladder;
5. resume the lane or mark that lane blocked.

Split Basilisk debugging into a separate lane when the failure class repeats, the fix is larger than the current evidence task, TV-side development can proceed without that specific original-runtime evidence, or all useful Basilisk observation is blocked.

Parallel original-runtime observations can support fidelity claims only when each observation packet names its lane record and evidence path. Missing lane records are a setup defect; the emulator count remains 4.

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

Use metrics to tell whether the accelerated model actually improves throughput:

- time to playable increment: selected → verifier passing;
- integration lead time: worker handoff → merged/verified/committed;
- worker lane utilization: active lanes with clear owner/verifier/merge contract;
- backlog executability rate: candidate items with all required fields;
- verifier pass rate: first-pass success vs fixup needed;
- source-gap rate: items blocked only at fidelity promotion, not broad implementation;
- fan-in load: worker/scout/reviewer outputs awaiting integration-owner verification;
- rework rate: reopened increments, reverted commits, docs/test/source-label mismatch;
- schedule target health: whether current throughput supports a 6-10 month playable-TV target.

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
