# Long-Running Task Wrapper Spec

Artifact name: `long-running-task-wrapper-spec`

Status: current operational spec for the Terminal Velocity `tv-spec` continuous wrapper.

Scope: this artifact specifies the wrapper around the long-running `tv-spec` implementation task, not Terminal Velocity gameplay behavior. It is a process/operations artifact and does not create EV Classic fidelity evidence.

Primary implementation surfaces:

- Wrapper script: `/home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh`
- Workdir: `/home/bh/workspaces/loki/terminal-velocity`
- Task state: `.hermes/long-running/tv-spec-implementation/task-ledger.json`
- Event stream: `.hermes/long-running/tv-spec-implementation/events.jsonl`
- Invocation prompt: `docs/prompts/tv-spec-implementation-long-task-prompt.md`
- Per-invocation logs: `.hermes/long-running/tv-spec-implementation/continuous-runner/run-*.log`
- Per-invocation summaries: `.hermes/long-running/tv-spec-implementation/continuous-runner/run-*.summary.json`
- Latest summary sidecar: `.hermes/long-running/tv-spec-implementation/continuous-runner/latest-summary.json`
- Runner index: `.hermes/long-running/tv-spec-implementation/continuous-runner/index.jsonl`
- Runner state: `.hermes/long-running/tv-spec-implementation/continuous-runner/runner-state.json`
- Lock file: `.hermes/long-running/tv-spec-implementation/continuous-runner.lock`
- Lock metadata: `.hermes/long-running/tv-spec-implementation/continuous-runner.lock.json`
- Stop file: `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER`
- Paused cron fallback: job `5430276bcaa5`, `Terminal Velocity tv-spec implementation loop`

## Objective

Run Terminal Velocity development as a continuous, source-aligned, zero-polling-gap loop:

1. invoke Hermes on the `tv-spec` implementation prompt;
2. complete one or more adjacent safe increments in the same lane/subsystem;
3. record compact local state and/or material Telegram progress;
4. inspect the ledger stop conditions;
5. immediately launch the next invocation when no real stop condition exists.

A completed safe increment is a checkpoint, not task completion.

## Wrapper lifecycle

The wrapper is a single Bash process with an atomic `flock` lock and lock metadata.

Startup contract:

1. Create `.hermes/long-running/tv-spec-implementation/continuous-runner/` if needed.
2. Open `continuous-runner.lock` and acquire a non-blocking `flock`.
3. If the lock is already held, print `TV_SPEC_CONTINUOUS_ALREADY_RUNNING` with the metadata PID when available and exit `0`.
4. Write `continuous-runner.lock.json` metadata: `pid`, `ppid`, `host`, `started_at`, `workdir`, `cmdline`, and `lock_kind`.
5. Remove lock metadata and lock file on process exit via shell trap.
6. Change directory to `/home/bh/workspaces/loki/terminal-velocity`.
7. Enter the zero-sleep invocation loop.

Loop contract:

1. If `STOP_CONTINUOUS_RUNNER` exists before an invocation starts, print `TV_SPEC_CONTINUOUS_STOP_FILE` and exit `0`.
2. Generate a fast-start context sidecar containing ledger status/gate/next action, `latest-summary.json` highlights, `git status --short --branch`, and the last 20 event lines.
3. Build a prompt from `docs/prompts/tv-spec-implementation-long-task-prompt.md`, the fast-start context sidecar, and the wrapper overlay.
4. Run Hermes with:

   ```bash
   /home/bh/.hermes/profiles/loki-game/home/.local/bin/hermes \
     -p loki-game \
     chat -Q --source tv-spec-continuous-runner -t terminal,file,messaging -q "$prompt"
   ```

   Test-only overrides are supported for wrapper smoke tests: `TV_SPEC_HERMES_BIN` can point at a fake Hermes-compatible command, and `TV_SPEC_MAX_ITERATIONS=1` stops after one completed iteration.

5. Write stdout/stderr to `.hermes/long-running/tv-spec-implementation/continuous-runner/run-<UTCSTAMP>-<ITERATION>.log`.
6. On known transient transport/provider/time-limit failures, retry up to the configured short retry limit with short backoff; do not retry ledger parse failure, explicit gate, unsafe dirty state, verifier failure, or unknown nonzero exit.
7. After Hermes exits, write `run-<UTCSTAMP>-<ITERATION>.summary.json`, update `latest-summary.json`, append `index.jsonl`, and append one idempotent local `runner_invocation_summary` event keyed by `tv-spec-continuous-runner:<UTCSTAMP>:<ITERATION>:summary`.
8. Read `.hermes/long-running/tv-spec-implementation/task-ledger.json`.
9. Stop if the Hermes command failed after retry classification, the ledger is unreadable, the ledger status is terminal/gated, `active_gate` is set, or the progress token is unchanged for the configured no-progress limit.
10. Otherwise immediately start the next loop iteration with no intentional polling sleep.

Ledger statuses that stop the wrapper:

- `waiting_gate`
- `blocked`
- `failed_terminal`
- `complete`
- any truthy `active_gate`

Progress-token stop:

- The wrapper computes `last_progress_token` from ledger status, active gate, next action, `HEAD`, material git status, material event count, and last material event digest. Material git status excludes generated continuous-runner summaries/index/lock/stop files; material events exclude wrapper `runner_invocation_summary` rows.
- Material progress means at least one of: new verified event ID, changed git tree/commit, changed ledger status, changed active gate, changed next action, or changed verification result.
- If an invocation exits cleanly but the material progress token is unchanged for the configured limit, the wrapper records `status=blocked` with `blocked_reason=no_material_progress_detected_by_continuous_runner` and stops.

## Invocation policy

Each Hermes invocation must treat the repo prompt, ledger, latest summary, event tail, `docs/research/tv-spec.md`, and live backlog as the current operating authority.

Fast-start skim order:

1. ledger status / active gate / next action;
2. `continuous-runner/latest-summary.json`;
3. `git status --short --branch`, `HEAD`, and `origin/main`;
4. last 20 event lines;
5. only the relevant source/backlog/source-code surface needed for the current slice.

Default context policy:

- Do not preload full skills by default.
- Do not expose the `skills` toolset by default.
- Use only `terminal,file,messaging` for routine invocations.
- Load or consult additional skills/docs only when crossing an uncovered surface, changing runner/process policy, hitting a gate, or entering original-runtime/gameplay/operator procedure.

Throughput policy:

- Batch adjacent safe increments inside one invocation when they share lane/subsystem, source-basis family, verifier surface, and understandable dirty working set.
- Stop an invocation at a real gate, failed verifier, subsystem switch, risky/destructive/original-runtime step, checkpoint-policy trigger, cap/handoff boundary, unsafe dirty state, or no-safe-local-slice condition.
- Do not stop just because one safe increment completed.
- Do not inspect or wait on the wrapper process from inside a runner invocation.
- Treat `continuous-runner.lock` as known wrapper state, not development dirty work.
- A tool/time/context cap is a checkpoint boundary, not task completion.
- Gates are resumable states and require status/gate/next-action checkpointing before stop.

## Reporting policy

Local reporting:

- Every invocation gets a local log under `.hermes/long-running/tv-spec-implementation/continuous-runner/`.
- Every invocation gets a machine-readable summary sidecar under `.hermes/long-running/tv-spec-implementation/continuous-runner/`.
- `latest-summary.json` is the compact current-state entrypoint for the next invocation.
- `index.jsonl` records one summary row per invocation and is the retention-safe log index.
- Routine increment history goes to `.hermes/long-running/tv-spec-implementation/events.jsonl`.
- The ledger is rewritten only when resumable state changes: current status, active gate, next action, last verification summary, runner policy, or resume prompt.

Summary sidecar fields include: exit code, retry classification, ledger status, active gate boolean/type, `reported_touched_files`, `git_dirty_summary`, `commits_created`, `pushed_commits`, verifier commands, material next action, `delivery_status`, whether repo changes occurred, progress token/change status, summary/log paths, and retention policy.

Log retention policy: do not delete old full logs until summary/event evidence is sufficient and deletion is explicitly approved. Adding `index.jsonl` bounds inspection cost without deleting task evidence.

Telegram/GameTV reporting:

- Send progress only at material boundaries:
  - gate;
  - failure;
  - checkpoint commit/push;
  - fidelity promotion/demotion;
  - explicit user request;
  - periodic material batch summary.
- Do not send routine wrapper iteration starts.
- Do not send every small verified increment if those increments are part of a coherent local batch.
- Use `delivery_status` in the summary sidecar rather than a channel-specific field name.

Process-manager reporting:

- Launch the wrapper without `watch_patterns` to avoid iteration-start spam.
- `notify_on_complete=true` is allowed for a single completion/failure notice if the wrapper exits.

## Stop and restart procedure

Preferred safe stop:

1. Write `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER`.
2. Wait for the current Hermes child invocation to finish.
3. Confirm the wrapper printed `TV_SPEC_CONTINUOUS_STOP_FILE` and exited `0`.
4. Remove `STOP_CONTINUOUS_RUNNER` and any stale `continuous-runner.lock` only after confirming no live wrapper owns it.

Restart:

1. Ensure no live wrapper process owns the `flock` on `continuous-runner.lock`; use `continuous-runner.lock.json` only as metadata, not as proof by itself.
2. Remove stale stop/lock/lock-metadata files if safe.
3. Start the wrapper as a background process without watch patterns:

   ```bash
   /home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh
   ```

4. Use `notify_on_complete=true` rather than `watch_patterns`.
5. Verify a live wrapper PID, a live child Hermes PID, and the current `run-*.log` path.

Hard stop is reserved for confirmed stuck/unsafe states. Do not kill active dirty development work merely to change wrapper settings unless the user explicitly accepts that risk.

## Cron fallback policy

Cron job `5430276bcaa5` is retained as a paused fallback and must not run concurrently with the continuous wrapper.

Current fallback contract if re-enabled later:

- no default skill attachments;
- toolsets: `terminal,file,messaging`;
- delivery target may remain `telegram:Loki GameTV`, but routine progress should still follow material-boundary policy;
- resume only after confirming no continuous wrapper is active or after intentionally replacing it.

## Safety gates

Wrapper/process changes require care because they can alter live development cadence and messaging. Gate or pause before:

- changing gateway/profile/provider/account/credential config;
- changing unrelated cron/watchdog jobs;
- force-pushing or rewriting history;
- deleting live task state/logs/ledger;
- interrupting active dirty code work;
- publishing raw proprietary assets or non-TV side effects.

Normal coherent non-force TV pushes remain governed by the existing TV project policy and are not specified by this wrapper artifact except as checkpoint/report boundaries.

## Verification checklist

After changing the wrapper, verify:

- `bash -n /home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh`
- `python3 -m unittest native_ev.tests.test_tv_spec_continuous_runner -v`
- the fake-Hermes single-iteration smoke test creates and parses `run-*.summary.json`, `latest-summary.json`, `index.jsonl`, and `runner-state.json` in an isolated temp fixture, not the live task directory
- `git status --short --branch` in `/home/bh/workspaces/loki/terminal-velocity`
- lock owner metadata and live process tree, when wrapper is running
- current `run-*.log` exists and is being written during active invocation
- `latest-summary.json` and any new `run-*.summary.json` parse as JSON
- `index.jsonl` parses line-by-line as JSONL
- `task-ledger.json` parses as JSON
- `events.jsonl` parses line-by-line as JSONL
- cron fallback `5430276bcaa5` live state is checked and remains paused unless intentionally resumed

## Non-goals

This artifact does not define:

- EV Classic gameplay truth;
- source/fidelity promotion criteria beyond wrapper reporting boundaries;
- the contents of individual Terminal Velocity slices;
- gateway supervision or provider configuration;
- cross-profile Hermes operations.
