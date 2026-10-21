# scripts/sync-adapters.ps1 - Cross-platform PowerShell runner for sync-adapters.py
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ScriptArgs
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "sync-adapters.py"

$pythonCmd = $null
if (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} else {
    Write-Error "Error: Python 3 is required to run sync-adapters.py"
    exit 1
}

& $pythonCmd $pythonScript @ScriptArgs
exit $LASTEXITCODE
