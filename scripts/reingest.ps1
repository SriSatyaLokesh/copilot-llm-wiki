# scripts/reingest.ps1 - PowerShell runner for reingest.py
[CmdletBinding()]
param (
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Source
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "reingest.py"

$pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "Python 3 is required to run reingest.py"
    exit 1
}

& $pythonCmd.Source $PythonScript $Source
exit $LASTEXITCODE
