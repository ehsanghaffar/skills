#!/usr/bin/env python3
"""Validate every skills/*/SKILL.md has clean frontmatter.

Required keys: name, description, version. No duplicate keys.
Exits non-zero on the first broken file.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

REQUIRED = ("name:", "description:", "version:")
FM = re.compile(r"\A---[ \t]*\n(.*?)\n---", re.DOTALL)


def validate(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    body = FM.match(text)
    if not body:
        print(f"::error file={path}::missing or malformed frontmatter", file=sys.stderr)
        raise SystemExit(1)
    for needed in REQUIRED:
        if not re.search(rf"^\s*{needed}", body.group(1), re.MULTILINE):
            print(f"::error file={path}::frontmatter missing '{needed}'", file=sys.stderr)
            raise SystemExit(1)
    keys = re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", body.group(1), re.MULTILINE)
    for k in dict.fromkeys(keys):
        if keys.count(k) > 1:
            print(f"::error file={path}::duplicate frontmatter key '{k}'", file=sys.stderr)
            raise SystemExit(1)


def main() -> int:
    root = Path(__file__).resolve().parents[2] / "skills"
    for path in sorted(root.glob("*/SKILL.md")):
        validate(path)
    print(f"✅ {len(list(root.glob('*/SKILL.md')))} skill frontmatters validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
