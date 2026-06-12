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

GENERIC_REVIEW_TERMS = ("review-required", "review_required", "human review", "ready_for_review")


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


def validate(packet: dict[str, Any]) -> dict[str, Any]:
    classification = str(packet.get("classification") or packet.get("status") or "").strip()
    lower_classification = classification.lower()
    safe_local = bool(packet.get("safe_local"))
    focused_passed = bool(packet.get("focused_verifiers_passed") or packet.get("focused_verifier_passed"))
    human_boundary = str(packet.get("human_gate_boundary") or packet.get("explicit_human_gate") or "").strip()

    problems: list[str] = []
    warnings: list[str] = []

    if safe_local and focused_passed and has_generic_review(packet):
        problems.append("generic_review_required_for_safe_local_work")

    if lower_classification in {"continue", "push_ready"}:
        pass
    elif is_blocked_class(lower_classification):
        if lower_classification == HUMAN_GATE_CLASS and not human_boundary:
            problems.append("explicit_human_gate_missing_named_boundary")
    elif has_generic_review(packet):
        problems.append("generic_review_required_closeout_class")
    else:
        warnings.append("unknown_closeout_class")

    if packet.get("known_unrelated_failure_surface") and safe_local and focused_passed:
        warnings.append("known_unrelated_failure_surface_is_non_gating")

    return {
        "decision": "valid" if not problems else "invalid",
        "classification": classification,
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
    return 0 if payload.get("decision") == "valid" else 2


if __name__ == "__main__":
    sys.exit(main())
