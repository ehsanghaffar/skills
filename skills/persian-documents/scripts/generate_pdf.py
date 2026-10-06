#!/usr/bin/env python3
"""
generate_pdf.py — Generate PDFs with correct Persian text shaping and RTL layout.

Usage:
    python generate_pdf.py --output document.pdf --title "عنوان سند" [options]

Requires: weasyprint or reportlab with Persian font support.

The script creates PDFs with:
- RTL text direction
- Proper Persian text shaping
- Mixed Persian/Latin content
- Correct number rendering
- Professional typography
"""

import argparse
import json
import os
import sys
from typing import List, Dict, Optional, Tuple


# Try to import weasyprint; fall back to reportlab
try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT, TA_LEFT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
    from reportlab.platypus.flowables import HRFlowable
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# RTL CSS for HTML-based PDF generation
RTL_CSS = """
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
<meta charset="UTF-8">
<style>
  body {
    font-family: 'B Nazanin', 'Tahoma', 'Arial', sans-serif;
    font-size: 14pt;
    line-height: 1.8;
    direction: rtl;
    text-align: right;
    color: #333;
    margin: 2cm;
  }
  h1 { font-size: 20pt; text-align: right; margin-bottom: 20pt; }
  h2 { font-size: 16pt; text-align: right; margin-top: 24pt; margin-bottom: 12pt; }
  h3 { font-size: 14pt; text-align: right; margin-top: 18pt; margin-bottom: 10pt; }
  p { text-align: right; margin-bottom: 12pt; }
  table {
    border-collapse: collapse;
    width: 100%;
    margin: 16pt 0;
    direction: rtl;
  }
  th, td {
    border: 1px solid #ccc;
    padding: 8pt 12pt;
    text-align: right;
  }
  th { background-color: #f5f5f5; font-weight: bold; }
  code {
    font-family: 'Consolas', 'Monaco', monospace;
    background-color: #f4f4f4;
    padding: 2pt 6pt;
    border-radius: 3pt;
    font-size: 11pt;
  }
  pre {
    background-color: #f8f8f8;
    padding: 12pt;
    border-radius: 4pt;
    border-right: 4pt solid #0066cc;
    overflow-x: auto;
    direction: ltr;
    text-align: left;
  }
  pre code { background: none; padding: 0; }
  blockquote {
    border-right: 3pt solid #999;
    padding-right: 16pt;
    margin: 16pt 0;
    color: #666;
    font-style: italic;
  }
  ul, ol { padding-right: 20pt; }
  li { margin-bottom: 6pt; }
  .page-break { page-break-before: always; }
  .ltr { direction: ltr; text-align: left; }
  .rtl { direction: rtl; text-align: right; }
  .mixed { direction: rtl; text-align: right; }
  .url { direction: ltr; text-align: left; word-break: break-all; }
</style>
</head>
<body>
"""

HTML_FOOTER = """
</body>
</html>
"""


class PersianPDFGenerator:
    """Generates RTL-aware Persian PDFs."""

    def __init__(self, title: str = "", output_path: str = "document.pdf"):
        self.title = title
        self.output_path = output_path
        self.sections: List[Dict] = []
        self.html_content = RTL_CSS

    def add_title(self, text: str) -> None:
        """Add a document title."""
        self.html_content += f"<h1>{text}</h1>\n"

    def add_heading(self, text: str, level: int = 2) -> None:
        """Add a heading."""
        tag = f"h{min(level, 6)}"
        self.html_content += f"<{tag}>{text}</{tag}>\n"

    def add_paragraph(self, text: str, mixed_parts: Optional[List[Dict]] = None,
                       alignment: str = "right") -> None:
        """Add a paragraph with RTL direction.

        Args:
            text: Full paragraph text
            mixed_parts: List of dicts with 'text' and 'type'
                         ('persian', 'latin', 'mono', 'url')
            alignment: Text alignment ('right', 'left', 'center', 'justify')
        """
        if mixed_parts:
            html_text = ""
            for part in mixed_parts:
                text_content = part['text']
                seg_type = part.get('type', 'persian')
                if seg_type == 'latin':
                    html_text += f'<span class="ltr">{text_content}</span>'
                elif seg_type == 'mono':
                    html_text += f'<code>{text_content}</code>'
                elif seg_type == 'url':
                    html_text += f'<span class="url">{text_content}</span>'
                else:
                    html_text += text_content
            self.html_content += f"<p>{html_text}</p>\n"
        else:
            self.html_content += f"<p>{text}</p>\n"

    def add_table(self, headers: List[str], rows: List[List[str]],
                   mixed_columns: Optional[Dict[int, List[str]]] = None) -> None:
        """Add an RTL table.

        Args:
            headers: Column headers
            rows: Data rows
            mixed_columns: Dict mapping column index to segment types
        """
        html = '<table>\n<thead>\n<tr>\n'
        for header in headers:
            html += f'<th>{header}</th>\n'
        html += '</tr>\n</thead>\n<tbody>\n'

        for row in rows:
            html += '<tr>\n'
            for col_idx, cell in enumerate(row):
                if mixed_columns and col_idx in mixed_columns:
                    segments = self._parse_mixed_cell(cell, mixed_columns[col_idx])
                    cell_html = ""
                    for text, seg_type in segments:
                        if seg_type == 'latin':
                            cell_html += f'<span class="ltr">{text}</span> '
                        else:
                            cell_html += text + ' '
                    html += f'<td>{cell_html.strip()}</td>\n'
                else:
                    html += f'<td>{cell}</td>\n'
            html += '</tr>\n'

        html += '</tbody>\n</table>\n'
        self.html_content += html

    def _parse_mixed_cell(self, text: str, segment_types: List[str]) -> List[Tuple[str, str]]:
        """Parse a mixed cell into segments with types."""
        parts = text.split()
        segments = []
        for i, part in enumerate(parts):
            seg_type = segment_types[i] if i < len(segment_types) else 'persian'
            segments.append((part, seg_type))
        return segments

    def add_ordered_list(self, items: List[str]) -> None:
        """Add an ordered list."""
        self.html_content += "<ol>\n"
        for item in items:
            self.html_content += f"<li>{item}</li>\n"
        self.html_content += "</ol>\n"

    def add_unordered_list(self, items: List[str]) -> None:
        """Add an unordered list."""
        self.html_content += "<ul>\n"
        for item in items:
            self.html_content += f"<li>{item}</li>\n"
        self.html_content += "</ul>\n"

    def add_code_block(self, code: str, language: str = "") -> None:
        """Add a code block (LTR direction)."""
        escaped_code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        self.html_content += f'<pre><code>{escaped_code}</code></pre>\n'

    def add_page_break(self) -> None:
        """Add a page break."""
        self.html_content += '<div class="page-break"></div>\n'

    def add_quote(self, text: str, attribution: str = "") -> None:
        """Add a block quote."""
        self.html_content += f'<blockquote><p>{text}</p>'
        if attribution:
            self.html_content += f'<p>— {attribution}</p>'
        self.html_content += '</blockquote>\n'

    def _add_footer_html(self) -> None:
        """Add footer with page numbers."""
        self.html_content += """
<div style="position: fixed; bottom: 0; left: 0; right: 0; text-align: center;
            font-size: 10pt; color: #666; border-top: 1px solid #ccc;
            padding: 8pt 0;">
  صفحه <span class="pageNum"></span>
</div>
"""

    def build_html(self) -> str:
        """Build complete HTML document."""
        return RTL_CSS + self.html_content + HTML_FOOTER

    def save(self) -> str:
        """Save the PDF and return the output path."""
        html = self.build_html()

        if WEASYPRINT_AVAILABLE:
            HTML(string=html).write_pdf(self.output_path)
        elif REPORTLAB_AVAILABLE:
            self._save_with_reportlab()
        else:
            # Fallback: save HTML and warn
            html_path = self.output_path.replace('.pdf', '.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Warning: No PDF library available. HTML saved to: {html_path}")
            print("Install weasyprint or reportlab for PDF generation.")
            return html_path

        return self.output_path

    def _save_with_reportlab(self) -> None:
        """Generate PDF using reportlab as fallback."""
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )

        # RTL-friendly styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            'PersianNormal',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=14,
            leading=20,
            alignment=TA_RIGHT,
            direction='rtl',
        ))
        styles.add(ParagraphStyle(
            'PersianHeading',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=28,
            alignment=TA_RIGHT,
            direction='rtl',
        ))

        story = []
        # Simple content generation from HTML
        # This is a simplified fallback
        story.append(Paragraph(self.title, styles['PersianHeading']))
        story.append(Spacer(1, 12))

        doc.build(story)


def create_sample_pdf(output_path: str = "sample_persian.pdf") -> str:
    """Create a sample Persian PDF demonstrating all features."""
    gen = PersianPDFGenerator(
        title="گزارش نمونه — تولید سند فارسی",
        output_path=output_path
    )

    # Title
    gen.add_title("گزارش نمونه تولید سند فارسی")

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
            {'text': 'hello@example.com', 'type': 'url'},
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
        0: ['persian', 'latin'],
        1: ['latin'],
        3: ['persian'],
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
        '```'
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
    gen.add_heading("پیوست", level=2)
    gen.add_paragraph("این بخش شامل اطلاعات تکمیلی است.")

    # Save
    return gen.save()


def main():
    parser = argparse.ArgumentParser(
        description="Generate RTL-aware Persian PDFs"
    )
    parser.add_argument("--output", "-o", default="document.pdf",
                        help="Output file path (default: document.pdf)")
    parser.add_argument("--title", "-t", default="",
                        help="Document title")
    parser.add_argument("--sample", action="store_true",
                        help="Generate a sample document")
    parser.add_argument("--config", "-c", help="Path to JSON config file")

    args = parser.parse_args()

    if args.sample:
        output = create_sample_pdf(args.output)
        print(f"Sample PDF created: {output}")
        return 0

    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        gen = PersianPDFGenerator(
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
        print(f"PDF created from config: {output}")
        return 0

    # Default: create sample
    output = create_sample_pdf(args.output)
    print(f"PDF created: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
