#!/usr/bin/env python3
"""Publication guard regressions, using isolated temporary repositories."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parent
PAYLOAD = ".agents/skills/keelson/SKILL.md"


class WorkflowGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "tools").mkdir()
        for name in ("leak-check.sh", "workflow_guard.py"):
            shutil.copy2(TOOLS / name, self.root / "tools" / name)
        self.env = dict(os.environ, LEAK_DENYLIST="keelson\nimpeccable\n" + r"\.keelson" + "\nprivate-sentinel\n", GIT_AUTHOR_NAME="Entuvo", GIT_AUTHOR_EMAIL="info@entuvo.com", GIT_COMMITTER_NAME="Entuvo", GIT_COMMITTER_EMAIL="info@entuvo.com")
        self.run_cmd("git", "init", "-q")
        self.payload("# Keelson\nGeneric Impeccable workflow.\n")
        self.stage()

    def run_cmd(self, *args):
        return subprocess.run(args, cwd=self.root, env=self.env, capture_output=True, text=True)

    def payload(self, text):
        p = self.root / PAYLOAD
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        value = {"factory_revision": "a" * 40, "files": {PAYLOAD: hashlib.sha256(p.read_bytes()).hexdigest(), "tools/workflow_guard.py": hashlib.sha256((self.root / "tools/workflow_guard.py").read_bytes()).hexdigest()}}
        (self.root / "tools/workflow-files.json").write_text(json.dumps(value))

    def stage(self):
        self.assertEqual(self.run_cmd("git", "add", "-A").returncode, 0)

    def scan(self, mode="staged", *args):
        return self.run_cmd("bash", "tools/leak-check.sh", mode, *args).returncode

    def test_approved_generic_payload_passes(self):
        self.assertEqual(self.scan(), 0)
        self.assertEqual(self.scan("tree"), 0)

    def test_changed_or_unlisted_payload_fails(self):
        (self.root / PAYLOAD).write_text("changed")
        self.stage()
        self.assertNotEqual(self.scan(), 0)
        self.payload("# Keelson\n")
        (self.root / PAYLOAD).with_name("extra.md").write_text("unreviewed")
        self.stage()
        self.assertNotEqual(self.scan(), 0)

    def test_hard_protections_even_with_matching_hash(self):
        for text in ("/Us" + "ers/alice/private", "/ho" + "me/alice/private", "PRIVATE KEY" + "-----", json.dumps({'modelUsage': {}}), json.dumps({'costUSD': 3}), "private-sentinel"):
            with self.subTest(text=text):
                self.payload(text)
                self.stage()
                self.assertNotEqual(self.scan(), 0)

    def test_hard_protections_cover_binary_payload(self):
        self.payload(chr(0) + "/Us" + "ers/alice/private")
        self.stage()
        self.assertNotEqual(self.scan(), 0)

    def test_private_paths_are_not_whitelisted(self):
        for name in (".keelson/checkpoint.md", "PRODUCT.md", ".codex/config.toml", ".agents/skills/other/SKILL.md"):
            with self.subTest(name=name):
                p = self.root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("private")
                self.stage()
                self.assertNotEqual(self.scan(), 0)
                p.unlink()

    def test_nonworkflow_content_keeps_denylist(self):
        (self.root / "README.md").write_text("private-sentinel")
        self.stage()
        self.assertNotEqual(self.scan(), 0)

    def test_manifest_cannot_allow_private_path(self):
        p = self.root / "tools/workflow-files.json"
        value = json.loads(p.read_text())
        value["files"][".keelson/checkpoint.md"] = "a" * 64
        p.write_text(json.dumps(value))
        self.stage()
        self.assertNotEqual(self.scan(), 0)

    def test_staged_policy_not_unstaged_policy(self):
        self.payload("tampered")
        self.run_cmd("git", "add", PAYLOAD)
        self.assertNotEqual(self.scan(), 0)

    def test_push_checks_each_commits_own_manifest(self):
        self.assertEqual(self.run_cmd("git", "commit", "-qm", "Generic workflow").returncode, 0)
        old = self.run_cmd("git", "rev-parse", "HEAD").stdout.strip()
        self.payload("# Keelson updated\n")
        self.stage()
        self.assertEqual(self.run_cmd("git", "commit", "-qm", "Update generic workflow").returncode, 0)
        self.payload("# Keelson revised again\n")
        self.stage()
        self.assertEqual(self.run_cmd("git", "commit", "-qm", "Second generic update").returncode, 0)
        head = self.run_cmd("git", "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(self.scan("push", old, head), 0)
        self.payload("private-sentinel")
        self.stage()
        self.run_cmd("git", "commit", "-qm", "Private fixture")
        head = self.run_cmd("git", "rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(self.scan("push", old, head), 0)


if __name__ == "__main__":
    unittest.main()
