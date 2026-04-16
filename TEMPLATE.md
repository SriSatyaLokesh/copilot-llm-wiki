# Template Customization Guide

This guide explains how to adapt the **LLM Wiki Template** to your specific domain.

## 1. Core Schema (`.github/copilot-instructions.md`)

This is the "brain" of your wiki. Copilot reads this on every request.

- **Domain Definition**: Replace `[YOUR DOMAIN]` with your topic.
- **Key Entities**: Update the list of example entities in the `## Structure - entities/` section to match your domain.
- **Concepts**: Update the foundational ideas in `## Structure - concepts/`.

## 2. Page Formats

If your domain requires specific metadata (e.g., "Clinical Studies" might need "Methodology" and "Sample Size" fields), update the **Page formats** table in `copilot-instructions.md`.

## 3. The `raw/` Directory

Keep the `raw/` directory clean. It is meant to be an immutable record of where your knowledge came from.
- **Single files**: Just drop them in and type "ingest <filename>".
- **URLs**: You can simply give Copilot the URL. It is instructed to fetch and save it to `raw/` first.

## 4. Automation with Intake Scripts

If you have a large folder of existing markdown files:
1.  Copy them into `raw/`.
2.  Run `scripts/intake.ps1` (Windows) or `scripts/intake.sh` (Mac/Linux).

The script will iterate through the files and call Copilot for each one, ensuring your `wiki/index.md` and `wiki/log.md` stay perfectly in sync.

## 5. Deployment (Optional)

Since the wiki is entirely markdown:
- **[Obsidian](https://obsidian.md/) (Highly Recommended)**: Open the root folder as an Obsidian Vault. Use the **Graph View** to visualize your interlinked entities and concepts as a second brain.
- **GitHub Pages**: Use any static site generator (like MkDocs or Jekyll) to publish the `wiki/` directory as a website.

---
*Follow the conventions. Trust the process. Build your knowledge.*
