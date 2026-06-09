import json
import os
import shutil
import stat
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
WRAPPER = Path("/home/bh/.hermes/profiles/loki-game/scripts/tv_spec_continuous_runner.sh")


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
