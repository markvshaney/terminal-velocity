import json
import tempfile
import unittest
from pathlib import Path

from tools.basilisk_speed_qualification import (
    check_basilisk_speed_qualification,
    validate_basilisk_speed_qualification,
)


VALID_MATRIX = {
    "schema_version": 1,
    "entries": [
        {
            "evidence_family": "runtime-ui",
            "lane_id": "basilisk-lane-1",
            "speed": "4x",
            "qualification_class": "promotion-grade non-timing",
            "sentinel_used": "1x-starting-hud-state-comparison",
            "verifier": "manual capture comparison plus screenshot notes",
            "last_checked": "2026-06-09",
            "status": "qualified",
            "restore_readiness": "known_save_state_available",
            "capture_readiness": "screenshots_reliable",
            "input_readiness": "single-step_menu_input_reliable",
            "allowed_oracle_classes": ["runtime-ui"],
            "disallowed_oracle_classes": ["timing-feel", "combat-cadence"],
            "promotion_limitations": [
                "not valid for timing/feel",
                "not valid for combat cadence",
            ],
        }
    ],
}


class BasiliskSpeedQualificationTests(unittest.TestCase):
    def test_validates_qualified_non_timing_entry(self):
        result = validate_basilisk_speed_qualification(VALID_MATRIX)

        self.assertTrue(result.ok, result.errors)

    def test_rejects_timing_or_combat_allowed_without_1x_sentinel(self):
        matrix = json.loads(json.dumps(VALID_MATRIX))
        matrix["entries"][0]["allowed_oracle_classes"] = ["timing-feel"]
        matrix["entries"][0]["sentinel_used"] = "none"

        result = validate_basilisk_speed_qualification(matrix)

        self.assertFalse(result.ok)
        self.assertIn("1x sentinel", "\n".join(result.errors))

    def test_check_reads_checked_in_json_and_reports_ok(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "basilisk-speed-qualification.json"
            path.write_text(json.dumps(VALID_MATRIX, indent=2) + "\n")

            result = check_basilisk_speed_qualification(path)

        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
