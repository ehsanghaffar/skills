# Contributing

This repo is for personal agent skills. Please open an issue before submitting PRs.

## Adding a skill

1. Create `skills/{kebab-case-name}/`
2. Add `SKILL.md` with frontmatter: `name`, `description`, `version`
3. Add scripts to `scripts/` (optional)
4. Add references to `references/` (optional)
5. Add evals to `evals/evals.json` (optional but encouraged)
6. Update `README.md`

## Code style

- Bash: `#!/bin/bash` + `set -e`
- Python: type hints, `#!/usr/bin/env python3`
- UTF-8 everywhere
- Semantic versioning for `version` field
