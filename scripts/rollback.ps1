# scripts/rollback.ps1 - PowerShell runner for rollback.py
[CmdletBinding()]
param (
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Name,

    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "rollback.py"

$pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "Python 3 is required to run rollback.py"
    exit 1
}

$ArgsList = @($Name)
if ($Force) { $ArgsList += "--force" }

& $pythonCmd.Source $PythonScript @ArgsList
exit $LASTEXITCODE
