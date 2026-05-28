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
    tv-movement-log|tv-travel-event-log|tv-landed-ui-matrix|tv-map-route-log|tv-route-jump-log|tv-route-land-refuel-log|tv-low-fuel-jump-log)
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
