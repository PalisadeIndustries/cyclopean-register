<#
.SYNOPSIS
  Links this checkout into a Company of Heroes install for development.

.DESCRIPTION
  Builds the .ucs strings, creates a junction <GamePath>\City17 -> <repo>\mod\City17
  (no admin rights needed, and edits in the repo show up in-game straight away), and
  copies City17.module next to RelicCOH.exe. Safe to re-run after changing the module.

.EXAMPLE
  .\tools\install-dev.ps1 -GamePath "C:\Program Files (x86)\Steam\steamapps\common\Company of Heroes Relaunch"
#>
param(
  [Parameter(Mandatory)][string]$GamePath
)
$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
if (-not (Test-Path (Join-Path $GamePath 'RelicCOH.exe'))) {
  throw "RelicCOH.exe not found in '$GamePath'. Pass the folder that contains it."
}

$py = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { 'python' }
& $py (Join-Path $PSScriptRoot 'modtool.py') build-ucs
if ($LASTEXITCODE) { throw 'Building strings failed; run "py tools\modtool.py check".' }

$link = Join-Path $GamePath 'City17'
$target = Join-Path $repo 'mod\City17'
if (Test-Path $link) {
  $item = Get-Item $link -Force
  if (-not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
    throw "'$link' is a real folder, not a link. Move it somewhere safe and re-run."
  }
  Write-Host "Link already exists: $link"
} else {
  New-Item -ItemType Junction -Path $link -Target $target | Out-Null
  Write-Host "Linked $link -> $target"
}

Copy-Item (Join-Path $repo 'mod\City17.module') $GamePath -Force
Write-Host "Copied City17.module to $GamePath"
Write-Host ''
Write-Host 'Launch with:  RelicCOH.exe -dev -mod City17'
