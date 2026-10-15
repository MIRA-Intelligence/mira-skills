# Provenance

Vendored from https://github.com/nyblnet/bento (MIT, (c) 2026 The Bento authors).

- `SKILL.md` is adapted from `plugins/bento-slides/skills/bento-slides/SKILL.md`
  (upstream commit `1cc5dba2e6eb1d813bc52b657b142fd2dbb5599d`). Changed to use the
  bundled app copy instead of downloading it, and to validate with `scripts/build_deck.py`.
- `assets/Bento_Slides.bento.html` is the signed release fetched from
  https://bento.page/releases/slides/Bento_Slides.bento.html on 2026-10-15
  (sha256 `fdb1afc21a5defea75a1bb5390e5f34eeb2c35658c6bed9c62cb2ef3f997d64c`).
  Bundled third-party components keep their own licenses (Reveal.js, Moveable, Selecto: MIT; typefaces: OFL).
- `references/agents.md` is https://bento.page/agents.md fetched the same day.
- `scripts/build_deck.py` is MIRA's own helper.

To refresh, re-download the two files above and update the hash here.
