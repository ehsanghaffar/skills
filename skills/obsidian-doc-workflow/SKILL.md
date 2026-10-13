---
name: obsidian-doc-workflow
description: Create, update, classify, and archive Obsidian documentation documents following structured vault conventions and templates.
version: 1.0.3
---

# Obsidian Documentation Workflow

This skill manages structured documentation in an Obsidian vault following a formal documentation system with strict conventions.

## Vault Path

Resolved vault path is typically(Mac):
${OBSIDIAN_VAULT_PATH:-/Users/${USER}/.obsidian}

The vault uses three main sections:
- `01 Projects/` - Project-specific documentation
- `02 Shared Knowledge/` - Reusable engineering patterns
- `00 Meta/` - Vault standards, templates, and guidance

## Document Creation

### For Project Documents

Use the project root template. Always start with `Project Overview.md` in the project root, then architecture, guides, API reference, and so on.

**Example project structure:**
```
01 Projects/{Project}/
├── Project Overview.md
├── Architecture & Tech Stack.md
├── Development Guide.md
├── Component & API Reference.md
├── Testing Guide.md
├── Deployment & Infrastructure.md
├── Maintenance Board.md
├── Changelog.md
└── <Architecture>, <Services>, <Database>, <Guides>, 等。
```

**Standard frontmatter:**
```yaml
---
type: project|architecture|guide|reference|research|runbook|maintenance|changelog
project: "Project Name"
status: active|archived|deprecated
area: frontend|backend|infra|security|testing|devops
created: 2026-09-19
updated: 2026-09-19
tags: [project-slug, area, type]
related_projects: []
---
```

### For Shared Knowledge Documents

Use the `Concept.md` or `Tool.md` templates.

**Standard frontmatter:**
```yaml
---
type: concept|tool|architecture|guide
status: active|archived
area: patterns|frontend|backend|testing|devops
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [category, subcategory, type]
related_projects: [Project A, Project B]
---
```

## Classification Rules

### Project vs Shared Knowledge

- **Project knowledge** → `01 Projects/{Project}/` (obsoletes when project disappears)
- **Reusable patterns** → `02 Shared Knowledge/` (remains useful after projects are gone)

### Residence Categories

- Project-specific implementations → Project folder
- General patterns, tech guides, security practices, deployment strategies → Shared Knowledge
- External references → `03 Resources/`

**Examples:**
- `Backend Integration Guide` (specific to a project) → Project folder
- `Monorepo Patterns` (any team can use) → Shared Knowledge
- `Vercel deployment docs` → Resources

## Templates

Respective templates in `00 Meta/Templates/`:
- `Project Overview.md`
- `Architecture.md`
- `Development Guide.md`
- `Technical Guide.md`
- `API Reference.md`
- `Testing Guide.md`
- `Deployment & Infrastructure.md`
- `ADR.md`
- `Decision.md`
- `Research.md`
- `Concept.md`
- `Tool.md`
- `Runbook.md`
- `Maintenance Item.md`
- `Resource.md`

## Linking Rules

- Use Wikilinks `[[Document Name]]` for internal links
- Cross-folder links: `[[Folder/Document Name]]`
- Deep links: `[[Document Name#Section Heading]]`
- Never create giant navigation pages — use links to build a knowledge graph

## Tagging Convention

Tags are lowercase, kebab-case, max 5 tags per document.

**Categories:**
- Technology: `nextjs`, `typescript`, `prisma`, `turborepo`, `lti-tool`
- Domain: `architecture`, `security`, `testing`, `deployment`, `frontend`, `backend`
- Type: `adr`, `guide`, `reference`, `research`, `runbook`, `concept`, `tool`
- Status: `active`, `archived`, `deprecated`, `draft`
- Project: `project-one`, `project-two`, `project-three`

## Creating New Documents

Follow this sequence:
1. Determine document type and location (Project vs Shared Knowledge)
2. Use the appropriate template from `00 Meta/Templates/`
3. Fill all required frontmatter with current date
4. Write content following structure defined by the template
5. Link to related documents (bidirectional where appropriate)
6. Place in the correct folder

## Validating Created Documents

Before considering a document complete:

- [ ] Frontmatter complete and accurate (all required fields present)
- [ ] Title matches filename (without extension)
- [ ] Structure follows document template
- [ ] All internal wikilinks resolve
- [ ] External links have descriptive text
- [ ] No broken wikilinks
- [ ] Has 1 domain tag and 1 document type tag
- [ ] Code blocks specify language
- [ ] Updated date reflects current date
- [ ] No generic Chinese messages or placeholders

## Archive Process

When content is obsolete or superseded:

1. Move file: `04 Archives/Deprecated/`, `Superseded/`, or `Historical/` as appropriate
2. Change `status` to `archived` or `deprecated`
3. Add link from new/superseding document

**Archive destinations:**
- Deprecated → Obsolete technology, outdated patterns, deprecated tools
- Superseded → Replaced by newer version or consolidated docs
- Historical → Completed reviews, old decisions, old snapshots

## Special Guardrails

- Do not delete content without archiving first
- Do not rewrite technical content for flavor/style only
- Do not create empty documents just to satisfy structure
- Always keep `00 Meta/Templates/` as the authoritative source for document structures
- All documents use English primarily; Persian content is translated/summarized in English
- Frontmatter property order: `type` → `status` → `project` (project-scoped) → `area` → `created` → `updated` → `tags` → additional fields

## Using the reference files

This skill’s core logic lives above; the six reference documents contain the detailed rules. Open them when you need to:

- **references/archive-rules.md** — When you need to archive content (see “Archive Process” above). This file defines the archival workflow and the three destinations (Deprecated, Superseded, Historical) with examples of what belongs in each.
- **references/classification-guide.md** — When you are unsure whether a piece of knowledge belongs in `01 Projects/` or `02 Shared Knowledge/`. Read this guide first; it gives the decision framework and examples that clarify the boundary.
- **references/document-types.md** — When you need to know which frontmatter fields are required for a given document type (project, guide, reference, etc.) or which template to use. This document enumerates every supported type with its required frontmatter and the canonical template.
- **references/linking-conventions.md** — When you are creating or reviewing links. This file defines the three link flavors (simple Wikilink, cross-folder, deep link) and warns against navigation pages; it also gives the preferred styles for headings and anchors so links stay stable.
- **references/tagging-conventions.md** — When you are assigning tags to a new document. This reference lists the controlled vocabularies for technology, domain, type, status, and project tags, and shows how to combine them to stay within the five-tag limit.
- **references/vault-structure.md** — When you are setting up a new vault or auditing an existing one. This document recaps the three-top-level-section layout (`00 Meta/`, `01 Projects/`, `02 Shared Knowledge/`) and explains why each section exists, plus the naming conventions for folders and files inside them.

These references are not optional reading; they are the detailed rules that the skill’s checklists above summarize. Treat the skill as the router and the references as the manuals.