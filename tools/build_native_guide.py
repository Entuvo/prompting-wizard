#!/usr/bin/env python3
"""Build standalone native-app learning material from canonical sources."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build(root: Path, destination: Path) -> Path:
    skill = root / 'prompting-wizard'
    def read(name):
        path = skill / name
        parts = path.relative_to(root).parts
        if any((root / Path(*parts[:i])).is_symlink() for i in range(1, len(parts) + 1)):
            raise ValueError('Native guide source contains a symlink')
        return path.read_text(encoding='utf-8')
    instructions = read('references/native-instructions.txt')
    if len(instructions) > 1400:
        raise ValueError('Native instructions exceed 1400 characters')
    catalog = json.loads(read('references/learning-catalog.json'))
    rubrics = read('rubrics.md')
    headings = re.findall(r'^## (.+)$', rubrics, re.M)
    anchors = [h.lower().replace(' ', '-') for h in headings]
    if len(catalog) != 26 or len({e['skill'] for e in catalog}) != 26:
        raise ValueError('Incomplete or duplicate catalog')
    for entry in catalog:
        if anchors.count(entry['skill']) != 1 or entry['rubric'] != 'rubrics.md#' + entry['skill']:
            raise ValueError('Missing or duplicate rubric anchor')
        read(entry['lesson'])
    policy = read('references/learning-policy.md')
    card_format = read('references/learning-card.md')
    templates = re.findall(r'^```json\n(.*?)^```$', card_format, re.M | re.S)
    template = json.loads(templates[0])
    if template['events'] or template['retracted_ids']:
        raise ValueError('Card template must contain no learner evidence')
    version = read('VERSION.md').split('version: ', 1)[1].splitlines()[0]
    guide = ('# Prompting Wizard: everyday learning pilot\n\nCourse version: ' + version +
             '\n\nNo interview required. Complete work, practise one useful change, reflect, and retain your card. '
             'This guide supplies rules; it does not install an app or run background tracking. '
             'Native surface compatibility and learning efficacy require separate evaluation.\n\n'
             '## One-time account instructions\n\n```text\n' + instructions + '```\n\n' + policy + '\n' + card_format +
             '\n## Skill map\n\n' + '\n'.join('- [' + e['label'] + '](#' + e['skill'] + ') — ' + e['skill'] +
             '; optional course lesson ' + e['lesson'][5:7] for e in catalog) + '\n\n' + rubrics)
    # Canonical course links, if introduced later, must be resolved deliberately.
    if re.search(r'\]\((?!#|https://)[^)]+\)', guide):
        raise ValueError('Unresolved relative link in native guide')
    card_text = ('# Learning Card\n\nEmpty pilot template. Ask your coach to replace the synthetic profile UUID '
                 'once at first use; retain it across apps. Keep the latest complete file.\n\n```json\n' +
                 json.dumps(template, indent=2) + '\n```\n')
    destination.mkdir(parents=True, exist_ok=True)
    path = destination / 'prompting-wizard-native-guide.md'
    path.write_text(guide, encoding='utf-8')
    (destination / 'prompting-wizard-learning-card.md').write_text(card_text, encoding='utf-8')
    return path


if __name__ == '__main__':
    print(build(ROOT, ROOT / 'dist'))
