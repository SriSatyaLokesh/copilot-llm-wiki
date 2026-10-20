#!/usr/bin/env python3
"""
tests/test_build_index.py

Unit tests for deterministic wiki index compilation (Issue #10 and Issue #17).
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add repo root to python path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import importlib
build_index = importlib.import_module("build-index")


class TestBuildIndex(unittest.TestCase):

    def test_clean_markdown_inline(self):
        raw = "This is a **bold** and *italic* text with [a link](https://example.com) and `code`."
        cleaned = build_index.clean_markdown_inline(raw)
        self.assertEqual(cleaned, "This is a bold and italic text with a link and code.")

    def test_clean_wikilink_inline(self):
        raw = "Refers to [[target-note|Display Name]] and [[another-note]]."
        cleaned = build_index.clean_markdown_inline(raw)
        self.assertEqual(cleaned, "Refers to Display Name and another-note.")

    def test_parse_page_with_overview(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_file = Path(tmpdir) / "test-entity.md"
            sample_file.write_text(
                "# Test Entity\n\n## Overview\n\nTest Entity is a high-performance service for order processing.\n\n## Key Facts\n- Fact 1\n",
                encoding="utf-8"
            )
            title, desc = build_index.parse_page(sample_file)
            self.assertEqual(title, "Test Entity")
            self.assertEqual(desc, "Test Entity is a high-performance service for order processing.")

    def test_parse_page_with_definition(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_file = Path(tmpdir) / "test-concept.md"
            sample_file.write_text(
                "# Test Concept\n\n## Definition\n\nTest Concept defines the state transition model for quotes.\n\n## How It Works\n",
                encoding="utf-8"
            )
            title, desc = build_index.parse_page(sample_file)
            self.assertEqual(title, "Test Concept")
            self.assertEqual(desc, "Test Concept defines the state transition model for quotes.")

    def test_parse_page_fallback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_file = Path(tmpdir) / "no-header.md"
            sample_file.write_text("Just some text without H1.", encoding="utf-8")
            title, desc = build_index.parse_page(sample_file)
            self.assertEqual(title, "No Header")

    def test_live_wiki_check_passes(self):
        """Verify that running build_all_indexes(check_only=True) on the actual repo passes."""
        exit_code = build_index.build_all_indexes(check_only=True)
        self.assertEqual(exit_code, 0, "Index files in wiki/ should be completely synchronized and pass --check")


if __name__ == "__main__":
    unittest.main()
