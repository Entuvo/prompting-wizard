# Wizard commands

This guide handles `pw` requests and equivalent natural-language controls. Resolve course paths relative to this guide's parent skill directory. Read the course's `AGENTS.md`. Only `start`, `continue`, or a request for a guided lesson enters `SKILL.md`'s Every session flow. Other commands must not start an assessment, update the course, change scores, or advance a day.

## Routing

Remove only the leading invocation (`/pw`, `/prompting-wizard:pw`, `$pw`, or `$prompting-wizard:pw`) if present. Host-expanded arguments may arrive separately. Use this vocabulary consistently, but display the invocation supported by the current host: standalone Claude `/pw`, Claude plugin `/prompting-wizard:pw`, standalone Codex `$pw`, Codex plugin `$prompting-wizard:pw`. Do not promise arbitrary slash-command registration in Codex.

| Arguments | Action |
| --- | --- |
| empty or `help` | Show this menu in plain language, suggest `start` for new learners or `continue` for returning learners. No state inspection or mutation required. |
| `start` | Read `SKILL.md`; follow its new/returning learner and recovery rules. Existing progress is never reset. |
| `continue` | Read `SKILL.md` and resume the existing course. Missing progress follows its recovery rules. |
| `progress` | Show current day, recorded lever scores, and available next lesson. Use shared progress when available; otherwise working/attached `PROGRESS.md`. Do not assess, import, reconcile, repair, or advance state just to show progress. Explain missing or invalid state. |
| `feedback on` | Set the learner default to `after-result` using `configure`. Existing workspace overrides remain in effect; inspect `status --workspace ABSOLUTE_WORKSPACE` and report the current workspace's effective setting. Only when `workspace_mode` is an explicit non-default mode that differs, ask whether to change that existing override. A null mode, exclusion or pause means not collected, not a conflicting override. Never use workspace-level `configure` to fix absent opt-in: it enables collection. Never enable a workspace implicitly. |
| `feedback off` | Same procedure, using `lesson-only`. Confirm: feedback is saved for lessons; collection continues in enabled workspaces unless paused. |
| `pause` | Invoke `pause`. Confirm collection stopped; preserve feedback mode and existing examples. |
| `resume` | Invoke `resume`. Restore collection only for already-enabled workspaces; use `status --workspace ABSOLUTE_WORKSPACE` to report exclusions and effective mode. |
| `examples` | Use `list` to show a bounded page of pending/reviewed records, host, date, and a short paraphrase. Offer another page when present. Keep exact IDs privately for selection. |
| `forget <example>` | Resolve the learner's selection against `list`. Delete that exact record using its ID and kind. If ambiguous or absent, ask which example; never broaden to workspace/all. Distinguish raw observations, findings, and reviewed lessons and describe actual deletion scope. |
| `model` | With trusted integration context, call `guidance --root ROOT --token TOKEN`, then add applicable `--task-tag` values from the task scopes in `references/coaching.md`. Report this as the last model reported by the host for the session, not proof of the model that executed any completed result. Use only returned applicable candidates; cite their source, checked date and stale status. Without a token, missing identity, or matching task scope, teach labeled core principles. If the host may have switched models since that report, use core principles until fresh metadata is available. Do not infer identity from self-description, invent an observation ID, or change the host model. |

For conversational arguments (for example `help me write clearer instructions`), identify the learning goal and coach using the relevant course material. Ask one focused question when intent is ambiguous. Do not count a quick answer as a completed lesson. An unknown short command, invalid control value, or typo (such as `feedback sometimes`) gets available choices, with no mutation. A command never authorizes arbitrary shell execution. Use structured arguments and safe quoting for the existing runtime; do not interpolate the user's trailing text into a shell command.

## Local integration and state

For any command beyond help, when trusted SessionStart context supplies a runtime, data root and session token, read `references/coaching.md` and enter tutor mode before handling the request. Retain suppression during follow-up selection, clarification or learning; exit on completion, cancellation or error. Exiting tutor mode only ends conversation suppression; it does not resume a paused profile or enable a workspace. Never say capture is active again based on `session-exit` success. If reporting capture status, read `status --workspace ABSOLUTE_WORKSPACE` and use its paused/excluded/effective-mode fields. Without this context, do not guess identifiers or profile paths. Course/help/model guidance remain available; controls and saved examples explain that local coaching setup is needed and point to the repository's `COACHING.md`. Do not install hooks automatically.

For shared progress, `status` reports whether imported progress exists. If present, `progress-read` returns the authoritative text without creating an export or replacing the working copy. Otherwise inspect working/attached `PROGRESS.md`. Never overwrite or import conflicting history during a progress request. For guided learning, the full coaching procedure still governs reconciliation and learner-confirmed commits.

Show success only after the relevant runtime command succeeds. On denied access or failure, report what remains unchanged or unverified. Commands must not become learning examples: the runtime excludes explicit leading pw invocations, and tutor mode suppresses subsequent command/lesson conversation. A command that interrupts unfinished work discards that incomplete capture pair to avoid pairing work with a control response. Natural-language controls require the tutor-mode procedure; do not claim text recognition at the hook layer.
