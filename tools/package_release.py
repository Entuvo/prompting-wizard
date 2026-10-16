#!/usr/bin/env python3
"""Build deterministic Prompting Wizard release archives."""
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "prompting-wizard"
DIST = ROOT / "dist"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
from course_files import COURSE_FILES
from build_native_guide import build as build_native_guide


def course_version(skill: Path) -> str:
    match = re.search(
        r"^version: (\d+\.\d+\.\d+)$",
        (skill / "VERSION.md").read_text(encoding="utf-8"),
        re.M,
    )
    if not match:
        raise ValueError("VERSION.md has no semantic version")
    return match.group(1)


def core_files(skill: Path) -> tuple[Path, ...]:
    paths = [skill / name for name in COURSE_FILES]
    for path in paths:
        parts=path.relative_to(skill).parts
        if any((skill / Path(*parts[:i])).is_symlink() for i in range(1,len(parts)+1)):
            raise ValueError('Course source contains a symlink')
    missing = [path.relative_to(skill).as_posix() for path in paths if not path.is_file()]
    if missing:
        raise ValueError(f"canonical skill is incomplete: {', '.join(missing)}")
    return tuple(paths)


def write_zip(path: Path, entries: list[tuple[str, bytes]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(entries):
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    return path


# The OpenAI directory build installs nothing from outside the package: no update check that fetches and
# replaces skill files, and no session-history readers that need extra packages. The repository marketplace
# and the Claude download keep both. Each change is exact text; drift raises instead of shipping silently.
OPENAI_OMIT = frozenset({"skills/prompting-wizard/scripts/history_hosts.py"})
OPENAI_UPDATES = """## Updates

Updates come only through the plugin manager of the app where this plugin is installed. Never fetch, download or replace skill files, and never check a remote location for a newer version.

If `course_version` is absent or differs from the installed `version` in this skill's `VERSION.md`, write the installed version; this is a state change, so apply step 6's durable write or stateless artifact-or-complete-fenced-file delivery rule. When the learner asks to check for or install an update, tell them to update Prompting Wizard through their app's plugin settings, then continue the lesson.

"""
OPENAI_EDITS = {
    "skills/prompting-wizard/SKILL.md": (
        ("Run the update check below before continuing when `current_day` is 30 or below, or whenever the learner "
         "explicitly asks to check or update.",
         "Apply `## Updates` below before continuing."),
        (re.compile(r"^## Update check\n.*?(?=^## )", re.M | re.S), OPENAI_UPDATES),
    ),
    "skills/prompting-wizard/references/history.md": (
        ("- Claude Code: needs `pip install claude-agent-sdk`.\n- Codex: needs `pip install openai-codex`.\n"
         "- A ChatGPT or Claude app data export (`--host chatgpt|claude --file EXPORT`): no SDK needed. "
         "The learner requests the export from the app's settings",
         "- A ChatGPT data export (`--host chatgpt --file EXPORT`). This build reviews exports only; local session "
         "history comes with the repository marketplace install. The learner requests the export from ChatGPT's settings"),
        ("Claude Code reviews only Claude exports (`--host claude`), and Codex reviews only ChatGPT exports "
         "(`--host chatgpt`).",
         "Codex reviews only ChatGPT exports (`--host chatgpt`)."),
        ("Otherwise run the scan with `--host` set to the current host's own provider (`claude` in Claude Code, "
         "`chatgpt` in Codex), never the other. The runtime enforces this too: under Codex it refuses Claude sources, "
         "and under Claude Code it refuses ChatGPT sources (detected from each host's session variables). If both "
         "hosts' variables are set, it refuses everything and asks the learner to run it directly in the right host.",
         "Otherwise run the scan with `--host chatgpt`, never `--host claude`. The runtime enforces this too: under "
         "Codex it refuses Claude sources."),
        (" Run the Python interpreter that has the host SDK installed.",
         " Run `python3`; the export reader needs only the standard library."),
        ("- that excluded coaching workspaces are skipped. Exports have no workspaces:",
         "- that exports have no workspaces:"),
        ("python3 scripts/history.py scan --root ROOT --host claude-code|codex [--days N] [--cap N]\n"
         "python3 scripts/history.py scan --root ROOT --host chatgpt|claude --file EXPORT",
         "python3 scripts/history.py scan --root ROOT --host chatgpt --file EXPORT"),
        ("report `error` (for a missing SDK, that's the install command) and stop.", "report `error` and stop."),
    ),
    "skills/prompting-wizard/references/commands.md": (
        ("Available in Claude Code and Codex only, and each reviews only its own provider's history "
         "(Claude Code: Claude; Codex: ChatGPT).",
         "In this build it runs in Codex on a ChatGPT export only; local session history comes with the repository "
         "marketplace install. In the ChatGPT app, the `learn` skill reviews an uploaded export instead."),
    ),
    "skills/learn/SKILL.md": (
        ("In Claude Code or Codex, the full course offers `pw history` with stored, local results.",
         "In Codex, the full course offers `pw history` on a ChatGPT export, with stored, local results."),
    ),
    "README.md": (
        ("To review your past work, use `pw history` in Claude Code or Codex, or upload your app's own data export "
         "in ChatGPT or Claude and ask the coach to review it.",
         "To review your past work, upload your app's own data export in ChatGPT or Claude and ask the coach to "
         "review it, or run `pw history` on a ChatGPT export in Codex. This directory build reviews exports only. "
         "The full local `pw history`, which also reads your past sessions, comes from the "
         "[repository marketplace install](https://github.com/Entuvo/prompting-wizard)."),
        ("| Past-work review | upload that app's own export | `pw history`, with stored results |",
         "| Past-work review | upload that app's own export | `pw history` on an export, with stored results |"),
    ),
}
OPENAI_FORBIDDEN = ("raw.githubusercontent", "pip install", "curl ", "git clone", "npx ", "Update check",
                    "--host claude-code", "--host codex")


def openai_entries(data: dict[str, bytes]) -> list[tuple[str, bytes]]:
    entries = []
    for name, content in data.items():
        if name in OPENAI_OMIT:
            continue
        for old, new in OPENAI_EDITS.get(name, ()):
            text = content.decode("utf-8")
            if isinstance(old, re.Pattern):
                text, count = old.subn(lambda _: new, text)
            else:
                count = text.count(old)
                text = text.replace(old, new)
            if count != 1:
                raise ValueError(f"{name}: expected one match for OpenAI edit, found {count}: {str(old)[:60]}")
            content = text.encode("utf-8")
        found = [s for s in OPENAI_FORBIDDEN if s.encode() in content]
        if found:
            raise ValueError(f"{name}: OpenAI build must not contain {', '.join(found)}")
        entries.append((name, content))
    return entries


def relative_entries(skill: Path, prefix: str) -> list[tuple[str, bytes]]:
    return [
        (f"{prefix}/{path.relative_to(skill).as_posix()}", path.read_bytes())
        for path in core_files(skill)
    ]


def validate_source(root: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(root / "tools/validate.py"), "--complete"],
        cwd=root,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"canonical skill validation failed: {detail}")


def build_all(
    root: Path = ROOT,
    dist: Path = DIST,
    *,
    validate: bool = True,
) -> tuple[Path, Path]:
    """Two downloads from the one plugin: Claude (app, Cowork, Claude Code) and OpenAI (ChatGPT, Codex).
    Both have the manifest and skills/ at the archive root. The manual-setup guide and empty card are
    written beside them."""
    from sync_codex_plugin import MANIFESTS, plugin_entries

    if validate:
        validate_source(root)
    version = course_version(root / "prompting-wizard")
    data = plugin_entries(root)
    for name in MANIFESTS:
        if json.loads(data[name]).get("version") != version:
            raise ValueError(f"{name} version does not match VERSION.md")
    for stale in ("prompting-wizard-claude-skill.zip", "prompting-wizard-claude-plugin.zip",
                  "prompting-wizard-openai-plugin.zip", "prompting-wizard-teacher-chatgpt.zip",
                  "prompting-wizard-teacher-claude.zip"):
        (dist / stale).unlink(missing_ok=True)
    build_native_guide(root, dist)
    claude_only, openai_only = {".claude-plugin/plugin.json"}, {"plugin.json", ".codex-plugin/plugin.json"}
    claude_zip = write_zip(dist / "prompting-wizard-claude.zip",
                           [(n, c) for n, c in data.items() if n not in openai_only])
    openai_zip = write_zip(dist / "prompting-wizard-openai.zip",
                           openai_entries({n: c for n, c in data.items() if n not in claude_only}))
    return claude_zip, openai_zip


if __name__ == "__main__":
    for artifact in build_all():
        print(artifact.relative_to(ROOT))
    for name in ("prompting-wizard-native-guide.md", "prompting-wizard-learning-card.md"):
        print((DIST / name).relative_to(ROOT))
