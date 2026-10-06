# Persian Typography Rules

## Character forms

Persian uses different character forms depending on position in a word:

- Isolated: ا ب پ ت ث ج چ ح خ د ذ ر ز ژ س ش ص ض ط ظ ع غ ف ق ک گ ل م ن و ه ی
- Initial: ـب ـپ ـت ـث ـج ـچ ـح ـخ ـد ـر ـز ـس ـش ـص ـض ـط ـظ ـع ـغ ـف ـق ـک ـل ـم ـن ـو ـه ـی
- Medial: ـبـ ـپـ ـتـ ـثـ ـجـ ـچـ ـحـ ـخـ ـدـ ـرـ ـزـ ـسـ ـشـ ـصـ ـضـ ـطـ ـظـ ـعـ ـغـ ـفـ ـقـ ـکـ ـلـ ـمـ ـنـ ـوـ ـهـ ـیـ
- Final: ـب ـپ ـت ـث ـج ـچ ـح ـخ ـد ـر ـز ـس ـش ـص ـض ـط ـظ ـع ـغ ـف ـق ـک ـل ـم ـن ـو ـه ـی

The rendering engine handles shaping automatically. Do not manually select character forms.

## Common character confusions

| Wrong | Correct | Context |
|-------|---------|---------|
| ي | ی | Persian letter ye (always use ی for Persian) |
| ك | ک | Persian letter kef (always use ک for Persian) |
| ئ | ی | Word-final ye |
| ؤ | و | Word-final waw |

Do not substitute Arabic forms (ي, ك) for Persian forms (ی, ک) unless the text explicitly contains Arabic words.

## ZWNJ (Zero-Width Non-Joiner)

ZWNJ (U+200C) is used to prevent two characters from joining. Meaningful uses in Persian:

- **Verb prefixes**: می‌خواهم (I want), می‌شود (becomes), می‌توانم (I can)
- **Compound words**: کتاب‌ها (books), خانه‌ها (houses)
- **After certain particles**: از او، با او، در او
- **Before certain suffixes**: نمی‌روم، نمی‌خوانم

**Do not:**
- Add ZWNJ where it doesn't belong (e.g., between unrelated words)
- Remove ZWNJ from verb prefixes (میخواهم is wrong)
- Replace ZWNJ with regular spaces

## ZWNJ vs. ZWSP

- ZWNJ (U+200C): Prevents joining, has width zero, used in Persian typography
- ZWSP (U+200B): Zero-width space, used for line-breaking
- Do not confuse the two — they serve different purposes

## Numbers and digits

### Persian numerals
۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹

Used in: ordinary text, dates (shamsi), prices in Persian context, counts

### Latin numerals
0 1 2 3 4 5 6 7 8 9

Used in: version numbers (v2.4.1), technical IDs, codes, URLs, mathematical expressions

### Arabic-Indic numerals (avoid)
٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩

These are used in Arabic-language contexts, not Persian. Avoid unless quoting Arabic text.

## Punctuation marks

Persian uses different punctuation than Latin:

| Persian | Latin | Usage |
|---------|-------|-------|
| ، | , | comma |
| ؛ | ; | semicolon |
| ؟ | ? | question mark |
| ! | ! | exclamation (same shape, different spacing) |
| « » | " " | quotation marks (Guillemets) |
| … | ... | ellipsis (three dots, not six) |
| – | - | en dash |
| — | — | em dash |

### Spacing with punctuation
- Persian punctuation attaches to the preceding word (no space before)
- A space follows Persian punctuation (،،)
- Latin punctuation in mixed text follows its own rules

## Font guidance

Fonts that properly support Persian/Arabic shaping:
- **System**: B Nazanin, B Mitra, B Lotus, B Yekan, B Shahab
- **Google Noto**: Noto Naskh Arabic, Noto Naskh Persian
- **Common**: Tahoma, Arial (with Persian support), Calibri

For code/technical content mixed with Persian, use a monospace font that supports Persian (e.g., Noto Sans Mono).

## URL and technical content in Persian text

- URLs remain in Latin script, left-to-right within the RTL paragraph
- Use Unicode bidirectional markers (LRM/RLM) only when the renderer cannot determine direction automatically
- File paths: `/home/user/فایل.txt` — the path stays LTR, Persian filename stays RTL
- Email addresses: `نام@دامنه.ir` — local part and domain follow their own direction rules

## Common rendering problems and prevention

| Problem | Cause | Prevention |
|---------|-------|------------|
| Reversed English words | Forcing RTL on English text | Let the renderer handle direction; use logical order |
| Broken URLs | RTL reordering URL characters | Keep URLs in logical order; use LRM markers if needed |
| Scrambled version numbers | Numbers treated as RTL | Keep version strings as-is; they're LTR by default |
| Disconnected glyphs | Wrong font or rendering engine | Use fonts with proper Persian shaping support |
| Missing ZWNJ | Automated text processing | Preserve ZWNJ in verb prefixes and compounds |
| Incorrect ي/ی | Font fallback or input method | Use ی consistently for Persian; check font support |
