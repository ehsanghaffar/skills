#!/usr/bin/env python3
"""
generate_docx.py — Generate RTL-aware Word documents with mixed Persian/Latin support.

Usage:
    python generate_docx.py --output document.docx --title "عنوان سند" [options]

The script creates a properly structured DOCX with:
- RTL paragraph direction
- Correct table direction
- Mixed-direction text support
- Proper font selection for Persian/Latin rendering
- Headers and footers with correct direction
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Optional, Tuple
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import copy


# Default fonts that support Persian shaping
PERSIAN_FONT = "B Nazanin"
LATIN_FONT = "Arial"
MONO_FONT = "Noto Sans Mono"

# RTL direction marker
RTL_DIR = "rtl"
LTR_DIR = "ltr"


class PersianDocumentGenerator:
    """Generates RTL-aware Persian Word documents."""

    def __init__(self, title: str = "", output_path: str = "document.docx"):
        self.doc = Document()
        self.output_path = output_path
        self.title = title
        self._setup_document()

    def _setup_document(self):
        """Configure document-level RTL settings."""
        # Set default section direction to RTL
        section = self.doc.sections[0]
        section.direction = 1  # WD_DIRECTION.RTL

        # Set default margins
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2)

        # Set default font
        style = self.doc.styles['Normal']
        style.font.name = PERSIAN_FONT
        style.font.size = Pt(14)
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        style.paragraph_format.line_spacing = 1.5

        # Configure RTL font for the style
        rPr = style.element.get_or_add_rPr()
        rFonts = parse_xml(
            f'<w:rFonts {nsdecls("w")} w:ascii="{PERSIAN_FONT}" '
            f'w:hAnsi="{PERSIAN_FONT}" w:cs="{PERSIAN_FONT}" w:fareast="{PERSIAN_FONT}"/>'
        )
        rPr.insert(0, rFonts)

    def _set_paragraph_direction(self, paragraph, direction: str = RTL_DIR):
        """Set paragraph direction (RTL or LTR)."""
        # paragraph can be a Paragraph object or a CT_P element
        if hasattr(paragraph, '_element'):
            pPr = paragraph._element.get_or_add_pPr()
        else:
            pPr = paragraph.get_or_add_pPr()
        bidi = parse_xml(
            f'<w:bidi {nsdecls("w")} w:val="1"/>' if direction == RTL_DIR
            else f'<w:bidi {nsdecls("w")} w:val="0"/>'
        )
        # Remove existing bidi if any
        for existing in pPr.findall(qn('w:bidi')):
            pPr.remove(existing)
        pPr.append(bidi)

    def _set_run_font(self, run, persian: bool = True, latin: bool = False, mono: bool = False):
        """Configure font for a run based on content type."""
        if mono:
            run.font.name = MONO_FONT
            run.font.size = Pt(11)
        elif persian:
            run.font.name = PERSIAN_FONT
            run.font.size = Pt(14)
        elif latin:
            run.font.name = LATIN_FONT
            run.font.size = Pt(14)

    def add_title(self, text: str, level: int = 1):
        """Add a title with RTL direction."""
        heading = self.doc.add_heading(text, level=level)
        self._set_paragraph_direction(heading._element, RTL_DIR)
        for run in heading.runs:
            run.font.name = PERSIAN_FONT
        return heading

    def add_heading(self, text: str, level: int = 2):
        """Add a heading with RTL direction."""
        heading = self.doc.add_heading(text, level=level)
        self._set_paragraph_direction(heading._element, RTL_DIR)
        for run in heading.runs:
            run.font.name = PERSIAN_FONT
        return heading

    def add_paragraph(self, text: str, mixed_parts: Optional[List[Dict]] = None,
                      alignment: str = "right", bold: bool = False,
                      italic: bool = False, font_size: int = 14) -> None:
        """Add a paragraph with RTL direction.

        Args:
            text: Full paragraph text
            mixed_parts: List of dicts with 'text' and 'type' ('persian', 'latin', 'mono')
                         for mixed-direction content. If None, treated as pure Persian.
            alignment: Text alignment ('right', 'left', 'center', 'justify')
            bold: Whether text is bold
            italic: Whether text is italic
            font_size: Font size in points
        """
        para = self.doc.add_paragraph()
        self._set_paragraph_direction(para, RTL_DIR)

        if mixed_parts:
            for part in mixed_parts:
                run = para.add_run(part['text'])
                run.font.size = Pt(font_size)
                run.bold = bold
                run.italic = italic
                if part.get('type') == 'latin':
                    run.font.name = LATIN_FONT
                elif part.get('type') == 'mono':
                    run.font.name = MONO_FONT
                    run.font.size = Pt(11)
                else:
                    run.font.name = PERSIAN_FONT
        else:
            run = para.add_run(text)
            run.font.name = PERSIAN_FONT
            run.font.size = Pt(font_size)
            run.bold = bold
            run.italic = italic

        # Set alignment
        align_map = {
            'right': WD_ALIGN_PARAGRAPH.RIGHT,
            'left': WD_ALIGN_PARAGRAPH.LEFT,
            'center': WD_ALIGN_PARAGRAPH.CENTER,
            'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
        }
        para.alignment = align_map.get(alignment, WD_ALIGN_PARAGRAPH.RIGHT)

        return para

    def add_mixed_paragraph(self, segments: List[Tuple[str, str]]) -> None:
        """Add a paragraph with mixed Persian/Latin content.

        Args:
            segments: List of (text, type) tuples where type is 'persian', 'latin',
                      'mono', 'number', 'url', or 'code'
        """
        para = self.doc.add_paragraph()
        self._set_paragraph_direction(para, RTL_DIR)

        for text, seg_type in segments:
            run = para.add_run(text)
            if seg_type in ('latin', 'url', 'code'):
                run.font.name = LATIN_FONT if seg_type != 'mono' else MONO_FONT
                run.font.size = Pt(12) if seg_type == 'mono' else Pt(14)
            elif seg_type == 'mono':
                run.font.name = MONO_FONT
                run.font.size = Pt(11)
            else:
                run.font.name = PERSIAN_FONT
                run.font.size = Pt(14)

        return para

    def add_table(self, headers: List[str], rows: List[List[str]],
                  header_align: str = "center", col_widths: Optional[List[float]] = None,
                  mixed_columns: Optional[Dict[int, List[str]]] = None) -> None:
        """Add an RTL table with proper direction.

        Args:
            headers: Column headers (right-to-left order)
            rows: Data rows, each row is a list of cell values
            header_align: Header alignment ('center', 'right', 'left')
            col_widths: Optional column widths in cm
            mixed_columns: Dict mapping column index to list of segment types
                          for mixed-direction cells (e.g., {2: ['persian', 'latin']})
        """
        table = self.doc.add_table(rows=1 + len(rows), cols=len(headers))
        table.style = 'Table Grid'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Set table direction to RTL
        tblPr = table._element.tblPr
        bidiVisual = parse_xml(
            f'<w:bidiVisual {nsdecls("w")} w:val="1"/>'
        )
        tblPr.append(bidiVisual)

        # Add headers
        for i, header in enumerate(headers):
            cell = table.rows[0].cells[i]
            cell.text = ""
            para = cell.paragraphs[0]
            self._set_paragraph_direction(para, RTL_DIR)
            run = para.add_run(header)
            run.bold = True
            run.font.name = PERSIAN_FONT
            run.font.size = Pt(12)
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Add data rows
        for row_idx, row in enumerate(rows):
            for col_idx, cell_value in enumerate(row):
                cell = table.rows[row_idx + 1].cells[col_idx]
                cell.text = ""
                para = cell.paragraphs[0]
                self._set_paragraph_direction(para, RTL_DIR)

                # Handle mixed content in cells
                if mixed_columns and col_idx in mixed_columns:
                    segments = self._parse_mixed_cell(cell_value, mixed_columns[col_idx])
                    for text, seg_type in segments:
                        run = para.add_run(text)
                        run.font.name = LATIN_FONT if seg_type == 'latin' else PERSIAN_FONT
                        run.font.size = Pt(11)
                else:
                    run = para.add_run(cell_value)
                    run.font.name = PERSIAN_FONT
                    run.font.size = Pt(11)

                # Right-align numbers, left-align URLs
                if cell_value.strip().replace(',', '').replace('.', '').isdigit():
                    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                elif cell_value.startswith('http') or '@' in cell_value:
                    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        # Set column widths if provided
        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    if idx < len(row.cells):
                        row.cells[idx].width = Cm(width)

        return table

    def _parse_mixed_cell(self, text: str, segment_types: List[str]) -> List[Tuple[str, str]]:
        """Parse a mixed cell into segments with types."""
        # Simple split by whitespace for mixed content
        parts = text.split()
        segments = []
        for i, part in enumerate(parts):
            seg_type = segment_types[i] if i < len(segment_types) else 'persian'
            segments.append((part + ' ', seg_type))
        return segments

    def add_ordered_list(self, items: List[str], start_num: int = 1) -> None:
        """Add an ordered list with RTL direction.

        Args:
            items: List of item texts
            start_num: Starting number (default 1)
        """
        for idx, item in enumerate(items):
            para = self.doc.add_paragraph()
            self._set_paragraph_direction(para, RTL_DIR)
            number = f"{start_num + idx}."
            run_num = para.add_run(f"{number} ")
            run_num.font.name = PERSIAN_FONT
            run_num.font.size = Pt(14)
            run_text = para.add_run(item)
            run_text.font.name = PERSIAN_FONT
            run_text.font.size = Pt(14)
            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    def add_unordered_list(self, items: List[str], nested: bool = False) -> None:
        """Add an unordered list with RTL direction.

        Args:
            items: List of item texts
            nested: Whether this is a nested list (indented)
        """
        bullet = "•"
        for item in items:
            para = self.doc.add_paragraph()
            self._set_paragraph_direction(para, RTL_DIR)
            run_bullet = para.add_run(f" {bullet} ")
            run_bullet.font.name = PERSIAN_FONT
            run_bullet.font.size = Pt(14)
            run_text = para.add_run(item)
            run_text.font.name = PERSIAN_FONT
            run_text.font.size = Pt(14)
            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            if nested:
                para.paragraph_format.left_indent = Cm(1)

    def add_code_block(self, code: str, language: str = "") -> None:
        """Add a code block with proper formatting.

        Args:
            code: The code content (preserved as-is, no direction changes)
            language: Programming language for syntax highlighting hint
        """
        para = self.doc.add_paragraph()
        self._set_paragraph_direction(para, LTR_DIR)  # Code blocks are LTR

        # Add a left border to indicate code block
        pPr = para._element.get_or_add_pPr()
        pBdr = parse_xml(
            f'<w:pBdr {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="12" w:space="8" w:color="0000FF"/>'
            f'</w:pBdr>'
        )
        pPr.append(pBdr)

        for line in code.split('\n'):
            run = para.add_run(line)
            run.font.name = MONO_FONT
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            para.add_run('\n')

        return para

    def add_page_break(self) -> None:
        """Add a page break."""
        self.doc.add_page_break()

    def add_header(self, text: str) -> None:
        """Add a header with RTL direction.

        Args:
            text: Header text
        """
        section = self.doc.sections[0]
        header = section.header
        header.is_linked_to_previous = False
        para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
        self._set_paragraph_direction(para, RTL_DIR)
        run = para.add_run(text)
        run.font.name = PERSIAN_FONT
        run.font.size = Pt(10)
        run.italic = True

    def add_footer(self, text: str = "", page_number: bool = True) -> None:
        """Add a footer with RTL direction.

        Args:
            text: Footer text (optional)
            page_number: Whether to include page numbers
        """
        section = self.doc.sections[0]
        footer = section.footer
        footer.is_linked_to_previous = False
        para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        self._set_paragraph_direction(para, RTL_DIR)

        if text:
            run = para.add_run(text)
            run.font.name = PERSIAN_FONT
            run.font.size = Pt(9)

        if page_number:
            # Add page number field
            run = para.add_run(" | صفحه ")
            run.font.name = PERSIAN_FONT
            run.font.size = Pt(9)
            # Insert PAGE field
            fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
            run._element.append(fldChar1)
            instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
            run._element.append(instrText)
            fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
            run._element.append(fldChar2)

    def add_quote(self, text: str, attribution: str = "") -> None:
        """Add a block quote with RTL direction.

        Args:
            text: Quoted text
            attribution: Optional attribution
        """
        para = self.doc.add_paragraph()
        self._set_paragraph_direction(para, RTL_DIR)

        # Indent the quote
        para.paragraph_format.left_indent = Cm(1.5)
        para.paragraph_format.right_indent = Cm(0.5)

        run = para.add_run(f"«{text}»")
        run.font.name = PERSIAN_FONT
        run.font.size = Pt(13)
        run.italic = True

        if attribution:
            para2 = self.doc.add_paragraph()
            self._set_paragraph_direction(para2, RTL_DIR)
            para2.paragraph_format.left_indent = Cm(1.5)
            run2 = para2.add_run(f"— {attribution}")
            run2.font.name = PERSIAN_FONT
            run2.font.size = Pt(12)
            run2.italic = True

    def save(self) -> str:
        """Save the document and return the output path."""
        self.doc.save(self.output_path)
        return self.output_path


def create_sample_document(output_path: str = "sample_persian.docx") -> str:
    """Create a sample Persian document demonstrating all features."""
    gen = PersianDocumentGenerator(
        title="گزارش نمونه — تولید سند فارسی",
        output_path=output_path
    )

    # Header and footer
    gen.add_header("گزارش نمونه — نسخه ۱.۰")
    gen.add_footer(page_number=True)

    # Title
    gen.add_title("گزارش نمونه تولید سند فارسی", level=1)

    # Mixed content paragraph
    gen.add_paragraph(
        "نسخه Next.js 16.0.7 منتشر شد. این نسخه شامل قابلیت‌های جدید متعددی است.",
        mixed_parts=[
            {'text': 'نسخه ', 'type': 'persian'},
            {'text': 'Next.js', 'type': 'latin'},
            {'text': ' 16.0.7 منتشر شد. این نسخه شامل قابلیت‌های جدید متعددی است.', 'type': 'persian'},
        ]
    )

    # Technical content
    gen.add_paragraph(
        "دستور نصب: npm install @tanstack/react-query",
        mixed_parts=[
            {'text': 'دستور نصب: ', 'type': 'persian'},
            {'text': 'npm install @tanstack/react-query', 'type': 'mono'},
        ]
    )

    gen.add_paragraph(
        "ایمیل پشتیبانی: hello@example.com | آدرس وب: https://api.example.com/v1/users",
        mixed_parts=[
            {'text': 'ایمیل پشتیبانی: ', 'type': 'persian'},
            {'text': 'hello@example.com', 'type': 'latin'},
            {'text': ' | آدرس وب: ', 'type': 'persian'},
            {'text': 'https://api.example.com/v1/users', 'type': 'url'},
        ]
    )

    # Section heading
    gen.add_heading("جدول نمونه", level=2)

    # Table with mixed content
    headers = ['نام فیچر', 'نسخه', 'وضعیت', 'توضیحات']
    rows = [
        ['React Query', 'v5.60.0', 'فعال', 'مدیریت state سمت کلاینت'],
        ['Next.js', '16.0.7', 'پیشنهادی', 'فریمورک React'],
        ['TypeScript', '5.8.3', 'توصیه‌شده', 'تایپ‌سیستم برای JS'],
    ]
    mixed_cols = {
        0: ['persian', 'latin'],  # Feature name (mixed)
        1: ['latin'],              # Version (LTR)
        3: ['persian'],            # Description (RTL)
    }
    gen.add_table(headers, rows, mixed_columns=mixed_cols)

    # Lists
    gen.add_heading("فهرست قابلیت‌ها", level=2)
    gen.add_unordered_list([
        'پشتیبانی از RTL کامل',
        'ترکیب فارسی و انگلیسی',
        'نمایش صحیح اعداد و تاریخ‌ها',
        'پشتیبانی از کد و دستورات',
    ])

    gen.add_heading("مراحل نصب", level=2)
    gen.add_ordered_list([
        'نصب Node.js نسخه 20.11.0 یا بالاتر',
        'اجرای دستور npm install',
        'تنظیم فایل محیط .env',
        'اجرای دستور npm run dev',
    ])

    # Code block
    gen.add_heading("نمونه کد", level=2)
    gen.add_code_block(
        '```javascript\n'
        'import { QueryClient } from "@tanstack/react-query";\n'
        '\n'
        'const client = new QueryClient();\n'
        'console.log("نسخه:", "5.60.0");\n'
        '```',
        language="javascript"
    )

    # Block quote
    gen.add_heading("نقل‌قول", level=2)
    gen.add_quote(
        "تولید سند فارسی با RTL صحیح نیازمند توجه دقیق به جهت متن و ترتیب 런‌هاست.",
        "تیم توسعه"
    )

    # Page break
    gen.add_page_break()

    # New section
    gen.add_heading("پیوست")
    gen.add_paragraph("این بخش شامل اطلاعات تکمیلی است.")

    # Save
    return gen.save()


def main():
    parser = argparse.ArgumentParser(
        description="Generate RTL-aware Persian Word documents"
    )
    parser.add_argument("--output", "-o", default="document.docx",
                        help="Output file path (default: document.docx)")
    parser.add_argument("--title", "-t", default="",
                        help="Document title")
    parser.add_argument("--sample", action="store_true",
                        help="Generate a sample document")
    parser.add_argument("--config", "-c", help="Path to JSON config file")

    args = parser.parse_args()

    if args.sample:
        output = create_sample_document(args.output)
        print(f"Sample document created: {output}")
        return 0

    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        gen = PersianDocumentGenerator(
            title=config.get('title', ''),
            output_path=config.get('output', args.output)
        )
        # Process sections from config
        for section in config.get('sections', []):
            section_type = section.get('type', 'paragraph')
            if section_type == 'heading':
                gen.add_heading(section['text'], level=section.get('level', 2))
            elif section_type == 'paragraph':
                gen.add_paragraph(
                    section.get('text', ''),
                    mixed_parts=section.get('mixed_parts'),
                    alignment=section.get('alignment', 'right'),
                )
            elif section_type == 'table':
                gen.add_table(
                    section['headers'],
                    section['rows'],
                    mixed_columns=section.get('mixed_columns'),
                )
            elif section_type == 'list':
                if section.get('ordered'):
                    gen.add_ordered_list(section['items'])
                else:
                    gen.add_unordered_list(section['items'])
            elif section_type == 'code':
                gen.add_code_block(section['code'], section.get('language', ''))
            elif section_type == 'quote':
                gen.add_quote(section['text'], section.get('attribution', ''))
            elif section_type == 'page_break':
                gen.add_page_break()
        output = gen.save()
        print(f"Document created from config: {output}")
        return 0

    # Default: create sample
    output = create_sample_document(args.output)
    print(f"Document created: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
