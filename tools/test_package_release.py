#!/usr/bin/env python3
"""Tests for deterministic Prompting Wizard release packaging."""
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


class PackageReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.skill = self.root / "prompting-wizard"
        shutil.copytree(package_release.SKILL, self.skill)
        shutil.copy2(package_release.ROOT / "LICENSE", self.root / "LICENSE")
        (self.root / "packaging").mkdir()
        shutil.copy2(
            package_release.ROOT / "packaging/openai-plugin.json",
            self.root / "packaging/openai-plugin.json",
        )
        listing = self.root / "assets" / "listing"
        listing.mkdir(parents=True)
        shutil.copy2(
            package_release.ROOT / "assets/listing/logo.png",
            listing / "logo.png",
        )
        self.dist = self.root / "dist"

    def archive_names(self, path):
        with zipfile.ZipFile(path) as archive:
            return archive.namelist()

    def test_every_distribution_manifest_matches_version_md(self):
        expected = package_release.course_version(package_release.SKILL)
        manifests = (
            package_release.SKILL / ".claude-plugin/plugin.json",
            package_release.ROOT / ".claude-plugin/marketplace.json",
            package_release.ROOT / "packaging/openai-plugin.json",
            package_release.ROOT / ".agents/plugins/marketplace.json",
        )
        versions = []
        for path in manifests:
            data = json.loads(path.read_text(encoding="utf-8"))
            if path == package_release.ROOT / ".claude-plugin/marketplace.json":
                versions.extend(
                    (data["metadata"]["version"], data["plugins"][0]["version"])
                )
            elif path.name == "marketplace.json":
                versions.append(data["plugins"][0]["version"])
            else:
                versions.append(data["version"])
        self.assertEqual(expected, "1.1.0")
        self.assertEqual(versions, [expected, expected, expected, expected, expected])

    def test_account_zip_contains_only_canonical_course_files(self):
        account, _, _ = package_release.build_all(
            self.root, self.dist, validate=False
        )
        names = self.archive_names(account)
        self.assertIn("prompting-wizard/SKILL.md", names)
        self.assertIn("prompting-wizard/days/30.md", names)
        self.assertNotIn("prompting-wizard/.claude-plugin/plugin.json", names)

    def test_openai_plugin_has_standard_skill_layout(self):
        _, _, openai = package_release.build_all(
            self.root, self.dist, validate=False
        )
        names = self.archive_names(openai)
        self.assertIn("prompting-wizard/.codex-plugin/plugin.json", names)
        self.assertIn("prompting-wizard/skills/prompting-wizard/SKILL.md", names)
        self.assertIn("prompting-wizard/LICENSE", names)
        self.assertIn("prompting-wizard/assets/logo.png", names)

    def test_openai_manifest_includes_validator_required_capabilities_array(self):
        _, _, openai = package_release.build_all(
            self.root, self.dist, validate=False
        )
        with zipfile.ZipFile(openai) as archive:
            manifest = json.loads(
                archive.read("prompting-wizard/.codex-plugin/plugin.json")
            )
        interface = manifest["interface"]
        self.assertEqual(interface.get("capabilities"), [])
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        self.assertEqual(interface["logo"], "./assets/logo.png")
        self.assertEqual(interface["composerIcon"], "./assets/logo.png")
        self.assertEqual(
            interface["supportURL"],
            "https://github.com/Entuvo/prompting-wizard/blob/main/SUPPORT.md",
        )
        self.assertEqual(
            interface["privacyPolicyURL"],
            "https://github.com/Entuvo/prompting-wizard/blob/main/PRIVACY.md",
        )
        self.assertEqual(
            interface["termsOfServiceURL"],
            "https://github.com/Entuvo/prompting-wizard/blob/main/TERMS.md",
        )

    def test_packages_exclude_state_and_repository_artifacts(self):
        (self.skill / "PROGRESS.md").write_text("private", encoding="utf-8")
        (self.skill / "__pycache__").mkdir()
        (self.skill / "__pycache__/x.pyc").write_bytes(b"cache")
        (self.skill / "review-report.md").write_text("internal", encoding="utf-8")
        for archive in package_release.build_all(
            self.root, self.dist, validate=False
        ):
            names = self.archive_names(archive)
            self.assertFalse(any("PROGRESS.md" in name for name in names))
            self.assertFalse(any("__pycache__" in name for name in names))
            self.assertFalse(any(name.endswith(".pyc") for name in names))
            self.assertFalse(any("review-report.md" in name for name in names))

    def test_repeated_builds_are_byte_identical(self):
        first = package_release.build_all(self.root, self.dist, validate=False)
        digests1 = [hashlib.sha256(path.read_bytes()).hexdigest() for path in first]
        second = package_release.build_all(self.root, self.dist, validate=False)
        digests2 = [hashlib.sha256(path.read_bytes()).hexdigest() for path in second]
        self.assertEqual(digests1, digests2)

    def test_validation_failure_prevents_archive_creation(self):
        (self.root / "tools").mkdir()
        shutil.copy2(
            package_release.ROOT / "tools/validate.py",
            self.root / "tools/validate.py",
        )
        (self.skill / "days/30.md").write_text(
            "# Day 30\n\nIncomplete lesson.\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            RuntimeError,
            r"days/30\.md: missing '## Concept'",
        ):
            package_release.build_all(self.root, self.dist, validate=True)

        for name in (
            "prompting-wizard-claude-skill.zip",
            "prompting-wizard-claude-plugin.zip",
            "prompting-wizard-openai-plugin.zip",
        ):
            self.assertFalse((self.dist / name).exists())


if __name__ == "__main__":
    unittest.main()
