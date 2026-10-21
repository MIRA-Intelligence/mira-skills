# MIRA Skills

This repository contains specialized skills designed for [MIRA (Medical  Intelligence Research Agent)](https://github.com/MIRA-Intelligence/mira.git). These skills extend MIRA's capabilities across medical imaging, statistical analysis, scientific writing, and research automation.

## 🌟 Core Domains

MIRA's skills are organized into specialized domains to support the entire lifecycle of medical research:

- **Medical Image Analysis**: Deep learning pipelines (MONAI) and specialized agents for data preprocessing, architecture design, and testing.
- **ML & Statistics**: Radiomics feature extraction, survival analysis, and advanced statistical modeling.
- **Data Processing**: Standards-based handling of DICOM, NIfTI, and structured medical data.
- **Research & Writing**: Literature search automation, scientific writing assistance, and document generation (LaTeX, PPTX, DOCX).
- **Visualization**: Professional publication-quality plotting and medical data visualization.

## 🛠 Skill Format

Each skill is a directory containing a `SKILL.md` file which defines:
- **Metadata**: Name, description, and dependencies.
- **Instructions**: Specialized prompts and workflows for the MIRA agent.
- **Tools/Scripts**: Supporting Python scripts or shell utilities.

### Efficiency Guidelines
When skills reference large local documentation or logs, MIRA utilizes built-in `grep` and `glob` tools to narrow the search space before loading files. This ensures high-performance context management.

## 📂 Available Skills (Summary)

| Category | Key Skills / Tools |
|----------|-------------------|
| **Medical Imaging** | MONAI, DICOM2NIfTI, NiBabel, PyRadiomics |
| **ML & Stats** | Scikit-Learn, Scikit-Survival, Survival Analysis, Radiomics Agents |
| **Documents** | LaTeX Posters, Scientific Slides (Beamer/PPTX), Office (DOCX/XLSX) |
| **Research** | Literature Search, Literature Review, Scientific Writing |
| **Visualization** | Matplotlib, Seaborn, Plotly, Scientific Viz |
| **Utilities** | GitHub, Tmux, Cron, Memory, Summarize, Skill Creator |

## 🧩 MIRA Hub skills

`skills/` is the source of truth for skills published on **MIRA Hub** — the
research-focused skill marketplace at
<https://mira-intelligence.github.io/mira-hub/>.

Each skill is a single folder under [`skills/`](./skills) shaped like:

```
skills/<slug>/
├── SKILL.md          # untouched, engine-compatible (YAML frontmatter + markdown)
├── mirahub.yaml      # hub-only metadata (tags, version, author, screenshots, ...)
├── plugin.json       # optional; the engine infers it if absent
├── hub/
│   ├── cover.png
│   └── screenshots/01.png
└── ...               # scripts, references, assets
```

The folder name **must** equal the `slug` in `mirahub.yaml` and the `name`
field in `SKILL.md`'s frontmatter. There is **no** category / domain folder
nesting — categorisation is purely tag-driven (see
[`schemas/mirahub.schema.json`](./schemas/mirahub.schema.json) and the
hub's [`taxonomy.yaml`](https://github.com/MIRA-Intelligence/mira-hub/blob/main/taxonomy.yaml)).

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to add a skill.

### Tag conventions

Tags are flat strings; namespaced ones (`<ns>:<value>`) become faceted
filters in the hub UI:

- `domain:<id>` — research domain. Default values: `radiology`, `pathology`,
  `genomics`, `clinical`, `pharma`, `neuroscience`, `bio`, `epidemiology`,
  `software`, `general`.
- `functionality:<id>` — what the skill does. Default values: `search`,
  `data`, `analysis`, `modeling`, `visualization`, `writing`, `documents`,
  `coding`, `automation`, `integration`.
- `lang:<id>` — primary language(s) the skill targets, e.g. `lang:python`.
- Anything else (`dicom`, `texture`, …) is a free-form tag and is searchable
  but does not show up as a filter checkbox.
- `source:lobehub` — vendored third-party skill (see below).

The hub site is bilingual: each skill's abstract comes from `SKILL.md`
`description` plus a translation in `mirahub.yaml` `description` (`zh` or
`en`); see [`CONTRIBUTING.md`](./CONTRIBUTING.md).

Adding new namespace values is a one-line PR to `mira-hub/taxonomy.yaml`.

### Third-party skills

Skills listed in [`upstream.yaml`](./upstream.yaml) are vendored from their
original authors' repositories at a pinned commit. They're copied as-is
except for the `SKILL.md` `name` (set to the slug), upstream dev/test files
listed under `exclude`, and sections listed under `strip_sections` (e.g. ones
telling the agent to cite the vendor in the user's manuscripts). Each such
folder keeps the upstream `LICENSE`, and its generated `mirahub.yaml` credits
the upstream author and links the exact source. That per-folder `LICENSE`
(not this repository's root license) governs the skill. Don't edit those
folders by hand; change `upstream.yaml` and re-run:

```bash
# from inside a local checkout of mira-hub
npm run vendor:upstream -- --skills-dir ../mira-skills/skills
```

### Local validation

```bash
# from inside a local checkout of mira-hub
npm run -w @mirahub/builder check -- --skills-dir ../mira-skills/skills
```

CI runs the same check on every PR.

---
*Developed for the MIRA Intelligence ecosystem.*
