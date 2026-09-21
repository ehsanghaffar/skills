---
name: digikala
description: Integrate with Digikala Marketplace Open API for seller operations. Use when users need to manage products, upload images, search categories, handle orders, or automate seller workflows on Digikala (Iran's largest e-commerce platform). Trigger phrases: "Digikala API", "seller.digikala.com", "marketplace API", "Iran e-commerce", "product creation Digikala", "Digikala seller panel".
version: 0.1.2
---

# Digikala Marketplace API Skill

This skill enables Claude to work with the **Digikala Marketplace Open API** (seller.digikala.com) — Iran's largest e-commerce platform's seller API with 274 endpoints covering product management, categories, orders, shipments, finance, and more.

## ⚠️ Important Safety Notice

**This skill interacts with a LIVE production marketplace.** Several operations are **state-changing** and affect your actual seller account:

| Operation | Impact | Confirmation Required |
|-----------|--------|----------------------|
| `save-product` | Creates/updates live product visible to customers | ✅ Yes (script prompts) |
| `assign` | Adds product to your seller inventory | ✅ Yes (script prompts) |
| `brand-request` | Submits brand registration for manual review | ✅ Yes (script prompts) |
| `save-title` | Updates product title on marketplace | ⚠️ Review before running |
| `upload-*` | Uploads images to Digikala servers | ⚠️ Review files before upload |

**Read-only operations** (safe to run anytime): `search`, `suggest`, `be-seller`, `validate-*`, `get-*`, `draft-count`, `auto-title`, `get-attributes`, `tree`, `ai-check`

---

## How It Works

1. **Authentication**: Provide access token via `DIGIKALA_ACCESS_TOKEN` env var or `~/.digikala/token` file (user-managed)
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
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories/tree` | Get category tree (filter by parent_id) |

### Product (28 endpoints)
| Method | Endpoint | Type | Description |
|--------|----------|------|-------------|
| GET | `/product-creation/search/v2` | READ | Search existing products by keyword/filters |
| GET | `/product-creation/search/suggestion/v2` | READ | Suggest products to sell |
| GET | `/product-creation/be-seller/{product_id}` | READ | Check if can sell a product, get commission |
| GET | `/product-creation/search/category/v2/{keyword}` | READ | Find categories by keyword |
| GET | `/product-creation/category/{category_id}/validation` | READ | Validate category & get required attributes |
| POST | `/product-creation/product/detail/validation` | READ | Validate product details |
| GET | `/product-creation/draft-product/count` | READ | Count draft products |
| GET | `/product-creation/draft-product/{id}` | READ | Get draft product details |
| GET | `/product-creation/{id}/auto-title` | READ | Get AI title suggestion |
| POST | `/product-creation/auto-title/save` | WRITE | Save/validate title |
| GET | `/product-creation/attributes/{category_id}` | READ | Get category attributes |
| POST | `/product-creation/attributes` | READ | Validate attributes |
| POST | `/product-creation/images/upload` | WRITE | Upload product image to temp |
| POST | `/product-creation/images/requests/upload` | WRITE | Upload content request image |
| POST | `/product-creation/images/requests/brand-logo/upload` | WRITE | Upload brand logo |
| POST | `/product-creation/images/ai` | READ | AI image quality check |
| POST | `/product-creation/save` | **STATE-CHANGING** | Save/create LIVE product |
| POST | `/product-creation/assign` | **STATE-CHANGING** | Assign product to seller |
| POST | `/product-creation/brand/request` | **STATE-CHANGING** | Request new brand |

---

**Legend**: READ = Safe to run | WRITE = Modifies remote data | **STATE-CHANGING** = Affects live marketplace (scripts prompt for confirmation)

## Usage

```bash
# Product creation workflow
bash /mnt/skills/user/digikala/scripts/product-create.sh <step> [args]

# Category utilities
bash /mnt/skills/user/digikala/scripts/category.sh <command> [args]

# Image handling
bash /mnt/skills/user/digikala/scripts/image.sh <command> [args]
```

**Script Arguments:**

| Script | Commands | Description |
|--------|----------|-------------|
| `product-create.sh` | `search`, `validate-category`, `save-title`, `save-product`, `assign`, `brand-request` | Full product pipeline |
| `category.sh` | `tree`, `search`, `validate` | Category navigation |
| `image.sh` | `upload-product`, `upload-request`, `upload-brand`, `ai-check` | Image operations |

**Examples:**
```bash
# Set token (one time)
export DIGIKALA_ACCESS_TOKEN="your_access_token_here"
# OR: echo "your_access_token_here" > ~/.digikala/token && chmod 600 ~/.digikala/token

# ✅ READ-ONLY: Safe to run anytime
# Search products to sell
bash /mnt/skills/user/digikala/scripts/product-create.sh search "iPhone 15"

# Validate category and get required attributes
bash /mnt/skills/user/digikala/scripts/product-create.sh validate-category 12345

# Upload product image (uploads to Digikala temp storage)
bash /mnt/skills/user/digikala/scripts/image.sh upload-product /path/to/image.jpg

# AI quality check on uploaded image
bash /mnt/skills/user/digikala/scripts/image.sh ai-check "image_id" true

# Save product title (modifies remote data)
bash /mnt/skills/user/digikala/scripts/product-create.sh save-title 123 "گوشی موبایل اپل آیفون 15"

# ⚠️ STATE-CHANGING: These prompt for confirmation before executing
# Save product (CREATES LIVE PRODUCT on marketplace)
bash /mnt/skills/user/digikala/scripts/product-create.sh save-product '{"category_id":123,"draft_product_id":456,...}'

# Assign product to seller (MODIFIES SELLER INVENTORY)
bash /mnt/skills/user/digikala/scripts/product-create.sh assign 789
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
        "commission": {"canSell": true, "commission": 0.055},
        "referencePrice": 150000000
      }
    ]
  }
}
```

## Present Results to User

When presenting API results to users, format as:

```
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
```
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/expired token | Update `DIGIKALA_ACCESS_TOKEN` or `~/.digikala/token` |
| 403 Forbidden | Missing scope | Check `/auth/scopes/{client_code}` for available scopes |
| 404 Not Found | Wrong ID or resource doesn't exist | Verify product/category IDs |
| 429 Too Many Requests | Rate limit exceeded | Wait for `reset_time` or implement backoff |
| 500 Server Error | Digikala platform issue | Retry later, contact support if persistent |
| Validation errors | Missing required fields | Check response `errors` object for field-specific messages |

## Important Notes

- **Sandbox Available**: Use `https://github.com/salimousavi/seller_service_sandbox` for development with mock data
- **Persian Content**: Many fields (titles, descriptions, categories) use Persian/Farsi
- **Client Registration**: Must have active client registered with Digikala; contact `Marketplace-API@digikala.com`
- **Scopes Required**: Each endpoint needs specific scope — check `/auth/scopes/{client_code}` for your app's permissions
- **Image URLs**: Temp images expire; use `use_temp_images: true` in product save to reference them
- **Commission Rates**: Vary by category; check `/product-creation/be-seller/{id}` before listing
- **Token Management**: Tokens are NOT stored by scripts. Provide via `DIGIKALA_ACCESS_TOKEN` env var or `~/.digikala/token` file (chmod 600 recommended)