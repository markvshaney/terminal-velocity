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
import shutil
import subprocess
import sys
import time
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


def git_dirty_entries(repo: Path, exclude: set[Path]) -> tuple[list[dict[str, str]], str | None]:
    code, raw = run_checked(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, timeout=15)
    if code != 0:
        return [], raw.strip() or "git status failed"
    entries: list[dict[str, str]] = []
    for line in raw.splitlines():
        if not line:
            continue
        status = line[:2]
        status_path = line[3:] if len(line) > 3 else ""
        if " -> " in status_path:
            status_path = status_path.split(" -> ", 1)[1]
        full = (repo / status_path).resolve()
        if full in exclude:
            continue
        entries.append({"status": status, "path": status_path})
    return sorted(entries, key=lambda item: item["path"]), None


def git_dirty_paths(repo: Path, exclude: set[Path]) -> tuple[str, list[str], str | None]:
    entries, error = git_dirty_entries(repo, exclude)
    if error:
        return "unknown", [], error
    paths = [entry["path"] for entry in entries]
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
    return "\n".join(text for _, text in task_evidence_texts(task))


def _comment_text(comment: Any) -> str:
    if isinstance(comment, str):
        return comment
    if not isinstance(comment, dict):
        return ""
    values: list[str] = []
    for key in ("body", "content", "text", "summary", "result"):
        if comment.get(key) is not None:
            values.append(str(comment.get(key)))
    return "\n".join(values)


def task_evidence_texts(task: dict[str, Any]) -> list[tuple[str, str]]:
    """Return ordered handoff evidence text surfaces for a Kanban task.

    Recovery must prefer the places where workers actually leave structured
    closeout evidence. Task-list prose remains a fallback; comments and latest
    summaries are first-class sources when present in task JSON.
    """
    surfaces: list[tuple[str, str]] = []
    latest_summary = task.get("latest_summary")
    if latest_summary is not None:
        surfaces.append(("kanban_latest_summary", str(latest_summary)))
    comments = task.get("comments")
    if isinstance(comments, list):
        comment_values = [_comment_text(comment) for comment in comments]
        comment_text = "\n".join(value for value in comment_values if value)
        if comment_text:
            surfaces.append(("kanban_comment", comment_text))
    task_values: list[str] = []
    for key in ("id", "title", "body", "result", "summary", "reason", "status", "current_step_key"):
        if task.get(key) is not None:
            task_values.append(str(task.get(key)))
    if task_values:
        surfaces.append(("kanban_task_text", "\n".join(task_values)))
    return surfaces


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


def closeout_packet_text(packet: dict[str, Any]) -> str:
    values: list[str] = []
    for key in ("task_id", "summary", "successor_recommendation", "evidence_boundary"):
        if packet.get(key) is not None:
            values.append(str(packet.get(key)))
    verification = packet.get("verification")
    if isinstance(verification, dict):
        values.extend(f"{key}: {value}" for key, value in verification.items())
    return "\n".join(values)


def load_closeout_packets(repo: Path) -> list[dict[str, Any]]:
    packet_root = repo / ".hermes/long-running/tv-spec-implementation"
    packets: list[dict[str, Any]] = []
    for path in sorted(packet_root.glob("closeout-packet-*.json")):
        try:
            packet = json.loads(path.read_text())
        except Exception:
            continue
        if not isinstance(packet, dict):
            continue
        changed_files = packet.get("changed_files")
        if not isinstance(changed_files, list):
            continue
        normalized_files = [str(item) for item in changed_files if isinstance(item, str) and item]
        if not normalized_files:
            continue
        packet["_path"] = str(path.relative_to(repo))
        packet["_changed_files"] = sorted(set(normalized_files))
        packet["_text"] = closeout_packet_text(packet)
        packets.append(packet)
    return packets


def dirty_match(dirty_paths: list[str], evidence_paths: set[str]) -> tuple[bool, dict[str, list[str]]]:
    dirty_set = set(dirty_paths)
    return dirty_set == evidence_paths, {
        "matched_paths": sorted(dirty_set & evidence_paths),
        "missing_from_evidence": sorted(dirty_set - evidence_paths),
        "extra_in_evidence": sorted(evidence_paths - dirty_set),
    }


def choose_handoff(
    repo: Path,
    tasks: list[dict[str, Any]],
    dirty_paths: list[str],
    assignee: str,
) -> tuple[dict[str, Any] | None, str, bool, list[str], dict[str, list[str]]]:
    packets = load_closeout_packets(repo)
    packets_by_task_id: dict[str, list[dict[str, Any]]] = {}
    for packet in packets:
        task_id = packet.get("task_id")
        if task_id is not None:
            packets_by_task_id.setdefault(str(task_id), []).append(packet)

    candidates: list[tuple[int, dict[str, Any], str, list[str], dict[str, list[str]]]] = []
    empty_match = {"matched_paths": [], "missing_from_evidence": dirty_paths, "extra_in_evidence": []}
    for task in tasks:
        if task.get("assignee") != assignee:
            continue
        if task.get("status") not in {"blocked", "done", "running"}:
            continue
        evidence_surfaces = task_evidence_texts(task)
        text = "\n".join(surface_text for _, surface_text in evidence_surfaces)
        lower = text.lower()
        if task.get("status") != "blocked" and not any(term in lower for term in REVIEW_TERMS):
            continue

        task_evidence_paths: set[str] = set()
        sources: list[str] = []
        evidence_text_parts: list[str] = []
        for source, surface_text in evidence_surfaces:
            source_paths = {path for path in dirty_paths if path.lower() in surface_text.lower()}
            if source_paths or (source == "kanban_latest_summary" and focused_verifier_status(surface_text) != "missing"):
                if source not in sources:
                    sources.append(source)
                evidence_text_parts.append(surface_text)
            task_evidence_paths.update(source_paths)
        matched, match_detail = dirty_match(dirty_paths, task_evidence_paths)
        evidence_text = "\n".join(evidence_text_parts) if evidence_text_parts else text

        if not matched:
            for packet in packets_by_task_id.get(str(task.get("id")), []):
                packet_paths = set(packet["_changed_files"])
                packet_matched, packet_match_detail = dirty_match(dirty_paths, packet_paths)
                if packet_matched:
                    matched = True
                    match_detail = packet_match_detail
                    evidence_text = text + "\n" + str(packet.get("_text") or "")
                    sources = ["closeout_packet"]
                    if task_evidence_paths:
                        sources.insert(0, "kanban_task_text")
                    break
                if len(packet_match_detail["matched_paths"]) > len(match_detail["matched_paths"]):
                    match_detail = packet_match_detail

        if dirty_paths and matched:
            candidates.append((int(task.get("created_at") or task.get("started_at") or 0), task, evidence_text, sources, match_detail))
        elif match_detail["matched_paths"] and not candidates:
            empty_match = match_detail
    if not candidates:
        return None, "missing", False, [], empty_match
    candidates.sort(key=lambda item: item[0], reverse=True)
    _, task, text, sources, match_detail = candidates[0]
    return task, focused_verifier_status(text), True, sources, match_detail


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
        "handoff_evidence_sources": [],
        "handoff_dirty_path_match": {
            "matched_paths": [],
            "missing_from_evidence": dirty_paths,
            "extra_in_evidence": [],
        },
        "matched_changed_files": [],
        "missing_changed_files": dirty_paths,
        "extra_dirty_paths": [],
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

    handoff, verifier_status, matched, evidence_sources, match_detail = choose_handoff(repo, tasks, dirty_paths, assignee)
    payload["handoff_match"] = matched
    payload["handoff_evidence_sources"] = evidence_sources
    payload["handoff_dirty_path_match"] = match_detail
    payload["matched_changed_files"] = match_detail["matched_paths"]
    payload["missing_changed_files"] = match_detail["extra_in_evidence"]
    payload["extra_dirty_paths"] = match_detail["missing_from_evidence"]
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


def path_has_sensitive_terms(path: str) -> bool:
    return any(part in path.lower() for part in SENSITIVE_PATH_PARTS)


def empty_parent_dirs_until_repo(repo: Path, path: Path) -> None:
    current = path.parent
    repo = repo.resolve()
    while current != repo and repo in current.parents:
        try:
            current.rmdir()
        except OSError:
            return
        current = current.parent


def repair_unsafe_debris(repo: Path, tasks: list[dict[str, Any]], *, tasks_json: Path | None, assignee: str, quarantine_root: Path) -> dict[str, Any]:
    """Move only clearly non-sensitive untracked non-project debris, then reclassify."""
    payload = classify(repo, tasks, tasks_json=tasks_json, assignee=assignee)
    payload["repair"] = {
        "attempted": True,
        "action": "not_needed",
        "moved_paths": [],
        "blocked_paths": [],
        "quarantine_root": str(quarantine_root),
    }
    if payload.get("recommended_action") != "unsafe_dirty_state":
        return payload

    exclude: set[Path] = set()
    if tasks_json is not None:
        try:
            exclude.add(tasks_json.resolve())
        except Exception:
            pass
    entries, error = git_dirty_entries(repo, exclude)
    if error:
        payload["repair"]["action"] = "not_repairable"
        payload["repair"]["error"] = error
        return payload

    movable: list[str] = []
    blocked: list[str] = []
    for entry in entries:
        path = entry["path"]
        status = entry["status"]
        if status == "??" and not path_safe(path) and not path_has_sensitive_terms(path):
            movable.append(path)
        else:
            blocked.append(path)

    if blocked or not movable:
        payload["repair"]["action"] = "not_repairable"
        payload["repair"]["blocked_paths"] = sorted(blocked or [entry["path"] for entry in entries])
        return payload

    quarantine_id = f"tv-unsafe-debris-{int(time.time())}"
    quarantine_dir = quarantine_root / quarantine_id
    moved: list[str] = []
    try:
        for path in sorted(movable):
            source = repo / path
            destination = quarantine_dir / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            empty_parent_dirs_until_repo(repo, source)
            moved.append(path)
    except Exception as exc:
        payload["repair"]["action"] = "repair_failed"
        payload["repair"]["error"] = str(exc)
        payload["repair"]["moved_paths"] = moved
        payload["repair"]["quarantine_id"] = quarantine_id
        return payload

    payload["repair"].update({
        "action": "moved_untracked_debris",
        "moved_paths": moved,
        "quarantine_id": quarantine_id,
    })
    post = classify(repo, tasks, tasks_json=tasks_json, assignee=assignee)
    payload["post_repair"] = post
    payload["repo_state"] = post.get("repo_state")
    payload["dirty_paths"] = post.get("dirty_paths")
    payload["recommended_action"] = post.get("recommended_action")
    payload["explicit_gate"] = post.get("explicit_gate")
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
    parser.add_argument("--repair-unsafe-debris", action="store_true", help="Move clearly non-sensitive untracked non-project debris out of the repo and reclassify instead of stopping at unsafe_dirty_state.")
    parser.add_argument("--quarantine-root", type=Path, default=Path("/home/bh/.hermes/profiles/loki-game/unsafe-dirty-quarantine"), help="Directory where repaired untracked debris is preserved outside the worktree.")
    args = parser.parse_args()

    repo = args.repo.resolve()
    tasks, task_error = load_tasks(args.tasks_json, args.board)
    if args.repair_unsafe_debris and not task_error:
        payload = repair_unsafe_debris(repo, tasks, tasks_json=args.tasks_json, assignee=args.assignee, quarantine_root=args.quarantine_root.resolve())
    else:
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
