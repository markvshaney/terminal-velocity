# Workflow cadence hill-climb autoresearch

Goal: continuously improve Loki's Terminal Velocity workflow toward faster proactive implementation while preserving real safety/fidelity gates.

Metric direction: higher is better.

Primary rubric, 0-10 per reviewed work segment:

- +2 proactive implementation: safe local next step was executed instead of merely recommended.
- +2 batching: related safe changes were grouped into coherent player-visible slices instead of micro-sliced.
- +2 proportional verification: targeted checks during development, full verification at meaningful commit boundary only.
- +1 durable preservation: durable memory/artifact/checklist/skill update made when the user explicitly requested it or when a reusable workflow lesson appeared.
- +1 low ritual overhead: avoided unnecessary planning, todo churn, doc churn, repeated full-suite runs, and repeated identical failed commands.
- +1 source/fidelity discipline: EV Classic truth vs Terminal Velocity scaffold boundary preserved.
- +1 gate discipline: real approval gates preserved for Strict Play, destructive original-EV tests, credentials/account/provider/gateway changes, external messages, publishing, pushes, and other irreversible/socially consequential actions.

Critical regressions:

- Mutates approval-gated state without explicit approval.
- Leaves a clearly safe local next action as a recommendation only.
- Stores a workflow correction only in chat when the user asked for durable preservation.
- Uses repeated no-state-change / identical failing commands without changing strategy.

Mutable surface for scheduled runs:

- This directory only: `.hermes/autoresearch/workflow-cadence-hillclimb/`.
- The existing workflow decision artifact may be patched only when the run finds a clear reusable cadence rule: `docs/decisions/2026-05-19-ev-classic-observation-to-implementation-workflow.md`.

Trusted/read-only surfaces:

- Recent session transcripts via `session_search`.
- Repository status, tests, and existing docs/checklists.
- User memory/profile and active Terminal Velocity preferences.

Keep/revert policy:

- Keep local artifact updates when they add specific evidence-backed workflow lessons, cases, or candidate improvements.
- Do not change game code, tests, cron topology, Hermes config, credentials, gateway, memory, skills, or external delivery targets from scheduled runs.
- Any proposed change outside the mutable surface becomes an approval item in `approval-queue.jsonl`.

Cadence/reporting:

- Quiet if no meaningful new evidence or improvement candidate is found.
- Report concise terminal summaries only when a new finding, durable artifact update, or approval-gated recommendation exists.
- Prefer one actionable next improvement over broad generic advice.

Artifacts:

- `findings.jsonl`: structured workflow findings and evidence.
- `experiments.jsonl`: candidate workflow improvements and keep/discard status.
- `approval-queue.jsonl`: exact approval-gated next steps, if any.
- `last-run.json`: run state.
