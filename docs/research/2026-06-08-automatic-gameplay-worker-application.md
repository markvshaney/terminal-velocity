# Automatic gameplay sources: worker application deep dive

Date: 2026-06-08
Purpose: convert the automatic-gameplay/game-testing source stack into concrete Terminal Velocity worker patterns. This is a process and automation-design artifact. It is **not** EV Classic behavior evidence.

## Source boundary

Use these labels on any output that cites this page:

- `automation-design`: general game-agent/game-testing/process pattern.
- `terminal-velocity-observed`: Terminal Velocity scenario/Godot/log evidence.
- `original-runtime-observed`: Basilisk/EV Classic runtime evidence.
- `decoded-resource-backed` or `manual/docs-backed`: EV Classic source/data evidence.
- `external-adaptation-observed`: behavior of an external tool/source itself, not EV behavior.

External automation sources can justify worker shape, trace format, evaluator design, and promotion rules. They do not justify EV Classic gameplay semantics.

## Sources rechecked in this pass

Existing project sources:

- `docs/research/automated-gameplay-learning-reference-sources.md`
- `docs/research/ev-automated-gameplay-learning-synthesis.md`
- `docs/research/terminal-velocity-coordination-topology.md`
- `docs/research/2026-06-08-terminal-velocity-topology-implementation-manifest.md`

External source observations rechecked live on 2026-06-08:

- Voyager README: open-ended LLM embodied agent with automatic curriculum, executable skill library, environment feedback, execution-error repair, and self-verification.
- Airtest README: cross-platform UI automation for games/apps with image recognition, simulated input, assertions, command-line/Python API runs, HTML reports, and screen recording.
- Poco README: cross-engine UI automation using runtime UI hierarchy access; Unity/cocos/native examples include element lookup, actions, text assertions, and hierarchy viewing.
- Stable-Retro README: turns classic games into Gymnasium environments; integrations include memory locations, reward functions, episode end conditions, savestates, and ROM hashes.
- Wuji README: automatic online combat-game testing using multi-objective evolutionary algorithm plus deep reinforcement learning to explore state and discover bugs.
- Tencent GAutomator README: mobile-game test automation through engine elements/GameObjects; robust against resolution/UI visual drift when engine object access exists.
- BrowserGym README: Gymnasium-style benchmark/task harness for browser agents; task classes, benchmarks, agent/evaluator split, and run APIs.
- LMGame/GamingAgent README and arXiv `2505.15146`: standardized interactive gaming environments, VLM/LLM gaming agents, unified Gym-style API, lightweight perception/memory scaffolds; direct LLM-in-game evaluation is brittle because of vision perception, prompt sensitivity, and contamination risks.
- TITAN arXiv `2509.22170`: LLM-driven MMORPG testing with state abstraction, action prioritization/regulation, long-horizon trace memory and reflective correction, and diagnostic bug oracles.
- MIMIC-Py arXiv `2604.07752`: reusable automated game-testing tool that decouples planning, execution, memory, and game-specific logic; exposes personality/config traits for behavioral diversity and supports API or synthesized-code interaction.

## Deep-dive conclusions

### 1. Worker value is in structured loops, not broad unattended play

The common pattern across Voyager, TITAN, BrowserGym, Stable-Retro, and MIMIC-Py is a bounded loop:

1. define a task/curriculum item;
2. observe state through a stable schema;
3. choose from regulated/allowed actions;
4. execute one short macro or command;
5. validate with a predicate/oracle;
6. record trace/failure artifacts;
7. promote, revise, or discard the macro.

For Terminal Velocity workers, this means the first application is **worker-ready scenario/evaluator lanes**, not a single large autonomous EV player. A worker should own one curriculum item or source-mined lane and return a compact evidence packet.

### 2. Prefer semantic Godot probes over pixels when the engine is ours

Poco and GAutomator are valuable because engine hierarchy/GameObject access avoids brittle screenshot matching. Terminal Velocity can implement an even cleaner Godot-side equivalent: JSON state, named UI/control actions, scenario fixtures, and event logs.

Use screen/capture automation only when testing original EV Classic/Basilisk, when the target has no semantic API, or when visual layout itself is the question.

### 3. Basilisk is a capture/input oracle, not a broad training environment

Stable-Retro's useful transferable pattern is not “use RL now”; it is the requirement for named state, restore commands, memory/state variables, rewards, done conditions, and ROM/save integrity checks. Until Basilisk lanes have verified pilot/window/input/capture/restore records for the exact question, workers should not run long mutating Basilisk play.

Short accelerated Basilisk traces are high-value for UI/state-transition calibration. If Basilisk becomes flaky, debugging/stabilizing the lane is itself priority acceleration work.

### 4. Failure packets must be typed

Airtest reports/screen recordings, BrowserGym artifacts, and TITAN diagnostic oracles all point to the same worker rule: a failing run is useful only if it says what kind of failure it is.

Terminal Velocity failure packet types:

- `automation-flake`: input delivery, focus, capture, timing, OCR/vision, or restore issue.
- `TV-bug`: Terminal Velocity behavior violates its scenario/source-labeled expected result.
- `source-gap`: worker cannot determine expected behavior from current sources.
- `fidelity-pending`: Terminal Velocity behavior is plausible/scaffolded but needs EV Classic/runtime/source confirmation.
- `worker-contract-breach`: worker touched unclaimed files, skipped verifier, or returned unverifiable claims.

### 5. Workers need action regulation, not just goals

TITAN's action regulation and existing TV safety rules translate into explicit worker allowed/forbidden action sets.

For TV workers:

- Allowed: inspect assigned sources; edit assigned files; run lane verifier; write evidence packet; create generated artifacts only in the claimed path.
- Forbidden unless explicitly gated: external publication beyond normal integration-owner push, cron/watchdog mutation, raw proprietary asset publication, destructive original-EV/save actions, Strict Play, force-push/history rewrite, unclaimed repo surfaces.

### 6. Reusable macro libraries should be promoted like code

Voyager's skill library pattern applies if macros/scripts have preconditions, postconditions, verifier, failure modes, and a promotion rule. Do not preserve random successful transcripts as “skills.” Promote only after repeatable verification.

Suggested Terminal Velocity macro/library surfaces:

- `tools/run_gameplay_scenarios.py` and scenario fixtures for deterministic Godot/native probes.
- `docs/research/playtest-runs/` for per-run evidence packets.
- Future explicit macro directory only after a second reusable macro exists and the interface is stable.

## Worker lane types to use now

### Lane type A: read-only source scout

Use when deepening source evidence without code mutation.

- Input: source list, question, expected output schema.
- Writes: one evidence packet under `docs/research/` or no files if delegated as a report.
- Verifier: source URLs/paths and quoted observations are checkable.
- Good tasks: compare external automation frameworks; mine EV-family docs; identify candidate scenario fields.
- Not allowed: direct code changes or fidelity promotion.

### Lane type B: semantic Godot probe worker

Use for Terminal Velocity scenario/evaluator growth.

- Input: one curriculum item and state/action schema.
- Writes: claimed scenario/test/tool files plus optional playtest-run packet.
- Verifier: focused scenario command, plus all-scenario run if runtime-facing behavior changed.
- Good tasks: mission cargo reservation scenario, route/jump/land scenario, service scan scenario, help-log objective hints.
- Label output: `terminal-velocity-observed`, not EV Classic proof.

### Lane type C: capture-driven Basilisk worker

Use only for bounded original-runtime UI/state-transition questions.

- Input: Basilisk lane ID, pilot/save/restore state, window/input target, capture directory, exact evidence question.
- Writes: capture packet and observation doc/backlog update only.
- Verifier: before/after screenshots or trace log; no destructive state unless gated.
- Good tasks: exact route-selection sequence, landing/refuel UI flow, mission acceptance modal flow.
- Stop on: focus/input/capture ambiguity, freeze/flakiness, save mutation risk, or unexpected modal.

### Lane type D: static/source-mined semantic promotion worker

Use for decoded/manual-backed data promotion.

- Input: one EV Classic resource field family and target manifest/model surface.
- Writes: extractor/data/tests/docs surfaces named in manifest.
- Verifier: deterministic extractor output, JSON parse, focused native tests, scenario suite if runtime-facing data changed.
- Good tasks: topology coordinates/links, service matrix, commodity metadata, mission field families.
- Label output: `decoded-resource-backed` or `manual/docs-backed`.

### Lane type E: mutation-gated experiment worker

Use sparingly for autoresearch/RL/evolutionary optimization-style loops.

Required before launch:

- objective and trusted metric;
- baseline;
- mutable surface;
- trusted surface that cannot be edited by the worker;
- fixed run budget;
- experiment log path;
- keep/revert rule;
- integration-owner review gate.

Do not use this lane for normal source-aligned implementation.

## Worker packet template

Every automated-gameplay worker packet should include:

```text
Worker id:
Lane type: read-only-source-scout | semantic-godot-probe | capture-driven-basilisk | static-source-mined-promotion | mutation-gated-experiment
Question / curriculum item:
Source/fidelity label:
Claimed writable surfaces:
Read-only/trusted surfaces:
Starting state / restore method:
Allowed actions:
Forbidden actions:
Action or macro source:
Observation schema:
Success predicate / metric:
Failure packet path:
Verifier command(s):
Promotion rule:
Budget / stop condition:
Keep/revert rule:
Handoff requirements:
```

## Immediate application to existing worker burst

Apply the source findings to the current topology manifest as follows:

1. Keep lanes A-D as data/source-promotion lanes; they are good worker targets because each has bounded writable surfaces and verifiers.
2. Split current Lane E into two sublanes when activating workers:
   - `E1 semantic-godot-probe`: deterministic scenario/evaluator packet from structured state/log output.
   - `E2 capture-driven-basilisk-scout`: only if there is a named EV Classic UI/state-transition question with restore/capture records.
3. Do not put long autonomous gameplay or RL inside Lane E yet. Create Lane type E only after objective/metric/budget/keep rules exist.
4. Make failure packets mandatory for all automated gameplay workers, even when no code changes.
5. For any worker-submitted macro or “learned skill,” require at least one verifier run and one documented failure mode before it becomes reusable process.

## Recommended next worker-ready slice

Best first worker application: `semantic-godot-probe` for the safe merchant curriculum.

- Curriculum item: route/jump/land/refuel or mission cargo reservation, whichever has the clearest existing model hooks.
- Starting state: deterministic Terminal Velocity scenario fixture.
- Observation schema: JSON/log state first; no screenshots unless visual UI is the claim.
- Success predicate: exact state deltas and no destructive/legal gate.
- Verifier: focused scenario command plus `python3 tools/run_gameplay_scenarios.py --all --pretty` after integration.
- Promotion: if the probe catches regressions or enables a visible scenario, convert it into a permanent regression/evaluator entry.

Second worker application: `capture-driven-basilisk-scout` for exact EV Classic route-selection/jump sequence, but only after naming one Basilisk lane's pilot/save/restore/window/input/capture records. Run at Basilisk K / 2x+ for exploration when safe; slow/1x only for contradictions or promotion-sensitive timing/feel claims.
