# Grader Instructions for Persian Document Generator

This grader evaluates Persian document generation outputs for RTL correctness and quality.

## What to check

For each output, verify the following criteria:

### 1. RTL Layout (20 points)
- Text flows right-to-left
- Paragraphs have RTL direction
- Document structure follows RTL conventions

### 2. Mixed-Direction Content (25 points)
- English words and terms are NOT reversed or scrambled
- URLs remain intact and readable
- Email addresses are correct
- Version numbers are unchanged
- Technical content (commands, code) is readable
- Numbers render correctly (Persian or Latin as appropriate)

### 3. Typography (20 points)
- Persian characters are properly shaped
- ZWNJ usage is correct (verb prefixes, compounds)
- Punctuation is correct (Persian punctuation marks)
- Character forms are correct (ی vs ي, ک vs ك)

### 4. Tables (15 points)
- Table direction is RTL
- Column order is correct (right-to-left)
- Cell alignment matches content type
- Mixed content in cells renders correctly

### 5. Lists (10 points)
- Unordered lists have correct bullet placement
- Ordered lists have correct number placement
- Nested lists maintain direction

### 6. Document Structure (10 points)
- Headings follow RTL direction
- Headers/footers have correct direction
- Page breaks are placed correctly
- Overall document feels professional

## Grading scale

- **100-90**: Excellent — all criteria met, document is production-quality
- **89-70**: Good — most criteria met, minor issues
- **69-50**: Fair — some criteria missing, needs improvement
- **49-0**: Poor — significant RTL/formatting issues

## How to grade

1. Read the output file (DOCX)
2. Check each criterion above
3. Assign points for each criterion
4. Calculate total score
5. Note specific issues found

## Example grading

```json
{
  "rtl_layout": {"score": 18, "max": 20, "notes": "Text flows RTL, paragraphs correctly aligned"},
  "mixed_content": {"score": 22, "max": 25, "notes": "English terms readable, URLs intact"},
  "typography": {"score": 18, "max": 20, "notes": "ZWNJ correct, punctuation proper"},
  "tables": {"score": 14, "max": 15, "notes": "Table RTL, columns correct"},
  "lists": {"score": 9, "max": 10, "notes": "Bullets/numbers correct"},
  "structure": {"score": 9, "max": 10, "notes": "Professional layout"}
}
```

## Common issues to flag

1. **Reversed English**: "txet" instead of "text"
2. **Broken URLs**: "moc.elpmaxe//:sptth" instead of "https://example.com"
3. **Scrambled versions**: "7.0.16" instead of "16.0.7"
4. **Wrong character forms**: ي instead of ی, ك instead of ک
5. **Missing ZWNJ**: "میخواهم" instead of "می‌خواهم"
6. **LTR paragraph**: Persian paragraph set to LTR direction
7. **Table column order**: Columns in wrong order (LTR instead of RTL)
8. **List numbering**: Numbers on wrong side
