# Archive Rules

This document defines the archival workflow for the vault.

## Archive Structure

```
04 Archives/
├── Deprecated/     # Obsolete patterns, old technology, deprecated tools
├── Superseded/     # Replaced by newer documents with forward links
└── Historical/     # Completed reviews, old decisions, snapshots
```

## When to Archive

### Move to `Deprecated/`

Archive when content is obsolete or wrong:

- Technology no longer used (e.g., MongoDB.md if project moved to PostgreSQL)
- Patterns superseded by better/approved approaches
- Tools no longer maintained or replaced by newer tools
- Security practices that are now insecure
- Outdated documentation moved to newer docs

**Examples:**
- `Old Auth Implementation.md` — Old JWT implementation replaced with OAuth2
- `MongoDB Guide.md` — Project migrated from MongoDB to PostgreSQL
- `V1 API Documentation.md` — GraphQL API replaced REST API

### Move to `Superseded/`

Archive when content is periodically replaced:

- Document replaced by newer version
- Major rewrite with new structure
- Consolidated multiple docs into one canonical doc
- **Always** add link from new document to superseded version

**Example:**
```
04 Archives/Superseded/
├── Old Architecture Doc.md
├── V1 Testing Guide.md
├── AAD Integration for Generations.md (moved to SSO migration)
```

### Move to `Historical/`

Archive when content is complete and no longer guide:

- Completed project reviews
- Old decisions (ADRs that are no longer relevant)
- Snapshots of project state at a point in time
- Completed maintenance boards
- Cleanup task summaries

**Example:**
```
04 Archives/Historical/
├── Peer Review for Tutorify AI.md
├── ADR-Old-Signature-Based-OAuth.md
├── Tutorify AI v0.1 Snapshot.md
└── LTI-CORE Milestone 1 Summary.md
```

## Archive Process Steps

### Step 1: Verify Archive Decision

Before moving anything, verify:

- Confirmed content is truly obsolete/superseded
- No active links depend on this location (check in Obsidian Graph)
- Replacement document exists (for Superseded only)
- Researched search results don't reference this content elsewhere

**Useful commands (for testing; do NOT include in vault):**
- `grep -r "Archived Document" vault/01 Projects/Project 1/` — Check for active references
- `grep -r "OldAuthImplementation" vault/01 Projects/Project 1/` — Check usage

**Do NOT perform these in production; do only in dev/test:** Use Obsidian's Graph view or "Backlinks" view (if available) instead.

### Step 2: Move File

Move to appropriate archive folder:

```bash
mv "01 Projects/Project 1/01b Old Implementation.md" "04 Archives/Deprecated/Old Implementation.md"
```

**Rules:**
- Preserve original filename (do not rename)
- Do NOT move project root documents (Overview, Architecture, etc.)
- Move entire subfolders for project docs if appropriate

### Step 3: Update Frontmatter

Change status in frontmatter:

For Historical/Superseded:
```yaml
status: archived
```

For Deprecated:
```yaml
status: deprecated
```

**Do NOT delete or modify `status` field; update it instead.**

### Step 4: Add Link from Replacement

In the new/superseding document, add a note:

```markdown
> **Superseded**: [[04 Archives/Superseded/Old Architecture Implementation.md]] — Previous version
```

Or for deprecated tech:
```markdown
> **Archived**: [[04 Archives/Deprecated/Old MongoDB Setup.md]] — Replaced by PostgreSQL setup
```

**Best practice:** Add it as a collapsible block with proper styling in Markdown:

```markdown
> **Superseded content**

> **Archived**: [[04 Archives/Superseded/Old Database Schema.md]]

> This content is superseded by the current database architecture documented in [[01 Projects/Tutorify AI/Architecture/Current Database Design]]
```

### Step 5: Update Links (if needed)

- Check for broken links pointing to old location
- Update any index/navigation documents manually (use Obsidian's Find & Replace with caution)
- Do NOT alter content beyond linking/renaming

**Use Obsidian's Find & Replace feature for bulk re-linking if needed:**
- Find: `[[Old Path/Document]]`
- Replace with: `[[New Path/Document]]`

## What NOT to Archive

### Never Archive

- Active project documentation
- Current Shared Knowledge concepts
- Active maintenance items
- Documentation with `status: active` that are still referenced in Graph

### Never Delete

- **Never delete** content — always archive first
- Even "obvious" trash may have historical value
- If truly disposable (exact duplicates, temp notes), document reason then archive, don't delete directly

## Specific Rules by Content Type

### Project Documents

| Document Type | Archive Destination | When |
|---------------|---------------------|------|
| Project Overview | Never archive | Update instead |
| Architecture | Superseded/ | When replaced by new architecture |
| Guides | Superseded/ | When guide structure changes |
| Research | Historical/ | When investigations complete |
| Maintenance Board | Historical/ | After project review complete |
| Changelog | Never archive | Append-only, never move |

**Flow:** Project Review → Archive reviews to Historic/ → Archive old docs to Superseded/ → Update Project Overview

### Shared Knowledge

| Document Type | Archive Destination | When |
|---------------|---------------------|------|
| Concepts | Deprecated/ | When pattern obsolete |
| Tools | Deprecated/ | When tool no longer used or replaced |
| Workflows | Superseded/ | When replaced by new workflow |

### Resources

| Document Type | Archive Destination | When |
|---------------|---------------------|------|
| External docs | Historical/ | When no longer relevant |
| Personal references | Historic/ or Active | Convert to Shared/ if reusable |

### ADRs (Architecture Decision Records)

| Type | Archive Destination | When |
|------|---------------------|------|
| Accepted ADRs | Keep in place (Decisions/) | Never move |
| Superseded ADRs | Keep in place (Decisions/) | Update status to `superseded`, keep in place |
| Rejected ADRs | Keep in place (Decisions/) | Keep for reference usage |

**ADR-specific rules:**
- Do NOT archive accepted ADRs into Archives/ folder
- Superseded ADRs remain in the same location (Decisions/) with `status: superseded`
- Add link from new ADR to superseded ADR for continuity

## Bulk Archive Operations

When archiving multiple related documents:

1. Create archive folder if needed:
   ```
   04 Archives/Historical/Project 1/
   ```

2. Move all related files:
   ```
   mv 01\ Projects/Project 1/Phase\ 1\ Review.md 04\ Archives/Historical/Project 1/
   mv 01\ Projects/Project 1/Phase\ 2\ Review.md 04\ Archives/Historical/Project 1/
   mv 01\ Projects/Project 1/Phase\ 3\ Review.md 04\ Archives/Historical/Project 1/
   ```

3. Create an index document:
   ```
   04 Archives/Historical/Project 1/Peer\ Review\ Index.md
   ```

   Index content:
   ```markdown
   # Peer Review Index

   This folder contains completed peer reviews for Project 1.

   ## Reviews
   - [[Phase 1 Review]] — Initial review (completed Q2 2026)
   - [[Phase 2 Review]] — Architecture review (completed Q3 2026)
   - [[Phase 3 Review]] — Performance review (completed Q4 2026)

   ## Context
   These reviews archived before the project initial implementation was complete. References in active docs link back here for historical context.
   ```

4. Add link from project's Archives/ folder or relevant document:
   ```markdown
   ## Archives
   - [[04 Archives/Historical/Project 1/Peer Review Index]]
   ```

## Restoring from Archive

If archived content becomes relevant again:

1. Move back to active location (same path as original)
2. Update `status` to `active` or `deprecated` (remove `archived`)
3. Update `updated` date:
   ```yaml
   updated: 2026-09-19  # Current date
   ```
4. Review and update content as needed
5. Add links from related documents back to this location

## Archive Views

The `bases` plugin provides views for managing archives:

**Archived Material view:**
- Filters: `status = archived OR status = deprecated`
- Useful for: Quarterly reviews, identifying restore candidates

**Usage:**
- Open Archive Material view in Obsidian
- Periodically (monthly/quarterly) for cleanup or re-evaluation
- Mark items for restoration or permanent deletion based on re-evaluations

## Verification Checklist

Before archiving any content:

- [ ] Okay to remove from active vault or will it have value later?
- [ ] Verified no active links depend on this location
- [ ] Replaced document exists (for Superseded)
- [ ] Replacement document linked to archived version
- [ ] Archives folder exists (`Deprecated/`, `Superseded/`, `Historical/`)
- [ ] Frontmatter `status` updated to appropriate value
- [ ] Project Overview reflects current status (do not archive Project Overview)
- [ ] ADRs updated correctly (accepted > keep, superseded > keep with `superseded`)
- [ ] Files moved, not renamed

## Archival Tempo

**Frequency:**
- **Weekly:** Review Inbox, classify and archive
- **Monthly:** Rescrape Archive Material view, re-evaluate status
- **Quarterly:** Complete content cleanup, consolidate duplicate archives
- **Per Project:** Archive Maintenance Boards after reviews

**Granularity:**
- Archive frequently to keep main vault clean (weekly inbox review)
- Consolidate slowly to avoid too many small archival folders (monthly)
- Re-evaluate quarterly for potential restoration

**Policy:**
- Archival > Deletion
- Keep historical contiguity
- Always preserve forward references
- Document archival decisions explicitly for future cross-reference