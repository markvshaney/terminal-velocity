# Terminal Velocity acceleration plan

Date: 2026-06-07
Source: Loki Game Telegram assistant post at 2026-06-07 09:20:26 EDT, message stored in profile session `20260607_084853_b72a9a`, message id `42847`.

Purpose: preserve the long acceleration/process recommendation as a durable Terminal Velocity process artifact so it is not lost in chat. This is a process artifact, not an EV Classic behavior source.

Canonical summary: this page is part of the Terminal Velocity development compendium. Read `docs/research/terminal-velocity-development-compendium.md` first for current doctrine; keep this page as the acceleration synthesis and deficiency/improvement rationale.

## Decision

The strongest acceleration plan is **source-aligned vertical slices + cheap evaluators + parallel read-only support + one-writer coordination**, not a broad increase in autonomous coding workers.

Operationally:

1. keep one serial implementer/coordinator for repo mutation;
2. use parallel agents primarily for read-only scouting, review, source mining, and test design;
3. make backlog items executable before adding more worker lanes;
4. use deterministic TV scenario/evaluator coverage as the velocity lane;
5. use Basilisk as a bounded source oracle and inline blocker surface, not the main velocity loop;
6. use Kanban, worktrees, and watchdogs only where the coordination cost is justified.

## Source post preserved

Copied exact from the stored Telegram-session message content.

> Summary: the strongest acceleration plan is **not “more autonomous workers everywhere.”** It is **source-aligned vertical slices + cheap evaluators + parallel read-only support + one-writer coordination.**
>
> I inspected the durable artifacts before summarizing: topology doc, source-aligned gameplay method, and Basilisk inline-blocker policy.
>
> ## Core development loop
>
> Default TV loop should be:
>
> 1. Pick **one player-visible or symbolic behavior**
> 2. Find/label source truth:
>    - original EV runtime
>    - decoded resources
>    - manual/docs
>    - EV-family hypothesis
>    - TV-only scaffold
> 3. Implement the smallest useful slice
> 4. Add a **scenario/evaluator/regression**
> 5. Run cheap verification
> 6. Update backlog/docs/provenance
> 7. Commit/push
> 8. Continue unless a real gate appears
>
> This is the fastest safe loop because it avoids large speculative rewrites.
>
> ## Best acceleration levers
>
> ### 1. Make backlog items executable
>
> Backlog items should not be just ideas. Each useful item needs:
>
> - status
> - source/evidence
> - concrete next action
> - verifier
> - expected touched files
> - gates/blockers
>
> First recommended process step remains: **read-only backlog executability audit** before adding more workers.
>
> ### 2. Use vertical slices, not broad systems
>
> Good slice examples:
>
> - map route selection → jump → land → refuel
> - mission offer → accept → reserve cargo → deliver → reward
> - faction branch → incompatible branch blocked
> - outfitter/shipyard compare → purchase → capability changes
>
> A slice is done only when it has behavior, verifier, source label, and docs/backlog update if future behavior is affected.
>
> ### 3. Use scenario/evaluator coverage as the velocity lane
>
> TV-side deterministic scenarios are the fast lane:
>
> - named scenario per capability
> - structured state/action logs
> - blocked reasons, not just pass/fail
> - cheap Python/Godot verification
> - curriculum growth over vague “AI play” goals
>
> Basilisk is source truth, but TV scenarios are where we can iterate quickly.
>
> ### 4. Keep Basilisk as source oracle, not primary velocity tool
>
> Current policy:
>
> - Use Basilisk for bounded original-runtime evidence.
> - If it freezes/input-wedges, treat it as an **inline blocker first**:
>   - capture
>   - wait/capture again
>   - classify process/guest/input/modal state
>   - use known recovery ladder
>   - resume original slice
> - Split Basilisk debugging into its own lane only after recurrence or scope growth.
>
> The four-instance trial showed the Think laptop can host multiple Basilisk processes, but that only proves host load capacity, not long-term guest/EV responsiveness.
>
> ### 5. Parallelize scouting/review, not overlapping writes
>
> Default topology:
>
> - **Serial coordinator/implementer:** owns repo mutation, verification, commit/push.
> - **Parallel read-only scouts:** source mining, code inspection, test design.
> - **Read-only reviewers:** fidelity/spec/test/consolidation review.
> - **One writer per file/resource surface.**
>
> This avoids agent collisions.
>
> ### 6. Use Kanban only for durable multi-lane work
>
> Use Kanban when work naturally splits into lanes:
>
> - evidence/source lane
> - implementation lane
> - verifier/evaluator lane
> - docs/provenance lane
> - fan-in review lane
>
> Do **not** use Kanban for a single failing test or small dependent patch.
>
> ### 7. Use delegate/subagents for synchronous bursts
>
> Useful for:
>
> - read-only source scans
> - codebase inspection
> - test-plan generation
> - second-opinion review
> - post-change spec/fidelity review
>
> Pattern: subagents scout/review; main agent mutates and verifies.
>
> ### 8. Use isolated worktrees only for true parallel coding
>
> If multiple coding workers must edit:
>
> - create separate worktrees/branches
> - assign non-overlapping scopes
> - merge one at a time
> - coordinator runs final tests
> - no independent pushes unless explicitly assigned
>
> ### 9. Add watchdogs for stale state, not overlapping mutation
>
> Good lightweight watchdogs:
>
> - dirty repo/unpushed commit detector
> - backlog items missing next action/verifier
> - docs/provenance drift detector
> - stale gate summary
> - smoke-test cadence
>
> They should report actionable deltas, not noisy heartbeat spam.
>
> ### 10. Add fan-in review after commit trains
>
> After several slices or noisy trains:
>
> - inspect all touched files
> - check docs/tests/source labels agree
> - find repeated patterns
> - propose one consolidation slice
> - refactor repeated surfaces into data/config when appropriate
>
> ## Source hierarchy
>
> Development speed must not weaken fidelity discipline:
>
> 1. **Primary truth:** EV Classic runtime/Basilisk, decoded resources, manuals/docs
> 2. **Hypothesis sources:** EV-family guides/implementations/resources
> 3. **Automation methods:** Voyager/Go-Explore/GVGAI/VPT-style scenario/evaluator patterns
> 4. **General game-dev process:** Godot docs, backlog/vertical-slice/playtesting practices
>
> TV-only observations are useful, but they remain `terminal-velocity-observed` or `scaffold` until original/source-backed.
>
> ## Practical default going forward
>
> Best operating mode:
>
> - **One serial implementer/coordinator**
> - **Small source-aligned playable slices**
> - **Fast TV scenario/evaluator verification**
> - **Basilisk only for bounded source-truth checks**
> - **Parallel read-only scouts/reviewers when useful**
> - **Kanban only for durable multi-lane work**
> - **Worktrees only when true parallel coding is worth the merge cost**
> - **Watchdogs for stale state and gates, not competing repo mutation**
>
> Strongest next move remains: **audit the fidelity backlog for executability and pick the next clean vertical slice with source label, verifier, expected files, and gates already clear.**

## First safe step

Run the **read-only backlog executability audit** before adding more workers or scheduling new mutation-capable automation.

Audit each candidate backlog item for:

- status;
- source/evidence label;
- concrete next action;
- verifier or scenario/evaluator;
- expected touched files;
- gates/blockers.

Then pick the next clean vertical slice with source label, verifier, expected files, and gates already clear.

## Relationship to existing process artifacts

- Extends `docs/research/terminal-velocity-coordination-topology.md` by preserving the later acceleration synthesis that ties topology, vertical slices, evaluators, Basilisk policy, and watchdog/fan-in review together.
- Reinforces `docs/research/source-aligned-game-development-method.md`, especially small source-aligned playable slices with cheap verification.
- Uses `docs/checklists/ev-classic-fidelity-implementation-backlog.md` as the execution surface for the backlog executability audit and next slice selection.
- Aligns with `docs/research/2026-05-20-basilisk-freeze-input-debug.md` for Basilisk as an inline blocker/source-oracle surface, not a permanently separate velocity lane.
