# Document Types and Templates

This document lists all document types, their required frontmatter fields, and which template to use.

## Document Type Reference

| Type | Purpose | Required Frontmatter | Recommended Template |
|------|---------|----------------------|---------------------|
| `project` | Project entry point | `type`, `project`, `status`, `area`, `created`, `updated`, `tags` | `Project Overview.md` |
| `architecture` | System architecture | `type`, `project`, `status`, `area`, `created`, `updated`, `tags` | `Architecture.md` |
| `guide` | How-to guides | `type`, `status`, `area`, `created`, `updated`, `tags` | `Development Guide.md`, `Technical Guide.md` |
| `reference` | API/component reference | `type`, `status`, `created`, `updated`, `tags` | `API Reference.md` |
| `adr` | Architecture Decision Record | `type`, `project`, `status`, `area`, `created`, `updated`, `tags` | `ADR.md` |
| `decision` | General project decisions | `type`, `project`, `status`, `area`, `created`, `updated`, `tags` | `Decision.md` |
| `research` | Research/analysis notes | `type`, `project`, `status`, `area`, `created`, `updated`, `tags` | `Research.md` |
| `runbook` | Operational procedures | `type`, `project`, `status`, `area`, `created`, `updated`, `tags` | `Runbook.md` |
| `concept` | Reusable engineering concepts | `type`, `area`, `status`, `created`, `updated`, `tags`, `related_projects` | `Concept.md` |
| `tool` | Tool/utility documentation | `type`, `area`, `status`, `created`, `updated`, `tags`, `related_projects` | `Tool.md` |
| `maintenance` | Maintenance board items | `type`, `project`, `status`, `area`, `priority`, `assignee`, `estimate`, `created`, `updated`, `tags` | `Maintenance Item.md` |
| `changelog` | Changelog entries | `type`, `project`, `status`, `area`, `created`, `updated`, `tags` | `Changelog Entry.md` |
| `resource` | External resources | `type`, `source`, `status`, `created`, `updated`, `tags` | `Resource.md` |

## Standard Frontmatter Fields

### All Documents
```yaml
---
type: <document-type>
status: active|archived|deprecated
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### Project Documents (additional required)
```yaml
project: "Exact Project Folder Name"
area: frontend|backend|infra|security|testing|devops
```

### Shared Knowledge Documents (additional recommended)
```yaml
area: patterns|frontend|backend|testing|devops
related_projects: ["Project A", "Project B"]
```

### Resource Documents (additional required)
```yaml
source: "URL or citation"
```

### Maintenance Documents (additional required)
```yaml
priority: high|medium|low
assignee: "Name"
estimate: "2h" or "Variable"
```

### Optional Fields
```yaml
tags: [tag1, tag2]
```

## Property Order

All frontmatter should follow this order:

1. `type`
2. `status`
3. `project` (if project-scoped)
4. `area`
5. `created`
6. `updated`
7. `tags`
8. `source` / `related_projects` / `assignee` / `priority` / `estimate` (as applicable)

## Template Example: Project Overview

```
---
type: project
project: "{{PROJECT_NAME}}"
status: active
area: frontend
created: {{DATE}}
updated: {{DATE}}
tags: [{{PROJECT_SLUG}}, project]
---

# {{PROJECT_NAME}} — Project Overview

## What
Brief description of what this project is.

## Why
The problem this project solves and why it exists.

## Status
Current state: active / maintenance / deprecated / archived

## Goals
- Primary goal
- Secondary goals

## Scope
What this project includes.

## Non-Goals
What this project explicitly does not include.

## Key Technologies
- Technology 1
- Technology 2
- Technology 3

## Important Links
- Repository: [URL]
- Deployment: [URL]
- Documentation: [URL]

## Related Projects
- [[Related Project 1]]
- [[Related Project 2]]

## Related Shared Knowledge
- [[Shared Knowledge Concept 1]]
- [[Shared Knowledge Concept 2]]
```

## Template Example: Concept (Shared Knowledge)

```
---
type: concept
area: patterns
status: active
created: {{DATE}}
updated: {{DATE}}
tags: [concept, {{AREA}}]
related_projects: []
---

# {{CONCEPT_NAME}}

## Overview
One-sentence summary of the concept.

## Problem
What problem this concept solves.

## Solution
How this concept works.

## Key Principles
- Principle 1
- Principle 2

## When to Use
- Use case 1
- Use case 2

## When Not to Use
- Anti-pattern 1

## Implementation Guidelines
Guidelines for applying this concept.

## Examples
### Example 1
```typescript
// Code example
```

## Related Concepts
- [[Related Concept 1]]
- [[Related Concept 2]]

## Related Projects
- [[Project 1]]
- [[Project 2]]
```

## Template Example: Maintenance Item

```
---
type: maintenance
project: "{{PROJECT_NAME}}"
status: open
area: maintenance
priority: medium
created: {{DATE}}
updated: {{DATE}}
tags: [{{PROJECT_SLUG}}, maintenance]
assignee: ""
estimate: ""
---

# Maintenance Item: {{ITEM_TITLE}}

## Description
What needs to be done.

## Context
Why this maintenance is needed.

## Phase
Phase 0 / Phase 1 / Phase 2 / Phase 3

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Related Documents
- [[Maintenance Board]]
- [[Related Architecture Document]]
```

## Finding the Right Template

To find the appropriate template for a document type:

1. Open `00 Meta/Templates/` in the vault
2. Look for the template matching the document type
3. If no template exists, create one following the naming convention

**Template naming convention:**
- `{document_type}.md` (e.g., `Architecture.md`, `Tool.md`)
- Use Title Case for filename
- Use kebab-case for the frontmatter `type` field

## Document Type Validation Checklist

Before creating a document:

- [ ] **Type selected correctly** (matches the content's nature)
- [ ] **Location decided** (Project vs Shared Knowledge)
- [ ] **Template file created** from `00 Meta/Templates/`
- [ ] **Frontmatter fields populated** (all required + at least 5 tags)
- [ ] **Date fields use current date** (`YYYY-MM-DD` format)
- [ ] **Original template placeholders removed** (except section-specific ones)

## Common Mistakes

### Frontmatter Errors
- ❌ Missing `type` field
- ❌ Wrong `status` value (`active/archived/deprecated`)
- ❌ Missing `created` and `updated` dates
- ❌ Project documents missing `project` field
- ❌ Shared Knowledge documents missing both `area` and `related_projects`
- ❌ Too many tags (max 5)

### Location Errors
- ❌ Placing project-specific content in Shared Knowledge
- ❌ Creating duplicate Shared Knowledge concepts
- ❌ Keeping obsolete docs in active folders
- ❌ Not using subfolders for organized structure

### Template Errors
- ❌ Not using the official template from `00 Meta/Templates/`
- ❌ Leaving template placeholders unremoved
- ❌ Not matching document type to template structure
- ❌ Adding custom frontmatter fields before required ones
- ❌ Misnaming frontmatter keys (case sensitivity matters)