#!/usr/bin/env python3
"""Shared validation utilities for URLs, emails, version numbers."""

import re
from typing import List, Dict

RE_URL = re.compile(r'https?://[^\s]+|www\.[^\s]+')
RE_EMAIL = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
RE_VERSION = re.compile(r'\bv?\d+\.\d+(?:\.\d+)*\b')


def validate_url(url: str) -> Dict:
    """Check if a URL has a valid protocol."""
    if url.startswith(('http://', 'https://', 'www.')):
        return {"valid": True, "url": url}
    return {"valid": False, "url": url, "error": "Missing protocol"}


def validate_email(email: str) -> Dict:
    """Check if an email address looks valid."""
    if RE_EMAIL.fullmatch(email):
        return {"valid": True, "email": email}
    return {"valid": False, "email": email, "error": "Invalid email format"}


def validate_version(version: str) -> Dict:
    """Check if a version string is well-formed."""
    ver = version.lstrip('v')
    parts = ver.split('.')
    if all(p.isdigit() for p in parts):
        return {"valid": True, "version": version}
    return {"valid": False, "version": version, "error": "Invalid version format"}


def find_urls(text: str) -> List[str]:
    """Extract all URLs from text."""
    return RE_URL.findall(text)


def find_emails(text: str) -> List[str]:
    """Extract all email addresses from text."""
    return RE_EMAIL.findall(text)
