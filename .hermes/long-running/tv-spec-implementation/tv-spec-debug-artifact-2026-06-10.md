# TV spec debug artifact — runner topology conflict

Created for: explicit Loki Game request, “Create a TV spec debug artifact.”

Scope: Terminal Velocity repo-local tv-spec implementation runner state only. This artifact records the current restart/debug problem without changing runner ownership, removing stop files, pushing, or restarting background work.

## Current architecture repair

The review recommendation has been applied as a repo-local control-plane repair. The runner ledger is now a compact declared intent/checkpoint pointer, not primary runtime truth. `tools/check_tv_runner_topology.py` now derives live topology from current surfaces first:

- profile cron jobs metadata;
- profile process registry;
- continuous loop state;
- gateway dispatch config;
- then ledger intent/checkpoint state only as reconciliation input.

New explicit classifications:

- `active_owner_conflict` — another live implementation owner/surface is active or unresolved;
- `ledger_stale` — ledger intent or old gate disagrees with derived live state;
- `passive_reporter_ignored` — no-agent script-only reporter cron is not an implementation owner;
- `stale_bootstrap_job_ignored` — completed/disabled bootstrap cron is not a live owner;
- `gateway_global_enabled_warning` — global gateway dispatch is enabled but does not by itself prove TV ownership.

Current live readback during the repair:

- cron: only TV job `4e9cc82d1a99`, `no_agent: true`, `script: tv_slice_reporter.py`, `enabled: false`, `state: paused`;
- processes: `[]`;
- loop state: `last_state: stopped_by_user_kill`;
- stop marker: `STOP_CONTINUOUS_RUNNER` still present and says user requested no auto-resume;
- gateway config: `kanban.dispatch_in_gateway: true`, now classified as warning unless a TV-specific live owner is derived.

The scoped stop file was not removed, no runner was started, cron/gateway settings were not changed, and no push/publication was performed.

## 2026-06-11 cron cleanup / debug-state update

After the user asked to do the cleanup path, the paused passive reporter cron job was removed:

- removed cron job: `4e9cc82d1a99` (`Terminal Velocity slice completion reporter`);
- verified with `cronjob list`: `count: 0`;
- verified `~/.hermes/profiles/loki-game/cron/jobs.json`: `"jobs": []`;
- verified process registry: `~/.hermes/profiles/loki-game/processes.json` is `[]`;
- loop state still says `last_state: stopped_by_user_kill` with stop reason `user requested kill after every-minute posting/control-plane confusion`;
- scoped stop marker remains present and now records that the reporter was removed, not merely paused.

No cron jobs remain. No runner was restarted, no STOP marker was removed, no gateway/config/provider change was made, and no push/publication was performed.

Command execution is unavailable in this Telegram session and in a delegated read-only verification attempt, so the next restart still must begin with a real shell run of:

```text
python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner
python3 -m unittest native_ev.tests.test_tv_spec_continuous_runner.TvRunnerTopologyTests -v
```

## Superseded diagnosis retained for provenance

The TV spec implementation runner is not running because the restart bootstrap hit a `topology_conflict` preflight gate. The gate is currently recorded in:

- `.hermes/long-running/tv-spec-implementation/task-ledger.json`
- `.hermes/long-running/tv-spec-implementation/events.jsonl`
- cron output: `/home/bh/.hermes/profiles/loki-game/cron/output/a8e3601b6e98/2026-06-10_19-15-02.md`

The scoped stop file still exists:

- `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER`

Latest runner state remains old:

- `.hermes/long-running/tv-spec-implementation/continuous-runner/latest-summary.json`
- last invocation: `tv-spec-continuous-runner:20260610T043308Z:9`
- ended at: `2026-06-10T04:46:35Z`
- ledger status at that time: `waiting_gate`
- old gate: worker push auth unavailable

## Evidence inspected for this artifact

### Bootstrap output

File: `/home/bh/.hermes/profiles/loki-game/cron/output/a8e3601b6e98/2026-06-10_19-15-02.md`

Relevant reported command evidence:

- `git fetch origin`: succeeded.
- `git status --short --branch`: `## main...origin/main [ahead 14]`
- Modified files at bootstrap closeout:
  - `.hermes/long-running/tv-spec-implementation/events.jsonl`
  - `.hermes/long-running/tv-spec-implementation/runner-topology-bug-review-2026-06-10.md`
  - `.hermes/long-running/tv-spec-implementation/task-ledger.json`
  - `docs/prompts/tv-spec-implementation-long-task-prompt.md`
  - `docs/research/tv-spec.md`
- Untracked at bootstrap closeout:
  - `tools/check_tv_runner_topology.py`
- `git rev-parse HEAD`: `cf4d431f62a4a28d076f98794fe95e041b7b4a93`
- `git rev-parse origin/main`: `a26caaa7f5502ab8b2548b967bdb53feb3b340e3`
- Remotes: `origin https://github.com/markvshaney/terminal-velocity.git`
- Ahead commits: 14 local commits ahead of `origin/main`.

Topology preflight command:

```text
python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner
```

Result reported by bootstrap:

- exit code: `2`
- `topology_conflict: true`

Reported problems:

1. startup owner `continuous_kanban_runner` does not match ledger `runner_ownership.implementation_owner: none_active`
2. enabled TV cron job `4e9cc82d1a99` is not allowed as an implementation/repair/dispatch surface
3. enabled TV cron job `a8e3601b6e98` is not allowed as an implementation/repair/dispatch surface
4. startup requested a non-gateway implementation owner while gateway Kanban dispatch is enabled

Actions withheld by bootstrap:

- no push performed
- `STOP_CONTINUOUS_RUNNER` not removed
- standalone continuous runner not started
- no new PID/lock/log timestamp exists for a new run

Bootstrap verification reported:

- ledger JSON validation passed with `python3 -m json.tool`
- events JSONL parse passed: `events_jsonl_ok lines=163`
- topology preflight rerun after recording gate still conflicted, as expected

### Ledger state

File: `.hermes/long-running/tv-spec-implementation/task-ledger.json`

Current recorded gate:

```json
{
  "type": "topology_conflict",
  "reason": "Topology preflight refused standalone continuous runner startup for requested owner continuous_kanban_runner.",
  "resume_after": "Reconcile runner ownership/control-plane topology: ledger owner, enabled TV cron surfaces, and gateway Kanban dispatch must agree with the intended single implementation owner before restart.",
  "withheld_action": "Did not remove STOP_CONTINUOUS_RUNNER and did not start /home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh."
}
```

Ledger runner ownership at artifact creation:

- `runner_ownership.implementation_owner`: `none_active`
- `allowed_surfaces.cron`: `no_agent_reporting_only`
- `allowed_surfaces.direct_session`: `allowed_when_no_background_owner`
- `allowed_surfaces.gateway_kanban_dispatcher`: `enabled_but_not_tv_owner`
- `allowed_surfaces.standalone_continuous_loop`: `stopped`

### Prompt/spec rules that matter

`docs/prompts/tv-spec-implementation-long-task-prompt.md` now requires the standalone continuous runner to run topology preflight before implementation work:

```text
python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner
```

If it reports `topology_conflict`, the prompt says to record the conflict and stop instead of dispatching work.

`docs/research/tv-spec.md` says:

- checkpoint policy decides when remote publication has coordination/durability value; role policy decides who may publish
- workers/continuous runners do not push
- missing GitHub credentials in a worker are not a TV development gate
- local branch-ahead state by itself is not gated
- changing/resuming scheduled cron/watchdog jobs is gated
- ordinary safe-local TV development is not gated

## Working interpretation

This is no longer primarily a GitHub-auth problem. The old push-auth gate is superseded by a control-plane conflict introduced or exposed by the topology checker and by the active/queued cron surfaces at bootstrap time.

The important mismatch is:

- the user requested a restart;
- the ledger says no implementation owner is active;
- the requested startup owner was `continuous_kanban_runner`;
- gateway Kanban dispatch is enabled;
- at least one TV cron surface was enabled when the preflight ran;
- the topology checker treats that combination as unsafe ambiguity.

The passive slice reporter, if genuinely script-only/no-agent and incapable of implementation/repair/dispatch, may be a false positive in the topology checker because the ledger explicitly allows cron as `no_agent_reporting_only`. The one-shot bootstrap job `a8e3601b6e98` should disappear or be disabled after completion; if it remains enabled in job metadata during its own run, it can also be a transient false positive. These are hypotheses; verify before changing code or policy.

## Debug questions to answer next

1. Is `4e9cc82d1a99` purely passive reporting?
   - Confirm `no_agent: true` and `script: tv_slice_reporter.py` cannot start/repair/dispatch implementation work.
   - If yes, update `tools/check_tv_runner_topology.py` so script-only passive reporting jobs are allowed under `allowed_surfaces.cron: no_agent_reporting_only`.

2. Is `a8e3601b6e98` still present/enabled after its one-shot run?
   - If absent, classify its topology conflict as self-observation during bootstrap, not a durable active conflict.
   - If still enabled, remove or disable only after confirming it is the completed one-shot bootstrap surface.

3. Does gateway Kanban dispatch being enabled always conflict with `continuous_kanban_runner`, or only when it can claim Terminal Velocity implementation cards?
   - Inspect profile config and any board-specific dispatch controls.
   - Decide whether the intended owner is standalone continuous runner or gateway dispatcher.
   - Record the choice in `runner_ownership.implementation_owner` before restart.

4. Should the restart path use the standalone continuous runner or the gateway Kanban dispatcher?
   - Existing ledger runner says script: `/home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh`.
   - Existing prompt says startup owner `continuous_kanban_runner`.
   - Existing ledger warning says gateway Kanban dispatch is enabled but not TV owner.
   - The debug fix should make these surfaces agree rather than start both.

5. Is the local branch-ahead/dirt coherent enough for integration-owner push before restart?
   - Bootstrap saw `ahead 14` plus modified process/spec files and untracked `tools/check_tv_runner_topology.py`.
   - Before any push: inspect status/remotes, review intended files, rerun relevant checks, screen for secrets/proprietary/unrelated changes, push normally only as integration owner, fetch, verify `HEAD == origin/main`.

## Safe next local action

Do not restart the continuous runner yet. First perform a read/write debug slice that only resolves the control-plane preflight ambiguity:

1. Inspect current cron list after the bootstrap job completed.
2. Inspect profile Kanban dispatch setting and any active TV Kanban/worker surfaces.
3. Inspect `tools/check_tv_runner_topology.py` logic for cron classification.
4. If confirmed, patch the checker to allow passive no-agent reporter jobs and ignore completed one-shot bootstrap jobs.
5. Rerun topology preflight.
6. If preflight still conflicts, update this artifact with the remaining concrete conflict.
7. If preflight passes, then update ledger ownership and only then remove `STOP_CONTINUOUS_RUNNER` and start the canonical runner.

## Non-actions in this artifact

This artifact does not:

- remove `STOP_CONTINUOUS_RUNNER`
- start `/home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh`
- change cron jobs
- change gateway/supervision/config/providers/credentials
- push to GitHub
- force-push, rewrite history, delete files, or publish EV captures

## Review set

Primary files:

- `.hermes/long-running/tv-spec-implementation/task-ledger.json`
- `.hermes/long-running/tv-spec-implementation/events.jsonl`
- `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER`
- `.hermes/long-running/tv-spec-implementation/continuous-runner/latest-summary.json`
- `docs/prompts/tv-spec-implementation-long-task-prompt.md`
- `docs/research/tv-spec.md`
- `tools/check_tv_runner_topology.py`

Primary cron output:

- `/home/bh/.hermes/profiles/loki-game/cron/output/a8e3601b6e98/2026-06-10_19-15-02.md`

Related stub/archive pointer:

- `.hermes/long-running/tv-spec-implementation/runner-topology-bug-review-2026-06-10.md`
- `/home/bh/workspaces/loki/terminal-velocity-doc-archive/2026-06-10-topology-bug-review/runner-topology-bug-review-2026-06-10.md`
