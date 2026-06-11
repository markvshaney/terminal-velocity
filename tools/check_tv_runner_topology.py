#!/usr/bin/env python3
"""Validate Terminal Velocity runner/control-plane ownership state.

The topology preflight derives current runtime truth from live surfaces first
(cron metadata, process registry, loop state, and profile config), then
reconciles the repo-local ledger as declared intent/checkpoint state. The
ledger is deliberately not treated as primary runtime truth because it may
contain stale gates from prior invocations.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Any

DEFAULT_REPO = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = Path("/home/bh/.hermes/profiles/loki-game")
REPO = Path(os.environ.get("TV_TOPOLOGY_REPO", DEFAULT_REPO))
PROFILE = Path(os.environ.get("TV_TOPOLOGY_PROFILE", DEFAULT_PROFILE))
LEDGER = REPO / ".hermes/long-running/tv-spec-implementation/task-ledger.json"
CRON_JOBS = PROFILE / "cron/jobs.json"
PROCESSES = PROFILE / "processes.json"
LOOP_STATE = PROFILE / "run/tv_kanban_continuous_loop_state.json"
CONFIG = PROFILE / "config.yaml"

ALLOWED_OWNERS = {
    "none_active",
    "direct_session",
    "continuous_kanban_runner",
    "gateway_kanban_dispatcher",
    "integration_owner",
}

TV_TERMS = ("terminal velocity", "tv-spec", "tv ", "loki gametv")
IMPLEMENTATION_TERMS = ("implementation", "repair", "coordinator", "dispatch", "watchdog")
PASSIVE_REPORTER_SCRIPTS = {"tv_slice_reporter.py"}
TERMINAL_JOB_STATES = {"completed", "complete", "done", "disabled", "paused", "removed"}
ACTIVE_KANBAN_STATUSES = {"running"}


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def gateway_dispatch_enabled(path: Path) -> bool:
    if not path.exists():
        return False
    in_kanban = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not raw.startswith((" ", "\t")) and stripped.endswith(":"):
            in_kanban = stripped == "kanban:"
            continue
        if in_kanban and stripped.startswith("dispatch_in_gateway:"):
            return stripped.split(":", 1)[1].strip().lower() == "true"
    return False


def is_tv_job(job: dict[str, Any]) -> bool:
    text = " ".join(
        str(job.get(k, ""))
        for k in ("id", "name", "prompt", "script", "deliver", "workdir")
    ).lower()
    return any(term in text for term in TV_TERMS)


def job_enabled(job: dict[str, Any]) -> bool:
    state = str(job.get("state", "")).lower()
    return bool(job.get("enabled")) or state == "scheduled"


def job_completed_repeat(job: dict[str, Any]) -> bool:
    repeat = job.get("repeat")
    if not isinstance(repeat, dict):
        return False
    times = repeat.get("times")
    completed = repeat.get("completed")
    return isinstance(times, int) and isinstance(completed, int) and times > 0 and completed >= times


def is_stale_bootstrap_job(job: dict[str, Any]) -> bool:
    text = " ".join(str(job.get(k, "")) for k in ("name", "prompt", "script")).lower()
    state = str(job.get("state", "")).lower()
    return "bootstrap" in text and (state in TERMINAL_JOB_STATES or job_completed_repeat(job) or not job_enabled(job))


def is_passive_reporter_job(job: dict[str, Any]) -> bool:
    script = str(job.get("script", "")).rsplit("/", 1)[-1]
    name = str(job.get("name", "")).lower()
    return bool(job.get("no_agent")) and script in PASSIVE_REPORTER_SCRIPTS and "reporter" in name


def add_issue(items: list[dict[str, str]], issue_type: str, message: str) -> None:
    items.append({"type": issue_type, "message": message})


def hermes_root_from_profile(profile: Path) -> Path:
    """Return the shared Hermes root for a profile-scoped Hermes home."""
    if profile.parent.name == "profiles":
        return profile.parent.parent
    return profile


def kanban_db_candidates(profile: Path) -> list[Path]:
    """Return plausible Hermes Kanban DB paths without mutating/initializing them."""
    root = hermes_root_from_profile(profile)
    candidates: list[Path] = []
    override = os.environ.get("HERMES_KANBAN_DB", "").strip()
    if override:
        candidates.append(Path(override).expanduser())
    current = root / "kanban/current"
    if current.exists():
        try:
            slug = current.read_text(encoding="utf-8").strip()
        except OSError:
            slug = ""
        if slug and slug != "default":
            candidates.append(root / "kanban/boards" / slug / "kanban.db")
    candidates.append(root / "kanban.db")
    boards_root = root / "kanban/boards"
    if boards_root.is_dir():
        for board_dir in sorted(boards_root.iterdir()):
            candidates.append(board_dir / "kanban.db")
    seen: set[str] = set()
    unique: list[Path] = []
    for path in candidates:
        key = str(path)
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def row_is_tv_related(row: dict[str, Any]) -> bool:
    text = " ".join(str(value or "") for value in row.values()).lower()
    explicit_terms = tuple(term for term in TV_TERMS if term != "tv ")
    return any(term in text for term in explicit_terms) or bool(
        re.search(r"(?<![a-z0-9-])tv(?:[-_ ]|$)", text)
    )


def inspect_kanban_db(path: Path, warnings: list[dict[str, str]]) -> bool:
    """Return True when a DB has an active TV Kanban task/run claim."""
    if not path.exists():
        return False
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row
    except sqlite3.Error as exc:
        add_issue(warnings, "kanban_inspection_error", f"could not open Kanban DB {path}: {exc}")
        return False
    try:
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        if "tasks" not in tables:
            return False
        task_columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
        select_columns = [col for col in ("id", "title", "body", "assignee", "status", "tenant", "workspace_path", "claim_lock", "worker_pid") if col in task_columns]
        if select_columns and "status" in task_columns:
            sql = f"SELECT {', '.join(select_columns)} FROM tasks WHERE status IN ({', '.join('?' for _ in ACTIVE_KANBAN_STATUSES)})"
            for row in conn.execute(sql, sorted(ACTIVE_KANBAN_STATUSES)):
                if row_is_tv_related(dict(row)):
                    return True
        if "task_runs" in tables:
            run_columns = {row[1] for row in conn.execute("PRAGMA table_info(task_runs)")}
            joinable = "task_id" in run_columns and "id" in task_columns
            if "status" in run_columns and joinable:
                # Include task title/body metadata in the text match so a run row
                # with an opaque task id can still be identified as TV work.
                fields = [
                    "r.id AS run_id",
                    "r.task_id AS run_task_id",
                    "r.status AS run_status",
                ]
                for col in ("profile", "metadata", "summary", "worker_pid", "claim_lock"):
                    if col in run_columns:
                        fields.append(f"r.{col} AS run_{col}")
                for col in ("id", "title", "body", "assignee", "tenant", "workspace_path", "status", "current_run_id"):
                    if col in task_columns:
                        fields.append(f"t.{col} AS task_{col}")
                sql = f"SELECT {', '.join(fields)} FROM task_runs r LEFT JOIN tasks t ON t.id = r.task_id WHERE r.status IN ({', '.join('?' for _ in ACTIVE_KANBAN_STATUSES)})"
                for row in conn.execute(sql, sorted(ACTIVE_KANBAN_STATUSES)):
                    row_dict = dict(row)
                    # task_runs can outlive their parent task's current state.
                    # Treat a run as live only when the parent task still says it
                    # is running, or when tasks.current_run_id points at this run.
                    task_status = str(row_dict.get("task_status") or "").lower()
                    current_run_id = row_dict.get("task_current_run_id")
                    run_id = row_dict.get("run_id")
                    run_is_current = task_status == "running" or (
                        current_run_id is not None and str(current_run_id) == str(run_id)
                    )
                    if run_is_current and row_is_tv_related(row_dict):
                        return True
    except sqlite3.Error as exc:
        add_issue(warnings, "kanban_inspection_error", f"could not inspect Kanban DB {path}: {exc}")
    finally:
        conn.close()
    return False


def infer_live_owners(
    jobs_doc: dict[str, Any],
    processes: Any,
    loop_state: dict[str, Any],
    profile: Path,
    warnings: list[dict[str, str]],
) -> set[str]:
    owners: set[str] = set()

    for job in jobs_doc.get("jobs", []):
        if not isinstance(job, dict) or not is_tv_job(job):
            continue
        if is_stale_bootstrap_job(job):
            add_issue(warnings, "stale_bootstrap_job_ignored", f"TV bootstrap cron job {job.get('id')} is completed/disabled and ignored")
            continue
        if not job_enabled(job):
            continue
        if is_passive_reporter_job(job):
            add_issue(warnings, "passive_reporter_ignored", f"TV cron job {job.get('id')} is no-agent script-only reporting and ignored as an implementation owner")
            continue
        job_text = " ".join(str(job.get(k, "")) for k in ("name", "prompt", "script")).lower()
        if not bool(job.get("no_agent")) or any(term in job_text for term in IMPLEMENTATION_TERMS):
            owners.add("cron_implementation_surface")

    for proc in processes if isinstance(processes, list) else []:
        proc_text = json.dumps(proc, sort_keys=True).lower()
        if "tv_kanban_continuous_loop.py" in proc_text or "tv_spec_continuous_runner.sh" in proc_text:
            owners.add("continuous_kanban_runner")

    if loop_state.get("last_state") == "running":
        owners.add("continuous_kanban_runner")

    for db_path in kanban_db_candidates(profile):
        if inspect_kanban_db(db_path, warnings):
            owners.add("gateway_kanban_dispatcher")
            break

    return owners


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--startup-owner",
        choices=sorted(ALLOWED_OWNERS),
        help="Owner this preflight is about to start. Adds stricter conflict checks.",
    )
    args = parser.parse_args()

    conflicts: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    ledger = read_json(LEDGER, {})
    runner_ownership = ledger.get("runner_ownership") or {}
    declared_owner = ledger.get("declared_owner", runner_ownership.get("implementation_owner"))

    if declared_owner is not None and declared_owner not in ALLOWED_OWNERS:
        add_issue(
            conflicts,
            "ledger_invalid",
            f"ledger runner_ownership.implementation_owner must be one of {sorted(ALLOWED_OWNERS)}; got {declared_owner!r}",
        )

    jobs_doc = read_json(CRON_JOBS, {"jobs": []})
    processes = read_json(PROCESSES, [])
    loop_state = read_json(LOOP_STATE, {})
    live_owners = infer_live_owners(jobs_doc, processes, loop_state, PROFILE, warnings)

    if "cron_implementation_surface" in live_owners:
        add_issue(
            conflicts,
            "active_owner_conflict",
            "enabled TV cron implementation/repair/dispatch surface is active",
        )

    concrete_live_owners = sorted(owner for owner in live_owners if owner != "cron_implementation_surface")
    if len(concrete_live_owners) > 1:
        add_issue(conflicts, "active_owner_conflict", f"multiple live implementation owners are active: {concrete_live_owners}")

    live_owner = concrete_live_owners[0] if concrete_live_owners else "none_active"
    startup_owner = args.startup_owner
    if startup_owner and live_owner != "none_active" and live_owner != startup_owner:
        add_issue(
            conflicts,
            "active_owner_conflict",
            f"startup owner {startup_owner!r} conflicts with live implementation owner {live_owner!r}",
        )

    ledger_status = str(ledger.get("status") or "").lower()
    ledger_declares_active_owner = ledger_status not in {"", "stopped_by_user", "stopped", "paused"}
    if declared_owner and declared_owner != live_owner and ledger_declares_active_owner:
        add_issue(
            warnings,
            "ledger_stale",
            f"ledger declared owner {declared_owner!r} does not match derived live owner {live_owner!r}",
        )
    if (
        startup_owner
        and declared_owner
        and declared_owner != startup_owner
        and live_owner == "none_active"
        and ledger_declares_active_owner
    ):
        add_issue(
            warnings,
            "ledger_stale",
            f"startup owner {startup_owner!r} differs from stale ledger owner {declared_owner!r}; update ledger intent after preflight",
        )
    active_gate = ledger.get("active_gate")
    if isinstance(active_gate, dict) and active_gate.get("type") == "topology_conflict" and not conflicts:
        add_issue(
            warnings,
            "ledger_stale",
            "ledger still records an old topology_conflict gate, but live topology has no active owner conflict",
        )

    gateway_enabled = gateway_dispatch_enabled(CONFIG)
    gateway_startup_selected = startup_owner == "gateway_kanban_dispatcher"
    if gateway_enabled and live_owner != "gateway_kanban_dispatcher" and gateway_startup_selected:
        add_issue(
            warnings,
            "gateway_global_enabled_warning",
            "gateway Kanban dispatch is globally enabled in profile config; no TV-specific live owner was derived from that setting alone",
        )
    elif gateway_enabled and declared_owner == "gateway_kanban_dispatcher":
        gateway_state = (runner_ownership.get("allowed_surfaces") or {}).get("gateway_kanban_dispatcher")
        if gateway_state not in {"owner", "active_owner", "declared_owner"}:
            add_issue(conflicts, "ledger_invalid", "gateway dispatch is ledger owner but allowed_surfaces does not mark it as owner")

    result = {
        "ok": not conflicts,
        "topology_conflict": bool(conflicts),
        "live_implementation_owner": live_owner,
        "declared_implementation_owner": declared_owner,
        "startup_owner": startup_owner,
        "conflict_types": sorted({item["type"] for item in conflicts}),
        "warning_types": sorted({item["type"] for item in warnings}),
        "conflicts": conflicts,
        "warnings": warnings,
        "problems": [item["message"] for item in conflicts],
        "paths": {
            "ledger": str(LEDGER),
            "cron_jobs": str(CRON_JOBS),
            "processes": str(PROCESSES),
            "loop_state": str(LOOP_STATE),
            "config": str(CONFIG),
            "kanban_db_candidates": [str(path) for path in kanban_db_candidates(PROFILE)],
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not conflicts else 2


if __name__ == "__main__":
    raise SystemExit(main())
