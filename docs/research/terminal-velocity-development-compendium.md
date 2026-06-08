# Terminal Velocity development compendium

Date: 2026-06-07

Purpose: provide the canonical entry point for Terminal Velocity development method, acceleration, and worker coordination. This is a process artifact, not an EV Classic behavior source.

This compendium summarizes the current operating doctrine. Detailed rationale and provenance remain in:

- `docs/research/source-aligned-game-development-method.md` — source hierarchy and gameplay-development method.
- `docs/research/terminal-velocity-coordination-topology.md` — worker/resource topology, manifest, Kanban/worktree rules.
- `docs/research/2026-06-08-terminal-velocity-topology-implementation-manifest.md` — current safe-local topology application: live preflight, resource claims, lane contracts, Basilisk lane records, and next-burst manifest.
- `docs/research/2026-06-07-terminal-velocity-acceleration-plan.md` — acceleration synthesis and source-cross-check improvement candidates.
- `docs/research/2026-06-07-static-source-fidelity-learning-pass-1.md` — current static/source-mined fidelity inventory and semantic-promotion boundaries.
- `docs/checklists/ev-classic-fidelity-implementation-backlog.md` — execution surface for concrete work items.

## Operating doctrine

The default Terminal Velocity development system is **parallel executable lanes + fast evaluators + batched integration + fidelity gates**, operated aggressively rather than conservatively.

Non-blocking acceleration rule: coordination structure exists to increase throughput, not to delay safe work. Lane-contract audits, Kanban, coordination manifests, isolated worktrees, and Basilisk lane records gate only multi-worker bursts, durable dependency tracking, parallel mutating work, scheduled/watchdog mutation, or parallel original-runtime evidence collection. They do **not** block a single safe-local acceleration slice, source/static semantic promotion, labeled build-track scaffold, or cheap verifier improvement.

Use two coordinated tracks:

1. **Build track** — finish a broad playable Terminal Velocity implementation quickly. Multiple Kanban workers may write in isolated worktrees when each lane has an owner, writable surface, verifier, source/fidelity label policy, and merge contract. Build-track work may be labeled `scaffold`, `terminal-velocity-observed`, `source-grounded EV-family`, or `needs original confirmation` without blocking implementation.
2. **Fidelity gate track** — decide what can be called EV Classic faithful. Strict evidence remains required for original-runtime claims, decoded-resource constants, exact UI text, mission behavior, economy values, movement/physics tuning, and Classic quirk/intentional-TV-divergence decisions.

Vertical slices remain the unit of quality: each worker should still produce player-visible or symbolic behavior with a cheap verifier and source/fidelity label. They are not the global speed limit. Do not serialize all development merely because a fidelity question remains open; label the uncertainty, keep the scaffold moving, and promote only when evidence supports promotion. Default posture is try-first/test-after for safe-local acceleration: attempt the faster build/evidence route, then use verifiers, source labels, and targeted confirmation to decide what can be promoted.

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

1. **Static/source-mined fidelity** is source/data limited, not Basilisk-speed limited. Map topology, planets/systems, stations, landing services, commodities, ships, outfits, weapons, descriptions/text resources, and decoded mission/resource data should primarily move through decoded-resource/manual/local-source lanes and structured import/compare pipelines. Basilisk is a spot-check and ambiguity-resolution oracle for these surfaces, not the main data source. Much of the primitive/resource inventory is already learned; remaining work is semantic promotion, cross-linking, runtime-facing import, and tests. Current promoted static-source semantics include government, mission, weapon, and specialized `jünk` commodity manifests. The current Lane A/E acceleration checkpoint is `static_topology_source_readiness_scout`: a verified read-only evaluator confirming the decoded 67-record `syst-like` / 88-byte primitive run, 9 heuristic system-name seeds, 72 landing-name seeds, and unchanged 10-system runtime subset before topology IDs/names are promoted. Remaining broad topology/service/economy promotions are tracked in the fidelity backlog and static learning pass.
2. **UI/state-transition fidelity** is partly runtime-speed limited. Mission board flow, spaceport bar offers, commodity buy/sell semantics, landing/refueling, shipyard/outfitter availability, route setting, hyperspace outcomes, and dialog progression should use Basilisk aggressively: the Basilisk K setup speeds EV by at least 2x, and evidence/exploration lanes should start there, try faster settings first when lane state can be restored, and test afterward rather than holding back preemptively. Reserve slower confirmation only for disagreements, flaky capture/input behavior, failed post-run checks, or canonical promotion.
3. **Timing/feel fidelity** is speed-sensitive. Acceleration, turn rate, weapon cadence, projectile speed, combat feel, animation timing, input responsiveness, and frame/tick-linked recharge/drain claims may still be explored at accelerated speed, but require 1x confirmation or explicit 1x-vs-accelerated comparison before promotion.

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

Before assigning a multi-worker lane, make the candidate executable enough to avoid collision and drift:

- status;
- source/evidence label;
- concrete next action;
- verifier or scenario/evaluator;
- expected touched files/resources;
- owner/lane;
- merge contract;
- gates/blockers.

Backlog grooming is a lane-contract tool, not a reason to fall back to serial development or pause a safe single-writer slice. Prefer grooming existing `ready` / `needs evidence` items into worker-ready lane contracts before adding fresh ideas when parallelizing. The fidelity backlog remains the execution surface; process docs explain method and rationale.

## Worker and coordination rules

Default accelerated mode:

- one integration owner owns final fan-in, diff review, integrated verification, commit, and normal non-force push;
- multiple mutating workers may run in isolated worktrees when a manifest assigns non-overlapping surfaces;
- each worker lane owns a subsystem, worktree, emulator lane, artifact surface, or verifier surface;
- workers may write code/tests/docs inside assigned boundaries;
- subagent/worker output is evidence, not proof; the integration owner verifies returned paths/claims with live files, diffs, and tests;
- one writer per file/resource surface remains mandatory, but it is enforced by lane ownership rather than by banning parallel writing.

Use Kanban when work has durable independent lanes, must survive context resets, or needs dependency tracking across evidence → implementation → review → docs. Do not use Kanban for line-level patches or a single failing test.

Use isolated worktrees for parallel coding. Record each branch/worktree path, file/resource claim, merge order, cleanup plan, and final integrated verification. Do not require extra worktrees for one checkout doing one safe slice.

- Current automated gameplay worker application: `docs/research/2026-06-08-automatic-gameplay-worker-application.md` turns the automatic-gameplay/game-testing source stack into concrete worker lane types, typed failure packets, packet templates, and immediate Lane E split guidance. Treat it as `automation-design`, not EV Classic behavior proof.
- Current executable topology packet: `docs/research/2026-06-08-terminal-velocity-topology-implementation-manifest.md` implements the first lane-contract audit and is the starting point for any worker burst. It defines five ready lane contracts: static galaxy topology semantics, system service/store provisioning, economy/commodity semantic expansion, mission-family semantic promotion, and deterministic evaluator/playtest packets. Refresh its live-state preflight before launching workers; do not refresh it just to perform one safe-local slice.

## WIP and fan-in defaults

Default accelerated limits until a manifest says otherwise:

- integration owner: 1;
- active mutating worker lanes: 3 initially, scale to 5 after clean integration flow is proven;
- read-only scouts/reviewers: 1-2 when they produce structured evidence packets;
- Basilisk/original-runtime emulator lanes: 4;
- unresolved worker/scout/reviewer reports awaiting integration-owner verification: up to 3.

For Basilisk work, do not write vague capacity language such as “up to 4” or “probably supports four.” The local operating fact is **4 Basilisk emulator lanes**, and Basilisk K speeds EV by at least **2x**. Prefer accelerated original-runtime exploration by default; start from Basilisk K, try faster speeds first when restore state, capture/input reliability, and post-run checks can preserve the needed fidelity, and test afterward rather than holding back initially. If a specific lane lacks disk/prefs/window/input/capture/state isolation, mark that Basilisk lane blocked and fix the lane setup; do not lower the documented emulator count, and do not block non-Basilisk source/static or Godot-scenario acceleration work.

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

Basilisk is the original-runtime evidence surface. The local runtime setup has **4 Basilisk emulator lanes**; Basilisk K speeds EV by at least **2x**, and faster settings should be tried first when fidelity can be checked afterward.

Each Basilisk lane used for parallel or claim-supporting original-runtime evidence needs an unambiguous lane record:

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

Parallel original-runtime observations can support fidelity claims only when each observation packet names its lane record and evidence path. Missing lane records are a setup defect for those Basilisk lanes, not a general build-track blocker; the emulator count remains 4.

## Watchdog and automation acceptance criteria

Watchdogs should reduce stale-state toil without adding coordination noise.

A TV watchdog should be:

- report-only unless explicitly approved otherwise;
- quiet on no change;
- script-only/no-agent by default;
- no repo mutation;
- specific about the changed file/card/gate/test;
- bounded by an owner, disable path, and noise threshold.

Mutation-heavy exploration, autoresearch, RL/evolutionary loops, or scheduled LLM mutation require a manifest with goal, metric, baseline, mutable surface, trusted surface, budget, experiment log, keep/revert rule, and human gates. Ordinary deterministic probes and single safe-local slices do not require this manifest.

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
- Read `source-aligned-game-development-method.md` when source hierarchy, vertical-slice method, or playtest/evidence labels matter. Dated section-7 playtest/run records live under `docs/research/playtest-runs/`.
- Read `terminal-velocity-coordination-topology.md` before multi-worker work, Kanban, extra worktrees, cron/watchdogs, or any coordination manifest; do not treat it as a prerequisite for every single local slice.
- Read `2026-06-08-terminal-velocity-topology-implementation-manifest.md` when actually activating or reviewing the current topology packet: live preflight, resource claims, lane contracts, Basilisk lane records, worktree registry, and next-burst manifest.
- Read `2026-06-07-terminal-velocity-acceleration-plan.md` when evaluating acceleration tradeoffs, metrics, and deficiencies/improvements.
- Use `ev-classic-fidelity-implementation-backlog.md` for concrete executable tasks.

## Coordination manifest pointer

For bigger/multi-worker work, start from the implemented manifest in `docs/research/2026-06-08-terminal-velocity-topology-implementation-manifest.md`, refreshing live state before launch. For a new or different burst, use the manifest template in `docs/research/terminal-velocity-coordination-topology.md` and include at minimum:

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
