import unittest
from unittest.mock import patch

from tools import tv_runner_autostart


class TvRunnerAutostartTests(unittest.TestCase):
    def test_continuation_body_requires_runner_preflight_before_work_selection(self):
        body = tv_runner_autostart.continuation_body("abc1234")

        self.assertIn("python3 tools/backlog_dispatch_index.py runner-preflight", body)
        self.assertIn("before selecting work", body)

    def test_continuation_body_requires_closeout_guard_before_review_required(self):
        body = tv_runner_autostart.continuation_body("abc1234")

        self.assertIn("python3 tools/tv_closeout_guard.py", body)
        self.assertIn("continue, push_ready, or blocked:*", body)
        self.assertIn("generic review-required", body)

    def test_create_continuation_omits_unavailable_target_profile_skills(self):
        commands = []

        def fake_run(cmd, *, cwd=None, timeout=45):
            commands.append(cmd)
            return '{"id":"t_created"}'

        with patch.object(tv_runner_autostart, "git_head", return_value="abc1234"), \
             patch.object(tv_runner_autostart, "target_profile_skill_names", return_value={"source-and-fidelity", "artifact-governance"}), \
             patch.object(tv_runner_autostart, "run", side_effect=fake_run):
            created = tv_runner_autostart.create_continuation(dry_run=False)

        self.assertEqual(created, "t_created")
        create_cmd = commands[0]
        forced_skills = [create_cmd[index + 1] for index, value in enumerate(create_cmd) if value == "--skill"]
        self.assertEqual(forced_skills, ["source-and-fidelity", "artifact-governance"])
        self.assertNotIn("long-running-task-harness", forced_skills)

    def test_pre_dispatch_preflight_fails_closed_on_checker_error(self):
        with patch.object(tv_runner_autostart, "run_checked", return_value=(1, "ERROR: broken")):
            with self.assertRaises(RuntimeError) as raised:
                tv_runner_autostart.pre_dispatch_preflight(dry_run=False)

        self.assertIn("runner-preflight failed", str(raised.exception))

    def test_idle_dirty_autostart_reports_recovery_preflight_before_seeding(self):
        tasks = [{"id": "t_blocked", "assignee": "terminal-velocity", "status": "blocked"}]
        output = '{"recommended_action":"rerun_focused_verifier"}\n'

        with patch.object(tv_runner_autostart, "board_tasks", return_value=tasks), \
             patch.object(tv_runner_autostart, "assignee_tasks", side_effect=lambda all_tasks, status: [t for t in all_tasks if t["status"] == status]), \
             patch.object(tv_runner_autostart, "git_dirty", return_value=True), \
             patch.object(tv_runner_autostart, "git_status_summary", return_value="## main...origin/main; M native_ev/scenario_eval.py"), \
             patch.object(tv_runner_autostart, "recovery_preflight", return_value=(1, output)), \
             patch.object(tv_runner_autostart, "save_state") as save_state, \
             patch("builtins.print") as printed:
            code = tv_runner_autostart.main([])

        self.assertEqual(code, 0)
        save_state.assert_called()
        lines = [call.args[0] for call in printed.call_args_list]
        self.assertTrue(any("recovery preflight" in line for line in lines))
        self.assertIn(output.strip(), lines)


if __name__ == "__main__":
    unittest.main()
