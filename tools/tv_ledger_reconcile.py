#!/usr/bin/env python3
"""Normalize the TV long-running task ledger to provenance-only form.

Dry-run is the default and is side-effect-free. With --write, this command
rewrites only .hermes/long-running/tv-spec-implementation/task-ledger.json to a
schema that preserves durable provenance, policy, event/closeout pointers, and
resume hints. It deliberately removes mutable live-status fields; live runner
truth is derived from Kanban, topology, git, and process state at preflight time.
It never starts workers, mutates Kanban, commits, or pushes.
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
TASK_DIR = Path(".hermes/long-running/tv-spec-implementation")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_error": str(exc), "_path": str(path)}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_checked(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None, timeout: int = 45) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            cmd,
            cwd=cwd,
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


def is_control_projection_path(path: str) -> bool:
    return path == str(TASK_DIR / "task-ledger.json") or path == str(TASK_DIR / "events.jsonl") or (
        path.startswith(str(TASK_DIR / "closeout-packet-")) and path.endswith(".json")
    ) or (
        path.startswith(str(TASK_DIR / "event-")) and path.endswith(".json")
    )


def git_info(repo: Path) -> dict[str, Any]:
    head_code, head = run_checked(["git", "rev-parse", "HEAD"], cwd=repo, timeout=15)
    status_code, status = run_checked(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, timeout=15)
    all_dirty_paths: list[str] = []
    dirty_paths: list[str] = []
    if status_code == 0:
        for line in status.splitlines():
            if not line:
                continue
            path = line[3:] if len(line) > 3 else ""
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            all_dirty_paths.append(path)
            if not is_control_projection_path(path):
                dirty_paths.append(path)
    return {
        "head": head.strip() if head_code == 0 else None,
        "head_error": None if head_code == 0 else head.strip(),
        "dirty_paths": sorted(dirty_paths),
        "all_dirty_paths": sorted(all_dirty_paths),
        "ignored_control_projection_paths": sorted(set(all_dirty_paths) - set(dirty_paths)),
        "status_error": None if status_code == 0 else status.strip(),
        "repo_state": "dirty" if dirty_paths else "clean",
    }


def run_topology(repo: Path, profile: Path) -> dict[str, Any]:
    env = os.environ.copy()
    env.update({"TV_TOPOLOGY_REPO": str(repo), "TV_TOPOLOGY_PROFILE": str(profile)})
    checker = DEFAULT_REPO / "tools/check_tv_runner_topology.py"
    code, raw = run_checked(
        ["python3", str(checker), "--startup-owner", "gateway_kanban_dispatcher"],
        cwd=repo,
        env=env,
        timeout=60,
    )
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = {"ok": False, "topology_conflict": True, "raw_output": raw}
    payload["exit_code"] = code
    return payload


def event_key(event: dict[str, Any]) -> tuple[str, str]:
    timestamp = str(event.get("timestamp") or event.get("updated_at") or "")
    event_id = str(event.get("event_id") or event.get("id") or "")
    return timestamp, event_id


def load_events(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    events: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    if not path.exists():
        return events, errors
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append({"line": str(idx), "error": str(exc)})
            continue
        if isinstance(event, dict):
            events.append(event)
    events.sort(key=event_key)
    return events, errors


def closeout_text(packet: dict[str, Any]) -> str:
    values: list[str] = []
    for key in ("timestamp", "task_id", "summary", "next_action", "successor_recommendation"):
        if packet.get(key) is not None:
            values.append(str(packet.get(key)))
    return "\n".join(values)


def load_closeout_packets(repo: Path) -> list[dict[str, Any]]:
    root = repo / TASK_DIR
    packets: list[dict[str, Any]] = []
    for path in sorted(root.glob("closeout-packet-*.json")):
        packet = read_json(path, None)
        if not isinstance(packet, dict) or packet.get("_error"):
            continue
        changed_files = packet.get("changed_files")
        if not isinstance(changed_files, list):
            continue
        changed = sorted(str(item) for item in changed_files if isinstance(item, str) and item)
        if not changed:
            continue
        packet = dict(packet)
        packet["_path"] = str(path.relative_to(repo))
        packet["_changed_files"] = changed
        packet["_sort_key"] = str(packet.get("timestamp") or packet.get("updated_at") or path.name)
        packet["_text"] = closeout_text(packet)
        packets.append(packet)
    packets.sort(key=lambda item: (str(item.get("_sort_key") or ""), str(item.get("_path") or "")))
    return packets


def latest_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    return events[-1] if events else None


def newest_matching_packet(packets: list[dict[str, Any]], dirty_paths: list[str]) -> dict[str, Any] | None:
    dirty_set = set(dirty_paths)
    if not dirty_set:
        return packets[-1] if packets else None
    matches = [packet for packet in packets if set(packet.get("_changed_files") or []) == dirty_set]
    return matches[-1] if matches else None


def handoff_from(event: dict[str, Any] | None, packet: dict[str, Any] | None, dirty_paths: list[str]) -> dict[str, Any] | None:
    if packet is not None:
        changed_files = list(packet.get("_changed_files") or [])
        return {
            "task_id": packet.get("task_id"),
            "event_id": packet.get("event_id"),
            "timestamp": packet.get("timestamp") or packet.get("updated_at"),
            "changed_files": changed_files,
            "matched_dirty_paths": sorted(set(changed_files) & set(dirty_paths)),
            "closeout_packet": packet.get("_path"),
            "verification": packet.get("verification") or {},
            "summary": packet.get("summary"),
        }
    if event is not None:
        changed_files = event.get("changed_files") if isinstance(event.get("changed_files"), list) else event.get("artifacts_touched")
        return {
            "task_id": event.get("kanban_task") or event.get("task_id"),
            "event_id": event.get("event_id") or event.get("id"),
            "timestamp": event.get("timestamp") or event.get("updated_at"),
            "changed_files": changed_files if isinstance(changed_files, list) else [],
            "matched_dirty_paths": sorted(set(changed_files or []) & set(dirty_paths)) if isinstance(changed_files, list) else [],
            "closeout_packet": event.get("closeout_packet"),
            "verification": event.get("verification") or event.get("tests") or {},
            "summary": event.get("summary") or event.get("behavior_claim"),
        }
    return None


def isoish(value: Any) -> str:
    return str(value or "")


def build_projection(repo: Path, profile: Path) -> dict[str, Any]:
    task_dir = repo / TASK_DIR
    ledger_path = task_dir / "task-ledger.json"
    events_path = task_dir / "events.jsonl"
    current_ledger = read_json(ledger_path, {})
    events, event_errors = load_events(events_path)
    packets = load_closeout_packets(repo)
    latest = latest_event(events)
    git = git_info(repo)
    topology = run_topology(repo, profile)
    live_owner = topology.get("live_implementation_owner") or "unknown"
    matching_packet = newest_matching_packet(packets, git["dirty_paths"])
    handoff = handoff_from(latest, matching_packet, git["dirty_paths"])

    classifications: list[str] = []
    ledger_updated = isoish(current_ledger.get("updated_at")) if isinstance(current_ledger, dict) else ""
    latest_event_time = isoish(latest.get("timestamp") or latest.get("updated_at")) if latest else ""
    if latest_event_time and (not ledger_updated or latest_event_time > ledger_updated):
        classifications.append("ledger_projection_stale")
    ledger_owner = None
    if isinstance(current_ledger, dict):
        runner_ownership = current_ledger.get("runner_ownership") if isinstance(current_ledger.get("runner_ownership"), dict) else {}
        ledger_owner = current_ledger.get("declared_owner") or runner_ownership.get("implementation_owner")
        ledger_status = str(current_ledger.get("status") or "").lower()
    else:
        runner_ownership = {}
        ledger_status = ""
    if ledger_owner and ledger_owner != live_owner and ledger_status not in {"", "stopped", "paused", "stopped_by_user"}:
        classifications.append("ledger_historical_owner_mismatch")
    if git["repo_state"] == "dirty":
        if matching_packet is not None:
            classifications.append("dirty_handoff_pending")
        else:
            classifications.append("unsafe_dirty_state")
    if topology.get("topology_conflict"):
        classifications.append("live_owner_conflict")
    if event_errors:
        classifications.append("events_jsonl_parse_errors")
    classifications = sorted(set(classifications))

    if "live_owner_conflict" in classifications:
        live_state_class = "blocked_live_owner_conflict"
        active_gate = {"type": "live_owner_conflict", "topology_conflicts": topology.get("conflict_types") or []}
    elif "unsafe_dirty_state" in classifications:
        live_state_class = "blocked_unsafe_dirty_state"
        active_gate = {"type": "unsafe_dirty_state", "dirty_paths": git["dirty_paths"]}
    elif "dirty_handoff_pending" in classifications:
        live_state_class = "push_ready_recovery"
        active_gate = {"type": "dirty_handoff_pending", "dirty_paths": git["dirty_paths"]}
    elif "ledger_projection_stale" in classifications or "ledger_historical_owner_mismatch" in classifications:
        live_state_class = "waiting_integration_recovery"
        active_gate = None
    else:
        live_state_class = "idle_clean"
        active_gate = None

    planned = {
        "schema_version": 3,
        "task_id": "tv-spec-implementation",
        "scope": "Terminal Velocity long-running implementation provenance. This ledger is not a live runner status source.",
        "runtime_truth_rule": "Live runner state is derived from Kanban/topology/git/processes, not this ledger.",
        "policy": {
            "valid_closeout_classes": ["continue", "push_ready", "blocked:<concrete_reason>"],
            "generic_review_required_allowed": False,
        },
        "evidence_pointers": current_ledger.get("evidence_pointers", {}) if isinstance(current_ledger, dict) else {},
        "latest_worker_handoff": handoff,
        "resume_hint": {
            "text": current_ledger.get("next_resume_action") if isinstance(current_ledger, dict) else None,
            "not_authoritative": True,
        },
        "historical_notes": {
            "classifications": classifications,
            "event_parse_errors": event_errors,
        },
        "diagnostics": {
            "live_state_class_at_reconcile_time": live_state_class,
            "active_gate_at_reconcile_time": active_gate,
            "generated_from": {
                "command": "tools/tv_ledger_reconcile.py",
                "events_jsonl": str(events_path.relative_to(repo)),
                "event_count": len(events),
                "latest_event_id": (latest or {}).get("event_id") or (latest or {}).get("id"),
                "closeout_packets": [packet.get("_path") for packet in packets],
                "matching_closeout_packet": matching_packet.get("_path") if matching_packet else None,
                "topology": {
                    "live_implementation_owner": live_owner,
                    "warning_types": topology.get("warning_types") or [],
                    "conflict_types": topology.get("conflict_types") or [],
                },
                "git": git,
            },
        },
    }
    if latest_event_time:
        planned["updated_at"] = latest_event_time
    elif isinstance(current_ledger, dict) and current_ledger.get("updated_at"):
        planned["updated_at"] = current_ledger.get("updated_at")

    changed = planned != current_ledger
    recommended = "none"
    if changed:
        recommended = "write_normalized_provenance"
    payload = {
        "repo": str(repo),
        "profile": str(profile),
        "ledger_path": str(ledger_path),
        "classifications": classifications,
        "source_delta": {
            "ledger_updated_at": ledger_updated or None,
            "latest_event_time": latest_event_time or None,
            "ledger_differs_from_projection": changed,
            "dirty_paths": git["dirty_paths"],
            "matching_closeout_packet": matching_packet.get("_path") if matching_packet else None,
        },
        "recommended_action": recommended,
        "planned_projection": planned,
        "write_applied": False,
    }
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--write", action="store_true", help="Rewrite task-ledger.json with the normalized projection")
    args = parser.parse_args(argv)

    repo = args.repo.resolve()
    profile = args.profile.resolve()
    payload = build_projection(repo, profile)
    if args.write:
        write_json(Path(payload["ledger_path"]), payload["planned_projection"])
        payload["write_applied"] = True
        payload["recommended_action"] = "none"
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if args.write or payload["recommended_action"] == "none" else 1


if __name__ == "__main__":
    sys.exit(main())
