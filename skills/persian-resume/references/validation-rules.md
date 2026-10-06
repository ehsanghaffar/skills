# Validation Rules

Rules applied by `validate_resume.py` after generation.

## RTL / bidi checks

- Document direction is RTL (`<html dir="rtl">` or DOCX rtl setting)
- Paragraphs flow right-to-left, not left-to-right
- No manually reversed strings (check for common reversed English words)
- No zero-width character hacks (ZWNJ/ZWJ only where meaningful)

## Content checks

- All provided facts present (name, contact, experience entries)
- No invented companies, roles, dates, or metrics
- Dates consistent: one calendar used throughout (Persian or Gregorian)
- Date ranges valid: start ≤ end (or "current" handled)
- English terms intact: JavaScript, Next.js, Django, etc. not transliterated
- URLs and emails readable, unbroken, correct scheme
- Version numbers unchanged: v1.2.3, 16.0.7, etc.

## Typography checks

- Persian font embedded/available
- Body text ≥ 10pt, headings ≥ 14pt
- Line height 1.4–1.8
- Margins 1.5–2.5cm

## Structure checks

- Headings in logical order (h1 → h2 → h3)
- No orphaned headings at page bottom (multi-page)
- Sections not split awkwardly across pages
- Contact info visually separated from main content

## Output checks

- File opens without errors (docx validation, PDF header check)
- Page count matches content (no over/under-compression)
- Text extractable and readable (ATS check)
- Tables: RTL column order, cells correct direction

## Severity

| Level | Meaning | Action |
|-------|---------|--------|
| error | Broken RTL / scrambled content | Regenerate |
| warning | Suboptimal typography / spacing | Fix in next iteration |
| info | Suggestion | Apply if easy |
