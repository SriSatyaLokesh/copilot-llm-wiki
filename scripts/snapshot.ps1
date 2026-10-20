# scripts/snapshot.ps1 - PowerShell runner for snapshot.py
[CmdletBinding()]
param (
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Name,

    [Parameter(Position = 1)]
    [string]$Description = "",

    [switch]$NoAutoCommit
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "snapshot.py"

$pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "Python 3 is required to run snapshot.py"
    exit 1
}

$ArgsList = @($Name)
if ($Description) { $ArgsList += $Description }
if ($NoAutoCommit) { $ArgsList += "--no-auto-commit" }

& $pythonCmd.Source $PythonScript @ArgsList
exit $LASTEXITCODE
