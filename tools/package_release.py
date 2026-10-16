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
                           [(n, c) for n, c in data.items() if n not in claude_only])
    return claude_zip, openai_zip


if __name__ == "__main__":
    for artifact in build_all():
        print(artifact.relative_to(ROOT))
    for name in ("prompting-wizard-native-guide.md", "prompting-wizard-learning-card.md"):
        print((DIST / name).relative_to(ROOT))
