"""Portable Learning Cards. Pure reference logic; no capture, storage or network."""
import copy
import datetime
import json
import re
import uuid
from pathlib import Path
from typing import Optional

CATALOG = json.loads((Path(__file__).resolve().parents[1] / 'references/learning-catalog.json').read_text(encoding='utf-8'))
BY_SKILL = {entry['skill']: entry for entry in CATALOG}
MAX_BYTES = 1024 * 1024
TOP_FIELDS = {'schema_version', 'profile_id', 'revision', 'preferences', 'events', 'retracted_ids'}
EVENT_FIELDS = {'id', 'skill', 'date', 'source', 'task_id', 'task_family', 'activity', 'assistance',
                'context_quality', 'outcome', 'learner_action', 'reflection', 'comparison', 'confirmed'}
ENUMS = {'source': ('chatgpt', 'claude', 'codex', 'claude-code', 'manual'),
         'activity': ('introduction', 'practice', 'natural-use'),
         'assistance': ('example', 'hint', 'none', 'unknown'), 'context_quality': ('sufficient', 'partial'),
         'outcome': ('met', 'not-yet', 'uncertain', 'not-applicable'),
         'comparison': ('none', 'same-chat', 'fresh-context')}


def _size(text):
    try:
        return len(text.encode('utf-8'))
    except (AttributeError, UnicodeError) as exc:
        raise ValueError('Expected valid UTF-8 text') from exc


def _keys(value, fields):
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError('Missing or unknown fields')


def _uuid(value):
    try:
        if not isinstance(value, str) or str(uuid.UUID(value)) != value:
            raise ValueError('Expected canonical lowercase UUID')
    except (ValueError, AttributeError) as exc:
        raise ValueError('Expected canonical lowercase UUID') from exc


def _text(value, limit, byte_limit=False):
    if not isinstance(value, str) or not value.strip() or (_size(value) if byte_limit else len(value)) > limit:
        raise ValueError('Empty or oversized text')
    _size(value)


def _today(today):
    if type(today) is not datetime.date:
        raise ValueError('Supply an explicit local datetime.date')


def _canonical(card):
    result = copy.deepcopy(card)
    result['events'].sort(key=lambda e: (e['date'], e['id']))
    result['retracted_ids'].sort()
    return result


def validate_card(card: dict, today: datetime.date) -> dict:
    """Validate strictly and return a detached, canonical copy. Never trim history."""
    _today(today)
    _keys(card, TOP_FIELDS)
    if type(card['schema_version']) is not int or card['schema_version'] != 1:
        raise ValueError('Unsupported card schema')
    if type(card['revision']) is not int or card['revision'] < 0:
        raise ValueError('Invalid revision')
    _uuid(card['profile_id'])
    prefs = card['preferences']
    _keys(prefs, {'frequency', 'mode'})
    if prefs['frequency'] not in ('occasional', 'frequent', 'on-request') or prefs['mode'] != 'everyday':
        raise ValueError('Invalid preferences')
    for field in ('events', 'retracted_ids'):
        if not isinstance(card[field], list) or len(card[field]) > 1000:
            raise ValueError('Expected at most 1000 entries; preserve old card and archive deliberately')
    seen = set()
    for event in card['events']:
        _keys(event, EVENT_FIELDS)
        _uuid(event['id'])
        if event['id'] in seen:
            raise ValueError('Repeated event ID')
        seen.add(event['id'])
        if not isinstance(event['skill'], str) or event['skill'] not in BY_SKILL:
            raise ValueError('Unknown skill')
        if event['confirmed'] is not True:
            raise ValueError('Only explicitly accepted events belong in a card')
        for field, options in ENUMS.items():
            if not isinstance(event[field], str) or event[field] not in options:
                raise ValueError('Invalid ' + field)
        date = event['date']
        if not isinstance(date, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
            raise ValueError('Invalid event date')
        if datetime.date.fromisoformat(date) > today:
            raise ValueError('Future event date')
        _text(event['task_id'], 128)
        _text(event['task_family'], 120)
        _text(event['learner_action'], 1024, True)
        if event['reflection'] is not None:
            _text(event['reflection'], 1024, True)
    for identifier in card['retracted_ids']:
        _uuid(identifier)
        if identifier in seen:
            raise ValueError('Repeated or simultaneously active/retracted ID')
        seen.add(identifier)
    try:
        encoded = json.dumps(card, ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError, RecursionError) as exc:
        raise ValueError('Invalid JSON data') from exc
    if _size(encoded) > MAX_BYTES:
        raise ValueError('Card exceeds 1 MiB; preserve old card and archive deliberately')
    return _canonical(card)


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON key: ' + key)
        result[key] = value
    return result


def parse_card(text: str, today: datetime.date) -> dict:
    """Read the sole JSON fence; surrounding prose is non-authoritative data."""
    if not isinstance(text, str) or _size(text) > MAX_BYTES:
        raise ValueError('Card exceeds 1 MiB or is not text')
    openings = re.findall(r'^```json\s*$', text, re.M)
    blocks = re.findall(r'^```json[ \t]*\r?\n(.*?)^```[ \t]*\r?$', text, re.M | re.S)
    if len(openings) != 1 or len(blocks) != 1:
        raise ValueError('Expected exactly one complete JSON fence')
    try:
        card = json.loads(blocks[0], object_pairs_hook=_unique_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError('Non-finite JSON value')))
    except (ValueError, RecursionError) as exc:
        raise ValueError('Invalid card JSON: ' + str(exc)) from exc
    return validate_card(card, today)


def render_card(card: dict, today: datetime.date) -> str:
    card = validate_card(card, today)
    stages = '\n'.join('- ' + BY_SKILL[skill]['label'] + ': ' + state['stage'] +
                       ('; review needed' if state['needs_review'] else '')
                       for skill, state in summarize(card, today).items() if state['evidence_ids'])
    text = ('# Learning Card\n\n' + str(len(card['events'])) + ' accepted events. Frequency: ' +
            card['preferences']['frequency'] + '. Revision: ' + str(card['revision']) +
            '.\n\nRetain this complete file and supply it in the next chat. The JSON is authoritative; '
            'this summary is derived. This export does not replace earlier uploads.\n\n' +
            (stages + '\n\n' if stages else 'No demonstrated skills yet.\n\n') + '```json\n' +
            json.dumps(card, ensure_ascii=False, indent=2) + '\n```\n')
    if _size(text) > MAX_BYTES:
        raise ValueError('Rendered card exceeds 1 MiB; keep original and archive deliberately')
    return text


def merge_cards(current: dict, incoming: dict, today: datetime.date,
                preferences_from: Optional[str] = None) -> dict:
    a, b = validate_card(current, today), validate_card(incoming, today)
    if preferences_from not in (None, 'current', 'incoming'):
        raise ValueError('Choose current or incoming preferences')
    if a['profile_id'] != b['profile_id']:
        raise ValueError('Different profiles cannot be merged')
    if a['preferences'] != b['preferences'] and preferences_from is None:
        raise ValueError('Preferences conflict; explicitly choose current or incoming')
    events = {e['id']: e for e in a['events']}
    for event in b['events']:
        if event['id'] in events and events[event['id']] != event:
            raise ValueError('Conflicting content for event ' + event['id'])
        events[event['id']] = event
    result = copy.deepcopy(a)
    result['preferences'] = copy.deepcopy(b['preferences'] if preferences_from == 'incoming' else a['preferences'])
    result['retracted_ids'] = sorted(set(a['retracted_ids']) | set(b['retracted_ids']))
    result['events'] = [e for key, e in events.items() if key not in result['retracted_ids']]
    result = _canonical(result)
    if result != a:
        result['revision'] = max(a['revision'], b['revision']) + 1
    return validate_card(result, today)


def _performances(events):
    return [e for e in events if e['activity'] != 'introduction' and
            e['context_quality'] == 'sufficient' and e['outcome'] in ('met', 'not-yet')]


def _assistance(event, events):
    prior = {'hint' if e['activity'] == 'introduction' else e['assistance'] for e in events
             if e['task_id'] == event['task_id'] and e['date'] <= event['date']}
    if prior & {'hint', 'example'}:
        return 'helped'
    return 'unknown' if 'unknown' in prior else 'none'


def _independent(events):
    """Count a task once; previous/same-day assistance cannot be erased by retries."""
    result, tasks = [], set()
    for event in _performances(events):
        if (event['outcome'] == 'met' and _assistance(event, events) == 'none' and event['task_id'] not in tasks):
            result.append(event)
            tasks.add(event['task_id'])
    return result


def summarize(card: dict, today: datetime.date) -> dict:
    card = validate_card(card, today)
    summaries = {}
    for skill in BY_SKILL:
        events = [e for e in card['events'] if e['skill'] == skill]
        performances = _performances(events)
        met = [e for e in performances if e['outcome'] == 'met']
        independent = _independent(events)
        stage = 'unknown'
        if any(e['activity'] == 'introduction' and e['context_quality'] == 'sufficient' for e in events):
            stage = 'introduced'
        if any(_assistance(e, events) == 'unknown' for e in met):
            stage = 'practised-assistance-unknown'
        if any(_assistance(e, events) == 'helped' for e in met):
            stage = 'practised-with-help'
        if independent:
            stage = 'demonstrated-independently'
            first = independent[0]
            transfer = next((e for e in independent[1:] if e['task_family'] != first['task_family']), None)
            if transfer:
                stage = 'demonstrated-another-context'
                threshold = datetime.date.fromisoformat(transfer['date']) + datetime.timedelta(days=7)
                if any(datetime.date.fromisoformat(e['date']) >= threshold for e in independent):
                    stage = 'retained-later'
        latest = max((e['date'] for e in performances), default=None)
        summaries[skill] = {'stage': stage, 'evidence_ids': [e['id'] for e in events],
                            'last_independent_date': independent[-1]['date'] if independent else None,
                            'needs_review': any(e['date'] == latest and e['outcome'] == 'not-yet' for e in performances)}
    return summaries


def select_next(card: dict, relevant_skills: list, task_family: str,
                today: datetime.date) -> Optional[dict]:
    """Task relevance is supplied by the tutor, never inferred from keywords here."""
    card = validate_card(card, today)
    if (not isinstance(relevant_skills, list) or
            any(not isinstance(s, str) or s not in BY_SKILL for s in relevant_skills) or
            len(set(relevant_skills)) != len(relevant_skills)):
        raise ValueError('Supply distinct canonical skills in relevance order')
    _text(task_family, 120)
    states = summarize(card, today)
    candidates = []
    for relevance, skill in enumerate(relevant_skills):
        state = states[skill]
        stage, last = state['stage'], state['last_independent_date']
        if state['needs_review']:
            rank, activity, reason = 1, 'supported-practice', 'Latest applicable evidence includes a difficulty; revisit it in this task.'
        elif stage in ('introduced', 'practised-with-help', 'practised-assistance-unknown'):
            rank, activity, reason = 2, 'independent-practice', 'Try a new task without help; prior evidence does not yet show independent performance.'
        elif last and (today - datetime.date.fromisoformat(last)).days >= 7:
            rank, activity, reason = 3, 'revisit', 'Revisit a relevant skill after at least seven days; this interval is a pilot heuristic.'
        elif stage == 'unknown':
            rank, activity, reason = 4, 'introduction', 'This task offers a relevant skill with no sufficient learning evidence yet.'
        elif stage == 'demonstrated-independently' and task_family not in {
                e['task_family'] for e in _independent([e for e in card['events'] if e['skill'] == skill])}:
            rank, activity, reason = 5, 'transfer', 'Try this independently demonstrated skill in a different task family.'
        else:
            continue
        entry = BY_SKILL[skill]
        candidates.append((rank, relevance, {'skill': skill, 'label': entry['label'], 'lesson': entry['lesson'],
                                             'activity': activity, 'reason': reason, 'evidence_ids': state['evidence_ids']}))
    return min(candidates, key=lambda item: item[:2])[2] if candidates else None
