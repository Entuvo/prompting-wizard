# State contract and logic census

Scope: `prompting-wizard/SKILL.md`, `prompting-wizard/assessment.md`, `prompting-wizard/days/01.md`–`30.md`, `prompting-wizard/rubrics.md`. Read-only census. Nothing was modified.

All 30 day files exist and every `rubrics.md#…` anchor referenced by a day resolves to a real `##` heading. The eleven lever keys in `assessment.md`'s `## Levers` template match the eleven lever rubrics in `rubrics.md` exactly. `tools/validate.py` checks day sections, rubric anchors and absolute paths — it does not check the `PROGRESS.md` contract at all, so nothing below is caught mechanically.

## PROGRESS.md lifecycle table

| Field/section | Written by | Read by | Round-trips? | Notes |
|---|---|---|---|---|
| `level` | `assessment.md:61` (value derived at `assessment.md:46-52`) — **only writer in the repo** | `SKILL.md:16`, `SKILL.md:30` | **No** — write-once, read 30× | Selects the exercise tier every session for 30 days. No day file mentions `level`. See DEFECT-S01. |
| `current_day` | `assessment.md:62` (=1); `SKILL.md:20` (increment); `days/30.md:45` (=31) | `SKILL.md:16`, `:17`, `:18`; `days/30.md:45` | Yes | Two writers on day 30, in an order the loop makes ambiguous. See DEFECT-S07, S10. Lower bound and integrality unguarded — S18. |
| `## Levers` (11 scores) | `assessment.md:64-67`; `SKILL.md:20` (only for levers the day scored) | `SKILL.md:16`, `:30`; `days/14.md:17`,`:25`; `days/21.md:31`; `days/30.md:45` | Partially | Scored days 1–14 only (days 1–5 one each, days 6–7 five each, days 8–13 one each, day 14 all eleven). Days 15–30 score techniques, so after day 14 only levers ≤2 can move, via the secondary constraint. See S13, S14. |
| `## Tasks` (3–5 entries) | `assessment.md:42`, `:69-72` — **only writer** | `SKILL.md:16`, `:24`, `:28`; `days/14.md:17`,`:29`; `days/21.md:35`; `days/28.md:42` | **No** — write-once | Count never validated on read; `days/28.md:42` needs three entries. See S15. Substitution rule differs between `SKILL.md:24` and `:28` — S12. |
| `## Log` — Day 0 baseline line | `assessment.md:75`, mandated `assessment.md:78` | `days/30.md:45` | Yes, when it exists | Format differs from per-day lines (`level working, diagnosis 6/10 — baseline noun 4, …`). Never documented in `SKILL.md`'s `## Log line format` section (`SKILL.md:61-67`). Not produced by the rebuild path at `SKILL.md:13`. See S06, S09. |
| `## Log` — per-day lines | `SKILL.md:20` per format at `SKILL.md:63-67` | `SKILL.md:30`; `days/27.md:17`,`:25`; `days/30.md:17`,`:25` | Partially | `## Log` is absent from the required-field list at `SKILL.md:14` and from the read list at `SKILL.md:16`, yet three consumers depend on it. See S06. |
| `## Log` field 2 (topic) | `SKILL.md:66` example only (`interjection`) | `days/27.md:17` (calls it "the task"), `days/30.md:17` | **Format mismatch** | Undefined for days 6/7/14 (multi-lever) and for all technique days. `days/27.md:17` describes it as the task; it is not. See S19. |
| `## Log` field 3 (`self N, rubric N`) | `SKILL.md:20`, `:34`, `:36` | `days/27.md:17` ("lowest rubric score") | **Format mismatch** | One `rubric N` slot; days 6, 7, 14 produce 5, 5 and 11 rubric scores. See S08. Ties and the day-0 line's stray numbers unhandled — S09. |
| `## Log` — which lever was used as secondary constraint | **Nothing writes it** | `SKILL.md:30` ("break ties by whichever you have used least recently, which you can see in `## Log`"; "Do not use the same lever on consecutive sessions") | **Read, never written** | See DEFECT-S02. |
| `## Log` — day-29 task | `days/29.md:25` instructs it be written into the day-29 line | `days/30.md:17`, `:25` | **No field exists** | The Log format at `SKILL.md:63-67` has four fields and reserves the only free-text one for the step-5 quote (`SKILL.md:36`). See DEFECT-S05. |
| `level` re-derivation input (mean of `## Levers`) | n/a | n/a | n/a | `assessment.md:46-52` defines the mapping but is only ever run at day 0. See S01. |

## Findings

Counts: 7 high, 10 medium, 3 low.

### DEFECT-S01 — `level` is written once on day 0 and never re-derived; the day-0 label sets the exercise tier for all 30 days — severity: high

`assessment.md:61` is the only writer:

> `level: working`

derived from `assessment.md:46-52`:

> | Mean lever score below 2.5 | `novice` |

`SKILL.md:16` reads it, `SKILL.md:30` uses it:

> **2. Write — 5 min.** Present the `## Exercise` tier matching `level`: `### Novice`, `### Working`, or `### Advanced`.

A grep for `level` across `SKILL.md`, `assessment.md` and all 30 day files finds no other writer. No day file mentions the field.

Failure scenario. A learner assessed with mean 2.3 gets `novice`. Days 1–13 each rescore a lever and day 14 rescores all eleven (`days/14.md:41`), so by day 15 `## Levers` may show a mean of 4.2 — `advanced` by `assessment.md:50`'s own table. Day 15 still serves `### Novice`. Concretely, on day 29 the Novice tier is capped by design: `days/29.md:29` — "run it once, and confirm it produces the deliverable they wanted — **anchor 1, the floor everyone starts from**" — while `days/29.md:37` targets anchor 3. The day-0 label therefore fixes the capstone ceiling, and (via DEFECT-S07) determines whether the learner ever sees the completion ceremony. The course's own state proves the label wrong from day 14 onwards and nothing acts on it.

Minimal fix. Day 14 is the only point after day 0 where all eleven levers are simultaneously fresh, so it is the only honest re-derivation point. Add one clause to `SKILL.md:20`: after day 14's lever scores are written, recompute the mean over `## Levers` and rewrite `level` using the table at `assessment.md:46-52` (without the day-0 diagnosis-count adjustment at `assessment.md:52`, which is a day-0-only correction), and tell the learner the tier changed. Re-running the assessment on review days is the wrong fix — it costs a full session and `assessment.md:3` forbids teaching during it, which would break the day-14 lesson.

### DEFECT-S02 — the secondary-constraint tie-break and the no-repeat rule both read a fact the `## Log` format never records — severity: high

`SKILL.md:30`:

> If several qualify, take the lowest-scoring; break ties by whichever you have used least recently, **which you can see in `## Log`**. Do not use the same lever on consecutive sessions.

The Log format, `SKILL.md:63-67`:

> `- Day 12 — interjection — self 3, rubric 4 — "priority markers changed what it did first"`

Field 2 is the day's own topic — day 12 *is* the interjection lesson (`days/12.md:1`). There is no field for the secondary lever, and `SKILL.md:20` ("Append one `## Log` line") does not add one.

Failure scenario. Take the assessment example verbatim (`assessment.md:65-67`): `pronoun: 2` and `particle: 2`. Day 1: two levers qualify, tied at 2. The stated tie-break is "used least recently, which you can see in `## Log`" — on day 1 `## Log` holds only the day-0 baseline line (`assessment.md:75`), which records no secondary usage, so the tie-break has no input at all and the tutor picks arbitrarily. Day 2 is worse: the session is fresh, has no memory of day 1, and must both break the same tie *and* honour "do not use the same lever on consecutive sessions" — neither is derivable from the file. Every session for the rest of the course inherits this. Two learners with identical state get different practice, and the "least recently used" rotation the rule is trying to buy never happens.

Minimal fix. Extend the format at `SKILL.md:63-67` with an optional fifth field written only when a secondary constraint was added, e.g. `- Day 12 — interjection — self 3, rubric 4 — secondary pronoun 3 — "…"`, and point `SKILL.md:30` at it. This also gives DEFECT-S03 and S16 somewhere to record their decisions.

### DEFECT-S03 — "add exactly one" and "not on consecutive sessions" contradict each other whenever exactly one lever scores ≤2 — severity: high

`SKILL.md:30`, one sentence apart:

> If any lever in `## Levers` scores 2 or below, add exactly one of them as a named secondary constraint … One only.

> Do not use the same lever on consecutive sessions.

Failure scenario. A learner leaves the assessment with a single weak lever, `particle: 2` (a common outcome — the example in `assessment.md:67` has two, but one is the modal case). Day 3: the tutor adds particle. The learner scores 2 again, and `SKILL.md:20` writes it back as 2 ("Set it to the score just given"), so it still qualifies. Day 4: the first instruction is mandatory and particle is the only candidate; the last instruction forbids particle. Nothing resolves the conflict. One tutor adds particle anyway (rule 2 loses), another adds nothing (rule 1 loses) and the learner practises their one weak lever every other day at best. The divergence is silent — neither branch produces an error the learner can see — and it persists for however many days the lever stays at 2.

Minimal fix. Rewrite the mandate as conditional at `SKILL.md:30`: "If a lever other than last session's secondary scores 2 or below, add the lowest-scoring of those. If the only qualifying lever is last session's, add none this session." That makes rule 2 the constraint and rule 1 the default, which is the ordering the surrounding prose implies.

### DEFECT-S04 — day 28 must show the literal `{{TASK}}` token; `SKILL.md` forbids ever showing it — severity: high

`SKILL.md:24`:

> Wherever `{{TASK}}` appears in any text you present, substitute the task the learner is working on this session. … **Never show the raw token to the learner.**

`days/28.md:22-23`, inside the **After** block the tutor is told to present at `SKILL.md:28`:

> \> Template: `Summarise {{TASK}} in five bullets, one per risk.`
> \> Slot: `{{TASK}}` — the document or diff being reviewed.

and `days/28.md:7` in the `## Concept`, which `SKILL.md:28` says to present **verbatim**:

> "{{TASK}}: summarise in five bullets, one per risk. Known failure: invents a risk when fewer than five exist — check the count first." **The slot says what to substitute**

Failure scenario. Day 28, first `## Tasks` entry "Reviewing PRs on the payments service". Obeying `SKILL.md:24` renders the After block as "Slot: `Reviewing PRs on the payments service` — the document or diff being reviewed", which is a prompt with no slot in it — i.e. the **Before**, presented as the After. The learner is then scored against `rubrics.md#prompt-library`, whose anchor 2 (`rubrics.md:350`) is "A prompt is saved, but without marking which parts change between uses" and whose anchor 3 (`rubrics.md:351`) requires marked slots — criteria for a technique they were never shown. The two instructions also collide directly at `SKILL.md:28` ("Present the day's `## Concept` verbatim") vs `SKILL.md:24` ("substitute … never show the raw token"), which cannot both be obeyed on `days/28.md:7`.

Minimal fix. Cheapest and localised: change the illustrated slot in `days/28.md:7`, `:17`, `:22`, `:23` to a name that is not the reserved token — `{{DOC}}` — leaving the token substitution rule untouched and keeping `{{TASK}}` live in the exercise tiers (`days/28.md:34`, `:38`, `:42`) where substitution is wanted. The alternative — an exemption clause in `SKILL.md:24` — puts a day-specific exception in the general loop and has to be maintained by every future day that teaches templating.

### DEFECT-S05 — day 29 is told to record the learner's task in the Log line; the Log format has no field for it, and day 30 depends on reading it — severity: high

`days/29.md:25`:

> then record it, in the learner's own words, in the day-29 `## Log` line, so day 30 can read it back without asking again.

`days/30.md:17` and `:25`:

> The tutor reads the day-29 `## Log` line and takes the task recorded there — not a fresh question to the learner.

> Read the task recorded in the day-29 `## Log` line before presenting a tier; **do not ask the learner to restate the task**.

The format at `SKILL.md:63-67` has four fields, and `SKILL.md:36` reserves the only free-text one:

> **5. Name it — 3 min.** Ask the learner which single change moved the output, and for a 1–5 self-rating. Log both.

Failure scenario. Day 29 ends. The tutor follows `SKILL.md:20` and `:36` and writes `- Day 29 — capstone — self 4, rubric 3 — "naming the stop condition"`. There is nowhere the task went. Day 30 opens, `days/30.md:25` says read the task from that line and forbids asking. The tutor either invents a task (the learner is now hardening a prompt for work they did not name) or breaks the explicit prohibition. This is the same shape as the previously-fixed capstone defect: the write side was added at `days/29.md:25` but the format contract at `SKILL.md:63-67` was never extended, so the field still has no home.

Minimal fix. Document a day-29 variant in the `## Log line format` section of `SKILL.md`, e.g. `- Day 29 — capstone — self 4, rubric 3 — task: "reviewing PRs on the payments service" — "naming the stop condition"`, and have `days/30.md:25` name that field explicitly rather than "the task recorded there".

### DEFECT-S06 — `## Log` is neither required nor read at session start, and the rebuild path cannot produce the Day 0 baseline line that day 30 requires — severity: high

`SKILL.md:14` enumerates the fields whose failure stops the session:

> for any other missing or unparseable field (`## Levers`, `## Tasks`, or `level`), offer to re-run the assessment instead

`## Log` is not in that list. `SKILL.md:16` does not read it either:

> 2. Read `level`, `current_day`, `## Levers`, and `## Tasks`.

Yet three consumers depend on it: `SKILL.md:30` (tie-break), `days/27.md:17`/`:25`, `days/30.md:17`/`:25`/`:45`. And `SKILL.md:13` offers a rebuild:

> If they were mid-course, accept a day number they state and rebuild the file from it, or re-run the assessment if they prefer.

Failure scenario. A learner loses `PROGRESS.md` on day 22 and states "day 22". The rebuild yields `current_day: 22` and nothing else that is recoverable — no `level`, no eleven lever scores, no `## Tasks`, no `## Log`. Session 22 passes validation at `SKILL.md:14` only if the tutor invents those fields; if it invents an empty `## Log`, validation still passes because `## Log` is not checked. Five sessions later `days/27.md:17`'s fallback ("the tutor reads `## Log` … finds the entry with the lowest rubric score") has nothing to read. Eight sessions later `days/30.md:45` reads "the eleven baseline scores from the Day 0 `## Log` line — **the only surviving record** of the learner's starting point", a line that was never written and that `assessment.md:78` says must never be edited after the fact, so it cannot be back-filled. The thirty-day payoff — baseline versus current, lever by lever — silently degrades to nothing, and the learner is told about it on day 30 rather than on the day of the rebuild.

Minimal fix. Two edits. (a) Add `## Log`, and specifically a parseable Day 0 line, to the required-field list at `SKILL.md:14`. (b) At `SKILL.md:13`, state that a rebuild from a stated day number cannot reconstruct the day-0 baseline, so the tutor must say so at rebuild time and name re-assessment as the only path that keeps day 30's comparison intact — which is a real choice the learner can make on day 22 and cannot make on day 30.

### DEFECT-S07 — day 30's `## Completion` is gated on an outcome the Novice tier structurally cannot produce, contradicting `SKILL.md`'s own tier-independence rule — severity: high

`days/30.md:45`:

> **When the revised prompt passes both**, set `current_day` to 31 in `PROGRESS.md`. Read the eleven baseline scores from the Day 0 `## Log` line … and show them alongside the current `## Levers` scores, lever by lever.

`SKILL.md:38`:

> **6. Completion.** If the day file has a `## Completion` section, carry it out after step 5, **whatever the learner's tier**.

`days/30.md:29` (Novice):

> Ask the learner to write three checks for the day-29 prompt, then run it once more **on the same case** and score it against those checks.

The Novice tier runs one case. "Passes both" has no referent — and the phrase is ambiguous even for the other tiers: `days/30.md:21` says "re-run against the same criteria" (both = criteria?), `days/30.md:37` says "passes the written criteria on both the original case and the unseen one" (both = cases).

Failure scenario. A `novice` learner — which, by DEFECT-S01, is anyone assessed novice on day 0, regardless of thirty days of improvement — completes day 30. The Completion trigger never fires. `SKILL.md:20` still increments `current_day` to 31 unconditionally, so the next session hits `SKILL.md:17` ("If `current_day` is above 30, tell the learner the course is complete and stop"). The learner is told the course is over and never sees the baseline-versus-current comparison, which is the only thing in thirty days that shows them they improved. There is no path back: `assessment.md:78` forbids editing the Day 0 line, and nothing re-enters day 30.

Minimal fix. Make the trigger unconditional and tier-independent, matching `SKILL.md:38`: "When day 30's critique is complete, whatever the tier, …". Drop the `current_day` write from `days/30.md:45` entirely and leave `SKILL.md:20` as the single writer (see S10). If a gate is genuinely wanted, gate the *anchor 4–5 claim*, not the ceremony.

### DEFECT-S08 — the single `rubric N` Log field is undefined on the four days that score more than one rubric, and day 27 searches that field — severity: medium

`SKILL.md:34`:

> Score the prompt against the rubric named in the day's `## Rubric` section, criterion by criterion, 1–5

Day 6 (`days/06.md:43`) and day 7 (`days/07.md:39`) each name five rubrics; day 14 (`days/14.md:41`) names eleven. The Log format (`SKILL.md:66`) has one slot: `rubric 4`. `days/27.md:17` then searches it:

> finds the entry with the lowest rubric score

Failure scenario. Day 14 produces eleven scores, say ranging 2 to 5. Tutor A logs the mean (3). Tutor B logs the minimum (2). Tutor C writes eleven numbers into the field. On day 27, "the entry with the lowest rubric score" resolves to day 14 under B, to some other day under A, and is unparseable under C — so the learner is asked to retrieve a prompt from a different day depending on a choice `SKILL.md` never made. Day 27's whole exercise (`days/27.md:29`–`:37`) is built on that prompt.

Minimal fix. State in `SKILL.md:63-67` which number occupies the field on multi-rubric days. The mean, rounded to the nearest integer, is the only choice comparable across single- and multi-rubric days; the per-rubric scores go to `## Levers` (`SKILL.md:20`) and are not lost.

### DEFECT-S09 — day 27's lowest-score search has no tie-break, does not exclude the Day 0 line, and misdescribes what the line contains — severity: medium

`days/27.md:17`:

> the tutor reads `## Log` in `PROGRESS.md`, finds the entry with the lowest rubric score, names that day to the learner, and asks them for the prompt they used that day — **the log line records the task and score**, not the prompt itself

The log line does not record the task. Per `SKILL.md:66` field 2 is the day's topic (`interjection`), and per S05 there is no task field at all before day 29. And the Day 0 line sits in the same list (`assessment.md:75`):

> `- Day 0 — assessment — level working, diagnosis 6/10 — baseline noun 4, verb 3, adjective 2, adverb 3, pronoun 2, preposition 4, conjunction 3, determiner 3, numeral 5, interjection 4, particle 2`

`SKILL.md:61-67` never documents this variant, so nothing tells the day-27 tutor it exists or that it must be skipped.

Failure scenario. Day 27, learner has no failed prompt ready. `## Log` holds 26 per-day lines, three of them `rubric 2`. Nothing says which of the three to take. A tutor scanning `## Log` for the smallest number instead lands on the day-0 line's `adjective 2`, or reads `diagnosis 6/10` as a score of 6, and announces "your lowest-scoring day was day 0" — a day with no prompt to retrieve. The learner is then asked to supply a prompt that never existed.

Minimal fix. In `SKILL.md`'s Log format section, document the Day 0 variant and state that only lines carrying a `rubric N` field are scored days. In `days/27.md:17`, add a tie-break — most recent among the tied, since the learner is most likely to still have that prompt — and correct "records the task and score" to "records the day's topic and score".

### DEFECT-S10 — `## Completion` runs before the state update, so it reports stale `## Levers` and double-writes `current_day` — severity: medium

`SKILL.md:38` places Completion inside the daily loop (loop step 6, after loop step 5). `SKILL.md:20` places the state write after the loop (session step 6):

> 6. Append one `## Log` line, update lever scores, and increment `current_day`.

`days/30.md:45` reads state inside Completion:

> show them alongside the **current** `## Levers` scores, lever by lever

Failure scenario. Day 30 with a secondary constraint added under `SKILL.md:30` — say `pronoun: 2`, scored 4 in step 4 per `SKILL.md:34`. Completion runs first and prints `pronoun 2` as the "current" score, then `SKILL.md:20` writes 4. The final comparison the learner is shown is wrong for exactly the lever the course spent thirty days pushing on. Separately, Completion sets `current_day` to 31 and `SKILL.md:20` then increments it to 32 — harmless against `SKILL.md:17` ("above 30") but two writers for one field with an order-dependent result.

Minimal fix. Either move Completion after the session-level state update (a one-line reorder in `SKILL.md`), or remove the state reads/writes from `days/30.md:45` and put the baseline comparison in `SKILL.md` as a post-update step. The first is smaller; the second removes the only day-file writer of `PROGRESS.md`, which is the cleaner contract.

### DEFECT-S11 — five days' exercise tiers are written as directions about the learner, and `SKILL.md`'s "present the tier" instruction has no guard that catches them — severity: medium

`SKILL.md:30`:

> Present the `## Exercise` tier matching `level`: `### Novice`, `### Working`, or `### Advanced`.

`SKILL.md:26` guards two signals only:

> Some passages are written to you rather than to the learner — they refer to **"the tutor"**, or describe **reading `PROGRESS.md`**. That text is direction, not script: act on it, never read it out.

The tiers on days 14, 21, 27, 29 and 30 are third-person directions about the learner and match neither signal: `days/29.md:29` "Ask the learner to write a first pass at the production prompt for their named task…"; `days/27.md:29` "Have the learner go lever by lever…"; also `days/14.md:29`, `days/21.md:35`, `days/30.md:29`. Days 1–13 and 15–28 use second-person imperatives ("Write a prompt for {{TASK}}…"), so the register is inconsistent within the same slot.

Failure scenario. Day 29, novice learner. The tutor obeys `SKILL.md:30` literally and says: "Ask the learner to write a first pass at the production prompt for their named task, run it once, and confirm it produces the deliverable they wanted — anchor 1, the floor everyone starts from." The learner is shown the scaffolding, told which tier they are in, and handed the rubric ceiling that `days/29.md:9` deliberately frames only for the tutor. Same class as the raw-token defect: internal machinery on screen.

Minimal fix. One line at `SKILL.md:26`: add third-person reference to "the learner" to the list of direction signals, and instruct the tutor to convert such a tier into a request addressed to the learner. That covers days not yet written; rewriting the fifteen tiers in second person is the alternative and costs more edits.

### DEFECT-S12 — the `## Exercise` preamble is never presented and never executed, which kills the "pick one" branch of the substitution rule and orphans five days' setup steps — severity: medium

Every lesson day has text between `## Exercise` and `### Novice`. On 24 days it is learner-facing (`days/01.md:27` and the same line on days 2–6, 8–13, 15–20, 22–26, 28): "Pick one of your recurring tasks. Write a single prompt for it." On days 14, 21, 27, 29, 30 it is tutor setup (`days/14.md:25`, `days/21.md:31`, `days/27.md:25`, `days/29.md:25`, `days/30.md:25`), each beginning "Before presenting a tier…" or "Read … before presenting a tier".

`SKILL.md:30` mentions only the tier. No step in the daily loop reads or acts on the preamble.

Failure scenario A. `SKILL.md:24` says: "Default to their first `## Tasks` entry; **when the exercise invites them to pick one and they do**, use their pick." The invitation lives only in the unpresented preamble, so the learner is never invited, never picks, and the pick clause is dead on all 24 days — the first `## Tasks` entry silently drives every exercise for a month. A learner with four tasks practises one.

Failure scenario B. Day 29: the preamble at `days/29.md:25` is the *only* place that instructs the tutor to record the task for day 30 (DEFECT-S05). A tutor that presents tiers and nothing else never executes it. The day-14/21 lever-naming (`days/14.md:25`, `days/21.md:31`) and the day-27 failed-prompt setup (`days/27.md:25`) are in the same position; `SKILL.md:26` rescues 14 and 21 because they name `PROGRESS.md`, but 27, 29 and 30 name only `## Log` and are not literally covered.

Minimal fix. Amend `SKILL.md:30` to "Present the `## Exercise` preamble, then the tier matching `level`", and extend `SKILL.md:26`'s signal list to include `## Log` alongside `PROGRESS.md` so the tutor-facing preambles are still filtered rather than read out.

### DEFECT-S13 — day 21 is designated a lever review day but its rubric scores no lever, so the levers it targets can never be cleared there — severity: medium

`SKILL.md:59`:

> Days 14 and 21 are review days: draw their material from the three lowest-scoring levers.

`days/21.md:31` does exactly that. But `days/21.md:47` is:

> Score against `rubrics.md#context-ordering`.

and `SKILL.md:20`:

> A lever's score changes only when the day actually scored it … Levers the day did not score are left untouched.

Day 14 does not have this problem — `days/14.md:41` names all eleven lever rubrics.

Failure scenario. A learner enters day 21 with pronoun 3, adverb 3, particle 3 as the three lowest. `days/21.md:31` builds the whole context-ordering exercise around those three ("if pronoun is weak, thread an unresolved 'it' through the paragraph"), the learner fixes all three convincingly, and `## Levers` records nothing. Those levers are also outside the ≤2 secondary-constraint pool at `SKILL.md:30`, so nothing else can touch them either. On day 30 (`days/30.md:45`) the comparison shows pronoun 3, adverb 3, particle 3 — no movement on precisely the dimensions the course targeted hardest.

Minimal fix. Add the targeted lever rubrics to `days/21.md:47` alongside `#context-ordering` — the tutor already has the revised prompt in hand and already knows which three levers to look at, so this costs no session time. Phrase it as "Score against `rubrics.md#context-ordering`, and against the rubric for each of the three levers named at the start of the exercise."

### DEFECT-S14 — after day 14, only levers scoring ≤2 can move, so `## Levers` is up to sixteen days stale when day 30 presents it as current — severity: medium

Lever scoring by day, from the `## Rubric` sections: day 1 noun, 2 verb, 3 adjective, 4 adverb, 5 preposition, 6 and 7 those same five (`days/06.md:43`, `days/07.md:39`), 8 pronoun, 9 conjunction, 10 determiner, 11 numeral, 12 interjection, 13 particle, 14 all eleven (`days/14.md:41`). Days 15–30 name technique rubrics only. Per `SKILL.md:20` the only remaining lever writer is the secondary constraint, and per `SKILL.md:30` that fires only for levers "2 or below".

Failure scenario. A learner finishes day 14 with every lever at 3 or 4 — no lever qualifies for a secondary constraint on any of days 15–30. `## Levers` is then frozen for sixteen sessions. `days/30.md:45` shows the day-0 baseline "alongside the current `## Levers` scores, lever by lever" and presents a day-14 snapshot as the day-30 state, understating two weeks of work on days 15–28 (role framing, schemas, decomposition, and the rest all exercise the same levers in passing). The learner's most likely reaction — that the second half of the course did nothing — is an artefact of the scoring schedule, not of their prompts.

Minimal fix. The cheapest honest option is to label rather than to add scoring: change `days/30.md:45` to show the day-0 baseline against `## Levers` **and state when each lever was last scored** (which requires the Log to identify scored levers — see S02's field). If a genuine end-state is wanted, day 30's rubric could add the eleven lever rubrics the way day 14 does, since the capstone prompt is exactly the artefact worth scoring on all eleven; that is a larger change to `days/30.md:41` and to the day-30 time budget.

### DEFECT-S15 — `## Tasks` is never validated for count, and at least one exercise tier needs three entries — severity: medium

`assessment.md:42`:

> Extract 3–5 recurring, concrete tasks.

Nothing enforces it. `SKILL.md:14` treats `## Tasks` as required but says nothing about how many entries make it valid, and the rebuild path at `SKILL.md:13` can produce any number, including none. Consumers that need more than one: `days/28.md:42` — "Save three prompts for three of your recurring tasks, including {{TASK}}" — and the 24 preambles inviting a pick (`days/01.md:27` etc.).

Failure scenario. A learner whose Part 3 interview honestly yields one recurring task ("writing incident postmortems") gets a one-entry `## Tasks`. Every session passes `SKILL.md:14`. On day 28 the Advanced tier asks for three tasks they do not have; the tutor either invents two — contradicting `SKILL.md:3` ("using the learner's own real tasks") and `assessment.md:42` ("in the learner's words, not yours") — or silently drops the learner to a lower tier, which corrupts the `level` contract from the other direction.

Minimal fix. Put the minimum where the other field checks already live, at `SKILL.md:14`: "`## Tasks` with fewer than three entries is a failed field — offer to re-run Part 3 of the assessment." Part 3 is four minutes (`assessment.md:34`), so this is a cheap repair rather than a full re-assessment.

### DEFECT-S16 — a weak lever can be added as a secondary constraint on the day whose own lesson is that same lever — severity: medium

`SKILL.md:57` states the intent:

> A lever scoring 2 or below is practised as a secondary constraint on a later day, **never by repeating its lesson**.

but `SKILL.md:30` has no exclusion for the day's own lever.

Failure scenario. A learner scores `pronoun: 2` at day 0 and it is the only lever ≤2. Day 8 is the pronoun lesson (`days/08.md:1`, rubric `days/08.md:43`). Step 2 presents the pronoun exercise, then appends the example constraint from `SKILL.md:30` almost verbatim — "and bind every reference; you scored low on pronoun" — to the pronoun exercise. Step 4 (`SKILL.md:34`) then scores pronoun twice against the same rubric: once as the day's rubric, once as the secondary. Step 6 (`SKILL.md:20`) gets two writes for one field in one session with no precedence rule, and the session spends its secondary-constraint budget on the one lever that did not need it, so no other lever is practised that day.

Minimal fix. One clause at `SKILL.md:30`: "never the lever the day's own `## Rubric` already scores." With the assessment example (`assessment.md:65-67`) this changes what days 8 and 13 practise, and nothing else.

### DEFECT-S17 — day 30 assumes a day-29 Log line exists, with no fallback when it does not — severity: medium

`days/30.md:17` and `:25` both read "the day-29 `## Log` line" as a given, and `:25` forbids the obvious recovery ("do not ask the learner to restate the task"). `README.md:33` explicitly invites the state to be hand-edited:

> It is plain markdown — edit it if you want to redo a day or change your tasks.

and `SKILL.md:13`'s rebuild path accepts any stated day number.

Failure scenario. A learner edits `current_day` from 28 to 30 to skip the day-29 capstone build, or rebuilds a lost file at day 30. `## Log` has no day-29 line. `days/30.md:25` instructs the tutor to read a line that does not exist and forbids the question that would recover it. Combined with DEFECT-S05, this fires even on the happy path.

Minimal fix. One clause at `days/30.md:25`: "if there is no day-29 line, ask the learner for the task and the prompt before presenting a tier." That is also the correct handling for S05's missing field, so the two fixes compose.

### DEFECT-S18 — `current_day` is guarded only at the upper bound; 0, negative, and non-integer values pass validation and then resolve to a non-existent day file — severity: low

`SKILL.md:17`:

> 3. If `current_day` is above 30, tell the learner the course is complete and stop.

`SKILL.md:18`:

> 4. Read `days/NN.md`, where NN is `current_day` zero-padded to two digits.

`SKILL.md:14` fails only on "missing or unparseable". `current_day: 0` and `current_day: 7.5` are both parseable.

Failure scenario. A learner hand-edits `current_day` to 0 intending "start over" (invited by `README.md:33`). Validation passes, `SKILL.md:17` does not fire, and step 4 tries `days/00.md`, which does not exist — the tutor is mid-session with no lesson and no instruction for that state, and `SKILL.md:13`'s "never silently restart at day 1" forbids the obvious guess.

Minimal fix. Fold the range check into the field check at `SKILL.md:14`: "`current_day` that is not an integer from 1 to 31 is a failed field." Keep `SKILL.md:17`'s "above 30" as the completion branch.

### DEFECT-S19 — the Log line's topic field is undefined for technique days and multi-lever days, and day 27 names it wrongly — severity: low

`SKILL.md:63-67` gives one example and no rule:

> `- Day 12 — interjection — self 3, rubric 4 — "…"`

`interjection` is day 12's lever. Nothing says what the field holds on day 7 (five levers), day 14 (eleven), day 25 (`writing evals`, a technique) or day 29 (`capstone`). `days/27.md:17` calls it "the task", `days/30.md:17` calls it nothing.

Failure scenario. Low impact because any reasonable tutor writes the day's title topic, but the ambiguity compounds S02 and S08: once the field is being used for tie-breaks and lowest-score searches, "day 14" logged as `review`, as `all eleven`, or as a list of eleven lever names are three different parses of the same session.

Minimal fix. One sentence in `SKILL.md`'s Log format section: field 2 is the day's lever or technique name as it appears in the day file's title, one value, even when the day scores several rubrics.

### DEFECT-S20 — `SKILL.md`'s list of review days contradicts day 7's own title — severity: low

`SKILL.md:59`:

> Days 14 and 21 are review days: draw their material from the three lowest-scoring levers.

`days/07.md:1`:

> \# Day 7 — Review: rewrite your worst prompt

Day 7 is a review day of a different kind — it draws from the learner's own failed prompt (`days/07.md:15`), as does day 27 (`days/27.md:17`). The rule at `SKILL.md:59` is correct about what days 14 and 21 do, but a tutor opening day 7, seeing "Review" in the title and a rule that names only 14 and 21, has to decide whether the omission is deliberate.

Minimal fix. Reword `SKILL.md:59` to name both kinds: "Days 14 and 21 draw their review material from the three lowest-scoring levers; days 7 and 27 review the learner's own failed prompts instead."
