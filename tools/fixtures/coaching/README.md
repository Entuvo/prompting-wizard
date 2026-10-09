# Synthetic host evidence

`valid/` contains sanitized native callbacks observed on 8 October 2026: Claude Code 2.1.293 and Codex CLI 0.159.3 interactive. Paths and session/turn IDs are replaced; prompts concern synthetic work. Numeric order follows each recorder, including new sessions. These are event-shape receipts, not claims that every interaction was a successful lesson.

`invalid/` contains constructed negative cases. Each must fail open without creating a profile, retaining content, or requesting a continuation. Adapter tests separately specify pairing, interruption, steering, missing results, replay, lease and model-identity outcomes.

Teaching expectations: exact-count generated formats can be valid; evidence-limited extraction needs a fallback rather than invented items; long-document ordering depends on model/task; a successful short prompt needs no additions; a weak practice exercise is not independent proficiency; tool failures can have non-prompt causes; an excerpted follow-up cannot establish missing context. Two facts alone do not prove at most two distinct risks.

Numeral scoring regression pair: (A) an evidence extraction task demands exactly five supported items when only two are supported and prohibits speculation: maximum 2, regardless of the exact wording of other counts. (B) the same task asks for a few supported items, with no conflicting demand: 3 because the bound is vague. (C) up to five, fewer when evidence is limited: 5. These are evaluator cases, not automated claims of teaching efficacy.

(D) A task needs a length limit, but the prompt gives no quantity: 1. (E) A task needs count and length; only count is given: 2. Anchor 3 requires all necessary quantities to be present, though at least one is vague.
