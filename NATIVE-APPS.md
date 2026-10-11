# Learn through everyday chats — pilot

Finish your normal work, then practise one useful prompting skill. No interview required. The same teaching flow is designed for ChatGPT and Claude. This is an early pilot: native web, desktop, iOS and Android setup has not yet been exercised end to end. Installation in Claude Code/Codex does not install account instructions in either consumer app.

## Start with lightweight coaching

1. Open the [one-time instructions](prompting-wizard/references/native-instructions.txt). Copy the entire block.
2. **ChatGPT:** put it in your account's custom instructions/personalization field. **Claude:** use Settings → Instructions for Claude. Preserve any existing instructions you want to keep. Labels and available controls can vary by app version and account.
3. Start a new chat and do your normal work. Ask “What coaching instructions can you see?” to check that they loaded. If they did not, paste the block in that chat; do not assume installation worked.

The block defaults to occasional tips. Change “Occasionally” to “Frequently” for more opportunities, or add “Only offer teaching when I ask” for on-request coaching. Saying “more”, “less” or “pause coaching” inside a chat changes that chat; update account instructions for later chats. These are qualitative preferences, not guaranteed turn counts.

These settings are documented by [OpenAI](https://learn.chatgpt.com/docs/personalize) and [Anthropic](https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features). We checked documentation on 11 October 2026; that is not a native compatibility test.

## Add lessons and carry learning between chats

Use the **native guide** and **empty Learning Card** produced with the release artifacts. From a source checkout, a developer can produce them with `python3 tools/package_release.py`: `dist/prompting-wizard-native-guide.md` and `dist/prompting-wizard-learning-card.md`. Until those assets are published, the [teaching policy](prompting-wizard/references/learning-policy.md), [card format/template](prompting-wizard/references/learning-card.md), [skill map](prompting-wizard/references/learning-catalog.json) and [rubrics](prompting-wizard/rubrics.md) are the source materials. Ordinary learners do not need Python.

1. Attach the guide and empty card to a chat, or add them as project sources if your account offers that feature. Ask: “Start everyday learning. Replace the template's synthetic profile ID with a new UUID; no interview.” Keep the resulting card as `LEARNING.md`.
2. Work normally. After meaningful practice, the coach proposes a short record explaining the skill, help received and what you demonstrated. Accept it only if accurate. Reading an example is not independent performance.
3. Ask for the **complete updated card**, save it over your retained copy, and bring that file to the next chat—even when switching providers. Check that existing events remain and that the new record matches what you accepted.
4. If using a project, deliberately replace its old card upload. A newly generated card does not overwrite old uploads, other projects or other apps. Outside that project, attach/paste the current card again.

No current card means no reliable learning history. The coach can still help from current context. Account memory is not a complete ledger, and instructions alone do not load the full curriculum. If two card copies disagree, keep both and ask for reconciliation; never choose by highest revision. Failed validation leaves both originals intact. Use retractions for corrections and removal; old uploads, chat histories and provider memories require separate deletion.

## A normal conversation

**You:** Help me prepare a parent meeting.

**Coach:** [Completes the useful preparation, or asks a task clarification if needed. Only after the work is done:] “Naming the thing you wanted could make your next request clearer. Practice / Example / Lesson / Later?”

**You:** Practice.

**Coach:** “Change just the part that names what should be produced. Then, separately, predict what difference you expect.”

**You:** Prompt: “Write talking points for a parent meeting about reading progress.” Prediction: “I'll get lines I can say, rather than a general agenda.”

**Coach:** “We can retry that prompt here. This chat already contains the first answer, so the comparison is exploratory. Retry, or stop here?”

**You:** Retry.

**Coach:** [Runs only the revised prompt, without the prediction.] “What changed, if anything? Did it help your meeting preparation?”

**You:** It gave me more usable lines.

**Coach:** “You chose a concrete output after a hint. Proposed record: choosing an output, practised with help—not independent yet. Add that to your card?”

**You:** Yes.

**Coach:** [Returns the complete updated card.] “Retain this file and supply it next time. Your previous upload hasn't changed.”

**Next chat in the other app, with that card:** “Your card shows practice with help. When this skill is relevant, I'll offer a different task you can try without a hint.”

Example and Lesson offer short explanations, with an optional route back to practice. Later dismisses the opportunity. A strong prompt may need no tip; a retry may show no improvement. External actions such as sending messages, purchases or edits are never repeated merely to compare prompts. Choices are text replies, not added native buttons; type them, or use your app's ordinary voice input where available.

## What is tracked

Only accepted learning evidence: the skill, task category, learner action, help received and optional reflection. Stages describe evidence: introduced, practised with help/unknown assistance, demonstrated independently, transferred to another context, retained later. Unseen skills remain unknown. A seven-day revisit is a pilot scheduling rule, not a validated claim about memory. The next suggestion should name its evidence and why it fits your task.

Mini-lessons never advance the separate 30-lesson course. In installed coding-agent skills, use `pw learn` for everyday teaching, `pw learning` for card progress, and `pw progress` for course progress. These are not registered native ChatGPT/Claude app commands.

## Limits and automatic continuity

This pilot does not watch other chats, run background capture, or sync accounts. Local coding-host collection still uses its existing explicit opt-in and controls; these account instructions do not enable it. Exported cards do not synchronize with the local course database yet.

A shared authenticated connector is the next candidate for reducing manual transfer. [Continuity investigation](CONTINUITY.md) separates documented capabilities from the untested cross-app round-trip. No Wizard service, new account or integration is installed by this pilot. Human learning outcomes remain unvalidated.
