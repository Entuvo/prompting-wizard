#!/usr/bin/env python3
"""Disposable synthetic host probe. Never installs user hooks or reads transcripts."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

FIELDS = ('hook_event_name', 'session_id', 'turn_id', 'cwd', 'model', 'source',
          'prompt', 'last_assistant_message', 'stop_hook_active', 'agent_id',
          'agent_type', 'from_model', 'to_model', 'requested_model')


def record(directory):
    raw = sys.stdin.buffer.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024:
        return
    event = json.loads(raw)
    if not isinstance(event, dict):
        return
    if os.environ.get('PROMPTING_WIZARD_EXPERIMENT') == '1':
        return
    selected = {k: event[k] for k in FIELDS if k in event}
    # Temporary synthetic sessions only. Do not point this at real work.
    with (directory / 'events.jsonl').open('a') as stream:
        stream.write(json.dumps(selected) + '\n')
    control = directory / 'control.json'
    if control.exists():
        config = json.loads(control.read_text())
        if 'runtime_module' in config:
            sys.path.insert(0, config['runtime_module'])
            from store import Store
            from wizard import handle_event
            print(json.dumps(handle_event(config['host'], event, Store(Path(config['runtime_root'])))))
            return
    name = event.get('hook_event_name')
    if name == 'SessionStart':
        print(json.dumps({'hookSpecificOutput': {'hookEventName': name,
              'additionalContext': 'Synthetic probe session token: WIZARD_PROBE_TOKEN'}}))
    if name == 'Stop' and not event.get('stop_hook_active'):
        control = directory / 'control.json'
        if control.exists():
            if json.loads(control.read_text()).get('disabled'):
                return
            print(json.dumps({'decision': 'block', 'reason': json.loads(control.read_text())['reason']}))
            return
        print(json.dumps({'decision': 'block', 'reason':
            'Synthetic probe: reply WIZARD_PROBE_FEEDBACK only. Do not repeat the original answer.'}))


def prepare(host):
    directory = Path(tempfile.mkdtemp(prefix='wizard-host-probe-'))
    command = shlex.join([sys.executable, str(Path(__file__).resolve()), 'record', str(directory)])
    events = ['SessionStart', 'UserPromptSubmit', 'Stop', 'SessionEnd']
    config = {'hooks': {name: [{'hooks': [{'type': 'command', 'command': command}]}]
                        for name in events}}
    target = directory / ('.codex/hooks.json' if host == 'codex' else 'settings.json')
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(config, indent=2) + '\n')
    subprocess.run(['git', 'init', '-q', str(directory)], check=True)
    print(directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'record'])
    parser.add_argument('target')
    args = parser.parse_args()
    if args.action == 'record':
        record(Path(args.target))
    elif args.target in ('claude', 'codex'):
        prepare(args.target)
    else:
        parser.error('target must be claude or codex')
