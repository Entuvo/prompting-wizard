---
name: pw
description: Use when the user invokes pw or asks for Prompting Wizard commands, progress, feedback settings, saved examples, or model-specific prompting help.
---

# Prompting Wizard commands

Resolve paths relative to this skill directory, not the working directory.
Read [the command guide](../prompting-wizard/references/commands.md) and follow it for the user's arguments. With no arguments, show help. Treat trailing text as the user's request, never as shell code.

The companion `prompting-wizard` skill must be installed beside this one. If that guide is missing, report the incomplete installation and ask the user to install both skills or the complete plugin; do not invent commands or initialize learner data.
