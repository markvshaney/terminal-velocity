# Terminal Velocity coordination topology

Date: 2026-06-06
Source: Loki Game Telegram post at 2026-06-06 15:27:45 EDT, message stored in profile session `bg_152708_d421b5`, message id `37710`.

Purpose: preserve the coordination/worker-efficiency recommendation as a durable Terminal Velocity process artifact. This is a process artifact, not an EV Classic behavior source.

## Decision

Do **not** start by adding a larger autonomous worker pool. Start by making Terminal Velocity work easier to coordinate safely:

1. keep the normal implementation loop serial unless work naturally splits;
2. use parallel workers first for read-only scouting/review/test-design;
3. use Kanban only for durable multi-lane work;
4. use a coordination manifest before any multi-worker coding slice;
5. keep one writer per file/resource surface unless using isolated worktrees and a clear merge plan.

## Source post preserved

> Yes. Biggest efficiency wins are not just “more workers”; they’re **better partitioning + fewer collisions + stronger reusable patterns**.
>
> Recommended order:
>
> 1. **Make the backlog executable, not descriptive**
>    - Each item should have: status, source/evidence, concrete next action, verifier, expected touched files.
>    - Prefer grooming existing `ready` / `needs evidence` items before adding fresh ideas.
>    - This prevents rediscovery and “interesting but inert” backlog growth.
>
> 2. **Split TV work into stable lanes**
>    Good lanes for Terminal Velocity:
>    - **Source/evidence mining**: EV Classic, EV Bible, plug-in manuals, exposed variables, quirks ledger.
>    - **Implementation slice**: one player-visible behavior or fidelity fix at a time.
>    - **Verifier/evaluator**: scenario tests, regressions, Godot/tool smoke, behavior comparison.
>    - **Docs/provenance**: update source-backed notes, backlog, quirk ledger.
>    - **Review/consolidation**: after commit trains, inspect pattern repetition, noisy diffs, missing tests.
>
> 3. **Use parallel workers only where resource ownership is clean**
>    Parallel is useful when tasks touch different resources:
>    - Worker A: read-only evidence mining.
>    - Worker B: implementation in specific files.
>    - Worker C: read-only review/test design.
>    - Coordinator: final diff review, tests, commit/push.
>
>    Avoid parallel writers on the same subsystem unless using isolated worktrees and a clear merge plan.
>
> 4. **Introduce a coordination manifest for bigger slices**
>    Before dispatching workers, write a short manifest:
>    - Objective.
>    - Worker lanes.
>    - One-writer file/resource claims.
>    - Read-only reviewers.
>    - Required verification.
>    - Human gates.
>    - Fan-in rule: who integrates and verifies.
>
>    This is cheap and prevents agent collision.
>
> 5. **Use Kanban for durable multi-worker work**
>    Use Kanban when:
>    - Work should survive context resets.
>    - Multiple profiles/workers should operate asynchronously.
>    - There are natural dependencies: `evidence → implement → review → docs`.
>    - You want auditability.
>
>    Don’t use Kanban just because “faster”; if the next action is one integrated implementation slice, a normal serial loop is cleaner.
>
> 6. **Use `delegate_task` for synchronous bursts**
>    Best for:
>    - Read-only codebase inspection.
>    - Independent research.
>    - Second-opinion review.
>    - Test-plan generation.
>    - Spec compliance review after a change.
>
>    Pattern:
>    - Main agent owns repo mutation.
>    - Subagents scout/review.
>    - Main agent verifies with actual tests and git diff.
>
> 7. **Use isolated worktrees for true parallel coding**
>    If two workers both need to edit code:
>    - Spawn with Hermes `-w` worktree mode or manually create separate git worktrees.
>    - Assign non-overlapping scopes.
>    - Merge one branch at a time.
>    - Coordinator runs final tests and resolves conflicts.
>
> 8. **Generalize repeated bug fixes into skills or checklists**
>    Any repeated pattern should become durable:
>    - EV source-mining procedure.
>    - TV verifier workflow.
>    - Godot smoke-test recipe.
>    - “Classic quirk vs bug” decision checklist.
>    - Commit-train consolidation checklist.
>
>    This reduces future steering more than adding raw worker count.
>
> 9. **Add lightweight automated watchdogs**
>    Useful no-agent/script cron jobs:
>    - Dirty repo / unpushed commit detector.
>    - Backlog items missing next action.
>    - Docs/provenance drift detector.
>    - Test smoke runner on a cadence.
>    - “Open gates” summary.
>
>    These should report only actionable deltas, not noisy status.
>
> 10. **Separate discovery from mutation**
>    Most efficient safe pattern:
>    - First worker reads and reports evidence.
>    - Main/implementer mutates.
>    - Reviewer checks against source + tests.
>    - Coordinator commits/pushes.
>
>    This avoids the common agent failure mode: changing code while still unsure what the source of truth says.
>
> 11. **Use smaller, player-visible vertical slices**
>    For TV specifically, the most productive loop is:
>    - Pick one behavior/fidelity gap.
>    - Find source truth.
>    - Implement smallest visible change.
>    - Add verifier/regression.
>    - Update provenance/backlog.
>    - Commit.
>    - Continue.
>
>    Big multi-system rewrites are less efficient unless we first decompose them into these slices.
>
> 12. **Add a “fan-in reviewer” role**
>    After multiple workers or several commits:
>    - Inspect all touched files.
>    - Check whether docs/tests/source ledger agree.
>    - Look for duplicated logic.
>    - Identify reusable abstractions.
>    - Recommend one consolidation slice.
>
>    This is where pattern generalization should happen, not during every tiny implementation.
>
> My strongest recommendation: **start with a concrete TV coordination topology**, not a larger worker pool immediately.
>
> Default topology:
> - **Serial implementer/coordinator**: me in this thread.
> - **Parallel read-only scouts**: evidence mining, code inspection, test design.
> - **Occasional reviewer**: spec/fidelity and quality review before push.
> - **Kanban only for durable multi-lane backlog work.**
> - **Cron/watchdogs only for stale-state detection, not autonomous overlapping repo mutation.**
>
> If you want, the next safe action is for me to inspect the live TV repo/backlog/profile setup and propose a concrete worker/cron/Kanban topology with exact lanes, gates, and “do not collide” file ownership rules.

## Coordination topology

### Default mode: serial implementation, parallel read-only support

Use this for most Terminal Velocity slices:

- Coordinator/implementer owns repo mutation in the active checkout.
- Read-only scouts can inspect sources, backlog, code, and tests.
- Read-only reviewers can propose test cases, fidelity risks, and consolidation opportunities.
- Coordinator performs all file edits, final verification, commits, and normal non-force pushes.

### Multi-lane Kanban mode

Use Kanban when the slice has durable independent lanes or must survive context resets:

- Evidence/source lane: EV Classic runtime/resources/manuals/EV-family sources; read-only unless updating source/provenance docs.
- Implementation lane: one player-visible or symbolic behavior with explicit file ownership.
- Verifier/evaluator lane: scenario/test/probe design and review; preferably read-only until handed to the coordinator.
- Docs/provenance lane: backlog, quirk ledger, source labels, and continuation notes.
- Fan-in review lane: final diff review, repeated-pattern detection, missing-test scan, and one consolidation recommendation.

### True parallel coding mode

Use only after a manifest exists and only when scopes are non-overlapping or isolated worktrees are available:

- Each coding worker gets an isolated branch/worktree.
- Each worker has explicit file/resource claims.
- Coordinator merges one branch at a time.
- Coordinator runs final integrated tests and resolves conflicts.
- No worker pushes independently unless the coordinator explicitly assigns that publication role.

## Coordination manifest template

Before any bigger/multi-worker slice, write a short manifest with:

- Objective:
- Source/fidelity boundary:
- Live-state preflight:
  - branch/status checked:
  - active TV workers/processes checked:
  - Kanban/cron/watchdog state checked:
  - available Hermes profiles checked:
- Worker lanes:
- Resource claims:
  - `read` surfaces:
  - `review-only` surfaces:
  - `write-exclusive` file/directory/resource claims:
  - `external-effect` claims and approval gate:
- Workspaces for any mutating worker:
  - branch:
  - worktree path:
  - cleanup/merge plan:
- Read-only reviewers:
- Required verification:
- Human gates:
- Fan-in/integration owner:
- Done condition:
- Do-not-redo notes:

## Source cross-check: deficiencies and improvements

This artifact is source-backed process guidance, not an EV Classic behavior source. A 2026-06-06 source pass checked these coordination references:

- Anthropic Claude Code common workflows: plan-before-editing, subagent research, and parallel worktree sessions. Source: `https://docs.anthropic.com/en/docs/claude-code/common-workflows.md`.
- Git worktree documentation: multiple working trees can check out more than one branch at a time; linked worktrees have separate `HEAD`/`index` metadata and should be removed with `git worktree remove`. Source: `https://raw.githubusercontent.com/git/git/master/Documentation/git-worktree.adoc`.
- Karpathy `autoresearch`: one mutable training file, fixed 5-minute eval budget, trusted `val_bpb` metric, TSV logging, and keep/reset rule. Sources: `https://raw.githubusercontent.com/karpathy/autoresearch/master/README.md` and `https://raw.githubusercontent.com/karpathy/autoresearch/master/program.md`.
- Hermes/local coordination guidance: `subagent-driven-development` / `references/multi-agent-resource-coordination.md`, `kanban-orchestrator`, `bounded-autoresearch`, and the live `delegate_task`/`cronjob` tool contracts.

Deficiencies found in the first draft and corrective rules:

1. **Missing live-state preflight.** Before any topology decision, inspect the live repo state, current branch, dirty files, active long-running TV workers, existing Kanban/cron/watchdog state, and available Hermes profiles. Do not assign Kanban profiles by invented names.
2. **Manifest too prose-heavy for collisions.** Add explicit resource claims for files, directories, generated data, local captures, cron jobs, Kanban cards, skills/memory, and external side effects. Use `read`, `review-only`, `write-exclusive`, or `external-effect` claim levels.
3. **Parallel coding needs workspace verification, not just intent.** For true parallel coding, record the actual branch/worktree path for each writer, verify it exists, and require merge-one-at-a-time fan-in. Clean up linked worktrees deliberately after use.
4. **Subagent output is evidence, not proof.** Read-only scouts/reviewers may summarize, but the coordinator must verify returned paths/claims against live files, `git diff`, and real tests before reporting success.
5. **Kanban needs profile discovery and dependency links.** Use Kanban only after `hermes profile list` or equivalent profile discovery. Independent lanes may fan out; dependent lanes must be created with parent links so implementation/review cannot start before evidence exists.
6. **Cron/watchdogs are approval-gated runtime topology.** Keep proposed watchdogs report-only, quiet-on-no-change, and preferably script-only/no-agent. Do not let scheduled LLM runners mutate the same repo surface as a live serial implementer unless a manifest and gate explicitly say so.
7. **Autoresearch is not just “more agents.”** If a TV workflow becomes iterative optimization, define goal, metric, baseline, mutable surface, trusted surface, fixed budget, experiment log, and keep/revert rule before running it. Otherwise treat it as normal source-aligned development or read-only discovery.
8. **Source separation must stay visible.** External agent/workflow sources may improve process only. They do not justify EV Classic behavior claims; EV behavior still requires original runtime, decoded resources, manuals/Bibles, or explicitly labeled EV-family/community evidence.

## First safe step

Run a **read-only backlog executability audit** before adding more workers.

Scope:

- Inspect the live fidelity backlog and current continuation ledger.
- Identify items missing any of: status, source/evidence, concrete next action, verifier, expected touched files, or gate.
- Pick one candidate multi-lane slice where parallel read-only scouting would help and file/resource ownership is clean.
- Produce a coordination manifest for that one slice.
- Do **not** create more autonomous coding workers yet.
- Do **not** mutate the active worker’s code files while the current TV worker is running.

Why this first:

- It improves coordination without increasing collision risk.
- It gives workers clearer contracts before adding capacity.
- It can be done read-only even while the current serial TV development worker is active.
- It turns the prior Telegram recommendation into an executable next decision rather than a broad process wish.

## Relationship to existing process artifacts

- Extends `docs/research/source-aligned-game-development-method.md`, especially its rule to keep the inner loop direct and use Kanban at feature boundaries.
- Uses `docs/checklists/ev-classic-fidelity-implementation-backlog.md` as the execution surface, not this artifact.
- This artifact is the coordination rationale and template; concrete work items should still land in the backlog or Kanban board.
