#!/usr/bin/env python3
"""
generate_resume.py — Generate a professional Persian RTL resume/CV.

Usage:
    python generate_resume.py --input resume.json --output resume.pdf
    python generate_resume.py --input resume.json --output resume.docx --format docx

Input: JSON file following references/resume-data-schema.md
Output: PDF (default, via WeasyPrint) or DOCX
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional, Any

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False


# =====================================================================
# Constants
# =====================================================================
PERSIAN_FONTS = {
    "Vazir": "Vazir, Vazirmatn, Tahoma, sans-serif",
    "Sahel": "Sahel, Tahoma, sans-serif",
    "Shabnam": "Shabnam, Tahoma, sans-serif",
    "Samim": "Samim, Tahoma, sans-serif",
}
PERSIAN_DOCX_FONT = "B Nazanin"
LATIN_DOCX_FONT = "Arial"
MONO_DOCX_FONT = "Consolas"


# =====================================================================
# HTML helpers
# =====================================================================

def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def html_style(font_name: str = "Vazir", font_size: int = 11,
               line_height: float = 1.6, margins_cm: float = 2.0) -> str:
    pf = PERSIAN_FONTS.get(font_name, PERSIAN_FONTS["Vazir"])
    return f"""
    @page {{
      size: A4;
      margin: {margins_cm}cm {margins_cm}cm {margins_cm}cm {margins_cm}cm;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: {pf};
      direction: rtl;
      text-align: right;
      font-size: {font_size}pt;
      line-height: {line_height};
      color: #1a1a1a;
      margin: 0; padding: 0;
    }}
    .resume {{ max-width: 21cm; margin: 0 auto; }}

    .header {{
      text-align: right;
      margin-bottom: 18pt;
      border-bottom: 2.5pt solid #1a1a1a;
      padding-bottom: 12pt;
    }}
    .header .name {{ font-size: 22pt; font-weight: bold; margin: 0 0 4pt 0; }}
    .header .title {{ font-size: 13pt; color: #444; margin: 0; }}
    .header .contact {{ font-size: 10pt; color: #555; margin-top: 6pt; line-height: 1.5; }}
    .header .contact a {{ color: #333; text-decoration: none; unicode-bidi: isolate; }}

    .section {{ margin-bottom: 14pt; page-break-inside: avoid; }}
    .section h2 {{
      font-size: 14pt; font-weight: bold;
      border-bottom: 1pt solid #999;
      padding-bottom: 3pt; margin: 0 0 6pt 0;
    }}

    .entry-header {{ margin-bottom: 2pt; }}
    .entry-header .role {{ font-weight: bold; font-size: 11.5pt; }}
    .entry-header .dates {{ font-size: 10pt; color: #555; unicode-bidi: isolate; white-space: nowrap; }}
    .entry-header .company {{ font-style: italic; font-size: 11pt; }}

    ul {{ margin: 2pt 0 6pt 0; padding-right: 18pt; }}
    ul li {{ margin-bottom: 2pt; font-size: 10.5pt; }}
    .bullets {{ margin: 2pt 0 4pt 0; padding-right: 18pt; }}
    .bullets li {{ margin-bottom: 1.5pt; font-size: 10.5pt; }}
    .metric {{ font-weight: bold; color: #1a5276; }}

    .skill-category {{ margin-bottom: 4pt; }}
    .skill-category .cat-name {{ font-weight: bold; }}
    .skill-category .cat-items {{ font-size: 10.5pt; }}

    table {{ width: 100%; border-collapse: collapse; direction: rtl; margin: 6pt 0; font-size: 10.5pt; }}
    th {{ background: #f0f0f0; font-weight: bold; text-align: right; padding: 4pt 6pt; border-bottom: 1.5pt solid #999; }}
    td {{ padding: 3pt 6pt; border-bottom: 0.5pt solid #ddd; text-align: right; }}
    td.ltr, th.ltr {{ unicode-bidi: isolate; text-align: left; }}

    .ltr {{ unicode-bidi: isolate; }}
    code, .code {{ font-family: Consolas, monospace; font-size: 9.5pt; background: #f5f5f5; padding: 1pt 4pt; }}
    a {{ color: #2472a8; text-decoration: none; }}

    .page-break {{ page-break-before: always; }}
    .no-orphan {{ page-break-inside: avoid; }}

    .compact .section {{ margin-bottom: 8pt; }}
    .compact .bullets li {{ font-size: 10pt; margin-bottom: 1pt; }}
    .compact .header .name {{ font-size: 18pt; }}
    """


def build_html_modern(data: Dict[str, Any]) -> str:
    """Build a modern two-column RTL resume."""
    c = data.get("candidate", {})
    opts = data.get("options", {})
    font = opts.get("font", "Vazir")
    pf = PERSIAN_FONTS.get(font, PERSIAN_FONTS["Vazir"])
    sections = data.get("sections", [])
    order = {
        "experience": 0, "project": 1, "education": 2,
        "skills": 3, "certification": 4, "language": 5,
        "award": 6, "publication": 7, "achievement": 8,
    }
    sections = sorted(sections, key=lambda s: order.get(s.get("type", ""), 99))

    main_items = []
    sidebar_items = []
    for sec in sections:
        stype = sec.get("type", "")
        title = sec.get("title", "")
        if stype in ("skills", "language", "certification", "award"):
            sidebar_items.append(sec)
        else:
            main_items.append(sec)

    p = []
    p.append('<html lang="fa" dir="rtl">')
    p.append("<head><meta charset='utf-8'>")
    p.append(f"<style>{html_style(font, font_size=10.5, line_height=1.55, margins_cm=1.8)}</style>")
    p.append(
        """<style>
        .modern { display: flex; gap: 18pt; }
        .sidebar { width: 38%; }
        .main { width: 62%; }
        .resume > .header { border-bottom: none; margin-bottom: 10pt; }
        .resume > .header .name { font-size: 18pt; }
        .resume > .header .title { font-size: 11.5pt; }
        .resume > .header .contact { font-size: 9.5pt; margin-top: 4pt; }
        .modern .section { margin-bottom: 10pt; }
        .modern .section h2 { font-size: 12.5pt; margin: 0 0 4pt 0; }
        .modern .entry-header .role { font-size: 11pt; }
        .modern .bullets li { font-size: 10pt; }
        .sidebar-section { margin-bottom: 10pt; page-break-inside: avoid; }
        .sidebar-section h2 { font-size: 11pt; border-bottom: 0.8pt solid #999;
                             padding-bottom: 2pt; margin: 0 0 3pt 0; }
        .sidebar-section .skill-category { margin-bottom: 3pt; }
        .sidebar-section .cat-name { font-weight: bold; font-size: 10pt; }
        .sidebar-section .cat-items { font-size: 9.8pt; }
        .sidebar-section li { font-size: 10pt; margin-bottom: 1.5pt; }
        </style>
        """
    )
    p.append("</head><body>")
    p.append('<div class="resume">')
    p.append(f'<div class="header"><p class="name">{esc(c.get("name", ""))}</p>'
             f'<p class="title">{esc(c.get("title", ""))}</p>')

    contact = []
    for fld in ["phone", "email", "location"]:
        if c.get(fld):
            contact.append(esc(c[fld]))
    for fld in ["website", "github", "linkedin", "portfolio"]:
        val = c.get(fld, "").strip()
        if val:
            display = val if val.startswith(("http://", "https://")) else "https://" + val
            contact.append(f'<a class="ltr" href="{esc(display)}">{esc(val)}</a>')
    if contact:
        p.append(f'<p class="contact">{"  |  ".join(contact)}</p>')
    p.append("</div>")

    p.append('<div class="modern">')
    p.append('<div class="main">')
    if c.get("summary"):
        p.append('<div class="section"><p>' + esc(c["summary"]) + '</p></div>')
    for sec in main_items:
        stype = sec.get("type", "")
        title = sec.get("title", "")
        items = sec.get("items", [])
        categories = sec.get("categories", [])
        if stype == "skills":
            continue
        if not items and not categories:
            continue
        p.append('<div class="section"><h2>' + esc(title) + '</h2>')
        if stype in ("experience", "project"):
            for item in items:
                role = esc(item.get("role", ""))
                company = esc(item.get("company", ""))
                location = esc(item.get("location", ""))
                start = esc(item.get("start", ""))
                end_display = "اکنون" if item.get("current", False) else esc(item.get("end", "اکنون"))
                p.append('<div class="entry-header no-orphan">')
                p.append(f'<span class="role">{role}</span>')
                p.append(f'<span class="company"> — {company}</span>')
                if location:
                    p.append(f'<span class="location"> ({location})</span>')
                p.append(f'<span class="dates">{start} – {end_display}</span>')
                p.append("</div>")
                bullets = item.get("bullets", [])
                if bullets:
                    p.append('<ul class="bullets">')
                    for b in bullets:
                        if isinstance(b, dict):
                            pieces = []
                            for k in ("responsibility", "action", "outcome", "metric"):
                                if b.get(k):
                                    v = esc(b[k])
                                    if k == "metric":
                                        v = f'<span class="metric">{v}</span>'
                                    elif k == "outcome":
                                        v = f'<b>{v}</b>'
                                    pieces.append(v)
                            txt = " → ".join(pieces)
                        else:
                            txt = esc(b)
                        if txt:
                            p.append(f"<li>{txt}</li>")
                    p.append("</ul>")
                techs = item.get("technologies", [])
                if techs:
                    tech_str = ", ".join(esc(t) for t in techs)
                    p.append(f'<p style="font-size:9.5pt;color:#555;margin:2pt 0 0 0;">'
                             f'<span class="ltr">{tech_str}</span></p>')
        elif stype == "education":
            for item in items:
                degree = esc(item.get("degree", ""))
                inst = esc(item.get("institution", ""))
                start = esc(item.get("start", ""))
                end = esc(item.get("end", ""))
                gpa = esc(item.get("gpa", ""))
                p.append('<div class="entry-header no-orphan">')
                p.append(f'<span class="role">{degree}</span>')
                p.append(f'<span class="company"> — {inst}</span>')
                if start or end:
                    p.append(f'<span class="dates">{start} – {end}</span>')
                if gpa:
                    p.append(f'<span style="font-size:9.8pt;color:#555;"> (معدل: {gpa})</span>')
                p.append("</div>")
        elif stype in ("certification", "award"):
            p.append('<ul class="bullets">')
            for item in items:
                if isinstance(item, dict):
                    name = esc(item.get("name", ""))
                    extra = esc(item.get("issuer", item.get("level", item.get("date", ""))))
                    date = esc(item.get("date", ""))
                    parts = [name]
                    if extra and extra != name:
                        parts.append(extra)
                    if date:
                        parts.append(f"({date})")
                    txt = " — ".join(parts)
                else:
                    txt = esc(item)
                p.append(f"<li>{txt}</li>")
            p.append("</ul>")
        elif stype == "achievement":
            p.append('<ul class="bullets">')
            for item in items:
                if isinstance(item, dict):
                    pieces = []
                    if item.get("title"):
                        pieces.append(esc(item["title"]))
                    if item.get("desc"):
                        pieces.append(esc(item["desc"]))
                    txt = " — ".join(pieces)
                else:
                    txt = esc(item)
                p.append(f"<li>{txt}</li>")
            p.append("</ul>")
        p.append("</div>")
    p.append("</div>")

    p.append('<div class="sidebar">')
    for sec in sidebar_items:
        stype = sec.get("type", "")
        title = sec.get("title", "")
        items = sec.get("items", [])
        categories = sec.get("categories", [])
        p.append('<div class="sidebar-section"><h2>' + esc(title) + '</h2>')
        if stype == "skills":
            for cat in categories:
                cat_name = esc(cat.get("name", ""))
                cat_items = ", ".join(esc(i) for i in cat.get("items", []))
                p.append('<div class="skill-category">'
                         f'<span class="cat-name">{cat_name}:</span> '
                         f'<span class="cat-items">{cat_items}</span></div>')
        elif stype in ("certification", "language", "award"):
            p.append('<ul class="bullets">')
            for item in items:
                if isinstance(item, dict):
                    name = esc(item.get("name", ""))
                    extra = esc(item.get("issuer", item.get("level", item.get("date", ""))))
                    date = esc(item.get("date", ""))
                    parts = [name]
                    if extra and extra != name:
                        parts.append(extra)
                    if date:
                        parts.append(f"({date})")
                    txt = " — ".join(parts)
                else:
                    txt = esc(item)
                p.append(f"<li>{txt}</li>")
            p.append("</ul>")
        else:
            p.append("<ul>")
            for item in items:
                p.append(f"<li>{esc(str(item))}</li>")
            p.append("</ul>")
        p.append("</div>")
    p.append("</div>")

    p.append("</div></div></body></html>")
    return "\n".join(p)


def build_html(data: Dict[str, Any]) -> str:
    """Build the resume as an RTL HTML document for WeasyPrint."""
    c = data.get("candidate", {})
    opts = data.get("options", {})
    font = opts.get("font", "Vazir")
    target = opts.get("targetRole", "")

    p = []
    p.append('<html lang="fa" dir="rtl">')
    p.append("<head><meta charset='utf-8'>")
    p.append(f"<style>{html_style(font)}</style>")
    p.append("</head><body>")
    p.append('<div class="resume">')

    # Header
    p.append('<div class="header">')
    p.append(f'<p class="name">{esc(c.get("name", ""))}</p>')
    p.append(f'<p class="title">{esc(c.get("title", ""))}</p>')
    contact = []
    for fld in ["phone", "email", "location"]:
        if c.get(fld):
            contact.append(esc(c[fld]))
    for fld in ["website", "github", "linkedin", "portfolio"]:
        val = c.get(fld, "").strip()
        if val:
            display = val if val.startswith(("http://", "https://")) else "https://" + val
            contact.append(f'<a class="ltr" href="{esc(display)}">{esc(val)}</a>')
    if contact:
        p.append(f'<p class="contact">{"  |  ".join(contact)}</p>')
    p.append("</div>")

    # Summary
    if c.get("summary"):
        p.append('<div class="section">')
        p.append(f'<p>{esc(c["summary"])}</p>')
        p.append("</div>")

    if target:
        p.append(f'<p style="font-size:10pt;color:#666;margin:0 0 6pt 0;">'
                 f'هدف شغلی: {esc(target)}</p>')

    # Sections in priority order
    order = {"experience": 0, "project": 1, "education": 2,
             "skills": 3, "certification": 4, "language": 5,
             "award": 6, "publication": 7, "achievement": 8}
    sections = sorted(data.get("sections", []),
                      key=lambda s: order.get(s.get("type", ""), 99))

    for sec in sections:
        stype = sec.get("type", "")
        title = sec.get("title", "")
        items = sec.get("items", [])
        categories = sec.get("categories", [])

        if stype == "skills":
            p.append('<div class="section">')
            p.append(f'<h2>{esc(title)}</h2>')
            for cat in categories:
                cat_name = esc(cat.get("name", ""))
                cat_items = ", ".join(esc(i) for i in cat.get("items", []))
                p.append(f'<div class="skill-category">'
                         f'<span class="cat-name">{cat_name}:</span> '
                         f'<span class="cat-items">{cat_items}</span></div>')
            p.append("</div>")
            continue

        if not items and not categories:
            continue

        p.append('<div class="section">')
        p.append(f'<h2>{esc(title)}</h2>')

        if stype in ("experience", "project"):
            for item in items:
                role = esc(item.get("role", ""))
                company = esc(item.get("company", ""))
                location = esc(item.get("location", ""))
                start = esc(item.get("start", ""))
                end_display = "اکنون" if item.get("current", False) else esc(item.get("end", "اکنون"))

                p.append('<div class="entry-header no-orphan">')
                p.append(f'<span class="role">{role}</span>')
                p.append(f'<span class="company"> — {company}</span>')
                if location:
                    p.append(f'<span class="location"> ({location})</span>')
                p.append(f'<span class="dates">{start} – {end_display}</span>')
                p.append("</div>")

                bullets = item.get("bullets", [])
                if bullets:
                    p.append('<ul class="bullets">')
                    for b in bullets:
                        if isinstance(b, dict):
                            pieces = []
                            for k in ("responsibility", "action", "outcome", "metric"):
                                if b.get(k):
                                    v = esc(b[k])
                                    if k == "metric":
                                        v = f'<span class="metric">{v}</span>'
                                    elif k == "outcome":
                                        v = f'<b>{v}</b>'
                                    pieces.append(v)
                            txt = " → ".join(pieces)
                        else:
                            txt = esc(b)
                        if txt:
                            p.append(f"<li>{txt}</li>")
                    p.append("</ul>")

                techs = item.get("technologies", [])
                if techs:
                    tech_str = ", ".join(esc(t) for t in techs)
                    p.append(f'<p style="font-size:10pt;color:#555;'
                             f'margin:2pt 0 0 0;"><span class="ltr">{tech_str}</span></p>')

        elif stype == "education":
            for item in items:
                degree = esc(item.get("degree", ""))
                inst = esc(item.get("institution", ""))
                start = esc(item.get("start", ""))
                end = esc(item.get("end", ""))
                gpa = esc(item.get("gpa", ""))
                p.append('<div class="entry-header no-orphan">')
                p.append(f'<span class="role">{degree}</span>')
                p.append(f'<span class="company"> — {inst}</span>')
                if start or end:
                    p.append(f'<span class="dates">{start} – {end}</span>')
                if gpa:
                    p.append(f'<span style="font-size:10pt;color:#555;"> (معدل: {gpa})</span>')
                p.append("</div>")

        elif stype in ("certification", "language", "award"):
            for item in items:
                if isinstance(item, dict):
                    name = esc(item.get("name", ""))
                    extra = esc(item.get("issuer", item.get("level", item.get("date", ""))))
                    date = esc(item.get("date", ""))
                    parts = [name]
                    if extra and extra != name:
                        parts.append(extra)
                    if date:
                        parts.append(f"({date})")
                    txt = " — ".join(parts)
                else:
                    txt = esc(item)
                p.append(f"<li>{txt}</li>")

        elif stype == "achievement":
            for item in items:
                if isinstance(item, dict):
                    pieces = []
                    if item.get("title"):
                        pieces.append(esc(item["title"]))
                    if item.get("desc"):
                        pieces.append(esc(item["desc"]))
                    txt = " — ".join(pieces)
                else:
                    txt = esc(item)
                p.append(f"<li>{txt}</li>")

        p.append("</div>")

    p.append("</div></body></html>")
    return "\n".join(p)


# =====================================================================
# DOCX generator
# =====================================================================

class ResumeDocxGenerator:
    """Generate a DOCX resume with RTL direction."""

    def __init__(self, output_path: str = "resume.docx", font: str = "Vazir", template: str = "classic"):
        self.doc = Document()
        self.output_path = output_path
        self.template = template
        self._setup(font)

    def _setup(self, font: str) -> None:
        section = self.doc.sections[0]
        section.direction = 1  # RTL
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2)

        style = self.doc.styles['Normal']
        style.font.name = PERSIAN_DOCX_FONT
        style.font.size = Pt(11)
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        style.paragraph_format.line_spacing = 1.5
        rPr = style.element.get_or_add_rPr()
        rFonts = parse_xml(
            f'<w:rFonts {nsdecls("w")} w:ascii="{PERSIAN_DOCX_FONT}" '
            f'w:hAnsi="{PERSIAN_DOCX_FONT}" w:cs="{PERSIAN_DOCX_FONT}" '
            f'w:fareast="{PERSIAN_DOCX_FONT}"/>'
        )
        rPr.insert(0, rFonts)

    def _bidi(self, element, direction="rtl"):
        pPr = element.get_or_add_pPr()
        bidi = parse_xml(
            f'<w:bidi {nsdecls("w")} w:val="1"/>'
            if direction == "rtl"
            else f'<w:bidi {nsdecls("w")} w:val="0"/>'
        )
        for existing in pPr.findall(qn('w:bidi')):
            pPr.remove(existing)
        pPr.append(bidi)

    def _para(self, text="", mixed=None, alignment="right",
              bold=False, italic=False, size=11, direction="rtl"):
        para = self.doc.add_paragraph()
        self._bidi(para._element, direction)
        if mixed:
            for text_seg, seg_type in mixed:
                run = para.add_run(text_seg)
                run.font.size = Pt(size)
                run.bold = bold
                run.italic = italic
                if seg_type in ("latin", "url"):
                    run.font.name = LATIN_DOCX_FONT
                elif seg_type == "mono":
                    run.font.name = MONO_DOCX_FONT
                    run.font.size = Pt(10)
                else:
                    run.font.name = PERSIAN_DOCX_FONT
        else:
            run = para.add_run(text)
            run.font.name = PERSIAN_DOCX_FONT
            run.font.size = Pt(size)
            run.bold = bold
            run.italic = italic
        align_map = {
            "right": WD_ALIGN_PARAGRAPH.RIGHT,
            "left": WD_ALIGN_PARAGRAPH.LEFT,
            "center": WD_ALIGN_PARAGRAPH.CENTER,
            "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
        }
        para.alignment = align_map.get(alignment, WD_ALIGN_PARAGRAPH.RIGHT)
        return para

    def _heading(self, text, level=2):
        h = self.doc.add_heading(text, level=level)
        self._bidi(h._element)
        for run in h.runs:
            run.font.name = PERSIAN_DOCX_FONT
        return h

    def build(self, data: Dict[str, Any]) -> str:
        c = data.get("candidate", {})
        opts = data.get("options", {})
        target = opts.get("targetRole", "")

        if self.template == "modern":
            return self._build_modern(data)

        # Classic template
        self._para(c.get("name", ""), bold=True, size=18, alignment="center")
        self._para(c.get("title", ""), size=12, alignment="center")
        contact = []
        for fld in ["phone", "email", "location"]:
            if c.get(fld):
                contact.append(c[fld])
        for fld in ["website", "github", "linkedin", "portfolio"]:
            if c.get(fld):
                contact.append(c[fld])
        if contact:
            self._para("  |  ".join(contact), size=9, alignment="center")
        if target:
            self._para(f"هدف شغلی: {target}", size=10, alignment="center", italic=True)
        if c.get("summary"):
            self._heading("خلاصه حرفه‌ای", level=2)
            self._para(c["summary"])

        # Sections in priority order
        order = {"experience": 0, "project": 1, "education": 2,
                 "skills": 3, "certification": 4, "language": 5,
                 "award": 6, "publication": 7, "achievement": 8}
        sections = sorted(data.get("sections", []),
                          key=lambda s: order.get(s.get("type", ""), 99))

        for sec in sections:
            stype = sec.get("type", "")
            title = sec.get("title", "")
            items = sec.get("items", [])
            categories = sec.get("categories", [])

            if stype == "skills":
                self._heading(title, level=2)
                for cat in categories:
                    self._para(f"{cat.get('name', '')}: "
                               + ", ".join(cat.get("items", [])))
                continue

            if not items:
                continue

            self._heading(title, level=2)

            if stype in ("experience", "project"):
                for item in items:
                    role = item.get("role", "")
                    company = item.get("company", "")
                    start = item.get("start", "")
                    end = "اکنون" if item.get("current", False) else item.get("end", "")
                    loc = item.get("location", "")
                    header = f"{role} — {company}  |  {start} – {end}"
                    if loc:
                        header += f"  ({loc})"
                    self._para(header, bold=True, size=11)
                    for b in item.get("bullets", []):
                        if isinstance(b, dict):
                            pieces = []
                            for k in ("responsibility", "action", "outcome", "metric"):
                                if b.get(k):
                                    pieces.append(b[k])
                            txt = " → ".join(pieces)
                        else:
                            txt = b
                        self._para(f"• {txt}", size=10)
                    if item.get("technologies"):
                        self._para(", ".join(item["technologies"]), size=9)

            elif stype == "education":
                for item in items:
                    line = f"{item.get('degree', '')} — {item.get('institution', '')}"
                    if item.get("start") or item.get("end"):
                        line += f"  |  {item.get('start', '')} – {item.get('end', '')}"
                    if item.get("gpa"):
                        line += f"  (معدل: {item['gpa']})"
                    self._para(line, size=11)

            elif stype == "certification":
                for item in items:
                    name = item.get("name", item) if isinstance(item, dict) else item
                    issuer = item.get("issuer", "") if isinstance(item, dict) else ""
                    date = item.get("date", "") if isinstance(item, dict) else ""
                    line = name
                    if issuer:
                        line += f" — {issuer}"
                    if date:
                        line += f" ({date})"
                    self._para(f"• {line}", size=10)

            elif stype == "language":
                for item in items:
                    lang = item.get("name", item) if isinstance(item, dict) else item
                    lvl = item.get("level", "") if isinstance(item, dict) else ""
                    self._para(f"• {lang}" + (f" — {lvl}" if lvl else ""), size=10)

            elif stype == "award":
                for item in items:
                    name = item.get("name", item) if isinstance(item, dict) else item
                    date = item.get("date", "") if isinstance(item, dict) else ""
                    line = name + (f" ({date})" if date else "")
                    self._para(f"• {line}", size=10)

            elif stype == "achievement":
                for item in items:
                    if isinstance(item, dict):
                        line = item.get("title", "")
                        if item.get("desc"):
                            line += f" — {item['desc']}"
                    else:
                        line = item
                    self._para(f"• {line}", size=10)

        self.doc.save(self.output_path)
        return self.output_path

    def _build_modern(self, data: Dict[str, Any]) -> str:
        """Build a modern two-column DOCX resume."""
        c = data.get("candidate", {})
        opts = data.get("options", {})
        target = opts.get("targetRole", "")

        # Header
        self._para(c.get("name", ""), bold=True, size=18, alignment="center")
        self._para(c.get("title", ""), size=12, alignment="center")
        contact = []
        for fld in ["phone", "email", "location"]:
            if c.get(fld):
                contact.append(c[fld])
        for fld in ["website", "github", "linkedin", "portfolio"]:
            if c.get(fld):
                contact.append(c[fld])
        if contact:
            self._para("  |  ".join(contact), size=9, alignment="center")
        if target:
            self._para(f"هدف شغلی: {target}", size=10, alignment="center", italic=True)

        sections = data.get("sections", [])
        order = {
            "experience": 0, "project": 1, "education": 2,
            "skills": 3, "certification": 4, "language": 5,
            "award": 6, "publication": 7, "achievement": 8,
        }
        sections = sorted(sections, key=lambda s: order.get(s.get("type", ""), 99))

        main_sections = []
        sidebar_sections = []
        for sec in sections:
            if sec.get("type") in ("skills", "language", "certification", "award"):
                sidebar_sections.append(sec)
            else:
                main_sections.append(sec)

        for sec in main_sections:
            stype = sec.get("type", "")
            title = sec.get("title", "")
            items = sec.get("items", [])
            categories = sec.get("categories", [])
            if stype == "skills":
                continue
            if not items and not categories:
                continue
            self._heading(title, level=2)
            if stype in ("experience", "project"):
                for item in items:
                    role = item.get("role", "")
                    company = item.get("company", "")
                    start = item.get("start", "")
                    end = "اکنون" if item.get("current", False) else item.get("end", "")
                    loc = item.get("location", "")
                    header = f"{role} — {company}  |  {start} – {end}"
                    if loc:
                        header += f"  ({loc})"
                    self._para(header, bold=True, size=11)
                    for b in item.get("bullets", []):
                        if isinstance(b, dict):
                            pieces = []
                            for k in ("responsibility", "action", "outcome", "metric"):
                                if b.get(k):
                                    pieces.append(b[k])
                            txt = " → ".join(pieces)
                        else:
                            txt = b
                        self._para(f"• {txt}", size=10)
                    if item.get("technologies"):
                        self._para(", ".join(item["technologies"]), size=9)
            elif stype == "education":
                for item in items:
                    line = f"{item.get('degree', '')} — {item.get('institution', '')}"
                    if item.get("start") or item.get("end"):
                        line += f"  |  {item.get('start', '')} – {item.get('end', '')}"
                    if item.get("gpa"):
                        line += f"  (معدل: {item['gpa']})"
                    self._para(line, size=11)
            elif stype in ("certification", "award"):
                for item in items:
                    if isinstance(item, dict):
                        name = item.get("name", "")
                        extra = item.get("issuer", item.get("level", item.get("date", "")))
                        date = item.get("date", "")
                        parts = [name, extra, f"({date})" if date else ""]
                        parts = [p for p in parts if p]
                        line = " — ".join(parts)
                    else:
                        line = str(item)
                    self._para(f"• {line}", size=10)

        for sec in sidebar_sections:
            stype = sec.get("type", "")
            title = sec.get("title", "")
            items = sec.get("items", [])
            categories = sec.get("categories", [])
            self._heading(title, level=2)
            if stype == "skills":
                for cat in categories:
                    self._para(f"{cat.get('name', '')}: "
                               + ", ".join(cat.get("items", [])))
            elif stype in ("certification", "language", "award"):
                for item in items:
                    if isinstance(item, dict):
                        name = item.get("name", "")
                        extra = item.get("issuer", item.get("level", item.get("date", "")))
                        date = item.get("date", "")
                        parts = [name, extra, f"({date})" if date else ""]
                        parts = [p for p in parts if p]
                        line = " — ".join(parts)
                    else:
                        line = str(item)
                    self._para(f"• {line}", size=10)
            else:
                for item in items:
                    self._para(f"• {item}", size=10)

        self.doc.save(self.output_path)
        return self.output_path


# =====================================================================
# Main
# =====================================================================

def generate_resume(input_path: str, output_path: str,
                    fmt: str = "pdf") -> str:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ensure_dir(output_path)

    if fmt == "docx":
        template = data.get("options", {}).get("template", "classic")
        gen = ResumeDocxGenerator(
            output_path,
            data.get("options", {}).get("font", "Vazir"),
            template=template,
        )
        return gen.build(data)

    if not WEASYPRINT_AVAILABLE:
        print("WeasyPrint not available; falling back to DOCX", file=sys.stderr)
        gen = ResumeDocxGenerator(output_path.replace(".pdf", ".docx"),
                                  data.get("options", {}).get("font", "Vazir"))
        return gen.build(data)

    template = data.get("options", {}).get("template", "classic")
    if template == "modern":
        html = build_html_modern(data)
    else:
        html = build_html(data)
    HTML(string=html).write_pdf(output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate a professional Persian RTL resume/CV"
    )
    parser.add_argument("--input", "-i", required=True,
                        help="Path to JSON resume data")
    parser.add_argument("--output", "-o", required=True,
                        help="Output file (.pdf or .docx)")
    parser.add_argument("--format", "-f", choices=["pdf", "docx"],
                        default=None,
                        help="Output format (default: from extension)")
    args = parser.parse_args()

    fmt = args.format
    if not fmt:
        fmt = "docx" if args.output.endswith(".docx") else "pdf"

    output = generate_resume(args.input, args.output, fmt)
    print(f"Resume generated: {output} ({fmt})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
