"""
adapters/pdf_adapter.py

Pluggable adapter for PDF documents.
Fulfills Issue #19:
- Extracts text from PDF files into normalized markdown in raw/
- Gracefully detects pypdf/pdfminer or falls back to basic stream extraction
"""

import re
from pathlib import Path
from typing import Optional

from adapters.base import BaseSourceAdapter


class PdfSourceAdapter(BaseSourceAdapter):
    """Extracts text content from PDF files."""

    def can_handle(self, source: str) -> bool:
        clean = source.split("?")[0].split("#")[0].strip().lower()
        return clean.endswith(".pdf")

    def _extract_with_pypdf(self, path: Path) -> Optional[str]:
        """Try extracting text using pypdf if available."""
        try:
            import pypdf
            reader = pypdf.PdfReader(str(path))
            pages_text = []
            for idx, page in enumerate(reader.pages, 1):
                t = page.extract_text()
                if t and t.strip():
                    pages_text.append(f"## Page {idx}\n\n{t.strip()}")
            if pages_text:
                return "\n\n".join(pages_text)
        except Exception:
            pass
        return None

    def _fallback_stream_extract(self, path: Path) -> str:
        """Basic text extraction from uncompressed PDF streams."""
        try:
            raw_bytes = path.read_bytes()
            # Match text between parentheses in Tj and TJ operators
            text_matches = re.findall(rb'\(([^\)]+)\)\s*(?:Tj|TJ)', raw_bytes)
            if text_matches:
                decoded_words = [m.decode("latin1", errors="replace").strip() for m in text_matches if m.strip()]
                clean_text = " ".join(decoded_words)
                if len(clean_text) > 50:
                    return clean_text
        except Exception:
            pass

        return f"*PDF document '{path.name}'. Text could not be extracted directly with standard library. Install 'pypdf' (`pip install pypdf`) for complete multi-page extraction.*"

    def extract(self, source: str) -> str:
        path = Path(source)
        title = path.stem.replace("-", " ").replace("_", " ").title()

        extracted_body = self._extract_with_pypdf(path)
        if not extracted_body:
            extracted_body = self._fallback_stream_extract(path)

        return f"# {title}\n\n{extracted_body}\n"
