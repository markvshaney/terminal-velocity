param(
    [switch]$SelfTest,
    [switch]$MovementLog
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
} else {
    & $Godot --path $Project
}
