# Telegram Persian Enforcer

Enforce Persian output for all Telegram interactions.

## Installation

No installation needed — the skill uses `scripts/check_persian.py`.

## Usage

Check a draft before sending:
```bash
python scripts/check_persian.py --file draft.txt
python scripts/check_persian.py --file draft.txt --strict
python scripts/check_persian.py --file draft.txt --pending
```

## How it works

1. Draft your message
2. Run `check_persian.py` — flags Latin words and Western digits
3. Fix flagged items, re-run
4. Final check with `--strict` before sending

See `SKILL.md` for full documentation.
