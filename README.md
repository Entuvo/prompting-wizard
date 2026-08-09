# Prompting Wizard

A 30-day course that turns you into a deliberate prompter. Twenty minutes a day. It assesses you first, then teaches using the tasks you actually do.

Each day covers one lever or one technique — starting with the parts of speech, because each one controls a different dimension of a prompt — then builds up to structure, systems, and a capstone. You write a prompt, it runs verbatim, you see the output, then you see a stronger version's output beside it.

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

For the run step to happen automatically, Codex needs to expose an isolated-agent dispatch tool (for example `spawn_agent`). The course detects whether one is actually available to it rather than checking any config setting — Codex can expose one without a matching entry in `~/.codex/config.toml`.

Without one available the course still works — it asks you to run each prompt in a fresh chat and paste the output back.

Your prompts are run for real. An agent with this session's file and network access executes them, in whatever directory you started from, before anyone has improved them — that is the whole point of the course. Start it from a directory you would not mind an agent poking around in, and not from a repository with uncommitted work in it.

Codex discovers `AGENTS.md` from the current directory, which is why the instructions above start you inside the checkout — but that also makes the checkout every dispatched agent's workspace. If you are contributing to this repository rather than taking the course, run the course from a scratch directory instead and accept that Codex will not auto-discover `AGENTS.md` there.

## How it works

Your progress lives in `PROGRESS.md` in whatever directory you start from. It holds your level, your day number, your score on each of the 11 levers, and the real tasks the exercises are built from. It is plain markdown — edit it if you want to redo a day or change your tasks.

Skipping days costs nothing. There is no backlog.

## Contributing

Lesson content lives in `prompting-wizard/days/`, scoring criteria in `prompting-wizard/rubrics.md`. Run `python3 tools/validate.py --complete` before opening a PR. It checks that every day has the required sections, that every rubric reference resolves, and that no shipped file contains an absolute path.

Day files carry instructions addressed to the tutor as well as text read aloud to the learner. Changes to `prompting-wizard/days/`, `prompting-wizard/SKILL.md`, or `prompting-wizard/assessment.md` need human review of intent, not just a green `tools/validate.py` run.
