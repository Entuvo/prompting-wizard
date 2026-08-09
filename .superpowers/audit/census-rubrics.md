# Rubrics census

Read-only audit of `prompting-wizard/rubrics.md` (369 lines, 26 rubrics). Nothing was modified. All line references are `prompting-wizard/rubrics.md:NN` unless another file is named.

**Headline.** The file has one dominant, systematic defect: **anchor 4 is very often anchor 5 with a hedge inserted**, and in five rubrics anchor 5's text is a *strict subset* of anchor 4's, so a prompt sitting at 4 satisfies every word of 5. Two tutors following `SKILL.md:34` ("quoting the rubric's anchor for each score you give") can each quote a fitting anchor and land on different numbers. 9 of 26 anchor-4s are not occupiable as distinct states; 7 more are occupiable only through an unquantified degree word. Ten of the eleven unreferenced hedge words in the file sit on an anchor-4 row.

**Slugs.** All 26 headings produce the slugs the 30 day files cite; the map is currently intact. **No fix recommended below changes a heading**, so no day file breaks. See "Slug risk" at the end for what would break if any heading were touched.

## Summary table

| Rubric | Monotonic? | Anchor 4 distinct? | Vague anchors | Fastest fix valid? |
|---|---|---|---|---|
| noun | No — economy axis enters at 5 | Yes (but 5 is off-axis) | 3 ("a reasonable reader"), 5 ("beyond what pins it down") | Partial — reaches 4, cannot reach 5 |
| verb | Yes | **No** — 5 ⊆ 4 | 4 ("a more specific verb ... exists") | Yes |
| adjective | No — 5 adds an exclusion axis | Weak | 4 ("some slack") | Partial |
| adverb | No — 4 is degree, 5 is timing | **No** | 4 ("clearly enough", "mostly predictable") | Partial |
| pronoun | Yes | Weak | 4 ("takes a re-read") | Yes |
| preposition | Yes | Weak | 4 ("loosely enough", "a small stretch") | Yes |
| conjunction | Yes | Yes | — | Partial — stops at 4 |
| determiner | Yes | Weak | 3 ("significantly"), 4 ("a minor reading") | Yes |
| numeral | No — 4 switches to verification effort | **No** — incoherent | 3 (coverage/hardness conflated) | Yes |
| interjection | No — marking → position → salience | Yes, but contradicts day 12 | 5 ("cannot be missed") | Partial — silent on position |
| particle | Yes | Weak | 3 ("a small remaining ambiguity"), 4 ("only cosmetic") | **No** — its own test unscoreable |
| role-framing | Yes | Weak | 4 ("only implied"), 5 ("you can say how") | Yes |
| few-shot-examples | No — 1/2 inverted | Yes | — | Yes |
| output-schemas | Yes | Yes | 4 ("in most cases" — has referent) | Yes |
| task-decomposition | Yes | **No** — 4 = 5 + "mostly" | 4 ("mostly clear") | Partial — reaches 3 |
| reasoning-scaffolds | No — ordering only at 4 | **No** — 5 ⊇ 4 | 4 ("minor slack") | Partial |
| negative-constraints | Yes | Yes | 4 ("mostly" — has referent) | Yes |
| context-ordering | No — 1 mixes completeness; 5 drops criterion | Yes | 5 ("what it needs when it needs it") | Yes |
| system-prompts | No — 3 and 4 are opposite leak directions | Yes | 3 ("mostly separated") | Yes |
| agent-and-tool-prompting | Yes | **No** — 5 ⊇ 4 | 4 ("could still be gamed") | **No** — scores unscored ordering |
| self-critique-loops | Yes | **No** — 5 ⊇ 4 | 4 ("only loosely defined") | Yes |
| writing-evals | No — timing axis enters at 4 | **No** | 3 ("mostly objective"), 4 ("most of the time") | Partial |
| token-economy | Yes | Yes | 3 ("most padding" — has referent) | Yes |
| failure-diagnosis | No — "or technique" dropped after 3 | Yes | — | Partial — excludes techniques |
| prompt-library | Yes | **No** — 4 = 5 + "most" | 4 ("most known failure modes") | **No** — reaches 3 only |
| capstone | No — three axes, robustness dropped after 3 | Weak | 4 ("not systematically") | Partial |

## Findings

### DEFECT-R01 — Noun anchor 5 switches the ladder from specificity to economy — severity: medium

`rubrics.md:9,16-17,19`

> **Measures:** the artifact the prompt asks for.
> | 4 | The artifact is named unambiguously. Someone reading only the prompt could describe the finished output. |
> | 5 | Named unambiguously and economically — no words spent on the artifact beyond what pins it down. |

Anchors 1–4 measure one thing: how far the artifact is pinned down. Anchor 5 keeps that and adds a second, independent property — word economy — which is not "the artifact the prompt asks for" and is scored elsewhere (`token-economy`, `rubrics.md:315-327`). A prompt that names the artifact perfectly but verbosely is a 4 forever, on an axis the Measures line does not claim.

Compounding: economy is taught only in day 1's **Advanced** tier (`days/01.md:41`, "under 15 words total ... every word you spend has to be pinning the artifact down"). `SKILL.md:30` presents exactly one tier, so novice and working learners are scored at anchor 5 against a criterion they were never shown. Day 1's Working tier (`days/01.md:37`) is a near-verbatim restatement of anchor 4, so 4 is well anchored; 5 is not.

"beyond what pins it down" has no checkable referent — two tutors will disagree about which words pin.

**Minimal fix:** make 5 the endpoint of the same axis ("named unambiguously, and the naming survives a hostile reading — no second delivery satisfies it"), and move the economy claim to `token-economy` or to a stated word budget imported from `days/01.md:41`.

### DEFECT-R02 — Verb anchor 5's text is a strict subset of anchor 4's — severity: high

`rubrics.md:30-31`

> | 4 | Exactly one operation named, and it is the operation wanted, but expressed with a generic synonym ("check" instead of "audit") where a more specific verb in the same family exists. |
> | 5 | Exactly one operation named, and it is the operation actually wanted. |

Every condition anchor 5 states is satisfied by an anchor-4 prompt. The property that is supposed to separate them — using the most precise verb available — appears only as a negative clause inside 4 and is never stated positively at 5. A tutor scoring by quoting the matching anchor (`SKILL.md:34`) can honestly quote either row for the same prompt. This is not hypothetical drift: commit `9041425` deleted the phrase "in the most precise verb available for it" from anchor 5 and did not re-home it.

Second, opposite failure under a strict reading: "where a more specific verb in the same family exists" is unbounded — a more specific verb almost always exists ("audit" → "line-audit", "reconcile") — so a strict tutor caps every prompt at 4 and anchor 5 becomes unoccupiable. The pair fails in both directions.

**Minimal fix:** restore the differentiator to 5 — "Exactly one operation named, it is the operation actually wanted, and no verb in the same family names it more narrowly."

### DEFECT-R03 — Adjective anchors 3–5 score the writer's intent, which the file's own preamble forbids — severity: medium

`rubrics.md:5,43-45`

> Score the prompt as written, not the intent behind it.
> | 3 | One real quality is named, but a second quality that matters as much is left unstated. |
> | 4 | Every quality that matters is named, though some slack remains in how they're worded. |
> | 5 | Every quality that matters is named, and none that do not — each word does rejection work. |

"Every quality that matters" is a fact about the learner's unwritten standard, not about the prompt. Two tutors with different reads of what matters for the same task score the same prompt 3 and 5. The rubric's own preamble (`rubrics.md:5`) rules this out.

Day 3 supplies the referent the rubric omits (`days/03.md:9`: "the one you'd complain about first if it were missing, and the one you'd complain about second"), and the fastest fix half-imports it ("list the two qualities that would make you reject the output"). Anchor text should carry it.

**Minimal fix:** anchor 3/4/5 to the count the day teaches — "the two qualities the writer names as rejection-triggers" — so the standard is elicited once and then checked against the text.

### DEFECT-R04 — Adjective anchor 5 bundles two independent changes — severity: medium

`rubrics.md:44-45`

Anchor 4 → 5 changes two things at once: wording slack disappears **and** extraneous qualities must be absent ("and none that do not"). A prompt with two precisely-worded necessary qualities plus one decorative adjective matches neither row cleanly. The exclusion clause also duplicates `token-economy` (`rubrics.md:317`, "whether every token earns its place").

**Minimal fix:** move "none that do not" into anchor 4 as the differentiator from 3, leaving 5 to carry wording precision alone.

### DEFECT-R05 — Adverb 4 and 5 are on different axes and neither is checkable — severity: high

`rubrics.md:58-59`

> | 4 | Depth and manner set clearly enough that output length and thoroughness are mostly predictable. |
> | 5 | Depth and manner set so output length and thoroughness are predictable in advance, not just in hindsight. |

Anchor 4 grades *how much* predictability there is ("mostly"); anchor 5 grades *when* the prediction is available ("in advance, not just in hindsight"). These are orthogonal — "mostly predictable in advance" satisfies both rows. Neither "clearly enough" nor "mostly" has a referent, and hindsight-vs-advance is untestable at scoring time because the tutor has already seen the output (`SKILL.md:32-34` runs the prompt before critique).

Day 4 has the operational test the rubric lacks (`days/04.md:11`: "if two competent people followed this manner word, would their outputs be roughly the same length and thoroughness?").

**Minimal fix:** import the day-4 two-reader test into both rows — 4: "two competent readers would land within a stated tolerance"; 5: "two competent readers would produce the same length and depth, because a measure is attached."

### DEFECT-R06 — Pronoun anchors 2 and 3 describe the same condition — severity: medium

`rubrics.md:70-71`

> | 2 | An antecedent exists somewhere in the prompt, but it's ambiguous which of two candidates it refers to. |
> | 3 | Most references resolve, but one pronoun still requires the reader to guess. |

A prompt with exactly one pronoun ambiguous between two candidates matches both rows verbatim. There is no stated property — count, severity, distance — that puts it in one rather than the other. Two tutors diverge by a full point on the commonest case this rubric will ever see.

**Minimal fix:** make 2 the multi-failure row ("more than one reference unresolvable, or the prompt's main referent unresolvable") and 3 the single-failure row, which the "one pronoun" clause already implies.

### DEFECT-R07 — Pronoun anchor 4 measures reader effort, not the prompt — severity: medium

`rubrics.md:72-73`

> | 4 | Every reference resolves, though the resolution takes a re-read to confirm. |
> | 5 | Every reference resolves inside the prompt or to a quoted block, on first read. |

"Takes a re-read" is a property of the reader, and the tutor scoring on day 8 has read the prompt several times by step 4. Anchor 5 also adds a scope condition ("inside the prompt or to a quoted block") that anchor 4 does not carry, so a prompt resolving to an external artifact is 4 by 5's exclusion but 4's text says nothing about it. The differentiator is doing two jobs and neither is checkable.

**Minimal fix:** move the scope condition into 4 and distinguish by distance — 4: "resolution requires crossing more than one sentence"; 5: "each pronoun's antecedent is the nearest preceding noun phrase or a quoted block."

### DEFECT-R08 — Preposition anchor 4 is anchor 5 with an unquantified hedge — severity: medium

`rubrics.md:86-87`

> | 4 | Boundaries, audience and exclusions are all set, though phrased loosely enough to invite a small stretch. |
> | 5 | Boundaries, audience and exclusions all set precisely — in what, for whom, without what. |

Anchors 1–3 are countable (one of three dimensions, then two of three). At 4 the count stops carrying the ladder and "loosely enough to invite a small stretch" takes over, with no referent for "loosely" or "small". Everything that distinguishes a 4 from a 5 is now vibes.

**Minimal fix:** keep the count all the way up and make 4/5 turn on falsifiability — 4: "all three set, but at least one could be satisfied two ways"; 5: "all three set so each admits exactly one reading."

### DEFECT-R09 — Conjunction (and particle, interjection, few-shot) has no not-applicable state, and the course says it needs one — severity: high

`rubrics.md:97`, against `days/14.md:9`

> | 1 | Branching cases collapsed into one instruction, so edge cases silently pick a branch. |

Anchor 1 presupposes branching cases exist. For a task with no conditional logic — which day 14 explicitly contemplates: "Not every lever needs pulling hard; **some tasks have no fallback to state**. What matters is every lever considered, and either set deliberately or **left out on purpose**" (`days/14.md:9`) — no anchor fits. One tutor scores 1 (nothing branched), another scores 5 (nothing needed to). The same hole exists in `particle` (see DEFECT-R16), `interjection` (a prompt with one instruction has no priority to mark), and `few-shot-examples` (a task needing no examples).

This is not cosmetic: lever scores feed `PROGRESS.md`, and `SKILL.md:30` routes any lever at 2 or below into a later day as a secondary constraint. A spurious 1 sends the learner to practise a lever their tasks do not use; a spurious 5 hides a real gap.

**Minimal fix:** add one line to the preamble at `rubrics.md:5` — "If the task has no instance of the property (no branch, no phrasal verb, no competing instructions), score the lever N/A and leave `PROGRESS.md` untouched for it" — and make `SKILL.md:20` tolerate N/A. Preamble-only; no slug changes.

### DEFECT-R10 — Determiner anchor 4 is anchor 5 with "a minor reading" inserted — severity: medium

`rubrics.md:114-115`

> | 4 | Each noun is bound — the, a, each, every, any — with only a minor reading left open. |
> | 5 | Each noun is bound — the, a, each, every, any — with no reading left open. |

The rows are byte-identical up to "with only a minor reading left open" / "with no reading left open". "Minor" has no referent, and the rubric's own anchor 3 shows what a referent looks like ("one noun that changes scope significantly"). Anchor 3 also leans on "significantly" without one.

**Minimal fix:** 4: "each noun bound, but one binding could be read two ways without changing what gets done"; 5: "each noun bound, and swapping any determiner would change what gets done" — which is exactly the fastest fix at `rubrics.md:117` and the day-10 test at `days/10.md:11`.

### DEFECT-R11 — Numeral anchor 4 is incoherent: it grades verification effort, not boundedness — severity: high

`rubrics.md:128-129`

> | 4 | Every countable dimension is bounded with a number, though one bound is awkward to verify without counting carefully. |
> | 5 | Every countable dimension bounded, and the bounds checkable without judgement. |

Anchors 1–3 grade coverage and hardness of bounds. Anchor 4 introduces a third property — how laborious verification is — which is not on the ladder and is not what the Measures line claims ("budgets that make output checkable", `rubrics.md:121`). Worse, the condition is close to vacuous: *every* numeric bound is verified by counting carefully, so either anchor 4 swallows every numerically-bounded prompt and 5 is unreachable, or a tutor reads "awkward" charitably and 4 is unoccupiable. There is no third reading.

Note that the true differentiator is already stated correctly at 5 ("checkable without judgement") and at anchor 3 ("vague enough to need judgement"). Anchor 4 has nothing left to grade.

**Minimal fix:** make 4 the partial-hardness row — "every dimension bounded, but one bound is a range or an approximation rather than an exact count" — leaving 5 for exact bounds throughout.

### DEFECT-R12 — Numeral anchor 3 conflates coverage with hardness — severity: medium

`rubrics.md:127`

> | 3 | Most countable dimensions are bounded, but the bound is vague enough to need judgement ("a few", "several"). |

Two different prompts land here with no way to tell them apart from the row: (a) most dimensions bounded numerically, one unbounded; (b) all dimensions bounded, but with "a few". The rubric ties them together with "but", implying they co-occur; they usually do not.

**Minimal fix:** split — coverage carries 1→2→3, hardness carries 3→4→5, stated as such.

### DEFECT-R13 — Interjection anchor 4 contradicts day 12's canonical answer and the context-ordering rubric — severity: high

`rubrics.md:142-143` against `days/12.md:21,23,31` and `rubrics.md:257`

> | 4 | The must-not-fail instruction is marked and **positioned near the top**, but competes with one other marked item. |
> | 5 | The must-not-fail instruction is marked and positioned so it cannot be missed. |

Day 12's own After example puts the marked instruction **last**:

> `days/12.md:21` — "... Summarise your findings in five bullets at the end. IMPORTANT: do not suggest changing the public API — it's frozen for this release."
> `days/12.md:23` — "Marked and moved to stand alone **at the end**, it reads as the one thing that cannot slip."
> `days/12.md:31` (Novice tier) — "Mark that instruction IMPORTANT: and **move it to stand alone at the end**, then send the completed prompt."

A learner who follows the Novice tier verbatim produces a prompt anchor 4 cannot describe. The tutor must then either score it 3 ("its position in the prompt still lets it get skimmed past", `rubrics.md:141`) — punishing correct compliance — or jump to 5 through the unfalsifiable clause. Both happen; that is unrepeatable scoring on the lesson's own model answer.

The contradiction is three-way: `context-ordering`'s fastest fix is "task first, material second, **constraints last**" (`rubrics.md:257`), and day 12's marked item is a constraint. A learner cannot satisfy interjection-4 and context-ordering-5 in the same prompt.

**Minimal fix:** replace "positioned near the top" with the position-independent property the day actually teaches — "positioned where it cannot be skimmed past (standing alone, not mid-paragraph)".

### DEFECT-R14 — Interjection anchor 5 restates the goal instead of stating a test — severity: medium

`rubrics.md:143`

> | 5 | The must-not-fail instruction is marked and positioned so it cannot be missed. |

"Cannot be missed" is the outcome the rubric exists to measure, not a criterion for measuring it. Missed by whom, over what output? Anchor 3 uses the same untestable frame ("lets it get skimmed past"). Day 12 has the concrete version — "Standing alone, the same sentence becomes the hardest thing to have missed" (`days/12.md:7`) and "The marker is only honest if rare. If everything is IMPORTANT, nothing is" (`days/12.md:9`).

**Minimal fix:** 5: "exactly one marker in the prompt, on the highest-stakes instruction, standing alone as its own line."

### DEFECT-R15 — Interjection anchor 2 requires knowing the highest-stakes instruction — severity: medium

`rubrics.md:140`

> | 2 | A priority word is used ("important:") but attached to something that isn't actually the highest-stakes instruction. |

Same class as DEFECT-R03: "actually the highest-stakes" is unwritten intent, and `rubrics.md:5` forbids scoring intent. Two tutors ranking the stakes differently score 2 or 4 for the same text.

**Minimal fix:** elicit it once — "the learner names the instruction they would be angriest to see ignored; score against that" — mirroring the fastest fix at `rubrics.md:145` and `days/12.md:11`.

### DEFECT-R16 — Particle is unscoreable for the prompt day 13 tells the learner to write — severity: high

`rubrics.md:153-157` against `days/13.md:11`

> | 1 | Phrasal verbs used loosely, so the operation is ambiguous (look up / look over / look into). |
> | 4 | Every phrasal verb is chosen deliberately, with only cosmetic substitutions available. |
> | 5 | Every phrasal verb chosen deliberately; no substitution preserves the meaning. |

Day 13's test ends: "swap the particle for a plausible alternative. If the task changed, keep it. **If it didn't, use a plain verb instead.**" (`days/13.md:11`; the same rule at `days/13.md:9`: "If two particles satisfy your prompt equally well, neither is load-bearing"). A learner who complies produces a prompt with **zero phrasal verbs**. Anchors 1–3 do not apply; anchors 4 and 5 are vacuously true ("every phrasal verb" over an empty set). One tutor scores 5 on a vacuous truth, another scores 1 because no particle is doing work. This is a lever score written to `PROGRESS.md` and used for secondary-constraint routing (`SKILL.md:30`), so the divergence propagates.

This also collides with `verb`, which rewards "the most precise verb available" (DEFECT-R02) — following the verb rubric removes the phrasal verbs the particle rubric needs.

**Minimal fix:** the N/A rule from DEFECT-R09, plus rewording 4/5 as "each phrasal verb present is load-bearing, and no plain verb would have served" — which scores the day's actual instruction rather than presupposing phrasal verbs.

### DEFECT-R17 — Particle 4 and 5 assert the same thing twice — severity: low

`rubrics.md:156-157`

"only cosmetic substitutions available" (4) and "no substitution preserves the meaning" (5) are near-complements stated so loosely that a cosmetic substitution — one that preserves meaning — is exactly what 5 forbids and 4 permits, with no way to tell a cosmetic substitution from a meaning-preserving one. Separately, "no substitution preserves the meaning" is close to always false: "look over" / "look through" are interchangeable in many sentences, so anchor 5 is hard to occupy honestly.

**Minimal fix:** grade by count of load-bearing particles rather than by the existence of substitutions.

### DEFECT-R18 — Role framing 4/5 turn on "you can say how", with no stated "you" — severity: medium

`rubrics.md:170-171`

> | 4 | Role changes what is included, excluded and assumed, though the mechanism is only implied, not stated. |
> | 5 | Role changes what is included, excluded and assumed, and you can say how. |

If the mechanism is implied strongly enough that the scorer can articulate it, the scorer "can say how" — and anchor 4 collapses into 5. Whose articulation counts (learner's? tutor's? the prompt's own text?) is never fixed. Day 15 has the countable test the rubric omits: "list two things the output contains because of it that it wouldn't contain otherwise. Fewer than two, and the role is decoration" (`days/15.md:11`).

**Minimal fix:** import the count — 4: "the role text names one thing it changes"; 5: "the role text names two or more, and each is checkable against the output."

### DEFECT-R19 — Role framing's Measures line names an output effect the loop never measures — severity: medium

`rubrics.md:163`

> **Measures:** whether the role changes the output.

Anchors 2–5 score properties of the prompt text; only anchors 1 and the Measures line refer to the output. Establishing "whether the role changes the output" requires an A/B run with and without the role, which the daily loop does not perform — `SKILL.md:32-34` runs the learner's prompt once and the tutor's rewrite once, and `days/15.md` never asks for a role-stripped control. A tutor reading the Measures line literally will either invent a third run or score something the anchors do not describe.

**Minimal fix:** restate as "whether the prompt says what the role changes" — matching what anchors 2–5 actually inspect.

### DEFECT-R20 — Few-shot anchors 1 and 2 invert: adding a second easy example lowers the score — severity: medium

`rubrics.md:181-183`

> | 1 | No examples, or examples that only show the easy case. |
> | 2 | One example given, showing a typical case with nothing instructive about its edges. |
> | 3 | Examples show variety, but none demonstrates a boundary or a near-miss. |

One typical example matches 2. **Three** typical examples match 1's second disjunct ("examples that only show the easy case") and match neither 2 (which says "one example") nor 3 (which requires variety). The ladder therefore penalises adding examples. The inversion is real and reachable — a learner told "give a few examples" hits it immediately.

**Minimal fix:** make anchor 1 "no examples" only, and anchor 2 "one or more examples, all typical, none instructive about the edges."

### DEFECT-R21 — Output schemas anchor 4 hedges with "in most cases" — severity: low

`rubrics.md:198`

> | 4 | An exact structure is given, checkable in most cases, with one edge (e.g. empty values) unaddressed. |

The trailing clause supplies a real, checkable referent — the unaddressed edge — and `days/17.md:8,29-33` makes the empty-value case concrete, so this anchor is occupiable. "checkable in most cases" is redundant with it and invites a second, vaguer reading. This is the best-behaved technique rubric in the file; the note is wording only.

**Minimal fix:** delete "checkable in most cases,".

### DEFECT-R22 — Task decomposition anchor 4 is anchor 5 with "mostly" — severity: high

`rubrics.md:212-213`

> | 4 | Work split so each step has one output and a mostly clear input from the last. |
> | 5 | Work split so each step has one output and a clear input from the last. |

The rows differ by one word, with no referent for it. Nothing in the file says what makes an input "clear", so 3, 4 and 5 all rest on the same undefined term ("one step's output isn't a clean input to the next", `rubrics.md:211`).

Day 18 has a fully mechanical test — "check whether each half's input is **verbatim** the other half's output — not a paraphrase, the actual text" (`days/18.md:11`) — and commit `3e48ea7` removed the equivalent sentence from the day's Concept while never adding it to the rubric. The one checkable referent in the course for this property lives in a single line of one day file and nowhere in the rubric.

**Minimal fix:** import it — 4: "each step has one output, and the next step's input is the previous output plus at most one added instruction"; 5: "each step's input is verbatim the previous step's output, nothing added, nothing re-explained."

### DEFECT-R23 — Reasoning scaffolds anchor 5 does not exclude anchor 4 — severity: high

`rubrics.md:226-227`

> | 4 | The reasoning steps asked for match the ones the task requires, with minor slack in ordering. |
> | 5 | The reasoning steps asked for match the ones the task requires. |

Anchor 5 states only the matching condition, which anchor 4 also states in full. Ordering enters the ladder at 4 and vanishes at 5, so a prompt with correctly-matched steps in a sloppy order satisfies 5's text exactly. Same structural defect as DEFECT-R02. "Minor slack" has no referent.

Ordering is also scored by two other rubrics — `conjunction` anchor 4/5 ("the order of checks", `rubrics.md:100-101`) and `context-ordering` — so the axis is both misplaced here and duplicated elsewhere.

**Minimal fix:** either restore ordering to 5 ("...match the ones the task requires, in the order the task requires") or strike it from 4 and differentiate on completeness ("4: matches, with one step named that the answer does not depend on").

### DEFECT-R24 — Reasoning scaffolds fastest fix is singular; the scored property is set-match — severity: medium

`rubrics.md:229`

> **Fastest fix:** name the intermediate you want to see before the answer.

Naming one intermediate moves a prompt from 2 to 3 at best — anchor 3 is precisely "Some intermediate steps are named, but one that the task actually depends on is missing" (`rubrics.md:225`). What separates 4 and 5 is the *set* matching: no padding, no omissions. Day 19 states this exactly ("Anything named that isn't on it, cut. Anything on the list that isn't named, add", `days/19.md:11`; and the Working tier "no more, no fewer", `days/19.md:33`), so the day and the rubric's fastest fix disagree about what to do.

Historical note relevant to the brief: this rubric is the one whose day was rebuilt. Commit `3e48ea7` rewrote day 19 away from a gating heuristic ("the scaffold has to gate the answer too ... forbid answering until they exist") because no anchor scores gating. The day now says gating is "useful, but secondary" (`days/19.md:7`). The fastest fix survived that rewrite unchanged and is now the stale half.

**Minimal fix:** "list what the answer depends on; name every item on that list and nothing else."

### DEFECT-R25 — Negative constraints anchor 5 scores the learner's history, not the prompt — severity: medium

`rubrics.md:240-241`

> | 4 | Exclusions are specific and mostly map to failures you've seen, with one still speculative. |
> | 5 | Exclusions are specific, and each prevents a failure you have actually seen. |

"A failure you have actually seen" is unverifiable from the text and unfalsifiable by the tutor — the learner can simply assert it. Day 20's model answer solves this by putting the incident **in the prompt** ("Do not invent a field name that isn't in the source data — **last time you added 'priority' when it wasn't a column**", `days/20.md:20`), which makes it checkable. The rubric never requires that.

**Minimal fix:** 5: "each exclusion cites the incident it prevents, in the prompt." That makes it text-checkable and keeps `rubrics.md:5` honest. Anchor 4 is otherwise well-formed (the "one still speculative" clause is a real referent).

### DEFECT-R26 — Context ordering anchor 5 abandons the criterion anchors 3 and 4 use — severity: medium

`rubrics.md:253-255,257`

> | 3 | Instruction is findable, but constraints are scattered rather than grouped at the end. |
> | 4 | Instruction and context are ordered sensibly, with constraints mostly grouped but one placed early. |
> | 5 | Instruction and context ordered so the model reads what it needs when it needs it. |

Anchors 3 and 4 are checkable against a fixed template (instruction findable; constraints grouped at the end). Anchor 5 drops it for a purpose statement no tutor can verify by inspection. The concrete version of 5 is already written one line below in the fastest fix — "task first, material second, constraints last" — and is the day's title (`days/21.md:1`).

**Minimal fix:** 5: "task first, material second, constraints grouped last."

### DEFECT-R27 — Context ordering anchor 1's second disjunct measures completeness, not order — severity: medium

`rubrics.md:251`

> | 1 | Instruction buried after a wall of context, **or context missing where needed**. |

The Measures line is "placement of instruction and material" (`rubrics.md:247`). Missing context is a coverage failure, not a placement failure, and no other anchor on this ladder mentions it — so a prompt with perfect ordering and one missing fact scores 1 on a rubric about ordering. Day 21 is emphatic that this is a reorder and not a rewrite: "This is a pure reorder, not a trim" (`days/21.md:9`), and the After block is the Before block's words rearranged with nothing added.

**Minimal fix:** delete "or context missing where needed".

### DEFECT-R28 — System prompts 3 and 4 are opposite leak directions, not two degrees — severity: medium

`rubrics.md:267-268`

> | 3 | Durable rules and turn request are mostly separated, but one standing rule is restated per turn out of habit. |
> | 4 | Standing behaviour and per-turn request are separated into two blocks, but one line in the system prompt is turn-specific and could move to the per-turn request without changing behaviour. |

Anchor 3 is the standing→turn leak (redundant restatement); anchor 4 is the turn→system leak (a landmine). Day 22 names them as two independent directions of the same failure — "Leakage runs both ways" (`days/22.md:9`) — and does not rank one as worse. A prompt with only the type-4 leak is arguably cleaner than one with only the type-3 leak, yet the ladder forces a ranking. A prompt with both fits neither row.

Anchor 4 is otherwise the best-repaired anchor in the file (commit `9041425`) — concrete, occupiable, and countable.

**Minimal fix:** grade by count of leaking lines regardless of direction — 3: "two or more lines leak, in either direction"; 4: "exactly one line leaks".

### DEFECT-R29 — Agent-and-tool anchor 5 does not exclude anchor 4 — severity: high

`rubrics.md:282-283`

> | 4 | Which tools, when, and what "done" means are all stated, though the done-condition could still be gamed. |
> | 5 | Which tools, when, and what "done" means are all stated. |

Anchor 5's text is a strict subset of anchor 4's; gameability appears only as a negative in 4 and is never stated positively at 5. Day 23 is explicit that gameability *is* the separator — "What separates strong from merely adequate is whether 'done' can be gamed: 'stop when you've made a change' is satisfied by a change that does nothing useful, while 'stop when the tests pass and you can point to the fix' can't be satisfied by motion alone" (`days/23.md:7`) — so the intent is unambiguous and the rubric simply fails to record it.

**Minimal fix:** 5: "...are all stated, and the done-condition names a checkable state that motion alone cannot satisfy."

### DEFECT-R30 — Agent-and-tool fastest fix names an ordering day 23 explicitly declares unscored — severity: medium

`rubrics.md:285` against `days/23.md:9`

> **Fastest fix:** state the stop condition first, then the tools.

No anchor on this ladder scores order. Day 23 says so in as many words: "Stating the condition before the tools is a useful habit, **not a scored one** — tools listed first with an airtight, ungameable condition after them score no lower" (`days/23.md:9`), and its Novice tier says "all three stated, **in any order**" (`days/23.md:31`).

This is the exact defect class the brief flags — a fastest fix naming a property the anchors do not score. Day 23 was already rewritten to disclaim it (its title, "the stop condition first", is the residue); the rubric line is the surviving stale half. A tutor who reads the fastest fix and not `days/23.md:9` will mark down a compliant prompt for its ordering.

**Minimal fix:** "make the done-condition un-gameable, then name which tool serves which situation." Half the current fix is valid — stating a stop condition at all moves 1/2/3 → 4 — so only the "first" needs removing.

### DEFECT-R31 — Self-critique anchor 5 does not exclude anchor 4 — severity: high

`rubrics.md:296-297`

> | 4 | A check the model can apply to its own output is given, with an action on failure that's only loosely defined. |
> | 5 | A check the model can apply to its own output, with a stated action when it fails. |

A loosely-defined action is still a stated action, so every anchor-4 prompt satisfies anchor 5's text. "Only loosely defined" has no referent. The real ladder underneath (`rubrics.md:295-297`) is: no action / vague action / specific action — and day 24 supplies the specific version ("if any claim doesn't trace to something in the source, **cut it or mark it 'unverified'**", `days/24.md:21`), an action naming a concrete operation.

**Minimal fix:** 4: "an action on failure that names no operation ('fix it', 'try again')"; 5: "an action naming what to do to the failing element."

### DEFECT-R32 — Writing evals introduces a binary timing precondition at anchor 4 only — severity: medium

`rubrics.md:307-311`

> | 3 | Criteria are written and mostly objective, but one is still a judgement call. |
> | 4 | **Criteria written before the output**, specific enough that two people would agree most of the time. |

Anchors 1–3 grade objectivity. Anchor 4 adds an unrelated, binary precondition — written before the output — with no partial state. A learner with three perfectly objective criteria written after seeing the output caps at 3 no matter how good they are, and the ladder gives no signal about which failing caused it. Day 25 treats the timing as the whole point ("The order is the whole discipline", `days/25.md:9`), which argues it should carry the ladder from anchor 1, not appear at 4.

**Minimal fix:** put timing on the ladder from the bottom (1: no criteria; 2: criteria written after the output; 3+: criteria written before, graded by objectivity).

### DEFECT-R33 — Writing evals 4/5 ask one scorer to predict inter-rater agreement — severity: high

`rubrics.md:310-311`

> | 4 | Criteria written before the output, specific enough that two people would agree **most of the time**. |
> | 5 | Criteria written before the output, specific enough that two people would **score the same**. |

Both anchors require a single tutor to forecast how two hypothetical scorers would behave, and 4 asks for that forecast as a frequency ("most of the time") with no threshold. Nothing in the loop produces a second scorer. The rubric whose entire purpose is measuring whether criteria are repeatable is itself the least repeatable rubric in the file. Anchor 2 has the same frame ("subjective enough ... that two scorers would diverge", `rubrics.md:308`), but there the divergence is the failure being named, so it survives; at 4/5 it is the measurement instrument.

Day 25 has a workable substitute: "show your criteria to someone who hasn't seen the output. Could they score it without asking you what you meant?" (`days/25.md:11`) — a yes/no test on the criteria text.

**Minimal fix:** 4: "each criterion states a checkable property, but at least one needs the writer present to interpret"; 5: "every criterion is scoreable by a reader who has not seen the output and cannot ask the writer."

### DEFECT-R34 — Token economy 4/5 score process evidence not present in the prompt — severity: low

`rubrics.md:324-325`

> | 4 | Every included token earns its place on inspection, but the cuts have not been tested against the output to confirm accuracy held. |
> | 5 | Every included token earns its place; cuts made without losing accuracy. |

The separator is whether a cut was *tested*, which is not a property of the prompt (`rubrics.md:5`). It is rescued in practice: day 26's exercise makes every tier cut and rerun (`days/26.md:31,35,39`), so the tutor observes the test happening. Worth recording because the rescue lives in one day file, not in the rubric — anyone scoring this rubric outside day 26 has no way to establish anchor 5.

This anchor pair is otherwise well-formed and is one of `9041425`'s successful repairs.

**Minimal fix:** anchor 5 to the observable — "the cut version was rerun and the output held" — so the evidence is named.

### DEFECT-R35 — Failure diagnosis narrows from "lever or technique" to "lever" at anchor 4 — severity: medium

`rubrics.md:336-339,341` against `days/27.md:7`

> | 2 | A cause is guessed at, but it isn't named as one of the specific **levers or techniques**. |
> | 3 | A **lever or technique** is named as the cause, but the fix doesn't actually target it. |
> | 4 | The failing **lever** is identified by name and the fix changes that lever ... |
> | 5 | The failing **lever** is identified by name and the fix targets it. |
> **Fastest fix:** ask which of **the 11 levers** was underspecified, and fix that one.

A learner who correctly diagnoses a *technique* failure — no output schema, no stop condition, examples that teach nothing — and fixes exactly that cannot be described by anchor 4 or 5, and the fastest fix routes them away from techniques entirely. Day 27 is unambiguous that techniques count: "A real diagnosis names one of the eleven levers **or one of the techniques from the last two weeks**: the pronoun had no antecedent, **the stop condition was never stated**, the reasoning steps weren't named" (`days/27.md:7`); its Working tier says "the single lever or technique responsible" (`days/27.md:33`). Day 27 runs after day 23, so a stop-condition diagnosis is the likely case.

**Minimal fix:** say "lever or technique" in anchors 4 and 5 and in the fastest fix. Text-only; no slug change.

### DEFECT-R36 — Prompt library anchor 4 grades against an unknowable denominator — severity: medium

`rubrics.md:352-353`

> | 4 | Reusable prompts stored with their slots and **most** known failure modes noted. |
> | 5 | Reusable prompts stored with their slots and their known failure modes. |

"Most known failure modes" requires the scorer to know the full set of failure modes the learner knows — which exists only in the learner's head. Two tutors cannot converge, and the learner can move themselves between 4 and 5 by recalling more or fewer. Anchor 3 is well-formed by contrast (slots marked, no failures recorded).

Day 28 supplies a countable version: "would they know, before running it, **the one way** it's failed before?" (`days/28.md:11`) and the model answer records exactly one ("Known failure: invents a risk when fewer than five exist", `days/28.md:7`).

**Minimal fix:** 4: "slots marked and at least one failure mode recorded, but not specifically enough for a stranger to recognise it"; 5: "...recorded specifically enough that a stranger would recognise the failure before running it."

### DEFECT-R37 — Prompt library fastest fix reaches only anchor 3 — severity: medium

`rubrics.md:355`

> **Fastest fix:** save the prompt with the task slot left as a blank.

Marking the slot is precisely anchor 3 ("Saved prompts mark their variable slots, but don't record how they've failed before", `rubrics.md:351`). The fix says nothing about failure notes, which is the only property separating 3 from 4 and 5. Day 28 says as much: "Marking the slot without the failure gets you partway" (`days/28.md:9`). A learner who follows the fastest fix and stops has, by the rubric's own text, capped themselves at 3.

**Minimal fix:** "save the prompt with the task slot blank, and one line naming the way it failed last time."

### DEFECT-R38 — Capstone drops its robustness axis after anchor 3, so anchor 5 is satisfiable by an untested prompt — severity: high

`rubrics.md:359,363-367`

> **Measures:** production readiness.
> | 1 | Prompt works once, on the example it was written against. |
> | 2 | Prompt works on a couple of close variants, but hasn't been tried on anything unlike the original case. |
> | 3 | Prompt is specified and works on varied cases, but has no written evaluation criteria. |
> | 4 | Prompt is specified and evaluated against written criteria, with failure modes noted but not systematically. |
> | 5 | Prompt is specified, evaluated against written criteria, and its failure modes documented. |

Three axes run through five rows: robustness (1→2→3), written evaluation (3→4), documentation (4→5). Robustness is never mentioned again after anchor 3, so a prompt that has only ever run on its original case — but is specified, has written criteria, and has documented failure modes — matches every word of anchor 5. That is the exact opposite of "production readiness", and it is reachable: day 30's Novice tier runs the prompt "once more on **the same case**" (`days/30.md:29`).

**Minimal fix:** carry robustness into 4 and 5 — 4: "...and holds on varied cases, with failure modes noted"; 5: "...and holds on a case it was not designed for, with failure modes documented."

### DEFECT-R39 — Capstone 4/5 turn on "systematically", which nothing defines — severity: medium

`rubrics.md:366-367` and `days/30.md:9`

> | 4 | ... with failure modes noted but not systematically. |
> | 5 | ... and its failure modes documented. |

The separator is "noted" vs "documented", qualified by "not systematically". Day 30 restates the two rows verbatim without adding a test — "anchor 5, the same evaluation with failure modes 'documented' rather than just 'noted'" (`days/30.md:9`) — so the course's only elaboration is a tautology. Day 30's Working tier does contain a usable criterion, unused by the rubric: "write the failure mode down specifically enough that **someone else could recognise it**" (`days/30.md:33`).

**Minimal fix:** import the day-30 Working-tier test into anchor 5 and make 4 the row where the note exists but is not recognisable to a third party.

### DEFECT-R40 — Capstone fastest fix targets the axis that stops at anchor 3 — severity: medium

`rubrics.md:369`

> **Fastest fix:** run it on the case you did not design it for.

That is the robustness move (1/2 → 3), the axis the ladder abandons after anchor 3 (DEFECT-R38). It does nothing for the criteria and documentation steps that separate 3 from 4 and 5.

Related, and by design rather than by defect: this rubric is cited by two days. Day 29 caps itself at anchor 3 explicitly ("Reaching that rung honestly caps you at anchor 3. Anchors 4 and 5 need written criteria and documented failures — day 30's work", `days/29.md:9`; also `days/29.md:21,37`). The rubric itself gives no hint that 4 and 5 are out of reach on day 29, so a tutor who reads the rubric and skims the day will score against an unreachable top half.

**Minimal fix:** "run it on a case you did not design it for, then write the criteria that would have caught what broke." Optionally note in the rubric that anchors 4–5 require day 30's work.

### DEFECT-R41 — "Criterion by criterion" is degenerate for all 26 rubrics — severity: medium

`SKILL.md:34` against the whole file

> Score the prompt against the rubric named in the day's `## Rubric` section, **criterion by criterion**, 1–5, quoting the rubric's anchor for each score you give.

Every rubric in the file has exactly one criterion: one `**Measures:**` line and one 1–5 ladder. On the 24 days that cite a single rubric, "criterion by criterion" reduces to "give one number". It carries meaning only where a day cites several rubrics — day 6 and day 7 (five levers each: `days/06.md:43`, `days/07.md:39`) and day 14 (all eleven: `days/14.md:41`) — where "criterion" silently means "rubric".

The sharper problem is the inverse. Five rubrics **do** bundle multiple independent criteria into a single number, and those are precisely the ones the instruction would help if it could be followed:

- `preposition` (`rubrics.md:87`) — three: boundaries, audience, exclusions.
- `agent-and-tool-prompting` (`rubrics.md:283`) — three: which tools, when, what "done" means.
- `conjunction` (`rubrics.md:101`) — three: condition, fallback, order.
- `output-schemas` (`rubrics.md:197`) — three: fields, types, order/optionality.
- `capstone` (`rubrics.md:363-367`) — three: robustness, written evaluation, documentation (see DEFECT-R38).

A prompt strong on two of three and absent on the third has no correct score in any of these, and the tutor cannot report the split because there is one row to quote.

**Minimal fix:** either give those five rubrics sub-criteria with their own 1–5 rows, or reword `SKILL.md:34` to "anchor by anchor" and accept that most days yield one number.

## Cross-rubric analysis

### Direct contradictions between rubrics

1. **`interjection` anchor 4 vs `context-ordering`.** Anchor 4 requires the must-not-fail instruction "positioned near the top" (`rubrics.md:142`); `context-ordering`'s fastest fix requires "constraints last" (`rubrics.md:257`), and day 12's marked item is a constraint placed last (`days/12.md:21,31`). A prompt cannot score 4 on the first and 5 on the second. See DEFECT-R13.
2. **`verb` vs `particle`.** `verb` rewards the narrowest verb available (`rubrics.md:30`); `particle` requires phrasal verbs to exist in order to score them (`rubrics.md:153-157`), and day 13 tells the learner to fall back to a plain verb when no particle is load-bearing (`days/13.md:11`). Following one rubric's advice makes the other unscoreable. See DEFECT-R02, DEFECT-R16.

### Nearest-neighbour pairs and how cleanly they separate

| Pair | Overlap | Separation |
|---|---|---|
| `adverb` / `numeral` | `adverb` anchor 2 fails a manner word "without a measure" (`rubrics.md:56`); a measure is normally a numeral. Reaching adverb 3+ usually requires satisfying numeral. | **Clean enough.** Day 4 shows a non-numeric manner spec — "Line by line, checking each function against its callers" (`days/04.md:7`) — so adverb has territory numeral does not. |
| `preposition` / `negative-constraints` | Both score exclusions: "without what" (`rubrics.md:87`) vs "what is ruled out" (`rubrics.md:233`). | **Thin.** A clause like "do not mention pricing" is scoreable under either and no rule assigns it. Separation intended: preposition = static topic boundary; negative-constraints = a forbidden *failure mode tied to an observed incident*. State that in the Measures lines. |
| `interjection` / `context-ordering` | Interjection anchors 3–5 are all about position in the prompt; context-ordering is about global sequence. | **Contradictory, not merely overlapping.** See above. |
| `conjunction` / `reasoning-scaffolds` / `context-ordering` | Order-of-things is scored three times: conjunction 4/5 "the order of checks" (`rubrics.md:100-101`), reasoning-scaffolds 4 "minor slack in ordering" (`rubrics.md:226`), context-ordering wholesale. | **Muddy.** Reasoning-scaffolds is the weak link — ordering appears only at anchor 4 and vanishes at 5 (DEFECT-R23). Removing it there leaves a clean split: conjunction = order of *branch evaluation*; context-ordering = order of *prompt sections*. |
| `writing-evals` / `self-critique-loops` | Both score "criteria the output is checked against"; their anchor-2 rows are near-twins ("a check is mentioned ... with no criteria", `rubrics.md:294`; "Criteria exist but are subjective enough", `rubrics.md:308`). | **Clean in intent, unstated in text.** self-critique = the *model* checks itself, inside the prompt, with an action on failure; writing-evals = the *human* writes criteria before the output. Neither Measures line says who does the checking. |
| `writing-evals` / `capstone` | Capstone anchors 3, 4 and 5 all hinge on "written evaluation criteria" (`rubrics.md:365-367`) — the whole subject of `writing-evals`. | **Not separated.** Two-fifths of the capstone ladder re-scores day 25's rubric. Day 30 says so outright: "written criteria — day 25's discipline" (`days/30.md:7`). |
| `capstone` / `prompt-library` | Capstone 5's "failure modes documented" (`rubrics.md:367`) is `prompt-library` 5's "their known failure modes" (`rubrics.md:353`). | **Not separated.** Capstone is largely `writing-evals` + `prompt-library` + a robustness axis it drops at anchor 3 (DEFECT-R38). If the robustness axis were carried to the top, capstone would have something of its own. |
| `token-economy` / `noun` 5 / `adjective` 5 | Economy is scored in three places: "no words spent on the artifact beyond what pins it down" (`rubrics.md:17`), "none that do not — each word does rejection work" (`rubrics.md:45`), and the whole of `token-economy`. | **Double-scored.** The two lever anchors punish verbosity on ladders whose Measures lines are about artifact and quality. See DEFECT-R01, DEFECT-R04. |
| `task-decomposition` / `agent-and-tool-prompting` | Both score step sequencing and hand-off between stages. | **Clean.** Decomposition scores the *seam* between two prompts; agent-and-tool scores tool selection and the stop condition. No anchor collides. |
| `negative-constraints` / `failure-diagnosis` | Both anchor on failures the learner has actually observed (`rubrics.md:241`, `rubrics.md:339`). | **Clean.** Different objects — one scores a prompt's exclusions, the other scores a diagnosis. |

### Properties the course teaches that no rubric scores

1. **Composition — levers not fighting for the same space.** Day 6's core claim is that a composed prompt is "not five sentences bolted together. It's one sentence carrying five jobs, each done by one word or phrase, **none fighting for the same space**" (`days/06.md:9`), and day 7 adds "every clause, if removed, visibly weakens the result" (`days/07.md:9`). Days 6 and 7 score against the five individual lever rubrics (`days/06.md:43`, `days/07.md:39`), each of which is blind to the others by construction. Nothing scores the composition itself. This is the largest genuine gap: two of thirty days teach a property with no rubric.
2. **Example non-redundancy.** Day 16's test is "could either example be swapped for a different instance of the same pattern without changing what the model would learn?" (`days/16.md:11`). The `few-shot-examples` anchors score coverage of the boundary and failure cases (`rubrics.md:184-185`), not whether each example is load-bearing. Anchor 3's "Examples show variety" is the nearest thing and does not reach it.
3. **Un-gameability of a stop condition** is taught as the strong/adequate separator (`days/23.md:7`) but appears in the rubric only as a negative inside anchor 4, never positively at 5. See DEFECT-R29.
4. **Predict-before-you-run** appears in three days' tiers (`days/21.md:39`, `days/26.md:39`, `days/27.md:37`) and is scored by nothing. Arguably fine — it is a study habit, not a prompt property — but worth recording so it is not mistaken for an omission.
5. **Day 21's weak-lever practice is never rescored.** `SKILL.md:59` designates days 14 and 21 as review days drawing on the three lowest-scoring levers; day 21 duly builds its exercise around them (`days/21.md:31,43`). But day 21 scores only `context-ordering` (`days/21.md:47`), and `SKILL.md:20` states that "a lever's score changes only when the day actually scored it". So day 21's targeted lever work leaves `PROGRESS.md` untouched, and those levers stay eligible for secondary-constraint routing forever. Day 14 does not have this problem — it scores all eleven (`days/14.md:41`).

### Deliberately-unscored property, for the record

Gating the answer on named intermediates was removed from day 19 in commit `3e48ea7` and is now explicitly demoted — "Naming steps can also gate the answer on them — useful, but **secondary** to getting the list right" (`days/19.md:7`). That is coherent: the `reasoning-scaffolds` anchors score set-match, not gating, and the day now agrees. The residue is the fastest fix (DEFECT-R24), which was not updated with the day.

### Slug risk

No fix recommended above touches a `## ` heading, so no day file breaks. For reference, if any heading were changed:

- Any of the eleven lever headings breaks its own day, plus `days/06.md:43` and `days/07.md:39` (noun, verb, adjective, adverb, preposition), plus `days/14.md:41` (all eleven) — up to three day files each — and would desynchronise the `## Levers` key names in `PROGRESS.md` (`assessment.md:65-67`), which `SKILL.md:16` reads by name.
- `## Capstone` breaks two days (`days/29.md:41`, `days/30.md:41`).
- Each of the other fourteen technique headings breaks exactly one day.
- `assessment.md:13` cites `rubrics.md` for all eleven levers without slugs, so it survives a rename but would then point at renamed rubrics with unchanged `PROGRESS.md` keys.

Any such change is high severity by the standing rule and should be avoided; every defect above is fixable inside anchor text, `**Measures:**` lines, `**Fastest fix:**` lines, or the preamble at `rubrics.md:3-5`.

## Counts

- **High: 12** — R02, R05, R09, R11, R13, R16, R22, R23, R29, R31, R33, R38
- **Medium: 26** — R01, R03, R04, R06, R07, R08, R10, R12, R14, R15, R18, R19, R20, R24, R25, R26, R27, R28, R30, R32, R35, R36, R37, R39, R40, R41
- **Low: 3** — R17, R21, R34
- **Total: 41** across 26 rubrics. Rubrics with no substantive defect: none — `output-schemas` (wording only) and `token-economy` (evidence sourcing only) are the cleanest.
