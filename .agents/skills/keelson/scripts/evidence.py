#!/usr/bin/env python3
"""Run scoped checks, validate source evidence, and summarize attempt measurements."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import tempfile
from pathlib import Path
import subprocess
import time


def save(path, value):
    path = Path(path)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(json.dumps(value, indent=2) + '\n')
            stream.flush()
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


def save_output(output, result, stdout_name='stdout.txt'):
    """Keep raw complete or partial bytes, including incomplete UTF-8."""
    for name, data in [(stdout_name, result.stdout), ('stderr.txt', result.stderr)]:
        (output / name).write_bytes(data.encode('utf-8') if isinstance(data, str) else data or b'')


def contract(path):
    value = json.loads(Path(path).read_text())
    if not isinstance(value, dict) or set(value) != {'unit', 'check', 'inputs', 'command', 'context'}:
        raise ValueError('Contract requires unit, check, inputs, command and context')
    for key in ['unit', 'check', 'context']:
        if not isinstance(value[key], str) or not value[key].strip():
            raise ValueError(f'Nonempty {key} required')
    for key in ['inputs', 'command']:
        if not isinstance(value[key], list) or not value[key] or not all(isinstance(x, str) and x for x in value[key]):
            raise ValueError(f'Nonempty string list required: {key}')
    return value


def inputs(project, spec):
    files = {}
    for pattern in spec['inputs']:
        if Path(pattern).is_absolute() or '..' in Path(pattern).parts:
            raise ValueError(f'Input escapes project: {pattern}')
        matches = list(project.glob(pattern))
        if not matches:
            raise ValueError(f'Input matched nothing: {pattern}')
        for path in matches:
            resolved = path.resolve()
            if not resolved.is_relative_to(project) or path.is_symlink():
                raise ValueError(f'Input symlink or escape: {path}')
            if path.is_file():
                files[str(path.relative_to(project))] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not files:
        raise ValueError('Inputs contain no files')
    return dict(sorted(files.items()))


def require_current(project, receipt_path):
    """Validate successful source evidence; external runtime state still needs inspection."""
    project = Path(project).resolve()
    receipt = json.loads(Path(receipt_path).read_text())
    if not isinstance(receipt, dict) or not {'contract_path', 'contract', 'inputs'}.issubset(receipt):
        raise ValueError('Incomplete verification receipt')
    if receipt.get('stage') != 'verification' or receipt.get('status') != 'passed' or receipt.get('project') != str(project):
        raise ValueError('Verification failed, incomplete, or belongs to another project')
    current = contract(receipt['contract_path'])
    if current != receipt['contract'] or inputs(project, current) != receipt['inputs']:
        raise ValueError('Verification inputs or dependency contract changed; rerun affected check')
    return receipt


def run_check(project, spec_path, output, timeout=300, *, reason="Initial verification"):
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("Verification reason required")
    project, spec_path, output = Path(project).resolve(), Path(spec_path).resolve(), Path(output).absolute()
    if not project.is_dir() or timeout <= 0:
        raise ValueError('Project directory and positive timeout required')
    spec = contract(spec_path)
    before = inputs(project, spec)
    if output.exists() or output.is_symlink():
        raise FileExistsError(f'Attempt already exists: {output}')
    output.mkdir(parents=True)
    receipt = {'stage':'verification', 'status':'running', 'unit':spec['unit'], 'check':spec['check'],
               'reason':reason, 'project':str(project), 'contract_path':str(spec_path), 'contract':spec, 'inputs':before,
               'started_at':datetime.now(timezone.utc).isoformat(), 'reported_cost_usd':None}
    save(output / 'receipt.json', receipt)
    started = time.monotonic()
    try:
        result = subprocess.run(spec['command'], cwd=project, capture_output=True, timeout=timeout)
        save_output(output, result)
        receipt.update(exit_code=result.returncode, status='passed' if result.returncode == 0 else 'failed')
        if contract(spec_path) != spec or inputs(project, spec) != before:
            receipt['status'] = 'stale'
    except subprocess.TimeoutExpired as error:
        save_output(output, error)
        receipt.update(status='failed', timed_out=True, error=str(error))
    except (OSError, ValueError) as error:
        receipt.update(status='failed', error=str(error))
    receipt.update(elapsed_seconds=round(time.monotonic() - started, 3), finished_at=datetime.now(timezone.utc).isoformat())
    save(output / 'receipt.json', receipt)
    return receipt


def summarize(paths):
    receipts = [json.loads(path.read_text()) for path in sorted({Path(p).resolve() for p in paths})]
    costs = [r.get('reported_cost_usd') for r in receipts]
    durations = [r.get('elapsed_seconds') for r in receipts]
    return {'attempts':len(receipts), 'units':sorted({r.get('unit') or 'unassigned' for r in receipts}),
            'statuses':{s:sum(r.get('status', 'unknown') == s for r in receipts) for s in sorted({r.get('status', 'unknown') for r in receipts})},
            'reported_cost_usd':sum(c for c in costs if c is not None),
            'unknown_cost_attempts':costs.count(None),
            'summed_elapsed_seconds':sum(d for d in durations if d is not None),
            'unknown_duration_attempts':durations.count(None),
            'by_stage':{stage:{'attempts':sum(r.get('stage', 'unknown') == stage for r in receipts),
                              'summed_elapsed_seconds':sum(r.get('elapsed_seconds') or 0 for r in receipts if r.get('stage', 'unknown') == stage),
                              'unknown_duration_attempts':sum(r.get('elapsed_seconds') is None for r in receipts if r.get('stage', 'unknown') == stage)}
                        for stage in sorted({r.get('stage', 'unknown') for r in receipts})},
            'user_wait_seconds':None, 'external_wait_seconds':None, 'unrecorded_lead_cost_usd':None,
            'limits':['Selected receipts only; summed execution is not wall time.',
                      'Provider-reported costs only; unrecorded lead work, waiting and other model costs remain unknown.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    run = sub.add_parser('run')
    run.add_argument('--project', required=True, type=Path)
    run.add_argument('--contract', required=True, type=Path)
    run.add_argument('--output', required=True, type=Path)
    run.add_argument('--timeout', type=int, default=300)
    run.add_argument('--reason', default='Initial verification')
    status = sub.add_parser('status')
    status.add_argument('--project', required=True, type=Path)
    status.add_argument('receipt', type=Path)
    summary = sub.add_parser('summary')
    summary.add_argument('receipts', type=Path, nargs='+')
    args = parser.parse_args()
    try:
        if args.action == 'run':
            result = run_check(args.project, args.contract, args.output, args.timeout, reason=args.reason)
        elif args.action == 'status':
            result = require_current(args.project, args.receipt)
        else:
            result = summarize(args.receipts)
        print(json.dumps(result, indent=2))
        return 0 if result.get('status', 'passed') == 'passed' else 1
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
