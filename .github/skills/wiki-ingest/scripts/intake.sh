#!/bin/bash
# GitHub Copilot Wiki Intake Script (Bash)
# Purpose: Programmatic or batch ingestion of sources into the wiki.
# Security Hardened: Validates paths against shell injection, removes --allow-all-tools,
# and enforces raw/ source immutability for delta reingest and claim provenance (Issues #6, #8).

set -e

# Configuration
LOG_FILE="wiki/log.md"
RAW_DIR="raw"

ingest_source() {
    local source=$1
    if [[ ! "$source" =~ ^[a-zA-Z0-9_./-]+\.md$ ]]; then
        echo "Security Error: Source '$source' contains invalid characters." >&2
        return 1
    fi
    echo "🚀 Ingesting: $source"
    # Principle of least privilege: do NOT pass unrestricted --allow-all-tools
    copilot -p "ingest $source"
}

cleanup_raw() {
    # Invariant: raw/ documents are immutable source references required for delta reingest.
    echo "🛡️  Preserving raw/ sources for delta provenance."
}

# 1. Single source mode
if [ ! -z "$1" ]; then
    ingest_source "$1"
    exit 0
fi

# 2. Batch mode
echo "📂 Scanning $RAW_DIR for unprocessed sources..."

# Find all regular markdown files in raw/ excluding .gitkeep (rejecting symlinks)
sources=$(find "$RAW_DIR" -maxdepth 1 -type f -name "*.md" -not -name ".gitkeep")

processed_count=0
skipped_count=0

if [ -z "$sources" ]; then
    echo "✔ No files to process."
    exit 0
fi

canonical_raw=$(realpath "$RAW_DIR" 2>/dev/null || pwd -P)

for source in $sources; do
    resolved_file=$(realpath "$source" 2>/dev/null || echo "$source")
    case "$resolved_file" in
        "$canonical_raw"/*) ;;
        *)
            echo "Skipping out-of-bounds candidate: $resolved_file" >&2
            continue
            ;;
    esac

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
