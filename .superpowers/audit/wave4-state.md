# Wave 4 — `SKILL.md` and the state contract

All 22 wave-4 entries executed. Six files changed: `prompting-wizard/SKILL.md`,
`prompting-wizard/assessment.md`, `prompting-wizard/days/27.md`, `days/28.md`, `days/30.md`,
`prompting-wizard/rubrics.md` (FIX-4.22 only, under the re-opening ruling below).

`python3 tools/validate.py --complete` → `ok` (exit 0). `python3 -m unittest discover -s tools` →
103 tests, OK.

No `## ` or `### ` heading was changed anywhere (`git diff -U0 | grep -E '^[+-]#{1,3} '` → empty).
No `## Exercise` tier body was touched. `days/09.md` was not edited.

---

## Entries executed

| Entry | Site(s) | Landed |
|---|---|---|
| FIX-4.01 | `SKILL.md:20` | Day-14 `level` re-derivation, one departure (see D10) |
| FIX-4.02 | `SKILL.md:30`, `:63-83` | `secondary <lever> <score>` field + tie-break rewording |
| FIX-4.03 | `SKILL.md:30` | Conditional mandate; merged with FIX-4.15 (D8) |
| FIX-4.04 | `days/28.md:7,17,22,23` | `{{TASK}}` → `{{DOC}}`; `:34,:38,:42` left live |
| FIX-4.05 | `SKILL.md:79-83`, `days/30.md:25` | `task:` field + day-30 read; sentence 2 preserved (D7) |
| FIX-4.06 | `SKILL.md:13,:14,:16` | (b) literal; (a) departed (D5) |
| FIX-4.07 | `days/30.md:45` | Tier-independent Completion trigger + rebuild fallback (D6) |
| FIX-4.08 | `SKILL.md:73` | Mean rule; day list corrected (D2), N/A clause added (D3) |
| FIX-4.09 | `SKILL.md:77`, `days/27.md:17` | "numeric" added to (a) (D4); (b) literal |
| FIX-4.10 | `SKILL.md:38`, `days/30.md:45` | Completion after state update; day-30 `current_day` write deleted. Step reference disambiguated (D11) |
| FIX-4.11 | `SKILL.md:26` | Literal |
| FIX-4.12 | `SKILL.md:30` | Literal |
| FIX-4.13 | `days/30.md:45`, `SKILL.md:75` | Literal |
| FIX-4.14 | `SKILL.md:14` | Literal |
| FIX-4.15 | `SKILL.md:30` | Merged into the mandate (D8) |
| FIX-4.16 | `days/30.md:25` | Literal, composed with FIX-4.05 |
| FIX-4.17 | `SKILL.md:14` | Literal |
| FIX-4.18 | `SKILL.md:71` | Literal |
| FIX-4.19 | `SKILL.md:59` | Literal |
| FIX-4.20 | `SKILL.md:20`, `:34`, `assessment.md:13` | All three; (b) gains a reconciling clause (D12) |
| FIX-4.21 | `SKILL.md:34` | Literal |
| FIX-4.22 | `rubrics.md:102-103` | **Landed in corrected form** — see the ruling (D1) |

---

## FIX-4.22 — re-opening ruling

**Ruling: `rubrics.md` is re-opened, and FIX-4.22 lands — but not in the plan's literal text. The
plan's replacement breaks `days/09.md`'s settled 3/4/5 ladder. Landed as plurality on anchor 5 only,
with anchor 4 rewritten to positively admit the single-branch case.**

### Why re-opening is warranted

OPEN-3.01 is a live ambiguity in a contract 30 days of scoring depend on: `conjunction` anchors 4 and
5 differ *only* by whether the order of checks is ambiguous, and over one branch there is no order to
be ambiguous about. Nothing in `rubrics.md` said whether anchor 5's discriminator is vacuously
satisfied or unsatisfied over one branch, so `days/09.md`'s Working tier scored 4 or 5 by tutor
convention. Wave 3A deferred the edit here and the checkpoint forbids deferring it again. The only
place a tutor reads the convention is `rubrics.md`, so the fix cannot live anywhere else. Blast
radius is one table row: `conjunction` is cited by `days/09.md:47` (its own ladder), by
`days/14.md:41` (eleven levers, no per-lever ladder derivation), and named as example material at
`days/21.md:31`. Only day 9 has an anchor-derived ladder at stake.

### Why the plan's literal text is wrong

FIX-4.22 puts "Two or more branches" on **both** anchor 4 and anchor 5. `days/09.md:39` (Working)
asks for "one condition, its outcome, and an explicit fallback for everything else" — one branch. A
branch in this ladder is a unit of condition + outcome + fallback: anchor 4 says "each branch stated
with its condition and its fallback", and `days/09.md:43` (Advanced) says "two branches, **each** with
its own condition, outcome, and fallback". The plan's own *Why* concedes it: "Day 9's Working tier
asks for exactly one condition plus a fallback."

Under the literal text, Working satisfies neither 4 nor 5. It cannot fall to anchor 3 either — anchor
3 is "the fallback is missing" and Working mandates a fallback. The plan's line "genuinely
single-branch tasks fall to the not-applicable rule at `rubrics.md:7` or to anchor 3, whichever the
tutor judges" therefore lands day 9's Working at **3, or N/A, at tutor discretion** — a 3/3/5 ladder,
or a 3/N-A/5 one, and the discretion the entry exists to remove reappears one rung lower.

The plan asserts "No day file needs to change either way" and "Day 9's tiers are untouched by this
entry." That is true of `days/09.md`'s **concept**, which was checked and is correct under every
outcome, and false of its **ladder**. Checkpoint item 7's own requirement — "If FIX-4.22 lands,
re-read `rubrics.md`'s `conjunction` row against `days/09.md:39` and `:43` and confirm the ladder
still reads 3 / 4 / 5" — is the test the literal text fails.

### What landed

```
| 4 | Each branch stated with its condition and its fallback, but the order of checks is not fixed — either only one branch is stated, or the wording leaves the order between them ambiguous. |
| 5 | Two or more branches, each stated with its condition and its fallback, in an order that resolves without ambiguity. |
```

This takes the rubric side, as wave 3A recommended, and makes plurality explicit — at the anchor
where the ambiguity actually lives. Anchor 5's ordering discriminator now always has an instance to
test (two or more branches to order). Anchor 4 now names both ways the order fails to be fixed, so a
single-branch prompt with condition, outcome and fallback has one determinate score. Monotonicity
holds: 5 is strictly stronger than 4. `rubrics.md:7`'s not-applicable rule is unchanged and still
governs the *no branch at all* case, which is a different case from *one branch*: a task with no
branch scores N/A, a task with one branch scores on the ladder and tops out at 4.

Nothing else in `rubrics.md` was touched. No global vacuous-vs-unsatisfied convention clause was
added — the plan's rejection fallback — because such a clause would apply to all 26 rubrics and
could move settled ladders in waves 1–3 that nobody re-derived against it. The narrow fix resolves
OPEN-3.01 for every `conjunction` scoring in the course, which is the class the entry names.

**OPEN-3.01 is closed, not deferred.**

### `days/09.md` verification (checkpoint item 7)

`days/09.md` is unedited — confirmed by `git status`; it does not appear in the diff.

Ladder re-read against the landed `conjunction` row:

| Tier | Text | Anchor |
|---|---|---|
| Novice `:33` | "a condition and its outcome — the outcome only, with no fallback for everything the condition doesn't match" | **3** — "Branches and conditions are named, but the fallback (the otherwise) is missing." |
| Working `:39` | "one condition, its outcome, and an explicit fallback for everything else" | **4** — condition and fallback stated; "only one branch is stated", so the order of checks is not fixed. Cannot reach 5, which now requires two or more. |
| Advanced `:43` | "two branches, each with its own condition, outcome, and fallback, ordered so a reader checks them in a fixed sequence with no overlap" | **5** — two or more branches, each complete, in an order that resolves without ambiguity. |

**3 / 4 / 5. Holds.**

Concept correctness under all three outcomes, verified in the file rather than assumed:

- `:7` gives a one-branch example ("If the input is empty ... otherwise process every row") and says
  "Nothing is left to invent" — a statement about invention, not about score. It never claims that
  example is the top rung.
- `:11` — "With more than one condition, order them the way you want them checked, so overlaps
  resolve as you intend" — scopes ordering to plural conditions **already**. The landed anchor 5 says
  the same thing. The concept was ahead of the rubric; this edit makes the rubric agree with the
  lesson rather than the reverse.
- `:13`'s self-test — "the fallback is the last one to close" — describes the 1→4 climb through
  condition, outcome and fallback. It asserts nothing about the 4/5 boundary.

Correct under the landed form, under the plan's literal form, and under outright rejection. No rework
created anywhere.

---

## The N/A rule, end to end

Four sites now, one of them wave 1's. A tutor reading all of them in one session receives no
contradictory instruction.

**`rubrics.md:7` (wave 1, unchanged) — the authority.**

> If the task has no instance of the property the rubric measures — no branch to state, no phrasal
> verb, no competing instructions, no case where an example would teach anything — score the lever
> N/A rather than 1, and leave its `PROGRESS.md` entry untouched.

**FIX-4.20(c) — `SKILL.md:34`, the instruction that *produces* the score.** Before, step 4 said
"criterion by criterion, 1–5, quoting the rubric's anchor for each score you give" — no legal N/A
value and no anchor to quote. Now (the FIX-4.21 rewrite of the same line carries it):

> Score the prompt against each rubric named in the day's `## Rubric` section, 1–5, quoting the
> anchor you are scoring against. […] Where `rubrics.md`'s not-applicable rule applies, write `N/A`
> in place of a number and name the missing property instead of quoting an anchor — the task has no
> instance of it to score.

**FIX-4.20(a) — `SKILL.md:20`, where the score is *recorded*.**

> A lever scored N/A under `rubrics.md`'s not-applicable rule is left untouched in `## Levers`,
> exactly as if the day had not scored it, and is recorded in the `## Log` line as `N/A` rather than
> as a number.

**FIX-4.20(b) — `assessment.md:13`, day 0.**

> Score all three together against each of the 11 levers, 1–5, using `rubrics.md`. One score per
> lever, not per prompt. Take the median where the three prompts disagree. Where `rubrics.md`'s
> not-applicable rule applies — a prompt gives a lever nothing to score — take the median of the
> prompts that do give it something; if none of the three does, record 3 and note it, so the mean
> that sets `level` is not skewed by a property the learner's prompts never exercised. Day 0 is the
> one place `N/A` is not written: all eleven `## Levers` keys carry a number before the course starts.

**Why the four are consistent.** `rubrics.md:7` grants the state and says what happens to the
`PROGRESS.md` entry. `SKILL.md:34` tells the tutor what to write during scoring — the site that was
still forcing a number, and the reason (c) was added in wave 1 round 2. `SKILL.md:20` tells them
where it goes: nowhere in `## Levers`, `N/A` in the Log. `assessment.md:13` carves day 0 out
explicitly and *names the rule it is carving out of*, so the carve-out reads as a scoped exception
rather than a second, contradictory instruction. The carve-out is necessary and not arbitrary:
`rubrics.md:7`'s remedy is "leave its `PROGRESS.md` entry untouched", and at day 0 there is no entry
to leave untouched — the file does not exist yet — while `assessment.md:78` requires all eleven keys
and `assessment.md:46-52` computes a mean over them.

Two downstream compositions were closed so no reader meets a non-number it cannot parse:
`SKILL.md:73` excludes N/A scores from the multi-rubric mean, and `SKILL.md:77` defines a scored day
as one carrying a **numeric** `rubric N` field, which keeps `days/27.md:17`'s lowest-score search off
both the Day 0 line and any `rubric N/A` line.

**What a day-0 assessor now records for a lever the learner's three prompts never exercise: `3`, with
a note.** Not `N/A`, not `1`. Three is the midpoint, so the lever neither promotes nor demotes the
tier the mean sets, and `## Levers` still carries eleven numbers on the day the course starts.

---

## `PROGRESS.md` traced through a full 30-day run

Every field, after this wave. No field is read-but-never-written, and no field is written in a format
its reader cannot parse.

| Field | Written by | Read by | Format contract | Status |
|---|---|---|---|---|
| `level` | `assessment.md:61` (day 0); **`SKILL.md:20` after day 14** | `SKILL.md:16`, `:30` | `novice` / `working` / `advanced`, from `assessment.md`'s "Setting the level" table | **Fixed** — was write-once, read 30× |
| `current_day` | `assessment.md:62` (creation, =1); **`SKILL.md:20` — sole updater** | `SKILL.md:16`, `:17`, `:18` | whole number 1–31, enforced at `SKILL.md:14` | **Fixed** — `days/30.md:45`'s write deleted; lower bound and integrality now guarded |
| `## Levers` | `assessment.md:64-67` (all eleven, numeric); `SKILL.md:20` (only levers the day scored; N/A leaves the entry untouched) | `SKILL.md:16`, `:30`, `:20` (day-14 mean); `days/14.md:25`; `days/21.md:31`; `days/30.md:45` | `lever: N`, eleven keys always present | OK |
| `## Tasks` | `assessment.md:42`, `:69-72` | `SKILL.md:16`, `:24`, `:28`, **`:30` (preamble now presented, so the "pick one" branch is live)**; `days/14.md:29`; `days/21.md:35` | 3–5 entries, count enforced at `SKILL.md:14` | **Fixed** — count validated; pick-one no longer dead |
| `## Log` section | `SKILL.md:20` (append per day); `assessment.md:75` (Day 0 line) | `SKILL.md:30`; `days/27.md:17`, `:25`; `days/30.md:17`, `:25`, `:45` | required and parseable per `SKILL.md:14`; in the read list at `:16` | **Fixed** — was neither required nor read |
| `## Log` Day 0 baseline line | `assessment.md:75`, mandated `:78` | `days/30.md:45` | documented at `SKILL.md:77`: level, diagnosis count, eleven baselines, **no** `rubric N` field | **Fixed** — shape documented; absence disclosed at `SKILL.md:13` and handled at `days/30.md:45` |
| Log field 2 (topic) | `SKILL.md:20` per `:71` | `days/27.md:17`; `SKILL.md:75` | the day's lever or technique as it appears in the day file's title — one value | **Fixed** — defined; day 27 no longer calls it "the task" |
| Log field 3 (`self N, rubric N`) | `SKILL.md:20`, `:36` | `days/27.md:17` | one integer; on days 6, 7 and 14 the mean of that day's rubric scores, rounded, N/A excluded (`SKILL.md:73`) | **Fixed** — single-slot ambiguity resolved |
| Log `secondary <lever> <score>` | **`SKILL.md:20` per `:69`** | `SKILL.md:30` (tie-break and last-session exclusion); `SKILL.md:75` (staleness) | written only when a secondary was added; omitted otherwise | **Fixed** — was read, never written |
| Log `task:` (day 29 only) | `days/29.md:25`, format at `SKILL.md:79-83` | `days/30.md:17`, `:25` | `task: "…"`, in the learner's words, after the score fields | **Fixed** — field now exists; `days/30.md:25` has a fallback when it does not |
| Level re-derivation input | mean over `## Levers`, `SKILL.md:20` | `SKILL.md:20` | eleven numbers; the diagnosis adjustment is excluded as day-0-only | **Fixed** — was defined but never run after day 0 |

### Session-by-session walk

**Day 0.** `assessment.md` writes `level`, `current_day: 1`, eleven numeric `## Levers`, 3–5
`## Tasks`, and the Day 0 `## Log` line. A lever no prompt exercised gets 3 with a note.

**Days 1–13.** Each session: `SKILL.md:14` validates; `:16` reads five things including `## Log`;
`:30` presents the `## Exercise` preamble (so the learner is actually invited to pick a task) and the
tier for `level`, then picks at most one secondary constraint from the levers at ≤2, excluding last
session's secondary and any lever the day's own `## Rubric` scores. Step 4 scores, with N/A available.
Session step 6 appends the Log line — including `secondary <lever> <score>` when one was added —
rewrites the levers the day scored, and increments `current_day`.

**Day 14.** Eleven rubrics; the Log line's `rubric N` field carries their rounded mean, the eleven
individual scores go to `## Levers`. No secondary constraint is possible (every lever is the day's
own), which is correct: the day rescores everything anyway. Session step 6 then recomputes the mean
over `## Levers` and rewrites `level` — the one re-derivation. A learner assessed `novice` at 2.3 who
now averages 4.2 gets `advanced`, and day 15 serves the Advanced tier.

**Days 15–28.** Technique days. Only the secondary constraint can move a lever, per `SKILL.md:20`
and `:30`. `SKILL.md:75` records that field 2 and the `secondary` field are what make a lever's last
rescoring recoverable — the input day 30 needs for its staleness note. Day 27 reads `## Log` for the
scored day with the lowest `rubric` score, most recent on a tie, skipping the Day 0 line and any
`rubric N/A` line. Day 28 shows a literal `{{DOC}}` in its concept and Before/After — no collision
with `SKILL.md:24` — and keeps `{{TASK}}` live in its three tiers, where substitution is wanted.

**Day 29.** The preamble is now executed (`SKILL.md:30`), so the learner's named task is actually
recorded, into the `task:` field the format now defines.

**Day 30.** The preamble reads the `task:` field, or falls back to asking for task and prompt if
there is no day-29 line. Session step 6 runs first: Log line appended, any secondary-scored lever
written, `current_day` → 31. `## Completion` then runs — "when day 30's critique is complete,
whatever the learner's tier" — reads the Day 0 baselines, shows them against the *post-update*
`## Levers`, and notes which levers have not been rescored since day 14. If the file was rebuilt
mid-course and has no Day 0 line, it says so and shows current scores alone.

**Day 31+.** `SKILL.md:17` reports the course complete. `SKILL.md:20` is the sole updater of
`current_day`; nothing else writes it.

### Checkpoint item 3 — three sessions simulated against `assessment.md:58-76`

Baseline: `noun 4, verb 3, adjective 2, adverb 3, pronoun 2, preposition 4, conjunction 3,
determiner 3, numeral 5, interjection 4, particle 2`; `## Log` holds the Day 0 line only.

- **Day 1** (`noun`). Qualifying at ≤2: adjective, pronoun, particle — a three-way tie. The Day 0
  line carries no `secondary` field, so there is no last-session secondary and none of the three has
  ever been used as one. Under the tie-break as landed — never-used counts as least-recently-used,
  then first in `## Levers` order — the choice is **adjective**. Determinate. The day's own lever,
  `noun`, does not qualify, so the exclusion is not exercised.
- **Day 2** (`verb`). Day 1's line records `secondary adjective N`. If adjective was scored 3 it no
  longer qualifies; if it was scored 2 it is excluded as last session's secondary. Either way the
  qualifiers are pronoun and particle, neither ever used as a secondary, and `## Levers` order gives
  **pronoun**. Determinate, and the no-consecutive-repeat intent holds without contradicting the
  mandate — the old rule pair had no answer here at all.
- **Day 8** (`pronoun`), with pronoun the only lever at 2. `pronoun` is the lever day 8's own
  `## Rubric` scores, so it is excluded; nothing else qualifies; **add none this session**.
  Determinate, and it never lands on day 8's own lever.

### Checkpoint item 4 — a novice completing day 30

`level: novice`, `current_day: 30`. The daily loop runs the Novice tier (three checks, close variant,
nothing written about breakage). Session step 6 appends the Log line, writes any secondary-scored
lever, and sets `current_day` to 31. `## Completion` then fires — its trigger is "when day 30's
critique is complete, whatever the learner's tier", with no reference to a revised prompt, a second
case, or "both" — and reports `## Levers` **after** the update, so a secondary lever scored 4 this
session prints as 4, not as the 2 it was at session start. The ceremony a novice previously never saw
now runs.

---

## FIX-3.22 — per-file `## Concept` / `## Before / After` check

Run against every day file this wave opened, whether or not the wave edited it, and whether or not
anything was found. Every sentence of each concept and each Before/After was read against that day's
own Novice and Working tier text.

**`days/09.md` — opened read-only for the FIX-4.22 ruling. Clean.**
`:5` names the defect the seed has, not a state any tier mandates. `:7`'s one-branch example asserts
completeness, not a score. `:9` — "the fallback can be missing, which gets you partway" — is the
Novice tier's exact mandated state, named as a rung (FIX-3.21(d)'s landed wording). `:11` scopes
ordering to "more than one condition", which is the Advanced tier's state and not a demand on
Working's single branch. `:13`'s self-test enumerates the 1→4 climb and asserts nothing about 4/5.
Before/After `:19-25`: the After is a one-branch conditional with condition, outcome and fallback —
anchor 4 under the landed row, which is the Working tier's target, so an imitator of the After reaches
Working's rung and not Advanced's. No sentence instructs or condemns a state Novice or Working
mandates or forecloses.

**`days/17.md` — opened read-only (no wave-4 entry edits it). Clean, with one close call recorded.**
`:5` condemns unfalsifiable prose ("nice"), which no tier mandates. `:7` defines what makes a schema
checkable — a definition of the top state, and `:18`'s self-test explicitly ladders it: "fields
enumerated, with types and order unstated, is a rung of its own; an exact structure with empty values
unaddressed is the climb from there; a structure output can be checked against mechanically … is the
top". Novice mandates the first, Working the second. **Close call:** `:16`'s closing clause — "'list
the results with a status and a note' can't be checked that way at all" — describes something near
the Novice tier's mandated output (a plain list of field names, no types). It is a true statement
about mechanical checkability, not a condemnation: `output-schemas` anchor 3 is "Fields are
enumerated, but types, order, or optionality are left unstated", which is precisely where Novice
lands, and `:18` names that state "a rung of its own". The concept never says a prompt must be
script-checkable; it says script-checkability is the top. Clean, and recorded here so the next wave
does not have to re-derive it. Before/After `:24-39`: the After is a full anchor-5 schema; the tiers
below it are foreclosed by their own wording ("no types and no example values"), so the
imitate-the-After route is closed. Nothing found; nothing edited.

**`days/27.md` — `## Before / After` edited at `:17`, so the check was re-run in full. Clean.**
`:5` and `:7` describe diagnosis; Novice names a lever, which is a subset of `:7`'s "levers or
techniques" — a superset is not a foreclosure. `:9` — "The fix has to target only what you named" —
governs fixes; the Novice tier makes no fix ("no fix today"), so `:9` is unexercised rather than
violated, and it has not been turned into a tier-level demand (wave 3's checkpoint item 17). Working
diagnoses, then runs, then fixes; `:9`'s "diagnose on paper first, before you run anything" is
satisfied. `:11`'s self-test is satisfied by all three tiers. The edited `:17` is tutor direction,
covered by the extended `SKILL.md:26`, and mandates nothing of any tier; it now names the day's
*topic* rather than "the task", which is what the Log line actually carries. `:21`'s "Where the tier
also asks for a fix" keeps FIX-3.20's scoping intact, so a Novice learner is still not told aloud to
write the fix their tier forbids. No collision.

**`days/28.md` — `## Concept` edited at `:7` and `## Before / After` at `:17`, `:22`, `:23`. Clean.**
The edit is a token rename inside an illustrative string; it adds and removes no claim, and the
concept's word count is unchanged. `:5` is a motivation sentence. `:7` — "stays low on the shelf
until two more things are marked" — is immediately laddered by `:9`, "Marking the slot without the
failure gets you partway", which is the Novice tier's mandated state (slots only, "nothing yet about
how it has failed") named as a rung. Working adds the failure notes `:9` calls the climb. `:11`'s
self-test is untouched, per CONFLICT-07's ruling and wave 3's checkpoint item 5. The Before/After now
shows `{{DOC}}` in the template and the slot line, so the After is a template *with a slot in it* when
presented — the defect FIX-4.04 exists to close — and no tier's mandated state is condemned.

**`days/30.md` — `## Exercise` preamble edited at `:25` and `## Completion` at `:45`. Neither is a
`## Concept`, a self-test line, or a `## Before / After`, so wave 3C's re-check trigger is not tripped;
the check was run anyway. Clean.**
`:7`'s three parts end with "is the top rung's addition", which scopes documenting breakage away from
the Novice tier that forecloses it (FIX-3.19's landed wording). `:9` quotes the settled capstone
anchors and attributes the unfamiliar case to anchor 5, which is above Novice's close variant. `:11`'s
self-test — "run your day-29 prompt on a close variant, then on a case you didn't build it for. The
second is the climb" — names Novice's close variant as the first step, not a failure. `:17` and `:21`
were not touched. The edited `:25` is tutor direction that adds a fallback and forecloses nothing.
The edited `:45` is tier-independent by construction — that is the entry's point — and reports
post-update scores.

---

## Word counts

No `## Concept` gained or lost a word this wave. Recounted with `validate.py`'s own `section()` plus
`len(str.split())`, after the edits:

| Day | Words | Headroom | Change |
|---|---|---|---|
| 09 | 197 | 3 | unedited |
| 17 | 184 | 16 | unedited |
| 27 | 174 | 26 | unchanged (edit was in `## Before / After`) |
| 28 | 181 | 19 | unchanged (`{{TASK}}` → `{{DOC}}` is word-neutral) |
| 30 | 195 | 5 | unchanged (edits were in `## Exercise` and `## Completion`) |

**No addition to any concept, so no deletion was needed to pay for one.** All five figures match the
wave-3C census exactly. `SKILL.md`, `assessment.md`, `rubrics.md`, `## Exercise` preambles and
`## Completion` carry no word cap.

---

## Departures from the plan's literal text

Twelve. Four are substantive.

**D1 — FIX-4.22 landed in corrected form. Substantive.** Full reasoning in the ruling above. The
plan's literal replacement puts plurality on anchors 4 *and* 5, which strands `days/09.md`'s Working
tier below anchor 4 and turns a settled 3/4/5 ladder into 3/3/5 or 3/N-A/5, failing checkpoint item
7's own test. Landed with plurality on anchor 5 and anchor 4 rewritten to admit the single-branch
case explicitly.

**D2 — FIX-4.08's day list is "days 6, 7 and 14", not "days 6, 7, 14 and 21".** Day 21's
`## Rubric` at `days/21.md:47` names one rubric, `context-ordering`. FIX-2.21(b) was **rejected** in
wave 3B ("Closed as ACCEPTED. FIX-2.21(b) is rejected. `days/21.md:47` keeps its single rubric
citation"), and the plan's own "Wave 2 → wave 1" back-edge makes day 21's inclusion conditional on
that entry landing: "FIX-2.21(b) makes day 21 a multi-rubric day … which must then list days 6, 7, 14
**and 21**." It did not land, so day 21 is not listed. Verified in `days/21.md`, not inferred.

**D3 — FIX-4.08 gains "A rubric scored N/A is left out of the mean."** FIX-4.08 and FIX-4.20 compose
on days 6, 7 and 14: FIX-4.20 makes a rubric score potentially non-numeric, and FIX-4.08's mean is
undefined over a non-number. Day 14 scores eleven levers on one prompt and is the likeliest place an
N/A appears. One clause, no new mechanism.

**D4 — FIX-4.09(a) reads "Only lines carrying a **numeric** `rubric N` field are scored days."** One
word, same composition. Without it, a single-rubric day logged `rubric N/A` is a "scored day" whose
score `days/27.md:17` cannot compare, which is the parse failure FIX-4.09 exists to prevent, arriving
by a different door.

**D5 — FIX-4.06(a) departed. Substantive.** The plan requires "a parseable Day 0 `## Log` line" in
the failed-field list at `SKILL.md:14`. That directly contradicts FIX-4.06(b), landed one line above
it, which preserves rebuild-from-a-day-number as a real learner choice made "knowing that" the Day 0
baseline is gone: a rebuilt file has no Day 0 line, so on the very next session `:14` would name the
failed field and stop, every session, forever — the learner is offered a choice the next session
refuses to honour. Landed instead as: `## Log` itself is the required field (which is what FIX-4.06's
own *Why* argues for — "it is in neither the required-field list nor the read list"), its lines must
be parseable, and an empty `## Log` on a rebuilt file is explicitly **not** a failed field. This is
enforceable — a session can check whether `## Log` exists and parses, but cannot check whether the
file's history entitles it to be empty.

**D6 — `days/30.md:45` gains a rebuild fallback. Substantive, and the consequence of D5.** Once a
rebuilt file legitimately reaches day 30 with no Day 0 line, FIX-4.07's replacement text reads that
line unconditionally and has nothing to read. Added: "If `PROGRESS.md` was rebuilt mid-course and
carries no Day 0 line, say so and show the current scores alone." Same shape as FIX-4.16's fallback
for the day-29 line, and it makes `SKILL.md:14`'s promise ("day 30 says so when it reaches the
baseline comparison") true.

**D7 — `days/30.md:25` keeps its existing second sentence.** The plan quotes `:25` as one sentence
and replaces it, but the line in the file has two, and the second — "The log line does not carry the
prompt, so ask the learner to paste the prompt they built on day 29" — is load-bearing: day 30 cannot
run without the prompt. Sentence 1 was replaced as specified, sentence 2 preserved, and the fallback
appended reads "ask the learner for the task as well as the prompt" so it composes with the sentence
that already asks for the prompt.

**D8 — FIX-4.03 and FIX-4.15 merged, with one determinacy tail covering both exclusions.** The plan
gives FIX-4.03 an "add none this session" tail for the last-session case and FIX-4.15 a bare
prohibition with no tail, so a day whose only qualifying lever is the day's own lever — checkpoint
item 3's day-8 scenario exactly — has no stated outcome. Landed as one sentence covering both: "If
setting aside last session's secondary and the day's own levers leaves nothing qualifying, add none
this session." FIX-4.15's clause is also plural-tolerant ("a lever the day's own `## Rubric` already
scores"), because days 6, 7 and 14 score several.

**D9 — the tie-break was made total. Substantive.** Checkpoint item 3 requires the choice be
"determined at every step", and the plan's tie-break — "whichever you have used least recently as a
secondary constraint" — returns three candidates on day 1 of the assessment example, where adjective,
pronoun and particle are all at 2 and none has ever been used as a secondary. Added: "a lever never
used as one counts as least recently used, and among those take the first in `## Levers` order."
`## Levers` has a fixed eleven-key order in `assessment.md:65-67`, so this always resolves.

**D10 — FIX-4.01's "tell the learner their tier changed" → "tell the learner if their tier changed".**
The re-derivation runs on every learner at day 14 and most tiers will not move; the literal text
instructs the tutor to announce a change that did not happen.

**D11 — FIX-4.10(a)'s "in step 6 above" disambiguated.** Both the daily loop and `## Every session`
have a step 6, and the entry's whole point is that Completion must run after the *session's* step 6.
Landed as "after the session's state update — step 6 of `## Every session`, not of this loop".

**D12 — FIX-4.20(b) gains a reconciling clause.** The plan's literal append tells a day-0 assessor to
record 3 where `rubrics.md:7` tells them to score N/A, with nothing naming the relationship between
the two instructions — a tutor reading both in one session sees a bare conflict, which is the failure
mode FIX-4.20 exists to remove. Landed with the rule named ("Where `rubrics.md`'s not-applicable rule
applies") and the exception stated ("Day 0 is the one place `N/A` is not written: all eleven
`## Levers` keys carry a number before the course starts").

---

## Wave-4 checkpoint

1. **`validate.py --complete` exits 0.** ✅ The validator makes no assertion about `{{TASK}}`
   anywhere — checked in `tools/validate.py`, which tests headings, concept word count, tier
   presence, rubric slugs and absolute paths only — so the `{{DOC}}` rename cannot break placeholder
   handling. 103 unit tests pass.
2. **Lifecycle table walked row by row.** ✅ See the trace above. All five previously-broken rows now
   have a writer, a reader and a documented format: `level` (day-14 re-derivation), the
   secondary-constraint record (`secondary` field), the day-29 task (`task:` field), the Day 0
   baseline line (documented at `SKILL.md:77`), `## Log` itself (required at `:14`, read at `:16`).
3. **Three sessions simulated.** ✅ Days 1, 2 and 8 above. Determinate at every step; day 8 adds no
   secondary rather than landing on its own lever.
4. **Novice completing day 30.** ✅ Ceremony fires; scores are post-update.
5. **`days/30.md` no longer writes `current_day`.** ✅ Its only remaining mention is the closing
   sentence's read-only reference to `SKILL.md:17`'s rule. `SKILL.md:20` is the sole updater;
   `assessment.md:62` writes the initial value at file creation, which is not an update.
6. **`{{TASK}}` inside a `## Concept`.** ✅ Day 28 is no longer a hit. The remaining hits — days 02,
   03, 04, 05, 09, 10, 11, 13, 15, 19, 22, 23, 24 — are all intended substitution sites.
7. **OPEN-3.01 closed, not deferred.** ✅ FIX-4.22 landed under the re-opening ruling above.
   `days/09.md` **not** edited; its ladder re-read against the landed `conjunction` row and confirmed
   3 / 4 / 5.

---

## Notes for wave 5

- `days/09.md`'s concept `:11` and the landed `conjunction` anchor 5 now say the same thing about
  plural branches. If wave 5 touches `:11`, the anchor is the contract.
- The concept-cap census is unchanged by this wave; all sixteen tight days keep the headroom
  `wave3c-concepts.md` recorded.
- `days/17.md:16`'s "can't be checked that way at all" is recorded above as checked and clean. Wave 5
  opens `days/17.md` for prose; if it edits `:16` or `:18`, the FIX-3.22 check must be re-run,
  because `:18` is what ladders `:16`.
- `SKILL.md:14` is now a long line carrying five distinct failure rules. Wave 5 may want to break it
  into a list; that is formatting, not contract. **Filed as FIX-5.12(e).**

---
---

# Wave 4 — round 2

Three items from the gate. One shipped-file change, in `assessment.md` only. `rubrics.md`, all thirty
day files, every `## Exercise` tier body and every heading are untouched this round — verified with
`git diff --name-only -- prompting-wizard/rubrics.md prompting-wizard/days/`, which returns nothing.
No `## Concept` word count changed, by construction: no day file was opened for edit.

`python3 tools/validate.py --complete` → `ok` (exit 0). `python3 -m unittest discover -s tools` →
103 tests, OK.

## 1. `assessment.md`'s no-skew claim — the arithmetic is now true

**The finding is correct and the shipped text was false.** Round 1 recorded 3 for an unexercised
lever "so the mean that sets `level` is not skewed", and then counted that 3 in an eleven-lever mean
whose bands (2.5 and 4.0) are not symmetric about 3. The imputation moved learners in both
directions, and it did so on the one number the sentence told the tutor was safe.

Both of the gate's worked cases, re-run against the landed text:

| Case | Round 1 | Round 2 |
|---|---|---|
| Ten exercised levers summing to 40, one imputed 3 | 43/11 = 3.909 → `working` — **demoted** | 40/10 = **4.0** → `advanced` |
| Nine exercised summing to 22, two imputed 3s | 28/11 = 2.545 → `working` — **promoted** | 22/9 = **2.44** → `novice` |

The imputation no longer moves anyone. Landed at `assessment.md:13`:

> Where `rubrics.md`'s not-applicable rule applies — a prompt gives a lever nothing to score — take
> the median of the prompts that do give it something. Where none of the three gives it anything,
> record 3 and note it, and leave that lever out of the mean under "Setting the level": average only
> the levers the three prompts actually exercised, so the level is not skewed by a property they
> never touched. An imputed 3 counted in an eleven-lever mean drags it toward 3, and the bands either
> side of 3 are not symmetric, so counting it can move the learner a whole tier. Day 0 is the one
> place `N/A` is not written: all eleven `## Levers` keys carry a number before the course starts.

`assessment.md:78`'s "All 11 lever keys must be present" is preserved — the 3 still goes into
`## Levers`; it is only excluded from the average.

**One addition beyond the single clause requested, and why.** A tutor can reach "Setting the level"
and read its table — "Mean lever score below 2.5" — without carrying `:13`'s qualifier with them, and
the table is where the mean is actually taken. One sentence was added directly above the adjustment
paragraph: *"The mean is taken over the levers the three prompts actually exercised, per Part 1 — not
over any lever recorded as an imputed 3."* Without it the fix lives only at the site that computes the
scores, not at the site that consumes them — the same split-contract shape as the defects this wave
exists to close. `assessment.md` carries no word cap.

**Residue filed, not fixed: FIX-5.13(b).** `SKILL.md:20`'s day-14 re-derivation still averages all
eleven `## Levers` entries, and a lever imputed at day 0, never taught on days 1–13, and N/A again on
the day-14 prompt still sits in that mean as a 3. The window is narrow — day 14 rescores all eleven,
so only a lever N/A *on that prompt* survives — and closing it properly needs a state field recording
which levers have ever been exercised, which is a contract change, not a clause. Filed with that
reasoning so wave 5 decides rather than inherits it silently. The two means now differ and nothing in
the file explains why; that is the part which must not stand unaddressed.

## 2. M-7 — the thirteenth departure

**D13 — FIX-4.20(b)'s first N/A clause was rewritten, not appended. Substantive, and undocumented in
round 1.** The plan's literal text reads:

> If none of the three prompts gives a lever anything to score, take the median of the ones that do;
> if none does, record 3 and note it…

The first clause is self-defeating: its condition is "none of the three gives the lever anything to
score" and its instruction is "take the median of the ones that do" — of which, by that condition,
there are none. The two halves are the *same* condition with different remedies. Landed as two
separate conditions — partial coverage takes the median of the prompts that do score it, total
absence records 3 — which is plainly what the entry intends. Round 1 described D12 as covering only
the reconciling clause added at the end of the sentence; the rewrite of the opening clause was a
second, independent departure and is now on the list. **Departure count for wave 4: thirteen, five
substantive** (D1, D5, D6, D9, D13).

## 3. M-8 — FIX-3.22 run on the four files opened without recording it

`days/06.md`, `days/07.md`, `days/14.md` and `days/21.md` were opened in round 1 to verify D2 and
FIX-4.08's day list, and the check was not recorded. The mandate reads "any wave opening a day file
**for any reason**", and it exists precisely because two defects survived being named by an entry.
Run in full; results recorded in `MASTER-FIX-PLAN.md` under FIX-3.22's standing consequence, and
summarised here. **The likely outcome — all four clean — did not hold.**

**`days/06.md` — clean; one close call.** `:5`, `:7`, `:9` describe composition and the Novice tier
sets all five levers too, weakly, so nothing it mandates is condemned. `:11`'s deletion test ("If the
sentence still reads as a full instruction with one gap, that lever wasn't pulling weight") is an
Advanced-rung diagnostic — `:39` is the tier it tests — presented as "the test" on a day whose Novice
tier is built to produce levers that fail it, and day 06's concept carries no rung or partway language
anywhere. It names a property rather than instructing a state, so it is not a mandate-vs-foreclosure
collision. Recorded against FIX-5.01's live `days/06.md:11` row, which already rewrites that exact
line; budget after the opener swap is 191 of 200, so nine words are available if wave 5 wants a
scoping clause.

**`days/07.md` — DEFECT. Filed as new entry FIX-5.11.** `:7` reads "The job is to work out which of
the five levers … was left open, and rewrite until none of them are." `:29`, the Novice tier, reads
"State which **one** of the five levers … was most clearly missing … then rewrite **only that lever**
in." `## Concept` is read aloud verbatim (`SKILL.md:28`) and is in the second person, so a Novice
learner is told the job is to close all five and then told to close one. The day's self-test at `:11`
does not cover it: "Setting all five levers is the climb; leaving no clause whose deletion changes
nothing is the rung above" ladders Working against Advanced and is silent on the one-lever rung. That
sentence was **added by FIX-3.05** — the wave-3 entry that opened this file wrote the laddering
sentence and still left `:7` uncovered, which is the exact failure mode FIX-3.22 names.

Not fixed in this wave: it is a `## Concept` edit on a day no wave-4 entry opens, and the budget is
tight — `days/07.md` is at **197** of 200. Filed with two counted candidates so wave 5 does not have
to re-derive them: "was left open; one closed is a rung, all five the climb" → **199**, and "was left
open; closing one is a rung, closing all five the climb" → 200. Both recount with `validate.py`'s own
`section()` plus `len(str.split())`.

**`days/14.md` — clean; one close call.** `:9` is CONFLICT-03-protected and untouched. The Novice
tier goes through all eleven levers, which is exactly what `:9` requires ("every lever considered"),
and sets three. `:11`'s "A score of 2 or below is a dimension you thought you'd covered and hadn't"
mildly misdescribes the Novice tier's *deliberate* leaving of eight — the tier has the learner state
what each currently sets — but it names, it does not instruct. Worth recording: `:17` and `:21` are
third-person direction about the learner and so are **not read aloud**, per `SKILL.md:26` as extended
by FIX-4.11. That is what stops `:21`'s "deliberately setting all eleven levers" reaching a learner
whose tier tells them to set three — a collision FIX-4.11 closed as a side effect, on a day nobody
filed it against.

**`days/21.md` — clean.** `:11` ladders all three tiers explicitly and in order — "Constraints
scattered through the material is where this starts; all but one grouped at the end is the climb from
there; every one grouped last is the top" — matching `:35` / `:39` / `:43` one to one, which is
FIX-3.13's landed work and the cleanest example of the pattern in the course. `:9`'s "pure reorder,
not a trim" is what all three tiers mandate. `:5` condemns the buried-instruction state, which the
Novice tier *constructs* as its starting material and then moves; the tier's product has the
instruction at the top, so nothing it mandates is condemned. The Before/After models the Advanced
state and both lower tiers are foreclosed in their own words.

## Filed for wave 5

Three new entries in `MASTER-FIX-PLAN.md`, placed after FIX-5.10, plus wave 5's "Files touched" list
corrected — it omitted `days/07.md`, `days/10.md`, `days/21.md`, `days/30.md` and `SKILL.md`, which
FIX-5.09 through FIX-5.13 now require.

- **FIX-5.11** — day 07's concept-vs-Novice collision above. Severity medium; carries the counted
  replacement candidates and the do-not-touch constraints.
- **FIX-5.12** — the six harness prose seams, as lettered sub-items: **(a)** M-2, field 2 undetermined
  on days 6, 7 and 14, which makes `SKILL.md:75`'s recoverability claim inexact there; **(b)** M-3,
  `days/30.md:45` and `SKILL.md:38` wording the Completion trigger differently, where the day file's
  reading reproduces the S10 defect FIX-4.10 closed; **(c)** M-4, no forward pointer from session step
  6 to the deferred Completion; **(d)** M-5, `SKILL.md:38`'s "whatever the learner's tier" trailing
  three em-dash clauses; **(e)** M-6, the rebuild path's missing output specification, paired with
  breaking `SKILL.md:14` into a list; **(f)** M-9, `SKILL.md:24` and `:28` still stating substitution
  differently, which now matters because FIX-4.12 made the pick real.
- **FIX-5.13** — the level-arithmetic residues: **(a)** M-1, half-integer lever scores reachable at day
  0 via a two-prompt median against an otherwise-integer contract; **(b)** the day-14 mean still
  counting a day-0 imputation, described above; **(c)** gate item 7, a learner promoted by the day-0
  diagnosis adjustment and visibly demoted at day 15 when the re-derivation drops it — specified
  behaviour with nothing preparing the learner for it.

## Round-2 verification

- `python3 tools/validate.py --complete` → `ok`, exit 0.
- `python3 -m unittest discover -s tools` → 103 tests, OK.
- No `## Concept` word count changed: `git diff --name-only -- prompting-wizard/days/` is empty, so no
  concept was opened for edit.
- No tier body changed, no heading in any shipped file changed, and `rubrics.md` was not touched —
  `git diff --name-only -- prompting-wizard/rubrics.md` is empty.
- Shipped-file diff for this round: `prompting-wizard/assessment.md` only, 3 insertions, 1 deletion.
