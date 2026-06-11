# TV development-time minimization review

Date: 2026-06-11
Status: current setup assessment and recommendations
Scope: Terminal Velocity development workflow/process only. This is not an EV Classic gameplay/fidelity source.

## Decision

Keep the current direction: **parallel executable lanes + fast evaluators + batched integration + fidelity gates + playable-payoff dispatch** is the right time-minimizing architecture.

Revise the operating setup before restarting autonomous implementation, because the live control plane now has one remaining local gate:

1. the continuous runner is not live;
2. `HEAD` equals `origin/main`, but tracked and untracked local changes remain;
3. the topology checker false positive for the enabled Loki Game memory-hygiene cron was fixed on 2026-06-11 by narrowing cron TV ownership detection to explicit TV control-plane surfaces;
4. the ledger was reconciled on 2026-06-11 to `declared_owner: none_active`, `status: paused`, and active gate `dirty_worktree_reconciliation`.

So the highest-leverage next move is **dirty-worktree cleanup/checkpointing first, then resume playable-payoff batches**. Do not start another runner until the dirty files are classified and either checkpointed or reverted.

## Sources inspected

Live/repo sources inspected for this review:

- `docs/research/tv-spec.md`
- `docs/prompts/tv-spec-implementation-long-task-prompt.md`
- `docs/research/long-running-task-wrapper-spec.md`
- `docs/research/tv-kanban-topology-review-2026-06-10.md`
- `.hermes/long-running/tv-spec-implementation/task-ledger.json`
- `.hermes/long-running/tv-spec-implementation/events.jsonl` tail, lines 142-181
- `.hermes/long-running/tv-spec-implementation/continuous-runner/latest-summary.json`
- `.hermes/long-running/tv-spec-implementation/continuous-runner/index.jsonl`
- `docs/checklists/tv-playable-milestone-priority-map.json`
- `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json`
- `docs/checklists/tv-verifier-impact-map.json`
- `docs/research/basilisk-speed-qualification.json`
- `/home/bh/.hermes/profiles/loki-game/cron/jobs.json`
- `tools/check_tv_runner_topology.py`

Live commands run:

```text
git status --short --branch
# -> ## main...origin/main
# -> dirty tracked files: .hermes/long-running/tv-spec-implementation/task-ledger.json, native_ev/data/sourced_ev_systems.json, native_ev/model.py, native_ev/scenario_eval.py, native_ev/tests/test_model.py, native_ev/tests/test_scenario_eval.py, native_ev/tests/test_tv_spec_continuous_runner.py, tools/check_tv_runner_topology.py, tools/extract_ev_system_semantics.py
# -> untracked files: docs/research/tv-development-time-minimization-review-2026-06-11.md

git rev-parse HEAD origin/main
# -> both 2e3ff8679497a109e5d189fc125d6972792fdc6c

git diff --stat
# -> source/gameplay files plus topology-checker/doc/ledger changes are dirty; see git status for exact current set.

python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner
# -> exit 0; ok true; topology_conflict false; conflict_types []
# -> live_implementation_owner none_active; declared_implementation_owner none_active; warning_types []
```

Cron cross-check:

- Hermes `cronjob list` and `/home/bh/.hermes/profiles/loki-game/cron/jobs.json` show only one enabled cron job: `20dca3ae3beb`, `Daily Loki Game memory hygiene`.
- That job is not a TV implementation/repair/dispatch surface. Its prompt merely mentions preserving “TV safety/fidelity/user-preference semantics.”
- Therefore the current topology conflict is a **checker false positive**, not evidence of an active TV implementation cron.

## What is already good

### 1. The spec now encodes the right throughput model

`tv-spec.md` already contains the key time-saving doctrines:

- batch adjacent increments inside one invocation;
- report only at material boundaries;
- update backlog/provenance only when future execution changes;
- match verifier breadth to risk;
- use event logs for routine history and ledger for resumable state;
- avoid workers/subagents for mechanical sequential source-mining loops.

Assessment: **already in spec; do not re-litigate.**

### 2. Dispatch metadata exists and is machine-readable enough for current use

The repo has:

- `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json` with `next_action`, `lane_class`, `oracle_class`, `source_basis`, `verifier`, `blocked_reason`, and `promotion_status` per item;
- `docs/checklists/tv-playable-milestone-priority-map.json` ranking playable payoff, with `playable_travel_loop` currently rank 1;
- `docs/checklists/tv-verifier-impact-map.json` mapping touched surfaces to cheap required verifiers.

Assessment: **major operationalization gap has been substantially closed.** Keep improving on-touch, but do not spend a fresh pass redesigning these artifacts unless a checker or dispatch failure exposes a concrete gap.

### 3. Recent runner output shows useful player-visible batching

The recent event tail shows the continuous runner made several adjacent route/fuel/guardrail increments in one lane:

- route invalid-stop structured recovery;
- blocked-jump structured recovery;
- route-clear reselect structured recovery;
- manual route-fuel structured recovery.

These are labeled as TV scaffolds / route guardrails, not promoted EV Classic fidelity. That is the right quality-preserving speed pattern: player-visible progress now, source/fidelity promotion later.

Assessment: **the workflow can produce useful batches when the control plane is healthy.**

## Current setup problems

### 1. Topology checker false-positive cron conflict — fixed locally

`tools/check_tv_runner_topology.py` previously used broad TV term matching:

- `TV_TERMS = ("terminal velocity", "tv-spec", "tv ", "loki gametv")`
- it scanned cron job `id`, `name`, `prompt`, `script`, `deliver`, and `workdir`

The memory-hygiene cron prompt contains a sentence about preserving TV safety/fidelity semantics, so the checker classified it as TV-related. Because it is enabled and agent-backed, the checker reported an `active_owner_conflict` even though no TV cron implementation job existed.

Status: **fixed locally on 2026-06-11.** Cron TV ownership detection now prefers explicit TV control-plane surface fields (`id`, `name`, `script`, `deliver`, `workdir`) and only uses prompt text for strong TV owner phrases. A regression test covers the current memory-hygiene cron shape and proves it is ignored as a non-TV owner.

Remaining implication: the topology false positive is no longer a restart blocker; the ledger also no longer reports a stale owner. Dirty source/gameplay files remain the restart blocker.

### 2. Ledger reconciled; latest summary remains historical

Live git says:

- local `HEAD` equals `origin/main`;
- branch is not ahead;
- tracked and untracked local changes remain.

Before reconciliation, the ledger/latest runner summary still said or implied:

- integration owner should push local main;
- `head_equals_origin_main: false` in the latest summary;
- `git_dirty_summary: ## main...origin/main [ahead 19]` in the latest summary;
- ledger status `running` with next action to push/fetch/verify.

Status: **ledger fixed locally on 2026-06-11.** `.hermes/long-running/tv-spec-implementation/task-ledger.json` now records `declared_owner: none_active`, `status: paused`, `HEAD == origin/main`, `latest_summary_is_historical: true`, and an active `dirty_worktree_reconciliation` gate.

Remaining implication: `continuous-runner/latest-summary.json` is still historical output from the old runner invocation. Treat it as evidence of what that invocation saw, not current runtime truth. The live topology checker now returns no conflicts and no warnings.

### 3. Dirty source-mining/gameplay files need stabilization before more automation

Pre-existing dirty tracked source/gameplay files still need reconciliation before restarting autonomous implementation:

- `native_ev/data/sourced_ev_systems.json`
- `native_ev/model.py`
- `native_ev/scenario_eval.py`
- `native_ev/tests/test_model.py`
- `native_ev/tests/test_scenario_eval.py`
- `tools/extract_ev_system_semantics.py`

Separate from those, this topology-checker fix intentionally modifies `tools/check_tv_runner_topology.py` and `native_ev/tests/test_tv_spec_continuous_runner.py`; the review artifact itself remains untracked until checkpointed.

Assessment: **do not restart autonomous implementation over the unknown source/gameplay slice.** First classify it as either:

- intentional uncommitted continuation work from the route/system semantics lane;
- generated output that should be rebuilt/committed/reverted;
- stale residue after pushed commits.

Recommended fix:

1. Inspect the diff by file.
2. Run the relevant targeted verifiers from the verifier impact map.
3. Either checkpoint the coherent slice locally or revert stale/generated residue.
4. Only then restart the continuous runner.

### 4. Basilisk capacity is declared but not yet qualified

`tv-spec.md` correctly treats four Basilisk lanes as concrete capacity. But `docs/research/basilisk-speed-qualification.json` still marks all four lanes as `setup-incomplete` / `unqualified`.

Assessment: **not a blocker for TV-scaffold/Godot/Python work, but still a real bottleneck for original-runtime promotion.**

Recommended fix:

- Do not schedule Basilisk-heavy promotion work until at least one lane has restore/capture/input qualification for the needed evidence family.
- Continue TV-side playable scaffolds and static-resource/manual-backed semantic promotion in the meantime.
- Add Basilisk qualification work only when the backlog item genuinely needs original-runtime evidence.

## Highest-leverage recommendations

### P0 — Fix topology false positive and reconcile dirty live state

Why it minimizes time:

- removes a fake restart blocker;
- prevents stale ledger/summary churn;
- avoids running an autonomous loop over ambiguous dirty source files.

Done condition:

- topology checker passes or reports only real live conflicts;
- memory-hygiene cron is explicitly ignored by regression test;
- git dirty state is understood and either verified/checkpointed or reverted;
- ledger next action matches live git and runner state.

### P1 — Resume the playable-payoff batch lane after cleanup

The current priority map says rank 1 is `playable_travel_loop`. Recent successful increments are in that lane. Continue there unless the dirty-state inspection shows a more urgent stabilization task.

Preferred next implementation shape after cleanup:

- choose the next route/fuel/travel blocker or recovery affordance from the backlog index;
- keep it `tv-scaffold` unless Classic evidence supports promotion;
- use focused scenario/unit verifiers first;
- batch adjacent route/fuel increments in one invocation;
- report externally only at material boundary.

### P2 — Qualify one Basilisk lane only when it unblocks a specific promotion claim

Do not make Basilisk setup the default next move just because it is incomplete. Use it when a backlog item needs original-runtime evidence, especially exact UI wording/timing or route/map behavior.

Recommended first qualified family when needed:

- non-destructive route/map UI observation for travel-loop promotion candidates;
- highest safe accelerated speed for scout evidence;
- 1x sentinel only for timing-sensitive promotion.

### P3 — Keep the machine-readable dispatch artifacts as the execution surface

Do not replace the current backlog index, priority map, or verifier map with new narrative doctrine. They are already the right kind of machinery. Patch them on touch when future dispatch would otherwise be stale.

## Rejected time savers

- **Turning off source/fidelity labels to move faster.** Reject. It saves apparent time by creating later rework and Classic-claim contamination.
- **Restarting the runner despite dirty files and topology conflict.** Reject until the conflict is proven false in code/tests and dirty files are stabilized.
- **Using cron as an implementation fallback.** Reject. Current policy is right: cron should not implement, repair, coordinate, or dispatch TV work.
- **Broad Basilisk-first exploration.** Reject as a default. Use Basilisk for specific original-runtime claims; static/resource/manual-backed and TV-scaffold work should proceed without waiting.

## Current gate

No human approval is needed to edit this review artifact or to perform safe local repo inspection/tests.

Starting/restarting the continuous runner, changing cron/gateway/provider/account config, or mutating scheduler state remains separately gated by the existing TV control-plane policy. The immediate safe local implementation follow-up is a code/test/docs cleanup of the topology checker false positive plus dirty-state reconciliation.

## Closeout classification

This artifact is a **current setup assessment with recommendations**. It does not itself start/stop runners, mutate cron, push commits, or promote any EV Classic gameplay claim.
