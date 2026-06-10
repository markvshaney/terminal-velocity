# Git policy history reference (non-normative)

Created: 2026-06-10T13:38:35Z

Purpose: historical reference for how the Terminal Velocity Git checkpoint / push policy changed during the tv-spec long-running-runner incident and repair. This artifact is **not** an execution authority and must not be relied on for future action.

For current action, use the live canonical surfaces instead:

- `docs/research/tv-spec.md`
- `docs/prompts/tv-spec-implementation-long-task-prompt.md`
- `.hermes/long-running/tv-spec-implementation/task-ledger.json`
- `.hermes/long-running/tv-spec-implementation/events.jsonl`
- live `git status`, `HEAD`, and `origin/main`

## Non-normative boundary

This file records history and state as observed when written. It deliberately does not define policy, grant permission, resume a runner, or override any live ledger/spec/prompt. If this artifact conflicts with current live files or user instruction, ignore this artifact for action.

## Source basis for this record

Inspected while creating this artifact:

- `git status --short --branch`
- `git log --oneline -5`
- `git show --stat --oneline --name-only df3c4aa`
- `git show --stat --oneline --name-only 1d07401`
- `tail -n 12 .hermes/long-running/tv-spec-implementation/events.jsonl`
- `docs/research/tv-spec.md` lines 310-376
- `docs/prompts/tv-spec-implementation-long-task-prompt.md` lines 1-55
- `.hermes/long-running/tv-spec-implementation/task-ledger.json` lines 1-148

## Short history

1. Earlier runner behavior treated normal non-force TV pushes as available to the running worker/continuous-runner itself.
2. A headless worker made local checkpoint commits and then tried to push to `origin/main`.
3. The push failed because that worker environment lacked GitHub HTTPS credentials, and later checks showed `gh` was not logged in and SSH auth was unavailable there.
4. The runner/ledger/events represented that as `push_auth_unavailable`, which made missing worker credentials look like a TV development gate.
5. A later authorized Loki Game integration action pushed the accumulated checkpoint and verified `HEAD == origin/main` at `1d074018ce8b3b1727c994fca0d939c930e353c8`.
6. The policy repair then separated two concepts:
   - checkpoint policy: when remote publication is useful or needed;
   - role policy: who may push.
7. Commit `df3c4aa Separate TV runner push authority` updated the canonical prompt/spec/ledger/events so workers and continuous runners do not push. They record `push_ready` when publication is needed. The integration owner performs normal non-force pushes after review and verification.
8. Commit `df3c4aa` was pushed and verified with local `HEAD == origin/main == df3c4aacb5fb08b4ac3ef74127a962ad4bc54b31`.

## Key commits referenced

- `1d07401 Record coordinate scale push gate`
  - touched `.hermes/long-running/tv-spec-implementation/events.jsonl`
  - touched `.hermes/long-running/tv-spec-implementation/task-ledger.json`
  - historical meaning: checkpoint/gate recording around the coordinate scale work and stale push-auth condition.

- `df3c4aa Separate TV runner push authority`
  - touched `.hermes/long-running/tv-spec-implementation/events.jsonl`
  - touched `.hermes/long-running/tv-spec-implementation/task-ledger.json`
  - touched `docs/prompts/tv-spec-implementation-long-task-prompt.md`
  - touched `docs/research/tv-spec.md`
  - historical meaning: current repair that distinguishes checkpoint triggers from push authority.

## Current policy shape at time of writing

Observed in `docs/research/tv-spec.md` and the long-task prompt:

- Commit/push is a durability or coordination action, not the unit of development.
- Checkpoint policy decides when remote publication is needed.
- Role policy decides who may publish.
- Workers/continuous runners may inspect, edit, test, update local docs/backlog/events, and create local checkpoint commits when needed.
- Workers/continuous runners must not run `git push`.
- If a non-integrator worker reaches a checkpoint that needs remote publication, it records `push_ready` with commit SHA, intended files, verifier output, and next action.
- Missing GitHub credentials in a worker are not a TV development gate.
- The integration owner performs final status/diff review, required checkpoint verification, normal non-force push, fetch, `HEAD == origin/main` verification, and checkpoint record.
- Force-push/history rewrite remains gated.

## Current runner/repo state at time of writing

Observed state:

- Branch: `main`
- Remote tracking: `main...origin/main`
- Last pushed repair commit: `df3c4aa Separate TV runner push authority`
- Ledger status: `stopped_by_user`
- Ledger active gate: `null`
- Ledger next resume action: do not auto-resume; if explicitly resumed, remove `STOP_CONTINUOUS_RUNNER` and start the continuation runner in no-push worker mode; integration owner handles `push_ready` checkpoints.
- Known dirty worktree items observed while creating this artifact: `tools/extract_ev_system_semantics.py`, `native_ev/model.py`, `native_ev/scenario_eval.py`, and `native_ev/tests/test_model.py` had unstaged development changes unrelated to this historical reference artifact.

This state snapshot is historical only. Re-check live status before doing anything.

## What this record is not

This record is not:

- a prompt to resume the long-running runner;
- a grant to push, commit, force-push, delete, release, or change settings;
- a replacement for `tv-spec`;
- a replacement for the long-task prompt;
- a source of truth for current Git state after 2026-06-10T13:38:35Z;
- a TODO list or backlog item.

## Lessons captured historically

- The old phrasing mixed “normal non-force pushes are preapproved” with “the active worker may push.”
- That made an environment credential absence look like a product-development blocker.
- The repair keeps normal integration publication available while preventing headless worker credential loops.
- The durable action surfaces are the spec, prompt, ledger, and event log; this file is only a historical marker explaining why they changed.
