import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools/tv_ledger_reconcile.py"


class TvLedgerReconcileTests(unittest.TestCase):
    def make_fixture(self) -> tuple[tempfile.TemporaryDirectory, Path, Path, Path]:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        repo = root / "repo"
        profile = root / "profile"
        task_dir = repo / ".hermes/long-running/tv-spec-implementation"
        task_dir.mkdir(parents=True)
        (profile / "cron").mkdir(parents=True)
        (profile / "run").mkdir(parents=True)
        (profile / "config.yaml").write_text("kanban:\n  dispatch_in_gateway: true\n")
        (profile / "cron/jobs.json").write_text(json.dumps({"jobs": []}) + "\n")
        (profile / "processes.json").write_text("[]\n")
        (profile / "run/tv_kanban_continuous_loop_state.json").write_text(json.dumps({"last_state": "stopped"}) + "\n")
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        (repo / "README.md").write_text("fixture\n")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run([
            "git",
            "-c",
            "user.name=TV Test",
            "-c",
            "user.email=tv-test@example.invalid",
            "commit",
            "-q",
            "-m",
            "fixture baseline",
        ], cwd=repo, check=True)
        return tmp, repo, profile, task_dir

    def run_reconcile(self, repo: Path, profile: Path, *args: str) -> tuple[int, dict]:
        result = subprocess.run(
            ["python3", str(SCRIPT), "--repo", str(repo), "--profile", str(profile), *args],
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

    def test_dry_run_reports_stale_projection_without_inventing_live_owner(self):
        _, repo, profile, task_dir = self.make_fixture()
        ledger = {
            "schema_version": 1,
            "task_id": "tv-spec-implementation",
            "status": "running",
            "declared_owner": "continuous_kanban_runner",
            "runner_ownership": {"implementation_owner": "continuous_kanban_runner"},
            "updated_at": "2026-06-13T10:00:00Z",
        }
        (task_dir / "task-ledger.json").write_text(json.dumps(ledger) + "\n")
        (task_dir / "events.jsonl").write_text(json.dumps({
            "event_id": "evt-newer",
            "timestamp": "2026-06-13T11:00:00Z",
            "event": "slice_completed",
            "kanban_task": "t_new",
            "changed_files": ["README.md"],
        }) + "\n")

        code, payload = self.run_reconcile(repo, profile)

        self.assertEqual(code, 1, payload)
        self.assertFalse(payload["write_applied"])
        self.assertIn("ledger_projection_stale", payload["classifications"])
        self.assertIn("ledger_historical_owner_mismatch", payload["classifications"])
        self.assertEqual(payload["recommended_action"], "write_normalized_projection")
        planned = payload["planned_projection"]
        self.assertEqual(planned["runner_ownership"]["implementation_owner"], "none_active")
        self.assertEqual(planned["status"], "waiting_integration_recovery")
        self.assertEqual(planned["latest_worker_handoff"]["event_id"], "evt-newer")
        self.assertEqual(planned["generated_from"]["topology"]["live_implementation_owner"], "none_active")
        self.assertEqual(json.loads((task_dir / "task-ledger.json").read_text()), ledger)

    def test_write_normalizes_projection_and_newest_matching_closeout_packet_wins(self):
        _, repo, profile, task_dir = self.make_fixture()
        (repo / "native_ev").mkdir()
        (repo / "native_ev/scenario_eval.py").write_text("dirty\n")
        (task_dir / "task-ledger.json").write_text(json.dumps({
            "schema_version": 1,
            "task_id": "tv-spec-implementation",
            "status": "running",
            "runner_ownership": {"implementation_owner": "none_active"},
            "updated_at": "2026-06-13T09:00:00Z",
        }) + "\n")
        (task_dir / "events.jsonl").write_text(json.dumps({
            "event_id": "evt-old",
            "timestamp": "2026-06-13T09:30:00Z",
            "kanban_task": "t_old",
            "changed_files": ["README.md"],
        }) + "\n" + json.dumps({
            "event_id": "evt-new",
            "timestamp": "2026-06-13T10:30:00Z",
            "kanban_task": "t_new",
            "changed_files": ["native_ev/scenario_eval.py"],
        }) + "\n")
        (task_dir / "closeout-packet-t_old.json").write_text(json.dumps({
            "task_id": "t_old",
            "timestamp": "2026-06-13T09:30:00Z",
            "changed_files": ["README.md"],
            "verification": {"targeted": "passed"},
        }) + "\n")
        (task_dir / "closeout-packet-t_new.json").write_text(json.dumps({
            "task_id": "t_new",
            "timestamp": "2026-06-13T10:30:00Z",
            "changed_files": ["native_ev/scenario_eval.py"],
            "verification": {"targeted": "passed"},
        }) + "\n")

        code, payload = self.run_reconcile(repo, profile, "--write")

        self.assertEqual(code, 0, payload)
        self.assertTrue(payload["write_applied"])
        self.assertIn("dirty_handoff_pending", payload["classifications"])
        planned = payload["planned_projection"]
        self.assertEqual(planned["status"], "push_ready_recovery")
        self.assertEqual(planned["latest_worker_handoff"]["task_id"], "t_new")
        self.assertEqual(planned["latest_worker_handoff"]["closeout_packet"], ".hermes/long-running/tv-spec-implementation/closeout-packet-t_new.json")
        self.assertEqual(planned["latest_worker_handoff"]["matched_dirty_paths"], ["native_ev/scenario_eval.py"])
        written = json.loads((task_dir / "task-ledger.json").read_text())
        self.assertEqual(written, planned)


if __name__ == "__main__":
    unittest.main()
