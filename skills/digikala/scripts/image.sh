#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_common.sh
source "$SCRIPT_DIR/_common.sh"

require_cmds curl jq

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
        echo "Authentication: export DIGIKALA_ACCESS_TOKEN=<token>, or point DIGIKALA_TOKEN_FILE at a file you choose" >&2
        exit 1
        ;;
esac
