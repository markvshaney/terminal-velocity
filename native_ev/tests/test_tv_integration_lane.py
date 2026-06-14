import importlib.util
import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
INTEGRATOR = REPO / "tools/tv_integration_lane.py"
_SPEC = importlib.util.spec_from_file_location("tv_integration_lane", INTEGRATOR)
assert _SPEC and _SPEC.loader
tv_integration_lane = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(tv_integration_lane)


class TvIntegrationLaneTests(unittest.TestCase):
    def run_integrator(self, repo: Path, *args: str, env_overrides: dict[str, str] | None = None) -> tuple[int, dict]:
        env = os.environ.copy()
        env["TV_INTEGRATOR_REPO"] = str(repo)
        if "--profile" not in args:
            env["TV_INTEGRATOR_PROFILE"] = str(repo / ".test-profile")
        if env_overrides:
            env.update(env_overrides)
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

    def make_fake_hermes_send_bin(self, root: Path, response: dict) -> Path:
        bin_path = root / "fake-hermes"
        bin_path.write_text(textwrap.dedent(f"""\
            #!/usr/bin/env python3
            import json
            import sys
            from pathlib import Path

            payload = {{
                "argv": sys.argv[1:],
                "stdin": sys.stdin.read(),
            }}
            log_path = Path({str(root / "send-cli-call.jsonl")!r})
            previous = log_path.read_text() if log_path.exists() else ""
            log_path.write_text(previous + json.dumps(payload, sort_keys=True) + "\\n")
            Path({str(root / "send-cli-call.json")!r}).write_text(json.dumps(payload, sort_keys=True))
            print(json.dumps({response!r}))
        """))
        bin_path.chmod(0o755)
        return bin_path

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

    def test_post_push_report_message_summarizes_published_tv_bundle(self):
        payload = {
            "head": "abcdef1234567890",
            "origin_main": "abcdef1234567890",
            "commit_summaries": [
                "feat(native): promote coordinate map readiness",
                "chore(ledger): refresh provenance",
            ],
            "changed_files": [
                "tools/extract_ev_system_semantics.py",
                "native_ev/data/sourced_ev_systems.json",
                "native_ev/model.py",
                "native_ev/scenario_eval.py",
                "docs/checklists/ev-classic-fidelity-implementation-backlog.md",
                ".hermes/long-running/tv-spec-implementation/task-ledger.json",
            ],
            "passed_checks": ["extractor_idempotence", "focused_model_scenario_tests", "git_diff_check"],
        }

        report = tv_integration_lane.build_post_push_report(payload)

        self.assertIn("TV progress published", report)
        self.assertIn("abcdef1", report)
        self.assertIn("feat(native): promote coordinate map readiness", report)
        self.assertIn("Game-dev content:", report)
        self.assertIn("EV Classic sourced systems manifest / galaxy topology semantics", report)
        self.assertIn("Native EV model validation and scenario readiness surfaces", report)
        self.assertIn("Fidelity backlog/source-readiness docs", report)
        self.assertIn("Changed:", report)
        self.assertIn("Native EV sourced systems extractor and manifest", report)
        self.assertIn("git_diff_check", report)

    def test_post_push_report_dry_run_payload_uses_requested_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            target = repo / "docs/checklists/ev-classic-fidelity-implementation-backlog.md"
            target.write_text(target.read_text() + "\n<!-- integration fixture -->\n")
            subprocess.run(["git", "add", str(target.relative_to(repo))], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "fixture safe checkpoint"], cwd=repo, check=True)

            code, payload = self.run_integrator(
                repo,
                "--dry-run",
                "--post-push-report-target",
                "telegram:Loki GameTV",
                "--post-push-report-dry-run",
            )

            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["post_push_report"]["target"], "telegram:Loki GameTV")
            self.assertEqual(payload["post_push_report"]["status"], "dry_run")
            self.assertIn("TV progress published", payload["post_push_report"]["message"])

    def test_blocked_runner_report_dry_run_summarizes_integration_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            (repo / "scratch.txt").write_text("untracked\n")

            code, payload = self.run_integrator(
                repo,
                "--dry-run",
                "--blocked-report-target",
                "telegram:Loki GameTV",
                "--blocked-report-dry-run",
            )

            self.assertEqual(code, 2, payload)
            report = payload["blocked_runner_report"]
            self.assertEqual(report["target"], "telegram:Loki GameTV")
            self.assertEqual(report["status"], "dry_run")
            self.assertIn("TV runner blocked by integration owner", report["message"])
            self.assertIn("dirty_worktree", report["message"])
            self.assertIn("scratch.txt", report["message"])

    def test_blocked_runner_report_skips_when_integration_not_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))

            code, payload = self.run_integrator(
                repo,
                "--dry-run",
                "--blocked-report-target",
                "telegram:Loki GameTV",
            )

            self.assertEqual(code, 0, payload)
            self.assertEqual(payload["blocked_runner_report"]["status"], "skipped")
            self.assertEqual(payload["blocked_runner_report"]["reason"], "integration_not_blocked")

    def test_blocked_runner_report_failure_adds_runner_visible_blocker(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = self.make_repo(root)
            (repo / "scratch.txt").write_text("untracked\n")
            fake_send = self.make_fake_hermes_send_bin(root, {"error": "Platform telegram is not configured"})

            old_bin = os.environ.get("HERMES_SEND_BIN")
            os.environ["HERMES_SEND_BIN"] = str(fake_send)
            try:
                code, payload = self.run_integrator(
                    repo,
                    "--dry-run",
                    "--blocked-report-target",
                    "telegram:Loki GameTV",
                )
            finally:
                if old_bin is None:
                    os.environ.pop("HERMES_SEND_BIN", None)
                else:
                    os.environ["HERMES_SEND_BIN"] = old_bin

            self.assertEqual(code, 2, payload)
            self.assertEqual(payload["blocked_runner_report"]["status"], "failed")
            self.assertIn("blocked_runner_report_failed", payload["blockers"])

    def test_blocked_runner_report_includes_recovery_dirty_buckets(self):
        report = tv_integration_lane.build_blocked_runner_report({
            "decision": "needs_human",
            "blockers": ["dirty_worktree", "control_plane_dirty_state"],
            "dirty_state_recovery": {
                "matched_handoff_paths": ["native_ev/model.py"],
                "control_plane_dirty_paths": ["tools/tv_integration_lane.py"],
                "historical_runner_metadata_dirty_paths": [".hermes/long-running/tv-spec-implementation/old.json"],
                "extra_unexplained_dirty_paths": ["scratch.txt"],
                "recommended_action": "split_or_review_control_plane_dirty_state",
            },
        })

        self.assertIn("matched handoff paths:", report)
        self.assertIn("native_ev/model.py", report)
        self.assertIn("control-plane dirty paths:", report)
        self.assertIn("tools/tv_integration_lane.py", report)
        self.assertIn("historical runner metadata dirty paths:", report)
        self.assertIn("old.json", report)
        self.assertIn("extra unexplained dirty paths:", report)
        self.assertIn("scratch.txt", report)
        self.assertIn("next safe action:", report)

    def test_blocked_runner_report_suppresses_duplicate_fingerprint_and_force_resends(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = self.make_repo(root)
            (repo / "scratch.txt").write_text("untracked\n")
            fake_send = self.make_fake_hermes_send_bin(root, {"success": True})

            first_code, first_payload = self.run_integrator(
                repo,
                "--dry-run",
                "--blocked-report-target",
                "telegram:Loki GameTV",
                env_overrides={"HERMES_SEND_BIN": str(fake_send)},
            )
            second_code, second_payload = self.run_integrator(
                repo,
                "--dry-run",
                "--blocked-report-target",
                "telegram:Loki GameTV",
                env_overrides={"HERMES_SEND_BIN": str(fake_send)},
            )
            forced_code, forced_payload = self.run_integrator(
                repo,
                "--dry-run",
                "--blocked-report-target",
                "telegram:Loki GameTV",
                "--force-blocked-report",
                env_overrides={"HERMES_SEND_BIN": str(fake_send)},
            )

            self.assertEqual(first_code, 2, first_payload)
            self.assertEqual(second_code, 2, second_payload)
            self.assertEqual(forced_code, 2, forced_payload)
            self.assertEqual(first_payload["blocked_runner_report"]["status"], "sent")
            self.assertEqual(second_payload["blocked_runner_report"]["status"], "skipped")
            self.assertEqual(second_payload["blocked_runner_report"]["reason"], "duplicate_fingerprint")
            self.assertEqual(forced_payload["blocked_runner_report"]["status"], "sent")
            calls = (root / "send-cli-call.jsonl").read_text().splitlines()
            self.assertEqual(len(calls), 2)
            state = json.loads((repo / ".hermes/long-running/tv-spec-implementation/report-state.json").read_text())
            self.assertEqual(state["blocked_runner_report"]["fingerprint"], first_payload["blocked_runner_report"]["fingerprint"])

    def test_blocked_runner_report_dry_run_never_writes_dedupe_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            (repo / "scratch.txt").write_text("untracked\n")

            code, payload = self.run_integrator(
                repo,
                "--dry-run",
                "--blocked-report-target",
                "telegram:Loki GameTV",
                "--blocked-report-dry-run",
            )

            self.assertEqual(code, 2, payload)
            self.assertEqual(payload["blocked_runner_report"]["status"], "dry_run")
            self.assertFalse((repo / ".hermes/long-running/tv-spec-implementation/report-state.json").exists())

    def test_delivery_targets_named_profile_when_profile_path_is_named_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_send = self.make_fake_hermes_send_bin(root, {"success": True})
            profile = root / ".hermes" / "profiles" / "loki-game"
            old_bin = os.environ.get("HERMES_SEND_BIN")
            os.environ["HERMES_SEND_BIN"] = str(fake_send)
            try:
                result = tv_integration_lane.deliver_message_report(
                    "telegram:Loki GameTV",
                    "hello",
                    profile=profile,
                )
            finally:
                if old_bin is None:
                    os.environ.pop("HERMES_SEND_BIN", None)
                else:
                    os.environ["HERMES_SEND_BIN"] = old_bin

            sent = json.loads((root / "send-cli-call.json").read_text())
            self.assertEqual(result["status"], "sent")
            self.assertEqual(sent["argv"], ["-p", "loki-game", "send", "--json", "--to", "telegram:Loki GameTV"])
            self.assertEqual(sent["stdin"], "hello")

    def test_failed_post_push_report_changes_publish_packet_to_needs_human(self):
        payload = {"decision": "publish", "blockers": [], "pushed": True}
        tv_integration_lane.apply_report_delivery_failure_gate(
            payload,
            "post_push_report",
            {"status": "failed", "output": '{"error":"Platform telegram is not configured"}'},
        )

        self.assertEqual(payload["decision"], "needs_human")
        self.assertIn("post_push_report_failed", payload["blockers"])

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

    def add_comment_only_blocked_card(self, db: Path, repo: Path) -> None:
        conn = sqlite3.connect(db)
        try:
            conn.execute(
                "INSERT INTO tasks (id, title, body, assignee, status, tenant, workspace_path, claim_lock, worker_pid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ("t_comment_review", "TV generic blocked handoff", "Needs follow-up", "terminal-velocity", "blocked", "terminal-velocity", str(repo), None, None),
            )
            conn.execute(
                "INSERT INTO task_comments (task_id, author, body, created_at) VALUES (?, ?, ?, ?)",
                ("t_comment_review", "worker", "review-required handoff: verified safe-local TV work", 123),
            )
            conn.commit()
        finally:
            conn.close()

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

    def test_gate_normalization_dry_run_uses_comment_evidence_for_generic_blocked_cards(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            profile, db = self.make_profile_with_blocked_cards(Path(tmp), repo)
            self.add_comment_only_blocked_card(db, repo)

            code, payload = self.run_integrator(repo, "--normalize-gates", "--profile", str(profile))

            self.assertEqual(code, 0, payload)
            planned = {action["task_id"]: action["canonical_class"] for action in payload["gate_normalization"]["planned_comments"]}
            self.assertEqual(planned["t_comment_review"], "review_required_process_bug")

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

    def test_recover_push_ready_can_normalize_only_the_resolved_gate_and_reconcile_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            profile, db = self.make_profile_with_blocked_cards(Path(tmp), repo)
            task_dir = repo / ".hermes/long-running/tv-spec-implementation"
            task_dir.mkdir(parents=True)
            ledger = {
                "schema_version": 1,
                "task_id": "tv-spec-implementation",
                "status": "running",
                "declared_owner": "continuous_kanban_runner",
                "updated_at": "2026-06-13T09:00Z",
            }
            (task_dir / "task-ledger.json").write_text(json.dumps(ledger) + "\n")
            (task_dir / "events.jsonl").write_text(json.dumps({
                "event_id": "evt-integrated",
                "timestamp": "2026-06-13T10:00Z",
                "event_type": "checkpoint_published",
                "task_id": "t_push",
                "changed_files": ["tools/tv_integration_lane.py"],
            }) + "\n")
            subprocess.run([
                "git",
                "add",
                ".hermes/long-running/tv-spec-implementation/task-ledger.json",
                ".hermes/long-running/tv-spec-implementation/events.jsonl",
            ], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "fixture ledger projection"], cwd=repo, check=True)
            subprocess.run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], cwd=repo, check=True)

            first_code, first_payload = self.run_integrator(
                repo,
                "--recover-push-ready-handoff",
                "--apply-push-ready-recovery",
                "--normalize-gates",
                "--apply-gate-comments",
                "--reconcile-ledger",
                "--apply-ledger-reconcile",
                "--profile",
                str(profile),
            )
            self.assertEqual(first_code, 0, first_payload)
            self.assertTrue(first_payload["ledger_reconciliation"]["write_applied"])
            self.assertEqual(first_payload["gate_normalization"]["comments_written"], 1)
            self.assertEqual([item["task_id"] for item in first_payload["gate_normalization"]["planned_comments"]], ["t_push"])
            self.assertNotIn("t_review", {item["task_id"] for item in first_payload["gate_normalization"]["planned_comments"]})
            written = json.loads((task_dir / "task-ledger.json").read_text())
            self.assertNotIn("status", written)
            self.assertNotIn("declared_owner", written)
            self.assertNotIn("runner_ownership", written)
            self.assertEqual(written["runtime_truth_rule"], "Live runner state is derived from Kanban/topology/git/processes, not this ledger.")
            self.assertEqual(written["diagnostics"]["generated_from"]["latest_event_id"], "evt-integrated")
            conn = sqlite3.connect(db)
            try:
                comments = conn.execute("SELECT task_id, body FROM task_comments ORDER BY id").fetchall()
                events = conn.execute("SELECT task_id, kind FROM task_events ORDER BY id").fetchall()
            finally:
                conn.close()
            self.assertEqual([row[0] for row in comments], ["t_push", "t_push"])
            self.assertTrue(any("tv_gate_normalization" in row[1] for row in comments))
            self.assertTrue(any("tv_push_ready_recovery" in row[1] for row in comments))
            self.assertEqual(sorted(row[1] for row in events), ["tv_gate_normalized", "tv_push_ready_recovered"])

    def test_recover_unsafe_dirty_state_dry_run_plans_stale_clean_closeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            profile, _db = self.make_profile_with_blocked_cards(Path(tmp), repo)

            code, payload = self.run_integrator(repo, "--recover-unsafe-dirty-state", "--profile", str(profile))

            self.assertEqual(code, 0, payload)
            recovery = payload["unsafe_dirty_recovery"]
            self.assertFalse(recovery["applied"])
            self.assertEqual(recovery["recommended_action"], "close_stale_unsafe_dirty_state_handoffs")
            self.assertEqual([item["task_id"] for item in recovery["planned_closeouts"]], ["t_unsafe"])
            self.assertEqual(recovery["skipped"]["t_push"], "push_ready")
            self.assertEqual(recovery["skipped"]["t_review"], "review_required_process_bug")

    def test_recover_unsafe_dirty_state_apply_closes_stale_clean_handoff_idempotently(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = self.make_repo(Path(tmp))
            profile, db = self.make_profile_with_blocked_cards(Path(tmp), repo)

            first_code, first_payload = self.run_integrator(repo, "--recover-unsafe-dirty-state", "--apply-unsafe-dirty-recovery", "--profile", str(profile))
            second_code, second_payload = self.run_integrator(repo, "--recover-unsafe-dirty-state", "--apply-unsafe-dirty-recovery", "--profile", str(profile))

            self.assertEqual(first_code, 0, first_payload)
            self.assertEqual(second_code, 0, second_payload)
            self.assertEqual(first_payload["unsafe_dirty_recovery"]["closeouts_written"], 1)
            self.assertEqual(second_payload["unsafe_dirty_recovery"]["closeouts_written"], 0)
            conn = sqlite3.connect(db)
            try:
                status = conn.execute("SELECT status FROM tasks WHERE id = 't_unsafe'").fetchone()[0]
                comments = conn.execute("SELECT task_id, body FROM task_comments WHERE task_id = 't_unsafe' ORDER BY id").fetchall()
                events = conn.execute("SELECT task_id, kind FROM task_events WHERE task_id = 't_unsafe' ORDER BY id").fetchall()
            finally:
                conn.close()
            self.assertEqual(status, "done")
            self.assertEqual(len(comments), 1)
            self.assertIn("tv_unsafe_dirty_recovery", comments[0][1])
            self.assertEqual([row[1] for row in events], ["tv_unsafe_dirty_recovered"])


if __name__ == "__main__":
    unittest.main()
