import json
import os
import shutil
import sqlite3
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
WRAPPER = Path("/home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh")
TOPOLOGY_CHECKER = REPO / "tools/check_tv_runner_topology.py"


class TvRunnerTopologyTests(unittest.TestCase):
    def run_checker(self, repo: Path, profile: Path, *args: str) -> tuple[int, dict]:
        env = os.environ.copy()
        env.update({
            "TV_TOPOLOGY_REPO": str(repo),
            "TV_TOPOLOGY_PROFILE": str(profile),
        })
        result = subprocess.run(
            ["python3", str(TOPOLOGY_CHECKER), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            timeout=30,
        )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise AssertionError(result.stdout) from exc
        return result.returncode, payload

    def make_topology_fixture(self, root: Path) -> tuple[Path, Path, Path]:
        repo = root / "repo"
        profile = root / "profile"
        task_dir = repo / ".hermes/long-running/tv-spec-implementation"
        task_dir.mkdir(parents=True)
        (profile / "cron").mkdir(parents=True)
        (profile / "run").mkdir(parents=True)
        (profile / "config.yaml").write_text("kanban:\n  dispatch_in_gateway: true\n")
        (profile / "processes.json").write_text("[]\n")
        (profile / "run/tv_kanban_continuous_loop_state.json").write_text(json.dumps({
            "last_state": "stopped_by_user_kill",
            "updated_at": "2026-06-10T20:06:29Z",
        }) + "\n")
        return repo, profile, task_dir

    def write_kanban_db(self, profile: Path, *, active_tv_task: bool = False) -> Path:
        root = profile.parent.parent if profile.parent.name == "profiles" else profile
        db = root / "kanban.db"
        db.parent.mkdir(parents=True, exist_ok=True)
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
                CREATE TABLE task_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    profile TEXT,
                    status TEXT NOT NULL,
                    claim_lock TEXT,
                    worker_pid INTEGER,
                    metadata TEXT,
                    summary TEXT
                );
            """)
            if active_tv_task:
                conn.execute(
                    "INSERT INTO tasks (id, title, body, assignee, status, tenant, workspace_path, claim_lock, worker_pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        "t_tv_active",
                        "Terminal Velocity source-backed implementation slice",
                        "Continue tv-spec implementation work",
                        "loki-game",
                        "running",
                        "terminal-velocity",
                        None,
                        "claim-tv",
                        4242,
                    ),
                )
                conn.execute(
                    "INSERT INTO task_runs (task_id, profile, status, claim_lock, worker_pid, metadata, summary) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("t_tv_active", "loki-game", "running", "claim-tv", 4242, "{}", None),
                )
            else:
                conn.execute(
                    "INSERT INTO tasks (id, title, body, assignee, status, tenant, workspace_path, claim_lock, worker_pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    ("t_other", "Non-TV task", "unrelated", "loki-game", "running", None, None, "claim-other", 111),
                )
            conn.commit()
        finally:
            conn.close()
        return db

    def test_live_state_overrides_stale_ledger_and_passive_reporter(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, profile, task_dir = self.make_topology_fixture(Path(tmp))
            (task_dir / "task-ledger.json").write_text(json.dumps({
                "task_id": "tv-spec-implementation",
                "status": "waiting_gate",
                "active_gate": {"type": "topology_conflict"},
                "runner_ownership": {
                    "implementation_owner": "none_active",
                    "last_verified_at": "2026-06-10T23:13:44Z",
                },
            }) + "\n")
            (profile / "cron/jobs.json").write_text(json.dumps({"jobs": [{
                "id": "4e9cc82d1a99",
                "name": "Terminal Velocity slice completion reporter",
                "prompt": "Output only when a new Terminal Velocity development slice artifact appears; do not dispatch implementation work.",
                "script": "tv_slice_reporter.py",
                "no_agent": True,
                "enabled": True,
                "state": "scheduled",
            }]}) + "\n")

            code, payload = self.run_checker(repo, profile, "--startup-owner", "continuous_kanban_runner")

            self.assertEqual(code, 0, payload)
            self.assertFalse(payload["topology_conflict"])
            self.assertEqual(payload["live_implementation_owner"], "none_active")
            self.assertIn("ledger_stale", payload["warning_types"])
            self.assertIn("passive_reporter_ignored", payload["warning_types"])
            self.assertNotIn("gateway_global_enabled_warning", payload["warning_types"])
            self.assertNotIn("active_owner_conflict", payload["conflict_types"])

    def test_active_continuous_loop_conflicts_with_startup_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, profile, task_dir = self.make_topology_fixture(Path(tmp))
            (task_dir / "task-ledger.json").write_text(json.dumps({
                "task_id": "tv-spec-implementation",
                "status": "running",
                "runner_ownership": {"implementation_owner": "none_active"},
            }) + "\n")
            (profile / "cron/jobs.json").write_text(json.dumps({"jobs": []}) + "\n")
            (profile / "processes.json").write_text(json.dumps([{
                "pid": 123,
                "cmd": "/home/bh/.hermes/profiles/loki-game/scripts/tv_kanban_continuous_loop.py",
            }]) + "\n")

            code, payload = self.run_checker(repo, profile, "--startup-owner", "direct_session")

            self.assertEqual(code, 2, payload)
            self.assertTrue(payload["topology_conflict"])
            self.assertEqual(payload["live_implementation_owner"], "continuous_kanban_runner")
            self.assertIn("active_owner_conflict", payload["conflict_types"])

    def test_gateway_dispatch_enabled_without_tv_claim_is_warning_only_for_gateway_startup(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, profile, task_dir = self.make_topology_fixture(Path(tmp))
            (task_dir / "task-ledger.json").write_text(json.dumps({
                "runner_ownership": {"implementation_owner": "none_active"},
            }) + "\n")
            (profile / "cron/jobs.json").write_text(json.dumps({"jobs": []}) + "\n")
            self.write_kanban_db(profile, active_tv_task=False)

            code, payload = self.run_checker(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["live_implementation_owner"], "none_active")
            self.assertIn("gateway_global_enabled_warning", payload["warning_types"])
            self.assertNotIn("active_owner_conflict", payload["conflict_types"])

    def test_gateway_dispatch_enabled_is_quiet_for_standalone_runner_startup(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, profile, task_dir = self.make_topology_fixture(Path(tmp))
            (task_dir / "task-ledger.json").write_text(json.dumps({
                "runner_ownership": {"implementation_owner": "none_active"},
            }) + "\n")
            (profile / "cron/jobs.json").write_text(json.dumps({"jobs": []}) + "\n")
            self.write_kanban_db(profile, active_tv_task=False)

            code, payload = self.run_checker(repo, profile, "--startup-owner", "continuous_kanban_runner")

            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["live_implementation_owner"], "none_active")
            self.assertNotIn("gateway_global_enabled_warning", payload["warning_types"])
            self.assertNotIn("active_owner_conflict", payload["conflict_types"])

    def test_active_tv_kanban_claim_derives_gateway_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, profile, task_dir = self.make_topology_fixture(Path(tmp))
            (task_dir / "task-ledger.json").write_text(json.dumps({
                "runner_ownership": {
                    "implementation_owner": "gateway_kanban_dispatcher",
                    "allowed_surfaces": {"gateway_kanban_dispatcher": "owner"},
                },
            }) + "\n")
            (profile / "cron/jobs.json").write_text(json.dumps({"jobs": []}) + "\n")
            self.write_kanban_db(profile, active_tv_task=True)

            code, payload = self.run_checker(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["live_implementation_owner"], "gateway_kanban_dispatcher")
            self.assertNotIn("gateway_global_enabled_warning", payload["warning_types"])

    def test_stale_running_task_run_for_blocked_task_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, profile, task_dir = self.make_topology_fixture(Path(tmp))
            (task_dir / "task-ledger.json").write_text(json.dumps({
                "runner_ownership": {"implementation_owner": "none_active"},
            }) + "\n")
            (profile / "cron/jobs.json").write_text(json.dumps({"jobs": []}) + "\n")
            db = self.write_kanban_db(profile, active_tv_task=False)
            conn = sqlite3.connect(db)
            try:
                conn.execute("ALTER TABLE tasks ADD COLUMN current_run_id INTEGER")
                conn.execute(
                    "INSERT INTO tasks (id, title, body, assignee, status, tenant, workspace_path, claim_lock, worker_pid, current_run_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        "t_tv_blocked",
                        "Continue TV tv-spec Lane A through Kanban",
                        "Terminal Velocity work that has already blocked",
                        "terminal-velocity",
                        "blocked",
                        None,
                        "/home/bh/workspaces/loki/terminal-velocity",
                        None,
                        None,
                        None,
                    ),
                )
                conn.execute(
                    "INSERT INTO task_runs (task_id, profile, status, claim_lock, worker_pid, metadata, summary) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("t_tv_blocked", "terminal-velocity", "running", "stale-claim", 4242, None, None),
                )
                conn.commit()
            finally:
                conn.close()

            code, payload = self.run_checker(repo, profile, "--startup-owner", "continuous_kanban_runner")

            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["live_implementation_owner"], "none_active")
            self.assertNotIn("active_owner_conflict", payload["conflict_types"])

    def test_gateway_tv_claim_conflicts_with_standalone_startup(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, profile, task_dir = self.make_topology_fixture(Path(tmp))
            (task_dir / "task-ledger.json").write_text(json.dumps({
                "runner_ownership": {"implementation_owner": "none_active"},
            }) + "\n")
            (profile / "cron/jobs.json").write_text(json.dumps({"jobs": []}) + "\n")
            self.write_kanban_db(profile, active_tv_task=True)

            code, payload = self.run_checker(repo, profile, "--startup-owner", "continuous_kanban_runner")

            self.assertEqual(code, 2, payload)
            self.assertEqual(payload["live_implementation_owner"], "gateway_kanban_dispatcher")
            self.assertIn("active_owner_conflict", payload["conflict_types"])


class TvSpecContinuousRunnerTests(unittest.TestCase):
    def test_wrapper_exposes_test_safe_path_overrides(self):
        source = WRAPPER.read_text()

        self.assertIn("TV_SPEC_WORKDIR", source)
        self.assertIn("TV_SPEC_TASK_DIR", source)
        self.assertIn("TV_SPEC_PROMPT_FILE", source)
        self.assertIn("TV_SPEC_LOG_DIR", source)
        self.assertNotIn("workdir = pathlib.Path('/home/bh/workspaces/loki/terminal-velocity')", source)
        self.assertNotIn("cwd='/home/bh/workspaces/loki/terminal-velocity'", source)
        self.assertNotIn("p = pathlib.Path('/home/bh/workspaces/loki/terminal-velocity/.hermes/long-running/tv-spec-implementation/task-ledger.json')", source)

    def test_fake_single_iteration_populates_summary_sidecars_and_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            shutil.copytree(REPO, root, ignore=shutil.ignore_patterns(".git", ".hermes"))
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "fixture"], cwd=root, check=True)
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            subprocess.run(["git", "update-ref", "refs/remotes/origin/main", head], cwd=root, check=True)

            task_dir = root / ".hermes/long-running/tv-spec-implementation"
            task_dir.mkdir(parents=True)
            (task_dir / "task-ledger.json").write_text(json.dumps({
                "schema_version": 1,
                "task_id": "tv-spec-implementation",
                "status": "running",
                "active_gate": None,
                "next_resume_action": "continue fixture work",
                "last_touched_files": ["docs/research/long-running-task-wrapper-spec.md"],
                "last_verified_commands": ["fake verifier passed"],
            }) + "\n")
            (task_dir / "events.jsonl").write_text(json.dumps({
                "event_id": "fixture-start",
                "event_type": "slice_completed",
                "timestamp": "2026-06-09T00:00:00Z",
            }) + "\n")
            prompt = root / "docs/prompts/tv-spec-implementation-long-task-prompt.md"
            prompt.parent.mkdir(parents=True, exist_ok=True)
            prompt.write_text("fixture prompt\n")
            fake_hermes = Path(tmp) / "fake-hermes"
            fake_hermes.write_text(textwrap.dedent("""
                #!/usr/bin/env bash
                set -euo pipefail
                printf 'fake hermes invoked with %s args\\n' "$#"
                python3 - <<'PY'
                import json, os, pathlib
                task_dir = pathlib.Path(os.environ['TV_SPEC_TASK_DIR'])
                events = task_dir / 'events.jsonl'
                with events.open('a') as f:
                    f.write(json.dumps({
                        'event_id': 'fixture-material-progress',
                        'event_type': 'verification',
                        'timestamp': '2026-06-09T00:00:01Z',
                    }, sort_keys=True) + '\\n')
                PY
            """).lstrip())
            fake_hermes.chmod(fake_hermes.stat().st_mode | stat.S_IXUSR)

            env = os.environ.copy()
            env.update({
                "TV_SPEC_WORKDIR": str(root),
                "TV_SPEC_TASK_DIR": str(task_dir),
                "TV_SPEC_LEDGER_FILE": str(task_dir / "task-ledger.json"),
                "TV_SPEC_EVENTS_FILE": str(task_dir / "events.jsonl"),
                "TV_SPEC_PROMPT_FILE": str(prompt),
                "TV_SPEC_LOG_DIR": str(task_dir / "continuous-runner"),
                "TV_SPEC_HERMES_BIN": str(fake_hermes),
                "TV_SPEC_MAX_ITERATIONS": "1",
                "TV_SPEC_RETRY_BACKOFF_SECONDS": "0",
            })
            result = subprocess.run([str(WRAPPER)], cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)

            self.assertEqual(result.returncode, 0, result.stdout)
            log_dir = task_dir / "continuous-runner"
            summaries = sorted(log_dir.glob("run-*.summary.json"))
            self.assertEqual(len(summaries), 1, result.stdout)
            summary = json.loads(summaries[0].read_text())
            latest = json.loads((log_dir / "latest-summary.json").read_text())
            self.assertEqual(latest["invocation_id"], summary["invocation_id"])
            index_lines = (log_dir / "index.jsonl").read_text().splitlines()
            self.assertEqual(len(index_lines), 1)
            self.assertEqual(json.loads(index_lines[0])["invocation_id"], summary["invocation_id"])
            runner_state = json.loads((log_dir / "runner-state.json").read_text())
            self.assertEqual(runner_state["last_invocation_id"], summary["invocation_id"])

            required_summary_keys = {
                "exit_code", "attempt_count", "retry_classification", "ledger_status",
                "active_gate", "active_gate_value", "reported_touched_files",
                "git_dirty_summary", "diff_name_status", "repo_changes_occurred",
                "commits_created", "pushed_commits", "verifier_commands",
                "material_next_action", "delivery_status", "progress_token",
                "progress_token_changed", "consecutive_no_progress_iterations",
                "no_progress_stop", "log_file", "summary_file", "retention_policy",
            }
            self.assertTrue(required_summary_keys.issubset(summary), sorted(required_summary_keys - set(summary)))
            self.assertEqual(summary["exit_code"], 0)
            self.assertEqual(summary["retry_classification"], "none")
            self.assertEqual(summary["reported_touched_files"], ["docs/research/long-running-task-wrapper-spec.md"])
            self.assertEqual(summary["verifier_commands"], ["fake verifier passed"])


if __name__ == "__main__":
    unittest.main()
