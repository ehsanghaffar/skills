# Tagging Conventions

This document defines the tagging rules for the vault.

## Tag Format

- **Lowercase** — No uppercase characters anywhere
- **Kebab-case** — Hyphens only, no spaces, underscores, or special characters
- **No special characters** — Only `a-z`, `0-9`, `-`
- **Example format:** `nextjs`, `api-design`, `testing-strategy`

## Tag Categories

### Technology Tags

Used for specific technologies or tools. Prefix by technology name only (no category prefix for tech).

| Technology | Common Tags |
|------------|-------------|
| Next.js | `nextjs`, `nextjs-14`, `nextjs-15` |
| TypeScript | `typescript` |
| React | `react` |
| Prisma | `prisma` |
| Suno AI | `suno` |
| LTI | `lti`, `lti-1.3`, `lti-2.0` |
| Slack | `slack` |
| Telegram | `telegram` |
| Twitter/X | `x`, `twitter` |
| GitHub | `github` |
| Vercel | `vercel` |
| Docker | `docker` |
| Kubernetes | `kubernetes` |
| PostgreSQL | `postgresql` |
| MongoDB | `mongodb` |
| Redis | `redis` |
| Turborepo | `turborepo` |
| Nx | `nx` |
| pnpm | `pnpm` |

**Tags per technology:** Don't tag every version separately. Use main tag (`typescript`) rather than `typescript-4-9` and `typescript-5-x`.

### Domain Tags

Used for general domains/areas. These are **not** technology-specific.

| Domain | Common Tags |
|--------|-------------|
| Architecture | `architecture` |
| Security | `security` |
| Testing | `testing` |
| Deployment | `deployment` |
| Development | `development` |
| Performance | `performance` |
| Scalability | `scalability` |
| Reliability | `reliability` |
| Monitoring | `monitoring` |
| Debugging | `debugging` |
| API Design | `api-design` |
| Database | `database` |
| Frontend | `frontend` |
| Backend | `backend` |
| DevOps | `devops` |
| Operations | `operations` |

### Document Type Tags

Used to identify the type of document in the archive, for filtering and browsing.

| Document Type | Tags |
|---------------|------|
| Architecture Decision Record | `adr` |
| Guide | `guide` |
| Reference | `reference` |
| Research | `research` |
| Runbook | `runbook` |
| Concept | `concept` |
| Tool | `tool` |
| Maintenance item | `maintenance` |
| Project | `project` |
| Change log | `changelog` |
| Resource | `resource` |

### Status Tags

Used for document lifecycle status. Only used in archives.

| Status | Tags |
|--------|------|
| Active | `active` |
| Archived | `archived` |
| Deprecated | `deprecated` |
| Draft | `draft` |

### Project Tags

Use project slugs (lowercase, kebab-case) to identify projects.

| Project | Tag |
|---------|-----|
| Talkway | `talkway` |
| Farsi UI | `farsi-ui` |
| MLBB Hub | `mlbb-hub` |

## Tag Selection Logic

### Minimum Tags

Every document must have:
- 1 domain tag (e.g., `architecture`, `security`, `testing`)
- 1 document type tag (e.g., `adr`, `guide`, `concept`)

### Maximum Tags

**Maximum 5 tags per document.**

### Tag Priority

Use this hierarchy when selecting tags:

1. **Domain tags** (Domain > Type > Technology)
   - Example: `testing` is better than `testing-strategy` for broad coverage
   - Example: `architecture` is better than `monorepo-architecture`

2. **Technology tags** (Secondary)
   - Use sparingly. Only add if the specific technology is central to the document
   - Example: Use `prisma` in a database guide about Prisma
   - Don't use `prisma` just to document Prisma as a tool unless that's the entire focus

3. **Document type tags** (Always final)
   - Always include for better navigation in Base views

4. **Status tags** (Only in archives)
   - `active` for current documents (do not tag active docs with `archived` or `deprecated`)
   - `archived`, `deprecated`, `draft` only for documents that deserve these states

5. **Project tags** (Project docs only)
   - Only for project-scoped documents
   - Don't add project tags to Shared Knowledge unless the concept is specifically about that project

## Tag Examples

### Project Overview Document

```yaml
tags: [frontend, project, active]
```

**Rationale:**
- Domain: `frontend`
- Type: `project`
- Technology: `project-ai`
- Status: `active`

**Better:**
```yaml
tags: [project-ai, architecture, project, active, frontend]
```
(Added `architecture` since it's about system architecture)

### Shared Knowledge Concept

```yaml
tags: [api-design, patterns, concept, typescript, nextjs]
```

**Rationale:**
- Domain: `api-design`
- Type: `concept`
- Technology: `typescript`, `nextjs` (both central to the concept)

### Architecture Decision Record

```yaml
tags: [adr, architecture, security, postgresql, dependent-type-pg]
```

**Rationale:**
- Type: `adr`
- Domain: `architecture`, `security`
- Technology: `postgresql`, `dependent-type-pg`

### Research Note

```yaml
tags: [research, testing, nextjs, performance]
```

**Rationale:**
- Type: `research`
- Domain: `testing`, `performance`
- Technology: `nextjs`

### Maintenance Item

```yaml
tags: [tool-core, maintenance, high, backend]
```

**Rationale:**
- Type: `maintenance`
- Project: `tool-core`
- Status: `high`
- Domain: `backend`

### Resource Document

```yaml
tags: [resource, documentation, vercel]
```

**Rationale:**
- Type: `resource`
- Domain: `documentation`
- Technology: `vercel`

## Bad Tagging Examples

### Too Generic

❌ Bad: `note` or `info` or `stuff`
✅ Good: `architecture`, `testing`, `api-design`

❌ Bad: `nextjs` when your document is about app performance in Next.js
✅ Good: `performance`, `nextjs` OR `testing`, `performance`

❌ Bad: `project` when your document is a project Overview
✅ Good: `project`, `frontend`, `architecture` (include domain and type)

### Too Niche

❌ Bad: `nextjs-14` when the concept applies to Next.js 13 and 15 too
✅ Good: `nextjs` or `nextjs-13-15`

❌ Bad: `project-ai-v2` when the concept applies to both v1 and v2
✅ Good: `project-ai` only

### Too Organized

❌ Bad: `project:architecture:testing` (format violations)
✅ Good: Use plain tags like `project`, `architecture`, `testing`

### Wrong Case

❌ Bad: `Project` or `APP-DESIGN` (uppercase or underscores)
✅ Good: `project`, `app-design`

### Exceeds Limit

❌ Bad: 6 or more tags (e.g., `api-design`, `nextjs`, `frontend`, `typesafe`, `typescript`, `architecture`)
✅ Good: Reduce to 5: `api-design`, `nextjs`, `frontend`, `typesafe`, `architecture`

## Tag-Document Relationship Mapping

The Base plugin creates views based on tags. Ensure your tags align with:

**Active Projects view筛选条件：**
- `type = project`
- Status tags: `active`

**Documents Needing Review view筛选条件：**
- `updated < date(-90d)`
- Status tags: `active`

**Archived Material view筛选条件：**
- Status tags: `archived` or `deprecated`

**Shared Knowledge Index view筛选条件：**
- `type = concept` OR `type = tool`

## Tag naming standards by category

| Category | Naming Rule | Example |
|----------|-------------|---------|
| Technology | Lowercase, single word | `prisma`, `docker` |
| Domain | Lowercase, single word | `security`, `deployment` |
| Type | Type document field | `adr`, `guide`, `concept` |
| Status | Field `status` | `active`, `archived`, `deprecated` |
| Project | Project slug | `project-ai`, `tool-core` |

**Contradictory standards:** Domain tags match document area (e.g., `architecture` matches `Architecture & Patterns`), and type tags match frontmatter `type`. This consistency improves filtering in Base views.