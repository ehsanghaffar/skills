#!/bin/bash
# Shared helpers for the digikala scripts. Sourced, never run directly.
#
# ISOLATION CONTRACT
# ------------------
# The skill must work when it is the only skill installed, wherever it lives.
# Therefore this file never reads a hard-coded path outside the skill directory.
# The one exception is fully opt-in: the user must name the exact file through
# DIGIKALA_TOKEN_FILE. There is no implicit ~/.digikala/token lookup.
#
# CREDENTIAL CONTRACT
# -------------------
# The access token is a live seller credential. These scripts only ever *send* it
# to the Digikala API. They never print it, never write it to stdout, never place
# it in argv, and never read it from an undeclared location.

# --- base url ----------------------------------------------------------------

DEFAULT_BASE_URL="https://seller.digikala.com/open-api/v1"

die() {
    echo "Error: $1" >&2
    shift
    [[ $# -gt 0 ]] && echo "$@" >&2
    exit 1
}

# The token is attached to every request, so a redirecting base URL would send a
# live seller credential to a third party. The default is an https URL on an
# official Digikala host. Anything else (a local mock server, a self-hosted
# proxy) requires the user to opt in explicitly, and plaintext is confined to
# loopback so a real token can never travel unencrypted to a remote host.
#
# Sets the BASE_URL global rather than printing it: `die` inside a command
# substitution would only exit the subshell, leaving the caller to continue with
# an empty base URL and no error.
validate_base_url() {
    local url="${DIGIKALA_BASE_URL:-$DEFAULT_BASE_URL}"

    if [[ "$url" == "$DEFAULT_BASE_URL" ]]; then
        BASE_URL="$url"
        return 0
    fi

    local scheme rest host
    if [[ "$url" == https://* ]]; then
        scheme="https"
    elif [[ "$url" == http://* ]]; then
        scheme="http"
    else
        die "Refusing DIGIKALA_BASE_URL '$url': must be an http(s) URL."
    fi

    rest="${url#"$scheme://"}"
    host="${rest%%/*}"
    host="${host%%:*}"
    [[ "$host" =~ ^[A-Za-z0-9.-]+$ ]] || die "Refusing DIGIKALA_BASE_URL '$url': malformed host."

    if [[ "$scheme" == "http" ]]; then
        case "$host" in
            localhost | 127.0.0.1 | ::1 | "[::1]") ;;
            *) die "Refusing plaintext DIGIKALA_BASE_URL host '$host'." \
                    "http is accepted only for localhost/127.0.0.1." ;;
        esac
        [[ "${DIGIKALA_ALLOW_CUSTOM_HOST:-0}" == "1" ]] || \
            die "Refusing DIGIKALA_BASE_URL '$url'." \
                "Set DIGIKALA_ALLOW_CUSTOM_HOST=1 to target a local mock server." \
                "Never do that with a real token."
        BASE_URL="$url"
        return 0
    fi

    if [[ "$host" != "digikala.com" && "$host" != *.digikala.com ]]; then
        if [[ "${DIGIKALA_ALLOW_CUSTOM_HOST:-0}" != "1" ]]; then
            die "Refusing DIGIKALA_BASE_URL host '$host': not a digikala.com host." \
                "The seller token would be sent to it." \
                "For a local mock server, also set DIGIKALA_ALLOW_CUSTOM_HOST=1." \
                "Never do that with a real token."
        fi
    fi

    BASE_URL="$url"
}

# Guards against a caller-supplied path turning into a different origin, or
# walking out of the API namespace. Endpoints must be relative, ASCII, and free
# of traversal segments; user-supplied segments are percent-encoded by
# urlencode() before they get here.
require_relative_endpoint() {
    local endpoint="$1"
    if [[ "$endpoint" != /* ]]; then
        die "Endpoint must be an absolute API path starting with '/': '$endpoint'"
    fi
    if [[ "${endpoint:0:2}" == "//" ]]; then
        die "Endpoint must not begin with '//': '$endpoint'"
    fi
    if [[ ! "$endpoint" =~ ^/[A-Za-z0-9%._~/-]*$ ]]; then
        die "Endpoint contains unsupported characters: '$endpoint'"
    fi
    if [[ "/$endpoint/" == *"/../"* ]]; then
        die "Endpoint must not contain '..': '$endpoint'"
    fi
}

require_method() {
    local method="$1"
    case "$method" in
        GET | POST | PUT | PATCH | DELETE) return 0 ;;
        *) die "Unsupported HTTP method: '$method'" ;;
    esac
}

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

# Resolves the access token, printing it on stdout for immediate use by the
# caller. Two sources, both explicit:
#   1. DIGIKALA_ACCESS_TOKEN  - environment variable
#   2. DIGIKALA_TOKEN_FILE    - a file path the user names themselves
# No implicit home-directory path is consulted.
#
# Callers must NOT assign this with `local token=$(...)`: `local` swallows the
# exit status of the command substitution and the script would continue with an
# empty token.
get_access_token() {
    if [[ -n "${DIGIKALA_ACCESS_TOKEN:-}" ]]; then
        printf '%s' "${DIGIKALA_ACCESS_TOKEN}"
        return 0
    fi

    if [[ -n "${DIGIKALA_TOKEN_FILE:-}" ]]; then
        if [[ ! -f "${DIGIKALA_TOKEN_FILE}" || ! -r "${DIGIKALA_TOKEN_FILE}" ]]; then
            echo "Error: DIGIKALA_TOKEN_FILE is not a readable file: ${DIGIKALA_TOKEN_FILE}" >&2
            return 1
        fi
        printf '%s' "$(cat "${DIGIKALA_TOKEN_FILE}")"
        return 0
    fi

    cat >&2 <<'EOF'
Error: No access token found.
Provide the token explicitly, one of:
  export DIGIKALA_ACCESS_TOKEN="<token>"
  DIGIKALA_TOKEN_FILE=/path/to/token   # a file you choose
This skill never looks in a default location; it must be told where the token is.
EOF
    return 1
}

# Holds the Authorization header for curl. Two properties matter here:
#
#   1. The token is never an argv element. A `-H "Authorization: ..."` flag is
#      readable by any local process via ps//proc/<pid>/cmdline. curl -K reads
#      the header from a file instead, so it never enters the process table.
#   2. The file lives in a private directory. mktemp -d creates it 0700 by
#      construction, so no follow-up chmod is needed and no other user can
#      observe or replace it between creation and use.
#
# Must run in the main shell, NOT inside a command substitution, or the trap
# and the variable are lost.
_auth_dir=""

_cleanup_auth() {
    if [[ -n "$_auth_dir" && -d "$_auth_dir" && "$_auth_dir" == */digikala-curl.* ]]; then
        rm -rf -- "$_auth_dir"
    fi
    _auth_dir=""
    return 0
}

prepare_auth() {
    # Written as an `if` rather than `[[ ... ]] && return 0`: under `set -e` the
    # behaviour of a failing non-final command in an && list is subtle, and this
    # must not be the thing that silently aborts a run.
    if [[ -n "$_auth_dir" && -d "$_auth_dir" ]]; then
        return 0
    fi

    local token
    token="$(get_access_token)" || exit 1
    [[ -n "$token" ]] || die "Access token resolved to an empty value."

    _auth_dir="$(mktemp -d "${TMPDIR:-/tmp}/digikala-curl.XXXXXX")" || exit 1
    printf 'header = "Authorization: Bearer %s"\n' "$token" >"$_auth_dir/auth.conf"
    unset token
    trap _cleanup_auth EXIT
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
#
# Validation lives here rather than in each caller so that no code path can
# reach the network with an unchecked method, path, or origin.
api_request() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local content_type="${4:-application/json}"
    local n=$(( $# < 4 ? $# : 4 ))
    shift "$n"
    local -a query=("$@")

    require_method "$method"
    require_relative_endpoint "$endpoint"
    validate_base_url

    prepare_auth

    local -a args=(-sS -g -X "$method" -K "$_auth_dir/auth.conf" -H "Content-Type: $content_type")
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
# The file is uploaded as-is; callers are responsible for having verified with
# the user which file should leave the machine. Nothing is read from the user's
# home directory or any other implicit location.
api_upload() {
    local endpoint="$1"
    local file_path="$2"
    local field_name="${3:-file}"

    require_method POST
    require_relative_endpoint "$endpoint"
    [[ "$field_name" =~ ^[A-Za-z0-9_.-]+$ ]] || die "Invalid upload field name: '$field_name'"
    validate_base_url

    if [[ ! -f "$file_path" || ! -r "$file_path" ]]; then
        echo "Error: File not found or not readable: $file_path" >&2
        return 1
    fi

    prepare_auth

    curl -sS -g -X POST -K "$_auth_dir/auth.conf" -F "${field_name}=@${file_path}" \
        "$BASE_URL$endpoint"
}

# --- confirmation -----------------------------------------------------------

# Dangerous operations must confirm. Interactive terminals prompt; when stdin
# is not a TTY (agent, CI, pipeline) the caller must opt in up front with
# DIGIKALA_CONFIRM=1, otherwise the operation is refused rather than hanging.
#
# The default is refusal. An unattended run cannot silently mutate a live
# seller account: someone has to set an explicit flag, which shows up in the
# user's command history and in this script's own stderr output.
confirm_dangerous() {
    local message="$1"

    if [[ "${DIGIKALA_CONFIRM:-0}" == "1" ]]; then
        echo "$message" >&2
        echo "Proceeding: DIGIKALA_CONFIRM=1 was set for this command." >&2
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