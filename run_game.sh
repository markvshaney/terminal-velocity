#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIN_DIR="/mnt/c/Users/bh/Games/TerminalVelocity"
mkdir -p "$WIN_DIR/assets/ships" "$WIN_DIR/data"
cp "$ROOT/native_ev/windows/TerminalVelocity.ps1" "$WIN_DIR/TerminalVelocity.ps1"
for ship_dir in "$ROOT/native_ev/assets/ships"/*; do
  [ -d "$ship_dir" ] || continue
  ship="$(basename "$ship_dir")"
  mkdir -p "$WIN_DIR/assets/ships/$ship"
  cp "$ship_dir"/frame_*.png "$WIN_DIR/assets/ships/$ship/" 2>/dev/null || true
done
if [ -d "$ROOT/native_ev/assets/ships/ev_classic" ]; then
  mkdir -p "$WIN_DIR/assets/ships/ev_classic"
  cp -R "$ROOT/native_ev/assets/ships/ev_classic"/* "$WIN_DIR/assets/ships/ev_classic/"
fi
cp "$ROOT/native_ev/data"/*.json "$WIN_DIR/data/"
powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File 'C:\Users\bh\Games\TerminalVelocity\TerminalVelocity.ps1'
