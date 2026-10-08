## Agent skills

### Frontend Design
Whenever making changes to the frontend, proactively invoke the `frontend-design` skill to ensure design quality and consistency.

### Issue tracker

Issues and specs live in the repo's GitHub Issues. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context layout (one `CONTEXT.md` + `docs/adr/` at the root). See `docs/agents/domain.md`.

### Git Workflow
When a ticket is completed:
1. Create a separate feature branch.
2. Clean all backlogs and resolve any pending issues.
3. Commit with a descriptive, professional commit message.
4. Push the feature branch and merge it into `main` after verification.


## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
