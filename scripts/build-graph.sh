#!/usr/bin/env bash
# scripts/build-graph.sh - Cross-platform bash runner for build-graph.py
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_CMD="python3"

if ! command -v python3 &>/dev/null; then
    if command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo "Error: Python 3 is required to run build-graph.py" >&2
        exit 1
    fi
fi

exec "$PYTHON_CMD" "$SCRIPT_DIR/build-graph.py" "$@"
