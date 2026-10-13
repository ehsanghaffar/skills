#!/usr/bin/env bash
# Enforce the single-skill-install contract from CONTRIBUTING.md.
# A skill must work when it is the ONLY skill installed, so it must not reach
# into sibling skills, the repo root, or assume a fixed user path.
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
SKILLS_DIR="$ROOT_DIR/skills"

fail=0
add_error() { echo "::error::$1"; fail=1; }

# 1. No absolute install paths anywhere in a skill.
if grep -rnE '/mnt/skills|/home/[^ /]*/\.claude/skills' "$SKILLS_DIR" 2>/dev/null; then
    add_error "absolute install paths (/mnt/skills, ~/.claude/skills) are forbidden in skills/"
fi

# 2. No cross-skill references: skills/X/ may only mention skills/X/.
for s in "$SKILLS_DIR"/*/; do
    name="$(basename "$s")"
    [[ -d "$s" ]] || continue
    if grep -rnE "skills/[a-z]" "$s" | grep -v "skills/$name/" | grep -v Binary; then
        add_error "skill '$name' references another skill's directory"
        fail=1
    fi
done

# 3. No imports from the repo-root lib/ (skills must be self-contained).
if grep -rnE 'from lib\.|import lib\.' "$SKILLS_DIR"; then
    add_error "skills must not import from the repo-root lib/"
    fail=1
fi

if [[ "$fail" -ne 0 ]]; then
    echo "❌ isolation gates failed"
    exit 1
fi
echo "✅ isolation gates passed"
