# Design: learning from past work history

Status: approved for implementation · Branch: `feat/history-analysis` · Drafted 14 October 2026

## Problem

Prompting Wizard teaches with the learner's own tasks, but today it only sees work from the moment coaching is enabled (and only in enabled workspaces) or tasks the learner names during assessment. Most learners already have months of AI-assistant history that shows exactly where their prompts cost them: the follow-up that says "no, I meant…", the interrupt, the third restatement of a rule. That evidence is the best teaching material available and is currently unused.

## Goal

An explicit, one-shot `pw history` action that reads the learner's past sessions from a supported host, finds the prompts that cost them turns, and turns them into:

1. a **baseline**: costly-turn rates and per-lever scores, re-measurable later;
2. a **casebook**: the learner's own costly prompts, each with the correction that exposed the gap and a single-edit rewrite;
3. **course inputs**: proposed starting lever scores, a lesson order weighted by cost, and real cases for `{{TASK}}` and Before/After;
4. **Learning Card candidates**: paraphrased `natural-use` events the learner may accept;
5. a **standing-rules draft**: rules the learner kept restating, offered as text for them to place in CLAUDE.md / AGENTS.md themselves.

## Non-goals (v1)

- ChatGPT and Claude app exports (v2; see Host matrix).
- Background or recurring reading. Every run is learner-initiated.
- Any Entuvo service, upload, or telemetry.
- Writing to CLAUDE.md, AGENTS.md, settings or memory files.
- Replacing the assessment. History can inform it; the learner confirms.

## Evidence from the maintainer pilot

A prototype ran on one maintainer's Claude Code history (2026-05-30 → 2026-10-14). Aggregates only; no excerpts leave that machine.

| Finding | Value | Design consequence |
|---|---|---|
| Raw user turns that were hand-typed prompts | ~1,234 of 34k user records | Most records are tool results, notifications, commands. Filtering is the first job. |
| Replays and non-human prompts removed | 228 of 1,234 (18%) | Resumed/forked sessions replay history under new ids; harness and health-check prompts look human. Dedupe and template detection are required, not optional. |
| Prompts with a clean outcome | 74% | Most prompts are fine; the signal is concentrated. |
| Costly rate: task openers vs replies to Claude's options | 39% vs 13% | Score openers in full; score steers only for gaps. |
| Costly rate: planning tasks vs ops tasks | 41% vs 16% | Task type belongs in the episode schema. |
| Lowest lever means (openers, 1–5) | adjective 1.5, adverb 1.5, noun 2.8, preposition 2.9 | History produces a usable lever profile in course terms. |
| Frustrated turns traced to an unwritten standing rule | 21 of 35 | Some fixes are configuration, not prompting. Hence the standing-rules draft. |
| Regex-only correction detection | found 66 corrections; model scoring found 228 costly turns | Heuristics seed; model scoring decides. |
| Scoring cost | ~1.6M subagent tokens for 1,234 prompts (18 parallel batches) | Show an estimate and default to a bounded sample. |
| Fair side-by-side reruns | 2 of 20 cases | Most work prompts depend on repo or live state. Comparisons stay optional and must name confounders. |

The pilot's key insight: **the learner's next message is a free label.** "No, I meant X" names what the prompt lacked, so the minimal rewrite is the original plus X.

## Decision (ADR-0001)

**Read host history only through documented interfaces, once, on explicit request, and keep raw excerpts local.**

- **Claude Code**: the Claude Agent SDK documents `list_sessions()` and `get_session_messages(session_id)` (Python) / `listSessions()` / `getSessionMessages()` (TypeScript). Use those. Do not parse `~/.claude/projects/*.jsonl` directly. The pilot did, and it needed undocumented record-type knowledge (`isMeta`, `isSidechain`, `entrypoint`, command wrappers).
- **Codex**: the Codex Python SDK documents `Codex.thread_list(cwd=, source_kinds=, limit=, cursor=, ...)`, and the app-server documents `thread/read` and `thread/items/list` (paginated thread history). Use those, with `source_kinds` excluding non-interactive threads. Rollout files at `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` are defined only in source (`codex-rs/rollout`); do not read them. Confirmed via Context7 against `openai/codex` main, 14 October 2026. Pin and recheck the SDK version at implementation.
- This keeps COACHING.md's contributor rule, "Never parse undocumented private transcripts", intact. No exception is needed.

Alternatives rejected:
- *Parse the local JSONL files.* Works today, breaks silently on format change, and contradicts a stated project rule.
- *Collect history via hooks going forward only.* This is already the coaching runtime. It cannot reach the months of evidence that already exist.

## Pipeline

```
host adapter ──► episodes ──► filter ──► heuristic labels ──► model scoring ──► outputs
(documented API)  (schema)   (dedupe,     (outcome hint)      (host agent,        (local files,
                              non-human)                       SCORING spec)       card candidates)
```

1. **Adapter** (one per host): yields turns in order per session: user text, assistant text, tool-call count, output tokens, timestamp, workspace path, stable message id.
2. **Episode builder**: one episode per human prompt, plus everything until the next human prompt and the next prompt's text.
3. **Filter**:
   - drop tool results, host notifications, local-command echoes, slash commands without arguments, and compaction summaries;
   - dedupe by message id, then by identical text within 5 minutes, or an identical zero-output copy (replays);
   - mark as non-human any text repeated verbatim across at least 5 sessions, temp-directory workspaces, and single-word health checks.

   Generic rules only. The pilot's maintainer-specific patterns must not ship.
4. **Heuristic labels**: interrupt marker, correction/frustration regex, short acknowledgement. These label the episode as `outcome_hint` and are never scored.
5. **Model scoring**: the current host's model applies `history-scoring.md` (from the pilot's SCORING spec). Keys are the `learning-catalog.json` skill ids, so scores land in course terms. Batches of about 70 episodes. Parallel where the host can dispatch isolated agents, sequential otherwise.
6. **Outputs**: see below. Generated by a stdlib script from validated score files.

Scripts stay stdlib-only. The SDK is needed only by the adapter. **Open:** whether to require `pip install claude-agent-sdk` for `pw history`, or to call the TypeScript SDK through `npx`.

## Data contracts

**Episode** (local only): `id, host, session, turn, ts, workspace, prompt (≤6,000 chars, secrets masked), prompt_chars, has_image, command, reply_first (≤400), reply_last (≤600), tool_calls, out_tokens, next_prompt (≤400), outcome_hint, source (human|automated), kind (prompt|ack)`.

**Score** (local only): `id, task_type, role (opener|steer|answer|paste|meta), outcome (clean|clarification|redirected|corrected|frustrated|interrupted|unclear), gaps[≤3]{key, score, evidence≤25w}, missing_info≤30w, levers{11 keys → 1–5|null} (openers only), teach 0–3, exemplar, note`.

Masking happens before anything is written. It covers API keys and tokens, `key=value` secrets, long hex strings and email addresses.

## Outputs and where they live

| Output | Contains raw excerpts? | Location | Retention |
|---|---|---|---|
| episodes, scores | yes | `ROOT/history/<run-id>/` (the coaching data root, never the skill dir or workspace) | 30 days, same as raw observations; `delete --history` |
| casebook pages | yes (verbatim prompts) | same | same; the learner can copy out what they keep |
| BASELINE | no (aggregates) | same, plus summary shown in chat | until deleted |
| proposed lever scores | no | shown for confirmation, then into `PROGRESS.md` as a history-sourced baseline line | per course rules |
| Learning Card candidates | no (paraphrased findings) | proposed in chat; appended only if accepted | per card rules |
| standing-rules draft | short quotes | shown in chat or written to ROOT | not written to any config file |

The Day 0 baseline line is never edited. A history baseline is a separate, labelled log line (`Day 0 — history — n prompts, date range — baseline …`). Day 30's comparison can then use either baseline or both.

## Consent flow

1. The learner runs `pw history`.
2. The tutor states the scope before any reading:
   - which host;
   - the date range (default: last 90 days);
   - how many sessions and workspaces;
   - that excluded workspaces are skipped;
   - an estimated prompt count and token cost (default sample cap: 300 prompts);
   - that excerpts will pass through the current provider for scoring.
3. Explicit yes. Then the adapter reads and builds episodes and shows counts. Then a second yes before scoring. Scoring is the step that costs quota and sends excerpts to the model.
4. Results arrive as a short chat summary plus local file paths. Nothing becomes course or card state without learner confirmation.

## Host matrix

| Host | v1 | Reading | Scoring | Notes |
|---|---|---|---|---|
| Claude Code | yes | Agent SDK session APIs | parallel isolated subagents | pilot-proven |
| Codex | yes | Codex SDK `thread_list` + app-server `thread/items/list` | `spawn_agent` or sequential | otherwise v1.1 |
| ChatGPT / Claude apps | v2 | learner uploads the provider's data export | in-chat, sampled (~50 openers) | output is card candidates only, since there is no local storage for a casebook |

## Changes by file (planned)

- `prompting-wizard/scripts/history.py`: episode builder, filter, heuristics, merge/validate, baseline and casebook rendering (from the pilot's `mine.py`, `score.py`, `build.py`).
- `prompting-wizard/scripts/history_hosts.py`: SDK-backed readers for Claude Code and Codex.
- `prompting-wizard/references/history-scoring.md` and `history-casebook.md`: specs the host model follows.
- `prompting-wizard/references/commands.md`: `history` routing; `wizard.py`: `history` and `delete --history` controls.
- `SKILL.md` / `assessment.md`: optional history baseline line, and case substitution into lessons.
- `PRIVACY.md`, `COACHING.md`, `CHANGELOG.md`: the new one-shot read, retention, and what reaches the provider.
- `tools/test_history.py` plus `tools/fixtures/history/`: synthetic sessions only.

## Testing

- Adapter tests against synthetic SDK message objects: commands, interrupts, replays, and subagent/sidechain messages excluded.
- Filter and heuristic unit tests: every pilot pitfall becomes a fixture (replay with a new id, harness prompt, health check, temp-dir workspace).
- Score validation: reject unknown keys, bad enums, missing ids, and duplicate ids.
- Label agreement: a hand-labelled synthetic set of about 60 episodes, with the outcome agreement threshold set before the first run.
- `tools/leak-check.sh` over fixtures and generated docs. No real history in the repo.

## Milestones

1. This doc approved, and the ADR decision recorded.
2. ~~Confirm the Codex thread-read API and the SDK-dependency choice.~~ Done.
3. `history.py` plus the Claude Code adapter plus fixtures and tests.
4. Scoring spec plus the `pw history` command and consent flow.
5. Outputs wired into the course baseline, lesson cases and card candidates.
6. Codex adapter. Then privacy and docs updates, then release notes.

## Coverage finding (14 October 2026)

`get_session_messages` returns the session's current conversation chain, not every message ever written. On the pilot history, the SDK path found 761 of the pilot's 992 distinct hand-typed prompts. All 305 missing prompts came from 5 long sessions with compaction or heavy rewinding; one session's file holds 16,616 user records and the SDK returns 410 messages. 15 of the pilot's 51 strongest teaching cases were in those lost branches. Abandoned branches are often where a prompt went wrong, so this loss is not neutral.

The rule stands: documented interfaces only. v1 reports coverage honestly ("read the current conversation of N sessions; earlier branches of compacted or rewound sessions are not available") and does not fall back to parsing files. Revisit if the SDK adds a full-history option.

## Resolved defaults (maintainer, 14 October 2026)

1. **SDK dependency**: acceptable for `pw history` only. The course and coaching runtime stay stdlib-only. A missing SDK gives a clear install message, not a fallback to file parsing.
2. **Codex**: in v1. The documented thread list/read APIs were confirmed (see the Decision section).
3. **Retention**: casebook pages and episodes follow the 30-day raw-evidence rule. The learner can copy out anything they want to keep.
4. **Assessment**: a history baseline adds to the assessment and never replaces it. Assessment still runs; the history line is logged next to Day 0.
5. **Default sample**: last 90 days, capped at 300 prompts, and the learner can widen either. The token estimate is shown before scoring.
