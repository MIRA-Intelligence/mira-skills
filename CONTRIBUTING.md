# Contributing a skill

Thanks for sharing! Skills accepted here become installable from
<https://mira-intelligence.github.io/mira-hub/> in two clicks.

## 1. Fork & branch

```bash
git clone https://github.com/MIRA-Intelligence/mira-skills
cd mira-skills
git checkout -b add-my-skill
```

## 2. Create your skill folder

```
skills/<slug>/
├── SKILL.md
├── mirahub.yaml
├── plugin.json        # optional
└── hub/cover.png      # optional but strongly recommended (1200×630)
```

`<slug>` must be lowercase kebab-case, match `mirahub.yaml.slug`, and match
the `name:` field of `SKILL.md`.

### `SKILL.md`

Engine-compatible YAML frontmatter + markdown body. See
[`mira/mira_engine/skills/`](https://github.com/MIRA-Intelligence/mira/tree/main/mira_engine/skills)
for many examples.

```markdown
---
name: my-skill
description: One sentence describing when to use this skill.
metadata:
  mira:
    emoji: "🔬"
    requires: { bins: ["python"] }
---

# My Skill

Markdown instructions for the agent...
```

### `mirahub.yaml`

```yaml
slug: my-skill
version: 0.1.0
maturity: beta                 # stable | beta | experimental
license: MIT
author:
  name: Your Name
  github: yourhandle
homepage: https://...           # optional
links:                          # optional
  repo: https://...
  docs: https://...
  issues: https://...
cover: hub/cover.png            # optional, relative to skill folder
screenshots:                    # optional
  - hub/screenshots/01.png
tags:
  - domain:radiology
  - functionality:analysis
  - lang:python
  - dicom                       # free-form tags are fine too
```

Validate against [`schemas/mirahub.schema.json`](./schemas/mirahub.schema.json)
in your editor (VS Code's YAML extension picks it up automatically) or via
the hub builder.

## 3. Run the validator

```bash
git clone https://github.com/MIRA-Intelligence/mira-hub
cd mira-hub
npm install
npm run -w @mirahub/builder check -- --skills-dir ../mira-skills/skills
```

## 4. Open a PR

CI re-runs the validator, builds a preview registry, and a maintainer will
review. After merging to `main`, the hub site is rebuilt automatically and
your skill becomes installable within minutes.

## Appendix · vendoring a third-party skill

Good skills published elsewhere (e.g. found on the LobeHub marketplace) can be
mirrored here instead of rewritten:

1. Find the **original** repository (marketplaces re-host the same skill many
   times) and check its license: MIT / Apache-2.0 / BSD / CC-BY(-SA) only.
2. Read the whole `SKILL.md` and every bundled script before adding it.
3. Add the repo under `sources:` in [`upstream.yaml`](./upstream.yaml) with a
   pinned commit `ref`, and the skill under `skills:` with its tags.
4. From a sibling `mira-hub` checkout run
   `npm run vendor:upstream -- --skills-dir ../mira-skills/skills`
   (add `--only <slug>` for one skill), then the usual `check`. Use
   `exclude` for upstream dev/test files and the source's `strip_sections`
   for sections that shouldn't ship (e.g. self-citation instructions).

Vendored folders are regenerated from the manifest, so never hand-edit them.
Bump `ref` to pull upstream updates.

## Appendix · backfilling the built-in skills

`mira_engine/skills/` (in the main `mira` repo) ships ~30 first-party skills
(`pyradiomics`, `survival-analysis`, `pubmed-search`, `agent-browser`, …).
We are progressively mirroring them here so the hub becomes the single,
versioned source of truth and `mira-engine` can ship fewer hard-coded
defaults over time.

Migration recipe per skill:

1. `cp -R mira/mira_engine/skills/<category>/<slug> mira-skills/skills/<slug>`
2. Add a `mirahub.yaml` next to `SKILL.md`:
   - `slug` mirrors the folder name and `SKILL.md`'s `name`.
   - Pick `domain:*` / `functionality:*` tags from
     [`mira-hub/taxonomy.yaml`](https://github.com/MIRA-Intelligence/mira-hub/blob/main/taxonomy.yaml).
     Keep free-form tags too — they stay searchable.
   - `version: 0.1.0` for the first hub release; bump on substantive
     content changes.
3. If the skill ships large reference assets that aren't useful at install
   time (PDFs, model snapshots), prune them or move them behind a
   download-on-first-use pattern in the skill body.
4. Run `npm run -w @mirahub/builder check -- --skills-dir ../mira-skills/skills`
   from a sibling `mira-hub` checkout.
5. Open a PR with the slug + a one-line clinical/research rationale.

Status of the backfill effort (work-in-progress, edit as you migrate):

| State | Skills |
| --- | --- |
| Migrated | `agent-browser`, `pubmed-search`, `scientific-slides` |
| Queued for migration | `pyradiomics`, `radiomics`, `medical-image-dl-pipeline`, `survival-analysis`, `scikit-survival`, `monai`, `nibabel`, `pydicom`, `dicom2nifti`, `medical-imaging-review`, `scikit-learn`, `statistical-analysis`, `deep-research`, `multi-search-engine`, `peer-review`, `scientific-method`, `find-skills`, … |
| Hub-only (no engine equivalent) | everything in [`upstream.yaml`](./upstream.yaml) (third-party, vendored) |

Until a skill is migrated, the engine continues to ship it locally; the hub
just won't list it.
