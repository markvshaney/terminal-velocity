#!/usr/bin/env python3
"""Classifier and guarded checkpoint helper for TV idle dirty handoff recovery.

Default mode is deterministic and side-effect-free: classify an idle worktree
before autostart seeds overlapping work. With --checkpoint, the integration
owner may create a local checkpoint commit only after classification proves the
dirty bundle matches a verifier-passed handoff. This script never pushes,
unblocks Kanban cards, or starts workers.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

DEFAULT_REPO = Path("/home/bh/workspaces/loki/terminal-velocity")
DEFAULT_BOARD = "terminal-velocity"
DEFAULT_ASSIGNEE = "terminal-velocity"
PROFILE_ARGS = ["hermes", "-p", "loki-game"]

REVIEW_TERMS = (
    "review-required",
    "review_required",
    "ready_for_review",
    "ready_for_review_or_integration",
    "push_ready",
    "handoff",
)
FOCUSED_PASS_TERMS = (
    "focused verifier passed",
    "focused verifiers passed",
    "targeted verifier passed",
    "targeted verification passed",
    "targeted scenario verifier passed",
    "focused scenario verification passed",
    "-> ok",
    " ok",
    " passed",
)
SENSITIVE_PATH_PARTS = (
    ".env",
    "secret",
    "secrets",
    "credential",
    "credentials",
    "token",
    "tokens",
    "private",
    "proprietary",
    "captures/raw",
    "screenshots/raw",
)
SAFE_TV_PREFIXES = (
    "native_ev/",
    "tools/",
    "docs/",
    "godot_ev/",
    ".hermes/long-running/tv-spec-implementation/",
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


def git_dirty_paths(repo: Path, exclude: set[Path]) -> tuple[str, list[str], str | None]:
    code, raw = run_checked(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, timeout=15)
    if code != 0:
        return "unknown", [], raw.strip() or "git status failed"
    paths: list[str] = []
    for line in raw.splitlines():
        if not line:
            continue
        status_path = line[3:] if len(line) > 3 else ""
        if " -> " in status_path:
            status_path = status_path.split(" -> ", 1)[1]
        full = (repo / status_path).resolve()
        if full in exclude:
            continue
        paths.append(status_path)
    return ("dirty" if paths else "clean"), sorted(paths), None


def load_tasks(path: Path | None, board: str) -> tuple[list[dict[str, Any]], str | None]:
    if path:
        try:
            data = json.loads(path.read_text())
        except Exception as exc:
            return [], f"tasks_json_unreadable: {exc}"
    else:
        code, raw = run_checked(PROFILE_ARGS + ["kanban", "--board", board, "list", "--json"], timeout=60)
        if code != 0:
            return [], f"kanban_unavailable: {raw.strip()}"
        try:
            data = json.loads(raw)
        except Exception as exc:
            return [], f"kanban_json_unreadable: {exc}"
    if isinstance(data, dict) and isinstance(data.get("tasks"), list):
        data = data["tasks"]
    if not isinstance(data, list):
        return [], "tasks_shape_unexpected"
    return [task for task in data if isinstance(task, dict)], None


def task_text(task: dict[str, Any]) -> str:
    values: list[str] = []
    for key in ("id", "title", "body", "result", "summary", "reason", "status", "current_step_key"):
        if task.get(key) is not None:
            values.append(str(task.get(key)))
    return "\n".join(values)


def path_safe(path: str) -> bool:
    lower = path.lower()
    if any(part in lower for part in SENSITIVE_PATH_PARTS):
        return False
    return path.startswith(SAFE_TV_PREFIXES)


def sensitive_path_check(paths: list[str]) -> dict[str, Any]:
    unsafe = [path for path in paths if not path_safe(path)]
    return {
        "status": "unsafe" if unsafe else "safe",
        "unsafe_paths": unsafe,
    }


def focused_verifier_status(text: str) -> str:
    lower = text.lower()
    if "focused" not in lower and "targeted" not in lower:
        return "missing"
    if any(term in lower for term in FOCUSED_PASS_TERMS):
        return "passed"
    if "failed" in lower or "failure" in lower:
        return "failed"
    return "missing"


def choose_handoff(tasks: list[dict[str, Any]], dirty_paths: list[str], assignee: str) -> tuple[dict[str, Any] | None, str, bool]:
    candidates: list[tuple[int, dict[str, Any], str]] = []
    for task in tasks:
        if task.get("assignee") != assignee:
            continue
        if task.get("status") not in {"blocked", "done", "running"}:
            continue
        text = task_text(task)
        lower = text.lower()
        if task.get("status") != "blocked" and not any(term in lower for term in REVIEW_TERMS):
            continue
        matched = sum(1 for path in dirty_paths if path.lower() in lower)
        if dirty_paths and matched == len(dirty_paths):
            candidates.append((int(task.get("created_at") or task.get("started_at") or 0), task, text))
    if not candidates:
        return None, "missing", False
    candidates.sort(key=lambda item: item[0], reverse=True)
    _, task, text = candidates[0]
    return task, focused_verifier_status(text), True


def classify(repo: Path, tasks: list[dict[str, Any]], *, tasks_json: Path | None = None, assignee: str = DEFAULT_ASSIGNEE) -> dict[str, Any]:
    exclude: set[Path] = set()
    if tasks_json is not None:
        try:
            exclude.add(tasks_json.resolve())
        except Exception:
            pass
    repo_state, dirty_paths, git_error = git_dirty_paths(repo, exclude)
    payload: dict[str, Any] = {
        "repo": str(repo),
        "repo_state": repo_state,
        "dirty_paths": dirty_paths,
        "candidate_handoff": None,
        "handoff_match": False,
        "sensitive_path_check": sensitive_path_check(dirty_paths),
        "focused_verifier_status": "not_applicable",
        "known_unrelated_failures": [],
        "active_worker": None,
        "recommended_action": "missing_handoff",
        "explicit_gate": None,
        "git_error": git_error,
    }

    if git_error:
        payload["recommended_action"] = "unsafe_dirty_state"
        payload["explicit_gate"] = "git_state_unreadable"
        return payload
    if repo_state == "clean":
        payload["recommended_action"] = "seed_successor"
        return payload
    if payload["sensitive_path_check"]["status"] != "safe":
        payload["recommended_action"] = "unsafe_dirty_state"
        payload["explicit_gate"] = "unsafe_dirty_state"
        return payload

    handoff, verifier_status, matched = choose_handoff(tasks, dirty_paths, assignee)
    payload["handoff_match"] = matched
    payload["focused_verifier_status"] = verifier_status
    if handoff:
        payload["candidate_handoff"] = {
            "id": handoff.get("id"),
            "title": handoff.get("title"),
            "status": handoff.get("status"),
            "assignee": handoff.get("assignee"),
        }
    if not matched:
        payload["recommended_action"] = "unsafe_dirty_state"
        payload["explicit_gate"] = "unsafe_dirty_state"
    elif verifier_status == "passed":
        payload["recommended_action"] = "checkpoint_and_push_ready"
        payload["explicit_gate"] = None
    elif verifier_status == "failed":
        payload["recommended_action"] = "rerun_focused_verifier"
        payload["explicit_gate"] = "rerun_focused_verifier"
    else:
        payload["recommended_action"] = "rerun_focused_verifier"
        payload["explicit_gate"] = "rerun_focused_verifier"
    return payload


def exit_code_for(payload: dict[str, Any]) -> int:
    return 0 if payload.get("recommended_action") in {"seed_successor", "checkpoint_and_push_ready", "push_ready"} else 1


def create_checkpoint(repo: Path, payload: dict[str, Any]) -> dict[str, Any]:
    """Create a local checkpoint commit for an already-classified safe dirty handoff."""
    if payload.get("recommended_action") != "checkpoint_and_push_ready":
        payload["checkpoint"] = {"created": False, "error": "not_checkpoint_ready"}
        return payload
    paths = list(payload.get("dirty_paths") or [])
    if not paths:
        payload["checkpoint"] = {"created": False, "error": "no_dirty_paths"}
        payload["recommended_action"] = "unsafe_dirty_state"
        payload["explicit_gate"] = "unsafe_dirty_state"
        return payload

    add = run_checked(["git", "add", "--", *paths], cwd=repo, timeout=30)
    if add[0] != 0:
        payload["checkpoint"] = {"created": False, "error": "git_add_failed", "output": add[1].strip()}
        payload["recommended_action"] = "unsafe_dirty_state"
        payload["explicit_gate"] = "unsafe_dirty_state"
        return payload
    diff_check = run_checked(["git", "diff", "--cached", "--check"], cwd=repo, timeout=30)
    if diff_check[0] != 0:
        run_checked(["git", "reset", "--", *paths], cwd=repo, timeout=30)
        payload["checkpoint"] = {"created": False, "error": "git_diff_check_failed", "output": diff_check[1].strip()}
        payload["recommended_action"] = "unsafe_dirty_state"
        payload["explicit_gate"] = "unsafe_dirty_state"
        return payload

    handoff_id = None
    if isinstance(payload.get("candidate_handoff"), dict):
        handoff_id = payload["candidate_handoff"].get("id")
    message = "checkpoint: recover TV worker handoff"
    if handoff_id:
        message += f" {handoff_id}"
    commit = run_checked(
        [
            "git",
            "-c",
            "user.name=TV Integration Owner",
            "-c",
            "user.email=tv-integration-owner@example.invalid",
            "commit",
            "-m",
            message,
        ],
        cwd=repo,
        timeout=60,
    )
    if commit[0] != 0:
        payload["checkpoint"] = {"created": False, "error": "git_commit_failed", "output": commit[1].strip()}
        payload["recommended_action"] = "unsafe_dirty_state"
        payload["explicit_gate"] = "unsafe_dirty_state"
        return payload
    commit_id = run_checked(["git", "rev-parse", "HEAD"], cwd=repo, timeout=15)[1].strip()
    payload["checkpoint"] = {
        "created": True,
        "commit": commit_id,
        "handoff_id": handoff_id,
        "staged_paths": paths,
        "message": message,
    }
    payload["recommended_action"] = "push_ready"
    payload["explicit_gate"] = None
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--tasks-json", type=Path, help="Optional Kanban list JSON file; defaults to hermes kanban list --json")
    parser.add_argument("--board", default=DEFAULT_BOARD)
    parser.add_argument("--assignee", default=DEFAULT_ASSIGNEE)
    parser.add_argument("--checkpoint", action="store_true", help="Create a local checkpoint commit when the dirty handoff is classified checkpoint_and_push_ready.")
    args = parser.parse_args()

    repo = args.repo.resolve()
    tasks, task_error = load_tasks(args.tasks_json, args.board)
    payload = classify(repo, tasks, tasks_json=args.tasks_json, assignee=args.assignee)
    if task_error:
        payload["task_source_warning"] = task_error
        if payload.get("repo_state") == "dirty" and payload.get("recommended_action") == "unsafe_dirty_state":
            payload["recommended_action"] = "missing_handoff"
            payload["explicit_gate"] = "missing_handoff"
    if args.checkpoint and not task_error:
        payload = create_checkpoint(repo, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return exit_code_for(payload)


if __name__ == "__main__":
    sys.exit(main())
