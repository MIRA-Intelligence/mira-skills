---
name: bento-slides
description: Build self-contained HTML slide decks (.bento.html) for the "Slides (HTML)" deliverable, previewed inline instead of PDF/PPTX. Maps results to charts, tables and morph transitions. Offline, bundled app.
metadata:
  scenarios: ["HTML slide deck deliverable", "Inline-previewed research presentation", "Self-contained slides without PDF or PPTX", "Editing an existing .bento.html deck"]
---

# Authoring Bento decks (offline, bundled)

A Bento deck is one self-contained `.bento.html` file. The document is plain
JSON in a single block:

```html
<script type="application/bento+json" id="bento-doc"> { "format":"bento/slides", ... } </script>
```

Vendored from https://github.com/nyblnet/bento (MIT); see `SOURCE.md`. Everything
this skill needs ships next to this file, so **do not download anything**:

- `assets/Bento_Slides.bento.html` — the app with an empty document block
- `references/agents.md` — the full schema and recipes. **Read it before authoring.**
- `scripts/build_deck.py` — builds and validates decks

## Starting from nothing (the normal MIRA path)

1. Read `references/agents.md`; start from its "Minimal valid document".
   `size` and `theme` (including `theme.fontFamily`) are **required**.
2. Write the document JSON to a working file, e.g. `result/exports/_deck.json`.
   Omit `docId` and `collab` entirely.
3. Build the deck (path relative to this skill's directory):

   ```bash
   python <skill_dir>/scripts/build_deck.py build result/exports/_deck.json result/exports/slides.bento.html
   ```

   By default the deck is built with `"readonly": true`, so it boots straight
   into the slideshow. **Keep that default**: MIRA previews the file in a
   sandboxed iframe where the editor cannot start. Use `--editable` only if the
   user explicitly asks for an editable deck.

   The script validates the document (required fields, unique element ids,
   `asset:` references resolve, no external image URLs), injects it with every
   `<` escaped as `<`, and writes the file. Fix every `error:` and read
   each `warning:`; rerun until it exits 0.
4. Delete the working JSON, and publish **only** the `.bento.html`.

## Editing an existing deck

1. `python <skill_dir>/scripts/build_deck.py check deck.bento.html` first.
   If it warns about `collab` keys, the file is a live-session invitation:
   **tell the user before continuing** and offer a read-only copy.
2. Edit only the `#bento-doc` block, in place, escaping `<` as `<`.
   Never regenerate the whole HTML and never change an existing `docId`.

## Content for research results

Build from the project evidence (`task_plan.json`, experiment artifacts); never
invent numbers. A good scientific deck: title, motivation, data, methods,
2-4 results slides (chart/table/figure each), limitations, next steps.

Map material to features instead of bullet text:

- numbers to compare (metrics across models/folds) → a **chart** element
- comparison / ablation / spec grids → a **table** element
- consecutive slides about the same thing changing → **morph**: same element
  `id` on both slides + `transition:"morph"` on the later one
- a drill-down → a **state slide** (`stateOf` + element `link`)
- a headline metric → big text + `fx:{countUp:true}`
- figures from the project → embed as data URIs in `doc.assets`, reference as
  `"asset:<key>"`. The file must stay self-contained (no external URLs).

Style: one accent colour, at most 2 typefaces, 96px side margins (right-most
x ≤ 1184), speaker notes on every slide.

## Critical gotchas

- **Charts:** bar/line series `data` must be plain numbers (`{value,…}` items
  coerce to 0 — only pie takes `{name,value}`); colour by series, not per bar;
  `option` is pure JSON with template formatters only (`{b}`/`{c}`/`{d}`), never functions.
- **Morph needs deterministic, stable ids** shared across the slides that
  should animate together; different ids simply cut.
- **Fully specify element fields** as the skeleton shows (shapes need
  `stroke`/`strokeWidth`; text needs `fontFamily`/`align`/`valign`).
- **Media:** embed only short clips as data URIs; large videos bloat the file.
- `template:true` → every open mints a fresh deck; `readonly:true` → boots
  straight into the show with no editor.

## Self-audit before delivering

- [ ] `build_deck.py` exits 0 and warnings were reviewed
- [ ] numbers shown as text that should be a **chart**?
- [ ] consecutive slides on one subject share ids + `transition:"morph"`?
- [ ] one motion moment (ken-burns / loop / count-up), especially on the cover?
- [ ] speaker notes on every slide, figures embedded, no external URLs
- [ ] text fits its box: estimate line wraps for long headings and shrink or split

The MIRA preview runs the deck in a sandboxed iframe (scripts allowed, no
same-origin access), which is why read-only slideshow mode is the default. If a
browser is available you may open the file to eyeball slides, but it is not required.
