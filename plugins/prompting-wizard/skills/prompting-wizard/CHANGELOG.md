# Prompting Wizard release notes

## 1.4.0 — 2026-10-14

- Added `pw history` for Claude Code and Codex. It is an explicit, one-shot read of your recent sessions through each host's documented SDK, with two consents: one before reading and one before scoring. It finds the prompts that cost you turns and turns them into an aggregate baseline, a casebook of your own prompts with single-edit rewrites, and lesson suggestions.
- Course: an informational `History` log line records lever means from past work. It is kept apart from the Day 0 baseline. Lessons can show one of your own cases after the Before / After, and day 30 shows past-work scores as a separate column.
- `pw history` also reads a ChatGPT or Claude data export (`--host chatgpt|claude --file EXPORT`). ChatGPT prompts you edited in place are kept and scored with what the edit added.
- Everyday plugin 0.2.0: on request, reviews an uploaded export inside ChatGPT or Claude. It covers up to 30 recent conversations and reports the top gaps and three of your own cases, with nothing stored.
- Learning Card: up to three paraphrased `natural-use` candidates, appended only when accepted.
- History runs are local, owner-only, honor coaching exclusions and expire after 30 days. Transcript files are never parsed, and the learner's config files are never written.

## 1.3.0 — 2026-10-11

- Added an everyday teaching pilot: optional interview, work first, Practice / Example / Lesson / Later, learner prediction and opt-in exploratory retry.
- Added a portable Learning Card with strict validation, conflict-safe merging, retractions, evidence stages and task-relevant next opportunities. Independent evidence requires an uncued task; guided changes remain assisted.
- Added compact native-app instructions, a standalone guide/card build, and `pw learn` / `pw learning` routing. Existing course progress, baselines and local capture controls remain separate.
- Added synthetic teaching scenarios and offline evaluation receipts. Native ChatGPT/Claude web, desktop and mobile walkthroughs remain unverified; human learning efficacy is not established.
- Investigated remote connectors for future automatic continuity. This pilot requires manual card transfer and has no shared service or automatic cross-app synchronization.

## 1.2.2 — 2026-10-11

- Reworked examples in Lessons 2, 6, 9, 10, 20 and 28 around meeting agendas, notes, factual corrections, spreadsheets and document reviews, preserving each lesson's teaching point.
- Varied the assessment task examples and clarified the Verb and Conjunction rubric wording.

## 1.2.1 — 2026-10-11

- Describe the course as 30 self-paced lessons everywhere: plugin and marketplace descriptions, the skill, coaching notes and the README no longer say "30-day", "a lever a day" or "20-minute lessons".

## 1.2.0 — 2026-10-09

- Require source blocks in source-dependent practice and inspect actual few-shot failure evidence; clarify the attention-marker and phrasal-verb examples.

- Reworked Days 1, 4, 5, 8, 12, 13, 16, 17 and 23 around varied professional tasks; schemas now use tables/forms and tool workflows use documents/spreadsheets, with no programming prerequisite.

- Added the pw command skill: course navigation, feedback and collection controls, saved examples and model guidance, with conversational arguments.
- Both plugin packages now use the shared two-skill layout; original course invocation remains available. Codex uses skill mentions; standalone Claude supports /pw.
- Explicit pw commands are excluded from capture; paused profiles retain control context, and status reports workspace policy and shared-progress presence.

- Added optional local coaching runtime, shared learner profile, after-result and lesson-only modes, and scoped hook installation.
- Added bounded evidence retention, learner controls, atomic reviewed lessons and preserved Day 0 progress imports.
- Added reviewed model guidance with exact identities and explicit unknown-model fallback.
- Corrected quantity limits, task-dependent context ordering and evidence-based failure diagnosis; constrained exercises no longer overwrite independent proficiency.
- Kept portable course archives hook-free. See repository COACHING.md for measured host compatibility and remaining limits.

## 1.1.0 — 2026-08-11

- Added native Claude plugin and marketplace metadata plus OpenAI plugin release packaging.
- Added an account-skill ZIP and a safe local installer for pre-listing fallbacks.
- Added stateless `PROGRESS.md` attachment and download handling for regular chat hosts.
- Changed managed installations to use their host's update mechanism.
- Reworked the README around product-native installation and an honest direct-load fallback.

## 1.0.0 — 2026-08-10

- Added a confirmation-only weekly update check with release notes.
- Added one-paste installation guidance for Codex and Claude Code.
- Hardened lesson scoring, clean-context execution, progress recovery, and structural validation.
