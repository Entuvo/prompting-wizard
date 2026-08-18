# Prompting Wizard

## Stop guessing what to type. Learn to direct AI.

You already use ChatGPT, Claude, Codex, or another AI assistant. Sometimes it gives you exactly what you need. Other times you rephrase the same request three times, accept an answer that is merely "good enough," or rewrite it yourself.

Prompting Wizard is a 30-day course that teaches you to get clear, useful, dependable results from AI. One guided lesson takes about 20 minutes and uses work you already do.

By day 30, you will be expert at prompting AI **for your work**: knowing what to ask for, how to make important information surface, how to judge the answer, and how to repair a prompt when it fails.

No coding knowledge is required.

![A professional uses the same AI with two different prompts: one produces a tangled, unfocused response while the other produces a clear, structured briefing.](assets/readme/prompting-before-after.webp)

*The same AI. Clearer direction.*

## The same AI. A better direction.

An AI model can produce thousands of reasonable answers to one request. Your prompt reduces those possibilities until the answer fits the job you actually need done.

**A casual prompt**

> Review this report and tell me what matters.

The AI has to guess what “review” means, who the answer is for, what “matters,” and what shape the response should take. It may produce a polished summary that still does not help you act.

**A deliberate prompt**

> Create a one-page briefing for a department head from this report. Identify the three decisions that need attention. For each decision, cite the supporting passage, explain the likely consequence of waiting, and end with one recommended next step. Separate facts from assumptions. Do not summarize sections that do not affect a decision.

Now the AI knows the audience, the deliverable, the evidence to extract, the quality bar, and what to leave out. The result is easier to trust and easier to use.

This is not about memorizing magic phrases. It is about learning which part of your instruction controls which part of the result.

## How the course works

First, Prompting Wizard assesses how you currently prompt. It also asks about the real tasks in your working life: perhaps planning a lesson, reviewing a contract, preparing a meeting, comparing proposals, writing a report, or making a difficult decision. Those tasks become your exercises for the rest of the course.

Every lesson follows a practical loop:

1. **Write** — You write a prompt for one of your real tasks.
2. **Run** — Your prompt runs exactly as you wrote it. It is not quietly improved first.
3. **Compare** — You see its result beside the result from a stronger version.
4. **Improve** — You identify the change that mattered and receive a score against a clear standard.

Watching both prompts run is important. You do not merely read advice about better prompting; you see how a small change affects the work produced.

The course adapts to your current level. If a skill remains weak, it returns later as a constraint inside another lesson. Review days use your own unsuccessful prompts, not generic examples.

## Your 30-day journey

### Diagnose

You begin with a short assessment. Prompting Wizard records your starting level, the skills you already control, and the recurring tasks you want AI to help with.

### Control

During the first half of the course, you learn eleven language levers. They help you control what should be made, what action the AI should take, which material is in scope, how good the answer must be, how references and conditions should work, how much to produce, and what deserves attention.

These are ordinary parts of language—nouns, verbs, descriptions, quantities, relationships—not technical incantations.

### Build

Next, you combine those foundations into reliable working prompts. You practise examples, output formats, multi-step tasks, context ordering, role instructions, negative constraints, self-review, evaluation criteria, and reusable prompt templates.

### Harden

Finally, you build a capstone prompt for one of your real tasks. You test it on a case it was not designed for, document what breaks, fix only the failures the test revealed, and run it again against written criteria.

![The Prompting Wizard journey moves through four milestones: assessing current skill, gaining precise control, assembling reliable prompts, and testing a finished prompt against different cases.](assets/readme/30-day-journey.webp)

*Thirty days. Four stages: Diagnose, Control, Build, and Harden.*

Skipping a day costs nothing. There is no backlog waiting for you; you simply continue with your next lesson.

## What changes by day 30

You will be able to:

- turn a vague request into a clearly defined deliverable;
- direct AI toward the relevant evidence instead of a generic summary;
- set scope, quantity, format, audience, and quality in language the model can follow;
- separate facts, assumptions, recommendations, and unknowns;
- recognize why a prompt failed instead of blaming the model or starting over;
- write criteria that make an answer checkable before you see it;
- test whether a prompt works beyond the example it was written for; and
- save reusable prompt templates for work you perform repeatedly.

The goal is not to become an expert in every AI model. It is to become the person who can reliably direct an AI assistant toward useful work—and explain why the result is good.

## Who this is for

Prompting Wizard is for anyone who already asks AI for help and wants more control over the result.

- A **teacher** can turn source material into a lesson plan with a defined age level, learning objective, and assessment.
- A **lawyer** can extract obligations, dates, exceptions, and unanswered questions from a document while keeping conclusions tied to the text.
- A **manager** can turn meeting notes into decisions, owners, deadlines, and follow-up questions.
- A **researcher or analyst** can separate evidence from inference and require traceable support.
- A **writer, consultant, or administrator** can create dependable drafts without spending the next hour correcting the AI's assumptions.

You bring the professional judgment. Prompting Wizard teaches you how to communicate that judgment to an AI assistant.

![An open professional toolkit holds reusable prompt cards for teaching, legal review, decision-making, meeting follow-up, and research.](assets/readme/professional-prompt-toolkit.webp)

*Different professions. One shared skill: turning judgment into clear direction for AI.*

## Start the course

The compare step works best in a coding agent that can run your prompt in a clean, isolated context. Claude Code, Codex, and similar agents can do that. In Claude.ai or ChatGPT chat, the course can still teach, but you will usually paste the practice prompt into a new chat yourself.

After any of the installs below, open a new chat and say: `Start Prompting Wizard.`

### Claude Code

```text
/plugin marketplace add Entuvo/prompting-wizard
/plugin install prompting-wizard@entuvo-prompting
```

Claude Code then updates the plugin through its own marketplace refresh. Do not replace files inside a managed install by hand.

### Codex

```text
codex plugin marketplace add Entuvo/prompting-wizard
```

Install Prompting Wizard from that marketplace in the Codex plugin UI, then start the course. Codex updates managed plugins; do not overwrite those files yourself.

### Any agent that can run the skills CLI

```text
npx skills add Entuvo/prompting-wizard
```

If the CLI asks which skill, choose `prompting-wizard`. Later, `npx skills update` refreshes installed skills.

### Other chat apps

If your assistant cannot install plugins or skills, paste this prompt. It will use a native install when one exists, otherwise load the course for this chat only.

```text
Install or load Prompting Wizard from:

https://github.com/Entuvo/prompting-wizard/tree/main/prompting-wizard

First determine which AI environment you are running in and which capabilities it actually provides. Use its native skill, plugin, marketplace, repository, or filesystem installation method when available.

If persistent installation is unavailable but you can read GitHub, load Prompting Wizard for this chat by reading AGENTS.md and then SKILL.md from that repository path. Follow those instructions directly.

Do not overwrite an existing installation without asking me. Never claim the skill is installed unless the host confirms it. Do not stop after explaining installation or creating a package. Once Prompting Wizard is available, start the Day 0 assessment.

If this environment cannot preserve files between chats, accept an attached PROGRESS.md and return the complete updated PROGRESS.md after every state change.

If you can neither install the skill nor read its files from GitHub, state exactly which capability is missing. Do not fabricate a successful installation.
```

Some hosts can keep Prompting Wizard between chats. Others can load it only for the current chat. The prompt requires the AI to say which outcome actually occurred.

A local `./install.sh` remains available for air-gapped or pre-listing installs. Prefer the host commands above when they work.

### Updates

Managed Claude Code, Codex, and skills-CLI installs update through those tools. For a copy loaded some other way, Prompting Wizard checks for a newer version at most once every seven days. When one is available, it shows the version and release-notes link, then asks before changing anything. Updates never replace `PROGRESS.md`, so your current day, scores, tasks, and lesson history stay intact.

To check immediately, tell the tutor: `Check Prompting Wizard for updates.`

## Before your first lesson

Your practice prompts run for real. When possible, the course runs them in a clean, isolated context so the lesson itself cannot influence the answer. If your tool cannot do that, Prompting Wizard asks you to run the prompt in a fresh chat and paste the result back.

Those runs may have the same file and network access as your current AI session. Start the course in a directory you are comfortable letting an AI inspect, and avoid a repository containing important uncommitted work.

The course never improves your prompt before the first run. Seeing what your own words produce is part of the lesson.

## Your progress belongs to you

Prompting Wizard keeps your state in a plain Markdown file named `PROGRESS.md` in the directory where you start the course. It records:

- your current level and day;
- your score on each of the eleven prompting levers;
- the real tasks used for your exercises; and
- a short log of what you learned each day.

You can read or edit the file whenever you want. You can redo a day, change your tasks, take a break, and return without a penalty.

## Open issues

See the [open issues](https://github.com/Entuvo/prompting-wizard/issues) for known bugs and planned improvements. If you find a problem or have an idea, [open a new issue](https://github.com/Entuvo/prompting-wizard/issues/new).

## Contributing

Lesson content lives in `prompting-wizard/days/`, and scoring criteria live in `prompting-wizard/rubrics.md`.

Before opening a pull request, run:

```bash
python3 tools/validate.py --complete
python3 tools/test_validate.py
python3 tools/test_package_release.py
python3 tools/test_install.py
```

If you change files under `prompting-wizard/` or `packaging/openai-plugin.json`, refresh the Codex plugin copies first:

```bash
python3 tools/sync_codex_plugin.py
```

The validator checks required section and tier order, duplicate sections, duplicate and non-empty tiers, the 200-word concept cap, rubric references in both directions, supported domain slots, canonical lever order in `assessment.md`, shipped absolute paths, the shipped `VERSION.md` semantic version, release-notes URL, matching `CHANGELOG.md` heading, and that `plugins/prompting-wizard/` is a real-file copy of the course. Changes to `prompting-wizard/days/`, `prompting-wizard/SKILL.md`, or `prompting-wizard/assessment.md` also require human review of their teaching intent.

## License

Prompting Wizard is available under the [MIT License](LICENSE).
