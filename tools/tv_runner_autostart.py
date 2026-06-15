#!/usr/bin/env python3
"""Script-only autostart watchdog for the Terminal Velocity Kanban runner.

This is intentionally narrow:
- no feature implementation;
- no git commit/push/rewrite;
- no gateway/provider/config restart;
- dispatch one ready TV Kanban task when the lane is idle;
- seed exactly one continuation task when the lane is idle and clean.

stdout is reserved for material actions/problems so a no-agent cron job can stay
quiet during healthy ticks.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/bh/workspaces/loki/terminal-velocity")
BOARD = "terminal-velocity"
ASSIGNEE = "terminal-velocity"
PROFILE_ARGS = ["hermes", "-p", "loki-game"]
STATE_PATH = Path("/home/bh/.hermes/profiles/loki-game/cron/tv_runner_autostart_state.json")
PROFILE_SKILLS_ROOT = Path("/home/bh/.hermes/profiles/loki-game/skills")
REQUESTED_CONTINUATION_SKILLS = (
    "long-running-task-harness",
    "source-and-fidelity",
    "artifact-governance",
)


def run(cmd: list[str], *, cwd: Path | None = None, timeout: int = 45) -> str:
    return subprocess.check_output(
        cmd,
        cwd=str(cwd) if cwd else None,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
    )


def run_checked(cmd: list[str], *, cwd: Path | None = None, timeout: int = 45) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode(errors="replace")
        return 124, output + f"\ncommand timed out after {timeout}s"
    return completed.returncode, completed.stdout


def git_status_lines() -> list[str]:
    return run(["git", "status", "--short", "--branch"], cwd=REPO, timeout=10).splitlines()


def git_dirty() -> bool:
    lines = git_status_lines()
    return any(line and not line.startswith("## ") for line in lines)


def git_head() -> str:
    return run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, timeout=10).strip()


def git_status_summary() -> str:
    return "; ".join(git_status_lines()[:12])


def load_state() -> dict:
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return {}


def save_state(**updates: object) -> None:
    state = load_state()
    state.update(updates)
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def board_tasks() -> list[dict]:
    code, raw = run_checked(PROFILE_ARGS + ["kanban", "--board", BOARD, "list", "--json"], timeout=60)
    if code != 0:
        raise RuntimeError(f"kanban list failed with exit {code}: {raw.strip()}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        excerpt = raw.strip().splitlines()[0] if raw.strip() else "<empty output>"
        raise RuntimeError(f"kanban list --json returned non-JSON output: {excerpt}") from exc
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("tasks"), list):
        return data["tasks"]
    raise RuntimeError("unexpected kanban list --json shape")


def assignee_tasks(tasks: list[dict], status: str) -> list[dict]:
    return [t for t in tasks if t.get("assignee") == ASSIGNEE and t.get("status") == status]


def dispatch(dry_run: bool) -> str:
    if dry_run:
        return "dry-run-dispatch"
    return run(
        PROFILE_ARGS + ["kanban", "--board", BOARD, "dispatch", "--max", "1"],
        timeout=60,
    ).strip()


def pre_dispatch_preflight(dry_run: bool) -> str:
    if dry_run:
        return "dry-run-runner-preflight"
    code, raw = run_checked(["python3", "tools/backlog_dispatch_index.py", "runner-preflight"], cwd=REPO, timeout=90)
    if code != 0:
        raise RuntimeError(f"runner-preflight failed with exit {code}: {raw.strip()}")
    return raw.strip()


def recovery_preflight(tasks: list[dict]) -> tuple[int, str]:
    """Run the deterministic idle-dirty recovery classifier with current Kanban state."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(tasks, handle)
        tasks_path = Path(handle.name)
    try:
        return run_checked(
            [
                "python3",
                "tools/tv_runner_recovery_preflight.py",
                "--repo",
                str(REPO),
                "--tasks-json",
                str(tasks_path),
            ],
            cwd=REPO,
            timeout=60,
        )
    finally:
        try:
            tasks_path.unlink()
        except FileNotFoundError:
            pass


def start_resume_preflight() -> tuple[int, dict]:
    code, raw = run_checked(
        ["python3", "tools/tv_runner_start_resume_preflight.py", "--startup-owner", "gateway_kanban_dispatcher"],
        cwd=REPO,
        timeout=60,
    )
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"start/resume preflight returned non-JSON output: {raw.strip()[:240]}") from exc
    return code, payload


def compact_preflight_result(payload: dict) -> dict:
    """Return the bounded start-protocol packet suitable for watchdog stdout."""
    if isinstance(payload.get("machine_result"), dict):
        return payload["machine_result"]
    topology = payload.get("topology") or {}
    blocked = payload.get("blocked_cards") or {}
    return {
        "safe_to_start": payload.get("safe_to_start"),
        "recommended_action": payload.get("recommended_action"),
        "explicit_gate": payload.get("explicit_gate"),
        "live_owner": topology.get("live_implementation_owner"),
        "repo_state": payload.get("repo_state"),
        "dirty_paths": payload.get("dirty_paths") or [],
        "blocked_handoffs": blocked.get("counts_by_class") or {},
        "heartbeat_or_task_id": None,
        "preflight_tier": payload.get("preflight_tier"),
        "escalations_run": payload.get("escalations_run") or [],
    }


def require_start_resume_safe(now: str) -> bool:
    try:
        code, payload = start_resume_preflight()
    except Exception as exc:
        save_state(last_problem="start_resume_preflight_failed", last_problem_at=now, last_active="")
        print(f"TV runner autostart blocked: start/resume preflight failed: {exc}")
        print("repo: " + git_status_summary())
        return False
    if code != 0 or payload.get("explicit_gate") is not None or not payload.get("safe_to_start"):
        save_state(
            last_problem="start_resume_preflight_blocked",
            last_problem_at=now,
            last_active="",
            last_start_resume_action=payload.get("recommended_action"),
        )
        print("TV runner autostart blocked: start/resume preflight blocked dispatch/seeding.")
        print(json.dumps(compact_preflight_result(payload), indent=2, sort_keys=True))
        print("repo: " + git_status_summary())
        return False
    return True


def target_profile_skill_names() -> set[str]:
    """Return skill names available in the active target Hermes profile."""
    if not PROFILE_SKILLS_ROOT.exists():
        return set()
    return {path.parent.name for path in PROFILE_SKILLS_ROOT.glob("**/SKILL.md")}


def continuation_skill_args() -> list[str]:
    available = target_profile_skill_names()
    args: list[str] = []
    for skill in REQUESTED_CONTINUATION_SKILLS:
        if skill in available:
            args.extend(["--skill", skill])
    return args


def continuation_body(head: str) -> str:
    return f"""Continue Terminal Velocity tv-spec implementation from current live repo state using the durable long-running task envelope.

Repo/workdir: {REPO}
Board/assignee: {BOARD} / {ASSIGNEE}
Base: current origin/main. Inspect live git state before editing; do not trust copied SHAs. Current local HEAD at autostart seed: {head}.

Required preflight:
- Read .hermes/long-running/tv-spec-implementation/task-ledger.json and tail .hermes/long-running/tv-spec-implementation/events.jsonl.
- Read docs/prompts/tv-spec-implementation-long-task-prompt.md and docs/research/tv-spec.md; use docs/checklists/ev-classic-fidelity-implementation-backlog.md for next work selection.
- Run python3 tools/backlog_dispatch_index.py runner-preflight before selecting work; fail closed on checker, verifier-map, playable-priority, or selected-item metadata errors.
- Run git fetch origin, git status --short --branch, inspect HEAD/origin/main before edits.
- Preserve runner-state artifacts; do not start/stop/restart live continuous runner, cron jobs, gateway/supervision, providers, accounts, or credential/config surfaces.

Continuation contract:
- This is a long-running autonomous loop. Do not stop for human review on verified safe-local TV code/data/docs changes.
- Implement one smallest coherent source-aligned safe local Terminal Velocity increment, then hand it off. In a shared worktree, do not batch adjacent increments or expand the dirty working set; adjacent-increment batching, checkpoint bundling, and successor seeding belong to the integration owner after handoff inspection.
- Each increment must include source/fidelity labels, deterministic verifier(s), and durable event/checkpoint updates when future behavior/state changes.
- Terminal Velocity/Godot logs are implementation evidence, not Classic truth; label scaffolds/pending Classic confirmations explicitly.
- A verified slice is an integration handoff boundary for shared-worktree workers. Do not create a successor continuation task from the worker when the worktree has unintegrated dirty handoff files; record the next action and let the autonomous integration owner checkpoint/bundle/push as appropriate, then seed the successor.
- If checkpoint publication is needed from a non-integrator worker, record push_ready with intended files, verifier output, and next action; the autonomous integration owner should resolve it. Human review is not a gate unless the task crosses an explicit risky/destructive/external/publication/credential/config boundary.
- Before blocking or completing as review-related, validate the closeout packet with python3 tools/tv_closeout_guard.py. Valid closeout classes are continue, push_ready, or blocked:*; generic review-required is invalid for verified safe-local TV code/data/docs work.
- If unable to create a successor, block with a self-contained handoff instead of silently finishing.

Verification defaults:
- Targeted sourced-system/static-topology tests for Lane A.
- python3 tools/extract_ev_system_semantics.py when extractor/model data touched.
- python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty when scenario packet touched.
- python3 tools/backlog_dispatch_index.py check when backlog dispatch fields touched.
- Broader native/Godot checks only at material checkpoint or touched-surface boundary.

Do not redo prior verified slices recorded in the ledger/events; continue from live state and the current backlog/priority/verifier maps.
"""


def create_continuation(dry_run: bool) -> str:
    head = git_head()
    if dry_run:
        return f"dry-run-create-tv-autostart-continuation-{head}"
    raw = run(
        PROFILE_ARGS
        + [
            "kanban",
            "--board",
            BOARD,
            "create",
            "Continue TV tv-spec autonomous loop after autostart watchdog",
            "--assignee",
            ASSIGNEE,
            "--workspace",
            f"dir:{REPO}",
            *continuation_skill_args(),
            "--max-runtime",
            "45m",
            "--idempotency-key",
            f"tv-autostart-continuation-{head}",
            "--body",
            continuation_body(head),
            "--json",
        ],
        timeout=60,
    )
    created = json.loads(raw)
    return str(created.get("id") or "").strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    now = datetime.now(timezone.utc).isoformat()
    try:
        tasks = board_tasks()
    except Exception as exc:
        save_state(last_problem="kanban_unavailable", last_problem_at=now, last_active="")
        print(f"TV runner autostart blocked: kanban state unavailable: {exc}")
        return 0
    running = assignee_tasks(tasks, "running")
    ready = assignee_tasks(tasks, "ready")
    blocked = assignee_tasks(tasks, "blocked")
    scheduled = assignee_tasks(tasks, "scheduled")

    if running:
        active = f"{running[0].get('id')} {running[0].get('title')}"
        state = load_state()
        if active != state.get("last_active"):
            save_state(last_active=active, last_ok_at=now)
            print(f"TV runner autostart status: running {active}")
            print("repo: " + git_status_summary())
        else:
            save_state(last_ok_at=now)
        return 0

    if ready:
        if not require_start_resume_safe(now):
            return 0
        try:
            pre_dispatch_preflight(args.dry_run)
        except Exception as exc:
            save_state(last_problem="runner_preflight_failed", last_problem_at=now, last_active="")
            print(f"TV runner autostart blocked: runner-preflight failed before dispatch: {exc}")
            print("repo: " + git_status_summary())
            return 0
        out = dispatch(args.dry_run)
        save_state(last_action="dispatch_ready", last_action_at=now, last_active="")
        print(f"TV runner autostart: dispatched ready task; ready_before={len(ready)} blocked_ignored={len(blocked)}")
        if out:
            print(out.splitlines()[-1])
        print("repo: " + git_status_summary())
        return 0

    if scheduled:
        save_state(last_ok_at=now, last_active="")
        return 0

    if git_dirty():
        code, recovery = recovery_preflight(tasks)
        save_state(last_problem="idle_dirty_repo", last_problem_at=now, last_active="", last_recovery_preflight_exit=code)
        print("TV runner autostart blocked: idle lane but repo has uncommitted work; recovery preflight classified the state before seeding new work.")
        print(recovery.strip())
        print("repo: " + git_status_summary())
        print(f"blocked_tasks_ignored={len(blocked)}")
        return 0

    try:
        if not require_start_resume_safe(now):
            return 0
        pre_dispatch_preflight(args.dry_run)
    except Exception as exc:
        save_state(last_problem="runner_preflight_failed", last_problem_at=now, last_active="")
        print(f"TV runner autostart blocked: runner-preflight failed before seeding continuation: {exc}")
        print("repo: " + git_status_summary())
        return 0

    created = create_continuation(args.dry_run)
    out = dispatch(args.dry_run)
    save_state(last_action="seed_and_dispatch", last_action_at=now, last_seeded_task=created, last_active="")
    print(f"TV runner autostart: seeded and dispatched continuation {created}; blocked_ignored={len(blocked)}")
    if out:
        print(out.splitlines()[-1])
    print("repo: " + git_status_summary())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
