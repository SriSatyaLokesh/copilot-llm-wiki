#!/usr/bin/env python3
"""
scripts/build-semantic-index.py

Lightweight local semantic and keyword index compiler (wiki/semantic-index.json).
Fulfills Issue #23:
- Extracts entity/concept titles, dense summaries, keywords, and outbound links
- Zero external vector DB or cloud dependencies; sub-second regeneration
- High-signal tokenization with built-in stopword filtering
- Fast candidate search/retrieval helper for LLM agent query routing
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"

EXCLUDED_FILENAMES = {"index.md", "README.md", ".gitkeep", "log.md", "overview.md"}
CANONICAL_SILOS = {"entities", "concepts", "comparisons", "sources", "qa", "archive"}

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
    "by", "can", "did", "do", "does", "doing", "don", "down", "during", "each", "few", "for",
    "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how", "if", "in", "into", "is", "it", "its", "itself", "just",
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "s", "same", "she",
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "why", "will", "with", "you", "your", "yours", "yourself", "yourselves"
}

LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def clean_markdown_inline(text: str) -> str:
    """Strip markdown links, bold, italics, code markers, and extra whitespace."""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'[*_`~^]', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_keywords(text: str, max_keywords: int = 25) -> List[str]:
    """Tokenize and extract significant alphanumeric keywords."""
    words = re.findall(r'[a-zA-Z0-9_\-]+', text.lower())
    freq: Dict[str, int] = {}
    for w in words:
        if len(w) >= 3 and w not in STOPWORDS and not w.isdigit():
            freq[w] = freq.get(w, 0) + 1

    # Sort by frequency descending, then alphabetically
    sorted_keywords = sorted(freq.keys(), key=lambda k: (-freq[k], k))
    return sorted_keywords[:max_keywords]


def extract_outbound_slugs(content: str, current_slug: str) -> List[str]:
    """Extract list of valid target markdown slugs from outbound links."""
    outbound: Set[str] = set()
    for m in LINK_PATTERN.finditer(content):
        href = m.group(2)
        clean = href.split("#")[0].split("?")[0].strip()
        if not clean or clean.startswith("http://") or clean.startswith("https://") or clean.startswith("mailto:"):
            continue
        p = Path(clean)
        if p.suffix.lower() == ".md":
            target = p.stem
            if target != current_slug and target not in EXCLUDED_FILENAMES:
                outbound.add(target)
    return sorted(list(outbound))


def parse_page_semantic_entry(file_path: Path, silo: str) -> Dict[str, Any]:
    """Parse a markdown file into a dense semantic index entry."""
    slug = file_path.stem
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    title = ""
    summary = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not title:
            title = clean_markdown_inline(stripped[2:])
            break
    if not title:
        title = slug.replace("-", " ").title()

    overview_lines: List[str] = []
    in_overview = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            in_overview = True
            continue
        if in_overview:
            if stripped.startswith("## "):
                if overview_lines:
                    break
                continue
            if stripped and not stripped.startswith(">") and not stripped.startswith("-"):
                overview_lines.append(stripped)
            elif not stripped and overview_lines:
                break
    if overview_lines:
        summary = clean_markdown_inline(" ".join(overview_lines))
        if len(summary) > 280:
            summary = summary[:277] + "..."

    # Extract keywords from title, summary, and whole content
    title_words = extract_keywords(title, max_keywords=10)
    summary_words = extract_keywords(summary, max_keywords=15)
    content_words = extract_keywords(content, max_keywords=30)

    combined_keywords: List[str] = []
    seen = set()
    for w in title_words + summary_words + content_words:
        if w not in seen:
            seen.add(w)
            combined_keywords.append(w)

    outbound_links = extract_outbound_slugs(content, slug)

    return {
        "id": slug,
        "title": title,
        "silo": silo,
        "summary": summary,
        "keywords": combined_keywords[:25],
        "outbound_links": outbound_links,
        "path": f"wiki/{silo}/{file_path.name}",
    }


def generate_semantic_index(wiki_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Scan wiki directory and compile a dense semantic index."""
    if wiki_dir is None:
        wiki_dir = WIKI_DIR

    entries: List[Dict[str, Any]] = []

    for silo_dir in sorted(wiki_dir.iterdir()):
        if not silo_dir.is_dir() or silo_dir.name not in CANONICAL_SILOS:
            continue
        silo = silo_dir.name
        for md_file in sorted(silo_dir.glob("*.md")):
            if md_file.name in EXCLUDED_FILENAMES:
                continue
            entry = parse_page_semantic_entry(md_file, silo)
            entries.append(entry)

    entries.sort(key=lambda e: e["id"])

    return {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total_entries": len(entries),
            "silos": sorted(list(CANONICAL_SILOS)),
        },
        "entries": entries,
    }


def query_semantic_index(semantic_index: Dict[str, Any], query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Simple, zero-dependency token similarity search for routing queries."""
    query_tokens = set(extract_keywords(query))
    if not query_tokens:
        return []

    scored_entries = []
    for entry in semantic_index.get("entries", []):
        score = 0
        entry_keywords = set(entry.get("keywords", []))
        entry_id = entry.get("id", "").lower()
        entry_title = entry.get("title", "").lower()

        for qt in query_tokens:
            if qt == entry_id:
                score += 10
            elif qt in entry_id:
                score += 5
            if qt in entry_title:
                score += 4
            if qt in entry_keywords:
                score += 2

        if score > 0:
            scored_entries.append((score, entry))

    scored_entries.sort(key=lambda x: -x[0])
    return [e[1] for e in scored_entries[:top_k]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic Semantic & Keyword Index compiler for GitHub Copilot LLM Wiki.")
    parser.add_argument("--check", action="store_true", help="Verify semantic-index.json is up to date without writing.")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Custom output path for semantic-index.json.")
    parser.add_argument("--query", "-q", type=str, default=None, help="Search semantic index for matching candidates.")
    parser.add_argument("--quiet", action="store_true", help="Suppress status output.")
    args = parser.parse_args()

    target_path = args.output or (WIKI_DIR / "semantic-index.json")

    if args.query:
        if not target_path.exists():
            print(f"[FAIL] {target_path} not found. Run without --query to generate.", file=sys.stderr)
            return 1
        data = json.loads(target_path.read_text(encoding="utf-8"))
        results = query_semantic_index(data, args.query)
        print(f"Top matches for '{args.query}':")
        for idx, r in enumerate(results, 1):
            print(f"  {idx}. [{r['title']}]({r['path']}) - {r['summary']}")
        return 0

    index_data = generate_semantic_index()
    new_json = json.dumps(index_data, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not target_path.exists():
            if not args.quiet:
                print(f"[FAIL] {target_path} does not exist.")
            return 1
        existing_json = target_path.read_text(encoding="utf-8")
        existing_obj = json.loads(existing_json)
        test_new = dict(index_data)
        test_existing = dict(existing_obj)
        test_new["metadata"]["generated_at"] = ""
        test_existing["metadata"]["generated_at"] = ""
        if test_new != test_existing:
            if not args.quiet:
                print(f"[FAIL] {target_path} is out of sync with wiki markdown source.")
            return 1
        if not args.quiet:
            print(f"[PASS] {target_path} is in sync ({index_data['metadata']['total_entries']} entries).")
        return 0

    target_path.write_text(new_json, encoding="utf-8")
    if not args.quiet:
        print(f"[OK] Compiled semantic index to {target_path}")
        print(f"     Entries: {index_data['metadata']['total_entries']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
