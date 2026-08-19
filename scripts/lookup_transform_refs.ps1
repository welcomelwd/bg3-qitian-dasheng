param(
    [string]$GamePath = ""
)

$ErrorActionPreference = "Stop"

$refs = @(
    "Shout_WildShape_Combat_Cat",
    "WILDSHAPE_CAT_PLAYER",
    "Shout_WildShape_Combat_Raven",
    "WILDSHAPE_RAVEN_PLAYER",
    "Shout_Wildshape_Combat_SaberTooth_Tiger",
    "WILDSHAPE_SABERTOOTH_TIGER_PLAYER"
)

$outDir = Join-Path $PSScriptRoot "..\local-reference\bg3forge"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$common = @()
if ($GamePath -ne "") {
    $common += @("--game-path", $GamePath)
}

Write-Host "Checking BG3 Forge environment..."
& bg3forge @common doctor
if ($LASTEXITCODE -ne 0) {
    throw "bg3forge doctor failed. Install bg3forge[all]==0.2.0 and confirm the BG3 game path."
}

foreach ($ref in $refs) {
    $safeName = $ref -replace '[^A-Za-z0-9_.-]', '_'
    $outFile = Join-Path $outDir "$safeName.txt"
    Write-Host "Looking up $ref"
    & bg3forge @common lookup $ref | Tee-Object -FilePath $outFile
    if ($LASTEXITCODE -ne 0) {
        throw "Lookup failed: $ref"
    }
}

Write-Host "Reference output written to: $outDir"
Write-Host "Compare the results with docs/V02_VERIFIED_FORM_CHAIN.md before marking toolkit-verified."
