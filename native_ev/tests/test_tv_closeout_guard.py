import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
GUARD = REPO / "tools/tv_closeout_guard.py"


class TvCloseoutGuardTests(unittest.TestCase):
    def run_guard(self, packet: dict) -> tuple[int, dict]:
        with tempfile.TemporaryDirectory() as tmp:
            packet_path = Path(tmp) / "packet.json"
            packet_path.write_text(json.dumps(packet))
            result = subprocess.run(
                ["python3", str(GUARD), "--packet", str(packet_path)],
                cwd=REPO,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=30,
            )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise AssertionError(result.stdout) from exc
        return result.returncode, payload

    def test_rejects_generic_review_required_for_verified_safe_local_slice(self):
        code, payload = self.run_guard({
            "classification": "review-required",
            "summary": "verified safe-local code/docs changed; needs human review because files changed",
            "safe_local": True,
            "focused_verifiers_passed": True,
            "known_unrelated_failure_surface": "live owner topology tests failed separately",
            "changed_files": ["native_ev/scenario_eval.py", "native_ev/tests/test_scenario_eval.py"],
        })

        self.assertEqual(code, 2, payload)
        self.assertEqual(payload["decision"], "invalid")
        self.assertIn("generic_review_required_for_safe_local_work", payload["problems"])
        self.assertIn("continue", payload["allowed_closeout_classes"])
        self.assertIn("push_ready", payload["allowed_closeout_classes"])
        self.assertIn("blocked:*", payload["allowed_closeout_classes"])

    def test_accepts_explicit_human_gate_with_named_boundary(self):
        code, payload = self.run_guard({
            "classification": "blocked: explicit_human_gate",
            "safe_local": False,
            "human_gate_boundary": "destructive original-EV pilot mutation",
            "focused_verifiers_passed": True,
        })

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["decision"], "valid")

    def test_valid_push_ready_packet_requires_machine_contract_fields(self):
        code, payload = self.run_guard({
            "closeout_class": "push_ready",
            "kanban_task": "t_push",
            "changed_files": ["native_ev/scenario_eval.py", "native_ev/tests/test_scenario_eval.py"],
            "verification": {
                "focused": {
                    "command": "python3 -m unittest native_ev.tests.test_scenario_eval -v",
                    "result": "passed",
                },
                "diff_check": {
                    "command": "git diff --check",
                    "result": "passed",
                },
            },
            "next_action": "integration owner should checkpoint and publish this verified handoff",
            "event_ids": ["evt-1"],
            "successor_kanban_task": "t_next",
            "safe_local": True,
        })

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["decision"], "valid")
        self.assertEqual(payload["closeout_class"], "push_ready")
        self.assertEqual(payload["contract_version"], "machine_contract_v1")

    def test_rejects_push_ready_packet_missing_machine_contract_fields(self):
        code, payload = self.run_guard({
            "closeout_class": "push_ready",
            "task_id": "t_push",
            "changed_files": ["native_ev/scenario_eval.py"],
            "verification": {"focused": "passed"},
        })

        self.assertEqual(code, 2, payload)
        self.assertEqual(payload["decision"], "invalid")
        self.assertIn("missing_next_action", payload["problems"])
        self.assertIn("verification_missing_command_result", payload["problems"])

    def test_rejects_ready_for_review_or_integration_for_current_packets(self):
        code, payload = self.run_guard({
            "closeout_class": "ready_for_review_or_integration",
            "task_id": "t_review",
            "changed_files": ["native_ev/scenario_eval.py"],
            "verification": {
                "focused": {
                    "command": "python3 -m unittest native_ev.tests.test_scenario_eval -v",
                    "result": "passed",
                },
            },
            "next_action": "human review because files changed",
            "safe_local": True,
        })

        self.assertEqual(code, 2, payload)
        self.assertEqual(payload["decision"], "invalid")
        self.assertIn("ready_for_review_or_integration_not_current_contract", payload["problems"])

    def test_reports_schema_loose_timestamped_packets_as_legacy(self):
        code, payload = self.run_guard({
            "task_id": "t_legacy",
            "timestamp": "2026-06-13T20:43:25Z",
            "changed_files": ["native_ev/scenario_eval.py"],
            "verification": {
                "targeted_unittest": "passed; python3 -m unittest native_ev.tests.test_scenario_eval -v",
            },
            "completion_recommendation": "safe-local code/docs increment verified; ready for review/integration checkpoint",
        })

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["decision"], "legacy")
        self.assertIn("legacy_schema_without_closeout_class", payload["warnings"])


if __name__ == "__main__":
    unittest.main()
