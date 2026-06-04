#!/usr/bin/env bash
set -euo pipefail

GODOT_EXE="${GODOT_EXE:-C:\\Users\\bh\\AppData\\Local\\Microsoft\\WinGet\\Packages\\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\\Godot_v4.6.2-stable_win64_console.exe}"
PROJECT_DIR="$(wslpath -w "$(pwd)/godot_ev")"

usage() {
    cat <<'USAGE'
Usage: ./run_godot.sh [mode]

Modes:
  play                    Launch the Godot project editor/runtime window (default)
  self-test               Run the headless Godot selftest
  tv-movement-log         Run deterministic movement log
  tv-afterburner-log      Run afterburner thrust/fuel scaffold log
  tv-travel-event-log     Run travel event log
  tv-landed-ui-matrix     Run landed UI matrix log
  tv-map-route-log        Run map route log
  tv-route-invalid-log    Run invalid/duplicate map route guardrail log
  tv-route-clear-log      Run explicit queued route clear guardrail log
  tv-route-clear-reselect-log Run clear-then-reselect route recovery log
  tv-route-jump-log       Run route jump log
  tv-route-land-refuel-log Run route/land/refuel log
  tv-low-fuel-jump-log    Run blocked low-fuel jump log
  tv-near-center-jump-log Run blocked near-system-center jump log
  tv-commodity-trade-log  Run commodity buy/sell round-trip log
  tv-mission-offer-scan-log Run mission offer scan log
  tv-mission-chain-offer-log Run post-delivery mission chain offer log
  tv-mission-chain-lock-log Run mission story-chain lock/blocked reason log
  tv-mission-alignment-branch-log Run post-chain alignment branch offer log
  tv-mission-route-hint-log Run mission destination route hint log
  tv-mission-abort-log Run mission abort/reserved cargo release log
  tv-mission-deadline-failure-log Run mission deadline failure/recovery log
  tv-mission-log-history-log Run mission log completed/aborted/failed history log
  tv-active-mission-deadline-log Run active mission deadline display log
  tv-first-mission-delivery-log Run first mission acceptance/delivery log
  tv-pilot-save-resume-log Run pilot save/resume log
  tv-outfitter-shipyard-log Run outfitter/shipyard purchase progression log
  tv-repair-service-log Run landed repair service/hull restoration log
  tv-gameplay-curriculum-help-log Run gameplay curriculum help/hint log
  tv-combat-log          Run primary weapon combat scaffold log
  tv-combat-guardrail-log Legacy alias for primary weapon combat scaffold log
  tv-cargo-salvage-log  Run combat cargo salvage pickup scaffold log
  tv-secondary-weapon-log Run secondary weapon selection/fire scaffold log
  tv-target-selection-log Run target cycle/closest selection log
  tv-autopilot-log      Run autopilot assist scaffold log
  tv-navigation-guardrail-log Run navigation blocked-reason guardrail log
  tv-legal-status-log    Run legal/reputation status scaffold log
  tv-legal-service-gate-log Run legal-gated service/shop refusal log
  tv-legal-patrol-posture-log Run legal patrol warning/hostile posture log
  tv-mission-legal-eligibility-log Run mission legal eligibility gate log
  tv-legal-consequence-log Run inferred legal patrol attack consequence log
  tv-legal-clemency-log Run inferred landed legal clemency log
  tv-contraband-scan-log Run inferred contraband scan/fine log
  tv-contraband-risk-log Run commodity exchange contraband risk surface log
USAGE
}

mode="${1:-play}"
case "$mode" in
    play)
        powershell.exe -NoProfile -Command "& '$GODOT_EXE' --path '$PROJECT_DIR'"
        ;;
    self-test)
        powershell.exe -NoProfile -Command "& '$GODOT_EXE' --headless --path '$PROJECT_DIR' --script 'res://scripts/self_test.gd'"
        ;;
    tv-movement-log|tv-afterburner-log|tv-travel-event-log|tv-landed-ui-matrix|tv-map-route-log|tv-route-invalid-log|tv-route-clear-log|tv-route-clear-reselect-log|tv-route-jump-log|tv-route-land-refuel-log|tv-low-fuel-jump-log|tv-near-center-jump-log|tv-commodity-trade-log|tv-mission-offer-scan-log|tv-mission-chain-offer-log|tv-mission-chain-lock-log|tv-mission-alignment-branch-log|tv-mission-route-hint-log|tv-mission-abort-log|tv-mission-deadline-failure-log|tv-mission-log-history-log|tv-active-mission-deadline-log|tv-first-mission-delivery-log|tv-pilot-save-resume-log|tv-outfitter-shipyard-log|tv-repair-service-log|tv-gameplay-curriculum-help-log|tv-combat-log|tv-combat-guardrail-log|tv-cargo-salvage-log|tv-secondary-weapon-log|tv-target-selection-log|tv-autopilot-log|tv-navigation-guardrail-log|tv-legal-status-log|tv-legal-service-gate-log|tv-legal-patrol-posture-log|tv-mission-legal-eligibility-log|tv-legal-consequence-log|tv-legal-clemency-log|tv-contraband-scan-log|tv-contraband-risk-log)
        powershell.exe -NoProfile -Command "& '$GODOT_EXE' --headless --path '$PROJECT_DIR' -- --$mode"
        ;;
    -h|--help|help)
        usage
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac
