#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIN_DIR="/mnt/c/Users/bh/Games/TerminalVelocity"
mkdir -p "$WIN_DIR/assets/ships/shuttle" "$WIN_DIR/assets/ships/light_freighter" "$WIN_DIR/data"
cp "$ROOT/native_ev/windows/TerminalVelocity.ps1" "$WIN_DIR/TerminalVelocity.ps1"
cp "$ROOT/native_ev/assets/ships/shuttle"/frame_*.png "$WIN_DIR/assets/ships/shuttle/"
cp "$ROOT/native_ev/assets/ships/light_freighter"/frame_*.png "$WIN_DIR/assets/ships/light_freighter/"
for ship in lightning argosy frigate; do
  mkdir -p "$WIN_DIR/assets/ships/$ship"
  cp "$ROOT/native_ev/assets/ships/$ship"/frame_*.png "$WIN_DIR/assets/ships/$ship/"
done
cp "$ROOT/native_ev/data/universe.json" "$WIN_DIR/data/universe.json"
cp "$ROOT/native_ev/data/ships.json" "$WIN_DIR/data/ships.json"
cp "$ROOT/native_ev/data/weapons.json" "$WIN_DIR/data/weapons.json"
cp "$ROOT/native_ev/data/missions.json" "$WIN_DIR/data/missions.json"
cp "$ROOT/native_ev/data/outfits.json" "$WIN_DIR/data/outfits.json"
cp "$ROOT/native_ev/data/economy.json" "$WIN_DIR/data/economy.json"
cp "$ROOT/native_ev/data/governments.json" "$WIN_DIR/data/governments.json"
cp "$ROOT/native_ev/data/sourced_ev_names.json" "$WIN_DIR/data/sourced_ev_names.json"
cp "$ROOT/native_ev/data/sourced_ev_structures.json" "$WIN_DIR/data/sourced_ev_structures.json"
powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File 'C:\Users\bh\Games\TerminalVelocity\TerminalVelocity.ps1'
