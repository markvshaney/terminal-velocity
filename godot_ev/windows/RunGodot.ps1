param(
    [switch]$SelfTest,
    [switch]$MovementLog,
    [switch]$TravelEventLog,
    [switch]$LandedUiMatrix,
    [switch]$MapRouteLog,
    [switch]$RouteJumpLog,
    [switch]$RouteLandRefuelLog,
    [switch]$LowFuelJumpLog,
    [switch]$CommodityTradeLog,
    [switch]$MissionOfferScanLog,
    [switch]$MissionRouteHintLog,
    [switch]$FirstMissionDeliveryLog,
    [switch]$PilotSaveResumeLog,
    [switch]$OutfitterShipyardLog
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
} else {
    & $Godot --path $Project
}
