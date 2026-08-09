# Rubrics

One rubric per lever and per technique. Every lesson scores against a rubric here rather than restating criteria, so the same weakness gets the same name on day 3 and on day 27.

Scores are 1–5. Anchors are given for every point. Score the prompt as written, not the intent behind it.

If the task has no instance of the property the rubric measures — no branch to state, no phrasal verb, no competing instructions, no case where an example would teach anything — score the lever N/A rather than 1, and leave its `PROGRESS.md` entry untouched.

## Noun

**Measures:** the artifact the prompt asks for, and the words spent naming it.

| Score | Anchor |
|---|---|
| 1 | No artifact named. The prompt describes a topic or a wish, not a thing to produce. |
| 2 | A category is named ("a review", "some notes") but its shape is left open. |
| 3 | The artifact is recognisable, but a reasonable reader could still deliver two different things. |
| 4 | The artifact is named unambiguously. Someone reading only the prompt could describe the finished output. |
| 5 | Named unambiguously and economically — no words spent on the artifact beyond what pins it down. |

**Fastest fix:** ask what physical thing lands when the model finishes. Put that noun phrase in the prompt.

## Verb

**Measures:** the operation requested.

| Score | Anchor |
|---|---|
| 1 | No verb, or one that names no operation ("help", "look at"). |
| 2 | A verb is present but names a family of operations, not one ("handle", "deal with"), so the model must guess which. |
| 3 | An operation is named, but a nearby operation would satisfy the same wording just as well. |
| 4 | Exactly one operation named, and it is the operation wanted, but expressed with a generic synonym ("check" instead of "audit") where a more specific verb in the same family exists. |
| 5 | Exactly one operation named, it is the operation actually wanted, and no verb in the same family names it more narrowly. |

**Fastest fix:** name the operation: summarise, rank, critique, refactor, enumerate.

## Adjective

**Measures:** quality constraints on the artifact.

| Score | Anchor |
|---|---|
| 1 | No quality named; any output passes. |
| 2 | A quality is named but so generically ("good", "high-quality") that it rules nothing out. |
| 3 | Of the qualities the writer names as rejection-triggers, one is in the prompt and a second is not. |
| 4 | Every quality the writer names as a rejection-trigger is in the prompt, and no others are. |
| 5 | Every rejection-trigger is named and no others are, and each is worded specifically enough that a generic output visibly fails one. |

**Fastest fix:** list the two qualities that would make you reject the output, then state them.

## Adverb

**Measures:** manner and degree of the action.

| Score | Anchor |
|---|---|
| 1 | Manner unspecified; depth left to chance. |
| 2 | A manner word is used ("briefly", "carefully") but without a measure, so two readers would produce different depths. |
| 3 | Depth or manner is set for part of the task, but another part is left to guess. |
| 4 | Depth and manner set with a measure attached across the whole task, but attached as a stated tolerance rather than a fixed figure, so two competent readers would land inside that tolerance rather than on the same length. |
| 5 | Depth and manner set with a measure attached to every part, so two competent readers would produce the same length and thoroughness. |

**Fastest fix:** say how thoroughly, and in what manner.

## Preposition

**Measures:** scope and relation.

| Score | Anchor |
|---|---|
| 1 | No scope; the task could touch anything. |
| 2 | One boundary is given (e.g. audience) but others (what's excluded, for whom) are missing. |
| 3 | Most of scope, audience and exclusion are set, but one relation is left implicit. |
| 4 | Boundaries, audience and exclusions are all set, but at least one could be satisfied two ways. |
| 5 | Boundaries, audience and exclusions all set so each admits exactly one reading — in what, for whom, without what. |

**Fastest fix:** add: in what, for whom, without what.

## Pronoun

**Measures:** reference binding.

| Score | Anchor |
|---|---|
| 1 | Pronouns with no antecedent ("fix it", "do this"). |
| 2 | More than one reference is unresolvable, or the prompt's main referent is ambiguous between two candidates. |
| 3 | Exactly one pronoun still requires the reader to guess; the rest resolve. |
| 4 | Every reference resolves inside the prompt or to a quoted block, but at least one antecedent sits more than a sentence away from its pronoun. |
| 5 | Every reference resolves inside the prompt or to a quoted block, and each pronoun's antecedent is the nearest preceding noun phrase. |

**Fastest fix:** replace each it/this/that with the thing it means.

## Conjunction

**Measures:** conditional logic.

| Score | Anchor |
|---|---|
| 1 | Branching cases collapsed into one instruction, so edge cases silently pick a branch. |
| 2 | One branch is acknowledged but its condition or its outcome is missing. |
| 3 | Branches and conditions are named, but the fallback (the otherwise) is missing. |
| 4 | Each branch stated with its condition and its fallback, but the order of checks is not fixed — either only one branch is stated, or the wording leaves the order between them ambiguous. |
| 5 | Two or more branches, each stated with its condition and its fallback, in an order that resolves without ambiguity. |

**Fastest fix:** write down the if/then/otherwise you are holding in your head.

## Determiner

**Measures:** definiteness and quantity binding.

| Score | Anchor |
|---|---|
| 1 | Bare nouns leave it unclear whether one, some, or all are meant. |
| 2 | A determiner is used on the main noun, but supporting nouns nearby are still bare. |
| 3 | Most nouns are bound, but one noun is left bare where swapping "the" for "any" would change what gets done. |
| 4 | Each noun is bound — the, a, each, every, any — but one binding could be read two ways without changing what gets done. |
| 5 | Each noun is bound — the, a, each, every, any — and swapping any determiner would change what gets done. |

**Fastest fix:** put the/a/each in front of every noun and see which changes the meaning.

## Numeral

**Measures:** budgets that make output checkable.

| Score | Anchor |
|---|---|
| 1 | No quantity anywhere; length and count unbounded. |
| 2 | One quantity is given (e.g. a word count) but other countable dimensions (item count, number of examples) are open. |
| 3 | Every countable dimension is bounded, but at least one bound is vague enough to need judgement ("a few", "several"). |
| 4 | Every countable dimension is bounded, and every bound is a number, but at least one is a range or an approximation rather than an exact count. |
| 5 | Every countable dimension is bounded, and every bound is an exact count or length, checkable without judgement. |

**Fastest fix:** add a count and a length you could verify with a ruler.

## Interjection

**Measures:** attention and priority markers.

| Score | Anchor |
|---|---|
| 1 | All instructions carry equal weight; the critical one is buried mid-paragraph. |
| 2 | A priority word is used ("important:") but attached to something other than the instruction the writer names as the one they would be angriest to see ignored. |
| 3 | The critical instruction is marked, but the marker sits inline in a paragraph with other instructions rather than on a line of its own. |
| 4 | The must-not-fail instruction is marked and stands alone rather than sitting mid-paragraph, but competes with one other marked item. |
| 5 | Exactly one marker in the prompt, on the instruction the writer names as highest-stakes, standing alone as its own line. |

**Fastest fix:** mark the one instruction you would be angry about being ignored.

## Particle

**Measures:** phrasal precision.

| Score | Anchor |
|---|---|
| 1 | Phrasal verbs used loosely, so the operation is ambiguous (look up / look over / look into). |
| 2 | A phrasal verb is used, and swapping its particle would plausibly change the intended task without the writer noticing. |
| 3 | The phrasal verb is close to right, but a stricter synonym would remove a small remaining ambiguity. |
| 4 | Each phrasal verb present was chosen deliberately, but at least one could be swapped for a plain verb without changing the task. |
| 5 | Each phrasal verb present is load-bearing and no plain verb would have served — swapping any particle changes the task. |

**Fastest fix:** swap the particle and check whether the task changed. If it did, you needed the precise one.

## Role framing

**Measures:** whether the prompt says what the role changes.

| Score | Anchor |
|---|---|
| 1 | Role asserted with no bearing on output ("you are a world-class expert"). |
| 2 | The role is domain-relevant, but nothing in the prompt tells you what it includes, excludes, or assumes differently. |
| 3 | The role implies a standard or a body of knowledge, but the prompt doesn't say which parts to draw on. |
| 4 | The role text names at least one thing the output includes, excludes or assumes because of the role, but not how the role produces it. |
| 5 | The role text names what the output includes, excludes and assumes because of the role, and says how the role produces each. |

**Fastest fix:** name the knowledge or standard the role brings; drop the flattery.

## Few-shot examples

**Measures:** what the examples teach.

| Score | Anchor |
|---|---|
| 1 | No examples. |
| 2 | One or more examples, all typical, none instructive about the edges. |
| 3 | Examples show variety, but none demonstrates a boundary or a near-miss. |
| 4 | Examples cover the boundary case but not a genuine failure case. |
| 5 | Examples cover the boundary case and the failure case. |

**Fastest fix:** add the example you would worry it gets wrong.

## Output schemas

**Measures:** the format contract.

| Score | Anchor |
|---|---|
| 1 | Format unspecified, or described in prose only. |
| 2 | A format is named ("as a table", "in JSON") but its fields or columns are not enumerated. |
| 3 | Fields are enumerated, but types, order, or optionality are left unstated. |
| 4 | An exact structure is given, with one edge (e.g. empty values) unaddressed. |
| 5 | An exact structure given, which output can be checked against mechanically. |

**Fastest fix:** write the shape you want, filled with dummy values.

## Task decomposition

**Measures:** whether the work is split correctly.

| Score | Anchor |
|---|---|
| 1 | One prompt carries several tasks that interfere. |
| 2 | The tasks are listed, but their inputs and outputs aren't separated, so they still interfere. |
| 3 | Tasks are split into steps, but one step's output isn't a clean input to the next. |
| 4 | Work split so each step has one output, and the next step's input is the previous step's output plus exactly one added instruction or re-explanation. |
| 5 | Work split so each step has one output, and each step's input is verbatim the previous step's output — nothing added, nothing re-explained. |

**Fastest fix:** find the "and then" in your prompt and cut there.

## Reasoning scaffolds

**Measures:** whether reasoning is structured where needed.

| Score | Anchor |
|---|---|
| 1 | Reasoning demanded without structure, or suppressed where it was needed. |
| 2 | Reasoning is requested, but the intermediate steps expected aren't named. |
| 3 | Some intermediate steps are named, but one that the task actually depends on is missing. |
| 4 | The reasoning steps asked for match the ones the task requires, but the prompt does not fix the order they are produced in. |
| 5 | The reasoning steps asked for match the ones the task requires, in the order the task requires them produced. |

**Fastest fix:** list what the answer depends on; name every item on that list and nothing else.

## Negative constraints

**Measures:** what is ruled out.

| Score | Anchor |
|---|---|
| 1 | No exclusions; known failure modes not ruled out. |
| 2 | An exclusion is stated, but it's generic ("don't be verbose") rather than tied to an observed failure. |
| 3 | One real failure mode is excluded, but a second, equally likely one is not. |
| 4 | Exclusions are specific and each names the failure it prevents, but at least one is speculative rather than observed, or names its failure without citing the incident in the prompt. |
| 5 | Exclusions are specific, and each cites in the prompt the incident it prevents. |

**Fastest fix:** write down what it did wrong last time, put that incident in the prompt, and forbid exactly that.

## Context ordering

**Measures:** placement of instruction and material.

| Score | Anchor |
|---|---|
| 1 | Instruction buried after a wall of context. |
| 2 | Instruction and context are both present but interleaved in a way that obscures which material serves which step. |
| 3 | Instruction is findable, but constraints are scattered rather than grouped at the end. |
| 4 | Task first, material second, with constraints grouped last except for one placed early. |
| 5 | Task first, material second, constraints grouped last. |

**Fastest fix:** task first, material second, constraints last.

## System prompts

**Measures:** separation of standing rules from the turn.

| Score | Anchor |
|---|---|
| 1 | Durable rules repeated per turn, or turn-specific detail promoted into standing rules. |
| 2 | Some durable rules are separated out, but turn-specific detail still leaks into them. |
| 3 | Standing behaviour and per-turn request are separated into two blocks, but two or more lines are on the wrong side — in either direction. |
| 4 | Standing behaviour and per-turn request are separated into two blocks, and exactly one line is on the wrong side — in either direction. |
| 5 | Standing behaviour and per-turn request are separated into two blocks, and no line is on the wrong side — in either direction. |

**Fastest fix:** ask which lines you would want true on every turn — those are the system prompt.

## Agent and tool prompting

**Measures:** tool use and stopping conditions.

| Score | Anchor |
|---|---|
| 1 | Tool use implied but not specified; no stopping condition. |
| 2 | Tools are named, but when to use each one and what counts as done are both unstated. |
| 3 | Tools and rough sequencing are given, but the stopping condition is missing or vague. |
| 4 | Which tools, when, and what "done" means are all stated, though the done-condition could still be gamed. |
| 5 | Which tools, when, and what "done" means are all stated, and the done-condition names a checkable state that motion alone cannot satisfy. |

**Fastest fix:** make the done-condition un-gameable, then name which tool serves which situation.

## Self-critique loops

**Measures:** whether output is checked.

| Score | Anchor |
|---|---|
| 1 | Single-pass output accepted with no check. |
| 2 | A check is mentioned ("review your answer") but with no criteria to check against. |
| 3 | A concrete check is named, but there's no stated action for when it fails. |
| 4 | A check the model can apply to its own output is given, with an action on failure that names no operation ("fix it", "try again"). |
| 5 | A check the model can apply to its own output, with an action on failure that names what to do to the failing element. |

**Fastest fix:** name the test the output must pass, and require it be run.

## Writing evals

**Measures:** whether quality is measurable.

| Score | Anchor |
|---|---|
| 1 | Quality judged by feel; no criteria written down. |
| 2 | Criteria written, but after the output existed, so they describe what was produced rather than what was required. |
| 3 | Criteria written before the output, but at least one names a feeling rather than a checkable property. |
| 4 | Criteria written before the output, each naming a checkable property a reader who has not seen the output could apply without asking the writer, but at least one could be applied two ways. |
| 5 | Criteria written before the output, and every criterion is specific enough that two readers who have not seen the output would produce the same score. |

**Fastest fix:** write the three checks you would apply, then apply them.

## Token economy

**Measures:** whether every token earns its place.

| Score | Anchor |
|---|---|
| 1 | Context padded with material the task never uses. |
| 2 | Some unused material is trimmed, but redundant restatements of the same instruction remain. |
| 3 | Most padding is removed, but one section is included "just in case" rather than because the task needs it. |
| 4 | Every included token earns its place on inspection, but the cuts have not been tested against the output to confirm accuracy held. |
| 5 | Every included token earns its place, and the cut version was rerun and the output held. |

**Fastest fix:** delete a third of the context and see whether the output degrades.

## Failure diagnosis

**Measures:** whether the cause is identified.

| Score | Anchor |
|---|---|
| 1 | Failure blamed on the model; prompt unchanged. |
| 2 | A cause is guessed at, but it isn't named as one of the specific levers or techniques. |
| 3 | A lever or technique is named as the cause, but the fix doesn't actually target it. |
| 4 | The failing lever or technique is identified by name and the fix changes it, but it also changes a second lever or technique that was not implicated. |
| 5 | The failing lever or technique is identified by name and the fix targets it and nothing else. |

**Fastest fix:** ask which of the 11 levers or the techniques from weeks 3–4 was underspecified, and fix that one.

## Prompt library

**Measures:** reusability.

| Score | Anchor |
|---|---|
| 1 | Prompts rewritten from scratch each time. |
| 2 | A prompt is saved, but without marking which parts change between uses. |
| 3 | Saved prompts mark their variable slots, but don't record how they've failed before. |
| 4 | Reusable prompts stored with their slots and at least one failure mode recorded, but not specifically enough for a stranger to recognise it before running the prompt. |
| 5 | Reusable prompts stored with their slots and their failure modes recorded specifically enough that a stranger would recognise each one before running the prompt. |

**Fastest fix:** save the prompt with the task slot blank, and one line naming the way it failed last time.

## Capstone

**Measures:** production readiness.

| Score | Anchor |
|---|---|
| 1 | Prompt works once, on the example it was written against. |
| 2 | Prompt works on a couple of close variants, but hasn't been tried on anything unlike the original case. |
| 3 | Prompt is specified and works on varied cases, but has no written evaluation criteria. |
| 4 | Prompt is specified, holds on varied cases, and is evaluated against written criteria, with failure modes noted but not specifically enough for someone else to recognise them. |
| 5 | Prompt is specified, holds on a case it was not designed for, is evaluated against written criteria, and its failure modes are documented specifically enough that someone else could recognise each one. |

Anchors 4 and 5 need written criteria and documented failures — day 30's work. A prompt scored before then caps at 3.

**Fastest fix:** run it on a case you did not design it for, then write the criteria that would have caught what broke.
