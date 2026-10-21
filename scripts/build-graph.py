#!/usr/bin/env python3
"""
scripts/build-graph.py

Auto-generated knowledge graph manifest (wiki/graph.json).
Fulfills Issue #20:
- Extracts nodes (id, type, title, tags, silo, summary, path)
- Extracts edges (from, to, type) from explicit relationships and links
- Computes graph metrics and isolated/orphan nodes
- Cross-platform, deterministic, stdlib-only
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Root directory of the repository
REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"

EXCLUDED_FILENAMES = {"index.md", "README.md", ".gitkeep", "log.md", "overview.md"}
CANONICAL_SILOS = {
    "entities": "entity",
    "concepts": "concept",
    "comparisons": "comparison",
    "sources": "source",
    "qa": "qa",
    "archive": "archive",
}

RELATIONSHIP_PATTERN = re.compile(
    r'^[*-]\s+\*\*([a-zA-Z0-9_-]+)\*\*:\s*\[([^\]]+)\]\(([^)]+)\)',
    re.MULTILINE
)

LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def clean_markdown_inline(text: str) -> str:
    """Strip markdown links, bold, italics, code markers, and extra whitespace."""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'[*_`~^]', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_target_slug(href: str) -> Optional[str]:
    """Convert an href link to a target node slug."""
    clean = href.split("#")[0].split("?")[0].strip()
    if not clean or clean.startswith("http://") or clean.startswith("https://") or clean.startswith("mailto:"):
        return None
    p = Path(clean)
    if p.suffix.lower() == ".md":
        slug = p.stem
        if slug not in EXCLUDED_FILENAMES:
            return slug
    return None


def parse_page_node_and_edges(file_path: Path, silo: str) -> Tuple[Dict[str, Any], List[Dict[str, str]]]:
    """Parse a markdown file into a node dict and its outgoing edge list."""
    slug = file_path.stem
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    title = ""
    summary = ""
    tags: List[str] = []
    edges: List[Dict[str, str]] = []
    seen_edge_targets: Set[Tuple[str, str]] = set()

    # Extract title
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not title:
            title = clean_markdown_inline(stripped[2:])
            break
    if not title:
        title = slug.replace("-", " ").title()

    # Extract tags
    tag_match = re.search(r'\*\*Tags\*\*:\s*([^\n\r]+)', content)
    if tag_match:
        tag_str = tag_match.group(1)
        tags = [t.strip().lstrip("#") for t in re.split(r'[,|]', tag_str) if t.strip()]

    # Extract summary (first non-empty paragraph after heading)
    in_overview = False
    overview_lines: List[str] = []
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
        # Keep summary compact
        if len(summary) > 280:
            summary = summary[:277] + "..."

    # Extract explicit relationships
    rel_section = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## Relationships"):
            rel_section = True
            continue
        elif stripped.startswith("## ") and rel_section:
            rel_section = False

        if rel_section:
            m = re.match(r'^[*-]\s+\*\*([a-zA-Z0-9_-]+)\*\*:\s*\[([^\]]+)\]\(([^)]+)\)', stripped)
            if m:
                rel_type = m.group(1).lower()
                target_href = m.group(3)
                target_slug = extract_target_slug(target_href)
                if target_slug and (slug, target_slug, rel_type) not in seen_edge_targets:
                    seen_edge_targets.add((slug, target_slug, rel_type))
                    edges.append({
                        "from": slug,
                        "to": target_slug,
                        "type": rel_type,
                    })

    # Extract general inline links (as links-to if not already explicitly related)
    for m in LINK_PATTERN.finditer(content):
        href = m.group(2)
        target_slug = extract_target_slug(href)
        if target_slug and target_slug != slug:
            # Check if any edge already exists from slug to target_slug
            if not any(e["from"] == slug and e["to"] == target_slug for e in edges):
                edges.append({
                    "from": slug,
                    "to": target_slug,
                    "type": "links-to",
                })

    node = {
        "id": slug,
        "title": title,
        "silo": silo,
        "type": CANONICAL_SILOS.get(silo, "document"),
        "tags": tags,
        "summary": summary,
        "path": f"wiki/{silo}/{file_path.name}",
    }
    return node, edges


def generate_graph(wiki_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Scan wiki directory and compile nodes and edges into a graph dictionary."""
    if wiki_dir is None:
        wiki_dir = WIKI_DIR

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, str]] = []
    valid_slugs: Set[str] = set()

    # Collect nodes
    for silo_dir in sorted(wiki_dir.iterdir()):
        if not silo_dir.is_dir() or silo_dir.name not in CANONICAL_SILOS:
            continue
        silo = silo_dir.name
        for md_file in sorted(silo_dir.glob("*.md")):
            if md_file.name in EXCLUDED_FILENAMES:
                continue
            node, file_edges = parse_page_node_and_edges(md_file, silo)
            nodes.append(node)
            valid_slugs.add(node["id"])
            edges.extend(file_edges)

    # Filter edges so both ends exist in valid nodes
    valid_edges = [
        e for e in edges
        if e["from"] in valid_slugs and e["to"] in valid_slugs
    ]

    # Deduplicate edges
    seen = set()
    deduped_edges = []
    for e in valid_edges:
        key = (e["from"], e["to"], e["type"])
        if key not in seen:
            seen.add(key)
            deduped_edges.append(e)

    # Sort nodes and edges deterministically
    nodes.sort(key=lambda n: n["id"])
    deduped_edges.sort(key=lambda e: (e["from"], e["to"], e["type"]))

    return {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "node_count": len(nodes),
            "edge_count": len(deduped_edges),
            "silos": sorted(list(CANONICAL_SILOS.keys())),
        },
        "nodes": nodes,
        "edges": deduped_edges,
    }


def find_isolated_nodes(graph_data: Dict[str, Any]) -> List[str]:
    """Identify nodes that have zero inbound and zero outbound edges."""
    connected_nodes: Set[str] = set()
    for e in graph_data.get("edges", []):
        connected_nodes.add(e["from"])
        connected_nodes.add(e["to"])

    orphans = [
        n["id"] for n in graph_data.get("nodes", [])
        if n["id"] not in connected_nodes
    ]
    return sorted(orphans)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic Knowledge Graph compiler for GitHub Copilot LLM Wiki.")
    parser.add_argument("--check", action="store_true", help="Verify graph.json is up to date without writing.")
    parser.add_argument("--output", "-o", type=Path, default=None, help="Custom output path for graph.json.")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress status output.")
    args = parser.parse_args()

    target_path = args.output or (WIKI_DIR / "graph.json")
    graph_data = generate_graph()
    new_json = json.dumps(graph_data, indent=2, ensure_ascii=False) + "\n"

    if args.check:
        if not target_path.exists():
            if not args.quiet:
                print(f"[FAIL] {target_path} does not exist.")
            return 1
        existing_json = target_path.read_text(encoding="utf-8")
        # Compare parsed content ignoring timestamp differences
        existing_obj = json.loads(existing_json)
        test_new = dict(graph_data)
        test_existing = dict(existing_obj)
        test_new["metadata"]["generated_at"] = ""
        test_existing["metadata"]["generated_at"] = ""
        if test_new != test_existing:
            if not args.quiet:
                print(f"[FAIL] {target_path} is out of sync with wiki markdown source.")
            return 1
        if not args.quiet:
            print(f"[PASS] {target_path} is in sync ({graph_data['metadata']['node_count']} nodes, {graph_data['metadata']['edge_count']} edges).")
        return 0

    target_path.write_text(new_json, encoding="utf-8")
    if not args.quiet:
        print(f"[OK] Compiled knowledge graph to {target_path}")
        print(f"     Nodes: {graph_data['metadata']['node_count']}, Edges: {graph_data['metadata']['edge_count']}")
        orphans = find_isolated_nodes(graph_data)
        if orphans:
            print(f"     [WARN] {len(orphans)} isolated nodes detected: {', '.join(orphans[:5])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
