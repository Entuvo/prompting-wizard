#!/usr/bin/env python3
"""Check that every local stylesheet in docs/*.html carries ?v=<hash of the file>.

Pages caches stylesheets for 10 minutes; the hash makes browsers fetch a changed file at once.
Run:  python3 tools/check_site.py          (exit 1 on a missing or stale hash)
      python3 tools/check_site.py --fix    (rewrite the hashes)
"""
import hashlib
import pathlib
import re
import sys

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
LINK = re.compile(r'(<link rel="stylesheet" href=")([^"?#:]+)(?:\?v=([0-9a-f]*))?(")')


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:8]


def main(fix):
    problems = 0
    for page in sorted(DOCS.glob("*.html")):
        text = page.read_text()

        def check(m):
            nonlocal problems
            target = page.parent / m.group(2)
            if not target.is_file():
                print(f"{page.name}: {m.group(2)} not found")
                problems += 1
                return m.group(0)
            want = file_hash(target)
            if m.group(3) != want:
                if not fix:
                    print(f"{page.name}: {m.group(2)} needs ?v={want} (has {m.group(3) or 'none'}); run with --fix")
                    problems += 1
                return f"{m.group(1)}{m.group(2)}?v={want}{m.group(4)}"
            return m.group(0)

        new = LINK.sub(check, text)
        if fix and new != text:
            page.write_text(new)
            print(f"{page.name}: hashes updated")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main("--fix" in sys.argv[1:]))
