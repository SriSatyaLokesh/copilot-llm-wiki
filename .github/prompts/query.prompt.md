---
agent: 'agent'
description: 'Ask a question based on wiki knowledge'
---

Read the **Query workflow** in `.github/copilot-instructions.md` and execute it now.

**User Question**: ${input:question:What would you like to know from the wiki?}

**Instructions for Librarian**:
1. Search ONLY the `wiki/` directory content.
2. If the answer is not in the wiki, say: "I couldn't find an answer in the wiki. Would you like me to ingest a new source for this?"
3. Follow the citation format: **Pages consulted:** [page1.md], [page2.md]

**Filing offer:** If the answer synthesizes content from 2 or more wiki pages, offer to file it as `wiki/qa/<slug>.md` and update `index.md` and `log.md`.
