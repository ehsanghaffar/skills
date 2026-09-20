---
name: digikala
description: Integrate with Digikala Marketplace Open API for seller operations. Use when users need to authenticate, manage products, upload images, search categories, handle orders, or automate seller workflows on Digikala (Iran's largest e-commerce platform). Trigger phrases: "Digikala API", "seller.digikala.com", "marketplace API", "Iran e-commerce", "product creation Digikala", "Digikala seller panel".
---

# Digikala Marketplace API Skill

This skill enables Claude to work with the **Digikala Marketplace Open API** (seller.digikala.com) — Iran's largest e-commerce platform's seller API with 274 endpoints covering authentication, product management, categories, orders, shipments, finance, and more.

## How It Works

1. **Authentication Flow**: OAuth2-style flow with authorization_code → access_token + refresh_token → token refresh → revoke
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

### Authentication (5 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/scopes` | List all defined scopes |
| GET | `/auth/scopes/{client_code}` | List scopes available for your app |
| POST | `/auth/token` | Exchange authorization_code for tokens |
| POST | `/auth/refresh-token` | Refresh expired access_token |
| POST | `/auth/revoke` | Revoke seller access token |

### Category (1 endpoint)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories/tree` | Get category tree (filter by parent_id) |

### Product (28 endpoints)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/product-creation/search/v2` | Search existing products by keyword/filters |
| GET | `/product-creation/search/suggestion/v2` | Suggest products to sell |
| GET | `/product-creation/be-seller/{product_id}` | Check if can sell a product, get commission |
| GET | `/product-creation/search/category/v2/{keyword}` | Find categories by keyword |
| GET | `/product-creation/category/{category_id}/validation` | Validate category & get required attributes |
| POST | `/product-creation/product/detail/validation` | Validate product details |
| GET | `/product-creation/draft-product/count` | Count draft products |
| GET | `/product-creation/draft-product/{id}` | Get draft product details |
| GET | `/product-creation/{id}/auto-title` | Get AI title suggestion |
| POST | `/product-creation/auto-title/save` | Save/validate title |
| GET | `/product-creation/attributes/{category_id}` | Get category attributes |
| POST | `/product-creation/attributes` | Validate attributes |
| POST | `/product-creation/images/upload` | Upload product image to temp |
| POST | `/product-creation/images/requests/upload` | Upload content request image |
| POST | `/product-creation/images/requests/brand-logo/upload` | Upload brand logo |
| POST | `/product-creation/images/ai` | AI image quality check |
| POST | `/product-creation/save` | Save/create product |
| POST | `/product-creation/assign` | Assign product to seller |
| POST | `/product-creation/brand/request` | Request new brand |

## Usage

```bash
# Authentication helper
bash /mnt/skills/user/digikala/scripts/auth.sh <command> [args]

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
| `auth.sh` | `get-token`, `refresh`, `revoke`, `scopes` | Handle OAuth flow |
| `product-create.sh` | `search`, `validate-category`, `create-draft`, `upload-image`, `ai-check`, `save-title`, `save-product`, `assign` | Full product pipeline |
| `category.sh` | `tree`, `search`, `validate` | Category navigation |
| `image.sh` | `upload-product`, `upload-request`, `upload-brand`, `ai-check` | Image operations |

**Examples:**
```bash
# Get access token after seller authorization
bash /mnt/skills/user/digikala/scripts/auth.sh get-token "auth_code_here"

# Search products to sell
bash /mnt/skills/user/digikala/scripts/product-create.sh search "iPhone 15"

# Validate category and get required attributes
bash /mnt/skills/user/digikala/scripts/product-create.sh validate-category 12345

# Upload product image
bash /mnt/skills/user/digikala/scripts/image.sh upload-product /path/to/image.jpg

# AI quality check on uploaded image
bash /mnt/skills/user/digikala/scripts/image.sh ai-check "image_id" true

# Save product title
bash /mnt/skills/user/digikala/scripts/product-create.sh save-title 123 "گوشی موبایل اپل آیفون 15"
```

## Output

All scripts output JSON to stdout. Example responses:

**Auth Token Response:**
```json
{
  "status": "ok",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "WQ098gF5PG3salmqewqvfbgxzzgTgAmWvkrQaWkgnpiqky1KAoqnxunQBz09Xc5UI1eg9tSo1h6k1",
    "access_token_expires_at": {"date": "2025-02-07 00:00:00.000000", "timezone": "Asia/Tehran"},
    "refresh_token_expires_at": {"date": "2025-03-09 00:00:00.000000", "timezone": "Asia/Tehran"}
  }
}
```

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
| 401 Unauthorized | Invalid/expired token | Run `auth.sh refresh` with refresh_token |
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