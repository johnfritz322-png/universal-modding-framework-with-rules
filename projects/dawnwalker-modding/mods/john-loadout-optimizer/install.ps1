param(
    [string]$GameRoot = "D:\steam\steamapps\common\The Blood of Dawnwalker"
)

$ErrorActionPreference = "Stop"

$win64 = Join-Path $GameRoot "Dawnwalker\Binaries\Win64"
$modsRoot = Join-Path $win64 "Mods"
$target = Join-Path $modsRoot "JohnLoadoutOptimizer"
$source = Join-Path $PSScriptRoot "ue4ss\Mods\JohnLoadoutOptimizer"

if (-not (Test-Path -LiteralPath $win64 -PathType Container)) {
    throw "DW Win64 folder not found: $win64"
}

if (-not (Test-Path -LiteralPath (Join-Path $win64 "UE4SS.dll") -PathType Leaf)) {
    throw "UE4SS is not installed yet. Expected file: $(Join-Path $win64 "UE4SS.dll")"
}

if (-not (Test-Path -LiteralPath $source -PathType Container)) {
    throw "Source mod folder not found: $source"
}

New-Item -ItemType Directory -Force -Path $modsRoot | Out-Null
Copy-Item -LiteralPath $source -Destination $modsRoot -Recurse -Force

$modsTxt = Join-Path $modsRoot "mods.txt"
if (Test-Path -LiteralPath $modsTxt -PathType Leaf) {
    $lines = Get-Content -LiteralPath $modsTxt
    if ($lines -notmatch '^JohnLoadoutOptimizer\s*:') {
        Add-Content -LiteralPath $modsTxt -Value "JohnLoadoutOptimizer : 1"
    } else {
        $lines = $lines | ForEach-Object {
            if ($_ -match '^JohnLoadoutOptimizer\s*:') { "JohnLoadoutOptimizer : 1" } else { $_ }
        }
        Set-Content -LiteralPath $modsTxt -Value $lines
    }
}

Write-Host "Installed JohnLoadoutOptimizer to:"
Write-Host $target
Write-Host "Hotkeys: Numpad 1 = attack, Numpad 2 = defense"
