"""
adapters/registry.py

Adapter registry and intake routing engine.
Fulfills Issue #19:
- Dispatches source inputs to the appropriate adapter based on extension or protocol
- Allows dynamic registration of custom source adapters
"""

from typing import List, Optional

from adapters.base import BaseSourceAdapter
from adapters.csv_adapter import CsvSourceAdapter
from adapters.github_issues_adapter import GitHubIssuesAdapter
from adapters.pdf_adapter import PdfSourceAdapter
from adapters.url_adapter import UrlSourceAdapter

_REGISTERED_ADAPTERS: List[BaseSourceAdapter] = [
    GitHubIssuesAdapter(),
    CsvSourceAdapter(),
    PdfSourceAdapter(),
    UrlSourceAdapter(),
]


def register_adapter(adapter: BaseSourceAdapter) -> None:
    """Register a custom source adapter at the front of the routing pipeline."""
    _REGISTERED_ADAPTERS.insert(0, adapter)


def get_adapter_for(source: str) -> BaseSourceAdapter:
    """Find and return the matching adapter for a given source string or file path."""
    for adapter in _REGISTERED_ADAPTERS:
        if adapter.can_handle(source):
            return adapter
    raise ValueError(f"No registered source adapter found capable of handling: '{source}'")
