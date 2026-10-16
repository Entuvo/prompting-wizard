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
AGENT_PLUGIN_KEYS = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license",
                     "keywords", "extensions"}  # agent-plugins.org 1.0.0: additionalProperties false
SHORT_DESCRIPTION_MAX = 30  # OpenAI submission listing metadata
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


def frontmatter_errors(text: str, label: str) -> list[str]:
    """Plain YAML scalars only: an unquoted value containing ': ' or starting with a YAML indicator breaks
    strict parsers (claude.ai, Codex), so require quotes in those cases."""
    block = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not block:
        return [f"{label}: missing YAML frontmatter"]
    errors = []
    for line in block.group(1).splitlines():
        key, sep, value = line.partition(": ")
        if not sep or not re.fullmatch(r"[a-z][a-z0-9-]*", key):
            errors.append(f"{label}: unparseable frontmatter line {line[:40]!r}")
            continue
        quoted = len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'"
        if not quoted and (": " in value or " #" in value or value[:1] in "&*!|>%@`[{,\"'"):
            errors.append(f"{label}: frontmatter value for {key} must be quoted")
    return errors


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
        text = data[f"skills/{skill}/SKILL.md"].decode("utf-8")
        check_skill_metadata(text, errors)
        errors += frontmatter_errors(text, f"skills/{skill}/SKILL.md")
    agent = json.loads(data["plugin.json"])
    extra = set(agent) - AGENT_PLUGIN_KEYS
    if extra:
        errors.append(f"plugin.json: fields not allowed by the Agent Plugins schema: {sorted(extra)}")
    interfaces = (agent.get("extensions", {}).get("com.openai", {}).get("interface", {}),
                  json.loads(data[".codex-plugin/plugin.json"]).get("interface", {}))
    for interface in interfaces:
        if len(interface.get("shortDescription", "")) > SHORT_DESCRIPTION_MAX:
            errors.append(f"OpenAI shortDescription exceeds {SHORT_DESCRIPTION_MAX} characters")
    if errors:
        raise ValueError("; ".join(errors))
    versions = {json.loads(data[m]).get("version") for m in MANIFESTS}
    names = {json.loads(data[m]).get("name") for m in MANIFESTS}
    if names != {PLUGIN_NAME} or len(versions) != 1:
        raise ValueError(f"Plugin manifests disagree: names {sorted(names)}, versions {sorted(map(str, versions))}")
    if _readme_words(data["README.md"].decode("utf-8")) < 40:
        raise ValueError("Plugin README must contain at least 40 words outside code blocks")
    return data


def _plugin_dir(root: Path) -> Path:
    """The plugin destination; refuse if it, or any directory between it and the repo root, is a symlink."""
    for i in range(1, len(PLUGIN_REL.parts) + 1):
        if (root / Path(*PLUGIN_REL.parts[:i])).is_symlink():
            raise ValueError(f"{Path(*PLUGIN_REL.parts[:i])} must not be a symlink")
    return root / PLUGIN_REL


def sync(root: Path = ROOT) -> Path:
    data = plugin_entries(root)
    plugin = _plugin_dir(root)
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
    try:
        plugin = _plugin_dir(root)
    except ValueError as exc:
        return [str(exc)]
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
