#!/usr/bin/env python3
"""Assemble the one Prompting Wizard plugin (plugins/prompting-wizard) from canonical sources.

The plugin carries three skills (the course, the pw shortcut and everyday learning) and three manifests:
`.claude-plugin/plugin.json` (Claude app, Cowork, Claude Code), root `plugin.json` (OpenAI Agent Plugins:
ChatGPT and Codex) and the legacy `.codex-plugin/plugin.json` (Codex CLI). Files are real copies, not
symlinks: Codex omits plugin-cache entries whose symlink targets escape the plugin directory.

  python3 tools/sync_codex_plugin.py           # write the tree
  python3 tools/sync_codex_plugin.py --check   # report missing, stale or unexpected files
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_REL = Path("plugins") / "prompting-wizard"
from course_files import COURSE_FILES

PLUGIN_NAME = "prompting-wizard"
MANIFESTS = {  # plugin path -> canonical source
    ".claude-plugin/plugin.json": "prompting-wizard/.claude-plugin/plugin.json",
    ".codex-plugin/plugin.json": "packaging/openai-plugin.json",
    "plugin.json": "packaging/plugin.json",
}


def _read(root: Path, rel: str | Path) -> bytes:
    parts = Path(rel).parts
    if any((root / Path(*parts[:i])).is_symlink() for i in range(1, len(parts) + 1)):
        raise ValueError(f"Plugin source contains a symlink: {rel}")
    return (root / rel).read_bytes()


def _readme_words(text: str) -> int:
    text = re.sub(r"(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[ \t]*$", "", text)
    return len(re.sub(r"(?m)^(?: {4}|\t).*$", "", text).split())


def plugin_entries(root: Path = ROOT) -> dict[str, bytes]:
    """Every file in the plugin, keyed by its path inside the plugin. The single source of truth for
    syncing the tree, checking it, and building release archives."""
    from build_native_guide import build as build_guide
    from validate import check_skill_metadata

    data: dict[str, bytes] = {}
    for name in COURSE_FILES:
        data[f"skills/prompting-wizard/{name}"] = _read(root, Path("prompting-wizard") / name)
    data["skills/pw/SKILL.md"] = _read(root, "pw/SKILL.md")
    data["skills/learn/SKILL.md"] = _read(root, "learn/SKILL.md")
    with tempfile.TemporaryDirectory() as tmp:
        guide = build_guide(root, Path(tmp))
        data["skills/learn/references/guide.md"] = guide.read_bytes()
        data["skills/learn/references/empty-card.md"] = (Path(tmp) / "prompting-wizard-learning-card.md").read_bytes()
    for dest, source in MANIFESTS.items():
        data[dest] = _read(root, source)
    data["README.md"] = _read(root, "packaging/README.md")
    data["LICENSE"] = _read(root, "LICENSE")
    data["assets/logo.png"] = _read(root, "assets/listing/logo.png")

    errors: list[str] = []
    for skill in ("prompting-wizard", "pw", "learn"):
        check_skill_metadata(data[f"skills/{skill}/SKILL.md"].decode("utf-8"), errors)
    if errors:
        raise ValueError("; ".join(errors))
    versions = {json.loads(data[m]).get("version") for m in MANIFESTS}
    names = {json.loads(data[m]).get("name") for m in MANIFESTS}
    if names != {PLUGIN_NAME} or len(versions) != 1:
        raise ValueError(f"Plugin manifests disagree: names {sorted(names)}, versions {sorted(map(str, versions))}")
    if _readme_words(data["README.md"].decode("utf-8")) < 40:
        raise ValueError("Plugin README must contain at least 40 words outside code blocks")
    return data


def sync(root: Path = ROOT) -> Path:
    data = plugin_entries(root)
    plugin = root / PLUGIN_REL
    if plugin.is_symlink():
        raise ValueError("Plugin directory must not be a symlink")
    for path in sorted(plugin.rglob("*"), reverse=True) if plugin.exists() else []:
        rel = path.relative_to(plugin).as_posix()
        if path.is_symlink() or (path.is_file() and rel not in data):
            path.unlink()
        elif path.is_dir() and not any(path.iterdir()):
            path.rmdir()
    for rel, content in data.items():
        dest = plugin / rel
        if dest.is_symlink():
            dest.unlink()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(content)
    return plugin


def check(root: Path = ROOT) -> list[str]:
    data = plugin_entries(root)
    plugin = root / PLUGIN_REL
    problems = []
    for rel, content in data.items():
        path = plugin / rel
        if path.is_symlink() or not path.is_file() or path.read_bytes() != content:
            problems.append(f"{PLUGIN_REL / rel}: missing or stale; run tools/sync_codex_plugin.py")
    for path in plugin.rglob("*"):
        rel = path.relative_to(plugin).as_posix()
        if path.is_symlink() or (path.is_file() and rel not in data):
            problems.append(f"{PLUGIN_REL / rel}: unexpected plugin entry")
    return problems


if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        found = check()
        for problem in found:
            print(problem)
        sys.exit(1 if found else 0)
    print(sync().relative_to(ROOT))
