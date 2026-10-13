#!/bin/bash
# Shared helpers for the digikala scripts. Sourced, never run directly.
# Keep this file inside the skill directory: the skill must work when it is
# the only skill installed, so nothing here may reach outside this directory.

BASE_URL="${DIGIKALA_BASE_URL:-https://seller.digikala.com/open-api/v1}"

# --- dependencies -----------------------------------------------------------

require_cmds() {
    local missing=()
    local cmd
    for cmd in "$@"; do
        command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
    done
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Error: missing required command(s): ${missing[*]}" >&2
        echo "Install them and retry (e.g. brew install ${missing[*]})." >&2
        exit 127
    fi
}

# --- authentication ---------------------------------------------------------

# Resolves the access token from the environment, then ~/.digikala/token.
# Prints the token on stdout, or exits non-zero. Callers must NOT assign this
# with `local token=$(...)`: `local` swallows the exit status of the command
# substitution and the script would continue with an empty token.
get_access_token() {
    if [[ -n "${DIGIKALA_ACCESS_TOKEN:-}" ]]; then
        printf '%s' "${DIGIKALA_ACCESS_TOKEN}"
        return 0
    fi

    if [[ -n "${HOME:-}" && -f "${HOME}/.digikala/token" ]]; then
        printf '%s' "$(cat "${HOME}/.digikala/token")"
        return 0
    fi

    echo "Error: No access token found." >&2
    echo "Provide token via DIGIKALA_ACCESS_TOKEN env var or ~/.digikala/token file" >&2
    return 1
}

# Sets _auth_config to the path of a 0600 curl config file holding the
# Authorization header, and registers cleanup on EXIT. The token goes in a
# file rather than a -H argument so it never appears in the process table
# (`ps`, /proc/*/cmdline). Must run in the main shell, NOT inside a
# command substitution, or the trap and the variable are lost.
_auth_config=""

_cleanup_auth_config() {
    [[ -n "$_auth_config" && -f "$_auth_config" ]] && rm -f "$_auth_config"
    return 0
}

prepare_auth() {
    [[ -n "$_auth_config" && -f "$_auth_config" ]] && return 0

    local token
    token="$(get_access_token)" || exit 1

    _auth_config="$(mktemp "${TMPDIR:-/tmp}/digikala-curl.XXXXXX")" || exit 1
    chmod 600 "$_auth_config"
    printf 'header = "Authorization: Bearer %s"\n' "$token" >"$_auth_config"
    trap _cleanup_auth_config EXIT
}

# --- URL encoding -----------------------------------------------------------

# Percent-encodes a value for use inside a URL *path* segment.
# Query strings should go through curl --data-urlencode instead.
urlencode() {
    local value="$1"
    if command -v jq >/dev/null 2>&1; then
        jq -rn --arg s "$value" '$s|@uri'
    elif command -v python3 >/dev/null 2>&1; then
        python3 -c 'import sys,urllib.parse; sys.stdout.write(urllib.parse.quote(sys.argv[1], safe=""))' "$value"
    else
        echo "Error: need jq or python3 to URL-encode '$value'" >&2
        return 1
    fi
}

# --- HTTP -------------------------------------------------------------------

# api_request METHOD PATH [JSON_BODY] [CONTENT_TYPE] [QUERY_ARG...]
# QUERY_ARGs are raw "key=value" pairs passed to --data-urlencode, so values
# may contain spaces, Persian text, and characters like [ and ] that curl
# would otherwise read as URL globs.
api_request() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local content_type="${4:-application/json}"
    local n=$(( $# < 4 ? $# : 4 ))
    shift "$n"
    local -a query=("$@")

    prepare_auth

    local -a args=(-sS -g -X "$method" -K "$_auth_config" -H "Content-Type: $content_type")
    local pair
    if [[ ${#query[@]} -gt 0 ]]; then
        [[ "$method" == "GET" ]] || { echo "Error: query args only supported for GET" >&2; return 1; }
        [[ -n "$data" ]] && { echo "Error: GET query args and a request body cannot be combined" >&2; return 1; }
        args+=(-G)
        for pair in "${query[@]}"; do
            [[ -n "$pair" ]] && args+=(--data-urlencode "$pair")
        done
    else
        [[ -n "$data" ]] && args+=(-d "$data")
    fi

    curl "${args[@]}" "$BASE_URL$endpoint"
}

# api_upload PATH FILE_PATH [FIELD_NAME]
api_upload() {
    local endpoint="$1"
    local file_path="$2"
    local field_name="${3:-file}"

    if [[ ! -f "$file_path" ]]; then
        echo "Error: File not found: $file_path" >&2
        return 1
    fi

    prepare_auth

    curl -sS -g -X POST -K "$_auth_config" -F "${field_name}=@${file_path}" \
        "$BASE_URL$endpoint"
}

# --- confirmation -----------------------------------------------------------

# Dangerous operations must confirm. Interactive terminals prompt; when stdin
# is not a TTY (agent, CI, pipeline) the caller must opt in up front with
# DIGIKALA_CONFIRM=1, otherwise the operation is refused rather than hanging.
confirm_dangerous() {
    local message="$1"

    if [[ "${DIGIKALA_CONFIRM:-0}" == "1" ]]; then
        echo "$message (proceeding: DIGIKALA_CONFIRM=1)" >&2
        return 0
    fi

    if [[ ! -t 0 ]]; then
        echo "$message" >&2
        echo "Refusing to proceed: stdin is not a terminal, so it cannot be confirmed." >&2
        echo "Re-run with DIGIKALA_CONFIRM=1 to confirm non-interactively." >&2
        return 1
    fi

    echo "$message" >&2
    local reply=""
    read -r -p "Confirm? (y/N) " reply </dev/tty 2>/dev/null || read -r -p "Confirm? (y/N) " reply
    [[ "$reply" =~ ^[Yy]$ ]] || { echo "Aborted." >&2; return 1; }
}
