#!/usr/bin/env python3
"""
tests/test_relationships_provenance.py

Unit tests for explicit relationship taxonomy and claim provenance linting (Issues #12 and #14).
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import importlib
lint_wiki_mod = importlib.import_module("lint-wiki")


class TestRelationshipsProvenance(unittest.TestCase):

    def test_relationship_taxonomy(self):
        """Check that the 6 standardized relationship primitives are supported."""
        expected = {"depends-on", "implements", "part-of", "supersedes", "contradicts", "related-to"}
        self.assertEqual(lint_wiki_mod.VALID_RELATIONSHIP_TYPES, expected)

    def test_resolve_existing_and_broken_links(self):
        """Verify local link resolver correctly differentiates valid from broken links."""
        existing_file = REPO_ROOT / "wiki" / "entities" / "submitorder-api.md"
        self.assertTrue(lint_wiki_mod.resolve_markdown_link(existing_file, "dynamics.md"))
        self.assertTrue(lint_wiki_mod.resolve_markdown_link(existing_file, "wiki/entities/dynamics.md"))
        self.assertFalse(lint_wiki_mod.resolve_markdown_link(existing_file, "non-existent-fake-page.md"))


if __name__ == "__main__":
    unittest.main()
