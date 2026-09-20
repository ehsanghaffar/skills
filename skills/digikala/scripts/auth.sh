#!/bin/bash
set -e

BASE_URL="https://seller.digikala.com/open-api/v1"
CONFIG_FILE="${HOME}/.digikala/config.json"

# Load config
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        cat "$CONFIG_FILE"
    else
        echo '{}'
    fi
}

# Save config
save_config() {
    mkdir -p "$(dirname "$CONFIG_FILE")"
    echo "$1" > "$CONFIG_FILE"
}

# Get auth header
get_auth_header() {
    local config=$(load_config)
    local access_token=$(echo "$config" | jq -r '.access_token // empty')
    if [[ -z "$access_token" ]]; then
        echo "Error: No access token. Run 'get-token' first." >&2
        exit 1
    fi
    echo "Authorization: Bearer $access_token"
}

# Make API request
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

# Handle multipart upload
api_upload() {
    local endpoint="$1"
    local file_path="$2"
    local field_name="${3:-file}"
    
    local auth_header=$(get_auth_header)
    
    curl -s -X POST \
        -H "$auth_header" \
        -F "${field_name}=@${file_path}" \
        "$BASE_URL$endpoint"
}

case "${1:-}" in
    get-token)
        auth_code="${2:-}"
        if [[ -z "$auth_code" ]]; then
            echo "Usage: $0 get-token <authorization_code>" >&2
            exit 1
        fi
        response=$(curl -s -X POST \
            -H "Content-Type: application/json" \
            -d "{\"authorization_code\": \"$auth_code\"}" \
            "$BASE_URL/auth/token")
        echo "$response"
        # Save tokens to config
        access_token=$(echo "$response" | jq -r '.data.access_token // empty')
        refresh_token=$(echo "$response" | jq -r '.data.refresh_token // empty')
        if [[ -n "$access_token" && -n "$refresh_token" ]]; then
            config=$(load_config)
            config=$(echo "$config" | jq --arg at "$access_token" --arg rt "$refresh_token" '. + {access_token: $at, refresh_token: $rt}')
            save_config "$config"
            echo "Tokens saved to config" >&2
        fi
        ;;
    
    refresh)
        config=$(load_config)
        access_token=$(echo "$config" | jq -r '.access_token // empty')
        refresh_token=$(echo "$config" | jq -r '.refresh_token // empty')
        if [[ -z "$access_token" || -z "$refresh_token" ]]; then
            echo "Error: No tokens in config. Run 'get-token' first." >&2
            exit 1
        fi
        response=$(curl -s -X POST \
            -H "Content-Type: application/json" \
            -d "{\"access_token\": \"$access_token\", \"refresh_token\": \"$refresh_token\"}" \
            "$BASE_URL/auth/refresh-token")
        echo "$response"
        # Update tokens
        new_access=$(echo "$response" | jq -r '.data.access_token // empty')
        new_refresh=$(echo "$response" | jq -r '.data.refresh_token // empty')
        if [[ -n "$new_access" && -n "$new_refresh" ]]; then
            config=$(echo "$config" | jq --arg at "$new_access" --arg rt "$new_refresh" '. + {access_token: $at, refresh_token: $rt}')
            save_config "$config"
            echo "Tokens refreshed and saved" >&2
        fi
        ;;
    
    revoke)
        response=$(api_request POST "/auth/revoke")
        echo "$response"
        # Clear tokens
        save_config '{}'
        echo "Tokens revoked and cleared" >&2
        ;;
    
    scopes)
        client_code="${2:-}"
        if [[ -n "$client_code" ]]; then
            response=$(api_request GET "/auth/scopes/$client_code")
        else
            response=$(api_request GET "/auth/scopes")
        fi
        echo "$response"
        ;;
    
    *)
        echo "Usage: $0 {get-token|refresh|revoke|scopes} [args]" >&2
        echo "  get-token <auth_code>     - Exchange auth code for tokens" >&2
        echo "  refresh                   - Refresh expired access token" >&2
        echo "  revoke                    - Revoke current token" >&2
        echo "  scopes [client_code]      - List available scopes" >&2
        exit 1
        ;;
esac