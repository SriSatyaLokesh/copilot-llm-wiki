# Open Knowledge Format (OKF v0.2) Adapter

This adapter provides full **Open Knowledge Format (OKF) v0.2** interoperability for **Copilot LLM Wiki**, allowing your personal markdown second brain to be exported into a standardized, machine-readable knowledge bundle for enterprise AI systems, Google Cloud agents, and multi-agent orchestrators.

---

## Architecture: Clean Core + Adapter Pattern

Rather than forcing mandatory YAML frontmatter and multiple sub-indexes onto your daily desktop note-taking workflow, this repository separates concerns:

1. **Core Wiki (`wiki/`)**: Maintained as clean, fluid, standard Markdown. Optimal for rapid human note-taking and distraction-free viewing in Obsidian, VS Code, and JetBrains.
2. **OKF Adapter (`adapters/okf/`)**: Transforms the clean wiki into an official OKF v0.2 bundle on demand, deterministically generating YAML frontmatter, actor conventions (`copilot-librarian/1.0`), timestamps, and progressive disclosure sub-indexes.

---

## 🚀 Exporting to an OKF v0.2 Bundle

Run the Python exporter from the repository root:

```bash
python adapters/okf/export.py
```

The script will compile your wiki into `dist/okf/`:
- Injects standard OKF v0.2 YAML frontmatter (`type`, `title`, `description`, `status`, `generated`).
- Creates `index.md` files in each subdirectory (`entities/`, `concepts/`, etc.) with asterisk bullet syntax.
- Generates a root `dist/okf/index.md` with `okf_version: "0.2"` frontmatter.
- Formats `dist/okf/log.md` into newest-first dates.

---

## 🤖 Optional: Native OKF Copilot Persona

If you want your desktop Copilot instance to author notes directly with OKF frontmatter during interactive chat:
1. Replace or supplement your `.github/copilot-instructions.md` with `adapters/okf/copilot-instructions.okf.md`.
2. Copilot will write OKF frontmatter natively on every newly generated concept or entity note.

---

## 📜 Specification Reference

For complete schema details, trust tiers, and lifecycle definitions, consult [SPEC.md](SPEC.md).

---
*Original OKF v0.2 specification structure contributed by [@aayush-t-gilead](https://github.com/aayush-t-gilead).*
