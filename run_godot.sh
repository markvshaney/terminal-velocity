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
  tv-travel-event-log     Run travel event log
  tv-landed-ui-matrix     Run landed UI matrix log
  tv-map-route-log        Run map route log
  tv-route-jump-log       Run route jump log
  tv-route-land-refuel-log Run route/land/refuel log
  tv-low-fuel-jump-log    Run blocked low-fuel jump log
  tv-near-center-jump-log Run blocked near-system-center jump log
  tv-commodity-trade-log  Run commodity buy/sell round-trip log
  tv-mission-offer-scan-log Run mission offer scan log
  tv-mission-route-hint-log Run mission destination route hint log
  tv-first-mission-delivery-log Run first mission acceptance/delivery log
  tv-pilot-save-resume-log Run pilot save/resume log
  tv-outfitter-shipyard-log Run outfitter/shipyard purchase progression log
  tv-gameplay-curriculum-help-log Run gameplay curriculum help/hint log
  tv-combat-log          Run primary weapon combat scaffold log
  tv-combat-guardrail-log Legacy alias for primary weapon combat scaffold log
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
    tv-movement-log|tv-travel-event-log|tv-landed-ui-matrix|tv-map-route-log|tv-route-jump-log|tv-route-land-refuel-log|tv-low-fuel-jump-log|tv-near-center-jump-log|tv-commodity-trade-log|tv-mission-offer-scan-log|tv-mission-route-hint-log|tv-first-mission-delivery-log|tv-pilot-save-resume-log|tv-outfitter-shipyard-log|tv-gameplay-curriculum-help-log|tv-combat-log|tv-combat-guardrail-log|tv-navigation-guardrail-log|tv-legal-status-log|tv-legal-service-gate-log|tv-legal-patrol-posture-log|tv-mission-legal-eligibility-log|tv-legal-consequence-log|tv-legal-clemency-log|tv-contraband-scan-log|tv-contraband-risk-log)
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
