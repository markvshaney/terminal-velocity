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
import subprocess
import sys
from pathlib import Path
from typing import Any


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


def blocked_cards(topology: dict[str, Any]) -> dict[str, Any]:
    # Keep this wrapper read-only and bounded. The topology checker already names
    # Kanban DB candidates and live owners; blocked-card detail can be added as a
    # later ledger/Kanban normalization layer without weakening start safety.
    return {
        "status": "not_inspected_detail",
        "source": "topology_paths",
        "kanban_db_candidates": (topology.get("paths") or {}).get("kanban_db_candidates", []),
    }


def classify(repo: Path, profile: Path, startup_owner: str) -> dict[str, Any]:
    repo_state, dirty_paths, git_error = git_state(repo)
    topology_code, topology = run_topology(repo, profile, startup_owner)
    stop_lock = stop_lock_state(repo, profile)
    capability = capability_check(repo)
    live_owner = topology.get("live_implementation_owner")

    payload: dict[str, Any] = {
        "repo": str(repo),
        "profile": str(profile),
        "startup_owner": startup_owner,
        "repo_state": repo_state,
        "dirty_paths": dirty_paths,
        "git_error": git_error,
        "topology": topology,
        "topology_exit_code": topology_code,
        "blocked_cards": blocked_cards(topology),
        "stop_lock_state": stop_lock,
        "watchdog_reporter_state": watchdog_reporter_state(repo, profile),
        "capability_check": capability,
        "safe_to_start": False,
        "recommended_action": "blocked:unknown",
        "explicit_gate": "unknown",
    }

    if git_error:
        payload["recommended_action"] = "blocked:git_state_unreadable"
        payload["explicit_gate"] = "git_state_unreadable"
    elif repo_state == "dirty":
        payload["recommended_action"] = "recover_dirty_handoff"
        payload["explicit_gate"] = "recovery_preflight_required"
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
