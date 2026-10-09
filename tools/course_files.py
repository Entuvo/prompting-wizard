"""Explicit distribution allowlist. Learner data and local hooks never ship."""
TOP_FILES = ('SKILL.md','AGENTS.md','assessment.md','rubrics.md','VERSION.md','CHANGELOG.md')
EXTRA_FILES = (
    'scripts/store.py','scripts/wizard.py','references/coaching.md','references/commands.md',
    'references/model-guidance/manifest.json',
    'references/model-guidance/claude-long-context.md',
    'references/model-guidance/astra-task-boundaries.md',
)
COURSE_FILES = TOP_FILES + tuple(f'days/{day:02d}.md' for day in range(1,31)) + EXTRA_FILES
