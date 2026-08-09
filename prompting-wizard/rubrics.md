# Rubrics

One rubric per lever and per technique. Every lesson scores against a rubric here rather than restating criteria, so the same weakness gets the same name on day 3 and on day 27.

Scores are 1–5. Anchors are given for every point. Score the prompt as written, not the intent behind it.

## Noun

**Measures:** the artifact the prompt asks for.

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
| 4 | Exactly one operation named, and it matches the operation actually wanted. |
| 5 | Exactly one operation named, matching what is wanted, in the most precise verb available for it. |

**Fastest fix:** name the operation: summarise, rank, critique, refactor, enumerate.

## Adjective

**Measures:** quality constraints on the artifact.

| Score | Anchor |
|---|---|
| 1 | No quality named; any output passes. |
| 2 | A quality is named but so generically ("good", "high-quality") that it rules nothing out. |
| 3 | One real quality is named, but a second quality that matters as much is left unstated. |
| 4 | Every quality that matters is named, though some slack remains in how they're worded. |
| 5 | Every quality that matters is named, and none that do not — each word does rejection work. |

**Fastest fix:** list the two qualities that would make you reject the output, then state them.

## Adverb

**Measures:** manner and degree of the action.

| Score | Anchor |
|---|---|
| 1 | Manner unspecified; depth left to chance. |
| 2 | A manner word is used ("briefly", "carefully") but without a measure, so two readers would produce different depths. |
| 3 | Depth or manner is set for part of the task, but another part is left to guess. |
| 4 | Depth and manner set clearly enough that output length and thoroughness are mostly predictable. |
| 5 | Depth and manner set so output length and thoroughness are predictable in advance, not just in hindsight. |

**Fastest fix:** say how thoroughly, and in what manner.

## Pronoun

**Measures:** reference binding.

| Score | Anchor |
|---|---|
| 1 | Pronouns with no antecedent ("fix it", "do this"). |
| 2 | An antecedent exists somewhere in the prompt, but it's ambiguous which of two candidates it refers to. |
| 3 | Most references resolve, but one pronoun still requires the reader to guess. |
| 4 | Every reference resolves, though the resolution takes a re-read to confirm. |
| 5 | Every reference resolves inside the prompt or to a quoted block, on first read. |

**Fastest fix:** replace each it/this/that with the thing it means.

## Preposition

**Measures:** scope and relation.

| Score | Anchor |
|---|---|
| 1 | No scope; the task could touch anything. |
| 2 | One boundary is given (e.g. audience) but others (what's excluded, for whom) are missing. |
| 3 | Most of scope, audience and exclusion are set, but one relation is left implicit. |
| 4 | Boundaries, audience and exclusions are all set, though phrased loosely enough to invite a small stretch. |
| 5 | Boundaries, audience and exclusions all set precisely — in what, for whom, without what. |

**Fastest fix:** add: in what, for whom, without what.

## Conjunction

**Measures:** conditional logic.

| Score | Anchor |
|---|---|
| 1 | Branching cases collapsed into one instruction, so edge cases silently pick a branch. |
| 2 | One branch is acknowledged but its condition or its outcome is missing. |
| 3 | Branches and conditions are named, but the fallback (the otherwise) is missing. |
| 4 | Each branch stated with its condition and its fallback, though the wording leaves the order of checks ambiguous. |
| 5 | Each branch stated with its condition and its fallback, in an order that resolves without ambiguity. |

**Fastest fix:** write down the if/then/otherwise you are holding in your head.

## Determiner

**Measures:** definiteness and quantity binding.

| Score | Anchor |
|---|---|
| 1 | Bare nouns leave it unclear whether one, some, or all are meant. |
| 2 | A determiner is used on the main noun, but supporting nouns nearby are still bare. |
| 3 | Most nouns are bound, but one noun that changes scope significantly ("the" vs "any") is left bare. |
| 4 | Each noun is bound — the, a, each, every, any — with only a minor reading left open. |
| 5 | Each noun is bound — the, a, each, every, any — with no reading left open. |

**Fastest fix:** put the/a/each in front of every noun and see which changes the meaning.

## Numeral

**Measures:** budgets that make output checkable.

| Score | Anchor |
|---|---|
| 1 | No quantity anywhere; length and count unbounded. |
| 2 | One quantity is given (e.g. a word count) but other countable dimensions (item count, number of examples) are open. |
| 3 | Most countable dimensions are bounded, but the bound is vague enough to need judgement ("a few", "several"). |
| 4 | Every countable dimension is bounded with a number, though one bound is awkward to verify without counting carefully. |
| 5 | Every countable dimension bounded, and the bounds checkable without judgement. |

**Fastest fix:** add a count and a length you could verify with a ruler.

## Interjection

**Measures:** attention and priority markers.

| Score | Anchor |
|---|---|
| 1 | All instructions carry equal weight; the critical one is buried mid-paragraph. |
| 2 | A priority word is used ("important:") but attached to something that isn't actually the highest-stakes instruction. |
| 3 | The critical instruction is marked, but its position in the prompt still lets it get skimmed past. |
| 4 | The must-not-fail instruction is marked and positioned near the top, but competes with one other marked item. |
| 5 | The must-not-fail instruction is marked and positioned so it cannot be missed. |

**Fastest fix:** mark the one instruction you would be angry about being ignored.

## Particle

**Measures:** phrasal precision.

| Score | Anchor |
|---|---|
| 1 | Phrasal verbs used loosely, so the operation is ambiguous (look up / look over / look into). |
| 2 | A phrasal verb is used, and swapping its particle would plausibly change the intended task without the writer noticing. |
| 3 | The phrasal verb is close to right, but a stricter synonym would remove a small remaining ambiguity. |
| 4 | Every phrasal verb is chosen deliberately, with only cosmetic substitutions available. |
| 5 | Every phrasal verb chosen deliberately; no substitution preserves the meaning. |

**Fastest fix:** swap the particle and check whether the task changed. If it did, you needed the precise one.

## Role framing

**Measures:** whether the role changes the output.

| Score | Anchor |
|---|---|
| 1 | Role asserted with no bearing on output ("you are a world-class expert"). |
| 2 | The role is domain-relevant, but nothing in the prompt tells you what it includes, excludes, or assumes differently. |
| 3 | The role implies a standard or a body of knowledge, but the prompt doesn't say which parts to draw on. |
| 4 | Role changes what is included, excluded and assumed, though the mechanism is only implied, not stated. |
| 5 | Role changes what is included, excluded and assumed, and you can say how. |

**Fastest fix:** name the knowledge or standard the role brings; drop the flattery.

## Few-shot examples

**Measures:** what the examples teach.

| Score | Anchor |
|---|---|
| 1 | No examples, or examples that only show the easy case. |
| 2 | One example given, showing a typical case with nothing instructive about its edges. |
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
| 4 | An exact structure is given, checkable in most cases, with one edge (e.g. empty values) unaddressed. |
| 5 | An exact structure given, which output can be checked against mechanically. |

**Fastest fix:** write the shape you want, filled with dummy values.

## Task decomposition

**Measures:** whether the work is split correctly.

| Score | Anchor |
|---|---|
| 1 | One prompt carries several tasks that interfere. |
| 2 | The tasks are listed, but their inputs and outputs aren't separated, so they still interfere. |
| 3 | Tasks are split into steps, but one step's output isn't a clean input to the next. |
| 4 | Work split so each step has one output and a mostly clear input from the last. |
| 5 | Work split so each step has one output and a clear input from the last. |

**Fastest fix:** find the "and then" in your prompt and cut there.

## Reasoning scaffolds

**Measures:** whether reasoning is structured where needed.

| Score | Anchor |
|---|---|
| 1 | Reasoning demanded without structure, or suppressed where it was needed. |
| 2 | Reasoning is requested, but the intermediate steps expected aren't named. |
| 3 | Some intermediate steps are named, but one that the task actually depends on is missing. |
| 4 | The reasoning steps asked for match the ones the task requires, with minor slack in ordering. |
| 5 | The reasoning steps asked for match the ones the task requires. |

**Fastest fix:** name the intermediate you want to see before the answer.

## Negative constraints

**Measures:** what is ruled out.

| Score | Anchor |
|---|---|
| 1 | No exclusions; known failure modes not ruled out. |
| 2 | An exclusion is stated, but it's generic ("don't be verbose") rather than tied to an observed failure. |
| 3 | One real failure mode is excluded, but a second, equally likely one is not. |
| 4 | Exclusions are specific and mostly map to failures you've seen, with one still speculative. |
| 5 | Exclusions are specific, and each prevents a failure you have actually seen. |

**Fastest fix:** write down what it did wrong last time, and forbid exactly that.

## Context ordering

**Measures:** placement of instruction and material.

| Score | Anchor |
|---|---|
| 1 | Instruction buried after a wall of context, or context missing where needed. |
| 2 | Instruction and context are both present but interleaved in a way that obscures which material serves which step. |
| 3 | Instruction is findable, but constraints are scattered rather than grouped at the end. |
| 4 | Instruction and context are ordered sensibly, with constraints mostly grouped but one placed early. |
| 5 | Instruction and context ordered so the model reads what it needs when it needs it. |

**Fastest fix:** task first, material second, constraints last.

## System prompts

**Measures:** separation of standing rules from the turn.

| Score | Anchor |
|---|---|
| 1 | Durable rules repeated per turn, or turn-specific detail promoted into standing rules. |
| 2 | Some durable rules are separated out, but turn-specific detail still leaks into them. |
| 3 | Durable rules and turn request are mostly separated, but one standing rule is restated per turn out of habit. |
| 4 | Standing behaviour and per-turn request cleanly separated, with only a minor overlap. |
| 5 | Standing behaviour and per-turn request cleanly separated. |

**Fastest fix:** ask which lines you would want true on every turn — those are the system prompt.

## Agent and tool prompting

**Measures:** tool use and stopping conditions.

| Score | Anchor |
|---|---|
| 1 | Tool use implied but not specified; no stopping condition. |
| 2 | Tools are named, but when to use each one and what counts as done are both unstated. |
| 3 | Tools and rough sequencing are given, but the stopping condition is missing or vague. |
| 4 | Which tools, when, and what "done" means are all stated, though the done-condition could still be gamed. |
| 5 | Which tools, when, and what "done" means are all stated. |

**Fastest fix:** state the stop condition first, then the tools.

## Self-critique loops

**Measures:** whether output is checked.

| Score | Anchor |
|---|---|
| 1 | Single-pass output accepted with no check. |
| 2 | A check is mentioned ("review your answer") but with no criteria to check against. |
| 3 | A concrete check is named, but there's no stated action for when it fails. |
| 4 | A check the model can apply to its own output is given, with an action on failure that's only loosely defined. |
| 5 | A check the model can apply to its own output, with a stated action when it fails. |

**Fastest fix:** name the test the output must pass, and require it be run.

## Writing evals

**Measures:** whether quality is measurable.

| Score | Anchor |
|---|---|
| 1 | Quality judged by feel; no criteria written down. |
| 2 | Criteria exist but are subjective enough ("sounds right") that two scorers would diverge. |
| 3 | Criteria are written and mostly objective, but one is still a judgement call. |
| 4 | Criteria written before the output, specific enough that two people would agree most of the time. |
| 5 | Criteria written before the output, specific enough that two people would score the same. |

**Fastest fix:** write the three checks you would apply, then apply them.

## Token economy

**Measures:** whether every token earns its place.

| Score | Anchor |
|---|---|
| 1 | Context padded with material the task never uses. |
| 2 | Some unused material is trimmed, but redundant restatements of the same instruction remain. |
| 3 | Most padding is removed, but one section is included "just in case" rather than because the task needs it. |
| 4 | Every included token earns its place, verified for most of the context but not all. |
| 5 | Every included token earns its place; cuts made without losing accuracy. |

**Fastest fix:** delete a third of the context and see whether the output degrades.

## Failure diagnosis

**Measures:** whether the cause is identified.

| Score | Anchor |
|---|---|
| 1 | Failure blamed on the model; prompt unchanged. |
| 2 | A cause is guessed at, but it isn't named as one of the specific levers or techniques. |
| 3 | A lever or technique is named as the cause, but the fix doesn't actually target it. |
| 4 | The failing lever is identified by name and the fix mostly targets it, with some drift. |
| 5 | The failing lever is identified by name and the fix targets it. |

**Fastest fix:** ask which of the 11 levers was underspecified, and fix that one.

## Prompt library

**Measures:** reusability.

| Score | Anchor |
|---|---|
| 1 | Prompts rewritten from scratch each time. |
| 2 | A prompt is saved, but without marking which parts change between uses. |
| 3 | Saved prompts mark their variable slots, but don't record how they've failed before. |
| 4 | Reusable prompts stored with their slots and most known failure modes noted. |
| 5 | Reusable prompts stored with their slots and their known failure modes. |

**Fastest fix:** save the prompt with the task slot left as a blank.

## Capstone

**Measures:** production readiness.

| Score | Anchor |
|---|---|
| 1 | Prompt works once, on the example it was written against. |
| 2 | Prompt works on a couple of close variants, but hasn't been tried on anything unlike the original case. |
| 3 | Prompt is specified and works on varied cases, but has no written evaluation criteria. |
| 4 | Prompt is specified and evaluated against written criteria, with failure modes noted but not systematically. |
| 5 | Prompt is specified, evaluated against written criteria, and its failure modes documented. |

**Fastest fix:** run it on the case you did not design it for.
