param(
    [Parameter(Mandatory = $true)]
    [string]$OfficialDlssSdkZip,
    [string]$GameRoot = "D:\steam\steamapps\common\The Blood of Dawnwalker"
)

$ErrorActionPreference = "Stop"

$target = Join-Path $GameRoot "Engine\Plugins\Runtime\Nvidia\DLSS\Binaries\ThirdParty\Win64\nvngx_dlss.dll"
$backupRoot = Join-Path $PSScriptRoot "backups"
$stageRoot = Join-Path $PSScriptRoot "stage"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backupDir = Join-Path $backupRoot "dw-dlss-sr-$stamp"
$stageDir = Join-Path $stageRoot $stamp

function Get-VersionSummary {
    param([string]$Path)
    $item = Get-Item -LiteralPath $Path
    $version = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($item.FullName)
    [pscustomobject]@{
        Path = $item.FullName
        Size = $item.Length
        ProductVersion = $version.ProductVersion
        FileVersion = $version.FileVersion
        CompanyName = $version.CompanyName
        Hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash
    }
}

if (-not (Test-Path -LiteralPath $OfficialDlssSdkZip -PathType Leaf)) {
    throw "Official NVIDIA DLSS SDK zip not found: $OfficialDlssSdkZip"
}

if (-not (Test-Path -LiteralPath $target -PathType Leaf)) {
    throw "DW DLSS DLL not found: $target"
}

New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
New-Item -ItemType Directory -Force -Path $stageDir | Out-Null

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($OfficialDlssSdkZip)
try {
    $entry = $zip.Entries |
        Where-Object { $_.FullName -replace '\\','/' -eq "DLSS_Sample_App/bin/ngx_dlss_demo/nvngx_dlss.dll" } |
        Select-Object -First 1
    if (-not $entry) {
        throw "Could not find official nvngx_dlss.dll inside the SDK zip."
    }
    $candidate = Join-Path $stageDir "nvngx_dlss.dll"
    [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $candidate, $true)
}
finally {
    $zip.Dispose()
}

$candidateInfo = Get-VersionSummary $candidate
if ($candidateInfo.CompanyName -notmatch "NVIDIA") {
    throw "Refusing to install: candidate DLL is not identified as NVIDIA. CompanyName=$($candidateInfo.CompanyName)"
}

$currentInfo = Get-VersionSummary $target
Copy-Item -LiteralPath $target -Destination (Join-Path $backupDir "nvngx_dlss.dll.original") -Force
Set-Content -LiteralPath (Join-Path $backupDir "versions.txt") -Value @(
    "Original:"
    "  Path: $($currentInfo.Path)"
    "  Version: $($currentInfo.ProductVersion)"
    "  Company: $($currentInfo.CompanyName)"
    "  SHA256: $($currentInfo.Hash)"
    ""
    "Replacement:"
    "  Path: $($candidateInfo.Path)"
    "  Version: $($candidateInfo.ProductVersion)"
    "  Company: $($candidateInfo.CompanyName)"
    "  SHA256: $($candidateInfo.Hash)"
)

Copy-Item -LiteralPath $candidate -Destination $target -Force

Write-Host "Installed official NVIDIA DLSS Super Resolution DLL."
Write-Host "Backup:"
Write-Host $backupDir
Write-Host "New DLL:"
Write-Host $target
