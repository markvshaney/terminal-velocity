import unittest
from unittest.mock import patch

from tools import tv_runner_autostart


class TvRunnerAutostartTests(unittest.TestCase):
    def test_continuation_body_requires_runner_preflight_before_work_selection(self):
        body = tv_runner_autostart.continuation_body("abc1234")

        self.assertIn("python3 tools/backlog_dispatch_index.py runner-preflight", body)
        self.assertIn("before selecting work", body)

    def test_pre_dispatch_preflight_fails_closed_on_checker_error(self):
        with patch.object(tv_runner_autostart, "run_checked", return_value=(1, "ERROR: broken")):
            with self.assertRaises(RuntimeError) as raised:
                tv_runner_autostart.pre_dispatch_preflight(dry_run=False)

        self.assertIn("runner-preflight failed", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
