# Source-aligned game development method for Terminal Velocity

Date: 2026-05-28

Purpose: improve Terminal Velocity development method using external game-development/agent-development sources while preserving EV Classic source-of-truth discipline.

This is a process artifact, not an EV Classic behavior source. It governs how to develop faster without letting secondary sources or convenient scaffolds become fidelity claims.

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

### 1. Build in vertical playable slices

Optimize for one complete player-visible loop at a time:

- map route selection → jump → land → refuel;
- scan offers → accept mission → reserve cargo → deliver → reward;
- choose faction branch → incompatible branch blocked;
- outfitter/shipyard comparison → purchase → changed capability.

A slice is done only when it has:

- a player-visible Godot behavior or explicit symbolic surrogate;
- a symbolic scenario/evaluator;
- a cheap verification command;
- a source/fidelity label;
- a backlog/docs update if it affects future behavior.

### 2. Keep the inner loop direct, but use Kanban at feature boundaries

Use direct TDD for small dependent changes. Use Kanban when work splits into independent lanes:

- Godot runtime/UI lane;
- symbolic model/curriculum lane;
- original EV observation lane;
- source research/fidelity-doc lane;
- verification/review lane.

Avoid Kanban for line-level patches or while debugging a single failing test. Use it when multiple cards can run independently or when human-gated observation/review matters.

### 3. Maintain two linked backlogs

- Live execution checklist: `docs/checklists/ev-classic-fidelity-implementation-backlog.md`.
- Source/process rationale: this artifact and the existing automation synthesis.

Every durable source-driven recommendation should land in the checklist as one of:

- `candidate` — plausible but not ready;
- `needs evidence` — source gap blocks fidelity claim;
- `ready` — enough evidence to implement safely;
- `implemented` — code exists but may need stronger verification;
- `verified` — implementation and verification evidence exist.

### 4. Add scenario/evaluator coverage before broad systems

General game-agent sources favor task suites, state archives, and evaluator separation. For Terminal Velocity this means:

- add one named scenario per capability;
- keep action traces structured;
- record blocked reasons, not just success/failure;
- prefer multi-scenario curriculum progress over one large vague “AI play” goal;
- use scenario outcomes to decide what should become player tutorial/hint UI.

### 5. Use playtesting as evidence, not just feel

For each playtest/manual run, record:

- goal;
- initial state/pilot safety;
- player action sequence or macro;
- resulting state changes;
- problems and bright spots;
- whether observation is source truth, EV-family hypothesis, or Terminal Velocity-only design.

Do not let a fun Terminal Velocity scaffold become an EV Classic fidelity claim unless a primary source supports it.

### 6. Protect source alignment with explicit labels in artifacts and logs

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

- Promote the current curriculum approach as the default development method for gameplay systems: one vertical slice, one scenario, one verifier, one source label.
- Use the existing fidelity backlog as the execution surface rather than creating isolated chat-only recommendations.
- Add Kanban only when work splits across observation/model/Godot/docs/review lanes.

## Next candidate improvements

1. Run the read-only backlog executability audit from `docs/research/terminal-velocity-coordination-topology.md` before adding more autonomous workers. Source basis: Loki Game Telegram coordination recommendation preserved in that artifact, plus its 2026-06-06 coordination-source cross-check against Claude Code worktrees/subagents, Git worktrees, Karpathy autoresearch, and Hermes local coordination guidance.
2. Split Godot’s growing `main.gd` into source-backed scene/script modules once the next gameplay slice stabilizes. Source basis: Godot best-practice/project-organization docs.
3. Add playtest/run records for manual Godot sessions, not just automated self-tests. Source basis: playtesting source plus VPT/action-trace references.
4. Add branch/faction/legal scenarios before combat. Source basis: EV-family mission/legal/faction records and current safety policy.
5. Create Kanban cards only for multi-lane work: e.g. “observe original EV mission surfaces” can run separately from “implement TV mission log UI.”
