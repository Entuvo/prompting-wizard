#!/usr/bin/env python3
"""Structural check for the prompting-wizard skill directory.

Dev-time only. Lives outside the shipped skill and is never loaded by it.

Run:  python3 tools/validate.py             # checks what exists
      python3 tools/validate.py --complete  # also requires all 30 day files
Exit: 0 clean, 1 problems (listed on stderr).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "prompting-wizard"

TOP_FILES = ("SKILL.md", "AGENTS.md", "assessment.md", "rubrics.md",
             "VERSION.md", "CHANGELOG.md")

LEVERS = ("noun", "verb", "adjective", "adverb", "pronoun", "preposition",
          "conjunction", "determiner", "numeral", "interjection", "particle")

TECHNIQUES = ("role-framing", "few-shot-examples", "output-schemas",
              "task-decomposition", "reasoning-scaffolds", "negative-constraints",
              "context-ordering", "system-prompts", "agent-and-tool-prompting",
              "self-critique-loops", "writing-evals", "token-economy",
              "failure-diagnosis", "prompt-library", "capstone")

DAY_SECTIONS = ("## Concept", "## Before / After", "## Exercise", "## Rubric")
TIERS = ("### Novice", "### Working", "### Advanced")
CONCEPT_MAX_WORDS = 200
SKILL_DESCRIPTION_MAX = 200
ABS_PATH = re.compile(r"(?:/Users/|/home/|~/)")
ABS_PATH_ALLOWED = ("~/.codex/config.toml",)
SLOT_TOKEN = re.compile(r"\{\{[^{}\n]+\}\}")
TASK_SLOT_OPTIONAL_DAYS = (14, 27, 29, 30)
EXTRA_SLOT_DAYS = {28: {"{{DOC}}"}}
SEMANTIC_VERSION = re.compile(
    r"^version: (?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$",
    re.M,
)
RELEASE_NOTES_LINE = (
    "release-notes: https://github.com/Entuvo/prompting-wizard/"
    "blob/main/prompting-wizard/CHANGELOG.md"
)


def slugify(heading):
    r"""Anchor slug for a heading: 'Few-shot examples' -> 'few-shot-examples'.

    `[\W_]` means "not a letter or digit" in Unicode terms, so an accented
    letter is kept ('café' -> 'café') instead of being treated as a separator
    and dropped. ASCII headings slugify exactly as before; `_` stays a
    separator because `\W` alone would keep it.
    """
    return re.sub(r"[\W_]+", "-", heading.strip().lower()).strip("-")


# CommonMark allows up to three spaces of indentation before a fence, and a
# fence may sit inside a blockquote. The blockquote prefix is backreferenced so
# a quoted fence is closed only at the same quote depth, and `(?!(?P=char))`
# stops the opener backtracking to a shorter run -- without it a three-backtick
# line would close a five-backtick block.
QUOTE_PREFIX = r"(?:[ ]{0,3}>[ ]?)*"
FENCE = re.compile(
    rf"^(?P<quote>{QUOTE_PREFIX})[ ]{{0,3}}"
    rf"(?P<fence>(?P<char>[`~])(?P=char){{2,}})(?!(?P=char))[^\n]*\n"
    rf".*?"
    rf"^(?P=quote)[ ]{{0,3}}(?P=fence)(?P=char)*[ \t]*$",
    re.M | re.S,
)


def strip_fences(text):
    """Blank out fenced code blocks, preserving line count so line numbers hold."""
    return FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def h2_slugs(text):
    text = strip_fences(text)
    return {slugify(h) for h in re.findall(r"^## (.+)$", text, re.M)}


def section(text, heading):
    """Body of one section, up to the next heading of the same or higher level.

    The newline after the heading is optional, so a heading on the final line of
    a file saved without a trailing newline yields an empty body, not None.
    """
    text = strip_fences(text)
    level = len(heading) - len(heading.lstrip("#"))
    pattern = rf"^{re.escape(heading)}\s*$\n?(.*?)(?=^#{{1,{level}}} |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1) if match else None


def raw_section(text, heading):
    """Body of a section with fenced content intact and fenced headings ignored."""
    level = len(heading) - len(heading.lstrip("#"))
    raw_lines = text.split("\n")
    stripped_lines = strip_fences(text).split("\n")
    start = next(
        (index for index, line in enumerate(stripped_lines)
         if line.rstrip(" \t") == heading),
        None,
    )
    if start is None:
        return None
    boundary = re.compile(rf"^#{{1,{level}}} ")
    end = next(
        (index for index in range(start + 1, len(stripped_lines))
         if boundary.match(stripped_lines[index])),
        len(stripped_lines),
    )
    return "\n".join(raw_lines[start + 1:end])


def heading_occurrences(text, heading):
    """How many times `heading` appears on a line of its own, outside fences."""
    return len(re.findall(rf"^{re.escape(heading)}\s*$", strip_fences(text), re.M))


def read_text(path, errors, label):
    """Return the file's text, or None after recording why it could not be read."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{label}: unreadable ({type(exc).__name__})")
        return None


def read_manifest(path: Path, label: str, errors: list[str]) -> dict | None:
    """Load one JSON manifest, reporting read and parse failures as problems."""
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"{label}: unreadable ({type(exc).__name__})")
        return None
    except json.JSONDecodeError as exc:
        errors.append(
            f"{label}: malformed JSON (line {exc.lineno} column {exc.colno})"
        )
        return None

    if not isinstance(manifest, dict):
        errors.append(f"{label}: manifest must be a JSON object")
        return None
    return manifest


def check_skill_metadata(text: str, errors: list[str]) -> None:
    """Enforce metadata limits for the regular Claude.ai upload artifact."""
    frontmatter = re.match(r"\A---[ \t]*\n(.*?)^---[ \t]*$", text, re.M | re.S)
    if not frontmatter:
        return
    description = re.search(
        r"^description:[ \t]*(.*)$", frontmatter.group(1), re.M
    )
    if (
        description
        and len(description.group(1).strip()) > SKILL_DESCRIPTION_MAX
    ):
        errors.append(
            "SKILL.md: description exceeds Claude.ai 200-character maximum"
        )


CODEX_PLUGIN_TOP_FILES = (
    "SKILL.md",
    "AGENTS.md",
    "assessment.md",
    "rubrics.md",
    "VERSION.md",
    "CHANGELOG.md",
)


def _codex_plugin_source_path(entry: dict) -> str | None:
    """Return the relative plugin path from a Codex marketplace entry."""
    source = entry.get("source")
    if isinstance(source, str):
        return source
    if isinstance(source, dict):
        path = source.get("path")
        if isinstance(path, str):
            return path
    return None


def check_distribution_metadata(version: str, errors: list[str]) -> None:
    """Keep shipped plugin and marketplace metadata aligned with the course."""
    plugin = read_manifest(
        SKILL / ".claude-plugin" / "plugin.json",
        "prompting-wizard/.claude-plugin/plugin.json",
        errors,
    )
    marketplace = read_manifest(
        ROOT / ".claude-plugin" / "marketplace.json",
        ".claude-plugin/marketplace.json",
        errors,
    )
    openai_plugin = read_manifest(
        ROOT / "packaging" / "openai-plugin.json",
        "packaging/openai-plugin.json",
        errors,
    )
    codex_marketplace = read_manifest(
        ROOT / ".agents" / "plugins" / "marketplace.json",
        ".agents/plugins/marketplace.json",
        errors,
    )

    if plugin is not None and plugin.get("name") != "prompting-wizard":
        errors.append("Claude plugin: name must be prompting-wizard")
    if plugin is not None and plugin.get("version") != version:
        errors.append("Claude plugin: version does not match VERSION.md")
    if openai_plugin is not None and openai_plugin.get("version") != version:
        errors.append("OpenAI plugin: version does not match VERSION.md")

    if marketplace is not None:
        metadata = marketplace.get("metadata")
        if not isinstance(metadata, dict) or metadata.get("version") != version:
            errors.append(
                "Claude marketplace metadata: version does not match VERSION.md"
            )

    entries = marketplace.get("plugins", []) if marketplace else []
    has_canonical_entry = (
        isinstance(entries, list)
        and len(entries) == 1
        and isinstance(entries[0], dict)
        and entries[0].get("source") == "./prompting-wizard"
    )
    if not has_canonical_entry:
        errors.append("Claude marketplace: must point to ./prompting-wizard")
    elif entries[0].get("version") != version:
        errors.append("Claude marketplace: version does not match VERSION.md")

    codex_entries = (
        codex_marketplace.get("plugins", []) if codex_marketplace else []
    )
    codex_entry = (
        codex_entries[0]
        if isinstance(codex_entries, list)
        and len(codex_entries) == 1
        and isinstance(codex_entries[0], dict)
        else None
    )
    if (
        codex_entry is None
        or _codex_plugin_source_path(codex_entry) != "./plugins/prompting-wizard"
    ):
        errors.append(
            "Codex marketplace: must point to ./plugins/prompting-wizard"
        )
    elif codex_entry.get("version") != version:
        errors.append("Codex marketplace: version does not match VERSION.md")

    codex_plugin = ROOT / "plugins" / "prompting-wizard"
    if not (codex_plugin / ".codex-plugin" / "plugin.json").is_file():
        errors.append(
            "Codex plugin: missing plugins/prompting-wizard/.codex-plugin/plugin.json"
        )
    if not (codex_plugin / "skills" / "prompting-wizard" / "SKILL.md").is_file():
        errors.append(
            "Codex plugin: missing plugins/prompting-wizard/skills/prompting-wizard/SKILL.md"
        )


def _file_is_symlink(path: Path) -> bool:
    return path.is_symlink()


def check_codex_plugin_copies(errors: list[str]) -> None:
    """Codex omits escaping symlinks, so the plugin tree must be real copies."""
    plugin = ROOT / "plugins" / "prompting-wizard"
    skill_copy = plugin / "skills" / "prompting-wizard"
    if skill_copy.is_symlink():
        errors.append(
            "Codex plugin skills/prompting-wizard: must be a real directory, not a symlink"
        )
        return
    pairs = [
        (plugin / "LICENSE", ROOT / "LICENSE", "Codex plugin LICENSE"),
        (
            plugin / ".codex-plugin" / "plugin.json",
            ROOT / "packaging" / "openai-plugin.json",
            "Codex plugin manifest",
        ),
        (
            plugin / "assets" / "logo.png",
            ROOT / "assets" / "listing" / "logo.png",
            "Codex plugin logo",
        ),
    ]
    for name in CODEX_PLUGIN_TOP_FILES:
        pairs.append(
            (skill_copy / name, SKILL / name, f"Codex plugin {name}")
        )
    for copy, canonical, label in pairs:
        if _file_is_symlink(copy):
            errors.append(f"{label}: must be a real file, not a symlink")
            continue
        if not canonical.is_file():
            continue
        if not copy.is_file():
            errors.append(f"{label}: missing required copy")
            continue
        if copy.read_bytes() != canonical.read_bytes():
            errors.append(f"{label}: does not match canonical file")

    days_copy = skill_copy / "days"
    days_canonical = SKILL / "days"
    if days_copy.is_symlink():
        errors.append("Codex plugin days/: must be a real directory, not a symlink")
        return
    if not days_copy.is_dir() or not days_canonical.is_dir():
        return
    for day in range(1, 31):
        name = f"{day:02d}.md"
        copy = days_copy / name
        canonical = days_canonical / name
        if _file_is_symlink(copy):
            errors.append(f"Codex plugin days/{name}: must be a real file, not a symlink")
        elif not canonical.is_file():
            continue
        elif not copy.is_file():
            errors.append(f"Codex plugin days/{name}: missing required copy")
        elif copy.read_bytes() != canonical.read_bytes():
            errors.append(f"Codex plugin days/{name}: does not match canonical file")


def check_assessment_lever_order(text, errors):
    """Keep both assessment examples in the order used for state tie-breaking."""
    names = "|".join(map(re.escape, LEVERS))
    block = re.search(
        r"^## Levers\s*$\n(.*?)(?=^## Tasks\s*$)",
        text,
        re.M | re.S,
    )
    if block:
        order = tuple(re.findall(rf"\b({names}):\s*[1-5]\b", block.group(1)))
        if order != LEVERS:
            errors.append(
                "assessment.md: ## Levers example is not in canonical lever order"
            )
    else:
        errors.append("assessment.md: no ## Levers example found")

    baseline = re.search(r"^- Day 0 .*? — baseline (.+)$", text, re.M)
    if baseline:
        order = tuple(re.findall(rf"\b({names})\s+[1-5]\b", baseline.group(1)))
        if order != LEVERS:
            errors.append(
                "assessment.md: Day 0 baseline is not in canonical lever order"
            )
    else:
        errors.append("assessment.md: no Day 0 baseline example found")


def check_version_manifest(text, changelog_text, errors):
    """Keep update comparisons machine-readable and release notes reachable."""
    machine_text = strip_fences(text)
    version_lines = SEMANTIC_VERSION.findall(machine_text)
    if not version_lines:
        errors.append("VERSION.md: version must be semantic MAJOR.MINOR.PATCH")
    elif len(version_lines) != 1:
        errors.append("VERSION.md: expected exactly one semantic version line")

    release_notes_lines = re.findall(
        rf"^{re.escape(RELEASE_NOTES_LINE)}$", machine_text, re.M
    )
    if not release_notes_lines:
        errors.append("VERSION.md: missing canonical release-notes URL")
    elif len(release_notes_lines) != 1:
        errors.append(
            "VERSION.md: expected exactly one canonical release-notes URL"
        )

    if len(version_lines) == 1 and changelog_text is not None:
        version = version_lines[0].removeprefix("version: ")
        if not re.search(
            rf"^## {re.escape(version)}(?:\s|$)",
            strip_fences(changelog_text),
            re.M,
        ):
            errors.append(
                f"CHANGELOG.md: no release heading for version {version}"
            )

    return (
        version_lines[0].removeprefix("version: ")
        if len(version_lines) == 1
        else None
    )


def check_day(text, label, day_number, rubric_slugs, referenced_slugs, errors):
    """Record every structural problem in one day file."""
    stripped = strip_fences(text)
    section_positions = []
    for heading in DAY_SECTIONS:
        count = heading_occurrences(text, heading)
        if count == 0:
            errors.append(f"{label}: missing '{heading}'")
        elif count > 1:
            errors.append(f"{label}: duplicate '{heading}' ({count} occurrences)")
        else:
            match = re.search(rf"^{re.escape(heading)}\s*$", stripped, re.M)
            section_positions.append(match.start())

    if len(section_positions) == len(DAY_SECTIONS):
        if section_positions != sorted(section_positions):
            errors.append(f"{label}: day sections are out of order")

    concept = section(text, "## Concept")
    if concept is not None:
        words = len(concept.split())
        if words > CONCEPT_MAX_WORDS:
            errors.append(f"{label}: concept is {words} words (max {CONCEPT_MAX_WORDS})")

    exercise = raw_section(text, "## Exercise") or ""
    tier_positions = []
    for tier in TIERS:
        count = heading_occurrences(exercise, tier)
        if count == 0:
            errors.append(f"{label}: exercise missing '{tier}'")
        elif count > 1:
            errors.append(f"{label}: duplicate exercise tier '{tier}' ({count} occurrences)")
        else:
            match = re.search(rf"^{re.escape(tier)}\s*$", exercise, re.M)
            tier_positions.append(match.start())
            if not (raw_section(exercise, tier) or "").strip():
                errors.append(f"{label}: exercise tier '{tier}' is empty")

    if len(tier_positions) == len(TIERS):
        if tier_positions != sorted(tier_positions):
            errors.append(f"{label}: exercise tiers are out of order")

    rubric = section(text, "## Rubric") or ""
    refs = re.findall(r"rubrics\.md#([a-z0-9-]+)", rubric)
    if not refs:
        errors.append(f"{label}: rubric section has no 'rubrics.md#slug' reference")
    for ref in refs:
        if ref not in rubric_slugs:
            errors.append(f"{label}: rubric '{ref}' not in rubrics.md")
        else:
            referenced_slugs.add(ref)

    if day_number not in TASK_SLOT_OPTIONAL_DAYS and "{{TASK}}" not in text:
        errors.append(f"{label}: missing '{{{{TASK}}}}' domain slot")

    allowed_slots = {"{{TASK}}"} | EXTRA_SLOT_DAYS.get(day_number, set())
    for token in sorted(set(SLOT_TOKEN.findall(text)) - allowed_slots):
        errors.append(f"{label}: unsupported slot token '{token}'")


def check_absolute_paths(text, label, errors):
    """Record machine-specific paths, at most one per line.

    Deliberately reads raw text. Every other check strips fences first; this one
    does not, because a fenced install snippet is exactly where a home-directory
    path hides, and being inside a code block is not a reason to ship one.
    """
    for i, line in enumerate(text.splitlines(), 1):
        for match in ABS_PATH.finditer(line):
            tail = line[match.start():]
            if not any(tail.startswith(a) for a in ABS_PATH_ALLOWED):
                errors.append(f"{label}:{i}: absolute path in shipped file")
                break


def check(require_all_days=False):
    if not SKILL.is_dir():
        return [f"skill directory not found: {SKILL}"]

    errors = []
    cache = {}
    referenced_slugs = set()
    all_days_loaded = True

    def load(path, label):
        """Read each file at most once a run, so one bad file is one problem."""
        if path not in cache:
            cache[path] = read_text(path, errors, label)
        return cache[path]

    for name in TOP_FILES:
        if not (SKILL / name).is_file():
            errors.append(f"{name}: missing")

    skill_path = SKILL / "SKILL.md"
    text = load(skill_path, "SKILL.md") if skill_path.is_file() else None
    if text is not None:
        check_skill_metadata(text, errors)

    assessment_path = SKILL / "assessment.md"
    text = load(assessment_path, "assessment.md") if assessment_path.is_file() else None
    if text is not None:
        check_assessment_lever_order(text, errors)

    version_path = SKILL / "VERSION.md"
    text = load(version_path, "VERSION.md") if version_path.is_file() else None
    if text is not None:
        changelog_path = SKILL / "CHANGELOG.md"
        changelog_text = (
            load(changelog_path, "CHANGELOG.md")
            if changelog_path.is_file()
            else None
        )
        version = check_version_manifest(text, changelog_text, errors)
        if version is not None:
            check_distribution_metadata(version, errors)

    rubrics_path = SKILL / "rubrics.md"
    text = load(rubrics_path, "rubrics.md") if rubrics_path.is_file() else None
    rubric_slugs = h2_slugs(text) if text else set()
    for expected in LEVERS + TECHNIQUES:
        if expected not in rubric_slugs:
            errors.append(f"rubrics.md: no rubric for '{expected}'")

    for n in range(1, 31):
        day = SKILL / "days" / f"{n:02d}.md"
        label = f"days/{n:02d}.md"
        if not day.is_file():
            all_days_loaded = False
            if require_all_days:
                errors.append(f"{label}: missing")
            continue

        text = load(day, label)
        if text is not None:
            check_day(text, label, n, rubric_slugs, referenced_slugs, errors)
        else:
            all_days_loaded = False

    if require_all_days and all_days_loaded:
        for slug in LEVERS + TECHNIQUES:
            if slug not in referenced_slugs:
                errors.append(
                    f"rubrics.md: rubric '{slug}' is not referenced by any day"
                )
        check_codex_plugin_copies(errors)

    for path in sorted(SKILL.rglob("*.md")):
        label = str(path.relative_to(SKILL))
        text = load(path, label)
        if text is not None:
            check_absolute_paths(text, label, errors)

    return errors


if __name__ == "__main__":
    problems = check(require_all_days="--complete" in sys.argv)
    for problem in problems:
        print(problem, file=sys.stderr)
    print(f"{len(problems)} problem(s)" if problems else "ok")
    sys.exit(1 if problems else 0)
