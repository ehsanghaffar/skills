#!/usr/bin/env python3
"""
check_persian.py — Automated enforcement pass for the telegram-persian-language skill.

This is NOT a translator. It is a last-line-of-defense linter meant to be run
on EVERY drafted Telegram message, not just long ones. It flags:
  - Latin-script words that survived outside code spans/blocks, URLs, and
    parenthetical asides (the skill's own convention for first-mention
    foreign names, e.g. "اوپن‌ای‌آی (OpenAI)")
  - Western (0-9) digits inside ordinary prose, which should normally be
    Persian digits (۰-۹), while leaving digits inside code/URLs alone

Two ways this is meant to be used:

1. Interactively, while drafting:
       python check_persian.py --file draft.txt

2. As a hard gate in an enforcement loop (see SKILL.md "اجرای خودکار و
   اجباری"): draft -> run this script -> if exit code is 1, revise the
   draft and run again -> only send once exit code is 0 (or remaining
   flags have been explicitly reviewed and are genuine exceptions).

Exit code 0 = clean. Exit code 1 = issues found. The final line of output
is always a machine-parseable "RESULT: CLEAN" or "RESULT: ISSUES=<n>" so a
calling agent/script can branch on it without re-parsing the human-readable
report above it.
"""

import argparse
import os
import re
import sys

# Matches fenced code blocks ```...``` (including language tag) and inline `code`
CODE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")

# Matches URLs and telegram-style entities we should never touch
URL_RE = re.compile(r"https?://\S+|www\.\S+|t\.me/\S+|@[A-Za-z0-9_]{4,}")

# Parenthetical asides — the skill's sanctioned spot for a first-mention
# foreign name/brand, e.g. "اوپن‌ای‌آی (OpenAI)". Content inside is exempted
# from the Latin-word check (but NOT from the digit check).
PAREN_CONTENT_RE = re.compile(r"\(([^()]*)\)")

# A "Latin word" worth flagging: 2+ Latin letters, not glued to Persian script
LATIN_WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-']{1,}")

# Western (ASCII) digits only — deliberately NOT \d, since \d also matches
# Persian (۰-۹) and Arabic-Indic (٠-٩) digits in Unicode mode, which must
# NOT be flagged.
WESTERN_DIGIT_RE = re.compile(r"[0-9]+")

PLACEHOLDER = "\uE000"  # private-use char used to blank out protected spans
DEFAULT_ALLOWLIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "allowlist.txt")


def load_allowlist(path):
    terms = set()
    if path and os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    terms.add(line.lower())
    return terms


def mask_protected_spans(text: str):
    """Replace code blocks, inline code, and URLs with placeholders so they
    are never flagged."""
    def _mask(pattern, s):
        def repl(m):
            return PLACEHOLDER * len(m.group(0))
        return pattern.sub(repl, s)

    masked = _mask(CODE_BLOCK_RE, text)
    masked = _mask(INLINE_CODE_RE, masked)
    masked = _mask(URL_RE, masked)
    return masked


def get_paren_ranges(text: str):
    return [(m.start(1), m.end(1)) for m in PAREN_CONTENT_RE.finditer(text)]


def inside_any(pos_start, pos_end, ranges):
    return any(r_start <= pos_start and pos_end <= r_end for r_start, r_end in ranges)


def find_issues(text: str, allowlist):
    masked = mask_protected_spans(text)
    paren_ranges = get_paren_ranges(masked)
    issues = []

    for m in LATIN_WORD_RE.finditer(masked):
        word = m.group(0)
        if word.lower() in allowlist:
            continue
        if inside_any(m.start(), m.end(), paren_ranges):
            continue
        issues.append(("latin_text", word, m.start()))

    for m in WESTERN_DIGIT_RE.finditer(masked):
        issues.append(("western_digit", m.group(0), m.start()))

    return issues


def report(text: str, issues):
    if not issues:
        print("✅ چیزی برای پرچم‌گذاری پیدا نشد — متن از نظر زبان و اعداد تمیز به نظر می‌رسد.")
        print("RESULT: CLEAN")
        return 0

    print(f"⚠️  {len(issues)} مورد برای بازبینی پیدا شد:\n")
    for kind, snippet, pos in issues:
        context = text[max(0, pos - 20):pos + len(snippet) + 20].replace("\n", " ")
        label = "متن لاتین خارج از کد/لینک/پرانتز" if kind == "latin_text" else "رقم لاتین در نثر (احتمالاً باید فارسی شود)"
        print(f"- [{label}] «{snippet}»  …{context}…")

    print(
        "\nنکته: پرانتز، کد و لینک از قبل مستثنا شده‌اند و اصطلاحات فهرست‌شده در "
        "allowlist.txt هم پرچم نمی‌خورند. اگر با این حال چیزی این‌جا پرچم خورده، "
        "معمولاً واقعاً باید فارسی شود — پیش‌نویس را اصلاح و دوباره اجرا کنید."
    )
    print(f"RESULT: ISSUES={len(issues)}")
    return 1


def main():
    parser = argparse.ArgumentParser(description="Check a Telegram draft for leftover non-Persian text/digits.")
    parser.add_argument("text", nargs="?", help="The message text to check (or use --file / stdin)")
    parser.add_argument("--file", help="Path to a file containing the draft message")
    parser.add_argument(
        "--allowlist",
        default=DEFAULT_ALLOWLIST,
        help="Path to a file of terms allowed to stay in Latin script (default: scripts/allowlist.txt next to this script). Pass --allowlist '' to disable.",
    )
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    allowlist = load_allowlist(args.allowlist)
    issues = find_issues(text, allowlist)
    sys.exit(report(text, issues))


if __name__ == "__main__":
    main()
