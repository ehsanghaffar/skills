# Persian Documents

Generate production-quality Persian documents (PDF, DOCX, Markdown) with correct RTL layout.

## Installation

Requires: `python-docx`, `weasyprint` (for PDF)

## Usage

Generate a DOCX: `python scripts/generate_docx.py`
Generate a PDF: `python scripts/generate_pdf.py`
Validate a document: `python scripts/validate_doc.py --file document.docx`

## Core principle

Persian documents are RTL rendering problems, not just Persian text in LTR layout. Always validate the rendered output.

See `SKILL.md` for full documentation.
