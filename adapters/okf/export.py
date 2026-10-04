#!/usr/bin/env python3
"""
OKF v0.2 Bundle Exporter
Converts the human-readable Markdown wiki into a strictly conformant
Open Knowledge Format (OKF) v0.2 bundle in dist/okf/
"""

import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
OUTPUT_DIR = REPO_ROOT / "dist" / "okf"

SILOS = {
    "entities": "Entity",
    "concepts": "Concept",
    "comparisons": "Comparison",
    "sources": "Source",
    "qa": "Q&A",
}

def parse_markdown(content: str):
    """Extract frontmatter and body from markdown content."""
    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            raw_fm = parts[1]
            body = parts[2].strip()
            # Simple line-by-line YAML parser for basic fields
            for line in raw_fm.splitlines():
                if ":" in line and not line.strip().startswith("-"):
                    k, v = line.split(":", 1)
                    frontmatter[k.strip()] = v.strip().strip('"').strip("'")
    return frontmatter, body

def get_title_and_description(body: str, fallback_title: str):
    title = fallback_title
    description = ""
    lines = [line.strip() for line in body.splitlines() if line.strip()]
    
    for i, line in enumerate(lines):
        if line.startswith("# ") and title == fallback_title:
            title = line.replace("# ", "").strip()
        elif not line.startswith("#") and not description:
            # First non-header paragraph is used as description
            description = line[:150]
            
    if not description:
        description = f"Knowledge document for {title}."
    return title, description

def export_okf_bundle():
    print(f"[*] Generating OKF v0.2 bundle from {WIKI_DIR} -> {OUTPUT_DIR}...")
    
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Process silos
    for silo, okf_type in SILOS.items():
        silo_src = WIKI_DIR / silo
        silo_dest = OUTPUT_DIR / silo
        silo_dest.mkdir(parents=True, exist_ok=True)
        
        pages = []
        if silo_src.exists():
            for f in sorted(silo_src.glob("*.md")):
                if f.name == "index.md" or f.name.startswith("."):
                    continue
                content = f.read_text(encoding="utf-8")
                fm, body = parse_markdown(content)
                fallback = f.stem.replace("-", " ").title()
                title, desc = get_title_and_description(body, fallback)
                
                # Build OKF v0.2 frontmatter
                page_fm = {
                    "type": fm.get("type", okf_type),
                    "title": fm.get("title", title),
                    "description": fm.get("description", desc),
                    "status": fm.get("status", "stable"),
                }
                
                fm_block = [
                    "---",
                    f"type: {page_fm['type']}",
                    f"title: \"{page_fm['title']}\"",
                    f"description: \"{page_fm['description']}\"",
                    f"status: {page_fm['status']}",
                    f"generated: {{ by: copilot-librarian/1.0, at: {now_iso} }}",
                    "---",
                    "",
                ]
                
                (silo_dest / f.name).write_text("\n".join(fm_block) + body, encoding="utf-8")
                pages.append((page_fm['title'], f.name, page_fm['description']))
        
        # Generate progressive disclosure subdirectory index.md
        sub_index_lines = [
            f"# {silo.capitalize()}",
            "",
            f"Curated {okf_type} concepts in this knowledge bundle.",
            "",
        ]
        if pages:
            for p_title, p_file, p_desc in pages:
                sub_index_lines.append(f"* [{p_title}]({p_file}) - {p_desc}")
        else:
            sub_index_lines.append("* _No pages yet._")
            
        (silo_dest / "index.md").write_text("\n".join(sub_index_lines) + "\n", encoding="utf-8")
        print(f"  [OK] {silo}: processed {len(pages)} pages + index.md")
        
    # Overview
    overview_src = WIKI_DIR / "overview.md"
    if overview_src.exists():
        content = overview_src.read_text(encoding="utf-8")
        fm, body = parse_markdown(content)
        title, desc = get_title_and_description(body, "Domain Overview")
        overview_content = (
            f"---\n"
            f"type: Overview\n"
            f"title: \"{title}\"\n"
            f"description: \"{desc}\"\n"
            f"status: stable\n"
            f"generated: {{ by: copilot-librarian/1.0, at: {now_iso} }}\n"
            f"---\n\n"
            f"{body}"
        )
        (OUTPUT_DIR / "overview.md").write_text(overview_content, encoding="utf-8")

    # Root index.md
    root_index = [
        "---",
        'okf_version: "0.2"',
        "---",
        "",
        "# Wiki Knowledge Bundle — Root Catalog",
        "",
        "## Overview",
        "* [Overview](overview.md) - Top-level orientation",
        "",
    ]
    for silo in SILOS.keys():
        root_index.append(f"## {silo.capitalize()}")
        silo_dest = OUTPUT_DIR / silo
        silo_pages = [f for f in sorted(silo_dest.glob("*.md")) if f.name != "index.md"]
        if silo_pages:
            for sp in silo_pages:
                c = sp.read_text(encoding="utf-8")
                fm, _ = parse_markdown(c)
                t = fm.get("title", sp.stem)
                d = fm.get("description", "")
                root_index.append(f"* [{t}]({silo}/{sp.name}) - {d}")
        else:
            root_index.append("* _No pages yet._")
        root_index.append("")
        
    (OUTPUT_DIR / "index.md").write_text("\n".join(root_index), encoding="utf-8")
    print("  [OK] root index.md generated with okf_version: \"0.2\"")

    # Newest-first log.md
    log_src = WIKI_DIR / "log.md"
    today_str = datetime.now().strftime("%Y-%m-%d")
    okf_log = [
        "# Wiki Knowledge Bundle — Log",
        "",
        f"## {today_str}",
        "* **Export**: Compiled clean wiki into OKF v0.2 conformant bundle.",
        "",
    ]
    if log_src.exists():
        raw_log = log_src.read_text(encoding="utf-8")
        okf_log.append("### Historical Operations")
        okf_log.append(raw_log)
    (OUTPUT_DIR / "log.md").write_text("\n".join(okf_log), encoding="utf-8")
    print("  [OK] log.md compiled to OKF format")

    print(f"\n[SUCCESS] Successfully compiled OKF v0.2 bundle at: {OUTPUT_DIR}")

if __name__ == "__main__":
    export_okf_bundle()
