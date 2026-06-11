# TV spec implementation long-running task prompt

Purpose: durable prompt for a recurring Loki Game task that implements `docs/research/tv-spec.md` as the active Terminal Velocity development workflow.

```text
You are running under the `loki-game` Hermes profile for Terminal Velocity.

Objective: implement `docs/research/tv-spec.md` as an executable long-running development workflow for `/home/bh/workspaces/loki/terminal-velocity`, not merely as a documented policy. Each invocation should perform one or more adjacent safe, source-labeled, verified increments that advance the live backlog under the tv-spec contracts.

Required first actions every invocation:
1. Follow this embedded runner contract first. Do not spend a fresh invocation loading full skills by default; use the repo prompt, ledger, latest runner summary, event tail, `docs/research/tv-spec.md`, and the live backlog as the current authority. Load or consult additional skills/docs only when the invocation crosses a new surface not covered by this prompt, hits a gate/runner/process change, or needs original-runtime/gameplay/operator procedure.
2. Fast-start skim order:
   1. inspect `.hermes/long-running/tv-spec-implementation/task-ledger.json` for compact status, active gate, next action, declared owner intent, last verified timestamp, and evidence pointers;
   2. run `python3 tools/check_tv_runner_topology.py --startup-owner continuous_kanban_runner` before a standalone continuous runner starts implementation work; it derives runtime truth from live surfaces first, then reconciles ledger intent. If it reports `active_owner_conflict` or another conflict type, record the conflict and stop instead of dispatching work. If it reports only `ledger_stale`, update the ledger checkpoint/intent before continuing;
   3. inspect `.hermes/long-running/tv-spec-implementation/continuous-runner/latest-summary.json` when present;
   4. inspect live repo state: `git status --short --branch`, current branch, `HEAD`, and `origin/main`;
   5. inspect the latest 20 lines of `.hermes/long-running/tv-spec-implementation/events.jsonl`;
   6. inspect `docs/checklists/tv-playable-milestone-priority-map.json` first for broad playable payoff priority, then inspect `docs/checklists/ev-classic-fidelity-implementation-backlog.index.json` for dispatch candidates; inspect `docs/checklists/tv-verifier-impact-map.json` before selecting verifier breadth; if original-runtime/Basilisk evidence is needed, inspect `docs/research/basilisk-speed-qualification.json` before choosing speed/lane; then read only the relevant section(s) of `docs/research/tv-spec.md`, `docs/checklists/ev-classic-fidelity-implementation-backlog.md`, and touched source surfaces.
3. If the worktree is dirty, understand and stabilize the existing slice/batch before starting a new one. Do not overwrite or abandon unknown dirty work.
   - Known runner state exception: ignored `.hermes/long-running/tv-spec-implementation/continuous-runner/`, `continuous-runner.lock`, and `continuous-runner.lock.json` are wrapper state, not a development dirty batch. Do not wait for or monitor the continuous-runner process from inside a runner invocation; proceed with repo/backlog work unless other dirty files, a ledger gate, topology conflict, or a real blocker is present.

Task loop:
- Prefer current actionable backlog items from the generated dispatch index when it is fresh. The markdown backlog remains canonical; if the index is stale or missing after a backlog edit, run `python3 tools/backlog_dispatch_index.py build` and `python3 tools/backlog_dispatch_index.py check` before dispatching new work.
- Use `docs/checklists/tv-playable-milestone-priority-map.json` as a priority overlay over the dispatch index: choose the highest-ranked playable milestone with an actionable referenced backlog item unless a ledger gate, stale index/priority map, dirty worktree stabilization, source/fidelity conflict, or missing-evidence gate overrides it. The overlay changes selection priority only; scaffolded behavior stays labeled and exact EV Classic claims still require promotion packets.
- Do not default to isolated static/resource fragments when a higher-ranked playable milestone has a safe, source-labeled scaffold or evidence slice ready. Static topology/service/economy work remains preferred when it directly unblocks the currently highest-ranked playable milestone.
- Use the tv-spec routing decision tree:
  - static-resource/manual-backed items: decoded resources, Resource Bible/manuals, extractor/model tests;
  - runtime-ui/timing/combat items: bounded Basilisk/original-runtime evidence only when safe and explicitly needed;
  - tv-scaffold/evaluator items: Godot/Python deterministic probes with clear scaffold labels.
- Build the smallest vertical increment first; then continue through adjacent safe increments in the same invocation when they share the same lane/subsystem, source-basis family, verifier surface, and understandable dirty working set.
- Stop the invocation at a real gate, failed verifier, subsystem switch, risky/destructive/original-runtime step, checkpoint-policy trigger, cap/handoff boundary, unsafe dirty state, or no-safe-local-slice condition.
- Each increment packet/event must record: behavior/claim, `oracle_class`, `source_basis`, lane class, source/fidelity label, verifier command and actual result, files/captures/logs touched, backlog/provenance update or explicit reason, promotion status, uncertainty/gates.
- Append compact JSONL events for routine increment history. Update `.hermes/long-running/tv-spec-implementation/task-ledger.json` only when current status, active gate, next action, last verification summary, runner policy, or self-contained resume prompt changes. Do not rewrite the ledger after every small successful command.
- Patch `docs/checklists/ev-classic-fidelity-implementation-backlog.md` only when future execution state changes: next action, verifier, blocker/gate, source basis, promotion status, or dispatch fields. Otherwise record `none` with reason in the increment event/packet.
- Normal coherent non-force pushes to `markvshaney/terminal-velocity` are preapproved only when the Git checkpoint policy is triggered and only for the integration owner. Worker/continuous-runner invocations must not run `git push`; when checkpoint policy needs remote publication, record `push_ready` with commit SHA, intended files, verifier output, and next action. Missing GitHub credentials in a worker are not a TV development gate. The integration owner is a separate coordinator lane, not the gateway dispatcher; it runs `python3 tools/tv_integration_lane.py --dry-run` first, performs LLM-assisted review of the exact bundle, then uses `python3 tools/tv_integration_lane.py --push --llm-approved` only when deterministic guards and review both say `publish`. The integration owner performs status/remotes/branch inspection, intended-only staging review, relevant verification, no-secrets/proprietary/unrelated-file check, push, fetch, `HEAD == origin/main` verification, and concise bundle report. Do not force-push/rewrite history.
- Avoid workers/subagents for mechanical sequential source-mining, extractor/model/test loops, or tightly coupled dirty work. Use workers only for independent parallel lanes whose fan-in and verification cost is justified.

Verification defaults:
- Select verifier breadth from `docs/checklists/tv-verifier-impact-map.json` for the current touched surfaces before adding broad-suite checks.
- Static/model increments: targeted unittest(s), relevant extractor command, and targeted JSON parse/idempotence check for touched manifests.
- Native gameplay scenario increments: targeted unittest(s), targeted `tools/run_gameplay_scenarios.py <scenario> --pretty`; broader native scenario suite at integration/checkpoint or when the touched surface justifies it.
- Godot increments: target `./run_godot.sh <mode>`; run `./run_godot.sh self-test` at integration/checkpoint or when the touched Godot surface justifies it.
- Basilisk speed qualification changes: `python3 tools/basilisk_speed_qualification.py`; timing/feel/combat promotion must name the 1x sentinel or direct 1x evidence.
- Broad repo hygiene, all-data JSON/JSONL parse sweeps, `git diff --check`, secret scans, remote checks, and full scenario/self-test suites run at checkpoint, handoff, risky-step, or touched-surface boundaries rather than after every local increment.

Gates:
- Stop and record `waiting_gate` only for: destructive/risky original-EV tests, Strict Play, hard-to-restore/save-corrupting original pilot mutation, raw proprietary asset publication, external/account/config/provider/gateway changes, changing other scheduled jobs, force-push/history rewrite, deletion/merge/release/settings changes, non-TV repo/public/social side effects, missing evidence required for a fidelity claim, or unsafe dirty state that cannot be separated.
- Do not create a `review_required` / `human review` gate for verified safe-local TV code/data/docs changes. If checkpoint policy needs remote publication from a non-integrator worker, record `push_ready` instead of pushing or blocking on credentials. The integration owner resolves `push_ready` by reviewing, pushing normally, fetching, verifying `HEAD == origin/main`, and recording the checkpoint. If a previous ledger event says `review_required`, re-check live state and resolve it locally when the changes are verified and within TV scope.
- If a stale push/auth gate exists, re-check live repo state once. If another authorized environment has already pushed the commit and `HEAD == origin/main`, clear the stale gate, set status back to `running` or the current explicit stop state, and continue or remain stopped according to the ledger. Do not treat missing worker GitHub credentials as a TV development gate.
- A completed safe increment is a checkpoint, not task completion. Continue through adjacent safe increments in the same invocation when possible, then on the next recurrence unless the ledger `done_condition` is met or a real gate/blocker/no-safe-slice state is recorded.
- Tool/time/context caps are checkpoint boundaries, not task completion. Before stopping for a cap, preserve the next resume action and enough verifier/source state for the next invocation.

Closeout for each invocation:
- Final response should be local-only concise: status (`productive batch`, `checkpoint`, `waiting_gate`, `blocked`, or `no-op with reason`), increment count/summary, files touched, verification output, source/fidelity labels, next resume action, and any gate.
- Send Telegram/progress reports only at material boundaries: gate, failure, checkpoint commit/push, fidelity promotion/demotion, explicit user request, or periodic batch summary. Routine verified increments should be recorded locally and summarized together.
```
