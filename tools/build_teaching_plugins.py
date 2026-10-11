#!/usr/bin/env python3
"""Build skills-only native packages and check their generated repository assets."""
import argparse
import json
import tempfile
from pathlib import Path

from build_native_guide import build as build_guide
from package_release import write_zip
from validate import check_skill_metadata

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path('plugins/prompting-wizard-teacher')
CANONICAL = ('plugin.json', '.claude-plugin/plugin.json', 'skills/learn/SKILL.md')


def safe_path(root, name):
    path = root / name
    relative = path.relative_to(root)
    if any((root / Path(*relative.parts[:i])).is_symlink() for i in range(1, len(relative.parts) + 1)):
        raise ValueError(f'Symlink is not a package source or destination: {name}')
    return path


def entries(root=ROOT):
    """Explicit allowlist: never collect a user's working card or local runtime."""
    data = {name: safe_path(root, PLUGIN / name).read_bytes() for name in CANONICAL}
    errors = []
    check_skill_metadata(data['skills/learn/SKILL.md'].decode('utf-8'), errors)
    if errors:
        raise ValueError('; '.join(errors))
    manifests = [json.loads(data[name]) for name in CANONICAL[:2]]
    if any(m.get('name') != 'prompting-wizard-teacher' for m in manifests):
        raise ValueError('Unexpected native plugin identity')
    if manifests[0].get('version') != manifests[1].get('version'):
        raise ValueError('Native plugin manifest versions disagree')
    data['LICENSE'] = safe_path(root, Path('LICENSE')).read_bytes()
    data['assets/logo.png'] = safe_path(root, Path('assets/listing/logo.png')).read_bytes()
    with tempfile.TemporaryDirectory() as tmp:
        guide = build_guide(root, Path(tmp))
        data['skills/learn/references/guide.md'] = guide.read_bytes()
        data['skills/learn/references/empty-card.md'] = (Path(tmp) / 'prompting-wizard-learning-card.md').read_bytes()
    return data


def sync(root=ROOT):
    data = entries(root)
    destinations = {name: safe_path(root, PLUGIN / name) for name in data if name not in CANONICAL}
    for name, path in destinations.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data[name])
    return root / PLUGIN


def check(root=ROOT):
    data = entries(root)
    problems = []
    version = json.loads(data['plugin.json'])['version']
    for name in ('.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
        marketplace = json.loads(safe_path(root, Path(name)).read_text())
        matches = [entry for entry in marketplace.get('plugins', [])
                   if isinstance(entry, dict) and entry.get('name') == 'prompting-wizard-teacher']
        source = './' + PLUGIN.as_posix()
        expected = {'source': 'local', 'path': source} if name.startswith('.agents') else source
        if len(matches) != 1 or matches[0].get('source') != expected or matches[0].get('version') != version:
            problems.append(f'{name}: native teaching entry missing, duplicated or stale')
    for name, content in data.items():
        path = safe_path(root, PLUGIN / name)
        if not path.is_file() or path.read_bytes() != content:
            problems.append(f'{PLUGIN / name}: missing or stale; run tools/build_teaching_plugins.py --sync')
    for path in (root / PLUGIN).rglob('*'):
        if path.is_symlink() or (path.is_file() and path.relative_to(root / PLUGIN).as_posix() not in data):
            problems.append(f'{path.relative_to(root)}: unexpected package entry')
    return problems


def build(root=ROOT, dist=None):
    dist = dist or root / 'dist'
    data = entries(root)
    outputs = []
    for host, excluded in (('chatgpt', '.claude-plugin/plugin.json'), ('claude', 'plugin.json')):
        outputs.append(write_zip(dist / f'prompting-wizard-teacher-{host}.zip',
                                 [(name, content) for name, content in data.items() if name != excluded]))
    return tuple(outputs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sync', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.sync:
        print(sync().relative_to(ROOT))
    if args.check:
        problems = check()
        for problem in problems:
            print(problem)
        raise SystemExit(bool(problems))
    if not args.sync:
        for path in build():
            print(path.relative_to(ROOT))
