# Evaluate workflow behavior without leaking the answer

Use when changing skill/prompt behavior or deciding whether a workflow variant improves delivery. A routine product edit needs no evaluation. Static routing checks remain useful but cannot establish behavioral compliance or delivery gains. Use the host's actual capabilities through [Codex adaptation](codex.md), existing [verification](verification.md) receipts and exact [Opus review](review.md); no new evaluator engine is required.

## Define and isolate the comparison

Record the specific behavioral question and a small judge-only rubric before execution. Criteria must describe observable outcomes, not desired phrases or a candidate's self-assessment. Fix relevant scenario inputs, model/settings where controllable, limits and success/failure conditions. Keep rubric, expected answers, variant mapping, baseline verdicts and evaluator notes outside candidate-accessible context and files. Approved private records may be outside the engineering root.

Prepare fresh, isolated project-shaped workspaces with the context a real task needs. Use neutral names without evaluation, judge, scoring or candidate labels. Install the intended instruction variant. Sanitize task wrappers, slugs, prompts and supplied metadata that reveal the comparison. Ordinary project tests and filenames can remain when they belong to the real task; remove evaluation scaffolding rather than distorting the project to hide ordinary engineering vocabulary. Keep equivalent starting source/data for variants and record any unavoidable differences.

Use the same organic user request for compared variants. State the user goal and constraints, not that skills are being tested, which rule should fire, or that competitors exist. Do not ask for hidden reasoning or a list of rules applied. Ask for normal deliverables and concise design notes only where the real task would warrant them. A fresh native worker with no inherited conversation is preferred when authorized and available. An instruction not to read a judge file is weaker than withholding access: disclose shared-host visibility or other isolation limits.

## Run and judge actual work

Run candidates under the recorded limits with disjoint ownership. Capture resulting files, commands, test output, timestamps and available host execution traces from the assigned workspace. Inspect artifacts directly. A promise to run tests is not execution; a route declaration is not the requested task; a model's summary does not establish what it read or changed. Do not inspect unrelated chats or scan global transcript stores to recover missing traces. Mark unavailable evidence unavailable.

Give an independent judge the frozen rubric and all relevant outputs in one comparison pass, labeled neutrally with variant/model identities and lead preferences withheld. Prefer a different model family where supported. For Keelson's mandatory review, use exactly Opus 5.5 through the existing adapter; do not silently substitute a model. If the required reviewer is unavailable, preserve artifacts and report the gate open. Text-only judging cannot inspect screenshot pixels; provide a capable visual reviewer when the criterion requires them, or report that criterion unverified.

Ask for criterion-level evidence, concrete failures, coverage limits and a recommendation. Inspect every output and relevant trace yourself, then reconcile the verdict against artifacts. Investigate disagreement as possible ambiguous criteria, missing context or judge error; do not quietly rewrite the rubric after seeing results. If criteria must change, record the change and rerun the affected comparison. Retain rejected outputs and failed attempts alongside winners.

## Report what the exercise establishes

Keep `question / variant-input hashes / organic request / hidden criteria location / environment and limits / candidate outputs and execution evidence / neutral judge verdict / lead disposition / contamination / recommendation` in existing private records. Sanitize secrets before external model review. These records grant no execution, deployment or wider-data authority.

Report contamination explicitly: inherited planning context, leaked expected answers, model labels, shared accessible judge material, unequal environments or missing traces. Contaminated runs can diagnose workflow weaknesses but do not establish a clean blinded comparison. When historical transcripts are unavailable, say which observable artifacts still support narrower conclusions.

Separate a scenario routing replay, an executed task demonstration and a repeated controlled comparison. One successful example supports that example; it does not establish reliability, statistical improvement, cost savings or general superiority. Comparative performance claims need comparable repeated scenarios, failures/dropouts, recorded resource boundaries and measured uncertainty. Missing cost or usage is unknown, never zero. Promote only within demonstrated scope after required independent review, recording remaining limitations and targeted follow-up scenarios.
