"""
adapters/url_adapter.py

Pluggable adapter for web pages and documentation URLs.
Fulfills Issue #19:
- Fetches remote HTML via standard library urllib
- Strips scripts, styles, navigational elements
- Converts HTML semantics into clean, readable markdown in raw/
"""

import html
import re
import urllib.request
from typing import Optional

from adapters.base import BaseSourceAdapter


class UrlSourceAdapter(BaseSourceAdapter):
    """Fetches and cleans web pages into readable markdown."""

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    def can_handle(self, source: str) -> bool:
        clean = source.strip().lower()
        return clean.startswith("http://") or clean.startswith("https://")

    def fetch_html(self, url: str) -> str:
        """Fetch raw HTML with standard headers."""
        req = urllib.request.Request(
            url,
            headers={"User-Agent": self.USER_AGENT}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            return resp.read().decode(charset, errors="replace")

    def html_to_markdown(self, raw_html: str, title: Optional[str] = None) -> str:
        """Convert HTML to clean markdown using regex and standard library."""
        text = raw_html

        # Remove scripts, styles, noscript, nav, header, footer
        text = re.sub(r'<(script|style|noscript|nav|header|footer)[^>]*>.*?</\1>', '', text, flags=re.DOTALL | re.IGNORECASE)
        # Remove comments
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

        # Extract title if not provided
        if not title:
            title_match = re.search(r'<title[^>]*>(.*?)</title>', text, flags=re.DOTALL | re.IGNORECASE)
            if title_match:
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()

        # Headings
        for i in range(6, 0, -1):
            pattern = rf'<h{i}[^>]*>(.*?)</h{i}>'
            prefix = '#' * i
            text = re.sub(
                pattern,
                lambda m: f"\n\n{prefix} {re.sub(r'<[^>]+>', '', m.group(1)).strip()}\n\n",
                text,
                flags=re.DOTALL | re.IGNORECASE
            )

        # Code blocks
        text = re.sub(
            r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',
            lambda m: f"\n\n```\n{html.unescape(m.group(1)).strip()}\n```\n\n",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )
        text = re.sub(
            r'<code[^>]*>(.*?)</code>',
            lambda m: f"`{html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()}`",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Links
        text = re.sub(
            r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
            lambda m: f"[{re.sub(r'<[^>]+>', '', m.group(2)).strip()}]({m.group(1).strip()})",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Lists
        text = re.sub(
            r'<li[^>]*>(.*?)</li>',
            lambda m: f"\n- {re.sub(r'<[^>]+>', '', m.group(1)).strip()}",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        # Paragraphs and line breaks
        text = re.sub(r'<p[^>]*>', '\n\n', text, flags=re.IGNORECASE)
        text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)

        # Remove all remaining HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)

        # Unescape HTML entities
        text = html.unescape(text)

        # Normalize whitespace and blank lines
        lines = [line.strip() for line in text.splitlines()]
        cleaned_lines = []
        consecutive_blank = 0
        for line in lines:
            if not line:
                consecutive_blank += 1
                if consecutive_blank <= 1:
                    cleaned_lines.append("")
            else:
                consecutive_blank = 0
                cleaned_lines.append(line)

        result = "\n".join(cleaned_lines).strip()

        # Prepend title if present and not already at top
        if title and not result.startswith("# "):
            result = f"# {title}\n\n{result}"

        return result

    def extract(self, source: str) -> str:
        if source.startswith("http://") or source.startswith("https://"):
            raw_html = self.fetch_html(source)
        else:
            p = Path(source)
            raw_html = p.read_text(encoding="utf-8", errors="replace")
        return self.html_to_markdown(raw_html)
