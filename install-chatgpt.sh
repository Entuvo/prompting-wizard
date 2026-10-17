#!/bin/sh
# Register Prompting Wizard as a local plugin in the ChatGPT desktop app.
#   curl -fsSL https://raw.githubusercontent.com/Entuvo/prompting-wizard/v<version>/install-chatgpt.sh | sh
#   sh install-chatgpt.sh [--zip PATH] [--uninstall]
# Without --zip it uses ~/Downloads/prompting-wizard-openai.zip when that file matches the pinned
# release's SHA256SUMS, and otherwise downloads the zip from the pinned release.
# With --zip it checks the zip against the SHA256SUMS beside it, or else the pinned release's.

set -eu

version=1.5.3
zip_name=prompting-wizard-openai.zip
release_url=${PW_RELEASE_URL:-https://github.com/Entuvo/prompting-wizard/releases/download/v$version}

fail() {
    echo "Error: $*" >&2
    exit 1
}

usage() {
    echo "Usage: install-chatgpt.sh [--zip PATH] [--uninstall]" >&2
    exit 2
}

sha256_of() {
    if command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$1" | cut -d ' ' -f 1
    elif command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$1" | cut -d ' ' -f 1
    else
        fail "shasum or sha256sum is required to verify the download"
    fi
}

verify_checksum() {
    expected=$(awk -v name="$zip_name" '$2 == name || $2 == "*" name { print $1; exit }' "$2")
    [ -n "$expected" ] || fail "SHA256SUMS has no line for $zip_name"
    actual=$(sha256_of "$1")
    if [ "$actual" != "$expected" ]; then
        given=$(basename -- "$1")
        [ "$given" = "$zip_name" ] || fail "wrong zip: $given is not $zip_name from the $version release; nothing was installed"
        fail "checksum mismatch for $zip_name (expected $expected, got $actual); nothing was installed"
    fi
    echo "Checksum verified: $zip_name"
}

# Reads a marketplace file and writes the planned one. Prints "unchanged" or "changed".
# Exit 3: the existing file is not valid marketplace JSON.
plan_marketplace() {
    python3 -I - "$@" <<'PY'
import json, os, sys
from pathlib import Path

mode, current, planned = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
entry = {
    "name": "prompting-wizard",
    "source": {"source": "local", "path": "./.codex/plugins/prompting-wizard"},
    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
    "category": "Productivity",
}
if current.exists():
    raw = current.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except ValueError as exc:
        print(f"Error: {current} is not valid JSON ({exc}); it was not changed", file=sys.stderr)
        sys.exit(3)
    if not isinstance(data, dict) or not isinstance(data.get("plugins", []), list):
        print(f"Error: {current} is not a marketplace (an object with a plugins list); it was not changed", file=sys.stderr)
        sys.exit(3)
else:
    raw, data = None, {"name": "personal", "interface": {"displayName": "Personal"}, "plugins": []}

plugins = data.setdefault("plugins", [])
ours = [i for i, p in enumerate(plugins) if isinstance(p, dict) and p.get("name") == entry["name"]]
kept = [p for i, p in enumerate(plugins) if i not in ours]
if mode == "install":
    kept.insert(ours[0] if ours else len(kept), {**plugins[ours[0]], **entry} if ours else entry)
data["plugins"] = kept

text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
if raw is not None and json.loads(raw) == data:
    print("unchanged")
elif raw is None and mode == "uninstall":
    print("unchanged")
else:
    planned.write_text(text, encoding="utf-8")
    os.chmod(planned, current.stat().st_mode & 0o7777 if raw is not None else 0o644)
    print("changed")
PY
}

print_manual_entry() {
    cat >&2 <<EOF
python3 is required to edit $marketplace. Add this entry to its "plugins" list by hand:

    {
      "name": "prompting-wizard",
      "source": { "source": "local", "path": "./.codex/plugins/prompting-wizard" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Productivity"
    }

A new file also needs "name" and "plugins" at the top level, as in:
    { "name": "personal", "interface": { "displayName": "Personal" }, "plugins": [ <the entry> ] }
EOF
}

update_marketplace() {
    action=$1
    if [ "$action" = uninstall ] && [ ! -e "$marketplace" ]; then
        echo "No marketplace to update: $marketplace"
        return 0
    fi
    mkdir -p "$marketplace_dir"
    planned=$(mktemp "$marketplace_dir/.marketplace.json.XXXXXX")
    status=0
    result=$(plan_marketplace "$action" "$marketplace" "$planned") || status=$?
    if [ "$status" -ne 0 ]; then
        rm -f "$planned"
        exit 1
    fi
    if [ "$result" = unchanged ]; then
        rm -f "$planned"
        echo "Marketplace already up to date: $marketplace"
        return 0
    fi
    if [ -e "$marketplace" ]; then
        backup="$marketplace.bak-$(date +%Y%m%d%H%M%S)"
        cp -p "$marketplace" "$backup"
        echo "Backed up $marketplace to $backup"
    fi
    mv -f "$planned" "$marketplace"
    echo "Updated $marketplace"
}

main() {
    zip_path=
    action=install
    while [ "$#" -gt 0 ]; do
        case "$1" in
            --zip) [ "$#" -ge 2 ] || usage; zip_path=$2; shift ;;
            --uninstall) action=uninstall ;;
            -h|--help) usage ;;
            *) usage ;;
        esac
        shift
    done

    : "${HOME:?HOME must be set}"
    plugins_dir="$HOME/.codex/plugins"
    target="$plugins_dir/prompting-wizard"
    previous="$plugins_dir/.prompting-wizard.previous"
    marketplace_dir="$HOME/.agents/plugins"
    marketplace="$marketplace_dir/marketplace.json"

    [ ! -L "$target" ] || fail "$target is a symlink; remove it and run again"
    [ ! -L "$marketplace" ] || fail "$marketplace is a symlink; refusing to edit it"
    have_python=yes
    command -v python3 >/dev/null 2>&1 || have_python=no

    if [ "$action" = uninstall ]; then
        if [ "$have_python" = no ]; then
            echo "Remove $target and the prompting-wizard entry from $marketplace by hand." >&2
            exit 1
        fi
        update_marketplace uninstall
        if [ -d "$target" ]; then
            rm -rf "$previous"
            mv "$target" "$previous"
            echo "Removed $target (backup: $previous)"
        fi
        echo "Prompting Wizard is unregistered. Quit and reopen the ChatGPT desktop app, and uninstall it under Plugins if it is still listed."
        return 0
    fi

    work=$(mktemp -d)
    stage=
    trap 'rm -rf "$work"; [ -z "$stage" ] || rm -rf "$stage"' 0
    trap 'exit 130' 2
    trap 'exit 143' 15

    if [ -n "$zip_path" ]; then
        [ -f "$zip_path" ] || fail "zip not found: $zip_path"
        sums="$(dirname -- "$zip_path")/SHA256SUMS"
        if [ ! -f "$sums" ]; then
            sums="$work/SHA256SUMS"
            if command -v curl >/dev/null 2>&1 && curl -fsSL -o "$sums" "$release_url/SHA256SUMS" </dev/null 2>/dev/null; then
                echo "Fetched SHA256SUMS for $version from $release_url"
            else
                sums=
                echo "Warning: no SHA256SUMS beside $zip_path and $release_url/SHA256SUMS could not be fetched; installing it without a checksum check" >&2
            fi
        fi
        [ -z "$sums" ] || verify_checksum "$zip_path" "$sums"
    else
        command -v curl >/dev/null 2>&1 || fail "curl is required to download the release"
        curl -fsSL -o "$work/SHA256SUMS" "$release_url/SHA256SUMS" </dev/null || fail "download failed: $release_url/SHA256SUMS"
        downloaded="$HOME/Downloads/$zip_name"
        if [ -f "$downloaded" ] && (verify_checksum "$downloaded" "$work/SHA256SUMS") >/dev/null 2>&1; then
            echo "Using $downloaded: it matches the $version release checksum"
            zip_path=$downloaded
        else
            if [ -f "$downloaded" ]; then
                echo "$downloaded is not the $version release; downloading $version instead"
            fi
            echo "Downloading Prompting Wizard $version from $release_url"
            curl -fsSL -o "$work/$zip_name" "$release_url/$zip_name" </dev/null || fail "download failed: $release_url/$zip_name"
            zip_path="$work/$zip_name"
            verify_checksum "$zip_path" "$work/SHA256SUMS"
        fi
    fi

    # Check the marketplace before touching the plugin folder, so invalid JSON or an
    # unwritable folder leaves nothing half installed.
    if [ "$have_python" = yes ]; then
        plan_marketplace install "$marketplace" "$work/marketplace.check" >/dev/null || exit 1
        probe=$( { mkdir -p "$marketplace_dir" && mktemp "$marketplace_dir/.marketplace.json.XXXXXX"; } 2>/dev/null) ||
            fail "cannot write to $marketplace_dir; nothing was installed"
        rm -f "$probe"
    fi

    command -v unzip >/dev/null 2>&1 || fail "unzip is required"
    mkdir -p "$plugins_dir"
    stage=$(mktemp -d "$plugins_dir/.prompting-wizard.stage.XXXXXX")
    unzip -q "$zip_path" -d "$stage" </dev/null || fail "cannot unzip $zip_path"
    grep -q '"name": *"prompting-wizard"' "$stage/plugin.json" 2>/dev/null || \
        fail "$zip_path is not the Prompting Wizard plugin (plugin.json name is not prompting-wizard)"
    [ -z "$(find "$stage" -type l | head -n 1)" ] || fail "$zip_path contains symlinks; refusing to install it"
    chmod -R u+rwX,go=rX "$stage"

    moved=no
    if [ -e "$target" ]; then
        rm -rf "$previous"
        mv "$target" "$previous"
        moved=yes
    fi
    if ! mv "$stage" "$target"; then
        [ ! -d "$previous" ] || mv "$previous" "$target"
        fail "cannot move the plugin into $target; the previous copy was restored"
    fi
    stage=
    echo "Installed Prompting Wizard $version: $target"
    [ "$moved" = no ] || echo "Previous copy kept at $previous"

    if [ "$have_python" = no ]; then
        print_manual_entry
        exit 1
    fi
    update_marketplace install

    cat <<'EOF'

One step is left, in the ChatGPT desktop app:
1. Quit the app and open it again.
2. Open Plugins, then Personal, and install Prompting Wizard.
3. Start a new chat and say: "Use Prompting Wizard to teach me through my work; no interview."
EOF
}

main "$@"
