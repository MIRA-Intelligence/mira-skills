---
name: mira-hub
description: Find and install skills from MIRA Hub, MIRA's own skill marketplace (research, medical, bioinformatics, document and coding skills). Use when the user asks to install a skill "from MIRA Hub", pastes a hub.mira-intelligence.com (or mira-intelligence.github.io/mira-hub) link or a hub install prompt, or asks whether a skill exists for a research task. 从 MIRA Hub 搜索、安装技能。
homepage: https://hub.mira-intelligence.com/
metadata:
  aliases: ["MIRA Hub", "mirahub", "skill marketplace", "install skill", "安装技能", "技能市场"]
---

# MIRA Hub

MIRA Hub (<https://hub.mira-intelligence.com/>) publishes curated,
checksummed skills. Two tools cover it — don't download or unpack hub archives
with `exec` or `web_fetch`.

## Install

Call `hub_install` once with the slug or the hub page URL:

- "Install the "scanpy" skill from MIRA Hub" → `hub_install(slug="scanpy")`
- `https://hub.mira-intelligence.com/skills/scanpy/` → `hub_install(slug="<that URL>")`
  (links from the older `mira-intelligence.github.io/mira-hub/` site work the same way)

It downloads the zip, verifies its sha256 and installs it as a custom plugin
for all projects (Settings → Skills & Plugins). Reinstalling updates the skill.
Then tell the user it's installed and usable from their next message. Don't
read the new skill, check its dependencies, or try it out unless asked — the
skill handles its own setup when it's first used.

If the tool returns an error, report it as is. "already built into MIRA" means
nothing needs installing.

## Find

`hub_search(query="...")` returns the best matches (slug, version, English and
Chinese abstract, tags). Query in English or Chinese, e.g. `single-cell`,
`DICOM`, `单细胞`. Show the user the few relevant matches and install the one
they pick.
