#!/usr/bin/env python3
"""
tests/test_snapshots.py

Unit tests for semantic snapshot creation and rollback operations (Issue #16).
"""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import importlib
snapshot_mod = importlib.import_module("snapshot")
rollback_mod = importlib.import_module("rollback")


class TestSnapshots(unittest.TestCase):

    def test_invalid_snapshot_name(self):
        """Disallowed characters in snapshot names should fail with exit code 1."""
        res = snapshot_mod.create_snapshot("invalid name with spaces!")
        self.assertEqual(res, 1)

    def test_rollback_nonexistent_snapshot(self):
        """Rolling back to a non-existent tag should fail with exit code 1."""
        res = rollback_mod.rollback_to_snapshot("nonexistent-test-snapshot-12345")
        self.assertEqual(res, 1)


if __name__ == "__main__":
    unittest.main()
