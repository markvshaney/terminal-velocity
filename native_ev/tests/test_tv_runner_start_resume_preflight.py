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

    def add_comment_only_review_block(self, profile: Path) -> None:
        db = profile / "kanban.db"
        conn = sqlite3.connect(db)
        try:
            conn.executescript("""
                CREATE TABLE tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    body TEXT,
                    latest_summary TEXT,
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
                    body TEXT NOT NULL
                );
            """)
            conn.execute(
                "INSERT INTO tasks (id, title, body, latest_summary, assignee, status, tenant, workspace_path, claim_lock, worker_pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    "t_comment_review",
                    "Continue TV EV Classic fidelity backlog slice",
                    "Pick the next safe bounded backlog item after parent checkpoint.",
                    None,
                    "terminal-velocity",
                    "blocked",
                    "terminal-velocity",
                    str(REPO),
                    None,
                    None,
                ),
            )
            conn.execute(
                "INSERT INTO task_comments (task_id, body) VALUES (?, ?)",
                (
                    "t_comment_review",
                    "review-required handoff: verified safe-local TV work; focused tests passed; needs integration review",
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def add_done_push_ready_handoff(self, repo: Path, profile: Path) -> None:
        packet_dir = repo / ".hermes/long-running/tv-spec-implementation"
        packet_dir.mkdir(parents=True, exist_ok=True)
        changed_files = [
            "native_ev/scenario_eval.py",
            "native_ev/tests/test_scenario_eval.py",
            ".hermes/long-running/tv-spec-implementation/closeout-packet-t_done_push.json",
        ]
        (packet_dir / "closeout-packet-t_done_push.json").write_text(json.dumps({
            "contract_version": "machine_contract_v1",
            "closeout_class": "push_ready",
            "kanban_task": "t_done_push",
            "changed_files": changed_files,
            "focused_verifiers_passed": True,
            "verification": {
                "targeted_unittest": {
                    "command": "python3 -m unittest native_ev.tests.test_scenario_eval -v",
                    "result": "passed",
                },
            },
            "next_action": "integration owner should checkpoint and push this verified handoff",
            "summary": "Focused verifier passed for done-task handoff.",
        }) + "\n")
        db = profile / "kanban.db"
        conn = sqlite3.connect(db)
        try:
            conn.executescript("""
                CREATE TABLE tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    body TEXT,
                    latest_summary TEXT,
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
                    body TEXT NOT NULL
                );
            """)
            conn.execute(
                "INSERT INTO tasks (id, title, body, latest_summary, assignee, status, tenant, workspace_path, claim_lock, worker_pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    "t_done_push",
                    "Continue TV EV Classic fidelity backlog slice",
                    "push_ready handoff recorded; closeout packet has changed files and verification.",
                    "Focused verifier passed: python3 -m unittest native_ev.tests.test_scenario_eval -v",
                    "terminal-velocity",
                    "done",
                    "terminal-velocity",
                    str(repo),
                    None,
                    None,
                ),
            )
            conn.execute(
                "INSERT INTO task_comments (task_id, body) VALUES (?, ?)",
                (
                    "t_done_push",
                    "push_ready handoff: changed files native_ev/scenario_eval.py, native_ev/tests/test_scenario_eval.py; focused verifier passed",
                ),
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
        self.assertEqual(payload["preflight_tier"], "fast_path")
        self.assertEqual(payload["handoff_candidates"]["status"], "skipped_fast_path")
        self.assertEqual(payload["machine_result"], {
            "safe_to_start": True,
            "recommended_action": "start_gateway_kanban_dispatcher",
            "explicit_gate": None,
            "live_owner": "none_active",
            "repo_state": "clean",
            "dirty_paths": [],
            "blocked_handoffs": {},
            "heartbeat_or_task_id": None,
            "preflight_tier": "fast_path",
            "escalations_run": [],
        })

    def test_dirty_repo_routes_to_recovery_before_start(self):
        _, repo, profile = self.make_fixture()
        (repo / "native_ev").mkdir()
        (repo / "native_ev/scenario_eval.py").write_text("dirty\n")

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(code, 1, payload)
        self.assertEqual(payload["repo_state"], "dirty")
        self.assertEqual(payload["dirty_paths"], ["native_ev/scenario_eval.py"])
        self.assertEqual(payload["recommended_action"], "unsafe_dirty_state")
        self.assertEqual(payload["explicit_gate"], "unsafe_dirty_state")
        self.assertEqual(payload["dirty_handoff_recovery"]["recommended_action"], "unsafe_dirty_state")
        self.assertFalse(payload["safe_to_start"])

    def test_dirty_repo_uses_recovery_classifier_candidate_and_action(self):
        _, repo, profile = self.make_fixture()
        (repo / "native_ev/tests").mkdir(parents=True)
        (repo / "native_ev/scenario_eval.py").write_text("dirty\n")
        (repo / "native_ev/tests/test_scenario_eval.py").write_text("dirty\n")
        db = profile / "kanban.db"
        conn = sqlite3.connect(db)
        try:
            conn.executescript("""
                CREATE TABLE tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    body TEXT,
                    latest_summary TEXT,
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
                    body TEXT NOT NULL
                );
            """)
            conn.execute(
                "INSERT INTO tasks (id, title, body, latest_summary, assignee, status, tenant, workspace_path, claim_lock, worker_pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    "t_4ad7b9e5",
                    "TV push ready dirty handoff",
                    "push_ready handoff recorded; changed files and verification are in task comments/latest summary.",
                    "Focused verifier passed: python3 -m unittest native_ev.tests.test_scenario_eval -v",
                    "terminal-velocity",
                    "blocked",
                    "terminal-velocity",
                    str(REPO),
                    None,
                    None,
                ),
            )
            conn.execute(
                "INSERT INTO task_comments (task_id, body) VALUES (?, ?)",
                (
                    "t_4ad7b9e5",
                    "handoff JSON: {\"changed_files\": [\"native_ev/scenario_eval.py\", \"native_ev/tests/test_scenario_eval.py\"], \"verification\": {\"targeted_unittest\": \"passed\"}}",
                ),
            )
            conn.commit()
        finally:
            conn.close()

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(code, 1, payload)
        self.assertEqual(payload["repo_state"], "dirty")
        self.assertEqual(payload["recommended_action"], "checkpoint_and_push_ready")
        self.assertIsNone(payload["explicit_gate"])
        self.assertFalse(payload["safe_to_start"])
        recovery = payload["dirty_handoff_recovery"]
        self.assertEqual(recovery["recommended_action"], payload["recommended_action"])
        self.assertEqual(recovery["explicit_gate"], payload["explicit_gate"])
        self.assertEqual(recovery["candidate_handoff"]["id"], "t_4ad7b9e5")
        self.assertEqual(recovery["focused_verifier_status"], "passed")
        self.assertIn("kanban_comment", recovery["handoff_evidence_sources"])
        self.assertIn("kanban_latest_summary", recovery["handoff_evidence_sources"])
        self.assertEqual(recovery["matched_changed_files"], ["native_ev/scenario_eval.py", "native_ev/tests/test_scenario_eval.py"])
        self.assertEqual(recovery["extra_dirty_paths"], [])

    def test_dirty_repo_uses_done_push_ready_handoff_candidate(self):
        _, repo, profile = self.make_fixture()
        self.add_done_push_ready_handoff(repo, profile)
        (repo / "native_ev/tests").mkdir(parents=True, exist_ok=True)
        for path in [
            "native_ev/scenario_eval.py",
            "native_ev/tests/test_scenario_eval.py",
        ]:
            (repo / path).write_text(f"dirty {path}\n")

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(code, 1, payload)
        self.assertEqual(payload["repo_state"], "dirty")
        self.assertEqual(payload["blocked_cards"]["cards"], [])
        self.assertEqual(payload["recommended_action"], "checkpoint_and_push_ready")
        self.assertIsNone(payload["explicit_gate"])
        recovery = payload["dirty_handoff_recovery"]
        self.assertEqual(recovery["candidate_handoff"]["id"], "t_done_push")
        self.assertEqual(recovery["candidate_handoff"]["status"], "done")
        self.assertIn("validated_closeout_packet", recovery["handoff_evidence_sources"])
        self.assertEqual(recovery["focused_verifier_status"], "passed")
        self.assertEqual(recovery["extra_dirty_paths"], [])

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

    def test_blocked_card_classification_uses_comments_when_task_fields_are_generic(self):
        _, repo, profile = self.make_fixture()
        self.add_comment_only_review_block(profile)

        code, payload = self.run_preflight(repo, profile, "--startup-owner", "gateway_kanban_dispatcher")

        self.assertEqual(code, 1, payload)
        classes = {card["id"]: card["canonical_class"] for card in payload["blocked_cards"]["cards"]}
        self.assertEqual(classes["t_comment_review"], "review_required_process_bug")
        self.assertEqual(payload["recommended_action"], "normalize_blocked_gates")
        self.assertEqual(payload["explicit_gate"], "gate_normalization_required")

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
