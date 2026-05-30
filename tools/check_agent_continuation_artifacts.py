#!/usr/bin/env python3
"""Lint Terminal Velocity continuation-process artifacts.

This is a cheap guard against the recurring process bug where a stored
continuation prompt or closeout block makes an agent stop after one safe local
slice instead of running the post-slice gate check and continuing.
"""
from __future__ import annotations

import argparse
from pathlib import Path


REPO_CHECKS = {
    "docs/prompts/terminal-velocity-continuation-prompt.md": [
        "Stored-artifact regression checklist before implementation",
        "exact artifact read with line numbers?",
        "Post-slice gate template before using the closeout block",
        "Do not stop at recommendations or at a completed slice",
        "push/PR/publication gate on the just-finished commit is not a blocker",
        "Closeout format only when the autonomous run is genuinely ending",
        "no other safe local slice remains available",
    ],
    "docs/checklists/agent-continuation-process-failure-remediation.md": [
        "The exact artifact must be read before executing instructions derived from it",
        "Skills explicitly named by a stored artifact must be loaded before acting on that artifact",
        "Slice-boundary gate check",
        "If another safe local slice exists and no real gate/cap blocks it, start that slice instead of final-reporting",
    ],
}

OPTIONAL_PROFILE_CHECKS = {
    "skills/gaming/ev-terminal-velocity-play/SKILL.md": [
        "follow, resume, continue, or find a stored Terminal Velocity prompt/artifact/handoff",
        "first locate and read the exact artifact",
        "stored-continuation-artifact-and-slice-boundary-failures.md",
    ],
    "skills/gaming/ev-terminal-velocity-play/references/stored-continuation-artifact-and-slice-boundary-failures.md": [
        "mechanism existed but was not reached/applied",
        "At the slice boundary, run the gate check below before reporting",
        "Start the next safe local slice",
    ],
    "skills/gaming/ev-terminal-velocity-play/references/terminal-velocity-autonomous-restart-prompt.md": [
        "Stored-artifact regression checklist before implementation",
        "Post-slice gate template before using the closeout block",
        "Closeout format only when the autonomous run is genuinely ending",
        "start the next safe local slice",
    ],
    "skills/software-development/source-and-fidelity/SKILL.md": [
        "stored prompt/artifact/handoff references",
        "Terminal Velocity continuation requests that say to follow, resume, continue from, or find a stored prompt/artifact/handoff",
    ],
    "skills/software-development/game-prototyping/SKILL.md": [
        "Terminal Velocity work starts from a stored continuation prompt/artifact/handoff",
    ],
    "skills/gaming/ev-classic-basilisk-observation/SKILL.md": [
        "A stored Terminal Velocity continuation prompt/artifact/handoff names original EV Classic",
    ],
}


def check_file(root: Path, rel: str, needles: list[str], *, optional: bool = False) -> list[str]:
    path = root / rel
    if not path.exists():
        return [] if optional else [f"missing file: {rel}"]
    text = path.read_text(encoding="utf-8")
    return [f"{rel}: missing required phrase: {needle!r}" for needle in needles if needle not in text]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Terminal Velocity repo root")
    parser.add_argument(
        "--profile-home",
        default=None,
        help="Optional Loki Game profile home to lint profile-local skill safeguards",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    failures: list[str] = []
    for rel, needles in REPO_CHECKS.items():
        failures.extend(check_file(repo, rel, needles))

    if args.profile_home:
        profile_home = Path(args.profile_home).expanduser().resolve()
        for rel, needles in OPTIONAL_PROFILE_CHECKS.items():
            failures.extend(check_file(profile_home, rel, needles))

    if failures:
        print("CONTINUATION ARTIFACT CHECK FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CONTINUATION ARTIFACT CHECK OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
