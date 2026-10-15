#!/usr/bin/env python3
"""Build or validate a MIRA Slides ``.mira.html`` deck without any network access.

Usage:
    build_deck.py build DOC.json OUT.mira.html [--editable]
                                                  # copy bundled app, inject document
    build_deck.py check DECK.mira.html            # validate an existing deck

``DOC.json`` is the plain deck document. MIRA Slides is built from Bento and keeps
its document format, so the format id stays ``{"format": "bento/slides", ...}``.
By default the deck is built with ``readonly: true`` so it boots straight into the
slideshow. That is what MIRA's inline preview needs: the preview iframe is sandboxed
(scripts only, opaque origin) and the editor cannot start there. Pass ``--editable``
only when the user asked for an editable deck.

Exit status is 0 on success, 1 when validation fails; problems go to stderr.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "assets" / "Mira_Slides.html"
BLOCK = re.compile(
    r'(<script type="application/bento\+json" id="bento-doc">)(.*?)(</script>)',
    re.DOTALL,
)
RIGHT_EDGE = 1184  # 96px side margins on a 1280px canvas


def validate(doc: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if doc.get("format") != "bento/slides":
        errors.append('"format" must be "bento/slides"')
    size = doc.get("size")
    if not (isinstance(size, dict) and size.get("width") and size.get("height")):
        errors.append('"size" {width,height} is required (canonical 1280x720)')
    theme = doc.get("theme")
    if not (isinstance(theme, dict) and theme.get("fontFamily")):
        errors.append('"theme" with "fontFamily" is required; the app will not boot without it')
    for key in ("docId", "collab"):
        if key in doc:
            errors.append(f'omit "{key}" for a new deck; the app mints it on first open')
    slides = doc.get("slides")
    if not isinstance(slides, list) or not slides:
        errors.append('"slides" must be a non-empty list')
        return errors, warnings
    assets = doc.get("assets") or {}
    for si, slide in enumerate(slides, 1):
        seen: set[str] = set()
        if not slide.get("id"):
            errors.append(f"slide {si}: missing id")
        if not slide.get("notes"):
            warnings.append(f"slide {si}: no speaker notes")
        for el in slide.get("elements", []):
            eid = el.get("id")
            where = f"slide {si} element {eid!r}"
            if not eid:
                errors.append(f"slide {si}: element without id")
            elif eid in seen:
                errors.append(f"{where}: duplicate id on the slide")
            seen.add(eid)
            for field in ("x", "y", "w", "h"):
                if not isinstance(el.get(field), (int, float)):
                    errors.append(f"{where}: numeric {field!r} required")
            if el.get("type") == "text" and not (el.get("fontFamily") and el.get("align")):
                errors.append(f"{where}: text needs fontFamily and align")
            if el.get("type") == "shape" and el.get("shape") != "line" and "stroke" not in el:
                warnings.append(f"{where}: shape without stroke/strokeWidth may render wrong")
            if isinstance(el.get("x"), (int, float)) and isinstance(el.get("w"), (int, float)):
                if el["x"] + el["w"] > RIGHT_EDGE + 1 and el.get("fit") != "cover":
                    warnings.append(f"{where}: right edge {el['x'] + el['w']} > {RIGHT_EDGE} (96px margin)")
            src = el.get("src")
            if isinstance(src, str):
                if src.startswith("asset:"):
                    if src[6:] not in assets:
                        errors.append(f"{where}: {src} is not defined in doc.assets")
                elif re.match(r"https?:", src) and el.get("kind") not in ("video", "audio"):
                    errors.append(f"{where}: external image URL; embed it as a data URI in doc.assets")
    return errors, warnings


def encode(doc: dict) -> str:
    # Escape every "<" so the JSON can never contain a literal </script>.
    return json.dumps(doc, ensure_ascii=False, indent=1).replace("<", "\\u003c")


def read_doc(html: str) -> dict:
    match = BLOCK.search(html)
    if not match:
        raise SystemExit('no #bento-doc block found; not a mira-slides deck')
    body = match.group(2).strip()
    if not body:
        raise SystemExit("the #bento-doc block is empty")
    return json.loads(body)


def report(errors: list[str], warnings: list[str]) -> int:
    for message in warnings:
        print(f"warning: {message}", file=sys.stderr)
    for message in errors:
        print(f"error: {message}", file=sys.stderr)
    return 1 if errors else 0


def main(argv: list[str]) -> int:
    editable = "--editable" in argv
    argv = [a for a in argv if a != "--editable"]
    if len(argv) == 4 and argv[1] == "build":
        doc = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
        if not editable:
            doc["readonly"] = True
        errors, warnings = validate(doc)
        if report(errors, warnings):
            return 1
        html = APP.read_text(encoding="utf-8")
        if not BLOCK.search(html):
            raise SystemExit("bundled app is missing the #bento-doc block")
        out = BLOCK.sub(lambda m: f"{m.group(1)}\n{encode(doc)}\n{m.group(3)}", html, count=1)
        target = Path(argv[3])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(out, encoding="utf-8")
        print(f"wrote {target} ({target.stat().st_size // 1024} KB, {len(doc['slides'])} slides)")
        return 0
    if len(argv) == 3 and argv[1] == "check":
        doc = read_doc(Path(argv[2]).read_text(encoding="utf-8"))
        errors, warnings = validate(doc)
        # An existing deck legitimately carries docId; only collab keys are a concern.
        errors = [e for e in errors if "docId" not in e]
        if "collab" in doc:
            warnings.append("deck carries live-session keys (collab); tell the user before sharing")
            errors = [e for e in errors if '"collab"' not in e]
        return report(errors, warnings)
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
