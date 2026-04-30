---
name: documents
description: "Use this skill as an orchestrator for any task involving office documents or PDFs. This includes Word (.docx), Excel (.xlsx), PowerPoint (.pptx), and PDF files. Trigger this skill whenever a user wants to create, read, edit, or convert documents. This skill will guide you to the correct specialized sub-skill based on the file format."
---

# Document Processing Orchestrator

This skill acts as a central hub for all document-related operations in MIRA. It delegates tasks to specialized skills based on the file format involved.

## Specialized Skills

| Format | Specialized Skill | Primary Triggers |
|--------|-------------------|------------------|
| **PDF** | `pdf` | Any mention of PDF, scanned documents, filling forms, OCR, or merging/splitting PDF files. |
| **Word** | `docx` | Word docs, .docx files, professional reports, memos, letterheads, or Word templates. |
| **Excel** | `xlsx` | Spreadsheets, .xlsx, .csv, .tsv, data analysis, financial models, or tabular data cleaning. |
| **PowerPoint** | `pptx` | Slide decks, presentations, pitch decks, .pptx files, or speaker notes. |
| **Scientific Slides** | `scientific-slides` | Scientific slide decks, presentations for research talks, conference presentations, thesis defense slides, or LaTeX Beamer. |

## Decision Guide

### 1. Identify the Format
- **Is it a PDF?** Use the `pdf` skill. This is the best choice for text extraction from non-editable files, OCR, and form filling.
- **Is it a Word Document?** Use the `docx` skill. Best for high-fidelity document generation and editing XML-based Word files.
- **Is it a Spreadsheet?** Use the `xlsx` skill. Use this for anything involving rows, columns, formulas, and data analysis via pandas.
- **Is it a Presentation?** Use the `pptx` skill. Use this for creating and editing slide decks.
- **Is it a Scientific Slide Deck?** Use the `scientific-slides` skill. This is specialized for building slide decks and presentations for research talks using Nano Banana Pro or LaTeX Beamer, with a focus on visual engagement and research backing.

### 2. Multi-Format Workflows
If a task involves multiple formats, use this orchestrator to manage the sequence:
- **Conversion to PDF**: Start with the source format skill (`docx`, `xlsx`, or `pptx`) and use the `soffice` scripts provided within those skills to generate the PDF.
- **Data to Document**: Use `xlsx` to process tabular data, then pass the findings to `docx` or `pptx` to generate a report or presentation.
- **PDF to Data**: Use `pdf` (via `pdfplumber`) to extract tables, then pass the data to `xlsx` for further analysis.

## Common Pitfalls
- **Don't hardcode values in Excel**: Use the `xlsx` skill's guidance on Excel formulas.
- **Don't use Unicode bullets in Word/PPT**: Use the specialized list formatting described in `docx` and `pptx` skills.
- **Validate Outputs**: Always use the validation scripts (e.g., `validate.py`, `recalc.py`) provided in the sub-skills after making modifications.
