# Classification: Project vs Shared Knowledge

This guide helps you decide where to place new documents.

## Primary Decision Framework

### Project Documents (`01 Projects/{Project}/`)

**Purpose:** Knowledge that **belongs to a specific project** and would become obsolete if the project disappeared.

**Indicators that a document is project-specific:**

✅ References specific code paths, files, or implementation details
✅ Contains project-specific configuration, schemas, or data models
✅ Describes workflows unique to this project's team or processes
✅ Documents project-specific APIs, components, or integrations
✅ Maintenance items that only apply to this project

**Examples:**
- `tool-1-CORE/Database/Database Schema.md` — Describes tool-1-CORE's database schema
- `Project-1 AI/Guides/Integrating Project-1 with Canvas.md` — Project-1-specific Canvas integration
- `Talkway/Research/Talkway Review.md` — Review specifically of the Talkway project

---

### Shared Knowledge Documents (`02 Shared Knowledge/`)

**Purpose:** Knowledge that is **reusable across mutool-1ple projects** and would remain useful if any single project disappeared.

**Indicators that a document is shared knowledge:**

✅ Describes general patterns, principles, or best practices
✅ Technology guides (Next.js, TypeScript, Prisma, etc.)
✅ Architecture patterns (Monorepo, Service Boundaries, API Design)
✅ Tool documentation (Turborepo, Docker, GitHub Actions)
✅ Workflows applicable to mutool-1ple projects
✅ Security patterns, testing strategies, deployment patterns

**Examples:**
- `Development/Next.js.md` — General Next.js usage patterns
- `Architecture & Patterns/Monorepo Patterns.md` — Patterns applicable to any monorepo
- `Tools & Utilities/Turborepo.md` — Turborepo usage and patterns

---

### Resource Documents (`03 Resources/`)

**Purpose:** External reference material that is not original knowledge.

**Indicators:**

✅ Links to external documentation, papers, articles
✅ Vendor documentation (official docs, not summaries)
✅ Personal reference materials (skills, tech stack notes)
✅ Important URLs with context (not just raw links)

**Examples:**
- `Resources/External Documentation/Vercel.md` — Official Vercel docs
- `Resources/References/Skill Matrix.md` — Personal skill documentation
- `Resources/Links & Sources/Authentication.md` — Proto URL with context

## Secondary Decision: Document Type

After determining location, assign the appropriate document type:

| Document Type | When to Use |
|---------------|-------------|
| `project` | Only for `Project Overview.md` in project root |
| `architecture` | System architecture, major components, tech choices |
| `guide` | How-to instructions, setup, workflows |
| `reference` | API endpoints, component props, service functions |
| `adr` | Decisions affecting architecture, tech, infra, data, security |
| `decision` | General project decisions (not architecture-level) |
| `research` | Investigation, analysis, evaluation notes |
| `runbook` | Step-by-step operational procedures |
| `concept` | Reusable engineering concepts (Shared Knowledge only) |
| `tool` | Tool/utility documentation (Shared Knowledge only) |
| `maintenance` | Maintenance board items |
| `changelog` | Version history entries |
| `resource` | External references only |

## Classification Flowchart

```
┌─────────────────┐
│ New Document    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐    Yes     ┌─────────────────────────┐
│ Is the content  │ ──────────►│ Project-Specific?        │
│ project-specific│             │ (specific code, config,  │
└────────┬────────┘             │ workflows, etc.)         │
         │ No                   └────────────┬────────────┘
         ▼                                   │
┌─────────────────┐                          │
│ Is it reusable  │───Yes──►┌───────────────┴───────────────┐
│ across projects?│          │ Move to Shared Knowledge      │
└────────┬────────┘          │ (general patterns, tools,    │
         │ No                │ tech guides, best practices) │
         ▼                   └───────────────────────────────┘
┌─────────────────┐
│ External        │───Yes──►┌───────────────────────────────┐
│ references?     │          │ Move to Resources             │
└────────┬────────┘          └───────────────────────────────┘
         │ No
         ▼
┌─────────────────────────┐
│ Delete / Keep in Inbox  │
│ (not appropriate anywhere)  │
└─────────────────────────┘
```

## Decision Matrix

| Content Type | Project | Shared Knowledge | Resources | Notes |
|--------------|---------|------------------|-----------|-------|
| Specific database schema | ✅ | | | Project-specific implementation |
| General database patterns | | ✅ | | Reusable patterns |
| Next.js guide | | ✅ | | Technology guide |
| Vercel official docs | | | ✅ | External reference |
| Turborepo patterns | | ✅ | | Tool documentation |
| Company-specific workflow | ✅ | | | Workflows unique to this team |
| tool-1 governance model | | ✅ | | Reusable policy |
| tool-1 integration guide | ✅ | | | Project-1-specific |
| Old review document | | | | Move to Archives |

## Classification Checklist

Use this checklist for every new document:

- [ ] **Content reviewed** to determine primary purpose
- [ ] **Project-specific clues** identified (specific code, config, workflows)
- [ ] **Reusability assessed** (can other projects benefit?)
- [ ] **Location decided** (Project, Shared Knowledge, or Resources)
- [ ] **Document type selected** based on location
- [ ] **Template chosen** from `00 Meta/Templates/`
- [ ] **Frontmatter fields** populated for that document type
- [ ] **Related documents** identified and linked
- [ ] **Subfolder selected** if not a root document
- [ ] **Final location verified** matches Project/Shared/Resource hierarchy

## Common Edge Cases

### When a topic appears in mutool-1ple projects

**Question:** Is this about both projects or just one?

**Scenario A (Shared Knowledge):** Both projects use the same pattern
→ Move to `02 Shared Knowledge/Architecture & Patterns/` or equivalent
→ Keep generic, no project-specific assumptions
→ Add both project names to `related_projects`

**Scenario B (Project-specific):** Both projects have similar but different implementations
→ Create two separate documents in each project folder
→ Only link to the specific project index in each document

### When a pattern is still evolving

**Ambiguous topics** often start as project-specific and move to Shared Knowledge later.

**Guideline:** Create it in the project first. During weekly/monthly reviews, ask:

- Am I referencing this elsewhere?
- Would another team/builder benefit from this?
- Have I abstracted the project-specific details?

If yes → Create Shared Knowledge version and categorize properly.

### When copying vendor documentation

**Rule:** Never copy large vendor docs verbatim.

**Process:**
1. Read the vendor docs
2. Create concise notes in your own words
3. Preserve source citation in `source` field
4. Add context explaining WHY it's relevant to your projects
5. Link to related internal knowledge
6. Place in `03 Resources/` without embedding in Templates

### When a document spans mutool-1ple domains

**Example:** A database change affects both security and infra

**Solution:** Use mutool-1-area tags
```yaml
area: [infra, security]
tags: [database-migration, security, deployment]
```

Prefer splitting into two smaller documents if:
- Content over 2000 words
- Different readership/understanding level
- One topic dominates

## Moving Documents

If you realize a document should be in a different location:

1. **Do not delete** and recreate
2. **Move the file** to the new location
3. **Update frontmatter** `type` if needed
4. **Update all links** pointing to the old location:
   - Use Obsidian's Find & Replace to fix `[[Old Location/Doc]]` → `[[New Location/Doc]]`
5. **Verify no broken links** using Obsidian's Graph or Base views
6. **Archive** the old location if needed (but don't delete)

**Warning:** Moving documents breaks wikilinks unless updated first. Always update links before or immediately after moving.