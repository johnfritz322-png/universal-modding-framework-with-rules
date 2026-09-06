param(
    [string]$GameRoot = "D:\steam\steamapps\common\The Blood of Dawnwalker"
)

$ErrorActionPreference = "Stop"

$win64 = Join-Path $GameRoot "Dawnwalker\Binaries\Win64"
$nvidiaRoot = Join-Path $GameRoot "Engine\Plugins\Runtime\Nvidia"
$reportDir = Join-Path $PSScriptRoot "reports"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$report = Join-Path $reportDir "dw-dlss-audit-$stamp.txt"

New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

function Get-FileRecord {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $null
    }
    $item = Get-Item -LiteralPath $Path
    $version = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($item.FullName)
    [pscustomobject]@{
        Name = $item.Name
        Path = $item.FullName
        Size = $item.Length
        ProductVersion = $version.ProductVersion
        FileVersion = $version.FileVersion
        CompanyName = $version.CompanyName
        Hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash
    }
}

$files = @()
foreach ($root in @($win64, $nvidiaRoot)) {
    if (Test-Path -LiteralPath $root -PathType Container) {
        $files += Get-ChildItem -Path $root -Recurse -File -Force -ErrorAction SilentlyContinue |
            Where-Object {
                $_.Name -match '^(nvngx_|sl\.|dxgi\.dll|dwmapi\.dll|UE4SS\.dll|ReShade.*\.dll|amd_fidelityfx_|OptiScaler|renodx-|dlss5-)'
            } |
            ForEach-Object { Get-FileRecord $_.FullName }
    }
}

$unsafeNames = @(
    "renodx-dlss5.addon64",
    "nvngx_dlssnr.dll",
    "dlss5-feed.addon64",
    "dlss5-feed.addon32",
    "dlss5-bridge.addon64",
    "dlss5-dx11-bridge.addon64"
)

$unsafeHits = $files | Where-Object { $unsafeNames -contains $_.Name }

$lines = @()
$lines += "Dawnwalker DLSS Safety Audit"
$lines += "Checked: $(Get-Date -Format s)"
$lines += "GameRoot: $GameRoot"
$lines += ""
$lines += "Unsafe/community DLSS 5 files found:"
if ($unsafeHits) {
    foreach ($hit in $unsafeHits) {
        $lines += "- $($hit.Path)"
    }
} else {
    $lines += "- None"
}
$lines += ""
$lines += "Tracked runtime files:"
foreach ($file in ($files | Sort-Object Path)) {
    $lines += ""
    $lines += $file.Name
    $lines += "  Path: $($file.Path)"
    $lines += "  Version: $($file.ProductVersion)"
    $lines += "  Company: $($file.CompanyName)"
    $lines += "  SHA256: $($file.Hash)"
}

Set-Content -LiteralPath $report -Value $lines

Write-Host "Audit written to:"
Write-Host $report
if ($unsafeHits) {
    Write-Warning "Unsafe/community DLSS 5 files were found. Review the audit before launching DW."
} else {
    Write-Host "No unsafe/community DLSS 5 files found."
}
