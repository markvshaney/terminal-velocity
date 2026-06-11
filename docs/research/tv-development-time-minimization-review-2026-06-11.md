# TV development-time minimization review

Date: 2026-06-11
Status: current setup assessment after completed cleanup/qualification work
Scope: Terminal Velocity development workflow/process only. This is not an EV Classic gameplay/fidelity source.

## Decision

The time-minimizing architecture remains: **parallel executable lanes + fast evaluators + batched integration + fidelity gates + playable-payoff dispatch**.

Completed cleanup and qualification work has been removed from the action list. The artifact now tracks only the current operating posture and remaining recommendations:

1. resume playable-payoff batches under `continuous_kanban_runner` after a fresh topology preflight;
2. continue route/fuel/travel-player affordance work as TV scaffolds unless Classic evidence supports promotion;
3. use the four Basilisk `TV4-*` lanes only for scout-grade non-timing runtime-UI setup/capture/focus work until one lane is separately qualified for EV app state, guest input, and restore/reset;
4. keep backlog/priority/verifier maps as the machine-readable dispatch surface.

Starting/restarting the runner remains an operational side effect and should use the established TV control-plane policy. There is no current dirty-worktree, stale-ledger, or topology-conflict blocker recorded by this artifact.

## Current truth sources

Live/repo sources for this current assessment:

- `.hermes/long-running/tv-spec-implementation/task-ledger.json`
- `docs/research/basilisk-speed-qualification.json`
- `docs/checklists/ev-classic-original-runtime-observation-checklist.md`
- `tools/check_tv_runner_topology.py`
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

Historical run summaries are not current truth. The stale `continuous-runner/latest-summary.json` sidecar was deleted by explicit user request; the run-specific historical summary remains at `.hermes/long-running/tv-spec-implementation/continuous-runner/run-20260611T072555Z-4.summary.json` with `events.jsonl`.

## Current setup status

### Control plane

Current state:

- declared implementation owner: `none_active`
- live implementation owner: `none_active`
- topology conflict: `false`
- topology warnings: `[]`
- ledger active gate: `null`
- ledger status: `paused`

Assessment: **clean but idle.** The next implementation step is not more reconciliation; it is a fresh preflight and then a single-owner runner start if operationally approved.

### Dispatch machinery

The repo already has the right execution surfaces:

- `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json`
- `docs/checklists/tv-playable-milestone-priority-map.json`
- `docs/checklists/tv-verifier-impact-map.json`

Assessment: **use these, patch on touch, do not replace with more narrative process.**

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

Before start:

- verify `git status --short --branch` has only intended local edits or is clean at `origin/main`;
- run `python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner`;
- start under exactly one owner surface, preferably `continuous_kanban_runner`.

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
- **Restarting via cron/gateway workaround.** Reject. Use the intended single-owner runner/control-plane path.
- **Using cron as an implementation fallback.** Reject. Cron should not implement, repair, coordinate, or dispatch TV work.
- **Broad Basilisk-first exploration.** Reject as a default. Use Basilisk for specific original-runtime claims; static/resource/manual-backed and TV-scaffold work should proceed without waiting.

## Current gate

No human approval is needed for safe local repo inspection/tests or for updating this review artifact.

Starting/restarting the continuous runner, changing cron/gateway/provider/account config, mutating scheduler state, or publishing raw captures remains separately gated by the existing TV control-plane and source/provenance policy.

## Closeout classification

This artifact is a **current setup assessment with only remaining recommendations**. Completed cleanup items have been removed from the action list. It does not itself start/stop runners, mutate cron, push commits, or promote any EV Classic gameplay claim.
