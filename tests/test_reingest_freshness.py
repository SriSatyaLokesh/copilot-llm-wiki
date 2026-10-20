#!/usr/bin/env python3
"""
tests/test_reingest_freshness.py

Unit tests for source versioning reingest and volatility freshness calculations (Issues #13 and #15).
"""

import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import importlib
lint_wiki_mod = importlib.import_module("lint-wiki")
reingest_mod = importlib.import_module("reingest")


class TestReingestFreshness(unittest.TestCase):

    def test_freshness_calculations(self):
        today = datetime(2026, 10, 20)

        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Current source (10 days old, medium volatility = 90d cycle)
            src_current = Path(tmpdir) / "source-current.md"
            src_current.write_text(
                "# Current Source\n- **Last Verified**: 2026-10-10\n- **Volatility**: medium\n",
                encoding="utf-8"
            )
            status, _ = lint_wiki_mod.check_source_freshness(src_current, today)
            self.assertEqual(status, "current")

            # 2. Aging source (75 days old, medium volatility = 90d cycle)
            src_aging = Path(tmpdir) / "source-aging.md"
            src_aging.write_text(
                "# Aging Source\n- **Last Verified**: 2026-08-01\n- **Volatility**: medium\n",
                encoding="utf-8"
            )
            status, _ = lint_wiki_mod.check_source_freshness(src_aging, today)
            self.assertEqual(status, "aging")

            # 3. Stale source (40 days old, high volatility = 30d cycle)
            src_stale = Path(tmpdir) / "source-stale.md"
            src_stale.write_text(
                "# Stale API Source\n- **Last Verified**: 2026-09-01\n- **Volatility**: high\n",
                encoding="utf-8"
            )
            status, _ = lint_wiki_mod.check_source_freshness(src_stale, today)
            self.assertEqual(status, "stale")

    def test_reingest_missing_source(self):
        """Reingest on a non-existent source document should return exit code 1."""
        res = reingest_mod.reingest_source("non-existent-source-file-1234")
        self.assertEqual(res, 1)


if __name__ == "__main__":
    unittest.main()
