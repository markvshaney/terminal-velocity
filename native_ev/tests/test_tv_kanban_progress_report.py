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
