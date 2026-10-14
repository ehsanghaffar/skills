#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_common.sh
source "$SCRIPT_DIR/_common.sh"

require_cmds curl

case "${1:-}" in
    tree)
        parent_id="${2:-}"
        if [[ -n "$parent_id" ]]; then
            api_request GET "/categories/tree" "" "" "search[parent_id]=$parent_id"
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
        api_request GET "/product-creation/search/category/v2/$(urlencode "$keyword")"
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
        echo "Authentication: export DIGIKALA_ACCESS_TOKEN=<token>, or point DIGIKALA_TOKEN_FILE at a file you choose" >&2
        exit 1
        ;;
esac
