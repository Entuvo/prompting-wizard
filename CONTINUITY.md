# Automatic continuity investigation

Checked 12 October 2026. **A shared remote connector is plausible; automatic cross-app learning continuity is not yet demonstrated.** The [native plugin pilot](NATIVE-PLUGINS.md) bundles teaching materials and uses manual Learning Card transfer. No service or account connection has been created.

## What current documentation establishes

| Route | Documented capability | Remaining limit |
|---|---|---|
| ChatGPT plugin with a remote MCP server | Plugins can supply skills/tools in Chat and Work across web, desktop and mobile; desktop-only plugins are an exception. Installed capabilities become available in new chats. | Availability does not guarantee a profile read at every chat start or an accepted-event write after every lesson. Specific account/distribution eligibility needs testing. |
| Claude remote custom connector | Account-brokered remote tools can read/write authorized services across clients, including mobile. Free accounts have a one-custom-connector limit; managed plans need organization approval. | Connector access and tool use depend on chat/account controls. Documented “Always available” tool access is per conversation; it is not proof of an account-wide observer. |
| Account instructions + project sources | Carry teaching preferences and explicitly supplied material within supported context boundaries. | No authoritative cross-provider ledger or reliable automatic file replacement. |
| Browser extension | A possible separate browser product. | Would require independent implementation/testing and would not cover native mobile/desktop chats. Not selected for this pilot. |

Sources: [ChatGPT plugins](https://learn.chatgpt.com/docs/plugins), [building an MCP server](https://developers.openai.com/plugins/build/mcp-server), [Claude remote connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp), [Claude tool access](https://support.claude.com/en/articles/13730515-manage-claude-s-tool-access). These are documented platform capabilities, not tests of Prompting Wizard on those surfaces.

Claude also documents [account-installed plugins](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) and [skills/plugins across Cowork surfaces](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile). Bundling the guide reduces setup but does not synchronize learning evidence or establish automatic skill activation.

OpenAI currently [does not support adding an MCP server to an existing skills-only plugin](https://developers.openai.com/plugins/deploy/submission). A future connected version may require a separate plugin identity and migration; recheck this before choosing the service rollout.

## Recommended next experiment

Use one minimal authenticated service with the existing card semantics and provider adapters. Treat the following as proposed contracts, not implemented tools:

- `read_learning`: return the authenticated learner's card and revision.
- `append_learning`: append explicitly accepted events with an expected revision and idempotency key; return committed event IDs and revision only after success.
- `retract_learning`, `export_learning`, `delete_learning`: explicit correction/export/deletion without expanding scope to other provider memories or old exports.

Bind identity to authenticated server claims, never to a model-supplied `profile_id`. Keep read/write scopes distinct. The MCP authorization specification requires audience-bound token validation; expired/invalid tokens must fail instead of falling back to another account. Current documentation was resolved through Context7 against [MCP 2026-07-28 authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization). No SDK version or compatibility commitment has been selected; verify each client's actual supported protocol during the experiment.

Use two synthetic accounts and an empty card. In each selected app/surface/plan:

1. Connect once; begin a fresh chat; observe whether the current card is read without asking the user to re-enable it.
2. Complete a teaching interaction; accept one event; verify the service committed it before the tutor says saved.
3. Open a fresh chat in the other provider; read the same profile and select the next opportunity from that event.
4. Repeat a write, submit a stale revision, revoke access and simulate a failed write. Check idempotency, conflict handling, no false save, and no leakage into the second account.
5. Repeat on desktop, web, iOS and Android. Record every unavoidable activation/approval step. Separate a tool that is available from one that is invoked reliably.

A working backend or a successful same-chat tool call is insufficient. If this fails the desired “configure once” experience, retain manual cards or propose a browser-only scope explicitly. Do not describe native chat monitoring as built.

## Gate before service implementation

Agree account linking, what accepted evidence goes to each provider, retention/deletion, hosting budget, and acceptable activation friction. Then run the authenticated round-trip using disposable accounts and a chosen deployment. Current scope authorizes investigation, not a deployed service or changes to live account connections.

Native testing was left for the user's walkthrough. Outstanding: real account eligibility, OAuth round-trip, invocation reliability, cross-provider identity isolation, mobile behavior, failed-write UX and observed learning/transfer. The local reference validator and tool-disabled model scenarios do not answer those questions.
