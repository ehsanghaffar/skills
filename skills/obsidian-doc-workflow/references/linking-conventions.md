# Linking Conventions

This document defines how to link documents in this vault.

## Primary Linking Mechanism: Wikilinks

All internal links use Obsidian's wikilink syntax: `[[Document Name]]`.

### Basic Wikilinks

**Simple link:**
```
[[Architecture & Tech Stack]]
```

Displays as: `Architecture & Tech Stack` (using document title)

### Cross-Folder Links

Link to documents in other top-level sections:

```
[[01 Projects/Project-1/Architecture & Tech Stack]]
[[02 Shared Knowledge/Development/Next.js]]
[[03 Resources/External Documentation/Vercel]]
```

**Best practice:** Use canonical folder structure rather than creating shortcuts like `[[Project-1]]` which may become outdated if project names change.

### Deep Links

Link to specific sections within a document:

```
[[Project Overview#Goals]]
[[Architecture & Tech Stack#Data Flow]]
```

**Rules:**
- Section heading must match exactly (case-sensitive)
- No spaces in section name (use hyphens/replacement)
- Only link to canonical sections, not auto-generated sections

**Example:** If section heading is `## Goals`, link with `[[Document#Goals]]`, not `[[Document#goals]]`

### Custom Display Text

Override link display text when needed:

```
[[01 Projects/Project-1/Architecture & Tech Stack|tool integration]]
```

Displays as: `tool integration`

**When to use custom display:**
- Linking from a list where the document name alone is ambiguous
- The document name is too long for context
- Need to distinguish between similar-named documents

```
[[02 Shared Knowledge/Architecture & Patterns/API Design|API Design]]
```

Displays as: `API Design` (instead of `API Design`)

### Duplicate Document Links

When linking to concept appearing in mutoolple places:

```
[[Architectural Decision/External tool Provider]

This links to a single canonical location across the knowledge base.
```

**Best practice:** Keep a canonical link in the main sections; duplicate the link elsewhere with aliases if needed.

## External Links

Use Markdown links for URLs outside the vault:

```
[Vercel Pricing](https://vercel.com/pricing)
[Prisma Documentation](https://www.prisma.io/docs)
```

**Rules:**
- Use descriptive link text (not `here`, `click here`, `link`)
- Include context in the title
- Include the URL (another place to find if link title is unclear)

**Bad:**
```
[Read more here.](https://example.com/pricing)
```

**Good:**
```
[Comparison with other tool providers](https://example.com/comparison)
```

## Backlinks

Obsidian automatically manages backlinks for you. Do **not**:

- ❌ Generate backlinks manually
- ❌ Maintain backlink sections manually (e.g., `### See Also`)
- ❌ Update backlinks when moving documents

Instead:
- Use the Graph view to discover connections
- Use the Base plugin "Backlinks" view when available
- Trust that your wikilinks are enough to build a cross-referenced knowledge graph

## Link Structure Guidelines

### Canonical Locations

**Project Overview** is the canonical entry point for projects. Other docs in the project should link from there:

```
## Related Projects
- [[01 Projects/tool-CORE/tool-CORE Project Overview]]
- [[01 Projects/Talkway/Talkway Project Overview]]
```

### Bidirectional Links

For important relationships, link both ways when appropriate:

```
[[Architecture & Patterns/Authentication Patterns]]

In the Authentication Patterns doc, add:
## Related Projects
- [[01 Projects/Project-1]]
- [[01 Projects/tool-CORE]]
```

### Category Groups

For Organization (e.g., Architecture, Database), link the category and subcategories:

```
## Architecture
- [[Architecture & Patterns/Monorepo Patterns]]
- [[Architecture & Patterns/Service Boundaries]]
- [[Architecture & Patterns/API Design]]
```

### No Giant Navigation Pages

Avoid:

❌
```
## Architecture
- [Architecture & Patterns/Intro](related/Architecture%20and%20Patterns/Intro.md)
- [Architecture & Patterns/API Design](related/Architecture%20and%20Patterns/API%20Design.md)
- [Architecture & Patterns/Caching Patterns](related/Architecture%20and%20Patterns/Caching%20Patterns.md)
- ... and 20 more
```

✅ Instead, use concise category groups and let the Graph view connect content.

## Common Link Forms

### From Project Overview

```
## Key Technologies
- [[02 Shared Knowledge/Development/Prisma]]
- [[02 Shared Knowledge/Development/Turborepo]]
- [[02 Shared Knowledge/DevOps & Infrastructure/Docker]]

## Architecture
- [[Architecture & Patterns/Service Boundaries]]
- [[Architecture & Patterns/Error Handling]]
```

### From Architecture Document

```
## Related Projects
- [[01 Projects/Project-1/Project-1 Project Overview]]
- [[01 Projects/tool-CORE/tool-CORE Project Overview]]

## Related Shared Knowledge
- [[Architecture & Patterns/Authentication Patterns]]
- [[02 Shared Knowledge/Testing/Testing Strategy]]
```

### From Shared Knowledge Concept

```
## Related Concepts
- [[Architecture & Patterns/Service Boundaries]]
- [[Architecture & Patterns/API Design]]

## Related Projects
- [[01 Projects/Project-1/Project-1 Project Overview]]
- [[01 Projects/tool-CORE/tool-CORE Project Overview]]
```

**Pattern:** Concepts should link to where they might be applied.

### From Maintenance Item

```
## Related Documents
- [[Maintenance Board]]
- [[Memory Handling Implementation]]
- [[Database Migration Guide]]
```

## Backlink Optimization Basics

**Periodically (monthly/quarterly):**
- Check Graph view for floating islands (documents with no links in/out)
- Add at least one link to or from these documents
- Do NOT force unnatural linking; use the content to justify

**Tools:**
- Graph view in Obsidian
- Base plugins may have "Backlinks" view
- Wikilinks are self-maintaining; existing links require no action

## Link Verification

Use this checklist before considering content complete:

- **No broken wikilinks**
  - Use Obsidian's "Backlinks" view or Graph view
  - Fix `[[Document]]` when document doesn't exist or name has changed

- **External links have descriptive text**
  - Avoid `[click here](url)`
  - Use `[Context](url)`

- **No duplicate link clutter**
  - Test unique, meaningful grouping in navigation sections

- **Deep links point to canonical sections**
  - Use `[[Document#Canonical Section]]` not `[[Document#Auto-generated Section]]`

- **Links improve discoverability**
  - Link relationship for searchability, don't link just to fill structure

## Linking to Projects

Can you add uppercase filename?

No. Use canonical names from Vault Structure. The proper format:
```
[[01 Projects/Project-1/Project-1 Project Overview]]
```

### Linking to ADRs

Link ADRs in two contexts:

1. From Architecture documents:
```markdown
Decisions were documented in:
- [[01 Projects/Project-1/Decisions/ADR-3-Vercel-for-Hosting]]
- [[01 Projects/Project-1/Decisions/ADR-5-tool-1-3-Middleware]]
```

2. From Shared Knowledge ADR index (if exists):
```markdown
[[Architecture & Patterns/Monorepo Patterns]]
```

## Linking to Resources

Concise links serve as pointers to external content:

```
[Prisma ORM Documentation](https://www.prisma.io/docs)
[Stripe API Reference](https://stripe.com/docs/api)
```

**Add context in navigation sections, not forced links.**

## Section Linking Template Pattern

In many docs, you'll repeat this pattern:

```
## Related Topics
- [[About auth]]
- [[Auth flow in Project-1]]
- [[OAuth 2.0 token refresh]]
```

**Pattern:** Mix general concepts, project-specific flows, and detailed implementations.

**Key:** Explain WHY you link to each as part of content context:

```
## Authentication Flow
This document describes the OAuth 2.0 code flow for Project-1.

## Related Topics
- [[About OAuth 2.0]] — General progress overview
- [[Auth flow in Project-1]] — Project-specific implementation
- [[OAuth 2.0 token refresh]] — Maintenance procedures
```