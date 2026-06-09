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
- Lock file: `.hermes/long-running/tv-spec-implementation/continuous-runner.lock`
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

The wrapper is a single Bash process with a PID lock.

Startup contract:

1. Create `.hermes/long-running/tv-spec-implementation/continuous-runner/` if needed.
2. If `continuous-runner.lock` exists and its PID is alive, print `TV_SPEC_CONTINUOUS_ALREADY_RUNNING` and exit `0`.
3. Otherwise write the wrapper PID to `continuous-runner.lock`.
4. Remove the lock on process exit via shell trap.
5. Change directory to `/home/bh/workspaces/loki/terminal-velocity`.
6. Enter the zero-sleep invocation loop.

Loop contract:

1. If `STOP_CONTINUOUS_RUNNER` exists before an invocation starts, print `TV_SPEC_CONTINUOUS_STOP_FILE` and exit `0`.
2. Build a prompt from `docs/prompts/tv-spec-implementation-long-task-prompt.md` plus the wrapper overlay.
3. Run Hermes with:

   ```bash
   /home/bh/.hermes/profiles/loki-game/home/.local/bin/hermes \
     -p loki-game \
     chat -Q --source tv-spec-continuous-runner -t terminal,file,messaging -q "$prompt"
   ```

4. Write stdout/stderr to `.hermes/long-running/tv-spec-implementation/continuous-runner/run-<UTCSTAMP>-<ITERATION>.log`.
5. After Hermes exits, read `.hermes/long-running/tv-spec-implementation/task-ledger.json`.
6. Stop if the Hermes command failed, the ledger is unreadable, the ledger status is terminal/gated, or `active_gate` is set.
7. Otherwise immediately start the next loop iteration with no intentional polling sleep.

Ledger statuses that stop the wrapper:

- `waiting_gate`
- `blocked`
- `failed_terminal`
- `complete`
- any truthy `active_gate`

## Invocation policy

Each Hermes invocation must treat the repo prompt, ledger, event tail, `docs/research/tv-spec.md`, and live backlog as the current operating authority.

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

## Reporting policy

Local reporting:

- Every invocation gets a local log under `.hermes/long-running/tv-spec-implementation/continuous-runner/`.
- Routine increment history goes to `.hermes/long-running/tv-spec-implementation/events.jsonl`.
- The ledger is rewritten only when resumable state changes: current status, active gate, next action, last verification summary, runner policy, or resume prompt.

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

1. Ensure no live wrapper PID owns `continuous-runner.lock`.
2. Remove stale stop/lock files if safe.
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
- `git status --short --branch` in `/home/bh/workspaces/loki/terminal-velocity`
- lock owner PID and live process tree, when wrapper is running
- current `run-*.log` exists and is being written during active invocation
- `task-ledger.json` parses as JSON
- `events.jsonl` parses line-by-line as JSONL
- cron fallback `5430276bcaa5` remains paused unless intentionally resumed

## Non-goals

This artifact does not define:

- EV Classic gameplay truth;
- source/fidelity promotion criteria beyond wrapper reporting boundaries;
- the contents of individual Terminal Velocity slices;
- gateway supervision or provider configuration;
- cross-profile Hermes operations.
