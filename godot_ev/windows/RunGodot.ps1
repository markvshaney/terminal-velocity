param(
    [switch]$SelfTest,
    [switch]$MovementLog,
    [switch]$AfterburnerLog,
    [switch]$TravelEventLog,
    [switch]$LandedUiMatrix,
    [switch]$ServiceProvisioningLog,
    [switch]$MapRouteLog,
    [switch]$RouteInvalidLog,
    [switch]$RouteClearLog,
    [switch]$RouteClearReselectLog,
    [switch]$RouteJumpLog,
    [switch]$RouteLandRefuelLog,
    [switch]$LowFuelJumpLog,
    [switch]$NearCenterJumpLog,
    [switch]$CommodityTradeLog,
    [switch]$MissionOfferScanLog,
    [switch]$MissionChainOfferLog,
    [switch]$MissionChainLockLog,
    [switch]$MissionAlignmentBranchLog,
    [switch]$MissionAlignmentReturnLog,
    [switch]$MissionRouteHintLog,
    [switch]$MissionTradeDestinationSaleLog,
    [switch]$ChapterOneTradeCarryoverLog,
    [switch]$MissionAbortLog,
    [switch]$MissionAbortForbiddenLog,
    [switch]$MissionAbortPenaltyLog,
    [switch]$MissionAutoAbortLog,
    [switch]$MissionScanFailureLog,
    [switch]$MissionDeadlineFailureLog,
    [switch]$MissionDeadlineLastDayLog,
    [switch]$MissionDeadlineCompletedLog,
    [switch]$MissionDeadlineRecoveryLog,
    [switch]$MissionDeadlineSequentialLog,
    [switch]$MissionDeadlineAbortLog,
    [switch]$MissionDeadlineTradeCarryoverLog,
    [switch]$MissionLogHistoryLog,
    [switch]$ActiveMissionDeadlineLog,
    [switch]$FirstMissionDeliveryLog,
    [switch]$PilotSaveResumeLog,
    [switch]$OutfitterShipyardLog,
    [switch]$RepairServiceLog,
    [switch]$GameplayCurriculumHelpLog,
    [switch]$StartingEquipmentLog,
    [switch]$PirateAvoidanceLog,
    [switch]$CombatLog,
    [switch]$CombatGuardrailLog,
    [switch]$PlayerDisabledLog,
    [switch]$ShieldRechargeLog,
    [switch]$RetaliationLog,
    [switch]$ProjectileMotionLog,
    [switch]$ExplosionLog,
    [switch]$CargoSalvageLog,
    [switch]$SecondaryWeaponLog,
    [switch]$TargetSelectionLog,
    [switch]$AutopilotLog,
    [switch]$NavigationGuardrailLog,
    [switch]$LegalStatusLog,
    [switch]$LegalDockingLog,
    [switch]$LegalServiceGateLog,
    [switch]$WeaponReputationGateLog,
    [switch]$WeaponCreditGateLog,
    [switch]$WeaponAvailabilityGateLog,
    [switch]$WeaponInventoryStackLog,
    [switch]$WeaponMissionCargoLog,
    [switch]$WeaponTradeCargoLog,
    [switch]$WeaponLegalDockingLog,
    [switch]$LightFreighterMissionTradeLog,
    [switch]$LightFreighterRepairTradeLog,
    [switch]$LightFreighterRepairMissionTradeLog,
    [switch]$LightFreighterRepairRefuelMissionTradeLog,
    [switch]$LightFreighterDeadlineRepairRefuelLog,
    [switch]$LegalPatrolPostureLog,
    [switch]$MissionLegalEligibilityLog,
    [switch]$MissionStoryGateLog,
    [switch]$MissionAlignmentGateLog,
    [switch]$LegalConsequenceLog,
    [switch]$LegalClemencyLog,
    [switch]$ContrabandScanLog,
    [switch]$ContrabandRiskLog,
    [switch]$ContrabandScanTradeLog,
    [switch]$ContrabandClemencyFundingLog
)

$Godot = "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\Godot_v4.6.2-stable_win64_console.exe"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).ProviderPath

if (!(Test-Path $Godot)) {
    throw "Godot executable not found: $Godot"
}
if (!(Test-Path (Join-Path $Project "project.godot"))) {
    throw "Godot project not found: $Project"
}

if ($SelfTest) {
    & $Godot --headless --path $Project --script "res://scripts/self_test.gd"
} elseif ($MovementLog) {
    & $Godot --headless --path $Project -- --tv-movement-log
} elseif ($AfterburnerLog) {
    & $Godot --headless --path $Project -- --tv-afterburner-log
} elseif ($TravelEventLog) {
    & $Godot --headless --path $Project -- --tv-travel-event-log
} elseif ($LandedUiMatrix) {
    & $Godot --headless --path $Project -- --tv-landed-ui-matrix
} elseif ($ServiceProvisioningLog) {
    & $Godot --headless --path $Project -- --tv-service-provisioning-log
} elseif ($MapRouteLog) {
    & $Godot --headless --path $Project -- --tv-map-route-log
} elseif ($RouteInvalidLog) {
    & $Godot --headless --path $Project -- --tv-route-invalid-log
} elseif ($RouteClearLog) {
    & $Godot --headless --path $Project -- --tv-route-clear-log
} elseif ($RouteClearReselectLog) {
    & $Godot --headless --path $Project -- --tv-route-clear-reselect-log
} elseif ($RouteJumpLog) {
    & $Godot --headless --path $Project -- --tv-route-jump-log
} elseif ($RouteLandRefuelLog) {
    & $Godot --headless --path $Project -- --tv-route-land-refuel-log
} elseif ($LowFuelJumpLog) {
    & $Godot --headless --path $Project -- --tv-low-fuel-jump-log
} elseif ($NearCenterJumpLog) {
    & $Godot --headless --path $Project -- --tv-near-center-jump-log
} elseif ($CommodityTradeLog) {
    & $Godot --headless --path $Project -- --tv-commodity-trade-log
} elseif ($MissionOfferScanLog) {
    & $Godot --headless --path $Project -- --tv-mission-offer-scan-log
} elseif ($MissionChainOfferLog) {
    & $Godot --headless --path $Project -- --tv-mission-chain-offer-log
} elseif ($MissionChainLockLog) {
    & $Godot --headless --path $Project -- --tv-mission-chain-lock-log
} elseif ($MissionAlignmentBranchLog) {
    & $Godot --headless --path $Project -- --tv-mission-alignment-branch-log
} elseif ($MissionAlignmentReturnLog) {
    & $Godot --headless --path $Project -- --tv-mission-alignment-return-log
} elseif ($MissionRouteHintLog) {
    & $Godot --headless --path $Project -- --tv-mission-route-hint-log
} elseif ($MissionTradeDestinationSaleLog) {
    & $Godot --headless --path $Project -- --tv-mission-trade-destination-sale-log
} elseif ($ChapterOneTradeCarryoverLog) {
    & $Godot --headless --path $Project -- --tv-chapter-one-trade-carryover-log
} elseif ($MissionAbortLog) {
    & $Godot --headless --path $Project -- --tv-mission-abort-log
} elseif ($MissionAbortForbiddenLog) {
    & $Godot --headless --path $Project -- --tv-mission-abort-forbidden-log
} elseif ($MissionAbortPenaltyLog) {
    & $Godot --headless --path $Project -- --tv-mission-abort-penalty-log
} elseif ($MissionAutoAbortLog) {
    & $Godot --headless --path $Project -- --tv-mission-auto-abort-log
} elseif ($MissionScanFailureLog) {
    & $Godot --headless --path $Project -- --tv-mission-scan-failure-log
} elseif ($MissionDeadlineFailureLog) {
    & $Godot --headless --path $Project -- --tv-mission-deadline-failure-log
} elseif ($MissionDeadlineLastDayLog) {
    & $Godot --headless --path $Project -- --tv-mission-deadline-last-day-log
} elseif ($MissionDeadlineCompletedLog) {
    & $Godot --headless --path $Project -- --tv-mission-deadline-completed-log
} elseif ($MissionDeadlineRecoveryLog) {
    & $Godot --headless --path $Project -- --tv-mission-deadline-recovery-log
} elseif ($MissionDeadlineSequentialLog) {
    & $Godot --headless --path $Project -- --tv-mission-deadline-sequential-log
} elseif ($MissionDeadlineAbortLog) {
    & $Godot --headless --path $Project -- --tv-mission-deadline-abort-log
} elseif ($MissionDeadlineTradeCarryoverLog) {
    & $Godot --headless --path $Project -- --tv-mission-deadline-trade-carryover-log
} elseif ($MissionLogHistoryLog) {
    & $Godot --headless --path $Project -- --tv-mission-log-history-log
} elseif ($ActiveMissionDeadlineLog) {
    & $Godot --headless --path $Project -- --tv-active-mission-deadline-log
} elseif ($FirstMissionDeliveryLog) {
    & $Godot --headless --path $Project -- --tv-first-mission-delivery-log
} elseif ($PilotSaveResumeLog) {
    & $Godot --headless --path $Project -- --tv-pilot-save-resume-log
} elseif ($OutfitterShipyardLog) {
    & $Godot --headless --path $Project -- --tv-outfitter-shipyard-log
} elseif ($RepairServiceLog) {
    & $Godot --headless --path $Project -- --tv-repair-service-log
} elseif ($GameplayCurriculumHelpLog) {
    & $Godot --headless --path $Project -- --tv-gameplay-curriculum-help-log
} elseif ($StartingEquipmentLog) {
    & $Godot --headless --path $Project -- --tv-starting-equipment-log
} elseif ($PirateAvoidanceLog) {
    & $Godot --headless --path $Project -- --tv-pirate-avoidance-log
} elseif ($CombatLog) {
    & $Godot --headless --path $Project -- --tv-combat-log
} elseif ($CombatGuardrailLog) {
    & $Godot --headless --path $Project -- --tv-combat-guardrail-log
} elseif ($PlayerDisabledLog) {
    & $Godot --headless --path $Project -- --tv-player-disabled-log
} elseif ($ShieldRechargeLog) {
    & $Godot --headless --path $Project -- --tv-shield-recharge-log
} elseif ($RetaliationLog) {
    & $Godot --headless --path $Project -- --tv-retaliation-log
} elseif ($ProjectileMotionLog) {
    & $Godot --headless --path $Project -- --tv-projectile-motion-log
} elseif ($ExplosionLog) {
    & $Godot --headless --path $Project -- --tv-explosion-log
} elseif ($CargoSalvageLog) {
    & $Godot --headless --path $Project -- --tv-cargo-salvage-log
} elseif ($SecondaryWeaponLog) {
    & $Godot --headless --path $Project -- --tv-secondary-weapon-log
} elseif ($TargetSelectionLog) {
    & $Godot --headless --path $Project -- --tv-target-selection-log
} elseif ($AutopilotLog) {
    & $Godot --headless --path $Project -- --tv-autopilot-log
} elseif ($NavigationGuardrailLog) {
    & $Godot --headless --path $Project -- --tv-navigation-guardrail-log
} elseif ($LegalStatusLog) {
    & $Godot --headless --path $Project -- --tv-legal-status-log
} elseif ($LegalDockingLog) {
    & $Godot --headless --path $Project -- --tv-legal-docking-log
} elseif ($LegalServiceGateLog) {
    & $Godot --headless --path $Project -- --tv-legal-service-gate-log
} elseif ($WeaponReputationGateLog) {
    & $Godot --headless --path $Project -- --tv-weapon-reputation-gate-log
} elseif ($WeaponCreditGateLog) {
    & $Godot --headless --path $Project -- --tv-weapon-credit-gate-log
} elseif ($WeaponAvailabilityGateLog) {
    & $Godot --headless --path $Project -- --tv-weapon-availability-gate-log
} elseif ($WeaponInventoryStackLog) {
    & $Godot --headless --path $Project -- --tv-weapon-inventory-stack-log
} elseif ($WeaponMissionCargoLog) {
    & $Godot --headless --path $Project -- --tv-weapon-mission-cargo-log
} elseif ($WeaponTradeCargoLog) {
    & $Godot --headless --path $Project -- --tv-weapon-trade-cargo-log
} elseif ($WeaponLegalDockingLog) {
    & $Godot --headless --path $Project -- --tv-weapon-legal-docking-log
} elseif ($LightFreighterMissionTradeLog) {
    & $Godot --headless --path $Project -- --tv-light-freighter-mission-trade-log
} elseif ($LightFreighterRepairTradeLog) {
    & $Godot --headless --path $Project -- --tv-light-freighter-repair-trade-log
} elseif ($LightFreighterRepairMissionTradeLog) {
    & $Godot --headless --path $Project -- --tv-light-freighter-repair-mission-trade-log
} elseif ($LightFreighterRepairRefuelMissionTradeLog) {
    & $Godot --headless --path $Project -- --tv-light-freighter-repair-refuel-mission-trade-log
} elseif ($LightFreighterDeadlineRepairRefuelLog) {
    & $Godot --headless --path $Project -- --tv-light-freighter-deadline-repair-refuel-log
} elseif ($LegalPatrolPostureLog) {
    & $Godot --headless --path $Project -- --tv-legal-patrol-posture-log
} elseif ($MissionLegalEligibilityLog) {
    & $Godot --headless --path $Project -- --tv-mission-legal-eligibility-log
} elseif ($MissionStoryGateLog) {
    & $Godot --headless --path $Project -- --tv-mission-story-gate-log
} elseif ($MissionAlignmentGateLog) {
    & $Godot --headless --path $Project -- --tv-mission-alignment-gate-log
} elseif ($LegalConsequenceLog) {
    & $Godot --headless --path $Project -- --tv-legal-consequence-log
} elseif ($LegalClemencyLog) {
    & $Godot --headless --path $Project -- --tv-legal-clemency-log
} elseif ($ContrabandScanLog) {
    & $Godot --headless --path $Project -- --tv-contraband-scan-log
} elseif ($ContrabandRiskLog) {
    & $Godot --headless --path $Project -- --tv-contraband-risk-log
} elseif ($ContrabandScanTradeLog) {
    & $Godot --headless --path $Project -- --tv-contraband-scan-trade-log
} elseif ($ContrabandClemencyFundingLog) {
    & $Godot --headless --path $Project -- --tv-contraband-clemency-funding-log
} else {
    & $Godot --path $Project
}
