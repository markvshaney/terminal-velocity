param(
    [switch]$SelfTest,
    [switch]$MovementLog,
    [switch]$TravelEventLog,
    [switch]$LandedUiMatrix,
    [switch]$MapRouteLog,
    [switch]$RouteJumpLog,
    [switch]$RouteLandRefuelLog,
    [switch]$LowFuelJumpLog,
    [switch]$NearCenterJumpLog,
    [switch]$CommodityTradeLog,
    [switch]$MissionOfferScanLog,
    [switch]$MissionRouteHintLog,
    [switch]$FirstMissionDeliveryLog,
    [switch]$PilotSaveResumeLog,
    [switch]$OutfitterShipyardLog,
    [switch]$GameplayCurriculumHelpLog,
    [switch]$CombatLog,
    [switch]$CombatGuardrailLog,
    [switch]$NavigationGuardrailLog,
    [switch]$LegalStatusLog,
    [switch]$LegalServiceGateLog,
    [switch]$LegalPatrolPostureLog,
    [switch]$MissionLegalEligibilityLog,
    [switch]$LegalConsequenceLog,
    [switch]$LegalClemencyLog,
    [switch]$ContrabandScanLog,
    [switch]$ContrabandRiskLog
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
} elseif ($TravelEventLog) {
    & $Godot --headless --path $Project -- --tv-travel-event-log
} elseif ($LandedUiMatrix) {
    & $Godot --headless --path $Project -- --tv-landed-ui-matrix
} elseif ($MapRouteLog) {
    & $Godot --headless --path $Project -- --tv-map-route-log
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
} elseif ($MissionRouteHintLog) {
    & $Godot --headless --path $Project -- --tv-mission-route-hint-log
} elseif ($FirstMissionDeliveryLog) {
    & $Godot --headless --path $Project -- --tv-first-mission-delivery-log
} elseif ($PilotSaveResumeLog) {
    & $Godot --headless --path $Project -- --tv-pilot-save-resume-log
} elseif ($OutfitterShipyardLog) {
    & $Godot --headless --path $Project -- --tv-outfitter-shipyard-log
} elseif ($GameplayCurriculumHelpLog) {
    & $Godot --headless --path $Project -- --tv-gameplay-curriculum-help-log
} elseif ($CombatLog) {
    & $Godot --headless --path $Project -- --tv-combat-log
} elseif ($CombatGuardrailLog) {
    & $Godot --headless --path $Project -- --tv-combat-guardrail-log
} elseif ($NavigationGuardrailLog) {
    & $Godot --headless --path $Project -- --tv-navigation-guardrail-log
} elseif ($LegalStatusLog) {
    & $Godot --headless --path $Project -- --tv-legal-status-log
} elseif ($LegalServiceGateLog) {
    & $Godot --headless --path $Project -- --tv-legal-service-gate-log
} elseif ($LegalPatrolPostureLog) {
    & $Godot --headless --path $Project -- --tv-legal-patrol-posture-log
} elseif ($MissionLegalEligibilityLog) {
    & $Godot --headless --path $Project -- --tv-mission-legal-eligibility-log
} elseif ($LegalConsequenceLog) {
    & $Godot --headless --path $Project -- --tv-legal-consequence-log
} elseif ($LegalClemencyLog) {
    & $Godot --headless --path $Project -- --tv-legal-clemency-log
} elseif ($ContrabandScanLog) {
    & $Godot --headless --path $Project -- --tv-contraband-scan-log
} elseif ($ContrabandRiskLog) {
    & $Godot --headless --path $Project -- --tv-contraband-risk-log
} else {
    & $Godot --path $Project
}
