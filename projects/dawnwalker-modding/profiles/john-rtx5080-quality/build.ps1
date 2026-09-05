param(
    [string]$RepakPath = 'C:\Users\johnf\Documents\Codex\Tools\repak-v0.2.3\repak.exe',
    [string]$UnrealPakPath = 'D:\Vortex Mods\palworld\UnrealPakTool\UnrealPakTool\UnrealPak.exe'
)

$ErrorActionPreference = 'Stop'
$profileRoot = $PSScriptRoot
$pakRoot = Join-Path $profileRoot 'pak-root'
$dist = Join-Path $profileRoot 'dist'
$outputPak = Join-Path $dist '~JohnRTX5080Quality_P.pak'

if (-not (Test-Path -LiteralPath $RepakPath -PathType Leaf)) {
    throw "repak was not found at: $RepakPath"
}

New-Item -ItemType Directory -Force -Path $dist | Out-Null

$sourceFiles = Get-ChildItem -LiteralPath $pakRoot -Recurse -File
if (-not $sourceFiles) {
    throw "No package source files were found under: $pakRoot"
}

Remove-Item -LiteralPath $outputPak -Force -ErrorAction SilentlyContinue

& $RepakPath pack --version V3 --mount-point '../../../' --verbose $pakRoot $outputPak
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $outputPak -PathType Leaf)) {
    throw 'repak did not create the package successfully.'
}

& $RepakPath info $outputPak
if ($LASTEXITCODE -ne 0) {
    throw 'The generated package metadata could not be read.'
}

& $RepakPath list $outputPak
if ($LASTEXITCODE -ne 0) {
    throw 'The generated package could not be listed after creation.'
}

if (Test-Path -LiteralPath $UnrealPakPath -PathType Leaf) {
    & $UnrealPakPath $outputPak -Test
    if ($LASTEXITCODE -ne 0) {
        throw 'The generated package failed the independent UnrealPak test.'
    }
}

Write-Output "Built and verified: $outputPak"
