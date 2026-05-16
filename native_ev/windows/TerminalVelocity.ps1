param(
    [switch]$SelfTest,
    [switch]$Autopilot,
    [int]$AutoCloseSeconds = 0
)

Add-Type -AssemblyName PresentationCore,PresentationFramework,WindowsBase

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$gameRoot = $scriptDir
$parentDir = Split-Path -Parent $scriptDir
if (!(Test-Path (Join-Path $gameRoot 'data\ships.json')) -and (Test-Path (Join-Path $parentDir 'data\ships.json'))) {
    $gameRoot = $parentDir
}
$assetDir = Join-Path $gameRoot 'assets\ships\shuttle'
$dataPath = Join-Path $gameRoot 'data\universe.json'
$shipsPath = Join-Path $gameRoot 'data\ships.json'
$weaponsPath = Join-Path $gameRoot 'data\weapons.json'
$missionsPath = Join-Path $gameRoot 'data\missions.json'
$outfitsPath = Join-Path $gameRoot 'data\outfits.json'
$economyPath = Join-Path $gameRoot 'data\economy.json'
$governmentsPath = Join-Path $gameRoot 'data\governments.json'
$savePath = Join-Path $gameRoot 'savegame.json'
if ($SelfTest) {
    $savePath = Join-Path ([System.IO.Path]::GetTempPath()) 'terminal_velocity_selftest_save.json'
    if (Test-Path $savePath) { Remove-Item $savePath -Force }
}

function New-Text($text, $x, $y, $size = 14, $color = 'White') {
    $t = New-Object Windows.Controls.TextBlock
    $t.Text = $text
    $t.FontFamily = 'Consolas'
    $t.FontSize = $size
    $t.Foreground = $color
    [Windows.Controls.Canvas]::SetLeft($t, $x)
    [Windows.Controls.Canvas]::SetTop($t, $y)
    return $t
}

function Clamp($v, $lo, $hi) {
    if ($v -lt $lo) { return $lo }
    if ($v -gt $hi) { return $hi }
    return $v
}

function Dist($ax, $ay, $bx, $by) {
    $dx = $ax - $bx
    $dy = $ay - $by
    return [Math]::Sqrt($dx * $dx + $dy * $dy)
}

function Load-Bitmap($path) {
    $bmp = New-Object Windows.Media.Imaging.BitmapImage
    $bmp.BeginInit()
    $bmp.CacheOption = [Windows.Media.Imaging.BitmapCacheOption]::OnLoad
    $bmp.UriSource = New-Object Uri($path, [UriKind]::Absolute)
    $bmp.EndInit()
    $bmp.Freeze()
    return $bmp
}

# Window and scene root
$window = New-Object Windows.Window
$window.Title = 'Terminal Velocity - Native EV-style Prototype'
$window.Width = 1024
$window.Height = 768
$window.WindowStartupLocation = 'CenterScreen'
$window.Background = 'Black'

$canvas = New-Object Windows.Controls.Canvas
$canvas.Width = 1024
$canvas.Height = 768
$canvas.Background = 'Black'
$window.Content = $canvas

# Load file-backed ship definitions, weapons, and original facings.
if (!(Test-Path $shipsPath)) { throw "Missing ships data file: $shipsPath" }
if (!(Test-Path $weaponsPath)) { throw "Missing weapons data file: $weaponsPath" }
if (!(Test-Path $missionsPath)) { throw "Missing missions data file: $missionsPath" }
if (!(Test-Path $outfitsPath)) { throw "Missing outfits data file: $outfitsPath" }
if (!(Test-Path $economyPath)) { throw "Missing economy data file: $economyPath" }
if (!(Test-Path $governmentsPath)) { throw "Missing governments data file: $governmentsPath" }
$rawShips = Get-Content -Raw $shipsPath | ConvertFrom-Json
$rawWeapons = Get-Content -Raw $weaponsPath | ConvertFrom-Json
$rawMissions = Get-Content -Raw $missionsPath | ConvertFrom-Json
$rawOutfits = Get-Content -Raw $outfitsPath | ConvertFrom-Json
$rawEconomy = Get-Content -Raw $economyPath | ConvertFrom-Json
$rawGovernments = Get-Content -Raw $governmentsPath | ConvertFrom-Json
$missionDefs = @{}
foreach ($mission in $rawMissions.missions) { $missionDefs[[string]$mission.id] = $mission }
$weaponDefs = @{}
foreach ($weapon in $rawWeapons.weapons) { $weaponDefs[[string]$weapon.id] = $weapon }
$outfitDefs = @{}
foreach ($outfit in $rawOutfits.outfits) { $outfitDefs[[string]$outfit.id] = $outfit }
$shipyardListings = @($rawOutfits.shipyard)
$repairPricePerHullPoint = [int]$rawOutfits.repair.pricePerHullPoint
$commodityDefs = @{}
$commodityList = @($rawEconomy.commodities)
foreach ($commodity in $commodityList) { $commodityDefs[[string]$commodity.id] = $commodity }
$governmentDefs = @{}
foreach ($govProp in $rawGovernments.governments.PSObject.Properties) { $governmentDefs[[string]$govProp.Name] = $govProp.Value }
$shipDefs = @{}
$shipFrameSets = @{}
foreach ($ship in $rawShips.ships) {
    $shipDefs[[string]$ship.id] = $ship
    $dir = Join-Path $gameRoot ([string]$ship.assetDir).Replace('/', '\')
    $frames = @()
    for ($i = 0; $i -lt [int]$ship.frameCount; $i++) {
        $p = Join-Path $dir ('frame_{0:D2}.png' -f $i)
        if (Test-Path $p) { $frames += Load-Bitmap $p }
    }
    if ($frames.Count -ne [int]$ship.frameCount) { throw "Ship $($ship.id) expected $($ship.frameCount) frames, got $($frames.Count)" }
    $shipFrameSets[[string]$ship.id] = $frames
}
$playerShipId = 'shuttle'
$playerShipDef = $shipDefs[$playerShipId]
$shipFrames = $shipFrameSets[$playerShipId]
if ($shipFrames.Count -eq 0) { throw "No shuttle frames found from $shipsPath" }

$shipImage = New-Object Windows.Controls.Image
$shipImage.Width = [double]$playerShipDef.width
$shipImage.Height = [double]$playerShipDef.height
$shipImage.Source = $shipFrames[0]
$canvas.Children.Add($shipImage) | Out-Null

$hud = New-Text '' 12 10 14 'LightGreen'
$canvas.Children.Add($hud) | Out-Null
$message = New-Text '' 12 708 14 'Khaki'
$canvas.Children.Add($message) | Out-Null
$scanner = New-Text '' 760 10 13 'LightSkyBlue'
$canvas.Children.Add($scanner) | Out-Null
$targetReticle = New-Object Windows.Shapes.Rectangle
$targetReticle.Width = 80
$targetReticle.Height = 80
$targetReticle.Stroke = 'Yellow'
$targetReticle.StrokeThickness = 1
$targetReticle.Visibility = 'Hidden'
$canvas.Children.Add($targetReticle) | Out-Null

$landingPanel = New-Object Windows.Controls.Border
$landingPanel.Width = 760
$landingPanel.Height = 520
$landingPanel.Background = '#DD050508'
$landingPanel.BorderBrush = 'Gray'
$landingPanel.BorderThickness = 2
[Windows.Controls.Canvas]::SetLeft($landingPanel, 132)
[Windows.Controls.Canvas]::SetTop($landingPanel, 100)
$landingText = New-Object Windows.Controls.TextBlock
$landingText.FontFamily = 'Consolas'
$landingText.FontSize = 15
$landingText.Foreground = 'White'
$landingText.Margin = 18
$landingText.TextWrapping = 'Wrap'
$landingPanel.Child = $landingText
$landingPanel.Visibility = 'Hidden'
$canvas.Children.Add($landingPanel) | Out-Null

$mapPanel = New-Object Windows.Controls.Border
$mapPanel.Width = 560
$mapPanel.Height = 420
$mapPanel.Background = '#EE000018'
$mapPanel.BorderBrush = 'DodgerBlue'
$mapPanel.BorderThickness = 2
[Windows.Controls.Canvas]::SetLeft($mapPanel, 232)
[Windows.Controls.Canvas]::SetTop($mapPanel, 145)
$mapText = New-Object Windows.Controls.TextBlock
$mapText.FontFamily = 'Consolas'
$mapText.FontSize = 15
$mapText.Foreground = 'White'
$mapText.Margin = 18
$mapText.TextWrapping = 'Wrap'
$mapPanel.Child = $mapText
$mapPanel.Visibility = 'Hidden'
$canvas.Children.Add($mapPanel) | Out-Null

# Visual object pools.
$bodyShapes = @()
$starShapes = @()
for ($i = 0; $i -lt 180; $i++) {
    $s = New-Object Windows.Shapes.Ellipse
    $size = Get-Random -Minimum 1 -Maximum 3
    $s.Width = $size
    $s.Height = $size
    $s.Fill = 'White'
    $canvas.Children.Add($s) | Out-Null
    $starShapes += $s
}
for ($i = 0; $i -lt 8; $i++) {
    $b = New-Object Windows.Shapes.Ellipse
    $b.Stroke = 'White'
    $b.StrokeThickness = 1
    $canvas.Children.Add($b) | Out-Null
    $bodyShapes += $b
}

$npcShips = @()
foreach ($traffic in $rawShips.traffic) {
    $sid = [string]$traffic.shipId
    if (!$shipDefs.ContainsKey($sid)) { continue }
    $def = $shipDefs[$sid]
    $img = New-Object Windows.Controls.Image
    $img.Width = [double]$def.width
    $img.Height = [double]$def.height
    $img.Source = $shipFrameSets[$sid][0]
    $canvas.Children.Add($img) | Out-Null
    $label = New-Text ([string]$traffic.name) 0 0 10 'LightGray'
    $canvas.Children.Add($label) | Out-Null
    $rad = (([double]$traffic.heading) - 90.0) * [Math]::PI / 180.0
    $npcShips += @{ ShipId=$sid; Name=[string]$traffic.name; System=[string]$traffic.system; X=[double]$traffic.x; Y=[double]$traffic.y; Heading=[double]$traffic.heading; Speed=[double]$traffic.speed; VX=([Math]::Cos($rad) * [double]$traffic.speed); VY=([Math]::Sin($rad) * [double]$traffic.speed); Image=$img; Label=$label; Width=[double]$def.width; Height=[double]$def.height; Hull=[double]$def.hull; MaxHull=[double]$def.hull; WeaponId=[string]$def.weaponId; Cooldown=0; Faction=[string]$traffic.faction; Disposition=[string]$traffic.disposition; Alive=$true }
}

# Universe is file-backed so autonomous iterations can improve the game by editing data, not code.
if (!(Test-Path $dataPath)) { throw "Missing universe data file: $dataPath" }
$rawUniverse = Get-Content -Raw $dataPath | ConvertFrom-Json
$systems = @()
foreach ($sys in $rawUniverse.systems) {
    $bodies = @()
    foreach ($body in $sys.bodies) {
        $bodies += @{ Name=[string]$body.name; X=[double]$body.x; Y=[double]$body.y; R=[double]$body.r; Color=[string]$body.color; Type=[string]$body.type; Market=[string]$body.market; inventory=$body.inventory }
    }
    $links = @()
    if ($sys.links -ne $null) { foreach ($link in $sys.links) { $links += [string]$link } }
    $systems += @{ Name=[string]$sys.name; X=[double]$sys.x; Y=[double]$sys.y; Links=$links; Bodies=$bodies }
}
if ($systems.Count -eq 0) { throw "Universe data has no systems: $dataPath" }

$jobs = @()
$acceptedJobs = @()
$availableMissions = @()
$activeMissions = @()
$completedMissionIds = @{}
$storyFlags = @{}
$keys = @{}
$state = 'space'
$currentSystemIndex = 0
$selectedSystemIndex = 1
$mapVisible = $false
$dockedAt = $null
$credits = 5000
$cargoSpace = [int]$playerShipDef.cargoSpace
$baseCargoSpace = [int]$playerShipDef.cargoSpace
$cargoUsed = 0
$playerMaxHull = [double]$playerShipDef.hull
$playerHull = $playerMaxHull
$playerMaxFuel = 100.0
$playerWeaponId = [string]$playerShipDef.weaponId
$ownedOutfits = @{}
$commodityHold = @{}
$selectedCommodityIndex = 0
$tradeProfit = 0
$legalStatus = 'Clean'
$totalFinesPaid = 0
$scannedSystems = @{}
$selectedShipyardIndex = 0
$stationOutfitsForSale = @($rawOutfits.outfits)
$stationShipyardListings = @($rawOutfits.shipyard)
$stationWeaponsForSale = @($rawWeapons.weapons)
$selectedWeaponIndex = 0
$playerCooldown = 0
$projectiles = @()
$currentTargetName = $null
$scannerRange = 1400.0

$player = @{ X=240.0; Y=180.0; VX=0.0; VY=0.0; Heading=0.0; Fuel=$playerMaxFuel }

# Deterministic star positions so navigation feels stable.
$stars = @()
for ($i = 0; $i -lt 180; $i++) {
    $stars += @{ X=(Get-Random -Minimum -3200 -Maximum 3200); Y=(Get-Random -Minimum -2400 -Maximum 2400); A=(Get-Random -Minimum 90 -Maximum 255) }
}

function Current-System { return $systems[$currentSystemIndex] }

function System-Index-By-Name($name) {
    for ($i = 0; $i -lt $systems.Count; $i++) {
        if ($systems[$i].Name -eq $name) { return $i }
    }
    return 0
}

function Sorted-Hash-Keys($table) {
    $keys = @()
    foreach ($key in $table.Keys) { $keys += [string]$key }
    return @($keys | Sort-Object)
}

function Mission-Ids($missions) {
    $ids = @()
    foreach ($m in $missions) { $ids += [string]$m.id }
    return $ids
}

function Save-Game {
    $owned = @{}
    foreach ($key in $ownedOutfits.Keys) { $owned[[string]$key] = [int]$ownedOutfits[$key] }
    $hold = @{}
    foreach ($key in $commodityHold.Keys) {
        $hold[[string]$key] = @{ tons=[int]$commodityHold[$key].Tons; basis=[int]$commodityHold[$key].Basis }
    }
    $save = [ordered]@{
        schemaVersion = 1
        credits = [int]$credits
        currentSystem = [string](Current-System).Name
        selectedSystem = [string]$systems[$selectedSystemIndex].Name
        playerShipId = [string]$playerShipId
        playerWeaponId = [string]$playerWeaponId
        playerHull = [double]$playerHull
        playerFuel = [double]$player.Fuel
        cargoUsed = [int]$cargoUsed
        cargoSpace = [int]$cargoSpace
        ownedOutfits = $owned
        commodityHold = $hold
        activeMissionIds = @(Mission-Ids $activeMissions)
        completedMissionIds = @(Sorted-Hash-Keys $completedMissionIds)
        storyFlags = @(Sorted-Hash-Keys $storyFlags)
        legalStatus = [string]$legalStatus
    }
    $save | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $savePath
    $message.Text = ('Game saved: {0}' -f $savePath)
}

function Load-Game {
    if (!(Test-Path $savePath)) { return $false }
    $save = Get-Content -Raw $savePath | ConvertFrom-Json
    if ($save.schemaVersion -ne $null -and [int]$save.schemaVersion -gt 1) { throw "Unsupported save schema: $($save.schemaVersion)" }
    if ($save.currentSystem -ne $null) { $script:currentSystemIndex = System-Index-By-Name ([string]$save.currentSystem) }
    if ($save.selectedSystem -ne $null) { $script:selectedSystemIndex = System-Index-By-Name ([string]$save.selectedSystem) } else { $script:selectedSystemIndex = $script:currentSystemIndex }
    if ($save.playerShipId -ne $null -and $shipDefs.ContainsKey([string]$save.playerShipId)) {
        $script:playerShipId = [string]$save.playerShipId
        $script:playerShipDef = $shipDefs[$playerShipId]
        $script:shipFrames = $shipFrameSets[$playerShipId]
        $shipImage.Width = [double]$playerShipDef.width
        $shipImage.Height = [double]$playerShipDef.height
        $shipImage.Source = $shipFrames[0]
    }
    if ($save.credits -ne $null) { $script:credits = [int]$save.credits }
    if ($save.playerWeaponId -ne $null -and $weaponDefs.ContainsKey([string]$save.playerWeaponId)) { $script:playerWeaponId = [string]$save.playerWeaponId }
    if ($save.ownedOutfits -ne $null) {
        $script:ownedOutfits = @{}
        foreach ($prop in $save.ownedOutfits.PSObject.Properties) { $script:ownedOutfits[[string]$prop.Name] = [int]$prop.Value }
    }
    Recalculate-Player-Stats
    if ($save.playerHull -ne $null) { $script:playerHull = [Math]::Min([double]$save.playerHull, $playerMaxHull) }
    if ($save.playerFuel -ne $null) { $player.Fuel = [Math]::Min([double]$save.playerFuel, $playerMaxFuel) }
    if ($save.cargoUsed -ne $null) { $script:cargoUsed = [int]$save.cargoUsed }
    if ($save.commodityHold -ne $null) {
        $script:commodityHold = @{}
        foreach ($prop in $save.commodityHold.PSObject.Properties) {
            $script:commodityHold[[string]$prop.Name] = @{ Tons=[int]$prop.Value.tons; Basis=[int]$prop.Value.basis }
        }
    }
    $script:activeMissions = @()
    if ($save.activeMissionIds -ne $null) {
        foreach ($id in $save.activeMissionIds) { if ($missionDefs.ContainsKey([string]$id)) { $script:activeMissions += $missionDefs[[string]$id] } }
    }
    $script:completedMissionIds = @{}
    if ($save.completedMissionIds -ne $null) { foreach ($id in $save.completedMissionIds) { $script:completedMissionIds[[string]$id] = $true } }
    $script:storyFlags = @{}
    if ($save.storyFlags -ne $null) { foreach ($flag in $save.storyFlags) { $script:storyFlags[[string]$flag] = $true } }
    if ($save.legalStatus -ne $null) { $script:legalStatus = [string]$save.legalStatus }
    $message.Text = ('Loaded saved game: {0}' -f $savePath)
    return $true
}

function Add-Story-Flags($flags) {
    if ($flags -eq $null) { return }
    foreach ($flag in $flags) {
        $storyFlags[[string]$flag] = $true
    }
}

function Has-Required-Flags($mission) {
    if ($mission.requiresFlags -ne $null) {
        foreach ($flag in $mission.requiresFlags) {
            if (!$storyFlags.ContainsKey([string]$flag)) { return $false }
        }
    }
    if ($mission.excludesFlags -ne $null) {
        foreach ($flag in $mission.excludesFlags) {
            if ($storyFlags.ContainsKey([string]$flag)) { return $false }
        }
    }
    return $true
}

function System-Distance($from, $to) {
    $dx = [double]$to.X - [double]$from.X
    $dy = [double]$to.Y - [double]$from.Y
    return [int][Math]::Round([Math]::Sqrt(($dx * $dx) + ($dy * $dy)))
}

function Route-Risk-Score($destSystemName) {
    $risk = 1
    $govName = 'Unclaimed'
    if ($rawGovernments.systems.$destSystemName -ne $null) { $govName = [string]$rawGovernments.systems.$destSystemName.government }
    if ($governmentDefs.ContainsKey($govName)) {
        $gov = $governmentDefs[$govName]
        if ([double]$gov.scanRange -lt 250.0) { $risk += 1 }
        if ([int]$gov.finePerTon -ge 250) { $risk += 1 }
    }
    foreach ($npc in $npcShips) {
        if ($npc.System -eq $destSystemName -and $npc.Disposition -eq 'hostile') { $risk += 2 }
    }
    return $risk
}

function Cargo-Job-Pay($tons, $distance, $risk) {
    return [int](350 + ([int]$tons * 120) + ([int]$distance * 2) + ([int]$risk * 250))
}

function Has-Service($serviceName) {
    if ($dockedAt -eq $null -or $dockedAt.inventory -eq $null -or $dockedAt.inventory.services -eq $null) { return $true }
    return @($dockedAt.inventory.services) -contains $serviceName
}

function Refresh-Station-Inventory {
    if ($dockedAt -eq $null -or $dockedAt.inventory -eq $null) {
        $script:stationOutfitsForSale = @($rawOutfits.outfits)
        $script:stationShipyardListings = @($rawOutfits.shipyard)
        $script:stationWeaponsForSale = @($rawWeapons.weapons)
        return
    }
    $outfitIds = @($dockedAt.inventory.outfitsForSale | ForEach-Object { [string]$_ })
    $shipIds = @($dockedAt.inventory.shipsForSale | ForEach-Object { [string]$_ })
    $weaponIds = @($dockedAt.inventory.weaponsForSale | ForEach-Object { [string]$_ })
    $script:stationOutfitsForSale = @($rawOutfits.outfits | Where-Object { $outfitIds -contains [string]$_.id })
    $script:stationShipyardListings = @($rawOutfits.shipyard | Where-Object { $shipIds -contains [string]$_.shipId })
    $script:stationWeaponsForSale = @($rawWeapons.weapons | Where-Object { $weaponIds -contains [string]$_.id })
    $script:selectedShipyardIndex = 0
    $script:selectedWeaponIndex = 0
}

function Generate-Jobs($portName) {
    $script:jobs = @()
    $current = Current-System
    $candidates = @($systems | Where-Object { $_.Name -ne $current.Name })
    for ($i = 0; $i -lt 5; $i++) {
        $sys = $candidates[(Get-Random -Minimum 0 -Maximum $candidates.Count)]
        $body = $sys.Bodies[(Get-Random -Minimum 0 -Maximum $sys.Bodies.Count)]
        $tons = Get-Random -Minimum 2 -Maximum 8
        $distance = System-Distance $current $sys
        $risk = Route-Risk-Score $sys.Name
        $pay = Cargo-Job-Pay $tons $distance $risk
        $cargoLabel = 'Freight lot {0}' -f (Get-Random -Minimum 100 -Maximum 999)
        if ($risk -ge 4) { $cargoLabel = 'Hazard bonus freight {0}' -f (Get-Random -Minimum 100 -Maximum 999) }
        elseif ($distance -ge 400) { $cargoLabel = 'Long-haul freight {0}' -f (Get-Random -Minimum 100 -Maximum 999) }
        $script:jobs += @{ Cargo=$cargoLabel; DestSystem=$sys.Name; DestBody=$body.Name; Tons=$tons; Pay=$pay; Distance=$distance; Risk=$risk }
    }
    $script:availableMissions = @()
    foreach ($mission in $rawMissions.missions) {
        if ($completedMissionIds.ContainsKey([string]$mission.id)) { continue }
        $alreadyActive = $false
        foreach ($active in $activeMissions) { if ($active.id -eq $mission.id) { $alreadyActive = $true } }
        if (!$alreadyActive -and (Has-Required-Flags $mission) -and $mission.originSystem -eq (Current-System).Name -and $mission.originBody -eq $portName) {
            $script:availableMissions += $mission
        }
    }
}

function Nearest-Port {
    $nearest = $null
    $nearestD = 999999.0
    foreach ($b in (Current-System).Bodies) {
        $d = Dist $player.X $player.Y $b.X $b.Y
        if ($d -lt $nearestD) { $nearestD = $d; $nearest = $b }
    }
    return @{ Body=$nearest; Distance=$nearestD }
}

function Speed { return [Math]::Sqrt($player.VX * $player.VX + $player.VY * $player.VY) }

function Current-Targets {
    $targets = @()
    foreach ($npc in $npcShips) {
        if ($npc.Alive -and $npc.System -eq (Current-System).Name) { $targets += $npc }
    }
    return $targets
}

function Resolve-Target {
    foreach ($npc in (Current-Targets)) {
        if ($npc.Name -eq $currentTargetName) { return $npc }
    }
    return $null
}

function Target-Nearest {
    $nearest = $null; $nearestD = 999999.0
    foreach ($npc in (Current-Targets)) {
        $d = Dist $player.X $player.Y $npc.X $npc.Y
        if ($d -lt $nearestD -and $d -le $scannerRange) { $nearestD = $d; $nearest = $npc }
    }
    if ($nearest -ne $null) {
        $script:currentTargetName = $nearest.Name
        $message.Text = ('Target locked: {0}' -f $nearest.Name)
    } else {
        $script:currentTargetName = $null
        $message.Text = 'No target in scanner range.'
    }
}

function Cycle-Target {
    $targets = @(Current-Targets | Where-Object { (Dist $player.X $player.Y $_.X $_.Y) -le $scannerRange })
    if ($targets.Count -eq 0) { $script:currentTargetName = $null; $message.Text = 'No target in scanner range.'; return }
    $idx = -1
    for ($i = 0; $i -lt $targets.Count; $i++) { if ($targets[$i].Name -eq $currentTargetName) { $idx = $i; break } }
    $next = ($idx + 1) % $targets.Count
    $script:currentTargetName = $targets[$next].Name
    $message.Text = ('Target locked: {0}' -f $targets[$next].Name)
}

function Dock-If-Possible {
    $n = Nearest-Port
    if ($n.Body -ne $null -and $n.Distance -lt ($n.Body.R + 58) -and (Speed) -lt 45) {
        $script:state = 'landed'
        $script:dockedAt = $n.Body
        $player.VX = 0.0; $player.VY = 0.0
        Complete-Deliveries
        Complete-Missions
        Refresh-Station-Inventory
        Generate-Jobs $dockedAt.Name
    } else {
        $message.Text = 'Get close to a port/planet and slow below 45 before pressing E.'
    }
}

function Complete-Deliveries {
    $remaining = @()
    $completeText = @()
    foreach ($j in $acceptedJobs) {
        if ($j.DestSystem -eq (Current-System).Name -and $j.DestBody -eq $dockedAt.Name) {
            $script:credits += $j.Pay
            $script:cargoUsed -= $j.Tons
            $completeText += ('Delivered {0} to {1}: +{2} credits' -f $j.Cargo, $j.DestBody, $j.Pay)
        } else { $remaining += $j }
    }
    $script:acceptedJobs = $remaining
    if ($completeText.Count -gt 0) { $message.Text = ($completeText -join ' | ') }
}

function Current-Market {
    $systemName = (Current-System).Name
    if ($rawEconomy.markets.$systemName -eq $null) { return $null }
    return $rawEconomy.markets.$systemName
}

function Current-Government-Name {
    $systemName = (Current-System).Name
    if ($rawGovernments.systems.$systemName -eq $null) { return 'Unclaimed' }
    return [string]$rawGovernments.systems.$systemName.government
}

function Current-Government {
    $name = Current-Government-Name
    if ($governmentDefs.ContainsKey($name)) { return $governmentDefs[$name] }
    return $null
}

function Commodity-Tons($cid) {
    if ($commodityHold.ContainsKey($cid)) { return [int]$commodityHold[$cid].Tons }
    return 0
}

function Illegal-Cargo-Ids {
    $govName = Current-Government-Name
    $ids = @()
    if ($rawGovernments.contraband.$govName -ne $null) {
        foreach ($cid in $rawGovernments.contraband.$govName) { $ids += [string]$cid }
    }
    return $ids
}

function Scan-For-Contraband($scannerName) {
    $gov = Current-Government
    if ($gov -eq $null) { return }
    $illegal = @(Illegal-Cargo-Ids)
    if ($illegal.Count -eq 0) { return }
    $tons = 0
    foreach ($cid in $illegal) { $tons += Commodity-Tons $cid }
    if ($tons -le 0) { $script:legalStatus = 'Clean'; return }
    $fine = [int]$gov.finePerTon * $tons
    $script:credits = [Math]::Max(0, $credits - $fine)
    $script:totalFinesPaid += $fine
    foreach ($cid in $illegal) {
        if ($commodityHold.ContainsKey($cid)) {
            $script:cargoUsed -= [int]$commodityHold[$cid].Tons
            $commodityHold[$cid].Tons = 0
            $commodityHold[$cid].Basis = 0
        }
    }
    $script:legalStatus = ('Fined {0} by {1}' -f $fine, $scannerName)
    $message.Text = ('{0} scan: contraband seized, fine {1} credits.' -f $scannerName, $fine)
}

function Selected-Commodity {
    if ($commodityList.Count -eq 0) { return $null }
    return $commodityList[$selectedCommodityIndex]
}

function Cycle-Commodity($delta) {
    if ($commodityList.Count -eq 0) { return }
    $script:selectedCommodityIndex = ($selectedCommodityIndex + $delta + $commodityList.Count) % $commodityList.Count
    $c = Selected-Commodity
    $message.Text = ('Market selected: {0}' -f $c.name)
}

function Buy-Commodity {
    if ($state -ne 'landed') { return }
    $c = Selected-Commodity
    if ($c -eq $null) { return }
    if (($cargoUsed + 1) -gt $cargoSpace) { $message.Text = 'No free cargo space for market purchase.'; return }
    $market = Current-Market
    if ($market -eq $null) { $message.Text = 'No commodity market here.'; return }
    $cid = [string]$c.id
    if ($market.$cid -eq $null) { $message.Text = ('No {0} market here.' -f $c.name); return }
    $price = [int]$market.$cid.buy
    if ($credits -lt $price) { $message.Text = ('{0} costs {1}; not enough credits.' -f $c.name, $price); return }
    $script:credits -= $price
    $script:cargoUsed += 1
    if (!$commodityHold.ContainsKey($cid)) { $commodityHold[$cid] = @{ Tons=0; Basis=0 } }
    $commodityHold[$cid].Tons = [int]$commodityHold[$cid].Tons + 1
    $commodityHold[$cid].Basis = [int]$commodityHold[$cid].Basis + $price
    $message.Text = ('Bought 1 ton {0} for {1} credits.' -f $c.name, $price)
}

function Sell-Commodity {
    if ($state -ne 'landed') { return }
    $c = Selected-Commodity
    if ($c -eq $null) { return }
    $market = Current-Market
    if ($market -eq $null) { $message.Text = 'No commodity market here.'; return }
    $cid = [string]$c.id
    if (!$commodityHold.ContainsKey($cid) -or [int]$commodityHold[$cid].Tons -le 0) { $message.Text = ('No {0} in hold.' -f $c.name); return }
    if ($market.$cid -eq $null) { $message.Text = ('No {0} market here.' -f $c.name); return }
    $price = [int]$market.$cid.sell
    $avgBasis = [int][Math]::Round([double]$commodityHold[$cid].Basis / [double]$commodityHold[$cid].Tons)
    $script:credits += $price
    $script:cargoUsed -= 1
    $commodityHold[$cid].Tons = [int]$commodityHold[$cid].Tons - 1
    $commodityHold[$cid].Basis = [Math]::Max(0, [int]$commodityHold[$cid].Basis - $avgBasis)
    $profit = $price - $avgBasis
    $script:tradeProfit += $profit
    $message.Text = ('Sold 1 ton {0} for {1} credits ({2:+#;-#;0} profit).' -f $c.name, $price, $profit)
}

function Accept-Job($idx) {
    if ($state -ne 'landed') { return }
    if ($idx -lt 0 -or $idx -ge $jobs.Count) { return }
    $j = $jobs[$idx]
    if (($cargoUsed + $j.Tons) -gt $cargoSpace) {
        $message.Text = 'Not enough cargo space.'
        return
    }
    $script:acceptedJobs += $j
    $script:cargoUsed += $j.Tons
    $script:jobs = @($jobs | Where-Object { $_ -ne $j })
    $message.Text = ('Accepted {0} tons to {1}/{2}.' -f $j.Tons, $j.DestSystem, $j.DestBody)
}

function Accept-Mission($idx) {
    if ($state -ne 'landed') { return }
    if ($idx -lt 0 -or $idx -ge $availableMissions.Count) { return }
    $m = $availableMissions[$idx]
    if (($cargoUsed + [int]$m.cargoTons) -gt $cargoSpace) { $message.Text = 'Not enough cargo space for mission.'; return }
    $script:activeMissions += $m
    Add-Story-Flags $m.setsFlags
    $script:cargoUsed += [int]$m.cargoTons
    $script:availableMissions = @($availableMissions | Where-Object { $_.id -ne $m.id -and (Has-Required-Flags $_) })
    $message.Text = ('Mission accepted: {0} -> {1}/{2}' -f $m.title, $m.destinationSystem, $m.destinationBody)
}

function Complete-Missions {
    if ($dockedAt -eq $null) { return }
    $remaining = @()
    $completeText = @()
    foreach ($m in $activeMissions) {
        if ($m.destinationSystem -eq (Current-System).Name -and $m.destinationBody -eq $dockedAt.Name) {
            $script:credits += [int]$m.reward
            $script:cargoUsed -= [int]$m.cargoTons
            $completedMissionIds[[string]$m.id] = $true
            Add-Story-Flags $m.completionFlags
            $completeText += ('Mission complete: {0}: +{1} credits' -f $m.title, $m.reward)
        } else { $remaining += $m }
    }
    $script:activeMissions = $remaining
    if ($completeText.Count -gt 0) { $message.Text = ($completeText -join ' | ') }
}

function Hyperspace {
    if ($state -ne 'space') { return }
    if ($player.Fuel -lt 10) { $message.Text = 'Not enough fuel to hyperspace.'; return }
    $destIndex = $selectedSystemIndex
    if ($destIndex -eq $currentSystemIndex) { $message.Text = 'Already in selected system.'; return }
    $current = Current-System
    $dest = $systems[$destIndex]
    if ($current.Links.Count -gt 0 -and !($current.Links -contains $dest.Name)) {
        $message.Text = ('No hyperspace link from {0} to {1}.' -f $current.Name, $dest.Name)
        return
    }
    $script:currentSystemIndex = $destIndex
    $script:currentTargetName = $null
    $script:projectiles = @()
    $player.X = 260.0; $player.Y = 200.0; $player.VX *= 0.25; $player.VY *= 0.25; $player.Fuel -= 10.0
    $message.Text = ('Entered {0} system.' -f (Current-System).Name)
}

function Select-System($delta) {
    $script:selectedSystemIndex = ($selectedSystemIndex + $delta + $systems.Count) % $systems.Count
    $message.Text = ('Hyperspace destination: {0}' -f $systems[$selectedSystemIndex].Name)
}

function Toggle-Map {
    $script:mapVisible = -not $mapVisible
    if ($mapVisible) { $message.Text = 'Galaxy map open. N/P select, H jump, M close.' }
}

function Recalculate-Player-Stats {
    $cargoBonus = 0
    $hullBonus = 0.0
    $fuelBonus = 0.0
    foreach ($key in $ownedOutfits.Keys) {
        if (!$outfitDefs.ContainsKey($key)) { continue }
        $effects = $outfitDefs[$key].effects
        if ($effects.cargoSpace -ne $null) { $cargoBonus += [int]$effects.cargoSpace * [int]$ownedOutfits[$key] }
        if ($effects.maxHull -ne $null) { $hullBonus += [double]$effects.maxHull * [int]$ownedOutfits[$key] }
        if ($effects.maxFuel -ne $null) { $fuelBonus += [double]$effects.maxFuel * [int]$ownedOutfits[$key] }
    }
    $script:baseCargoSpace = [int]$playerShipDef.cargoSpace
    $script:cargoSpace = $baseCargoSpace + $cargoBonus
    $oldMaxHull = $script:playerMaxHull
    $script:playerMaxHull = [double]$playerShipDef.hull + $hullBonus
    if ($oldMaxHull -ne $null -and $playerMaxHull -gt $oldMaxHull) { $script:playerHull += ($playerMaxHull - $oldMaxHull) }
    $script:playerHull = [Math]::Min($script:playerHull, $script:playerMaxHull)
    $script:playerMaxFuel = 100.0 + $fuelBonus
    $player.Fuel = [Math]::Min([double]$player.Fuel, $script:playerMaxFuel)
}

function Reset-Ship {
    $player.X = 240.0; $player.Y = 180.0; $player.VX = 0.0; $player.VY = 0.0; $player.Heading = 0.0
    $script:playerHull = $playerMaxHull
    $message.Text = 'Ship reset.'
}

function Repair-Ship {
    if ($state -ne 'landed') { return }
    if (!(Has-Service 'repairs')) { $message.Text = 'No repair service at this port.'; return }
    $missing = [Math]::Max(0.0, $playerMaxHull - $playerHull)
    if ($missing -le 0) { $message.Text = 'No repairs needed.'; return }
    $cost = [int][Math]::Ceiling($missing * $repairPricePerHullPoint)
    if ($credits -lt $cost) { $message.Text = ('Repairs cost {0}; not enough credits.' -f $cost); return }
    $script:credits -= $cost
    $script:playerHull = $playerMaxHull
    $message.Text = ('Repaired hull for {0} credits.' -f $cost)
}

function Buy-Outfit($idx) {
    if ($state -ne 'landed') { return }
    if (!(Has-Service 'outfitter')) { $message.Text = 'No outfitter at this port.'; return }
    $outfits = @($stationOutfitsForSale)
    if ($idx -lt 0 -or $idx -ge $outfits.Count) { return }
    $o = $outfits[$idx]
    $price = [int]$o.price
    if ($credits -lt $price) { $message.Text = ('{0} costs {1}; not enough credits.' -f $o.name, $price); return }
    $script:credits -= $price
    $id = [string]$o.id
    if (!$ownedOutfits.ContainsKey($id)) { $ownedOutfits[$id] = 0 }
    $ownedOutfits[$id] = [int]$ownedOutfits[$id] + 1
    Recalculate-Player-Stats
    $message.Text = ('Installed {0}.' -f $o.name)
}

function Cycle-Shipyard($delta) {
    if (!(Has-Service 'shipyard')) { $message.Text = 'No shipyard at this port.'; return }
    if ($stationShipyardListings.Count -eq 0) { return }
    $script:selectedShipyardIndex = ($selectedShipyardIndex + $delta + $stationShipyardListings.Count) % $stationShipyardListings.Count
    $listing = $stationShipyardListings[$selectedShipyardIndex]
    $message.Text = ('Shipyard selected: {0}' -f $shipDefs[[string]$listing.shipId].name)
}

function Buy-Selected-Ship {
    if ($state -ne 'landed' -or $stationShipyardListings.Count -eq 0) { return }
    if (!(Has-Service 'shipyard')) { $message.Text = 'No shipyard at this port.'; return }
    $listing = $stationShipyardListings[$selectedShipyardIndex]
    $newShipId = [string]$listing.shipId
    $price = [int]$listing.price
    if ($newShipId -eq $playerShipId) { $message.Text = 'You already own this ship.'; return }
    if ($credits -lt $price) { $message.Text = ('{0} costs {1}; not enough credits.' -f $shipDefs[$newShipId].name, $price); return }
    if ($cargoUsed -gt [int]$shipDefs[$newShipId].cargoSpace) { $message.Text = 'Cannot trade ships while cargo exceeds new hold.'; return }
    $script:credits -= $price
    $script:playerShipId = $newShipId
    $script:playerShipDef = $shipDefs[$playerShipId]
    $script:shipFrames = $shipFrameSets[$playerShipId]
    $shipImage.Width = [double]$playerShipDef.width
    $shipImage.Height = [double]$playerShipDef.height
    $script:playerWeaponId = [string]$playerShipDef.weaponId
    $script:ownedOutfits = @{}
    $script:playerHull = [double]$playerShipDef.hull
    Recalculate-Player-Stats
    $player.Fuel = $playerMaxFuel
    $message.Text = ('Purchased {0}.' -f $playerShipDef.name)
}

function Cycle-Weapon($delta) {
    $weaponsForSale = @($stationWeaponsForSale)
    if ($weaponsForSale.Count -eq 0) { $message.Text = 'No weapons dealer at this port.'; return }
    if (!(Has-Service 'weapons')) { $message.Text = 'No weapons dealer at this port.'; return }
    $script:selectedWeaponIndex = ($selectedWeaponIndex + $delta + $weaponsForSale.Count) % $weaponsForSale.Count
    $w = $weaponsForSale[$selectedWeaponIndex]
    $message.Text = ('Weapon selected: {0}' -f $w.name)
}

function Buy-Selected-Weapon {
    $weaponsForSale = @($stationWeaponsForSale)
    if ($state -ne 'landed' -or $weaponsForSale.Count -eq 0) { return }
    if (!(Has-Service 'weapons')) { $message.Text = 'No weapons dealer at this port.'; return }
    $w = $weaponsForSale[$selectedWeaponIndex]
    $wid = [string]$w.id
    $price = [int]$w.price
    if ($wid -eq $playerWeaponId) { $message.Text = ('{0} already installed.' -f $w.name); return }
    if ($credits -lt $price) { $message.Text = ('{0} costs {1}; not enough credits.' -f $w.name, $price); return }
    $script:credits -= $price
    $script:playerWeaponId = $wid
    $message.Text = ('Installed weapon: {0}.' -f $w.name)
}

function Spawn-Projectile($owner, $x, $y, $heading, $weaponId) {
    if (!$weaponDefs.ContainsKey($weaponId)) { return }
    $w = $weaponDefs[$weaponId]
    $rad = ($heading - 90.0) * [Math]::PI / 180.0
    $shape = New-Object Windows.Shapes.Ellipse
    $shape.Width = [double]$w.radius * 2.0
    $shape.Height = [double]$w.radius * 2.0
    $shape.Fill = [string]$w.color
    $canvas.Children.Add($shape) | Out-Null
    $script:projectiles += @{ Owner=$owner; X=[double]$x; Y=[double]$y; VX=([Math]::Cos($rad) * [double]$w.speed); VY=([Math]::Sin($rad) * [double]$w.speed); Life=[int]$w.lifetime; Damage=[double]$w.damage; Shape=$shape; Radius=[double]$w.radius; Active=$true }
}

function Fire-Player-Weapon {
    if ($playerCooldown -gt 0) { return }
    $heading = $player.Heading
    $target = Resolve-Target
    if ($target -ne $null) {
        $dx = $target.X - $player.X; $dy = $target.Y - $player.Y
        if ([Math]::Sqrt($dx * $dx + $dy * $dy) -le $scannerRange) {
            $heading = ([Math]::Atan2($dy, $dx) * 180.0 / [Math]::PI) + 90.0
        }
    }
    Spawn-Projectile 'player' $player.X $player.Y $heading $playerWeaponId
    $script:playerCooldown = [int]$weaponDefs[$playerWeaponId].cooldownTicks
}

function Fire-Npc-Weapon($npc) {
    if ($npc.Cooldown -gt 0 -or !$npc.Alive) { return }
    Spawn-Projectile $npc.Name $npc.X $npc.Y $npc.Heading $npc.WeaponId
    $npc.Cooldown = [int]$weaponDefs[$npc.WeaponId].cooldownTicks
}

function Update-Law-Enforcement {
    if ($state -ne 'space') { return }
    $gov = Current-Government
    if ($gov -eq $null) { return }
    $sysName = (Current-System).Name
    if ($scannedSystems.ContainsKey($sysName)) { return }
    $scanRange = [double]$gov.scanRange
    $patrolFaction = [string]$gov.patrolFaction
    foreach ($npc in $npcShips) {
        if (!$npc.Alive -or $npc.System -ne $sysName) { continue }
        if ($npc.Faction -eq $patrolFaction -and (Dist $player.X $player.Y $npc.X $npc.Y) -le $scanRange) {
            $scannedSystems[$sysName] = $true
            Scan-For-Contraband $npc.Name
            return
        }
    }
}

function Update-Npc-Traffic {
    foreach ($npc in $npcShips) {
        if (!$npc.Alive) { continue }
        if ($npc.Cooldown -gt 0) { $npc.Cooldown -= 1 }
        if ($npc.System -eq (Current-System).Name -and $npc.Disposition -eq 'hostile') {
            $dx = $player.X - $npc.X; $dy = $player.Y - $npc.Y
            $distToPlayer = [Math]::Sqrt($dx * $dx + $dy * $dy)
            $npc.Heading = ([Math]::Atan2($dy, $dx) * 180.0 / [Math]::PI) + 90.0
            if ($distToPlayer -lt 520) { Fire-Npc-Weapon $npc }
        }
        $npc.X += $npc.VX
        $npc.Y += $npc.VY
        if ([Math]::Abs($npc.X) -gt 1400) { $npc.VX *= -1; $npc.Heading = (360.0 - $npc.Heading) % 360.0 }
        if ([Math]::Abs($npc.Y) -gt 1000) { $npc.VY *= -1; $npc.Heading = (180.0 - $npc.Heading + 360.0) % 360.0 }
    }
}

function Update-Projectiles {
    $remaining = @()
    foreach ($p in $projectiles) {
        if (!$p.Active) { continue }
        $p.X += $p.VX; $p.Y += $p.VY; $p.Life -= 1
        if ($p.Owner -eq 'player') {
            foreach ($npc in $npcShips) {
                if (!$npc.Alive -or $npc.System -ne (Current-System).Name) { continue }
                if ((Dist $p.X $p.Y $npc.X $npc.Y) -lt (($npc.Width + $npc.Height) / 4.0)) {
                    $npc.Hull -= $p.Damage
                    $p.Active = $false
                    $message.Text = ('Hit {0}: hull {1:n0}/{2:n0}' -f $npc.Name, [Math]::Max(0, $npc.Hull), $npc.MaxHull)
                    if ($npc.Hull -le 0) {
                        $npc.Alive = $false
                        $npc.Image.Visibility = 'Hidden'; $npc.Label.Visibility = 'Hidden'
                        $script:credits += 250
                        $message.Text = ('Destroyed {0}: +250 credits' -f $npc.Name)
                    }
                    break
                }
            }
        } else {
            if ((Dist $p.X $p.Y $player.X $player.Y) -lt 24.0) {
                $script:playerHull -= $p.Damage
                $p.Active = $false
                $message.Text = ('Incoming hit: hull {0:n0}/{1:n0}' -f [Math]::Max(0, $playerHull), $playerMaxHull)
                if ($playerHull -le 0) { Reset-Ship; $message.Text = 'Ship disabled; emergency reset.' }
            }
        }
        if ($p.Active -and $p.Life -gt 0) {
            $remaining += $p
        } else {
            $canvas.Children.Remove($p.Shape) | Out-Null
        }
    }
    $script:projectiles = $remaining
}

function Draw-Space {
    $cw = $canvas.ActualWidth; if ($cw -le 0) { $cw = 1024 }
    $ch = $canvas.ActualHeight; if ($ch -le 0) { $ch = 768 }
    $cx = $cw / 2; $cy = $ch / 2
    $target = Resolve-Target
    if ($target -eq $null -and $currentTargetName -ne $null) { $script:currentTargetName = $null }

    foreach ($i in 0..($starShapes.Count - 1)) {
        $star = $stars[$i]
        $sx = (($star.X - $player.X * 0.2 + 20000) % 3200) - 1600 + $cx
        $sy = (($star.Y - $player.Y * 0.2 + 20000) % 2400) - 1200 + $cy
        [Windows.Controls.Canvas]::SetLeft($starShapes[$i], $sx)
        [Windows.Controls.Canvas]::SetTop($starShapes[$i], $sy)
    }

    $bodies = (Current-System).Bodies
    for ($i = 0; $i -lt $bodyShapes.Count; $i++) {
        if ($i -lt $bodies.Count) {
            $b = $bodies[$i]
            $shape = $bodyShapes[$i]
            $shape.Visibility = 'Visible'
            $shape.Width = $b.R * 2; $shape.Height = $b.R * 2
            $shape.Fill = $b.Color
            $shape.Stroke = 'White'
            $sx = $cx + ($b.X - $player.X)
            $sy = $cy + ($b.Y - $player.Y)
            [Windows.Controls.Canvas]::SetLeft($shape, $sx - $b.R)
            [Windows.Controls.Canvas]::SetTop($shape, $sy - $b.R)
        } else { $bodyShapes[$i].Visibility = 'Hidden' }
    }

    foreach ($npc in $npcShips) {
        if ($npc.System -eq (Current-System).Name) {
            $frames = $shipFrameSets[$npc.ShipId]
            $normNpc = (($npc.Heading % 360) + 360) % 360
            $npcIdx = [int][Math]::Round($normNpc / 10.0) % $frames.Count
            $npc.Image.Source = $frames[$npcIdx]
            $npc.Image.Visibility = 'Visible'
            $npc.Label.Visibility = 'Visible'
            $sxNpc = $cx + ($npc.X - $player.X) - ($npc.Width / 2.0)
            $syNpc = $cy + ($npc.Y - $player.Y) - ($npc.Height / 2.0)
            [Windows.Controls.Canvas]::SetLeft($npc.Image, $sxNpc)
            [Windows.Controls.Canvas]::SetTop($npc.Image, $syNpc)
            [Windows.Controls.Canvas]::SetLeft($npc.Label, $sxNpc - 8)
            [Windows.Controls.Canvas]::SetTop($npc.Label, $syNpc + $npc.Height + 2)
            if ($target -ne $null -and $npc.Name -eq $target.Name) {
                $targetReticle.Visibility = 'Visible'
                $targetReticle.Width = $npc.Width + 16
                $targetReticle.Height = $npc.Height + 16
                [Windows.Controls.Canvas]::SetLeft($targetReticle, $sxNpc - 8)
                [Windows.Controls.Canvas]::SetTop($targetReticle, $syNpc - 8)
            }
        } else {
            $npc.Image.Visibility = 'Hidden'
            $npc.Label.Visibility = 'Hidden'
        }
    }
    if ($target -eq $null) { $targetReticle.Visibility = 'Hidden' }

    foreach ($p in $projectiles) {
        if ($p.Active) {
            [Windows.Controls.Canvas]::SetLeft($p.Shape, $cx + ($p.X - $player.X) - $p.Radius)
            [Windows.Controls.Canvas]::SetTop($p.Shape, $cy + ($p.Y - $player.Y) - $p.Radius)
        }
    }

    # EV-like discrete 36-facing sprite selection. Heading 0 points up.
    $norm = (($player.Heading % 360) + 360) % 360
    $idx = [int][Math]::Round($norm / 10.0) % $shipFrames.Count
    $shipImage.Source = $shipFrames[$idx]
    [Windows.Controls.Canvas]::SetLeft($shipImage, $cx - ([double]$playerShipDef.width / 2.0))
    [Windows.Controls.Canvas]::SetTop($shipImage, $cy - ([double]$playerShipDef.height / 2.0))
    $shipImage.Visibility = 'Visible'
}

function Update-Map-Text {
    if (!$mapVisible) { $mapPanel.Visibility = 'Hidden'; return }
    $mapPanel.Visibility = 'Visible'
    $lines = @()
    $lines += 'GALAXY MAP'
    $lines += ('Current: {0}' -f (Current-System).Name)
    $lines += ('Selected: {0}' -f $systems[$selectedSystemIndex].Name)
    $lines += ''
    for ($i = 0; $i -lt $systems.Count; $i++) {
        $s = $systems[$i]
        $mark = ' '
        if ($i -eq $currentSystemIndex) { $mark = '*' }
        if ($i -eq $selectedSystemIndex) { $mark = '>' }
        $link = ''
        if ((Current-System).Links -contains $s.Name) { $link = ' linked' }
        $lines += (' {0} {1,-10} ({2,4:n0},{3,4:n0}){4}' -f $mark, $s.Name, $s.X, $s.Y, $link)
    }
    $lines += ''
    $lines += 'N/P: select destination   H: hyperspace   M: close map'
    $mapText.Text = ($lines -join "`n")
}

function Update-Landing-Text {
    if ($state -ne 'landed') { $landingPanel.Visibility = 'Hidden'; return }
    $landingPanel.Visibility = 'Visible'
    $lines = @()
    $lines += ('LANDED: {0} / {1}' -f (Current-System).Name, $dockedAt.Name)
    $lines += $dockedAt.Market
    $lines += ''
    $lines += ('Credits: {0}   Ship: {1}   Cargo: {2}/{3} tons   Hull: {4:n0}/{5:n0}   Fuel: {6:n0}/{7:n0}' -f $credits, $playerShipDef.name, $cargoUsed, $cargoSpace, $playerHull, $playerMaxHull, $player.Fuel, $playerMaxFuel)
    $lines += ('Government: {0}   Legal: {1}   Fines Paid: {2}' -f (Current-Government-Name), $legalStatus, $totalFinesPaid)
    if ($dockedAt.inventory -ne $null) { $lines += ('Services: {0}' -f (@($dockedAt.inventory.services) -join ', ')) }
    $lines += ('Repair: {0} credits per hull point. Press 6 to repair all.' -f $repairPricePerHullPoint)
    $lines += ''
    $lines += 'Outfitter:'
    $outfitsForSale = @($stationOutfitsForSale)
    if ($outfitsForSale.Count -eq 0) { $lines += '  No outfit sales at this port.' }
    for ($oi = 0; $oi -lt $outfitsForSale.Count; $oi++) {
        $o = $outfitsForSale[$oi]
        $owned = 0
        if ($ownedOutfits.ContainsKey([string]$o.id)) { $owned = [int]$ownedOutfits[[string]$o.id] }
        $lines += ('  {0}. {1} - {2} credits (owned {3})' -f ($oi + 7), $o.name, $o.price, $owned)
        $lines += ('      {0}' -f $o.description)
    }
    $lines += ''
    $lines += 'Shipyard:'
    if ($stationShipyardListings.Count -eq 0) { $lines += '  No shipyard at this port.' }
    for ($si = 0; $si -lt $stationShipyardListings.Count; $si++) {
        $listing = $stationShipyardListings[$si]
        $def = $shipDefs[[string]$listing.shipId]
        $mark = ' '
        if ($si -eq $selectedShipyardIndex) { $mark = '>' }
        if ([string]$listing.shipId -eq $playerShipId) { $mark = '*' }
        $lines += ('  {0} {1}: {2} credits, cargo {3}, hull {4}' -f $mark, $def.name, $listing.price, $def.cargoSpace, $def.hull)
    }
    $lines += '  G: cycle shipyard selection   B: buy selected ship'
    $lines += ''
    $lines += 'Weapons:'
    if ($stationWeaponsForSale.Count -eq 0) { $lines += '  No weapons dealer at this port.' }
    for ($wi = 0; $wi -lt $stationWeaponsForSale.Count; $wi++) {
        $w = $stationWeaponsForSale[$wi]
        $mark = ' '
        if ($wi -eq $selectedWeaponIndex) { $mark = '>' }
        if ([string]$w.id -eq $playerWeaponId) { $mark = '*' }
        $lines += ('  {0} {1}: {2} credits, damage {3}, cooldown {4}' -f $mark, $w.name, $w.price, $w.damage, $w.cooldownTicks)
    }
    $lines += '  U: cycle weapon selection   O: buy selected weapon'
    $lines += ''
    $lines += 'Commodity Exchange:'
    $market = Current-Market
    if ($market -eq $null) { $lines += '  No commodity market in this system.' }
    for ($ci = 0; $ci -lt $commodityList.Count; $ci++) {
        $c = $commodityList[$ci]
        $cid = [string]$c.id
        $mark = ' '
        if ($ci -eq $selectedCommodityIndex) { $mark = '>' }
        $held = 0
        if ($commodityHold.ContainsKey($cid)) { $held = [int]$commodityHold[$cid].Tons }
        if ($market -ne $null -and $market.$cid -ne $null) {
            $illegalMark = ''
            if (@(Illegal-Cargo-Ids) -contains $cid) { $illegalMark = ' CONTRABAND' }
            $lines += ('  {0} {1}: buy {2}, sell {3}, held {4}{5}' -f $mark, $c.name, $market.$cid.buy, $market.$cid.sell, $held, $illegalMark)
        }
    }
    $lines += ('  C/V: select commodity   X: buy 1 ton   Z: sell 1 ton   Realized profit: {0}' -f $tradeProfit)
    $lines += ''
    $lines += 'Jobs Board:'
    for ($i = 0; $i -lt $jobs.Count; $i++) {
        $j = $jobs[$i]
        $lines += ('  {0}. {1} tons to {2}/{3} - {4} credits' -f ($i + 1), $j.Tons, $j.DestSystem, $j.DestBody, $j.Pay)
    }
    if ($jobs.Count -eq 0) { $lines += '  No remaining jobs here.' }
    $lines += ''
    $lines += 'Accepted Cargo:'
    if ($acceptedJobs.Count -eq 0) { $lines += '  None.' }
    foreach ($j in $acceptedJobs) { $lines += ('  {0} tons -> {1}/{2} for {3}' -f $j.Tons, $j.DestSystem, $j.DestBody, $j.Pay) }
    $lines += ''
    $lines += 'Mission Computer:'
    if ($availableMissions.Count -eq 0) { $lines += '  No new missions here.' }
    for ($i = 0; $i -lt $availableMissions.Count; $i++) {
        $m = $availableMissions[$i]
        $lines += ('  F{0}. {1}: {2} tons to {3}/{4} - {5} credits' -f ($i + 1), $m.title, $m.cargoTons, $m.destinationSystem, $m.destinationBody, $m.reward)
        $lines += ('      {0}' -f $m.description)
    }
    $lines += ''
    $lines += 'Active Missions:'
    if ($activeMissions.Count -eq 0) { $lines += '  None.' }
    foreach ($m in $activeMissions) { $lines += ('  {0}: {1} tons -> {2}/{3} for {4}' -f $m.title, $m.cargoTons, $m.destinationSystem, $m.destinationBody, $m.reward) }
    $lines += ''
    $lines += 'Press 1-5 cargo jobs, F1-F5 missions, 6 repairs, 7-9 outfits, G/B shipyard, U/O weapons, L launch.'
    $landingText.Text = ($lines -join "`n")
}

function Tick {
    if ($state -eq 'space') {
        Update-Npc-Traffic
        Update-Law-Enforcement
        if ($keys['Left'] -or $keys['A']) { $player.Heading -= 4.2 }
        if ($keys['Right'] -or $keys['D']) { $player.Heading += 4.2 }
        $rad = ($player.Heading - 90.0) * [Math]::PI / 180.0
        if ($keys['Up'] -or $keys['W']) {
            $player.VX += [Math]::Cos($rad) * 0.32
            $player.VY += [Math]::Sin($rad) * 0.32
        }
        if ($keys['Down'] -or $keys['S']) {
            $player.VX *= 0.975
            $player.VY *= 0.975
            $player.VX -= [Math]::Cos($rad) * 0.08
            $player.VY -= [Math]::Sin($rad) * 0.08
        }
        if ($keys['Space']) { Fire-Player-Weapon }
        if ($playerCooldown -gt 0) { $script:playerCooldown -= 1 }
        Update-Projectiles
        $player.X += $player.VX
        $player.Y += $player.VY
        $player.VX *= 0.997
        $player.VY *= 0.997
        $player.Fuel = Clamp ($player.Fuel + 0.005) 0 $playerMaxFuel
    }

    Draw-Space
    Update-Map-Text
    Update-Landing-Text
    $n = Nearest-Port
    $dockHint = ''
    if ($state -eq 'space' -and $n.Body -ne $null -and $n.Distance -lt ($n.Body.R + 90)) { $dockHint = (' | E dock: {0}' -f $n.Body.Name) }
    $target = Resolve-Target
    if ($target -ne $null) {
        $td = Dist $player.X $player.Y $target.X $target.Y
        $scanner.Text = ('TARGET`n{0}`n{1} / {2}`nHull {3:n0}/{4:n0}`nRange {5:n0}' -f $target.Name, $target.Faction, $target.Disposition, [Math]::Max(0, $target.Hull), $target.MaxHull, $td)
    } else {
        $visible = @(Current-Targets | Where-Object { (Dist $player.X $player.Y $_.X $_.Y) -le $scannerRange }).Count
        $scanner.Text = ('SCANNER`nNo target`nContacts: {0}`nT: nearest`nY: cycle' -f $visible)
    }
    $hud.Text = ('{0} ({1}) | Credits {2} | Cargo {3}/{4} | Hull {5:n0}/{6:n0} | Speed {7:n1} | Fuel {8:n0} | Legal {9}{10}' -f (Current-System).Name, (Current-Government-Name), $credits, $cargoUsed, $cargoSpace, [Math]::Max(0, $playerHull), $playerMaxHull, (Speed), $player.Fuel, $legalStatus, $dockHint)
}

if (!$SelfTest) { [void](Load-Game) }
$window.Add_Closing({ if (!$SelfTest) { Save-Game } })

$window.Add_KeyDown({
    param($sender, $e)
    $keys[$e.Key.ToString()] = $true
    switch ($e.Key.ToString()) {
        'Escape' { $window.Close() }
        'E' { Dock-If-Possible }
        'L' { if ($state -eq 'landed') { $script:state = 'space'; $script:dockedAt = $null; $message.Text = 'Launched.' } }
        'H' { Hyperspace }
        'M' { Toggle-Map }
        'N' { Select-System 1 }
        'P' { Select-System -1 }
        'R' { Reset-Ship }
        'T' { Target-Nearest }
        'Y' { Cycle-Target }
        'Space' { Fire-Player-Weapon }
        'D1' { Accept-Job 0 }
        'D2' { Accept-Job 1 }
        'D3' { Accept-Job 2 }
        'D4' { Accept-Job 3 }
        'D5' { Accept-Job 4 }
        'D6' { Repair-Ship }
        'D7' { Buy-Outfit 0 }
        'D8' { Buy-Outfit 1 }
        'D9' { Buy-Outfit 2 }
        'G' { Cycle-Shipyard 1 }
        'B' { Buy-Selected-Ship }
        'U' { Cycle-Weapon 1 }
        'O' { Buy-Selected-Weapon }
        'C' { Cycle-Commodity 1 }
        'V' { Cycle-Commodity -1 }
        'X' { Buy-Commodity }
        'Z' { Sell-Commodity }
        'F1' { Accept-Mission 0 }
        'F2' { Accept-Mission 1 }
        'F3' { Accept-Mission 2 }
        'F4' { Accept-Mission 3 }
        'F5' { Accept-Mission 4 }
        'F6' { Save-Game }
        'F7' { [void](Load-Game) }
    }
})
$window.Add_KeyUp({ param($sender, $e) $keys[$e.Key.ToString()] = $false })

$tickCount = 0
$timer = New-Object Windows.Threading.DispatcherTimer
$timer.Interval = [TimeSpan]::FromMilliseconds(16)
$timer.Add_Tick({
    $script:tickCount += 1
    if ($Autopilot -or $SelfTest) {
        if ($state -eq 'space' -and $tickCount -eq 20) {
            # Deterministic no-human smoke path: start at nearest port, dock, accept cargo, launch, hyperspace.
            $player.X = 0.0; $player.Y = 0.0; $player.VX = 0.0; $player.VY = 0.0
            Dock-If-Possible
        } elseif ($state -eq 'landed' -and $tickCount -eq 50) {
            Accept-Mission 0
            $script:selectedCommodityIndex = 1
            Buy-Commodity
            $script:selectedCommodityIndex = 3
            Buy-Commodity
            Buy-Outfit 0
            $script:playerHull = [Math]::Max(1.0, $playerHull - 12.0)
            Repair-Ship
            if ($activeMissions.Count -eq 0) { Accept-Job 0 }
        } elseif ($state -eq 'landed' -and $tickCount -eq 80) {
            $script:state = 'space'; $script:dockedAt = $null; $message.Text = 'Autopilot launched.'
        } elseif ($state -eq 'space' -and $tickCount -eq 90) {
            $player.X = -720.0; $player.Y = 520.0; $player.VX = 0.0; $player.VY = 0.0
        } elseif ($state -eq 'space' -and $tickCount -eq 100) {
            Toggle-Map
            $script:selectedSystemIndex = 1
            $message.Text = ('Hyperspace destination: {0}' -f $systems[$selectedSystemIndex].Name)
        } elseif ($state -eq 'space' -and $tickCount -eq 120) {
            Hyperspace
        } elseif ($state -eq 'space' -and $tickCount -eq 130) {
            $player.X = -520.0; $player.Y = -300.0; $player.VX = 0.0; $player.VY = 0.0
            Dock-If-Possible
        } elseif ($state -eq 'landed' -and $tickCount -eq 140) {
            $script:selectedCommodityIndex = 1
            Sell-Commodity
            Save-Game
        } elseif ($state -eq 'landed' -and $tickCount -eq 145) {
            Accept-Mission 0
        } elseif ($state -eq 'landed' -and $tickCount -eq 150) {
            $script:state = 'space'; $script:dockedAt = $null; $message.Text = 'Autopilot relaunched for Sirius Station.'
        } elseif ($state -eq 'space' -and $tickCount -eq 155) {
            $script:selectedSystemIndex = 2
            $message.Text = ('Hyperspace destination: {0}' -f $systems[$selectedSystemIndex].Name)
        } elseif ($state -eq 'space' -and $tickCount -eq 165) {
            Hyperspace
        } elseif ($state -eq 'space' -and $tickCount -eq 175) {
            $player.X = -80.0; $player.Y = -40.0; $player.VX = 0.0; $player.VY = 0.0
            Dock-If-Possible
        } elseif ($state -eq 'landed' -and $tickCount -eq 185) {
            Buy-Selected-Weapon
            Accept-Mission 1
            Save-Game
        } elseif ($state -eq 'landed' -and $tickCount -eq 195) {
            $script:state = 'space'; $script:dockedAt = $null; $message.Text = 'Autopilot relaunched after branch choice.'
        } elseif ($state -eq 'space' -and $tickCount -eq 205) {
            Target-Nearest
        } elseif ($state -eq 'space' -and ($tickCount -eq 215 -or $tickCount -eq 225)) {
            Fire-Player-Weapon
        }
    }
    Tick
    if ($SelfTest -and $tickCount -ge 240) {
        if ($shipFrames.Count -ne 36) { throw "SelfTest expected 36 shuttle frames, got $($shipFrames.Count)" }
        if ($shipFrameSets['light_freighter'].Count -ne 36) { throw "SelfTest expected 36 light freighter frames, got $($shipFrameSets['light_freighter'].Count)" }
        if ($weaponDefs.Count -lt 1) { throw "SelfTest expected file-backed weapons" }
        if ($npcShips.Count -lt 1) { throw "SelfTest expected file-backed NPC traffic" }
        if ($systems.Count -lt 1) { throw "SelfTest expected at least one loaded system" }
        if ($systems[0].Links.Count -lt 1) { throw "SelfTest expected hyperspace links" }
        if ($missionDefs.Count -lt 1) { throw "SelfTest expected file-backed missions" }
        if ($outfitDefs.Count -lt 1) { throw "SelfTest expected file-backed outfits" }
        if ($commodityList.Count -lt 1) { throw "SelfTest expected file-backed commodities" }
        if ($governmentDefs.Count -lt 1) { throw "SelfTest expected file-backed governments" }
        if (!$storyFlags.ContainsKey('story_intro_started')) { throw "SelfTest expected mission accept story flag" }
        if (!$storyFlags.ContainsKey('story_intro_complete')) { throw "SelfTest expected mission completion story flag" }
        if (!$storyFlags.ContainsKey('frontier_samples_delivered')) { throw "SelfTest expected completed frontier story flag" }
        if (!$storyFlags.ContainsKey('alignment_federation')) { throw "SelfTest expected accepted branch alignment flag" }
        if ($completedMissionIds.Count -lt 2) { throw "SelfTest expected completed intro and frontier missions" }
        if (!$completedMissionIds.ContainsKey('frontier_sample_hera_freeport')) { throw "SelfTest expected completed frontier mission" }
        $federationBranchActive = $false
        foreach ($m in $activeMissions) { if ($m.id -eq 'federation_report_freeport') { $federationBranchActive = $true } }
        if (!$federationBranchActive) { throw "SelfTest expected active Federation branch mission" }
        foreach ($m in $availableMissions) { if ($m.id -eq 'freeport_pact_smugglers') { throw "SelfTest expected Sirius branch to be hidden after Federation choice" } }
        if ($totalFinesPaid -le 0) { throw "SelfTest expected contraband fine" }
        if ($tradeProfit -le 0) { throw "SelfTest expected profitable commodity trade" }
        if ($cargoSpace -le [int]$playerShipDef.cargoSpace) { throw "SelfTest expected installed outfit cargo bonus" }
        if ($playerWeaponId -ne 'pulse_cannon') { throw "SelfTest expected station weapon purchase" }
        if (@($stationWeaponsForSale).Count -ne 1) { throw "SelfTest expected selected station weapons inventory" }
        if (@($stationShipyardListings).Count -eq @($shipyardListings).Count) { throw "SelfTest expected station-specific shipyard inventory" }
        if ($jobs.Count -lt 1) { throw "SelfTest expected generated cargo jobs" }
        if ($jobs[0].Distance -eq $null -or $jobs[0].Risk -eq $null) { throw "SelfTest expected route-scored cargo jobs" }
        if ([int]$jobs[0].Pay -le ([int]$jobs[0].Tons * 120)) { throw "SelfTest expected distance/risk-adjusted cargo pay" }
        if (!(Test-Path $savePath)) { throw "SelfTest expected save file" }
        $selfTestSave = Get-Content -Raw $savePath | ConvertFrom-Json
        if ($selfTestSave.schemaVersion -ne 1) { throw "SelfTest expected save schema version 1" }
        if ($selfTestSave.completedMissionIds.Count -lt 1) { throw "SelfTest expected saved completed mission" }
        if (!($selfTestSave.storyFlags -contains 'story_intro_complete')) { throw "SelfTest expected saved story flag" }
        if ($selfTestSave.playerShipId -ne $playerShipId) { throw "SelfTest expected saved player ship id" }
        $targetForLog = 'none'
        if ($currentTargetName -ne $null) { $targetForLog = $currentTargetName }
        Write-Host ('SELFTEST OK frames={0} npcFrames={1} systems={2} links={3} current={4} selected={5} npcs={6} weapons={7} missions={8} outfits={9} activeMissions={10} completedMissions={11} storyFlags={12} projectiles={13} target={14} credits={15} cargo={16} cargoSpace={17} hull={18:n0}/{19:n0} commodities={20} tradeProfit={21} governments={22} fines={23} legal={24}' -f $shipFrames.Count, $shipFrameSets['light_freighter'].Count, $systems.Count, $systems[0].Links.Count, (Current-System).Name, $systems[$selectedSystemIndex].Name, $npcShips.Count, $weaponDefs.Count, $missionDefs.Count, $outfitDefs.Count, $activeMissions.Count, $completedMissionIds.Count, $storyFlags.Count, $projectiles.Count, $targetForLog, $credits, $cargoUsed, $cargoSpace, $playerHull, $playerMaxHull, $commodityList.Count, $tradeProfit, $governmentDefs.Count, $totalFinesPaid, $legalStatus)
        $window.Close()
    } elseif ($AutoCloseSeconds -gt 0 -and $tickCount -ge ($AutoCloseSeconds * 60)) {
        $window.Close()
    }
})
$timer.Start()

$message.Text = 'Native rebuild started. Fly to a planet/station, slow down, press E to land. H jumps systems.'
[void]$window.ShowDialog()
