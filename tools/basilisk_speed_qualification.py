#!/usr/bin/env python3
"""Validate the Basilisk speed qualification artifact.

The artifact records which Basilisk acceleration settings are safe for specific
Terminal Velocity original-runtime evidence families.  It is intentionally a
small validator, not an emulator controller.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
from pathlib import Path
from typing import Any

DEFAULT_ARTIFACT = Path("docs/research/basilisk-speed-qualification.json")
SCHEMA_VERSION = 1

REQUIRED_ENTRY_FIELDS = (
    "evidence_family",
    "lane_id",
    "speed",
    "qualification_class",
    "sentinel_used",
    "verifier",
    "last_checked",
    "status",
    "restore_readiness",
    "capture_readiness",
    "input_readiness",
    "allowed_oracle_classes",
    "disallowed_oracle_classes",
    "promotion_limitations",
)

VALID_QUALIFICATION_CLASSES = {
    "promotion-grade timing",
    "promotion-grade non-timing",
    "scout-grade",
    "reject/unstable",
    "setup-incomplete",
}

VALID_STATUSES = {
    "qualified",
    "scout-only",
    "rejected",
    "setup-incomplete",
    "stale",
    "needs-requalification",
}

VALID_ORACLE_CLASSES = {
    "static-resource",
    "runtime-ui",
    "runtime-behavior",
    "timing-feel",
    "combat-cadence",
    "tv-scaffold",
    "manual-backed",
}

TIMING_SENSITIVE_CLASSES = {"timing-feel", "combat-cadence"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$|^unknown$")


@dataclasses.dataclass
class CheckResult:
    ok: bool
    errors: list[str]
    warnings: list[str]


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _has_1x_sentinel(value: Any) -> bool:
    return isinstance(value, str) and "1x" in value.lower() and value.strip().lower() not in {"none", "n/a"}


def validate_basilisk_speed_qualification(matrix: dict[str, Any]) -> CheckResult:
    errors: list[str] = []
    warnings: list[str] = []

    if matrix.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    entries = matrix.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be a list")
        return CheckResult(ok=False, errors=errors, warnings=warnings)

    seen_keys: set[tuple[str, str, str]] = set()
    for index, entry in enumerate(entries, start=1):
        prefix = f"entry {index} ({entry.get('evidence_family', '<missing-family>')}/{entry.get('lane_id', '<missing-lane>')}/{entry.get('speed', '<missing-speed>')})"
        if not isinstance(entry, dict):
            errors.append(f"entry {index}: must be an object")
            continue

        for field in REQUIRED_ENTRY_FIELDS:
            if field not in entry:
                errors.append(f"{prefix}: missing {field}")

        key = (str(entry.get("evidence_family", "")), str(entry.get("lane_id", "")), str(entry.get("speed", "")))
        if key in seen_keys:
            errors.append(f"{prefix}: duplicate evidence_family/lane_id/speed key")
        seen_keys.add(key)

        for field in (
            "evidence_family",
            "lane_id",
            "speed",
            "qualification_class",
            "sentinel_used",
            "verifier",
            "last_checked",
            "status",
            "restore_readiness",
            "capture_readiness",
            "input_readiness",
        ):
            if field in entry and not _is_non_empty_string(entry[field]):
                errors.append(f"{prefix}: {field} must be a non-empty string")

        qualification = entry.get("qualification_class")
        if qualification and qualification not in VALID_QUALIFICATION_CLASSES:
            errors.append(f"{prefix}: invalid qualification_class {qualification!r}")
        status = entry.get("status")
        if status and status not in VALID_STATUSES:
            errors.append(f"{prefix}: invalid status {status!r}")
        last_checked = entry.get("last_checked")
        if last_checked and not DATE_RE.match(str(last_checked)):
            errors.append(f"{prefix}: last_checked must be YYYY-MM-DD or unknown")

        allowed = entry.get("allowed_oracle_classes", [])
        disallowed = entry.get("disallowed_oracle_classes", [])
        limitations = entry.get("promotion_limitations", [])
        for field_name, value in (
            ("allowed_oracle_classes", allowed),
            ("disallowed_oracle_classes", disallowed),
            ("promotion_limitations", limitations),
        ):
            if field_name in entry and not (isinstance(value, list) and all(isinstance(v, str) and v.strip() for v in value)):
                errors.append(f"{prefix}: {field_name} must be a list of non-empty strings")

        unknown_allowed = set(allowed) - VALID_ORACLE_CLASSES if isinstance(allowed, list) else set()
        unknown_disallowed = set(disallowed) - VALID_ORACLE_CLASSES if isinstance(disallowed, list) else set()
        if unknown_allowed:
            warnings.append(f"{prefix}: non-standard allowed_oracle_classes {sorted(unknown_allowed)!r}")
        if unknown_disallowed:
            warnings.append(f"{prefix}: non-standard disallowed_oracle_classes {sorted(unknown_disallowed)!r}")

        timing_allowed = bool(isinstance(allowed, list) and TIMING_SENSITIVE_CLASSES.intersection(allowed))
        timing_qualification = qualification == "promotion-grade timing"
        if (timing_allowed or timing_qualification) and not _has_1x_sentinel(entry.get("sentinel_used")):
            errors.append(f"{prefix}: timing/combat permission requires an explicit 1x sentinel")

        if status in {"qualified", "scout-only"}:
            for readiness in ("restore_readiness", "capture_readiness", "input_readiness"):
                value = str(entry.get(readiness, "")).lower()
                if value in {"unknown", "none", "n/a", "setup-incomplete"}:
                    errors.append(f"{prefix}: {status} entry needs concrete {readiness}")
            if not limitations:
                errors.append(f"{prefix}: {status} entry needs promotion_limitations")

        if status == "qualified" and qualification in {"reject/unstable", "setup-incomplete"}:
            errors.append(f"{prefix}: qualified status conflicts with {qualification!r}")

    return CheckResult(ok=not errors, errors=errors, warnings=warnings)


def check_basilisk_speed_qualification(path: Path) -> CheckResult:
    if not path.exists():
        return CheckResult(ok=False, errors=[f"artifact missing: {path}"], warnings=[])
    try:
        matrix = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return CheckResult(ok=False, errors=[f"JSON parse failed: {exc}"], warnings=[])
    return validate_basilisk_speed_qualification(matrix)


def _print_result(result: CheckResult) -> None:
    for warning in result.warnings:
        print(f"WARNING: {warning}")
    if result.ok:
        print("BASILISK SPEED QUALIFICATION OK")
    else:
        for error in result.errors:
            print(f"ERROR: {error}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args(argv)
    result = check_basilisk_speed_qualification(args.path)
    _print_result(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
