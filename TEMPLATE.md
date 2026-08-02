# Template Customization Guide

This guide explains how to adapt the **LLM Wiki Template** to your specific domain. The wiki is structured as an **Open Knowledge Format (OKF) v0.2** knowledge bundle — every concept page has YAML frontmatter for provenance, trust, and lifecycle tracking.

## 1. Core Schema (`.github/copilot-instructions.md`)

This is the "brain" of your wiki. Copilot reads this on every request.

- **Domain Definition**: Replace `[YOUR DOMAIN]` with your topic.
- **Key Entities**: Update the list of example entities in the `## Structure - entities/` section to match your domain.
- **Concepts**: Update the foundational ideas in `## Structure - concepts/`.

## 2. OKF Page Frontmatter

Every wiki concept page uses YAML frontmatter. The required fields are:

```yaml
---
type: Entity            # Entity | Concept | Comparison | Source | Q&A | Overview
title: "Page Title"
description: "One-line summary used in index listings and search."
tags: [domain, subtopic]
status: draft           # draft | stable | deprecated
generated: { by: copilot-librarian/1.0, at: 2026-08-02T13:00:00Z }
sources:
  - id: source-slug
    resource: /wiki/sources/source-slug.md
    title: "Source document title"
    author: human:username
    last_modified: 2026-08-01
---
```

If your domain requires additional metadata fields (e.g., "Clinical Studies" might need `methodology` and `sample_size`), add them as extra frontmatter keys — OKF allows any producer-defined keys.

## 3. Page Formats

If your domain requires specific body sections (e.g., a "Dosage" section for medical entities), update the **Page formats** table in `copilot-instructions.md`.

## 4. The `raw/` Directory

Keep the `raw/` directory clean. It is meant to be an immutable record of where your knowledge came from.
- **Single files**: Just drop them in and type "ingest <filename>".
- **URLs**: You can simply give Copilot the URL. It is instructed to fetch and save it to `raw/` first.

## 5. Automation with Intake Scripts

If you have a large folder of existing markdown files:
1.  Copy them into `raw/`.
2.  Run `scripts/intake.ps1` (Windows) or `scripts/intake.sh` (Mac/Linux).

The script will iterate through the files and call Copilot for each one, ensuring `wiki/index.md` and `wiki/log.md` stay in sync.

## 6. Deployment (Optional)

Since the wiki is entirely markdown with YAML frontmatter:
- **[Obsidian](https://obsidian.md/) (Highly Recommended)**: Open the root folder as an Obsidian Vault. Use the **Graph View** to visualize your interlinked entities and concepts as a second brain.
- **GitHub Pages**: Use any static site generator (like MkDocs or Jekyll) to publish the `wiki/` directory as a website.
- **OKF-compatible tools**: Because the wiki is OKF v0.2 conformant, any tool that consumes OKF bundles can index, query, or visualize it.

---
*Follow the conventions. Trust the process. Build your knowledge.*

