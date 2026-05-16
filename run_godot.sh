#!/usr/bin/env bash
set -euo pipefail
GODOT_EXE="${GODOT_EXE:-C:\\Users\\bh\\AppData\\Local\\Microsoft\\WinGet\\Packages\\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\\Godot_v4.6.2-stable_win64_console.exe}"
PROJECT_DIR="$(wslpath -w "$(pwd)/godot_ev")"
powershell.exe -NoProfile -Command "& '$GODOT_EXE' --path '$PROJECT_DIR'"
