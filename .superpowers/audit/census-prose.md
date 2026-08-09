# Prose consistency census

Read-only census. Nothing in the working tree, index, HEAD, or branch state was modified to produce this report. Scope: `prompting-wizard/days/01.md`–`30.md`, `prompting-wizard/SKILL.md`, `prompting-wizard/assessment.md`, `prompting-wizard/rubrics.md`, `README.md` (also consulted `prompting-wizard/AGENTS.md` and `tools/validate.py` for cross-file claims).

`tools/validate.py --complete` was run (read-only) as a sanity check: it reports `ok` — required sections present, rubric anchors resolve, no absolute paths. That validator does not check any of the prose-consistency dimensions below, which is the gap this census fills.

## Closing self-test table

Dominant formulation: **"Here is the test: `<instruction>`"** (colon, one sentence) — 23/30 days (Days 8–30).

| Day | Closing formulation (verbatim) | Conforms? |
|---|---|---|
| 1 | days/01.md:9 "Here is the test. Read your prompt and ask what physical thing lands when it finishes." | No — period, not colon |
| 2 | days/02.md:11 "Here is the test. Cover everything in your prompt except the verb." | No — period, not colon |
| 3 | days/03.md:11 "Test it this way: for each adjective in your prompt, ask what output it would make you reject." | No — different opener |
| 4 | days/04.md:11 "Test it by asking: if two competent people followed this manner word, would their outputs be roughly the same length and thoroughness?" | No — different opener |
| 5 | days/05.md:11 "Test it by asking three questions of your prompt: in what, for whom, without what." | No — different opener |
| 6 | days/06.md:11 "Test it by removing each lever in turn." | No — different opener |
| 7 | (none) | No — no closing self-test sentence anywhere in `## Concept` |
| 8 | days/08.md:11 "Here is the test: for each it/this/that/these in your prompt, point at the exact word or quoted block it refers to." | Yes |
| 9 | days/09.md:13 "Here is the test: find every \"and\", \"if\", or \"unless\" in your prompt." | Yes |
| 10 | days/10.md:11 "Here is the test: put the/a/each/every/any in front of every noun in your prompt and ask which swap would change what gets done." | Yes |
| 11 | days/11.md:13 "Here is the test: for each quantity in your prompt, ask whether you could check it with a count, not a feeling." | Yes |
| 12 | days/12.md:11 "Here is the test: find the sentence you'd be angriest to see ignored." | Yes |
| 13 | days/13.md:11 "Here is the test: swap the particle for a plausible alternative." | Yes |
| 14 | days/14.md:11 "Here is the test: score a prompt you'd call finished against each of the eleven rubrics in turn." | Yes |
| 15 | days/15.md:11 "Here is the test: name your prompt's role, then list two things the output contains because of it that it wouldn't contain otherwise." | Yes |
| 16 | days/16.md:11 "Here is the test: could either example be swapped for a different instance of the same pattern without changing what the model would learn?" | Yes |
| 17 | days/17.md:18 "Here is the test: could you write a script that rejects a malformed output without you reading it first?" | Yes |
| 18 | days/18.md:11 "Here is the test: cut a chained prompt of yours at every \"and then,\" and check whether each half's input is verbatim the other half's output — not a paraphrase, the actual text." | Yes |
| 19 | days/19.md:11 "Here is the test: list what the answer to {{TASK}} actually depends on, then check your named steps against that list." | Yes |
| 20 | days/20.md:11 "Here is the test: for each exclusion in your prompt, ask whether you've watched the model actually do that." | Yes |
| 21 | days/21.md:11 "Here is the test: before you run the reordered version, predict what changes about the output." | Yes |
| 22 | days/22.md:11 "Here is the test: read your system prompt line by line and ask, would this be false on some future turn?" | Yes |
| 23 | days/23.md:11 "Here is the test: read your done-condition and ask how a model could satisfy it without doing the real work." | Yes |
| 24 | days/24.md:11 "Here is the test: describe, in one sentence, what your output would look like if it failed your check." | Yes |
| 25 | days/25.md:11 "Here is the test: show your criteria to someone who hasn't seen the output." | Yes |
| 26 | days/26.md:11 "Here is the test: cut a third of your context, rerun, and compare outputs side by side." | Yes |
| 27 | days/27.md:11 "Here is the test: name the lever before you touch the prompt." | Yes |
| 28 | days/28.md:11 "Here is the test: open one saved prompt." | Yes |
| 29 | days/29.md:11 "Here is the test: run your prompt against two cases as different from each other as your recurring task allows." | Yes |
| 30 | days/30.md:11 "Here is the test: run your day-29 prompt on a case you didn't build it for." | Yes |

## Concept paragraph counts

Counted mechanically (blank-line-delimited blocks in `## Concept`, code fences counted as one block). Dominant: **4**.

| Day | Paragraphs | Note |
|---|---|---|
| 1 | 4 | |
| 2 | 4 | |
| 3 | 4 | |
| 4 | 4 | |
| 5 | 4 | |
| 6 | 4 | |
| 7 | 3 | outlier — also the day with no closing self-test |
| 8 | 4 | |
| 9 | 5 | outlier |
| 10 | 4 | |
| 11 | 5 | outlier |
| 12 | 4 | |
| 13 | 4 | |
| 14 | 4 | |
| 15 | 4 | |
| 16 | 4 | |
| 17 | 4 prose + 1 fenced code block (5 blocks total) | only day with a code fence inside `## Concept` |
| 18 | 4 | |
| 19 | 4 | |
| 20 | 4 | |
| 21 | 4 | |
| 22 | 4 | |
| 23 | 4 | |
| 24 | 4 | |
| 25 | 4 | |
| 26 | 4 | |
| 27 | 4 | |
| 28 | 4 | |
| 29 | 4 | |
| 30 | 4 | |

Distribution: 4 paragraphs — 26 days (1–6, 8, 10, 12–16, 18–30). 5 paragraphs — 2 days (9, 11). 3 paragraphs — 1 day (7). 4 prose + embedded code fence — 1 day (17).

## Title format

All 30 titles follow `# Day N — Term: description` — arabic numeral (never spelled out), one em dash `—`, first word after the dash capitalised. No numeral/spelled-out deviations found; no capitalisation deviations found. One structural deviation:

- Day 6 (days/06.md:1) `# Day 6 — Composing the first five` has no colon-delimited "Term: description" — every other day (all 29 others, including the two other review-style days 7 and 14: `Review: rewrite your worst prompt`, `Review: all eleven levers`) uses `Term: description`.

## Findings

### DEFECT-P01 — Two days close with "Here is the test." (period) instead of the colon idiom — severity: medium
days/01.md:9, days/02.md:11. Dominant pattern: "Here is the test: `<instruction>`" (colon), used verbatim on 23/30 days (8–30). Days 1 and 2 instead write "Here is the test." as a full stop, followed by a separate imperative sentence. Minimal fix: replace the period with a colon and fold the following clause into the same sentence, matching Day 8 onward.

### DEFECT-P02 — Four days use an entirely different self-test opener ("Test it...") — severity: medium
days/03.md:11 "Test it this way: for each adjective...", days/04.md:11 "Test it by asking: if two competent people...", days/05.md:11 "Test it by asking three questions of your prompt: in what, for whom, without what.", days/06.md:11 "Test it by removing each lever in turn." None of the four use "Here is the test" at all — the phrase the other 24 days (1–2 partially, 8–30 fully) converge on. Minimal fix: reword each opener to "Here is the test: ...".

### DEFECT-P03 — Day 7 has no closing self-test at all — severity: medium
days/07.md, `## Concept` (lines 5–9). The section ends on "...every clause, if removed, visibly weakens the result." with no "Here is the test" / "Test it..." sentence anywhere. Every other day in the course closes `## Concept` with some form of the idiom. Minimal fix: add a closing self-test sentence naming a check the learner can run against their own worst prompt.

### DEFECT-P04 — Two days run one paragraph longer than the dominant Concept length — severity: low
days/09.md (5 paragraphs: lines 5, 7, 9, 11, 13) and days/11.md (5 paragraphs: lines 5, 7, 9, 11, 13), against the 4-paragraph pattern used by 26/30 days. Minimal fix: merge the extra paragraph (line 11 in each) into an adjacent one, or accept as an intentional exception and note it.

### DEFECT-P05 — Day 7 runs one paragraph short of the dominant Concept length — severity: low
days/07.md, `## Concept` has 3 paragraphs (lines 5, 7, 9) against the 4-paragraph dominant pattern. Related to DEFECT-P03 — the missing 4th paragraph is precisely the missing self-test line.

### DEFECT-P06 — Day 6's title lacks the "Term: description" colon structure every other day uses — severity: medium
days/06.md:1 `# Day 6 — Composing the first five`. All other 29 titles (including the other "review"-flavoured days, 7 and 14) follow `Day N — Term: description`. Minimal fix: retitle to e.g. `# Day 6 — Composition: the first five together`.

### DEFECT-P07 — Day 17 uses different dummy vocabulary for the same illustrative schema — severity: medium
days/17.md:11-12 (in `## Concept`): `{"item": "example item one", ...}` / `{"item": "example item two", ...}`. days/17.md:32-33 (in `## Before / After`): `{"item": "sample entry one", ...}` / `{"item": "sample entry two", ...}`. The two JSON snippets are otherwise identical in shape and are meant to illustrate the same point ("dummy values shown to fix the contract"), but the placeholder strings drift between "example item" and "sample entry" within the same day. Minimal fix: use one placeholder vocabulary (e.g. always "sample entry one/two") in both snippets.

### DEFECT-P08 — Six days replace the standard Exercise opening line with a tutor-direction preamble — severity: medium
Dominant line, verbatim across 24/30 days (1–6, 8–13, 15–20, 22–26, 28): "Pick one of your recurring tasks. Write a single prompt for it." Deviating days: days/07.md:23, days/14.md:25, days/21.md:31, days/27.md:25, days/29.md:25, days/30.md:25 — each opens `## Exercise` instead with a paragraph of second-person-to-the-tutor direction ("Before presenting a tier, read `## Levers`...", "Ask the learner for a real failed prompt...", etc.). This is thematically justified (these are review/capstone days that need PROGRESS.md-driven setup) but is a visible seam against the otherwise identical opening line used everywhere else. No fix required if intentional; otherwise, minimal fix is to keep the standard line and move tutor direction into a separate sentence after it.

### DEFECT-P09 — Five days present `## Before / After` as tutor-facing prose instead of a quoted prompt pair — severity: medium
days/07.md:13-19, days/14.md:15-21, days/27.md:15-21, days/29.md:15-21, days/30.md:15-21. Dominant pattern (19/30 regular lesson days, e.g. days/01.md:15-21): `**Before**` / blank line / `> <quoted prompt>` / `**After**` / blank line / `> <quoted prompt>`. These five days instead put unquoted paragraphs of tutor instruction under the `**Before**` / `**After**` bold labels — no prompt is quoted at all. (Day 21, also a review day, keeps the standard quoted-blockquote form here — only its Exercise preamble deviates; see DEFECT-P08.) Minimal fix, if uniformity is wanted: none available without changing the pedagogical design of these days — otherwise, document the exception explicitly.

### DEFECT-P10 — `## Before / After` uses four different sub-formats for structured content — severity: low
- Dominant: single `**Before**` quote + single `**After**` quote (e.g. days/01.md:13-23) — ~19 days.
- days/16.md:19-24: extra labelled lines ("Boundary case:", "Failure case:") folded inline inside one continuous blockquote via `>` continuation.
- days/17.md:26-37 and days/18.md:19-33: labelled sub-prompts ("Prompt 1:", "Prompt 2 — input is Prompt 1's output, pasted verbatim:") as plain paragraph text, each introducing its own separate blockquote.
- days/22.md:19-27: same plain-label-then-separate-blockquote technique, labels "System prompt:" / "Per-turn ask:".
- days/17.md:28-36: a fenced code block nested inside a blockquote (lines prefixed with `>` even on the ``` fences) — the only such instance in the course.
No two of these techniques are identical even though all four serve the same purpose (showing multiple related prompt artifacts inside one `After`). Minimal fix: standardise on the plain-label-then-blockquote form (Day 18/22's pattern) everywhere multiple artifacts need to be shown.

### DEFECT-P11 — Day 17 formats the same code sample two different ways within one day — severity: low
days/17.md:9-14 shows the JSON schema as a bare fenced code block (no blockquote). days/17.md:30-35 shows the same shape of schema as a fenced code block nested inside a `>` blockquote. Minimal fix: pick one presentation and use it in both places.

### DEFECT-P12 — Five days address the tutor in third person inside the Exercise tiers, instead of the learner in second person — severity: medium
Dominant pattern, all 25 non-meta days: tiers address the learner directly and imperatively, e.g. days/01.md:31 "Write a prompt for {{TASK}} whose deliverable is unambiguous..." Deviating days — tiers instead instruct an implied "tutor" about "the learner":
- days/14.md:29 "Ask the learner for a real prompt for one of their `## Tasks` entries. Have them go lever by lever..."
- days/21.md:39 "Ask the learner to reorder their prompt into task, material, constraints..."
- days/27.md:29 "Have the learner go lever by lever through the failed prompt, out loud..."
- days/29.md:29 "Ask the learner to write a first pass at the production prompt for their named task..."
- days/30.md:29 "Ask the learner to write three checks for the day-29 prompt..."
This third-person "tutor" voice never appears inside any `## Concept` section (confirmed across all 30 days) — it is confined to `## Before / After` and `## Exercise` on these five days plus Day 7 (which uses a comparable third-person Before/After but keeps its Exercise tiers in second person — days/07.md:27 "State which one of the five levers..."). SKILL.md:26 explains this is deliberate ("Some passages are written to you rather than to the learner... That text is direction, not script"), which argues for low severity for the *design*, but the register still visibly diverges from the other 25 days' tier voice, which is what this audit is asked to flag.

### DEFECT-P13 — README.md claims "Each day covers one lever," which the course's own terminology contradicts — severity: medium
README.md:5 "Each day covers one lever — starting with the parts of speech, because each one controls a different dimension of a prompt — then builds up to structure, systems, and a capstone." But rubrics.md:3 states "One rubric per lever and per technique," and days/27.md:7 explicitly distinguishes "one of the eleven levers or one of the techniques from the last two weeks." Only 11 of the 30 days teach a new "lever" (parts of speech: Days 1–5, 8–13); Days 15–28 teach "techniques" (role framing, few-shot examples, output schemas, etc. — a term rubrics.md and days/27, days/29 use explicitly to distinguish them from levers); Days 6, 7, 14, 21 are review days; Days 29–30 are the capstone. README.md's own second sentence ("then builds up to structure, systems, and a capstone") actually contradicts its first ("each day covers one lever") in the same paragraph. Minimal fix: reword README.md:5 to something like "Each day covers one lever or technique."

### DEFECT-P14 — "Constraint" is used for three distinct, unrelated concepts without disambiguation — severity: low
(1) General usage throughout — any prompt boundary, e.g. days/05.md:1 "Preposition: scope and relation." (2) SKILL.md:30's "secondary constraint" mechanic — an extra weak lever bolted onto an exercise ("add exactly one of them as a named secondary constraint"). (3) Day 20's technique name, "Negative constraints" (days/20.md:1), meaning a stated forbidden failure mode. All three are legitimate but the bare word "constraint" carries all three meanings depending on context; no cross-reference disambiguates SKILL.md's "secondary constraint" from Day 20's "negative constraint" even though a low-scoring "negative constraints" lever could plausibly be assigned as a "secondary constraint" on another day, doubling the term inside one exercise. No hits found where this actually causes ambiguity in the text as written — flagged for completeness, not because it currently misleads a reader.

### DEFECT-P15 — rubrics.md and assessment.md order "Pronoun" before "Preposition," reversed from the day-teaching sequence — severity: medium
rubrics.md:63 `## Pronoun` precedes rubrics.md:77 `## Preposition`. assessment.md:66 lists `pronoun: 2    preposition: 4` in that order in the illustrative `PROGRESS.md` `## Levers` block. But in `days/`, Preposition is taught on Day 5 and Pronoun on Day 8 — Preposition comes first. Every other lever in both reference files follows the day-teaching order (noun, verb, adjective, adverb, [pronoun/preposition swapped], conjunction, determiner, numeral, interjection, particle). Minimal fix: reorder both files' Pronoun/Preposition entries to Preposition-then-Pronoun.

### DEFECT-P16 — Two single-lever days skip the fill-in-the-blank Novice template used by comparable days — severity: low
Days 1, 2, 3, 4, 5, 9, 10, 11, 13 (9 of the 11 single-lever days) give the Novice tier a `________`-blank template to complete, e.g. days/01.md:29-33. Days 8 (days/08.md:29-31, Pronoun) and 12 (days/12.md:29-31, Interjection) — structurally identical single-lever lesson days — instead open Novice with a free-form instruction and no blank template. Minimal fix: add a blank-template line to Days 8 and 12's Novice tier, or note why they're exempt.

### DEFECT-P17 — "Review day" is used inconsistently between day titles and SKILL.md's formal designation — severity: low
Day titles containing the word "Review": days/07.md:1 `Review: rewrite your worst prompt`, days/14.md:1 `Review: all eleven levers`. SKILL.md:59 designates a different pair as "review days": "Days 14 and 21 are review days: draw their material from the three lowest-scoring levers." Day 21's title (days/21.md:1, `Context ordering: task, material, constraints`) does not say "Review," and Day 7 — which does say "Review" in its title and behaves like one (bring-your-own-failed-prompt, no seed prompt) — is not in SKILL.md's formal "review days" list. The word "review" is therefore used for two overlapping but non-identical sets of days across the title text and the operational rule.

## British spelling check

Exhaustive grep across `prompting-wizard/` and `README.md` for American-only spelling forms (`-ize`/`-yze` family, `color/behavior/favorite/center/labor/neighbor/honor/humor/rumor/vapor/fiber/theater/traveling/canceled/modeling/gray/defense/offense/license/catalog/dialog/program/plow/mold/curb/tire/skeptic/practice-as-verb/judgment/aluminum/sulfur`, etc.) found **zero American spellings**. The course consistently uses British forms where the two dialects diverge: "practise"/"practised" as the verb (SKILL.md:3, SKILL.md:57, days/06.md:5) alongside "practice" correctly reserved for the noun (assessment.md:52 "needs practice, not first principles"); "recognise"/"recognises" (assessment.md:52, days/07.md:5, days/30.md:33); "summarising" (days/02.md:5); "generalises" (days/30.md:5,7); "memorised" (days/30.md:7); "exercising" (days/14.md:25, days/21.md:31); "judgement" (rubrics.md:127,129,309, days/11.md:43, days/19.md:23); "behaviour" (rubrics.md:268,269, days/22.md:7); "neighbour" (days/12.md:5). No file:line list of American spellings is given because none were found.

## Terminology

- **Lever** — consistently means one of the 11 parts-of-speech dimensions (Days 1–5, 8–13). No stray usage found referring to anything else.
- **Technique** — consistently means the non-lever, non-review content taught Days 15–28 (role framing, few-shot examples, output schemas, task decomposition, reasoning scaffolds, negative constraints, context ordering, system prompts, agent and tool prompting, self-critique loops, writing evals, token economy, failure diagnosis, prompt library). rubrics.md:3 and days/27.md:7 explicitly name both terms and distinguish them; README.md does not use the word "technique" at all and instead claims every day is a "lever" (DEFECT-P13).
- **Anchor** — consistently means the descriptive text tied to a specific 1–5 rubric score (rubrics.md's "Anchor" column; days/29.md:9,21,37 and days/30.md:9 use "anchor N" as shorthand for "the rubric's score-N description," a natural extension of the same meaning, not a clash).
- **Artifact** — consistently means the deliverable/noun the prompt asks for (rubrics.md:9, days/01.md, days/06.md:23). No conflicting usage found.
- **Slot** — consistently means a named variable part of a saved/reusable prompt template (days/28.md, rubrics.md:351-355), with one adjacent-but-distinct usage at days/22.md:7 ("the per-turn slot") that is a looser, non-technical use of the same word for "position in the prompt" rather than "named variable" — worth noting but not flagged as a defect since context disambiguates.
- **Constraint** — overloaded across three senses; see DEFECT-P14.
- No case was found of two different terms being used for what should be one concept.

## Cross-file consistency (README.md vs SKILL.md / assessment.md / rubrics.md / days/)

Checked claims:
- "20 minutes a day," "assesses you first, then teaches using the tasks you actually do," "write a prompt, it runs verbatim, you see the output, then a stronger version beside it," Codex `spawn_agent` / `~/.codex/config.toml` detection language, `PROGRESS.md` contents description, "skipping days costs nothing," and the `tools/validate.py --complete` contributing instructions all match the implementation in SKILL.md / assessment.md and were verified against the actual files (`tools/validate.py` exists and returns `ok`). No defects found on these points.
- "Each day covers one lever" does not match the lever/technique/review/capstone structure actually implemented — DEFECT-P13.
- rubrics.md/assessment.md lever ordering vs. days/ teaching order — DEFECT-P15.
- SKILL.md's "review days" designation vs. day titles containing "Review" — DEFECT-P17.

## Second person and register

`## Concept` sections are second-person-to-the-learner throughout all 30 days (verified: no "the learner" or "the tutor" phrasing appears in any `## Concept` section). The third-person "tutor" register is confined to `## Before / After` and `## Exercise` on Days 7, 14, 21, 27, 29, 30 — see DEFECT-P09 and DEFECT-P12. No hedging language ("perhaps," "maybe," "somewhat," "it seems") was found anywhere in `days/`. No marketing/praise adjectives ("powerful," "seamless," "world-class," "cutting-edge," etc.) were found in the course's own voice — the only hits for "world-class" are the two intentionally-bad example prompts being critiqued (days/15.md:5,17,23 and assessment.md:21, both "You are a world-class expert..."), which is correct use as an anti-pattern illustration, not a register slip.

## Structural consistency (not requested but mechanically verified in passing)

All 30 days share identical heading skeletons — `## Concept`, `## Before / After`, `## Exercise` (with `### Novice`, `### Working`, `### Advanced`), `## Rubric` — confirmed via `grep -n '^##'` on every file. Only Day 30 has an additional `## Completion` section, which matches SKILL.md:38's conditional step ("If the day file has a `## Completion` section..."). No heading-level or heading-text deviations found.
