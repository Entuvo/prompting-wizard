#!/usr/bin/env python3
"""Create/preserve a project-owned map and register it with the shared local viewer."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import socket
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent / 'dashboard'))
from model import confined, mapping_sources, read_json, validate_map

MAP = '.keelson/dashboard/map.json'
README = '.keelson/dashboard/README.md'
GUIDANCE = '''# Project dashboard

This project owns map.json and its evidence. The shared viewer's registry is machine-local; do not commit absolute registry paths or authentication tokens.

Onboarding must populate architecture, capabilities, journeys, milestones and tasks from current project records. An installation scaffold is unverified, not product implementation or acceptance. Preserve settled decisions, proposals and unknowns. Follow .agents/skills/keelson/references/dashboard.md for reconciliation and registration. Existing private/public record boundaries remain authoritative.
'''


def default_registry():
    return Path.home().resolve() / '.local/share/keelson/dashboard/registry.json'


def no_symlinks(path):
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError(f'Symlink dashboard destination: {path}')


@contextmanager
def registry_lock(registry):
    registry = Path(registry).expanduser().absolute()
    if registry.is_symlink():
        raise ValueError(f'Symlink dashboard registry: {registry}')
    # Existing parent aliases (for example macOS /tmp) identify the same directory.
    registry = registry.parent.resolve() / registry.name
    no_symlinks(registry)
    registry.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = registry.with_name(registry.name + '.lock')
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError:
        raise ValueError(f'Dashboard registry busy: {registry}; inspect {lock}/owner.json before interrupted-writer recovery') from None
    owner = lock / 'owner.json'
    try:
        owner.write_text(json.dumps({'pid':os.getpid(), 'host':socket.gethostname(),
                                     'started_at':datetime.now(timezone.utc).isoformat()}) + '\n')
        yield registry
    finally:
        owner.unlink(missing_ok=True)
        lock.rmdir()


def initial_map():
    return {**{key: [] for key in ('components', 'edges', 'capabilities', 'journeys', 'milestones', 'evidence', 'releaseGates')},
            'tasks': [{'id':'map-project', 'name':'Ground dashboard in current project records', 'owner':'Onboarding agent',
                       'state':'unverified', 'description':'Populate confirmed scope and explicitly unknown/planned work; no product behavior is established.'}],
            'workflow': [{'id':'onboarding', 'name':'Dashboard onboarding', 'taskIds':['map-project'], 'evidenceIds':[]}],
            'scopeNote':'Unverified installation scaffold. Onboarding has not yet mapped this project. No runtime or acceptance evidence.',
            'mappingInputs': {'engineering':{}, 'records':{}}}


def encoded(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def prepare(target, registry, *, reconcile=False, sources=()):
    """Preflight every record before installation mutates project files. Caller holds registry lock."""
    target, registry = Path(target).resolve(), Path(registry).absolute()
    if not target.is_dir():
        raise ValueError('Dashboard project must be an existing directory')
    destination = confined(target, MAP)
    readme = confined(target, README)
    values = read_json(registry) if registry.exists() else {'projects':[]}
    projects = values.get('projects')
    if not isinstance(projects, list) or len(projects) > 50:
        raise ValueError('Invalid dashboard registry project list')
    ids = set()
    for entry in projects:
        if not isinstance(entry, dict) or any(not isinstance(entry.get(k), str) or not entry[k] for k in ('id','name','engineeringRoot','recordsRoot')):
            raise ValueError('Invalid dashboard registration')
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:/-]{0,239}',entry['id']) or entry['id'] in ids:
            raise ValueError('Invalid or duplicate dashboard project ID')
        if any(not Path(entry[k]).is_absolute() for k in ('engineeringRoot','recordsRoot')):
            raise ValueError('Dashboard roots must be absolute')
        ids.add(entry['id'])
    matches = [p for p in projects if Path(p['recordsRoot']).resolve() == target]
    if len(matches) > 1:
        raise ValueError('Ambiguous dashboard registrations for project')
    if not matches and any(Path(p['engineeringRoot']).resolve() == target for p in projects):
        raise ValueError('Project has a separate owning records root; register from that root')
    entry = matches[0] if matches else None
    previous_map = None
    if entry and entry.get('map'):
        previous_map = confined(Path(entry.get('mappingRoot',entry['recordsRoot'])),entry['map'])
        if not previous_map.is_file():
            raise ValueError('Registered dashboard map is missing; reconcile before installation')
        validate_map(read_json(previous_map))
    if destination.exists():
        mapping = read_json(destination); validate_map(mapping)
        if previous_map and previous_map != destination and read_json(previous_map) != read_json(destination):
            raise ValueError('Existing repo map conflicts with registered map; reconcile without overwriting')
        raw = destination.read_bytes()
    elif previous_map:
        raw = previous_map.read_bytes(); mapping = json.loads(raw)
    else:
        mapping = initial_map(); raw = encoded(mapping)
    if entry is None:
        if len(projects) == 50:
            raise ValueError('Dashboard registry project limit reached')
        name = re.sub(r'[^A-Za-z0-9_.-]+','-',target.name).strip('-.')[:180] or 'project'
        identity = name if name not in ids else name + '-' + hashlib.sha256(str(target).encode()).hexdigest()[:12]
        if identity in ids:
            raise ValueError('Dashboard project ID collision')
        entry = {'id':identity, 'name':target.name, 'engineeringRoot':str(target), 'recordsRoot':str(target),
                 'receiptDirs':['.keelson/reviews','.keelson/checks']}
        projects.append(entry)
    entry.update(mappingRoot=str(target),map=MAP)
    if 'checkpoint' not in entry and (target/'.keelson/checkpoint.md').is_file():
        confined(target,'.keelson/checkpoint.md')
        entry['checkpoint'] = '.keelson/checkpoint.md'
    if reconcile:
        declared = mapping_sources(mapping,entry)
        old = mapping.get('mappingInputs',{})
        for group in ('engineering','records'):
            # Retain explicitly recorded additional dependencies on every reconciliation.
            declared[group].update(old.get(group,{}))
        declared['records'].update(sources)
        hashes = {}
        for group, root in (('engineering',entry['engineeringRoot']),('records',entry['recordsRoot'])):
            hashes[group] = {}
            for name in sorted(declared[group]):
                if name == MAP or name.startswith('.keelson/dashboard/'):
                    raise ValueError('Mapping inputs must be source records, not dashboard output')
                path = confined(root,name)
                if not path.is_file() or path.stat().st_size > 64*1024*1024:
                    raise ValueError(f'Mapping source unavailable or oversized: {name}')
                hashes[group][name] = hashlib.sha256(path.read_bytes()).hexdigest()
        if not any(hashes.values()):
            raise ValueError('Cannot reconcile a map without source records')
        mapping['mappingInputs'] = hashes
        raw = encoded(mapping)
    writes = []
    if not destination.exists() or destination.read_bytes() != raw: writes.append((destination,raw))
    if not readme.exists(): writes.append((readme,GUIDANCE.encode()))
    if not registry.exists() or read_json(registry) != values: writes.append((registry,encoded(values)))
    return [(path,data,path.read_bytes() if path.exists() else None) for path,data in writes], entry


def apply(writes):
    for path, data, expected in writes:
        no_symlinks(path)
        if (path.read_bytes() if path.exists() else None) != expected:
            raise ValueError(f'Dashboard record changed during setup: {path}')
        path.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as stream:
            temporary = Path(stream.name)
            try:
                stream.write(data);stream.flush()
                if path.exists(): os.chmod(temporary,path.stat().st_mode & 0o777)
                os.replace(temporary,path)
            finally:
                temporary.unlink(missing_ok=True)


def setup(target, registry=None, *, reconcile=False, sources=()):
    with registry_lock(registry or default_registry()) as path:
        writes, entry = prepare(target,path,reconcile=reconcile,sources=sources)
        apply(writes)
        return entry


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=Path,help='Owning project records root')
    parser.add_argument('--registry',type=Path,default=None)
    parser.add_argument('--reconcile',action='store_true',help='Record source hashes after the agent has reconciled map content')
    parser.add_argument('--source',action='append',default=[],help='Additional source path relative to records root; requires --reconcile')
    args=parser.parse_args()
    if args.source and not args.reconcile:parser.error('--source requires --reconcile')
    try:
        entry=setup(args.project,args.registry,reconcile=args.reconcile,sources=args.source)
    except (OSError,ValueError,TypeError) as error:parser.exit(1,f'{error}\n')
    print(f"Registered {entry['name']}: {entry['mappingRoot']}/{entry['map']}")

if __name__=='__main__':main()
