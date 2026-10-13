# Diagnose runtime behavior and measure performance

Use for live/captured runtime diagnosis or an explicit performance goal. Routine delivery needs no benchmark loop. For workflow or prompt comparisons use [evaluations](evaluations.md). Reuse existing tools and [verification](verification.md) for trusted commands, current receipts, private evidence and owned cleanup. Diagnosis requests remain diagnosis-only unless implementation is already authorized.

## Diagnose from live or captured evidence

For a live symptom, identify the affected process, workload and state. Capture the matching signal: CPU samples for spinning work, allocation/retainer evidence for memory growth, or a browser trace for interaction delay. Record capture command/tool version, source/build identity, environment, timing and workload. Use scoped instrumentation within existing permissions; invasive live probes need appropriate authority and recovery. A request to diagnose does not automatically authorize hot-patching a production process.

For an existing capture, preserve the original and identify format, completeness, time range, sampling settings and available source symbols. Parse with an existing appropriate tool into a queryable form. A small script or SQLite table can reduce a large trace without reading its entire raw payload into conversation. Do not rerun a supplied capture as though it were the same dataset.

Reduce evidence to the dominant frame/call path, blocked thread/wait reason, allocation growth, or object-to-root retainer chain. Retain the query and compact result. Attribute the finding to the capture's matching file, symbol and line; unresolved or mismatched symbols limit diagnosis. Distinguish elapsed, CPU, allocation and retained-memory measurements rather than equating them.

Test the proposed mechanism with a controlled repeat, safe targeted instrumentation or comparable paired capture when available. A before/after association alone may have confounders; name what the intervention established. Without confirmation, report the strongest supported hypothesis and alternatives. Never label a missing mapping, wrong workload or unavailable signal as confirmed cause. Return `artifact/provenance / reduced observation / source attribution / mechanism evidence / confidence and limits / next action`. Then route an authorized fix to [engineering](engineering.md) or the measurement procedure below.

## Freeze a useful measurement before optimizing

1. Reproduce the user's complaint on a representative workload. Inspect the actual path with [investigation](investigation.md). Record input size, history/state, concurrency, warm/cold behavior and relevant environment. If reproduction fails, repair the scenario before optimizing.
2. Select the metric, direction, correctness gates and bounded stopping condition. For sustained optimization, record target, attempt/time budget and enough repetitions to avoid a lucky early stop. Use supplied limits; state reasonable assumptions when limits are unspecified. No unlimited loop or implied future scheduling.
3. Reuse or build one rerunnable measurement command. Prove sensitivity with contrasting realistic workloads or a known controlled slowdown. If it cannot distinguish the effect, fix the measurement before accepting any win. Record command, inputs, tool/environment versions and harness hash.
4. Before baseline measurement, preserve workload, harness identity, metric, repetitions, correctness gates and keep/revert noise rule in a distinct write-once definition for this comparison. Show its contents and hash in captured command output before running the measurement; a mutable plan later containing results cannot prove prior criteria. Keep results separate. Run repeated baseline samples, report sample count, summary statistic and spread, and obtain a green correctness baseline. Preserve original test contents/hash (or an unchanged source revision) before expanding coverage; identify any added tests and say the expanded suite passed before optimization, not before any editing. Preserve raw measurements; a single run or mean without spread can hide noise and outliers.

When both sides of a baseline equality check call the same unchanged implementation, report that check as harness smoke, not independent value-equivalence evidence. Distinguish passing existing tests and meaningful type/input-preservation assertions from post-change candidate-versus-original equality; do not describe the latter as proved before the change.

Keep these fields in the existing record: `hypothesis / source and workload identity / frozen harness / samples and noise rule / before / after / correctness evidence / keep-or-revert / limit`. Hashes and records document evidence; they do not authorize commands or validate themselves. The existing evidence adapter remains the receipt-freshness owner.

## Change one mechanism and decide

Ground each hypothesis in the trace and source. Repeated identical computation may justify caching with an explicit invalidation rule; per-call overhead may justify batching; interactive blocking may justify scheduling. A hot path does not prove work is safe to delete. Confirm semantics before elimination, and measure the user-visible metric when moving work elsewhere.

Apply one scoped change, measure comparable before/after samples with the frozen command, and run unchanged correctness gates. Control warmup, competing load and ordering where they affect comparison. Keep a performance change only when improvement exceeds the declared noise threshold and correctness holds. Revert that attempt's owned changes otherwise, preserving unrelated work and failed evidence. A useful simplification with unchanged performance may be retained for its separate documented benefit; do not count it as a speedup.

Read the decision history before the next attempt. Never stack unmeasured changes or quietly alter the harness/baseline to pass. If a measurement defect requires a harness change, end the current comparison, record why, establish a new baseline, and remeasure affected candidates. Stop at the agreed predicate/budget, exhaustion of useful evidence-backed hypotheses, or an unresolved blocker. Report accepted/reverted attempts and next hypothesis rather than invent an optimum or numerical ceiling. Architecture changes still use the architecture gate; native delegation is optional and limited by actual authority/capability.

## Preserve UI behavior and explicit visual parity

For frontend performance, reuse the relevant Impeccable optimization and visual verification instructions through [Codex adaptation](codex.md); do not create a competing UI pipeline. Preserve accepted interactions, accessibility and appearance while measuring improvement.

For explicitly requested pixel-equivalent migration, capture approved baseline states before moving components, with fixed viewport, data, fonts and rendering environment. Freeze screenshot harness, images and declared comparison policy. When exact parity is required, a nonzero unexplained image diff fails; visual inspection alone is insufficient. Do not edit baselines, comparison tolerances or component behavior to conceal a failure. A genuine requirement/baseline change needs an explicit decision and new baseline lineage. Verify shared primitives before dependent components, retain each component's diff, and disclose unavailable image tooling. General screenshot review is not a pixel-parity claim.
