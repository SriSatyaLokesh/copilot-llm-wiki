# SEO, AEO, GEO & Open-Source Optimization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Transform the repository into an open-source ready, highly discoverable template optimized for traditional search (SEO), answer engines (AEO), and generative AI crawlers (GEO/AIO), while strictly preserving its #1 Google search ranking for `copilot llm wiki`.

**Architecture:** Additive-only enhancement strategy. We retain all existing top-of-fold keywords, headings, links, and text intact in `README.md`, while adding badges, a direct-answer definition block, deep FAQs, Schema.org JSON-LD structured data, emerging `llms.txt` and `llms-full.txt` standards, MIT License, Citation File Format, and GitHub community issue/PR templates.

**Tech Stack:** Markdown, YAML, JSON-LD, Jekyll / GitHub Pages, GitHub Actions / Issue Templates, Git/GitHub CLI.

---

### Task 1: Add Open-Source Governance & Scaffolding Files

**Files:**
- Create: `LICENSE`
- Create: `CODE_OF_CONDUCT.md`
- Create: `CITATION.cff`

**Step 1: Create `LICENSE`**
Standard MIT License with copyright 2026 Sri Satya Lokesh.

**Step 2: Create `CODE_OF_CONDUCT.md`**
Standard Contributor Covenant v2.1 with contact information.

**Step 3: Create `CITATION.cff`**
CFF 1.2.0 metadata for academic, technical, and LLM attribution.

**Step 4: Verify files exist and are valid**
Run file checks.

**Step 5: Commit**
`git commit -m "chore: add MIT license, code of conduct, and citation cff"`

---

### Task 2: Add GitHub Community Templates & Update Contribution Guides

**Files:**
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/feature_request.yml`
- Create: `.github/ISSUE_TEMPLATE/config.yml`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `CONTRIBUTING.md`

**Step 1: Create Issue Forms (`bug_report.yml`, `feature_request.yml`, `config.yml`)**
Clean GitHub Issue Forms asking for environment, logs, reproduction, and suggestions.

**Step 2: Update `PULL_REQUEST_TEMPLATE.md`**
Support both knowledge additions and template/tooling improvements.

**Step 3: Update `CONTRIBUTING.md`**
Replace `[YOUR DOMAIN]` with clear generic documentation for community contributors and personal template users.

**Step 4: Verify templates**
Verify syntax and file existence.

**Step 5: Commit**
`git commit -m "feat(community): add issue forms, update pr template and contributing guide"`

---

### Task 3: Implement AI Crawler & Discovery Standards (`llms.txt` & `llms-full.txt`)

**Files:**
- Create: `llms.txt`
- Create: `llms-full.txt`

**Step 1: Create `llms.txt`**
Adhere to the Answer.AI / llms.txt standard. Provide short project summary, key concepts, and clean directory of core files.

**Step 2: Create `llms-full.txt`**
Bundle complete context for one-shot LLM ingestion (README, architecture, Librarian schema, prompts).

**Step 3: Verify content density and formatting**
Verify markdown rendering and links.

**Step 4: Commit**
`git commit -m "feat(ai): add llms.txt and llms-full.txt for generative engine optimization"`

---

### Task 4: Enhance Jekyll & GitHub Pages SEO Metadata

**Files:**
- Modify: `_config.yml`

**Step 1: Add SEO and OpenGraph metadata in `_config.yml`**
Add `author`, `canonical_url`, `keywords`, `social`, and OpenGraph tags to maximize web indexing when hosted via GitHub Pages.

**Step 2: Commit**
`git commit -m "chore(seo): enrich _config.yml with metadata and OpenGraph configuration"`

---

### Task 5: Enhance `README.md` for SEO, AEO, GEO & Fix Prompt Syntax

**Files:**
- Modify: `README.md`

**Step 1: Preserve existing top content and keywords**
Ensure `# GitHub Copilot Wiki: An AI-Powered Second Brain Template`, `copilot llm wiki`, Karpathy gist link, and architecture remain intact.

**Step 2: Add status badges**
Badges for License, GitHub Template, Copilot, Obsidian, Stars, Forks, PRs Welcome.

**Step 3: Add AEO Direct Answer block**
A 50-word quick definition block for Google AI Overviews and Perplexity search answers.

**Step 4: Add Table of Contents**
Anchor links for deep crawling.

**Step 5: Fix lines 36–39 prompt syntax bug**
Format the `/ingest` VS Code Chat instruction and batch scripts cleanly.

**Step 6: Add Comprehensive FAQ section**
Semantic H3 questions for AEO / featured snippets.

**Step 7: Add Schema.org JSON-LD Structured Data**
`SoftwareSourceCode` and `FAQPage` embedded script.

**Step 8: Verify markdown and links**
Check link anchors and markdown validity.

**Step 9: Commit**
`git commit -m "docs: optimize README for SEO, AEO, GEO and add structured metadata"`

---

### Task 6: Final Verification, Push Branch & Raise Pull Request

**Step 1: Run comprehensive lint checks**
Check for git diff, file integrity, markdown cleanliness.

**Step 2: Push branch to origin**
`git push -u origin feature/seo-aeo-geo-oss-optimization`

**Step 3: Raise Pull Request via GitHub CLI**
`gh pr create --title "feat: comprehensive SEO, AEO, GEO & open-source optimization" --body "..."`
Reference Issue #2.
