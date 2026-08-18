#!/usr/bin/env python3
"""Unit tests for tools/validate.py, the structural validator for the skill.

Stdlib unittest only, to match the project's no-dependency constraint.

Run:  python3 tools/test_validate.py
      python3 -m unittest discover -s tools

Fixtures are built in a temp directory and `validate.SKILL` is repointed at
them for the duration of each test, so nothing here reads or mutates the real
`prompting-wizard/` content.

The eight gaps recorded in .superpowers/audit/validator-tests.md have been
closed (seven fixed, one confirmed intended); the tests that used to pin their
wrong behaviour now assert the corrected behaviour. See
.superpowers/audit/wave0-validator-fixes.md.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Importable whether run as a script, via discovery rooted at tools/, or from
# the repo root; validate.py is a plain module beside this file, not a package.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate  # noqa: E402


# --------------------------------------------------------------------------
# Fixture construction
# --------------------------------------------------------------------------

CLEAN_DAY = (
    ("## Concept", "A short concept, well under the word cap."),
    ("## Before / After", "**Before**\n\nvague {{TASK}} ask\n\n**After**\n\nprecise ask"),
    ("## Exercise", "### Novice\n\nn\n\n### Working\n\nw\n\n### Advanced\n\na"),
    ("## Rubric", "Score with rubrics.md#noun."),
)


def render_day(sections=CLEAN_DAY, title="# Day 01"):
    """Render an ordered (heading, body) sequence as a day file."""
    body = "\n\n".join(f"{heading}\n\n{text}" for heading, text in sections)
    return f"{title}\n\n{body}\n"


def without(sections, heading):
    """Copy of `sections` with one section dropped."""
    return tuple(pair for pair in sections if pair[0] != heading)


def replacing(sections, heading, text):
    """Copy of `sections` with one section's body replaced."""
    return tuple((h, text if h == heading else b) for h, b in sections)


def rubric_heading(slug):
    """A prose heading that slugifies back to `slug` (few-shot-examples -> Few shot examples)."""
    return slug.replace("-", " ").capitalize()


def render_rubrics(slugs=validate.LEVERS + validate.TECHNIQUES):
    entries = "\n".join(f"## {rubric_heading(s)}\n\nHow to score it.\n" for s in slugs)
    return f"# Rubrics\n\n{entries}"


def render_assessment(levers=validate.LEVERS, baseline_levers=None):
    """Minimal assessment carrying both canonical lever-order contracts."""
    baseline_levers = baseline_levers or levers
    lever_block = "    ".join(f"{slug}: 3" for slug in levers)
    baseline = ", ".join(f"{slug} 3" for slug in baseline_levers)
    return (
        "# Day 0 — Assessment\n\n"
        "```markdown\n"
        "## Levers\n"
        f"{lever_block}\n\n"
        "## Tasks\n- A task\n\n"
        "## Log\n"
        f"- Day 0 — assessment — level working, diagnosis 5/10 — baseline {baseline}\n"
        "```\n"
    )


def render_version(version="1.0.0", include_release_notes=True):
    """Minimal machine-readable update manifest shipped with the skill."""
    lines = ["# Prompting Wizard version", "", f"version: {version}"]
    if include_release_notes:
        lines.append(
            "release-notes: https://github.com/Entuvo/prompting-wizard/"
            "blob/main/prompting-wizard/CHANGELOG.md"
        )
    return "\n".join(lines) + "\n"


def render_changelog(version="1.0.0"):
    """Minimal release notes for the version declared by the manifest."""
    return f"# Prompting Wizard release notes\n\n## {version} — 2026-08-10\n"


def words(count, start=0):
    return " ".join(f"w{i}" for i in range(start, start + count))


def body_of(text, heading):
    """`validate.section`, asserted present, so callers get a `str` not `str | None`.

    Membership checks against `None` otherwise fail with a confusing container
    error, and static type checkers flag every such call site.
    """
    body = validate.section(text, heading)
    if body is None:
        raise AssertionError(f"fixture has no {heading!r} section")
    return body


def line_number_of(text, needle):
    """1-based line number of the first line containing `needle`."""
    for index, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return index
    raise AssertionError(f"fixture does not contain {needle!r}")


def write_codex_distribution(repo_root, version="1.0.0"):
    """Minimal Codex marketplace and plugin tree that check() accepts."""
    (repo_root / ".agents" / "plugins").mkdir(parents=True, exist_ok=True)
    plugin = repo_root / "plugins" / "prompting-wizard"
    skill = repo_root / "prompting-wizard"
    skill_copy = plugin / "skills" / "prompting-wizard"
    (plugin / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    skill_copy.mkdir(parents=True, exist_ok=True)
    (repo_root / ".agents" / "plugins" / "marketplace.json").write_text(
        json.dumps(
            {
                "name": "entuvo-prompting",
                "plugins": [
                    {
                        "name": "prompting-wizard",
                        "source": {
                            "source": "local",
                            "path": "./plugins/prompting-wizard",
                        },
                        "version": version,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    openai = repo_root / "packaging" / "openai-plugin.json"
    if openai.is_file():
        shutil.copy2(openai, plugin / ".codex-plugin" / "plugin.json")
    else:
        (plugin / ".codex-plugin" / "plugin.json").write_text(
            json.dumps({"name": "prompting-wizard", "version": version}),
            encoding="utf-8",
        )
    for name in (
        "SKILL.md",
        "AGENTS.md",
        "assessment.md",
        "rubrics.md",
        "VERSION.md",
        "CHANGELOG.md",
    ):
        source = skill / name
        if source.is_file():
            shutil.copy2(source, skill_copy / name)
    if (skill / "days").is_dir():
        shutil.copytree(skill / "days", skill_copy / "days", dirs_exist_ok=True)
    if (repo_root / "LICENSE").is_file():
        shutil.copy2(repo_root / "LICENSE", plugin / "LICENSE")


def build_clean_skill(root, days=(1,)):
    """Create the smallest skill tree that check() accepts."""
    (root / "days").mkdir(parents=True, exist_ok=True)
    (root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (root.parent / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (root.parent / "packaging").mkdir(parents=True, exist_ok=True)
    for name in validate.TOP_FILES:
        (root / name).write_text(f"# {name}\n\nplaceholder\n", encoding="utf-8")
    (root / "VERSION.md").write_text(render_version(), encoding="utf-8")
    (root / "CHANGELOG.md").write_text(render_changelog(), encoding="utf-8")
    (root / "assessment.md").write_text(render_assessment(), encoding="utf-8")
    (root / "rubrics.md").write_text(render_rubrics(), encoding="utf-8")
    (root / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "prompting-wizard", "version": "1.0.0"}),
        encoding="utf-8",
    )
    (root.parent / ".claude-plugin" / "marketplace.json").write_text(
        json.dumps(
            {
                "metadata": {"version": "1.0.0"},
                "plugins": [
                    {
                        "name": "prompting-wizard",
                        "source": "./prompting-wizard",
                        "version": "1.0.0",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (root.parent / "packaging" / "openai-plugin.json").write_text(
        json.dumps({"name": "prompting-wizard", "version": "1.0.0"}),
        encoding="utf-8",
    )
    write_codex_distribution(root.parent, version="1.0.0")
    for number in days:
        (root / "days" / f"{number:02d}.md").write_text(
            render_day(title=f"# Day {number:02d}"), encoding="utf-8")
    return root


class SkillFixture(unittest.TestCase):
    """Builds a clean throwaway skill tree and points validate.SKILL at it."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.skill = Path(tmp.name) / "prompting-wizard"

        self.addCleanup(setattr, validate, "SKILL", validate.SKILL)
        self.addCleanup(setattr, validate, "ROOT", validate.ROOT)
        validate.ROOT = self.skill.parent
        validate.SKILL = self.skill

        build_clean_skill(self.skill)

    def write(self, relative, text):
        path = self.skill / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def rebuild(self):
        """Discard the current fixture and start from a clean one (for subTest loops)."""
        self.setUp()

    def write_day(self, number, sections=CLEAN_DAY):
        return self.write(
            f"days/{number:02d}.md",
            render_day(sections, title=f"# Day {number:02d}"),
        )


# --------------------------------------------------------------------------
# Shipped contract
#
# Pinned as literals, not derived from the module, so that widening a rule
# (raising the word cap, dropping a lever) is a visible test change rather
# than a silent one.
# --------------------------------------------------------------------------

class ContractTests(unittest.TestCase):

    def test_required_top_level_files(self):
        self.assertEqual(validate.TOP_FILES,
                         ("SKILL.md", "AGENTS.md", "assessment.md", "rubrics.md",
                          "VERSION.md", "CHANGELOG.md"))

    def test_update_manifest_contract(self):
        self.assertEqual(
            validate.SEMANTIC_VERSION.pattern,
            r"^version: (?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)$",
        )
        self.assertEqual(
            validate.RELEASE_NOTES_LINE,
            "release-notes: https://github.com/Entuvo/prompting-wizard/"
            "blob/main/prompting-wizard/CHANGELOG.md",
        )

    def test_eleven_levers_are_required(self):
        self.assertEqual(
            validate.LEVERS,
            ("noun", "verb", "adjective", "adverb", "pronoun", "preposition",
             "conjunction", "determiner", "numeral", "interjection", "particle"),
        )

    def test_fifteen_techniques_are_required(self):
        self.assertEqual(
            validate.TECHNIQUES,
            ("role-framing", "few-shot-examples", "output-schemas",
             "task-decomposition", "reasoning-scaffolds", "negative-constraints",
             "context-ordering", "system-prompts", "agent-and-tool-prompting",
             "self-critique-loops", "writing-evals", "token-economy",
             "failure-diagnosis", "prompt-library", "capstone"),
        )

    def test_levers_and_techniques_cover_the_twenty_six_rubrics(self):
        self.assertEqual(len(set(validate.LEVERS + validate.TECHNIQUES)), 26)

    def test_required_day_sections(self):
        self.assertEqual(
            validate.DAY_SECTIONS,
            ("## Concept", "## Before / After", "## Exercise", "## Rubric"),
        )

    def test_required_exercise_tiers(self):
        self.assertEqual(validate.TIERS, ("### Novice", "### Working", "### Advanced"))

    def test_concept_word_cap_is_two_hundred(self):
        self.assertEqual(validate.CONCEPT_MAX_WORDS, 200)

    def test_codex_config_is_the_only_allowed_absolute_path(self):
        self.assertEqual(validate.ABS_PATH_ALLOWED, ("~/.codex/config.toml",))

    def test_task_slot_optional_days_are_pinned(self):
        self.assertEqual(validate.TASK_SLOT_OPTIONAL_DAYS, (14, 27, 29, 30))

    def test_day_28_doc_slot_exception_is_pinned(self):
        self.assertEqual(validate.EXTRA_SLOT_DAYS, {28: {"{{DOC}}"}})


class DistributionMetadataTests(unittest.TestCase):

    def test_claude_plugin_uses_canonical_root_skill(self):
        manifest = json.loads(
            (validate.SKILL / ".claude-plugin/plugin.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(manifest["name"], "prompting-wizard")
        self.assertNotIn("skills", manifest)

    def test_claude_marketplace_points_to_canonical_skill(self):
        marketplace = json.loads(
            (validate.ROOT / ".claude-plugin/marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        plugin = marketplace["plugins"][0]
        self.assertEqual(plugin["name"], "prompting-wizard")
        self.assertEqual(plugin["source"], "./prompting-wizard")

    def test_codex_marketplace_points_to_plugin_tree(self):
        marketplace = json.loads(
            (validate.ROOT / ".agents/plugins/marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        plugin = marketplace["plugins"][0]
        self.assertEqual(plugin["name"], "prompting-wizard")
        self.assertEqual(
            validate._codex_plugin_source_path(plugin),
            "./plugins/prompting-wizard",
        )
        skill = (
            validate.ROOT
            / "plugins/prompting-wizard/skills/prompting-wizard/SKILL.md"
        )
        self.assertTrue(skill.is_file())
        self.assertFalse(skill.is_symlink())
        self.assertEqual(
            skill.read_bytes(),
            (validate.SKILL / "SKILL.md").read_bytes(),
        )

    def test_distribution_versions_match_course_version(self):
        self.assertEqual(validate.check(), [])


class DistributionMetadataValidatorTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        skill = root / "prompting-wizard"
        (root / ".claude-plugin").mkdir()
        (root / "packaging").mkdir()
        (skill / ".claude-plugin").mkdir(parents=True)

        self.addCleanup(setattr, validate, "ROOT", validate.ROOT)
        self.addCleanup(setattr, validate, "SKILL", validate.SKILL)
        validate.ROOT = root
        validate.SKILL = skill

        self.plugin_path = skill / ".claude-plugin" / "plugin.json"
        self.marketplace_path = root / ".claude-plugin" / "marketplace.json"
        self.openai_plugin_path = root / "packaging" / "openai-plugin.json"
        self.plugin_path.write_text(
            json.dumps({"name": "prompting-wizard", "version": "1.0.0"}),
            encoding="utf-8",
        )
        self.marketplace_path.write_text(
            json.dumps(
                {
                    "metadata": {"version": "1.0.0"},
                    "plugins": [
                        {
                            "name": "prompting-wizard",
                            "source": "./prompting-wizard",
                            "version": "1.0.0",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        self.openai_plugin_path.write_text(
            json.dumps({"name": "prompting-wizard", "version": "1.0.0"}),
            encoding="utf-8",
        )
        (skill / "SKILL.md").write_text("# SKILL.md\n", encoding="utf-8")
        write_codex_distribution(root, version="1.0.0")
        self.codex_marketplace_path = (
            root / ".agents" / "plugins" / "marketplace.json"
        )

    def test_read_manifest_returns_json_object(self):
        errors = []

        manifest = validate.read_manifest(self.plugin_path, "plugin.json", errors)

        self.assertEqual(manifest["name"], "prompting-wizard")
        self.assertEqual(errors, [])

    def test_read_manifest_reports_malformed_json_without_raising(self):
        self.plugin_path.write_text("{", encoding="utf-8")
        errors = []

        manifest = validate.read_manifest(self.plugin_path, "plugin.json", errors)

        self.assertIsNone(manifest)
        self.assertEqual(len(errors), 1)
        self.assertTrue(errors[0].startswith("plugin.json: malformed JSON"))

    def test_read_manifest_reports_non_object_without_raising(self):
        self.plugin_path.write_text("[]", encoding="utf-8")
        errors = []

        manifest = validate.read_manifest(self.plugin_path, "plugin.json", errors)

        self.assertIsNone(manifest)
        self.assertEqual(errors, ["plugin.json: manifest must be a JSON object"])

    def test_valid_distribution_metadata_reports_no_errors(self):
        errors = []

        validate.check_distribution_metadata("1.0.0", errors)

        self.assertEqual(errors, [])

    def test_distribution_versions_must_match_course_version(self):
        errors = []

        validate.check_distribution_metadata("1.1.0", errors)

        self.assertIn(
            "Claude plugin: version does not match VERSION.md", errors
        )
        self.assertIn(
            "Claude marketplace: version does not match VERSION.md", errors
        )
        self.assertIn(
            "Codex marketplace: version does not match VERSION.md", errors
        )

    def test_marketplace_metadata_version_must_match_course_version(self):
        marketplace = json.loads(self.marketplace_path.read_text(encoding="utf-8"))
        marketplace["metadata"]["version"] = "9.9.9"
        self.marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")
        errors = []

        validate.check_distribution_metadata("1.0.0", errors)

        self.assertIn(
            "Claude marketplace metadata: version does not match VERSION.md",
            errors,
        )

    def test_openai_plugin_version_must_match_course_version(self):
        manifest = json.loads(
            self.openai_plugin_path.read_text(encoding="utf-8")
        )
        manifest["version"] = "9.9.9"
        self.openai_plugin_path.write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        errors = []

        validate.check_distribution_metadata("1.0.0", errors)

        self.assertIn(
            "OpenAI plugin: version does not match VERSION.md", errors
        )

    def test_codex_marketplace_version_must_match_course_version(self):
        marketplace = json.loads(
            self.codex_marketplace_path.read_text(encoding="utf-8")
        )
        marketplace["plugins"][0]["version"] = "9.9.9"
        self.codex_marketplace_path.write_text(
            json.dumps(marketplace), encoding="utf-8"
        )
        errors = []

        validate.check_distribution_metadata("1.0.0", errors)

        self.assertIn(
            "Codex marketplace: version does not match VERSION.md", errors
        )

    def test_codex_plugin_symlink_is_rejected(self):
        skill_copy = (
            validate.ROOT
            / "plugins/prompting-wizard/skills/prompting-wizard/SKILL.md"
        )
        skill_copy.unlink()
        skill_copy.symlink_to(validate.SKILL / "SKILL.md")
        errors = []

        validate.check_codex_plugin_copies(errors)

        self.assertIn(
            "Codex plugin SKILL.md: must be a real file, not a symlink", errors
        )

    def test_codex_plugin_copy_must_match_canonical(self):
        skill_copy = (
            validate.ROOT
            / "plugins/prompting-wizard/skills/prompting-wizard/SKILL.md"
        )
        skill_copy.write_text("stale copy\n", encoding="utf-8")
        errors = []

        validate.check_codex_plugin_copies(errors)

        self.assertIn("Codex plugin SKILL.md: does not match canonical file", errors)

    def test_codex_plugin_skill_root_symlink_is_rejected(self):
        skill_copy = (
            validate.ROOT / "plugins/prompting-wizard/skills/prompting-wizard"
        )
        shutil.rmtree(skill_copy)
        skill_copy.symlink_to(validate.SKILL)
        errors = []

        validate.check_codex_plugin_copies(errors)

        self.assertIn(
            "Codex plugin skills/prompting-wizard: must be a real directory, not a symlink",
            errors,
        )

    def test_codex_plugin_missing_copy_is_reported(self):
        (
            validate.ROOT
            / "plugins/prompting-wizard/skills/prompting-wizard/SKILL.md"
        ).unlink()
        errors = []

        validate.check_codex_plugin_copies(errors)

        self.assertIn("Codex plugin SKILL.md: missing required copy", errors)

    def test_empty_plugin_manifest_reports_missing_name_and_version(self):
        self.plugin_path.write_text("{}", encoding="utf-8")
        errors = []

        validate.check_distribution_metadata("1.0.0", errors)

        self.assertIn("Claude plugin: name must be prompting-wizard", errors)
        self.assertIn(
            "Claude plugin: version does not match VERSION.md", errors
        )

    def test_plugin_manifest_missing_version_is_rejected(self):
        self.plugin_path.write_text(
            json.dumps({"name": "prompting-wizard"}), encoding="utf-8"
        )
        errors = []

        validate.check_distribution_metadata("1.0.0", errors)

        self.assertIn(
            "Claude plugin: version does not match VERSION.md", errors
        )


# --------------------------------------------------------------------------
# slugify
# --------------------------------------------------------------------------

class SlugifyTests(unittest.TestCase):

    def test_lowercases_and_joins_words_with_hyphens(self):
        self.assertEqual(validate.slugify("Agent and tool prompting"),
                         "agent-and-tool-prompting")

    def test_existing_hyphens_survive_as_single_separators(self):
        self.assertEqual(validate.slugify("Few-shot examples"), "few-shot-examples")

    def test_run_of_separators_collapses_to_one_hyphen(self):
        self.assertEqual(validate.slugify("Before  /  After"), "before-after")

    def test_leading_and_trailing_punctuation_is_trimmed(self):
        self.assertEqual(validate.slugify("---Trim it!---"), "trim-it")

    def test_surrounding_whitespace_is_trimmed(self):
        self.assertEqual(validate.slugify("   Token economy   "), "token-economy")

    def test_digits_are_kept(self):
        self.assertEqual(validate.slugify("Day 30 Capstone"), "day-30-capstone")

    def test_empty_heading_slugifies_to_empty_string(self):
        self.assertEqual(validate.slugify(""), "")

    def test_punctuation_only_heading_slugifies_to_empty_string(self):
        self.assertEqual(validate.slugify("!!!"), "")

    def test_non_ascii_letters_are_kept_not_dropped(self):
        """`[\\W_]` is Unicode-aware, so an accent is a letter, not a separator."""
        self.assertEqual(validate.slugify("café"), "café")

    def test_non_ascii_letters_are_kept_mid_heading(self):
        self.assertEqual(validate.slugify("Café au lait"), "café-au-lait")

    def test_underscore_is_still_a_separator(self):
        self.assertEqual(validate.slugify("token_economy"), "token-economy")

    def test_em_dash_and_smart_quotes_are_separators(self):
        self.assertEqual(validate.slugify("Token — “economy”"),
                         "token-economy")

    def test_every_expected_rubric_slug_round_trips_from_a_prose_heading(self):
        for slug in validate.LEVERS + validate.TECHNIQUES:
            with self.subTest(slug=slug):
                self.assertEqual(validate.slugify(rubric_heading(slug)), slug)


# --------------------------------------------------------------------------
# strip_fences
# --------------------------------------------------------------------------

class StripFencesTests(unittest.TestCase):

    def assertLineCountPreserved(self, original, stripped):
        self.assertEqual(len(original.splitlines()), len(stripped.splitlines()))

    def test_backtick_fenced_block_is_blanked(self):
        text = "before\n```py\ncode()\n```\nafter\n"

        stripped = validate.strip_fences(text)

        self.assertEqual(stripped, "before\n\n\n\nafter\n")

    def test_tilde_fenced_block_is_blanked(self):
        text = "before\n~~~json\n{}\n~~~\nafter\n"

        stripped = validate.strip_fences(text)

        self.assertEqual(stripped, "before\n\n\n\nafter\n")

    def test_line_count_is_preserved_so_reported_line_numbers_stay_correct(self):
        text = "one\n```\ntwo\nthree\n```\nsix\n"

        stripped = validate.strip_fences(text)

        self.assertLineCountPreserved(text, stripped)
        self.assertEqual(stripped.splitlines()[5], "six")

    def test_two_blocks_are_stripped_separately_and_prose_between_them_survives(self):
        text = "```\nA\n```\nkeep me\n```\nB\n```\n"

        stripped = validate.strip_fences(text)

        self.assertEqual(stripped, "\n\n\nkeep me\n\n\n\n")

    def test_closing_fence_longer_than_the_opening_still_closes_the_block(self):
        text = "```\nA\n`````\n"

        self.assertEqual(validate.strip_fences(text), "\n\n\n")

    def test_longer_fence_wrapping_inner_fences_is_stripped_as_one_block(self):
        text = "````md\nintro\n```\ninner\n```\ntail\n````\nafter\n"

        stripped = validate.strip_fences(text)

        self.assertEqual(stripped, "\n" * 7 + "after\n")

    def test_shorter_closing_fence_does_not_close_a_longer_opening_fence(self):
        """CommonMark requires the closer to be at least as long as the opener.

        A 5-backtick block is not closed by a 3-backtick line, so the block is
        unterminated and the text is left alone.
        """
        text = "`````\nA\n```\nafter\n"

        self.assertEqual(validate.strip_fences(text), text)

    def test_equal_length_closing_fence_closes_a_longer_opening_fence(self):
        text = "`````\nA\n`````\nafter\n"

        self.assertEqual(validate.strip_fences(text), "\n\n\nafter\n")

    def test_tilde_line_inside_a_backtick_block_does_not_close_it(self):
        text = "```\n~~~\nstill code\n```\nafter\n"

        stripped = validate.strip_fences(text)

        self.assertEqual(stripped, "\n\n\n\nafter\n")

    def test_backtick_line_inside_a_tilde_block_does_not_close_it(self):
        text = "~~~\n```\nstill code\n~~~\nafter\n"

        stripped = validate.strip_fences(text)

        self.assertEqual(stripped, "\n\n\n\nafter\n")

    def test_unterminated_fence_leaves_the_text_untouched(self):
        text = "```\nA\nB\n"

        self.assertEqual(validate.strip_fences(text), text)

    def test_text_without_fences_is_returned_unchanged(self):
        text = "# Title\n\nJust prose.\n"

        self.assertEqual(validate.strip_fences(text), text)

    def test_blockquoted_fence_is_stripped(self):
        """A fence inside a blockquote, as in prompting-wizard/days/17.md:30-35."""
        text = "> ```\n> [{\"item\": \"one\"}]\n> ```\n"

        self.assertEqual(validate.strip_fences(text), "\n\n\n")

    def test_nested_blockquoted_fence_is_stripped(self):
        text = "before\n>> ```\n>> code()\n>> ```\nafter\n"

        self.assertEqual(validate.strip_fences(text), "before\n\n\n\nafter\n")

    def test_blockquoted_fence_is_not_closed_by_an_unquoted_fence(self):
        """The quote prefix is backreferenced, so quote depth must match."""
        text = "> ```\n> code()\n```\nafter\n"

        self.assertEqual(validate.strip_fences(text), text)

    def test_unquoted_fence_is_not_closed_by_a_blockquoted_fence(self):
        text = "```\ncode()\n> ```\nafter\n"

        self.assertEqual(validate.strip_fences(text), text)

    def test_indented_fence_is_stripped(self):
        """Up to three spaces of indentation, e.g. a fence under a list item."""
        text = "- item\n   ```\n   code()\n   ```\n"

        stripped = validate.strip_fences(text)

        self.assertEqual(stripped, "- item\n\n\n\n")
        self.assertLineCountPreserved(text, stripped)

    def test_opening_and_closing_fence_indentation_need_not_match(self):
        text = "  ```\ncode()\n ```\nafter\n"

        self.assertEqual(validate.strip_fences(text), "\n\n\nafter\n")

    def test_fence_indented_four_spaces_is_not_a_fence(self):
        """Four spaces is an indented code block in CommonMark, not a fence."""
        text = "- item\n    ```\n    code()\n    ```\n"

        self.assertEqual(validate.strip_fences(text), text)


# --------------------------------------------------------------------------
# section
# --------------------------------------------------------------------------

DOC = """# Day 01

## Concept

concept body

### Aside

aside body

## Exercise

### Novice

novice body

### Working

working body

# Appendix

appendix body
"""


class SectionTests(unittest.TestCase):

    def test_h2_section_includes_its_h3_subheadings(self):
        body = body_of(DOC, "## Concept")

        self.assertIn("concept body", body)
        self.assertIn("### Aside", body)
        self.assertIn("aside body", body)

    def test_h2_section_ends_at_the_next_h2(self):
        self.assertNotIn("novice body", body_of(DOC, "## Concept"))

    def test_h2_section_ends_at_a_following_h1(self):
        self.assertNotIn("appendix body", body_of(DOC, "## Exercise"))

    def test_h3_section_ends_at_the_next_h3(self):
        body = body_of(DOC, "### Novice")

        self.assertIn("novice body", body)
        self.assertNotIn("working body", body)

    def test_absent_heading_returns_none(self):
        self.assertIsNone(validate.section(DOC, "## Rubric"))

    def test_last_section_in_the_file_runs_to_end_of_file(self):
        self.assertEqual(validate.section(DOC, "# Appendix"), "appendix body\n")

    def test_hash_line_inside_a_fenced_block_does_not_truncate_the_section(self):
        text = ("## Concept\n\nbefore\n\n```\n# not a heading\n## also not\n```\n"
                "\nafter\n\n## Exercise\n\nx\n")

        body = body_of(text, "## Concept")

        self.assertIn("before", body)
        self.assertIn("after", body)
        self.assertNotIn("x", body)

    def test_only_the_first_of_two_identical_headings_is_returned(self):
        """`section` takes the first copy; `heading_occurrences` exposes the rest.

        `check` turns a count above one into an explicit problem, so the second
        copy is no longer silently ignored. See
        CheckDaySectionTests.test_duplicate_day_section_is_reported.
        """
        text = "## Concept\n\nfirst\n\n## Other\n\nz\n\n## Concept\n\nsecond\n"

        self.assertEqual(validate.section(text, "## Concept"), "first\n\n")
        self.assertEqual(validate.heading_occurrences(text, "## Concept"), 2)

    def test_empty_section_returns_empty_string_not_none(self):
        text = "## Concept\n\nx\n\n## Rubric\n"

        self.assertEqual(validate.section(text, "## Rubric"), "")

    def test_heading_on_the_final_line_without_a_trailing_newline_is_found(self):
        """A heading is present whether or not the editor saved a final newline."""
        text = "## Concept\n\nx\n\n## Rubric"

        self.assertEqual(validate.section(text, "## Rubric"), "")

    def test_final_heading_with_a_body_but_no_trailing_newline_is_found(self):
        text = "## Concept\n\nx\n\n## Rubric\n\nscore it"

        self.assertEqual(validate.section(text, "## Rubric"), "score it")


# --------------------------------------------------------------------------
# heading_occurrences
# --------------------------------------------------------------------------

class HeadingOccurrencesTests(unittest.TestCase):

    def test_absent_heading_counts_zero(self):
        self.assertEqual(validate.heading_occurrences(DOC, "## Rubric"), 0)

    def test_single_heading_counts_one(self):
        self.assertEqual(validate.heading_occurrences(DOC, "## Concept"), 1)

    def test_repeated_heading_counts_every_copy(self):
        text = "## A\n\n## A\n\n## A\n"

        self.assertEqual(validate.heading_occurrences(text, "## A"), 3)

    def test_heading_inside_a_fenced_block_is_not_counted(self):
        text = "## A\n\n```\n## A\n```\n"

        self.assertEqual(validate.heading_occurrences(text, "## A"), 1)

    def test_longer_heading_on_the_same_prefix_is_not_counted(self):
        text = "## Concept\n\n## Concept notes\n"

        self.assertEqual(validate.heading_occurrences(text, "## Concept"), 1)

    def test_heading_on_the_final_line_without_a_trailing_newline_is_counted(self):
        self.assertEqual(validate.heading_occurrences("x\n\n## Rubric", "## Rubric"), 1)


# --------------------------------------------------------------------------
# h2_slugs
# --------------------------------------------------------------------------

class H2SlugsTests(unittest.TestCase):

    def test_collects_slugs_for_every_h2(self):
        text = "# Title\n\n## Few-shot examples\n\nx\n\n## Token economy\n\ny\n"

        self.assertEqual(validate.h2_slugs(text), {"few-shot-examples", "token-economy"})

    def test_ignores_h1_and_h3_headings(self):
        text = "# One\n\n## Two\n\n### Three\n"

        self.assertEqual(validate.h2_slugs(text), {"two"})

    def test_ignores_h2_headings_inside_a_fenced_block(self):
        text = "## Real\n\n```\n## Fake\n```\n"

        self.assertEqual(validate.h2_slugs(text), {"real"})

    def test_returns_empty_set_for_text_without_headings(self):
        self.assertEqual(validate.h2_slugs("just prose\n"), set())


# --------------------------------------------------------------------------
# read_text
# --------------------------------------------------------------------------

class ReadTextTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)

    def test_returns_file_contents_and_records_no_problem(self):
        path = self.dir / "ok.md"
        path.write_text("hello\n", encoding="utf-8")
        errors = []

        text = validate.read_text(path, errors, "ok.md")

        self.assertEqual(text, "hello\n")
        self.assertEqual(errors, [])

    def test_missing_file_returns_none_and_records_a_problem(self):
        errors = []

        text = validate.read_text(self.dir / "gone.md", errors, "gone.md")

        self.assertIsNone(text)
        self.assertEqual(errors, ["gone.md: unreadable (FileNotFoundError)"])

    def test_undecodable_bytes_return_none_and_record_a_problem(self):
        path = self.dir / "bad.md"
        path.write_bytes(b"\xff\xfe not utf-8\n")
        errors = []

        text = validate.read_text(path, errors, "bad.md")

        self.assertIsNone(text)
        self.assertEqual(errors, ["bad.md: unreadable (UnicodeDecodeError)"])

    def test_appends_to_existing_problems_without_discarding_them(self):
        errors = ["earlier problem"]

        validate.read_text(self.dir / "gone.md", errors, "gone.md")

        self.assertEqual(errors[0], "earlier problem")
        self.assertEqual(len(errors), 2)


# --------------------------------------------------------------------------
# check: baseline and structural failures
# --------------------------------------------------------------------------

class CheckCleanFixtureTests(SkillFixture):

    def test_clean_fixture_reports_no_problems(self):
        self.assertEqual(validate.check(), [])

    def test_missing_skill_directory_is_the_only_reported_problem(self):
        missing = self.skill.parent / "absent"
        validate.SKILL = missing

        problems = validate.check()

        self.assertEqual(problems, [f"skill directory not found: {missing}"])


class CheckTopLevelFileTests(SkillFixture):

    def test_missing_top_level_file_is_reported_by_name(self):
        (self.skill / "AGENTS.md").unlink()

        self.assertEqual(validate.check(), ["AGENTS.md: missing"])

    def test_each_required_top_level_file_is_checked(self):
        for name in validate.TOP_FILES:
            with self.subTest(name=name):
                self.rebuild()
                (self.skill / name).unlink()

                self.assertIn(f"{name}: missing", validate.check())


class CheckSkillMetadataTests(SkillFixture):

    def test_description_over_claude_ai_limit_is_rejected(self):
        self.write(
            "SKILL.md",
            "---\n"
            "name: prompting-wizard\n"
            f"description: {'x' * 201}\n"
            "---\n\n"
            "# Prompting Wizard\n",
        )

        self.assertIn(
            "SKILL.md: description exceeds Claude.ai 200-character maximum",
            validate.check(),
        )


class CheckVersionManifestTests(SkillFixture):

    def test_missing_version_manifest_is_reported(self):
        (self.skill / "VERSION.md").unlink()

        self.assertIn("VERSION.md: missing", validate.check())

    def test_non_semantic_version_is_reported(self):
        self.write("VERSION.md", render_version("next"))

        self.assertIn(
            "VERSION.md: version must be semantic MAJOR.MINOR.PATCH",
            validate.check(),
        )

    def test_leading_zero_version_is_reported(self):
        self.write("VERSION.md", render_version("01.0.0"))

        self.assertIn(
            "VERSION.md: version must be semantic MAJOR.MINOR.PATCH",
            validate.check(),
        )

    def test_fenced_version_is_not_machine_readable(self):
        self.write(
            "VERSION.md",
            "# Prompting Wizard version\n\n```text\nversion: 1.0.0\n```\n"
            + validate.RELEASE_NOTES_LINE
            + "\n",
        )

        self.assertIn(
            "VERSION.md: version must be semantic MAJOR.MINOR.PATCH",
            validate.check(),
        )

    def test_missing_release_notes_url_is_reported(self):
        self.write("VERSION.md", render_version(include_release_notes=False))

        self.assertIn(
            "VERSION.md: missing canonical release-notes URL",
            validate.check(),
        )

    def test_near_miss_release_notes_url_is_reported(self):
        self.write(
            "VERSION.md",
            render_version().replace("https://", "http://"),
        )

        self.assertIn(
            "VERSION.md: missing canonical release-notes URL",
            validate.check(),
        )

    def test_duplicate_version_lines_are_reported(self):
        self.write("VERSION.md", render_version() + "version: 1.1.0\n")

        self.assertIn(
            "VERSION.md: expected exactly one semantic version line",
            validate.check(),
        )

    def test_duplicate_release_notes_lines_are_reported(self):
        self.write(
            "VERSION.md",
            render_version() + validate.RELEASE_NOTES_LINE + "\n",
        )

        self.assertIn(
            "VERSION.md: expected exactly one canonical release-notes URL",
            validate.check(),
        )

    def test_changelog_must_include_manifest_version(self):
        self.write("VERSION.md", render_version("1.1.0"))

        self.assertIn(
            "CHANGELOG.md: no release heading for version 1.1.0",
            validate.check(),
        )

    def test_fenced_changelog_heading_is_not_a_release_heading(self):
        self.write(
            "CHANGELOG.md",
            "# Prompting Wizard release notes\n\n"
            "```text\n## 1.0.0 — example only\n```\n",
        )

        self.assertIn(
            "CHANGELOG.md: no release heading for version 1.0.0",
            validate.check(),
        )


class CheckAssessmentLeverOrderTests(SkillFixture):

    def test_missing_levers_example_is_reported(self):
        assessment = render_assessment().replace("## Levers", "## Scores", 1)
        self.write("assessment.md", assessment)

        self.assertIn(
            "assessment.md: no ## Levers example found",
            validate.check(),
        )

    def test_missing_day_zero_baseline_is_reported(self):
        assessment = render_assessment().replace(" — baseline ", " — starting scores ")
        self.write("assessment.md", assessment)

        self.assertIn(
            "assessment.md: no Day 0 baseline example found",
            validate.check(),
        )

    def test_levers_example_out_of_canonical_order_is_reported(self):
        reordered = list(validate.LEVERS)
        reordered[4], reordered[5] = reordered[5], reordered[4]
        self.write("assessment.md", render_assessment(tuple(reordered)))

        self.assertIn(
            "assessment.md: ## Levers example is not in canonical lever order",
            validate.check(),
        )

    def test_day_zero_baseline_out_of_canonical_order_is_reported(self):
        reordered = list(validate.LEVERS)
        reordered[4], reordered[5] = reordered[5], reordered[4]
        self.write(
            "assessment.md",
            render_assessment(validate.LEVERS, tuple(reordered)),
        )

        self.assertIn(
            "assessment.md: Day 0 baseline is not in canonical lever order",
            validate.check(),
        )


class CheckRubricTests(SkillFixture):

    def test_rubric_slug_absent_from_rubrics_is_reported(self):
        remaining = tuple(s for s in validate.LEVERS + validate.TECHNIQUES
                          if s != "capstone")
        self.write("rubrics.md", render_rubrics(remaining))

        self.assertEqual(validate.check(), ["rubrics.md: no rubric for 'capstone'"])

    def test_every_expected_slug_is_required(self):
        self.write("rubrics.md", "# Rubrics\n\nnothing here\n")

        problems = validate.check()

        expected = {f"rubrics.md: no rubric for '{s}'"
                    for s in validate.LEVERS + validate.TECHNIQUES}
        self.assertTrue(expected.issubset(set(problems)))

    def test_day_rubric_reference_that_does_not_resolve_is_reported(self):
        self.write_day(1, replacing(CLEAN_DAY, "## Rubric", "See rubrics.md#no-such-slug."))

        self.assertEqual(validate.check(),
                         ["days/01.md: rubric 'no-such-slug' not in rubrics.md"])

    def test_day_rubric_section_without_any_reference_is_reported(self):
        self.write_day(1, replacing(CLEAN_DAY, "## Rubric", "Score it however you like."))

        self.assertEqual(
            validate.check(),
            ["days/01.md: rubric section has no 'rubrics.md#slug' reference"],
        )

    def test_complete_skill_reports_a_registry_rubric_no_day_references(self):
        slugs = validate.LEVERS + validate.TECHNIQUES
        for number in range(1, 31):
            slug = slugs[number - 1] if number <= len(slugs) else "capstone"
            sections = replacing(
                CLEAN_DAY,
                "## Rubric",
                f"Score with rubrics.md#{slug}.",
            )
            self.write_day(number, sections)

        orphan = "prompt-library"
        self.write_day(
            slugs.index(orphan) + 1,
            replacing(CLEAN_DAY, "## Rubric", "Score with rubrics.md#noun."),
        )

        self.assertIn(
            f"rubrics.md: rubric '{orphan}' is not referenced by any day",
            validate.check(require_all_days=True),
        )


class CheckDaySectionTests(SkillFixture):

    def test_missing_day_section_is_reported_by_heading(self):
        self.write_day(1, without(CLEAN_DAY, "## Before / After"))

        self.assertIn(
            "days/01.md: missing '## Before / After'",
            validate.check(),
        )

    def test_each_required_day_section_is_checked(self):
        for heading in validate.DAY_SECTIONS:
            with self.subTest(heading=heading):
                self.rebuild()
                self.write_day(1, without(CLEAN_DAY, heading))

                self.assertIn(f"days/01.md: missing '{heading}'", validate.check())

    def test_duplicate_day_section_is_reported(self):
        duplicated = CLEAN_DAY + (("## Concept", "a second copy nobody validates"),)
        self.write_day(1, duplicated)

        self.assertEqual(validate.check(),
                         ["days/01.md: duplicate '## Concept' (2 occurrences)"])

    def test_each_required_day_section_is_checked_for_duplication(self):
        for heading in validate.DAY_SECTIONS:
            with self.subTest(heading=heading):
                self.rebuild()
                body = dict(CLEAN_DAY)[heading]
                self.write_day(1, CLEAN_DAY + ((heading, body),))

                self.assertIn(f"days/01.md: duplicate '{heading}' (2 occurrences)",
                              validate.check())

    def test_required_day_sections_must_be_in_contract_order(self):
        reordered = (CLEAN_DAY[1], CLEAN_DAY[0], CLEAN_DAY[2], CLEAN_DAY[3])
        self.write_day(1, reordered)

        self.assertIn(
            "days/01.md: day sections are out of order",
            validate.check(),
        )

    def test_section_heading_mentioned_in_prose_does_not_affect_order(self):
        concept = "A short concept that refers ahead to ## Exercise in prose."
        self.write_day(1, replacing(CLEAN_DAY, "## Concept", concept))

        self.assertNotIn(
            "days/01.md: day sections are out of order",
            validate.check(),
        )

    def test_a_duplicate_heading_inside_a_fenced_block_is_not_counted(self):
        concept = "Short prose.\n\n```\n## Concept\n```"
        self.write_day(1, replacing(CLEAN_DAY, "## Concept", concept))

        self.assertEqual(validate.check(), [])

    def test_missing_exercise_tier_is_reported(self):
        exercise = "### Novice\n\nn\n\n### Advanced\n\na"
        self.write_day(1, replacing(CLEAN_DAY, "## Exercise", exercise))

        self.assertEqual(validate.check(), ["days/01.md: exercise missing '### Working'"])

    def test_each_tier_is_required(self):
        for tier in validate.TIERS:
            with self.subTest(tier=tier):
                self.rebuild()
                tiers = "\n\n".join(f"{t}\n\nbody" for t in validate.TIERS if t != tier)
                self.write_day(1, replacing(CLEAN_DAY, "## Exercise", tiers))

                self.assertIn(f"days/01.md: exercise missing '{tier}'", validate.check())

    def test_exercise_tiers_must_be_in_contract_order(self):
        exercise = "### Working\n\nw\n\n### Novice\n\nn\n\n### Advanced\n\na"
        self.write_day(1, replacing(CLEAN_DAY, "## Exercise", exercise))

        self.assertIn(
            "days/01.md: exercise tiers are out of order",
            validate.check(),
        )

    def test_tier_heading_mentioned_in_prose_does_not_affect_order(self):
        exercise = (
            "The ### Advanced tier comes later.\n\n"
            "### Novice\n\nn\n\n### Working\n\nw\n\n### Advanced\n\na"
        )
        self.write_day(1, replacing(CLEAN_DAY, "## Exercise", exercise))

        self.assertNotIn(
            "days/01.md: exercise tiers are out of order",
            validate.check(),
        )

    def test_empty_exercise_tier_is_reported(self):
        exercise = "### Novice\n\n### Working\n\nw\n\n### Advanced\n\na"
        self.write_day(1, replacing(CLEAN_DAY, "## Exercise", exercise))

        self.assertIn(
            "days/01.md: exercise tier '### Novice' is empty",
            validate.check(),
        )

    def test_each_duplicate_exercise_tier_is_reported(self):
        for tier in validate.TIERS:
            with self.subTest(tier=tier):
                self.rebuild()
                exercise = (
                    "### Novice\n\nn\n\n### Working\n\nw\n\n"
                    f"### Advanced\n\na\n\n{tier}\n\nsecond"
                )
                self.write_day(1, replacing(CLEAN_DAY, "## Exercise", exercise))

                self.assertIn(
                    f"days/01.md: duplicate exercise tier '{tier}' (2 occurrences)",
                    validate.check(),
                )

    def test_fenced_prompt_is_nonempty_exercise_tier(self):
        exercise = (
            "### Novice\n\n```text\nPrompt only.\n```\n\n"
            "### Working\n\nw\n\n### Advanced\n\na"
        )
        self.write_day(1, replacing(CLEAN_DAY, "## Exercise", exercise))

        self.assertNotIn(
            "days/01.md: exercise tier '### Novice' is empty",
            validate.check(),
        )


class CheckDomainSlotTests(SkillFixture):

    def test_domain_lesson_without_task_slot_is_reported(self):
        sections = replacing(
            CLEAN_DAY,
            "## Before / After",
            "**Before**\n\nvague ask\n\n**After**\n\nprecise ask",
        )
        self.write_day(1, sections)

        self.assertIn(
            "days/01.md: missing '{{TASK}}' domain slot",
            validate.check(),
        )

    def test_each_non_domain_day_may_omit_task_slot(self):
        sections = replacing(
            CLEAN_DAY,
            "## Before / After",
            "**Before**\n\nvague ask\n\n**After**\n\nprecise ask",
        )
        for day in validate.TASK_SLOT_OPTIONAL_DAYS:
            with self.subTest(day=day):
                self.rebuild()
                self.write_day(day, sections)

                self.assertNotIn(
                    f"days/{day:02d}.md: missing '{{{{TASK}}}}' domain slot",
                    validate.check(),
                )

    def test_unknown_slot_token_is_reported(self):
        self.write_day(
            1,
            replacing(CLEAN_DAY, "## Concept", "Use {{UNKNOWN}} here."),
        )

        self.assertIn(
            "days/01.md: unsupported slot token '{{UNKNOWN}}'",
            validate.check(),
        )

    def test_mixed_case_slot_typo_is_reported(self):
        self.write_day(
            1,
            replacing(CLEAN_DAY, "## Concept", "Use {{Task}} here."),
        )

        self.assertIn(
            "days/01.md: unsupported slot token '{{Task}}'",
            validate.check(),
        )

    def test_doc_slot_is_allowed_as_literal_lesson_content_on_day_28(self):
        self.write_day(
            28,
            replacing(CLEAN_DAY, "## Concept", "Save {{DOC}} as a named slot."),
        )

        self.assertNotIn(
            "days/28.md: unsupported slot token '{{DOC}}'",
            validate.check(),
        )

    def test_doc_slot_is_not_allowed_on_other_days(self):
        self.write_day(
            1,
            replacing(CLEAN_DAY, "## Concept", "Save {{DOC}} as a named slot."),
        )

        self.assertIn(
            "days/01.md: unsupported slot token '{{DOC}}'",
            validate.check(),
        )


class CheckConceptWordCapTests(SkillFixture):

    def test_concept_of_exactly_two_hundred_words_is_accepted(self):
        self.write_day(1, replacing(CLEAN_DAY, "## Concept", words(200)))

        self.assertEqual(validate.check(), [])

    def test_concept_of_two_hundred_and_one_words_is_reported_with_its_count(self):
        self.write_day(1, replacing(CLEAN_DAY, "## Concept", words(201)))

        self.assertEqual(validate.check(),
                         ["days/01.md: concept is 201 words (max 200)"])

    def test_words_inside_a_fenced_block_do_not_count_toward_the_cap(self):
        concept = f"Short prose.\n\n```\n{words(400)}\n```"
        self.write_day(1, replacing(CLEAN_DAY, "## Concept", concept))

        self.assertEqual(validate.check(), [])

    def test_blockquoted_fence_is_exempt_from_the_cap_like_a_plain_fence(self):
        """The same sample must cost the same whether or not it is quoted.

        A day written in the days/17.md house style is no longer charged for
        sample JSON it never should have been charged for.
        """
        sample = words(400)
        plain = f"Short prose.\n\n```\n{sample}\n```"
        quoted = f"Short prose.\n\n> ```\n> {sample}\n> ```"

        self.write_day(1, replacing(CLEAN_DAY, "## Concept", plain))
        plain_problems = validate.check()
        self.write_day(1, replacing(CLEAN_DAY, "## Concept", quoted))
        quoted_problems = validate.check()

        self.assertEqual(plain_problems, [])
        self.assertEqual(quoted_problems, [])

    def test_indented_fence_is_exempt_from_the_cap(self):
        sample = "\n".join(f"   {chunk}" for chunk in (words(200), words(200, 200)))
        concept = f"Short prose.\n\n- item\n   ```\n{sample}\n   ```"
        self.write_day(1, replacing(CLEAN_DAY, "## Concept", concept))

        self.assertEqual(validate.check(), [])


# --------------------------------------------------------------------------
# check: absolute path scan
# --------------------------------------------------------------------------

class CheckAbsolutePathTests(SkillFixture):

    def write_day_with_line(self, line):
        text = render_day() + f"\n{line}\n"
        self.write("days/01.md", text)
        return line_number_of(text, line)

    def test_home_directory_path_is_reported_with_its_line_number(self):
        number = self.write_day_with_line("Open /Users/dana/notes.md to start.")

        self.assertEqual(validate.check(),
                         [f"days/01.md:{number}: absolute path in shipped file"])

    def test_linux_home_path_is_reported(self):
        self.write_day_with_line("Open /home/dana/notes.md to start.")

        self.assertEqual(len(validate.check()), 1)

    def test_tilde_path_is_reported(self):
        self.write_day_with_line("Open ~/notes.md to start.")

        self.assertEqual(len(validate.check()), 1)

    def test_allowlisted_codex_config_path_is_permitted(self):
        self.write_day_with_line("Add the skill to ~/.codex/config.toml before day one.")

        self.assertEqual(validate.check(), [])

    def test_allowlisted_path_does_not_excuse_a_real_path_on_the_same_line(self):
        number = self.write_day_with_line(
            "Edit ~/.codex/config.toml and point it at /Users/dana/skills."
        )

        self.assertEqual(validate.check(),
                         [f"days/01.md:{number}: absolute path in shipped file"])

    def test_only_one_problem_is_reported_per_offending_line(self):
        self.write_day_with_line("Both /Users/dana/a and /home/dana/b are wrong.")

        self.assertEqual(len(validate.check()), 1)

    def test_every_markdown_file_under_the_skill_is_scanned(self):
        self.write("nested/notes.md", "See /Users/dana/x.\n")

        self.assertEqual(validate.check(),
                         ["nested/notes.md:1: absolute path in shipped file"])

    def test_absolute_path_inside_a_fenced_block_is_still_reported(self):
        """Intended, not a gap: this is the one check that reads raw text.

        A fenced install snippet is exactly where a machine-specific path hides,
        so a code block is not an excuse. Every other check strips fences first;
        see the docstring on validate.check_absolute_paths.
        """
        text = render_day() + "\n```\n/Users/dana/x\n```\n"
        self.write("days/01.md", text)

        self.assertEqual(
            validate.check(),
            [f"days/01.md:{line_number_of(text, '/Users/dana/x')}: "
             "absolute path in shipped file"],
        )


# --------------------------------------------------------------------------
# check: day coverage and unreadable files
# --------------------------------------------------------------------------

class CheckDayCoverageTests(SkillFixture):

    def test_missing_day_files_are_ignored_by_default(self):
        self.assertEqual(validate.check(require_all_days=False), [])

    def test_require_all_days_reports_every_absent_day(self):
        problems = validate.check(require_all_days=True)

        self.assertEqual(problems, [f"days/{n:02d}.md: missing" for n in range(2, 31)])

    def test_require_all_days_is_satisfied_when_every_day_exists(self):
        slugs = validate.LEVERS + validate.TECHNIQUES
        for n in range(2, 31):
            slug = slugs[n - 1] if n <= len(slugs) else "capstone"
            self.write_day(
                n,
                replacing(CLEAN_DAY, "## Rubric", f"Score with rubrics.md#{slug}."),
            )
        write_codex_distribution(validate.ROOT, version="1.0.0")

        self.assertEqual(validate.check(require_all_days=True), [])


class CheckUnreadableFileTests(SkillFixture):

    def test_unreadable_day_file_is_reported_once(self):
        """The day loop and the rglob scan share one read per file."""
        (self.skill / "days" / "01.md").write_bytes(b"\xff\xfe not utf-8\n")

        problems = validate.check()

        self.assertEqual(problems, ["days/01.md: unreadable (UnicodeDecodeError)"])

    def test_unreadable_rubrics_file_is_reported_once(self):
        (self.skill / "rubrics.md").write_bytes(b"\xff\xfe not utf-8\n")

        problems = validate.check()

        self.assertEqual(
            [p for p in problems if p.endswith("unreadable (UnicodeDecodeError)")],
            ["rubrics.md: unreadable (UnicodeDecodeError)"],
        )

    def test_unreadable_rubrics_file_does_not_stop_the_run(self):
        (self.skill / "rubrics.md").write_bytes(b"\xff\xfe not utf-8\n")

        problems = validate.check()

        self.assertIn("rubrics.md: unreadable (UnicodeDecodeError)", problems)
        self.assertIn("rubrics.md: no rubric for 'noun'", problems)


# --------------------------------------------------------------------------
# Command-line contract
#
# The ten build tasks gate on this script printing "ok" and exiting 0, so the
# entry point is exercised as a subprocess against a copy of validate.py that
# sits beside a fixture skill tree.
# --------------------------------------------------------------------------

class CommandLineTests(unittest.TestCase):

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "tools").mkdir()
        self.script = root / "tools" / "validate.py"
        shutil.copy(validate.__file__, self.script)
        self.skill = build_clean_skill(root / "prompting-wizard")

    def run_validator(self, *args):
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            capture_output=True, text=True, check=False,
        )

    def test_clean_skill_prints_ok_and_exits_zero(self):
        result = self.run_validator()

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "ok")
        self.assertEqual(result.stderr, "")

    def test_problems_are_counted_on_stdout_and_listed_on_stderr(self):
        (self.skill / "AGENTS.md").unlink()

        result = self.run_validator()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.strip(), "1 problem(s)")
        self.assertEqual(result.stderr.strip(), "AGENTS.md: missing")

    def test_complete_flag_requires_every_day_file(self):
        result = self.run_validator("--complete")

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.strip(), "29 problem(s)")
        self.assertIn("days/30.md: missing", result.stderr)

    def test_absent_days_are_tolerated_without_the_complete_flag(self):
        self.assertEqual(self.run_validator().returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
