# Scoped evidence and measurements

For reusable project recipes, feature-to-proof maps and source/live upkeep, use [app verification](app-verification.md). Regression/refactor proof belongs to [engineering](engineering.md); measured experiments and behavioral skill evaluations have separate [experiment](experiments.md) and [evaluation](evaluations.md) protocols. These guides link existing receipts; they do not introduce another freshness authority.

Use the target's real checks. Before running one, declare its dependencies in a small JSON contract in the resolved private records directory:

```json
{
  "unit": "booking-flow",
  "check": "booking-behavior",
  "inputs": ["src/booking/**/*.py", "tests/test_booking.py", "requirements.lock"],
  "command": ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_booking.py"],
  "context": "Synthetic local fixture; Python version and service/image versions recorded in linked brief."
}
```

Replace every example with real project paths and a trusted command. Include implementation, callers, shared helpers, harness, fixtures/assets, configuration, lockfiles and acceptance criteria that affect this check. Glob patterns track additions/deletions; exact paths must exist. Patterns are relative to the engineering workspace. Do not glob the whole repository or evidence output. Hashing does not prove dependency completeness: review the declaration against imports and fixture/configuration use. When the impact is uncertain, expand the affected check scope. Keep separately scoped documentation and runtime checks.

```sh
python3 "$SKILL_DIR/scripts/evidence.py" run --project "$ENGINEERING_ROOT" \
  --contract "$PRIVATE_RECORDS/checks/booking.json" \
  --output "$PRIVATE_RECORDS/checks/booking-01" --reason "Initial booking verification"
python3 "$SKILL_DIR/scripts/evidence.py" status --project "$ENGINEERING_ROOT" \
  "$PRIVATE_RECORDS/checks/booking-01/receipt.json"
```

Each new attempt preserves the command, dependency contract, input hashes, start/end, elapsed seconds, exit status and output. Record why each repeat is needed with `--reason`. Failed, interrupted or changing-input attempts cannot qualify review. The wrapper executes a trusted argv directly, without a shell; inspect it before running. It captures output, which may be private: keep outputs in the approved private location, sanitize selected excerpts before external review. A timeout does not establish descendant/resource cleanup; the harness owns that lifecycle.

Validity means successful execution against unchanged declared source and contract. It does **not** establish unchanged external data, credentials, service configuration, runtime versions or installed dependencies drifting from a lockfile. Record relevant versions, fixture identity and environment in `context`/brief; inspect them before reuse and rerun affected checks on change. Reuse is a per-check decision, never a blanket release approval. Full backup/export integrity hashes remain complete and separate; narrowing verification dependencies must not weaken recovery validation. Preserve historical receipts rather than editing hashes to make them current.

## Verification resource lifecycle

Name resources per run. Acquire them inside the protected cleanup scope, including startup and connection failures. In cleanup, attempt every owned resource even if an earlier cleanup fails, and report both original and cleanup failures. Remove owned containers/networks, release ports, close clients, restore changed selections/configuration, and retain declared data/volumes. Never prune shared resources or infer ownership from a broad prefix alone. Check cleanup results. Prove successful, failed-start and repeated teardown with a synthetic marker retained in storage; main/shared resources must survive. A network left behind is a cleanup failure even if tests passed. Cancellation/host termination still needs explicit recovery on resume.

## Stable review and delivery measurements

Finish coupled edits and required verification before dispatching one readiness review. Include current verification receipts with `review.py --verification` (repeatable), select relevant evidence in the packet and set `--unit`. The adapter validates receipts before paid dispatch and again after the response, including dependencies absent from the text packet. Hold selected files, contracts and dependencies stable until completion. Work only on unrelated inputs meanwhile. If a material defect requires editing, mark that review superseded, retain diagnostic output, then verify and review the corrected candidate. No global source lock or automatic rereview loop is needed.

```sh
python3 "$SKILL_DIR/scripts/evidence.py" summary \
  "$PRIVATE_RECORDS/checks/booking-01/receipt.json" \
  "$PRIVATE_RECORDS/reviews/booking-01/receipt.json"
```

Supply every attempt for the unit, including failed/stale reviews and checks, not only the final green receipts. Summary deduplicates receipt paths, groups execution time by stage, and reports known provider cost plus unknown-cost counts. Review receipts include unit, packet JSON byte count, provider usage/duration and reported cost when returned, including invalid assessments. Unknown is not zero. Preserve raw responses for attribution; no billing reconciliation is implied.

At completion, link summary from the current checkpoint and record delivered outcome, blocked reason (or none), checks rerun and why, and observed user/external waiting intervals. If waiting or lead usage was not measured, leave it unknown. Stage sums can overlap and are not end-to-end wall time. Before/after savings claims require the same scenario, environment and measurement boundaries; passing new tests alone proves no percentage improvement.
