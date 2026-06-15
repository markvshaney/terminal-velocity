#!/usr/bin/env python3
"""Narrow Terminal Velocity Kanban progress-report bridge.

This script is reporting-only: it snapshots material Kanban task transitions and
optionally sends one concise message via the loki-game Hermes profile. It does
not dispatch, implement, commit, push, or schedule work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

DEFAULT_REPO = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE_NAME = "loki-game"
DEFAULT_BOARD = "terminal-velocity"
STATE_PATH = Path(".hermes/long-running/tv-spec-implementation/progress-report-state.json")
MATERIAL_STATUSES = {"running", "blocked", "done"}


def run(cmd: list[str], *, cwd: Path | None = None, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"reported_fingerprints": []}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return {"reported_fingerprints": []}
    if not isinstance(data, dict):
        return {"reported_fingerprints": []}
    data.setdefault("reported_fingerprints", [])
    return data


def write_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def extract_tasks(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        raw_tasks = payload
    elif isinstance(payload, dict):
        raw_tasks = payload.get("tasks") or payload.get("items") or payload.get("rows") or []
    else:
        raw_tasks = []
    return [dict(item) for item in raw_tasks if isinstance(item, dict)]


def normalize_task(task: dict[str, Any]) -> dict[str, Any]:
    body = str(task.get("body") or task.get("summary") or task.get("result") or "")
    result = str(task.get("result") or "")
    status = str(task.get("status") or "")
    gate = None
    text = f"{body}\n{result}".lower()
    if "push_ready" in text or "push ready" in text:
        gate = "push_ready"
    elif "review-required" in text or "review_required" in text or "review required" in text:
        gate = "review_required_process_bug"
    elif "unsafe_dirty_state" in text:
        gate = "unsafe_dirty_state"
    elif "verifier_failed" in text:
        gate = "verifier_failed"
    elif status == "blocked":
        gate = "blocked"
    return {
        "id": str(task.get("id") or ""),
        "title": str(task.get("title") or ""),
        "status": status,
        "assignee": str(task.get("assignee") or ""),
        "run_id": task.get("run_id"),
        "worker_pid": task.get("worker_pid"),
        "gate": gate,
        "result": result,
        "completed_at": task.get("completed_at"),
        "started_at": task.get("started_at"),
    }


def snapshot_from_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    normalized = [normalize_task(task) for task in tasks]
    interesting = [
        task for task in normalized
        if task["id"] and (task["status"] in MATERIAL_STATUSES or task.get("gate"))
    ]
    interesting.sort(key=lambda item: item["id"])
    return {
        "schema_version": 1,
        "captured_at": int(time.time()),
        "tasks": {task["id"]: task for task in interesting},
    }


def material_transitions(previous: dict[str, Any], current: dict[str, Any]) -> list[dict[str, Any]]:
    prev_tasks = previous.get("tasks") or {}
    curr_tasks = current.get("tasks") or {}
    baseline_empty = not bool(prev_tasks)
    now = int(time.time())
    recent_window_seconds = int(os.environ.get("TV_PROGRESS_RECENT_WINDOW_SECONDS", "7200"))
    transitions: list[dict[str, Any]] = []
    for task_id, task in sorted(curr_tasks.items()):
        prev = prev_tasks.get(task_id) or {}
        status = task.get("status")
        gate = task.get("gate")
        completed_at = task.get("completed_at") or 0
        recently_completed = bool(completed_at and now - int(completed_at) <= recent_window_seconds)
        if baseline_empty and status == "done" and not recently_completed:
            # First reporter invocation establishes a baseline; do not replay the
            # whole historical board as progress. Current/recent closeouts and
            # active gates still surface so a late-started reporter does not miss
            # the material handoff that triggered it.
            continue
        if not prev and status == "running":
            kind = "worker_claimed"
        elif not prev and gate == "push_ready":
            kind = "worker_push_ready"
        elif not prev and gate == "review_required_process_bug":
            kind = "worker_contract_violation"
        elif prev.get("status") != status and status == "running":
            kind = "worker_claimed"
        elif prev.get("gate") != gate and gate == "push_ready":
            kind = "worker_push_ready"
        elif prev.get("gate") != gate and gate == "review_required_process_bug":
            kind = "worker_contract_violation"
        elif prev.get("status") != status and status == "done":
            kind = "task_done"
        elif prev.get("status") != status and status == "blocked":
            kind = "explicit_gate"
        else:
            continue
        transitions.append({"kind": kind, "task": task})
    return transitions


def fingerprint(transitions: list[dict[str, Any]]) -> str:
    stable = [
        {
            "kind": item.get("kind"),
            "id": (item.get("task") or {}).get("id"),
            "status": (item.get("task") or {}).get("status"),
            "gate": (item.get("task") or {}).get("gate"),
            "completed_at": (item.get("task") or {}).get("completed_at"),
            "started_at": (item.get("task") or {}).get("started_at"),
        }
        for item in transitions
    ]
    return hashlib.sha256(json.dumps(stable, sort_keys=True).encode()).hexdigest()[:16]


def build_message(transitions: list[dict[str, Any]]) -> str:
    lines = ["TV Kanban progress"]
    labels = {
        "worker_claimed": "worker claimed",
        "worker_push_ready": "worker push_ready",
        "worker_contract_violation": "worker closeout contract violation",
        "task_done": "task done",
        "explicit_gate": "explicit gate/blocker",
    }
    for item in transitions[:8]:
        task = item["task"]
        title = task.get("title") or "untitled"
        suffix = ""
        if task.get("gate"):
            suffix = f" gate={task['gate']}"
        if task.get("assignee"):
            suffix += f" assignee={task['assignee']}"
        lines.append(f"- {labels.get(item['kind'], item['kind'])}: `{task['id']}` — {title}{suffix}")
    if len(transitions) > 8:
        lines.append(f"- plus {len(transitions) - 8} more material transition(s)")
    return "\n".join(lines)


def read_kanban_tasks(profile_name: str, board: str) -> list[dict[str, Any]]:
    result = run(["hermes", "-p", profile_name, "kanban", "--board", board, "list", "--json"])
    if result.returncode != 0:
        raise RuntimeError(result.stdout)
    return extract_tasks(json.loads(result.stdout))


def deliver(profile_name: str, target: str, message: str, *, dry_run: bool) -> dict[str, Any]:
    if dry_run:
        return {"status": "dry_run", "target": target, "message": message}
    result = run(["hermes", "-p", profile_name, "send", "--json", "--to", target], input_text=message)
    if result.returncode != 0:
        return {"status": "failed", "target": target, "output": result.stdout}
    return {"status": "sent", "target": target, "output": result.stdout}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(os.environ.get("TV_PROGRESS_REPO", DEFAULT_REPO)))
    parser.add_argument("--profile-name", default=os.environ.get("TV_PROGRESS_PROFILE", DEFAULT_PROFILE_NAME))
    parser.add_argument("--board", default=os.environ.get("TV_PROGRESS_BOARD", DEFAULT_BOARD))
    parser.add_argument("--target", default=os.environ.get("TV_PROGRESS_TARGET"), help="Hermes send target; omit for snapshot/report JSON only")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Report even if fingerprint was already delivered")
    parser.add_argument("--state-path", type=Path, default=None)
    args = parser.parse_args()

    repo = args.repo.resolve()
    state_path = args.state_path or (repo / STATE_PATH)
    state = load_state(state_path)
    previous = state.get("last_snapshot") or {"tasks": {}}
    current = snapshot_from_tasks(read_kanban_tasks(args.profile_name, args.board))
    transitions = material_transitions(previous, current)
    fp = fingerprint(transitions) if transitions else None
    reported = set(str(item) for item in state.get("reported_fingerprints") or [])
    should_report = bool(transitions) and (args.force or fp not in reported)

    payload: dict[str, Any] = {
        "schema_version": 1,
        "should_report": should_report,
        "transition_count": len(transitions),
        "fingerprint": fp,
        "transitions": transitions,
        "delivery": {"status": "skipped", "reason": "no_target_or_no_material_transition"},
    }
    if should_report:
        message = build_message(transitions)
        payload["message"] = message
        if args.target:
            payload["delivery"] = deliver(args.profile_name, args.target, message, dry_run=bool(args.dry_run))
            if payload["delivery"].get("status") in {"sent", "dry_run"} and fp:
                reported.add(fp)
        elif fp:
            reported.add(fp)

    state["last_snapshot"] = current
    state["reported_fingerprints"] = sorted(reported)[-100:]
    if not args.dry_run:
        write_state(state_path, state)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["delivery"].get("status") != "failed" else 2


if __name__ == "__main__":
    sys.exit(main())
