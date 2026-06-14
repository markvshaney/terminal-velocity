#!/usr/bin/env python3
"""Deterministic Terminal Velocity integration-lane guard.

This is the scripted half of the TV integration owner. It does not implement
features. It classifies whether a local worker commit stack is safe to publish,
optionally performs the normal non-force push, and emits a JSON decision packet
for an LLM/coordinator lane to review or record.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

DEFAULT_REPO = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = Path("/home/bh/.hermes/profiles/loki-game")
SAFE_PREFIXES = (
    ".hermes/long-running/",
    "docs/checklists/",
    "docs/prompts/",
    "docs/research/",
    "godot_ev/",
    "native_ev/",
    "tools/",
)
DENY_PATTERNS = (
    re.compile(r"(^|/)\.env($|[.])"),
    re.compile(r"(^|/)auth\.json$"),
    re.compile(r"(^|/)credentials?($|[./])", re.I),
    re.compile(r"(^|/)secrets?($|[./])", re.I),
    re.compile(r"(^|/)raw[-_]?assets?($|/)", re.I),
)
SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{30,}"),
)
ACTIVE_STATUSES = {"running"}
TV_TERMS = ("terminal velocity", "terminal-velocity", "tv-spec", "continue tv", " tv ")
GATE_NORMALIZATION_MARKER = "tv_gate_normalization"
PUSH_READY_RECOVERY_MARKER = "tv_push_ready_recovery"
UNSAFE_DIRTY_RECOVERY_MARKER = "tv_unsafe_dirty_recovery"
ACTIONABLE_GATE_CLASSES = {"push_ready", "review_required_process_bug"}


def run(cmd: list[str], repo: Path, *, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed {cmd}: {result.stdout}")
    return result


def git_lines(repo: Path, *args: str) -> list[str]:
    result = run(["git", *args], repo, check=True)
    return [line for line in result.stdout.splitlines() if line.strip()]


def git_text(repo: Path, *args: str) -> str:
    return run(["git", *args], repo, check=True).stdout.strip()


def dirty_status(repo: Path) -> list[str]:
    return git_lines(repo, "status", "--porcelain")


def recovery_preflight(repo: Path) -> dict[str, Any] | None:
    script = repo / "tools/tv_runner_recovery_preflight.py"
    if not script.exists():
        return None
    result = subprocess.run(
        ["python3", str(script), "--repo", str(repo)],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=90,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"recommended_action": "unavailable", "error": result.stdout.strip()}
    payload["returncode"] = result.returncode
    return payload


def ahead_count(repo: Path) -> int:
    result = run(["git", "rev-list", "--count", "origin/main..HEAD"], repo)
    if result.returncode != 0:
        return 0
    try:
        return int(result.stdout.strip() or "0")
    except ValueError:
        return 0


def behind_count(repo: Path) -> int:
    result = run(["git", "rev-list", "--count", "HEAD..origin/main"], repo)
    if result.returncode != 0:
        return 0
    try:
        return int(result.stdout.strip() or "0")
    except ValueError:
        return 0


def changed_files(repo: Path) -> list[str]:
    result = run(["git", "diff", "--name-only", "origin/main..HEAD"], repo)
    if result.returncode != 0:
        return []
    return sorted(line for line in result.stdout.splitlines() if line.strip())


def commit_summaries(repo: Path) -> list[str]:
    result = run(["git", "log", "--oneline", "origin/main..HEAD"], repo)
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def path_allowed(path: str) -> bool:
    return path.startswith(SAFE_PREFIXES) and not any(pattern.search(path) for pattern in DENY_PATTERNS)


def scan_committed_diff_for_secrets(repo: Path) -> list[str]:
    result = run(["git", "diff", "origin/main..HEAD", "--"], repo)
    if result.returncode != 0:
        return ["diff_unavailable"]
    hits: list[str] = []
    current_file = "unknown"
    for raw in result.stdout.splitlines():
        if raw.startswith("+++ b/"):
            current_file = raw[6:]
            continue
        if not raw.startswith("+") or raw.startswith("+++"):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(raw):
                hits.append(current_file)
                break
    return sorted(set(hits))


def kanban_db_candidates(profile: Path) -> list[Path]:
    root = profile.parent.parent if profile.parent.name == "profiles" else profile
    candidates = [root / "kanban.db", profile / "kanban.db"]
    boards = root / "kanban/boards"
    if boards.is_dir():
        candidates.extend(sorted(path / "kanban.db" for path in boards.iterdir()))
    seen: set[str] = set()
    unique: list[Path] = []
    for path in candidates:
        key = str(path)
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def row_is_tv_related(row: dict[str, Any], repo: Path) -> bool:
    text = " ".join(str(value or "") for value in row.values()).lower()
    return str(repo).lower() in text or any(term in text for term in TV_TERMS)


def active_worker_claims(profile: Path, repo: Path) -> list[str]:
    claims: list[str] = []
    for db_path in kanban_db_candidates(profile):
        if not db_path.exists():
            continue
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row
        except sqlite3.Error:
            continue
        try:
            tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "tasks" not in tables:
                continue
            columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
            select_columns = [c for c in ("id", "title", "body", "assignee", "status", "tenant", "workspace_path", "claim_lock", "worker_pid") if c in columns]
            if "status" not in columns:
                continue
            sql = f"SELECT {', '.join(select_columns)} FROM tasks WHERE status IN ({', '.join('?' for _ in ACTIVE_STATUSES)})"
            for row in conn.execute(sql, sorted(ACTIVE_STATUSES)):
                data = dict(row)
                if row_is_tv_related(data, repo):
                    claims.append(str(data.get("id") or db_path))
        finally:
            conn.close()
    return sorted(set(claims))


def canonical_gate_class(task: dict[str, Any], evidence_texts: list[str] | None = None) -> str:
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


def task_comment_bodies(conn: sqlite3.Connection, task_id: str) -> list[str]:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "task_comments" not in tables:
        return []
    try:
        rows = conn.execute(
            "SELECT body FROM task_comments WHERE task_id = ? ORDER BY id",
            (task_id,),
        ).fetchall()
    except sqlite3.Error:
        return []
    bodies: list[str] = []
    for row in rows:
        body = str(row[0] or "")
        if any(marker in body for marker in (GATE_NORMALIZATION_MARKER, PUSH_READY_RECOVERY_MARKER, UNSAFE_DIRTY_RECOVERY_MARKER)):
            continue
        bodies.append(body)
    return bodies


def normalization_comment_body(task: dict[str, Any], klass: str) -> str:
    next_action = {
        "push_ready": "integration owner should verify bundle state, publish if still current, then close or supersede this gate",
        "review_required_process_bug": "generic review-required is stale for verified safe-local TV work; convert to push_ready, verifier_failed, unsafe_dirty_state, explicit_human_gate, or continue",
    }.get(klass, "inspect and convert to a concrete TV gate class")
    return (
        f"{GATE_NORMALIZATION_MARKER}: canonical_class={klass}\n"
        f"source_task={task.get('id')} title={task.get('title')}\n"
        f"next_action={next_action}"
    )


def task_has_normalization_comment(conn: sqlite3.Connection, task_id: str, klass: str) -> bool:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "task_comments" not in tables:
        return False
    needle = f"{GATE_NORMALIZATION_MARKER}: canonical_class={klass}"
    row = conn.execute(
        "SELECT 1 FROM task_comments WHERE task_id = ? AND body LIKE ? LIMIT 1",
        (task_id, f"%{needle}%"),
    ).fetchone()
    return row is not None


def insert_normalization_comment(conn: sqlite3.Connection, task: dict[str, Any], klass: str, author: str) -> None:
    now = int(time.time())
    body = normalization_comment_body(task, klass)
    conn.execute(
        "INSERT INTO task_comments (task_id, author, body, created_at) VALUES (?, ?, ?, ?)",
        (task["id"], author, body, now),
    )
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "task_events" in tables:
        conn.execute(
            "INSERT INTO task_events (task_id, run_id, kind, payload, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                task["id"],
                None,
                "tv_gate_normalized",
                json.dumps({"canonical_class": klass, "author": author}, sort_keys=True),
                now,
            ),
        )


def push_ready_recovery_comment_body(task: dict[str, Any]) -> str:
    return (
        f"{PUSH_READY_RECOVERY_MARKER}: canonical_class=push_ready\n"
        f"source_task={task.get('id')} title={task.get('title')}\n"
        "resolution=repo is clean and not ahead of origin/main; treating this push_ready handoff as already integrated/stale for start-resume gating"
    )


def task_has_push_ready_recovery_comment(conn: sqlite3.Connection, task_id: str) -> bool:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "task_comments" not in tables:
        return False
    row = conn.execute(
        "SELECT 1 FROM task_comments WHERE task_id = ? AND body LIKE ? LIMIT 1",
        (task_id, f"%{PUSH_READY_RECOVERY_MARKER}: canonical_class=push_ready%"),
    ).fetchone()
    return row is not None


def close_push_ready_task(conn: sqlite3.Connection, task: dict[str, Any], author: str, task_columns: set[str]) -> bool:
    task_id = str(task["id"])
    if task_has_push_ready_recovery_comment(conn, task_id):
        return False
    now = int(time.time())
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "task_comments" in tables:
        conn.execute(
            "INSERT INTO task_comments (task_id, author, body, created_at) VALUES (?, ?, ?, ?)",
            (task_id, author, push_ready_recovery_comment_body(task), now),
        )
    set_parts = ["status = 'done'"]
    params: list[Any] = []
    if "completed_at" in task_columns:
        set_parts.append("completed_at = ?")
        params.append(now)
    if "result" in task_columns:
        set_parts.append("result = ?")
        params.append("push_ready handoff already integrated/stale; closed by TV integration-owner recovery")
    params.append(task_id)
    conn.execute(f"UPDATE tasks SET {', '.join(set_parts)} WHERE id = ? AND status = 'blocked'", params)
    if "task_events" in tables:
        conn.execute(
            "INSERT INTO task_events (task_id, run_id, kind, payload, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                task_id,
                None,
                "tv_push_ready_recovered",
                json.dumps({"author": author, "resolution": "stale_clean_handoff_closed"}, sort_keys=True),
                now,
            ),
        )
    return True


def recover_push_ready_handoffs(
    profile: Path,
    repo: Path,
    classification: dict[str, Any],
    *,
    apply: bool,
    author: str = "integration_owner",
) -> dict[str, Any]:
    planned: list[dict[str, Any]] = []
    skipped: dict[str, str] = {}
    inspected_paths: list[str] = []
    errors: list[dict[str, str]] = []
    closeouts_written = 0

    if classification.get("status_porcelain"):
        recommended_action = "recover_dirty_handoff_first"
    elif classification.get("behind_count", 0) > 0:
        recommended_action = "sync_branch_before_recovery"
    elif classification.get("ahead_count", 0) > 0:
        recommended_action = "publish_local_checkpoint_before_closeout"
    elif classification.get("active_worker_claims"):
        recommended_action = "wait_for_active_worker"
    else:
        recommended_action = "close_stale_push_ready_handoffs"

    for db_path in kanban_db_candidates(profile):
        if not db_path.exists():
            continue
        inspected_paths.append(str(db_path))
        uri = f"file:{db_path}?mode={'rwc' if apply else 'ro'}"
        try:
            conn = sqlite3.connect(uri, uri=True)
            conn.row_factory = sqlite3.Row
        except sqlite3.Error as exc:
            errors.append({"path": str(db_path), "error": str(exc)})
            continue
        try:
            tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "tasks" not in tables:
                continue
            columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
            wanted = [column for column in ("id", "title", "body", "assignee", "status", "tenant", "workspace_path") if column in columns]
            if not {"id", "status"}.issubset(columns):
                continue
            rows = conn.execute(
                f"SELECT {', '.join(wanted)} FROM tasks WHERE status = ? ORDER BY id",
                ("blocked",),
            ).fetchall()
            for row in rows:
                task = dict(row)
                if not row_is_tv_related(task, repo):
                    continue
                task_id = str(task.get("id") or "")
                klass = canonical_gate_class(task, task_comment_bodies(conn, task_id))
                if klass != "push_ready":
                    skipped[task_id] = klass
                    continue
                action = {
                    "db_path": str(db_path),
                    "task_id": task_id,
                    "title": task.get("title"),
                    "canonical_class": klass,
                    "comment_marker": PUSH_READY_RECOVERY_MARKER,
                }
                planned.append(action)
                if apply and recommended_action == "close_stale_push_ready_handoffs":
                    if "task_comments" not in tables:
                        errors.append({"path": str(db_path), "error": "task_comments table missing"})
                    elif close_push_ready_task(conn, task, author, columns):
                        closeouts_written += 1
            if apply:
                conn.commit()
        except sqlite3.Error as exc:
            errors.append({"path": str(db_path), "error": str(exc)})
        finally:
            conn.close()

    return {
        "applied": apply,
        "author": author,
        "recommended_action": recommended_action,
        "inspected_paths": inspected_paths,
        "planned_closeouts": planned,
        "skipped": skipped,
        "closeouts_written": closeouts_written,
        "errors": errors,
    }


def unsafe_dirty_recovery_comment_body(task: dict[str, Any]) -> str:
    return (
        f"{UNSAFE_DIRTY_RECOVERY_MARKER}: canonical_class=unsafe_dirty_state\n"
        f"source_task={task.get('id')} title={task.get('title')}\n"
        "resolution=repo is currently clean and synced; treating this unsafe_dirty_state handoff as stale for start-resume gating"
    )


def task_has_unsafe_dirty_recovery_comment(conn: sqlite3.Connection, task_id: str) -> bool:
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "task_comments" not in tables:
        return False
    row = conn.execute(
        "SELECT 1 FROM task_comments WHERE task_id = ? AND body LIKE ? LIMIT 1",
        (task_id, f"%{UNSAFE_DIRTY_RECOVERY_MARKER}: canonical_class=unsafe_dirty_state%"),
    ).fetchone()
    return row is not None


def close_unsafe_dirty_task(conn: sqlite3.Connection, task: dict[str, Any], author: str, task_columns: set[str]) -> bool:
    task_id = str(task["id"])
    if task_has_unsafe_dirty_recovery_comment(conn, task_id):
        return False
    now = int(time.time())
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    if "task_comments" in tables:
        conn.execute(
            "INSERT INTO task_comments (task_id, author, body, created_at) VALUES (?, ?, ?, ?)",
            (task_id, author, unsafe_dirty_recovery_comment_body(task), now),
        )
    set_parts = ["status = 'done'"]
    params: list[Any] = []
    if "completed_at" in task_columns:
        set_parts.append("completed_at = ?")
        params.append(now)
    if "result" in task_columns:
        set_parts.append("result = ?")
        params.append("unsafe_dirty_state handoff is stale because repo is clean/synced; closed by TV integration-owner recovery")
    params.append(task_id)
    conn.execute(f"UPDATE tasks SET {', '.join(set_parts)} WHERE id = ? AND status = 'blocked'", params)
    if "task_events" in tables:
        conn.execute(
            "INSERT INTO task_events (task_id, run_id, kind, payload, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                task_id,
                None,
                "tv_unsafe_dirty_recovered",
                json.dumps({"author": author, "resolution": "stale_clean_handoff_closed"}, sort_keys=True),
                now,
            ),
        )
    return True


def recover_unsafe_dirty_handoffs(
    profile: Path,
    repo: Path,
    classification: dict[str, Any],
    *,
    apply: bool,
    author: str = "integration_owner",
) -> dict[str, Any]:
    planned: list[dict[str, Any]] = []
    skipped: dict[str, str] = {}
    inspected_paths: list[str] = []
    errors: list[dict[str, str]] = []
    closeouts_written = 0

    if classification.get("status_porcelain"):
        recommended_action = "repair_live_dirty_state_first"
    elif classification.get("behind_count", 0) > 0:
        recommended_action = "sync_branch_before_recovery"
    elif classification.get("ahead_count", 0) > 0:
        recommended_action = "publish_local_checkpoint_before_closeout"
    elif classification.get("active_worker_claims"):
        recommended_action = "wait_for_active_worker"
    else:
        recommended_action = "close_stale_unsafe_dirty_state_handoffs"

    for db_path in kanban_db_candidates(profile):
        if not db_path.exists():
            continue
        inspected_paths.append(str(db_path))
        uri = f"file:{db_path}?mode={'rwc' if apply else 'ro'}"
        try:
            conn = sqlite3.connect(uri, uri=True)
            conn.row_factory = sqlite3.Row
        except sqlite3.Error as exc:
            errors.append({"path": str(db_path), "error": str(exc)})
            continue
        try:
            tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "tasks" not in tables:
                continue
            columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
            wanted = [column for column in ("id", "title", "body", "assignee", "status", "tenant", "workspace_path") if column in columns]
            if not {"id", "status"}.issubset(columns):
                continue
            rows = conn.execute(
                f"SELECT {', '.join(wanted)} FROM tasks WHERE status = ? ORDER BY id",
                ("blocked",),
            ).fetchall()
            for row in rows:
                task = dict(row)
                if not row_is_tv_related(task, repo):
                    continue
                task_id = str(task.get("id") or "")
                klass = canonical_gate_class(task, task_comment_bodies(conn, task_id))
                if klass != "unsafe_dirty_state":
                    skipped[task_id] = klass
                    continue
                action = {
                    "db_path": str(db_path),
                    "task_id": task_id,
                    "title": task.get("title"),
                    "canonical_class": klass,
                    "comment_marker": UNSAFE_DIRTY_RECOVERY_MARKER,
                }
                planned.append(action)
                if apply and recommended_action == "close_stale_unsafe_dirty_state_handoffs":
                    if "task_comments" not in tables:
                        errors.append({"path": str(db_path), "error": "task_comments table missing"})
                    elif close_unsafe_dirty_task(conn, task, author, columns):
                        closeouts_written += 1
            if apply:
                conn.commit()
        except sqlite3.Error as exc:
            errors.append({"path": str(db_path), "error": str(exc)})
        finally:
            conn.close()

    return {
        "applied": apply,
        "author": author,
        "recommended_action": recommended_action,
        "inspected_paths": inspected_paths,
        "planned_closeouts": planned,
        "skipped": skipped,
        "closeouts_written": closeouts_written,
        "errors": errors,
    }


def normalize_gate_comments(profile: Path, repo: Path, *, apply: bool, author: str = "integration_owner") -> dict[str, Any]:
    return normalize_gate_comments_for_tasks(profile, repo, apply=apply, author=author, only_task_ids=None)


def normalize_gate_comments_for_tasks(
    profile: Path,
    repo: Path,
    *,
    apply: bool,
    author: str = "integration_owner",
    only_task_ids: set[str] | None = None,
) -> dict[str, Any]:
    planned: list[dict[str, Any]] = []
    skipped: dict[str, str] = {}
    inspected_paths: list[str] = []
    errors: list[dict[str, str]] = []
    comments_written = 0

    for db_path in kanban_db_candidates(profile):
        if not db_path.exists():
            continue
        inspected_paths.append(str(db_path))
        uri = f"file:{db_path}?mode={'rwc' if apply else 'ro'}"
        try:
            conn = sqlite3.connect(uri, uri=True)
            conn.row_factory = sqlite3.Row
        except sqlite3.Error as exc:
            errors.append({"path": str(db_path), "error": str(exc)})
            continue
        try:
            tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "tasks" not in tables:
                continue
            columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
            wanted = [column for column in ("id", "title", "body", "assignee", "status", "tenant", "workspace_path") if column in columns]
            if not {"id", "status"}.issubset(columns):
                continue
            rows = conn.execute(
                f"SELECT {', '.join(wanted)} FROM tasks WHERE status = ? ORDER BY id",
                ("blocked",),
            ).fetchall()
            for row in rows:
                task = dict(row)
                if not row_is_tv_related(task, repo):
                    continue
                task_id = str(task.get("id") or "")
                klass = canonical_gate_class(task, task_comment_bodies(conn, task_id))
                if only_task_ids is not None and task_id not in only_task_ids:
                    skipped[task_id] = f"outside_recovery_scope:{klass}"
                    continue
                if klass not in ACTIONABLE_GATE_CLASSES:
                    skipped[task_id] = klass
                    continue
                action = {
                    "db_path": str(db_path),
                    "task_id": task_id,
                    "title": task.get("title"),
                    "canonical_class": klass,
                    "comment_marker": GATE_NORMALIZATION_MARKER,
                }
                planned.append(action)
                if apply:
                    if "task_comments" not in tables:
                        errors.append({"path": str(db_path), "error": "task_comments table missing"})
                    elif not task_has_normalization_comment(conn, task_id, klass):
                        insert_normalization_comment(conn, task, klass, author)
                        comments_written += 1
            if apply:
                conn.commit()
        except sqlite3.Error as exc:
            errors.append({"path": str(db_path), "error": str(exc)})
        finally:
            conn.close()

    return {
        "applied": apply,
        "author": author,
        "inspected_paths": inspected_paths,
        "planned_comments": planned,
        "skipped": skipped,
        "comments_written": comments_written,
        "errors": errors,
    }


def reconcile_ledger_projection(repo: Path, profile: Path, *, apply: bool) -> dict[str, Any]:
    cmd = [
        sys.executable or "python3",
        str(repo / "tools/tv_ledger_reconcile.py"),
        "--repo",
        str(repo),
        "--profile",
        str(profile),
    ]
    if apply:
        cmd.append("--write")
    result = run(cmd, repo)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {
            "applied": apply,
            "error": "ledger_reconcile_json_parse_failed",
            "returncode": result.returncode,
            "output": result.stdout,
        }
    payload["applied"] = apply
    payload["returncode"] = result.returncode
    if result.returncode not in {0, 1}:
        payload.setdefault("errors", []).append("ledger_reconcile_failed")
    return payload


def _bullet_list(items: list[str], *, limit: int = 5) -> list[str]:
    visible = [str(item) for item in items[:limit]]
    if len(items) > limit:
        visible.append(f"… plus {len(items) - limit} more")
    return [f"- {item}" for item in visible]


def _unique_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def deterministic_game_dev_content(changed_files: list[str], commit_summaries: list[str]) -> list[str]:
    """Describe TV game-dev content from deterministic file/commit patterns only."""
    descriptions: list[str] = []
    changed = set(changed_files)
    commit_text = "\n".join(commit_summaries).lower()

    if any(path in changed for path in {
        "tools/extract_ev_system_semantics.py",
        "native_ev/data/sourced_ev_systems.json",
    }):
        descriptions.append("EV Classic sourced systems manifest / galaxy topology semantics")
    if any(path in changed for path in {
        "native_ev/model.py",
        "native_ev/scenario_eval.py",
    }) or any(path.startswith("native_ev/tests/test_") for path in changed):
        descriptions.append("Native EV model validation and scenario readiness surfaces")
    if any(path.startswith("godot_ev/") for path in changed):
        descriptions.append("Godot runtime/player-visible implementation")
    if any(path.startswith("docs/checklists/ev-classic-fidelity-implementation-backlog") for path in changed):
        descriptions.append("Fidelity backlog/source-readiness docs")
    if any(path.startswith("native_ev/data/") and "sourced_ev_" in path for path in changed):
        descriptions.append("Source-backed Native EV data manifest updates")
    if any(path.startswith("tools/tv_") for path in changed) or "runner" in commit_text or "integration" in commit_text:
        descriptions.append("TV runner/integration workflow reporting")
    if any(path.startswith(".hermes/long-running/") for path in changed):
        descriptions.append("Long-running TV task ledger/provenance update")
    return _unique_preserving_order(descriptions)


def deterministic_changed_areas(changed_files: list[str]) -> list[str]:
    """Group changed paths into human-readable, non-LLM TV areas."""
    changed = set(changed_files)
    areas: list[str] = []
    if any(path in changed for path in {
        "tools/extract_ev_system_semantics.py",
        "native_ev/data/sourced_ev_systems.json",
    }):
        areas.append("Native EV sourced systems extractor and manifest")
    if any(path in changed for path in {"native_ev/model.py", "native_ev/scenario_eval.py"}):
        areas.append("Native EV model/scenario readiness surfaces")
    if any(path.startswith("native_ev/tests/") for path in changed):
        areas.append("Native EV regression tests")
    if any(path.startswith("godot_ev/") for path in changed):
        areas.append("Godot runtime")
    if any(path.startswith("docs/checklists/") for path in changed):
        areas.append("Fidelity backlog/checklist artifacts")
    if any(path.startswith("tools/tv_") for path in changed):
        areas.append("TV integration/runner tooling")
    if any(path.startswith(".hermes/long-running/") for path in changed):
        areas.append("Long-running runner ledger/provenance")
    return _unique_preserving_order(areas) or changed_files


def build_post_push_report(payload: dict[str, Any]) -> str:
    """Build a concise deterministic TV progress report for Loki GameTV after a verified push."""
    head = str(payload.get("head") or payload.get("origin_main") or "")
    short_head = head[:7] if head else "unknown"
    commits = [str(item) for item in payload.get("commit_summaries") or []]
    changed_files = [str(item) for item in payload.get("changed_files") or []]
    changed = deterministic_changed_areas(changed_files)
    game_dev_content = deterministic_game_dev_content(changed_files, commits)
    checks = [str(item) for item in payload.get("passed_checks") or []]

    lines = [
        "TV progress published",
        f"Commit: `{short_head}`",
    ]
    if commits:
        lines.append("Bundle:")
        lines.extend(_bullet_list(commits, limit=4))
    if game_dev_content:
        lines.append("Game-dev content:")
        lines.extend(_bullet_list(game_dev_content, limit=6))
    if changed:
        lines.append("Changed:")
        lines.extend(_bullet_list(changed, limit=6))
    if checks:
        lines.append("Verified:")
        lines.extend(_bullet_list(checks, limit=6))
    return "\n".join(lines)


def deliver_message_report(target: str, message: str, *, dry_run: bool = False) -> dict[str, Any]:
    if dry_run:
        return {"target": target, "status": "dry_run", "message": message}
    hermes_agent = Path(os.environ.get("HERMES_AGENT_HOME", "/home/bh/.hermes/hermes-agent"))
    code = (
        "import sys; "
        "from tools.send_message_tool import send_message_tool; "
        "target=sys.argv[1]; message=sys.stdin.read(); "
        "print(send_message_tool({'action':'send','target':target,'message':message}))"
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(hermes_agent) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    result = subprocess.run(
        [sys.executable or "python3", "-c", code, target],
        input=message,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        timeout=60,
    )
    return {
        "target": target,
        "status": "sent" if result.returncode == 0 and '\"error\"' not in result.stdout else "failed",
        "returncode": result.returncode,
        "output": result.stdout.strip(),
        "message": message,
    }


def deliver_post_push_report(target: str, message: str, *, dry_run: bool = False) -> dict[str, Any]:
    return deliver_message_report(target, message, dry_run=dry_run)


def build_blocked_runner_report(payload: dict[str, Any]) -> str:
    """Build a concise deterministic TV report when integration blocks runner progress."""
    blockers = [str(item) for item in payload.get("blockers") or []]
    warnings = [str(item) for item in payload.get("warnings") or []]
    status = [str(item) for item in payload.get("status_porcelain") or []]
    active = [str(item) for item in payload.get("active_worker_claims") or []]
    unsafe = [str(item) for item in payload.get("unsafe_files") or []]
    changed_files = [str(item) for item in payload.get("changed_files") or []]
    commit_summaries = [str(item) for item in payload.get("commit_summaries") or []]

    lines = [
        "TV runner blocked by integration owner",
        f"decision: {payload.get('decision') or 'unknown'}",
    ]
    if blockers:
        lines.append("why blocked:")
        lines.extend(_bullet_list(blockers, limit=8))
    if warnings:
        lines.append("warnings:")
        lines.extend(_bullet_list(warnings, limit=6))
    if active:
        lines.append("active worker claims:")
        lines.extend(_bullet_list(active, limit=6))
    if status:
        lines.append("dirty worktree:")
        lines.extend(_bullet_list(status, limit=8))
    if unsafe:
        lines.append("unsafe files:")
        lines.extend(_bullet_list(unsafe, limit=8))
    if commit_summaries:
        lines.append("local commits pending integration:")
        lines.extend(_bullet_list(commit_summaries, limit=4))
    if changed_files:
        lines.append("changed areas:")
        lines.extend(_bullet_list(deterministic_changed_areas(changed_files), limit=6))
    return "\n".join(lines)


def should_send_blocked_runner_report(payload: dict[str, Any]) -> bool:
    """Return true when this integration packet explains a runner-stopping block."""
    if payload.get("decision") == "needs_human":
        return True
    if payload.get("blockers"):
        return True
    for key in ("push_ready_recovery", "unsafe_dirty_recovery"):
        recovery = payload.get(key) or {}
        action = recovery.get("recommended_action")
        if action and action not in {
            "close_stale_push_ready_handoffs",
            "close_stale_unsafe_dirty_state_handoffs",
        }:
            return True
    return False


def classify(repo: Path, profile: Path, *, allow_process_artifacts: bool) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    passed_checks: list[str] = []

    if not (repo / ".git").exists():
        blockers.append("not_git_repo")

    status = dirty_status(repo) if not blockers else []
    dirty_recovery = recovery_preflight(repo) if status else None
    if status:
        blockers.append("dirty_worktree")
        if dirty_recovery and dirty_recovery.get("explicit_gate") == "control_plane_dirty_state":
            blockers.append("control_plane_dirty_state")

    active_claims = active_worker_claims(profile, repo)
    if active_claims:
        blockers.append("active_worker")

    ahead = ahead_count(repo) if not blockers or "dirty_worktree" not in blockers else ahead_count(repo)
    behind = behind_count(repo)
    if behind:
        blockers.append("branch_behind_origin")
    if ahead <= 0:
        warnings.append("nothing_to_publish")

    files = changed_files(repo) if ahead > 0 else []
    unsafe_files = [path for path in files if not path_allowed(path)]
    if allow_process_artifacts:
        unsafe_files = [path for path in unsafe_files if not path.startswith(".hermes/long-running/")]
    if unsafe_files:
        blockers.append("unsafe_changed_files")

    diff_check = run(["git", "diff", "--check", "origin/main..HEAD"], repo)
    if diff_check.returncode == 0:
        passed_checks.append("git_diff_check")
    else:
        blockers.append("git_diff_check_failed")

    secret_hits = scan_committed_diff_for_secrets(repo) if ahead > 0 else []
    if secret_hits:
        blockers.append("secret_scan_hits")
    else:
        passed_checks.append("committed_diff_secret_scan")

    decision = "publish" if ahead > 0 and not blockers else "needs_human"
    if ahead <= 0 and not blockers:
        decision = "hold"

    return {
        "decision": decision,
        "blockers": sorted(set(blockers)),
        "warnings": sorted(set(warnings)),
        "passed_checks": passed_checks,
        "repo": str(repo),
        "profile": str(profile),
        "status_porcelain": status,
        "dirty_state_recovery": dirty_recovery,
        "ahead_count": ahead,
        "behind_count": behind,
        "changed_files": files,
        "unsafe_files": unsafe_files,
        "active_worker_claims": active_claims,
        "commit_summaries": commit_summaries(repo) if ahead > 0 else [],
        "secret_scan_hits": secret_hits,
        "llm_review": {
            "required_before_push": True,
            "instructions": [
                "Confirm changed files match the blocked Kanban handoff or coherent TV bundle.",
                "Confirm source/fidelity labels do not promote Classic truth without evidence.",
                "Return publish, hold, or needs_human before --push is used.",
            ],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(os.environ.get("TV_INTEGRATOR_REPO", DEFAULT_REPO)))
    parser.add_argument("--profile", type=Path, default=Path(os.environ.get("TV_INTEGRATOR_PROFILE", DEFAULT_PROFILE)))
    parser.add_argument("--dry-run", action="store_true", help="Classify only; never push.")
    parser.add_argument("--push", action="store_true", help="After successful deterministic+LLM approval, push normally and verify HEAD == origin/main.")
    parser.add_argument("--llm-approved", action="store_true", help="Structured LLM review already returned publish for this exact bundle.")
    parser.add_argument("--allow-process-artifacts", action="store_true", help="Allow repo-local .hermes/long-running files in a bundle.")
    parser.add_argument("--normalize-gates", action="store_true", help="Plan canonical comments for actionable blocked TV Kanban gates.")
    parser.add_argument("--apply-gate-comments", action="store_true", help="With --normalize-gates, write idempotent Kanban comments/events for planned gate normalization.")
    parser.add_argument("--recover-push-ready-handoff", action="store_true", help="Plan stale clean push_ready handoff closeout for start/resume recovery.")
    parser.add_argument("--apply-push-ready-recovery", action="store_true", help="With --recover-push-ready-handoff, close stale clean push_ready Kanban gates idempotently.")
    parser.add_argument("--recover-unsafe-dirty-state", action="store_true", help="Plan stale clean unsafe_dirty_state handoff closeout for start/resume recovery.")
    parser.add_argument("--apply-unsafe-dirty-recovery", action="store_true", help="With --recover-unsafe-dirty-state, close stale clean unsafe_dirty_state Kanban gates idempotently.")
    parser.add_argument("--reconcile-ledger", action="store_true", help="Attach deterministic task-ledger reconciliation dry-run payload.")
    parser.add_argument("--apply-ledger-reconcile", action="store_true", help="With --reconcile-ledger, write the normalized task-ledger projection.")
    parser.add_argument("--post-push-report-target", help="After a verified push, post a concise TV progress report to this Hermes messaging target, e.g. 'telegram:Loki GameTV'.")
    parser.add_argument("--post-push-report-dry-run", action="store_true", help="Build the post-push report payload without sending it.")
    parser.add_argument(
        "--blocked-report-target",
        default=os.environ.get("TV_INTEGRATOR_BLOCKED_REPORT_TARGET"),
        help="When the integration owner blocks runner progress, send the why-blocked report to this Hermes messaging target, e.g. 'telegram:Loki GameTV'.",
    )
    parser.add_argument("--blocked-report-dry-run", action="store_true", help="Build the blocked-runner report payload without sending it.")
    args = parser.parse_args()

    repo = args.repo.resolve()
    profile = args.profile.resolve()
    payload = classify(repo, profile, allow_process_artifacts=args.allow_process_artifacts)
    payload["dry_run"] = bool(args.dry_run or not args.push)
    payload["would_push"] = False
    payload["pushed"] = False

    scoped_normalization_task_ids: set[str] | None = None
    if args.recover_push_ready_handoff:
        payload["push_ready_recovery"] = recover_push_ready_handoffs(
            profile,
            repo,
            payload,
            apply=False,
        )
        scoped_normalization_task_ids = {str(item.get("task_id")) for item in payload["push_ready_recovery"].get("planned_closeouts", [])}

    if args.normalize_gates:
        payload["gate_normalization"] = normalize_gate_comments_for_tasks(
            profile,
            repo,
            apply=bool(args.apply_gate_comments),
            only_task_ids=scoped_normalization_task_ids,
        )

    if args.recover_push_ready_handoff and args.apply_push_ready_recovery:
        payload["push_ready_recovery"] = recover_push_ready_handoffs(
            profile,
            repo,
            payload,
            apply=True,
        )

    if args.recover_unsafe_dirty_state:
        payload["unsafe_dirty_recovery"] = recover_unsafe_dirty_handoffs(
            profile,
            repo,
            payload,
            apply=bool(args.apply_unsafe_dirty_recovery),
        )

    if args.reconcile_ledger:
        payload["ledger_reconciliation"] = reconcile_ledger_projection(
            repo,
            profile,
            apply=bool(args.apply_ledger_reconcile),
        )

    if args.push:
        if payload["decision"] != "publish":
            payload["blockers"] = sorted(set(payload["blockers"] + ["not_publishable"]))
        elif not args.llm_approved:
            payload["blockers"] = sorted(set(payload["blockers"] + ["llm_review_missing"]))
            payload["decision"] = "needs_human"
        else:
            payload["would_push"] = True
            push = run(["git", "push", "origin", "main"], repo)
            payload["push_output"] = push.stdout
            if push.returncode != 0:
                payload["blockers"] = sorted(set(payload["blockers"] + ["push_failed"]))
                payload["decision"] = "needs_human"
            else:
                run(["git", "fetch", "origin"], repo)
                head = git_text(repo, "rev-parse", "HEAD")
                origin = git_text(repo, "rev-parse", "origin/main")
                payload["head"] = head
                payload["origin_main"] = origin
                payload["pushed"] = head == origin
                if not payload["pushed"]:
                    payload["blockers"] = sorted(set(payload["blockers"] + ["post_push_head_mismatch"]))
                    payload["decision"] = "needs_human"

    if args.post_push_report_target:
        if payload.get("pushed") or args.post_push_report_dry_run:
            report = build_post_push_report(payload)
            payload["post_push_report"] = deliver_post_push_report(
                args.post_push_report_target,
                report,
                dry_run=bool(args.post_push_report_dry_run),
            )
        else:
            payload["post_push_report"] = {
                "target": args.post_push_report_target,
                "status": "skipped",
                "reason": "push_not_verified",
            }

    if args.blocked_report_target:
        if should_send_blocked_runner_report(payload) or args.blocked_report_dry_run:
            report = build_blocked_runner_report(payload)
            payload["blocked_runner_report"] = deliver_message_report(
                args.blocked_report_target,
                report,
                dry_run=bool(args.blocked_report_dry_run),
            )
        else:
            payload["blocked_runner_report"] = {
                "target": args.blocked_report_target,
                "status": "skipped",
                "reason": "integration_not_blocked",
            }

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["decision"] in {"publish", "hold"} and not payload["blockers"] else 2


if __name__ == "__main__":
    sys.exit(main())
