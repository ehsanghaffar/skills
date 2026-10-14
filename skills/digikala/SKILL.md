---
name: digikala
description: Integrate with Digikala Marketplace Open API for seller operations. Use when users need to manage products, upload images, search categories, handle orders, or automate seller workflows on Digikala (Iran's largest e-commerce platform). Trigger phrases "Digikala API", "seller.digikala.com", "marketplace API", "Iran e-commerce", "product creation Digikala", "Digikala seller panel".
version: 0.2.0
---

# Digikala Marketplace API Skill

This skill enables Claude to work with the **Digikala Marketplace Open API** (seller.digikala.com) — Iran's largest e-commerce platform's seller API with 274 endpoints covering product management, categories, orders, shipments, finance, and more.

## ⚠️ Important Safety Notice

**This skill interacts with a LIVE production marketplace.** Several operations are **state-changing** and affect your actual seller account:

| Operation       | Impact                                            | Confirmation Required         |
| --------------- | ------------------------------------------------- | ----------------------------- |
| `save-product`  | Creates/updates live product visible to customers | ✅ Yes (script prompts)       |
| `assign`        | Adds product to your seller inventory             | ✅ Yes (script prompts)       |
| `brand-request` | Submits brand registration for manual review      | ✅ Yes (script prompts)       |
| `save-title`    | Updates product title on marketplace              | ⚠️ Review before running      |
| `upload-*`      | Uploads images to Digikala servers                | ⚠️ Review files before upload |

**Read-only operations** (safe to run anytime): `search`, `suggest`, `be-seller`, `validate-*`, `get-*`, `draft-count`, `auto-title`, `get-attributes`, `tree`, `ai-check`

---

## Tool Scope & Boundaries

**Capabilities this skill requires**

| Capability   | Why it is needed                                          |
| ------------ | --------------------------------------------------------- |
| Shell (bash) | The scripts are bash                                       |
| Outbound net | `seller.digikala.com` only, for the Digikala API           |
| File read    | One image file the user explicitly names for upload         |
| File write   | A `0600` private temp dir for the auth header, removed on exit |

Nothing beyond this is used. No package installs, no `sudo`, no writes outside
the temp dir, no calls to any host other than Digikala.

**The skill must not, on its own initiative:**

- Read, list, or search the filesystem for credentials. The token comes from
  `DIGIKALA_ACCESS_TOKEN` or from the exact path in `DIGIKALA_TOKEN_FILE`, and
  nowhere else. Do not `cat`, `grep`, or `find` for tokens, SSH keys, `.env`
  files, or shell profiles.
- Print, log, echo, or include the token in any output, message, commit, or
  file. Never echo it back to the user — refer to it as "the token".
- Run a state-changing command without showing the user exactly what will change
  and getting their go-ahead first.
- Point `DIGIKALA_BASE_URL` anywhere but a `digikala.com` host. A different host
  would receive the live seller token. Only a `localhost` mock server is
  supported, and only with `DIGIKALA_ALLOW_CUSTOM_HOST=1` plus a throwaway token.
- Upload a file the user has not named and confirmed.

**Out of scope by design.** Digikala's API also covers orders, shipments,
finance, customer service, and seller identity/PII (addresses, business
documents, warehouse details). This skill does **not** call those. If a request
needs them, say so and let the user decide — they are high-impact, often
regulated, and outside the product-listing workflow this skill was built for.

---

## Working With the Token

The access token is a **live seller credential**: it can read business data and
mutate the storefront. Treat it accordingly.

- Ask the user to provide it. Do not go looking for it.
- Never display it. Do not echo it, print it into a command that gets logged,
  paste it into a report, or write it to a file.
- The scripts keep it out of the process table (the `Authorization` header is
  passed to `curl` via a private `0600` config file, never as an argument) and
  delete that file on exit.
- Do not log full API responses containing customer or order data into files
  that persist.
- If a token is ever exposed — pasted into chat, committed, or shared — tell the
  user to revoke it via `POST /auth/revoke` and issue a new one.

---

## How It Works

1. **Authentication**: The user supplies a seller access token, either via the `DIGIKALA_ACCESS_TOKEN` env var or by naming a file with `DIGIKALA_TOKEN_FILE`. The skill never looks in a default location.
2. **Product Creation Pipeline**: Search existing products → validate category/attributes → create draft → upload images → AI image validation → save title → save product → assign to seller
3. **Category Navigation**: Tree browsing, search by keyword, validation for product creation
4. **Image Management**: Upload to temp storage → AI quality check → attach to products
5. **Scope-Based Access**: Each endpoint requires specific scopes (product, order, finance, etc.)

## API Reference

**Base URL**: `https://seller.digikala.com/open-api/v1/`

**Headers Required**:

```
Content-Type: application/json
Authorization: Bearer <access_token>
```

**Rate Limits**: 429 response with `reset_time` header when exceeded

## Key Endpoints by Domain

### Category (1 endpoint - READ ONLY)

| Method | Endpoint           | Description                             |
| ------ | ------------------ | --------------------------------------- |
| GET    | `/categories/tree` | Get category tree (filter by parent_id) |

### Product (28 endpoints)

| Method | Endpoint                                              | Type               | Description                                 |
| ------ | ----------------------------------------------------- | ------------------ | ------------------------------------------- |
| GET    | `/product-creation/search/v2`                         | READ               | Search existing products by keyword/filters |
| GET    | `/product-creation/search/suggestion/v2`              | READ               | Suggest products to sell                    |
| GET    | `/product-creation/be-seller/{product_id}`            | READ               | Check if can sell a product, get commission |
| GET    | `/product-creation/search/category/v2/{keyword}`      | READ               | Find categories by keyword                  |
| GET    | `/product-creation/category/{category_id}/validation` | READ               | Validate category & get required attributes |
| POST   | `/product-creation/product/detail/validation`         | READ               | Validate product details                    |
| GET    | `/product-creation/draft-product/count`               | READ               | Count draft products                        |
| GET    | `/product-creation/draft-product/{id}`                | READ               | Get draft product details                   |
| GET    | `/product-creation/{id}/auto-title`                   | READ               | Get AI title suggestion                     |
| POST   | `/product-creation/auto-title/save`                   | WRITE              | Save/validate title                         |
| GET    | `/product-creation/attributes/{category_id}`          | READ               | Get category attributes                     |
| POST   | `/product-creation/attributes`                        | READ               | Validate attributes                         |
| POST   | `/product-creation/images/upload`                     | WRITE              | Upload product image to temp                |
| POST   | `/product-creation/images/requests/upload`            | WRITE              | Upload content request image                |
| POST   | `/product-creation/images/requests/brand-logo/upload` | WRITE              | Upload brand logo                           |
| POST   | `/product-creation/images/ai`                         | READ               | AI image quality check                      |
| POST   | `/product-creation/save`                              | **STATE-CHANGING** | Save/create LIVE product                    |
| POST   | `/product-creation/assign`                            | **STATE-CHANGING** | Assign product to seller                    |
| POST   | `/product-creation/brand/request`                     | **STATE-CHANGING** | Request new brand                           |

---

**Legend**: READ = Safe to run | WRITE = Modifies remote data | **STATE-CHANGING** = Affects live marketplace (scripts prompt for confirmation)

## Usage

```bash
# Product creation workflow
bash scripts/product-create.sh <step> [args]

# Category utilities
bash scripts/category.sh <command> [args]

# Image handling
bash scripts/image.sh <command> [args]
```

**Script Arguments:**

| Script              | Commands                                                                               | Description           |
| ------------------- | -------------------------------------------------------------------------------------- | --------------------- |
| `product-create.sh` | `search`, `validate-category`, `save-title`, `save-product`, `assign`, `brand-request` | Full product pipeline |
| `category.sh`       | `tree`, `search`, `validate`                                                           | Category navigation   |
| `image.sh`          | `upload-product`, `upload-request`, `upload-brand`, `ai-check`                         | Image operations      |

**Examples:**

```bash
# Provide the token. Ask the user for it; never go looking for it.
export DIGIKALA_ACCESS_TOKEN="<your_access_token_here>"
# OR keep it in a file you choose the path of:
#   DIGIKALA_TOKEN_FILE=/path/to/token

# ✅ READ-ONLY: Safe to run anytime
# Search products to sell
bash scripts/product-create.sh search "iPhone 15"

# Validate category and get required attributes
bash scripts/product-create.sh validate-category 12345

# Upload product image (uploads to Digikala temp storage)
bash scripts/image.sh upload-product /path/to/image.jpg

# AI quality check on uploaded image
bash scripts/image.sh ai-check "image_id" true

# Save product title (modifies remote data)
bash scripts/product-create.sh save-title 123 "گوشی موبایل اپل آیفون 15"

# ⚠️ STATE-CHANGING: These prompt for confirmation before executing
# Save product (CREATES LIVE PRODUCT on marketplace)
bash scripts/product-create.sh save-product '{"category_id":123,"draft_product_id":456,...}'

# Assign product to seller (MODIFIES SELLER INVENTORY)
bash scripts/product-create.sh assign 789
```

## Output

All scripts output JSON to stdout. Example responses:

**Product Search Response:**

```json
{
  "status": "ok",
  "data": {
    "items": [
      {
        "id": 12345,
        "name": "iPhone 15 Pro",
        "brand": "Apple",
        "commission": { "canSell": true, "commission": 0.055 },
        "referencePrice": 150000000
      }
    ]
  }
}
```

## Present Results to User

When presenting API results to users, format as:

````
## Digikala API Result: [Operation Name]

**Status**: ✅ Success / ❌ Failed
**Endpoint**: `METHOD /open-api/v1/...`

### Key Data
- **Field**: Value
- **Field**: Value

### Next Steps
1. [Action based on response]
2. [Follow-up if needed]

### Raw Response (if needed)
```json
{...}
````

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired token | Re-provide via `DIGIKALA_ACCESS_TOKEN` or `DIGIKALA_TOKEN_FILE` |
| 403 Forbidden | Missing scope | Check `/auth/scopes/{client_code}` for available scopes |
| 404 Not Found | Wrong ID or resource doesn't exist | Verify product/category IDs |
| 429 Too Many Requests | Rate limit exceeded | Wait for `reset_time` or implement backoff |
| 500 Server Error | Digikala platform issue | Retry later, contact support if persistent |
| Validation errors | Missing required fields | Check response `errors` object for field-specific messages |
| `Refusing DIGIKALA_BASE_URL` | `DIGIKALA_BASE_URL` points off Digikala | Unset it to use the default; the token would go to that host |
| `Refusing to proceed: stdin is not a terminal` | Unattended state-changing run | Re-run with `DIGIKALA_CONFIRM=1` once you have reviewed the change |

## Important Notes

- **Sandbox Available**: Use `https://github.com/salimousavi/seller_service_sandbox` for development with mock data. Point at it with `DIGIKALA_BASE_URL=http://localhost:<port>` **plus** `DIGIKALA_ALLOW_CUSTOM_HOST=1`, and use a throwaway token — never a real seller token.
- **Language**: Digikala's own API expects Persian (Farsi) for `title_fa` and other localized fields. That is a platform requirement, not a constraint this skill imposes. `title_en` accepts English, and any other field accepts the language the platform expects for it. If a request comes in another language, confirm with the user which field needs which language rather than assuming Persian everywhere.
- **Client Registration**: Must have active client registered with Digikala; contact `Marketplace-API@digikala.com`
- **Scopes Required**: Each endpoint needs specific scope — check `/auth/scopes/{client_code}` for your app's permissions
- **Image URLs**: Temp images expire; use `use_temp_images: true` in product save to reference them
- **Commission Rates**: Vary by category; check `/product-creation/be-seller/{id}` before listing
- **Token Management**: Tokens are NOT stored by scripts, and no default token location is read. Provide via `DIGIKALA_ACCESS_TOKEN` or `DIGIKALA_TOKEN_FILE` (a path you choose; keep it `chmod 600` if you create one)
- **Non-Interactive Use**: Dangerous operations (`save-product`, `assign`, `brand-request`) prompt on a terminal but refuse when stdin is not interactive; set `DIGIKALA_CONFIRM=1` to confirm from scripts or agents. Only set that flag after reviewing the exact change with the user.
- **Full API Surface**: See `references/endpoints.md` for all 274 operations.
