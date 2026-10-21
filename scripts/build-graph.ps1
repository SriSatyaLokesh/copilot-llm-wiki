# scripts/build-graph.ps1 - Cross-platform PowerShell runner for build-graph.py
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ScriptArgs
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "build-graph.py"

$pythonCmd = $null
if (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} else {
    Write-Error "Error: Python 3 is required to run build-graph.py"
    exit 1
}

& $pythonCmd $pythonScript @ScriptArgs
exit $LASTEXITCODE
