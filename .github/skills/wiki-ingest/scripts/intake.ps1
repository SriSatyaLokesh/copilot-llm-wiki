# GitHub Copilot Wiki Intake Script (PowerShell)
# Purpose: Programmatic or batch ingestion of sources into the wiki.
# Behavior: Processes files and clears raw/ directory upon completion.

param (
    [string]$Source
)

$ErrorActionPreference = "Stop"

# Configuration
$LogFile = "wiki/log.md"
$RawDir = "raw"

function Ingest-Source {
    param([string]$Path)
    Write-Host "🚀 Ingesting: $Path" -ForegroundColor Cyan
    # Run copilot command
    copilot -p "ingest $Path" --allow-all-tools
}

function Cleanup-Raw {
    Write-Host "🧹 Cleaning up raw/ directory..." -ForegroundColor Gray
    Get-ChildItem -Path $RawDir -Filter *.md | Where-Object { $_.Name -ne ".gitkeep" } | Remove-Item -Force
}

# 1. Single source mode
if ($Source) {
    Ingest-Source -Path $Source
    # Individual cleanup is handled by the calling agent if needed.
    exit 0
}

# 2. Batch mode
Write-Host "📂 Scanning $RawDir for unprocessed sources..." -ForegroundColor Yellow

if (-not (Test-Path $RawDir)) {
    Write-Error "Directory $RawDir not found."
    exit 1
}

$sources = Get-ChildItem -Path $RawDir -Filter *.md | Where-Object { $_.Name -ne ".gitkeep" }

$processedCount = 0
$skippedCount = 0

if (-not $sources) {
    Write-Host "✔ No files to process." -ForegroundColor Green
    exit 0
}

foreach ($file in $sources) {
    $slug = $file.Name
    
    # Check if the slug already exists in the log.md file
    if (Select-String -Path $LogFile -Pattern [regex]::Escape($slug) -Quiet) {
        $skippedCount++
    }
    else {
        Ingest-Source -Path $file.FullName
        $processedCount++
    }
}

Write-Host "`n✅ Batch complete." -ForegroundColor Green
Write-Host "   Processed: $processedCount"
Write-Host "   Skipped:   $skippedCount (already in log)"

Cleanup-Raw
