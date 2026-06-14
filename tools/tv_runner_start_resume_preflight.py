#!/usr/bin/env python3
"""Structured Terminal Velocity runner start/resume preflight.

This wrapper normalizes live repo/topology state into a machine-readable start
or resume decision. It is report-only: it does not seed, dispatch, clear stop
files, recover handoffs, commit, push, or mutate runner state.
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any

import tv_runner_recovery_preflight as recovery_preflight


DEFAULT_REPO = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = Path("/home/bh/.hermes/profiles/loki-game")
ALLOWED_OWNERS = {
    "none_active",
    "direct_session",
    "continuous_kanban_runner",
    "gateway_kanban_dispatcher",
    "integration_owner",
}


def run_checked(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None, timeout: int = 45) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode(errors="replace")
        return 124, output + f"\ncommand timed out after {timeout}s"
    return completed.returncode, completed.stdout


def git_state(repo: Path) -> tuple[str, list[str], str | None]:
    code, raw = run_checked(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, timeout=15)
    if code != 0:
        return "unknown", [], raw.strip() or "git status failed"
    paths: list[str] = []
    for line in raw.splitlines():
        if not line:
            continue
        path = line[3:] if len(line) > 3 else ""
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.append(path)
    return ("dirty" if paths else "clean"), sorted(paths), None


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_error": str(exc)}


def run_topology(repo: Path, profile: Path, startup_owner: str) -> tuple[int, dict[str, Any]]:
    env = os.environ.copy()
    env.update({
        "TV_TOPOLOGY_REPO": str(repo),
        "TV_TOPOLOGY_PROFILE": str(profile),
    })
    checker = repo / "tools/check_tv_runner_topology.py"
    if not checker.exists():
        checker = DEFAULT_REPO / "tools/check_tv_runner_topology.py"
    code, raw = run_checked(
        ["python3", str(checker), "--startup-owner", startup_owner],
        cwd=repo if repo.exists() else DEFAULT_REPO,
        env=env,
        timeout=60,
    )
    try:
        return code, json.loads(raw)
    except json.JSONDecodeError:
        return code or 1, {
            "ok": False,
            "topology_conflict": True,
            "live_implementation_owner": "unknown",
            "conflict_types": ["topology_unreadable"],
            "warning_types": [],
            "raw_output": raw,
        }


def stop_lock_state(repo: Path, profile: Path) -> dict[str, Any]:
    candidates = [
        repo / ".hermes/long-running/tv-spec-implementation/STOP_CONTINUOUS_RUNNER",
        repo / ".hermes/long-running/tv-spec-implementation/continuous-runner/STOP_CONTINUOUS_RUNNER",
        profile / "run/STOP_TV_CONTINUOUS_RUNNER",
    ]
    present = [str(path) for path in candidates if path.exists()]
    return {"status": "blocked" if present else "clear", "paths": present}


def watchdog_reporter_state(repo: Path, profile: Path) -> dict[str, Any]:
    autostart = read_json(profile / "run/tv_runner_autostart_state.json", {})
    reporter = read_json(profile / "run/tv_slice_reporter_state.json", {})
    runner_state = read_json(repo / ".hermes/long-running/tv-spec-implementation/continuous-runner/runner-state.json", {})
    return {
        "autostart_state": autostart,
        "reporter_state": reporter,
        "runner_state": runner_state,
    }


def capability_check(repo: Path) -> dict[str, Any]:
    names = [
        "tools/check_tv_runner_topology.py",
        "tools/tv_runner_recovery_preflight.py",
        "tools/tv_runner_autostart.py",
        "tools/tv_integration_lane.py",
    ]
    resolved: dict[str, str] = {}
    missing: list[str] = []
    for name in names:
        repo_path = repo / name
        default_path = DEFAULT_REPO / name
        if repo_path.exists():
            resolved[name] = str(repo_path)
        elif default_path.exists():
            resolved[name] = str(default_path)
        else:
            missing.append(str(repo_path))
    return {"status": "ok" if not missing else "missing", "missing": missing, "resolved": resolved}


def canonical_block_class(task: dict[str, Any], evidence_texts: list[str] | None = None) -> str:
    base_keys = ("title", "body", "status", "latest_summary", "result", "reason", "summary")
    values = [str(task.get(key) or "") for key in base_keys]
    if evidence_texts:
        values.extend(str(item or "") for item in evidence_texts)
    text = " ".join(values).lower()
    if "push_ready" in text or "push ready" in text:
        return "push_ready"
    if "unsafe_dirty_state" in text or "unsafe dirty" in text:
        return "unsafe_dirty_state"
    if "verifier_failed" in text or "verifier failed" in text:
        return "verifier_failed"
    if "explicit_human_gate" in text or "explicit human gate" in text:
        return "explicit_human_gate"
    if "review-required" in text or "review_required" in text or "review required" in text:
        return "review_required_process_bug"
    return "blocked:unclassified"


def _task_comments(conn: sqlite3.Connection, task_ids: list[str]) -> dict[str, list[dict[str, str]]]:
    if not task_ids:
        return {}
    comment_tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'task_comments'"
    ).fetchall()
    if not comment_tables:
        return {}
    columns = {row[1] for row in conn.execute("PRAGMA table_info(task_comments)")}
    if not {"task_id", "body"}.issubset(columns):
        return {}
    placeholders = ",".join("?" for _ in task_ids)
    rows = conn.execute(
        f"SELECT task_id, body FROM task_comments WHERE task_id IN ({placeholders}) ORDER BY id",
        task_ids,
    ).fetchall()
    comments: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        comments.setdefault(str(row["task_id"]), []).append({"body": str(row["body"] or "")})
    return comments


def _query_blocked_cards(db_path: Path) -> list[dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
        wanted = [
            column
            for column in ("id", "title", "body", "latest_summary", "assignee", "status", "tenant", "workspace_path")
            if column in columns
        ]
        if not {"id", "status"}.issubset(columns):
            return []
        rows = conn.execute(
            f"SELECT {', '.join(wanted)} FROM tasks WHERE status = ? ORDER BY id",
            ("blocked",),
        ).fetchall()
        task_ids = [str(row["id"]) for row in rows]
        comments_by_task = _task_comments(conn, task_ids)
    finally:
        conn.close()

    cards: list[dict[str, Any]] = []
    for row in rows:
        task = {key: row[key] for key in row.keys()}
        text = " ".join(str(task.get(key) or "") for key in ("title", "body", "latest_summary", "assignee", "tenant", "workspace_path")).lower()
        if "terminal-velocity" not in text and "tv" not in text:
            continue
        comments = comments_by_task.get(str(task.get("id"))) or []
        card = {
            "id": task.get("id"),
            "title": task.get("title"),
            "body": task.get("body"),
            "latest_summary": task.get("latest_summary"),
            "assignee": task.get("assignee"),
            "status": task.get("status"),
            "canonical_class": canonical_block_class(task, [comment.get("body", "") for comment in comments]),
        }
        if comments:
            card["comments"] = comments
        cards.append(card)
    return cards


def _query_handoff_candidates(db_path: Path) -> list[dict[str, Any]]:
    """Return Kanban tasks that may explain a dirty push-ready handoff.

    Blocked cards are only one durable surface. Normal workers can finish as
    ``done`` while leaving the push_ready evidence in latest_summary, comments,
    run metadata, and repo-local closeout packets. Dirty recovery needs those
    done candidates too; otherwise it sees an empty task set and misclassifies a
    verified handoff as generic unsafe dirt.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
        wanted = [
            column
            for column in (
                "id",
                "title",
                "body",
                "latest_summary",
                "assignee",
                "status",
                "tenant",
                "workspace_path",
                "created_at",
                "started_at",
                "updated_at",
            )
            if column in columns
        ]
        if not {"id", "status"}.issubset(columns):
            return []
        rows = conn.execute(
            f"SELECT {', '.join(wanted)} FROM tasks WHERE status IN (?, ?, ?) ORDER BY id",
            ("blocked", "done", "running"),
        ).fetchall()
        task_ids = [str(row["id"]) for row in rows]
        comments_by_task = _task_comments(conn, task_ids)
    finally:
        conn.close()

    candidates: list[dict[str, Any]] = []
    for row in rows:
        task = {key: row[key] for key in row.keys()}
        comments = comments_by_task.get(str(task.get("id"))) or []
        text_values = [str(task.get(key) or "") for key in ("title", "body", "latest_summary", "assignee", "tenant", "workspace_path")]
        text_values.extend(comment.get("body", "") for comment in comments)
        text = " ".join(text_values).lower()
        if "terminal-velocity" not in text and "tv" not in text:
            continue
        candidate = dict(task)
        if comments:
            candidate["comments"] = comments
        candidate["canonical_class"] = canonical_block_class(candidate, [comment.get("body", "") for comment in comments])
        candidates.append(candidate)
    return candidates


def blocked_cards(topology: dict[str, Any]) -> dict[str, Any]:
    candidates = [Path(path) for path in (topology.get("paths") or {}).get("kanban_db_candidates", [])]
    inspected: list[str] = []
    errors: list[dict[str, str]] = []
    cards: list[dict[str, Any]] = []
    seen: set[str] = set()
    for db_path in candidates:
        if not db_path.exists():
            continue
        inspected.append(str(db_path))
        try:
            for card in _query_blocked_cards(db_path):
                card_id = str(card.get("id") or "")
                if card_id in seen:
                    continue
                seen.add(card_id)
                cards.append(card)
        except sqlite3.Error as exc:
            errors.append({"path": str(db_path), "error": str(exc)})
    counts: dict[str, int] = {}
    for card in cards:
        klass = str(card.get("canonical_class"))
        counts[klass] = counts.get(klass, 0) + 1
    status = "inspected" if inspected else "no_db_found"
    if errors and not inspected:
        status = "error"
    return {
        "status": status,
        "source": "kanban_db",
        "kanban_db_candidates": [str(path) for path in candidates],
        "inspected_paths": inspected,
        "errors": errors,
        "cards": cards,
        "counts_by_class": counts,
    }


def handoff_candidates(topology: dict[str, Any]) -> dict[str, Any]:
    """Collect Kanban handoff evidence across blocked/running/done tasks."""
    candidates = [Path(path) for path in (topology.get("paths") or {}).get("kanban_db_candidates", [])]
    inspected: list[str] = []
    errors: list[dict[str, str]] = []
    tasks: list[dict[str, Any]] = []
    seen: set[str] = set()
    for db_path in candidates:
        if not db_path.exists():
            continue
        inspected.append(str(db_path))
        try:
            for task in _query_handoff_candidates(db_path):
                task_id = str(task.get("id") or "")
                if task_id in seen:
                    continue
                seen.add(task_id)
                tasks.append(task)
        except sqlite3.Error as exc:
            errors.append({"path": str(db_path), "error": str(exc)})
    counts: dict[str, int] = {}
    for task in tasks:
        task_status = str(task.get("status") or "unknown")
        counts[task_status] = counts.get(task_status, 0) + 1
    status = "inspected" if inspected else "no_db_found"
    if errors and not inspected:
        status = "error"
    return {
        "status": status,
        "source": "kanban_db",
        "kanban_db_candidates": [str(path) for path in candidates],
        "inspected_paths": inspected,
        "errors": errors,
        "tasks": tasks,
        "counts_by_status": counts,
    }


def compact_handoff_candidates(handoffs: dict[str, Any]) -> dict[str, Any]:
    """Return a report-safe summary without embedding historic task prose."""
    compact = {key: value for key, value in handoffs.items() if key != "tasks"}
    compact["tasks"] = [
        {
            "id": task.get("id"),
            "title": task.get("title"),
            "status": task.get("status"),
            "assignee": task.get("assignee"),
            "canonical_class": task.get("canonical_class"),
        }
        for task in (handoffs.get("tasks") or [])
    ]
    return compact


def blocked_card_start_gate(blocked: dict[str, Any]) -> tuple[str, str] | None:
    """Return the unresolved handoff/gate that must be resolved before idle start.

    Blocked cards are not an implementation owner, but several canonical classes
    represent unfinished integration/recovery work. When the lane is otherwise
    idle and clean, autostart must not seed or dispatch over those handoffs.
    """
    counts = blocked.get("counts_by_class") or {}
    priority = (
        ("push_ready", "recover_push_ready_handoff", "push_ready_integration_required"),
        ("review_required_process_bug", "normalize_blocked_gates", "gate_normalization_required"),
        ("verifier_failed", "rerun_focused_verifier", "verifier_failed"),
        ("unsafe_dirty_state", "blocked:unsafe_dirty_state", "unsafe_dirty_state"),
        ("explicit_human_gate", "blocked:explicit_human_gate", "explicit_human_gate"),
        ("blocked:unclassified", "blocked:unclassified_blocked_card", "unclassified_blocked_card"),
    )
    for klass, action, gate in priority:
        if int(counts.get(klass) or 0) > 0:
            return action, gate
    return None


def classify(repo: Path, profile: Path, startup_owner: str) -> dict[str, Any]:
    repo_state, dirty_paths, git_error = git_state(repo)
    topology_code, topology = run_topology(repo, profile, startup_owner)
    stop_lock = stop_lock_state(repo, profile)
    capability = capability_check(repo)
    live_owner = topology.get("live_implementation_owner")

    blocked = blocked_cards(topology)
    handoffs = handoff_candidates(topology)
    payload: dict[str, Any] = {
        "repo": str(repo),
        "profile": str(profile),
        "startup_owner": startup_owner,
        "repo_state": repo_state,
        "dirty_paths": dirty_paths,
        "git_error": git_error,
        "topology": topology,
        "topology_exit_code": topology_code,
        "blocked_cards": blocked,
        "handoff_candidates": compact_handoff_candidates(handoffs),
        "stop_lock_state": stop_lock,
        "watchdog_reporter_state": watchdog_reporter_state(repo, profile),
        "capability_check": capability,
        "dirty_handoff_recovery": None,
        "safe_to_start": False,
        "recommended_action": "blocked:unknown",
        "explicit_gate": "unknown",
    }

    if git_error:
        payload["recommended_action"] = "blocked:git_state_unreadable"
        payload["explicit_gate"] = "git_state_unreadable"
    elif repo_state == "dirty":
        recovery = recovery_preflight.classify(repo, handoffs.get("tasks") or blocked.get("cards") or [])
        payload["dirty_handoff_recovery"] = recovery
        payload["recommended_action"] = recovery.get("recommended_action") or "recover_dirty_handoff"
        payload["explicit_gate"] = recovery.get("explicit_gate")
    elif topology.get("topology_conflict") or topology_code != 0:
        payload["recommended_action"] = "blocked:topology_conflict"
        payload["explicit_gate"] = "topology_conflict"
    elif stop_lock["status"] != "clear":
        payload["recommended_action"] = "blocked:stop_lock_present"
        payload["explicit_gate"] = "stop_lock_present"
    elif capability["status"] != "ok":
        payload["recommended_action"] = "blocked:missing_capability"
        payload["explicit_gate"] = "missing_capability"
    elif live_owner == startup_owner:
        payload["recommended_action"] = "resume_existing_owner"
        payload["safe_to_start"] = True
        payload["explicit_gate"] = None
    elif live_owner == "none_active":
        blocked_gate = blocked_card_start_gate(blocked)
        if blocked_gate is not None:
            action, gate = blocked_gate
            payload["recommended_action"] = action
            payload["explicit_gate"] = gate
        else:
            action_suffix = startup_owner
            payload["recommended_action"] = f"start_{action_suffix}"
            payload["safe_to_start"] = True
            payload["explicit_gate"] = None
    else:
        payload["recommended_action"] = "blocked:topology_conflict"
        payload["explicit_gate"] = "topology_conflict"

    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--startup-owner", choices=sorted(ALLOWED_OWNERS), default="gateway_kanban_dispatcher")
    args = parser.parse_args(argv)

    payload = classify(args.repo.resolve(), args.profile.resolve(), args.startup_owner)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("safe_to_start") and payload.get("explicit_gate") is None else 1


if __name__ == "__main__":
    sys.exit(main())
