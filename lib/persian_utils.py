#!/usr/bin/env python3
"""Shared Persian text utilities used across skills."""

import re
from typing import List, Dict

# Unicode ranges
PERSIAN_RANGE = re.compile(r'[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]')
LATIN_RANGE = re.compile(r'[A-Za-z]')
PERSIAN_DIGITS = re.compile(r'[۰-۹]')
LATIN_DIGITS = re.compile(r'[0-9]')
ZWNJ = '‌'
LRM = '‎'
RLM = '‏'

# Arabic forms that should be Persian in text
WRONG_GLYPHS = {'ي': 'ی', 'ك': 'ک'}


def is_persian(text: str) -> bool:
    """Check if text contains Persian/Arabic script."""
    return bool(PERSIAN_RANGE.search(text))


def has_latin(text: str) -> bool:
    """Check if text contains Latin letters."""
    return bool(LATIN_RANGE.search(text))


def normalize_persian_digits(text: str) -> str:
    """Convert Western digits (0-9) to Persian digits (۰-۹)."""
    mapping = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return text.translate(mapping)


def normalize_latin_digits(text: str) -> str:
    """Convert Persian digits (۰-۹) to Western digits (0-9)."""
    mapping = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    return text.translate(mapping)


def fix_glyphs(text: str) -> str:
    """Replace Arabic glyph forms with Persian equivalents."""
    for wrong, correct in WRONG_GLYPHS.items():
        text = text.replace(wrong, correct)
    return text


def check_rtl_direction(text: str) -> List[Dict]:
    """Check for LTR-forcing patterns in Persian text."""
    issues = []
    if re.search(r'dir\s*=\s*["\']ltr["\']', text, re.IGNORECASE):
        issues.append({
            "check": "rtl_direction",
            "severity": "error",
            "message": "Explicit LTR direction found in RTL document",
        })
    for m in re.finditer(LRM, text):
        issues.append({
            "check": "rtl_direction",
            "severity": "warning",
            "message": f"LRM mark at position {m.start()}",
        })
    return issues


def check_zwnj_usage(text: str) -> List[Dict]:
    """Check for ZWNJ placement issues."""
    issues = []
    words = text.split()
    for word in words:
        if word.startswith(ZWNJ):
            issues.append({
                "check": "zwnj_placement",
                "severity": "warning",
                "message": f"ZWNJ at start of word: {word}",
            })
    if ZWNJ in text and len(text.strip()) == 1:
        issues.append({
            "check": "zwnj_isolation",
            "severity": "warning",
            "message": "Isolated ZWNJ character",
        })
    return issues
