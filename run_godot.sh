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
  tv-service-provisioning-log Run service/store provisioning scout log
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
  tv-mission-alignment-return-log Run alignment return-contract offer timing log
  tv-mission-alignment-delivery-log Run alignment branch delivery/completion log
  tv-mission-route-hint-log Run mission destination route hint log
  tv-mission-trade-destination-sale-log Run mission/trade destination-sale log
  tv-chapter-one-trade-carryover-log Run chapter-one mission/trade carryover log
  tv-mission-trade-return-margin-log Run chapter-one return-leg trade margin log
  tv-trade-margin-choice-log Run trade margin choice/negative-margin skip log
  tv-mission-abort-log Run mission abort/reserved cargo release log
  tv-mission-abort-reaccept-log Run mission abort/reaccept/delivery recovery log
  tv-mission-abort-forbidden-log Run non-abortable mission return-cleanup guardrail log
  tv-mission-abort-penalty-log Run mission abort reputation-penalty guardrail log
  tv-mission-auto-abort-log Run mission auto-abort completion flag guardrail log
  tv-mission-scan-failure-log Run mission cargo scan-failure guardrail log
  tv-mission-deadline-failure-log Run mission deadline failure/recovery log
  tv-mission-deadline-last-day-log Run mission deadline last-day delivery log
  tv-mission-deadline-completed-log Run mission deadline completed/no-late-failure log
  tv-mission-deadline-recovery-log Run post-deadline failure follow-up recovery log
  tv-mission-deadline-sequential-log Run mission deadline sequential-failures log
  tv-mission-deadline-abort-log Run mission deadline abort/no-late-failure log
  tv-mission-deadline-trade-carryover-log Run mission deadline trade-carryover log
  tv-mission-log-history-log Run mission log completed/aborted/failed history log
  tv-active-mission-deadline-log Run active mission deadline display log
  tv-first-mission-delivery-log Run first mission acceptance/delivery log
  tv-pilot-save-resume-log Run pilot save/resume log
  tv-outfitter-shipyard-log Run outfitter/shipyard purchase progression log
  tv-repair-service-log Run landed repair service/hull restoration log
  tv-gameplay-curriculum-help-log Run gameplay curriculum help/hint log
  tv-starting-equipment-log Run starting equipment/status fidelity log
  tv-pirate-avoidance-log Run noncombat pirate-avoidance route scaffold log
  tv-combat-log          Run primary weapon combat scaffold log
  tv-combat-reward-log   Run combat disable reward persistence scaffold log
  tv-combat-guardrail-log Run primary weapon cooldown/blocking guardrail log
  tv-player-disabled-log Run disabled-player guardrail/recovery scaffold log
  tv-shield-recharge-log Run player shield recharge scaffold log
  tv-retaliation-log    Run NPC retaliation cadence scaffold log
  tv-projectile-motion-log Run projectile motion/lifetime scaffold log
  tv-explosion-log       Run explosion visual lifetime scaffold log
  tv-cargo-salvage-log  Run combat cargo salvage pickup scaffold log
  tv-secondary-weapon-log Run secondary weapon selection/fire scaffold log
  tv-target-selection-log Run target cycle/closest selection log
  tv-autopilot-log      Run autopilot assist scaffold log
  tv-navigation-guardrail-log Run navigation blocked-reason guardrail log
  tv-legal-status-log    Run legal/reputation status scaffold log
  tv-legal-docking-log   Run legal-gated docking refusal log
  tv-legal-service-gate-log Run legal-gated service/shop refusal log
  tv-weapon-reputation-gate-log Run weapon service reputation-gate refusal log
  tv-weapon-credit-gate-log Run weapon insufficient-credit recovery log
  tv-weapon-availability-gate-log Run weapon store availability recovery log
  tv-weapon-inventory-stack-log Run repeated weapon purchase inventory stack log
  tv-weapon-secondary-activation-log Run weapon purchase-to-secondary activation log
  tv-weapon-mission-cargo-log Run weapon purchase with active mission cargo log
  tv-weapon-trade-cargo-log Run weapon purchase with held trade cargo log
  tv-weapon-legal-docking-log Run weapon purchase after legal docking recovery log
  tv-light-freighter-bulk-margin-log Run Light Freighter bulk margin choice log
  tv-light-freighter-bulk-mission-margin-log Run Light Freighter bulk mission margin log
  tv-light-freighter-refuel-mission-margin-log Run Light Freighter refuel mission margin log
  tv-light-freighter-mission-trade-log Run Light Freighter mission/trade cargo log
  tv-light-freighter-repair-trade-log Run Light Freighter repair-margin trade log
  tv-light-freighter-repair-mission-trade-log Run Light Freighter mission/trade repair-margin log
  tv-light-freighter-repair-refuel-mission-trade-log Run Light Freighter mission/trade repair/refuel-margin log
  tv-light-freighter-deadline-repair-refuel-log Run Light Freighter deadline repair/refuel margin log
  tv-legal-patrol-posture-log Run legal patrol warning/hostile posture log
  tv-mission-legal-eligibility-log Run mission legal eligibility gate log
  tv-mission-story-gate-log Run mission story-flag gate log
  tv-mission-alignment-gate-log Run mission alignment story/reputation/legal gate log
  tv-legal-consequence-log Run inferred legal patrol attack consequence log
  tv-legal-clemency-log Run inferred landed legal clemency log
  tv-contraband-scan-log Run inferred contraband scan/fine log
  tv-contraband-risk-log Run commodity exchange contraband risk surface log
  tv-contraband-scan-trade-log Run contraband scan/legal-cargo sale recovery log
  tv-contraband-clemency-funding-log Run contraband scan/trade-funded clemency log
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
    tv-movement-log|tv-afterburner-log|tv-travel-event-log|tv-landed-ui-matrix|tv-service-provisioning-log|tv-map-route-log|tv-route-invalid-log|tv-route-clear-log|tv-route-clear-reselect-log|tv-route-jump-log|tv-route-land-refuel-log|tv-low-fuel-jump-log|tv-near-center-jump-log|tv-commodity-trade-log|tv-mission-offer-scan-log|tv-mission-chain-offer-log|tv-mission-chain-lock-log|tv-mission-alignment-branch-log|tv-mission-alignment-return-log|tv-mission-alignment-delivery-log|tv-mission-route-hint-log|tv-mission-trade-destination-sale-log|tv-chapter-one-trade-carryover-log|tv-mission-trade-return-margin-log|tv-trade-margin-choice-log|tv-mission-abort-log|tv-mission-abort-reaccept-log|tv-mission-abort-forbidden-log|tv-mission-abort-penalty-log|tv-mission-auto-abort-log|tv-mission-scan-failure-log|tv-mission-deadline-failure-log|tv-mission-deadline-last-day-log|tv-mission-deadline-completed-log|tv-mission-deadline-recovery-log|tv-mission-deadline-sequential-log|tv-mission-deadline-abort-log|tv-mission-deadline-trade-carryover-log|tv-mission-log-history-log|tv-active-mission-deadline-log|tv-first-mission-delivery-log|tv-pilot-save-resume-log|tv-outfitter-shipyard-log|tv-repair-service-log|tv-gameplay-curriculum-help-log|tv-starting-equipment-log|tv-pirate-avoidance-log|tv-combat-log|tv-combat-reward-log|tv-combat-guardrail-log|tv-player-disabled-log|tv-shield-recharge-log|tv-retaliation-log|tv-projectile-motion-log|tv-explosion-log|tv-cargo-salvage-log|tv-secondary-weapon-log|tv-target-selection-log|tv-autopilot-log|tv-navigation-guardrail-log|tv-legal-status-log|tv-legal-docking-log|tv-legal-service-gate-log|tv-weapon-reputation-gate-log|tv-weapon-credit-gate-log|tv-weapon-availability-gate-log|tv-weapon-inventory-stack-log|tv-weapon-secondary-activation-log|tv-weapon-mission-cargo-log|tv-weapon-trade-cargo-log|tv-weapon-legal-docking-log|tv-light-freighter-bulk-margin-log|tv-light-freighter-bulk-mission-margin-log|tv-light-freighter-refuel-mission-margin-log|tv-light-freighter-mission-trade-log|tv-light-freighter-repair-trade-log|tv-light-freighter-repair-mission-trade-log|tv-light-freighter-repair-refuel-mission-trade-log|tv-light-freighter-deadline-repair-refuel-log|tv-legal-patrol-posture-log|tv-mission-legal-eligibility-log|tv-mission-story-gate-log|tv-mission-alignment-gate-log|tv-legal-consequence-log|tv-legal-clemency-log|tv-contraband-scan-log|tv-contraband-risk-log|tv-contraband-scan-trade-log|tv-contraband-clemency-funding-log)
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
