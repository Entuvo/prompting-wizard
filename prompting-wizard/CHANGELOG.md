# Prompting Wizard release notes

## 1.5.0 — 2026-10-16

- **One plugin.** The course, the `pw` shortcut and everyday learning (formerly the separate "Prompting Wizard — Everyday" plugin) now ship as one plugin, `prompting-wizard`. Releases attach two downloads: `prompting-wizard-claude.zip` (Claude app, Cowork, Claude Code) and `prompting-wizard-openai.zip` (ChatGPT and Codex), each with its manifest at the archive root. The old course zips, the standalone skill zip and the separate `prompting-wizard-teacher` plugin are retired. If you installed it, remove it and install `prompting-wizard`.
- The OpenAI download carries the portable Agent Plugins `plugin.json` plus the legacy `.codex-plugin/plugin.json` for the Codex CLI. All manifests share one version.
- The README, website and plugin setup now lead with a single "your app → file → install" table. The manual-setup guide and empty card remain attached for apps without plugins.
- Skill descriptions fit claude.ai's 200-character limit, since all three skills now upload to the Claude app.

## 1.4.4 — 2026-10-15

- Fixed: a `History` log line no longer breaks lesson commits with local coaching's shared progress. A lesson commit may now include `- History — …` lines beside its one lesson line.
- Fixed: `install.sh` installs the `pw` shortcut skill next to the course, so `/pw` and `$pw` work after a standalone install. The install check, and the update check in `SKILL.md`, now verify every shipped file under `references/` and `scripts/`.
- Website: lesson 22's comparison now shows the system-prompt split; lessons 8, 24 and 26 highlight every change; the lesson-video count is accurate (18 of 30); lesson footers name all four hosts; the one-paste setup prompt matches the README.
- Copy: `pw history` descriptions state the same-provider rule; lesson 29 and the lesson loop drop calendar and minute wording; history scoring documents why two catalog skills are not gap keys; manifests use the site's brand colour. Everyday plugin 0.2.3.

## 1.4.3 — 2026-10-14

- Each provider's history is reviewed only by that provider's hosts. Claude Code and the Claude app review only Claude exports, and Codex and ChatGPT review only ChatGPT exports; another provider's export is declined without review. In the apps, an upload still reaches that app's provider, so upload only that app's own export. Coding hosts confirm an export's source before running anything, and `history.py` refuses another provider's history under Codex or Claude Code. The scan output also carries the exact consent question. Everyday plugin 0.2.2.

## 1.4.2 — 2026-10-14

- `pw history` now ends a scan with a direct yes/no question before scoring, instead of only describing the consent.
- Everyday plugin 0.2.1: the in-app export review names at most three skills in total, and its card records never quote the export.

## 1.4.1 — 2026-10-14

- `pw history` now always ends a scan with the scoring disclosure and asks for a second consent, even when the learner has already asked to stop before scoring.
- `history.py` runs under `python3 -I` (isolated mode).
- Added `tools/e2e_hosts.py`, an end-to-end runner for Claude Code, Codex, and Claude/ChatGPT app simulations through their APIs.

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
