#!/usr/bin/env bash
# Regenerate the "## Skills" section of README.md from every skill's SKILL.md
# frontmatter. The generated section is the single source of truth: hand-edits
# inside "## Skills" are overwritten on the next run — edit SKILL.md instead.
#
# Portable: uses python3 for frontmatter parsing (BSD and GNU sed frontmatter
# hacks silently no-op or mangle block scalars, which is what broke the
# previous version of this script).

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

SKILLS_DIR="${SKILLS_DIR:-$ROOT_DIR/skills}"
README="${README:-$ROOT_DIR/README.md}"

# Default to the repo's own origin, not a placeholder.
if [[ -z "${GITHUB_REPO:-}" ]]; then
    origin_url="$(git -C "$ROOT_DIR" remote get-url origin 2>/dev/null || true)"
    GITHUB_REPO="$(printf '%s' "$origin_url" | sed -E 's#^.*github\.com[:/]##; s#\.git$##')"
    [[ -n "$GITHUB_REPO" ]] || GITHUB_REPO="ehsanghaffar/skills"
fi
GITHUB_BRANCH="${GITHUB_BRANCH:-main}"

export SKILLS_DIR README GITHUB_REPO GITHUB_BRANCH

python3 - <<'PYEOF'
import os
import re
import sys

skills_dir = os.environ["SKILLS_DIR"]
readme_path = os.environ["README"]
repo = os.environ["GITHUB_REPO"]
branch = os.environ["GITHUB_BRANCH"]


def parse_frontmatter(text):
    """Extract top-level `key: value` scalars from YAML frontmatter.

    Handles plain values, quoted values, and `>-` / `|-` block scalars,
    which is all SKILL.md frontmatter needs. Deliberately not a general
    YAML parser.
    """
    m = re.match(r"\A---[ \t]*\n(.*?\n)---[ \t]*\n", text, re.DOTALL)
    if not m:
        return {}
    fields = {}
    lines = m.group(1).split("\n")
    i = 0
    while i < len(lines):
        kv = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$", lines[i])
        if not kv:
            i += 1
            continue
        key, raw = kv.group(1), kv.group(2).strip()
        i += 1
        if raw in (">-", ">", "|", "|-"):
            parts = []
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith("  ")):
                parts.append(lines[i].strip())
                i += 1
            joiner = " " if raw in (">-", ">") else "\n"
            value = joiner.join(p for p in parts if p).strip()
        else:
            value = raw.strip("\"'")
        fields[key] = value
    return fields


entries = []
for name in sorted(os.listdir(skills_dir)):
    skill_md = os.path.join(skills_dir, name, "SKILL.md")
    if not os.path.isfile(skill_md):
        continue
    with open(skill_md, encoding="utf-8") as fh:
        fm = parse_frontmatter(fh.read())
    skill_name, description = fm.get("name"), fm.get("description")
    if not skill_name or not description:
        print(f"warning: skipping {skill_md} (missing name/description)", file=sys.stderr)
        continue
    relative = os.path.relpath(os.path.dirname(skill_md), os.path.dirname(readme_path))
    url = f"https://github.com/{repo}/blob/{branch}/{relative}/SKILL.md"
    # Collapse newlines so the entry stays a single README bullet.
    description = " ".join(description.split())
    entries.append(f"- [**{skill_name}**]({url}): {description}")

with open(readme_path, encoding="utf-8") as fh:
    readme = fh.read()

block = "## Skills\n\n" + "\n".join(entries) + "\n"

if re.search(r"^## Skills[ \t]*$", readme, re.MULTILINE):
    readme = re.sub(
        r"^## Skills[ \t]*$.*?(?=^## |\Z)",
        lambda _: block + "\n",
        readme,
        count=1,
        flags=re.MULTILINE | re.DOTALL,
    )
else:
    readme = readme.rstrip("\n") + "\n\n" + block

with open(readme_path, "w", encoding="utf-8") as fh:
    fh.write(readme)

print(f"updated {readme_path}: {len(entries)} skills")
PYEOF
