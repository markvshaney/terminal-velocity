# TV development-time minimization review

Date: 2026-06-11
Status: current setup assessment after completed cleanup/qualification work
Scope: Terminal Velocity development workflow/process only. This is not an EV Classic gameplay/fidelity source.

## Decision

The time-minimizing architecture remains: **parallel executable lanes + fast evaluators + batched integration + fidelity gates + playable-payoff dispatch**.

Completed cleanup, qualification, and false human-review handoff work has been removed from the action list. The artifact now tracks only the current operating posture and remaining recommendations:

1. keep the tv-spec loop moving through the autonomous integration-owner + Kanban successor path; do not wait on human review for verified safe-local TV changes;
2. continue route/fuel/travel-player affordance work as TV scaffolds unless Classic evidence supports promotion;
3. use the four Basilisk `TV4-*` lanes only for scout-grade non-timing runtime-UI setup/capture/focus work until one lane is separately qualified for EV app state, guest input, and restore/reset;
4. keep backlog/priority/verifier maps as the machine-readable dispatch surface;
5. automate continuous-runner start/restart from the scheduler with a script-only autostart watchdog, not a manual chat prompt.

Starting/restarting the runner is no longer a human-in-the-loop action when the lane is clean and only needs a ready-task dispatch or successor seed. It remains a control-plane action, so the automation must stay narrow: no feature implementation, no repo rewrite, no gateway/provider/account config mutation, and no new work over a dirty worktree.

## Current truth sources

Live/repo sources for this current assessment:

- `.hermes/long-running/tv-spec-implementation/task-ledger.json`
- `docs/research/basilisk-speed-qualification.json`
- `docs/checklists/ev-classic-original-runtime-observation-checklist.md`
- `tools/check_tv_runner_topology.py`
- `tools/tv_runner_autostart.py`
- `native_ev/tests/test_tv_spec_continuous_runner.py`
- current git status/history/remote-tracking state

Current verification commands from the recent setup pass:

```text
git status --short --branch
# -> ## main...origin/main plus current doc/ledger/qualification edits only

python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner
# -> ok true; topology_conflict false; warning_types []

python3 tools/basilisk_speed_qualification.py
# -> BASILISK SPEED QUALIFICATION OK

python3 -m unittest native_ev.tests.test_basilisk_speed_qualification -v
# -> Ran 3 tests OK

python3 -m json.tool .hermes/long-running/tv-spec-implementation/task-ledger.json
# -> valid JSON

git diff --check
# -> clean
```

Current autonomous-integration correction verification:

```text
python3 tools/tv_integration_lane.py --dry-run
# -> decision publish; blockers []; git_diff_check and committed_diff_secret_scan passed

python3 tools/tv_integration_lane.py --push --llm-approved
# -> pushed true; HEAD == origin/main == 924e689372ace8bd8f6afcf6e33bf7f52ca95afe

python3 -m unittest discover -s native_ev/tests -p 'test_*.py'
# -> Ran 295 tests OK

python3 -m unittest native_ev.tests.test_scenario_eval -v
# -> Ran 103 tests OK

python3 tools/run_gameplay_scenarios.py --all --pretty
# -> summary passed=99 failed=0 total=99
```

Historical run summaries are not current truth. The stale `continuous-runner/latest-summary.json` sidecar was deleted by explicit user request; the run-specific historical summary remains at `.hermes/long-running/tv-spec-implementation/continuous-runner/run-20260611T072555Z-4.summary.json` with `events.jsonl`.

## Current setup status

### Control plane

Current state:

- declared implementation owner: `none_active` for direct implementation; autonomous integration owner is available for normal non-force checkpoint fan-in
- live implementation owner: no direct-session implementation owner is active; the Kanban lane is the intended owner surface, and scheduler autostart is responsible for re-dispatching/seed-on-idle after reset
- topology conflict: `false`
- topology warnings: current live checker may report `ledger_stale` or `gateway_global_enabled_warning`; those are warnings, not a restart blocker when no live TV owner conflict exists
- ledger active gate: `null`
- ledger status: running/idle state must be verified live before dispatch; stale ledger owner alone is not a human gate
- last integrated checkpoint: verify with `git rev-parse HEAD origin/main`; do not trust copied SHAs

Assessment: **single-owner automation is required.** The next implementation step is not more reconciliation or human review; it is to let the Kanban lane continue and have the scheduler restart it after daily/session reset when the repo is clean. If a worker leaves verified safe-local work, autonomous integration-owner handling should cohere/push it instead of waiting on a human review gate.

### Runner autostart/restart automation

Implemented control-plane shape:

- canonical script: `tools/tv_runner_autostart.py`;
- intended scheduler shape: no-agent cron, profile `loki-game`, workdir `/home/bh/workspaces/loki/terminal-velocity`, frequent enough to cover daily reset without a manual chat nudge;
- if a `terminal-velocity` task is already `running`, stay quiet except for active-task transition status;
- if there is a ready task and no running task, dispatch exactly one task;
- if there is no running/ready/scheduled task and the repo is clean, seed exactly one continuation task with an idempotency key tied to current `HEAD`, then dispatch it;
- if the repo is dirty, do not seed overlapping work; emit an integration-owner problem report instead;
- ignore stale blocked legacy tasks for start/restart decisions so old blocked cards cannot halt the continuous lane.

Assessment: **starting/restarting is automated when safe.** The automation is deliberately not an implementation fallback: it only claims or seeds Kanban work. It does not edit gameplay files, commit, push, restart Hermes gateway, change provider/account config, or act over dirty local work.

### Dispatch machinery

The repo already has the right execution surfaces:

- `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json`
- `docs/checklists/tv-playable-milestone-priority-map.json`
- `docs/checklists/tv-verifier-impact-map.json`

Assessment: **use these, patch on touch, do not replace with more narrative process.**

### Integration ownership

Current rule:

- `review_required` / `human review` is not a valid stop condition for verified safe-local TV code/data/docs increments.
- Non-integrator workers may still avoid `git push`; they should emit `push_ready` with commit SHA, intended files, verifier output, and next action.
- The integration owner is autonomous for normal coherent non-force checkpoint review/push/fetch/`HEAD == origin/main` verification.
- Human approval remains required only for explicit risky/destructive/external/config/publication/credential/account/provider/gateway boundaries.

Assessment: **the previous human-review handoff was a process bug, not a real gate.** The correction is recorded in the runner prompt, task ledger, events log, Kanban completion for `t_99038daf`, and successor task `t_9460240d`.

### Basilisk capacity

`docs/research/basilisk-speed-qualification.json` now records four scout-qualified Basilisk II Windows GUI lanes:

- `TV4-1`
- `TV4-2`
- `TV4-3`
- `TV4-4`

Qualified for:

- live/responding Windows process capacity;
- dedicated disk/prefs path presence;
- local-only `PrintWindow` capture;
- host foreground focus via topmost/titlebar probe;
- non-timing runtime-UI setup/capture/focus smoke evidence.

Not qualified for:

- guest EV command input;
- route/travel/mission behavior promotion;
- timing/feel/combat cadence;
- combat or movement tuning claims.

Assessment: **Basilisk setup capacity is no longer the blocker.** Gameplay evidence still needs a lane-local EV app state + reversible guest-input + restore/reset qualification before use for promotion claims.

## Remaining recommendations

### P0 — Resume playable-payoff batches through the intended runner path

Current action:

- let the Kanban lane continue from live `origin/main`;
- do not spawn a second implementation owner over the same worktree;
- use `tools/tv_runner_autostart.py` under no-agent scheduler control to dispatch/seed the next Kanban task after daily reset or lane drain;
- if a worker produces verified safe-local work, complete/push via the autonomous integration-owner lane rather than asking for human review.

Before any future fresh start:

- verify `git status --short --branch` has only intended local edits or is clean at `origin/main`;
- run `python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner`;
- prefer `python3 tools/tv_runner_autostart.py` rather than a manual chat restart;
- start under exactly one owner surface, preferably the Kanban continuous-runner owner.

Implementation shape:

- choose the next route/fuel/travel blocker or recovery affordance from the backlog index;
- keep it `tv-scaffold` unless Classic evidence supports promotion;
- use focused scenario/unit verifiers first;
- batch adjacent route/fuel increments in one invocation;
- report externally only at a material boundary.

### P1 — Promote one Basilisk lane only when it unblocks a specific Classic claim

Do not make Basilisk gameplay setup the default next move just because the four lanes are now scout-qualified.

When a backlog item needs original-runtime evidence:

1. choose one `TV4-*` lane;
2. restore/launch to a known EV app or pilot state;
3. verify guest command input with a reversible action;
4. record the lane-local restore/reset procedure;
5. qualify non-destructive route/map UI observation for travel-loop promotion candidates;
6. keep high-speed scout evidence separate from any 1x timing sentinel.

### P2 — Keep machine-readable dispatch artifacts authoritative

Do not spend another pass redesigning process doctrine. Patch the backlog index, priority map, verifier map, and qualification matrix only when future dispatch would otherwise be stale or wrong.

## Rejected time savers

- **Turning off source/fidelity labels to move faster.** Reject. It creates later rework and Classic-claim contamination.
- **Restarting via manual chat nudges or gateway workaround.** Reject. Use the intended single-owner runner/control-plane path.
- **Using cron as an implementation fallback.** Reject. Cron should not implement feature work. A script-only autostart watchdog may dispatch/seed Kanban ownership when the lane is idle and clean.
- **Treating verified safe-local checkpoint review as a human gate.** Reject. Use the autonomous integration owner; human review is not in the long-winding loop unless a real gated boundary is crossed.
- **Broad Basilisk-first exploration.** Reject as a default. Use Basilisk for specific original-runtime claims; static/resource/manual-backed and TV-scaffold work should proceed without waiting.

## Current gate

No human approval is needed for safe local repo inspection/tests or for updating this review artifact.

No human approval is needed for autonomous integration-owner handling of normal coherent non-force TV checkpoint review/push/fetch/`HEAD == origin/main` verification after deterministic guards pass.

Starting/restarting the continuous runner through the approved script-only autostart path is allowed when the lane is idle/clean and only requires dispatch/seed. Changing gateway/provider/account config, destructive scheduler changes, force/rewrite, or publishing raw captures remains separately gated by the existing TV control-plane and source/provenance policy.

## Closeout classification

This artifact is a **current setup assessment with only remaining recommendations**. Completed cleanup items have been removed from the action list. It does not itself start/stop runners, mutate cron, push commits, or promote any EV Classic gameplay claim.
