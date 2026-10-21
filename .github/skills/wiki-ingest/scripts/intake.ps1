# GitHub Copilot Wiki Intake Script (PowerShell)
# Purpose: Programmatic or batch ingestion of sources into the wiki.
# Security Hardened: Validates paths against shell injection, removes --allow-all-tools,
# and enforces raw/ source immutability for delta reingest and claim provenance (Issues #6, #8).

param (
    [string]$Source
)

$ErrorActionPreference = "Stop"

# Configuration
$LogFile = "wiki/log.md"
$RawDir = "raw"

function Ingest-Source {
    param([string]$Path)
    # Security: Validate filename against command injection metacharacters
    if ($Path -notmatch '^[a-zA-Z0-9_\-\.\/\\:]+\.md$') {
        Write-Error "Security Error: Path '$Path' contains disallowed characters."
        return
    }

    Write-Host "🚀 Ingesting: $Path" -ForegroundColor Cyan
    # Principle of least privilege: do NOT pass unrestricted --allow-all-tools
    & copilot -p ("ingest " + $Path)
}

function Cleanup-Raw {
    # Invariant: raw/ documents are immutable source references required for delta reingest.
    Write-Host "🛡️  Preserving raw/ sources for delta provenance." -ForegroundColor Gray
}

# 1. Single source mode
if ($Source) {
    Ingest-Source -Path $Source
    exit 0
}

# 2. Batch mode
Write-Host "📂 Scanning $RawDir for unprocessed sources..." -ForegroundColor Yellow

if (-not (Test-Path $RawDir)) {
    Write-Error "Directory $RawDir not found."
    exit 1
}

$canonicalRaw = (Resolve-Path -Path $RawDir).Path

# Safe enumeration rejecting symlinks
$sources = Get-ChildItem -Path $RawDir -Filter *.md | Where-Object { 
    $_.Name -ne ".gitkeep" -and $_.LinkType -eq $null 
}

$processedCount = 0
$skippedCount = 0

if (-not $sources) {
    Write-Host "✔ No files to process." -ForegroundColor Green
    exit 0
}

foreach ($file in $sources) {
    $resolvedFile = (Resolve-Path -Path $file.FullName).Path
    if (-not $resolvedFile.StartsWith($canonicalRaw)) {
        Write-Warning "Skipping out-of-bounds candidate: $resolvedFile"
        continue
    }

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
