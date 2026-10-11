#!/usr/bin/env python3
"""Audit coverage of supplied, explicitly reviewed teaching transcripts. No model calls."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path


def _text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Expected nonempty text')


def evaluate(cases, transcripts):
    if not isinstance(cases, list) or not cases:
        raise ValueError('Cases must be a nonempty array')
    expected = {}
    for case in cases:
        if not isinstance(case, dict) or not {'id','input','expectations'} <= case.keys():
            raise ValueError('Malformed case')
        _text(case['id']); _text(case['input'])
        criteria = case['expectations']
        if not isinstance(criteria, list) or not criteria:
            raise ValueError('Case must declare expectations')
        for criterion in criteria: _text(criterion)
        if case['id'] in expected or len(set(criteria)) != len(criteria):
            raise ValueError('Duplicate case or criterion')
        expected[case['id']] = criteria
    if (not isinstance(transcripts, dict) or not isinstance(transcripts.get('runs'), list) or
            type(transcripts.get('request_all_pass', False)) is not bool):
        raise ValueError('Malformed transcript document')
    results = {}
    for run in transcripts['runs']:
        fields = {'case_id','surface','model','run_date','steps','reviewer','observations'}
        if not isinstance(run, dict) or not fields <= run.keys():
            raise ValueError('Malformed run')
        for field in ('case_id','surface','model','run_date','reviewer'): _text(run[field])
        identifier = run['case_id']
        if identifier not in expected or identifier in results:
            raise ValueError('Unknown or duplicate case ID')
        date = datetime.date.fromisoformat(run['run_date'])
        if date.isoformat() != run['run_date']:
            raise ValueError('Use YYYY-MM-DD')
        steps = run['steps']
        if not isinstance(steps, list) or len(steps) < 2:
            raise ValueError('Supply observed user and receiver steps')
        roles = set()
        for step in steps:
            if not isinstance(step, dict) or step.get('role') not in ('user','assistant','system','tool'):
                raise ValueError('Malformed transcript step')
            _text(step.get('content')); roles.add(step['role'])
        if not {'user','assistant'} <= roles:
            raise ValueError('No observed user/assistant boundary')
        observations = run['observations']
        if not isinstance(observations, dict) or set(observations) != set(expected[identifier]):
            raise ValueError('Every criterion needs explicit review')
        for rating in observations.values():
            if not isinstance(rating, dict) or rating.get('assessment') not in ('pass','fail','unsupported'):
                raise ValueError('Unreviewed semantic rating')
            _text(rating.get('reason'))
        results[identifier] = {'surface': run['surface'], 'model': run['model'], 'reviewer': run['reviewer'],
                               'pass': all(r['assessment'] == 'pass' for r in observations.values())}
    unrun = [key for key in expected if key not in results]
    all_pass = not unrun and all(result['pass'] for result in results.values())
    if transcripts.get('request_all_pass') and not all_pass:
        raise ValueError('Cannot claim all-pass with failed, unsupported or unrun cases')
    return {'all_pass': all_pass, 'unrun': unrun, 'results': results,
            'limits': 'Audits supplied reviewer ratings, not conversational semantics. A synthetic run does not establish native compatibility or human learning efficacy.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', required=True, type=Path)
    parser.add_argument('--transcripts', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.resolve() in (args.cases.resolve(), args.transcripts.resolve()):
        parser.error('Output must not overwrite input evidence')
    try:
        case_bytes, transcript_bytes = args.cases.read_bytes(), args.transcripts.read_bytes()
        receipt = evaluate(json.loads(case_bytes), json.loads(transcript_bytes))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    receipt['input_sha256'] = {'cases': hashlib.sha256(case_bytes).hexdigest(),
                              'transcripts': hashlib.sha256(transcript_bytes).hexdigest()}
    args.output.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return 0 if receipt['all_pass'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
