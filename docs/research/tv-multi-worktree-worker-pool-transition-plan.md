# TV Multi-Worktree Worker Pool Transition Plan

Status: active transition artifact; Phase 1 MVP implemented in `tools/tv_runner_autostart.py` with tests in `native_ev/tests/test_tv_runner_autostart.py`
Created: 2026-06-15
Last updated: 2026-06-15
Scope: Terminal Velocity long-running development process, worker dispatch, integration batching, and Kanban flow
Canonical context: `docs/research/tv-spec.md`, especially durable parallel/multi-writer work and parallel execution ceilings

## Decision intent

Proceed toward a higher-throughput Terminal Velocity runner model that preserves the last month of safety work while removing the main throughput bottleneck of serial shared-worktree handoffs.

The goal is not unrestricted parallel mutation. The goal is a controlled pipeline:

```text
coordinator keeps worker pool full
→ mutating workers use isolated worktrees/branches
→ completed slices enter a handoff queue
→ integration owner batches compatible handoffs
→ integration owner verifies, commits, pushes coherent checkpoints
→ coordinator continuously backfills safe workers
```

## Why this exists

The current conservative shared-worktree flow protects against collisions:

```text
one shared-worktree worker
→ dirty verified handoff
→ integration/checkpoint/push/gate cleanup
→ autostart next worker
→ repeat
```

That model fixed important failure modes, including buried dirty handoffs, overlapping shared-writer edits, generic `review-required` gates, and micro-push pressure. However, it risks becoming a slow serial process if every completed slice forces the whole development lane to wait for integration before any unrelated work can proceed.

This transition plan preserves the safety invariant — one writer per worktree/file surface — while restoring the original goal: continuous TV development until completion, minimal human intervention, bundled integration, and as much safe parallelism as possible.

## Current-policy continuity

This plan is a topology upgrade, not a reversal of the process doctrine.

Already-established rules that remain valid:

- Workers do not push directly.
- Normal non-force pushes belong to the integration owner.
- `push_ready` means integration-owner handoff, not human review.
- Safe-local verified work should not require human approval.
- The integration owner owns batching, checkpoint selection, push/fetch verification, stale-gate closeout, and successor seeding.
- Shared dirty worktree overlap is unsafe.
- Parallel mutating work requires isolated worktrees/branches, lane contracts, verifiers, rollback/cleanup paths, and fan-in ownership.
- Human intervention is reserved for unsafe/destructive/external/account/credential/config/publication-sensitive or source/fidelity decision gates.

Material change:

- Move from a serial shared-worktree runner to a coordinator-managed worker pool with isolated worktrees and a pending handoff queue.

## Target operating model

### Coordinator

A durable coordinator is the long-running process owner. Individual workers are disposable.

Coordinator responsibilities:

1. Inspect active workers, queued handoffs, blocked gates, repo sync, and backlog.
2. Keep a configured target number of safe workers active.
3. Allocate isolated worktrees/branches for mutating workers.
4. Prefer read-only/scout work when mutating surfaces are saturated or risky.
5. Route completed worker packets into a handoff queue.
6. Ask the integration owner to batch compatible handoffs when thresholds are met.
7. Reclaim stale/dead workers and clean abandoned worktrees only through verified cleanup rules.
8. Report only material transitions: batch published, explicit gate, global verifier failure, repeated conflict, or user-requested status.

### Workers

Mutating workers operate outside the main shared worktree.

Each worker receives:

- task id;
- isolated worktree path;
- branch name;
- allowed writable surfaces;
- oracle/source class;
- required verifier(s);
- closeout contract;
- explicit unsafe gates.

Each worker emits a structured handoff packet with:

- changed files;
- verifier commands and results;
- source/fidelity labels;
- risk class;
- merge/conflict notes;
- exact next suggested slice;
- whether the slice is self-contained or depends on another handoff.

Workers do not push and do not classify dirty state as globally safe. The integration owner owns final fan-in classification.

### Integration owner

The integration owner is a batching coordinator, not a manual review gate and not merely an autostart shim.

Responsibilities:

1. Collect `handoff_ready` packets.
2. Classify by conflict domain, verifier overlap, source/fidelity risk, and dependency relation.
3. Batch compatible handoffs.
4. Split, hold, or requeue incompatible handoffs without blocking unrelated development.
5. Run bundle-level verification.
6. Merge/commit/push coherent checkpoints using normal non-force push policy.
7. Fetch and verify `HEAD == origin/main`.
8. Close stale `push_ready`/process-only gates after verified integration.
9. Feed coordinator with updated backlog state and next recommended worker dispatches.

## Kanban/handoff states

Use explicit flow states instead of broad blocking labels:

- `running` — worker active.
- `handoff_ready` — worker completed a verified slice and emitted a packet.
- `integration_queued` — handoff accepted into batching queue.
- `integrating` — integration owner is processing the handoff/batch.
- `integrated_local` — merged locally, not yet pushed.
- `published` — pushed, fetched, and verified remote equality.
- `blocked:unsafe_gate` — human approval or unsafe action required.
- `blocked:verifier_failure` — verifier failed; scoped to relevant handoff/lane.
- `blocked:merge_conflict` — integration conflict; scoped to relevant handoff/lane.
- `blocked:source_uncertainty` — source/fidelity decision needed.
- `blocked:tooling_global` — verifier/dispatcher/repo infrastructure broken globally.

Avoid generic `review-required`. If a handoff is safe-local and verified, it should become queueable or integrable, not human-gated.

## Parallelism policy

Initial target:

- 3 active mutating workers in isolated worktrees.
- 1–2 read-only scouts/reviewers.
- Up to 3 unresolved worker/scout/reviewer packets awaiting integration-owner verification.

Scale-up condition:

- Increase toward 5 mutating workers only after at least two consecutive multi-lane integrations complete without unresolved merge conflicts, unverified returned paths, or failed integrated verification.

Conflict-domain dispatch should avoid assigning multiple mutating workers to the same high-conflict surface unless the work is mechanically independent.

Example safer parallel mix:

- one static resource/model worker;
- one scenario/evaluator worker;
- one docs/source-provenance worker;
- one read-only Classic research scout;
- one reviewer/verifier lane.

Example unsafe mix:

- three workers all editing the same native model file or generated manifest without a sharding/merge contract.

## Integration batching policy

`push_ready` should feed the integration queue. It should not stop unrelated safe work.

The integration owner should publish when one of these is true:

- enough compatible handoffs accumulated;
- a coherent feature/checkpoint is complete;
- bundle-size trigger reached;
- next work depends on merged result;
- time/context/reset risk makes local divergence costly;
- explicit gate requires clearing a coordination boundary.

Existing bundle-size policy remains useful:

- soft trigger: more than 8 touched files, more than 600 inserted+deleted diff lines, or mixed process-policy plus game/model/data changes;
- hard trigger: more than 15 touched files or more than 1000 inserted+deleted diff lines requires split or explicit integrator justification.

Micro-pushes are avoided by batching compatible handoffs, not by leaving workers idle.

## Estimated performance impact

Rough expected wall-clock savings over the current conservative serial shared-worktree flow:

- conservative: 50–60% faster;
- likely target: 65–75% faster;
- optimistic: 80%+ faster if conflict-domain dispatch and verifier batching work well.

This estimate comes from replacing per-slice serial integration overhead with a pipeline where several isolated workers advance at once and integration overhead is amortized across batches.

Serial model:

```text
worker time + integration time per slice
```

Pipeline model:

```text
max(worker_time / active_workers, integration_time / batch_size)
```

The estimate excludes true product/fidelity unknowns, source-decision gates, global verifier breakage, and human-approval gates.

## Migration plan

### Phase 0: Keep current safety path as fallback

Do not remove the existing shared-worktree autostart/integration path. Treat it as the conservative fallback for single safe-local slices and recovery.

Verification:

- current structured start/resume preflight still passes for clean shared-worktree starts;
- current integration lane still handles dirty shared-worktree handoffs.

### Phase 1: Add queue/state vocabulary

Add explicit state classes for `handoff_ready`, `integration_queued`, `integrated_local`, `published`, and concrete blocked classes.

Tests:

- safe verified worker closeout becomes `handoff_ready`, not generic `review-required`;
- `push_ready` maps to integration queue, not global development stop;
- unsafe gate remains explicit and blocks only affected lane unless marked global.

### Phase 2: Add handoff queue planner

Create deterministic planner output with:

- active workers;
- queued handoffs;
- changed-path/conflict domains;
- compatible batch candidates;
- explicit blockers;
- recommended spawns;
- recommended integration batch.

Tests:

- compatible handoffs batch together;
- conflicting handoffs are held/split;
- unrelated safe backlog still produces spawn recommendations.

### Phase 3: Add isolated worktree allocator

Implement worker worktree/branch allocation:

- deterministic branch names;
- per-task worktree path;
- origin/main base verification;
- cleanup/reclaim contract;
- one writer per file/resource-surface policy.

Tests:

- allocator refuses dirty main worktree when it would make provenance ambiguous;
- allocator creates isolated worktree for safe mutating task;
- stale worktree is reclaimable only when worker is terminal or explicitly superseded.

### Phase 4: Coordinator keeps target worker pool full

Teach coordinator/autostart to maintain target active workers rather than seeding only one successor.

Tests:

- with active count below target and no global gate, coordinator spawns safe non-conflicting workers;
- queued handoff does not prevent unrelated worker spawning;
- global tooling/repo gate prevents new mutating workers but may allow read-only scouts if safe.

### Phase 5: Integration owner batches handoffs

Extend integration owner from single-handoff recovery/publish to queue fan-in.

Tests:

- two compatible handoffs merge and publish as one batch;
- soft bundle trigger causes checkpoint/publish before more successor spawning;
- hard bundle trigger requires split or explicit reason;
- failed bundle verification blocks only the relevant batch/lanes.

### Phase 6: Scale parallelism

Increase target mutating workers from 3 toward 5 only after clean multi-lane integrations.

Tests/metrics:

- conflict rate;
- verifier failure rate;
- average pending handoff age;
- active worker utilization;
- batch size;
- push frequency;
- number of human gates per week;
- elapsed time from handoff_ready to published.

## Non-goals and gates

Non-goals:

- no unrestricted parallel edits in the same dirty worktree;
- no worker direct pushes;
- no force-push/history rewrite;
- no hiding integration authority inside a generic dispatcher;
- no generic `review-required` as a safe-local stop state;
- no cron/LLM implementation fallback as a substitute for the coordinator.

Still gated:

- destructive original EV/runtime mutation;
- external/public/account/credential/config changes;
- force push/history rewrite/releases/settings;
- proprietary/secret ambiguity;
- source/fidelity decisions that materially change gameplay;
- broad architecture changes outside the current TV spec.

## First implementation slice recommendation

Implement the queue/planner before broad worktree spawning.

Smallest useful first slice:

1. Add handoff queue state model and state normalization tests.
2. Add planner dry-run JSON for active workers, queued handoffs, compatible batches, blockers, and recommended spawns.
3. Make existing autostart consume planner output in dry-run only.
4. Prove with tests that a completed safe handoff does not block unrelated worker spawning.
5. Leave actual parallel worktree allocation for the next slice.

This gives immediate process clarity without risking uncontrolled parallel mutation.

## Tracking notes

This artifact is the durable transition plan. Future implementation work should either:

- update this artifact with phase status and links to commits/tests; or
- migrate accepted rules into `docs/research/tv-spec.md` and mark this artifact as superseded by the canonical spec.
