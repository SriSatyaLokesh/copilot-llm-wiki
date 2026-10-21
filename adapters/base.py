"""
adapters/base.py

Abstract Base Class for pluggable source adapters.
Fulfills Issue #19:
- Standardized adapter interface
- Normalizes incoming content into clean markdown in raw/<slug>.md
"""

import abc
import re
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "raw"


class BaseSourceAdapter(abc.ABC):
    """Abstract base class for all source format intake adapters."""

    @abc.abstractmethod
    def can_handle(self, source: str) -> bool:
        """Return True if this adapter can process the given URL or file path."""
        pass

    @abc.abstractmethod
    def extract(self, source: str) -> str:
        """Extract content from source and return clean normalized markdown."""
        pass

    def slugify(self, source: str, title: Optional[str] = None) -> str:
        """Generate a deterministic lowercase-kebab-case slug from title or source."""
        candidate = title or ""
        if not candidate:
            candidate = Path(source.split("?")[0].split("#")[0]).stem
            if not candidate or candidate in {"index", "default", "view"}:
                candidate = Path(source.rstrip("/")).name

        # Clean non-alphanumeric characters
        candidate = re.sub(r'[^a-zA-Z0-9_\-\s]', '', candidate)
        candidate = re.sub(r'[\s_]+', '-', candidate).strip("-").lower()
        return candidate or "source-document"

    def save_to_raw(
        self,
        source: str,
        raw_dir: Optional[Path] = None,
        slug: Optional[str] = None
    ) -> Path:
        """Extract markdown and save to raw/<slug>.md without modifying existing files."""
        if raw_dir is None:
            raw_dir = RAW_DIR
        raw_dir.mkdir(parents=True, exist_ok=True)

        markdown_content = self.extract(source)
        if not slug:
            # Try to infer from first heading
            m = re.search(r'^#\s+([^\n\r]+)', markdown_content, re.MULTILINE)
            first_heading = m.group(1).strip() if m else None
            slug = self.slugify(source, title=first_heading)

        out_path = raw_dir / f"{slug}.md"
        out_path.write_text(markdown_content.strip() + "\n", encoding="utf-8")
        return out_path
