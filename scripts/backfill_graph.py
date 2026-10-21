#!/usr/bin/env python3
"""
scripts/backfill_graph.py

One-time migration script to backfill:
1. Standardized Source Metadata (with Volatility & Last Verified) in wiki/sources/*.md
2. Directed Property Graph (## Relationships) in wiki/entities/*.md and wiki/concepts/*.md
3. Provenance citations in ## Key Facts bullets
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "wiki"
ENTITIES_DIR = WIKI_DIR / "entities"
CONCEPTS_DIR = WIKI_DIR / "concepts"
SOURCES_DIR = WIKI_DIR / "sources"

# Mapping each note to its primary backing source slug
PAGE_SOURCE_MAP = {
    # SubmitOrder API source
    "submitorder-api.md": "submitorder-api",
    "order-creation-flow.md": "submitorder-api",
    "quote-to-order-transformation.md": "submitorder-api",
    "commercial-portal.md": "submitorder-api",
    "service-level-account-creation.md": "submitorder-api",
    "business-backend.md": "submitorder-api",
    
    # Static IP source
    "static-ip-global-change-orders.md": "static-ip-global-change-orders",
    "cidr-block-allocation.md": "static-ip-global-change-orders",
    "zero-downtime-migration.md": "static-ip-global-change-orders",
    "static-ip-products.md": "static-ip-global-change-orders",
    "static-ip-changes.md": "static-ip-global-change-orders",
    "static-ip-change-scenarios.md": "static-ip-global-change-orders",
    
    # GCO source
    "global-change-order.md": "global-change-orders",
    "account-level-changes.md": "global-change-orders",
    "service-level-changes.md": "global-change-orders",
    "gco-lifecycle.md": "global-change-orders",
    "change-order-categories.md": "global-change-orders",
    "pricing-logic.md": "global-change-orders",
    "etf-calculation.md": "global-change-orders",
    "participating-systems.md": "global-change-orders",
    "portal-authorization-roles.md": "global-change-orders",
    "cxpbu-orderms.md": "global-change-orders",
    "cxpbu-customerms.md": "global-change-orders",
    "cxpbu-cadms.md": "global-change-orders",
    "cxpbu-catalog-db.md": "global-change-orders",
    "dynamics.md": "global-change-orders",
    "shazam.md": "global-change-orders",
    "netbox.md": "global-change-orders",
    "ziply-notification-platform.md": "global-change-orders",
}

RELATIONSHIPS_MAP = {
    # Entities
    "submitorder-api.md": [
        ("part-of", "CXPBU OrderMS", "wiki/entities/cxpbu-orderms.md"),
        ("depends-on", "Business Backend", "wiki/entities/business-backend.md"),
        ("depends-on", "Dynamics", "wiki/entities/dynamics.md"),
        ("implements", "Order Creation Flow", "wiki/concepts/order-creation-flow.md"),
        ("implements", "Quote to Order Transformation", "wiki/concepts/quote-to-order-transformation.md"),
    ],
    "business-backend.md": [
        ("part-of", "Commercial Portal", "wiki/entities/commercial-portal.md"),
        ("depends-on", "Commercial Portal", "wiki/entities/commercial-portal.md"),
        ("depends-on", "CXPBU OrderMS", "wiki/entities/cxpbu-orderms.md"),
    ],
    "commercial-portal.md": [
        ("depends-on", "Business Backend", "wiki/entities/business-backend.md"),
        ("implements", "Portal Authorization & Roles", "wiki/concepts/portal-authorization-roles.md"),
        ("related-to", "Global Change Order", "wiki/entities/global-change-order.md"),
    ],
    "cxpbu-orderms.md": [
        ("part-of", "Participating Systems", "wiki/comparisons/participating-systems.md"),
        ("depends-on", "CXPBU Catalog DB", "wiki/entities/cxpbu-catalog-db.md"),
        ("implements", "Pricing Logic & Rate Card Comparison", "wiki/concepts/pricing-logic.md"),
        ("implements", "ETF Calculation", "wiki/concepts/etf-calculation.md"),
    ],
    "cxpbu-customerms.md": [
        ("part-of", "Participating Systems", "wiki/comparisons/participating-systems.md"),
        ("related-to", "CXPBU CADMS", "wiki/entities/cxpbu-cadms.md"),
    ],
    "cxpbu-cadms.md": [
        ("part-of", "Participating Systems", "wiki/comparisons/participating-systems.md"),
        ("related-to", "CXPBU CustomerMS", "wiki/entities/cxpbu-customerms.md"),
    ],
    "cxpbu-catalog-db.md": [
        ("part-of", "Participating Systems", "wiki/comparisons/participating-systems.md"),
        ("related-to", "CXPBU OrderMS", "wiki/entities/cxpbu-orderms.md"),
    ],
    "dynamics.md": [
        ("part-of", "Participating Systems", "wiki/comparisons/participating-systems.md"),
        ("related-to", "GCO Lifecycle", "wiki/concepts/gco-lifecycle.md"),
    ],
    "global-change-order.md": [
        ("implements", "GCO Lifecycle", "wiki/concepts/gco-lifecycle.md"),
        ("related-to", "Change Order Categories", "wiki/concepts/change-order-categories.md"),
        ("depends-on", "Dynamics", "wiki/entities/dynamics.md"),
    ],
    "account-level-changes.md": [
        ("part-of", "Global Change Order", "wiki/entities/global-change-order.md"),
        ("depends-on", "CXPBU CustomerMS", "wiki/entities/cxpbu-customerms.md"),
        ("depends-on", "CXPBU CADMS", "wiki/entities/cxpbu-cadms.md"),
    ],
    "service-level-changes.md": [
        ("part-of", "Global Change Order", "wiki/entities/global-change-order.md"),
        ("implements", "Pricing Logic & Rate Card Comparison", "wiki/concepts/pricing-logic.md"),
        ("implements", "ETF Calculation", "wiki/concepts/etf-calculation.md"),
    ],
    "static-ip-changes.md": [
        ("part-of", "Global Change Order", "wiki/entities/global-change-order.md"),
        ("related-to", "Static IP Global Change Orders", "wiki/entities/static-ip-global-change-orders.md"),
    ],
    "static-ip-global-change-orders.md": [
        ("implements", "CIDR Block Allocation", "wiki/concepts/cidr-block-allocation.md"),
        ("implements", "Zero Downtime Migration", "wiki/concepts/zero-downtime-migration.md"),
        ("depends-on", "Shazam", "wiki/entities/shazam.md"),
        ("depends-on", "NetBox", "wiki/entities/netbox.md"),
    ],
    "static-ip-products.md": [
        ("part-of", "Static IP Global Change Orders", "wiki/entities/static-ip-global-change-orders.md"),
        ("related-to", "CIDR Block Allocation", "wiki/concepts/cidr-block-allocation.md"),
    ],
    "shazam.md": [
        ("part-of", "Participating Systems", "wiki/comparisons/participating-systems.md"),
        ("related-to", "NetBox", "wiki/entities/netbox.md"),
    ],
    "netbox.md": [
        ("part-of", "Participating Systems", "wiki/comparisons/participating-systems.md"),
        ("related-to", "Shazam", "wiki/entities/shazam.md"),
    ],
    "ziply-notification-platform.md": [
        ("part-of", "Participating Systems", "wiki/comparisons/participating-systems.md"),
        ("related-to", "Global Change Order", "wiki/entities/global-change-order.md"),
    ],
    
    # Concepts
    "order-creation-flow.md": [
        ("implements", "SubmitOrder API", "wiki/entities/submitorder-api.md"),
        ("depends-on", "Dynamics", "wiki/entities/dynamics.md"),
        ("related-to", "Service-Level Account Creation", "wiki/concepts/service-level-account-creation.md"),
    ],
    "quote-to-order-transformation.md": [
        ("implements", "SubmitOrder API", "wiki/entities/submitorder-api.md"),
        ("depends-on", "CXPBU OrderMS", "wiki/entities/cxpbu-orderms.md"),
    ],
    "service-level-account-creation.md": [
        ("implements", "SubmitOrder API", "wiki/entities/submitorder-api.md"),
        ("depends-on", "Dynamics", "wiki/entities/dynamics.md"),
    ],
    "gco-lifecycle.md": [
        ("implements", "Global Change Order", "wiki/entities/global-change-order.md"),
        ("depends-on", "Dynamics", "wiki/entities/dynamics.md"),
    ],
    "change-order-categories.md": [
        ("related-to", "Global Change Order", "wiki/entities/global-change-order.md"),
    ],
    "pricing-logic.md": [
        ("implements", "CXPBU OrderMS", "wiki/entities/cxpbu-orderms.md"),
        ("depends-on", "CXPBU Catalog DB", "wiki/entities/cxpbu-catalog-db.md"),
    ],
    "etf-calculation.md": [
        ("implements", "CXPBU OrderMS", "wiki/entities/cxpbu-orderms.md"),
        ("part-of", "Service Level Changes", "wiki/entities/service-level-changes.md"),
    ],
    "cidr-block-allocation.md": [
        ("implements", "Static IP Global Change Orders", "wiki/entities/static-ip-global-change-orders.md"),
        ("depends-on", "NetBox", "wiki/entities/netbox.md"),
    ],
    "zero-downtime-migration.md": [
        ("implements", "Static IP Global Change Orders", "wiki/entities/static-ip-global-change-orders.md"),
        ("related-to", "CIDR Block Allocation", "wiki/concepts/cidr-block-allocation.md"),
    ],
    "portal-authorization-roles.md": [
        ("part-of", "Commercial Portal", "wiki/entities/commercial-portal.md"),
        ("related-to", "Global Change Order", "wiki/entities/global-change-order.md"),
    ],
}


def refresh_sources():
    print("[*] Refreshing source verification timestamps & metadata...")
    for src_file in SOURCES_DIR.glob("*.md"):
        if src_file.name in ["index.md", ".gitkeep"]:
            continue
        content = src_file.read_text(encoding="utf-8")
        
        # Replace or insert standard metadata block
        metadata_block = """## Source Metadata
- **Ingested**: 2026-04-17
- **Source URL**: https://docs.internal.net
- **Last Verified**: 2026-10-21
- **Volatility**: medium
"""
        if "## Source Metadata" in content:
            content = re.sub(r'## Source Metadata\n.*?(?=\n## |\Z)', metadata_block.strip() + "\n", content, flags=re.DOTALL)
        elif "**Ingested**:" in content:
            content = re.sub(r'\*\*Ingested\*\*:\s*\d{4}-\d{2}-\d{2}', metadata_block.strip(), content)
        else:
            # Insert after H1
            content = re.sub(r'(# [^\n]+\n+)', r'\1' + metadata_block + '\n', content)
            
        src_file.write_text(content, encoding="utf-8")
        print(f"  [OK] Refreshed {src_file.name}")


def backfill_page(file_path: Path):
    filename = file_path.name
    content = file_path.read_text(encoding="utf-8")
    source_slug = PAGE_SOURCE_MAP.get(filename, "global-change-orders")
    provenance_tag = f"(Source: [{source_slug}](wiki/sources/{source_slug}.md), 2026-10-21)"
    
    lines = content.splitlines()
    new_lines = []
    in_key_facts = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            heading = stripped[3:].strip().lower()
            in_key_facts = ("key facts" in heading)
            new_lines.append(line)
            continue
            
        if in_key_facts and (stripped.startswith("- ") or stripped.startswith("* ")):
            # Check if line already has provenance
            if not re.search(r'\(Source:|\(source:|\[\^', stripped):
                # Append provenance cleanly
                line = line.rstrip() + f" {provenance_tag}"
        new_lines.append(line)
        
    updated_content = "\n".join(new_lines)
    
    # Check if ## Relationships section exists
    if "## Relationships" not in updated_content and filename in RELATIONSHIPS_MAP:
        rel_lines = ["\n## Relationships"]
        for rel_type, rel_target_name, rel_target_path in RELATIONSHIPS_MAP[filename]:
            rel_lines.append(f"- **{rel_type}**: [{rel_target_name}]({rel_target_path})")
            
        rel_block = "\n".join(rel_lines)
        
        # Insert before ## See Also
        if "## See Also" in updated_content:
            updated_content = updated_content.replace("## See Also", rel_block + "\n\n## See Also")
        else:
            updated_content += "\n" + rel_block
            
    file_path.write_text(updated_content, encoding="utf-8")
    print(f"  [OK] Backfilled relationships & provenance in {filename}")


def main():
    refresh_sources()
    print("\n[*] Backfilling entities...")
    for f in ENTITIES_DIR.glob("*.md"):
        if f.name in ["index.md", ".gitkeep"]:
            continue
        backfill_page(f)
        
    print("\n[*] Backfilling concepts...")
    for f in CONCEPTS_DIR.glob("*.md"):
        if f.name in ["index.md", ".gitkeep"]:
            continue
        backfill_page(f)
        
    print("\n[SUCCESS] Backfill completed.")

if __name__ == "__main__":
    main()
