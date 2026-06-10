# Runner topology bug review — 2026-06-10

Source: Loki GameTV post around 2:29 p.m. on 2026-06-10, promoted to an artifact at the user's request so the runner/control-plane bugs can be worked through systematically.

Scope: Terminal Velocity long-running workflow surfaces under `/home/bh/workspaces/loki/terminal-velocity` and profile-local Hermes state under `/home/bh/.hermes/profiles/loki-game/`.

## Current status at artifact creation

- `5430276bcaa5` — Terminal Velocity tv-spec implementation loop — was paused at `2026-06-10T14:43:11-04:00` after the user requested stopping cron.
- All four TV-related cron jobs listed by `cronjob list` were paused after that action.
- This artifact records bugs and review surfaces only; it does not itself restart, pause, push, or repair any runner.

## Original post content, preserved as review basis

Yes — one or more bugs occurred. I’d break it into four distinct bugs / process failures, plus one artifact-quality warning.

### 1. Runner topology bug: not a clean single-runner state

Bug: the live scheduler has one enabled cron runner, but durable state still claims a different continuous/Kanban runner is the owner.

Evidence:

- Enabled cron runner:
  - `/home/bh/.hermes/profiles/loki-game/cron/jobs.json`
  - job `5430276bcaa5`, “Terminal Velocity tv-spec implementation loop”
  - lines 145–188 show it is enabled, scheduled, delivered to `telegram:Loki GameTV`, workdir `/home/bh/workspaces/loki/terminal-velocity`.

- Ledger still says the intended owner is the continuous runner and cron fallback should be paused:
  - `.hermes/long-running/tv-spec-implementation/task-ledger.json`
  - line 102: `operational_owner_candidate`: continuous background runner; cron fallback retained but disabled
  - lines 125–145: runner kind is `continuous-background-loop`; `replaces_paused_cron_job_id: 5430276bcaa5`
  - line 180: `status: running`

- Process/run state still shows a Kanban continuous loop:
  - `/home/bh/.hermes/profiles/loki-game/run/tv_kanban_continuous_loop_state.json`
  - lines 2–12: active task, ready task, successor, PID `1970812`, updated at `2026-06-10T18:28:28Z`
  - `/home/bh/.hermes/profiles/loki-game/processes.json`
  - lines 3–8: registered detached `tv_kanban_continuous_loop.py`, PID `1970812`

Conclusion: yes, topology confusion exists. It is not one clean runner surface.

### 2. Stop-boundary bug: STOP file exists but cron continues

Bug: a stop file says not to auto-resume, yet the cron implementation loop is still enabled and running.

Evidence:

- Stop file:
  - `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER`
  - line 1: “Stop the Terminal Velocity continuous runner and do not auto-resume until explicitly requested.”

- Cron still enabled/running:
  - `cronjob list`
  - `5430276bcaa5` enabled, state `scheduled`, last run `2026-06-10T14:28:13`, next run `14:29:13`

Conclusion: either the STOP file only controls the old continuous wrapper and not the cron fallback, or the cron fallback was restarted without reconciling the STOP state. Either way, this is a control-plane bug.

### 3. Push/publication authority contradiction

Bug: the cron prompt and the ledger disagree about whether the runner may push.

Evidence:

- Cron prompt says pushes are preapproved:
  - `/home/bh/.hermes/profiles/loki-game/cron/output/5430276bcaa5/2026-06-10_14-28-12.md`
  - lines 31–32: normal coherent non-force pushes are preapproved after checks.

- Ledger says workers/continuous runners must not push:
  - `.hermes/long-running/tv-spec-implementation/task-ledger.json`
  - lines 42–47: integration owner owns push; worker/continuous runner “must not run git push”
  - line 144: `push_authority: non_integrator_runner_must_not_push_record_push_ready`

- Actual outputs show inconsistent behavior:
  - `2026-06-10_14-19-01.md`
    - lines 77–80: “committed and pushed normal non-force,” `HEAD == origin/main`
  - older continuous runner summary:
    - `.hermes/long-running/tv-spec-implementation/continuous-runner/latest-summary.json`
    - lines 2–7: push auth gate
    - lines 29–32: `ledger_status: waiting_gate`, next action says push after GitHub credentials/human action

Conclusion: yes, consistent blocking/confusion around publication authority occurred. It alternates between push-ready gate, no-push policy, and actual pushes.

### 4. Report/content integrity bug in latest cron output

Bug: latest cron output claims touched files / verified state while the tool layer warns a listed file was not modified because patch validation failed.

Evidence:

- Latest cron output:
  - `/home/bh/.hermes/profiles/loki-game/cron/output/5430276bcaa5/2026-06-10_14-28-12.md`
  - lines 42–50: lists touched files including `tools/extract_ev_system_semantics.py`
  - lines 52–59: reports verification and git state
  - lines 77–78: file-mutation verifier warning: `tools/extract_ev_system_semantics.py` was not modified; patch failed because hunk not found

Conclusion: this is a reporting/artifact-quality bug. The final message included claims that conflict with the tool guard.

### 5. “Possible update” / artifact drift warning

The latest ledger has moved beyond the first inspection while this review was happening:

- `.hermes/long-running/tv-spec-implementation/events.jsonl`
  - lines 140–142 show checkpoint pushed and later v41 events.
- `.hermes/long-running/tv-spec-implementation/task-ledger.json`
  - line 48: latest material event is now `lane-a-v41-resource-bible-syst-sequential-projection-negative-oracle-current-cron-verified`
  - line 186: updated at `2026-06-10T18:27:17Z`

So any review needs to treat these artifacts as live-moving unless the runner is paused. Pausing or updating the scheduled job is a scheduled-job mutation, so I’m not doing that under this report-only request.

## Artifact update after follow-up clarification

The topology issue should be framed more precisely:

- Intended topology: stop using cron as the main runner; use continuous Kanban/background runner.
- Cron `5430276bcaa5` was supposed to be a paused fallback, not an active implementation runner.
- The phrase “cron fallback” is itself probably too broad: under the continuous Kanban design, cron may only be a quiet no-agent watchdog/reporter, not an editable LLM implementation fallback for the same repo.

Clean invariant to restore:

> Continuous Kanban is the implementation runner. Cron may only be a quiet no-agent watchdog/reporter, never an editable LLM fallback for the same repo.

## Review artifacts

Primary review set:

- `/home/bh/.hermes/profiles/loki-game/cron/jobs.json`
- `.hermes/long-running/tv-spec-implementation/task-ledger.json`
- `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER`
- `.hermes/long-running/tv-spec-implementation/continuous-runner/latest-summary.json`
- `/home/bh/.hermes/profiles/loki-game/run/tv_kanban_continuous_loop_state.json`
- `/home/bh/.hermes/profiles/loki-game/processes.json`
- `/home/bh/.hermes/profiles/loki-game/cron/output/5430276bcaa5/2026-06-10_14-28-12.md`
- `/home/bh/.hermes/profiles/loki-game/cron/output/5430276bcaa5/2026-06-10_14-19-01.md`
- `.hermes/long-running/tv-spec-implementation/events.jsonl`

## Follow-up finding: active continuous Kanban task despite paused cron

Recorded after user observed messages still arriving every minute.

Evidence checked after cron pause:

- `cronjob list` shows all four TV cron jobs paused, including `5430276bcaa5` and `4e9cc82d1a99`.
- `/home/bh/.hermes/profiles/loki-game/run/tv_kanban_continuous_loop_state.json` still reports `last_state: running`, PID `1970812`, active task `t_ef52f8ee`, ready task `t_ef52f8ee`, successor `t_d1818f18`, updated at `2026-06-10T19:56:46.673887+00:00`.
- `/home/bh/.hermes/profiles/loki-game/processes.json` still registers detached `tv_kanban_continuous_loop.py`, PID `1970812`, cwd `/home/bh/workspaces/loki/terminal-velocity`, session key `agent:main:telegram:group:-5127009860:7956191079`.

Conclusion: user-visible every-minute posting is evidence of an active task path outside the now-paused cron scheduler, most likely the continuous Kanban loop or a child/session it is driving. The earlier cron-only answer was incomplete: cron is paused, but implementation/control-plane activity is not cleanly stopped.

## Fix-through checklist

Use this section to work the bugs without losing the distinctions.

### A. Restore runner ownership invariant

Status: pending

Actions to evaluate:

- Confirm `5430276bcaa5` remains paused.
- Decide whether to remove the “LLM implementation fallback” concept entirely from `task-ledger.json` and runner prompts.
- Ensure only continuous Kanban/background runner owns implementation writes.
- Ensure any cron surface left behind is script-only/no-agent/local/health-check-only.

Verification:

- `cronjob list` shows no enabled LLM implementation cron for TV.
- Ledger no longer says an editable LLM cron is a fallback implementation path.
- Continuous Kanban state has exactly one active/ready successor path or a named gate.

### B. Reconcile STOP semantics

Status: pending

Actions to evaluate:

- Decide whether `STOP_CONTINUOUS_RUNNER` applies only to the wrapper or to all TV implementation surfaces.
- If it applies globally, make every runner/supervisor check it before dispatching implementation work.
- If it applies only to the continuous wrapper, rename or replace it with a clearer scoped marker.

Verification:

- A STOP marker cannot coexist with active implementation work unless the artifact explicitly says which surface it does and does not control.

### C. Resolve push authority

Status: pending

Actions to evaluate:

- Pick one authority model for the continuous Kanban runner:
  - non-integrator worker records `push_ready`, or
  - direct runner is explicitly integration owner and may push after checks.
- Remove contradictory prompt text from non-owner surfaces.
- Ensure GitHub credential absence in worker contexts is not treated as a development gate if worker is not supposed to push.

Verification:

- Runner prompt, ledger `integration_policy`, and actual output behavior agree.
- No runner alternates between push-ready, no-push, and pushing without an explicit role change.

### D. Fix report/content integrity

Status: pending

Actions to evaluate:

- Treat file-mutation verifier warnings as final-output blockers for claims about touched files.
- Require outputs to distinguish attempted changes from confirmed changed files.
- Review `2026-06-10_14-28-12.md` against actual git state before accepting its touched-file list.

Verification:

- Latest output does not claim a file was touched when the tool guard says the patch failed.
- Any future runner report includes a verified touched-files list or explicit “attempted but unchanged” list.

### E. Freeze or version live-moving artifacts during review

Status: pending

Actions to evaluate:

- For bug review, snapshot or pause moving surfaces before line-number-based claims.
- Record whether line numbers are from a specific timestamp/run.

Verification:

- Review can be repeated from a named file/run timestamp without depending on currently moving ledger lines.

## Gates / boundaries

- Do not restart gateway/supervision/provider/config surfaces without explicit approval.
- Do not re-enable implementation cron.
- Do not force-push or rewrite history.
- Do not change external publication/account/credential surfaces without approval.
- Normal repo edits for this artifact/fix process are local unless the user explicitly asks for integration/push.
