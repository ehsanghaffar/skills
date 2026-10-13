# Contributing

This repo is for personal agent skills. Please open an issue before submitting PRs.

## Adding a skill

1. Create `skills/{kebab-case-name}/`
2. Add `SKILL.md` with frontmatter: `name`, `description`, `version`
3. Add scripts to `scripts/` (optional)
4. Add references to `references/` (optional)
5. Add evals to `evals/evals.json` (optional but encouraged)
6. Update `README.md`

## Isolation rule

A user may install **one single skill** from this repo. Therefore every skill
must be fully self-contained:

- No references to sibling skills by name — not in SKILL.md, not in scripts,
  not in evals. A skill may describe what it does *not* do, but must never
  route ("use skill X instead") or import from another skill.
- No absolute install paths (`/mnt/skills/...`, `~/.claude/skills/...`).
  Reference scripts relative to the skill directory and locate files from the
  script's own location.
- No state written inside the skill directory (allowlists as mutable queues,
  logs, caches). Mutable state belongs in a user-state location such as
  `$XDG_STATE_HOME` or a path the caller passes in.
- No shared code outside the skill directory: nothing imports from the repo
  root. Duplicated helpers between skills are acceptable and expected;
  coupling is not.

## Code style

- Bash: `#!/bin/bash` + `set -euo pipefail`
- Python: type hints, `#!/usr/bin/env python3`
- UTF-8 everywhere
- Semantic versioning for `version` field
