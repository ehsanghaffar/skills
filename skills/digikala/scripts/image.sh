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

api_upload() {
    local endpoint="$1"
    local file_path="$2"
    local field_name="${3:-file}"
    
    local auth_header=$(get_auth_header)
    
    if [[ ! -f "$file_path" ]]; then
        echo "Error: File not found: $file_path" >&2
        exit 1
    fi
    
    curl -s -X POST \
        -H "$auth_header" \
        -F "${field_name}=@${file_path}" \
        "$BASE_URL$endpoint"
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
    upload-product)
        file_path="${2:-}"
        if [[ -z "$file_path" ]]; then
            echo "Usage: $0 upload-product <file_path>" >&2
            exit 1
        fi
        api_upload "/product-creation/images/upload" "$file_path"
        ;;
    
    upload-request)
        file_path="${2:-}"
        if [[ -z "$file_path" ]]; then
            echo "Usage: $0 upload-request <file_path>" >&2
            exit 1
        fi
        api_upload "/product-creation/images/requests/upload" "$file_path"
        ;;
    
    upload-brand)
        file_path="${2:-}"
        if [[ -z "$file_path" ]]; then
            echo "Usage: $0 upload-brand <file_path>" >&2
            exit 1
        fi
        api_upload "/product-creation/images/requests/brand-logo/upload" "$file_path"
        ;;
    
    ai-check)
        image_id="${2:-}"
        is_main="${3:-true}"
        if [[ -z "$image_id" ]]; then
            echo "Usage: $0 ai-check <image_id> [is_main:true|false]" >&2
            exit 1
        fi
        data=$(jq -n --arg image_id "$image_id" --argjson is_main "$is_main" '{image_id: $image_id, is_main: $is_main}')
        api_request POST "/product-creation/images/ai" "$data"
        ;;
    
    *)
        echo "Usage: $0 {upload-product|upload-request|upload-brand|ai-check} [args]" >&2
        echo "  upload-product <file>     - Upload product image to temp storage" >&2
        echo "  upload-request <file>     - Upload content request image" >&2
        echo "  upload-brand <file>       - Upload brand logo image" >&2
        echo "  ai-check <image_id> [is_main] - AI quality check on uploaded image" >&2
        echo "" >&2
        echo "Authentication: Set DIGIKALA_ACCESS_TOKEN env var or create ~/.digikala/token file" >&2
        exit 1
        ;;
esac