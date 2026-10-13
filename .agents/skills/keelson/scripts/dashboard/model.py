"""Read-only dashboard projection. Records describe scope; receipts establish evidence."""
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from evidence import inputs as input_hashes

COLLECTIONS = ('components', 'edges', 'capabilities', 'journeys', 'tasks', 'milestones', 'evidence', 'workflow')
ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.:/-]{0,239}$')
MAX_BYTES = 2 * 1024 * 1024


def now():
    return datetime.now(timezone.utc).isoformat()


def confined(root, name):
    root = Path(root).resolve()
    name = Path(name)
    if name.is_absolute() or '..' in name.parts:
        raise ValueError('Record path escapes configured root')
    path = root / name
    if not path.resolve().is_relative_to(root) or any(p.is_symlink() for p in [path, *path.parents] if p != root and p.is_relative_to(root)):
        raise ValueError('Record symlinks are not allowed')
    return path


def read_json(path):
    with Path(path).open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('Record exceeds 2 MiB limit')
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError('Record must be an object')
    pending = [(value, 0)]
    while pending:
        item, depth = pending.pop()
        if depth > 64:
            raise ValueError('Record exceeds nesting limit')
        if isinstance(item, dict): pending.extend((v, depth + 1) for v in item.values())
        elif isinstance(item, list): pending.extend((v, depth + 1) for v in item)
    return value


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamp must include timezone')
    return parsed


def hashes_match(root, values):
    if not isinstance(values, dict) or not values:
        return False
    try:
        for name, digest in values.items():
            path = confined(root, name)
            if path.stat().st_size > 32 * MAX_BYTES:
                return False
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                return False
        return True
    except (OSError, ValueError, TypeError):
        return False


def validate_map(mapping):
    inputs = mapping.get('mappingInputs', {})
    if (not isinstance(inputs, dict) or set(inputs) - {'engineering','records'}
            or any(not isinstance(values, dict) or any(not isinstance(name,str) or not isinstance(digest,str)
                   or not re.fullmatch(r'[0-9a-f]{64}',digest) for name,digest in values.items()) for values in inputs.values())):
        raise ValueError('Invalid mapping input hashes')
    indexes = {}
    for key in COLLECTIONS:
        values = mapping.setdefault(key, [])
        if not isinstance(values, list) or len(values) > 1000:
            raise ValueError(f'{key}: expected list of at most 1000 records')
        indexes[key] = {}
        for item in values:
            if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not ID.fullmatch(item['id']):
                raise ValueError(f'{key}: invalid ID')
            if item['id'] in indexes[key]:
                raise ValueError(f'{key}: duplicate ID {item["id"]}')
            indexes[key][item['id']] = item
            for field in ('name', 'owner', 'state', 'source'):
                if field in item and not isinstance(item[field], str):
                    raise ValueError(f'{key}: invalid {field}')
    links = {'componentIds':'components', 'edgeIds':'edges', 'journeyIds':'journeys', 'taskIds':'tasks',
             'milestoneIds':'milestones', 'evidenceIds':'evidence', 'dependsOn':'tasks'}
    for values in indexes.values():
        for item in values.values():
            for field, target in links.items():
                refs = item.get(field, [])
                if not isinstance(refs, list) or any(not isinstance(ref, str) or ref not in indexes[target] for ref in refs):
                    raise ValueError(f'{item["id"]}: invalid {field}')
    for edge in mapping['edges']:
        if any(edge.get(k) not in indexes['components'] for k in ('from', 'to')):
            raise ValueError(f'{edge["id"]}: invalid endpoints')
    for component in mapping['components']:
        if not isinstance(component.get('sources', []), list) or any(not isinstance(s, str) for s in component.get('sources', [])):
            raise ValueError('Invalid component sources')
        for key in ('column', 'row'):
            if key in component and (type(component[key]) is not int or not 0 <= component[key] <= 12):
                raise ValueError('Invalid component layout')
    for task in mapping['tasks']:
        blockers = task.get('blockers', [])
        if not isinstance(blockers, list) or any(not isinstance(b, dict) or not all(isinstance(b.get(k), str) for k in ('owner','action')) for b in blockers):
            raise ValueError('Invalid blockers')
    def validate_gates(gates):
        if not isinstance(gates, list): raise ValueError('Gates must be a list')
        for gate in gates:
            if not isinstance(gate, dict) or not isinstance(gate.get('label'), str): raise ValueError('Invalid gate')
            keys = [k for k in ('evidenceId', 'milestoneId') if k in gate]
            if len(keys) != 1: raise ValueError('Gate needs exactly one evidence or milestone predicate')
            key = keys[0]
            if gate[key] not in indexes['evidence' if key == 'evidenceId' else 'milestones']: raise ValueError('Unknown gate target')
            if 'journeyId' in gate and gate['journeyId'] not in indexes['journeys']: raise ValueError('Unknown gate journey')
    validate_gates(mapping.setdefault('releaseGates', []))
    for milestone in mapping['milestones']: validate_gates(milestone.setdefault('gates', []))
    return indexes


def revision(root):
    try:
        return subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL, timeout=3, text=True).strip()
    except (OSError, subprocess.SubprocessError):
        return 'unversioned'


def mapping_sources(mapping, config):
    values = {'engineering':set(), 'records':set()}
    for component in mapping.get('components', []):
        values['engineering'].update(component.get('sources', []))
    for task in mapping.get('tasks', []):
        name = task.get('source')
        if name:
            group = 'records' if confined(config['recordsRoot'],name).is_file() else 'engineering'
            values[group].add(name)
    return values


def mapping_status(mapping, config):
    recorded = mapping.get('mappingInputs')
    if not recorded or not any(recorded.values()): return 'unverified'
    try:
        needed = mapping_sources(mapping,config)
        for group, root in (('engineering',config['engineeringRoot']),('records',config['recordsRoot'])):
            hashes = recorded.get(group,{})
            if not needed[group].issubset(hashes) or (hashes and not hashes_match(root,hashes)):
                return 'stale'
        return 'current'
    except (OSError,ValueError,TypeError,AttributeError):
        return 'stale'


def receipt_evidence(config, binding):
    root, records = Path(config['engineeringRoot']).resolve(), Path(config['recordsRoot']).resolve()
    result = {**binding, 'result':'unknown', 'freshness':'unknown', 'sourceApplicability':'unknown',
              'observedAt':None, 'startedAt':None, 'revision':None, 'environment':'not recorded', 'kind':'unknown'}
    try:
        path = confined(records, binding['receipt'])
        receipt = read_json(path)
        result.update(result=receipt.get('status', 'unknown'), kind=receipt.get('stage', 'review' if receipt.get('model') else 'legacy'),
                      observedAt=receipt.get('finished_at'), startedAt=receipt.get('started_at', receipt.get('created_at')),
                      revision=receipt.get('revision'), environment=receipt.get('contract', {}).get('context', 'source review' if receipt.get('model') else 'not recorded'),
                      unit=receipt.get('unit'), cost=receipt.get('reported_cost_usd'), duration=receipt.get('elapsed_seconds'))
        if result['observedAt']: timestamp(result['observedAt'])
        project_matches = receipt.get('project') == str(root)
        if receipt.get('stage') == 'verification' and project_matches:
            spec = receipt.get('contract', {})
            result['inputHashes'] = receipt.get('inputs', {})
            spec_path = Path(receipt.get('contract_path', ''))
            # Existing contracts may live in either registered root; never arbitrary paths.
            owner = next((r for r in (root, records) if spec_path.is_absolute() and spec_path.resolve().is_relative_to(r)), None)
            current_spec = read_json(confined(owner, str(spec_path.relative_to(owner)))) if owner else None
            try:
                matches = current_spec == spec and input_hashes(root, spec) == receipt.get('inputs')
            except (OSError, ValueError):
                matches = False
            result['sourceApplicability'] = 'current' if matches else 'stale'
        elif result['kind'] == 'review' and project_matches:
            values = {f['path']:f['sha256'] for f in receipt.get('files', [])}
            result['inputHashes'] = values
            matches = hashes_match(root, values)
            # Review packet embeds verified contracts: added dependency files invalidate it too.
            packet = read_json(confined(records, str(Path(binding['receipt']).parent / 'input.json')))
            for check in packet.get('verification', []):
                spec_path = Path(check['contract_path'])
                owner = next((r for r in (root, records) if spec_path.resolve().is_relative_to(r)), None)
                if owner is None or read_json(confined(owner, str(spec_path.relative_to(owner)))) != check['contract'] or input_hashes(root, check['contract']) != check['inputs']:
                    matches = False
            result['sourceApplicability'] = 'current' if matches else 'stale'
            result['result'] = 'passed' if receipt.get('status') == 'reviewed' and receipt.get('assessment') == 'ready' else receipt.get('status', 'unknown')
            if receipt.get('status') == 'reviewed':
                result['result'] = {'ready':'passed','changes':'changes requested','blocked':'blocked'}.get(receipt.get('assessment'),'unknown')
            # A verdict without its scope must not become a generic green review gate.
            result['reviewPurpose'] = packet.get('purpose')
            if receipt.get('status') == 'reviewed':
                try:
                    review = read_json(confined(records, str(Path(binding['receipt']).parent / 'review.json')))
                    limits = review.get('limits')
                    if (not isinstance(result['reviewPurpose'], str) or not result['reviewPurpose'].strip()
                            or not isinstance(limits, list) or not limits
                            or not all(isinstance(item, str) and item.strip() for item in limits)
                            or not isinstance(review.get('summary'), str) or not review['summary'].strip()
                            or review.get('assessment') != receipt.get('assessment')):
                        raise ValueError('Missing or inconsistent review scope')
                    result.update(reviewScope='recorded', reviewLimits=limits, reviewSummary=review['summary'])
                except (OSError, ValueError, TypeError):
                    result.update(reviewScope='unverified', result='unknown',
                                  note='Review scope unavailable or inconsistent; inspect the original review before relying on its verdict.')
            else:
                result.update(reviewScope='not applicable',
                              note=receipt.get('error') or 'Review attempt has no current completed verdict.')
        result['freshness'] = result['sourceApplicability']
        if binding.get('expiresAt') and timestamp(binding['expiresAt']) <= datetime.now(timezone.utc):
            result['freshness'] = 'expired'
        if receipt.get('status') == 'stale': result['freshness'] = 'stale'
        if result['result'] in ('passed', 'reviewed') and not result['observedAt']:
            result['freshness'] = 'unknown'
        if result['kind'] == 'legacy': result['note'] = 'Legacy receipt has no validated dependency contract; not journey verification.'
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        result.update(freshness='unknown', sourceApplicability='unknown', note=f'Receipt unavailable or invalid: {type(error).__name__}')
    return result


def collect_project(config):
    for key in ('id', 'name', 'engineeringRoot', 'recordsRoot'):
        if not isinstance(config.get(key), str) or not config[key]: raise ValueError(f'Missing {key}')
    root, records = Path(config['engineeringRoot']).resolve(), Path(config['recordsRoot']).resolve()
    if not root.is_dir() or not records.is_dir(): raise ValueError('Configured root unavailable')
    mapping_root = Path(config.get('mappingRoot', records)).resolve()
    mapping = read_json(confined(mapping_root, config['map'])) if config.get('map') else {}
    indexes = validate_map(mapping)
    result = {**mapping, 'id':config['id'], 'name':config['name'], 'revision':revision(root),
              'engineeringRoot':str(root), 'recordsRoot':str(records), 'collectedAt':now(), 'warnings':[], 'historical':False,
              'synthetic':bool(config.get('synthetic')), 'checkpoint':None}
    result['mappingStatus'] = mapping_status(mapping,config)
    if result['mappingStatus'] != 'current':
        result['warnings'].append('Architecture/task mapping ' + result['mappingStatus'] + '; reconcile against current project records.')
    if config.get('checkpoint'):
        path = confined(records, config['checkpoint'])
        if path.stat().st_size > MAX_BYTES: raise ValueError('Checkpoint too large')
        result['checkpoint'] = path.read_text()
    for component in result['components']:
        component['missingSources'] = [s for s in component.get('sources', []) if not confined(root, s).exists()]
        if component['missingSources']: result['warnings'].append(f'Mapping drift: {component["id"]} source missing')
    if not result['components']: result['warnings'].append('Architecture mapping not configured')
    mapped_paths = {b['receipt'] for b in mapping['evidence']}
    bindings = list(mapping['evidence'])
    for directory in config.get('receiptDirs', []):
        folder = confined(records, directory)
        for path in sorted(folder.glob('**/receipt.json')):
            if len(bindings) >= 1000: raise ValueError('Receipt limit exceeded; narrow receiptDirs')
            relative = str(path.relative_to(records))
            if relative not in mapped_paths:
                bindings.append({'id':'receipt:' + relative, 'receipt':relative, 'journeyIds':[], 'edgeIds':[], 'componentIds':[]})
    result['evidence'] = [receipt_evidence(config, b) for b in bindings]
    evidence = {e['id']:e for e in result['evidence']}
    result['unmappedUnits'] = []
    if config.get('units'):
        path = confined(records, config['units'])
        if path.exists():
            if path.stat().st_size > MAX_BYTES: raise ValueError('Work store exceeds limit')
            with path.open() as stream:
                units = list(csv.DictReader(stream, delimiter='\t'))
            for unit in units:
                task = indexes['tasks'].get(unit.get('id'))
                if task: task['state'] = unit.get('state', 'unknown'); task['recordRevision'] = unit.get('sha')
                else: result['unmappedUnits'].append(unit)
    visited, evaluating = {}, set()
    def gate_state(gate):
        satisfied, blocked = False, False
        if 'evidenceId' in gate:
            e = evidence[gate['evidenceId']]
            satisfied = e['result'] == 'passed' and e['freshness'] == 'current'
            if gate.get('journeyId'): satisfied &= e['kind'] == 'verification' and gate['journeyId'] in e.get('journeyIds', [])
            applicable = (not gate.get('journeyId') or (e['kind'] == 'verification' and gate['journeyId'] in e.get('journeyIds', []))) and (not gate.get('environment') or gate['environment'] == e['environment'])
            satisfied &= applicable
            blocked = applicable and e['freshness'] == 'current' and e['result'] in ('failed', 'changes requested', 'blocked')
            reason = f'{e["result"]}; {e["freshness"]}' if not satisfied else 'Current passing evidence'
            if gate.get('journeyId') and gate['journeyId'] not in e.get('journeyIds', []): reason = 'Evidence does not cover this journey'
            if gate.get('journeyId') and e['kind'] in ('review', 'legacy'): reason = 'Review or legacy evidence cannot qualify journey behavior'
            if e['kind'] == 'unknown': reason = e.get('note', 'No qualifying receipt recorded')
        else:
            dependency = milestone_state(gate['milestoneId'])
            satisfied = dependency == 'accepted'
            blocked = dependency == 'blocked'
            reason = 'Milestone accepted' if satisfied else 'Milestone not accepted'
        return {**gate, 'satisfied':bool(satisfied), 'status':'met' if satisfied else 'blocked' if blocked else 'unverified', 'reason':reason}
    def milestone_state(mid):
        if mid in visited: return visited[mid]
        if mid in evaluating: raise ValueError('Cyclic milestone gates')
        evaluating.add(mid)
        m = indexes['milestones'][mid]
        m['gates'] = [gate_state(g) for g in m['gates']]
        m['blockedTaskIds'] = [tid for tid in m.get('taskIds', []) if indexes['tasks'][tid].get('blockers') or indexes['tasks'][tid].get('state') == 'blocked']
        blocked = bool(m['blockedTaskIds']) or any(g['status'] == 'blocked' for g in m['gates'])
        ready = not blocked and bool(m['gates']) and all(g['satisfied'] for g in m['gates'])
        acceptance = m.get('acceptance') or {}
        accepted = (ready and isinstance(acceptance, dict) and bool(acceptance.get('actor')) and bool(acceptance.get('at'))
                    and acceptance.get('revision') == result['revision'] and hashes_match(root, acceptance.get('inputs')))
        if accepted: timestamp(acceptance['at'])
        m['status'] = 'accepted' if accepted else 'ready for acceptance' if ready else 'blocked' if blocked else 'unverified'
        visited[mid] = m['status']
        evaluating.remove(mid)
        return m['status']
    for m in result['milestones']: milestone_state(m['id'])
    result['releaseGates'] = [gate_state(g) for g in result['releaseGates']]
    result['releaseReady'] = bool(result['releaseGates']) and all(g['satisfied'] for g in result['releaseGates'])
    if result['mappingStatus'] != 'current': result['releaseReady'] = False
    return result


def collect_registry(path, previous=None):
    registry = read_json(path)
    configs = registry.get('projects')
    if not isinstance(configs, list) or not configs or len(configs) > 50: raise ValueError('Registry needs 1–50 projects')
    ids = [c.get('id') for c in configs]
    if any(not isinstance(i, str) or not ID.fullmatch(i) for i in ids) or len(set(ids)) != len(ids): raise ValueError('Invalid/duplicate project IDs')
    old = {p['id']:p for p in (previous or {}).get('projects', [])}
    projects = []
    for config in configs:
        try:
            projects.append(collect_project(config))
        except Exception as error:  # Isolate every ordinary collection failure; cancellation still propagates.
            fallback = {**old.get(config['id'], {}), 'id':config['id'], 'name':config.get('name', config['id']),
                        'historical':True, 'error':f'Collection failed: {type(error).__name__}: {error}'}
            projects.append(fallback)
    return {'collectedAt':now(), 'projects':projects}
