# Digikala Skill

Integrate with Digikala Marketplace Open API for seller operations.

## Installation

```bash
# Clone or copy the skill directory
cp -r skills/digikala ~/.claude/skills/
```

## Usage

Provide your access token. The skill never looks for it in a default location —
you tell it where it is:

```bash
export DIGIKALA_ACCESS_TOKEN="<your_token>"
# or, to keep it in a file:
DIGIKALA_TOKEN_FILE=/path/to/token bash scripts/category.sh tree
```

Treat the token as a live seller credential: don't paste it into shared logs or
repositories. If it's ever exposed, revoke it via `POST /auth/revoke` and issue
a new one.

Then use the scripts:

```bash
bash scripts/product-create.sh search "iPhone 15"
bash scripts/category.sh tree
bash scripts/image.sh upload-product ./photo.jpg
```

## Safety

- Read-only operations: safe to run anytime
- Write operations: review before running
- State-changing operations: refuse by default, need explicit confirmation
  (`DIGIKALA_CONFIRM=1` for non-interactive runs)

## Scope

The scripts only call the Category, Product Creation, and Image endpoints, and
only against `seller.digikala.com`. Orders, shipments, finance, customer
service, and seller identity/PII endpoints are deliberately not used.

For a local sandbox, set both `DIGIKALA_BASE_URL=http://localhost:<port>` and
`DIGIKALA_ALLOW_CUSTOM_HOST=1` — and use a throwaway token, never a real one.

See `SKILL.md` for full documentation.