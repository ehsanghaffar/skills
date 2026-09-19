#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"

SKILLS_DIR="$ROOT_DIR/skills"
README="$ROOT_DIR/README.md"

# GitHub repository.
GITHUB_REPO="${GITHUB_REPO:-YOUR_ORG/YOUR_REPO}"
GITHUB_BRANCH="${GITHUB_BRANCH:-main}"

[[ -d "$SKILLS_DIR" ]] || exit 0

touch "$README"

TMP_FILE="$(mktemp)"
SKILLS_FILE="$(mktemp)"

trap 'rm -f "$TMP_FILE" "$SKILLS_FILE"' EXIT

while IFS= read -r -d '' skill_file; do
    skill_dir="$(dirname -- "$skill_file")"

    name=""
    description=""

    # Read name from YAML frontmatter.
    name="$(
        sed -n '
            /^---[[:space:]]*$/ {
                x
                /./ {
                    x
                    /^---[[:space:]]*$/q
                }
                x
            }

            /^name:[[:space:]]*/ {
                s/^name:[[:space:]]*//
                s/[[:space:]]*$//
                p
                q
            }
        ' "$skill_file"
    )"

    # Read description from YAML frontmatter.
    description="$(
        sed -n '
            /^description:[[:space:]]*/ {
                s/^description:[[:space:]]*//
                s/[[:space:]]*$//
                p
                q
            }
        ' "$skill_file"
    )"

    # Skip malformed skill files.
    [[ -n "$name" ]] || continue
    [[ -n "$description" ]] || continue

    relative_path="${skill_dir#"$ROOT_DIR"/}"

    printf '%s\t%s\t%s\n' \
        "$name" \
        "$description" \
        "$relative_path"

done < <(
    find "$SKILLS_DIR" \
        -type f \
        -name "SKILL.md" \
        -print0
) |
sort -t $'\t' -k1,1 > "$SKILLS_FILE"

# Generate README entries.
while IFS=$'\t' read -r name description relative_path; do
    [[ -n "$name" ]] || continue

    printf '%s\n' \
        "- [**${name}**](https://github.com/${GITHUB_REPO}/blob/${GITHUB_BRANCH}/${relative_path}/SKILLS.md): ${description}"
done < "$SKILLS_FILE" > "${SKILLS_FILE}.formatted"

mv "${SKILLS_FILE}.formatted" "$SKILLS_FILE"

awk -v skills_file="$SKILLS_FILE" '
    BEGIN {
        while ((getline line < skills_file) > 0) {
            skills = skills line "\n"
        }

        close(skills_file)
    }

    /^## Skills[[:space:]]*$/ {
        print
        print ""
        printf "%s", skills
        found = 1
        next
    }

    {
        print
    }

    END {
        if (!found) {
            print ""
            print "## Skills"
            print ""
            printf "%s", skills
        }
    }
' "$README" > "$TMP_FILE"

mv "$TMP_FILE" "$README"

trap - EXIT
rm -f "$SKILLS_FILE"