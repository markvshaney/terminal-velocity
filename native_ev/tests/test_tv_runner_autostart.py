import json
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

    def test_continuation_body_leaves_adjacent_batching_to_integrator(self):
        body = tv_runner_autostart.continuation_body("abc1234")

        self.assertIn("Implement one smallest coherent", body)
        self.assertIn("adjacent-increment batching, checkpoint bundling, and successor seeding belong to the integration owner", body)
        self.assertIn("Do not create a successor continuation task from the worker when the worktree has unintegrated dirty handoff files", body)
        self.assertNotIn("Implement one or more adjacent", body)

    def test_integration_owner_close_push_ready_dry_run_does_not_apply(self):
        commands = []

        def fake_run_checked(cmd, *, cwd=None, timeout=45):
            commands.append(cmd)
            return 0, '{"decision":"hold","blockers":[]}'

        with patch.object(tv_runner_autostart, "run_checked", side_effect=fake_run_checked):
            code, _ = tv_runner_autostart.integration_owner_close_push_ready(dry_run=True)

        self.assertEqual(code, 0)
        self.assertEqual(len(commands), 1)
        command = commands[0]
        self.assertIn("--dry-run", command)
        self.assertIn("--recover-push-ready-handoff", command)
        self.assertIn("--normalize-gates", command)
        self.assertIn("--blocked-report-target", command)
        self.assertIn(tv_runner_autostart.LOKI_GAMETV_TARGET, command)
        self.assertNotIn("--apply-push-ready-recovery", command)
        self.assertNotIn("--apply-gate-comments", command)

    def test_integration_owner_publish_posts_bundle_report_only_from_push_path(self):
        commands = []

        def fake_run_checked(cmd, *, cwd=None, timeout=45):
            commands.append(cmd)
            return 0, '{"decision":"publish","blockers":[],"pushed":true}'

        with patch.object(tv_runner_autostart, "run_checked", side_effect=fake_run_checked):
            code, _ = tv_runner_autostart.integration_owner_publish(dry_run=False)

        self.assertEqual(code, 0)
        command = commands[0]
        self.assertIn("--push", command)
        self.assertIn("--llm-approved", command)
        self.assertIn("--post-push-report-target", command)
        self.assertIn(tv_runner_autostart.LOKI_GAMETV_TARGET, command)
        self.assertIn("--blocked-report-target", command)
        self.assertNotIn("--post-push-report-dry-run", command)

    def test_integration_owner_publish_dry_run_renders_but_does_not_send_bundle_report(self):
        commands = []

        def fake_run_checked(cmd, *, cwd=None, timeout=45):
            commands.append(cmd)
            return 0, '{"decision":"publish","blockers":[]}'

        with patch.object(tv_runner_autostart, "run_checked", side_effect=fake_run_checked):
            code, _ = tv_runner_autostart.integration_owner_publish(dry_run=True)

        self.assertEqual(code, 0)
        command = commands[0]
        self.assertIn("--dry-run", command)
        self.assertIn("--post-push-report-target", command)
        self.assertIn("--post-push-report-dry-run", command)
        self.assertIn("--blocked-report-target", command)
        self.assertNotIn("--push", command)

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

    def test_start_resume_preflight_blocks_dispatch_when_not_safe(self):
        tasks = [{"id": "t_ready", "assignee": "terminal-velocity", "status": "ready"}]
        packet = {"recommended_action": "blocked:topology_conflict", "explicit_gate": "topology_conflict", "safe_to_start": False}

        with patch.object(tv_runner_autostart, "board_tasks", return_value=tasks), \
             patch.object(tv_runner_autostart, "assignee_tasks", side_effect=lambda all_tasks, status: [t for t in all_tasks if t["status"] == status]), \
             patch.object(tv_runner_autostart, "start_resume_preflight", return_value=(1, packet)), \
             patch.object(tv_runner_autostart, "dispatch") as dispatch, \
             patch.object(tv_runner_autostart, "save_state") as save_state, \
             patch("builtins.print") as printed:
            code = tv_runner_autostart.main([])

        self.assertEqual(code, 0)
        dispatch.assert_not_called()
        save_state.assert_called()
        lines = [call.args[0] for call in printed.call_args_list]
        self.assertTrue(any("start/resume preflight blocked" in line for line in lines))
        self.assertIn(json.dumps(tv_runner_autostart.compact_preflight_result(packet), indent=2, sort_keys=True), lines)
        self.assertNotIn(json.dumps(packet, indent=2, sort_keys=True), lines)

    def test_idle_clean_autostart_consumes_start_resume_preflight_before_seeding(self):
        packet = {"recommended_action": "start_gateway_kanban_dispatcher", "explicit_gate": None, "safe_to_start": True}

        with patch.object(tv_runner_autostart, "board_tasks", return_value=[]), \
             patch.object(tv_runner_autostart, "assignee_tasks", return_value=[]), \
             patch.object(tv_runner_autostart, "git_dirty", return_value=False), \
             patch.object(tv_runner_autostart, "start_resume_preflight", return_value=(0, packet)) as preflight, \
             patch.object(tv_runner_autostart, "pre_dispatch_preflight", return_value="ok"), \
             patch.object(tv_runner_autostart, "create_continuation", return_value="t_created"), \
             patch.object(tv_runner_autostart, "dispatch", return_value="dry-run-dispatch"), \
             patch.object(tv_runner_autostart, "git_status_summary", return_value="## main...origin/main"), \
             patch.object(tv_runner_autostart, "save_state"), \
             patch("builtins.print"):
            code = tv_runner_autostart.main([])

        self.assertEqual(code, 0)
        preflight.assert_called_once()

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

    def test_idle_dirty_checkpoint_ready_runs_integration_owner_then_seeds_once(self):
        tasks = [{"id": "t_blocked", "assignee": "terminal-velocity", "status": "blocked"}]
        recovery = {"recommended_action": "checkpoint_and_push_ready", "explicit_gate": None}
        checkpoint = {
            "recommended_action": "push_ready",
            "explicit_gate": None,
            "checkpoint": {"created": True, "commit": "abc123"},
        }
        publish = {"decision": "publish", "blockers": [], "pushed": True, "head": "abc123", "origin_main": "abc123"}
        closeout = {"decision": "hold", "blockers": [], "push_ready_recovery": {"closeouts_written": 1}}

        with patch.object(tv_runner_autostart, "board_tasks", return_value=tasks), \
             patch.object(tv_runner_autostart, "assignee_tasks", side_effect=lambda all_tasks, status: [t for t in all_tasks if t["status"] == status]), \
             patch.object(tv_runner_autostart, "git_dirty", return_value=True), \
             patch.object(tv_runner_autostart, "git_status_summary", return_value="## main...origin/main"), \
             patch.object(tv_runner_autostart, "recovery_preflight", return_value=(0, json.dumps(recovery))), \
             patch.object(tv_runner_autostart, "checkpoint_handoff", return_value=(0, json.dumps(checkpoint))) as checkpoint_handoff, \
             patch.object(tv_runner_autostart, "integration_owner_publish", return_value=(0, json.dumps(publish))) as publish_owner, \
             patch.object(tv_runner_autostart, "integration_owner_close_push_ready", return_value=(0, json.dumps(closeout))) as close_push_ready, \
             patch.object(tv_runner_autostart, "require_start_resume_safe", return_value=True), \
             patch.object(tv_runner_autostart, "pre_dispatch_preflight", return_value="ok"), \
             patch.object(tv_runner_autostart, "create_continuation", return_value="t_created") as create_continuation, \
             patch.object(tv_runner_autostart, "dispatch", return_value="dispatched t_created") as dispatch, \
             patch.object(tv_runner_autostart, "save_state") as save_state, \
             patch("builtins.print") as printed:
            code = tv_runner_autostart.main([])

        self.assertEqual(code, 0)
        checkpoint_handoff.assert_called_once_with(tasks, False)
        publish_owner.assert_called_once_with(False)
        close_push_ready.assert_called_once_with(False)
        create_continuation.assert_called_once_with(False)
        dispatch.assert_called_once_with(False)
        save_state.assert_called()
        lines = [call.args[0] for call in printed.call_args_list]
        self.assertTrue(any("integration-owner recovered push_ready handoff" in line for line in lines))
        self.assertTrue(any("seeded and dispatched continuation t_created" in line for line in lines))

    def test_idle_dirty_checkpoint_ready_reports_explicit_gate_when_publish_blocked(self):
        tasks = [{"id": "t_blocked", "assignee": "terminal-velocity", "status": "blocked"}]
        recovery = {"recommended_action": "checkpoint_and_push_ready", "explicit_gate": None}
        checkpoint = {
            "recommended_action": "push_ready",
            "explicit_gate": None,
            "checkpoint": {"created": True, "commit": "abc123"},
        }
        publish = {"decision": "needs_human", "blockers": ["branch_behind_origin"], "pushed": False}

        with patch.object(tv_runner_autostart, "board_tasks", return_value=tasks), \
             patch.object(tv_runner_autostart, "assignee_tasks", side_effect=lambda all_tasks, status: [t for t in all_tasks if t["status"] == status]), \
             patch.object(tv_runner_autostart, "git_dirty", return_value=True), \
             patch.object(tv_runner_autostart, "git_status_summary", return_value="## main...origin/main"), \
             patch.object(tv_runner_autostart, "recovery_preflight", return_value=(0, json.dumps(recovery))), \
             patch.object(tv_runner_autostart, "checkpoint_handoff", return_value=(0, json.dumps(checkpoint))), \
             patch.object(tv_runner_autostart, "integration_owner_publish", return_value=(2, json.dumps(publish))), \
             patch.object(tv_runner_autostart, "create_continuation") as create_continuation, \
             patch.object(tv_runner_autostart, "dispatch") as dispatch, \
             patch.object(tv_runner_autostart, "save_state"), \
             patch("builtins.print") as printed:
            code = tv_runner_autostart.main([])

        self.assertEqual(code, 0)
        create_continuation.assert_not_called()
        dispatch.assert_not_called()
        lines = [call.args[0] for call in printed.call_args_list]
        self.assertTrue(any("explicit_gate" in line for line in lines))
        self.assertTrue(any("branch_behind_origin" in line for line in lines))

    def test_handoff_queue_plan_classifies_push_ready_as_queue_not_global_block(self):
        tasks = [
            {"id": "t_handoff", "assignee": "terminal-velocity", "status": "blocked", "blocked_reason": "push_ready: verified slice awaiting integration"},
            {"id": "t_other", "assignee": "terminal-velocity", "status": "blocked", "blocked_reason": "blocked:source_uncertainty"},
        ]

        plan = tv_runner_autostart.handoff_queue_plan(tasks, target_active_workers=3)

        self.assertEqual(plan["queued_handoff_ids"], ["t_handoff"])
        self.assertEqual(plan["global_blocker_ids"], ["t_other"])
        self.assertEqual(plan["recommended_spawns"], 0)
        self.assertEqual(plan["flow_state_by_task"]["t_handoff"], "integration_queued")

    def test_handoff_queue_plan_returns_recommended_non_conflicting_batch_and_holds_overlap(self):
        tasks = [
            {
                "id": "t_docs",
                "assignee": "terminal-velocity",
                "status": "blocked",
                "blocked_reason": "push_ready: verified slice awaiting integration",
                "changed_files": ["docs/research/tv-spec.md"],
            },
            {
                "id": "t_model",
                "assignee": "terminal-velocity",
                "status": "blocked",
                "blocked_reason": "push_ready: verified slice awaiting integration",
                "runs": [{"metadata": {"changed_files": ["native_ev/model.py"]}}],
            },
            {
                "id": "t_docs_overlap",
                "assignee": "terminal-velocity",
                "status": "blocked",
                "blocked_reason": "push_ready: verified slice awaiting integration",
                "changed_files": ["docs/research/ev-classic-quirk-review-ledger.md"],
            },
        ]

        plan = tv_runner_autostart.handoff_queue_plan(tasks, target_active_workers=4)

        self.assertEqual(plan["queued_handoff_ids"], ["t_docs", "t_model", "t_docs_overlap"])
        self.assertEqual(plan["recommended_integration_batch"]["handoff_ids"], ["t_docs", "t_model"])
        self.assertEqual(plan["recommended_integration_batch"]["conflict_domains"], ["docs/research", "native_ev/model.py"])
        self.assertEqual([item["id"] for item in plan["held_handoffs"]], ["t_docs_overlap"])
        self.assertEqual(plan["held_handoffs"][0]["conflicts_with_domains"], ["docs/research"])
        self.assertEqual(plan["queued_handoffs"][0]["flow_state"], "integration_queued")

    def test_handoff_queue_plan_recommends_spawn_tasks_from_unassigned_ready_backlog(self):
        tasks = [
            {"id": "t_running", "assignee": "terminal-velocity", "status": "running"},
            {"id": "t_ready_a", "assignee": None, "status": "ready", "title": "Ready A"},
            {"id": "t_ready_b", "assignee": "", "status": "ready", "title": "Ready B"},
            {"id": "t_other", "assignee": "other-profile", "status": "ready", "title": "Other"},
        ]

        plan = tv_runner_autostart.handoff_queue_plan(tasks, target_active_workers=3)

        self.assertEqual(plan["recommended_spawns"], 2)
        self.assertEqual([item["id"] for item in plan["recommended_spawn_tasks"]], ["t_ready_a", "t_ready_b"])
        self.assertEqual(plan["active_like_count"], 1)

    def test_clean_lane_with_only_queued_push_ready_handoff_seeds_unrelated_worker(self):
        tasks = [{"id": "t_handoff", "assignee": "terminal-velocity", "status": "blocked", "blocked_reason": "push_ready: verified slice awaiting integration"}]
        preflight_packet = {
            "recommended_action": "recover_push_ready_handoff",
            "explicit_gate": "push_ready_integration_required",
            "safe_to_start": False,
            "machine_result": {"blocked_handoffs": {"push_ready": 1}},
        }

        with patch.object(tv_runner_autostart, "board_tasks", return_value=tasks), \
             patch.object(tv_runner_autostart, "assignee_tasks", side_effect=lambda all_tasks, status: [t for t in all_tasks if t["status"] == status]), \
             patch.object(tv_runner_autostart, "git_dirty", return_value=False), \
             patch.object(tv_runner_autostart, "start_resume_preflight", return_value=(1, preflight_packet)), \
             patch.object(tv_runner_autostart, "pre_dispatch_preflight", return_value="ok"), \
             patch.object(tv_runner_autostart, "create_continuation", return_value="t_created") as create_continuation, \
             patch.object(tv_runner_autostart, "dispatch", return_value="dispatched t_created") as dispatch, \
             patch.object(tv_runner_autostart, "git_status_summary", return_value="## main...origin/main"), \
             patch.object(tv_runner_autostart, "save_state") as save_state, \
             patch("builtins.print") as printed:
            code = tv_runner_autostart.main([])

        self.assertEqual(code, 0)
        create_continuation.assert_called_once_with(False)
        dispatch.assert_called_once_with(False)
        save_state.assert_called()
        lines = [call.args[0] for call in printed.call_args_list]
        self.assertTrue(any("queued_handoffs=1" in line for line in lines))


if __name__ == "__main__":
    unittest.main()
