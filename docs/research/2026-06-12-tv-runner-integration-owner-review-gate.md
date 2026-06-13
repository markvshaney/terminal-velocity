# TV runner ownership and integration-recovery failure analysis

Date: 2026-06-12
Source: Loki Game Telegram assistant posts in session `20260611_225234_b37aa40b`:
- `03:07:24 EDT`, message id `57534`: runner status.
- `03:10:48 EDT`, message id `57544`: integration-owner policy check.
- `03:14:38 EDT`, message id `57559`: worker `push_ready` failure diagnosis.
Status: systemic control-plane failure analysis with partial implementation notes through the current start/resume/autostart guard setup; source text is summarized, not copied verbatim.
Reconstruction note: this artifact was reconstructed after accidental deletion. Treat reconstructed prose and any "now says" live-state claims as needing source/readback verification before implementation.

Purpose: comprehensive current-setup deficiency review plus proposed `tv-spec.md` edit. The embedded spec patch is an intentional deliverable of this artifact, not evidence that the spec has already changed. Later applied notes distinguish implemented control-plane behavior from still-recommended follow-up.

Status legend:

- **evidence_snapshot:** dated evidence reconstructed from the cited session and local inspections; reverify live state before acting.
- **durable_decision:** policy conclusion intended to survive the evidence case.
- **confirmed_fix_target:** current repair surface believed actionable after pre-edit evidence checks.
- **candidate_spec_edit:** proposed wording for `docs/research/tv-spec.md`; not applied unless a later spec-edit pass is explicitly requested.
- **applied_status_claim:** dated claim that some related surface was already changed; re-inspect before relying on it.
- **explicitly_gated:** requires the named authorization before mutating that surface.
- **unresolved_hypothesis:** unresolved mechanism or evidence gap with the next evidence surface named.

## Scope and durable decision

This artifact is not a single-incident report. The `t_d8b44829` stopped worker is the evidence case that exposed a broader failure cluster in TV runner ownership, closeout classification, integration recovery, verifier routing, and start/resume liveness. Preserve the detailed evidence because the repair needs to address the class of failure, not only unblock one task.

Durable decision: verified safe-local TV work must not close out as generic human `review-required`. It must resolve to one of: `continue`, `push_ready`, or a concrete `blocked:*` class with the exact blocker named. A human gate exists only for the already-defined safety/fidelity/publication/destructive/external/account/config boundaries, not merely because files changed, a worker lacks push authority, or an unrelated broad suite is red.

## Usage contract

This artifact is not a one-shot recommendation and not a request for human code review. Use it as a comprehensive systemic repair proposal and candidate `tv-spec.md` edit record. It defines an iterative control-plane repair loop:

1. **Investigate.** Reconstruct the live runner state from repo, Kanban, ledger/events, cron/process/watchdog, topology, and worker handoff evidence. Separate source-backed facts from hypotheses.
2. **Diagnose.** Classify each failure as one of: stale process gate, missing live owner, unsafe dirty state, relevant verifier failure, stale/ambiguous instruction surface, or real human-gated boundary.
3. **Fix.** Apply the smallest safe-local correction for the diagnosed class: integration-owner recovery, closeout-contract patch, start/resume protocol, verifier routing change, backlog linkage, or explicit `blocked:*` state.
4. **Verify.** Prove the fix with the relevant local check: exact dirty-bundle inspection, focused verifier output, topology/start preflight JSON, closeout-classifier regression, integration-lane dry-run, pushed-head verification when publication is in scope, or artifact readback.
5. **Iterate if needed.** If the first diagnosis is disproven or incomplete, do not broaden into generic policy. Record the unresolved hypothesis, gather the next evidence surface, revise the diagnosis, and run the next narrow fix/verification loop.

The intended outcome is a runner/start/closeout process that can continue Terminal Velocity game-development work until a real gate is reached. Any remaining uncertainty must be represented as an explicit investigation item with evidence needed, not as an implicit human review stop.

Do not blindly replay dated commands or state from the evidence snapshot. Treat those details as provenance for the failure class; before acting, re-inspect live repo/Kanban/runner/ledger state and apply the current narrow correction.

Implementation read order:

1. Reinspect live repo/Kanban/ledger/runner state before treating any evidence snapshot as current.
2. If the `t_d8b44829` evidence case is still live, start with P0 recovery and stop at any real `blocked:*` gate.
3. If the evidence case is no longer live, treat P0 as historical context and start with P1/P2 prevention: closeout validation, verifier routing, and integration-recovery/start-resume dry-run behavior.
4. Apply the candidate `tv-spec.md` edit only when the task explicitly authorizes spec mutation; otherwise review this artifact only.
5. Verify implementation with dry-run JSON, closeout regression fixtures, targeted search/readback, and the normal publication checks when push is in scope.

## Evidence/inference/action taxonomy

- **Observed evidence:** live topology, cron/process state, autostart state file, Kanban state, git state, integration-lane dry-run, dispatch preflight, ledger/events, and then-current spec/prompt language inspected around the 2026-06-12 evidence case.
- **Inferred failure class:** stale worker closeout plus missing live integration-owner/runner consumption; not a credential problem and not an inherent human gate.
- **Concrete repair path:** recover the stale handoff when still live, then harden worker closeout, verifier selection, integration-owner recovery, and runner start/resume preflight so the same class cannot recur.
- **Iteration trigger:** if a searched surface does not actually contain the suspected stale instruction, leave that mechanism unresolved and inspect the next candidate surface before editing policy.

## Evidence snapshot finding

At the 2026-06-12 inspection, the TV runner was not actively working. Live state showed no active implementation owner, no TV implementation cron, no active worker/continuous-runner process, and Kanban task `t_d8b44829` blocked as `review-required` while the repo was at `HEAD == origin/main` with six dirty worker-slice files.

## Policy expectation

The repo already defines an autonomous integration owner for coherent TV bundles. The integration owner owns fan-in, final diff review, verification, commit, normal non-force push, fetch, and `HEAD == origin/main` verification, using `tools/tv_integration_lane.py --dry-run` before publish and `--push --llm-approved` only after approval/guard success.

Worker closeout validators must reject human `review-required` for verified safe-local TV work unless the packet names `blocked: explicit_human_gate` and the exact gated boundary. When publication/integration is needed, workers/continuous runners must produce a committed, reviewable `push_ready` bundle with commit SHA, intended files, verification commands/results, known unrelated failure surfaces, and next action, leaving normal non-force push to the integration owner.

## Evidence case: actual failure

Worker task `t_d8b44829` implemented and verified a route-fuel hop-count/status slice, but ended in the old bad pattern:

- dirty uncommitted worktree;
- no staged changes;
- no new commit after `bfa9360`;
- Kanban blocked as `review-required`;
- ledger wording used `ready_for_review_or_integration` instead of canonical `push_ready`.

The worker ran broad native discovery, saw six known runner-topology/integration-lane failures, recognized them as unrelated to the scenario-eval slice, but after compaction still classified the safe-local slice as requiring review because files changed and the broad suite was not fully green.

## Systemic diagnosis

This was a worker closeout/control-plane bug, not a credentials problem and not a real human gate. The worker stopped before `git add` / `git commit`, so it could not honestly record `push_ready` with a commit SHA. The live integration-owner policy/tool existed, but no active live integration owner was catching the stale `review-required` block and converting it into a normal integration pass. The broader failure is the absence of a reliable owner/start/closeout path that consumes this state and produces either integration recovery or a concrete `blocked:*` reason.

Revised diagnosis: do not attribute the broad native discovery step to persistent worker memory or autonomous worker habit. There is no evidence here that workers retain legacy verification preferences internally. The safer diagnosis is that broad native discovery appears to be over-selected by worker prompts, handoffs, or closeout tooling as a default confidence check. If repeated workers start fresh from prompt/config/artifacts, then recurrence points to durable instruction surfaces or copied handoff patterns, not worker retention.

### Evidence snapshot: additional live topology inspected 2026-06-12

The 2026-06-12 live topology inspection adds causal detail beyond "the integrator was not in a live lane":

- `python3 tools/check_tv_runner_topology.py` returned `ok: true`, `live_implementation_owner: none_active`, `declared_implementation_owner: none_active`, and no conflicts/warnings. That means the topology checker could prove absence of a conflicting owner, but it did not treat missing owner/liveness as a blocker when a start/resume was intended.
- Hermes cron list for the `loki-game` profile contained only `Daily Loki Game memory hygiene`; there was no enabled TV implementation, autostart, integration-owner, or passive TV reporter cron. `process list` returned no tracked background processes.
- `/home/bh/.hermes/profiles/loki-game/cron/tv_runner_autostart_state.json` still recorded a prior autostart `seed_and_dispatch` action and `last_seeded_task: t_d8b44829`, plus earlier `idle_dirty_repo`, but no corresponding scheduled autostart job was live. The state file persisted, the control loop did not.
- Kanban board summary showed 263 tasks: 220 `done`, 43 `blocked`, and zero `running`, `ready`, or `scheduled` tasks for assignee `terminal-velocity`. The newest blocked tasks include `t_d8b44829` and `t_50368210`, both user-created autostart continuation tasks.
- Git status showed `main...origin/main` with no ahead/behind commits, six worker-slice dirty files, and the owner-analysis artifact untracked at inspection time. `python3 tools/tv_integration_lane.py --dry-run` returned `dirty_worktree` and `nothing_to_publish`; it can guard/push committed bundles, but it does not recover an uncommitted worker slice by itself.
- `python3 tools/backlog_dispatch_index.py runner-preflight` passed. The dispatch index/verifier-map layer was not the blocker.
- Ledger state was internally mixed: `status: running`, `declared_owner: none_active`, `runner_ownership.implementation_owner: none_active`, `current_gate_classification.review_required_process_bug: true`, and `last_reconciled_live_git.active_kanban_task: t_d8b44829`. The ledger knew the stale review gate was a process bug and pointed at the active task, but no live owner was consuming that fact.
- Event tail shows the recurring pattern: verified slices produced `push_ready` events for prior checkpoints, then later `review-required` was reclassified as a process bug, and the latest `t_d8b44829` route/fuel slice recorded focused verifier success plus broad native discovery failures labeled unrelated to the slice.

## Failure modes and concrete repair points

1. **Policy/tool availability was mistaken for a live lane.** `tv-spec.md` defines an integration owner and `tools/tv_integration_lane.py` exists, but live cron/process/Kanban evidence showed no scheduled or running actor invoking it.
   - Target surface: start/resume protocol.
   - Required behavior: verify an actual running/claimed owner or execute a one-shot integration-recovery action; do not treat `integration_owner` availability in the ledger as live ownership.
   - Verification target: preflight output includes `live_owner_verified` or `integration_recovery_completed`, otherwise `blocked: missing_live_owner`.

2. **The topology checker proves conflicts, not liveness obligations.** A clean `none_active` topology is acceptable for idle/manual states, but it is insufficient when the requested operation is "start/resume TV runner."
   - Target surface: topology/start preflight.
   - Required behavior: include `startup_intent` and fail/report `missing_live_owner` unless the preflight starts/claims exactly one owner surface or selects integration recovery.
   - Verification target: startup-intent fixture with `none_active` cannot pass solely from `topology_conflict: false`.

3. **Autostart state was durable, but autostart execution was not.** The state file records prior seed/dispatch and idle-dirty outcomes, while cron/process inspection shows no live autostart job.
   - Target surface: runner start/autostart preflight.
   - Required behavior: distinguish `state_file_exists` from `watchdog_scheduled/running`, and verify the watchdog or worker actually remains live after seeding.
   - Verification target: preflight JSON exposes separate `state_file_exists`, `watchdog_scheduled`, `watchdog_running`, and `worker_live` fields.

4. **Autostart can observe idle dirty state but cannot remediate it.** `tools/tv_runner_autostart.py` blocks on `idle_dirty_repo`; it does not match dirty paths to recent blocked handoffs, create a checkpoint, normalize `review-required` to `push_ready`, or invoke integration-owner recovery.
   - Target surface: `tools/tv_runner_autostart.py` and the selected integration-recovery preflight.
   - Required behavior: run integration-recovery classification before `seed new continuation` and before generic `stop dirty` when the lane is idle and the repo is dirty.
   - Verification target: idle dirty repo plus matching blocked handoff returns recovery recommendation instead of prose-only stop.

5. **The integration lane is too narrow for stale uncommitted worker handoffs.** `tools/tv_integration_lane.py --dry-run` correctly blocks dirty worktrees for publish safety, but this failure class needs a pre-publish recovery mode for an exact dirty bundle with focused verification.
   - Target surface: `tools/tv_integration_lane.py` or `tools/tv_runner_recovery_preflight.py`.
   - Required behavior: add a dry-run `recover-handoff` classifier that validates intended dirty files, sensitive paths, and targeted verifier freshness, then recommends checkpoint creation before normal publish preflight.
   - Verification target: uncommitted matching handoff fixture returns one of `checkpoint_and_push_ready`, `rerun_focused_verifier`, `unsafe_dirty_state`, or `missing_handoff`.

6. **Kanban status taxonomy stranded live work in `blocked`.** The board had zero `running`/`ready`/`scheduled` tasks and 43 blocked tasks; dispatch/autostart can ignore blocked history for liveness, but the newest blocked dirty-matching task was the active recovery target.
   - Target surface: Kanban scan in start/resume or integration-recovery preflight.
   - Required behavior: classify blocked cards by age/relevance; ignore old clean-history blocks for liveness; promote the newest dirty-matching `review-required`/`ready_for_review_or_integration` card into integration recovery.
   - Verification target: fixture with old blocked cards plus one dirty-matching current blocked card selects the dirty-matching card as recovery target.

7. **Ledger truth was not coupled to an executor.** The ledger recorded `review_required_process_bug: true` and pointed at `t_d8b44829`, but `declared_owner` and live owner were both `none_active`.
   - Target surface: ledger/start-resume coupling.
   - Required behavior: when the ledger records a process-bug gate with dirty work, the next start/resume must either run the recovery owner or mark `blocked: missing_live_owner` with the command/surface needed to recover.
   - Verification target: ledger fixture with `review_required_process_bug: true` and dirty matching task cannot leave `status: running` with `none_active` owner.

8. **Broad native discovery failures were known unrelated but still shaped closeout.** The latest ledger/event state labels six runner topology/integration-lane failures as unrelated to the route/fuel slice, yet the worker still ended as review-required.
   - Target surface: closeout validator and tooling-backlog routing.
   - Required behavior: make `known_unrelated_failure_surface` non-gating when focused required verifiers passed, and route separate topology/integration test failures to owner tooling backlog instead of worker review gates.
   - Verification target: focused-pass plus unrelated-broad-failure fixture cannot validate as generic `review-required`.

## First repair iteration for the evidence case

If the 2026-06-12 evidence case is still live, resolve it by treating `review-required` as stale process state: inspect the exact dirty bundle, rerun/confirm targeted verification, create the coherent local checkpoint/`push_ready` bundle if clean, then let the autonomous integration owner run the deterministic dry-run/review/push path. Separately harden worker closeout so verified safe-local TV slices cannot end as human `review-required` merely because broad unrelated topology tests fail or files changed.

If that classification is disproven by inspection, iterate: record which assumption failed, classify the actual blocker under the concrete `blocked:*` taxonomy, and apply the next narrow safe-local correction rather than falling back to generic human review.

## Systemic framing note added 2026-06-12

Artifact disposition: treat this as a control-plane fix for the long-running TV game-development loop, not as a request for human code review. The high-value distinction is:

- **real gate:** unsafe dirty state, failed relevant verifier, force/history/destructive/config/external/publication-risk boundary, unresolved source/fidelity conflict, or no safe local continuation;
- **stale process gate:** a worker labels a verified safe-local bundle `review-required` only because files changed, a broad unrelated suite is red, or the worker lacks publication authority.

The long-running task goal is continuous Terminal Velocity game development. Start/resume preflight must minimize idle time by converting stale process gates into integration-owner work automatically while preserving source/fidelity discipline and normal non-force publication checks. Under startup intent, preflight must return exactly one of: `integration_recovery`, `seed_successor`, or `blocked:*`; it must not report clean idle success solely because topology has no conflict.

Inference correction: do not describe broad native discovery as a habit retained by autonomous workers. There is no evidence here of a persistent worker-specific memory mechanism carrying a legacy preference for broad native discovery. Workers may start fresh from prompt, config, artifacts, and task inputs; if so, repeated broad native discovery is not worker retention.

Mechanism hypothesis: I infer that broad native discovery is being reproduced by some durable instruction surface or copied handoff pattern, not by autonomous workers remembering prior habits. The plausible reproduction path is prompt/artifact/tooling inheritance: each fresh worker may receive a continuation prompt, skill/spec excerpt, backlog item, task template, closeout checklist, copied worker comment, ledger handoff, or compaction summary that still says or implies broad native discovery as a standard confidence check for Python/native changes. That can make the behavior recur without any autonomous worker "remembering" an old habit. The fix target is therefore the durable instruction surfaces and closeout tooling that select verifiers, not the workers as agents.

Current-spec contradiction: `docs/research/tv-spec.md` already forbids routine broad native discovery. It names `docs/checklists/tv-verifier-impact-map.json` as the canonical map from touched surfaces to the cheapest sufficient verifier families; says each increment needs the narrowest verifier that proves the changed claim; and treats full native discovery (`python3 -m unittest discover -s native_ev/tests -p 'test_*.py'`) as checkpoint-optional for several surfaces rather than always required.

Safer claim for follow-up edits: broad native discovery appears to be over-selected by older/conservative worker prompts, handoffs, or closeout tooling as a default confidence check. Workers then overfit to "prove nothing broke anywhere" instead of "prove this touched surface"; when broad discovery exposes known unrelated failures, some closeouts misclassify the focused-passing slice as not clean. The fix is to make verifier-impact-map routing authoritative and state that broad native discovery is checkpoint-optional unless justified by touched surface, risk, handoff/checkpoint boundary, integration-owner preflight, unclear dependency risk, large accumulated bundle sealing, or explicit user request.

## Unresolved hypotheses requiring follow-up evidence and fix targets

Follow-up evidence collected on 2026-06-12 turns several items from generic hypotheses into concrete repair targets. Preserve historical event/comment records as evidence; patch only live prompts, skills, checkers, and runner tools that fresh workers or start/resume paths actually consume.

Use this section as an investigation queue, not as a stop gate. Each item must resolve to one of: `confirmed_fix_target`, `historical_only`, `not_reproduced`, or `unresolved_hypothesis` with the next evidence surface named.

No vague future promises: any forward-looking wording in this section must resolve to one of:

- an executable fix target with target surface, trigger condition, action, verifier, and gate;
- `historical_only` evidence that must not be patched;
- `unresolved_hypothesis` with `next_evidence_surface` named;
- `explicitly_gated` with the exact gate named.

### Remaining causal gaps before implementation

These gaps do not block the highest-priority confirmed fixes. They prevent overclaiming about the exact historical mechanism and define the next evidence surface for any implementation pass.

1. **`causal_gap`: exact source of the evidence-case `review-required` decision.**
   - Current evidence: the evidence-case Kanban task blocked as `review-required`, the task comment cited code/docs/ledger changes needing human/integration review, and the ledger used `ready_for_review_or_integration` vocabulary.
   - Unproven link: the artifact does not prove which loaded prompt, skill, template, validator, or closeout packet caused the actual worker to choose generic human review.
   - `next_evidence_surface`: archived worker prompt/skill bundle/load order, closeout packet, worker handoff comment, and ledger event writer for `t_d8b44829`.
   - Non-blocking action: implement the closeout validator and canonical status regression first; classify the exact historical source only if the evidence surface is still recoverable.

2. **`causal_gap`: whether generic `kanban-worker` guidance reached the TV worker.**
   - Current evidence: generic `kanban-worker` guidance contains a human-review closeout rule, and TV-specific runner policy defines a different `push_ready` / integration-owner path.
   - Unproven link: the artifact does not prove the evidence-case worker loaded generic `kanban-worker`, loaded it after TV-specific overrides, or used it as the closeout authority.
   - `next_evidence_surface`: fresh `terminal-velocity` worker creation/config path, injected skill list, skill load order, and any saved worker startup transcript.
   - Non-blocking action: treat the generic rule as a confirmed reproduction risk; require TV-specific override visibility in fresh workers regardless of whether it caused the historical case.

3. **`causal_gap`: why the live owner/watchdog was absent.**
   - Current evidence: topology, cron/process, autostart state, Kanban, git, and ledger inspections showed no active owner while stale dirty work and process-bug state existed.
   - Unproven link: the artifact proves absence of a consumer, but not whether the owner was never scheduled, exited, was manually stopped, was lost across compaction/profile boundaries, or lacked a durable scheduler by design.
   - `next_evidence_surface`: runner wrapper logs, Hermes process/session records, cron history, autostart state transition history, and any stop/lock files for the selected owner surface.
   - Non-blocking action: implement start/resume preflight that treats `startup_intent + none_active` as `missing_live_owner` or integration recovery; root-cause the historical disappearance only if needed to prevent recurrence.

4. **`causal_gap`: whether stale broad-discovery references are active inputs.**
   - Current evidence: older TV skill references framed broad native discovery as routine, while current top-level policy points to verifier-impact-map routing.
   - Unproven link: the artifact does not prove those references are consumed by current fresh workers or start/resume prompts.
   - `next_evidence_surface`: active caller search for continuation prompts, skill references, stored Kanban prompts, cron prompts, task templates, and checkers that fresh workers actually load.
   - Non-blocking action: classify edited stale references as confirmed stale surfaces; require active-surface evidence before claiming they caused a specific worker closeout.

5. **`causal_gap`: stale dirty handoff recoverability depends on handoff completeness.**
   - Current evidence: the proposed recovery path can match dirty paths against task comments, ledger/event tail, intended files, and verifier output.
   - Unproven link: not every stale dirty state is guaranteed to contain enough handoff evidence to create a safe checkpoint.
   - `next_evidence_surface`: recovery-classifier fixture set covering complete handoff, stale verifier, missing handoff, mismatched dirty files, and sensitive/unrelated paths.
   - Non-blocking action: make `missing_handoff`, `rerun_focused_verifier`, and `unsafe_dirty_state` first-class classifier outcomes instead of falling back to `needs_human`.

6. **`causal_gap`: ledger process-bug truth is not coupled to an executor.**
   - Current evidence: ledger state recorded `review_required_process_bug: true` and identified the active task, while owner fields remained `none_active`.
   - Unproven link: the exact missing component is not isolated between ledger writer invariants, runner start preflight, autostart watcher, and integration-owner scheduler.
   - `next_evidence_surface`: ledger schema/writer, start/resume preflight code, autostart dry-run path, integration-owner scheduler entry point, and fixtures for `status: running + none_active`.
   - Non-blocking action: add a machine-checkable invariant: process-bug truth plus matching dirty work must route to recovery or emit `blocked: missing_live_owner`.

7. **`causal_gap`: candidate `tv-spec.md` patch may not be the active policy ingestion point.**
   - Current evidence: the artifact contains a candidate spec patch, and current spec text already contains related safe-local/push-ready policy.
   - Unproven link: applying the patch to `tv-spec.md` alone may not reach fresh worker prompts, closeout validators, or start/resume tools.
   - `next_evidence_surface`: active caller/citation search for `tv-spec.md`, continuation prompt assembly, worker skill bundle construction, and closeout-validator inputs.
   - Non-blocking action: before spec mutation, re-inspect `tv-spec.md` and patch the active loaded surface or validator that workers actually consume.

### Hypothesis-to-action matrix

1. **Durable broad-discovery instruction source — `confirmed_fix_target`.**
   - Evidence found: `ev-terminal-velocity-play/references/terminal-velocity-source-aligned-vertical-slices.md` says to "run targeted + broad verification" before selecting the next slice and lists full native discovery plus Godot self-test as a minimum gameplay verification pattern.
   - Evidence found: `ev-terminal-velocity-play/references/terminal-velocity-autonomous-restart-prompt.md` still frames `python3 -m unittest discover -s native_ev/tests -p 'test_*.py'` as the Python test in the fast lane and says to run targeted verification, then broader cheap verification.
   - Current contradiction: the top-level `ev-terminal-velocity-play` skill now contains the better rule: use `docs/checklists/tv-verifier-impact-map.json` first and treat full native discovery as checkpoint-optional. Older references/templates still reproduce broad discovery as the default confidence check.
   - Fix target: patch or demote the older restart/vertical-slice references so broad native discovery is named as checkpoint/risk-boundary verification, not the default slice verifier.
   - Verification target: `skill_view` the edited references and search active prompt/reference surfaces for broad-discovery default-gate wording; classify any remaining hits as current policy, example, compatibility pointer, or historical evidence.

2. **Exact source of `ready_for_review_or_integration` — `confirmed_fix_target` for new closeout packets; `historical_only` for old records.**
   - Evidence found: the current evidence-case Kanban task `t_d8b44829` blocks with `review-required`, and its comment says "needs human/integration review before merge because code/docs/ledger changed."
   - Evidence found: the ledger field `last_reconciled_live_git.checkpoint_decision` contains `safe_local_route_fuel_hop_count_status_increment_ready_for_review_or_integration`.
   - Diagnosis: the phrase is primarily a ledger/checkpoint vocabulary leak, not the live Kanban block label itself.
   - Target surface: closeout-packet/checkpoint validator and any schema or event writer that creates new checkpoint decisions.
   - Trigger condition: any new closeout/checkpoint packet attempts to emit `ready_for_review_or_integration` outside a historical-evidence fixture.
   - Action: reject the packet and normalize the outcome to `push_ready` or a concrete `blocked:*` class before it reaches ledger/Kanban state.
   - Verification target: regression fixture containing `ready_for_review_or_integration` fails validation unless marked `historical_only`; fixture with `push_ready` plus commit SHA/intended files/verifier output passes.
   - Gate: historical ledger/event rewrites require explicit state-repair authorization; otherwise old records remain evidence.

3. **Why no live owner/watchdog existed — `confirmed_fix_target` as idle-dirty recovery gap.**
   - Evidence found: `python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner` reports `ok: true`, `live_implementation_owner: none_active`, and only `ledger_stale` because startup owner differs from stale ledger owner.
   - Evidence found: `python3 tools/tv_runner_autostart.py --dry-run` reports: `TV runner autostart blocked: idle lane but repo has uncommitted work; integration owner must cohere/publish or preserve it before seeding new work` and shows the current dirty files.
   - Evidence found: `python3 tools/tv_integration_lane.py --dry-run` reports `dirty_worktree`, `nothing_to_publish`, and `needs_human` because it only handles committed branch-ahead publish candidates, not uncommitted handoff recovery.
   - Diagnosis: the missing owner is a recovery-orchestration hole. Autostart correctly refuses to seed overlapping work, but no deterministic integration-recovery owner consumes the matching dirty handoff.
   - Fix target: add an uncommitted-handoff recovery classifier and make start/resume route matching dirty handoffs through it before any new continuation seed.
   - Verification target: dry-run fixture for idle dirty repo + matching blocked handoff returns `checkpoint_and_push_ready`, `rerun_focused_verifier`, `unsafe_dirty_state`, or `missing_handoff`, not generic `needs_human`.

4. **Existing topology startup support — `confirmed_fix_target` to extend, not reinvent.**
   - Evidence found: the topology checker already has a usable startup-owner mode and can distinguish clean topology from stale ledger intent.
   - Gap: its success condition proves "no conflict," not "a runner or integrator is live."
   - Fix target: extend the existing startup-owner path so a start/resume flow also asserts one of: owner claimed/started, integration recovery completed, or explicit `missing_live_owner`/`unsafe_dirty_state` emitted.
   - Verification target: topology/start preflight JSON includes `startup_intent`, `live_implementation_owner`, `recommended_action`, and `explicit_gate`, and does not report start success solely from `topology_conflict: false`.

5. **Canonical owner surface — `confirmed_fix_target`.**
   - Target surface: runner/start tooling or spec text that defines TV start/resume owner selection.
   - Trigger condition: a start/resume or autostart preflight is invoked for TV game-development work.
   - Required behavior: implementation ownership remains the continuous Kanban worker/runner surface once the repo is safe to mutate; dirty handoff/publication ownership is a distinct integration-recovery lane that runs before autostart seeds new work; passive reporters/watchdogs may observe and report material transitions but must not mutate implementation state.
   - Verification target: a start/resume dry-run emits exactly one selected mutating owner/recovery surface plus passive reporter status, not a list of plausible mechanisms.

6. **Separate tooling backlog for broad-suite failures — `confirmed_fix_target` for closeout misuse; `explicitly_gated` for backlog mutation.**
   - Evidence found: the evidence-case task already labeled the six full-discovery failures as unrelated live-state topology/integration-lane failures, while focused scenario eval and all gameplay scenarios passed.
   - Diagnosis: the immediate failure is not absence of a label; it is closeout policy allowing unrelated broad-suite failures plus generic code/docs/ledger changes to become `review-required` anyway.
   - Target surface: closeout classifier/validator for worker handoffs and any packet schema that records `known_unrelated_failure_surface`.
   - Trigger condition: focused verifier(s) passed and broad-suite failures are labeled unrelated to the touched surface.
   - Action: reject `review-required`; allow only `continue`, `push_ready`, or a concrete `blocked:*` class.
   - Verification target: evidence-case fixture with focused pass + unrelated broad failures cannot validate as generic `review-required`.
   - Backlog-linkage gate: adding a new backlog item is `explicitly_gated` on backlog mutation authorization. If granted, first search the live backlog/issue surface for existing topology/integration-lane tooling items; if none exist, add exactly one narrow tooling item in the appropriate project surface for the six failures.

7. **Generic Kanban/skill overload as a reproduction surface — `confirmed_fix_target`.**
   - Evidence found: `kanban-worker/SKILL.md` still instructs most code-changing tasks to block as `review-required` until a human reviewer has eyes on them. That generic rule matches the observed block shape.
   - Evidence found: `ev-terminal-velocity-play` has been reduced toward pointer-level process guidance, but older gameplay/restart references still embed process-heavy verification and continuation defaults.
   - Evidence found: `long-running-runner-operations` now carries the correct TV-specific exception: safe-local TV `review-required` is integration-owner work, not a human gate.
   - Target surface: the fresh `terminal-velocity` Kanban worker creation/config path and any generic `kanban-worker` closeout skill loaded by that path.
   - Trigger condition: a fresh `terminal-velocity` Kanban worker is spawned for code-changing TV work.
   - Required behavior: the TV-specific override must be visible after any generic Kanban worker closeout rule, or the generic `kanban-worker` skill must explicitly defer to project-specific local-commit/integration-owner policy when present.
   - Verification target: captured fresh worker skill bundle/order contains the TV runner/push policy after generic Kanban guidance, or the generic skill readback contains an explicit project-specific-policy deferral.

8. **LLM-heavy process steps without deterministic owners — `confirmed_fix_target`.**
   - Evidence found: `tv_integration_lane.py` is deterministic only after a clean local checkpoint exists; it cannot validate and checkpoint the current uncommitted dirty handoff.
   - Evidence found: `tv_runner_autostart.py` can detect idle dirty state and stop safely, but it cannot match dirty paths to the blocked handoff or recommend `checkpoint_and_push_ready` vs `unsafe_dirty_state` in JSON.
   - Evidence found: worker closeout status, verifier selection, and packet completeness are still mostly prose/LLM choices.
   - Fix target: add a dry-run uncommitted-handoff recovery classifier before publish dry-run, wire autostart to invoke/report it before seeding new work, and add mechanical verifier-map and closeout-packet validation.
   - Verification target: deterministic scripts emit bounded JSON packets; LLM review consumes exact JSON plus diff only after deterministic guards pass.

### Pre-edit evidence checklist

Before patching active surfaces, run these checks and record the result in the implementation notes for the patch:

- **Fresh worker skill bundle check**
  - Target surface: the command/config path that creates a fresh `terminal-velocity` Kanban worker.
  - Action: inspect which skills are actually injected, including whether generic `kanban-worker` is automatic when the card lists only `long-running-task-harness`, `source-and-fidelity`, and `artifact-governance`.
  - Output classification: `tv_override_visible_after_generic`, `generic_only`, `no_generic_kanban`, or `unresolved_hypothesis` with the next evidence surface.

- **Active-surface search check**
  - Target surface: live prompts, skill references, templates, checkers, and runner tools that fresh workers/start-resume paths consume.
  - Action: search for broad-discovery default-gate wording and generic `review-required` closeout wording.
  - Output classification: `patch_current_policy`, `historical_only`, `compatibility_pointer`, or `not_reproduced`.
  - Non-action: old events, comments, and this artifact remain historical evidence unless an explicit state-repair operation is authorized.

- **Broad-suite preservation check**
  - Target surface: any patch touching verifier wording.
  - Action: preserve full native discovery as checkpoint/risk-boundary verification while removing it as a default slice gate.
  - Verifier: targeted search shows no active wording that makes full native discovery mandatory for every worker slice, while at least one current policy surface still permits it for checkpoint/risk-boundary cases.

- **Unresolved-item handling check**
  - Trigger condition: a searched evidence surface does not confirm or disprove a hypothesis.
  - Action: mark that item `unresolved_hypothesis` with `next_evidence_surface`, then execute the highest-priority remaining `confirmed_fix_target` instead of blocking on the unresolved item.

## Fix plan by process phase

The fixes below are ordered by urgency. Before implementation, each fix item must identify evidence, target surface, trigger condition, required behavior, verifier, and gate. If any field is missing, add it to the implementation notes before editing the target surface.

### P0 — iteration 1: recover the evidence-case stopped loop

1. **Classify the evidence-case Kanban block as stale process state.**
   - Evidence: task `t_d8b44829` is blocked as `review-required`; changed files are local safe TV code/tests/docs/ledger; targeted scenario verification and all gameplay scenarios passed; broad native discovery failures were already identified as unrelated runner-topology/integration-lane tests.
   - Required behavior: no human review gate for this safe-local bundle.

2. **Run integration-owner preflight over the exact dirty bundle.**
   - Inspect `git status --short --branch` and the dirty file list.
   - Review the worker handoff comment and ledger/event tail.
   - Rerun or accept recent targeted verification only if the command outputs are sufficiently current for the exact dirty bundle; otherwise rerun the targeted route/fuel verifier set.
   - Confirm no proprietary/raw-capture/secrets/unrelated paths are present.

3. **Create a coherent local checkpoint commit or explicit `push_ready` packet.**
   - If the dirty bundle is coherent and targeted verification is still valid, stage only the intended six files and commit them with a route/fuel slice message.
   - Record `push_ready` with commit SHA, intended files, verification commands/results, known unrelated broad-suite failure surface, and next action.
   - Do not record `ready_for_review_or_integration`; use canonical `push_ready` for publication/integration handoff.

4. **Run the deterministic integration lane and normal push path.**
   - Run `python3 tools/tv_integration_lane.py --dry-run` against the committed bundle.
   - If the guard is clean and the LLM-assisted same-bundle review returns publish, run `python3 tools/tv_integration_lane.py --push --llm-approved`.
   - Fetch and verify `HEAD == origin/main`.
   - Complete or unblock `t_d8b44829` with the pushed commit and verification summary.

5. **Seed/dispatch the next continuation.**
   - If no real gate remains, create exactly one successor continuation task or let `tools/tv_runner_autostart.py` seed/dispatch it.
   - Verify the successor reaches `running` or clearly reports the next explicit blocker.

### P1 — harden worker closeout so the bug does not repeat

6. **Patch the worker closeout contract.**
   - Replace any `review-required` closeout for verified safe-local TV work with this decision table:
     - relevant verifier failed -> `blocked: verifier_failed`;
     - unsafe/unrelated/proprietary/destructive/config/external state -> `blocked: explicit_gate`;
     - coherent local changes but no commit yet -> commit locally if checkpoint policy triggers, then record `push_ready` when publication/integration is needed;
     - broad unrelated suite failures only -> record `known_unrelated_failure_surface`, keep targeted verifier result authoritative for the slice, and continue or hand off as `push_ready`.
   - Make `ready_for_review_or_integration` non-canonical wording; normalize it to `push_ready` or a concrete `blocked:*` reason.
   - Add an explicit TV override for generic Kanban-worker closeout guidance: a generic `review-required` rule may apply to ordinary code tasks, but for Terminal Velocity it must defer to the TV-specific `push_ready` / integration-owner policy whenever the work is safe-local, focused verification passed, and no explicit human gate is named.
   - TV worker prompts/load order must apply `long-running-runner-operations` and TV closeout policy after generic Kanban guidance when both are present, so the more specific project policy wins.

7. **Use verifier-impact-map routing before broad native discovery.**
   - Make `docs/checklists/tv-verifier-impact-map.json` authoritative for worker verifier selection.
   - Workers must run the focused required verifier for the touched surface first, using the verifier-impact map as the routing source.
   - Examples: scenario changes run the named scenario or focused scenario/unit test; data manifest changes run JSON parsing plus the focused model/manifest test; docs/process-only changes use readback/search plus `git diff --check`.
   - Treat full native discovery, `python3 -m unittest discover -s native_ev/tests -p 'test_*.py'`, as checkpoint-optional unless the touched surface, risk profile, handoff/checkpoint boundary, integration-owner preflight, unclear dependency risk, large accumulated bundle sealing, or explicit user request justifies it.
   - Make broad hygiene/full suites checkpoint, handoff, and risk-boundary tools; do not run them automatically after every worker slice.
   - Applied status claim as of 2026-06-12; re-inspect before relying on it. A limited fix was applied to the confirmed stale skill references:
     - `ev-terminal-velocity-play/references/terminal-velocity-source-aligned-vertical-slices.md` now says to run verifier-impact-map focused checks first and demotes broad native discovery/Godot self-test to checkpoint/risk-boundary use.
     - `ev-terminal-velocity-play/references/terminal-velocity-autonomous-restart-prompt.md` now says to choose focused verifier(s) from the verifier-impact map and run broader cheap verification only when the touched surface/risk/checkpoint boundary justifies it.

8. **Prevent broad native discovery from becoming a generic gate.**
   - If broad native discovery is run and reports known unrelated failures, record them as `known_unrelated_failure_surface`.
   - Do not convert a passed focused slice into `review-required` merely because broad discovery is red outside the touched surface.
   - Worker prompts and closeout text must say: run verifier-impact-map required checks first; broad native discovery is checkpoint-optional, not a default gate.
   - The two patched skill references retain the full native discovery command as an available checkpoint/risk-boundary command; the fix is removal of default-gate framing, not removal of the verifier.

9. **Investigate the remaining durable reproduction surfaces before attributing worker behavior.**
   - Treat prompt/artifact/tooling inheritance as a hypothesis to verify, not as a proven mechanism.
   - Search any remaining durable worker inputs for broad-native-discovery defaults: continuation prompts, skill/spec excerpts, backlog items, task templates, closeout checklists, copied worker comments, ledger handoffs, and compaction summaries.
   - For each hit, classify it as: authoritative current instruction, stale/superseded instruction, copied historical output, or harmless verifier example.
   - Patch only authoritative or actively copied surfaces that still imply broad native discovery is the default. Do not add new policy for hypothetical sources that are not actually present.
   - If no further durable instruction surface is found, leave the mechanism as resolved for the confirmed references and focus follow-up fixes on verifier routing/closeout behavior rather than claiming worker memory or legacy habits.

10. **Add a cheap closeout validator.**
    - Validate that a task cannot block as `review-required` when all of the following are true: dirty paths are inside approved TV surfaces, targeted verifier(s) passed, broad failures are labeled unrelated, and no explicit human gate is named.
    - The validator must fail with a fix-it message: commit/checkpoint + `push_ready`, or continue work.

11. **Add regression coverage for this failure-class shape.**
    - Unit-test the closeout classifier with the `t_d8b44829` shape: six intended safe files, targeted route/fuel verification green, broad topology tests red, no commit yet.
    - Expected result: not `review-required`; either local checkpoint + `push_ready`, or `blocked: unsafe_dirty_state` only if the dirty file classifier finds an actual unsafe path.

### P2 — make integration-owner catch stale gates automatically

12. **Teach the integration-owner lane to scan for stale `review-required` TV tasks and dirty matching handoffs.**
    - Candidate task must be assigned to `terminal-velocity`, reference the TV repo, and include a worker handoff with changed files and verification output.
    - It must not have active worker heartbeat or concurrent writer ownership.
    - Match dirty paths against the candidate handoff and the ledger/event tail; classify old clean-history blocked cards separately from the newest dirty-matching active recovery target.
    - If the worktree matches the handoff and passes intended-file/sensitive-path checks, the integration owner may convert the task to the normal preflight/commit/`push_ready`/push flow.

13. **Add an explicit uncommitted-handoff recovery mode before normal publish dry-run.**
    - In the evidence case, `tools/tv_integration_lane.py --dry-run` correctly returned `dirty_worktree`/`nothing_to_publish` because there was no commit stack to publish.
    - Split the integration workflow into two deterministic phases:
      - **uncommitted handoff recovery** validates dirty paths, blocked-task/ledger/event match, sensitive/proprietary path exclusions, and focused-verifier freshness, then recommends a local checkpoint action;
      - **publish guard** runs only after a coherent local checkpoint exists, using the existing branch-ahead/diff/review/push path.
    - Add a dry-run/report mode such as `recover-handoff` that can validate exact dirty paths, compare them to the blocked task/ledger event, check sensitive/proprietary path exclusions, decide whether focused verifier output is fresh enough, and recommend exactly one of: `checkpoint_and_push_ready`, `rerun_focused_verifier`, `unsafe_dirty_state`, or `missing_handoff`.
    - Run the existing publish guard only after a coherent local checkpoint exists.

14. **Let autostart prefer integration recovery before seeding new work.**
    - If the lane is idle and the repo is dirty, distinguish:
      - dirty state matches a blocked worker handoff -> invoke/report integration-owner recovery instead of merely stopping with prose;
      - dirty state is unexplained -> block with `unsafe_dirty_state` and exact paths;
      - repo clean with no active task -> seed/dispatch continuation.
    - This prevents idle dirty worker bundles from stopping long-running development indefinitely.

15. **Make missing liveness a start/resume failure, not a clean idle state.**
    - When the user/requested operation is to start or resume TV game development, `live_implementation_owner: none_active` must produce an explicit `missing_live_owner` recommendation unless the protocol immediately claims one owner or selects one-shot integration recovery.
    - `declared_owner: none_active` and ledger `integration_owner: autonomous_available...` are not evidence of a running integrator.
    - A successful start must verify a running/claimed task, heartbeat/log/summary update, or completed integration-recovery action; "topology has no conflict" is insufficient.

16. **Couple ledger process-bug truth to an executor.**
    - When the ledger says `review_required_process_bug: true` and identifies a Kanban task whose intended files match the current dirty bundle, the next start/resume path routes to integration recovery before ordinary dispatch.
    - If no recovery owner is available, record `blocked: missing_live_owner` with the exact command/surface needed rather than leaving `status: running` with no live process.

17. **Keep stale blocked legacy cards ignored only when they are not actionable handoffs.**
    - Old blocked cards do not stop a clean lane from continuing only when they are historical/non-actionable and do not represent unresolved integration/recovery work.
    - A clean repo with no live owner is not idle if a live blocked TV card is classed as `push_ready`, stale `review_required_process_bug`, `verifier_failed`, `unsafe_dirty_state`, `explicit_human_gate`, or `blocked:unclassified`.
    - A `push_ready` card is an integration-owner handoff and must route to `recover_push_ready_handoff` / `push_ready_integration_required` before autostart can seed a successor.
    - An active dirty worktree plus a blocked task whose intended files match the current dirty set is integration recovery work, not ignored history.

### P2.5 — add a runner-start protocol and blocker-remediation sweep

18. **Define a start/resume protocol before seeding or dispatching work.**
    - Starting the TV game-development runner is an explicit control-plane operation, not just "create another worker."
    - The protocol identifies the single intended implementation owner surface first: continuous wrapper, Kanban dispatcher/worker loop, integration-owner lane, no-agent autostart watchdog, or a cron surface only if explicitly authorized.
    - It inspects ledger/state/log/lock/stop-file surfaces before mutating them, then chooses exactly one action: resume the canonical runner with live proof, run integration recovery, seed one successor, or stop with a concrete `blocked:*` reason.

19. **Include a broad control-plane blocker search, not broad native test discovery.**
    - Runner start performs a broad search for potential **process blockers** because the failure mode here is stale control-plane state, not a narrow code regression.
    - That broad search is not permission to run full native discovery as a routine worker verifier. Code/test verification still follows `docs/checklists/tv-verifier-impact-map.json` and the narrowest relevant verifier rule.
    - The blocker sweep covers: dirty worktree and branch divergence; active worker/process/claim heartbeat; blocked `review-required`/`push_ready`/`ready_for_review_or_integration` cards; stale locks and stop files; cron/watchdog/reporting surfaces; latest ledger/events/runner-state summaries; untracked artifacts inside the repo; profile/skill capability failures for the target worker; and known unrelated failure surfaces that could be misread as current gates.

20. **Pair every discovered blocker class with a safe correction mechanism.**
    - `stale_review_required` with matching safe dirty bundle -> integration-owner recovery: intended-file/sensitive-path check, focused relevant verifier, local checkpoint if missing, normalize to `push_ready`, deterministic integration lane, successor dispatch if clean.
    - `push_ready` local checkpoint or blocked handoff with no active worker -> integration-owner dry-run/review/push or gate-normalization path; autostart must not seed over it. The current start/resume preflight reports `recover_push_ready_handoff` with `push_ready_integration_required` for this class until the integration-owner closeout path resolves it.
    - clean repo plus stale blocked legacy cards -> ignore for liveness only after blocked-card enrichment shows they are non-actionable historical cards rather than `push_ready`, stale `review_required_process_bug`, failed-verifier, unsafe, explicit-human, or unclassified TV gates.
    - unexplained dirty/untracked repo state -> preserve/move clearly unrelated process debris when safe; otherwise block as `unsafe_dirty_state` with exact paths.
    - stale lock/stop-file for the selected wrapper -> clear only if restarting that same wrapper and after recording why it is stale; otherwise report what surface it affects.
    - worker profile/skill crash-loop -> block/supersede the bad card with the concrete startup reason, create a corrected card only after profile capability is verified.
    - cron/runner topology mismatch -> keep one named implementation owner; remove or keep passive reporter surfaces only according to whether they can mutate implementation state.

21. **Make the start protocol machine-checkable.**
    - Add or extend an autostart/preflight command that emits structured JSON: `owner_surface`, `repo_state`, `active_worker`, `blocked_cards`, `stop_lock_state`, `reporter_state`, `capability_check`, `recommended_action`, `correction_applied`, and `explicit_gate`.
    - The command must default to dry-run/report mode; correction mode may apply only the safe-local remediations above, never external/account/provider/gateway/config changes, destructive original-EV actions, force/history operations, or raw proprietary publication.
    - After a correction/start action, verify more than "scheduled": check a running/claimed task, heartbeat/log/summary update, or integration-lane completion as applicable.

### P2.6 — instantiate skill and prompt-surface repairs

22. **Audit the overloaded play skill and active callers before adding more prose.**
   - Start from `ev-terminal-velocity-play/references/skill-scope-and-split-guidance.md` and `ev-terminal-velocity-play/references/skill-migration-inventory-2026-06-12.md`.
   - Include the confirmed generic `kanban-worker` closeout conflict as a concrete audit target: identify which fresh TV workers/prompts load it, whether they also load the TV runner/push policy, and which surface carries the explicit TV override.
   - Search active callers before moving anything: `docs/prompts/terminal-velocity-continuation-prompt.md`, `tools/check_agent_continuation_artifacts.py`, `docs/checklists/long-running-game-development-harness-audit.md`, `docs/checklists/agent-continuation-process-failure-remediation.md`, stored Kanban prompts, cron prompts, and skill cross-links.
   - Output a compact inventory row for each candidate rule: current path, active callers, class (`gameplay/operator`, `runner/process governance`, `Kanban/topology/reset`, `push/integration policy`, `mechanical validation`, `generic Kanban conflict`, or `do not migrate`), destination, and keep/move/archive/delete decision.

23. **Split skill responsibilities into named destination surfaces instead of adding another broad TV process paragraph.**
   - Keep `ev-terminal-velocity-play` as the gameplay/operator and play-learning dispatcher.
   - Move or point runner/start/resume/watchdog rules to `long-running-runner-operations` and its TV runner-process references.
   - Move or point Kanban/topology/dispatch rules to `kanban-orchestrator`, `kanban-worker`, or repo-local runner docs, depending on which worker actually loads them.
   - Add or patch the TV-specific override where fresh TV workers will actually see it: generic `kanban-worker` review-required closeout guidance must defer to TV `push_ready` / integration-owner policy for safe-local verified slices.
   - Move or point normal non-force push, `push_ready`, and stale `review-required` handling to the integration/push surface, not gameplay prose.
   - Preserve compatibility notes at old reference paths until active callers are updated; do not delete or rename references before caller migration.

24. **Patch only authoritative loaded surfaces, not historical evidence.**
   - If a stale broad-discovery or review-gate rule appears only in old comments, event history, or this evidence artifact, leave it as historical evidence.
   - If it appears in a prompt, skill, template, or checker that fresh workers load, patch that surface and add a regression or search check proving the stale wording no longer appears there.
   - Verification: `skill_view` the edited skills/references, run a targeted search for `review-required`, `ready_for_review_or_integration`, `full native discovery`, and `python3 -m unittest discover -s native_ev/tests -p 'test_*.py'`, then classify remaining hits as current policy, example, compatibility pointer, or historical evidence.

25. **Add a skill-scope regression check.**
   - Add or extend a checker that fails when `ev-terminal-velocity-play/SKILL.md` grows new full runner/Kanban/push/gateway procedure bodies instead of pointer-level routing.
   - Initial rule: top-level gameplay skill may contain trigger pointers to runner/Kanban/push surfaces, but detailed closeout/integration/start/resume protocols must live in narrower skills or repo artifacts.
   - Verification: run the checker against the existing skill and confirm it passes with current pointer-level text, then add a fixture that would fail on a duplicated process-procedure paragraph.

### P2.7 — instantiate deterministic automation with light LLM supervision

26. **Move routine state classification from prose/LLM judgment into a dry-run recovery classifier.**
   - Extend `tools/tv_integration_lane.py` or add `tools/tv_runner_recovery_preflight.py` with a dry-run mode that emits structured JSON for: `repo_state`, `dirty_paths`, `candidate_handoff`, `handoff_evidence_sources`, `matched_changed_files`, `missing_changed_files`, `extra_dirty_paths`, `handoff_match`, `sensitive_path_check`, `focused_verifier_status`, `known_unrelated_failures`, `active_worker`, `recommended_action`, `requires_llm_review`, and `explicit_gate`.
   - Recovery evidence sources must include Kanban comments/latest summary and local `.hermes/long-running/tv-spec-implementation/closeout-packet-*.json` files before falling back to task-list prose; ledger `last_reconciled_live_git` and event-tail checkpoints may provide corroborating evidence but must not override live dirty-path/sensitive-path checks.
   - Expected recommended actions for uncommitted recovery are exactly: `checkpoint_and_push_ready`, `rerun_focused_verifier`, `unsafe_dirty_state`, or `missing_handoff`.
   - Additional non-recovery actions may be emitted only when the classifier is operating in start/publish orchestration mode: `push_ready_publish`, `seed_successor`, `missing_live_owner`, or `normalize_ledger_state`.
   - LLM role: review the exact JSON plus exact diff only when the deterministic classifier returns a safe candidate requiring judgment; do not ask the LLM to discover routine state from prose logs.

27. **Make verifier selection mechanically routed.**
   - Extend `tools/backlog_dispatch_index.py check` or add a focused verifier-map command that accepts touched paths and returns required verifier families from `docs/checklists/tv-verifier-impact-map.json`.
   - Worker prompts must call this command before any broad native discovery.
   - Test cases: scenario-only change routes to focused scenario/unit verifier; docs/process-only change routes to readback/search plus `git diff --check`; unknown/high-risk native surface may recommend full native discovery as checkpoint-optional or risk-boundary verification.

28. **Make closeout packet completeness mechanically validated and consumable by recovery.**
   - Add a validator for `push_ready`/`blocked:*` packets that checks canonical status, commit SHA when required, intended files, verifier commands/results, known unrelated failures, explicit gate class, and next action.
   - Require closeout packets intended for recovery to include `task_id`, `changed_files`, structured `verification`, evidence boundary/source-fidelity note when applicable, and enough verifier command text for a later recovery pass to choose `checkpoint_and_push_ready` vs `rerun_focused_verifier`.
   - Recovery classifiers must be able to read these packets directly; otherwise the system can write a valid handoff that no deterministic owner can consume.
   - Reject `ready_for_review_or_integration` unless it is historical evidence; reject `review-required` unless paired with a concrete `blocked: explicit_human_gate` reason.
   - Add a regression fixture for the evidence-case shape: safe dirty bundle + focused verifier passed + unrelated broad failures + no commit yet + local closeout packet/Kanban comment evidence -> `checkpoint_and_push_ready` or `rerun_focused_verifier`, never generic `review-required` or `unsafe_dirty_state`.

29. **Convert watchdog/reporting into script-first, LLM-light supervision.**
   - Routine watchdogs must be no-agent or deterministic-script jobs that stay silent unless a material state transition occurs: stale gate converted, integration pushed, real explicit gate found, successor started, or watchdog/tooling failure.
   - LLM runs must summarize or decide only after the script emits a bounded event packet; they must not poll chatily or rediscover the entire state each tick.
   - Verification: a quiet no-change run emits no user message; a synthetic stale-gate fixture emits exactly one bounded remediation/report packet.

30. **Create one integration owner contract for LLM review boundaries.**
   - Deterministic guards own: dirty-path classification, branch status, sensitive-path scan, verifier-map routing, closeout packet validation, active-worker/liveness checks, and post-push `HEAD == origin/main` verification.
   - LLM-assisted review owns: exact-bundle risk assessment after deterministic guards pass, ambiguous source/fidelity tradeoffs, and concise human-readable reporting.
   - The LLM must not override a failed deterministic safety gate; it may only explain the gate or recommend the next safe local remediation.

### Applied implementation note — 2026-06-12 recovery-classifier and checkpoint first slices

Status: partial P2.7 implementation.

Implemented surfaces:

- `tools/tv_runner_recovery_preflight.py` now performs idle-dirty classification and emits structured JSON for `repo_state`, `dirty_paths`, `candidate_handoff`, `handoff_match`, `sensitive_path_check`, `focused_verifier_status`, `known_unrelated_failures`, `active_worker`, `recommended_action`, and `explicit_gate`.
- `tools/tv_runner_recovery_preflight.py --checkpoint` now creates a local checkpoint commit only when the dirty bundle is classified `checkpoint_and_push_ready`, then reports `push_ready` plus checkpoint metadata for the integration lane.
- `tools/tv_runner_recovery_preflight.py --repair-unsafe-debris` now repairs one safe subset of `unsafe_dirty_state`: clearly non-sensitive, untracked, non-project debris is moved to a quarantine directory outside the worktree and the repo is reclassified immediately.
- `tools/tv_runner_autostart.py` now runs the recovery preflight on idle dirty state and reports that JSON before refusing to seed overlapping work.
- Regression coverage lives in `native_ev/tests/test_tv_runner_recovery_preflight.py` and `native_ev/tests/test_tv_runner_autostart.py`.

Verified behavior:

- clean idle repo -> `seed_successor`;
- dirty repo without matching handoff -> `unsafe_dirty_state`;
- dirty repo matching a blocked handoff with focused verifier pass -> `checkpoint_and_push_ready`;
- dirty repo matching a blocked handoff without focused verifier evidence -> `rerun_focused_verifier`;
- `--checkpoint` on a matching, verifier-passed handoff stages only the matched dirty paths, runs `git diff --cached --check`, creates a local checkpoint commit, leaves the task JSON untracked, and reports `push_ready`;
- `--repair-unsafe-debris` moves only untracked, non-sensitive, non-project debris to quarantine and then returns `seed_successor` when the worktree is clean;
- `--repair-unsafe-debris` refuses to move tracked changes, sensitive paths, or plausible project paths and keeps `unsafe_dirty_state` explicit.

Remaining follow-up: wire the checkpoint/repaired-clean recovery path into a fuller integration-owner command that records or normalizes the Kanban/ledger `push_ready` packet and then runs the existing publish guard; separately decide whether autostart should call `--repair-unsafe-debris` automatically for this narrow debris class or keep it as explicit integration-owner operation.

### Applied implementation note — 2026-06-12/13 start/resume preflight and blocked-card start gate

Status: partial P2.7/P3 implementation; the current setup now treats clean-idle `push_ready` as unresolved integration work, not as an idle lane.

Implemented surfaces:

- `tools/tv_runner_start_resume_preflight.py` wraps the topology checker and live repo checks into a structured start/resume decision packet.
- The packet includes `repo_state`, `dirty_paths`, `topology`, `blocked_cards`, `stop_lock_state`, `watchdog_reporter_state`, `capability_check`, `recommended_action`, `safe_to_start`, and `explicit_gate`.
- `tools/tv_runner_start_resume_preflight.py` enriches `blocked_cards` from live Kanban SQLite task state when a topology candidate DB exists.
- Blocked TV cards are classified into canonical classes including `push_ready`, `review_required_process_bug`, `unsafe_dirty_state`, `verifier_failed`, `explicit_human_gate`, and `blocked:unclassified`.
- `tools/tv_runner_start_resume_preflight.py` now applies `blocked_card_start_gate(...)` when the lane is otherwise clean and has `live_implementation_owner: none_active`. That guard blocks start/seed over unresolved blocked-card handoffs and routes the highest-priority class to a concrete recovery action/gate:
  - `push_ready` -> `recover_push_ready_handoff` with `push_ready_integration_required`;
  - `review_required_process_bug` -> `normalize_blocked_gates` with `gate_normalization_required`;
  - `verifier_failed` -> `rerun_focused_verifier`;
  - `unsafe_dirty_state`, `explicit_human_gate`, and `blocked:unclassified` -> concrete blocked gates.
- `tools/tv_runner_autostart.py` consumes the structured start/resume preflight before dispatching a ready task or seeding a successor, and fails closed on any `explicit_gate`/unsafe result.
- Regression coverage lives in `native_ev/tests/test_tv_runner_start_resume_preflight.py` and `native_ev/tests/test_tv_runner_autostart.py`.

Verified behavior:

- clean idle repo + gateway startup owner + no unresolved blocked-card handoff -> `start_gateway_kanban_dispatcher`;
- clean idle repo + `push_ready` blocked TV card -> `recover_push_ready_handoff`, `explicit_gate: push_ready_integration_required`, `safe_to_start: false`;
- dirty repo -> `recover_dirty_handoff` with `recovery_preflight_required` before any start;
- active matching gateway owner -> `resume_existing_owner`;
- conflicting live owner -> `blocked:topology_conflict`;
- live blocked TV cards are listed with `counts_by_class`;
- stale generic `review-required` cards classify as `review_required_process_bug` rather than a human gate;
- autostart does not dispatch/seed when start/resume preflight reports a gate;
- idle clean autostart calls the structured start/resume preflight before seeding.

Current implication for this artifact: earlier text that says old blocked cards may be ignored for liveness is now qualified. Clean historical blocked cards may be ignored only when they do not represent an actionable unresolved handoff. A clean repo with no live owner is not idle if the live Kanban board still contains a `push_ready` handoff, stale `review_required_process_bug`, failed verifier gate, unsafe dirty-state gate, explicit human gate, or unclassified blocked TV card.

Remaining follow-up: promote canonical gate normalization and specific handoff recovery into the integration lane closeout path so the `recover_push_ready_handoff` and `normalize_blocked_gates` recommendations can be resolved automatically after deterministic review, instead of merely blocking autostart from seeding over them.

### Applied implementation note — 2026-06-12 integration-owner gate normalization

Status: partial P3 implementation.

Implemented surfaces:

- `tools/tv_integration_lane.py` now accepts `--normalize-gates` to plan canonical gate comments for actionable blocked TV Kanban cards.
- `--apply-gate-comments` writes idempotent `tv_gate_normalization` comments and `tv_gate_normalized` events for `push_ready` and stale `review_required_process_bug` cards.
- Non-actionable gates such as `unsafe_dirty_state`, `verifier_failed`, `explicit_human_gate`, and `blocked:unclassified` are reported under `skipped` and are not commented by default.
- Regression coverage lives in `native_ev/tests/test_tv_integration_lane.py`.

Verified behavior:

- dry-run plans comments only for actionable `push_ready` / `review_required_process_bug` cards;
- apply mode inserts one comment/event per actionable card;
- repeated apply is idempotent and writes zero duplicate comments.

Remaining follow-up: wire the normalization step into the publish/recovery closeout path so integration-owner actions can normalize a specific gate after verifying and publishing its bundle, rather than relying on an operator to run the planner manually.

### Evidence update — 2026-06-13 closeout-packet, recovery-classifier, and ledger-staleness bugs

Status: newly diagnosed follow-up bug cluster; source-backed by live readback of `tools/tv_runner_recovery_preflight.py`, `tools/tv_runner_start_resume_preflight.py`, `tools/check_tv_runner_topology.py`, `.hermes/long-running/tv-spec-implementation/closeout-packet-t_4ad7b9e5.json`, `.hermes/long-running/tv-spec-implementation/task-ledger.json`, and `hermes -p loki-game kanban --board terminal-velocity show t_4ad7b9e5 --json`.

#### Bug A — closeout evidence exists but is split across unconsumed surfaces

The current `t_4ad7b9e5` closeout packet does contain usable handoff evidence: `task_id`, exact `changed_files`, targeted verifier results, full scenario/unit verification summaries, `git diff --check`, and an explicit EV Classic source-boundary note. The Kanban card also contains the handoff JSON in a comment.

The failure is therefore not missing evidence. The failure is evidence-source mismatch: the recovery classifier does not currently consume the local closeout packet or Kanban comments where the evidence lives.

Proposed fix:

- Treat local closeout packets under `.hermes/long-running/tv-spec-implementation/closeout-packet-*.json` as first-class handoff evidence when they name the active blocked task and dirty bundle.
- Treat Kanban comments and `latest_summary` as first-class handoff evidence for blocked-card recovery, not only task body/result/summary fields from `kanban list`.
- Match current dirty paths against packet `changed_files` and comment `changed_files`, allowing exact equality plus explicitly safe generated/checkpoint artifacts such as the packet itself.
- Extract verifier status from structured `verification` fields before falling back to prose search.
- Regression: a dirty repo matching `closeout-packet-t_4ad7b9e5.json` plus a blocked `push_ready`/review-required Kanban card must classify as `checkpoint_and_push_ready` or `rerun_focused_verifier`, never generic `unsafe_dirty_state`.

#### Bug B — recovery classifier is narrower than the start/resume preflight

`tools/tv_runner_start_resume_preflight.py` can see the live blocked Kanban card and route dirty state to `recover_dirty_handoff`, but `tools/tv_runner_recovery_preflight.py` then searches only limited task-list fields:

- `id`
- `title`
- `body`
- `result`
- `summary`
- `reason`
- `status`
- `current_step_key`

It does not currently inspect Kanban comments, local closeout packets, ledger `last_reconciled_live_git.checkpoint_files`, or events tail records. That means start/resume can correctly identify recovery work while recovery preflight misclassifies the same state as `unsafe_dirty_state`.

Proposed fix:

- Add an evidence-aggregation layer for dirty-handoff recovery with ordered sources: live Kanban comments/latest summary, local closeout packets, ledger checkpoint files/last verification, then task-list prose as fallback.
- Emit provenance in classifier JSON, e.g. `handoff_evidence_sources: ["kanban_comment", "closeout_packet"]`, `matched_changed_files`, `missing_changed_files`, and `extra_dirty_paths`.
- Keep `unsafe_dirty_state` for true mismatch cases: sensitive paths, unrelated dirty paths not explained by the handoff, missing handoff evidence after all sources are checked, or failed relevant verifier.
- If matching evidence exists but verifier freshness is uncertain, return `rerun_focused_verifier` with the exact verifier command(s) from the packet, not `unsafe_dirty_state`.
- Wire autostart/start-resume to call the same evidence aggregator, so `recover_dirty_handoff` and the recovery classifier cannot disagree on candidate identity.

#### Bug C — ledger staleness recurs because `running` and `none_active` are allowed to coexist

The live ledger currently contains `status: running` while both top-level `declared_owner` and nested `runner_ownership.implementation_owner` are `none_active`. `tools/check_tv_runner_topology.py` treats most non-stopped statuses, including `running`, as declaring active runner intent. When a start/resume command supplies `--startup-owner continuous_kanban_runner`, the checker correctly warns that startup owner differs from the stale ledger owner.

This is a bookkeeping/invariant bug, not evidence of a real active owner conflict. The ledger is useful as checkpoint/provenance state, but it must not remain a primary runtime truth surface after the live owner has stopped or a worker has blocked. The durable fix is stronger than normalizing one bad pair of fields: `task-ledger.json` should be treated as a generated checkpoint projection/cache, while live owner truth comes from live Kanban/process/cron/lock/git surfaces.

Proposed fix:

- Demote `declared_owner`, `runner_ownership.implementation_owner`, `allowed_surfaces.*`, and ambiguous `status: running` from live authority to historical/checkpoint metadata unless they carry a fresh assertion marker such as `owner_assertion_source: live_preflight` plus a recent timestamp.
- Split ledger schema into explicit zones: `last_integrated_checkpoint`, `latest_worker_handoff`, `historical_notes`, and `generated_from`. Do not mix live ownership, handoff state, policy notes, and checkpoint summaries in a single status field.
- Generate or reconcile `task-ledger.json` deterministically from `events.jsonl`, current git HEAD/status, closeout packets, and Kanban task state. Workers may append events and closeout packets; a reconciler/integration-owner path updates the ledger projection.
- Replace generic `ledger_stale` with precise classes: `ledger_projection_stale`, `ledger_historical_owner_mismatch`, `dirty_handoff_pending`, `unsafe_dirty_state`, and true `live_owner_conflict`. Only true live conflicts and unsafe dirty state should block. Projection staleness should say which reconciler/normalizer to run.
- Introduce explicit non-running recovery projection states for unresolved handoffs, e.g. `waiting_integration_recovery`, `push_ready_recovery`, `waiting_focused_verifier`, or `blocked_unsafe_dirty_state`; avoid `running + none_active` as a representable current state.
- Regression: fixtures covering clean idle plus stale historical owner, active Kanban worker plus ledger `none_active`, clean repo plus old `status: running`, and dirty handoff with matching closeout evidence must not produce an ambiguous perpetual `ledger_stale` gate.

#### System fix — make the ledger a generated projection, not a control plane

The recurring ledger failures come from one file trying to be both the live control plane and the durable history. That coupling creates stale gates whenever a worker exits, blocks, or a live Kanban/process surface advances faster than the ledger writer. The repair is to make the live surfaces authoritative and make the ledger a deterministic projection over them.

Required system behavior:

- **Live truth source:** derive active owner/liveness from Kanban claimed/running tasks, worker PIDs/process registry, cron/watchdog state, stop/lock files, and git state. Do not infer a live owner from historical ledger fields.
- **Ledger role:** record the last integrated checkpoint, latest handoff summary, generated projection metadata, and historical notes. It may cache a summary of live state only when the cache names its source and generation timestamp.
- **Reconciler:** add or extend a deterministic command such as `python3 tools/tv_ledger_reconcile.py --write` to read `events.jsonl`, closeout packets, Kanban task state, and git state, then write a normalized ledger projection. Dry-run mode must show the planned projection and classify stale/mismatched inputs before writing.
- **Closeout packet contract:** closeout packets must include `closeout_class`, `kanban_task`, `changed_files`, `ledger_files` or generated/checkpoint files, `event_ids` when known, `verification`, `next_action`, and `successor_kanban_task` when applicable. Recovery should not depend on prose-only handoffs.
- **Topology/preflight contract:** topology may report ledger projection drift, but start/resume decisions must use live-owner and dirty-handoff classifiers. A stale historical owner should be a `normalize_ledger_projection` recommendation, not a runner blocker.
- **Safety boundary:** if live surfaces show actual concurrent writers, unsafe dirty paths, failed relevant verifier, or unresolved explicit human gate, block under those concrete classes. Do not hide real blockers behind ledger normalization.

Verification targets:

- active Kanban worker + ledger `none_active` -> `resume_existing_owner`, not blocking `ledger_stale`;
- clean idle repo + stale historical `status: running` -> `start_gateway_kanban_dispatcher` plus optional `normalize_ledger_projection`, not `missing_live_owner` solely from ledger;
- dirty handoff + matching closeout packet/comment evidence -> `checkpoint_and_push_ready` or `rerun_focused_verifier`, with `handoff_evidence_sources` naming the consumed surfaces;
- multiple closeout packets -> newest packet/comment set matching current dirty paths wins; older packets remain historical evidence;
- ledger projection behind `events.jsonl` -> `ledger_projection_stale` with a reconciler action, not a live-owner conflict.

#### Revised next implementation order from this evidence update

1. Extend dirty-handoff recovery evidence aggregation to consume closeout packets and Kanban comments.
2. Add regression fixtures for `t_4ad7b9e5` shape: packet/comment evidence present, dirty bundle safe, verifier pass recorded.
3. Demote ledger owner/status fields from live authority and add projection-staleness classes so stale historical ledger fields cannot block a live Kanban/process truth.
4. Add or extend a deterministic ledger reconciler that writes the normalized checkpoint projection and refuses to invent live-owner state.
5. Wire the richer recovery classifier and ledger reconciler into integration-owner checkpoint/publish closeout and autostart reporting.
6. Update candidate `tv-spec.md` prose to document the live-truth/projection split, exact stale-ledger classes, and the closeout-packet contract.

### P3 — tighten reporting and observability

31. **Use material progress reports, not process-chatter loops.**
   - Report when a stale review gate is converted, when integration pushes, when a real gate blocks, or when a successor starts.
   - Do not report routine watchdog ticks.

32. **Record gate class explicitly in ledger/events.**
   - Required fields: `gate_class`, `canonical_status`, `relevant_verifiers`, `known_unrelated_failures`, `requires_human`, `integration_owner_next_action`.
   - `requires_human` must be `false` for safe-local `push_ready` and `true` only for the existing human-gated categories.

33. **Retire ambiguous closeout language from prompts.**
   - Replace “review/integration” wording with “integration-owner handoff” unless a concrete human gate is named.
   - Every blocked state must say whether it is `verifier_failed`, `unsafe_dirty_state`, `explicit_human_gate`, `cap_handoff`, `no_safe_local_slice`, or `tooling_failure`.

## Matching proposed `tv-spec.md` edit

This section is a candidate spec patch, not evidence that `tv-spec.md` has already changed.

This section is part of the intended deliverable of this comprehensive artifact: proposed `tv-spec.md` wording for a later, explicitly authorized spec-edit pass.

- Target surface: `docs/research/tv-spec.md`.
- Trigger condition: an authorized implementation pass selects this artifact's spec-update fix target.
- Pre-edit action: re-inspect current `tv-spec.md` and compare the candidate wording below against any policy that has since moved elsewhere.
- Gate: mutating `tv-spec.md` is separate from this artifact cleanup; do it only when the user asks to apply artifact fixes beyond this review artifact.
- Verification: read back the edited `tv-spec.md`, run `git diff --check`, and search for duplicate/conflicting worker-closeout, integration-owner, and runner-start policy wording.

Apply the following edit to `docs/research/tv-spec.md` after the existing Git checkpoint policy paragraph that ends with `Missing GitHub credentials in a worker are not a TV development gate.`

```markdown
### Worker closeout and stale review-gate policy

Workers and continuous runners must not use human `review-required` as a generic closeout for verified safe-local TV work. File changes, local branch-ahead state, missing push credentials, or unrelated broad-suite failures are not human gates by themselves.

At worker closeout, classify the state into exactly one canonical outcome:

- `continue`: targeted verifier(s) passed, dirty work remains coherent, no checkpoint-policy trigger, and the worker can safely continue adjacent work under the long-running efficiency policy.
- `push_ready`: a coherent local checkpoint exists and remote publication/integration is needed for coordination, reset safety, another lane, or inspection-cost control. The packet must include commit SHA, intended files, verification commands/results, known unrelated failure surfaces, why publication is needed, and the next action.
- `blocked: verifier_failed`: a relevant verifier for the touched surface failed and cannot be narrowed or fixed in the current invocation.
- `blocked: unsafe_dirty_state`: dirty files are unexplained, unrelated, proprietary/raw-capture-risk, cross-repo, or otherwise unsafe to stage as a coherent TV bundle.
- `blocked: explicit_human_gate`: the task crosses a destructive original-EV, hard-to-restore save/pilot, raw proprietary publication, credential/account/provider/config/gateway, force/history rewrite, deletion/release/settings, non-TV, or external/social side-effect boundary.
- `blocked: cap_handoff` or `blocked: no_safe_local_slice`: context/tool limits or exhausted safe-local work require a self-contained handoff.

If targeted verifier(s) passed for the touched TV surface and any broad-suite failure is labeled unrelated to the slice, the worker must not stop as `review-required`. It must either continue, create a local checkpoint and record `push_ready`, or block under one of the concrete `blocked:*` classes above.

Worker verifier selection must start from `docs/checklists/tv-verifier-impact-map.json`: run the focused required verifier for the touched surface first, using the cheapest sufficient verifier family that proves the changed claim. Full native discovery (`python3 -m unittest discover -s native_ev/tests -p 'test_*.py'`) is checkpoint-optional, not a default gate; run it only when justified by the touched native/model surface, checkpoint/handoff boundary, integration-owner preflight, unclear dependency risk, large accumulated bundle sealing, or explicit user request. If full discovery is run and known unrelated failures appear, record them as `known_unrelated_failure_surface` without overriding a passing focused verifier for the slice.

`ready_for_review_or_integration` is non-canonical wording. Normalize it to `push_ready` when the next step is integration-owner publication, or to a concrete `blocked:*` status when a real blocker exists.

Closeout packets, Kanban comments, and ledger/event checkpoint records are handoff evidence, not separate optional prose. A blocked or dirty-handoff recovery path must inspect structured closeout packets such as `.hermes/long-running/tv-spec-implementation/closeout-packet-*.json`, Kanban comment handoffs, `latest_summary`, ledger projection fields, and event-tail checkpoint records before classifying a safe dirty bundle as missing handoff evidence. Closeout packets meant for recovery must include `closeout_class`, `kanban_task`, `changed_files`, generated/checkpoint `ledger_files` when applicable, `event_ids` when known, structured `verification`, `next_action`, and `successor_kanban_task` when a successor exists. If these surfaces agree on `changed_files` and relevant verifier success, recovery must return `checkpoint_and_push_ready` or `push_ready`; if verifier freshness is uncertain, return `rerun_focused_verifier` with the exact verifier commands. Reserve `unsafe_dirty_state` for sensitive paths, unrelated extra paths, failed relevant verifier, or no matching handoff after all listed evidence surfaces were inspected.
```

Apply the following edit to the Integration-owner paragraph that currently begins `The integration owner performs final status/diff review...`:

```markdown
The integration owner performs final status/diff review, runs required checkpoint verification, creates or validates the local checkpoint commit when recovering a stale worker handoff, pushes normal non-force bundles, fetches, verifies local `HEAD == origin/main`, and records the pushed checkpoint. Integration is event-triggered: publish as infrequently as possible while preventing worker blockage, stale coordination, context/reset loss, or inspection-expensive local divergence. Do not push by maximum-frequency cadence, per-commit habit, or arbitrary commit-count batching. The deterministic publish preflight is `python3 tools/tv_integration_lane.py --dry-run`; it must report no active worker, no unsafe dirty worktree, no branch-behind state, only safe TV paths, `git diff --check`, and committed-diff secret scan before an LLM review may return `publish`. Actual push uses `python3 tools/tv_integration_lane.py --push --llm-approved` only after that exact-bundle review. One clean commit may be pushed immediately if it unblocks another lane; several adjacent commits may remain local when no one is blocked and the stack remains coherent and easy to inspect.

When the lane is idle but the worktree is dirty, classify the dirty bundle before publish preflight or successor seeding. Match by evidence, not by vague recency: compare the dirty file set against the active or newest dirty-matching Kanban task, handoff intended-file list, closeout packet `changed_files`, Kanban comment handoff, `latest_summary`, ledger/event tail, and verifier output covering the exact dirty bundle. Old clean-history blocked cards are ignored for liveness unless their intended files match the current dirty set. If the bundle matches, handle it as integration recovery before publish preflight: validate intended dirty files against the handoff and ledger/event tail, scan for sensitive/proprietary/unrelated paths, verify or rerun the focused relevant verifier, create the coherent local checkpoint if missing, record or normalize `push_ready`, run the deterministic integration lane, and then dispatch exactly one successor if no real gate remains. An autostart watchdog may detect, report, or route this state, but only the integration owner mutates repo/task state, creates commits, or pushes. If dirty paths do not match a handoff after inspecting Kanban comments, closeout packets, ledger/event records, and task-list prose, block as `unsafe_dirty_state` or `missing_handoff` with exact paths and evidence surfaces inspected instead of seeding overlapping work.

A publish guard that reports `dirty_worktree`/`nothing_to_publish` is not itself a recovery failure for an uncommitted worker slice; it means the integration owner must run the uncommitted-handoff recovery classifier first, then rerun the normal publish guard after a coherent checkpoint exists.
```

Apply the following edit as a new subsection near the runner/autostart policy in `docs/research/tv-spec.md`:

```markdown
### Runner start/resume blocker protocol

Starting or resuming the TV game-development runner is a control-plane operation. Before seeding or dispatching implementation work, the start protocol must identify the single intended implementation owner surface and inspect live repo, Kanban, runner-state, ledger/event, lock/stop-file, cron/watchdog/reporter, and target-worker capability surfaces. A clean topology with `live_implementation_owner: none_active` proves absence of conflict, not successful start/resume. When startup was requested, the protocol must either claim/start exactly one owner surface and verify it with a running/claimed task, heartbeat/log/summary update, or completed integration-recovery action; run one-shot integration recovery; or report `blocked: missing_live_owner` with the exact missing surface/command.

The start protocol performs a broad **process-blocker** search, not broad native test discovery. It looks for dirty worktree or branch divergence, active worker/process/claim heartbeat, blocked `review-required`/`push_ready`/`ready_for_review_or_integration` cards, stale locks/stop files, untracked repo artifacts, profile/skill startup failures, topology mismatches, autostart state without a live watchdog, ledger `review_required_process_bug` without a consuming executor, and known unrelated failure surfaces that could be misread as current gates. Code/test verification remains governed by `docs/checklists/tv-verifier-impact-map.json`: run the focused relevant verifier for the touched surface first, and treat full native discovery as checkpoint-optional unless separately justified.

Each blocker class must map to a listed safe-local correction or explicit gate: evidence-matched stale worker handoff -> integration-owner recovery; clean repo plus stale legacy blocked cards -> ignore for liveness only when blocked-card enrichment classifies them as non-actionable historical cards rather than unresolved handoffs/gates; `push_ready` blocked handoff -> `recover_push_ready_handoff` / `push_ready_integration_required` before any successor seed; unexplained dirty state -> `blocked: unsafe_dirty_state` with exact paths; stale selected-wrapper stop/lock -> clear only for that wrapper after recording why stale; autostart state file but no scheduled/running watchdog -> report `missing_live_owner` unless the user has explicitly requested watchdog creation/repair; profile/skill crash-loop -> block/supersede only the bad TV task/card and create a corrected TV card only after target-worker capability verification passes, otherwise `blocked: capability_check_failed`; topology mismatch -> preserve one named implementation owner and keep only non-mutating passive reporters outside it. Safe-local correction mode is limited to selecting one owner, running/reporting integration recovery, clearing a proved-stale wrapper-local stop/lock, ignoring stale non-actionable legacy cards for liveness, and seeding one successor only when the repo is clean and no real gate remains; all account/provider/gateway/config/scheduled-job changes remain explicit gates.

The preflight is machine-checkable and defaults to dry-run/report mode, emitting `startup_intent`, `owner_surface`, `repo_state`, `active_worker`, `blocked_cards`, `stop_lock_state`, `watchdog_state`, `reporter_state`, `capability_check`, `ledger_projection_status`, `recommended_action`, `correction_applied`, and `explicit_gate`. Correction mode may apply only safe-local remediations; it must not perform external/account/provider/gateway/config changes, destructive original-EV actions, force/history operations, or raw proprietary publication. After a start/correction, verify more than "scheduled": check a running/claimed task, heartbeat/log/summary update, or completed integration-recovery action.

`task-ledger.json` is a generated checkpoint projection, not the live control plane. Live ownership must be derived from live Kanban/process/cron/watchdog/lock/git surfaces, not from historical ledger fields. The ledger may record `last_integrated_checkpoint`, `latest_worker_handoff`, `historical_notes`, and `generated_from` metadata; any cached live-state summary must name its source and generation timestamp. Fields such as `declared_owner`, `runner_ownership.implementation_owner`, `allowed_surfaces.*`, or `status: running` are historical/checkpoint metadata unless they carry a fresh assertion marker such as `owner_assertion_source: live_preflight` and a recent timestamp. Stale historical owner fields must not block start/resume by themselves.

The ledger must not remain `status: running` with `declared_owner: none_active` / `runner_ownership.implementation_owner: none_active` after a worker has blocked or no live owner exists. That state is stale projection data, not live ownership. The start/resume or closeout-normalization path must either claim/start one owner with live proof, or normalize the ledger projection to an explicit non-running recovery state such as `waiting_integration_recovery`, `push_ready_recovery`, `waiting_focused_verifier`, or `blocked_unsafe_dirty_state`. Replace generic recurring `ledger_stale` with precise classes such as `ledger_projection_stale`, `ledger_historical_owner_mismatch`, `dirty_handoff_pending`, `unsafe_dirty_state`, and true `live_owner_conflict`; only true live conflicts and unsafe dirty state block. Projection staleness must name the reconciler/normalizer action, for example `python3 tools/tv_ledger_reconcile.py --write`, and dry-run reconciliation must show the planned projection before writing.
```

Apply the following edit to the Human gates / Not gated section by adding these bullets under `Not gated:`

```markdown
- dirty safe-local worker bundles that match an intended TV handoff and have passing relevant verifier(s), provided the integration owner first performs intended-file, sensitive-path, diff-check, and exact-bundle review;
- unrelated broad-suite failures that are explicitly labeled as not covering the touched slice and are paired with passing relevant verifier(s);
- conversion of stale `review-required` or `ready_for_review_or_integration` worker states into canonical `push_ready` or a concrete `blocked:*` class by the integration owner.
```

Rationale for the spec edit: the current spec already says safe-local TV work, `push_ready`, and normal integration-owner pushes are not human-gated. The missing rule is the closeout classifier that prevents workers from reintroducing human `review-required` as a catch-all when the correct next step is automated integration-owner recovery.
