# Source-aligned game development method for Terminal Velocity

Date: 2026-05-28

Purpose: improve Terminal Velocity development method using external game-development/agent-development sources while preserving EV Classic source-of-truth discipline.

This is a process artifact, not an EV Classic behavior source. It governs how to develop faster without letting secondary sources or convenient scaffolds become fidelity claims.

Canonical summary: this page is part of the Terminal Velocity development compendium. Read `docs/research/terminal-velocity-development-compendium.md` first for current doctrine; keep this page as the detailed source hierarchy and gameplay-development method rationale.

## Sources checked

### Project-local sources

- `docs/research/ev-automated-gameplay-learning-synthesis.md`
  - Strongest existing recommendation: use a symbolic/LLM-controller gameplay loop with structured state, bounded actions, cheap verification, scoring, and reusable tactics.
- `docs/research/automated-gameplay-learning-reference-sources.md`
  - Automation references: Voyager, Go-Explore, GVGAI, Google Research game-agent loop, VPT, BrowserGym, WebArena, OSWorld.
- `docs/checklists/ev-classic-fidelity-implementation-backlog.md`
  - Existing live execution surface for source-backed/candidate/needs-evidence gameplay work.

### External sources

- Godot best-practices docs: https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html
  - Use for engine-facing organization, scenes/scripts boundaries, project organization, version-control practice.
- Godot project organization docs: https://docs.godotengine.org/en/stable/tutorials/best_practices/project_organization.html
  - Use for keeping Godot assets/scripts organized instead of accreting a monolithic prototype.
- Game Developer, “Basic Rules for Managing your Game Backlog”: https://www.gamedeveloper.com/game-platforms/basic-rules-for-managing-your-game-backlog
  - Source note: secondary practitioner source. Useful process signal: backlog granularity changes by phase; preproduction tolerates high-level/fluid design, production needs safer breakdown and estimates after vertical slice.
- Game Developer, “Paper Burns: Game Design With Agile Methodologies”: https://www.gamedeveloper.com/design/paper-burns-game-design-with-agile-methodologies
  - Source note: secondary practitioner source. Useful process signal: demonstrable iterations and prioritized vertical slices around critical features.
- Game Developer, “Design 101: Playtesting”: https://www.gamedeveloper.com/design/design-101-playtesting
  - Source note: secondary practitioner source. Useful process signal: playtesting should test player experience, find problems, replicate successes, and use early scattershot tests to compare variants.

## Source hierarchy for this project

1. **EV Classic fidelity truth**
   - Original EV runtime/Basilisk observation.
   - Decoded EV Classic resources.
   - EV Classic manuals/docs or local source artifacts.
2. **Transferable EV-family structure**
   - EV Override/Nova walkthroughs, Bible/data-derived mission records, and EV-family guides.
   - Use for mission/economy/UI architecture hypotheses, not exact Classic behavior.
3. **Automation/game-agent method**
   - Voyager, Go-Explore, GVGAI, VPT, BrowserGym/WebArena/OSWorld style harness patterns.
   - Use for scenario/evaluator/trace/checkpoint design, not game behavior truth.
4. **General game-development process**
   - Godot docs and practitioner game-production sources.
   - Use for workflow, organization, playtesting, vertical-slice/backlog discipline.

## Recommended operating method

Terminal Velocity uses **parallel build lanes with strict fidelity promotion**.

Non-blocking acceleration rule: coordination artifacts should accelerate work, not make every local change wait for topology setup. Use Kanban, extra worktrees, lane-contract audits, and Basilisk lane records when work genuinely splits into durable independent lanes or parallel original-runtime evidence. For one safe-local slice, proceed with direct TDD/source labeling and cheap verification.

### 1. Split build work from fidelity promotion

Use two linked tracks:

- **Build track:** implement playable Terminal Velocity behavior quickly with explicit labels such as `scaffold`, `terminal-velocity-observed`, `source-grounded EV-family`, or `needs original confirmation`.
- **Fidelity gate track:** promote behavior to EV Classic faithful only after original-runtime, decoded-resource, manual/docs, or explicitly weaker evidence is recorded.

This lets incomplete evidence block fidelity claims without blocking broad game completion.

### 2. Classify fidelity learning by bottleneck

Not all fidelity work waits on original-runtime speed.

- **Static/source-mined fidelity:** map topology, planets/systems, stations, landing services, commodities, ships, outfits, weapons, descriptions/text resources, and decoded mission/resource data. These should move through decoded-resource/manual/local-source lanes and structured import/compare pipelines. Basilisk spot-checks ambiguity; it is not the primary data source. Much of the primitive/resource inventory is already learned; remaining static work is semantic promotion, cross-linking, runtime-facing import, and tests. Current promoted semantic manifests include government, mission, weapon, and specialized `jünk` commodity records; broader topology/service/economy promotion remains backlog/static-pass work.
- **UI/state-transition fidelity:** mission board flow, spaceport bar offers, commodity buy/sell semantics, landing/refueling, shipyard/outfitter availability, route setting, hyperspace outcomes, and dialog progression. These can use Basilisk, including accelerated runs after lane-specific reliability checks.
- **Timing/feel fidelity:** acceleration, turn rate, weapon cadence, projectile speed, combat feel, animation timing, input responsiveness, and frame/tick-linked recharge/drain claims. These require 1x confirmation or explicit 1x-vs-accelerated comparison before promotion.

### 3. Build in vertical increments, not serial global slices

Optimize each lane for complete player-visible or system-visible increments:

- map route selection → jump → land → refuel;
- scan offers → accept mission → reserve cargo → deliver → reward;
- choose faction branch → incompatible branch blocked;
- outfitter/shipyard comparison → purchase → changed capability;
- commodity buy/sell → cargo/credits update → scenario assertion.

An increment is done when it has:

- a player-visible Godot behavior or explicit symbolic surrogate;
- a symbolic scenario/evaluator/probe;
- a cheap verification command;
- a source/fidelity label;
- a docs/backlog update if it affects future behavior;
- a mergeable lane handoff when developed in parallel.

### 4. Use Kanban/worktrees for owned executable lanes

Use direct TDD for small dependent changes. Use Kanban and isolated worktrees when work splits into independent lanes:

- missions/story chains;
- economy/commodity trade;
- map/routing/hyperspace;
- landed UI/services;
- combat/AI;
- ships/outfits/weapons/data import;
- tutorial/help/player guidance;
- scenario/evaluator harness;
- source/resource mining;
- Basilisk original-runtime observation lanes.

Each parallel/durable lane needs an owner, expected writable surfaces, verifier, source-label policy, merge contract, and rollback/cleanup plan. Avoid Kanban for line-level patches, while debugging a single failing test, or when one checkout can safely complete the next acceleration slice.

### 5. Maintain linked build and fidelity backlogs

- Live execution checklist: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`.
- Source/process rationale: this artifact and the acceleration/topology artifacts.

Every durable source-driven recommendation should land in the checklist as one of:

- `candidate` — plausible but not ready;
- `needs evidence` — source gap blocks fidelity claim, not necessarily scaffold implementation;
- `ready` — enough evidence to implement or promote safely;
- `implemented` — code exists but may need stronger verification;
- `verified` — implementation and verification evidence exist.

### 6. Add scenario/evaluator coverage as the speed layer

General game-agent sources favor task suites, state archives, and evaluator separation. For Terminal Velocity this means:

- add named scenarios per capability;
- keep action traces structured;
- record blocked reasons, not just success/failure;
- prefer multi-scenario curriculum progress over one large vague “AI play” goal;
- use scenario outcomes to decide what should become player tutorial/hint UI;
- require workers to return verifier output with their handoff.

### 7. Use playtesting as evidence, not just feel

For each playtest/manual run, record:

- goal;
- initial state/pilot safety;
- player action sequence or macro;
- resulting state changes;
- problems and bright spots;
- whether observation is source truth, EV-family hypothesis, or Terminal Velocity-only design.

Current run-record surface: `docs/research/playtest-runs/`. The first applied section-7 safe-local pass is `docs/research/playtest-runs/2026-06-08-section-7-playtest-evidence.md`.

Do not let a fun Terminal Velocity scaffold become an EV Classic fidelity claim unless a primary source supports it.

### 8. Protect source alignment with explicit labels in artifacts and logs

Required labels:

- `original-runtime-observed`
- `decoded-resource-backed`
- `manual/docs-backed`
- `source-grounded EV-family`
- `community-guide`
- `automation-design`
- `terminal-velocity-observed`
- `scaffold`
- `needs original confirmation`

## Immediate process changes applied

- Promote parallel executable lanes as the default development topology, with vertical increments as the quality unit for each lane.
- Preserve strict source hierarchy for fidelity promotion, exact-text claims, physics/economy constants, mission behavior, and Classic quirk decisions.
- Use the existing fidelity backlog as the execution/fidelity surface rather than creating isolated chat-only recommendations.
- Use Kanban/worktrees when work splits across subsystem, observation, verifier, docs, or review lanes.
- Treat missing original evidence as a fidelity gate, not a global build-track stop.

## Next candidate improvements

1. Convert the current high-value backlog items into lane contracts: owner, writable surface, verifier, source-label policy, merge contract, and gate.
2. Split Godot’s growing `main.gd` into source-backed scene/script modules once the next gameplay increment stabilizes. Source basis: Godot best-practice/project-organization docs.
3. Continue adding playtest/run records for manual Godot sessions and no-human probes under `docs/research/playtest-runs/`; first section-7 safe-local record added 2026-06-08. Source basis: playtesting source plus VPT/action-trace references.
4. Add branch/faction/legal scenarios before combat. Source basis: EV-family mission/legal/faction records and current safety policy.
5. Assign Basilisk evidence work to the 4 emulator lanes with explicit disk/prefs/window/input/capture/restore records when the next acceleration question actually needs original-runtime evidence; otherwise keep moving through source/static, Godot scenario, and build-track lanes.
