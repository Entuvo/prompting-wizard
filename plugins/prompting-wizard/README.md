# Prompting Wizard

Learn prompting through tasks you already do. One plugin for Claude (app, Cowork, Claude Code) and for ChatGPT and Codex:

- **Everyday learning:** finish your work first, then choose a short practice, an example or a lesson. No interview or programming prerequisite.
- **Learning Card:** keep the evidence you accept in a portable `LEARNING.md` you carry between chats and apps.
- **Optional 30-lesson course:** one assessment, then one prompting lever per lesson, using your own tasks.
- **Learn from your past chats:** see where your prompts cost you turns, from your own history with the same provider.

## Start

Install the plugin through your app's plugin settings, start a new chat, and say:

> Use Prompting Wizard to teach me through my work; no interview. Keep tips occasional. My task is: [your task].

For structured lessons, say "Start the Prompting Wizard course." To review your past work, use `pw history` in Claude Code or Codex, or upload your app's own data export in ChatGPT or Claude and ask the coach to review it.

## Choose how to learn

- **Practice:** revise one part of your prompt and separately predict its effect. Choose **Retry** to try your revision, then explain what changed. Same-chat comparisons are exploratory.
- **Example:** see a short demonstration.
- **Lesson:** learn the principle using your task.
- **Later:** dismiss the opportunity and continue working.

These are text replies, not app buttons. Ask for more, less, on-request teaching or pause coaching in the current chat. External actions are never repeated simply to compare prompts.

## What works where

| | ChatGPT, Claude app | Claude Code, Codex |
|---|---|---|
| Everyday learning and Learning Cards | yes | yes |
| 30-lesson course | yes, with an attached `PROGRESS.md` | yes, with local progress |
| Past-work review | upload that app's own export | `pw history`, with stored results |

Each provider's history is reviewed only by that provider's hosts. In the apps, an upload reaches that app's provider even if the coach declines it, so upload only that app's own export.

## Data and permissions

The plugin reads the current conversation, its bundled teaching references, and anything you explicitly supply: a Learning Card, `PROGRESS.md` or an export. These can contain personal information and are processed by your AI provider under your account settings and its policies. Entuvo operates no Wizard service and receives nothing. The course's local scripts and `pw history` run only in Claude Code or Codex, on your machine. Optional automatic coaching in those tools is a separate, opt-in setup. See [privacy](https://entuvo.github.io/prompting-wizard/privacy/) and [terms](https://entuvo.github.io/prompting-wizard/terms/).

## Status and support

Version 1.5.2. Everyday coaching has passed the device walkthrough in Claude on the web. Human learning effectiveness has not been validated. Report problems through [GitHub Issues](https://github.com/Entuvo/prompting-wizard/issues) using synthetic examples, never personal cards or transcripts. Maintained by Entuvo; MIT License.
