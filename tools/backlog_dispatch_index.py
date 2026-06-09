#!/usr/bin/env python3
"""Build and validate the EV Classic fidelity backlog dispatch index.

The markdown backlog is canonical.  The checked-in JSON index is a generated,
machine-readable dispatch surface for long-running agents and preflight checks.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

BACKLOG_RELATIVE_PATH = Path("docs/checklists/ev-classic-fidelity-implementation-backlog.md")
INDEX_RELATIVE_PATH = Path("docs/checklists/ev-classic-fidelity-implementation-backlog.index.json")
VERIFIER_IMPACT_MAP_RELATIVE_PATH = Path("docs/checklists/tv-verifier-impact-map.json")
PLAYABLE_MILESTONE_PRIORITY_MAP_RELATIVE_PATH = Path("docs/checklists/tv-playable-milestone-priority-map.json")
SCHEMA_VERSION = 1

REQUIRED_PLAYABLE_MILESTONES = (
    "playable_travel_loop",
    "mission_trade_loop",
    "landed_services_loop",
    "upgrade_ship_loop",
    "combat_survival_loop",
    "classic_promotion_backlog",
)

VALID_PLAYABLE_MILESTONE_PATHS = {
    "scaffold",
    "needs evidence",
    "fidelity-promoted",
}

REQUIRED_VERIFIER_IMPACT_SURFACES = (
    "extractor",
    "scenario",
    "godot_probe",
    "data_manifest",
    "backlog_dispatch_metadata",
    "docs_process_only",
)

REQUIRED_DISPATCH_FIELDS = (
    "next_action",
    "lane_class",
    "oracle_class",
    "source_basis",
    "verifier",
    "blocked_reason",
    "promotion_status",
)

VALID_ORACLE_CLASSES = {
    "combat-cadence",
    "static-resource",
    "runtime-ui",
    "runtime-behavior",
    "timing-feel",
    "tv-scaffold",
    "deterministic-evaluator",
    "manual-or-bible-guided",
    "manual-backed",
    "user-decision",
}

VALID_RISK_GATES = {
    "none",
    "original_runtime_non_mutating",
    "original_runtime_destructive",
    "external_action",
    "shared_checkout",
    "user_decision",
}

PATHISH_RE = re.compile(
    r"(?:^|\s)((?:\./|/)?(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+(?:\.[A-Za-z0-9_.-]+)?)"
)
FIELD_RE = re.compile(r"^\s{4}- `([a-z_]+)`: ?(.*)$")
STATUS_RE = re.compile(r"^\s{2}- Status: `?([^`\n]+)`?\s*$")
ITEM_RE = re.compile(r"^- \[([ xX])\] (.+?)\s*$")


@dataclasses.dataclass
class CheckResult:
    ok: bool
    errors: list[str]
    warnings: list[str]


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "item"


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _split_items(lines: list[str]) -> list[dict[str, Any]]:
    starts: list[tuple[int, str, str]] = []
    for index, line in enumerate(lines):
        match = ITEM_RE.match(line)
        if match:
            starts.append((index, match.group(1), match.group(2)))

    items: list[dict[str, Any]] = []
    for pos, (start, mark, title) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        items.append(
            {
                "checked": mark.lower() == "x",
                "title": title,
                "start_line": start + 1,
                "end_line": end,
                "lines": lines[start:end],
            }
        )
    return items


def _parse_status(block_lines: list[str]) -> str:
    for line in block_lines:
        match = STATUS_RE.match(line)
        if match:
            return match.group(1).strip()
    return ""


def _parse_dispatch_fields(block_lines: list[str]) -> dict[str, Any]:
    fields: dict[str, Any] = {}
    for line in block_lines:
        match = FIELD_RE.match(line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if key == "source_basis":
            fields[key] = _parse_source_basis(value)
        else:
            fields[key] = value
    return fields


def _parse_source_basis(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"\'') for part in inner.split(",") if part.strip()]
    if not value:
        return []
    return [value]


def _extract_backtick_text(block: str) -> list[str]:
    return re.findall(r"`([^`]+)`", block)


def _extract_pathish_surfaces(block: str, backlog_rel: str) -> list[str]:
    surfaces: set[str] = {backlog_rel}
    candidates: list[str] = []
    candidates.extend(_extract_backtick_text(block))
    candidates.extend(match.group(1) for match in PATHISH_RE.finditer(block))

    for candidate in candidates:
        for token in re.split(r"\s+|;|,", candidate):
            token = token.strip().strip("'\"()[]{}")
            if not token:
                continue
            if token.startswith("python3") or token in {"plus", "and", "or"}:
                continue
            if "/" not in token:
                continue
            token = token.removeprefix("./")
            token = token.rstrip(".:")
            if token.startswith("/home/"):
                # Local provenance/archive paths are not repo touched surfaces.
                continue
            if token.startswith("docs/") or token.startswith("tools/") or token.startswith("native_ev/") or token.startswith("godot_ev/") or token.endswith(".ps1"):
                surfaces.add(token)
    return sorted(surfaces)


def _derive_risk_gate(item: dict[str, Any], fields: dict[str, Any], block: str) -> str:
    text = "\n".join(
        [item["title"], item.get("status", ""), fields.get("next_action", ""), fields.get("blocked_reason", ""), block]
    ).lower()
    lane = str(fields.get("lane_class", "")).lower()

    if "destructive" in text or "disposable" in text:
        return "original_runtime_destructive"
    if "basilisk" in lane or "original-runtime" in text or "classic capture" in text or "classic player info" in text:
        return "original_runtime_non_mutating"
    if "external" in text or "public" in text or "publish" in text:
        return "external_action"
    if "user decision" in text or "user review" in text:
        return "user_decision"
    if "shared checkout" in text or "worktree" in text:
        return "shared_checkout"
    return "none"


def _active_unchecked_items(backlog_path: Path) -> list[dict[str, Any]]:
    lines = backlog_path.read_text().splitlines()
    return [item for item in _split_items(lines) if not item["checked"]]


def build_dispatch_index(backlog_path: Path, repo_root: Path | None = None) -> dict[str, Any]:
    repo_root = repo_root or Path.cwd()
    backlog_path = backlog_path.resolve()
    backlog_rel = _repo_relative(backlog_path, repo_root)
    items: list[dict[str, Any]] = []

    for item in _active_unchecked_items(backlog_path):
        block_lines = item["lines"]
        block = "\n".join(block_lines)
        fields = _parse_dispatch_fields(block_lines)
        status = _parse_status(block_lines)
        title = item["title"]
        item_id = slugify(title)
        body_hash = hashlib.sha256(block.encode("utf-8")).hexdigest()
        indexed = {
            "id": item_id,
            "title": title,
            "status": status,
            "next_action": fields.get("next_action", ""),
            "lane_class": fields.get("lane_class", ""),
            "oracle_class": fields.get("oracle_class", ""),
            "source_basis": fields.get("source_basis", []),
            "verifier": fields.get("verifier", ""),
            "blocked_reason": fields.get("blocked_reason", ""),
            "promotion_status": fields.get("promotion_status", ""),
            "risk_gate": _derive_risk_gate({**item, "status": status}, fields, block),
            "touched_surfaces": _extract_pathish_surfaces(block, backlog_rel),
            "markdown_anchor": f"#{item_id}",
            "line_range": [item["start_line"], item["end_line"]],
            "item_body_sha256": body_hash,
        }
        items.append(indexed)

    return {
        "schema_version": SCHEMA_VERSION,
        "source_path": backlog_rel,
        "generated_from": "markdown-backlog-derived; do not edit by hand",
        "item_count": len(items),
        "items": items,
    }


def load_playable_milestone_priority_map(map_path: Path) -> dict[str, Any]:
    return json.loads(map_path.read_text())


def validate_playable_milestone_priority_map(priority_map: dict[str, Any], dispatch_index: dict[str, Any]) -> CheckResult:
    errors: list[str] = []
    warnings: list[str] = []
    if priority_map.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"playable milestone priority map schema_version must be {SCHEMA_VERSION}")

    if not isinstance(priority_map.get("source_path"), str) or not priority_map.get("source_path"):
        errors.append("playable milestone priority map source_path must be a non-empty string")
    if not isinstance(priority_map.get("generated_from"), str) or not priority_map.get("generated_from"):
        errors.append("playable milestone priority map generated_from must be a non-empty string")
    if not isinstance(priority_map.get("selection_rule"), str) or not priority_map.get("selection_rule"):
        errors.append("playable milestone priority map selection_rule must be a non-empty string")

    milestones = priority_map.get("milestones")
    if not isinstance(milestones, list):
        errors.append("playable milestone priority map milestones must be a list")
        return CheckResult(ok=False, errors=errors, warnings=warnings)

    required = list(REQUIRED_PLAYABLE_MILESTONES)
    actual_ids = [m.get("milestone_id") if isinstance(m, dict) else None for m in milestones]
    if actual_ids != required:
        errors.append(f"playable milestone priority map milestone order must be {required!r}")

    ranks = [m.get("rank") if isinstance(m, dict) else None for m in milestones]
    expected_ranks = list(range(1, len(required) + 1))
    if ranks != expected_ranks:
        errors.append(f"playable milestone priority map ranks must be {expected_ranks!r}")

    index_items = {item.get("id"): item for item in dispatch_index.get("items", []) if isinstance(item, dict)}
    if not index_items:
        errors.append("dispatch index has no items for milestone backlog reference validation")

    for position, milestone in enumerate(milestones, start=1):
        if not isinstance(milestone, dict):
            errors.append(f"milestone {position}: entry must be an object")
            continue
        prefix = f"milestone {position} ({milestone.get('milestone_id', '<missing-id>')})"
        for key in (
            "milestone_id",
            "rank",
            "player_payoff",
            "current_path",
            "backlog_item_ids",
            "required_playable_capability",
            "acceptable_scaffold_boundary",
            "promotion_gate",
            "preferred_verifier_family",
            "notes",
        ):
            value = milestone.get(key)
            if value in (None, "", []):
                errors.append(f"{prefix}: missing {key}")

        current_path = milestone.get("current_path")
        if current_path and current_path not in VALID_PLAYABLE_MILESTONE_PATHS:
            errors.append(f"{prefix}: invalid current_path {current_path!r}")

        backlog_item_ids = milestone.get("backlog_item_ids")
        if not isinstance(backlog_item_ids, list):
            errors.append(f"{prefix}: backlog_item_ids must be a list")
            backlog_item_ids = []
        elif not all(isinstance(item_id, str) and item_id for item_id in backlog_item_ids):
            errors.append(f"{prefix}: backlog_item_ids values must be non-empty strings")

        for item_id in backlog_item_ids:
            if item_id not in index_items:
                errors.append(f"{prefix}: unknown backlog_item_id {item_id!r}")

        verifier_family = milestone.get("preferred_verifier_family")
        if not isinstance(verifier_family, list):
            errors.append(f"{prefix}: preferred_verifier_family must be a list")
        elif not all(isinstance(value, str) and value for value in verifier_family):
            errors.append(f"{prefix}: preferred_verifier_family values must be non-empty strings")

        if current_path == "fidelity-promoted":
            promoted_refs = [item_id for item_id in backlog_item_ids if index_items.get(item_id, {}).get("promotion_status") == "fidelity-promoted"]
            if not promoted_refs:
                errors.append(f"{prefix}: current_path fidelity-promoted requires at least one referenced backlog item with promotion_status fidelity-promoted")
            promotion_gate = str(milestone.get("promotion_gate", "")).lower()
            if "promotion" not in promotion_gate and "fidelity" not in promotion_gate and "evidence" not in promotion_gate:
                errors.append(f"{prefix}: fidelity-promoted milestone must name evidence/promotion in promotion_gate")

    return CheckResult(ok=not errors, errors=errors, warnings=warnings)


def _load_default_priority_map(repo_root: Path) -> dict[str, Any] | None:
    priority_map_path = repo_root / PLAYABLE_MILESTONE_PRIORITY_MAP_RELATIVE_PATH
    if not priority_map_path.exists():
        return None
    return load_playable_milestone_priority_map(priority_map_path)


def load_verifier_impact_map(map_path: Path) -> dict[str, Any]:
    return json.loads(map_path.read_text())


def validate_verifier_impact_map(impact_map: dict[str, Any]) -> CheckResult:
    errors: list[str] = []
    warnings: list[str] = []
    if impact_map.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"verifier impact map schema_version must be {SCHEMA_VERSION}")

    surfaces = impact_map.get("surfaces")
    if not isinstance(surfaces, dict):
        errors.append("verifier impact map surfaces must be an object")
        return CheckResult(ok=False, errors=errors, warnings=warnings)

    required = set(REQUIRED_VERIFIER_IMPACT_SURFACES)
    actual = set(surfaces)
    for missing in sorted(required - actual):
        errors.append(f"verifier impact map missing surface {missing!r}")
    for unknown in sorted(actual - required):
        errors.append(f"verifier impact map unknown surface {unknown!r}")

    for surface, entry in surfaces.items():
        prefix = f"verifier impact map surface {surface}"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}: entry must be an object")
            continue
        for key in ("cheap_required", "checkpoint_optional", "path_prefixes", "path_suffixes", "path_contains", "verifier_hints"):
            value = entry.get(key)
            if not isinstance(value, list):
                errors.append(f"{prefix}: {key} must be a list")
            elif key == "cheap_required" and not value:
                errors.append(f"{prefix}: cheap_required must not be empty")
            elif not all(isinstance(item, str) and item for item in value):
                errors.append(f"{prefix}: {key} values must be non-empty strings")
        if not isinstance(entry.get("notes"), str) or not entry.get("notes", "").strip():
            errors.append(f"{prefix}: notes must be a non-empty string")
        matchers = []
        for key in ("path_prefixes", "path_suffixes", "path_contains"):
            if isinstance(entry.get(key), list):
                matchers.extend(entry[key])
        if surface in required and not matchers:
            errors.append(f"{prefix}: at least one path matcher is required")

    return CheckResult(ok=not errors, errors=errors, warnings=warnings)


def _matching_verifier_surfaces(touched_surface: str, impact_map: dict[str, Any]) -> list[str]:
    matches: list[str] = []
    surfaces = impact_map.get("surfaces", {})
    for surface, entry in surfaces.items():
        if any(touched_surface.startswith(prefix) for prefix in entry.get("path_prefixes", [])):
            matches.append(surface)
            continue
        if any(touched_surface.endswith(suffix) for suffix in entry.get("path_suffixes", [])):
            matches.append(surface)
            continue
        if any(part in touched_surface for part in entry.get("path_contains", [])):
            matches.append(surface)
    return matches


def _load_default_impact_map(repo_root: Path) -> dict[str, Any] | None:
    impact_map_path = repo_root / VERIFIER_IMPACT_MAP_RELATIVE_PATH
    if not impact_map_path.exists():
        return None
    return load_verifier_impact_map(impact_map_path)


def validate_dispatch_index(index: dict[str, Any], impact_map: dict[str, Any] | None = None) -> CheckResult:
    errors: list[str] = []
    warnings: list[str] = []
    if index.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if index.get("item_count") != len(index.get("items", [])):
        errors.append("item_count does not match items length")

    if impact_map is not None:
        map_validation = validate_verifier_impact_map(impact_map)
        errors.extend(map_validation.errors)
        warnings.extend(map_validation.warnings)

    seen_ids: set[str] = set()
    for position, item in enumerate(index.get("items", []), start=1):
        prefix = f"item {position} ({item.get('id', '<missing-id>')})"
        item_id = item.get("id")
        if not item_id:
            errors.append(f"{prefix}: missing id")
        elif item_id in seen_ids:
            errors.append(f"{prefix}: duplicate id")
        else:
            seen_ids.add(item_id)

        for key in ("title", "status", *REQUIRED_DISPATCH_FIELDS, "risk_gate", "markdown_anchor", "line_range", "item_body_sha256"):
            value = item.get(key)
            if value in (None, "", []):
                errors.append(f"{prefix}: missing {key}")

        if item.get("oracle_class") and item["oracle_class"] not in VALID_ORACLE_CLASSES:
            warnings.append(f"{prefix}: non-standard oracle_class {item['oracle_class']!r}")
        if item.get("risk_gate") not in VALID_RISK_GATES:
            errors.append(f"{prefix}: invalid risk_gate {item.get('risk_gate')!r}")
        if item.get("verifier") in ("none", "n/a") and not item.get("blocked_reason"):
            errors.append(f"{prefix}: verifier is empty/none without blocked_reason")
        line_range = item.get("line_range")
        if not (isinstance(line_range, list) and len(line_range) == 2 and all(isinstance(v, int) for v in line_range)):
            errors.append(f"{prefix}: line_range must be [start, end]")
        touched_surfaces = item.get("touched_surfaces")
        if not isinstance(touched_surfaces, list):
            errors.append(f"{prefix}: touched_surfaces must be a list")
        elif impact_map is not None:
            if touched_surfaces and not item.get("verifier"):
                errors.append(f"{prefix}: missing verifier for actionable item with touched_surfaces")
            for touched_surface in touched_surfaces:
                if not isinstance(touched_surface, str) or not touched_surface:
                    errors.append(f"{prefix}: touched_surfaces values must be non-empty strings")
                    continue
                if not _matching_verifier_surfaces(touched_surface, impact_map):
                    errors.append(f"{prefix}: unmapped touched_surface {touched_surface!r}")

    return CheckResult(ok=not errors, errors=errors, warnings=warnings)


def write_dispatch_index(index: dict[str, Any], index_path: Path) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n")


def check_dispatch_index(backlog_path: Path, index_path: Path, repo_root: Path | None = None) -> CheckResult:
    repo_root = repo_root or Path.cwd()
    expected = build_dispatch_index(backlog_path, repo_root=repo_root)
    impact_map = _load_default_impact_map(repo_root)
    priority_map = _load_default_priority_map(repo_root)
    validation = validate_dispatch_index(expected, impact_map=impact_map)
    errors = list(validation.errors)
    warnings = list(validation.warnings)
    if priority_map is not None:
        priority_validation = validate_playable_milestone_priority_map(priority_map, expected)
        errors.extend(priority_validation.errors)
        warnings.extend(priority_validation.warnings)
    if not index_path.exists():
        errors.append(f"index missing: {index_path}")
        return CheckResult(ok=False, errors=errors, warnings=warnings)

    try:
        actual = json.loads(index_path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"index JSON parse failed: {exc}")
        return CheckResult(ok=False, errors=errors, warnings=warnings)

    actual_validation = validate_dispatch_index(actual, impact_map=impact_map)
    errors.extend(actual_validation.errors)
    warnings.extend(actual_validation.warnings)
    if actual != expected:
        errors.append("dispatch index is stale; run `python3 tools/backlog_dispatch_index.py build`")
    return CheckResult(ok=not errors, errors=errors, warnings=warnings)


def _print_result(result: CheckResult) -> None:
    for warning in result.warnings:
        print(f"WARNING: {warning}")
    if result.ok:
        print("BACKLOG DISPATCH INDEX OK")
    else:
        for error in result.errors:
            print(f"ERROR: {error}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "check", "print"), nargs="?", default="check")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--backlog", type=Path)
    parser.add_argument("--index", type=Path)
    args = parser.parse_args(argv)

    repo = args.repo.resolve()
    backlog = args.backlog or repo / BACKLOG_RELATIVE_PATH
    index = args.index or repo / INDEX_RELATIVE_PATH

    if args.mode == "build":
        built = build_dispatch_index(backlog, repo_root=repo)
        impact_map = _load_default_impact_map(repo)
        priority_map = _load_default_priority_map(repo)
        validation = validate_dispatch_index(built, impact_map=impact_map)
        if priority_map is not None:
            priority_validation = validate_playable_milestone_priority_map(priority_map, built)
            validation = CheckResult(
                ok=validation.ok and priority_validation.ok,
                errors=[*validation.errors, *priority_validation.errors],
                warnings=[*validation.warnings, *priority_validation.warnings],
            )
        if not validation.ok:
            _print_result(validation)
            return 1
        write_dispatch_index(built, index)
        print(f"wrote {index}")
        _print_result(validation)
        return 0
    if args.mode == "print":
        print(json.dumps(build_dispatch_index(backlog, repo_root=repo), indent=2, sort_keys=True))
        return 0

    result = check_dispatch_index(backlog, index, repo_root=repo)
    _print_result(result)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
