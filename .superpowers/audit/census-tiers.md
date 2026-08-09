# Tier ladder census

Read-only audit of the three-tier exercise ladders in `prompting-wizard/days/01.md`–`30.md`
against the anchors in `prompting-wizard/rubrics.md`. All 30 days audited. Nothing was fixed;
no file under `prompting-wizard/` was modified.

**Method.** For each day: the three `### Novice` / `### Working` / `### Advanced` tiers were quoted
verbatim; all five anchors of every rubric named in that day's `## Rubric` section were read verbatim in
`rubrics.md`; each tier was judged against those anchors by the language it echoes. In the findings and
the per-day evidence below, the anchor(s) a tier lands on — and any anchor rendered unreachable — are
quoted verbatim with `rubrics.md:<line>`. The full five-anchor block for each rubric is cited by line
range rather than reproduced 30 times; every one was read in full before judging.

**Scoring context that makes this load-bearing.** `rubrics.md:5` — "Score the prompt as written, not the
intent behind it." `SKILL.md:30` — the tutor presents exactly one tier, chosen by `level`. `SKILL.md:34` —
"Score the prompt against the rubric named in the day's `## Rubric` section, criterion by criterion, 1–5,
quoting the rubric's anchor for each score you give." `SKILL.md:20` — "Set it to the score just given; do
not average with the old score." So the anchor a tier is written at *becomes* the learner's recorded lever
score, and a tier written at anchor 5 hands that score to whoever follows it.

---

## Summary table

| Day | Rubric | Novice @ anchor | Working @ anchor | Advanced @ anchor | Monotonic? | Anchor 4 reachable? |
|---|---|---|---|---|---|---|
| 01 | noun | 3–4 | 4 | 5 | yes | yes (Working) |
| 02 | verb | 5 | 5 | 5 | **no — flat at 5** | **no** |
| 03 | adjective | 4 | 5 | 5 (can drop to 4) | **no** | only via Novice |
| 04 | adverb | 4 | 4 | 5 | **no — N = W** | yes (Novice, Working) |
| 05 | preposition | 4 | 4 | 5 | **no — N = W** | yes (Novice, Working) |
| 06 | noun, verb, adjective, adverb, preposition | 4 | 5 | 5 | **no** | only via Novice |
| 07 | noun, verb, adjective, adverb, preposition | 1–3 | 4 | 5 | yes | yes (Working) |
| 08 | pronoun | 3–4 | 5 | 5 | **no** | **no** |
| 09 | conjunction | 4 | 4 | 5 | **no — W restates N** | yes (Novice, Working) |
| 10 | determiner | 4–5 | 3 | 4–5 | **no — N > W** | yes, but not from Working |
| 11 | numeral | 4–5 | 4 | 5 | **no — N ≥ W** | yes (Working) |
| 12 | interjection | 5 | 5 | 5 | **no — flat at 5** | **no** |
| 13 | particle | 4–5 | 5 | 5 | **no** | **no** |
| 14 | all eleven levers | n/a — no rewrite produced | 4 | 5 | partly | yes (Working) |
| 15 | role framing | 3 | 4 | 5 | yes | yes (Working) |
| 16 | few-shot examples | 5 | 5 | 5 | **no — flat at 5** | **no** |
| 17 | output schemas | 5 | 5 | 5 | **no — flat at 5** | **no** |
| 18 | task decomposition | 5 | 5 | 5 | **no — flat at 5** | **no** |
| 19 | reasoning scaffolds | 4–5 | 5 | 5 | **no** | **no** |
| 20 | negative constraints | 5 | 5 | 5 | **no — flat at 5** | **no** |
| 21 | context ordering | **1 (by instruction)** | 5 | 5 | **no** | **no** |
| 22 | system prompts | 4–5 | 5 | 5 | **no** | **no** |
| 23 | agent and tool prompting | 3 | 4 | 5 | yes | yes (Working) |
| 24 | self-critique loops | 3 | 5 | 5 | **no — 3 → 5 → 5** | **no** |
| 25 | writing evals | 3 | 4 | 5 | yes | yes (Working) |
| 26 | token economy | 5 | 5 | 5 | **no — flat at 5** | **no** |
| 27 | failure diagnosis | 3 | 5 | 5 | **no — 3 → 5 → 5** | **no** |
| 28 | prompt library | 4 | 5 | 5 | **no** | only via Novice |
| 29 | capstone | 1 | 2–3 | 3 | yes | deferred to day 30 by design — not a defect |
| 30 | capstone | 3 | 5 | **4** | **no — W > A** | yes (Advanced, perversely) |

Clean days, no finding filed: **01, 07, 15, 23, 25, 29** (six of thirty).

---

## Findings

Severity key as briefed. **high** = a learner is scored wrongly or a tier is unreachable.
**medium** = demand does not rise. **low** = phrasing.

Totals: **21 high, 3 medium, 2 low** across 26 findings.

---

### DEFECT-T01 — Day 02: all three tiers written at verb anchor 5; anchor 4 unreachable — severity: high

`days/02.md:29–41`; rubric `rubrics.md#verb`, anchors `rubrics.md:27–31`, cited at `days/02.md:45`.

Tiers, verbatim:

- Novice (`days/02.md:31`): "Fill the blank with one verb naming the exact operation you want performed, then send the completed line as your prompt." Template (`days/02.md:33`): "> ________ the correctness issues in {{TASK}}, worst first."
- Working (`days/02.md:37`): "Write a prompt for {{TASK}} that uses exactly one verb, and make it the verb that names the operation you actually want — not a generic stand-in like 'check' or 'handle'."
- Advanced (`days/02.md:41`): "Write a prompt for {{TASK}} using exactly one verb in the whole prompt. Every other word can name the artifact, the criteria, or the scope, but only one word may be doing."

Anchors:

- `rubrics.md:31` (5): "Exactly one operation named, and it is the operation actually wanted."
- `rubrics.md:30` (4): "Exactly one operation named, and it is the operation wanted, but expressed with a generic synonym ('check' instead of 'audit') where a more specific verb in the same family exists."

Why it is a defect. Working is anchor 5 word-for-word — "exactly one verb" = "Exactly one operation named", "the verb that names the operation you actually want" = "it is the operation actually wanted" — and it then explicitly forbids the single thing that defines anchor 4 by naming "check" as a banned stand-in, the very example anchor 4 uses. Novice reaches the same place: "one verb naming the exact operation you want performed" dropped into a pre-written frame yields an anchor-5 prompt from two seconds of work. Advanced adds "exactly one verb in the whole prompt", a constraint the verb rubric does not measure at all — the rubric scores whether *the* operation is named precisely, not how many verbs appear elsewhere — so Advanced is anchor 5 plus an off-rubric flourish. A learner on Working and a learner on Advanced score identically; nobody can be scored 4.

Minimal fix. Move Working down to anchor 4 by dropping the anti-synonym clause: "Write a prompt for {{TASK}} that uses exactly one verb for the operation you want, replacing any verb that names a family of operations." Leave the "not a generic stand-in like 'check' or 'handle'" demand to Advanced, which is where anchor 5 lives.

---

### DEFECT-T02 — Day 03: Working at adjective anchor 5, and Advanced's mandated third quality can score *lower* than Working — severity: high

`days/03.md:29–41`; rubric `rubrics.md#adjective`, anchors `rubrics.md:41–45`, cited at `days/03.md:45`.

Tiers, verbatim:

- Novice (`days/03.md:31`): "Fill the blanks with two qualities that would make you reject the output if either were missing, then send the completed line as your prompt." Template (`days/03.md:33`): "> Write a ________, ________ summary of {{TASK}}."
- Working (`days/03.md:37`): "Write a prompt for {{TASK}} that names the two qualities that matter most, worded specifically enough that a generic output would visibly fail one of them."
- Advanced (`days/03.md:41`): "Write a prompt for {{TASK}} that names exactly three qualities. For each one, be ready to say in one sentence what it rules out. If a quality doesn't rule anything out, replace it."

Anchors:

- `rubrics.md:45` (5): "Every quality that matters is named, and none that do not — each word does rejection work."
- `rubrics.md:44` (4): "Every quality that matters is named, though some slack remains in how they're worded."

Why it is a defect. Working names exactly the qualities that matter ("the two qualities that matter most"), none that do not (exactly two), and requires wording tight enough to reject generic output — that is anchor 5's "each word does rejection work", and the "worded specifically enough" clause is precisely the removal of the slack that defines anchor 4. Worse, Advanced mandates a *third* quality, which the day's own concept contradicts at `days/03.md:9`: "Two qualities usually do the real work ... A third rarely earns its place, and padding the list with qualities that don't matter here just adds noise the model has to reconcile." A third quality that does not matter violates anchor 5's "and none that do not", so a learner who follows Advanced literally can be scored *below* a learner who followed Working. Anchor 4 is reachable only from the Novice tier.

Minimal fix. Swap the demands: make Working "names the two qualities that matter most" with no specificity clause (anchor 4), and make Advanced "names only the qualities that do rejection work — two or three, no more — and for each, be ready to say in one sentence what it rules out" (anchor 5), removing the "exactly three" quota that fights the concept.

---

### DEFECT-T03 — Day 04: Novice and Working both land at adverb anchor 4 — severity: low

`days/04.md:29–41`; rubric `rubrics.md#adverb`, anchors `rubrics.md:55–59`, cited at `days/04.md:45`.

Tiers, verbatim:

- Novice (`days/04.md:31`): "Fill the blank with a manner word and a measure that pins it down, then send the completed line as your prompt." Template (`days/04.md:33`): "> Review {{TASK}} ________ — specifically, ________."
- Working (`days/04.md:37`): "Write a prompt for {{TASK}} where the depth of the work is set clearly enough that you could predict roughly how long the output would be before seeing it."
- Advanced (`days/04.md:41`): "Write a prompt for {{TASK}} that sets two different depths for two different parts of the same task — one part gets more scrutiny than the other, and the prompt says which and by how much."

Anchors:

- `rubrics.md:58` (4): "Depth and manner set clearly enough that output length and thoroughness are mostly predictable."
- `rubrics.md:59` (5): "Depth and manner set so output length and thoroughness are predictable in advance, not just in hindsight."

Why it is a defect. Working's "clearly enough that you could predict roughly how long the output would be" is anchor 4 almost verbatim — "clearly enough", "roughly" = "mostly predictable". Novice's completed template also lands at 4: a manner word plus "a measure that pins it down" set for the whole task is the same anchor. The two tiers differ in form (scaffold vs bare brief) but not in scored demand. Advanced is correctly at 5. Low severity because the scaffold genuinely reduces effort and anchor 4 stays reachable; the ladder is 4/4/5 rather than 3/4/5.

Minimal fix. Drop the measure from Novice so it targets anchor 3: "Fill the blank with a manner word, then attach a measure to only the part of the task where depth matters most."

---

### DEFECT-T04 — Day 05: Working is a prose restatement of the Novice template; both at preposition anchor 4 — severity: medium

`days/05.md:29–41`; rubric `rubrics.md#preposition`, anchors `rubrics.md:83–87`, cited at `days/05.md:45`.

Tiers, verbatim:

- Novice (`days/05.md:31`): "Fill the blanks with a scope, an audience, and an exclusion, then send the completed line as your prompt." Template (`days/05.md:33`): "> Fix the ________ problems in {{TASK}}, for ________, without ________."
- Working (`days/05.md:37`): "Write a prompt for {{TASK}} that sets a scope, names an audience, and rules out one side effect — all three, none left to the model's default."
- Advanced (`days/05.md:41`): "Write a prompt for {{TASK}} that states an audience, a boundary, and an exclusion, in that order, and in no more words than the boundaries need."

Anchors:

- `rubrics.md:86` (4): "Boundaries, audience and exclusions are all set, though phrased loosely enough to invite a small stretch."
- `rubrics.md:87` (5): "Boundaries, audience and exclusions all set precisely — in what, for whom, without what."

Why it is a defect. Working asks for the identical three items the Novice template's three blanks already elicit — scope, audience, exclusion — with no added precision requirement, so both sit at anchor 4 and Working is a reworded restatement of Novice rather than a distinct demand. Demand does not rise across the first step of the ladder. (Advanced correctly reaches 5 via "precisely" + economy.)

Minimal fix. Reduce Novice to two blanks — scope and audience — so it targets anchor 3 ("one relation is left implicit", `rubrics.md:85`), leaving the exclusion as the thing Working adds.

---

### DEFECT-T05 — Day 06: Working demands full economy (noun/adjective anchor 5); Advanced only restates it with a word count — severity: high

`days/06.md:29–39`; rubrics `rubrics.md#noun` (`rubrics.md:13–17`), `#verb` (`27–31`), `#adjective` (`41–45`), `#adverb` (`55–59`), `#preposition` (`83–87`), cited at `days/06.md:43`.

Tiers, verbatim:

- Novice (`days/06.md:31`): "Take a one-line prompt for {{TASK}} with none of the five levers set, then rewrite it adding one lever at a time — noun, verb, adjective, adverb, preposition — checking after each addition that the sentence still reads naturally."
- Working (`days/06.md:35`): "Write a single prompt for {{TASK}} that sets all five levers — noun, verb, adjective, adverb, preposition — without writing five separate clauses stitched together. Every word should be doing one lever's job."
- Advanced (`days/06.md:39`): "Write a prompt for {{TASK}} that sets all five levers in under 40 words total."

Anchors:

- `rubrics.md:17` (noun 5): "Named unambiguously and economically — no words spent on the artifact beyond what pins it down."
- `rubrics.md:16` (noun 4): "The artifact is named unambiguously. Someone reading only the prompt could describe the finished output."
- `rubrics.md:45` (adjective 5): "Every quality that matters is named, and none that do not — each word does rejection work."

Why it is a defect. "Every word should be doing one lever's job" is the economy criterion that separates 4 from 5 on both noun ("no words spent ... beyond what pins it down") and adjective ("each word does rejection work"). Working therefore sits at anchor 5 on two of the five rubrics the day scores, leaving anchor 4 on those two reachable only from the Novice tier. Advanced's "under 40 words total" is the same economy demand expressed as a number — a verification device for what Working already requires, not a higher demand — so Advanced is a reworded restatement of Working.

Minimal fix. Cut the last sentence of Working, leaving "sets all five levers ... without writing five separate clauses stitched together" (anchor 4), and let "every word doing one lever's job, in under 40 words" be Advanced's combined anchor-5 demand.

---

### DEFECT-T06 — Day 08: Working at pronoun anchor 5 and Advanced degenerate; anchor 4 unreachable — severity: high

`days/08.md:29–39`; rubric `rubrics.md#pronoun`, anchors `rubrics.md:69–73`, cited at `days/08.md:43`.

Tiers, verbatim:

- Novice (`days/08.md:31`): "Take a prompt for {{TASK}} that uses a pronoun with no antecedent, then rewrite it by replacing the pronoun with the exact noun phrase it should have meant."
- Working (`days/08.md:35`): "Write a prompt for {{TASK}} where every pronoun resolves, on first read, to a single antecedent inside the prompt — no re-reading required to confirm which one."
- Advanced (`days/08.md:39`): "Write a prompt for {{TASK}} using zero pronouns. Every reference is a named noun phrase instead, so there is nothing left for a reader to resolve."

Anchors:

- `rubrics.md:73` (5): "Every reference resolves inside the prompt or to a quoted block, on first read."
- `rubrics.md:72` (4): "Every reference resolves, though the resolution takes a re-read to confirm."

Why it is a defect. Working reproduces anchor 5 clause by clause — "every pronoun resolves" / "Every reference resolves"; "on first read" / "on first read"; "inside the prompt" / "inside the prompt" — and then closes anchor 4 explicitly with "no re-reading required to confirm which one", which is the negation of anchor 4's only distinguishing feature. Advanced ("zero pronouns") cannot exceed 5 and in fact scores 5 vacuously: with no references to bind, the rubric's measured dimension is empty. Anchor 4 is unreachable at either tier. Previously reported; **independently confirmed**.

Minimal fix. Relax Working to anchor 4 — "where every pronoun has exactly one antecedent inside the prompt, even if the reader has to re-read a clause to confirm it" — and keep the "on first read" requirement as Advanced's anchor-5 bar rather than the zero-pronoun trick.

---

### DEFECT-T07 — Day 09: Working restates the Novice template; both at conjunction anchor 4 — severity: medium

`days/09.md:31–43`; rubric `rubrics.md#conjunction`, anchors `rubrics.md:97–101`, cited at `days/09.md:47`.

Tiers, verbatim:

- Novice (`days/09.md:33`): "Fill the blanks with a condition, its outcome, and a fallback, then send the completed line as your prompt." Template (`days/09.md:35`): "> Update {{TASK}}. If ________, ________; otherwise ________."
- Working (`days/09.md:39`): "Write a prompt for {{TASK}} that states one condition, its outcome, and an explicit fallback for everything else — no edge case left for the model to invent."
- Advanced (`days/09.md:43`): "Write a prompt for {{TASK}} that states two branches, each with its own condition, outcome, and fallback, ordered so a reader checks them in a fixed sequence with no overlap between them."

Anchors:

- `rubrics.md:100` (4): "Each branch stated with its condition and its fallback, though the wording leaves the order of checks ambiguous."
- `rubrics.md:101` (5): "Each branch stated with its condition and its fallback, in an order that resolves without ambiguity."

Why it is a defect. Working asks for exactly the three items the Novice template's three blanks elicit — one condition, one outcome, one fallback — so it is a reworded restatement of the scaffold with the frame deleted, and both land at the same anchor. (Advanced is correctly at 5: two branches plus a fixed check order is the only tier where the 4-vs-5 discriminator, order ambiguity, can even be tested.)

Minimal fix. Drop the fallback blank from the Novice template — "> Update {{TASK}}. If ________, ________." — putting Novice at anchor 2 ("its condition or its outcome is missing" / no fallback, `rubrics.md:98–99`) so that the fallback is what Working adds.

---

### DEFECT-T08 — Day 10: inverted ladder — Novice lands at determiner anchor 4–5 while Working is capped at 3 — severity: high

`days/10.md:29–41`; rubric `rubrics.md#determiner`, anchors `rubrics.md:111–115`, cited at `days/10.md:45`.

Tiers, verbatim:

- Novice (`days/10.md:31`): "Fill the blanks with a determiner for each noun, then send the completed line as your prompt." Template (`days/10.md:33`): "> Fix ________ correctness issue in {{TASK}}. Leave ________ style issue alone."
- Working (`days/10.md:37`): "Write a prompt for {{TASK}} where the two or three nouns that most affect scope are each bound with a determiner chosen deliberately, not left bare."
- Advanced (`days/10.md:41`): "Write a prompt for {{TASK}} that binds every noun in the prompt with an explicit determiner — the, a, each, every, or any — leaving none bare."

Anchors:

- `rubrics.md:113` (3): "Most nouns are bound, but one noun that changes scope significantly ('the' vs 'any') is left bare."
- `rubrics.md:114` (4): "Each noun is bound — the, a, each, every, any — with only a minor reading left open."
- `rubrics.md:115` (5): "Each noun is bound — the, a, each, every, any — with no reading left open."

Why it is a defect. This is the inversion the brief names as crucial, running the other way from the usual case. The Novice template contains exactly two bindable nouns and puts a blank in front of both, so the completed prompt has **every** noun bound — anchor 4, arguably 5 — for the least work on the day. Working, by contrast, asks only that "the two or three nouns that most affect scope" be bound and says nothing about the rest, so a learner who follows it exactly leaves other nouns bare and is capped below anchor 4, whose text is "**Each** noun is bound". A Working-tier learner following the lesson correctly is scored *lower* than a Novice-tier learner following it correctly, and Working can never reach 4 as written. Advanced ("binds every noun ... leaving none bare") echoes anchor 4/5 verbatim and is therefore roughly where Novice already is.

Minimal fix. Raise Working to anchor 4 — "where every noun is bound with a determiner chosen deliberately, none left bare" — and lower Novice to one blank so its completed prompt leaves a second noun bare (anchor 3).

---

### DEFECT-T09 — Day 11: Novice's pre-written frame lands at numeral anchor 4–5, at or above Working — severity: medium

`days/11.md:31–43`; rubric `rubrics.md#numeral`, anchors `rubrics.md:125–129`, cited at `days/11.md:47`.

Tiers, verbatim:

- Novice (`days/11.md:33`): "Fill the blanks with a count and a length, then send the completed line as your prompt." Template (`days/11.md:35`): "> Give me exactly ________ options for {{TASK}}, each under ________ words."
- Working (`days/11.md:39`): "Write a prompt for {{TASK}} that bounds every countable dimension — count, length, and any other quantity — with a number instead of a vague quantifier."
- Advanced (`days/11.md:43`): "Write a prompt for {{TASK}} where every constraint is verifiable without judgement — a reader could check each one with a count, not an opinion."

Anchors:

- `rubrics.md:128` (4): "Every countable dimension is bounded with a number, though one bound is awkward to verify without counting carefully."
- `rubrics.md:129` (5): "Every countable dimension bounded, and the bounds checkable without judgement."

Why it is a defect. Working is a clean anchor 4 ("bounded with a number") and Advanced a clean 5 ("checkable without judgement" is anchor 5 verbatim) — the top of this ladder is correct. The problem is below it: the Novice template pre-writes the word "exactly" and the frame "each under ___ words", so the completed prompt bounds both countable dimensions with hard numbers that are checkable by counting — anchor 4 at minimum and plausibly 5, i.e. at or above the tier above it, for filling in two numerals. Demand does not rise from Novice to Working.

Minimal fix. Remove the pre-supplied "exactly" and the length clause from the template — "> Give me ________ options for {{TASK}}." — so Novice lands at anchor 2 ("One quantity is given ... but other countable dimensions ... are open", `rubrics.md:126`) and Working's "every countable dimension" is a real step up.

---

### DEFECT-T10 — Day 12: all three tiers written at interjection anchor 5; anchor 4 is structurally impossible — severity: high

`days/12.md:29–39`; rubric `rubrics.md#interjection`, anchors `rubrics.md:139–143`, cited at `days/12.md:43`.

Tiers, verbatim:

- Novice (`days/12.md:31`): "Write a five-sentence prompt for {{TASK}} containing one instruction you'd be angriest to see ignored. Mark that instruction IMPORTANT: and move it to stand alone at the end, then send the completed prompt."
- Working (`days/12.md:35`): "Write a prompt for {{TASK}} where exactly one instruction is marked as critical and positioned so a reader skimming top to bottom cannot pass over it."
- Advanced (`days/12.md:39`): "Write a prompt for {{TASK}} with exactly one attention marker, on the one instruction that must not be missed — and be ready to say in one sentence why none of the other instructions in the prompt needed one."

Anchors:

- `rubrics.md:143` (5): "The must-not-fail instruction is marked and positioned so it cannot be missed."
- `rubrics.md:142` (4): "The must-not-fail instruction is marked and positioned near the top, but competes with one other marked item."

Why it is a defect. Every tier reaches anchor 5. Novice marks the highest-stakes instruction and moves it "to stand alone at the end" — the day's own `## Before / After` at `days/12.md:23` calls exactly that "the one thing that cannot slip". Working's "positioned so a reader skimming top to bottom cannot pass over it" is anchor 5 reworded. Advanced adds "be ready to say in one sentence why none of the other instructions needed one", which the rubric does not score. Anchor 4 is not merely unreached but structurally impossible: it requires the marked item to "compete with one other marked item", and all three tiers mandate **exactly one** marker. No learner following any tier of this day can ever be scored 4.

Minimal fix. Let Novice mark the instruction without repositioning it (anchor 3, "marked, but its position ... still lets it get skimmed past", `rubrics.md:141`), and let Working mark and move it near the top while permitting a second marked item (anchor 4). Reserve "exactly one marker, positioned so it cannot be missed" for Advanced.

---

### DEFECT-T11 — Day 13: Working and Advanced both at particle anchor 5; anchor 4 unreachable — severity: high

`days/13.md:29–41`; rubric `rubrics.md#particle`, anchors `rubrics.md:153–157`, cited at `days/13.md:45`.

Tiers, verbatim:

- Novice (`days/13.md:31`): "Fill the blank with a phrasal verb whose particle names the exact operation you want, then send the completed line as your prompt." Template (`days/13.md:33`): "> ________ each external call in {{TASK}} and check it against its documented contract."
- Working (`days/13.md:37`): "Write a prompt for {{TASK}} using one phrasal verb, choosing its particle so that swapping it for a plausible alternative would visibly change the task."
- Advanced (`days/13.md:41`): "Write a prompt for {{TASK}} using two phrasal verbs whose particles are both load-bearing — swapping either one changes what gets done."

Anchors:

- `rubrics.md:157` (5): "Every phrasal verb chosen deliberately; no substitution preserves the meaning."
- `rubrics.md:156` (4): "Every phrasal verb is chosen deliberately, with only cosmetic substitutions available."

Why it is a defect. Working's test — "swapping it for a plausible alternative would visibly change the task" — is anchor 5's "no substitution preserves the meaning", and it forecloses anchor 4, whose defining feature is that only *cosmetic* substitutions exist. Advanced changes nothing but the count: two phrasal verbs instead of one, applying the same anchor-5 test to each. The rubric's anchors say "Every phrasal verb", so the number of them is not a scored dimension; Advanced is Working times two, not a rung above it. Anchor 4 unreachable at every tier.

Minimal fix. Move Working to anchor 4 — "using one phrasal verb chosen deliberately rather than by habit" — and keep the swap test ("no plausible substitution preserves the meaning") as the Advanced bar.

---

### DEFECT-T12 — Day 14: the Novice tier produces no revised prompt, so the day scores the learner's untouched original — severity: low

`days/14.md:27–37`; rubrics: all eleven, cited at `days/14.md:41`.

Tiers, verbatim:

- Novice (`days/14.md:29`): "Ask the learner for a real prompt for one of their `## Tasks` entries. Have them go lever by lever, all eleven, in order, stating out loud what each one currently sets — starting with the three named as weakest."
- Working (`days/14.md:33`): "Ask the learner to revise their prompt so every one of the eleven levers is deliberately set, with the three named as weakest addressed first and checked hardest."
- Advanced (`days/14.md:37`): "Ask the learner to write a prompt for a real task that sets all eleven levers in under 60 words total, holding the three named as weakest to the same standard as the rest."

Why it is a defect. Working ("deliberately set" across eleven levers) is anchor 4 territory and Advanced ("under 60 words total") adds the economy that lifts noun and adjective to 5, so the top of the ladder escalates correctly. The Novice tier, though, asks only for a spoken inventory: no revision is produced, so the prompt that reaches `SKILL.md:32`'s run step and `SKILL.md:34`'s scoring step is the learner's original, unchanged. `SKILL.md:20` then writes those eleven scores into `## Levers`, overwriting them with a pre-lesson baseline on a review day whose purpose is to lift the three weakest. It is a tier-model fit problem rather than a wrong anchor: the "Write — 5 min" step (`SKILL.md:30`) has nothing to write.

Minimal fix. Add a revision to Novice: "... then rewrite only the three named as weakest into the prompt, leaving the other eight as they are."

---

### DEFECT-T13 — Day 16: all three tiers require both a boundary case and a failure case — few-shot anchor 5, anchor 4 impossible — severity: high

`days/16.md:32–42`; rubric `rubrics.md#few-shot-examples`, anchors `rubrics.md:181–185`, cited at `days/16.md:46`.

Tiers, verbatim:

- Novice (`days/16.md:34`): "Write a prompt for {{TASK}} with no examples, then add exactly one boundary case and one failure case, each with a one-line reason, then send the completed prompt."
- Working (`days/16.md:38`): "Write a prompt for {{TASK}} whose two examples disagree — one a borderline pass, one a near-miss failure — so a reader could state the rule the examples imply without you explaining it."
- Advanced (`days/16.md:42`): "Write a prompt for {{TASK}} with exactly two examples, and no more, that disagree in a way that's instructive: choosing between them should teach the actual rule, not just show two instances of it."

Anchors:

- `rubrics.md:185` (5): "Examples cover the boundary case and the failure case."
- `rubrics.md:184` (4): "Examples cover the boundary case but not a genuine failure case."

Why it is a defect. Anchor 4 is defined by the *absence* of a failure case. All three tiers mandate a failure case — Novice says "one boundary case and one failure case" in so many words, Working says "one a borderline pass, one a near-miss failure", Advanced says "two examples ... that disagree". Every tier is therefore anchor 5 and anchor 4 cannot be scored by anyone who follows the lesson. Advanced's "and no more" and "instructive" are quality gloss on the same two examples, not a further rung. Previously reported; **independently confirmed**, and the flatness extends to Novice as well.

Minimal fix. Make Novice add a boundary case only (anchor 4), make Working add the failure case alongside it (anchor 5), and give Advanced a genuinely adversarial constraint that the rubric can see — e.g. requiring the failure case be one the learner has watched the model actually produce, per `days/16.md:9`.

---

### DEFECT-T14 — Day 17: all three tiers close the empty-value edge that defines output-schema anchor 4 — severity: high

`days/17.md:45–55`; rubric `rubrics.md#output-schemas`, anchors `rubrics.md:195–199`, cited at `days/17.md:59`.

Tiers, verbatim:

- Novice (`days/17.md:47`): "Write the output schema for {{TASK}} as a fenced code block filled with dummy values — name every field, its type, and what an empty value looks like — then send it as part of your prompt."
- Working (`days/17.md:51`): "Write a prompt for {{TASK}} whose schema, once filled with dummy values, could be validated by a script without you reading the actual output first."
- Advanced (`days/17.md:55`): "Write a prompt for {{TASK}} with a schema that's checkable by a script, not by reading — every field typed, every optional value shown filled and shown empty, no field left to prose description."

Anchors:

- `rubrics.md:199` (5): "An exact structure given, which output can be checked against mechanically."
- `rubrics.md:198` (4): "An exact structure is given, checkable in most cases, with one edge (e.g. empty values) unaddressed."

Why it is a defect. Anchor 4's single discriminator is that empty values are left unaddressed. The Novice tier requires "what an empty value looks like" outright, so the lowest tier already forecloses anchor 4. Working's "could be validated by a script without you reading the actual output first" is anchor 5's "checked against mechanically" restated. Advanced repeats both ("checkable by a script, not by reading", "shown filled and shown empty") without adding a scored demand. Three tiers, one anchor. Previously reported; **independently confirmed**, and Novice is at 5 too.

Minimal fix. Cut "and what an empty value looks like" from Novice (leaving fields and types = anchor 3, `rubrics.md:197`), and cut the script-validation clause from Working so it sits at anchor 4 with the empty-value edge open — that edge is exactly what Advanced then closes.

---

### DEFECT-T15 — Day 18: all three tiers demand verbatim seams — task-decomposition anchor 5 throughout — severity: high

`days/18.md:39–49`; rubric `rubrics.md#task-decomposition`, anchors `rubrics.md:209–213`, cited at `days/18.md:53`.

Tiers, verbatim:

- Novice (`days/18.md:41`): "Write a single chained prompt for {{TASK}} with three asks in it, then split it into three prompts where each one's input is exactly the previous prompt's real output, pasted in as you go."
- Working (`days/18.md:45`): "Write three prompts for {{TASK}} such that prompt two's input is exactly prompt one's output and prompt three's input is exactly prompt two's output — verbatim, nothing added."
- Advanced (`days/18.md:49`): "Write a one-line brief for {{TASK}} that the whole chain must satisfy, then split it into three or more prompts so every seam carries exactly the previous step's output, verbatim, nothing added and nothing re-explained — check each seam by pasting the real output across it. Then add one adversarial constraint to the brief that a lazy decomposition would fail ..."

Anchors:

- `rubrics.md:213` (5): "Work split so each step has one output and a clear input from the last."
- `rubrics.md:212` (4): "Work split so each step has one output and a mostly clear input from the last."

Why it is a defect. The only gap between 4 and 5 is "mostly clear" versus "clear". All three tiers require the seam to carry the previous output *exactly / verbatim*, which is maximally clear, so all three are anchor 5 and nobody can be scored 4. Advanced is the one tier in the course that literally follows the design intent — it says "add one adversarial constraint" at `days/18.md:49` — but the constraint operates on the chain's content, not on a dimension this rubric measures, so it buys no rubric headroom over Working. Previously reported; **independently confirmed**.

Minimal fix. Let Novice and Working split the chain without requiring verbatim hand-off ("each step's input is the previous step's output, summarised or pasted" = anchors 3 and 4), and make the verbatim-seam requirement the thing Advanced adds.

---

### DEFECT-T16 — Day 19: Working at reasoning-scaffold anchor 5; Novice nearly so; anchor 4 unreachable — severity: high

`days/19.md:29–39`; rubric `rubrics.md#reasoning-scaffolds`, anchors `rubrics.md:223–227`, cited at `days/19.md:43`.

Tiers, verbatim:

- Novice (`days/19.md:31`): "Write a 'think step by step' prompt for {{TASK}}, then rewrite it, replacing 'step by step' with the specific things the answer actually depends on."
- Working (`days/19.md:35`): "Write a prompt for {{TASK}} that names the intermediates the answer actually depends on — no more, no fewer — so a reader could tell you removed a step because the task doesn't need it, not because you ran out of space."
- Advanced (`days/19.md:39`): "Write a prompt for {{TASK}} that names exactly the intermediates the task requires. For each one you named, be ready to say what breaks in the answer if it's cut; for each one you left out, be ready to say why the task doesn't depend on it."

Anchors:

- `rubrics.md:227` (5): "The reasoning steps asked for match the ones the task requires."
- `rubrics.md:226` (4): "The reasoning steps asked for match the ones the task requires, with minor slack in ordering."

Why it is a defect. Working's "names the intermediates the answer actually depends on — no more, no fewer" is anchor 5 verbatim ("match the ones the task requires"), and "no more, no fewer" leaves no room for the slack that anchor 4 allows. Novice's "the specific things the answer actually depends on" reaches the same place. Advanced restates anchor 5 ("names exactly the intermediates the task requires") and appends a "be ready to say" rider that the rubric never scores. Anchor 4 unreachable. Note also that this rubric's anchors 4 and 5 differ only by the phrase "with minor slack in ordering", so no tier phrased in terms of *which* steps are named can ever separate them — a rubric-side contributor worth recording alongside the tier defect.

Minimal fix. Put ordering into the ladder, since it is the only 4/5 discriminator: Working "names the intermediates the answer depends on, in any order"; Advanced "names them in the order the task requires them produced".

---

### DEFECT-T17 — Day 20: all three tiers require every exclusion be an observed failure — negative-constraints anchor 5 throughout — severity: high

`days/20.md:29–39`; rubric `rubrics.md#negative-constraints`, anchors `rubrics.md:237–241`, cited at `days/20.md:43`.

Tiers, verbatim:

- Novice (`days/20.md:31`): "Write a prompt for {{TASK}} with one generic exclusion ('don't be verbose', 'don't be wrong'), then replace it with two exclusions naming failures you've actually seen the model make on this task."
- Working (`days/20.md:35`): "Write a prompt for {{TASK}} with exactly two exclusions, each traceable to a specific past failure you could describe in one sentence if asked."
- Advanced (`days/20.md:39`): "Write a prompt for {{TASK}} where every exclusion cites a real failure you've seen, not a hypothetical one — be ready to say when and how each one happened."

Anchors:

- `rubrics.md:241` (5): "Exclusions are specific, and each prevents a failure you have actually seen."
- `rubrics.md:240` (4): "Exclusions are specific and mostly map to failures you've seen, with one still speculative."

Why it is a defect. Anchor 4 requires one exclusion to remain speculative. Every tier forbids that: Novice ends at "two exclusions naming failures you've actually seen", Working at "each traceable to a specific past failure", Advanced at "every exclusion cites a real failure you've seen". All three are anchor 5, anchor 4 cannot be scored, and Advanced's addition ("be ready to say when and how each one happened") is an unscored rider. Not previously reported.

Minimal fix. Let Novice replace the generic exclusion with **one** observed failure plus one plausible-but-untested one (anchor 4), and reserve "each exclusion an observed failure" for Working, with Advanced adding the incident detail as the ungameable bar.

---

### DEFECT-T18 — Day 21: the Novice tier instructs the learner to produce an anchor-1 prompt and never fix it — severity: high

`days/21.md:33–35`; rubric `rubrics.md#context-ordering`, anchors `rubrics.md:251–255`, cited at `days/21.md:47`.

Tier, verbatim (`days/21.md:35`): "Ask the learner for a real task from their `## Tasks` entries. Have them write 200+ words of context and material for it with the instruction buried at the end, unreordered. Read it back and point out where the instruction sits."

Anchor `rubrics.md:251` (1): "Instruction buried after a wall of context, or context missing where needed."

Why it is a defect. The tier's deliverable is, word for word, the rubric's anchor-1 failure: 200+ words of context with the instruction buried at the end. Nothing in the tier asks the learner to reorder it. Under `rubrics.md:5` ("Score the prompt as written, not the intent behind it") and `SKILL.md:34`, the tutor then scores that prompt against the context-ordering rubric and `SKILL.md:20` writes the result into `## Levers`. A Novice-tier learner who follows day 21 perfectly is guaranteed a recorded score of 1 on context ordering, and the whole 20-minute session produces no improved prompt — the run step at `SKILL.md:32` executes a prompt the lesson deliberately made bad. This is the clearest case in the course of a learner being scored wrongly for compliance.

Minimal fix. Add the reorder to the tier: "... then move the instruction to the top and group the constraints at the end, and send the reordered version as your prompt." Scoring the buried draft is the *demonstration*; the scored artifact must be the fix.

---

### DEFECT-T19 — Day 21: Working at context-ordering anchor 5; Advanced adds only work this day does not score — severity: high

`days/21.md:37–43`; rubric `rubrics.md#context-ordering`, anchors `rubrics.md:251–255`, cited at `days/21.md:47`.

Tiers, verbatim:

- Working (`days/21.md:39`): "Ask the learner to reorder their prompt into task, material, constraints — without deleting a word — and to predict, before running it, what changes about the output. Check the prediction against the real run."
- Advanced (`days/21.md:43`): "Ask the learner to reorder a prompt for a real task into task, material, constraints, predicting the change first, while also fixing the three levers named as weakest wherever they surface in the reordered material."

Anchors:

- `rubrics.md:255` (5): "Instruction and context ordered so the model reads what it needs when it needs it."
- `rubrics.md:254` (4): "Instruction and context are ordered sensibly, with constraints mostly grouped but one placed early."
- `rubrics.md:257` (fastest fix): "task first, material second, constraints last."

Why it is a defect. "Task, material, constraints" is the rubric's own top-anchor recipe, printed at `rubrics.md:257` as the fastest route to 5, and Working demands it exactly — with constraints fully grouped, not "mostly grouped but one placed early" as anchor 4 requires. Advanced asks for the same reorder and adds work on the three weakest levers, but `days/21.md:47` cites **only** `rubrics.md#context-ordering`, so that extra work is never scored. Advanced therefore scores identically to Working, and anchor 4 is unreachable. Compounding it: `SKILL.md:59` designates day 21 a review day drawing on the three lowest-scoring levers, yet the day scores one rubric that has nothing to do with them.

Minimal fix. Let Working reorder task-then-material while leaving one constraint early (anchor 4), and make full constraint-grouping plus the prediction check Advanced's anchor-5 demand; separately, add the three weakest levers' rubrics to `days/21.md:47` so Advanced's extra work is scored.

---

### DEFECT-T20 — Day 22: Working at system-prompt anchor 5; anchor 4 unreachable — severity: high

`days/22.md:35–45`; rubric `rubrics.md#system-prompts`, anchors `rubrics.md:265–269`, cited at `days/22.md:49`.

Tiers, verbatim:

- Novice (`days/22.md:37`): "Take a prompt you've sent more than once for {{TASK}}. Underline anything that would still be true on a future turn even if the request changed, and move it into a system prompt; leave the rest as the per-turn ask."
- Working (`days/22.md:41`): "Write a system prompt and a per-turn ask for {{TASK}} such that nothing in the system prompt would need to change if you sent a different per-turn ask tomorrow."
- Advanced (`days/22.md:45`): "Write a system prompt for {{TASK}} that stays unchanged across three different per-turn asks you could plausibly send tomorrow. Write all three per-turn asks. If any of them would force you to edit the system prompt, revise it and try again."

Anchors:

- `rubrics.md:269` (5): "Standing behaviour and per-turn request cleanly separated."
- `rubrics.md:268` (4): "Standing behaviour and per-turn request are separated into two blocks, but one line in the system prompt is turn-specific and could move to the per-turn request without changing behaviour."

Why it is a defect. Anchor 4 is defined by one surviving turn-specific line in the system prompt. Working's condition — "nothing in the system prompt would need to change if you sent a different per-turn ask tomorrow" — is the exact negation of that, i.e. clean separation, i.e. anchor 5. Novice's underline-what-stays-true test reaches the same criterion by a different route. Anchor 4 is unreachable. Advanced is the mildest offender in this class: it applies a genuinely stronger *verification* (three concrete asks rather than one hypothetical) to the same anchor, so it is not a pure restatement — but it still cannot score above Working. Not previously reported.

Minimal fix. Have Working produce the two blocks without the durability test — "split your prompt into a system block and a per-turn ask" (anchor 4, where a turn-specific line plausibly survives) — and keep the "nothing would need to change" test for Advanced.

---

### DEFECT-T21 — Day 24: ladder jumps 3 → 5 → 5; self-critique anchor 4 skipped entirely — severity: high

`days/24.md:29–39`; rubric `rubrics.md#self-critique-loops`, anchors `rubrics.md:293–297`, cited at `days/24.md:43`.

Tiers, verbatim:

- Novice (`days/24.md:31`): "Write a single-pass prompt for {{TASK}}, then add one named check the model applies to its own output before finishing."
- Working (`days/24.md:35`): "Write a prompt for {{TASK}} with a check specific enough that you can say, in one sentence, what a failure would look like, plus a stated action for when it fails."
- Advanced (`days/24.md:39`): "Write a prompt for {{TASK}} whose self-check the model could plausibly fail — not one it will always pass by default — with a stated correction. Be ready to say what output would have triggered it."

Anchors:

- `rubrics.md:297` (5): "A check the model can apply to its own output, with a stated action when it fails."
- `rubrics.md:296` (4): "A check the model can apply to its own output, with an action on failure that's only loosely defined."
- `rubrics.md:295` (3): "A concrete check is named, but there's no stated action for when it fails."

Why it is a defect. Novice sits correctly at anchor 3 — a named check, no failure action. Working then jumps straight to anchor 5: "plus a stated action for when it fails" is anchor 5's "with a stated action when it fails", word for word, and it skips anchor 4's *loosely defined* action entirely. Advanced ("with a stated correction") is the same anchor with an unscored rider. So the ladder is 3 / 5 / 5: anchor 4 is never occupied by any tier, and Working and Advanced learners are indistinguishable. Previously reported; **independently confirmed**.

Minimal fix. Insert the missing rung: Working "with a check specific enough that you can say what a failure would look like, and some response when it fails" (anchor 4); Advanced keeps the precisely stated correction plus the plausibly-failable check (anchor 5).

---

### DEFECT-T22 — Day 26: every tier requires the rerun, which is exactly what lifts token-economy 4 to 5 — severity: high

`days/26.md:29–39`; rubric `rubrics.md#token-economy`, anchors `rubrics.md:321–325`, cited at `days/26.md:43`.

Tiers, verbatim:

- Novice (`days/26.md:31`): "Take a prompt you've written for {{TASK}} with background you added 'just in case.' Cut it, rerun, and compare the two outputs."
- Working (`days/26.md:35`): "Cut a third of the context from a prompt for {{TASK}}, rerun both versions, and say which parts of the cut material — if any — the output actually needed."
- Advanced (`days/26.md:39`): "Cut half the context from a prompt for {{TASK}}. Before rerunning, predict which half mattered; then rerun and check your prediction against what actually changed."

Anchors:

- `rubrics.md:325` (5): "Every included token earns its place; cuts made without losing accuracy."
- `rubrics.md:324` (4): "Every included token earns its place on inspection, but the cuts have not been tested against the output to confirm accuracy held."

Why it is a defect. Anchor 4 is precisely "the cuts have not been tested against the output". All three tiers mandate the test: Novice "Cut it, rerun, and compare the two outputs", Working "rerun both versions", Advanced "then rerun and check". Every tier is anchor 5 and anchor 4 is unreachable. The escalation that does exist — a third of the context, then half, plus a prediction — is a change in cut size and in the learner's confidence, neither of which the rubric measures. Previously reported; **independently confirmed**, and Novice is at 5 as well.

Minimal fix. Make Novice and Working cut by inspection only ("cut what doesn't earn its place, and say why" = anchor 4) and make the rerun-and-compare, which is the anchor-5 evidence, the thing Advanced adds.

---

### DEFECT-T23 — Day 27: Working at failure-diagnosis anchor 5, forbidding the second-lever contamination that defines anchor 4 — severity: high

`days/27.md:27–37`; rubric `rubrics.md#failure-diagnosis`, anchors `rubrics.md:335–339`, cited at `days/27.md:41`.

Tiers, verbatim:

- Novice (`days/27.md:29`): "Have the learner go lever by lever through the failed prompt, out loud, until they find the one they'd bet money was underspecified. Name it before running anything."
- Working (`days/27.md:33`): "Have the learner name the single lever or technique responsible, state the fix that targets only it, then run the original prompt, if not already run, to confirm the diagnosis before applying the fix."
- Advanced (`days/27.md:37`): "Have the learner diagnose the lever, write the fix, and predict in one sentence what the rerun will show — then run both the original and the fixed version and check the prediction against both outputs."

Anchors:

- `rubrics.md:339` (5): "The failing lever is identified by name and the fix targets it."
- `rubrics.md:338` (4): "The failing lever is identified by name and the fix changes that lever, but it also changes a second lever that was not implicated."

Why it is a defect. Working is anchor 5 with the anchor-4 escape hatch nailed shut: "name the single lever ... state the fix that targets **only** it" both matches "the fix targets it" and forbids the second, unimplicated lever that is anchor 4's whole definition. Advanced adds a written prediction and a two-run comparison — good practice, but the rubric scores the diagnosis and the fix, not the prediction, so it lands on the same anchor. Novice is correctly at 3 (a lever named, no fix). Ladder is 3 / 5 / 5. Previously reported; **independently confirmed**.

Minimal fix. Drop "only" from Working — "state the fix for that lever" (anchor 4 permits collateral changes) — and make "the fix changes nothing but the named lever" the Advanced requirement.

---

### DEFECT-T24 — Day 28: Working at prompt-library anchor 5; Advanced multiplies quantity, not demand — severity: high

`days/28.md:32–42`; rubric `rubrics.md#prompt-library`, anchors `rubrics.md:349–353`, cited at `days/28.md:46`.

Tiers, verbatim:

- Novice (`days/28.md:34`): "Take a prompt you've written more than once for {{TASK}}. Save it with its slot marked and one failure mode you've actually seen written underneath it."
- Working (`days/28.md:38`): "Save a prompt for {{TASK}} with every variable part marked as a named slot and its known failure modes documented, so someone else could use it correctly without asking you anything."
- Advanced (`days/28.md:42`): "Save three prompts for three of your recurring tasks, including {{TASK}}, using the same slot name for the same kind of thing across all three, each with its known failure modes documented."

Anchors:

- `rubrics.md:353` (5): "Reusable prompts stored with their slots and their known failure modes."
- `rubrics.md:352` (4): "Reusable prompts stored with their slots and most known failure modes noted."

Why it is a defect. Working reproduces anchor 5 exactly — "with every variable part marked as a named slot and its known failure modes documented" against "stored with their slots and their known failure modes" — leaving anchor 4 ("most known failure modes noted") occupied only by the Novice tier, which records one. Advanced asks for the same artifact three times over with a naming convention across them; consistency of slot names is not a scored dimension, and three anchor-5 artifacts score the same as one. Previously reported; **independently confirmed**.

Minimal fix. Have Working save the prompt with all slots and the failure modes it remembers (anchor 4), and make Advanced require the *complete* set of known failure modes plus the shared slot vocabulary across three prompts (anchor 5).

---

### DEFECT-T25 — Day 30: inverted top of ladder — Advanced omits the documentation that puts Working at capstone anchor 5 — severity: high

`days/30.md:31–37`; rubric `rubrics.md#capstone`, anchors `rubrics.md:363–367`, cited at `days/30.md:41`.

Tiers, verbatim:

- Working (`days/30.md:33`): "Ask the learner to run the day-29 prompt on a case unlike the one it was designed for, name what broke, and write the failure mode down specifically enough that someone else could recognise it."
- Advanced (`days/30.md:37`): "Ask the learner to run the day-29 prompt against an unseen case, fix only what that case revealed, and rerun until it passes the written criteria on both the original case and the unseen one."

Anchors:

- `rubrics.md:367` (5): "Prompt is specified, evaluated against written criteria, and its failure modes documented."
- `rubrics.md:366` (4): "Prompt is specified and evaluated against written criteria, with failure modes noted but not systematically."

Why it is a defect. Anchor 5's third clause is "its failure modes documented". Working requires exactly that — "write the failure mode down specifically enough that someone else could recognise it" — and, with the criteria the day's `## Before / After` has the learner write (`days/30.md:21`), reaches anchor 5. Advanced never asks for the failure mode to be written down at all: it says "fix only what that case revealed", which is repair, not documentation, and lands at anchor 4's "failure modes noted but not systematically". Scored as written, the Advanced learner finishes the entire 30-day course one anchor *below* the Working learner, on the capstone.

Minimal fix. Add the documentation clause to Advanced: "... fix only what that case revealed, write down each failure mode the case exposed, and rerun until it passes the written criteria on both cases."

---

### DEFECT-T26 — Day 30: Working at capstone anchor 5, leaving Advanced no rung to climb — severity: high

`days/30.md:27–37`; rubric `rubrics.md#capstone`, anchors `rubrics.md:363–367`, cited at `days/30.md:41`.

Tiers, verbatim:

- Novice (`days/30.md:29`): "Ask the learner to write three checks for the day-29 prompt, then run it once more on the same case and score it against those checks."
- Working (`days/30.md:33`): "Ask the learner to run the day-29 prompt on a case unlike the one it was designed for, name what broke, and write the failure mode down specifically enough that someone else could recognise it."
- Advanced (`days/30.md:37`): "Ask the learner to run the day-29 prompt against an unseen case, fix only what that case revealed, and rerun until it passes the written criteria on both the original case and the unseen one."

Anchors: `rubrics.md:367` (5) and `rubrics.md:366` (4), quoted in DEFECT-T25; `rubrics.md:365` (3): "Prompt is specified and works on varied cases, but has no written evaluation criteria."

Why it is a defect. Separate from the inversion in T25: Working on its own already satisfies all three clauses of anchor 5 — specified (carried from day 29), evaluated against written criteria (supplied by `days/30.md:21`), failure modes documented — so the course's final rubric has nothing left for its top tier to demand. The three tiers land at roughly 3 / 5 / 4, which is neither monotonic nor bounded by the intended ceiling. Day 29 is deliberately capped at anchor 3 (`days/29.md:9–10`: "Reaching that rung honestly caps you at anchor 3. Anchors 4 and 5 need written criteria and documented failures — day 30's work"), so day 30 is the only place anchors 4 and 5 are distributed, and it distributes them backwards.

Minimal fix. Spread the two remaining rungs across the two top tiers: Working "run it on an unseen case, note what broke" (anchor 4, noted but not systematic); Advanced "run it on an unseen case, document every failure mode it exposed systematically, fix only what the case revealed, and rerun until it passes the written criteria on both cases" (anchor 5).

---

## Cross-cutting observations

These are patterns across the numbered findings, not separate defects.

**The systemic pattern is confirmed and it is nearly twice as wide as reported.** All nine previously
reported days — 02, 08, 16, 17, 18, 24, 26, 27, 28 — were re-derived independently from the tier text and
the anchor text, and all nine hold. The full pass adds **eleven more days** with Working at anchor 5 or a
tier written at or above the tier above it: 03, 06, 12, 13, 19, 20, 21, 22, 30, plus the two inversions on
10 and 11. Twenty of thirty days carry a high-severity ladder defect.

**Anchor 4 is unreachable on 15 of 30 days** (02, 08, 12, 13, 16, 17, 18, 19, 20, 21, 22, 24, 26, 27, 30
from Working). On three more (03, 06, 28) it is reachable only by a Novice-tier learner. Days 12, 16, 17,
20 and 26 are the sharpest cases: their anchor-4 text names a specific shortfall (a competing second
marker; no failure case; empty values unaddressed; one speculative exclusion; cuts untested) that *every*
tier explicitly forbids, so anchor 4 is not merely unreached but unwritable by anyone following the lesson.

**The recurring shape of a broken Advanced tier** is a constraint the cited rubric does not measure, bolted
onto Working's demand. Four variants recur: a word or item budget (02 "exactly one verb in the whole
prompt", 06 "under 40 words", 13 "two phrasal verbs", 28 "three prompts"); a "be ready to say" rider that
is never scored (12, 19, 20, 24); a degenerate maximum (08 "zero pronouns"); and unscored extra work on
other levers (21, whose `## Rubric` cites only context ordering). Where Advanced *does* escalate honestly
it does so by strengthening the verification of the same anchor rather than by climbing (22's three
per-turn asks, 25's "don't soften one it narrowly misses") — which works only because Working was left
below 5 on day 25 and is wasted on day 22 where it was not.

**Novice scaffolds sometimes over-deliver.** On days 10, 11, 12, 16, 17, 18, 20 and 26 the fill-in-the-blank
or step-by-step form hands the learner a frame that yields an anchor-4-or-5 artifact from minimal work — on
day 10 strictly above the Working tier. The Day 01 template ("Produce ________ for {{TASK}}") is the model
to copy: it leaves genuine room to fail, so a weak noun phrase still scores 2.

**Review days.** Day 07 is the best-fitting review day in the course: no seed prompt, learner brings a real
failure, and the tiers escalate cleanly 1–3 / 4 / 5. Day 29 is also clean — it caps itself at anchor 3 and
says so out loud, deferring 4 and 5 to day 30 by design. The tier model fits badly on days 14, 21, 27 and
30. On 14 and 27 the Novice tier is an oral inventory that produces no revised prompt, so the daily loop's
write-run-score cycle scores an unrevised original (T12). On 21 the Novice tier produces a deliberately
anchor-1 prompt that is then scored (T18), and Advanced's real work sits outside the day's cited rubric
(T19). On 30 the two top tiers are transposed (T25, T26). Day 06 is a composition day rather than a review
day but shares the pattern: five rubrics cited, and the Advanced tier's word budget touches only two of them.

---

## Per-day evidence

Tiers are quoted verbatim. For each tier, the anchor it is judged to sit at is quoted verbatim with its
`rubrics.md` line. All five anchors of every cited rubric were read; the full block's line range is given
so each judgement can be checked against the anchors above and below the one quoted. Days with a filed
finding cross-reference it rather than repeating the quotes.

### Day 01 — `rubrics.md#noun`, anchors `rubrics.md:13–17` — CLEAN

- Novice (`days/01.md:31,33`): "Fill the blank with a noun phrase naming exactly what you want back, then send the completed line as your prompt." / "> Produce ________ for {{TASK}}." → anchor 3–4. The blank admits "a summary" (anchor 2, `rubrics.md:14`: "A category is named ... but its shape is left open") as easily as "a five-bullet review", so the tier leaves genuine room to fail. Lands at `rubrics.md:15` (3): "The artifact is recognisable, but a reasonable reader could still deliver two different things."
- Working (`days/01.md:37`): "Write a prompt for {{TASK}} whose deliverable is unambiguous. Someone reading only your prompt, without seeing any output, should be able to describe the finished artifact." → anchor 4, `rubrics.md:16`: "The artifact is named unambiguously. Someone reading only the prompt could describe the finished output."
- Advanced (`days/01.md:41`): "Write a prompt for {{TASK}} that names the artifact unambiguously in under 15 words total. Precision without length is the constraint — every word you spend has to be pinning the artifact down." → anchor 5, `rubrics.md:17`: "Named unambiguously and economically — no words spent on the artifact beyond what pins it down."

Strictly monotonic, anchor 4 occupied by Working, no tier a restatement of another. This is the template the rest of the course should follow.

### Day 02 — `rubrics.md#verb`, anchors `rubrics.md:27–31` — see DEFECT-T01

Novice 5, Working 5, Advanced 5. Anchor 4 unreachable.

### Day 03 — `rubrics.md#adjective`, anchors `rubrics.md:41–45` — see DEFECT-T02

Novice 4, Working 5, Advanced 5 (droppable to 4). Anchor 4 reachable only via Novice.

### Day 04 — `rubrics.md#adverb`, anchors `rubrics.md:55–59` — see DEFECT-T03

Novice 4, Working 4, Advanced 5. Anchor 4 reachable; ladder not strictly rising.

### Day 05 — `rubrics.md#preposition`, anchors `rubrics.md:83–87` — see DEFECT-T04

Novice 4, Working 4, Advanced 5. Working restates Novice.

### Day 06 — five rubrics, see DEFECT-T05

Novice 4, Working 5 (noun, adjective), Advanced 5. Advanced restates Working with a word count.

### Day 07 — five rubrics (`rubrics.md:13–17`, `27–31`, `41–45`, `55–59`, `83–87`) — CLEAN

- Novice (`days/07.md:27`): "State which one of the five levers — noun, verb, adjective, adverb, preposition — was most clearly missing from your original prompt, then rewrite only that lever in." → one lever repaired, the other four left as the learner originally wrote them, so the prompt scores wherever it already sat on those: anchors 1–3.
- Working (`days/07.md:31`): "Rewrite your prompt so that all five levers are set, checking each one explicitly against the original before you send the new version." → anchor 4 on each, e.g. `rubrics.md:16`: "The artifact is named unambiguously."
- Advanced (`days/07.md:35`): "Rewrite your prompt so that removing any single clause measurably degrades the output — no clause is decorative, every one is load-bearing." → anchor 5 on the economy-sensitive rubrics, `rubrics.md:17`: "no words spent on the artifact beyond what pins it down"; `rubrics.md:45`: "each word does rejection work."

Strictly monotonic, anchor 4 occupied by Working. The best-fitting review day in the course.

### Day 08 — `rubrics.md#pronoun`, anchors `rubrics.md:69–73` — see DEFECT-T06

Novice 3–4, Working 5, Advanced 5 (vacuous). Anchor 4 unreachable.

### Day 09 — `rubrics.md#conjunction`, anchors `rubrics.md:97–101` — see DEFECT-T07

Novice 4, Working 4, Advanced 5. Working restates Novice.

### Day 10 — `rubrics.md#determiner`, anchors `rubrics.md:111–115` — see DEFECT-T08

Novice 4–5, Working 3, Advanced 4–5. Inverted: Novice scores above Working.

### Day 11 — `rubrics.md#numeral`, anchors `rubrics.md:125–129` — see DEFECT-T09

Novice 4–5, Working 4, Advanced 5. Top of ladder correct; Novice at or above Working.

### Day 12 — `rubrics.md#interjection`, anchors `rubrics.md:139–143` — see DEFECT-T10

Novice 5, Working 5, Advanced 5. Anchor 4 structurally impossible.

### Day 13 — `rubrics.md#particle`, anchors `rubrics.md:153–157` — see DEFECT-T11

Novice 4–5, Working 5, Advanced 5. Anchor 4 unreachable.

### Day 14 — all eleven rubrics — see DEFECT-T12

Novice produces no revised prompt; Working 4, Advanced 5. Top of ladder correct.

### Day 15 — `rubrics.md#role-framing`, anchors `rubrics.md:167–171` — CLEAN

- Novice (`days/15.md:31`): "Write a role for {{TASK}} that has a concrete stake — something it's responsible for, something that happens if it's wrong — then list one thing the output will contain because of that role, and send the completed prompt." → one named consequence; anchor 3, `rubrics.md:169`: "The role implies a standard or a body of knowledge, but the prompt doesn't say which parts to draw on."
- Working (`days/15.md:35`): "Write a prompt for {{TASK}} whose role changes what's included, excluded, or assumed. A reader should be able to name at least two things the output does because of the role." → anchor 4, `rubrics.md:170`: "Role changes what is included, excluded and assumed, though the mechanism is only implied, not stated." Working asks *what* the output does, not *how* the role produces it — the mechanism stays implied.
- Advanced (`days/15.md:39`): "Write a prompt for {{TASK}} whose role changes at least two specific things about the output — be ready to name both, and to say how the role produces each one." → anchor 5, `rubrics.md:171`: "Role changes what is included, excluded and assumed, and you can say how."

Strictly monotonic on the exact 4/5 discriminator ("and you can say how"). One of the two or three best-built days.

### Day 16 — `rubrics.md#few-shot-examples`, anchors `rubrics.md:181–185` — see DEFECT-T13

Novice 5, Working 5, Advanced 5. Anchor 4 impossible.

### Day 17 — `rubrics.md#output-schemas`, anchors `rubrics.md:195–199` — see DEFECT-T14

Novice 5, Working 5, Advanced 5. Anchor 4 impossible.

### Day 18 — `rubrics.md#task-decomposition`, anchors `rubrics.md:209–213` — see DEFECT-T15

Novice 5, Working 5, Advanced 5. Anchor 4 unreachable.

### Day 19 — `rubrics.md#reasoning-scaffolds`, anchors `rubrics.md:223–227` — see DEFECT-T16

Novice 4–5, Working 5, Advanced 5. Anchor 4 unreachable; rubric's own 4/5 gap is one phrase wide.

### Day 20 — `rubrics.md#negative-constraints`, anchors `rubrics.md:237–241` — see DEFECT-T17

Novice 5, Working 5, Advanced 5. Anchor 4 impossible.

### Day 21 — `rubrics.md#context-ordering`, anchors `rubrics.md:251–255` — see DEFECT-T18, DEFECT-T19

Novice 1 by instruction, Working 5, Advanced 5. Anchor 4 unreachable.

### Day 22 — `rubrics.md#system-prompts`, anchors `rubrics.md:265–269` — see DEFECT-T20

Novice 4–5, Working 5, Advanced 5. Anchor 4 unreachable; Advanced escalates verification, not anchor.

### Day 23 — `rubrics.md#agent-and-tool-prompting`, anchors `rubrics.md:279–283` — CLEAN

- Novice (`days/23.md:31`): "Write a prompt for {{TASK}} that names which tools to use, roughly when each applies, and a stop condition — all three stated, in any order." → no bar is set on the stop condition's quality, so a vague one satisfies the tier; anchor 3, `rubrics.md:281`: "Tools and rough sequencing are given, but the stopping condition is missing or vague."
- Working (`days/23.md:35`): "Write a prompt for {{TASK}} whose stop condition names a specific, checkable outcome rather than an action taken — something you could verify against the transcript without asking the agent whether it's done." → anchor 4, `rubrics.md:282`: "Which tools, when, and what 'done' means are all stated, though the done-condition could still be gamed." A checkable outcome can still be gamed; the tier never asks the learner to test that.
- Advanced (`days/23.md:39`): "Write a prompt for {{TASK}} whose stop condition is un-gameable. State one way a model could satisfy it without doing the real work, then rewrite the condition so that shortcut no longer counts as done." → anchor 5, `rubrics.md:283`, reached by closing exactly anchor 4's gameability gap.

Strictly monotonic. Notably rubric-aware in the concept text too (`days/23.md:9`: "Stating the condition before the tools is a useful habit, not a scored one").

### Day 24 — `rubrics.md#self-critique-loops`, anchors `rubrics.md:293–297` — see DEFECT-T21

Novice 3, Working 5, Advanced 5. Anchor 4 skipped.

### Day 25 — `rubrics.md#writing-evals`, anchors `rubrics.md:307–311` — CLEAN

- Novice (`days/25.md:31`): "Before writing a prompt for {{TASK}}, write three checks you'll apply to whatever it produces. Only then write the prompt and generate the output." → criteria written first, no specificity bar; anchor 3, `rubrics.md:309`: "Criteria are written and mostly objective, but one is still a judgement call."
- Working (`days/25.md:35`): "Write three criteria for {{TASK}} specific enough that someone else could apply them without asking you what you meant, then generate the output and score it against them unchanged." → anchor 4, `rubrics.md:310`: "Criteria written before the output, specific enough that two people would agree most of the time." Applying without asking is not the same as scoring identically.
- Advanced (`days/25.md:39`): "Write three criteria for {{TASK}} before generating anything. After you see the output, score it against exactly those three — don't add a fourth, and don't soften one it narrowly misses." → anchor 5, `rubrics.md:311`: "Criteria written before the output, specific enough that two people would score the same." The no-softening constraint is a genuine adversarial addition that tests the 4/5 discriminator.

Strictly monotonic; the clearest example in the course of an Advanced tier whose constraint is adversarial *and* on-rubric.

### Day 26 — `rubrics.md#token-economy`, anchors `rubrics.md:321–325` — see DEFECT-T22

Novice 5, Working 5, Advanced 5. Anchor 4 impossible.

### Day 27 — `rubrics.md#failure-diagnosis`, anchors `rubrics.md:335–339` — see DEFECT-T23

Novice 3, Working 5, Advanced 5. Anchor 4 unreachable.

### Day 28 — `rubrics.md#prompt-library`, anchors `rubrics.md:349–353` — see DEFECT-T24

Novice 4, Working 5, Advanced 5. Anchor 4 reachable only via Novice.

### Day 29 — `rubrics.md#capstone`, anchors `rubrics.md:363–367` — CLEAN (capped by design)

- Novice (`days/29.md:29`): "Ask the learner to write a first pass at the production prompt for their named task, run it once, and confirm it produces the deliverable they wanted — anchor 1, the floor everyone starts from." → anchor 1, `rubrics.md:363`: "Prompt works once, on the example it was written against." The tier names its own anchor.
- Working (`days/29.md:33`): "Ask the learner to run their prompt on two cases of the named task that differ from each other, not just from the original, revising it — without rewriting it per case — until it holds up on both." → anchor 2–3, `rubrics.md:364`: "Prompt works on a couple of close variants ..." rising toward `rubrics.md:365`: "Prompt is specified and works on varied cases, but has no written evaluation criteria."
- Advanced (`days/29.md:37`): "Ask the learner to specify the prompt fully — every lever and technique the task actually depends on — then run it on the most different case they can construct from their real work. If it holds, they've reached anchor 3 honestly. Tell them anchor 4–5 is day 30's job, not something to chase today by adding untested claims." → anchor 3.

Anchor 4 is not reachable on day 29, but that is deliberate, stated in the concept (`days/29.md:9–10`) and in the tier itself, and day 30 exists to supply it. Not a defect — though it does mean the two remaining rungs must be distributed correctly on day 30, which they are not (DEFECT-T25, DEFECT-T26).

### Day 30 — `rubrics.md#capstone`, anchors `rubrics.md:363–367` — see DEFECT-T25, DEFECT-T26

Novice 3, Working 5, Advanced 4. Inverted at the top.
