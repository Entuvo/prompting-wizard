# Wave 1 — `prompting-wizard/rubrics.md`

Status: **complete**. 27 of 27 entries applied. One file touched: `prompting-wizard/rubrics.md`
(+64 / −60). No `## ` heading changed. `tools/` untouched.

## Verification

| Check | Result |
|---|---|
| `python3 -m unittest discover -s tools` | 103 tests, OK |
| `python3 tools/validate.py --complete` | `ok`, exit 0 |
| 26 `## ` headings vs pre-wave copy | byte-identical (`diff` empty) |
| 26 slugs resolve | yes |
| `rubrics.md#slug` citations across 30 day files | 26 distinct, 0 unresolved, 0 headings uncited |
| SYS-1 acceptance grep on anchor-4 rows | no `mostly` / `minor` / `loosely` / `only cosmetic` / `most of the time` / `somewhat` / `a small stretch` / `in most cases` |
| Checkpoint 4 (anchor 5 not satisfiable by an anchor-4 prompt) | passes for all 26 |
| Day 23 / 25 / 29 tier mapping | 3/4/5, 3/4/5, 1 / 2–3 / 3 — unmoved |

The 26 slugs, in file order: `noun`, `verb`, `adjective`, `adverb`, `pronoun`, `preposition`,
`conjunction`, `determiner`, `numeral`, `interjection`, `particle`, `role-framing`,
`few-shot-examples`, `output-schemas`, `task-decomposition`, `reasoning-scaffolds`,
`negative-constraints`, `context-ordering`, `system-prompts`, `agent-and-tool-prompting`,
`self-critique-loops`, `writing-evals`, `token-economy`, `failure-diagnosis`, `prompt-library`,
`capstone`.

## The two systemic fixes

**SYS-1 — "anchor 4 is anchor 5 with a hedge."** Applied as the governing rule for every anchor
rewritten in this wave: anchor 5 states the discriminating property positively, anchor 4 names a
countable shortfall. This is what FIX-1.02, 1.04, 1.05, 1.06, 1.07, 1.08, 1.09, 1.12, 1.16, 1.17,
1.21, 1.22, 1.23, 1.24, 1.25, 1.26, 1.27 all are — they are not 17 independent edits but one rule
applied 17 times. Source findings closed: **R02, R05, R08, R10, R11, R17, R21, R22, R23, R29, R31,
R33, R34, R36, R39** (15), and the root cause of **T01, T06, T11, T15, T16, T20, T21, T22, T24**
(9 tier findings) is removed — every one of those days now has an anchor-4 rung with a positive
shortfall that a Working tier can target without negating it.

**SYS-2 — "the Advanced tier is Working plus an off-rubric budget."** Wave 2's rule. Wave 1's only
obligation to it was to make each rubric's 4→5 discriminator a thing visible in prompt text, so
wave 2 has something to point Advanced at. Done for all 26. No wave-1 edit belongs to SYS-2.

## Entries

Anchor rows are quoted before → after. Quality-bar codes: **1** occupiable, **2** anchor 5 not a
subset of 4, **3** repeatable, **4** on-axis, **5** monotonic.

### FIX-1.01 — preamble N/A rule (R09, R16a; CONFLICT-03) — high

Added after the "score as written" line:

> If the task has no instance of the property the rubric measures — no branch to state, no phrasal
> verb, no competing instructions, no case where an example would teach anything — score the lever
> N/A rather than 1, and leave its `PROGRESS.md` entry untouched.

Applied last, per the plan's sequencing note. Everything below the preamble shifts by **+1** —
waves 2–6 must re-derive `rubrics.md` line numbers. **Inert until FIX-4.20** lands in `SKILL.md:20`
and `assessment.md:13`; ship together.

### FIX-1.02 — verb anchor 5 (R02) — high

Before: `| 5 | Exactly one operation named, and it is the operation actually wanted. |`
After: `| 5 | Exactly one operation named, it is the operation actually wanted, and no verb in the same family names it more narrowly. |`

Gains **2** — anchor 5 was a strict subset of anchor 4; the narrowest-verb property now appears
positively at 5. Anchor 4 untouched, as the plan directs.

### FIX-1.03 — noun `**Measures:**` (R01, Measures half only) — medium

Before: `**Measures:** the artifact the prompt asks for.`
After: `**Measures:** the artifact the prompt asks for, and the words spent naming it.`

Gains **4** — the line now warrants the economy criterion anchor 5 applies. Per CONFLICT-01 the
anchor is untouched: day 1's ladder, plus days 6, 7 and 14, reach anchor 5 exclusively through
economy. Economy remains scored in three places by design.

### FIX-1.04 — adjective 3/4/5 (R03, R04) — medium

Before:
> | 3 | One real quality is named, but a second quality that matters as much is left unstated. |
> | 4 | Every quality that matters is named, though some slack remains in how they're worded. |
> | 5 | Every quality that matters is named, and none that do not — each word does rejection work. |

After:
> | 3 | Of the qualities the writer names as rejection-triggers, one is in the prompt and a second is not. |
> | 4 | Every quality the writer names as a rejection-trigger is in the prompt, and no others are. |
> | 5 | Every rejection-trigger is named and no others are, and each is worded specifically enough that a generic output visibly fails one. |

Gains **3** (the "qualities that matter" set is now elicited from the writer rather than guessed)
and **5** (4→5 changed two things at once; "none that do not" moves to 4, wording precision alone
carries 5). **Forces re-derivation of FIX-2.02** — CONFLICT-12.

### FIX-1.05 — adverb 4/5 (R05) — high

Before:
> | 4 | Depth and manner set clearly enough that output length and thoroughness are mostly predictable. |
> | 5 | Depth and manner set so output length and thoroughness are predictable in advance, not just in hindsight. |

After:
> | 4 | Depth and manner set with a measure attached, but only to part of the task, or attached as a stated tolerance rather than a fixed figure, so two competent readers would land inside that tolerance rather than on the same length. |
> | 5 | Depth and manner set with a measure attached to every part, so two competent readers would produce the same length and thoroughness. |

Gains **3, 5** — the rows were on different axes (how much predictability vs when the prediction is
available), and hindsight-vs-advance is untestable at scoring time. Anchor 2 left untouched so
FIX-3.02/3.03 stay live.

**Deviation from the drafted text, flagged.** The plan's draft reads "or loosely enough that two
competent readers would land within a stated tolerance". "Loosely" is on the plan's own checkpoint-3
ban list for anchor-4 rows. I kept the semantics exactly and phrased the same condition as "attached
as a stated tolerance rather than a fixed figure", which carries the referent without the degree
word. No meaning change.

### FIX-1.06 — pronoun 2/3/4/5 (R06, R07) — medium

Before:
> | 2 | An antecedent exists somewhere in the prompt, but it's ambiguous which of two candidates it refers to. |
> | 3 | Most references resolve, but one pronoun still requires the reader to guess. |
> | 4 | Every reference resolves, though the resolution takes a re-read to confirm. |
> | 5 | Every reference resolves inside the prompt or to a quoted block, on first read. |

After:
> | 2 | More than one reference is unresolvable, or the prompt's main referent is ambiguous between two candidates. |
> | 3 | Exactly one pronoun still requires the reader to guess; the rest resolve. |
> | 4 | Every reference resolves inside the prompt or to a quoted block, but at least one antecedent sits more than a sentence away from its pronoun. |
> | 5 | Every reference resolves inside the prompt or to a quoted block, and each pronoun's antecedent is the nearest preceding noun phrase. |

Gains **3** (rows 2 and 3 no longer both describe the single-ambiguous-pronoun case; "takes a
re-read" was a property of the reader and is replaced by countable distance) and **5** (the scope
condition no longer appears at 5 only). **Blocks FIX-2.07** — day 8's tiers must be re-derived.

### FIX-1.07 — preposition 4/5 (R08) — medium

Before:
> | 4 | Boundaries, audience and exclusions are all set, though phrased loosely enough to invite a small stretch. |
> | 5 | Boundaries, audience and exclusions all set precisely — in what, for whom, without what. |

After:
> | 4 | Boundaries, audience and exclusions are all set, but at least one could be satisfied two ways. |
> | 5 | Boundaries, audience and exclusions all set so each admits exactly one reading — in what, for whom, without what. |

Gains **3** — "loosely" and "a small stretch" had no referent; the split is now number-of-readings.

### FIX-1.08 — determiner 3/4/5 (R10) — medium

Before:
> | 3 | Most nouns are bound, but one noun that changes scope significantly ("the" vs "any") is left bare. |
> | 4 | Each noun is bound — the, a, each, every, any — with only a minor reading left open. |
> | 5 | Each noun is bound — the, a, each, every, any — with no reading left open. |

After:
> | 3 | Most nouns are bound, but one noun is left bare where swapping "the" for "any" would change what gets done. |
> | 4 | Each noun is bound — the, a, each, every, any — but one binding could be read two ways without changing what gets done. |
> | 5 | Each noun is bound — the, a, each, every, any — and swapping any determiner would change what gets done. |

Gains **3** — rows 4 and 5 were byte-identical up to "minor"/"no". The referent is now the rubric's
own fastest-fix test. **Blocks FIX-2.09.**

### FIX-1.09 — numeral 3/4 (R11, R12) — high

Before:
> | 3 | Most countable dimensions are bounded, but the bound is vague enough to need judgement ("a few", "several"). |
> | 4 | Every countable dimension is bounded with a number, though one bound is awkward to verify without counting carefully. |
> | 5 | Every countable dimension bounded, and the bounds checkable without judgement. |

After:
> | 3 | Every countable dimension is bounded, but at least one bound is vague enough to need judgement ("a few", "several"). |
> | 4 | Every countable dimension is bounded, and every bound is a number, but at least one is a range or an approximation rather than an exact count. |
> | 5 | Every countable dimension is bounded, and every bound is an exact count or length, checkable without judgement. |

Gains **1** (anchor 4 no longer grades verification labour, which is either vacuous or unoccupiable),
**4** and **5** (coverage carries 1→2→3, hardness carries 3→4→5).

**Deviation from the plan, flagged — the one place a wave-1 entry as drafted fails the plan's own
acceptance test.** The plan says "Leave rows 1, 2 and 5 as written." But with the new anchor 4, a
range bound ("3–5 bullets") is a *range* — anchor 4's shortfall — and is also "checkable without
judgement" — anchor 5's whole text. So an anchor-4 prompt satisfies anchor 5 verbatim, which is
exactly the defect SYS-1 exists to remove and which the plan's checkpoint 4 forbids. I applied the
minimal on-axis repair the systemic rule dictates: anchor 5 now states the discriminator positively
("every bound is an exact count or length"). Rows 1 and 2 left as written. This is an extension of
FIX-1.09 under SYS-1, not a re-litigation of a ruling; no ruling covers it. Wave 2's day-11 work
should be checked against the tightened anchor 5.

### FIX-1.10 — interjection anchor 4 (R13, A07; CONFLICT-02) — high

Before: `| 4 | The must-not-fail instruction is marked and positioned near the top, but competes with one other marked item. |`
After: `| 4 | The must-not-fail instruction is marked and stands alone rather than sitting mid-paragraph, but competes with one other marked item. |`

Gains **1** — the positional direction made anchor 4 unsatisfiable for any learner who also
satisfied `context-ordering` anchor 5 (constraints last), and day 12's own Novice tier produced a
prompt anchor 4 could not describe. The competing-second-marker discriminator survives and is now
reachable. This closes the `interjection`/`context-ordering` cross-rubric contradiction.
**Blocks FIX-2.11.**

### FIX-1.11 — interjection anchors 2 and 5 (R14, R15) — medium

Before:
> | 2 | A priority word is used ("important:") but attached to something that isn't actually the highest-stakes instruction. |
> | 5 | The must-not-fail instruction is marked and positioned so it cannot be missed. |

After:
> | 2 | A priority word is used ("important:") but attached to something other than the instruction the writer names as the one they would be angriest to see ignored. |
> | 5 | Exactly one marker in the prompt, on the instruction the writer names as highest-stakes, standing alone as its own line. |

Gains **3** on both rows — "cannot be missed" was the outcome the rubric measures, not a criterion
for measuring it; "actually the highest-stakes" was unwritten intent. Both now name the elicitation
the fastest fix already performs. Anchor 5's "exactly one marker" also imports day 12's rarity rule.

### FIX-1.12 — particle 4/5 (R16b, R17) — high

Before:
> | 4 | Every phrasal verb is chosen deliberately, with only cosmetic substitutions available. |
> | 5 | Every phrasal verb chosen deliberately; no substitution preserves the meaning. |

After:
> | 4 | Each phrasal verb present is load-bearing, but at least one plain verb would have served as well. |
> | 5 | Each phrasal verb present is load-bearing and no plain verb would have served — swapping any particle changes the task. |

Gains **1** (anchor 5 was close to always-false, since particles are usually interchangeable
somewhere) and **3** ("only cosmetic substitutions available" and "no substitution preserves the
meaning" were near-complements, and a cosmetic substitution *is* a meaning-preserving one). Together
with FIX-1.01's N/A rule this closes the `verb`/`particle` contradiction: the rubric now scores
whether a phrasal verb was the right choice rather than presupposing one exists, and the
zero-phrasal-verb prompt day 13 tells learners to write scores N/A rather than a coin-flip 1 or 5.

### FIX-1.13 — role framing Measures + 4/5 (R18, R19) — medium

Before:
> **Measures:** whether the role changes the output.
> | 4 | Role changes what is included, excluded and assumed, though the mechanism is only implied, not stated. |
> | 5 | Role changes what is included, excluded and assumed, and you can say how. |

After:
> **Measures:** whether the prompt says what the role changes.
> | 4 | The role text names at least one thing the output includes, excludes or assumes because of the role, but not how the role produces it. |
> | 5 | The role text names what the output includes, excludes and assumes because of the role, and says how the role produces each. |

Gains **2** (if the mechanism is implied strongly enough for the scorer to articulate, the scorer
"can say how" and 4 collapsed into 5), **3** and **4** — the Measures line claimed an output effect
that would need an A/B run the daily loop never performs; anchors 2–5 all inspect prompt text and the
line now says so. Wave 1 keeps day 15's "included, excluded **and** assumed" conjunction;
**FIX-2.14 and FIX-3.07** make the day match it.

### FIX-1.14 — few-shot anchors 1 and 2 (R20) — medium

Before:
> | 1 | No examples, or examples that only show the easy case. |
> | 2 | One example given, showing a typical case with nothing instructive about its edges. |

After:
> | 1 | No examples. |
> | 2 | One or more examples, all typical, none instructive about the edges. |

Gains **5** — three typical examples matched row 1's second disjunct and matched neither row 2
("one example") nor row 3 (variety), so the ladder penalised adding examples. Now monotone.

### FIX-1.15 — output-schemas anchor 4 (R21) — low

Before: `| 4 | An exact structure is given, checkable in most cases, with one edge (e.g. empty values) unaddressed. |`
After: `| 4 | An exact structure is given, with one edge (e.g. empty values) unaddressed. |`

Gains **3** — the trailing clause already supplied the checkable referent; "checkable in most cases"
was redundant with it and invited a vaguer second reading. Wording only.

### FIX-1.16 — task-decomposition 4/5 (R22) — high

Before:
> | 4 | Work split so each step has one output and a mostly clear input from the last. |
> | 5 | Work split so each step has one output and a clear input from the last. |

After:
> | 4 | Work split so each step has one output, and the next step's input is the previous step's output plus at most one added instruction or re-explanation. |
> | 5 | Work split so each step has one output, and each step's input is verbatim the previous step's output — nothing added, nothing re-explained. |

Gains **2, 3** — the rows differed by the single word "mostly" and nothing in the file defined
"clear". Day 18's verbatim-seam test is now in the rubric, where commit `3e48ea7` should have put it.
**Blocks FIX-2.17** — day 18's Novice and Working tiers must stop demanding verbatim.

### FIX-1.17 — reasoning-scaffolds 4/5 + fastest fix (R23, R24; CONFLICT-05) — high

Before:
> | 4 | The reasoning steps asked for match the ones the task requires, with minor slack in ordering. |
> | 5 | The reasoning steps asked for match the ones the task requires. |
> **Fastest fix:** name the intermediate you want to see before the answer.

After:
> | 4 | The reasoning steps asked for match the ones the task requires, but the prompt does not fix the order they are produced in. |
> | 5 | The reasoning steps asked for match the ones the task requires, in the order the task requires them produced. |
> **Fastest fix:** list what the answer depends on; name every item on that list and nothing else.

Gains **2** (ordering entered at 4 and vanished at 5, so a sloppily-ordered prompt satisfied 5
exactly) and **3**. Per CONFLICT-05 the fastest-fix line is the stale half: naming one intermediate
reaches anchor 3 at best, while 4/5 turn on the set match `days/19.md:11` already states.
**Blocks FIX-2.18.** Ordering is now cleanly divided three ways — `conjunction` owns
order-of-branch-evaluation, `context-ordering` owns order-of-prompt-sections, `reasoning-scaffolds`
owns order-of-intermediates.

### FIX-1.18 — negative-constraints anchor 5 (R25) — medium

Before: `| 5 | Exclusions are specific, and each prevents a failure you have actually seen. |`
After: `| 5 | Exclusions are specific, and each cites in the prompt the incident it prevents. |`

Gains **3** — "a failure you have actually seen" is unverifiable from the text and unfalsifiable by
the tutor. Day 20's model answer already puts the incident in the prompt.

**Deviation, flagged — anchor 4 also moved, against the plan's "anchor 4 stays untouched".**

Before: `| 4 | Exclusions are specific and mostly map to failures you've seen, with one still speculative. |`
After: `| 4 | Exclusions are specific and each names the failure it prevents, but at least one is speculative rather than observed, or names its failure without citing the incident in the prompt. |`

Two reasons, both forced by the plan itself. (a) The old row contains "mostly", which checkpoint 3
bans in anchor-4 rows. (b) More seriously, **CONFLICT-11 states the post-fix ladder as "Working =
every exclusion names an observed failure (still 4, since none cites its incident)"** — but the old
anchor 4 reads "with one still speculative", so a prompt where every exclusion is observed and none
cites its incident matched *neither* 4 nor 5. Wave 2's FIX-2.19 is derived from a rung that did not
exist. The added disjunct creates it while preserving the original speculative case. If wave 2
disagrees with this reading, flag it back — FIX-2.19 depends on it.

### FIX-1.19 — context-ordering anchors 1 and 5 (R26, R27) — medium

Before:
> | 1 | Instruction buried after a wall of context, or context missing where needed. |
> | 5 | Instruction and context ordered so the model reads what it needs when it needs it. |

After:
> | 1 | Instruction buried after a wall of context. |
> | 5 | Task first, material second, constraints grouped last. |

Gains **3** (anchor 5 was a purpose statement no tutor can verify by inspection; the concrete
version was already sitting in the fastest fix one line below) and **4** (missing context is a
coverage failure, not a placement failure — a perfectly-ordered prompt with one missing fact scored
1 on a rubric about ordering).

**Small deviation, flagged.** Anchor 4 read "with constraints mostly grouped but one placed early" —
"mostly" is on checkpoint 3's ban list. Changed to "with constraints grouped except for one placed
early". The countable shortfall ("one placed early") is unchanged; the redundant degree word is gone.
**Blocks FIX-2.21** (T19's Working/Advanced split must target the new anchor 5); FIX-2.20 is
unaffected — day 21's Novice tier still produces the narrowed anchor-1 artifact.

### FIX-1.20 — system-prompts 3/4 (R28) — medium

Before:
> | 3 | Durable rules and turn request are mostly separated, but one standing rule is restated per turn out of habit. |
> | 4 | Standing behaviour and per-turn request are separated into two blocks, but one line in the system prompt is turn-specific and could move to the per-turn request without changing behaviour. |

After:
> | 3 | Standing behaviour and per-turn request are separated into two blocks, but two or more lines are on the wrong side — in either direction. |
> | 4 | Standing behaviour and per-turn request are separated into two blocks, and exactly one line is on the wrong side — in either direction. |

Gains **4, 5** — the old ladder ranked the two leak directions that `days/22.md:9` explicitly says
are equivalent, and a prompt with both leaks fitted neither row. The axis is now leak *count*, which
is checkable. **Blocks FIX-2.22.**

### FIX-1.21 — agent-and-tool anchor 5 + fastest fix (R29, R30; CONFLICT-04) — high

Before:
> | 5 | Which tools, when, and what "done" means are all stated. |
> **Fastest fix:** state the stop condition first, then the tools.

After:
> | 5 | Which tools, when, and what "done" means are all stated, and the done-condition names a checkable state that motion alone cannot satisfy. |
> **Fastest fix:** make the done-condition un-gameable, then name which tool serves which situation.

Gains **2** — anchor 5 was a strict subset of anchor 4; gameability appeared only as a negative in 4.
Per CONFLICT-04 the ordering claim in the fastest fix is the stale half and is removed: `days/23.md:9`
says ordering is "not a scored one" and the Novice tier says "in any order". Half the old line was
valid (stating a stop condition at all moves 1/2/3 → 4) and is preserved. **No day-23 edit** — see
the day-23 check below.

### FIX-1.22 — self-critique 4/5 (R31) — high

Before:
> | 4 | A check the model can apply to its own output is given, with an action on failure that's only loosely defined. |
> | 5 | A check the model can apply to its own output, with a stated action when it fails. |

After:
> | 4 | A check the model can apply to its own output is given, with an action on failure that names no operation ("fix it", "try again"). |
> | 5 | A check the model can apply to its own output, with an action on failure that names what to do to the failing element. |

Gains **2, 3** — a loosely-defined action is still a stated action, so every anchor-4 prompt
satisfied 5. The real ladder (no action / vague action / specific action) is now written down.
**Blocks FIX-2.23** — day 24's 3 → 5 → 5 ladder now has its missing rung.

### FIX-1.23 — writing-evals anchors 1–5 (R32, R33; CONFLICT-08) — high

Before:
> | 1 | Quality judged by feel; no criteria written down. |
> | 2 | Criteria exist but are subjective enough ("sounds right") that two scorers would diverge. |
> | 3 | Criteria are written and mostly objective, but one is still a judgement call. |
> | 4 | Criteria written before the output, specific enough that two people would agree most of the time. |
> | 5 | Criteria written before the output, specific enough that two people would score the same. |

After:
> | 1 | Quality judged by feel; no criteria written down. |
> | 2 | Criteria written, but after the output existed, so they describe what was produced rather than what was required. |
> | 3 | Criteria written before the output, but at least one names a feeling rather than a checkable property. |
> | 4 | Criteria written before the output, each naming a checkable property a reader who has not seen the output could apply without asking the writer, but at least one could be applied two ways. |
> | 5 | Criteria written before the output, and every criterion is specific enough that two readers who have not seen the output would produce the same score. |

Gains **3** (both old rows asked one tutor to forecast two hypothetical scorers, and anchor 4 asked
for that forecast as a frequency with no threshold — the rubric measuring repeatability was the least
repeatable in the file) and **5** (timing was a binary precondition appearing at 4 only, so three
perfectly objective criteria written after the output capped at 3 with no signal why; timing now
carries the ladder from the bottom, as `days/25.md:9` says it should).

CONFLICT-08 honoured: R33's intent adopted, its drafting rejected. "Apply without asking" is
deliberately placed at **anchor 4**, not 5; "two readers produce the same score" carries 5. See the
day-25 verdict below.

### FIX-1.24 — token-economy anchor 5 (R34; CONFLICT-10) — low

Before: `| 5 | Every included token earns its place; cuts made without losing accuracy. |`
After: `| 5 | Every included token earns its place, and the cut version was rerun and the output held. |`

Gains **3** — the 4/5 separator was whether a cut was tested, which is not a property of the prompt
and was rescued only by day 26's exercise happening to make every tier rerun. Anyone scoring this
rubric outside day 26 had no way to establish anchor 5. Anchor 4's meaning is unchanged.
**Blocks FIX-2.24** — day 26's ladder is now forced: Novice and Working cut by inspection (anchor 4,
untested), Advanced reruns and compares.

### FIX-1.25 — failure-diagnosis 4/5 + fastest fix (R35, A15; CONFLICT-06) — medium

Before:
> | 4 | The failing lever is identified by name and the fix changes that lever, but it also changes a second lever that was not implicated. |
> | 5 | The failing lever is identified by name and the fix targets it. |
> **Fastest fix:** ask which of the 11 levers was underspecified, and fix that one.

After:
> | 4 | The failing lever or technique is identified by name and the fix changes it, but it also changes a second lever or technique that was not implicated. |
> | 5 | The failing lever or technique is identified by name and the fix targets it and nothing else. |
> **Fastest fix:** ask which of the 11 levers or the techniques from weeks 3–4 was underspecified, and fix that one.

Gains **5** (anchors 2 and 3 in the same ladder already admit techniques and 4/5 silently dropped
them — an internal monotonicity defect, not a lesson-vs-contract conflict) and **2** (the added "and
nothing else" states positively what anchor 4's shortfall implies). Per CONFLICT-06 the rubric moves
on both counts. **Blocks FIX-2.25** — day 27's Working tier drops "only", Advanced takes it.

### FIX-1.26 — prompt-library 4/5 + fastest fix (R36, R37; CONFLICT-07) — medium

Before:
> | 4 | Reusable prompts stored with their slots and most known failure modes noted. |
> | 5 | Reusable prompts stored with their slots and their known failure modes. |
> **Fastest fix:** save the prompt with the task slot left as a blank.

After:
> | 4 | Reusable prompts stored with their slots and at least one failure mode recorded, but not specifically enough for a stranger to recognise it before running the prompt. |
> | 5 | Reusable prompts stored with their slots and their failure modes recorded specifically enough that a stranger would recognise each one before running the prompt. |
> **Fastest fix:** save the prompt with the task slot blank, and one line naming the way it failed last time.

Gains **3** — the old rows graded against a denominator that exists only in the learner's head, and
the learner could move themselves between 4 and 5 by recalling more or fewer failures. The axis is
now specificity, which is in the text. The fastest fix no longer stops at anchor 3 (marking the slot
*is* anchor 3). **A14 dissolves** — day 28's self-test "the one way it's failed" is now correct as
written and the model answer's single recorded failure is a legitimate 5, so no wave-3 entry is
needed. **Blocks FIX-2.26.**

### FIX-1.27 — capstone 4/5 + fastest fix + reachability note (R38, R39, R40; CONFLICT-09) — high

Before:
> | 4 | Prompt is specified and evaluated against written criteria, with failure modes noted but not systematically. |
> | 5 | Prompt is specified, evaluated against written criteria, and its failure modes documented. |
> **Fastest fix:** run it on the case you did not design it for.

After:
> | 4 | Prompt is specified, holds on varied cases, and is evaluated against written criteria, with failure modes noted but not specifically enough for someone else to recognise them. |
> | 5 | Prompt is specified, holds on a case it was not designed for, is evaluated against written criteria, and its failure modes are documented specifically enough that someone else could recognise each one. |
>
> Anchors 4 and 5 need written criteria and documented failures — day 30's work. A prompt scored before then caps at 3.
>
> **Fastest fix:** run it on a case you did not design it for, then write the criteria that would have caught what broke.

Gains **4, 5** (robustness ran 1→2→3 and then vanished, so a prompt that had only ever run on its
original case matched every word of anchor 5 — the exact opposite of "production readiness", and
reachable via day 30's Novice tier which reruns on the same case) and **3** ("not systematically" was
defined nowhere; day 30's "someone else could recognise it" is imported). The fastest fix no longer
repeats the 1/2 → 3 move and now covers the criteria and documentation steps. The added note is
R40's secondary suggestion, taken. **FIX-2.27 must be derived from this text** — `census-tiers.md`'s
T25/T26 draft targets the old anchors and is stale.

## CONFLICT-08 — the day-25 check

Day 25 was **not touched**. Its three tiers, quoted from `prompting-wizard/days/25.md`, mapped
against the revised `writing-evals` anchors:

- **Novice** (`:31`) — "Before writing a prompt for {{TASK}}, write three checks you'll apply to
  whatever it produces. Only then write the prompt and generate the output."
  → **anchor 3**. Criteria are written before the output (clearing anchor 2's timing failure), but
  no specificity bar is set, so "reads well" is admitted — anchor 3's "at least one names a feeling
  rather than a checkable property". Rule 3 satisfied: a lazy but compliant learner still scores 3.
- **Working** (`:35`) — "Write three criteria for {{TASK}} specific enough that someone else could
  **apply** them without asking you what you meant, then generate the output and score it against
  them unchanged."
  → **anchor 4**. Verbatim anchor 4's positive content. Anchor 4's shortfall — "at least one could
  be applied two ways" — is neither demanded nor tested by the tier, so it stays open (rule 2).
- **Advanced** (`:39`) — "Write three criteria for {{TASK}} before generating anything. After you see
  the output, score it against exactly those three — don't add a fourth, and don't soften one it
  narrowly misses."
  → **anchor 5**. The no-drift test is the mechanism that makes two independent readers converge on
  the same score, which is anchor 5's demand and nothing less.

**Verdict: 3 / 4 / 5, unchanged. The model ladder survives.** The load-bearing decision is that
"apply without asking" sits at anchor 4 and "produce the same score" at anchor 5 — R33's original
drafting put "apply without asking" at 5, which would have lifted Working to 5 and flattened the
ladder to 3/5/5.

Day 23 (`agent-and-tool-prompting`, FIX-1.21) also re-checked and unmoved: Novice "all three stated,
in any order" → 3; Working "specific, checkable outcome ... you could verify against the transcript"
→ 4, gameability untested; Advanced "un-gameable ... rewrite the condition so that shortcut no longer
counts as done" → 5.

Day 29 (`capstone`, FIX-1.27, CONFLICT-09) re-checked and unmoved: Novice "run it once, confirm it
produces the deliverable" → 1; Working "two cases that differ from each other ... until it holds up
on both" → 2–3; Advanced "specify the prompt fully ... run it on the most different case" → **still
capped at 3**, because the tier still produces no written evaluation criteria and revised anchor 4
requires them. Day 29's self-cap at `:9` stays true.

## Not done, and why

- **Duplicate-`## `-heading check in `tools/validate.py`.** Left alone. The master plan's wave 1 is
  27 entries, all inside `rubrics.md`; it assigns no validator work to this wave.
  `wave0-validator-fixes.md:301` already records the residual ("a repeated `## Noun` in `rubrics.md`
  would still merge silently into `h2_slugs`") as a known limitation of wave 0's fix 6. Per the wave
  brief, the check is only in scope if the plan assigns it here, and it does not. No `tools/` file
  was modified; the 103-test suite is unchanged.

## Carried forward to later waves

1. **Line numbers.** FIX-1.01 inserted two lines (the rule plus its blank line) at the preamble.
   Every `rubrics.md:N` reference in waves 2–6 is stale by **+2**, not +1 as the plan's checkpoint 6
   predicts — the plan assumed a same-paragraph append; the rule reads better as its own paragraph.
   Re-derive from the file, not from the plan.
2. **FIX-1.01 is inert until FIX-4.20.** `SKILL.md:20` and `assessment.md:13` must tolerate N/A or
   the preamble rule has nowhere to write.
3. **Three flagged deviations** — numeral anchor 5 (tightened under SYS-1; the plan's "leave row 5"
   would have failed checkpoint 4), negative-constraints anchor 4 (the rung CONFLICT-11 assumes did
   not exist), context-ordering and adverb anchor 4 (degree words removed to pass checkpoint 3).
   All four preserve the plan's stated semantics. FIX-2.19 in particular should be re-read against
   the new negative-constraints anchor 4 before it is written.
4. **Re-derivations the plan already flags**, all now unblocked: FIX-2.02 (day 3), 2.07 (day 8),
   2.09 (day 10), 2.11 (day 12), 2.17 (day 18), 2.18 (day 19), 2.19 (day 20), 2.21 (day 21),
   2.22 (day 22), 2.23 (day 24), 2.24 (day 26), 2.25 (day 27), 2.26 (day 28), 2.27 (day 30).
