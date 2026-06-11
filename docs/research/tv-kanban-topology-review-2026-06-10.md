# TV Kanban topology review

Date: 2026-06-10
Source: Telegram / Loki Game post at approximately 10:54 p.m. local time, prompted by the question “Does TV spec have an idiosyncratic kanban setup as compared to the standard Hermes Kanban?” Source text preserved below from the assistant-visible post in this session.
Purpose: preserve and incorporate the sourced diagnosis/suggestions that TV spec has a project-specific Kanban/runner control-plane wrapper compared with standard Hermes Kanban. This is a process/rationale artifact, not an EV Classic fidelity source.
Status: durable project process artifact; execution policy remains in `docs/research/tv-spec.md`.

## Decision

TV spec does have an idiosyncratic Kanban setup relative to standard Hermes Kanban. The difference is not necessarily the Kanban board data model; it is the project-specific single-owner runner topology layered over Hermes Kanban.

Keep the TV-specific ownership layer for now, but make it narrower and more explicit:

1. Use actual Hermes Kanban board/claim state as the source for Kanban worker ownership.
2. Treat `continuous_kanban_runner` as a bespoke TV standalone runner using/dispatching Kanban, not as standard Hermes Kanban itself.
3. Keep `gateway_kanban_dispatcher` and `continuous_kanban_runner` mutually exclusive for implementation dispatch.
4. Extend `tools/check_tv_runner_topology.py` to inspect actual TV Kanban board claims/tasks, not only `kanban.dispatch_in_gateway`.
5. Rename docs wording from “continuous Kanban runner” to “TV standalone continuous runner using/dispatching Kanban” where precision matters; keep existing code identifiers only where they are literal process/owner names.

## Suggestions incorporated from the 10:54 p.m. post

The 10:54 p.m. post made five concrete suggestions. This review incorporates them as follows:

1. **Use Hermes Kanban board/claim state as source evidence.**
   - This artifact treats board claims/tasks/workers as the evidence for actual Kanban ownership.
   - `kanban.dispatch_in_gateway: true` alone is only profile configuration, not proof that the gateway is currently the TV implementation owner.

2. **Name the TV runner layer as a bespoke wrapper.**
   - `continuous_kanban_runner` is described here as a TV standalone continuous runner using/dispatching Kanban, not as standard Hermes Kanban itself.

3. **Keep dispatch owners mutually exclusive.**
   - `gateway_kanban_dispatcher` and `continuous_kanban_runner` remain mutually exclusive for TV implementation dispatch.

4. **Extend the topology checker toward live Kanban evidence.**
   - The first safe step targets read-only inspection of actual TV Kanban claims/tasks before classifying gateway dispatch as a live TV owner.

5. **Reduce naming confusion.**
   - Human-facing docs should prefer “TV standalone continuous runner using/dispatching Kanban” when discussing the concept.
   - Literal identifiers such as `continuous_kanban_runner`, `tv_kanban_continuous_loop.py`, and `tv_spec_continuous_runner.sh` remain unchanged unless a separate code rename is explicitly approved.

## Source post preserved

> Yes. **TV spec has an idiosyncratic Kanban setup compared with standard Hermes Kanban.** It is not just “use Hermes Kanban normally”; it adds a TV-specific runner/ownership layer around it.
>
> Evidence inspected:
>
> - `docs/research/tv-spec.md`
> - `docs/prompts/tv-spec-implementation-long-task-prompt.md`
> - `tools/check_tv_runner_topology.py`
> - `native_ev/tests/test_tv_spec_continuous_runner.py`
> - profile-local files under `/home/bh/.hermes/profiles/loki-game/`
>
> ## Standard Hermes Kanban
>
> From the Hermes skill/docs:
>
> - Kanban is a durable SQLite board.
> - Gateway dispatcher can claim/promote/reclaim tasks.
> - Workers get scoped env/tooling such as `HERMES_KANBAN_TASK`.
> - It is meant for multi-profile / multi-worker collaboration.
> - Dispatcher ownership is normally the Hermes Kanban subsystem, not a project-specific runner ledger.
>
> ## TV-specific/idiosyncratic layer
>
> TV adds these custom concepts:
>
> - `continuous_kanban_runner`
>   - a standalone explicitly-started continuous runner that owns implementation dispatch.
>   - Detected via custom process names:
>     - `tv_kanban_continuous_loop.py`
>     - `tv_spec_continuous_runner.sh`
>
> - `gateway_kanban_dispatcher`
>   - treated as a separate possible implementation owner from the standalone runner.
>
> - repo-local runner state:
>   - `.hermes/long-running/tv-spec-implementation/task-ledger.json`
>   - `.hermes/long-running/tv-spec-implementation/events.jsonl`
>   - `.hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER`
>   - `.hermes/long-running/tv-spec-implementation/continuous-runner/latest-summary.json`
>
- custom topology checker:
  - `tools/check_tv_runner_topology.py`
  - should be extended to classify proposed outcomes such as:
    - `active_owner_conflict`
    - `ledger_stale`
    - `passive_reporter_ignored`
    - `stale_bootstrap_job_ignored`
    - `gateway_global_enabled_warning`
  - These names are target behavior for the next checker patch, not a claim that the current checker already emits these exact categories.

> - custom single-owner policy:
>   - `direct_session`
>   - `continuous_kanban_runner`
>   - `gateway_kanban_dispatcher`
>   - `integration_owner`
>   - `none_active`
>
> That is beyond normal Hermes Kanban.
>
> ## Important distinction
>
> TV is not necessarily using a different Kanban *board model*. The idiosyncrasy is the **control-plane wrapper**:
>
> - Standard Hermes Kanban answers: “what task is claimed/spawned on the board?”
> - TV topology asks: “which implementation-dispatch owner is allowed to mutate/dispatch TV work at all?”
>
> That extra owner taxonomy is project-specific.
>
> ## Why this matters
>
> The setup can be valid, but it creates a real risk:
>
> - global Hermes gateway Kanban may be enabled;
> - a TV standalone continuous runner may also exist;
> - direct session/integration-owner work may happen;
> - cron reporter may exist;
> - old ledger state may be stale.
>
> So TV needs topology checks that standard Hermes Kanban alone would not need.
>
> ## Recommendation
>
> Keep the TV-specific ownership layer, but make it narrower:
>
> 1. Treat **Hermes Kanban board/claims** as the source for actual Kanban worker ownership.
> 2. Treat `continuous_kanban_runner` as a bespoke TV wrapper, not “standard Kanban.”
> 3. Keep `gateway_kanban_dispatcher` and `continuous_kanban_runner` mutually exclusive for implementation dispatch.
> 4. Extend `check_tv_runner_topology.py` to inspect actual TV Kanban board claims/tasks, not only `kanban.dispatch_in_gateway`.
> 5. Consider renaming docs wording from “continuous Kanban runner” to “TV standalone continuous runner using/dispatching Kanban” if it is causing confusion.
>
> Bottom line: **yes, TV spec is idiosyncratic relative to standard Hermes Kanban, mainly because it adds a project-specific single-owner runner topology on top of Hermes Kanban.**

## First safe step

Do a read-only/low-risk topology enhancement pass before any runner restart. This is an implementation checklist derived from the 10:54 p.m. suggestions, not authorization to restart or mutate gateway config:

1. Locate the Hermes Kanban board path and schema used by the `loki-game` profile.
2. Add read-only inspection to `tools/check_tv_runner_topology.py` for actual TV Kanban task claims/workers.
3. Classify `kanban.dispatch_in_gateway: true` as `gateway_global_enabled_warning` unless TV-specific claim/process evidence proves gateway ownership.
4. Add regression tests that distinguish:
   - global gateway dispatch enabled but no TV claim => warning only;
   - active TV Kanban worker claim => `gateway_kanban_dispatcher` live owner;
   - simultaneous gateway owner and standalone `continuous_kanban_runner` => `active_owner_conflict`.
5. Update human-facing docs/prompt wording to use “TV standalone continuous runner using/dispatching Kanban” where it clarifies the distinction from standard Hermes Kanban; do not rename literal code/process identifiers without a separate approved code-rename slice.
6. Do not remove `STOP_CONTINUOUS_RUNNER`, start a runner, mutate cron/gateway/provider config, or push as part of this artifact step.

## Current checker limitation

`tools/check_tv_runner_topology.py` is the intended enforcement surface, but the current checker must not be treated as already complete. The next patch should make live state primary: cron jobs, process registry, loop state, actual TV Kanban board claims/workers, profile config, and git state outrank ledger declarations. The ledger is a checkpoint/declaration to reconcile against live state, not live runtime truth by itself.

Until that patch exists, any `topology_conflict` derived only from ledger/config should be treated as a diagnosis candidate and rechecked against live state before restart, STOP removal, cron/config mutation, or publication.

## Relationship to existing process artifacts

- Extends `docs/research/tv-spec.md`, especially “Runner ownership and dispatch surfaces.”
- Uses `tools/check_tv_runner_topology.py` as the enforcement surface.
- Uses `native_ev/tests/test_tv_spec_continuous_runner.py` as the regression-test surface.
- Related prompt: `docs/prompts/tv-spec-implementation-long-task-prompt.md`.
