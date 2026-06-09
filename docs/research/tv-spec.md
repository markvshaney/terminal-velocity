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

**Parallel executable lanes + fast evaluators + batched integration + fidelity gates.**

This means:

- build playable systems before perfect Classic evidence when the behavior is labeled honestly;
- never let scaffolds become fidelity claims without promotion;
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

- one integration owner owns fan-in, final diff review, integrated verification, commit, and normal non-force push;
- mutating workers use isolated worktrees;
- each lane has owner, writable surface, verifier, source-label policy, merge contract, rollback/cleanup path;
- one writer per file/resource surface;
- Kanban/worktrees are for durable multi-lane work, not line-level patches or a single safe-local slice.

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

## Git checkpoint policy

Commit/push is a durability or coordination action, not the unit of development. Do not commit/push merely because a coherent local slice completed.

Run the full commit/push procedure only when one of these is true:

- user explicitly asks for a checkpoint/push;
- context/tool/reset limit is near and uncommitted work would be costly to reconstruct;
- work is about to switch to a different subsystem and the current bundle should be sealed;
- a risky/destructive/original-runtime step is about to begin and the repo needs a rollback anchor;
- another worker/session needs the work from the remote;
- work changes project-governing docs/spec/backlog in a way that future sessions are likely to rely on before the next natural checkpoint;
- local work has accumulated enough that losing it would be painful.

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
6. Integrate: one owner verifies, updates backlog/provenance only when future execution state changes, and commits/pushes only when the Git checkpoint policy is triggered.
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
- normal coherent non-force TV pushes under the existing repo policy.

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
