import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from tools.backlog_dispatch_index import (
    REQUIRED_PLAYABLE_MILESTONES,
    REQUIRED_VERIFIER_IMPACT_SURFACES,
    build_dispatch_index,
    check_dispatch_index,
    load_playable_milestone_priority_map,
    load_verifier_impact_map,
    validate_dispatch_index,
    validate_playable_milestone_priority_map,
    validate_verifier_impact_map,
    write_dispatch_index,
)


SAMPLE_BACKLOG = textwrap.dedent(
    """
    # EV Classic fidelity implementation backlog

    ## Candidates / potential implementations

    - [ ] Fuller EV Classic galaxy topology and coordinates
      - Status: `needs evidence`
      - Dispatch fields:
        - `next_action`: Continue promoting the `syst-like` primitive run one field family at a time.
        - `lane_class`: Lane A: static galaxy topology semantics
        - `oracle_class`: static-resource
        - `source_basis`: [decoded-record-family, resource-bible-field]
        - `verifier`: `python3 tools/extract_ev_system_semantics.py` plus focused sourced-system manifest tests.
        - `blocked_reason`: Exact record-to-name/runtime topology mapping is not fully promoted.
        - `promotion_status`: needs evidence
      - Implementation: `tools/extract_ev_system_semantics.py` generates `native_ev/data/sourced_ev_systems.json`.
      - Verification: `python3 tools/run_gameplay_scenarios.py static_topology_source_readiness_scout --pretty`.
      - Next action: continue with coordinate display-unit/map-scaling interpretation.

    - [x] Completed historical item
      - Status: `verified`
      - Next action: none.
    """
).lstrip()


class BacklogDispatchIndexTests(unittest.TestCase):
    def test_build_dispatch_index_extracts_actionable_fields_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            backlog = root / "docs/checklists/ev-classic-fidelity-implementation-backlog.md"
            backlog.parent.mkdir(parents=True)
            backlog.write_text(SAMPLE_BACKLOG)

            index = build_dispatch_index(backlog, repo_root=root)

        self.assertEqual(index["schema_version"], 1)
        self.assertEqual(index["source_path"], "docs/checklists/ev-classic-fidelity-implementation-backlog.md")
        self.assertEqual(index["item_count"], 1)
        item = index["items"][0]
        self.assertEqual(item["id"], "fuller-ev-classic-galaxy-topology-and-coordinates")
        self.assertEqual(item["title"], "Fuller EV Classic galaxy topology and coordinates")
        self.assertEqual(item["status"], "needs evidence")
        self.assertEqual(item["lane_class"], "Lane A: static galaxy topology semantics")
        self.assertEqual(item["oracle_class"], "static-resource")
        self.assertEqual(item["source_basis"], ["decoded-record-family", "resource-bible-field"])
        self.assertEqual(item["promotion_status"], "needs evidence")
        self.assertEqual(item["risk_gate"], "none")
        self.assertIn("docs/checklists/ev-classic-fidelity-implementation-backlog.md", item["touched_surfaces"])
        self.assertIn("tools/extract_ev_system_semantics.py", item["touched_surfaces"])
        self.assertIn("native_ev/data/sourced_ev_systems.json", item["touched_surfaces"])
        self.assertEqual(item["markdown_anchor"], "#fuller-ev-classic-galaxy-topology-and-coordinates")
        self.assertEqual(item["line_range"][0], 5)
        self.assertRegex(item["item_body_sha256"], r"^[0-9a-f]{64}$")

    def test_check_dispatch_index_fails_when_checked_in_index_is_stale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            backlog = root / "docs/checklists/ev-classic-fidelity-implementation-backlog.md"
            index_path = root / "docs/checklists/ev-classic-fidelity-implementation-backlog.index.json"
            backlog.parent.mkdir(parents=True)
            backlog.write_text(SAMPLE_BACKLOG)
            write_dispatch_index(build_dispatch_index(backlog, repo_root=root), index_path)

            stale = json.loads(index_path.read_text())
            stale["items"][0]["next_action"] = "stale value"
            index_path.write_text(json.dumps(stale, indent=2) + "\n")

            result = check_dispatch_index(backlog, index_path, repo_root=root)

        self.assertFalse(result.ok)
        self.assertIn("stale", "\n".join(result.errors))

    def test_checked_in_verifier_impact_map_is_valid(self):
        repo = Path(__file__).resolve().parents[2]
        impact_map = load_verifier_impact_map(repo / "docs/checklists/tv-verifier-impact-map.json")

        result = validate_verifier_impact_map(impact_map)

        self.assertTrue(result.ok, result.errors)
        self.assertEqual(set(impact_map["surfaces"]), set(REQUIRED_VERIFIER_IMPACT_SURFACES))
        for surface in REQUIRED_VERIFIER_IMPACT_SURFACES:
            self.assertGreater(len(impact_map["surfaces"][surface]["cheap_required"]), 0)

    def test_validate_dispatch_index_rejects_unknown_touched_surface_when_map_is_loaded(self):
        index = {
            "schema_version": 1,
            "source_path": "docs/checklists/ev-classic-fidelity-implementation-backlog.md",
            "generated_from": "test",
            "item_count": 1,
            "items": [
                {
                    "id": "unknown-surface",
                    "title": "Unknown surface",
                    "status": "ready",
                    "next_action": "Touch an unmapped surface.",
                    "lane_class": "Lane E: deterministic evaluator/playtest packets",
                    "oracle_class": "tv-scaffold",
                    "source_basis": ["tv-scaffold"],
                    "verifier": "python3 tools/run_gameplay_scenarios.py smoke --pretty",
                    "blocked_reason": "none",
                    "promotion_status": "scaffold",
                    "risk_gate": "none",
                    "touched_surfaces": ["mystery/runtime/file.xyz"],
                    "markdown_anchor": "#unknown-surface",
                    "line_range": [1, 2],
                    "item_body_sha256": "a" * 64,
                }
            ],
        }
        impact_map = {
            "schema_version": 1,
            "surfaces": {
                surface: {
                    "cheap_required": ["focused verifier"],
                    "checkpoint_optional": [],
                    "path_prefixes": [],
                    "path_suffixes": [],
                    "path_contains": [],
                    "verifier_hints": ["focused verifier"],
                    "notes": "test",
                }
                for surface in REQUIRED_VERIFIER_IMPACT_SURFACES
            },
        }

        result = validate_dispatch_index(index, impact_map=impact_map)

        self.assertFalse(result.ok)
        self.assertIn("unmapped touched_surface", "\n".join(result.errors))

    def test_validate_dispatch_index_requires_verifier_for_actionable_items_with_touched_surfaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            backlog = root / "docs/checklists/ev-classic-fidelity-implementation-backlog.md"
            backlog.parent.mkdir(parents=True)
            backlog.write_text(SAMPLE_BACKLOG)
            index = build_dispatch_index(backlog, repo_root=root)
        index["items"][0]["verifier"] = ""
        impact_map = {
            "schema_version": 1,
            "surfaces": {
                surface: {
                    "cheap_required": ["focused verifier"],
                    "checkpoint_optional": [],
                    "path_prefixes": ["tools/", "native_ev/data/", "docs/"],
                    "path_suffixes": [],
                    "path_contains": [],
                    "verifier_hints": ["focused verifier"],
                    "notes": "test",
                }
                for surface in REQUIRED_VERIFIER_IMPACT_SURFACES
            },
        }

        result = validate_dispatch_index(index, impact_map=impact_map)

        self.assertFalse(result.ok)
        self.assertIn("missing verifier", "\n".join(result.errors))

    def test_checked_in_playable_milestone_priority_map_is_valid(self):
        repo = Path(__file__).resolve().parents[2]
        dispatch_index = json.loads((repo / "docs/checklists/ev-classic-fidelity-implementation-backlog.index.json").read_text())
        priority_map = load_playable_milestone_priority_map(repo / "docs/checklists/tv-playable-milestone-priority-map.json")

        result = validate_playable_milestone_priority_map(priority_map, dispatch_index)

        self.assertTrue(result.ok, result.errors)
        self.assertEqual([m["milestone_id"] for m in priority_map["milestones"]], list(REQUIRED_PLAYABLE_MILESTONES))
        self.assertEqual([m["rank"] for m in priority_map["milestones"]], [1, 2, 3, 4, 5, 6])

    def test_validate_playable_milestone_priority_map_rejects_unknown_backlog_item_ids(self):
        dispatch_index = {"schema_version": 1, "items": [{"id": "known-item", "promotion_status": "scaffold"}]}
        priority_map = {
            "schema_version": 1,
            "source_path": "docs/research/tv-spec.md",
            "generated_from": "test",
            "selection_rule": "test",
            "milestones": [
                {
                    "milestone_id": milestone,
                    "rank": rank,
                    "player_payoff": "payoff",
                    "current_path": "scaffold",
                    "backlog_item_ids": ["known-item"] if rank == 1 else ["missing-item"],
                    "required_playable_capability": "capability",
                    "acceptable_scaffold_boundary": "boundary",
                    "promotion_gate": "gate",
                    "preferred_verifier_family": ["verifier"],
                    "notes": "notes",
                }
                for rank, milestone in enumerate(REQUIRED_PLAYABLE_MILESTONES, start=1)
            ],
        }

        result = validate_playable_milestone_priority_map(priority_map, dispatch_index)

        self.assertFalse(result.ok)
        self.assertIn("unknown backlog_item_id", "\n".join(result.errors))

    def test_validate_playable_milestone_priority_map_rejects_unbacked_fidelity_promotion(self):
        dispatch_index = {"schema_version": 1, "items": [{"id": "known-item", "promotion_status": "scaffold"}]}
        priority_map = {
            "schema_version": 1,
            "source_path": "docs/research/tv-spec.md",
            "generated_from": "test",
            "selection_rule": "test",
            "milestones": [
                {
                    "milestone_id": milestone,
                    "rank": rank,
                    "player_payoff": "payoff",
                    "current_path": "fidelity-promoted" if rank == 1 else "scaffold",
                    "backlog_item_ids": ["known-item"],
                    "required_playable_capability": "capability",
                    "acceptable_scaffold_boundary": "boundary",
                    "promotion_gate": "gate",
                    "preferred_verifier_family": ["verifier"],
                    "notes": "notes",
                }
                for rank, milestone in enumerate(REQUIRED_PLAYABLE_MILESTONES, start=1)
            ],
        }

        result = validate_playable_milestone_priority_map(priority_map, dispatch_index)

        self.assertFalse(result.ok)
        self.assertIn("fidelity-promoted", "\n".join(result.errors))


if __name__ == "__main__":
    unittest.main()
