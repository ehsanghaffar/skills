#!/bin/bash
set -e

BASE_URL="https://seller.digikala.com/open-api/v1"

# Token must be provided via DIGIKALA_ACCESS_TOKEN environment variable
# or ~/.digikala/token file (user-managed)
get_access_token() {
    if [[ -n "${DIGIKALA_ACCESS_TOKEN:-}" ]]; then
        echo "${DIGIKALA_ACCESS_TOKEN}"
        return 0
    fi
    
    local token_file="${HOME}/.digikala/token"
    if [[ -f "$token_file" ]]; then
        cat "$token_file"
        return 0
    fi
    
    echo "Error: No access token found." >&2
    echo "Provide token via DIGIKALA_ACCESS_TOKEN env var or ~/.digikala/token file" >&2
    exit 1
}

get_auth_header() {
    local token=$(get_access_token)
    echo "Authorization: Bearer $token"
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
    tree)
        parent_id="${2:-}"
        if [[ -n "$parent_id" ]]; then
            api_request GET "/categories/tree?search[parent_id]=$parent_id"
        else
            api_request GET "/categories/tree"
        fi
        ;;
    
    search)
        keyword="${2:-}"
        if [[ -z "$keyword" ]]; then
            echo "Usage: $0 search <keyword>" >&2
            exit 1
        fi
        api_request GET "/product-creation/search/category/v2/$keyword"
        ;;
    
    validate)
        category_id="${2:-}"
        if [[ -z "$category_id" ]]; then
            echo "Usage: $0 validate <category_id>" >&2
            exit 1
        fi
        api_request GET "/product-creation/category/$category_id/validation"
        ;;
    
    *)
        echo "Usage: $0 {tree|search|validate} [args]" >&2
        echo "  tree [parent_id]          - Get category tree (root or children)" >&2
        echo "  search <keyword>          - Search categories by keyword" >&2
        echo "  validate <category_id>    - Validate category for product creation" >&2
        echo "" >&2
        echo "Authentication: Set DIGIKALA_ACCESS_TOKEN env var or create ~/.digikala/token file" >&2
        exit 1
        ;;
esac