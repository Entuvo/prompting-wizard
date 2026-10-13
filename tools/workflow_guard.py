#!/usr/bin/env python3
"""Check exact reviewed workflow blobs without relaxing private-content checks.

Only published skill names, generic operating-model wording, workflow directory
references and the UI receipt class are exempted from private keyword matching.
Every other denylist rule and all local-path/key/run-log protections still apply.
Policy updates require review alongside the changed payload.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

POLICY = "tools/workflow-files.json"
AUXILIARY = {"AGENTS.md", "tools/workflow_guard.py", "tools/test_workflow_guard.py"}
ROOTS = (".agents/skills/keelson/", ".agents/skills/impeccable/", ".agents/skills/diagram-design/", "references/impeccable/")
EXCEPTIONS = {"keelson", "impeccable", "operating model", r"\.keelson", '\"receipt\"'}
HARD = r'/Users/[A-Za-z]|/home/[a-z]|\"modelUsage\"|\"costUSD\"|PRIVATE KEY' + r'-----'


def selected(name):
    return name in AUXILIARY or name.startswith(ROOTS)


def check(name, candidate, denylist, policy):
    if name != POLICY and not selected(name):
        return 2
    try:
        value = json.loads(Path(policy).read_text())
        if set(value) != {"factory_revision", "files"} or not re.fullmatch(r"[0-9a-f]{40}", value["factory_revision"]):
            return 1
        files = value["files"]
        if not isinstance(files, dict) or not files:
            return 1
        for path, digest in files.items():
            if not selected(path) or ".." in Path(path).parts or any(p.startswith(".") for p in Path(path).parts[1:]) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                return 1
        data = Path(candidate).read_bytes()
        if name == POLICY:
            if json.loads(data) != value:
                return 1
        elif hashlib.sha256(data).hexdigest() != files.get(name):
            return 1
        # Hard protections cover binary payloads too, even with an approved hash.
        if re.search(HARD.encode(), data):
            return 1
        patterns = [p for p in Path(denylist).read_text().splitlines() if p and p.lower() not in EXCEPTIONS] if denylist else []
        if patterns:
            with tempfile.NamedTemporaryFile(mode="w") as rules:
                rules.write("\n".join(patterns) + "\n")
                rules.flush()
                result = subprocess.run(["grep", "-I", "-i", "-E", "-q", "-f", rules.name, candidate])
                if result.returncode != 1:
                    return 1
        return 0
    except (OSError, ValueError, TypeError, AttributeError):
        return 1


if __name__ == "__main__":
    raise SystemExit(check(*sys.argv[1:]))
