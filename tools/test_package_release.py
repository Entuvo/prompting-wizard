#!/usr/bin/env python3
"""Tests for the one-plugin release: tree sync/check and the two deterministic downloads."""
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import package_release  # noqa: E402
import sync_codex_plugin  # noqa: E402

ROOT = package_release.ROOT
SOURCES = ("prompting-wizard", "pw", "learn", "packaging", "assets/listing", "tools")


class PackageReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for rel in SOURCES:
            shutil.copytree(ROOT / rel, self.root / rel, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(ROOT / "LICENSE", self.root / "LICENSE")
        self.dist = self.root / "dist"

    def build(self):
        return package_release.build_all(self.root, self.dist, validate=False)

    def names(self, path):
        with zipfile.ZipFile(path) as archive:
            return set(archive.namelist())

    def read(self, path, name):
        with zipfile.ZipFile(path) as archive:
            return archive.read(name)

    def test_exactly_two_plugin_downloads_plus_manual_setup_files(self):
        claude, openai = self.build()
        self.assertEqual((claude.name, openai.name), ("prompting-wizard-claude.zip", "prompting-wizard-openai.zip"))
        self.assertEqual(sorted(p.name for p in self.dist.iterdir()),
                         ["prompting-wizard-claude.zip", "prompting-wizard-learning-card.md",
                          "prompting-wizard-native-guide.md", "prompting-wizard-openai.zip"])

    def test_each_vendor_gets_its_manifests_at_the_archive_root(self):
        claude, openai = self.build()
        claude_names, openai_names = self.names(claude), self.names(openai)
        self.assertIn(".claude-plugin/plugin.json", claude_names)
        self.assertFalse({"plugin.json", ".codex-plugin/plugin.json"} & claude_names)
        self.assertTrue({"plugin.json", ".codex-plugin/plugin.json"} <= openai_names)
        self.assertNotIn(".claude-plugin/plugin.json", openai_names)
        self.assertFalse(any(n.startswith("prompting-wizard/") for n in claude_names | openai_names))

    def test_both_carry_all_three_skills_and_the_learn_references(self):
        for archive in self.build():
            names = self.names(archive)
            for required in ("skills/prompting-wizard/SKILL.md", "skills/prompting-wizard/scripts/history.py",
                             "skills/pw/SKILL.md", "skills/learn/SKILL.md", "skills/learn/references/guide.md",
                             "skills/learn/references/empty-card.md", "README.md", "LICENSE", "assets/logo.png"):
                self.assertIn(required, names, f"{archive.name}: {required}")
            self.assertIn(b"../prompting-wizard/references/commands.md", self.read(archive, "skills/pw/SKILL.md"))

    def test_manifests_share_name_and_version_md(self):
        claude, openai = self.build()
        version = package_release.course_version(self.root / "prompting-wizard")
        for archive, name in ((claude, ".claude-plugin/plugin.json"), (openai, "plugin.json"),
                              (openai, ".codex-plugin/plugin.json")):
            manifest = json.loads(self.read(archive, name))
            self.assertEqual((manifest["name"], manifest["version"]), ("prompting-wizard", version), name)

    def test_no_hooks_learner_state_or_caches_ship(self):
        (self.root / "prompting-wizard" / "PROGRESS.md").write_text("private")
        (self.root / "prompting-wizard" / "__pycache__").mkdir()
        for archive in self.build():
            names = self.names(archive)
            self.assertFalse([n for n in names if "PROGRESS" in n or "__pycache__" in n or n.endswith(".pyc")
                              or "hooks" in n.split("/") or n.endswith(("hooks.json", ".sqlite3"))], archive.name)

    def test_repeated_builds_are_byte_identical(self):
        first = [hashlib.sha256(p.read_bytes()).hexdigest() for p in self.build()]
        second = [hashlib.sha256(p.read_bytes()).hexdigest() for p in self.build()]
        self.assertEqual(first, second)

    def test_old_downloads_are_removed_from_dist(self):
        self.dist.mkdir()
        (self.dist / "prompting-wizard-teacher-claude.zip").write_bytes(b"old")
        self.build()
        self.assertFalse((self.dist / "prompting-wizard-teacher-claude.zip").exists())

    def test_manifest_version_mismatch_stops_the_build(self):
        manifest = self.root / "packaging" / "plugin.json"
        data = json.loads(manifest.read_text())
        data["version"] = "0.0.1"
        manifest.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            self.build()
        self.assertFalse(self.dist.exists() and any(self.dist.glob("*.zip")))

    def test_source_symlink_cannot_package_external_content(self):
        outside = Path(self.tmp.name) / "outside.md"
        outside.write_text("secret")
        (self.root / "learn" / "SKILL.md").unlink()
        (self.root / "learn" / "SKILL.md").symlink_to(outside)
        with self.assertRaises(ValueError):
            self.build()

    def test_sync_writes_the_tree_and_check_finds_drift(self):
        sync_codex_plugin.sync(self.root)
        self.assertEqual(sync_codex_plugin.check(self.root), [])
        plugin = self.root / "plugins" / "prompting-wizard"
        (plugin / "skills" / "learn" / "SKILL.md").write_text("edited")
        (plugin / "stray.txt").write_text("x")
        problems = " ".join(sync_codex_plugin.check(self.root))
        self.assertIn("skills/learn/SKILL.md: missing or stale", problems)
        self.assertIn("stray.txt: unexpected plugin entry", problems)
        sync_codex_plugin.sync(self.root)
        self.assertEqual(sync_codex_plugin.check(self.root), [])
        self.assertFalse((plugin / "stray.txt").exists())

    def test_unquoted_colon_in_frontmatter_is_rejected(self):
        skill = self.root / "pw" / "SKILL.md"
        skill.write_text(skill.read_text().replace('description: "', 'description: ', 1).replace('model guidance."', 'model guidance.', 1))
        with self.assertRaisesRegex(ValueError, "must be quoted"):
            self.build()

    def test_portable_manifest_rejects_fields_outside_the_schema(self):
        manifest = self.root / "packaging" / "plugin.json"
        data = json.loads(manifest.read_text())
        data["skills"] = "./skills/"
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Agent Plugins schema"):
            self.build()

    def test_openai_subtitle_fits_the_listing_limit(self):
        manifest = self.root / "packaging" / "openai-plugin.json"
        data = json.loads(manifest.read_text())
        data["interface"]["shortDescription"] = "x" * 31
        manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "shortDescription"):
            self.build()

    def test_symlinked_destination_is_refused(self):
        outside = Path(self.tmp.name).parent / (Path(self.tmp.name).name + "-outside")
        (outside / "prompting-wizard").mkdir(parents=True)
        (outside / "prompting-wizard" / "keep.txt").write_text("not ours")
        self.addCleanup(shutil.rmtree, outside, True)
        (self.root / "plugins").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "must not be a symlink"):
            sync_codex_plugin.sync(self.root)
        self.assertTrue((outside / "prompting-wizard" / "keep.txt").exists())
        self.assertIn("must not be a symlink", " ".join(sync_codex_plugin.check(self.root)))

    def test_openai_build_installs_nothing_from_outside_the_package(self):
        claude, openai = self.build()
        hosts = "skills/prompting-wizard/scripts/history_hosts.py"
        self.assertNotIn(hosts, self.names(openai))
        self.assertIn("skills/prompting-wizard/scripts/history_exports.py", self.names(openai))
        with zipfile.ZipFile(openai) as archive:
            for name in archive.namelist():
                content = archive.read(name)
                for forbidden in (b"raw.githubusercontent", b"pip install", b"curl ", b"git clone", b"npx "):
                    self.assertNotIn(forbidden, content, f"{name}: {forbidden!r}")
        skill = self.read(openai, "skills/prompting-wizard/SKILL.md").decode()
        self.assertNotIn("## Update check", skill)
        self.assertIn("Never fetch, download or replace skill files", skill)
        self.assertIn(hosts, self.names(claude))
        self.assertIn(b"## Update check", self.read(claude, "skills/prompting-wizard/SKILL.md"))
        self.assertIn(b"raw.githubusercontent.com", self.read(claude, "skills/prompting-wizard/SKILL.md"))

    def test_openai_edit_that_no_longer_matches_stops_the_build(self):
        history = self.root / "prompting-wizard" / "references" / "history.md"
        history.write_text(history.read_text().replace("needs `pip install openai-codex`", "needs the Codex SDK"))
        with self.assertRaisesRegex(ValueError, "expected one match for OpenAI edit"):
            self.build()

    def test_skill_descriptions_fit_claude_ai_uploads(self):
        (self.root / "pw" / "SKILL.md").write_text(
            (self.root / "pw" / "SKILL.md").read_text().replace("description: ", "description: " + "x" * 200, 1))
        with self.assertRaisesRegex(ValueError, "200-character"):
            self.build()


if __name__ == "__main__":
    unittest.main()
