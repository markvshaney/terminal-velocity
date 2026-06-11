# New-session handoff — TV spec topology/cron cleanup

Audience: next Loki Game / Terminal Velocity session.

## Objective

Resume Terminal Velocity runner/topology debugging without repeating the cron-as-terminal-execution mistake.

The immediate goal is **not** to restart the runner blindly. The next session should first verify the topology checker and tests with real terminal access, then decide whether to remove `STOP_CONTINUOUS_RUNNER` and start the canonical runner.

## Current state verified in this Telegram session

This Telegram session did **not** expose direct terminal/shell execution. A delegated verification attempt also lacked shell execution. Do not infer that commands below were run here.

Readbacks and tool state from this session:

- `cronjob list` after cleanup returned `count: 0`.
- `~/.hermes/profiles/loki-game/cron/jobs.json` contains `"jobs": []`.
- `~/.hermes/profiles/loki-game/processes.json` is `[]`.
- `~/.hermes/profiles/loki-game/run/tv_kanban_continuous_loop_state.json` has `last_state: stopped_by_user_kill` and stop reason `user requested kill after every-minute posting/control-plane confusion`.
- `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER` still exists.
- Profile config still has `kanban.dispatch_in_gateway: true`; the topology checker treats this as `gateway_global_enabled_warning` unless a TV-specific live owner is derived.

## Actions taken in this session

1. Removed cron job `4e9cc82d1a99` (`Terminal Velocity slice completion reporter`).
2. Verified no cron jobs remain via `cronjob list` and `cron/jobs.json` readback.
3. Updated `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER` to say the reporter job was removed, not merely paused.
4. Updated `.hermes/long-running/tv-spec-implementation/task-ledger.json`:
   - `status`: `stopped_by_user`
   - `active_gate`: `null`
   - `current_gate_classification.active_owner_conflict`: `false`
   - `current_gate_classification.ledger_stale`: `false`
   - `current_gate_classification.passive_reporter_ignored`: `false`
   - `current_gate_classification.stale_bootstrap_job_ignored`: `false`
   - `current_gate_classification.gateway_global_enabled_warning`: `true`
   - added note that command execution was unavailable here and topology preflight must be rerun before restart.
5. Updated `.hermes/long-running/tv-spec-implementation/tv-spec-debug-artifact-2026-06-10.md` with a `2026-06-11 cron cleanup / debug-state update` section.

## Files touched in this session

- `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER`
- `.hermes/long-running/tv-spec-implementation/task-ledger.json`
- `.hermes/long-running/tv-spec-implementation/tv-spec-debug-artifact-2026-06-10.md`
- `.hermes/long-running/tv-spec-implementation/new-session-handoff-2026-06-11.md` (this file)

No runner restart, gateway/config/provider/account change, push, force-push, deletion, or publication was performed.

## Important constraint / mistake prevention

Do **not** use cron as a one-shot terminal execution shim.

If the new session has terminal access, run commands directly. If it does not, report the explicit blocker instead of creating new cron/script jobs for immediate verification.

## Required skills / references to load

Load at least:

- `hermes-agent` if discussing Hermes terminal/tool availability, cron, gateway, profile, or toolsets.
- `ev-terminal-velocity-play` for Terminal Velocity runner/task context.
- `source-and-fidelity` for live-state/source hierarchy.
- `systematic-debugging` for topology/debug flow.
- `artifact-governance` for durable handoff/artifact updates.

Relevant EV/TV skill reference inside `ev-terminal-velocity-play`:

- `references/terminal-velocity-topology-live-state-debugging.md`

## First commands for new session if terminal is available

Run these from a real shell, directly, not via cron:

```bash
cd /home/bh/workspaces/loki/terminal-velocity
pwd
git status --short --branch
python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner
python3 -m unittest native_ev.tests.test_tv_spec_continuous_runner.TvRunnerTopologyTests -v
```

If those pass and topology checker reports `"ok": true`, inspect the repo diff/status before any restart:

```bash
git diff -- .hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER \
  .hermes/long-running/tv-spec-implementation/task-ledger.json \
  .hermes/long-running/tv-spec-implementation/tv-spec-debug-artifact-2026-06-10.md \
  .hermes/long-running/tv-spec-implementation/new-session-handoff-2026-06-11.md \
  tools/check_tv_runner_topology.py \
  native_ev/tests/test_tv_spec_continuous_runner.py
```

## Restart gate

Do not remove `STOP_CONTINUOUS_RUNNER` or start the runner until:

1. topology checker has been run in a real shell;
2. `TvRunnerTopologyTests` pass;
3. live repo state is inspected;
4. the intended single implementation owner is clear.

Only if the user explicitly asks to restart after successful verification, the canonical restart path is expected to be:

```bash
cd /home/bh/workspaces/loki/terminal-velocity
rm .hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER
/home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh
```

Before running that, re-read the current `task-ledger.json`, current debug artifact, and current live cron/process/Kanban state. Do not start both standalone runner and gateway-dispatch owner.

## Known current interpretation

The previous visible cron conflict has been cleaned up: no cron jobs remain. The remaining work is to verify whether the topology checker now reports no active owner conflict in live state.

The scoped runner stop is still intentional. Treat `stopped_by_user` plus `STOP_CONTINUOUS_RUNNER` as the current safety gate, not as a bug.

## If terminal is still unavailable

Do not create cron jobs to compensate. Report:

- terminal unavailable in this route/session;
- file/artifact state is ready for direct shell verification;
- exact commands above are the remaining explicit gate.
