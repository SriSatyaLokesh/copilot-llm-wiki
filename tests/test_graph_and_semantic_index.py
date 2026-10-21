#!/usr/bin/env python3
"""
tests/test_graph_and_semantic_index.py

Unit tests for Knowledge Graph manifest (Issue #20) and Semantic Index (Issue #23).
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

# Import build-graph and build-semantic-index via importlib
import importlib
build_graph_mod = importlib.import_module("build-graph")
build_semantic_index_mod = importlib.import_module("build-semantic-index")


class TestGraphAndSemanticIndex(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.wiki_dir = Path(self.test_dir) / "wiki"
        self.wiki_dir.mkdir(parents=True)
        (self.wiki_dir / "entities").mkdir()
        (self.wiki_dir / "concepts").mkdir()

        # Create a sample entity
        (self.wiki_dir / "entities" / "auth-service.md").write_text(
            """# Auth Service

Authentication and authorization microservice handling JWT tokens.

## Relationships
- **depends-on**: [Token Vault](wiki/concepts/token-vault.md)

## Key Facts
- Issues tokens with 1h TTL.

## See Also
- [Token Vault](wiki/concepts/token-vault.md)
""",
            encoding="utf-8"
        )

        # Create a sample concept
        (self.wiki_dir / "concepts" / "token-vault.md").write_text(
            """# Token Vault

Secure storage abstraction for public-key encryption keys.

## Relationships
- **part-of**: [Auth Service](wiki/entities/auth-service.md)

## Key Facts
- Rotates asymmetric keys every 30 days.

## See Also
- [Auth Service](wiki/entities/auth-service.md)
""",
            encoding="utf-8"
        )

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_build_graph_structure(self):
        """Test that build_graph extracts nodes and edges adhering to Issue #20 schema."""
        graph_data = build_graph_mod.generate_graph(wiki_dir=self.wiki_dir)

        self.assertIn("nodes", graph_data)
        self.assertIn("edges", graph_data)
        self.assertIn("metadata", graph_data)

        nodes = {n["id"]: n for n in graph_data["nodes"]}
        self.assertIn("auth-service", nodes)
        self.assertIn("token-vault", nodes)

        auth_node = nodes["auth-service"]
        self.assertEqual(auth_node["title"], "Auth Service")
        self.assertEqual(auth_node["silo"], "entities")
        self.assertEqual(auth_node["type"], "entity")

        edges = graph_data["edges"]
        self.assertTrue(any(e["from"] == "auth-service" and e["to"] == "token-vault" and e["type"] == "depends-on" for e in edges))
        self.assertTrue(any(e["from"] == "token-vault" and e["to"] == "auth-service" and e["type"] == "part-of" for e in edges))

    def test_graph_orphan_detection(self):
        """Test graph analysis detects isolated orphan nodes without edges."""
        # Create an isolated orphan entity
        (self.wiki_dir / "entities" / "orphan-entity.md").write_text(
            """# Orphan Entity

An isolated entity with no relationships or outgoing links.
""",
            encoding="utf-8"
        )

        graph_data = build_graph_mod.generate_graph(wiki_dir=self.wiki_dir)
        orphans = build_graph_mod.find_isolated_nodes(graph_data)
        self.assertIn("orphan-entity", orphans)
        self.assertNotIn("auth-service", orphans)

    def test_build_semantic_index_structure(self):
        """Test that build_semantic_index extracts dense keywords, summaries, and outgoing links (Issue #23)."""
        semantic_index = build_semantic_index_mod.generate_semantic_index(wiki_dir=self.wiki_dir)

        self.assertIn("entries", semantic_index)
        self.assertIn("metadata", semantic_index)
        self.assertEqual(semantic_index["metadata"]["total_entries"], 2)

        entry_map = {e["id"]: e for e in semantic_index["entries"]}
        self.assertIn("auth-service", entry_map)
        auth_entry = entry_map["auth-service"]

        self.assertEqual(auth_entry["title"], "Auth Service")
        self.assertEqual(auth_entry["silo"], "entities")
        self.assertIn("tokens", auth_entry["keywords"])
        self.assertIn("token-vault", auth_entry["outbound_links"])

    def test_semantic_index_search(self):
        """Test querying the semantic index by keyword."""
        semantic_index = build_semantic_index_mod.generate_semantic_index(wiki_dir=self.wiki_dir)
        matches = build_semantic_index_mod.query_semantic_index(semantic_index, "encryption")
        self.assertTrue(any(m["id"] == "token-vault" for m in matches))


if __name__ == "__main__":
    unittest.main()
