# Long-running game-development harness audit

Date: 2026-06-02

Purpose: reevaluate the Terminal Velocity / Loki Game setup as one instance of a general Hermes capability: any long-running task should continue across local safe slices, tool caps, context windows, platforms, profiles, and idle periods until a real gate or done condition is reached.

Generic capability surfaces:
- Active/default skill copy: `/home/bh/.hermes/skills/autonomous-ai-agents/long-running-task-harness/`.
- Shared profile skill copy: `/home/bh/.hermes/shared-skills/autonomous-ai-agents/long-running-task-harness/`. Profiles must opt in via `skills.external_dirs` to load the shared copy.

## Desired operating model

Terminal Velocity game development should be treated as a durable project workflow using the generic long-running task harness, not as a special game-only process or a single chat turn. A completed local slice is a checkpoint. It is not a stop condition unless one of these is true:

- a real gate is reached: push/PR/publication, credential/provider/config change, gateway/restart/supervision, destructive EV Classic play, unattended gameplay automation, Strict Play, or external/social output;
- no safe local backlog slice remains after live inspection;
- tool/time/context budget is near exhaustion and the next action would risk losing state instead of checkpointing;
- the worktree is too unsafe/ambiguous to continue without stabilization or user decision.

When a cap is near, the system should write a checkpoint/resume artifact and queue/wake the next run. It should not send a vague status report and abandon the task.

## Current setup evidence

### Repo and continuation artifacts

- Repo: `/home/bh/workspaces/loki/terminal-velocity`.
- Existing continuation prompt: `docs/prompts/terminal-velocity-continuation-prompt.md`.
- Existing process-remediation checklist: `docs/checklists/agent-continuation-process-failure-remediation.md`.
- Existing linter: `tools/check_agent_continuation_artifacts.py`.
- Verification run after this audit:
  - command: `python3 tools/check_agent_continuation_artifacts.py --repo . --profile-home /home/bh/.hermes/profiles/loki-game`
  - result: `CONTINUATION ARTIFACT CHECK OK`.

### Profiles and routing

- `terminal-velocity` profile exists and has `terminal.cwd: /home/bh/workspaces/loki/terminal-velocity`.
- `loki-game` profile exists and is currently running as a gateway process under tmux.
- `terminal-velocity` profile is not currently running as a gateway process.
- Both `terminal-velocity` and `loki-game` configs include `skills.external_dirs: ['/home/bh/.hermes/shared-skills']`.
- `loki-game` has Terminal Velocity / EV Classic profile-local gameplay skills such as:
  - `gaming/ev-terminal-velocity-play`
  - `gaming/ev-classic-basilisk-observation`
  - `gaming/terminal-velocity-provenance`
- `terminal-velocity` profile appears to have broad generic skills but lacks those Loki Game profile-local EV/Terminal Velocity skills. That means repo-focused `terminal-velocity` runs may miss project-specific play/fidelity procedures unless those skills are promoted/shared or explicitly copied.

### Runtime/durable systems currently available

- Hermes supports `cronjob` with `workdir`, `profile`, `skills`, `context_from`, and `no_agent` script modes.
- Hermes supports background `terminal(..., background=True, notify_on_complete=True)` for bounded long commands, and `process` for polling/logs.
- Hermes supports durable Kanban board/dispatcher in the codebase/skill docs, but no Terminal Velocity board/run was verified in this pass.
- Hermes skill text references a `long_task` tool as the ideal durable envelope, but source search found only risk classification and textual mentions, not a registered usable tool in this checkout. Treat `long_task` as missing/not currently operational until implemented and exposed.
- Existing cron portfolio has multiple Loki research/maintenance jobs, but no verified Terminal Velocity long-running development job was listed.

## External-source cross-check

These are technique/process sources, not Terminal Velocity feature requirements.

- Anthropic, **Effective harnesses for long-running agents**: frames the problem as multi-session work across context windows; recommends an initializer and repeated coding-agent sessions that make incremental progress while leaving clear artifacts and a clean mergeable state.
  - Implication: Terminal Velocity needs an initializer/runner/checkpoint loop, not only a stored prompt.
- Google Developers Blog, **Build Long-running AI agents that pause, resume, and never lose context with ADK**: emphasizes durable memory schemas, event-driven dormancy gates, multi-agent delegation, and pause/resume for human approvals and idle waits.
  - Implication: user approval and tool caps should become explicit dormancy gates/checkpoints.
- Microsoft Learn, **Durable Task for AI agents**: identifies long-running stateful sessions, expensive token consumption, infrastructure interruptions, checkpointing, and resume from failure as production issues solved by durable execution.
  - Implication: Terminal Velocity needs explicit persisted workflow state and recovery semantics; chat memory is not enough.
- LangGraph persistence docs/search result: checkpointed graph state at every step enables human-in-the-loop workflows, time travel debugging, and fault-tolerant execution.
  - Implication: checkpoint each slice and make gate/resume state inspectable.
- Harbor ATIF trajectory RFC: trajectories should log user/agent/tool/system steps, subagents, context-management boundaries, environment resets, and checkpoint creation.
  - Implication: Terminal Velocity should keep JSONL/trajectory-like records for autonomous runs, not only prose reports.
- Voyager / MineDojo: open-ended embodied agent pattern uses automatic curriculum, a skill library, iterative prompting, execution errors, environment feedback, and self-verification.
  - Implication: game development and EV-play learning should maintain a curriculum + verified skill library.
- Go-Explore: archive interesting states, return to promising states, then explore outward for long-horizon hard-exploration games.
  - Implication: EV Classic learning should archive saves/systems/routes/missions and explore from checkpoints instead of linear ad hoc play.

## Deficiencies found

1. **No verified durable task envelope for Terminal Velocity game development.**
   - Current artifacts say “continue,” but there is no verified `long_task` tool or Terminal Velocity cron/Kanban runner that owns the whole mission to completion.

2. **Tool caps are handled mostly by prose, not runtime state.**
   - The continuation prompt says caps are per-run budgets, but there is no machine-checked near-cap checkpoint/wakeup record tied to the next run.

3. **Shared skills are partially fixed but still fragile.**
   - Profiles now point at `/home/bh/.hermes/shared-skills`, and the shared `source-and-fidelity` skill was patched during this audit to trigger on stored Terminal Velocity prompt/artifact/handoff language.
   - Remaining issue: some Terminal Velocity-specific game skills still live only under `loki-game`, so `terminal-velocity` profile runs may lack project-specific procedures.

4. **Linter initially assumed profile-local skills only.**
   - `tools/check_agent_continuation_artifacts.py` failed on `skills/software-development/source-and-fidelity/SKILL.md` despite shared skill configuration.
   - Fixed locally in this pass: it now accepts an optional `--shared-skills-home` and checks shared skills when a profile-local skill is missing.

5. **Gateway/profile identity is still overloaded.**
   - Terminal Velocity is the game project/repo. `loki-game` is operational routing for game work. A separate `terminal-velocity` gateway/chat is not inherently required.
   - But if game development is meant to run autonomously to completion, it needs a durable operational owner. Today the verified running owner is `loki-game`; the repo-focused `terminal-velocity` profile is configured but not running.

6. **No source-backed autonomous development cadence is wired to the game repo.**
   - Existing recurring research jobs cover Loki/Hermes/autoresearch broadly, not a Terminal Velocity completion runner.

7. **Game-learning loop exists as research design, not as a durable runner.**
   - `docs/research/ev-gameplay-external-demo-and-autoresearch-plan.md` defines a JSONL scoring loop and approval gates.
   - It explicitly gates recurring cron/background autoresearch, unattended EV operation, Strict Play, combat-risk testing on reusable pilots, Hermes config/gateway changes, and external capture publication.

## Recommended target architecture

Use the generic long-running task harness, then specialize it per domain/project:

1. **Shared capability layer** — safe local skill/artifact surface, now created.
   - Active/default reusable skill path: `/home/bh/.hermes/skills/autonomous-ai-agents/long-running-task-harness/SKILL.md`.
   - Shared profile reusable skill path: `/home/bh/.hermes/shared-skills/autonomous-ai-agents/long-running-task-harness/SKILL.md`.
   - Templates: `templates/task-ledger.json` and `templates/events.jsonl`.
   - Source-backed pattern notes: `references/source-backed-patterns.md`.
   - This layer applies to software development, research, audits, operations, content pipelines, data work, and games.
   - Caveat: default profile currently has `skills.external_dirs: []`, so the active/default copy is needed unless/until shared-skill opt-in is approved/configured.

2. **Project ledger layer** — safe now.
   - Add a run ledger under `.hermes/long-running/terminal-velocity/` or `docs/checklists/` with fields: objective, current milestone, backlog slice queue, active gate, cap state, last verified command, artifacts touched, next wakeup prompt, and done condition.
   - Store per-run JSONL events: `slice_started`, `artifact_read`, `skill_loaded`, `edit`, `verification`, `gate_reached`, `checkpoint_written`, `resume_queued`, `slice_completed`.

3. **Profile/skill layer** — safe local audit; mutation gated if broad profile sync is requested.
   - Promote/copy only the reusable Terminal Velocity game skills that `terminal-velocity` profile actually needs, or keep `loki-game` as the single operational owner and stop treating `terminal-velocity` profile as a runner.
   - Keep source/fidelity, artifact-governance, bounded-autoresearch, game-prototyping, EV Classic observation, and Terminal Velocity provenance consistently available to the chosen runner.

4. **Durable runner layer** — approval-gated.
   - Preferred near-term: a `cronjob` or Kanban task that runs with `profile: loki-game` or `profile: terminal-velocity`, `workdir: /home/bh/workspaces/loki/terminal-velocity`, and a self-contained prompt that reads the ledger, does the next safe local slice, verifies, writes checkpoint, and either continues/queues or records a real gate.
   - Better long-term: implement/expose the missing `long_task` tool hinted by the Hermes skill docs so tasks can checkpoint/gate/complete in a first-class store instead of ad hoc docs.

## Gates

Do not proceed without explicit approval for:

- starting or changing a recurring Terminal Velocity cron/background/autonomous runner;
- starting/stopping/restarting `loki-game` or `terminal-velocity` gateways;
- broad skill/profile propagation outside the shared-skill patch already made;
- pushing, PR creation, merge/rebase, or external publication;
- unattended EV Classic play, Strict Play, destructive tests, or risky combat/piracy/privateering on reusable pilots;
- provider/credential/config changes.

## Safe next local actions

1. Create a minimal long-running task ledger schema and first checkpoint file for Terminal Velocity.
2. Audit exactly which `loki-game` Terminal Velocity skills should be promoted to shared skills versus left profile-local.
3. Add a second linter/check that fails if the chosen runner profile cannot load the required skills from profile-local or shared skill roots.
4. Draft, but do not schedule, a self-contained cron/Kanban runner prompt for user approval.
5. Search Hermes source for the implied `long_task` tool and either implement it or remove the misleading skill text. Current evidence says it is not registered as a usable tool.

## Changes made in this audit

- Created generic active/default capability skill: `/home/bh/.hermes/skills/autonomous-ai-agents/long-running-task-harness/SKILL.md`.
- Created generic shared capability skill for opted-in profiles: `/home/bh/.hermes/shared-skills/autonomous-ai-agents/long-running-task-harness/SKILL.md`.
- Added reusable generic templates in both copies: `templates/task-ledger.json` and `templates/events.jsonl`.
- Added generic source-backed pattern notes in both copies: `references/source-backed-patterns.md`.
- Patched `/home/bh/workspaces/loki/terminal-velocity/tools/check_agent_continuation_artifacts.py` to honor `/home/bh/.hermes/shared-skills` when profile-local safeguards are intentionally shared.
- Patched `/home/bh/.hermes/shared-skills/software-development/source-and-fidelity/SKILL.md` so stored Terminal Velocity prompt/artifact/handoff requests trigger source-and-fidelity.
- Created this durable audit artifact.

## Verification

- `python3 tools/check_agent_continuation_artifacts.py --repo . --profile-home /home/bh/.hermes/profiles/loki-game` -> `CONTINUATION ARTIFACT CHECK OK`.
- Generic long-running-task template JSON parses with `python3 -m json.tool`.
- Generic long-running-task event template parses as JSONL.
- Readback verified the generic shared skill and Terminal Velocity audit cross-link.
- Readback of shared `source-and-fidelity` showed the new trigger line.
- Live inspection found `skills.external_dirs: ['/home/bh/.hermes/shared-skills']` for both `terminal-velocity` and `loki-game`.
