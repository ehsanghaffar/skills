# Persian Resume Generator

Generate professional Persian RTL resumes/CVs.

## Installation

No extra dependencies beyond the skill's scripts.

## Usage

1. Prepare your career data as JSON (see `references/resume-data-schema.md`)
2. Generate: `python scripts/generate_resume.py --input resume.json --output resume.pdf`
3. Validate: `python scripts/validate_resume.py --input resume.json --output resume.pdf`

## Templates

- **classic** — Single-column layout
- **modern** — Two-column sidebar layout

## Quality checks

The validator checks: RTL direction, mixed-direction content, tech terms, URLs/emails, date consistency, version numbers, structure, file integrity.

See `SKILL.md` for full documentation.
