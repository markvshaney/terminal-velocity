# TV spec

Date: 2026-06-09
Status: canonical compact workflow spec

Purpose: define the current Terminal Velocity development workflow. This is a process artifact, not an EV Classic behavior source. EV Classic behavior claims still require source/fidelity promotion.

This file is authoritative for workflow. Superseded supporting drafts are local-only provenance, not required execution inputs; if archived draft material becomes needed for project work, promote the relevant claim into repo docs/backlog instead of depending on the local archive path. Local provenance pointer:

`/home/bh/workspaces/loki/terminal-velocity-doc-archive/2026-06-09-tv-spec-supporting-docs/`

## Controlling goal

Terminal Velocity is an EV Classic fidelity-copy project.

Development must accelerate toward a broadly playable TV, but claims of **EV Classic faithful** require source-backed promotion. Do not independently optimize aesthetics, pacing, balance, “fun,” or generic playability unless the behavior is either EV Classic-supported or explicitly labeled as TV scaffold / temporary build-track behavior.

## Operating doctrine

**Parallel executable lanes + fast evaluators + batched integration + fidelity gates + playable-payoff dispatch.**

This means:

- build playable systems before perfect Classic evidence when the behavior is labeled honestly;
- never let scaffolds become fidelity claims without promotion;
- use `docs/checklists/tv-playable-milestone-priority-map.json` as a thin priority overlay over the backlog dispatch index so agents prefer broad playable coverage before isolated fidelity fragments unless a gate, conflict, or direct blocker overrides it;
- keep that overlay backlog-backed and structurally validated; it changes selection order, not source/fidelity authority;
- use Godot/Python scenario probes for fast TV-side verification;
- use Basilisk/original EV where runtime behavior matters;
- use decoded resources/manuals/local source artifacts for static/data semantics where they are stronger than emulator observation;
- integrate in small verified packets and continue until a real gate is reached.

## Evidence labels

Use these labels on behavior, backlog items, probes, and handoffs:

- `scaffold` — useful TV build-track approximation; not Classic truth.
- `terminal-velocity-observed` — observed in current TV runtime/probes.
- `source-grounded EV-family` — supported by weaker EV-family/community/adaptation evidence.
- `decoded-resource-backed` — supported by decoded EV Classic resources.
- `manual-backed` — supported by EV Classic manuals/docs/Bible/local source artifacts.
- `original-runtime-observed` — supported by Basilisk/original EV observation.
- `needs original confirmation` — plausible but not promoted.
- `fidelity-promoted` — evidence-backed enough for current Classic-faithful claim.

`source/fidelity label` means the human-readable evidence label from this section. `source_basis` is the normalized provenance vocabulary; it records substrate type and does not imply promotion by itself.

## Promotion rubric

A behavior may be marked `fidelity-promoted` only when the increment packet names:

- the exact claim being promoted;
- `oracle_class`;
- `source_basis` list;
- source/fidelity label;
- evidence path(s), capture(s), decoded manifest(s), or manual/resource reference(s);
- verifier command and actual result;
- remaining uncertainty, or `none`;
- promotion owner / integration owner;
- backlog or provenance artifact updated.

Promotion thresholds:

- **Static/resource semantics**: decoded EV Classic resources plus Resource Bible/manual field interpretation may promote field/data semantics, but not runtime UI/timing behavior unless separately observed or accepted as a surrogate.
- **Runtime UI/state transitions**: require original-runtime observation or a clearly documented accepted surrogate. Accepted surrogates require a backlog/provenance note naming the surrogate, scope, verifier, uncertainty, and owner; materially consequential surrogates require user decision. One observation may promote only the exact observed claim when capture quality, state setup, and verifier are recorded; broader generalization needs additional evidence.
- **Timing/feel/combat cadence**: require Basilisk/original-runtime evidence, with 1x sentinel or contradiction check before canonical timing promotion.
- **TV scaffolds**: cannot become `fidelity-promoted` without a later promotion packet.
- **EV-family/community/adaptation evidence**: may generate hypotheses or implementation scaffolds, but cannot by itself promote exact EV Classic fidelity.
- **Quirk/bug cases**: require quirk-ledger classification and user decision when preservation vs cleanup is materially consequential.

Conflict/staleness rule: if newer evidence conflicts with an existing source/fidelity label, `source_basis`, promoted claim, backlog status, worker packet, runtime capture, EV-family/community hypothesis, or Terminal Velocity scaffold assumption, reopen the relevant backlog/provenance entry and demote the affected claim or task to `needs evidence` or `blocked` until resolved. Do not keep stale labels or promotion status just because an older packet verified successfully.

## Routing decision tree

Classify every item before acting:

1. **Static/resource/manual-resolvable**
   - Oracle: decoded resources, manuals, local source artifacts, structured import/compare pipelines.
   - Lane: A/B/C/D static path as appropriate.
   - Basilisk: only spot-check ambiguous UI-sensitive surfaces.

2. **Runtime UI/state transition**
   - Oracle: Basilisk/original EV production evidence.
   - Lane: Basilisk runtime lane plus matching implementation lane.
   - Speed: highest qualified Basilisk speed for the evidence family.

3. **Timing/feel/combat cadence**
   - Oracle: acceleration-first scout evidence plus 1x sentinel for timing-sensitive promotion.
   - Lane: Basilisk timing lane plus TV build-track tuning/evaluator lane.
   - Speed: accelerated scouting allowed; broad 1x waits until late promotion or contradiction.

4. **TV-only scaffold/evaluator**
   - Oracle: Godot/Python verifier.
   - Lane: E deterministic evaluator/playtest.
   - Basilisk: none.

5. **Classic quirk/bug decision**
   - Oracle: original runtime, decoded resources/manuals, EV-family fix history, user decision.
   - Lane: quirk ledger + implementation lane only after classification.
   - Default: preserve intentional/player-legible quirks; do not preserve harmful, invisible, crashy, save-corrupting, misleading, platform-artifact, or implementation-artifact defects by default.

6. **Single safe-local slice**
   - Use direct edit/test/report. No Kanban/worktree needed.

7. **Durable parallel or multi-writer work**
   - Require lane contract, isolated worktree for mutating workers, fan-in owner, verifier, rollback path.

## Oracle classes

Every backlog item or task packet must carry one `oracle_class` for high-level routing:

- `static-resource`
- `manual-backed`
- `runtime-ui`
- `timing-feel`
- `combat-cadence`
- `tv-scaffold`
- `quirk-review`
- `user-decision`

Every backlog item, task packet, increment packet, scenario/probe, and promotion packet must also carry `source_basis`: a normalized list of evidence/provenance substrates. `source_basis` records what kind of source supports the claim; it does not imply promotion by itself. Allowed values:

- `decoded-record-family`
- `decoded-original-variable`
- `resource-bible-field`
- `manual-doc-backed`
- `original-runtime-observed`
- `terminal-velocity-observed`
- `ev-family-transfer`
- `community-guide`
- `external-adaptation-observed`
- `tv-scaffold`
- `user-decision`

Use a list when a claim has multiple bases, for example `source_basis: [decoded-original-variable, resource-bible-field]`. EV-family, community, adaptation, Terminal Velocity scaffold, and user-decision bases may route or justify implementation work only under the promotion rubric; they do not by themselves promote exact EV Classic fidelity claims. `user-decision` is a policy/quirk-review basis, not fidelity proof.

Basilisk is chosen only when the `oracle_class` requires original-runtime evidence or resolves ambiguity.

## Lane classes

Use these lane classes for dispatch:

- **Lane A: static galaxy topology semantics** — system/resource topology, IDs, names, links, coordinates, import semantics.
- **Lane B: service/store provisioning** — landed services, shipyard/outfitter/store availability, UI-sensitive service surfaces.
- **Lane C: economy/commodity semantics** — commodity names, prices, spreads, formulas, cargo behavior.
- **Lane D: mission-family semantic promotion** — mission offers, deadlines, flags, accept/complete/abort/log/story behavior.
- **Lane E: deterministic evaluator/playtest packets** — fast TV-observed scenarios, probes, failure packets, regression coverage; no Basilisk dependency.
- **Basilisk runtime lanes** — original-runtime evidence for runtime UI/state/timing/feel/combat and ambiguity resolution.

## Basilisk policy

TV must minimize original-runtime bottlenecks by using the **fastest qualified Basilisk speed per evidence family**. Do not make 1x the default production lane.

1x is limited to:

- tiny sentinel/control probes for timing-sensitive evidence families;
- targeted contradiction resolution when accelerated lanes disagree or drift;
- late canonical promotion for timing/feel claims.

The local setup provides **4 Basilisk emulator lanes**. Treat them as concrete original-runtime evidence capacity, not aspirational capacity and not four duplicate uncontrolled workers.

Each Basilisk lane assignment must record:

- emulator lane ID;
- `oracle_class` / evidence family;
- speed setting and qualification class;
- disk/prefs and pilot/save/restore state;
- window/input target;
- capture/log path;
- allowed mutations;
- post-run verification;
- integration-owner handoff.

If a lane lacks restore/capture/input/post-run records, classify that lane as `setup-incomplete`; do not reduce the count below four unless physical emulator capacity changes.

### Basilisk speed matrix

Maintain `docs/research/basilisk-speed-qualification.json` as the persistent speed qualification matrix rather than re-reasoning every task. Validate it with `python3 tools/basilisk_speed_qualification.py`.

```text
basilisk_speed_qualification:
  evidence_family:
  lane_id:
  speed:
  qualification_class: promotion-grade timing | promotion-grade non-timing | scout-grade | reject/unstable
  sentinel_used:
  verifier:
  last_checked:
  status:
  restore_readiness:
  capture_readiness:
  input_readiness:
  allowed_oracle_classes:
  disallowed_oracle_classes:
  promotion_limitations:
```

Use the highest current qualified speed for the explicit evidence family/lane/oracle class. Requalify only when stale, contradicted, unsafe, or a new evidence family is being introduced. Do not treat any speed qualification as global; timing/feel/combat promotion requires an explicit 1x sentinel or direct 1x evidence.

## Increment packet contract

The quality unit is a vertical increment, not a global serial slice.

Every completed increment must include:

- behavior or explicit symbolic surrogate;
- `oracle_class`;
- `source_basis` list;
- lane class;
- source/fidelity label;
- verifier command and actual result;
- files/captures/logs touched;
- backlog/provenance update or explicit `none` with reason;
- promotion status: `scaffold`, `needs evidence`, `fidelity-promoted`, `blocked`, or `user-gated`.

A verified increment is a local work checkpoint, not a required commit/push boundary and not necessarily a stop. A single long-running invocation may complete multiple adjacent verified increments when they share the same lane, source-basis family, verifier surface, and understandable dirty working set.

## Scenario/evaluator contract

Scenarios and probes must record:

- scenario id/name;
- `oracle_class`, `source_basis` list, and source/fidelity label;
- starting state / restore method;
- action sequence or macro source;
- expected predicate/success metric;
- blocked reason enum;
- verification command;
- actual result;
- failure packet path, or `none` with reason;
- logs/screenshots/traces/JSON events;
- promotion rule from finding to regression/backlog entry.

Godot semantic probes should prefer stable JSON/event outputs. Basilisk observations need screenshots/logs and uncertainty labels.

## Worker/Basilisk handoff contract

A handoff is invalid unless it includes:

- lane id;
- exact files/captures/logs;
- `oracle_class`, `source_basis` list, and source/fidelity labels;
- verifier command/result;
- exact claim being made;
- promotion requested or explicitly not requested;
- unresolved uncertainty;
- rollback/cleanup note.

Subagent/worker output is an unverified claim packet until the integration owner checks returned paths, diffs, tests, and labels against live repo state.

## Parallel limits and fan-in

Default limits:

- 1 integration owner;
- 3 active mutating worker lanes initially;
- scale to 5 only after at least two consecutive multi-lane integrations complete without unresolved merge conflicts, unverified returned paths, or failed integrated verification;
- 1–2 read-only scouts/reviewers;
- 4 Basilisk emulator lanes;
- up to 3 unresolved worker/scout/reviewer packets awaiting integration-owner verification.

Rules:

- one integration owner owns fan-in, final diff review, integrated verification, commit, and normal non-force push; use `tools/tv_integration_lane.py --dry-run` as the deterministic guard packet before any LLM-assisted publish decision;
- mutating workers use isolated worktrees;
- each lane has owner, writable surface, verifier, source-label policy, merge contract, rollback/cleanup path;
- one writer per file/resource surface;
- Kanban/worktrees are for durable multi-lane work, not line-level patches or a single safe-local slice.

## Runner ownership and dispatch surfaces

TV implementation dispatch uses a single-owner control-plane model:

- `none_active` — no background implementation owner is active;
- `direct_session` — the current chat/session owns safe-local edits;
- `continuous_kanban_runner` — one explicitly started TV standalone continuous runner using/dispatching Kanban owns implementation dispatch;
- `gateway_kanban_dispatcher` — the profile gateway Kanban dispatcher owns TV implementation dispatch when actual TV Kanban board claims/tasks/workers show it owns TV work;
- `integration_owner` — fan-in, final review, normal non-force push, fetch, and remote verification. This is a named coordinator lane, not the generic gateway dispatcher; the dispatcher may invoke it, but the lane cannot implement feature work.

Only one implementation-dispatch owner may be active at a time. Cron is not an implementation owner. A scheduled cron surface, if retained, must be no-agent, script-only reporting or health observation; it must not implement, repair, coordinate, dispatch workers, edit the repo, or act as an LLM fallback for TV work.

Gateway Kanban dispatch, TV standalone continuous loops using/dispatching Kanban, direct sessions, and integration-owner fan-in are distinct control planes. Do not treat clearing one surface as proof that the others are stopped or authorized. Before starting any background implementation runner, run a topology preflight that derives current runtime truth from live cron metadata, detached process state, loop state, actual TV Kanban board claims/tasks/workers, gateway dispatch configuration, git state, and other active control-plane surfaces first, then reconciles `.hermes/long-running/tv-spec-implementation/task-ledger.json` only as declared intent/checkpoint state. The ledger is not live runtime truth by itself. Startup fails closed with a recorded `active_owner_conflict` when another implementation-dispatch owner is active or unresolved. Stale ledger-only disagreement is recorded as precise warnings such as `ledger_projection_stale` or `ledger_historical_owner_mismatch`, with `ledger_reconciliation_actions` naming follow-up such as `normalize_ledger_projection`; passive no-agent reporting cron surfaces are `passive_reporter_ignored`; completed/disabled bootstrap jobs are `stale_bootstrap_job_ignored`; globally enabled gateway dispatch without TV-specific active board/process evidence is `gateway_global_enabled_warning`. Until the topology checker implements the full live-state inspection above, any `topology_conflict` derived only from ledger/config is a diagnosis candidate that must be rechecked against live state before restart, STOP removal, cron/config mutation, or publication.

### Runner start/resume blocker protocol

Starting or resuming the TV game-development runner is a control-plane operation, not proof of liveness from a clean topology check. The start protocol must identify the single intended implementation owner surface and inspect live repo, Kanban, runner-state, ledger/event, lock/stop-file, cron/watchdog/reporter, and target-worker capability surfaces before seeding or dispatching implementation work.

When startup is requested, the protocol must return exactly one of: a claimed/started owner verified by a running or claimed task, heartbeat/log/summary update, or equivalent live proof; completed integration recovery; one clean successor seed/dispatch; or a concrete `blocked:*` class. A clean topology with `live_implementation_owner: none_active` proves absence of conflict, not successful start/resume. Clean idle state must not hide unresolved `push_ready`, stale `review_required_process_bug`, failed-verifier, unsafe dirty-state, explicit-human-gate, or unclassified blocked TV handoffs.

The start protocol performs a broad process-blocker search, not broad native test discovery. Code/test verification remains governed by `docs/checklists/tv-verifier-impact-map.json`: run the focused relevant verifier for the touched surface first, and treat full native discovery as checkpoint-optional unless separately justified.

`task-ledger.json` is a generated checkpoint projection, not the live control plane. Live ownership must be derived from live Kanban/process/cron/watchdog/lock/git surfaces, not from historical ledger fields. Ledger fields such as `declared_owner`, `runner_ownership.implementation_owner`, `allowed_surfaces.*`, or `status: running` are historical/checkpoint metadata unless they carry a fresh live assertion source and timestamp. `running` paired with `none_active` is stale projection data requiring reconciliation into a precise class such as `ledger_projection_stale`, `ledger_historical_owner_mismatch`, `dirty_handoff_pending`, `unsafe_dirty_state`, or true `live_owner_conflict`; projection staleness names the reconciler/normalizer action and is not by itself a live-owner conflict.

Related rationale artifact: `docs/research/tv-kanban-topology-review-2026-06-10.md` records why TV's Kanban setup is project-specific: standard Hermes Kanban owns board/claim dispatch, while TV adds a single-owner runner topology around that board. Future topology work should inspect actual TV Kanban claims/tasks before treating gateway dispatch as a live TV implementation owner.

## Backlog dispatch contract

The live execution surface is:

`docs/checklists/ev-classic-fidelity-implementation-backlog.md`

It is not an idea dump. Each actionable backlog item should expose:

```text
next_action:
lane_class:
oracle_class:
source_basis:
verifier:
blocked_reason:
promotion_status:
```

Before adding fresh work, prefer existing `ready`, narrow `needs evidence`, or safely actionable items. New evidence should produce one of:

- small source-backed implementation slice;
- labeled TV scaffold;
- bounded `needs evidence` / blocked next action;
- quirk-ledger entry requiring user decision.

### Verifier impact map

Maintain `docs/checklists/tv-verifier-impact-map.json` as the canonical routing map from touched surfaces to cheapest sufficient verifier families. Validate it through `python3 tools/backlog_dispatch_index.py check` and `python3 -m unittest native_ev.tests.test_backlog_dispatch_index -v`.

Required surface keys:

- `extractor`
- `scenario`
- `godot_probe`
- `data_manifest`
- `backlog_dispatch_metadata`
- `docs_process_only`

For each actionable backlog item with `touched_surfaces`, the dispatch checker requires every touched surface to resolve to one of those keys and requires a non-empty `verifier`. The v1 rule is structural: verifier routing must name a sufficient verifier family; exact command equivalence is not enforced.

## Git checkpoint policy

Commit/push is a durability or coordination action, not the unit of development. Do not commit/push merely because a coherent local slice completed.

Checkpoint policy decides when remote publication has coordination or durability value; role policy decides who may publish. A normal coherent non-force push is not human-gated under existing repo policy, but only the integration owner performs the push. The integration owner is automated as a two-layer lane: deterministic guard script first, then LLM-assisted bundle review.

Workers/continuous runners may checkpoint locally when this policy triggers, but they do not push. A worker does not stop merely because local `main` is ahead of `origin/main`. When remote publication is actually needed, a worker records `push_ready` with commit SHA, intended files, verification commands/results, why remote state is needed, and remaining next action, then continues safe local work when possible. A worker stops only at a real gate, cap/handoff boundary, unsafe dirty state, failed verifier, or no-safe-local-slice boundary. Missing GitHub credentials in a worker are not a TV development gate.

### Worker closeout and stale review-gate policy

Workers and continuous runners must not use human `review-required` as a generic closeout for verified safe-local TV work. File changes, local branch-ahead state, missing push credentials, or unrelated broad-suite failures are not human gates by themselves.

At worker closeout, classify the state into exactly one canonical outcome: `continue`, `push_ready`, `blocked: verifier_failed`, `blocked: unsafe_dirty_state`, `blocked: explicit_human_gate`, `blocked: cap_handoff`, or `blocked: no_safe_local_slice`. If targeted verifier(s) passed for the touched TV surface and any broad-suite failure is labeled unrelated to the slice, the worker must not stop as `review-required`. It must continue, create a local checkpoint and record `push_ready`, or block under one of the concrete `blocked:*` classes above.

Worker verifier selection starts from `docs/checklists/tv-verifier-impact-map.json`: run the focused required verifier for the touched surface first, using the cheapest sufficient verifier family that proves the changed claim. Full native discovery (`python3 -m unittest discover -s native_ev/tests -p 'test_*.py'`) is checkpoint-optional, not a default gate; run it only when justified by the touched native/model surface, checkpoint/handoff boundary, integration-owner preflight, unclear dependency risk, large accumulated bundle sealing, or explicit user request. If full discovery is run and known unrelated failures appear, record them as `known_unrelated_failure_surface` without overriding a passing focused verifier for the slice.

`ready_for_review_or_integration` is non-canonical wording. Normalize it to `push_ready` when the next step is integration-owner publication, or to a concrete `blocked:*` status when a real blocker exists.

Closeout packets, Kanban comments, and ledger/event checkpoint records are handoff evidence, not optional prose. A blocked or dirty-handoff recovery path must inspect structured closeout packets such as `.hermes/long-running/tv-spec-implementation/closeout-packet-*.json`, Kanban comment handoffs, `latest_summary`, ledger projection fields, and event-tail checkpoint records before classifying a safe dirty bundle as missing handoff evidence. Closeout packets meant for recovery must include `closeout_class`, `kanban_task`, `changed_files`, generated/checkpoint `ledger_files` when applicable, `event_ids` when known, structured `verification`, `next_action`, and `successor_kanban_task` when a successor exists. If these surfaces agree on changed files and relevant verifier success, recovery returns `checkpoint_and_push_ready` or `push_ready`; if verifier freshness is uncertain, return `rerun_focused_verifier` with the exact verifier commands. Reserve `unsafe_dirty_state` for sensitive paths, unrelated extra paths, failed relevant verifier, or no matching handoff after all listed evidence surfaces were inspected.

The integration owner performs final status/diff review, runs required checkpoint verification, creates or validates the local checkpoint commit when recovering a stale worker handoff, pushes normal non-force bundles, fetches, verifies local `HEAD == origin/main`, and records the pushed checkpoint. Integration is event-triggered: publish as infrequently as possible while preventing worker blockage, stale coordination, context/reset loss, or inspection-expensive local divergence. Do not push by maximum-frequency cadence, per-commit habit, or arbitrary commit-count batching. The deterministic publish preflight is `python3 tools/tv_integration_lane.py --dry-run --blocked-report-target 'telegram:Loki GameTV'`; it must report no active worker, no unsafe dirty worktree, no branch-behind state, only safe TV paths, `git diff --check`, and committed-diff secret scan before an LLM review may return `publish`. Actual push uses `python3 tools/tv_integration_lane.py --push --llm-approved --post-push-report-target 'telegram:Loki GameTV' --blocked-report-target 'telegram:Loki GameTV'` only after that exact-bundle review. If the integration owner blocks runner progress or causes the runner to stop, it sends the immediate why-blocked report to Loki GameTV; cron/reporting watchdogs are not the primary path. One clean commit may be pushed immediately if it unblocks another lane; several adjacent commits may remain local when no one is blocked and the stack remains coherent and easy to inspect.

When the lane is idle but the worktree is dirty, classify the dirty bundle before publish preflight or successor seeding. Match by evidence, not by vague recency: compare the dirty file set against the active or newest dirty-matching Kanban task, handoff intended-file list, closeout packet `changed_files`, Kanban comment handoff, `latest_summary`, ledger/event tail, and verifier output covering the exact dirty bundle. If the bundle matches, handle it as integration recovery before publish preflight: validate intended dirty files against the handoff and ledger/event tail, scan for sensitive/proprietary/unrelated paths, verify or rerun the focused relevant verifier, create the coherent local checkpoint if missing, record or normalize `push_ready`, run the deterministic integration lane, and then dispatch exactly one successor if no real gate remains. An autostart watchdog may detect, report, or route this state, but only the integration owner mutates repo/task state, creates commits, or pushes. If dirty paths do not match a handoff after inspecting Kanban comments, closeout packets, ledger/event records, and task-list prose, block as `unsafe_dirty_state` or `missing_handoff` with exact paths and evidence surfaces inspected instead of seeding overlapping work.

A publish guard that reports `dirty_worktree`/`nothing_to_publish` is not itself a recovery failure for an uncommitted worker slice; it means the integration owner must run the uncommitted-handoff recovery classifier first, then rerun the normal publish guard after a coherent checkpoint exists.

Run the full checkpoint procedure only when one of these is true:

- user explicitly asks for a checkpoint/push;
- context/tool/reset limit is near and uncommitted work would be costly to reconstruct;
- work is about to switch to a different subsystem and the current bundle should be sealed;
- a risky/destructive/original-runtime step is about to begin and the repo needs a rollback anchor;
- another worker/session needs the work from the remote;
- work changes project-governing docs/spec/backlog in a way that future sessions are likely to rely on before the next natural checkpoint;
- local work has accumulated enough that losing it would be painful or reviewing it later would become inspection-expensive;
- a recorded `push_ready` state is blocking another card/lane and standard normal-push checks pass.

Otherwise, keep the slice verified locally and continue. Fidelity discipline comes from source labels, verifiers, and backlog/provenance updates, not from remote publication after every slice.

## Long-running efficiency policy

Optimize the continuous workflow for accumulated development time without weakening source/fidelity claims:

- **Batch adjacent increments in one invocation.** Continue inside the same invocation while work remains in the same lane/subsystem, uses the same source-basis family and verifier surface, has no real gate or failed verifier, stays below context/tool cap pressure, and the dirty working set remains understandable. Stop at gates, failures, subsystem switches, risky original-runtime steps, checkpoint-policy triggers, or cap/handoff boundaries.
- **Report externally only at material boundaries.** Send Telegram/progress reports for gates, failures, checkpoint commits/pushes, fidelity promotions/demotions, explicit user requests, or periodic batch summaries. Routine verified increments can be recorded locally in the ledger/events log and summarized together.
- **Update backlog/provenance only when future execution changes.** Use migration-on-touch. Patch the live backlog/provenance when next action, verifier, blocker/gate, source basis, promotion status, or future dispatch would otherwise be stale; otherwise record `none` with reason in the increment packet/event.
- **Match verifier breadth to risk.** Each increment needs the narrowest verifier that proves the changed claim. Broad repo hygiene, JSON/JSONL parse sweeps, secret scans, remote checks, full scenario suites, and Godot self-tests run at checkpoint/handoff/risk boundaries or when their surface was touched, not automatically after every local increment.
- **Use event log for routine history and ledger for resumable state.** Append compact events for ordinary increment history. Rewrite the ledger only for current status, active gate, next action, last verification summary, changed runner policy, and self-contained resume prompt.
- **Avoid workers/subagents for mechanical sequential lanes.** Use direct tools/scripts for linear source-mining, extractor/model/test loops, and tightly coupled dirty work. Spawn workers only for genuinely independent parallel lanes where the expected parallelism beats fan-in and verification overhead.

## Normal workflow

Use this loop:

1. Classify item: build scaffold / fidelity promotion / static semantic / runtime UI / timing-feel / quirk.
2. Pick oracle: decoded resource / manual / Godot-Python evaluator / Basilisk / user decision.
3. Pick lane: A, B, C, D, E, or Basilisk runtime lane.
4. Execute the smallest vertical increment, then continue through adjacent increments under the long-running efficiency policy when safe.
5. Emit or locally record increment packets with files, command output, `oracle_class`, `source_basis`, evidence label, promotion status, uncertainty, and gates; batch routine external reports.
6. Integrate: one owner verifies, updates backlog/provenance only when future execution state changes, performs any local checkpoint commit when the Git checkpoint policy is triggered, and pushes only when acting as the integration owner.
7. Continue unless a real gate, cap/handoff boundary, failed verifier, unsafe dirty state, or no-safe-local-slice condition is reached.

## Autoresearch boundary

Normal TV work is vertical/parallel implementation with fidelity gates. Mutation-heavy exploration, autoresearch, RL/evolutionary loops, and scheduled LLM mutation are excluded unless separately gated with goal, metric, baseline, mutable surface, trusted evaluator or verification surface, budget, experiment log, keep/revert rule, and human gates.

## Human gates

Gated:

- destructive/risky original-EV tests;
- Strict Play;
- save-corrupting or hard-to-restore original pilot mutation;
- raw proprietary asset publication;
- external/account/config/provider/gateway changes;
- changing/resuming scheduled cron/watchdog jobs;
- force-push/history rewrite;
- deletion, release/settings changes;
- non-TV repo/public/social side effects.

Not gated:

- ordinary safe-local TV development in the current session;
- local branch-ahead state by itself;
- worker `push_ready` records that identify normal remote-publication need without unsafe state;
- dirty safe-local worker bundles that match an intended TV handoff and have passing relevant verifier(s), provided the integration owner first performs intended-file, sensitive-path, diff-check, and exact-bundle review;
- unrelated broad-suite failures that are explicitly labeled as not covering the touched slice and are paired with passing relevant verifier(s);
- conversion of stale `review-required` or `ready_for_review_or_integration` worker states into canonical `push_ready` or a concrete `blocked:*` class by the integration owner;
- normal coherent non-force TV pushes by the integration owner under the existing repo policy after standard status/remotes/branch, intended-file, sensitive-value, relevant-verifier, push, fetch, and `HEAD == origin/main` checks.

## Completion definition

A TV workflow increment is complete only when its packet or event can state:

- files inspected and modified;
- `oracle_class`;
- `source_basis`;
- evidence/source-fidelity label used;
- `promotion_status`;
- verifier command and actual result;
- backlog/provenance update or explicit `none` with reason;
- remaining blocker/gate, if any.

The user-facing report may summarize a batch of completed increments instead of repeating every packet, provided the durable ledger/events retain enough detail to resume safely.
