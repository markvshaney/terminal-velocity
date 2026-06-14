# TV runner recovery and ledger projection follow-up

Date: 2026-06-13
Source artifact: archived outside repo at `/home/bh/.hermes/profiles/loki-game/home/terminal-velocity-archived-research/2026-06-12-tv-runner-integration-owner-review-gate.md`
Canonical policy: `docs/research/tv-spec.md` as of commit `cc48997` (`docs: tighten TV runner recovery policy`)
Status: implementation follow-up extracted after the durable spec policy was incorporated and the source provenance artifact was archived outside the repo. Treat dated live-state evidence as historical until reverified.

## Purpose

This file preserves the remaining actionable implementation/tooling work from the original runner ownership and integration-recovery failure analysis. It is not a competing TV spec surface. Canonical runner/integration-owner policy lives in `docs/research/tv-spec.md`; this artifact names concrete repo tools, regressions, and verification targets still useful for implementation.

## Current boundary

- **Policy resolved:** canonical closeout, start/resume, human-gate, verifier-routing, and ledger-as-projection rules were incorporated into `docs/research/tv-spec.md` in `cc48997`.
- **Historical evidence:** the original `t_d8b44829` and `t_4ad7b9e5` details are evidence shapes, not necessarily live state. Reinspect repo, Kanban, ledger/events, closeout packets, and process/cron/lock surfaces before acting.
- **Actionable remainder:** implement/verify deterministic recovery, closeout-packet consumption, gate normalization, and ledger projection tooling so the canonical policy is executable.

## Residual implementation backlog

### 1. Consume closeout packets and Kanban comments as first-class recovery evidence

Status: implemented for `tools/tv_runner_recovery_preflight.py` on 2026-06-13. The recovery classifier now treats task JSON `latest_summary` and `comments` as first-class evidence when available, preserves closeout-packet matching, and emits top-level `matched_changed_files`, `missing_changed_files`, and `extra_dirty_paths` provenance fields. Remaining alignment work is tracked in item 2.

Target surfaces:

- `tools/tv_runner_recovery_preflight.py`
- `tools/tv_runner_start_resume_preflight.py`
- `tools/tv_runner_autostart.py`
- `.hermes/long-running/tv-spec-implementation/closeout-packet-*.json`
- live Kanban comments / `latest_summary`

Required behavior:

- Treat local closeout packets as handoff evidence when they name the active blocked task and dirty bundle.
- Treat Kanban comments and `latest_summary` as handoff evidence, not only task-list fields from `kanban list`.
- Match current dirty paths against packet/comment `changed_files`, allowing exact equality plus explicitly safe generated/checkpoint artifacts such as the packet itself.
- Extract verifier status from structured `verification` fields before falling back to prose search.
- Emit provenance fields such as `handoff_evidence_sources`, `matched_changed_files`, `missing_changed_files`, and `extra_dirty_paths`.

Verifier/regression:

- Dirty repo matching a blocked `push_ready`/stale review-required card plus matching closeout packet/comment evidence must classify as `checkpoint_and_push_ready` or `rerun_focused_verifier`, never generic `unsafe_dirty_state`.
- Matching evidence with uncertain verifier freshness should return `rerun_focused_verifier` with exact verifier commands from the packet.

### 2. Keep start/resume and recovery classifiers aligned

Status: implemented for dirty-repo start/resume preflight on 2026-06-13. `tools/tv_runner_start_resume_preflight.py` now enriches blocked-card records with Kanban `latest_summary` and `task_comments`, invokes the recovery preflight classifier for dirty worktrees, embeds its payload as `dirty_handoff_recovery`, and mirrors its `recommended_action` / `explicit_gate` so start/resume and recovery name the same candidate and next action.

Target surfaces:

- shared evidence aggregation module or function used by both start/resume and recovery preflight;
- `tools/tv_runner_start_resume_preflight.py`;
- `tools/tv_runner_recovery_preflight.py`.

Required behavior:

- `recover_dirty_handoff` from start/resume must identify the same candidate as the recovery classifier.
- Ordered evidence sources should be: live Kanban comments/latest summary, local closeout packets, ledger checkpoint files/last verification, then task-list prose as fallback.
- `unsafe_dirty_state` remains reserved for true mismatch cases: sensitive paths, unrelated dirty paths, missing handoff evidence after all sources are checked, or failed relevant verifier.

Verifier/regression:

- A fixture with the `t_4ad7b9e5` evidence shape should prove start/resume and recovery preflight agree on candidate identity and recommended action.

### 3. Demote ledger owner/status fields from live authority

Status: implemented for topology preflight on 2026-06-13. `tools/check_tv_runner_topology.py` now keeps live-owner truth derived from live cron/process/loop/Kanban surfaces, demotes stale ledger owner/status/`allowed_surfaces` disagreement to `ledger_historical_owner_mismatch`, demotes old topology gates to `ledger_projection_stale`, and emits `ledger_reconciliation_actions: ["normalize_ledger_projection"]` instead of treating stale ledger projection data as a live-owner conflict. Remaining ledger writer/schema normalization belongs to item 4.

Target surfaces:

- `tools/check_tv_runner_topology.py`
- `tools/tv_runner_start_resume_preflight.py`
- `tools/tv_runner_recovery_preflight.py`
- `.hermes/long-running/tv-spec-implementation/task-ledger.json` schema/projection writer

Required behavior:

- Treat `task-ledger.json` as generated checkpoint projection/cache, not the primary live control plane.
- Derive live owner/liveness from Kanban claimed/running tasks, worker PIDs/process registry, cron/watchdog state, stop/lock files, and git state.
- Historical ledger fields such as `declared_owner`, `runner_ownership.implementation_owner`, `allowed_surfaces.*`, and ambiguous `status: running` must not block start/resume unless accompanied by a fresh source/timestamp assertion.
- Replace generic `ledger_stale` with precise classes such as `ledger_projection_stale`, `ledger_historical_owner_mismatch`, `dirty_handoff_pending`, `unsafe_dirty_state`, and true `live_owner_conflict`.
- Avoid representable current states like `running + none_active`; use explicit non-running recovery projection states such as `waiting_integration_recovery`, `push_ready_recovery`, `waiting_focused_verifier`, or `blocked_unsafe_dirty_state`.

Verifier/regression:

- Active Kanban worker + ledger `none_active` -> `resume_existing_owner`, not blocking `ledger_stale`.
- Clean idle repo + stale historical `status: running` -> start/seed action plus optional `normalize_ledger_projection`, not `missing_live_owner` solely from ledger.
- Ledger projection behind `events.jsonl` -> `ledger_projection_stale` with reconciler action, not live-owner conflict.

### 4. Add or extend deterministic ledger reconciliation

Status: implemented for `tools/tv_ledger_reconcile.py` on 2026-06-13. Dry-run reports source deltas, precise classifications, and a planned normalized projection; `--write` rewrites only `task-ledger.json`. The projection reads events, closeout packets, current git state, and live topology truth, emits `last_integrated_checkpoint`, `latest_worker_handoff`, `historical_notes`, and `generated_from`, selects the newest closeout packet matching current dirty paths, and refuses to promote stale ledger owner/status metadata into live owner truth.

Target surface:

- add or extend a command such as `python3 tools/tv_ledger_reconcile.py --write`.

Required behavior:

- Read `events.jsonl`, closeout packets, Kanban task state, current git HEAD/status, and process/owner truth surfaces.
- Write a normalized ledger projection with zones such as `last_integrated_checkpoint`, `latest_worker_handoff`, `historical_notes`, and `generated_from`.
- Dry-run mode must show the planned projection and classify stale/mismatched inputs before writing.
- The reconciler must refuse to invent live-owner state from stale historical metadata.

Verifier/regression:

- Projection staleness reports the reconciler action and source delta.
- Multiple closeout packets: newest packet/comment set matching current dirty paths wins; older packets remain historical evidence.

### 5. Wire recovery and gate normalization into integration-owner closeout/publish path

Target surfaces:

- `tools/tv_integration_lane.py`
- `tools/tv_runner_recovery_preflight.py`
- `tools/tv_runner_autostart.py`
- Kanban comments/events writers
- ledger reconciler/projection writer

Required behavior:

- The checkpoint/repaired-clean recovery path should feed a fuller integration-owner command that records or normalizes the Kanban/ledger `push_ready` packet and then runs the existing publish guard.
- `recover_push_ready_handoff` and `normalize_blocked_gates` should resolve automatically after deterministic review, rather than only blocking autostart from seeding over them.
- `--normalize-gates` / `--apply-gate-comments` should be callable from the publish/recovery closeout path after the specific bundle is verified and, when applicable, published.
- Decide explicitly whether autostart may call `--repair-unsafe-debris` automatically for the narrow safe debris class or whether that remains an explicit integration-owner operation.

Verifier/regression:

- Dry-run plans comments only for actionable `push_ready` / stale `review_required_process_bug` cards.
- Apply mode is idempotent: one comment/event per actionable card, zero duplicates on repeated apply.
- Publish/recovery closeout can normalize the specific gate it resolves without relying on an operator to run a separate planner manually.

### 6. Validate closeout packets as consumable machine contracts

Target surfaces:

- closeout packet writer/validator;
- recovery classifier;
- Kanban handoff/comment writer.

Required behavior:

- Closeout packets intended for recovery must include `closeout_class`, `kanban_task` or `task_id`, `changed_files`, structured `verification`, `next_action`, `event_ids` when known, and `successor_kanban_task` when applicable.
- Packets must include enough verifier command text for a later recovery pass to choose `checkpoint_and_push_ready` vs `rerun_focused_verifier`.
- Reject `ready_for_review_or_integration` unless historical; reject generic `review-required` unless paired with a concrete `blocked: explicit_human_gate` reason.

Verifier/regression:

- Safe dirty bundle + focused verifier pass + unrelated broad failures + no commit + local closeout packet/Kanban comment evidence -> `checkpoint_and_push_ready` or `rerun_focused_verifier`, never generic `review-required` or `unsafe_dirty_state`.

### 7. Preserve narrow verifier routing and reporting discipline

Target surfaces:

- verifier-map command/checker, possibly `tools/backlog_dispatch_index.py check` or a dedicated verifier-map command;
- worker prompt/closeout surfaces that choose verifiers;
- watchdog/reporting jobs.

Required behavior:

- Verifier selection should be mechanically routed from `docs/checklists/tv-verifier-impact-map.json` before any broad native discovery.
- Broad native discovery remains checkpoint/risk-boundary verification, not a default slice gate.
- Routine watchdogs should be script-first/no-agent or LLM-light and stay silent unless a material state transition occurs: stale gate converted, integration pushed, real explicit gate found, successor started, or watchdog/tooling failure.
- LLM-assisted review may assess exact-bundle risk after deterministic guards pass; it must not override failed deterministic safety gates.

Verifier/regression:

- Scenario-only change routes to focused scenario/unit verifier.
- Docs/process-only change routes to readback/search plus `git diff --check`.
- Synthetic stale-gate fixture emits exactly one bounded remediation/report packet; no-change run is quiet.

## Suggested implementation order

1. Add the shared dirty-handoff evidence aggregation layer and consume closeout packets/Kanban comments.
2. Add `t_4ad7b9e5`-shape regression fixtures for packet/comment evidence, safe dirty bundle, and verifier pass.
3. Demote ledger owner/status fields from live authority and introduce projection-staleness classes.
4. Add or extend deterministic ledger reconciliation with dry-run/write modes.
5. Wire recovery classifier, ledger reconciler, and gate normalization into integration-owner checkpoint/publish closeout and autostart reporting.
6. Add closeout-packet completeness validation and verifier-map routing regressions.

## Gates

- Reinspect live state before applying dated evidence-case repairs.
- Do not mutate external/account/provider/gateway/config surfaces, force-push/rewrite history, delete tracked work, or publish raw/proprietary/source-capture material without explicit authorization.
- Normal non-force TV repo commits/pushes remain governed by the project push policy in `docs/research/tv-spec.md` and the user's standing TV workflow preference.
