#!/usr/bin/env bash
# Keeps local working material out of this public repository.
# Usage: leak-check.sh staged | message <file> | push <old> <new> | tree
# Extra patterns come from $LEAK_DENYLIST (CI secret) or the file at
# $LEAK_DENYLIST_FILE (default ~/.config/entuvo/leak-denylist.txt), one
# extended regex per line. Reports print file and line numbers only.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

blocked='^(\.[^/]+/|AGENTS\.md$|CLAUDE\.md$|PRODUCT\.md$|docs/|listing/|dist/)'
allowed='^(\.github/|\.gitignore$|\.claude-plugin/|\.agents/plugins/)'
generic='(/Users/[A-Za-z]|/home/[a-z]|"modelUsage"|"costUSD"|PRIVATE KEY-----)'
generic_exempt='^tools/(validate|test_validate|leak-check)\.(py|sh)$'

deny=""
list_file="${LEAK_DENYLIST_FILE:-$HOME/.config/entuvo/leak-denylist.txt}"
if [ -n "${LEAK_DENYLIST:-}" ]; then
  deny=$(mktemp); printf '%s\n' "$LEAK_DENYLIST" | grep -v -e '^#' -e '^$' > "$deny" || true
elif [ -f "$list_file" ]; then
  deny=$(mktemp); grep -v -e '^#' -e '^$' "$list_file" > "$deny" || true
else
  echo "leak-check: private denylist not found; generic checks only" >&2
fi

fail=0
flag=$(mktemp)
report() { echo "leak-check: $1" >&2; echo 1 > "$flag"; }

scan() { # $1 label, $2 path ("" for metadata); content on stdin
  local tmp hits; tmp=$(mktemp); cat > "$tmp"
  # Runs in a pipeline subshell, so failures are recorded in $flag, not $fail.
  if [ -n "$2" ] && [[ $2 =~ $blocked ]] && ! [[ $2 =~ $allowed ]]; then
    report "$1: path is not allowed in this repository"
  fi
  if ! [[ $2 =~ $generic_exempt ]]; then
    hits=$(grep -n -I -E "$generic" "$tmp" | cut -d: -f1 | tr '\n' ' ' || true)
    [ -n "$hits" ] && report "$1: lines $hits: local path, run log or key"
  fi
  if [ -n "$deny" ] && [ -s "$deny" ]; then
    hits=$(grep -n -I -i -E -f "$deny" "$tmp" | cut -d: -f1 | tr '\n' ' ' || true)
    [ -n "$hits" ] && report "$1: lines $hits: matches private denylist"
  fi
  rm -f "$tmp"
}

case "${1:-tree}" in
  staged)
    git var GIT_AUTHOR_IDENT | scan "author identity" ""
    while IFS= read -r f; do git show ":$f" | scan "$f" "$f"; done \
      < <(git diff --cached --name-only --diff-filter=ACMR) ;;
  message)
    scan "commit message" "" < "$2" ;;
  push)
    if [[ $2 =~ ^0+$ ]]; then range=("$3" --not --remotes); else range=("$2..$3"); fi
    git log --format='%an%n%ae%n%cn%n%ce%n%B' "${range[@]}" | scan "commit metadata" ""
    while IFS= read -r c; do
      while IFS= read -r f; do git show "$c:$f" | scan "${c:0:7}:$f" "$f"; done \
        < <(git diff-tree -r --root --no-commit-id --name-only --diff-filter=ACMR "$c")
    done < <(git rev-list "${range[@]}") ;;
  tree)
    while IFS= read -r f; do [ -f "$f" ] && scan "$f" "$f" < "$f"; done < <(git ls-files) ;;
  *) echo "usage: leak-check.sh staged | message <file> | push <old> <new> | tree" >&2; exit 2 ;;
esac

[ -s "$flag" ] && fail=1
rm -f "$flag"; [ -n "$deny" ] && rm -f "$deny"
exit $fail
