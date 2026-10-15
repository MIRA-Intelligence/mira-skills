# Provenance

MIRA Slides is MIRA's build of Bento Slides (https://github.com/nyblnet/bento,
MIT, (c) 2026 The Bento authors). The build comes from the fork
https://github.com/MIRA-Intelligence/mira-slides; its `MIRA.md` lists every
change.

- `assets/Mira_Slides.html` is built from fork tag `mira-v1.2.7-1`
  (commit `5be67a29822f510d7fb96ee5c258923730bd25d3`). That commit is upstream
  `Release 1.2.7` (`29ca0655`) plus the MIRA branding commit. The build command
  is `cd slides && npm ci && npm run build:single`, and the output's sha256 is
  `981aa7211d7cdf69efa66667f60516d453b9bac9268d16d36e6a096f4307e63d`.
  The fork changes only visible names (title, splash, app name) and disables
  the self-update check. Bundled third-party components keep their own
  licenses: Reveal.js, Moveable and Selecto are MIT; the typefaces are OFL.
- The document format is still Bento's: `"format": "bento/slides"`,
  `application/bento+json`, `#bento-doc`, `window.bento`. This is intentional,
  so that existing decks, upstream docs and tools keep working.
- `SKILL.md` is adapted from upstream `plugins/bento-slides/skills/bento-slides/SKILL.md`
  (commit `1cc5dba2e6eb1d813bc52b657b142fd2dbb5599d`). It was changed to use the
  bundled app and to validate decks with `scripts/build_deck.py`.
- `references/agents.md` is https://bento.page/agents.md (guide 1.2.7),
  fetched 2026-10-15, with a short MIRA note added at the top.
- `scripts/build_deck.py` is MIRA's own helper.

To refresh, rebuild from a newer fork tag (see the fork's `MIRA.md`), copy
`slides/dist-single/Mira_Slides.html` here, and update the tag, commit and hash
above.
