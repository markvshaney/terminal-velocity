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


if __name__ == "__main__":
    unittest.main()
