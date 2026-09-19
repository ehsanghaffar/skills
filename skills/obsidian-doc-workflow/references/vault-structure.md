# Vault Structure and Purposes

This document defines the top-level structure of the Obsidian vault and the purpose of each section.

## Top-Level Folder Structure

```
/
├── 00 Meta/              # Documentation system itself
├── 01 Projects/          # Project-specific documentation
├── 02 Shared Knowledge/  # Reusable engineering knowledge
├── 03 Resources/         # External references and research
├── 04 Archives/          # Historical/deprecated content
└── Inbox/                # Temporary capture before classification
```

## Folder Purposes

### 00 Meta

Information about the documentation system itself:

- **Vault Guide** — This document explains the structure and conventions
- **Documentation Standards** — Naming, frontmatter, linking rules
- **Naming Conventions** — File/folder naming rules
- **AI Guidance/** — Instructions for AI agents
  - `Vault Architecture.md` - What AI agents see
  - `Classification Rules.md` - How to place documents
  - `Archive Rules.md` - Archival workflow
  - `Template Usage.md` - Which template for which type
- **Templates/** — Reusable document templates
- **Maintenance/** — Review schedules, cleanup checklists, database views

### 01 Projects

Each substantial project has its own folder with consistent structure.

**Standard project root documents:**
| Document | Filename |
|----------|----------|
| Project Overview | `Project Overview.md` |
| Architecture | `Architecture & Tech Stack.md` |
| Development Guide | `Development Guide.md` |
| API Reference | `Component & API Reference.md` |
| Testing Guide | `Testing Guide.md` |
| Deployment | `Deployment & Infrastructure.md` |
| Maintenance Board | `Maintenance Board.md` |
| Changelog | `Changelog.md` |

**Standard project subfolders:**
| Folder | Used for |
|--------|----------|
| `Architecture/` | Architecture docs |
| `Services/` | Service documentation |
| `Database/` | Database docs |
| `Testing/` | Testing docs |
| `Deployment/` | Deployment docs |
| `Security/` | Security docs |
| `Maintenance/` | Maintenance items |
| `Guides/` | Additional guides |
| `Research/` | Research notes |
| `Operations/` | Runbooks |
| `Archives/` | Archived project docs |
| `Decisions/` | ADRs |

**Key Rule:** If changing the project would make the document obsolete, it belongs in the project. If it remains useful after the project disappears, it belongs in Shared Knowledge.

### 02 Shared Knowledge

Internal engineering knowledge base — reusable across projects.

**Standard domains:**
```
02 Shared Knowledge/
├── Architecture & Patterns/
├── Development/
├── DevOps & Infrastructure/
├── Databases/
├── Security & Privacy/
├── Testing/
├── Tools & Utilities/
├── Design Systems/
├── SEO/
├── Automation/
└── Resources/
```

**Rules:**
- One canonical document per reusable concept
- Avoid project-specific assumptions
- Link to related projects
- Prefer atomic docs over giant reference pages

### 03 Resources

External/reference material:
- **References/** — Personal reference docs (tech stack, skills)
- **External Documentation/** — Vendor docs, papers
- **Research/** — Research notes
- **Links & Sources/** — Important URLs with context

Do not copy large external documents. Create concise notes preserving source, relevance, and related internal knowledge.

### 04 Archives

Preserves history without polluting active docs:

- **Deprecated/** — Obsolete patterns, old tech
- **Superseded/** — Replaced by newer docs (link from new)
- **Historical/** — Completed reviews, old decisions

Prefer archiving over deletion.

### Inbox

Temporary capture area. Classify items during maintenance into Project, Shared Knowledge, Resource, Archive, or Delete.

## Document Types (Frontmatter `type`)

| Type | Purpose | Location |
|------|---------|----------|
| `project` | Project entry point | `01 Projects/{Project}/Project Overview.md` |
| `architecture` | System architecture | `01 Projects/{Project}/Architecture/` or `02 Shared Knowledge/Architecture & Patterns/` |
| `guide` | How-to guides | `01 Projects/{Project}/Guides/` or `02 Shared Knowledge/` |
| `reference` | API/component reference | `01 Projects/{Project}/Component & API Reference.md` |
| `adr` | Architecture Decision Records | `01 Projects/{Project}/Decisions/` |
| `decision` | General decisions | `01 Projects/{Project}/Research/` |
| `research` | Research/analysis notes | `01 Projects/{Project}/Research/` |
| `runbook` | Operational procedures | `01 Projects/{Project}/Operations/` |
| `concept` | Reusable concepts | `02 Shared Knowledge/` |
| `tool` | Tool/utility documentation | `02 Shared Knowledge/Tools & Utilities/` |
| `maintenance` | Maintenance board items | `01 Projects/{Project}/Maintenance/` |
| `changelog` | Changelog entries | `01 Projects/{Project}/Changelog.md` |
| `resource` | External resources | `03 Resources/` |
| `profile` | Personal/profile info | `03 Resources/References/` |

## Database Views (Bases Plugin)

The vault uses the `bases` plugin for structured views. Built-in views created from this vault:

- `Active Projects` — `type = project AND status = active`
- `Open Maintenance` — `type = maintenance AND status = open`
- `Architecture Decisions` — `type = adr`
- `Shared Knowledge Index` — `type = concept OR type = tool`
- `Recent Research` — `type = research ORDER BY updated DESC LIMIT 20`
- `Documents Needing Review` — `updated < date(-90d) AND status = active`
- `Archived Material` — `status = archived OR status = deprecated`

## Languages

All documents use **English** as the primary language. Persian content is translated or summarized in English.