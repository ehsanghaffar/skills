# Document Generation Patterns

## Report structure

```
[Title Page / Document Title]
├── Executive Summary
├── Introduction
├── Main Sections
│   ├── Subsection with tables
│   ├── Subsection with code/technical content
│   └── Subsection with mixed content
├── Conclusions
└── Appendices
```

### Headers and footers
- Header: Document title or section name (RTL-aligned)
- Footer: Page numbers (centered or right-aligned for RTL)
- First page may have different header/footer

### Page layout
- Default: A4 or Letter
- Margins: 2-2.5cm sides, 2cm top/bottom
- For RTL: right margin slightly larger than left (to account for pagination)

## Formal letter structure

```
[Sender address/info]
[Date — Persian calendar preferred]
[Recipient address/info]

[Subject line]

[Body — formal Persian prose]

[Closing]
[Signature]
```

### Letter formatting rules
- Date format: ۱۴۰۵/۰۷/۱۴ or ۱۴۰۵/۰۷/۱۴ هـ.ش
- Salutation: جناب آقا/سرکار خانم (or دانشمندان/همکاران for plural)
- Closing: با احترام, با تشکر, خداحافظی
- Signature block: aligned right (RTL)

## Technical documentation

### Structure
```
[Title]
├── Overview
├── Installation
│   ├── Prerequisites
│   └── Setup steps
├── Configuration
│   ├── Environment variables
│   └── Settings
├── Usage
│   ├── Examples
│   └── API reference
└── Troubleshooting
```

### Mixed content in technical docs
- Code: preserve original language (English for code, Persian for comments where appropriate)
- CLI commands: show as-is with Persian explanations
- Version numbers: keep Latin numerals
- URLs: keep完整, don't break across lines without hyphenation
- File paths: keep as-is

### Code block formatting
Use fenced code blocks with language tags:
```python
# Persian comments in code
سلام = "دفترچه مراجع"  # متن فارسی در کد
```

## Resume/CV structure

```
[Name]
[Contact info — RTL-aligned]

Summary
Experience
  [Company] — [Role] — [Dates]
  - Achievement 1
  - Achievement 2

Education
  [University] — [Degree] — [Dates]

Skills
  - Persian: native
  - English: fluent
  - Technical: [list]
```

### Resume RTL considerations
- Contact info (phone, email, location) — RTL-aligned
- Dates — right-aligned
- Skills list — RTL direction
- Technical skills (frameworks, tools) — keep Latin script intact

## Article/Essay structure

```
[Title]
[Subtitle (optional)]
[Byline — author, date]

[Introduction]
[Body — multiple sections]
  [Headings]
  [Paragraphs]
  [Quotes where appropriate]
  [Lists if needed]

[Conclusion]
[References]
```

### Article formatting
- First paragraph may be drop-cap styled (if supported by renderer)
- Block quotes: indented, with proper quotation marks (« »)
- Footnotes: RTL-aligned, numbered with Persian numerals

## Table patterns

### Simple data table
| ستون ۱ (راست) | ستون ۲ (وسط) | ستون ۳ (چپ) |
|---------------|--------------|-------------|
| مقدار ۱       | مقدار ۲      | مقدار ۳     |

### Mixed content table
| ترجمه | Original | توضیح |
|-------|----------|-------|
| Next.js | فریمورک JavaScript | سرور رندرینگ |
| API | رابط برنامه‌نویسی | REST endpoints |

### Table rules
- Column direction matches overall document direction (RTL)
- Header row: bold, centered or right-aligned
- Cell content: follows its own direction rules (English stays LTR within RTL cell)
- Numbers: right-aligned within cells
- URLs: left-aligned within cells (they break LTR)

## List patterns

### Unordered list
- Item 1 (RTL bullet on right)
- Item 2
  - Nested item (RTL bullet, indented)
- Item 3

### Ordered list
1. Item 1 (RTL number on right)
2. Item 2
   a. Nested item (lowercase Latin, indented)
3. Item 3

### Mixed list items
- نسخه Next.js 16.0.7 شامل [features] است
- دستور `npm install` برای نصب استفاده می‌شود
- آدرس سرور: https://api.example.com/v1/users

## Quotation patterns

### Short quote (inline)
متن «۱۴۰۵/۰۷/۱۴ منتشر شد» در گزارش آمده است.

### Block quote
```
«این متن بلندتر است و به‌عنوان نقل‌قول در گزارش قرار می‌گیرد.
محتوای کامل نقل‌قول در این بلاک جداگانه نمایش داده می‌شود.»
```

## Headers and footers

### Header
- Document title (right-aligned)
- Optional: section name, document ID
- Rule line (optional)

### Footer
- Page numbers (center or right-aligned for RTL)
- Optional: date, confidential marking
- Rule line (optional)

### First page considerations
- Title page may omit header/footer
- Subsequent pages include header/footer
- Different first-page option for formal documents
