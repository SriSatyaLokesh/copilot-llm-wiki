# scripts/lint.ps1 - PowerShell runner for lint-wiki.py
[CmdletBinding()]
param (
    [switch]$Strict
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "lint-wiki.py"

$pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "Python 3 is required to run lint-wiki.py"
    exit 1
}

$ArgsList = @()
if ($Strict) { $ArgsList += "--strict" }

& $pythonCmd.Source $PythonScript @ArgsList
exit $LASTEXITCODE
