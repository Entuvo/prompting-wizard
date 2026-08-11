#!/usr/bin/env python3
"""Filesystem-level tests for the local Prompting Wizard installer."""

import errno
import os
import pty
import select
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SYSTEM_PATH = os.pathsep.join(
    dict.fromkeys((str(Path(sys.executable).parent), "/usr/bin", "/bin"))
)
REAL_RM = shutil.which("rm", path=SYSTEM_PATH)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.sandbox = Path(self.tmp.name)
        self.home = self.sandbox / "home"
        self.home.mkdir()
        self.bin = self.sandbox / "bin"
        self.bin.mkdir()

    def stub(self, name, body="exit 0"):
        path = self.bin / name
        path.write_text(f"#!/bin/sh\n{body}\n", encoding="utf-8")
        path.chmod(0o755)
        return path

    def run_install(self, *args, input_text=None, env_extra=None):
        env = self.install_env(env_extra)
        return subprocess.run(
            ["sh", str(ROOT / "install.sh"), *args],
            input=input_text,
            text=True,
            capture_output=True,
            env=env,
        )

    def install_env(self, env_extra=None):
        env = os.environ.copy()
        env.update(
            {
                "HOME": str(self.home),
                "PATH": f"{self.bin}{os.pathsep}{SYSTEM_PATH}",
                "PW_REPO_ROOT": str(ROOT),
            }
        )
        if env_extra:
            env.update(env_extra)
        return env

    def run_install_pty(self, *args, env_extra=None, response=b"y\n"):
        env = self.install_env(env_extra)
        pid, master = pty.fork()
        if pid == 0:
            os.execve("/bin/sh", ["sh", str(ROOT / "install.sh"), *args], env)

        output = bytearray()
        sent_response = False
        deadline = time.monotonic() + 10
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    os.kill(pid, 9)
                    raise AssertionError("installer PTY timed out")
                readable, _, _ = select.select([master], [], [], remaining)
                if not readable:
                    os.kill(pid, 9)
                    raise AssertionError("installer PTY timed out")
                try:
                    chunk = os.read(master, 4096)
                except OSError as exc:
                    if exc.errno == errno.EIO:
                        break
                    raise
                if not chunk:
                    break
                output.extend(chunk)
                if not sent_response and b"Replace it?" in output:
                    os.write(master, response)
                    sent_response = True
        finally:
            os.close(master)
        _, status = os.waitpid(pid, 0)
        return subprocess.CompletedProcess(
            ["sh", str(ROOT / "install.sh"), *args],
            os.waitstatus_to_exitcode(status),
            stdout=output.decode("utf-8", errors="replace"),
            stderr="",
        )

    def copy_repo_without(self, relative):
        repo = self.sandbox / "broken-repo"
        shutil.copytree(ROOT / "prompting-wizard", repo / "prompting-wizard")
        shutil.copytree(ROOT / ".claude-plugin", repo / ".claude-plugin")
        (repo / "tools").mkdir()
        shutil.copy2(ROOT / "tools/validate.py", repo / "tools/validate.py")
        path = repo / relative
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        return repo

    def copy_repo_with_artifacts(self):
        repo = self.sandbox / "artifact-repo"
        shutil.copytree(ROOT / "prompting-wizard", repo / "prompting-wizard")
        shutil.copytree(ROOT / ".claude-plugin", repo / ".claude-plugin")
        (repo / "tools").mkdir()
        shutil.copy2(ROOT / "tools/validate.py", repo / "tools/validate.py")
        skill = repo / "prompting-wizard"
        (skill / "PROGRESS.md").write_text("private state\n", encoding="utf-8")
        (skill / "__pycache__").mkdir()
        (skill / "__pycache__/state.pyc").write_bytes(b"cache")
        (skill / "days/cache.pyc").write_bytes(b"cache")
        return repo

    def assert_clean_siblings(self, root):
        leftovers = list(root.glob(".prompting-wizard.*")) if root.exists() else []
        self.assertEqual(leftovers, [])

    def test_detects_codex_and_installs_canonical_skill(self):
        self.stub("codex")

        result = self.run_install()

        target = self.home / ".agents/skills/prompting-wizard"
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            (target / "SKILL.md").read_bytes(),
            (ROOT / "prompting-wizard/SKILL.md").read_bytes(),
        )
        self.assertFalse((target / ".claude-plugin").exists())
        self.assertFalse((self.home / ".claude/skills/prompting-wizard").exists())
        self.assertIn(str(target), result.stdout)
        self.assertIn(
            "Open a new chat in the installed agent and say: "
            "Start Prompting Wizard.",
            result.stdout,
        )

    def test_detects_claude_only_and_retains_claude_manifest(self):
        self.stub("claude")

        result = self.run_install()

        target = self.home / ".claude/skills/prompting-wizard"
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((target / "SKILL.md").is_file())
        self.assertTrue((target / ".claude-plugin/plugin.json").is_file())
        self.assertFalse((self.home / ".agents/skills/prompting-wizard").exists())

    def test_detects_both_clients_and_installs_both_host_layouts(self):
        self.stub("codex")
        self.stub("claude")

        result = self.run_install()

        codex = self.home / ".agents/skills/prompting-wizard"
        claude = self.home / ".claude/skills/prompting-wizard"
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((codex / "SKILL.md").is_file())
        self.assertFalse((codex / ".claude-plugin").exists())
        self.assertTrue((claude / ".claude-plugin/plugin.json").is_file())

    def test_no_detected_client_explains_all_explicit_overrides(self):
        result = self.run_install()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--codex", result.stderr)
        self.assertIn("--claude-code", result.stderr)
        self.assertIn("--all", result.stderr)
        self.assertFalse((self.home / ".agents").exists())
        self.assertFalse((self.home / ".claude").exists())

    def test_all_installs_to_custom_roots_without_detected_clients(self):
        codex_root = self.sandbox / "custom codex"
        claude_root = self.sandbox / "custom claude"

        result = self.run_install(
            "--all",
            env_extra={
                "PW_CODEX_SKILLS_DIR": str(codex_root),
                "PW_CLAUDE_SKILLS_DIR": str(claude_root),
            },
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((codex_root / "prompting-wizard/SKILL.md").is_file())
        self.assertTrue((claude_root / "prompting-wizard/SKILL.md").is_file())
        self.assertFalse((self.home / ".agents").exists())
        self.assertFalse((self.home / ".claude").exists())

    def test_all_rejects_one_shared_target_before_installing_either_host(self):
        shared_root = self.sandbox / "shared skills"

        result = self.run_install(
            "--all",
            env_extra={
                "PW_CODEX_SKILLS_DIR": str(shared_root),
                "PW_CLAUDE_SKILLS_DIR": str(shared_root),
            },
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((shared_root / "prompting-wizard").exists())
        self.assert_clean_siblings(shared_root)

    def test_invalid_flag_returns_usage_error_without_mutation(self):
        result = self.run_install("--unknown")

        self.assertEqual(result.returncode, 2)
        self.assertIn("Usage:", result.stderr)
        self.assertFalse((self.home / ".agents").exists())
        self.assertFalse((self.home / ".claude").exists())

    def test_noninteractive_existing_install_is_not_overwritten(self):
        target = self.home / ".agents/skills/prompting-wizard"
        target.mkdir(parents=True)
        (target / "sentinel").write_text("keep", encoding="utf-8")

        result = self.run_install("--codex", input_text="y\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((target / "sentinel").read_text(), "keep")
        self.assertFalse((target / "SKILL.md").exists())
        self.assertIn("--force", result.stderr)
        self.assert_clean_siblings(target.parent)

    def test_tty_confirmation_preserves_later_failure_diagnostics(self):
        target = self.home / ".agents/skills/prompting-wizard"
        target.mkdir(parents=True)
        (target / "sentinel").write_text("keep\n", encoding="utf-8")
        counter = self.sandbox / "pty-rename-count"
        self.stub(
            "python3",
            f'if [ "$1" = - ] && [ "$2" = rename ]; then\n'
            f'  count=0\n'
            f'  [ ! -f "$PW_RENAME_COUNT_FILE" ] || '
            f'count=$(sed -n "1p" "$PW_RENAME_COUNT_FILE")\n'
            f'  count=$((count + 1))\n'
            f'  echo "$count" > "$PW_RENAME_COUNT_FILE"\n'
            f'  [ "$count" -ne 2 ] || exit 72\n'
            f'fi\n'
            f'exec "{sys.executable}" "$@"',
        )

        result = self.run_install_pty(
            "--codex",
            env_extra={"PW_RENAME_COUNT_FILE": str(counter)},
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Replace it?", result.stdout)
        self.assertIn("prior installation restored", result.stdout)
        self.assertEqual((target / "sentinel").read_text(), "keep\n")
        self.assert_clean_siblings(target.parent)

    def test_target_appearing_during_staging_survives_without_authorization(self):
        target = self.home / ".agents/skills/prompting-wizard"
        race_marker = self.sandbox / "race-created"
        self.stub(
            "python3",
            f'if [ "$1" = - ] && '
            f'[ "$2" = "$PW_REPO_ROOT/prompting-wizard" ] && '
            f'[ ! -f "$PW_RACE_MARKER" ]; then\n'
            f'  mkdir -p "$PW_RACE_TARGET"\n'
            f'  printf "concurrent\\n" > "$PW_RACE_TARGET/sentinel"\n'
            f'  : > "$PW_RACE_MARKER"\n'
            f'fi\n'
            f'exec "{sys.executable}" "$@"',
        )

        result = self.run_install(
            "--codex",
            env_extra={
                "PW_RACE_MARKER": str(race_marker),
                "PW_RACE_TARGET": str(target),
            },
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((target / "sentinel").read_text(), "concurrent\n")
        self.assertEqual(sorted(p.name for p in target.iterdir()), ["sentinel"])
        self.assert_clean_siblings(target.parent)

    def test_empty_target_appearing_at_rename_boundary_is_not_replaced(self):
        target = self.home / ".agents/skills/prompting-wizard"
        inode_record = self.sandbox / "concurrent-inode"
        self.stub(
            "python3",
            f'if [ "$1" = - ] && [ "$2" = rename ] && '
            f'[ ! -f "$PW_RACE_INODE" ]; then\n'
            f'  case "$4" in\n'
            f'    */prompting-wizard)\n'
            f'      mkdir "$PW_RACE_TARGET"\n'
            f'      "{sys.executable}" -c '
            f'"import os,sys; print(os.stat(sys.argv[1]).st_ino)" '
            f'"$PW_RACE_TARGET" > "$PW_RACE_INODE"\n'
            f'      ;;\n'
            f'  esac\n'
            f'fi\n'
            f'exec "{sys.executable}" "$@"',
        )

        result = self.run_install(
            "--codex",
            env_extra={
                "PW_RACE_INODE": str(inode_record),
                "PW_RACE_TARGET": str(target),
            },
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(target.is_dir())
        self.assertEqual(target.stat().st_ino, int(inode_record.read_text()))
        self.assertEqual(list(target.iterdir()), [])
        self.assert_clean_siblings(target.parent)

    def test_force_replaces_only_the_named_skill(self):
        skills_root = self.home / ".agents/skills"
        target = skills_root / "prompting-wizard"
        target.mkdir(parents=True)
        (target / "old").write_text("old", encoding="utf-8")
        neighbor = skills_root / "other-skill"
        neighbor.mkdir()
        (neighbor / "sentinel").write_text("keep", encoding="utf-8")

        result = self.run_install("--codex", "--force")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((target / "old").exists())
        self.assertTrue((target / "SKILL.md").is_file())
        self.assertEqual((neighbor / "sentinel").read_text(), "keep")
        self.assert_clean_siblings(skills_root)

    def test_validation_failure_mutates_nothing(self):
        broken = self.copy_repo_without("prompting-wizard/days/30.md")
        skills_root = self.sandbox / "not-created"

        result = self.run_install(
            "--codex",
            env_extra={
                "PW_REPO_ROOT": str(broken),
                "PW_CODEX_SKILLS_DIR": str(skills_root),
            },
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(skills_root.exists())
        self.assertIn("days/30.md: missing", result.stderr)

    def test_state_caches_and_host_inappropriate_manifest_are_excluded(self):
        repo = self.copy_repo_with_artifacts()

        result = self.run_install("--all", env_extra={"PW_REPO_ROOT": str(repo)})

        codex = self.home / ".agents/skills/prompting-wizard"
        claude = self.home / ".claude/skills/prompting-wizard"
        self.assertEqual(result.returncode, 0, result.stderr)
        for target in (codex, claude):
            self.assertFalse((target / "PROGRESS.md").exists())
            self.assertFalse((target / "__pycache__").exists())
            self.assertFalse((target / "days/cache.pyc").exists())
        self.assertFalse((codex / ".claude-plugin").exists())
        self.assertTrue((claude / ".claude-plugin/plugin.json").is_file())

    def test_failed_replacement_restores_exact_prior_install(self):
        skills_root = self.home / ".agents/skills"
        target = skills_root / "prompting-wizard"
        (target / "nested").mkdir(parents=True)
        (target / "sentinel").write_bytes(b"keep\x00exact")
        (target / "nested/data").write_text("prior\n", encoding="utf-8")
        counter = self.sandbox / "rename-count"
        self.stub(
            "python3",
            f'if [ "$1" = - ] && [ "$2" = rename ]; then\n'
            f'  count=0\n'
            f'  [ ! -f "$PW_RENAME_COUNT_FILE" ] || '
            f'count=$(sed -n "1p" "$PW_RENAME_COUNT_FILE")\n'
            f'  count=$((count + 1))\n'
            f'  echo "$count" > "$PW_RENAME_COUNT_FILE"\n'
            f'  [ "$count" -ne 2 ] || exit 73\n'
            f'fi\n'
            f'exec "{sys.executable}" "$@"',
        )

        result = self.run_install(
            "--codex",
            "--force",
            env_extra={"PW_RENAME_COUNT_FILE": str(counter)},
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(counter.read_text(encoding="utf-8").strip(), "3")
        self.assertEqual((target / "sentinel").read_bytes(), b"keep\x00exact")
        self.assertEqual((target / "nested/data").read_text(), "prior\n")
        self.assertEqual(sorted(p.name for p in target.iterdir()), ["nested", "sentinel"])
        self.assert_clean_siblings(skills_root)

    def test_backup_cleanup_failure_cannot_remove_the_committed_install(self):
        if REAL_RM is None:
            self.skipTest("rm is unavailable")
        target = self.home / ".agents/skills/prompting-wizard"
        target.mkdir(parents=True)
        (target / "old").write_text("old\n", encoding="utf-8")
        self.stub("rm", f'"{REAL_RM}" "$@"\nexit 74')

        result = self.run_install("--codex", "--force")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((target / "SKILL.md").is_file())
        self.assertFalse((target / "old").exists())
        self.assertIn("Warning: could not completely remove backup", result.stderr)
        self.assert_clean_siblings(target.parent)


if __name__ == "__main__":
    unittest.main()
