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


if __name__ == "__main__":
    unittest.main()
