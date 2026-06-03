# Agent continuation process failure remediation checklist

Date: 2026-05-30

Purpose: turn the 6:19 p.m. and 6:23 p.m. process-failure posts into a concrete, step-by-step remediation checklist. This is about the agent workflow around Terminal Velocity continuation, not about EV Classic game mechanics.

## Source incidents

### 6:19 p.m. post: one-slice stop / incomplete continuation

Observed failures:

- The continuation rule already existed, but the agent did not apply it at the completed-slice boundary.
- The agent loaded only a partial skill set before acting.
- Older `required closeout` and generic inspected/changed/verified habits overrode the autonomous continuation rule.
- The agent treated `slice done` as `final report now` instead of `checkpoint and continue`.
- Prior corrections existed, so recurrence indicates a failed prevention system rather than a one-off misunderstanding.

### 6:23 p.m. post: stored-artifact prerequisite failure

Observed failures:

- The instruction referenced a stored artifact, but the agent did not first locate and read the exact artifact.
- The mandatory skill-selection reflex fired before artifact retrieval.
- `ev-terminal-velocity-play` metadata was too narrow, so it did not reliably trigger on `stored Terminal Velocity continuation prompt` wording.
- Always-injected memory partially masked the miss; memory was incorrectly treated as enough context.
- The mechanism existed but was not reached.

## Root invariants to enforce

- [ ] A user reference to a stored prompt/artifact/handoff is a prerequisite lookup, not optional context.
- [ ] The exact artifact must be read before executing instructions derived from it.
- [ ] Skills explicitly named by a stored artifact must be loaded before acting on that artifact.
- [ ] Memory may help locate/contextualize an artifact, but must not substitute for reading it.
- [ ] In Terminal Velocity continuation mode, a verified slice is a checkpoint, not a stop condition.
- [ ] Closeout/reporting happens only at a real gate, tool/time cap, unsafe dirty-worktree boundary, or proven no-safe-local-slice state.
- [ ] Push/PR/publication gates block external mutation only; they do not block further safe local work on top of an unpushed branch.

## Step-by-step remediation checklist

### Phase 1 — Detection and routing

- [x] Patch `ev-terminal-velocity-play` so it triggers on stored Terminal Velocity prompts/artifacts/handoffs.
- [x] Add explicit instruction to `ev-terminal-velocity-play`: locate and read the exact artifact before acting.
- [x] Add compact memory: when mulvray asks to follow a stored prompt/artifact, read the exact artifact before acting.
- [x] Add or update a project-level prompt/artifact lookup checklist that can be followed at the start of continuation runs.
- [x] Audit other TV-related skills for narrow trigger wording that could miss `continue`, `follow prompt`, `handoff`, or `stored artifact` instructions.
  - 2026-05-30 audit patched profile-local `source-and-fidelity`, `game-prototyping`, and `ev-classic-basilisk-observation` trigger wording so stored Terminal Velocity prompt/artifact/handoff requests route to artifact-first lookup and the named skill set.

### Phase 2 — Artifact-first execution

Start-of-continuation lookup checklist for every future `follow prompt` / `continue from stored artifact` request:

- [ ] Search for the artifact path if it is not already explicit.
- [ ] Read the artifact with line numbers.
- [ ] Extract required skills, repo path, verification commands, gates, and continuation loop from the artifact.
- [ ] Load every required skill named by the artifact before implementation.
- [ ] Inspect repo state after loading the required skills, not before applying the artifact rules.
- [ ] If artifact and memory conflict, treat the artifact as the operative task instructions and memory as background preference/context.

### Phase 3 — Slice-boundary gate check

After each verified safe local slice:

- [ ] Confirm whether a real gate exists: Strict Play, destructive original-EV test, credentials/accounts/provider/gateway, external message/publication, push/PR, live-browser mutation, or other irreversible/socially consequential action.
- [ ] Confirm whether a hard tool/time/budget cap is actually reached.
- [ ] Inspect dirty worktree safety: is the current work coherent enough to continue, or must it be stabilized first?
- [ ] Inspect the live backlog/docs for another safe local slice.
- [ ] If another safe local slice exists and no real gate/cap blocks it, start that slice instead of final-reporting.
- [ ] If stopping, name the exact gate/cap/no-safe-local-slice evidence.

### Phase 4 — Closeout-language repair

- [x] Search project docs/skills for `closeout`, `required closeout`, `inspected`, `changed`, `verified`, and similar report-boundary terms.
- [x] Patch wording that implies every completed slice is an autonomous-run ending.
- [x] Preserve reporting discipline, but subordinate it to the continuation rule: report only at real run end.
- [x] Where closeout remains necessary, add `only when a real gate/cap/no-safe-alternative has been reached`.
  - 2026-05-30 search found the risky `Required closeout` headings in `docs/decisions/2026-05-19-ev-classic-observation-to-implementation-workflow.md`; they now say required slice/candidate/observation evidence before the run can close, with closeout limited to real gate/cap/unsafe-dirty/no-safe-slice endings.

### Phase 5 — Regression prevention

- [x] Add a lightweight regression checklist to the stored continuation prompt or adjacent artifact:
  - artifact read?
  - all named skills loaded?
  - repo state inspected?
  - backlog inspected?
  - post-slice gate check run?
  - Added to both `docs/prompts/terminal-velocity-continuation-prompt.md` and profile-local `ev-terminal-velocity-play/references/terminal-velocity-autonomous-restart-prompt.md`.
- [x] Add a small textual linter for prompt artifacts that flags missing required-skill and closeout/continuation safeguards.
  - Script: `tools/check_agent_continuation_artifacts.py`
  - Verify with: `python3 tools/check_agent_continuation_artifacts.py --repo . --profile-home /home/bh/.hermes/profiles/loki-game`
- [ ] When the agent repeats any bug in this class, update this checklist with the new trigger and patch the highest-level reusable surface, not only memory/chat.

### Phase 6 — Runtime/durable-execution hardening options

These are optional follow-ups beyond prompt wording. They are not required to resume safe local Terminal Velocity work, but they are the next layer if the recurrence continues.

- [x] Add a tiny post-slice gate template to any stored continuation prompt before the closeout block: `real gate? cap? unsafe dirty state? no safe backlog slice?` If all answers are no, start the next slice.
- [x] Add the continuation-artifact linter to the normal verification bundle for process/prompt-only changes.
- [ ] Consider a Hermes-level/runtime check only if prompt/skill safeguards keep failing: a continuation-mode session state flag plus a pre-final-answer guard that detects `next safe local action` without a named stop condition. This would need code-level tests and activation through the Loki Game gateway/process boundary.
- [ ] If a run is likely to exceed a single tool/turn budget, create an explicit checkpoint/resume artifact rather than a final report; resumption should start from that artifact and re-run the slice-boundary gate check.
- [ ] Use `docs/checklists/long-running-game-development-harness-audit.md` as the current deficiency/improvement source for durable Terminal Velocity game-development continuation; update it when runtime/profile/skill architecture changes.

## Outside-source cross-check

External agent-framework references support moving beyond prose-only reminders when a workflow must survive long runs:

- LangGraph durable-execution/persistence docs emphasize checkpointed state, replay/resume, and durable writes around execution steps. Relevant implication here: continuation state and post-slice gates should be explicit artifacts/checkpoints, not only chat memory. Source: LangChain docs, `https://docs.langchain.com/oss/python/langgraph/persistence`; LangGraph project page, `https://github.com/langchain-ai/langgraph`.
- OpenAI Agents SDK materials expose guardrails, handoffs, sessions, tracing, and human-in-the-loop interruptions as first-class concepts. Relevant implication here: push/publication approval is a resumable interruption/gate, not a reason to abandon safe local work; guardrails should distinguish external mutation from local continuation. Source: OpenAI Agents SDK docs, `https://openai.github.io/openai-agents-python/`; HITL docs, `https://openai.github.io/openai-agents-python/human_in_the_loop/`.

## Current completed remediation from this incident

- [x] `ev-terminal-velocity-play` description expanded to include continuing development and stored Terminal Velocity continuation prompts.
- [x] `ev-terminal-velocity-play` `When to Use` expanded to include `follow`, `resume`, `continue`, or `find` stored Terminal Velocity prompts/artifacts/handoffs.
- [x] `ev-terminal-velocity-play` now says to locate/read the exact artifact before acting.
- [x] Persistent memory updated with the stored-artifact prerequisite rule.
- [x] `docs/decisions/2026-05-19-ev-classic-observation-to-implementation-workflow.md` already contains the one-slice stop recurrence analysis at checklist item 15.
- [x] `docs/decisions/2026-05-19-ev-classic-observation-to-implementation-workflow.md` cross-links this checklist at checklist item 16.

## Next safe local action

Execute the remaining unchecked remediation items above, starting with the project-level prompt/artifact lookup checklist and audit of TV-related skill trigger wording. After the process issue is tracked and the highest-risk triggers are patched, resume the pending Terminal Velocity implementation work from the dirty worktree.
