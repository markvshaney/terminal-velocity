import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
REPORTER = REPO / "tools/tv_kanban_progress_report.py"
_SPEC = importlib.util.spec_from_file_location("tv_kanban_progress_report", REPORTER)
assert _SPEC and _SPEC.loader
reporter = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(reporter)


class TvKanbanProgressReportTests(unittest.TestCase):
    def test_material_transitions_reports_claim_push_ready_contract_violation_and_done(self):
        previous = {
            "tasks": {
                "t_done": {"id": "t_done", "status": "running", "gate": None},
                "t_push": {"id": "t_push", "status": "running", "gate": None},
                "t_review": {"id": "t_review", "status": "running", "gate": None},
            }
        }
        current = {
            "tasks": {
                "t_claim": {"id": "t_claim", "title": "new worker", "status": "running", "gate": None, "assignee": "terminal-velocity"},
                "t_done": {"id": "t_done", "title": "integrated", "status": "done", "gate": None, "assignee": "loki-game"},
                "t_push": {"id": "t_push", "title": "worker handoff", "status": "blocked", "gate": "push_ready", "assignee": "terminal-velocity"},
                "t_review": {"id": "t_review", "title": "bad handoff", "status": "blocked", "gate": "review_required_process_bug", "assignee": "terminal-velocity"},
            }
        }

        transitions = reporter.material_transitions(previous, current)

        self.assertEqual(
            [item["kind"] for item in transitions],
            ["worker_claimed", "task_done", "worker_push_ready", "worker_contract_violation"],
        )
        message = reporter.build_message(transitions)
        self.assertIn("TV Kanban progress", message)
        self.assertIn("worker push_ready", message)
        self.assertIn("worker closeout contract violation", message)

    def test_progress_message_describes_pushed_bundle_contents(self):
        transitions = [
            {
                "kind": "worker_push_ready",
                "task": {
                    "id": "t_bundle",
                    "title": "worker handoff",
                    "status": "done",
                    "gate": "push_ready",
                    "assignee": "terminal-velocity",
                    "bundle_summary": "push_ready: Added service/store evidence packet intake triage.",
                    "changed_files": ["tools/extract.py", "native_ev/model.py", "native_ev/tests/test_model.py", "docs/backlog.md", "extra.json"],
                    "verification": {"extractor": "passed", "focused_tests": "passed"},
                    "closeout_packet": ".hermes/long-running/tv-spec-implementation/closeout-packet-t_bundle.json",
                },
            }
        ]

        message = reporter.build_message(transitions)

        self.assertIn("bundle: Added service/store evidence packet intake triage.", message)
        self.assertIn("files: tools/extract.py, native_ev/model.py, native_ev/tests/test_model.py, docs/backlog.md, +1 more", message)
        self.assertIn("verified: extractor, focused_tests", message)
        self.assertIn("closeout: `.hermes/long-running/tv-spec-implementation/closeout-packet-t_bundle.json`", message)

    def test_enrich_transition_bundles_reads_kanban_show_metadata(self):
        original = reporter.read_kanban_task_detail
        try:
            reporter.read_kanban_task_detail = lambda _profile, _board, _task_id: {
                "latest_summary": "push_ready: Added bundle summary from worker.",
                "runs": [
                    {
                        "metadata": {
                            "changed_files": ["native_ev/model.py"],
                            "verification": {"focused_tests": "passed"},
                            "closeout_packet": "packet.json",
                        }
                    }
                ],
            }
            enriched = reporter.enrich_transition_bundles(
                "loki-game",
                "terminal-velocity",
                [{"kind": "worker_push_ready", "task": {"id": "t1", "title": "handoff"}}],
            )
        finally:
            reporter.read_kanban_task_detail = original

        task = enriched[0]["task"]
        self.assertEqual(task["bundle_summary"], "push_ready: Added bundle summary from worker.")
        self.assertEqual(task["changed_files"], ["native_ev/model.py"])
        self.assertEqual(task["verification"], {"focused_tests": "passed"})
        self.assertEqual(task["closeout_packet"], "packet.json")

    def test_first_snapshot_does_not_replay_historical_done_tasks_but_keeps_recent_closeout(self):
        now = int(reporter.time.time())
        current = {
            "tasks": {
                "t_old": {"id": "t_old", "title": "old", "status": "done", "gate": "push_ready", "completed_at": now - 99_999},
                "t_recent": {"id": "t_recent", "title": "recent handoff", "status": "done", "gate": "push_ready", "completed_at": now - 60},
                "t_run": {"id": "t_run", "title": "current", "status": "running", "gate": None},
                "t_gate": {"id": "t_gate", "title": "ready handoff", "status": "ready", "gate": "push_ready"},
            }
        }

        transitions = reporter.material_transitions({"tasks": {}}, current)

        self.assertEqual([item["task"]["id"] for item in transitions], ["t_gate", "t_recent", "t_run"])
        self.assertEqual([item["kind"] for item in transitions], ["worker_push_ready", "worker_push_ready", "worker_claimed"])

    def test_snapshot_state_dedupes_by_fingerprint_without_scheduling_or_dispatching(self):
        transitions = [{"kind": "worker_claimed", "task": {"id": "t1", "status": "running", "gate": None, "started_at": 1}}]
        fp = reporter.fingerprint(transitions)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state.json"
            reporter.write_state(path, {"reported_fingerprints": [fp], "last_snapshot": {"tasks": {}}})
            state = reporter.load_state(path)

        self.assertIn(fp, state["reported_fingerprints"])
        self.assertNotIn("dispatch", json.dumps(state).lower())
        self.assertNotIn("push", json.dumps(state).lower())


if __name__ == "__main__":
    unittest.main()
