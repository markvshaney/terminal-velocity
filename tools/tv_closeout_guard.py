#!/usr/bin/env python3
"""Validate Terminal Velocity worker closeout classifications.

The guard is intentionally narrow: it prevents the known bad closeout class where
verified safe-local TV work is blocked as generic human review simply because
files changed, a worker lacks push authority, or an unrelated broad verifier is
red. It does not decide fidelity truth or publish anything.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ALLOWED_CLOSEOUT_CLASSES = ["continue", "push_ready", "blocked:*"]
HUMAN_GATE_CLASS = "blocked: explicit_human_gate"
CONTRACT_VERSION = "machine_contract_v1"

GENERIC_REVIEW_TERMS = ("review-required", "review_required", "human review", "ready_for_review")
RETIRED_REVIEW_CLASSES = {"ready_for_review", "ready_for_review_or_integration", "review-required", "review_required"}


def load_packet(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("packet must be a JSON object")
    return data


def has_generic_review(packet: dict[str, Any]) -> bool:
    text = " ".join(
        str(packet.get(key, ""))
        for key in ("classification", "status", "summary", "reason", "active_gate", "next_resume_action")
    ).lower()
    return any(term in text for term in GENERIC_REVIEW_TERMS)


def is_blocked_class(value: str) -> bool:
    return value == HUMAN_GATE_CLASS or value.startswith("blocked:")


def packet_task_id(packet: dict[str, Any]) -> str:
    return str(packet.get("kanban_task") or packet.get("task_id") or "").strip()


def changed_files_valid(packet: dict[str, Any]) -> bool:
    changed_files = packet.get("changed_files")
    return isinstance(changed_files, list) and all(isinstance(item, str) and item for item in changed_files) and bool(changed_files)


def verification_is_machine_contract(verification: Any) -> bool:
    if not isinstance(verification, dict) or not verification:
        return False
    for item in verification.values():
        if not isinstance(item, dict):
            return False
        command = str(item.get("command") or "").strip()
        result = str(item.get("result") or item.get("status") or "").strip()
        if not command or not result:
            return False
    return True


def verification_has_pass(packet: dict[str, Any]) -> bool:
    if packet.get("focused_verifiers_passed") or packet.get("focused_verifier_passed"):
        return True
    verification = packet.get("verification")
    if not isinstance(verification, dict):
        return False
    for item in verification.values():
        if isinstance(item, dict) and str(item.get("result") or item.get("status") or "").lower() == "passed":
            return True
        if isinstance(item, str) and "passed" in item.lower():
            return True
    return False


def is_legacy_packet(packet: dict[str, Any]) -> bool:
    return not packet.get("closeout_class") and bool(packet.get("timestamp")) and changed_files_valid(packet)


def validate(packet: dict[str, Any]) -> dict[str, Any]:
    classification = str(packet.get("closeout_class") or packet.get("classification") or packet.get("status") or "").strip()
    lower_classification = classification.lower()
    safe_local = bool(packet.get("safe_local"))
    focused_passed = verification_has_pass(packet)
    human_boundary = str(packet.get("human_gate_boundary") or packet.get("explicit_human_gate") or "").strip()

    problems: list[str] = []
    warnings: list[str] = []

    if is_legacy_packet(packet):
        warnings.append("legacy_schema_without_closeout_class")
        return {
            "decision": "legacy",
            "contract_version": "legacy_schema",
            "closeout_class": classification,
            "classification": classification,
            "task_id": packet_task_id(packet),
            "allowed_closeout_classes": ALLOWED_CLOSEOUT_CLASSES,
            "problems": [],
            "warnings": sorted(set(warnings)),
            "next_action": "legacy closeout packet accepted as historical evidence; new packets must use machine_contract_v1",
        }

    current_contract = bool(packet.get("closeout_class"))

    if safe_local and focused_passed and has_generic_review(packet):
        problems.append("generic_review_required_for_safe_local_work")

    if lower_classification in RETIRED_REVIEW_CLASSES:
        problems.append("ready_for_review_or_integration_not_current_contract")
    elif lower_classification in {"continue", "push_ready"}:
        pass
    elif is_blocked_class(lower_classification):
        if lower_classification == HUMAN_GATE_CLASS and not human_boundary:
            problems.append("explicit_human_gate_missing_named_boundary")
    elif has_generic_review(packet):
        problems.append("generic_review_required_closeout_class")
    else:
        if current_contract:
            problems.append("unknown_closeout_class")
        else:
            warnings.append("unknown_closeout_class")

    if current_contract:
        if not packet_task_id(packet):
            problems.append("missing_task_id")
        if not changed_files_valid(packet):
            problems.append("missing_changed_files")
        if not verification_is_machine_contract(packet.get("verification")):
            problems.append("verification_missing_command_result")
        if not str(packet.get("next_action") or "").strip():
            problems.append("missing_next_action")
        event_ids = packet.get("event_ids")
        if event_ids is not None and not (isinstance(event_ids, list) and all(isinstance(item, str) and item for item in event_ids)):
            problems.append("event_ids_must_be_string_list")

    if packet.get("known_unrelated_failure_surface") and safe_local and focused_passed:
        warnings.append("known_unrelated_failure_surface_is_non_gating")

    return {
        "decision": "valid" if not problems else "invalid",
        "contract_version": CONTRACT_VERSION if current_contract else "legacy_freeform",
        "closeout_class": classification,
        "classification": classification,
        "task_id": packet_task_id(packet),
        "allowed_closeout_classes": ALLOWED_CLOSEOUT_CLASSES,
        "problems": sorted(set(problems)),
        "warnings": sorted(set(warnings)),
        "next_action": (
            "Use continue, push_ready, or blocked:<concrete_reason>; reserve blocked: explicit_human_gate for named destructive/external/config/publication-risk boundaries."
            if problems
            else "closeout classification accepted"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, required=True, help="JSON packet describing the worker closeout classification")
    args = parser.parse_args()

    try:
        packet = load_packet(args.packet)
        payload = validate(packet)
    except Exception as exc:
        payload = {
            "decision": "invalid",
            "allowed_closeout_classes": ALLOWED_CLOSEOUT_CLASSES,
            "problems": ["packet_unreadable"],
            "error": str(exc),
        }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload.get("decision") in {"valid", "legacy"} else 2


if __name__ == "__main__":
    sys.exit(main())
