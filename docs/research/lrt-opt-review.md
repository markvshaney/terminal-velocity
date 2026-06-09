# Long-runner optimization review

Artifact name: `lrt-opt-review`

Status: temporary review artifact for cross-channel review. This is a standalone review of `docs/research/long-running-task-wrapper-spec.md`; it does not modify the source spec.

Scope: process/wrapper improvements only. This does not change Terminal Velocity gameplay behavior or EV Classic fidelity rules.

## Review ask

Which candidates should be promoted into actual wrapper behavior, and in what order?

## Recommendation

Promote in this order:

1. **Machine-readable run summary sidecar**
   - Add `continuous-runner/run-<UTCSTAMP>-<ITERATION>.summary.json`.
   - Update `continuous-runner/latest-summary.json` after every invocation.
   - Include: exit code, ledger status, active gate boolean/type, `reported_touched_files`, `git_dirty_summary`, `commits_created`, `pushed_commits`, verifier commands, material next action, `delivery_status`, and whether repo changes occurred.
   - Reason: biggest development-time win; prevents repeated log/state rediscovery.

2. **Fast-start skim order**
   - Invocation startup should inspect:
     1. ledger status / active gate / next action;
     2. `latest-summary.json`;
     3. `git status --short --branch`;
     4. last 20 event lines;
     5. only the relevant source/backlog surface.
   - Reason: turns summary sidecars into immediate context savings.

3. **Progress token**
   - Add `last_progress_token` or `last_material_event_id` to `task-ledger.json`.
   - If an invocation exits cleanly but token, event tail, git state, and next action are unchanged for N consecutive iterations, stop as `blocked` or `no_safe_local_slice`.
   - Material progress means at least one of: new verified event ID, changed git tree/commit, changed ledger status, changed active gate, changed next action, or changed verification result.
   - Reason: prevents clean no-progress loops and wasted model calls.

4. **Idempotency keys for side effects**
   - Use per-invocation IDs such as `tv-spec-continuous-runner:<UTCSTAMP>:<ITERATION>` for local events and Telegram/checkpoint messages.
   - Check for an existing ID before emitting the same event/report again.
   - Reason: retries/reconnects can otherwise duplicate side effects.

5. **Retry classification**
   - Retry known transient transport/provider/time-limit failures once or twice with short backoff.
   - Stop immediately on ledger parse failure, explicit gate, unsafe dirty state, verifier failure, or unknown nonzero exit.
   - Record retries in summary/event surfaces.
   - Reason: avoid fragile stops without hiding real blockers.

6. **Atomic lock hardening**
   - Replace plain PID-file semantics with `flock` or an atomic lease directory.
   - Store lock metadata: `pid`, `ppid`, `host`, `started_at`, `workdir`, `cmdline`.
   - Reason: avoids stale lock and PID-reuse issues.

7. **Compact baked-in runner rules**
   - Keep critical long-running rules in the prompt/spec because routine invocations intentionally omit full skills:
     - completed slice is a checkpoint, not completion;
     - tool caps are checkpoint boundaries;
     - gates are resumable states;
     - routine progress is local unless material.
   - Reason: preserves safety/process rules on the fast path.

8. **Log retention and index**
   - Add `continuous-runner/index.jsonl` per iteration.
   - Define retention for old full logs only after summary/event evidence exists.
   - Reason: bounds future inspection cost without deleting task evidence unexpectedly.

## Source-backed rationale

- LangGraph durable execution / persistence: checkpointed state, human-in-the-loop pause/resume, recovery from recorded state.
- Temporal durable execution / idempotency: event history, retries/timeouts, idempotent side effects.
- Agent-idempotency guidance: retry/reconnect behavior can duplicate side effects unless progress and side-effect IDs are stable.

## Promotion gate

Before implementing any candidate:

1. pause or safely stop the wrapper;
2. apply the smallest script/prompt change;
3. verify the wrapper script and state files;
4. restart only after confirming no live wrapper PID owns the active lock.

## Verification checklist for implementation

- `bash -n /home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh`
- `git status --short --branch` in `/home/bh/workspaces/loki/terminal-velocity`
- lock owner PID and live process tree, when wrapper is running
- current `run-*.log` exists and is being written during active invocation
- `task-ledger.json` parses as JSON
- `events.jsonl` parses line-by-line as JSONL
- cron fallback `5430276bcaa5` live state is checked and remains paused unless intentionally resumed
