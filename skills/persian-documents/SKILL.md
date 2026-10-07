---
name: persian-documents
description: Generate production-quality Persian documents with correct RTL layout, bidirectional text handling, and professional typography. Use this skill whenever the user asks to create Persian documents — reports, letters, articles, technical documentation, resumes, PDFs, Word documents, or any document containing Persian text mixed with English, numbers, code, URLs, or other LTR content. Also trigger when the user asks to "fix RTL" or "fix direction" in a Persian document, or when a document needs to be regenerated because Persian text rendered incorrectly. This skill is NOT just for writing Persian prose — it is for producing documents where the final rendered output is typographically correct, structurally sound, and ready for real-world use.
version: 0.1.1
---

# Persian Document Generator

Generate professional Persian documents that render correctly as RTL, not just Persian text inserted into an LTR layout.

## When to use this skill

- User asks for any Persian document (PDF, DOCX, report, letter, article, technical doc, resume)
- Document contains mixed Persian/English content
- Document contains numbers, URLs, code, or technical terms alongside Persian text
- User reports that Persian text rendered incorrectly (reversed, scrambled, wrong direction)
- User needs tables, lists, headers/footers, or page layout in a Persian document

## Core principle

Persian document generation is a **RTL and bidirectional text rendering problem**, not simply writing Persian text. The final rendered document — not the source text — is the judge of correctness.

**Never:**
- Reverse strings manually to "fix" RTL
- Rely on right-alignment alone to make a document RTL
- Assume Unicode text automatically guarantees correct rendering
- Insert arbitrary spaces or zero-width characters as visual hacks

**Always:**
- Use logical text order (the order a reader reads, not the order it appears visually)
- Let the document format handle directionality through proper markup/structure
- Validate the final rendered output, not just the source text

## Document generation approach

### Step 1: Determine the output format

| Format | Tool | Best for |
|--------|------|----------|
| DOCX | `scripts/generate_docx.py` | Editable Word documents, formal letters, reports |
| PDF | `scripts/generate_pdf.py` | Finalized documents, print-ready, shared output |
| Markdown | Direct | Drafting, simple articles, notes |

### Step 2: Understand the content structure

Before generating, identify:
- Document type and required sections
- Mixed-direction elements (English terms, URLs, code, numbers)
- Table structure and column content types
- List types (ordered/unordered, nested)
- Header/footer requirements
- Page layout needs (margins, orientation)

### Step 3: Generate with proper RTL structure

Use the appropriate script with RTL-aware settings. The scripts handle:
- Paragraph direction and alignment
- Table direction and cell alignment
- Mixed-direction text run ordering
- Font selection for Persian/Latin rendering
- Number rendering (Persian vs. Latin numerals)

### Step 4: Validate the output

After generation, check:
- Text flows right-to-left
- Mixed content reads naturally (English words not reversed)
- Numbers and version strings are intact
- Tables have correct column order
- Lists have correct bullet/number placement
- Headers/footers follow document direction

## RTL and bidirectional text rules

### Logical order, not visual order

Persian text must be stored and processed in logical order (the order characters are typed and read), not visual order (the order they appear on screen). The document renderer handles the visual display.

**Correct:** The text "سلام دنیا" is stored as سلام دنیا (logical order)
**Wrong:** Reversing to "ادین‌مالس" or manually rearranging characters

### Mixed Persian and English

When Persian and English appear together, each runs in its own direction within the same paragraph. The document format handles this — the model must not try to rearrange characters.

Examples of correct mixed content:
- `نسخه Next.js 16.0.7 منتشر شد.`
- `API: https://api.example.com/v1/users`
- `npm install @tanstack/react-query`
- `ایمیل پشتیبانی: hello@example.com`

In all cases, the Persian and English each maintain their own direction. The English is not reversed, and the Persian is not reordered.

### Numbers

- Persian numerals (۰۱۲۳۴۵۶۷۸۹) for Persian text contexts
- Latin numerals (0123456789) for code, versions, IDs, URLs, and technical values
- Never reverse or reorder numbers because of RTL context
- Currency symbols stay with their values: `$1,299.99` not `99.95$1,299`

### Punctuation

- Persian punctuation marks (، ؛ ؟ ! « ») stay in their correct positions
- Latin punctuation in mixed contexts stays Latin
- The document renderer handles placement — the model must not manually insert/remove spaces around punctuation

### ZWNJ and character shaping

- Preserve meaningful ZWNJ usage (کتاب‌ها، می‌خواهم)
- Do not add or remove ZWNJ arbitrarily
- Persian characters must be properly shaped (joined/non-joined forms)
- Avoid incorrect ي/ی or ك/ک substitutions — use the form appropriate to the context

## Tables

Tables in Persian documents must have:
- RTL table direction (columns flow right-to-left)
- Column alignment matching content type (right-aligned for Persian text, left for English, center for numbers)
- Correct cell content direction (mixed content stays logical)
- Header row direction matching table direction

## Lists

- Unordered lists: bullets on the right, text flows RTL
- Ordered lists: numbers on the right, text flows RTL
- Nested lists: maintain direction at each level
- List items with mixed content: each item follows the same direction rules as paragraphs

## Document structure

Professional Persian documents include:
- Title page or document title with proper alignment
- Headings that follow RTL direction
- Paragraphs with correct alignment and spacing
- Lists with proper bullet/number placement
- Tables with RTL column order
- Headers and footers with correct direction
- Page numbers (typically right-aligned or centered for RTL)
- Page breaks where needed for section separation

## Quality checklist

Before finalizing any document, verify:

- [ ] Text flows right-to-left throughout
- [ ] English words and terms are not reversed or scrambled
- [ ] URLs, email addresses, and file paths are intact and readable
- [ ] Version numbers, IDs, and technical values are unchanged
- [ ] Numbers render correctly (Persian or Latin as appropriate)
- [ ] Tables have correct column order and cell alignment
- [ ] Lists have correct bullet/number placement
- [ ] Headers/footers follow document direction
- [ ] Fonts support Persian glyphs (avoid missing-character boxes)
- [ ] ZWNJ usage is preserved where meaningful
- [ ] Page breaks don't split content awkwardly
- [ ] Mixed-direction sentences read naturally
- [ ] Code blocks and technical content remain readable

## References

- [Persian typography rules](references/persian-typography.md) — Detailed guidance on Persian/Arabic typography, ZWNJ usage, character forms, and common Unicode pitfalls
- [Document generation patterns](references/document-patterns.md) — Patterns for common document structures (reports, letters, technical docs, resumes)

## Scripts

- `scripts/generate_docx.py` — Generate RTL-aware Word documents with mixed-direction support
- `scripts/generate_pdf.py` — Generate PDFs with correct Persian text shaping and RTL layout
- `scripts/validate_doc.py` — Validate rendered documents for RTL correctness and common issues
