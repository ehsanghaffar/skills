# Digikala Marketplace API - Complete Endpoint Reference

Reference for all 274 available operations. This document is documentation only —
**the skill ships no script that calls the token endpoints or any endpoint outside
the Product Creation, Category, and Image groups.** Treat the sections below as
background; the scripts in `scripts/` are the actual supported surface.

> **Credential note:** the endpoints under "Authentication" mint and revoke the
> seller access token. They are listed here for orientation only. Never call them
> from an agent session, and never use this skill to obtain a token.

## Authentication (5) — not called by this skill
- GET  `/auth/scopes` - List all defined scopes
- GET  `/auth/scopes/{client_code}` - List scopes available for your application
- POST `/auth/token` - Generate access and refresh token (requires authorization_code)
- POST `/auth/refresh-token` - Generate new access token using refresh token
- POST `/auth/revoke` - Revoke seller access token (requires self_settings scope)

## Category (1)
- GET `/categories/tree` - Return child categories (optional parent_id filter)

## Product Creation (28)
- GET  `/product-creation/search/v2` - Search existing products by keyword/filters
- GET  `/product-creation/search/suggestion/v2` - Suggest products to sell
- GET  `/product-creation/be-seller/{product_id}` - Check if can sell product, get commission
- GET  `/product-creation/search/category/v2/{keyword}` - Find categories by keyword
- GET  `/product-creation/category/{category_id}/validation` - Validate category & get required data
- POST `/product-creation/product/detail/validation` - Validate product details
- GET  `/product-creation/draft-product/count` - Count draft products
- GET  `/product-creation/draft-product/{draft_product_id}` - Get draft product entity
- GET  `/product-creation/{draft_product_id}/auto-title` - Get AI title suggestion
- POST `/product-creation/auto-title/save` - Save/validate title
- GET  `/product-creation/attributes/{category_id}` - Get category attributes
- POST `/product-creation/attributes` - Validate attributes
- POST `/product-creation/images/upload` - Upload product image to temp storage
- POST `/product-creation/images/requests/upload` - Upload content request image
- POST `/product-creation/images/requests/brand-logo/upload` - Upload brand logo
- POST `/product-creation/images/ai` - AI image quality check
- POST `/product-creation/save` - Save/create product
- POST `/product-creation/assign` - Assign product to seller
- POST `/product-creation/brand/request` - Create brand request

## Product Management (not wrapped by this skill)
Digikala also exposes endpoints for:
- Product variants and pricing
- Inventory management
- Product status updates
- Bulk operations
- Product archiving

## Orders — out of scope
- Order listing and filtering
- Order details
- Order status updates
- Invoice generation
- Return/cancellation handling

These expose customer personal data and drive fulfilment. This skill does not
call them. If a request needs them, stop and tell the user.

## Shipments — out of scope
- Shipment creation
- Label printing
- Tracking updates
- Pickup scheduling

## Finance — out of scope
- Settlement reports
- Transaction history
- Payout management
- Fee breakdowns

## Customer Service — out of scope
- Ticket management
- Message threads
- Response templates

## Store Settings — out of scope
- Store profile
- Shipping settings
- Payment methods
- Notification preferences

The full spec also covers seller identity and PII (addresses, business
documents, warehouse details). This skill does not call those endpoints.

## Scopes Reference
Each endpoint requires specific scopes. Common scopes:
- `product` - Product creation and management
- `order` - Order viewing and management
- `finance` - Financial reports and transactions
- `shipment` - Shipment operations
- `customer_service` - Ticket/message handling
- `store_settings` - Store configuration
- `self_settings` - Token revocation

Check `/auth/scopes/{client_code}` for your application's available scopes.

## Error Codes
- 200 - Success
- 400 - Validation error (check response.errors)
- 401 - Unauthorized (token expired/invalid)
- 403 - Forbidden (missing scope/permission)
- 404 - Not found
- 429 - Rate limited (check reset_time header)
- 500 - Server error

## Rate Limits
Default limits apply per endpoint. Rate-limit responses carry a `reset_time` field (seconds until the window resets) — the API does not use `X-RateLimit-*` headers.

## Sandbox Environment
For development: https://github.com/salimousavi/seller_service_sandbox
Provides mock data for all endpoints without requiring live credentials.

## Support
Email: Marketplace-API@digikala.com
Documentation: https://seller.digikala.com/open-api/docs