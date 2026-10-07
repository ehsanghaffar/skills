#!/usr/bin/env python3
"""Shared date utilities for Persian/Gregorian calendar handling."""

from datetime import datetime


def to_jalali(date: datetime) -> str:
    """Convert a datetime to Jalali date string (YYYY/MM/DD)."""
    try:
        import jdatetime
        return jdatetime.date.fromgregorian(date=date).strftime('%Y/%m/%d')
    except ImportError:
        return date.strftime('%Y/%m/%d')


def to_gregorian(jalali_str: str) -> datetime:
    """Convert a Jalali date string to datetime."""
    try:
        import jdatetime
        parts = jalali_str.split('/')
        return jdatetime.date(int(parts[0]), int(parts[1]), int(parts[2])).togregorian()
    except ImportError:
        return datetime.strptime(jalali_str, '%Y/%m/%d')


def format_persian_date(dt: datetime) -> str:
    """Format date in Persian style: ۱۴۰۵/۰۷/۱۴."""
    jalali = to_jalali(dt)
    return normalize_persian_digits(jalali)


def normalize_persian_digits(text: str) -> str:
    """Convert Western digits to Persian digits."""
    mapping = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return text.translate(mapping)
