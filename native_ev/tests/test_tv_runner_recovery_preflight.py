import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools/tv_runner_recovery_preflight.py"


class TvRunnerRecoveryPreflightTests(unittest.TestCase):
    def make_repo(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        return root

    def run_preflight(self, repo: Path, tasks: list[dict], *extra_args: str) -> tuple[int, dict]:
        tasks_path = repo / "tasks.json"
        tasks_path.write_text(json.dumps(tasks))
        result = subprocess.run(
            ["python3", str(SCRIPT), "--repo", str(repo), "--tasks-json", str(tasks_path), *extra_args],
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

    def test_clean_idle_repo_recommends_seed_successor(self):
        repo = self.make_repo()

        code, payload = self.run_preflight(repo, [])

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["repo_state"], "clean")
        self.assertEqual(payload["dirty_paths"], [])
        self.assertEqual(payload["recommended_action"], "seed_successor")
        self.assertIsNone(payload["explicit_gate"])

    def test_unexplained_dirty_repo_is_unsafe_dirty_state(self):
        repo = self.make_repo()
        (repo / "native_ev").mkdir()
        (repo / "native_ev/scenario_eval.py").write_text("dirty\n")

        code, payload = self.run_preflight(repo, [])

        self.assertEqual(code, 1, payload)
        self.assertEqual(payload["repo_state"], "dirty")
        self.assertEqual(payload["dirty_paths"], ["native_ev/scenario_eval.py"])
        self.assertEqual(payload["recommended_action"], "unsafe_dirty_state")
        self.assertEqual(payload["explicit_gate"], "unsafe_dirty_state")
        self.assertFalse(payload["handoff_match"])

    def test_matching_blocked_handoff_with_focused_pass_recommends_checkpoint(self):
        repo = self.make_repo()
        (repo / "native_ev/tests").mkdir(parents=True)
        (repo / "native_ev/scenario_eval.py").write_text("dirty\n")
        (repo / "native_ev/tests/test_scenario_eval.py").write_text("dirty\n")
        tasks = [{
            "id": "t_recover",
            "status": "blocked",
            "assignee": "terminal-velocity",
            "title": "Continue TV tv-spec autonomous loop",
            "body": "Changed files: native_ev/scenario_eval.py, native_ev/tests/test_scenario_eval.py. Focused verifier passed: python3 -m unittest native_ev.tests.test_scenario_eval -v. Known unrelated failure surface: live owner topology tests.",
        }]

        code, payload = self.run_preflight(repo, tasks)

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["repo_state"], "dirty")
        self.assertEqual(payload["recommended_action"], "checkpoint_and_push_ready")
        self.assertTrue(payload["handoff_match"])
        self.assertEqual(payload["candidate_handoff"]["id"], "t_recover")
        self.assertEqual(payload["focused_verifier_status"], "passed")
        self.assertIsNone(payload["explicit_gate"])

    def test_matching_handoff_without_focused_verifier_requests_rerun(self):
        repo = self.make_repo()
        (repo / "native_ev").mkdir()
        (repo / "native_ev/scenario_eval.py").write_text("dirty\n")
        tasks = [{
            "id": "t_rerun",
            "status": "blocked",
            "assignee": "terminal-velocity",
            "title": "Continue TV tv-spec autonomous loop",
            "body": "Review-required handoff for native_ev/scenario_eval.py, but verifier output missing.",
        }]

        code, payload = self.run_preflight(repo, tasks)

        self.assertEqual(code, 1, payload)
        self.assertEqual(payload["recommended_action"], "rerun_focused_verifier")
        self.assertEqual(payload["focused_verifier_status"], "missing")
        self.assertTrue(payload["handoff_match"])
        self.assertEqual(payload["explicit_gate"], "rerun_focused_verifier")

    def test_closeout_packet_changed_files_are_handoff_evidence(self):
        repo = self.make_repo()
        (repo / "native_ev/tests").mkdir(parents=True)
        (repo / "docs/checklists").mkdir(parents=True)
        packet_dir = repo / ".hermes/long-running/tv-spec-implementation"
        packet_dir.mkdir(parents=True)
        changed_files = [
            "native_ev/scenario_eval.py",
            "native_ev/tests/test_scenario_eval.py",
            "docs/checklists/ev-classic-fidelity-implementation-backlog.md",
            ".hermes/long-running/tv-spec-implementation/task-ledger.json",
            ".hermes/long-running/tv-spec-implementation/events.jsonl",
            ".hermes/long-running/tv-spec-implementation/closeout-packet-t_packet.json",
        ]
        for path in changed_files:
            full_path = repo / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(f"dirty {path}\n")
        (packet_dir / "closeout-packet-t_packet.json").write_text(json.dumps({
            "task_id": "t_packet",
            "changed_files": changed_files,
            "verification": {
                "targeted_unittest": "passed; python3 -m unittest native_ev.tests.test_scenario_eval -v",
                "git_diff_check": "passed; git diff --check produced no whitespace errors",
            },
            "summary": "Recovered worker closeout packet with targeted verifier evidence.",
        }))
        tasks = [{
            "id": "t_packet",
            "status": "blocked",
            "assignee": "terminal-velocity",
            "title": "Continue TV tv-spec autonomous loop",
            "body": "push_ready handoff recorded; see closeout packet for changed files and verification.",
        }]

        code, payload = self.run_preflight(repo, tasks)

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["recommended_action"], "checkpoint_and_push_ready")
        self.assertTrue(payload["handoff_match"])
        self.assertEqual(payload["focused_verifier_status"], "passed")
        self.assertEqual(payload["candidate_handoff"]["id"], "t_packet")
        self.assertIn("closeout_packet", payload["handoff_evidence_sources"])
        self.assertEqual(payload["handoff_dirty_path_match"]["missing_from_evidence"], [])
        self.assertEqual(payload["handoff_dirty_path_match"]["extra_in_evidence"], [])
        self.assertIsNone(payload["explicit_gate"])

    def test_checkpoint_mode_commits_matching_handoff_bundle_and_reports_push_ready(self):
        repo = self.make_repo()
        (repo / "native_ev/tests").mkdir(parents=True)
        (repo / "native_ev/scenario_eval.py").write_text("dirty\n")
        (repo / "native_ev/tests/test_scenario_eval.py").write_text("dirty\n")
        tasks = [{
            "id": "t_recover",
            "status": "blocked",
            "assignee": "terminal-velocity",
            "title": "Continue TV tv-spec autonomous loop",
            "body": "Changed files: native_ev/scenario_eval.py, native_ev/tests/test_scenario_eval.py. Focused verifier passed: python3 -m unittest native_ev.tests.test_scenario_eval -v.",
        }]

        code, payload = self.run_preflight(repo, tasks, "--checkpoint")

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["recommended_action"], "push_ready")
        self.assertEqual(payload["checkpoint"]["created"], True)
        self.assertEqual(payload["checkpoint"]["handoff_id"], "t_recover")
        self.assertEqual(payload["checkpoint"]["staged_paths"], ["native_ev/scenario_eval.py", "native_ev/tests/test_scenario_eval.py"])
        self.assertRegex(payload["checkpoint"]["commit"], r"^[0-9a-f]{7,40}$")
        status = subprocess.run(["git", "status", "--porcelain"], cwd=repo, text=True, stdout=subprocess.PIPE, check=True)
        self.assertEqual(status.stdout.strip(), "?? tasks.json")

    def test_repair_mode_moves_untracked_non_sensitive_debris_and_reclassifies_clean(self):
        repo = self.make_repo()
        quarantine_root = repo.parent / "quarantine"
        (repo / "scratch").mkdir()
        (repo / "scratch/debug-note.txt").write_text("not project work\n")

        code, payload = self.run_preflight(
            repo,
            [],
            "--repair-unsafe-debris",
            "--quarantine-root",
            str(quarantine_root),
        )

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["repair"]["action"], "moved_untracked_debris")
        self.assertEqual(payload["repair"]["moved_paths"], ["scratch/debug-note.txt"])
        self.assertFalse((repo / "scratch/debug-note.txt").exists())
        moved = quarantine_root / payload["repair"]["quarantine_id"] / "scratch/debug-note.txt"
        self.assertEqual(moved.read_text(), "not project work\n")
        self.assertEqual(payload["post_repair"]["repo_state"], "clean")
        self.assertEqual(payload["recommended_action"], "seed_successor")

    def test_repair_mode_does_not_move_sensitive_or_tracked_dirty_files(self):
        repo = self.make_repo()
        quarantine_root = repo.parent / "quarantine"
        (repo / "secret.txt").write_text("token=do-not-touch\n")
        (repo / "README.md").write_text("tracked\n")
        subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
        subprocess.run(["git", "-c", "user.email=test@example.invalid", "-c", "user.name=Test User", "commit", "-m", "fixture"], cwd=repo, check=True, stdout=subprocess.PIPE)
        (repo / "README.md").write_text("tracked dirty\n")

        code, payload = self.run_preflight(
            repo,
            [],
            "--repair-unsafe-debris",
            "--quarantine-root",
            str(quarantine_root),
        )

        self.assertEqual(code, 1, payload)
        self.assertEqual(payload["recommended_action"], "unsafe_dirty_state")
        self.assertEqual(payload["repair"]["action"], "not_repairable")
        self.assertEqual(sorted(payload["repair"]["blocked_paths"]), ["README.md", "secret.txt"])
        self.assertTrue((repo / "secret.txt").exists())
        self.assertTrue((repo / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
