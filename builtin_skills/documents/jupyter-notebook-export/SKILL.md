---
name: jupyter-notebook-export
description: Export a project's experiment code and results as one executed Jupyter notebook (.ipynb) for reproduction ("Jupyter Notebook" deliverable). Builds from task_plan.json, runs nbconvert, verifies all cells ran.
metadata:
  scenarios: ["Jupyter Notebook deliverable", "Reproducible experiment export", "Share code and results as one file", "Convert experiment scripts into a notebook"]
---

# Exporting experiments as a reproduction notebook

Goal: one `.ipynb` file that contains the experiment code **and** real results
(tables, metrics, figures) from an actual run, so the user can open it and
reproduce the work. Never invent results and never deliver a notebook you did
not run successfully without saying so.

Bundled helper (path relative to this skill's directory):
`scripts/build_notebook.py` with subcommands `build`, `run`, `check`.

## Workflow

1. **Collect the evidence.** Read `task_plan.json` (`experiments[]`: `method`,
   `repro.script_path`, `results.metrics/findings/artifacts`, `conclusion`,
   `commit`) or, for modular projects, the selected experiment in
   `module_data`. Read the referenced scripts and look in
   `experiments/<id>/` or `outputs/<id>/` for `metrics.json`, `results.json`
   and figures. If the delivery run selected specific experiments, export
   only those.

2. **Design the notebook** as a story a stranger can run top to bottom:
   title and summary → environment → parameters → one section per
   experiment (goal, code, results, short interpretation) → conclusion.
   - Split long scripts into logical cells (load data → preprocess → train →
     evaluate → plot). Keep the original logic; do not "improve" the method.
   - Put paths and seeds in the parameters block (`DATA_DIR`, `SEED`, ...);
     refer to files relative to `PROJECT_ROOT`, which the generated setup
     cell finds automatically. No absolute paths, no credentials.
   - Re-compute results inside the notebook instead of pasting numbers. If
     recomputing is impossible (data not shipped, hours of training), load the
     saved `metrics.json` / figure files from the project and state clearly in
     a markdown cell that the notebook shows saved results.
   - Large or private data must not be embedded; document where it is expected.

3. **Write the spec** (see the docstring in `scripts/build_notebook.py`) to a
   working JSON file and build:

   ```bash
   python <skill_dir>/scripts/build_notebook.py build result/exports/_spec.json result/exports/reproduction.ipynb
   ```

4. **Prepare the project virtualenv and execute.** The exec tool already runs
   inside the project's uv environment:

   ```bash
   uv pip install nbformat nbconvert ipykernel <the experiment's own requirements>
   python <skill_dir>/scripts/build_notebook.py run result/exports/reproduction.ipynb --timeout 1800
   python <skill_dir>/scripts/build_notebook.py check result/exports/reproduction.ipynb
   ```

   `run` executes in place with `nbconvert --execute`; `check` must print
   `ok`. Use `exec`'s `background` mode for long runs and poll the job.

5. **If execution fails**, read the failing cell's error, fix the spec (missing
   dependency, wrong path, data not found), rebuild and rerun. After a few
   honest attempts, stop and report exactly which cell fails and why. Do not
   hand over a notebook with error outputs or unexecuted cells without telling
   the user, and never hide an error by deleting the cell.

6. **Clean up and publish.** Delete the working spec, and publish only the
   `.ipynb`. Mention in the summary the Python/package versions used and
   anything the user must provide (data location, GPU).

## Quality checklist

- [ ] `check` prints ok: all code cells executed, no error outputs
- [ ] first code cell sets `PROJECT_ROOT`; no absolute paths or secrets anywhere
- [ ] dependencies listed in the environment cell with the versions actually used
- [ ] figures are produced by cells (inline matplotlib) so they live in the file
- [ ] every result number comes from a cell output or a saved artifact, not from memory
- [ ] seeds are fixed and exposed as parameters
