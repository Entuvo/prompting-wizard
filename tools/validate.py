#!/usr/bin/env python3
"""Structural check for the prompting-wizard skill directory.

Dev-time only. Lives outside the shipped skill and is never loaded by it.

Run:  python3 tools/validate.py             # checks what exists
      python3 tools/validate.py --complete  # also requires all 30 day files
Exit: 0 clean, 1 problems (listed on stderr).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "prompting-wizard"

TOP_FILES = ("SKILL.md", "AGENTS.md", "assessment.md", "rubrics.md")

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
ABS_PATH = re.compile(r"(?:/Users/|/home/|~/)")
ABS_PATH_ALLOWED = ("~/.codex/config.toml",)


def slugify(heading):
    return re.sub(r"[^a-z0-9]+", "-", heading.strip().lower()).strip("-")


def h2_slugs(text):
    return {slugify(h) for h in re.findall(r"^## (.+)$", text, re.M)}


def section(text, heading):
    """Body of one section, up to the next heading of the same or higher level."""
    level = len(heading) - len(heading.lstrip("#"))
    pattern = rf"^{re.escape(heading)}\s*$\n(.*?)(?=^#{{1,{level}}} |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    return match.group(1) if match else None


def check(require_all_days=False):
    if not SKILL.is_dir():
        return [f"skill directory not found: {SKILL}"]

    errors = []
    for name in TOP_FILES:
        if not (SKILL / name).is_file():
            errors.append(f"{name}: missing")

    rubrics_path = SKILL / "rubrics.md"
    rubric_slugs = h2_slugs(rubrics_path.read_text()) if rubrics_path.is_file() else set()
    for expected in LEVERS + TECHNIQUES:
        if expected not in rubric_slugs:
            errors.append(f"rubrics.md: no rubric for '{expected}'")

    for n in range(1, 31):
        day = SKILL / "days" / f"{n:02d}.md"
        label = f"days/{n:02d}.md"
        if not day.is_file():
            if require_all_days:
                errors.append(f"{label}: missing")
            continue

        text = day.read_text()
        for heading in DAY_SECTIONS:
            if section(text, heading) is None:
                errors.append(f"{label}: missing '{heading}'")

        concept = section(text, "## Concept")
        if concept is not None:
            words = len(concept.split())
            if words > CONCEPT_MAX_WORDS:
                errors.append(f"{label}: concept is {words} words (max {CONCEPT_MAX_WORDS})")

        exercise = section(text, "## Exercise") or ""
        for tier in TIERS:
            if tier not in exercise:
                errors.append(f"{label}: exercise missing '{tier}'")

        rubric = section(text, "## Rubric") or ""
        refs = re.findall(r"rubrics\.md#([a-z0-9-]+)", rubric)
        if not refs:
            errors.append(f"{label}: rubric section has no 'rubrics.md#slug' reference")
        for ref in refs:
            if ref not in rubric_slugs:
                errors.append(f"{label}: rubric '{ref}' not in rubrics.md")

    for path in sorted(SKILL.rglob("*.md")):
        for i, line in enumerate(path.read_text().splitlines(), 1):
            if ABS_PATH.search(line) and not any(a in line for a in ABS_PATH_ALLOWED):
                errors.append(f"{path.relative_to(SKILL)}:{i}: absolute path in shipped file")

    return errors


if __name__ == "__main__":
    problems = check(require_all_days="--complete" in sys.argv)
    for problem in problems:
        print(problem, file=sys.stderr)
    print(f"{len(problems)} problem(s)" if problems else "ok")
    sys.exit(1 if problems else 0)
