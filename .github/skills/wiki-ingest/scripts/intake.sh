#!/bin/bash
# GitHub Copilot Wiki Intake Script (Bash)
# Purpose: Programmatic or batch ingestion of sources into the wiki.
# Behavior: Processes files and clears raw/ directory upon completion.

set -e

# Configuration
LOG_FILE="wiki/log.md"
RAW_DIR="raw"

ingest_source() {
    local source=$1
    echo "🚀 Ingesting: $source"
    copilot -p "ingest $source" --allow-all-tools
}

cleanup_raw() {
    echo "🧹 Cleaning up raw/ directory..."
    find "$RAW_DIR" -maxdepth 1 -name "*.md" -not -name ".gitkeep" -delete
}

# 1. Single source mode
if [ ! -z "$1" ]; then
    ingest_source "$1"
    # Individual cleanup is handled by the calling agent if needed, 
    # but for script safety we only bulk-clean in batch mode.
    exit 0
fi

# 2. Batch mode
echo "📂 Scanning $RAW_DIR for unprocessed sources..."

# Find all markdown files in raw/ excluding .gitkeep
sources=$(find "$RAW_DIR" -maxdepth 1 -name "*.md" -not -name ".gitkeep")

processed_count=0
skipped_count=0

if [ -z "$sources" ]; then
    echo "✔ No files to process."
    exit 0
fi

for source in $sources; do
    # Extract filename or slug to check in log.md
    slug=$(basename "$source")
    
    # Check if the slug already exists in the log.md file
    if grep -q "$slug" "$LOG_FILE"; then
        skipped_count=$((skipped_count + 1))
    else
        ingest_source "$source"
        processed_count=$((processed_count + 1))
    fi
done

echo "✅ Batch complete."
echo "   Processed: $processed_count"
echo "   Skipped:   $skipped_count (already in log)"

cleanup_raw
