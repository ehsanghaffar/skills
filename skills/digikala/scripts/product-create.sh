#!/bin/bash
set -e

BASE_URL="https://seller.digikala.com/open-api/v1"
CONFIG_FILE="${HOME}/.digikala/config.json"

load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        cat "$CONFIG_FILE"
    else
        echo '{}'
    fi
}

get_auth_header() {
    local config=$(load_config)
    local access_token=$(echo "$config" | jq -r '.access_token // empty')
    if [[ -z "$access_token" ]]; then
        echo "Error: No access token. Run 'auth.sh get-token' first." >&2
        exit 1
    fi
    echo "Authorization: Bearer $access_token"
}

api_request() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    local content_type="${4:-application/json}"
    
    local auth_header=$(get_auth_header)
    
    if [[ -n "$data" ]]; then
        curl -s -X "$method" \
            -H "Content-Type: $content_type" \
            -H "$auth_header" \
            -d "$data" \
            "$BASE_URL$endpoint"
    else
        curl -s -X "$method" \
            -H "Content-Type: $content_type" \
            -H "$auth_header" \
            "$BASE_URL$endpoint"
    fi
}

case "${1:-}" in
    search)
        keyword="${2:-}"
        if [[ -z "$keyword" ]]; then
            echo "Usage: $0 search <keyword> [categories] [brands] [statuses]" >&2
            exit 1
        fi
        categories="${3:-}"
        brands="${4:-}"
        statuses="${5:-}"
        
        query="search[keyword]=$keyword"
        [[ -n "$categories" ]] && query="$query&search[categories]=$categories"
        [[ -n "$brands" ]] && query="$query&search[brands]=$brands"
        [[ -n "$statuses" ]] && query="$query&search[statuses]=$statuses"
        
        api_request GET "/product-creation/search/v2?$query"
        ;;
    
    suggest)
        keyword="${2:-}"
        api_request GET "/product-creation/search/suggestion/v2?search[keyword]=$keyword"
        ;;
    
    be-seller)
        product_id="${2:-}"
        if [[ -z "$product_id" ]]; then
            echo "Usage: $0 be-seller <product_id>" >&2
            exit 1
        fi
        api_request GET "/product-creation/be-seller/$product_id"
        ;;
    
    search-category)
        keyword="${2:-}"
        if [[ -z "$keyword" ]]; then
            echo "Usage: $0 search-category <keyword>" >&2
            exit 1
        fi
        api_request GET "/product-creation/search/category/v2/$keyword"
        ;;
    
    validate-category)
        category_id="${2:-}"
        if [[ -z "$category_id" ]]; then
            echo "Usage: $0 validate-category <category_id>" >&2
            exit 1
        fi
        api_request GET "/product-creation/category/$category_id/validation"
        ;;
    
    validate-detail)
        # Required: category_id, division_id, model, brand_id
        # Optional: product_type_ids[], color_id, is_iranian, product_classes[], fake, fake_reasons[], mefa_ids
        cat <<'EOF' >&2
Usage: $0 validate-detail <json_data>
Required fields: category_id, division_id, model, brand_id
Example:
  $0 validate-detail '{"category_id":123,"division_id":456,"model":"iPhone 15","brand_id":789,"is_iranian":false}'
EOF
        exit 1
        ;;
    
    validate-detail)
        data="${2:-}"
        if [[ -z "$data" ]]; then
            echo "Usage: $0 validate-detail '<json_data>'" >&2
            exit 1
        fi
        api_request POST "/product-creation/product/detail/validation" "$data"
        ;;
    
    draft-count)
        api_request GET "/product-creation/draft-product/count"
        ;;
    
    get-draft)
        draft_id="${2:-}"
        if [[ -z "$draft_id" ]]; then
            echo "Usage: $0 get-draft <draft_product_id>" >&2
            exit 1
        fi
        api_request GET "/product-creation/draft-product/$draft_id"
        ;;
    
    auto-title)
        draft_id="${2:-}"
        if [[ -z "$draft_id" ]]; then
            echo "Usage: $0 auto-title <draft_product_id>" >&2
            exit 1
        fi
        api_request GET "/product-creation/$draft_id/auto-title"
        ;;
    
    save-title)
        draft_id="${2:-}"
        title_fa="${3:-}"
        title_en="${4:-}"
        description="${5:-}"
        advantages="${6:-}"
        disadvantages="${7:-}"
        
        if [[ -z "$draft_id" || -z "$title_fa" ]]; then
            echo "Usage: $0 save-title <draft_product_id> <title_fa> [title_en] [description] [advantages_json] [disadvantages_json]" >&2
            exit 1
        fi
        
        data=$(jq -n \
            --argjson draft_id "$draft_id" \
            --arg title_fa "$title_fa" \
            --arg title_en "$title_en" \
            --arg description "$description" \
            --argjson advantages "${advantages:-[]}" \
            --argjson disadvantages "${disadvantages:-[]}" \
            '{
                draft_product_id: $draft_id,
                title_fa: $title_fa,
                title_en: $title_en,
                description: $description,
                advantages: $advantages,
                disadvantages: $disadvantages
            }')
        api_request POST "/product-creation/auto-title/save" "$data"
        ;;
    
    get-attributes)
        category_id="${2:-}"
        if [[ -z "$category_id" ]]; then
            echo "Usage: $0 get-attributes <category_id>" >&2
            exit 1
        fi
        api_request GET "/product-creation/attributes/$category_id"
        ;;
    
    validate-attributes)
        data="${2:-}"
        if [[ -z "$data" ]]; then
            echo "Usage: $0 validate-attributes '<json_data>'" >&2
            echo "Required: draft_product_id, length, width, height, weight, attributes[]" >&2
            exit 1
        fi
        api_request POST "/product-creation/attributes" "$data"
        ;;
    
    save-product)
        data="${2:-}"
        if [[ -z "$data" ]]; then
            echo "Usage: $0 save-product '<json_data>'" >&2
            echo "Required: category_id, draft_product_id, photos_detail{main_image,order,images[]}, use_temp_images, only_b2b" >&2
            exit 1
        fi
        api_request POST "/product-creation/save" "$data"
        ;;
    
    assign)
        product_id="${2:-}"
        if [[ -z "$product_id" ]]; then
            echo "Usage: $0 assign <product_id>" >&2
            exit 1
        fi
        data=$(jq -n --argjson product_id "$product_id" '{productId: $product_id}')
        api_request POST "/product-creation/assign" "$data"
        ;;
    
    brand-request)
        data="${2:-}"
        if [[ -z "$data" ]]; then
            echo "Usage: $0 brand-request '<json_data>'" >&2
            echo "Required: brand_origin, description, logo_id, name_en, name_fa, iranian_registration_url, category_id" >&2
            exit 1
        fi
        api_request POST "/product-creation/brand/request" "$data"
        ;;
    
    *)
        echo "Usage: $0 {search|suggest|be-seller|search-category|validate-category|validate-detail|draft-count|get-draft|auto-title|save-title|get-attributes|validate-attributes|save-product|assign|brand-request} [args]" >&2
        exit 1
        ;;
esac