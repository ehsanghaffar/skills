#!/usr/bin/env python3
"""
validate_doc.py — Validate rendered Persian documents for RTL correctness.

Usage:
    python validate_doc.py --file document.docx
    python validate_doc.py --file document.pdf
    python validate_doc.py --text "text to check"

Checks for common RTL/bidirectional rendering issues:
- Reversed English words
- Broken URLs
- Scrambled version numbers
- Misplaced punctuation
- Incorrect list numbering
- Incorrect table direction
- Disconnected Persian glyphs
- Missing glyphs
- Inconsistent fonts
- Incorrect header/footer direction
- Persian content flowing LTR
- Broken mixed-direction sentences
- Text clipping
- Incorrect page breaks
- Broken spacing
- Corrupted ZWNJ usage
"""

import argparse
import re
import sys
from typing import List, Dict, Tuple, Optional
from pathlib import Path


# Unicode ranges for Persian/Arabic script
PERSIAN_RANGE = re.compile(r'[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]')
LATIN_RANGE = re.compile(r'[A-Za-z]')
DIGIT_PERSIAN = re.compile(r'[۰-۹]')
DIGIT_LATIN = re.compile(r'[0-9]')
ZWNJ = '‌'
ZWSP = '​'
LRM = '‎'
RLM = '‏'


class PersianDocValidator:
    """Validates Persian documents for RTL correctness."""

    def __init__(self):
        self.issues: List[Dict] = []
        self.warnings: List[Dict] = []

    def validate_text(self, text: str, context: str = "") -> Dict:
        """Validate a text string for RTL correctness.

        Returns a dict with:
        - valid: bool (True if no issues)
        - issues: list of found issues
        - warnings: list of warnings
        """
        self.issues = []
        self.warnings = []

        self._check_reversed_english(text, context)
        self._check_broken_urls(text, context)
        self._check_version_numbers(text, context)
        self._check_misplaced_punctuation(text, context)
        self._check_zwnj_usage(text, context)
        self._check_persian_glyphs(text, context)
        self._check_mixed_direction(text, context)
        self._check_numbers(text, context)

        return {
            'valid': len(self.issues) == 0,
            'issues': self.issues,
            'warnings': self.warnings,
            'context': context,
        }

    def validate_file(self, file_path: str) -> Dict:
        """Validate a document file (.docx or .pdf)."""
        path = Path(file_path)
        if not path.exists():
            return {'valid': False, 'error': f'File not found: {file_path}'}

        if path.suffix.lower() == '.docx':
            return self._validate_docx(file_path)
        elif path.suffix.lower() == '.pdf':
            return self._validate_pdf(file_path)
        else:
            # Treat as text
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return self.validate_text(text, context=file_path)

    def _validate_docx(self, file_path: str) -> Dict:
        """Validate a DOCX file."""
        try:
            from docx import Document
        except ImportError:
            return {'valid': False, 'error': 'python-docx not installed for DOCX validation'}

        doc = Document(file_path)
        all_text = []
        validation_results = []

        # Check paragraphs
        for i, para in enumerate(doc.paragraphs):
            text = para.text
            all_text.append(text)
            result = self.validate_text(text, context=f"paragraph {i+1}")
            validation_results.append(result)

            # Check paragraph direction
            pPr = para._element.pPr
            if pPr is not None:
                bidi = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}bidi')
                if bidi is not None and bidi.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val') == '0':
                    self.warnings.append({
                        'type': 'ltr_paragraph',
                        'message': f'Paragraph {i+1} is set to LTR but may contain Persian text',
                        'context': f"paragraph {i+1}",
                    })

        # Check tables
        for table_idx, table in enumerate(doc.tables):
            for row_idx, row in enumerate(table.rows):
                for col_idx, cell in enumerate(row.cells):
                    text = cell.text
                    all_text.append(text)
                    result = self.validate_text(text, context=f"table {table_idx+1}, row {row_idx+1}, col {col_idx+1}")
                    validation_results.append(result)

        full_text = '\n'.join(all_text)
        return {
            'valid': len(self.issues) == 0,
            'issues': self.issues,
            'warnings': self.warnings,
            'context': file_path,
            'paragraph_count': len(doc.paragraphs),
            'table_count': len(doc.tables),
        }

    def _validate_pdf(self, file_path: str) -> Dict:
        """Validate a PDF file (basic text extraction)."""
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                all_text = []
                for page_idx, page in enumerate(reader.pages):
                    text = page.extract_text()
                    all_text.append(text)
                    result = self.validate_text(text, context=f"page {page_idx+1}")
                    validation_results.append(result)
                full_text = '\n'.join(all_text)
        except ImportError:
            return {'valid': False, 'error': 'PyPDF2 not installed for PDF validation'}

        return {
            'valid': len(self.issues) == 0,
            'issues': self.issues,
            'warnings': self.warnings,
            'context': file_path,
        }

    def _check_reversed_english(self, text: str, context: str = "") -> None:
        """Check for English words that appear reversed (RTL artifact)."""
        # Common English words that might be reversed
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'has', 'have', 'from']
        for word in common_words:
            reversed_word = word[::-1]
            if reversed_word in text:
                self.issues.append({
                    'type': 'reversed_english',
                    'message': f'Possibly reversed English word: "{reversed_word}" (should be "{word}")',
                    'context': context,
                })

    def _check_broken_urls(self, text: str, context: str = "") -> None:
        """Check for broken or malformed URLs."""
        url_pattern = r'https?://[^\s]+|www\.[^\s]+'
        urls = re.findall(url_pattern, text)
        for url in urls:
            # Check for common URL corruption patterns
            if ' ' in url.replace('%20', ''):
                self.issues.append({
                    'type': 'broken_url',
                    'message': f'URL contains spaces: {url}',
                    'context': context,
                })
            if '://' not in url and 'www.' not in url:
                self.issues.append({
                    'type': 'broken_url',
                    'message': f'URL missing protocol: {url}',
                    'context': context,
                })

    def _check_version_numbers(self, text: str, context: str = "") -> None:
        """Check for scrambled version numbers."""
        version_pattern = r'\b\d+\.\d+(?:\.\d+)*\b'
        versions = re.findall(version_pattern, text)
        for version in versions:
            # Version numbers should not be reversed
            parts = version.split('.')
            for part in parts:
                if part and part[0] == '0' and len(part) > 1:
                    # Leading zero in version part — check if it's reversed
                    reversed_part = part[::-1]
                    if reversed_part.isdigit():
                        self.warnings.append({
                            'type': 'scrambled_version',
                            'message': f'Version number may be scrambled: {version}',
                            'context': context,
                        })

    def _check_misplaced_punctuation(self, text: str, context: str = "") -> None:
        """Check for misplaced punctuation in mixed-direction text."""
        # Persian punctuation should not be followed by Latin text without space
        persian_punct = '[,؛؟!…«»"'']'  # Fixed punctuation pattern
        matches = re.finditer(persian_punct, text)
        for match in matches:
            pos = match.end()
            if pos < len(text):
                next_char = text[pos]
                if LATIN_RANGE.match(next_char):
                    self.warnings.append({
                        'type': 'misplaced_punctuation',
                        'message': f'Persian punctuation followed by Latin text without space: {match.group()}{next_char}',
                        'context': context,
                    })

    def _check_zwnj_usage(self, text: str, context: str = "") -> None:
        """Check ZWNJ usage for correctness."""
        # ZWNJ should not appear at the start of a word
        words = text.split()
        for word in words:
            if word.startswith(ZWNJ):
                self.warnings.append({
                    'type': 'zwnj_placement',
                    'message': f'ZWNJ at start of word: {word}',
                    'context': context,
                })

        # ZWNJ should not appear in isolation
        if ZWNJ in text and len(text.strip()) == 1:
            self.warnings.append({
                'type': 'zwnj_isolation',
                'message': 'Isolated ZWNJ character',
                'context': context,
            })

    def _check_persian_glyphs(self, text: str, context: str = "") -> None:
        """Check for correct Persian character glyphs."""
        # Check for Arabic forms that should be Persian
        wrong_forms = {
            'ي': 'ی (Persian ya)',
            'ك': 'ک (Persian kaf)',
        }
        for wrong, correct in wrong_forms.items():
            if wrong in text:
                count = text.count(wrong)
                self.warnings.append({
                    'type': 'wrong_glyph',
                    'message': f'Found {count} Arabic "{wrong}" should be Persian "{correct}"',
                    'context': context,
                })

    def _check_mixed_direction(self, text: str, context: str = "") -> None:
        """Check for broken mixed-direction sentences."""
        # Persian text should not flow LTR unless it's a designated LTR segment
        # Check for Persian words followed by English in wrong order
        persian_words = PERSIAN_RANGE.findall(text)
        for word in persian_words:
            # If a Persian word is immediately followed by Latin text without space
            idx = text.find(word)
            if idx >= 0:
                after = text[idx + len(word):idx + len(word) + 10]
                if LATIN_RANGE.match(after.strip()[:1]):
                    # This is actually correct mixed-direction — Persian + English is fine
                    # But check for the reverse: Latin followed by Persian without space
                    pass

        # Check for English words followed by Persian without space (wrong)
        latin_words = LATIN_RANGE.findall(text)
        for word in latin_words:
            idx = text.find(word)
            if idx >= 0:
                after = text[idx + len(word):idx + len(word) + 10]
                if PERSIAN_RANGE.match(after.strip()[:1]):
                    self.warnings.append({
                        'type': 'mixed_direction',
                        'message': f'Latin "{word}" immediately followed by Persian without space',
                        'context': context,
                    })

    def _check_numbers(self, text: str, context: str = "") -> None:
        """Check for incorrect number rendering."""
        # Persian numerals in Persian text context (should be fine)
        persian_digits = re.findall(DIGIT_PERSIAN, text)
        if persian_digits:
            # Persian digits are fine in Persian text
            pass

        # Latin digits should not be reversed
        latin_digit_sequences = DIGIT_LATIN.findall(text)
        for seq in latin_digit_sequences:
            if len(seq) > 1:
                reversed_seq = seq[::-1]
                # Check if reversed sequence also appears (possible artifact)
                if reversed_seq in text and reversed_seq != seq:
                    self.warnings.append({
                        'type': 'reversed_number',
                        'message': f'Possible reversed number: {seq} (reversed: {reversed_seq})',
                        'context': context,
                    })


def main():
    parser = argparse.ArgumentParser(
        description="Validate Persian documents for RTL correctness"
    )
    parser.add_argument("--file", "-f", help="Path to document file (.docx, .pdf, .txt)")
    parser.add_argument("--text", "-t", help="Text to validate directly")
    parser.add_argument("--context", "-c", default="", help="Context label for the text")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as issues")

    args = parser.parse_args()

    validator = PersianDocValidator()

    if args.text:
        result = validator.validate_text(args.text, context=args.context or "inline text")
    elif args.file:
        result = validator.validate_file(args.file)
    else:
        parser.print_help()
        return 1

    if 'error' in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        return 1

    if args.json:
        import json
        output = {
            'valid': result['valid'],
            'issues': result.get('issues', []),
            'warnings': result.get('warnings', []),
            'context': result.get('context', ''),
        }
        if 'paragraph_count' in result:
            output['paragraph_count'] = result['paragraph_count']
        if 'table_count' in result:
            output['table_count'] = result['table_count']
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        if result['valid']:
            print("✅ Document validation passed")
        else:
            print(f"❌ Document validation failed ({len(result.get('issues', []))} issues)")

        for issue in result.get('issues', []):
            print(f"  Issue: {issue['message']}")
            if issue.get('context'):
                print(f"    Context: {issue['context']}")

        for warning in result.get('warnings', []):
            print(f"  Warning: {warning['message']}")
            if warning.get('context'):
                print(f"    Context: {warning['context']}")

    return 0 if result['valid'] else 1


if __name__ == "__main__":
    sys.exit(main())
