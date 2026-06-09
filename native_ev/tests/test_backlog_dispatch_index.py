import json
import tempfile
import textwrap
import unittest
from pathlib import Path

from tools.backlog_dispatch_index import (
    build_dispatch_index,
    check_dispatch_index,
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


if __name__ == "__main__":
    unittest.main()
