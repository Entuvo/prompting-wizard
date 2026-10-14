# Prompting Wizard — Everyday plugins

The teaching pilot is packaged as **Prompting Wizard — Everyday** (`prompting-wizard-teacher`, version 0.2.1) for ChatGPT and Claude. It bundles the teaching skill, guide, rubrics and empty Learning Card. Learn through your work without an interview; choose Practice, Example, Lesson or Later after a useful teaching opportunity.

These are buildable pilot packages, not a published directory listing or a verified native-app installation. The user walkthrough still needs to establish installation, activation and manual card transfer on each surface. Existing `prompting-wizard` course packages remain separate.

Neither directory submission nor publication has occurred.

## Packages

Build from a source checkout:

```sh
python3 tools/package_release.py
```

| Output in `dist/` | Purpose |
| --- | --- |
| `prompting-wizard-teacher-chatgpt.zip` | Portable root `plugin.json`, OpenAI presentation metadata and the bundled `learn` skill |
| `prompting-wizard-teacher-claude.zip` | Claude `.claude-plugin/plugin.json` and the same bundled `learn` skill |
| `prompting-wizard-native-guide.md` | Fallback guide for manual attachment |
| `prompting-wizard-learning-card.md` | Empty card; the coach creates a fresh profile ID at first use |

Both ZIPs have their manifest and `skills/` directly at the archive root. Neither requires a local Python runtime, hooks, MCP server, API key or a Wizard account. The developer build uses Python; the learner uses the host app. ZIPs contain no learner history. Release downloads will only be available after a maintainer publishes these assets; this document does not imply publication.

## Claude pilot installation

On a supported paid account, open **Customize → Plugins** on the web or desktop and upload `prompting-wizard-teacher-claude.zip`. Alternatively, after this change is merged, add the `Entuvo/prompting-wizard` GitHub marketplace and choose **Prompting Wizard — Everyday**, not the separate course plugin. Use an approved marketplace or administrator-provided plugin when workspace policy requires it.

Start a new conversation. Select the bundled **learn** skill from the skills menu if needed, then say:

> Use Prompting Wizard to teach me through my work; no interview. Keep tips occasional. My task is: [your task].

Confirm that the coach can read the bundled guide. If it cannot, use the [manual setup](NATIVE-APPS.md); do not assume files uploaded successfully are available in the conversation. Account installation does not prove the skill activates in every new chat.

Anthropic documents account-installed plugins in web chat and desktop, and skills/plugins on all three Cowork surfaces. Claude's merged Chat/Cowork experience is rolling out, so mobile availability and menus depend on account, plan and app version. See [Claude plugins](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) and [web, desktop and mobile support](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile). These statements describe platform support, not successful Wizard testing.

## ChatGPT pilot installation and distribution

For development, use the repository's marketplace entry pointing to `plugins/prompting-wizard-teacher`. Follow [OpenAI's local plugin setup](https://developers.openai.com/plugins/build/plugins#build-your-own-curated-plugin-list) in the ChatGPT desktop app. Local/repository marketplace availability differs by surface; a local install alone does not distribute the plugin to web or mobile.

To make the pilot available through an account/workspace, a workspace administrator can use the documented **Personal → plugin menu → Publish** route where supported, then grant the intended roles access. This is workspace distribution, not public publication. Users must be signed into that workspace. Follow [workspace publishing](https://developers.openai.com/plugins/build/plugins#publish-a-local-plugin-to-your-workspace) and verify the plugin appears on each device.

For public distribution, the publisher uploads `prompting-wizard-teacher-chatgpt.zip` through the [OpenAI plugin submission portal](https://developers.openai.com/plugins/deploy/submission), resolves validation findings, completes the required identity/permissions checks and submits for review. Publish only after approval. No submission, workspace publication or approval has been performed by this build. New documentation URLs must be live before submission.

Once the plugin is available to the account, install it, start a new chat, select it with `@` if necessary, and use the same start request above. [OpenAI documents plugins in Chat and Work on web, desktop and mobile](https://learn.chatgpt.com/docs/plugins); desktop-only components are exceptions. This pilot ships none, but end-to-end compatibility remains untested.

## Keep teaching and continuity separate

The plugin supplies the guide, so successful loading removes the need to attach that guide each time. It does **not** supply your learning history. Attach the current `LEARNING.md` in each new chat that needs it. Without a card, learning can begin from the current task without claiming past progress.

After meaningful practice, the coach proposes a learning record. Accept only an accurate description. Ask for the complete updated card, save it yourself and carry it to the next chat or provider. Replace an old project upload deliberately. An exported artifact is not proof of a durable save or account sync. Keep the previous file if validation or preservation is uncertain. Reading an example or following a hint does not establish independent skill.

To learn from past chats, export your data from the app's settings (ChatGPT: Data controls → Export data; Claude: Settings → Privacy → Export data) and upload `conversations.json` or a few conversations. Then ask the coach to review them. It reads up to 30 recent conversations and says how much it covered. It reports your most common gaps, with up to three of your own cases, and proposes card records that you accept or reject. Nothing is stored beyond that chat. Uploading one provider's export into the other provider's chat sends your history to that provider.

Occasional is the default; frequent or on-request can be chosen. More/less/pause affects this chat. Accepted card preferences travel only when the card is supplied. Installation cannot promise automatic coaching in every ordinary chat. Existing account instructions and the plugin should yield one invitation, not two; coding-host local feedback retains its ownership and opt-in rules.

The package contains no background observer, hosted storage or automatic cross-provider synchronization. See [privacy](PRIVACY.md).

## Walkthrough before claiming device compatibility

Use disposable chats and synthetic material. Record provider, account plan, app version, surface and date. Run these checks separately on web, desktop, iOS and Android:

1. Install through the chosen supported route; start a fresh chat and verify the skill and bundled guide are available. Record whether explicit selection is needed.
2. With no card, request normal work and teaching. Check work comes first, no interview occurs and no past history is claimed. Try Later and on-request.
3. Choose Practice, provide your own edit and a separate prediction, and choose whether to retry. Check the prediction is excluded, same-chat comparison is labeled exploratory, and no external action is repeated.
4. Accept an accurate record. Inspect the complete returned card, retain it, and attach it to a fresh chat in the other provider. Check profile ID and prior events are preserved and the next opportunity uses that evidence.
5. Try a missing guide, malformed card and conflicting card copies. Expect an honest limitation with originals preserved, not a fabricated save or merge.
6. Start an ordinary new chat without mentioning Wizard. Record whether it activates. A pass after explicit selection does not establish automatic activation.

Local package tests and model simulations do not establish these native results or human learning effectiveness.

## Maintainers

`plugins/prompting-wizard-teacher/skills/learn/SKILL.md`, its plugin-folder `README.md` and the two manifests are canonical native files. The guide/card, license and logo in that tree are generated from existing sources:

```sh
python3 tools/build_teaching_plugins.py --sync
python3 tools/build_teaching_plugins.py --check
python3 tools/test_teaching_plugins.py
```

Edit the shared learning policy and card format in `prompting-wizard/references/`, then regenerate; do not hand-edit generated references. Never place learner cards in a plugin tree. Packaging uses an explicit allowlist; the mirror check rejects unexpected files and symlinks.

The native plugin has its own version, separate from the course. Keep both native manifests and their marketplace versions aligned. Current OpenAI submission guidance does not support adding an MCP server to an existing skills-only plugin. If shared storage is implemented later, plan a separate connected plugin or reassess the then-current migration rules; do not promise a seamless upgrade.

Documentation checked 12 October 2026. No hosted service or account changes are part of this pilot.
