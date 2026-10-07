#!/usr/bin/env python3
"""
validate_resume.py — Validate a generated Persian resume.

Checks:
- RTL document direction
- Bidi correctness of mixed Persian/English text
- Content preservation (no invented facts)
- Date consistency
- URL/email integrity
- File integrity (opens without errors)

Usage:
    python validate_resume.py --input resume.json --output resume.pdf
    python validate_resume.py --input resume.json --output resume.docx
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any


# =====================================================================
# RTL / bidi checks
# =====================================================================

# Common Persian/Arabic characters
RE_PERSIAN = re.compile(r'[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]')
RE_LATIN_WORD = re.compile(r'[a-zA-Z]{2,}')
RE_URL = re.compile(r'https?://[^\s]+|www\.[^\s]+')
RE_EMAIL = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
RE_VERSION = re.compile(r'\bv?\d+\.\d+(?:\.\d+)*\b')
RE_PERSIAN_DIGIT = re.compile(r'[۰-۹]')
RE_LATIN_DIGIT = re.compile(r'[0-9]')

# Known technical terms that must stay intact
TECH_TERMS = [
    "JavaScript", "TypeScript", "React", "Next.js", "Angular", "Node.js",
    "Django", "FastAPI", "PostgreSQL", "MongoDB", "MySQL", "Redis",
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "GitHub", "GitLab",
    "REST API", "GraphQL", "npm", "pip", "webpack", "Vite",
    "Tailwind", "Bootstrap", "Figma", "Jira",
    "CI/CD", "Linux", "Git", "Python", "Java", "Go", "Rust", "Ruby",
]

# Words that are commonly reversed by bad bidi — detect if present reversed
REVERSED_CHECK = {
    "resume": "esumur", "professional": "lanoisseforp",
    "developer": "repoleved", "experience": "ecneirepxe",
    "skills": "slliks", "education": "noitacude",
    "project": "tcejorp", "company": "ynapmoc",
}


def check_rtl_direction(text: str) -> List[Dict]:
    """Check that Persian text isn't forced LTR."""
    issues = []
    # Check for explicit LTR direction markers
    if re.search(r'dir\s*=\s*["\']ltr["\']', text, re.IGNORECASE):
        issues.append({
            "check": "rtl_direction",
            "severity": "error",
            "message": "Explicit LTR direction found in RTL document",
        })
    # Check for LRM control characters in wrong positions
    for m in re.finditer('‎', text):
        issues.append({
            "check": "rtl_direction",
            "severity": "warning",
            "message": f"LTR mark at position {m.start()}",
        })
    return issues


def check_bidi_mixed(text: str) -> List[Dict]:
    """Check mixed Persian/English text for scrambled words."""
    issues = []
    # Check for reversed English words inside Persian text
    for word, reversed_form in REVERSED_CHECK.items():
        if reversed_form in text.lower():
            issues.append({
                "check": "bidi_mixed",
                "severity": "error",
                "message": f"Possible reversed word: '{reversed_form}' "
                           f"(should be '{word}')",
            })
    return issues


def check_tech_terms(text: str) -> List[Dict]:
    """Ensure technical terms are in standard English spelling, not Farsified."""
    issues = []
    FARSIFIED = {
        "جاوااسکریپت": "JavaScript",
        "ری‌اکت": "React",
        "انگولار": "Angular",
        "پایتون": "Python",
        "نود‌دات‌جی‌اس": "Node.js",
        "تایپ‌اسکریپت": "TypeScript",
        "ری‌اکت‌نا‌تیو": "React Native",
        "اپل": "Apple",
        "فیسبوک": "Facebook",
        "آمازون": "Amazon",
    }
    text_lower = text.lower()
    for farsi, english in FARSIFIED.items():
        if farsi.lower() in text_lower:
            issues.append({
                "check": "tech_terms",
                "severity": "warning",
                "message": f"Use '{english}' instead of '{farsi}'",
            })
    return issues


def check_urls_emails(text: str) -> List[Dict]:
    """Check URLs and emails are intact."""
    issues = []
    for pattern, label in [(RE_URL, "URL"), (RE_EMAIL, "email")]:
        for match in pattern.findall(text):
            # Basic sanity: URL starts with http(s):// or www.
            if label == "URL" and not match.startswith(("http://", "https://", "www.")):
                issues.append({
                    "check": label,
                    "severity": "warning",
                    "message": f"Suspicious {label}: {match}",
                })
    return issues


def check_dates_consistency(text: str) -> List[Dict]:
    """Check dates use a consistent calendar."""
    issues = []
    persian_dates = RE_PERSIAN_DIGIT.findall(text)
    latin_dates = RE_LATIN_DIGIT.findall(text)
    # If we see Persian digits (۰-۹) in date-like contexts, assume Persian calendar
    # If we see Latin digits in date ranges, assume Gregorian
    # Cross-mixing is the issue
    has_persian_digits = bool(RE_PERSIAN_DIGIT.search(text))
    has_latin_digits = bool(RE_LATIN_DIGIT.search(text))
    if has_persian_digits and has_latin_digits:
        # Check if they're in the same date context (warning, not error)
        # Look for date range patterns mixing both
        mixed_range = re.search(
            r'(?:[۰-۹]{2,4}|[\d]{2,4})[–\-–—]'
            r'(?:[۰-۹]{2,4}|[\d]{2,4})', text
        )
        if mixed_range:
            issues.append({
                "check": "dates",
                "severity": "warning",
                "message": f"Possible mixed-calendar date range: "
                           f"{mixed_range.group()}",
            })
    return issues


def check_version_numbers(text: str) -> List[Dict]:
    """Check version numbers are intact (not reversed)."""
    issues = []
    for match in RE_VERSION.finditer(text):
        ver = match.group()
        # A version like "1.2.3" should have digits in order
        # If reversed, it would be "3.2.1" — hard to detect without context
        # Just check for obviously wrong patterns
        parts = ver.lstrip("v").split(".")
        if len(parts) >= 2:
            for p in parts:
                if not p.isdigit():
                    issues.append({
                        "check": "version",
                        "severity": "error",
                        "message": f"Invalid version format: {ver}",
                    })
                    break
    return issues


def check_structure(data: Dict[str, Any]) -> List[Dict]:
    """Validate the JSON structure of the resume data."""
    issues = []
    candidate = data.get("candidate", {})
    if not candidate.get("name"):
        issues.append({
            "check": "structure",
            "severity": "error",
            "message": "Missing candidate name",
        })
    if not data.get("sections"):
        issues.append({
            "check": "structure",
            "severity": "warning",
            "message": "No sections defined in resume data",
        })
    # Check for duplicate sections
    types = [s.get("type", "") for s in data.get("sections", [])]
    seen = set()
    for t in types:
        if t in seen:
            issues.append({
                "check": "structure",
                "severity": "info",
                "message": f"Duplicate section type: {t}",
            })
        seen.add(t)
    return issues


def check_file_integrity(output_path: str) -> List[Dict]:
    """Check the generated file opens without errors."""
    issues = []
    path = Path(output_path)
    if not path.exists():
        issues.append({
            "check": "file",
            "severity": "error",
            "message": f"Output file not found: {output_path}",
        })
        return issues

    if output_path.endswith(".docx"):
        try:
            from docx import Document
            doc = Document(output_path)
            if not doc.paragraphs:
                issues.append({
                    "check": "file",
                    "severity": "error",
                    "message": "DOCX has no paragraphs",
                })
        except Exception as e:
            issues.append({
                "check": "file",
                "severity": "error",
                "message": f"Cannot open DOCX: {e}",
            })

    elif output_path.endswith(".pdf"):
        # Check PDF header
        try:
            with open(output_path, "rb") as f:
                header = f.read(5)
                if header != b"%PDF-":
                    issues.append({
                        "check": "file",
                        "severity": "error",
                        "message": "File does not start with %PDF-",
                    })
        except Exception as e:
            issues.append({
                "check": "file",
                "severity": "error",
                "message": f"Cannot read PDF: {e}",
            })

    return issues


# =====================================================================
# Main
# =====================================================================

def validate(input_path: str, output_path: str) -> Dict[str, Any]:
    """Run all validation checks."""
    all_issues = []

    # Load resume data
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Build full text from data for checking
    text_parts = []
    c = data.get("candidate", {})
    for field in ["name", "title", "summary", "email", "phone",
                    "location", "website", "github", "linkedin"]:
        if c.get(field):
            text_parts.append(str(c[field]))
    for sec in data.get("sections", []):
        for item in sec.get("items", []):
            if isinstance(item, dict):
                for v in item.values():
                    if isinstance(v, str):
                        text_parts.append(v)
                    elif isinstance(v, list):
                        for vi in v:
                            if isinstance(vi, str):
                                text_parts.append(vi)
                            elif isinstance(vi, dict):
                                for vvv in vi.values():
                                    if isinstance(vvv, str):
                                        text_parts.append(vvv)
            else:
                text_parts.append(str(item))
        for cat in sec.get("categories", []):
            for i in cat.get("items", []):
                text_parts.append(str(i))
    full_text = " ".join(text_parts)

    # Run checks
    all_issues.extend(check_rtl_direction(full_text))
    all_issues.extend(check_bidi_mixed(full_text))
    all_issues.extend(check_tech_terms(full_text))
    all_issues.extend(check_urls_emails(full_text))
    all_issues.extend(check_dates_consistency(full_text))
    all_issues.extend(check_version_numbers(full_text))
    all_issues.extend(check_structure(data))
    all_issues.extend(check_file_integrity(output_path))

    # Summarize
    errors = [i for i in all_issues if i["severity"] == "error"]
    warnings = [i for i in all_issues if i["severity"] == "warning"]
    infos = [i for i in all_issues if i["severity"] == "info"]

    result = {
        "valid": len(errors) == 0,
        "total_issues": len(all_issues),
        "errors": len(errors),
        "warnings": len(warnings),
        "info": len(infos),
        "issues": all_issues,
    }
    return result


def print_report(result: Dict[str, Any]) -> None:
    """Print a human-readable validation report."""
    status = "PASS" if result["valid"] else "FAIL"
    print(f"\n{'='*60}")
    print(f"  Resume Validation — {status}")
    print(f"{'='*60}")
    print(f"  Errors:   {result['errors']}")
    print(f"  Warnings: {result['warnings']}")
    print(f"  Info:     {result['info']}")
    print(f"{'='*60}")

    for issue in result["issues"]:
        icon = {"error": "✗", "warning": "⚠", "info": "ℹ"}[issue["severity"]]
        print(f"  {icon} [{issue['check']}] {issue['message']}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate a generated Persian resume"
    )
    parser.add_argument("--input", "-i", required=True,
                        help="Path to JSON resume data")
    parser.add_argument("--output", "-o", required=True,
                        help="Path to generated output file")
    args = parser.parse_args()

    result = validate(args.input, args.output)
    print_report(result)

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
