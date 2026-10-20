#!/usr/bin/env python3
"""
scripts/build-index.py

Deterministic compiler for hierarchical wiki indexes.
Scans content silos in wiki/, extracts titles and clean summaries,
and generates alphabetical silo index.md files and a root routing index.md.

Usage:
    python scripts/build-index.py             # Rebuilds all index.md files
    python scripts/build-index.py --check     # Verifies indexes are in sync (exit 0/1)
    python scripts/build-index.py --hierarchical  # Force progressive disclosure mode
    python scripts/build-index.py --flat          # Force flat index listing
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Root directory of the repository
REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"

# Canonical silos and their descriptions
SILO_CONFIG = {
    "entities": {
        "title": "Entities",
        "description": "Domain entities, actors, systems, services, and APIs.",
        "singular": "Entity",
    },
    "concepts": {
        "title": "Concepts",
        "description": "Core domain concepts, lifecycles, protocols, workflows, and rules.",
        "singular": "Concept",
    },
    "comparisons": {
        "title": "Comparisons",
        "description": "Side-by-side matrices, scenario analyses, and trade-off evaluations.",
        "singular": "Comparison",
    },
    "sources": {
        "title": "Sources",
        "description": "Summaries and key takeaways of ingested primary source documents.",
        "singular": "Source",
    },
    "qa": {
        "title": "Q&A",
        "description": "Synthesized answers to multi-page queries and architectural questions.",
        "singular": "Q&A",
    },
    "archive": {
        "title": "Archive",
        "description": "Deprecated, superseded, and merged knowledge documents.",
        "singular": "Archived Document",
    },
}

EXCLUDED_FILENAMES = {"index.md", "README.md", ".gitkeep"}


def clean_markdown_inline(text: str) -> str:
    """Strip markdown links, bold, italics, code markers, and extra whitespace."""
    # Convert [text](url) to text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Convert [[wikilink|text]] to text, or [[wikilink]] to wikilink
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    # Remove bold, italics, inline code, footnote anchors
    text = re.sub(r'[*_`~^]', '', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Collapse multiple whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_page(file_path: Path) -> Tuple[str, str]:
    """
    Extract title and first summary sentence/paragraph from a markdown file.
    Returns (title, description).
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return file_path.stem.replace("-", " ").title(), f"Error reading file: {e}"

    lines = content.splitlines()
    title = ""
    description = ""
    overview_lines = []
    in_target_section = False
    in_fence = False

    for line in lines:
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # Extract H1 title
        if stripped.startswith("# ") and not title:
            title = clean_markdown_inline(stripped[2:])
            continue

        # Check for target heading sections
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            if any(h in heading for h in ["overview", "definition", "summary table", "key takeaways", "description"]):
                in_target_section = True
                continue
            else:
                # If we were in a target section and hit a new H2, end extraction
                if in_target_section and overview_lines:
                    break
                in_target_section = False

        # If inside target section or before any other H2
        if in_target_section or (title and not description and not stripped.startswith("## ")):
            # Skip empty lines, blockquotes, bullets, tables
            if not stripped or stripped.startswith(">") or stripped.startswith("|") or stripped.startswith("- **Ingested"):
                continue
            if stripped.startswith("- ") or stripped.startswith("* "):
                # If bullet point contains rich text, take it if we have nothing else
                cleaned_bullet = clean_markdown_inline(stripped[2:])
                if len(cleaned_bullet) > 20 and not overview_lines:
                    overview_lines.append(cleaned_bullet)
                continue

            cleaned = clean_markdown_inline(stripped)
            if cleaned and not cleaned.startswith("#"):
                overview_lines.append(cleaned)
                # One good paragraph is enough
                if len(" ".join(overview_lines)) > 80:
                    break

    if not title:
        title = file_path.stem.replace("-", " ").title()

    full_desc = " ".join(overview_lines)
    if full_desc:
        # Truncate at sentence boundary or around 130 characters
        if ". " in full_desc[:140]:
            first_sentence = full_desc[:full_desc.find(". ") + 1]
            description = first_sentence.strip()
        elif len(full_desc) > 130:
            description = full_desc[:127].rsplit(" ", 1)[0] + "..."
        else:
            description = full_desc.strip()
    else:
        description = f"Knowledge document for {title}."

    return title, description


def scan_silo(silo_name: str, silo_path: Path) -> List[Tuple[str, str, str]]:
    """
    Scans a silo directory recursively (handling archive subdirs).
    Returns a sorted list of (title, relative_link, description).
    """
    if not silo_path.exists():
        return []

    entries = []
    # Find all .md files in this silo
    for md_file in silo_path.rglob("*.md"):
        if md_file.name in EXCLUDED_FILENAMES:
            continue
        rel_path = md_file.relative_to(silo_path).as_posix()
        title, desc = parse_page(md_file)
        entries.append((title, rel_path, desc))

    # Sort alphabetically by title (case-insensitive)
    entries.sort(key=lambda x: x[0].lower())
    return entries


def generate_silo_index(silo_name: str, entries: List[Tuple[str, str, str]]) -> str:
    """Generate content for wiki/<silo>/index.md."""
    config = SILO_CONFIG.get(silo_name, {
        "title": silo_name.capitalize(),
        "description": f"Catalog of {silo_name} documents.",
        "singular": "Document"
    })

    title = config["title"]
    description = config["description"]
    count = len(entries)

    lines = [
        f"# {title} Index",
        "",
        description,
        "",
        f"**Total Pages**: {count}",
        "",
    ]

    if not entries:
        lines.append("_No pages yet._")
    else:
        for p_title, p_file, p_desc in entries:
            lines.append(f"- [{p_title}]({p_file}) — {p_desc}")

    lines.append("")
    lines.append("## See Also")
    lines.append("- [Wiki Index](../index.md)")
    lines.append("- [Overview](../overview.md)")
    lines.append("")

    return "\n".join(lines)


def get_wiki_domain_name() -> str:
    """Attempt to detect domain name from wiki/overview.md or fallback."""
    overview_path = WIKI_DIR / "overview.md"
    if overview_path.exists():
        content = overview_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            if line.startswith("# "):
                h1 = line.replace("# ", "").strip()
                if "What is " in h1:
                    name = h1.replace("What is ", "").rstrip("?").strip()
                    if name and name != "[YOUR DOMAIN]":
                        return name
                elif h1 and h1 != "[YOUR DOMAIN]":
                    return h1
    return "GitHub Copilot"


def generate_root_index(
    silo_data: Dict[str, List[Tuple[str, str, str]]],
    hierarchical_mode: bool
) -> str:
    """Generate content for wiki/index.md."""
    domain_name = get_wiki_domain_name()
    total_pages = sum(len(entries) for entries in silo_data.values())

    lines = [
        f"# {domain_name} Wiki — Index",
        "",
        "Welcome to the knowledge base index. This catalog is automatically maintained",
        "to enable progressive disclosure and token-efficient context retrieval.",
        "",
        f"**Total Active Knowledge Pages**: {total_pages}",
        "",
        "## Silo Indexes",
        "",
    ]

    for silo_name, config in SILO_CONFIG.items():
        count = len(silo_data.get(silo_name, []))
        silo_title = config["title"]
        silo_desc = config["description"]
        lines.append(f"- [{silo_title}](wiki/{silo_name}/index.md) ({count} pages) — {silo_desc}")

    lines.append("")
    lines.append("## Overview")
    lines.append("- [Overview](wiki/overview.md) — Top-level domain orientation and architecture")
    lines.append("")

    # If flat mode or total pages <= 50, provide inline catalog under each section
    if not hierarchical_mode:
        for silo_name, config in SILO_CONFIG.items():
            entries = silo_data.get(silo_name, [])
            lines.append(f"## {config['title']}")
            if not entries:
                lines.append("_No pages yet._")
            else:
                for p_title, p_file, p_desc in entries:
                    lines.append(f"- [{p_title}](wiki/{silo_name}/{p_file}) — {p_desc}")
            lines.append("")

    return "\n".join(lines)


def build_all_indexes(check_only: bool = False, force_mode: Optional[str] = None) -> int:
    """Build or check all silo indexes and root index."""
    if not WIKI_DIR.exists():
        print(f"Error: wiki directory not found at {WIKI_DIR}", file=sys.stderr)
        return 1

    # Ensure archive directory structure exists
    archive_dir = WIKI_DIR / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    gitkeep = archive_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")

    silo_data: Dict[str, List[Tuple[str, str, str]]] = {}
    for silo_name in SILO_CONFIG.keys():
        silo_path = WIKI_DIR / silo_name
        silo_path.mkdir(parents=True, exist_ok=True)
        silo_data[silo_name] = scan_silo(silo_name, silo_path)

    total_pages = sum(len(entries) for entries in silo_data.values())

    if force_mode == "hierarchical":
        hierarchical = True
    elif force_mode == "flat":
        hierarchical = False
    else:
        # Default: Hierarchical progressive disclosure if > 25 pages
        hierarchical = total_pages > 25

    planned_writes: Dict[Path, str] = {}

    # 1. Silo indexes
    for silo_name, entries in silo_data.items():
        silo_index_path = WIKI_DIR / silo_name / "index.md"
        silo_content = generate_silo_index(silo_name, entries)
        planned_writes[silo_index_path] = silo_content

    # 2. Root index
    root_index_path = WIKI_DIR / "index.md"
    root_content = generate_root_index(silo_data, hierarchical_mode=hierarchical)
    planned_writes[root_index_path] = root_content

    # Check mode vs write mode
    if check_only:
        out_of_sync = []
        for file_path, content in planned_writes.items():
            if not file_path.exists():
                out_of_sync.append(f"Missing: {file_path.relative_to(REPO_ROOT)}")
            else:
                existing = file_path.read_text(encoding="utf-8")
                if existing.strip() != content.strip():
                    out_of_sync.append(f"Out of sync: {file_path.relative_to(REPO_ROOT)}")

        if out_of_sync:
            print("[FAIL] The following wiki index files are missing or out of sync:")
            for item in out_of_sync:
                print(f"  - {item}")
            print("\nRun 'python scripts/build-index.py' to regenerate all indexes deterministically.")
            return 1
        else:
            print(f"[PASS] All {len(planned_writes)} wiki indexes are up-to-date ({total_pages} total pages indexed).")
            return 0

    # Write mode
    written = 0
    for file_path, content in planned_writes.items():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        written += 1
        print(f"  [OK] Generated {file_path.relative_to(REPO_ROOT)}")

    print(f"\n[SUCCESS] Successfully compiled {written} indexes ({total_pages} knowledge pages indexed).")
    print(f"Mode: {'Hierarchical (Progressive Disclosure)' if hierarchical else 'Flat/Hybrid'}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Deterministic compiler for hierarchical wiki indexes.")
    parser.add_argument("--check", action="store_true", help="Check if indexes are in sync without writing")
    parser.add_argument("--hierarchical", action="store_const", dest="mode", const="hierarchical", help="Force hierarchical routing mode")
    parser.add_argument("--flat", action="store_const", dest="mode", const="flat", help="Force flat catalog mode")
    args = parser.parse_args()

    sys.exit(build_all_indexes(check_only=args.check, force_mode=args.mode))


if __name__ == "__main__":
    main()
