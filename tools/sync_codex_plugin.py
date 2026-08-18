#!/usr/bin/env python3
"""Copy the canonical skill into the Codex plugin tree as real files.

Codex 0.147 omits plugin-cache entries whose symlink targets escape the
plugin directory. The git marketplace therefore has to ship ordinary files.
This script is the only writer of that tree; the validator checks the copies
still match the canonical skill.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "prompting-wizard"
PLUGIN = ROOT / "plugins" / "prompting-wizard"
SKILL_COPY = PLUGIN / "skills" / "prompting-wizard"
CORE_TOP_FILES = (
    "SKILL.md",
    "AGENTS.md",
    "assessment.md",
    "rubrics.md",
    "VERSION.md",
    "CHANGELOG.md",
)


def _replace_file(source: Path, destination: Path) -> None:
    if destination.is_symlink() or destination.is_file():
        destination.unlink()
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination, follow_symlinks=True)


def sync(root: Path = ROOT) -> Path:
    skill = root / "prompting-wizard"
    plugin = root / "plugins" / "prompting-wizard"
    skill_copy = plugin / "skills" / "prompting-wizard"
    if skill_copy.is_symlink() or skill_copy.is_file():
        skill_copy.unlink()
    elif skill_copy.is_dir():
        shutil.rmtree(skill_copy)
    skill_copy.mkdir(parents=True)
    for name in CORE_TOP_FILES:
        _replace_file(skill / name, skill_copy / name)
    shutil.copytree(skill / "days", skill_copy / "days", dirs_exist_ok=True)
    _replace_file(root / "LICENSE", plugin / "LICENSE")
    _replace_file(
        root / "packaging" / "openai-plugin.json",
        plugin / ".codex-plugin" / "plugin.json",
    )
    _replace_file(
        root / "assets" / "listing" / "logo.png",
        plugin / "assets" / "logo.png",
    )
    return plugin


if __name__ == "__main__":
    path = sync()
    print(path.relative_to(ROOT))
    sys.exit(0)
