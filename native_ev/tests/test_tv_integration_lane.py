import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
INTEGRATOR = REPO / "tools/tv_integration_lane.py"


class TvIntegrationLaneTests(unittest.TestCase):
    def run_integrator(self, repo: Path, *args: str) -> tuple[int, dict]:
        env = os.environ.copy()
        env["TV_INTEGRATOR_REPO"] = str(repo)
        result = subprocess.run(
            ["python3", str(INTEGRATOR), *args],
            cwd=repo,
            env=env,
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

    def make_repo(self, root: Path) -> Path:
        repo = root / "repo"
        shutil.copytree(REPO, repo, ignore=shutil.ignore_patterns(".git", ".hermes"))
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "fixture"], cwd=repo, check=True)
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
        subprocess.run(["git", "update-ref", "refs/remotes/origin/main", head], cwd=repo, check=True)
        return repo

    def test_dry_run_allows_clean_ahead_safe_local_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            target = repo / "docs/checklists/ev-classic-fidelity-implementation-backlog.md"
            target.write_text(target.read_text() + "\n<!-- integration fixture -->\n")
            subprocess.run(["git", "add", str(target.relative_to(repo))], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "fixture safe checkpoint"], cwd=repo, check=True)

            code, payload = self.run_integrator(repo, "--dry-run")

            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["decision"], "publish")
            self.assertFalse(payload["would_push"])
            self.assertEqual(payload["ahead_count"], 1)
            self.assertIn("docs/checklists/ev-classic-fidelity-implementation-backlog.md", payload["changed_files"])
            self.assertIn("git_diff_check", payload["passed_checks"])

    def test_blocks_dirty_untracked_files_before_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            (repo / "scratch.txt").write_text("untracked\n")

            code, payload = self.run_integrator(repo, "--dry-run")

            self.assertEqual(code, 2, payload)
            self.assertEqual(payload["decision"], "needs_human")
            self.assertIn("dirty_worktree", payload["blockers"])

    def test_blocks_active_worker_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            profile = Path(tmp) / "profile"
            (profile / "cron").mkdir(parents=True)
            (profile / "run").mkdir(parents=True)
            (profile / "config.yaml").write_text("kanban:\n  dispatch_in_gateway: true\n")
            (profile / "processes.json").write_text("[]\n")
            (profile / "run/tv_kanban_continuous_loop_state.json").write_text("{}\n")
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
                    ("t_active", "Terminal Velocity worker", "Continue TV work", "terminal-velocity", "running", "terminal-velocity", str(repo), "claim", 123),
                )
                conn.commit()
            finally:
                conn.close()

            code, payload = self.run_integrator(repo, "--dry-run", "--profile", str(profile))

            self.assertEqual(code, 2, payload)
            self.assertEqual(payload["decision"], "needs_human")
            self.assertIn("active_worker", payload["blockers"])

    def make_profile_with_blocked_cards(self, root: Path, repo: Path) -> tuple[Path, Path]:
        profile = root / "profile"
        profile.mkdir()
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
                CREATE TABLE task_comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    author TEXT NOT NULL,
                    body TEXT NOT NULL,
                    created_at INTEGER NOT NULL
                );
                CREATE TABLE task_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    run_id INTEGER,
                    kind TEXT NOT NULL,
                    payload TEXT,
                    created_at INTEGER NOT NULL
                );
            """)
            rows = [
                ("t_push", "TV push handoff", "push_ready: commit abc verified", "terminal-velocity", "blocked", "terminal-velocity", str(repo), None, None),
                ("t_review", "TV stale review", "review-required: verified safe-local docs update", "terminal-velocity", "blocked", "terminal-velocity", str(repo), None, None),
                ("t_unsafe", "TV unsafe handoff", "blocked: unsafe_dirty_state has unrelated files", "terminal-velocity", "blocked", "terminal-velocity", str(repo), None, None),
            ]
            conn.executemany(
                "INSERT INTO tasks (id, title, body, assignee, status, tenant, workspace_path, claim_lock, worker_pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                rows,
            )
            conn.commit()
        finally:
            conn.close()
        return profile, db

    def test_gate_normalization_dry_run_plans_only_actionable_gate_comments(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            profile, _db = self.make_profile_with_blocked_cards(Path(tmp), repo)

            code, payload = self.run_integrator(repo, "--normalize-gates", "--profile", str(profile))

            self.assertEqual(code, 0, payload)
            normalization = payload["gate_normalization"]
            self.assertFalse(normalization["applied"])
            planned = {action["task_id"]: action["canonical_class"] for action in normalization["planned_comments"]}
            self.assertEqual(planned, {"t_push": "push_ready", "t_review": "review_required_process_bug"})
            self.assertEqual(normalization["skipped"]["t_unsafe"], "unsafe_dirty_state")

    def test_gate_normalization_apply_inserts_idempotent_comments_and_events(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            profile, db = self.make_profile_with_blocked_cards(Path(tmp), repo)

            first_code, first_payload = self.run_integrator(repo, "--normalize-gates", "--apply-gate-comments", "--profile", str(profile))
            second_code, second_payload = self.run_integrator(repo, "--normalize-gates", "--apply-gate-comments", "--profile", str(profile))

            self.assertEqual(first_code, 0, first_payload)
            self.assertEqual(second_code, 0, second_payload)
            self.assertEqual(first_payload["gate_normalization"]["comments_written"], 2)
            self.assertEqual(second_payload["gate_normalization"]["comments_written"], 0)
            conn = sqlite3.connect(db)
            try:
                comments = conn.execute("SELECT task_id, body FROM task_comments ORDER BY task_id").fetchall()
                events = conn.execute("SELECT task_id, kind FROM task_events ORDER BY task_id").fetchall()
            finally:
                conn.close()
            self.assertEqual([row[0] for row in comments], ["t_push", "t_review"])
            self.assertTrue(all("tv_gate_normalization" in row[1] for row in comments))
            self.assertEqual([row[1] for row in events], ["tv_gate_normalized", "tv_gate_normalized"])

    def test_recover_push_ready_handoff_dry_run_plans_stale_clean_handoff_closeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            profile, _db = self.make_profile_with_blocked_cards(Path(tmp), repo)

            code, payload = self.run_integrator(repo, "--recover-push-ready-handoff", "--profile", str(profile))

            self.assertEqual(code, 0, payload)
            recovery = payload["push_ready_recovery"]
            self.assertFalse(recovery["applied"])
            self.assertEqual(recovery["recommended_action"], "close_stale_push_ready_handoffs")
            self.assertEqual([item["task_id"] for item in recovery["planned_closeouts"]], ["t_push"])
            self.assertEqual(recovery["skipped"]["t_review"], "review_required_process_bug")
            self.assertEqual(recovery["skipped"]["t_unsafe"], "unsafe_dirty_state")

    def test_recover_push_ready_handoff_apply_closes_stale_clean_handoff_idempotently(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            profile, db = self.make_profile_with_blocked_cards(Path(tmp), repo)

            first_code, first_payload = self.run_integrator(repo, "--recover-push-ready-handoff", "--apply-push-ready-recovery", "--profile", str(profile))
            second_code, second_payload = self.run_integrator(repo, "--recover-push-ready-handoff", "--apply-push-ready-recovery", "--profile", str(profile))

            self.assertEqual(first_code, 0, first_payload)
            self.assertEqual(second_code, 0, second_payload)
            self.assertEqual(first_payload["push_ready_recovery"]["closeouts_written"], 1)
            self.assertEqual(second_payload["push_ready_recovery"]["closeouts_written"], 0)
            conn = sqlite3.connect(db)
            try:
                status = conn.execute("SELECT status FROM tasks WHERE id = 't_push'").fetchone()[0]
                comments = conn.execute("SELECT task_id, body FROM task_comments WHERE task_id = 't_push' ORDER BY id").fetchall()
                events = conn.execute("SELECT task_id, kind FROM task_events WHERE task_id = 't_push' ORDER BY id").fetchall()
            finally:
                conn.close()
            self.assertEqual(status, "done")
            self.assertEqual(len(comments), 1)
            self.assertIn("tv_push_ready_recovery", comments[0][1])
            self.assertEqual([row[1] for row in events], ["tv_push_ready_recovered"])


if __name__ == "__main__":
    unittest.main()
