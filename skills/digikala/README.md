# Digikala Skill

Integrate with Digikala Marketplace Open API for seller operations.

## Installation

```bash
# Clone or copy the skill directory
cp -r skills/digikala ~/.claude/skills/
```

## Usage

Set your access token:
```bash
export DIGIKALA_ACCESS_TOKEN="your_token"
```

Then use the scripts:
```bash
bash scripts/product-create.sh search "iPhone 15"
bash scripts/category.sh tree
bash scripts/image.sh upload-product ./photo.jpg
```

## Safety

- Read-only operations: safe to run anytime
- Write operations: review before running
- State-changing operations: confirm with y/N

See `SKILL.md` for full documentation.
