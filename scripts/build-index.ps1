# scripts/build-index.ps1 - PowerShell runner for build-index.py
[CmdletBinding()]
param (
    [switch]$Check,
    [switch]$Hierarchical,
    [switch]$Flat
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "build-index.py"

$ArgsList = @()
if ($Check) { $ArgsList += "--check" }
if ($Hierarchical) { $ArgsList += "--hierarchical" }
if ($Flat) { $ArgsList += "--flat" }

$pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "Python 3 is required to run build-index.py"
    exit 1
}

& $pythonCmd.Source $PythonScript @ArgsList
exit $LASTEXITCODE
