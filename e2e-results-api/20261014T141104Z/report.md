# Prompting Wizard end-to-end results

Run 20261014T141104Z · commit d5b05b6 · judge on

| scenario | claude-api |
|---|---|
| help | — |
| work-first | ✅ pass |
| lesson-no-mastery | ✅ pass |
| first-card | ✅ pass |
| external-action | ✅ pass |
| export-review | ✅ pass |
| history-consent | — |
| history-export-scan | — |

## Failures and skips


Package digests (dist/):

- `prompting-wizard-claude-plugin.zip` a13c69b299286aab3d4c5158adc35687e356a7e2296f324ddf4c80f2bfb01ef1
- `prompting-wizard-claude-skill.zip` 2fd9a20c0875b9f8aa05c6e173ea36a368999b900be89f90773ef443241fac5f
- `prompting-wizard-openai-plugin.zip` d6a0056395547298fb079d4c657c033e3a26d85ebf2735a60adf6efba2147b62
- `prompting-wizard-teacher-chatgpt.zip` 04b481d3e439365862c2fd6cd783cd1afbc51fa476cdb7762d3dbd3165da4dd9
- `prompting-wizard-teacher-claude.zip` 023175a86b7e3b440418d4cd6a30939b2d3919593e6cb810e2f359718a7bd7de

API rows simulate the app plugins through each provider API; they do not test native app loading, activation or uploads.
