#!/usr/bin/env python3
"""Tests for install-chatgpt.sh against a temporary HOME and a locally built OpenAI zip."""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from package_release import build_all

ZIP = "prompting-wizard-openai.zip"
ENTRY_PATH = "./.codex/plugins/prompting-wizard"


class ChatGPTInstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = tempfile.TemporaryDirectory()
        cls.dist = Path(cls.build.name) / "dist"
        build_all(ROOT, cls.dist, validate=False)
        digest = hashlib.sha256((cls.dist / ZIP).read_bytes()).hexdigest()
        (cls.dist / "SHA256SUMS").write_text(f"{digest}  {ZIP}\n", encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.build.cleanup()

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name) / "home"
        self.home.mkdir()
        self.target = self.home / ".codex/plugins/prompting-wizard"
        self.marketplace = self.home / ".agents/plugins/marketplace.json"

    def run_installer(self, *args, env=None):
        return subprocess.run(["sh", str(ROOT / "install-chatgpt.sh"), *args], text=True, capture_output=True,
                              env={**os.environ, "HOME": str(self.home), **(env or {})})

    def install(self, zip_path=None):
        return self.run_installer("--zip", str(zip_path or self.dist / ZIP))

    def entries(self):
        plugins = json.loads(self.marketplace.read_text(encoding="utf-8"))["plugins"]
        return [p for p in plugins if p.get("name") == "prompting-wizard"]

    def test_fresh_install_registers_plugin_and_rerun_keeps_one_entry(self):
        for _ in range(2):
            result = self.install()
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.target / "plugin.json").read_text())["name"], "prompting-wizard")
        self.assertTrue((self.target / "skills/prompting-wizard/SKILL.md").is_file())
        self.assertEqual([e["source"] for e in self.entries()], [{"source": "local", "path": ENTRY_PATH}])
        self.assertIn("Plugins, then Personal", result.stdout)
        self.assertEqual(list(self.marketplace.parent.glob("marketplace.json.bak-*")), [])

    def test_existing_marketplace_keeps_other_entries_and_fields(self):
        other = {"name": "other", "source": {"source": "local", "path": "./x"}, "custom": [1, "é"]}
        original = {"name": "mine", "interface": {"displayName": "Mine"}, "extra": True,
                    "plugins": [other, {"name": "prompting-wizard", "source": "./old"}]}
        self.marketplace.parent.mkdir(parents=True)
        self.marketplace.write_text(json.dumps(original), encoding="utf-8")
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(self.marketplace.read_text(encoding="utf-8"))
        self.assertEqual({k: v for k, v in data.items() if k != "plugins"},
                         {k: v for k, v in original.items() if k != "plugins"})
        self.assertEqual(data["plugins"][0], other)
        self.assertEqual(data["plugins"][1]["source"]["path"], ENTRY_PATH)
        self.assertEqual(len(data["plugins"]), 2)
        backups = list(self.marketplace.parent.glob("marketplace.json.bak-*"))
        self.assertEqual([json.loads(b.read_text()) for b in backups], [original])

    def test_invalid_marketplace_json_is_refused_without_writes(self):
        self.marketplace.parent.mkdir(parents=True)
        self.marketplace.write_text("{not json", encoding="utf-8")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not valid JSON", result.stderr)
        self.assertEqual(self.marketplace.read_text(encoding="utf-8"), "{not json")
        self.assertEqual(sorted(p.name for p in self.marketplace.parent.iterdir()), ["marketplace.json"])
        self.assertFalse((self.home / ".codex").exists())

    def test_checksum_mismatch_is_refused(self):
        bad = self.home / "dl"
        bad.mkdir()
        (bad / ZIP).write_bytes((self.dist / ZIP).read_bytes())
        (bad / "SHA256SUMS").write_text(f"{'0' * 64}  {ZIP}\n", encoding="utf-8")
        for result in (self.install(bad / ZIP), self.run_installer(env={"PW_RELEASE_URL": bad.as_uri()})):
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("checksum mismatch", result.stderr)
        self.assertFalse(self.target.exists())
        self.assertFalse(self.marketplace.exists())

    def test_download_from_release_url_verifies_and_installs(self):
        result = self.run_installer(env={"PW_RELEASE_URL": self.dist.as_uri()})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Checksum verified", result.stdout)
        self.assertEqual(len(self.entries()), 1)

    def test_matching_zip_in_downloads_is_used_instead_of_downloading(self):
        release = self.home / "release"
        release.mkdir()
        (release / "SHA256SUMS").write_bytes((self.dist / "SHA256SUMS").read_bytes())
        (self.home / "Downloads").mkdir()
        (self.home / "Downloads" / ZIP).write_bytes((self.dist / ZIP).read_bytes())
        result = self.run_installer(env={"PW_RELEASE_URL": release.as_uri()})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("matches the", result.stdout)
        self.assertEqual(len(self.entries()), 1)

    def test_other_zip_in_downloads_falls_back_to_pinned_download(self):
        (self.home / "Downloads").mkdir()
        (self.home / "Downloads" / ZIP).write_bytes(b"an older release")
        result = self.run_installer(env={"PW_RELEASE_URL": self.dist.as_uri()})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("is not the", result.stdout)
        self.assertIn("Checksum verified", result.stdout)
        self.assertTrue((self.target / "plugin.json").is_file())

    def test_symlink_target_is_refused(self):
        elsewhere = self.home / "elsewhere"
        elsewhere.mkdir()
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(elsewhere)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("is a symlink", result.stderr)
        self.assertEqual(list(elsewhere.iterdir()), [])
        self.assertTrue(self.target.is_symlink())

    def test_reinstall_keeps_previous_copy(self):
        self.install()
        (self.target / "marker").write_text("old", encoding="utf-8")
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.target / "marker").exists())
        self.assertTrue((self.target.parent / ".prompting-wizard.previous/marker").is_file())

    def test_uninstall_removes_folder_and_entry_only(self):
        self.marketplace.parent.mkdir(parents=True)
        self.marketplace.write_text(json.dumps({"name": "m", "plugins": [{"name": "other"}]}), encoding="utf-8")
        self.install()
        result = self.run_installer("--uninstall")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.target.exists())
        self.assertTrue((self.target.parent / ".prompting-wizard.previous/plugin.json").is_file())
        self.assertEqual(json.loads(self.marketplace.read_text())["plugins"], [{"name": "other"}])

    def test_wrong_zip_is_refused(self):
        claude = self.home / "prompting-wizard-claude.zip"
        claude.write_bytes((self.dist / claude.name).read_bytes())
        result = self.install(claude)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not the Prompting Wizard plugin", result.stderr)
        self.assertFalse(self.target.exists())
        self.assertEqual(list(self.target.parent.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
