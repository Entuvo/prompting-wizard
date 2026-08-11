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
CORE_TOP_FILES = (
    "SKILL.md", "AGENTS.md", "assessment.md", "rubrics.md",
    "VERSION.md", "CHANGELOG.md",
)


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
    paths = [skill / name for name in CORE_TOP_FILES]
    paths.extend(skill / "days" / f"{day:02d}.md" for day in range(1, 31))
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
) -> tuple[Path, Path, Path]:
    skill = root / "prompting-wizard"
    if validate:
        validate_source(root)
    version = course_version(skill)

    claude_manifest_path = skill / ".claude-plugin/plugin.json"
    claude_manifest = json.loads(claude_manifest_path.read_text(encoding="utf-8"))
    openai_manifest_path = root / "packaging/openai-plugin.json"
    openai_manifest = json.loads(openai_manifest_path.read_text(encoding="utf-8"))
    for label, manifest in (
        ("Claude plugin", claude_manifest),
        ("OpenAI plugin", openai_manifest),
    ):
        if manifest.get("version") != version:
            raise ValueError(f"{label} version does not match VERSION.md")

    account_entries = relative_entries(skill, "prompting-wizard")
    account_zip = write_zip(
        dist / "prompting-wizard-claude-skill.zip",
        account_entries,
    )

    claude_entries = list(account_entries)
    claude_entries.append((
        "prompting-wizard/.claude-plugin/plugin.json",
        claude_manifest_path.read_bytes(),
    ))
    claude_zip = write_zip(
        dist / "prompting-wizard-claude-plugin.zip",
        claude_entries,
    )

    openai_entries = relative_entries(
        skill,
        "prompting-wizard/skills/prompting-wizard",
    )
    openai_entries.extend((
        (
            "prompting-wizard/.codex-plugin/plugin.json",
            openai_manifest_path.read_bytes(),
        ),
        ("prompting-wizard/LICENSE", (root / "LICENSE").read_bytes()),
    ))
    openai_zip = write_zip(
        dist / "prompting-wizard-openai-plugin.zip",
        openai_entries,
    )
    return account_zip, claude_zip, openai_zip


if __name__ == "__main__":
    for artifact in build_all():
        print(artifact.relative_to(ROOT))
