"""
adapters/github_issues_adapter.py

Pluggable adapter for GitHub Issues and Pull Requests.
Fulfills Issue #19:
- Parses GitHub issue URLs or exported JSON files into clean markdown in raw/
"""

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from adapters.base import BaseSourceAdapter


class GitHubIssuesAdapter(BaseSourceAdapter):
    """Converts GitHub Issue/PR URLs and JSON exports into markdown."""

    GITHUB_ISSUE_URL_RE = re.compile(
        r'https?://github\.com/([^/]+)/([^/]+)/(issues|pull)/(\d+)'
    )

    def can_handle(self, source: str) -> bool:
        if self.GITHUB_ISSUE_URL_RE.match(source.strip()):
            return True
        clean = source.split("?")[0].split("#")[0].strip().lower()
        if clean.endswith(".json"):
            # Check if JSON looks like an issue export
            p = Path(source)
            if p.exists():
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                    if isinstance(data, dict) and ("number" in data or "issue" in data):
                        return True
                except Exception:
                    pass
        return False

    def _fetch_via_gh_cli(self, url: str) -> Optional[Dict[str, Any]]:
        """Attempt to fetch issue details using gh CLI."""
        try:
            m = self.GITHUB_ISSUE_URL_RE.match(url.strip())
            if not m:
                return None
            owner, repo, kind, number = m.groups()
            subcmd = "issue" if kind == "issues" else "pr"
            cmd = [
                "gh", subcmd, "view", url.strip(),
                "--json", "number,title,body,state,labels,comments,url,author"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(res.stdout)
        except Exception:
            return None

    def extract(self, source: str) -> str:
        data: Optional[Dict[str, Any]] = None

        p = Path(source)
        if p.exists() and p.suffix.lower() == ".json":
            data = json.loads(p.read_text(encoding="utf-8"))
        elif self.GITHUB_ISSUE_URL_RE.match(source.strip()):
            data = self._fetch_via_gh_cli(source.strip())
            if not data:
                # Fallback to stub markdown with URL reference
                m = self.GITHUB_ISSUE_URL_RE.match(source.strip())
                owner, repo, kind, number = m.groups()
                return f"# GitHub {kind.capitalize()} #{number} ({owner}/{repo})\n\nSource URL: {source}\n"

        if not data:
            raise ValueError(f"Could not load issue data from {source}")

        number = data.get("number", "Unknown")
        title = data.get("title", "Untitled Issue")
        body = data.get("body", "") or "*No description provided.*"
        state = data.get("state", "open")
        labels = [l.get("name", "") for l in data.get("labels", []) if isinstance(l, dict)]
        comments = data.get("comments", [])

        lines = [
            f"# Issue #{number}: {title}",
            "",
            f"- **State**: {state}",
        ]
        if labels:
            lines.append(f"- **Labels**: {', '.join(labels)}")
        if data.get("url") or data.get("html_url"):
            lines.append(f"- **Source URL**: {data.get('url') or data.get('html_url')}")

        lines.extend(["", "## Description", "", body.strip(), ""])

        if comments:
            lines.extend(["## Comments", ""])
            for idx, c in enumerate(comments, 1):
                user = c.get("user", {}).get("login") or c.get("author", {}).get("login") or "Anonymous"
                created = c.get("created_at") or c.get("createdAt") or ""
                comment_body = c.get("body", "").strip()
                lines.append(f"### Comment by @{user} ({created})")
                lines.append("")
                lines.append(comment_body)
                lines.append("")

        return "\n".join(lines)
