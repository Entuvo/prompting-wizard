# Prompting Wizard

A 30-day course that turns you into a deliberate prompter. Twenty minutes a day. It assesses you first, then teaches using the tasks you actually do.

Each day covers one lever — starting with the parts of speech, because each one controls a different dimension of a prompt — then builds up to structure, systems, and a capstone. You write a prompt, it runs verbatim, you see the output, then you see a stronger version's output beside it.

## Install

**Claude Code**

```bash
git clone https://github.com/Entuvo/prompting-wizard.git
cp -r prompting-wizard/prompting-wizard ~/.claude/skills/
```

Then ask: "start the prompting course".

**Codex**

```bash
git clone https://github.com/Entuvo/prompting-wizard.git
```

Then, from the inner `prompting-wizard` directory, ask: "read AGENTS.md and start the prompting course".

For the run step to happen automatically, enable multi-agent support in `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

Without it the course still works — it asks you to run each prompt in a fresh chat and paste the output back.

## How it works

Your progress lives in `PROGRESS.md` in whatever directory you start from. It holds your level, your day number, your score on each of the 11 levers, and the real tasks the exercises are built from. It is plain markdown — edit it if you want to redo a day or change your tasks.

Skipping days costs nothing. There is no backlog.

## Contributing

Lesson content lives in `prompting-wizard/days/`, scoring criteria in `prompting-wizard/rubrics.md`. Run `python3 tools/validate.py --complete` before opening a PR. It checks that every day has the required sections, that every rubric reference resolves, and that no shipped file contains an absolute path.
