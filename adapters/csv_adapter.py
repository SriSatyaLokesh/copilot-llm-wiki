"""
adapters/csv_adapter.py

Pluggable adapter for tabular CSV files.
Fulfills Issue #19:
- Converts CSV files and raw CSV strings into clean GitHub Flavored Markdown tables.
"""

import csv
import io
from pathlib import Path
from typing import List, Optional

from adapters.base import BaseSourceAdapter


class CsvSourceAdapter(BaseSourceAdapter):
    """Converts CSV tables into markdown."""

    def can_handle(self, source: str) -> bool:
        clean = source.split("?")[0].split("#")[0].strip().lower()
        return clean.endswith(".csv")

    def extract(self, source: str) -> str:
        path = Path(source)
        if path.exists():
            content = path.read_text(encoding="utf-8", errors="replace")
            title = path.stem.replace("-", " ").replace("_", " ").title()
        else:
            content = source
            title = "Tabular Data"

        reader = csv.reader(io.StringIO(content.strip()))
        rows = [row for row in reader if any(cell.strip() for cell in row)]
        if not rows:
            return f"# {title}\n\n*Empty CSV data.*"

        header = rows[0]
        data_rows = rows[1:]

        # Build Markdown Table
        lines = [f"# {title}", ""]
        header_line = "| " + " | ".join(c.strip() for c in header) + " |"
        sep_line = "| " + " | ".join("---" for _ in header) + " |"
        lines.append(header_line)
        lines.append(sep_line)

        for row in data_rows:
            # Pad row if shorter than header
            padded = row + [""] * (len(header) - len(row))
            clean_cells = [c.strip().replace("\n", " ").replace("|", "\\|") for c in padded[:len(header)]]
            lines.append("| " + " | ".join(clean_cells) + " |")

        lines.append("")
        return "\n".join(lines)
