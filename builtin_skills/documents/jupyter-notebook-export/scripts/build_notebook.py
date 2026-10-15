#!/usr/bin/env python3
"""Assemble, execute and verify a reproduction notebook (.ipynb).

Usage:
    build_notebook.py build SPEC.json OUT.ipynb
    build_notebook.py run   OUT.ipynb [--timeout SECONDS]
    build_notebook.py check OUT.ipynb

``build`` needs only the standard library (it writes nbformat 4.5 JSON by hand).
``run`` executes the notebook in place with ``jupyter nbconvert --execute`` using
the *current* interpreter, so run it with the project virtualenv's python after
``uv pip install nbformat nbconvert ipykernel``.
``check`` exits 1 unless every code cell ran (execution_count set) with no error output.

SPEC.json:
{
  "title": "Notebook title",
  "summary": "Markdown shown under the title (goal, data, headline result)",
  "requirements": ["numpy", "scikit-learn"],     # shown in the environment cell
  "parameters": {"DATA_DIR": "data", "SEED": 42},  # a single editable parameters cell
  "sections": [
    {"title": "Experiment exp001: baseline",
     "markdown": "What and why.",
     "code": "print('python source')",
     "markdown_after": "Interpretation of the output."}
  ]
}
Each section may also give "code" as a list of cells. Everything is optional except sections.
"""
from __future__ import annotations

import json
import subprocess
import sys
import uuid
from pathlib import Path

SETUP_CELL = '''\
# Locate the project root so relative paths work wherever this notebook is run.
# Override with the MIRA_PROJECT_ROOT environment variable if needed.
import os
from pathlib import Path

def find_project_root(start=None):
    if os.environ.get("MIRA_PROJECT_ROOT"):
        return Path(os.environ["MIRA_PROJECT_ROOT"]).resolve()
    here = Path(start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / "task_plan.json").exists() or (candidate / ".mira").exists():
            return candidate
    return here

PROJECT_ROOT = find_project_root()
print("Project root:", PROJECT_ROOT)
'''


def _source(text: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    return lines or [""]


def _cell(kind: str, text: str) -> dict:
    cell: dict = {"id": uuid.uuid4().hex[:8], "cell_type": kind, "metadata": {}, "source": _source(text)}
    if kind == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def build(spec: dict) -> dict:
    sections = spec.get("sections")
    if not isinstance(sections, list) or not sections:
        raise SystemExit('spec needs a non-empty "sections" list')
    cells: list[dict] = []
    head = f"# {spec.get('title') or 'Reproduction notebook'}"
    if spec.get("summary"):
        head += f"\n\n{spec['summary']}"
    cells.append(_cell("markdown", head))

    requirements = spec.get("requirements") or []
    env = "## Environment\n\n"
    env += "Install the dependencies below (for example `uv pip install ...`) before running."
    if requirements:
        env += "\n\n" + "\n".join(f"- `{r}`" for r in requirements)
    cells.append(_cell("markdown", env))
    cells.append(_cell("code", SETUP_CELL))

    params = spec.get("parameters") or {}
    if params:
        lines = ["# Parameters: edit these to point at your own data / settings."]
        lines += [f"{name} = {value!r}" for name, value in params.items()]
        cells.append(_cell("markdown", "## Parameters"))
        cells.append(_cell("code", "\n".join(lines) + "\n"))

    for section in sections:
        body = f"## {section['title']}" if section.get("title") else ""
        if section.get("markdown"):
            body = f"{body}\n\n{section['markdown']}".strip()
        if body:
            cells.append(_cell("markdown", body))
        code = section.get("code") or []
        for chunk in [code] if isinstance(code, str) else code:
            cells.append(_cell("code", chunk))
        if section.get("markdown_after"):
            cells.append(_cell("markdown", section["markdown_after"]))

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def _load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def check(path: str) -> list[str]:
    nb = _load(path)
    problems: list[str] = []
    if nb.get("nbformat") != 4:
        problems.append("not an nbformat 4 notebook")
    for index, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        label = f"code cell {index}"
        if cell.get("execution_count") is None and "".join(cell.get("source", [])).strip():
            problems.append(f"{label}: not executed")
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                problems.append(f"{label}: error {output.get('ename')}: {output.get('evalue')}")
    return problems


def run(path: str, timeout: int) -> int:
    command = [
        sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace",
        f"--ExecutePreprocessor.timeout={timeout}", "--ExecutePreprocessor.kernel_name=python3", path,
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout + 60)
    except subprocess.TimeoutExpired:
        print(f"error: execution exceeded {timeout}s", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: cannot start jupyter: {exc}", file=sys.stderr)
        return 1
    if result.returncode != 0:
        tail = (result.stderr or result.stdout).strip().splitlines()[-25:]
        print("error: nbconvert failed:\n" + "\n".join(tail), file=sys.stderr)
        missing = ("No module named jupyter", "No module named 'nbconvert'", "jupyter-nbconvert` not found")
        if any(marker in result.stderr for marker in missing):
            print("hint: uv pip install nbformat nbconvert ipykernel", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str]) -> int:
    if len(argv) == 4 and argv[1] == "build":
        nb = build(_load(argv[2]))
        Path(argv[3]).parent.mkdir(parents=True, exist_ok=True)
        Path(argv[3]).write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {argv[3]} ({len(nb['cells'])} cells)")
        return 0
    if len(argv) in (3, 5) and argv[1] == "run":
        timeout = int(argv[4]) if len(argv) == 5 and argv[3] == "--timeout" else 1800
        return run(argv[2], timeout)
    if len(argv) == 3 and argv[1] == "check":
        problems = check(argv[2])
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        if not problems:
            print("ok: every code cell executed without errors")
        return 1 if problems else 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
