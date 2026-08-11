#!/bin/sh

set -eu

usage() {
    echo "Usage: install.sh [--codex|--claude-code|--all] [--force]" >&2
}

fail() {
    echo "Error: $*" >&2
    exit 1
}

path_exists() {
    [ -e "$1" ] || [ -L "$1" ]
}

selected=auto
force=no
while [ "$#" -gt 0 ]; do
    case "$1" in
        --codex) selected=codex ;;
        --claude-code) selected=claude ;;
        --all) selected=all ;;
        --force) force=yes ;;
        *) usage; exit 2 ;;
    esac
    shift
done

: "${HOME:?HOME must be set}"

repo_root=${PW_REPO_ROOT:-$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)}
skill_source="$repo_root/prompting-wizard"
codex_root=${PW_CODEX_SKILLS_DIR:-"$HOME/.agents/skills"}
claude_root=${PW_CLAUDE_SKILLS_DIR:-"$HOME/.claude/skills"}

[ -d "$repo_root" ] || fail "repository root is not a directory: $repo_root"
[ -d "$skill_source" ] || fail "canonical skill directory not found: $skill_source"
[ -f "$repo_root/tools/validate.py" ] || fail "validator not found: $repo_root/tools/validate.py"
command -v python3 >/dev/null 2>&1 || fail "python3 is required"

repo_root_real=$(CDPATH= cd -P -- "$repo_root" && pwd)
skill_source_real=$(CDPATH= cd -P -- "$skill_source" && pwd)
home_real=
if [ -d "$HOME" ]; then
    home_real=$(CDPATH= cd -P -- "$HOME" && pwd)
fi

# The canonical source must pass its complete structural validation before a
# skills root, staging directory, backup, or target is created or changed.
python3 "$repo_root/tools/validate.py" --complete

install_codex=no
install_claude=no
case "$selected" in
    codex) install_codex=yes ;;
    claude) install_claude=yes ;;
    all)
        install_codex=yes
        install_claude=yes
        ;;
    auto)
        if command -v codex >/dev/null 2>&1; then
            install_codex=yes
        fi
        if command -v claude >/dev/null 2>&1; then
            install_claude=yes
        fi
        if [ "$install_codex" = no ] && [ "$install_claude" = no ]; then
            fail "no supported client detected; use --codex, --claude-code, or --all"
        fi
        ;;
esac

resolve_skills_root() {
    case "$1" in
        /*) ;;
        *) fail "skills root must be an absolute path: $1" ;;
    esac
    mkdir -p -- "$1"
    resolved_root=$(CDPATH= cd -P -- "$1" && pwd)
    [ "$resolved_root" != / ] || fail "refusing to use the filesystem root as a skills root"
}

confirm_replacement() {
    confirm_target=$1
    confirm_label=$2
    replacement_allowed=$force
    if ! path_exists "$confirm_target"; then
        return 0
    fi
    if [ "$force" = yes ]; then
        return 0
    fi

    replacement_allowed=no
    if [ -t 0 ]; then
        tty_open=no
        exec 4>&2
        if exec 3<>/dev/tty 2>/dev/null; then
            tty_open=yes
        fi
        exec 2>&4
        exec 4>&-
        if [ "$tty_open" = yes ] && [ -t 3 ]; then
            printf '%s already exists at %s. Replace it? [y/N] ' \
                "$confirm_label" "$confirm_target" >&3
            reply=
            IFS= read -r reply <&3 || true
            case "$reply" in
                y|Y|yes|YES|Yes) replacement_allowed=yes ;;
            esac
        fi
        if [ "$tty_open" = yes ]; then
            exec 3>&-
        fi
    fi

    if [ "$replacement_allowed" != yes ]; then
        fail "$confirm_label is already installed at $confirm_target; rerun with --force in noninteractive mode"
    fi
}

codex_target=
codex_replace=no
if [ "$install_codex" = yes ]; then
    resolve_skills_root "$codex_root"
    codex_root=$resolved_root
    codex_target="$codex_root/prompting-wizard"
    [ "$codex_target" != "$skill_source_real" ] || fail "install target is the canonical source"
    confirm_replacement "$codex_target" "Codex skill"
    codex_replace=$replacement_allowed
fi

claude_target=
claude_replace=no
if [ "$install_claude" = yes ]; then
    resolve_skills_root "$claude_root"
    claude_root=$resolved_root
    claude_target="$claude_root/prompting-wizard"
    [ "$claude_target" != "$skill_source_real" ] || fail "install target is the canonical source"
    confirm_replacement "$claude_target" "Claude Code skill"
    claude_replace=$replacement_allowed
fi

if [ "$install_codex" = yes ] && [ "$install_claude" = yes ] && \
        [ "$codex_target" = "$claude_target" ]; then
    fail "Codex and Claude Code cannot share one prompting-wizard target"
fi

safe_remove() {
    remove_path=$1
    remove_root=$2
    remove_kind=$3
    remove_parent=${remove_path%/*}
    remove_base=${remove_path##*/}

    [ -n "$remove_path" ] || return 1
    [ "$remove_parent" = "$remove_root" ] || return 1
    [ "$remove_path" != "$remove_root" ] || return 1
    [ "$remove_path" != "$repo_root_real" ] || return 1
    [ "$remove_path" != "$skill_source_real" ] || return 1
    if [ -n "$home_real" ]; then
        [ "$remove_path" != "$home_real" ] || return 1
    fi

    case "$remove_kind:$remove_base" in
        target:prompting-wizard) ;;
        stage:.prompting-wizard.stage.?*) ;;
        backup:.prompting-wizard.backup.?*) ;;
        *) return 1 ;;
    esac

    rm -rf -- "$remove_path"
}

copy_skill() {
    python3 - "$1" "$2" "$3" <<'PY'
import os
import shutil
import sys

source, destination, host = sys.argv[1:]


def ignored(directory, names):
    excluded = {
        name
        for name in names
        if name == "PROGRESS.md" or name == "__pycache__" or name.endswith(".pyc")
    }
    if host == "codex" and os.path.samefile(directory, source):
        excluded.add(".claude-plugin")
    return excluded


for entry in os.listdir(source):
    if entry in ignored(source, os.listdir(source)):
        continue
    src = os.path.join(source, entry)
    dst = os.path.join(destination, entry)
    if os.path.isdir(src) and not os.path.islink(src):
        shutil.copytree(src, dst, symlinks=True, ignore=ignored)
    else:
        shutil.copy2(src, dst, follow_symlinks=False)
PY
}

rename_exact() {
    python3 - rename "$1" "$2" <<'PY'
import ctypes
import errno
import os
import sys

_, source, destination = sys.argv[1:]


def rename_without_replacement(src, dst):
    libc = ctypes.CDLL(None, use_errno=True)
    encoded_src = os.fsencode(src)
    encoded_dst = os.fsencode(dst)
    if sys.platform == "darwin":
        rename = libc.renamex_np
        rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        rename.restype = ctypes.c_int
        result = rename(encoded_src, encoded_dst, 0x00000004)  # RENAME_EXCL
    elif sys.platform.startswith("linux") and hasattr(libc, "renameat2"):
        rename = libc.renameat2
        rename.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        rename.restype = ctypes.c_int
        result = rename(-100, encoded_src, -100, encoded_dst, 1)  # RENAME_NOREPLACE
    else:
        raise OSError(
            errno.ENOTSUP,
            "atomic no-replace directory rename is unavailable",
            dst,
        )
    if result != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), dst)


try:
    rename_without_replacement(source, destination)
except OSError as exc:
    print(f"Error: cannot rename {source} to {destination}: {exc}", file=sys.stderr)
    raise SystemExit(1)
PY
}

directory_identity() {
    python3 - identity "$1" <<'PY'
import os
import sys

stat = os.stat(sys.argv[2], follow_symlinks=False)
print(f"{stat.st_dev}:{stat.st_ino}")
PY
}

same_directory_identity() {
    python3 - same-identity "$1" "$2" <<'PY'
import os
import sys

try:
    stat = os.stat(sys.argv[2], follow_symlinks=False)
except OSError:
    raise SystemExit(1)
actual = f"{stat.st_dev}:{stat.st_ino}"
raise SystemExit(0 if actual == sys.argv[3] else 1)
PY
}

verify_install_tree() {
    verify_tree=$1
    verify_host=$2
    for verify_file in SKILL.md AGENTS.md assessment.md rubrics.md VERSION.md CHANGELOG.md; do
        [ -f "$verify_tree/$verify_file" ] || {
            echo "Error: installed skill is missing $verify_file" >&2
            return 1
        }
    done
    verify_day=1
    while [ "$verify_day" -le 30 ]; do
        verify_name=$(printf '%02d' "$verify_day")
        [ -f "$verify_tree/days/$verify_name.md" ] || {
            echo "Error: installed skill is missing days/$verify_name.md" >&2
            return 1
        }
        verify_day=$((verify_day + 1))
    done

    verify_artifact=$(find "$verify_tree" \
        \( -name PROGRESS.md -o -name __pycache__ -o -name '*.pyc' \) \
        -print | sed -n '1p')
    [ -z "$verify_artifact" ] || {
        echo "Error: excluded artifact was installed: $verify_artifact" >&2
        return 1
    }
    if [ "$verify_host" = codex ]; then
        if path_exists "$verify_tree/.claude-plugin"; then
            echo "Error: Claude manifest was installed into the Codex skill" >&2
            return 1
        fi
    else
        [ -f "$verify_tree/.claude-plugin/plugin.json" ] || {
            echo "Error: Claude manifest is missing from the Claude Code skill" >&2
            return 1
        }
    fi
}

install_one() (
    set -eu
    install_host=$1
    install_label=$2
    install_root=$3
    install_target=$4
    install_replace=$5
    stage_path=
    backup_path=
    prior_moved=no
    installed_moved=no
    transaction_state=active
    stage_identity=

    rollback_install() {
        rollback_ok=yes
        if [ "$installed_moved" = yes ] && path_exists "$install_target"; then
            if same_directory_identity "$install_target" "$stage_identity"; then
                safe_remove "$install_target" "$install_root" target || rollback_ok=no
            fi
        fi
        if [ "$prior_moved" = yes ] && path_exists "$backup_path/original"; then
            if ! path_exists "$install_target"; then
                rename_exact "$backup_path/original" "$install_target" || rollback_ok=no
            else
                rollback_ok=no
            fi
        fi
        if [ -n "$stage_path" ] && path_exists "$stage_path"; then
            safe_remove "$stage_path" "$install_root" stage || rollback_ok=no
        fi
        if [ -n "$backup_path" ] && path_exists "$backup_path"; then
            if ! path_exists "$backup_path/original"; then
                safe_remove "$backup_path" "$install_root" backup || rollback_ok=no
            else
                rollback_ok=no
            fi
        fi
        [ "$rollback_ok" = yes ]
    }

    installer_exit() {
        install_status=$?
        trap - 0 1 2 15
        if [ "$install_status" -ne 0 ] && [ "$transaction_state" != committed ]; then
            set +e
            restore_expected=no
            if [ "$prior_moved" = yes ] && path_exists "$backup_path/original"; then
                restore_expected=yes
            fi
            if ! rollback_install; then
                echo "Error: automatic rollback was incomplete; prior data remains in $backup_path" >&2
            elif [ "$restore_expected" = yes ]; then
                echo "Error: installation failed; prior installation restored" >&2
            fi
        fi
        exit "$install_status"
    }

    trap 'installer_exit' 0
    trap 'exit 129' 1
    trap 'exit 130' 2
    trap 'exit 143' 15

    if path_exists "$install_target" && [ "$install_replace" != yes ]; then
        echo "Error: $install_label appeared after confirmation; refusing to replace it" >&2
        exit 1
    fi

    stage_path=$(mktemp -d "$install_root/.prompting-wizard.stage.XXXXXX")
    case "${stage_path%/*}:${stage_path##*/}" in
        "$install_root":.prompting-wizard.stage.?*) ;;
        *) echo "Error: mktemp returned an unsafe staging path" >&2; exit 1 ;;
    esac
    copy_skill "$skill_source_real" "$stage_path" "$install_host"
    verify_install_tree "$stage_path" "$install_host"
    stage_identity=$(directory_identity "$stage_path")

    if path_exists "$install_target"; then
        if [ "$install_replace" != yes ]; then
            echo "Error: $install_label appeared during staging; refusing to replace it" >&2
            exit 1
        fi
        backup_path=$(mktemp -d "$install_root/.prompting-wizard.backup.XXXXXX")
        case "${backup_path%/*}:${backup_path##*/}" in
            "$install_root":.prompting-wizard.backup.?*) ;;
            *) echo "Error: mktemp returned an unsafe backup path" >&2; exit 1 ;;
        esac
        prior_moved=yes
        rename_exact "$install_target" "$backup_path/original"
    fi

    installed_moved=yes
    rename_exact "$stage_path" "$install_target"
    stage_path=
    verify_install_tree "$install_target" "$install_host"

    # Verification is the commit point. From here onward the new target must
    # survive interruption or best-effort cleanup failure.
    transaction_state=committed
    cleanup_backup=$backup_path
    installed_moved=no
    prior_moved=no
    backup_path=
    if [ -n "$cleanup_backup" ]; then
        if ! safe_remove "$cleanup_backup" "$install_root" backup; then
            echo "Warning: could not completely remove backup: $cleanup_backup" >&2
        fi
    fi
    trap - 0 1 2 15
    echo "Installed $install_label: $install_target"
)

if [ "$install_codex" = yes ]; then
    install_one codex "Codex skill" "$codex_root" "$codex_target" "$codex_replace"
fi
if [ "$install_claude" = yes ]; then
    install_one claude "Claude Code skill" "$claude_root" "$claude_target" "$claude_replace"
fi

echo "Open a new chat in the installed agent and say: Start Prompting Wizard."
