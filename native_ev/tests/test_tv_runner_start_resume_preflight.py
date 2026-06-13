import json
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools/tv_runner_start_resume_preflight.py"


class TvRunnerStartResumePreflightTests(unittest.TestCase):
    def make_fixture(self) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        repo = root / "repo"
        profile = root / "profile"
        repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        task_dir = repo / ".hermes/long-running/tv-spec-implementation"
        task_dir.mkdir(parents=True)
        (task_dir / "task-ledger.json").write_text(json.dumps({
            "task_id": "tv-spec-implementation",
            "runner_ownership": {"implementation_owner": "none_active"},
        }) + "\n")
        (profile / "cron").mkdir(parents=True)
        (profile / "run").mkdir(parents=True)
        (profile / "config.yaml").write_text("kanban:\n  dispatch_in_gateway: true\n")
        (profile / "cron/jobs.json").write_text(json.dumps({"jobs": []}) + "\n")
        (profile / "processes.json").write_text("[]\n")
        (profile / "run/tv_kanban_continuous_loop_state.json").write_text(json.dumps({
            "last_state": "stopped",
        }) + "\n")
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
        return tmp, repo, profile

    def run_preflight(self, repo: Path, profile: Path, *args: str) -> tuple[int, dict]:
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

    def add_active_tv_task(self, profile: Path) -> None:
        db = profile / "kanban.db"
        conn = sqlite3.connect(db)
        try:
            conn.executescript("""
                CREATE TABLE tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    body TEXT,
                    assignee TEXT,
                    status TEXT NOT NULL,
                    tenant TEXT,
                    workspace_path TEXT,
                    claim_lock TEXT,
                    worker_pid INTEGER
                );
            """)
            conn.execute(
                "INSERT INTO tasks (id, title, body, assignee, status, tenant, workspace_path, claim_lock, worker_pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    "t_tv_active",
                    "Terminal Velocity source-backed implementation slice",
                    "Continue tv-spec implementation work",
                    "terminal-velocity",
                    "running",
                    "terminal-velocity",
                    str(REPO),
                    "claim-tv",
                    4242,
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def add_blocked_tv_tasks(self, profile: Path) -> None:
        db = profile / "kanban.db"
        conn = sqlite3.connect(db)
        try:
            conn.executescript("""
                CREATE TABLE tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    body TEXT,
                    assignee TEXT,
                    status TEXT NOT NULL,
                    tenant TEXT,
                    workspace_path TEXT,
                    claim_lock TEXT,
                    worker_pid INTEGER
                );
            """)
            rows = [
                (
                    "t_push",
                    "TV push ready handoff",
                    "push_ready: local checkpoint abc123 verified; integration owner should publish",
                    "terminal-velocity",
                    "blocked",
                    "terminal-velocity",
                    str(REPO),
                    None,
                    None,
                ),
                (
                    "t_review_bug",
                    "TV stale review gate",
                    "review-required: tests passed for verified safe-local docs update",
                    "terminal-velocity",
                    "blocked",
                    "terminal-velocity",
                    str(REPO),
                    None,
                    None,
                ),
                (
                    "t_unsafe",
                    "TV unsafe dirty handoff",
                    "blocked: unsafe_dirty_state includes unrelated files",
                    "terminal-velocity",
                    "blocked",
                    "terminal-velocity",
                    str(REPO),
                    None,
                    None,
                ),
            ]
            conn.executemany(
                "INSERT INTO tasks (id, title, body, assignee, status, tenant, workspace_path, claim_lock, worker_pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                rows,
            )
            conn.commit()
        finally:
            conn.close()

    def test_clean_idle_gateway_startup_reports_start_action(self):
        _, repo, profile = self.make_fixture()

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["repo_state"], "clean")
        self.assertEqual(payload["topology"]["live_implementation_owner"], "none_active")
        self.assertEqual(payload["recommended_action"], "start_gateway_kanban_dispatcher")
        self.assertTrue(payload["safe_to_start"])
        self.assertIsNone(payload["explicit_gate"])

    def test_dirty_repo_routes_to_recovery_before_start(self):
        _, repo, profile = self.make_fixture()
        (repo / "native_ev").mkdir()
        (repo / "native_ev/scenario_eval.py").write_text("dirty\n")

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(code, 1, payload)
        self.assertEqual(payload["repo_state"], "dirty")
        self.assertEqual(payload["dirty_paths"], ["native_ev/scenario_eval.py"])
        self.assertEqual(payload["recommended_action"], "recover_dirty_handoff")
        self.assertEqual(payload["explicit_gate"], "recovery_preflight_required")
        self.assertFalse(payload["safe_to_start"])

    def test_active_gateway_owner_reports_resume_existing_owner(self):
        _, repo, profile = self.make_fixture()
        self.add_active_tv_task(profile)

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["topology"]["live_implementation_owner"], "gateway_kanban_dispatcher")
        self.assertEqual(payload["recommended_action"], "resume_existing_owner")
        self.assertTrue(payload["safe_to_start"])

    def test_conflicting_owner_blocks_start(self):
        _, repo, profile = self.make_fixture()
        (profile / "run/tv_kanban_continuous_loop_state.json").write_text(json.dumps({
            "last_state": "running",
        }) + "\n")

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(code, 1, payload)
        self.assertEqual(payload["recommended_action"], "blocked:topology_conflict")
        self.assertEqual(payload["explicit_gate"], "topology_conflict")
        self.assertFalse(payload["safe_to_start"])

    def test_blocked_cards_are_enriched_from_live_kanban_state(self):
        _, repo, profile = self.make_fixture()
        self.add_blocked_tv_tasks(profile)

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(payload["blocked_cards"]["status"], "inspected")
        classes = {card["id"]: card["canonical_class"] for card in payload["blocked_cards"]["cards"]}
        self.assertEqual(classes["t_push"], "push_ready")
        self.assertEqual(classes["t_review_bug"], "review_required_process_bug")
        self.assertEqual(classes["t_unsafe"], "unsafe_dirty_state")
        self.assertEqual(payload["blocked_cards"]["counts_by_class"]["push_ready"], 1)

    def test_push_ready_blocked_card_routes_to_integration_owner_before_start(self):
        _, repo, profile = self.make_fixture()
        self.add_blocked_tv_tasks(profile)

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(code, 1, payload)
        self.assertEqual(payload["recommended_action"], "recover_push_ready_handoff")
        self.assertEqual(payload["explicit_gate"], "push_ready_integration_required")
        self.assertFalse(payload["safe_to_start"])


if __name__ == "__main__":
    unittest.main()
