#!/usr/bin/env python3
"""
tests/test_source_adapters.py

Unit tests for Pluggable Source Adapter Architecture (Issue #19).
"""

import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from adapters.base import BaseSourceAdapter
from adapters.csv_adapter import CsvSourceAdapter
from adapters.github_issues_adapter import GitHubIssuesAdapter
from adapters.url_adapter import UrlSourceAdapter
from adapters.pdf_adapter import PdfSourceAdapter
from adapters.registry import get_adapter_for, register_adapter


class TestSourceAdapters(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.raw_dir = Path(self.test_dir) / "raw"
        self.raw_dir.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_csv_adapter(self):
        """Verify CSV adapter converts tabular rows into GitHub flavored markdown tables."""
        csv_file = Path(self.test_dir) / "pricing.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Tier", "Price", "Features"])
            writer.writerow(["Free", "$0", "Completions"])
            writer.writerow(["Pro", "$10", "Chat and CLI"])

        adapter = CsvSourceAdapter()
        self.assertTrue(adapter.can_handle(str(csv_file)))

        md = adapter.extract(str(csv_file))
        self.assertIn("# Pricing", md)
        self.assertIn("| Tier | Price | Features |", md)
        self.assertIn("| --- | --- | --- |", md)
        self.assertIn("| Free | $0 | Completions |", md)
        self.assertIn("| Pro | $10 | Chat and CLI |", md)

    def test_github_issues_adapter_from_dict(self):
        """Verify GitHub Issues adapter formats issue JSON into normalized markdown."""
        issue_data = {
            "number": 42,
            "title": "Support MCP Protocol in Agent Mode",
            "body": "We should support Model Context Protocol servers.",
            "html_url": "https://github.com/org/repo/issues/42",
            "state": "open",
            "labels": [{"name": "enhancement"}, {"name": "protocol"}],
            "comments": [
                {
                    "user": {"login": "octocat"},
                    "created_at": "2026-10-21T10:00:00Z",
                    "body": "Agreed, FastMCP provides great ergonomics."
                }
            ]
        }
        json_file = Path(self.test_dir) / "issue-42.json"
        json_file.write_text(json.dumps(issue_data), encoding="utf-8")

        adapter = GitHubIssuesAdapter()
        self.assertTrue(adapter.can_handle(str(json_file)))

        md = adapter.extract(str(json_file))
        self.assertIn("# Issue #42: Support MCP Protocol in Agent Mode", md)
        self.assertIn("**State**: open", md)
        self.assertIn("**Labels**: enhancement, protocol", md)
        self.assertIn("We should support Model Context Protocol servers.", md)
        self.assertIn("### Comment by @octocat", md)
        self.assertIn("FastMCP provides great ergonomics", md)

    def test_url_adapter_html_cleaning(self):
        """Verify URL adapter cleans HTML boilerplate into structured markdown."""
        html = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Article - Copilot</title></head>
        <body>
            <script>alert('noise');</script>
            <style>body { color: red; }</style>
            <h1>What is Copilot?</h1>
            <p>GitHub Copilot is an AI pair programmer.</p>
            <h2>Features</h2>
            <ul>
                <li>Code completions</li>
                <li>Chat assistance</li>
            </ul>
        </body>
        </html>
        """
        adapter = UrlSourceAdapter()
        md = adapter.html_to_markdown(html, title="What is Copilot?")
        self.assertIn("# What is Copilot?", md)
        self.assertIn("GitHub Copilot is an AI pair programmer.", md)
        self.assertIn("## Features", md)
        self.assertIn("- Code completions", md)
        self.assertNotIn("alert('noise')", md)
        self.assertNotIn("color: red", md)

    def test_adapter_registry_routing(self):
        """Verify registry routes inputs to correct adapters based on scheme/extension."""
        self.assertIsInstance(get_adapter_for("https://docs.github.com/copilot"), UrlSourceAdapter)
        self.assertIsInstance(get_adapter_for("http://example.com/spec.html"), UrlSourceAdapter)
        self.assertIsInstance(get_adapter_for("data/metrics.csv"), CsvSourceAdapter)
        self.assertIsInstance(get_adapter_for("docs/paper.pdf"), PdfSourceAdapter)
        self.assertIsInstance(get_adapter_for("https://github.com/owner/repo/issues/123"), GitHubIssuesAdapter)


if __name__ == "__main__":
    unittest.main()
