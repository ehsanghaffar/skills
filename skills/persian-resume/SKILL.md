---
name: persian-resume
description: >-
  Generate professional Persian (RTL) resumes/CVs that render correctly with mixed
  Persian-English content. Use this skill whenever the user asks to create,
  rewrite, polish, or transform a Persian resume/CV, or when a resume contains
  mixed Persian and English/technical content that must remain readable and
  correctly ordered in RTL. Also trigger when the user provides career info in
  any language and wants a professional Persian CV, or asks to fix RTL/bidi
  issues in a Persian resume. This skill is NOT for general Persian documents —
  use persian-documents for reports, letters, articles, and technical docs.
version: 0.1.0
---

# Persian Resume / CV Generator

Turn career information into a polished, professional Persian RTL resume or CV
that looks typeset, not generated. Supports both creating from raw info and
transforming existing content.

## When to use this skill

- User asks to write, rewrite, or polish a Persian resume/CV
- Resume mixes Persian and English (tech terms, company names, URLs)
- User provides career info in any language and wants a Persian CV
- Fixing RTL/bidi issues in an existing Persian resume
- Output must be PDF or DOCX for real job applications
- **Not for**: reports, letters, articles — use `persian-documents` instead

## Core principle

A resume is a **bidirectional document**, not Persian text in a layout. The
rendered output — not the source text — is the judge of correctness.

**Never:**
- Reverse strings manually to "fix" RTL
- Rely on right-alignment alone for RTL
- Assume Unicode text guarantees correct rendering
- Insert arbitrary ZWNJ/spaces as visual hacks

**Always:**
- Use logical text order (reading order), let the renderer handle display
- Keep English/Latin runs intact inside RTL paragraphs
- Preserve English technical terms in their standard spelling
- Validate the rendered output, not just the source text
- Make the PDF/DOCX the source of truth for directionality

## Resume structure

Choose sections based on the candidate's actual info. Do not force irrelevant
sections.

```
[Name + Professional title]
[Contact row — RTL, with LTR URLs/emails intact]
[Professional summary — optional, 2-4 lines max]
[Experience]
  [Company — Role — Dates]
  • Achievement/outcome (not responsibility list)
[Projects]        (if relevant to target role)
[Education]
[Skills]          (structured categories, not a dump)
[Certifications / Languages / Awards]  (only if present and meaningful)
```

## Information hierarchy

1. Identity + professional positioning (name, title, summary)
2. Current/recent experience
3. Strongest relevant skills
4. Major achievements with outcomes
5. Education + additional info

## Career history rules

Per entry:
- Company name, job title, employment type, location
- Start date, end date (or "current")
- 2-5 bullets: responsibility → action → outcome → metric
- Technologies used

Dates — keep one calendar throughout:
- Persian calendar preferred for Iranian candidates (`۱۴۰۲–۱۴۰۵`, `۱۳۹۹–اکنون`)
- Gregorian acceptable for international roles (`2024–2026`, `2021–Present`)
- Mixed formats: pick one and normalize, note the choice

## Achievement-oriented writing

Prefer: action + measurable outcome over responsibility lists.

**Good:**  `راه‌اندازی سرویس → کاهش زمان پاسخ ۸۰۰ms به ۱۲۰ms (۸۵٪)`
**Avoid:** `مسئولیت مدیریت تیم و نگهداری سرویس‌ها`

Never invent metrics, companies, technologies, dates, or responsibilities.
When info is missing, preserve known facts and leave gaps rather than fill them.

## Professional summary

2-4 lines reflecting real background, communicating professional positioning,
tailored to the target role when provided. Avoid generic buzzwords
("团队玩家", "چسبنده", "کار-hard"). Prioritize relevant expertise.

## Skills structure

Group and prioritize — never an unorganized dump:

- Programming languages
- Frameworks & libraries
- Frontend / Backend / DevOps (as relevant)
- Databases & infrastructure
- AI/ML (only if genuinely used)
- Soft skills only when they add signal

Preserve standard English spelling for technical terms:
JavaScript, TypeScript, React, Next.js, Django, FastAPI, PostgreSQL, Docker,
Kubernetes, AWS, REST API, GraphQL. Do not transliterate.

## Contact information

Clearly structured, visually separated from main content:
- Phone, email, location (Persian)
- Website, GitHub, LinkedIn, portfolio (LTR, intact)
- URLs/emails must remain LTR and readable inside RTL

## Templates

Choose a template via `options.template` in the resume JSON.

### classic
- Single-column layout
- Traditional heading underlines
- Contact info in a right-aligned strip below the name
- Section titles with horizontal rules
- Best for general-purpose professional use

### modern
- Two-column layout on A4
- Right main column: summary, experience, education, projects
- Left sidebar: contact, skills, languages, certifications
- Compact sidebar with bold category titles
- Best for tech/startup profiles, design-forward roles, or denser resumes

## Layout & typography

Select layout based on content volume:
- Single-column: < 8 years / compact profile
- Two-column: 8-15 years with rich skills/projects
- Compact: early-career / one-page target

Typography requirements:
- Persian font: Vazir, Vazirmatn, Sahel, Shabnam, or Samim
- Latin/technical: Arial, Noto Sans Mono for code
- Body 10.5-12pt, headings 14-18pt
- Line height 1.4-1.6, consistent spacing
- Margins 1.5-2cm, balanced whitespace
- Template consistency: use the same font stack across all sections in one template

Avoid: excessive decoration, oversized headings, dense unreadable blocks,
tiny typography, confusing timelines, unbalanced whitespace.

## Mixed Persian/English examples (must render correctly)

- `توسعه‌دهنده ارشد Frontend`
- `توسعه و نگهداری سرویس‌های Django و FastAPI`
- `Next.js 16`
- `GitHub: github.com/ehsanghaffarii`
- `email@example.com`
- `کاهش هزینه ۳۰٪ با استفاده از React و Node.js`

## Multi-page rules

If experience requires 2+ pages:
- Consistent header (name + page number) on each page
- No orphaned headings at page bottom
- Coherent section flow, no awkward splits
- Do not compress to force one page

## Content preservation (transform mode)

When transforming an existing resume:
- Preserve all factual info; improve structure/wording without changing meaning
- Remove duplication, fix consistency
- Do not invent or silently remove experience
- If user asks for shorter, prioritize relevant info — don't truncate arbitrarily

## Target-role adaptation

When a target role is given, prioritize relevant experience/tech/achievements.
Do not invent role-specific experience to fit the vacancy.

## Output pipeline

1. **Collect** candidate info + target role + preferences (layout, calendar, format, template)
2. **Select** template: `classic` for traditional single-column, `modern` for two-column sidebar layout
3. **Draft** content in logical order (Persian text, English terms intact)
4. **Generate** via `scripts/generate_resume.py` → PDF or DOCX
5. **Validate** via `scripts/validate_resume.py` (bidi, content, rendering)
6. **Render** final output; re-check if any issue

## Scripts

- `scripts/generate_resume.py` — Generate resume from JSON data → PDF/DOCX
- `scripts/validate_resume.py` — Validate RTL, content, file integrity
- `references/resume-data-schema.md` — JSON schema for resume input data
- `references/validation-rules.md` — Detailed validation rules and checks

## Quality checklist

Before finalizing, verify:

- [ ] RTL layout throughout (not just right-aligned)
- [ ] English words/terms not reversed or scrambled
- [ ] URLs, emails, file paths intact and readable
- [ ] Version numbers, IDs, technical values unchanged
- [ ] Dates consistent (one calendar, correct ranges)
- [ ] Table column order correct (RTL)
- [ ] Contact info with LTR content visually correct
- [ ] Fonts support Persian glyphs
- [ ] ZWNJ usage preserved where meaningful
- [ ] Page breaks don't split content awkwardly
- [ ] Mixed-direction sentences read naturally
- [ ] ATS-friendly structure (clear headings, logical reading order)
- [ ] Factual — no invented companies, metrics, dates, or roles
