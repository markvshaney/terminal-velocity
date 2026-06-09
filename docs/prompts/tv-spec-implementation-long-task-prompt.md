# TV spec implementation long-running task prompt

Purpose: durable prompt for a recurring Loki Game task that implements `docs/research/tv-spec.md` as the active Terminal Velocity development workflow.

```text
You are running under the `loki-game` Hermes profile for Terminal Velocity.

Objective: implement `docs/research/tv-spec.md` as an executable long-running development workflow for `/home/bh/workspaces/loki/terminal-velocity`, not merely as a documented policy. Each invocation should perform one or more adjacent safe, source-labeled, verified increments that advance the live backlog under the tv-spec contracts.

Required first actions every invocation:
1. Follow this embedded runner contract first. Do not spend a fresh invocation loading full skills by default; use the repo prompt, ledger, latest runner summary, event tail, `docs/research/tv-spec.md`, and the live backlog as the current authority. Load or consult additional skills/docs only when the invocation crosses a new surface not covered by this prompt, hits a gate/runner/process change, or needs original-runtime/gameplay/operator procedure.
2. Fast-start skim order:
   1. inspect `.hermes/long-running/tv-spec-implementation/task-ledger.json` for status, active gate, and next action;
   2. inspect `.hermes/long-running/tv-spec-implementation/continuous-runner/latest-summary.json` when present;
   3. inspect live repo state: `git status --short --branch`, current branch, `HEAD`, and `origin/main`;
   4. inspect the latest 20 lines of `.hermes/long-running/tv-spec-implementation/events.jsonl`;
   5. inspect `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json` first for dispatch candidates, then read only the relevant section(s) of `docs/research/tv-spec.md`, `docs/checklists/ev-classic-fidelity-implementation-backlog.md`, and touched source surfaces needed for the current slice.
3. If the worktree is dirty, understand and stabilize the existing slice/batch before starting a new one. Do not overwrite or abandon unknown dirty work.
   - Known runner state exception: ignored `.hermes/long-running/tv-spec-implementation/continuous-runner/`, `STOP_CONTINUOUS_RUNNER`, `continuous-runner.lock`, and `continuous-runner.lock.json` are wrapper state, not a development dirty batch. Do not wait for or monitor the continuous-runner process from inside a runner invocation; proceed with repo/backlog work unless other dirty files, a ledger gate, or a real blocker is present.

Task loop:
- Prefer current actionable backlog items from the generated dispatch index when it is fresh. The markdown backlog remains canonical; if the index is stale or missing after a backlog edit, run `python3 tools/backlog_dispatch_index.py build` and `python3 tools/backlog_dispatch_index.py check` before dispatching new work.
- Default initial lane, if the repo is clean and no stronger live blocker exists: Lane A static galaxy topology semantics from the backlog item “Fuller EV Classic galaxy topology and coordinates,” continuing one field family at a time after the current `syst` coordinate/link-slot static promotions.
- Use the tv-spec routing decision tree:
  - static-resource/manual-backed items: decoded resources, Resource Bible/manuals, extractor/model tests;
  - runtime-ui/timing/combat items: bounded Basilisk/original-runtime evidence only when safe and explicitly needed;
  - tv-scaffold/evaluator items: Godot/Python deterministic probes with clear scaffold labels.
- Build the smallest vertical increment first; then continue through adjacent safe increments in the same invocation when they share the same lane/subsystem, source-basis family, verifier surface, and understandable dirty working set.
- Stop the invocation at a real gate, failed verifier, subsystem switch, risky/destructive/original-runtime step, checkpoint-policy trigger, cap/handoff boundary, unsafe dirty state, or no-safe-local-slice condition.
- Each increment packet/event must record: behavior/claim, `oracle_class`, `source_basis`, lane class, source/fidelity label, verifier command and actual result, files/captures/logs touched, backlog/provenance update or explicit reason, promotion status, uncertainty/gates.
- Append compact JSONL events for routine increment history. Update `.hermes/long-running/tv-spec-implementation/task-ledger.json` only when current status, active gate, next action, last verification summary, runner policy, or self-contained resume prompt changes. Do not rewrite the ledger after every small successful command.
- Patch `docs/checklists/ev-classic-fidelity-implementation-backlog.md` only when future execution state changes: next action, verifier, blocker/gate, source basis, promotion status, or dispatch fields. Otherwise record `none` with reason in the increment event/packet.
- Normal coherent non-force pushes to `markvshaney/terminal-velocity` are preapproved only when the Git checkpoint policy is triggered. After the established TV checks, inspect status/remotes/branch, stage intended files only, run relevant verification, check no secrets/proprietary/unrelated files, push, fetch, verify local `HEAD == origin/main`, and report concise bundle summary. Do not force-push/rewrite history.
- Avoid workers/subagents for mechanical sequential source-mining, extractor/model/test loops, or tightly coupled dirty work. Use workers only for independent parallel lanes whose fan-in and verification cost is justified.

Verification defaults:
- Static/model increments: targeted unittest(s), relevant extractor command, and targeted JSON parse/idempotence check for touched manifests.
- Native gameplay scenario increments: targeted unittest(s), targeted `tools/run_gameplay_scenarios.py <scenario> --pretty`; broader native scenario suite at integration/checkpoint or when the touched surface justifies it.
- Godot increments: target `./run_godot.sh <mode>`; run `./run_godot.sh self-test` at integration/checkpoint or when the touched Godot surface justifies it.
- Broad repo hygiene, all-data JSON/JSONL parse sweeps, `git diff --check`, secret scans, remote checks, and full scenario/self-test suites run at checkpoint, handoff, risky-step, or touched-surface boundaries rather than after every local increment.

Gates:
- Stop and record `waiting_gate` only for: destructive/risky original-EV tests, Strict Play, hard-to-restore/save-corrupting original pilot mutation, raw proprietary asset publication, external/account/config/provider/gateway changes, changing other scheduled jobs, force-push/history rewrite, deletion/merge/release/settings changes, non-TV repo/public/social side effects, missing evidence required for a fidelity claim, or unsafe dirty state that cannot be separated.
- A completed safe increment is a checkpoint, not task completion. Continue through adjacent safe increments in the same invocation when possible, then on the next recurrence unless the ledger `done_condition` is met or a real gate/blocker/no-safe-slice state is recorded.
- Tool/time/context caps are checkpoint boundaries, not task completion. Before stopping for a cap, preserve the next resume action and enough verifier/source state for the next invocation.

Closeout for each invocation:
- Final response should be local-only concise: status (`productive batch`, `checkpoint`, `waiting_gate`, `blocked`, or `no-op with reason`), increment count/summary, files touched, verification output, source/fidelity labels, next resume action, and any gate.
- Send Telegram/progress reports only at material boundaries: gate, failure, checkpoint commit/push, fidelity promotion/demotion, explicit user request, or periodic batch summary. Routine verified increments should be recorded locally and summarized together.
```
