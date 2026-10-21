#!/usr/bin/env python3
"""
tests/test_instruction_adapters.py

Unit tests for Multi-LLM Instruction Adapters and Drift Detection (Issue #22).
"""

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import importlib
sync_adapters_mod = importlib.import_module("sync-adapters")


class TestInstructionAdapters(unittest.TestCase):

    def test_adapter_files_exist(self):
        """Verify that dedicated adapter files exist for all major LLM environments."""
        claude_path = REPO_ROOT / "CLAUDE.md"
        gemini_path = REPO_ROOT / ".gemini" / "GEMINI.md"
        cursorrules_path = REPO_ROOT / ".cursorrules"
        cursor_mdc_path = REPO_ROOT / ".cursor" / "rules" / "wiki.mdc"

        self.assertTrue(claude_path.exists(), "CLAUDE.md must exist")
        self.assertTrue(gemini_path.exists(), ".gemini/GEMINI.md must exist")
        self.assertTrue(cursorrules_path.exists(), ".cursorrules must exist")
        self.assertTrue(cursor_mdc_path.exists(), ".cursor/rules/wiki.mdc must exist")

    def test_core_schema_references(self):
        """Verify that each adapter references the authoritative schema."""
        for path in [
            REPO_ROOT / "CLAUDE.md",
            REPO_ROOT / ".gemini" / "GEMINI.md",
            REPO_ROOT / ".cursorrules",
            REPO_ROOT / ".cursor" / "rules" / "wiki.mdc",
        ]:
            if path.exists():
                content = path.read_text(encoding="utf-8")
                has_ref = (
                    "copilot-instructions.md" in content
                    or "AGENTS.md" in content
                )
                self.assertTrue(has_ref, f"{path} must reference authoritative instructions")
                self.assertIn("semantic-index.json", content, f"{path} must reference semantic-index.json")

    def test_sync_script_validation(self):
        """Verify that sync-adapters validator passes without errors."""
        res = sync_adapters_mod.validate_adapters()
        self.assertEqual(res, 0, "All instruction adapters must pass validation")


if __name__ == "__main__":
    unittest.main()
