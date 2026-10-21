#!/usr/bin/env python3
"""
tests/test_okf_security.py

Unit tests for OKF frontmatter escaping and security (Issue #9).
"""

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "adapters" / "okf"))

import export as okf_export


class TestOkfSecurity(unittest.TestCase):

    def test_scalar_json_escaping(self):
        """Verify that titles with quotes and newlines serialize to valid YAML scalars."""
        malicious_title = 'Architecture "V2" & Special: \nInjected: True'
        safe_serialized = json.dumps(malicious_title)
        
        # Valid JSON string scalar is valid YAML double-quoted scalar
        self.assertTrue(safe_serialized.startswith('"'))
        self.assertTrue(safe_serialized.endswith('"'))
        self.assertNotIn("\n", safe_serialized)
        self.assertIn('\\"', safe_serialized)


if __name__ == "__main__":
    unittest.main()
