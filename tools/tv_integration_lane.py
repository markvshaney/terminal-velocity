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


def canonical_gate_class(task: dict[str, Any]) -> str:
    text = " ".join(str(task.get(key) or "") for key in ("title", "body", "status")).lower()
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


def normalize_gate_comments(profile: Path, repo: Path, *, apply: bool, author: str = "integration_owner") -> dict[str, Any]:
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
                klass = canonical_gate_class(task)
                task_id = str(task.get("id") or "")
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


def classify(repo: Path, profile: Path, *, allow_process_artifacts: bool) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    passed_checks: list[str] = []

    if not (repo / ".git").exists():
        blockers.append("not_git_repo")

    status = dirty_status(repo) if not blockers else []
    if status:
        blockers.append("dirty_worktree")

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
    args = parser.parse_args()

    repo = args.repo.resolve()
    profile = args.profile.resolve()
    payload = classify(repo, profile, allow_process_artifacts=args.allow_process_artifacts)
    payload["dry_run"] = bool(args.dry_run or not args.push)
    payload["would_push"] = False
    payload["pushed"] = False

    if args.normalize_gates:
        payload["gate_normalization"] = normalize_gate_comments(
            profile,
            repo,
            apply=bool(args.apply_gate_comments),
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

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["decision"] in {"publish", "hold"} and not payload["blockers"] else 2


if __name__ == "__main__":
    sys.exit(main())
