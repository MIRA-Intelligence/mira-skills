name: documents
description: "Use this skill as an orchestrator for any task involving office documents, PDFs, or scientific writing. This includes Word (.docx), Excel (.xlsx), PowerPoint (.pptx), PDF files, research posters, and academic manuscripts. Trigger this skill whenever a user wants to create, read, edit, or convert documents. This skill will guide you to the correct specialized sub-skill based on the format or workflow."
metadata:
  scenarios: ["Automated report generation", "Extracting data from bulk PDFs", "Scientific manuscript writing", "Creating research posters", "Collaborative document co-authoring"]
---

# Document Processing Orchestrator

This skill acts as a central hub for all document-related operations in MIRA. It delegates tasks to specialized skills based on the file format or specific writing workflow involved.

## Specialized Skills

| Format / Task | Specialized Skill | Primary Triggers |
|--------|-------------------|------------------|
| **PDF** | `pdf` | Any mention of PDF, scanned documents, filling forms, OCR, or merging/splitting PDF files. |
| **Word** | `docx` | Word docs, .docx files, professional reports, memos, letterheads, or Word templates. |
| **Excel** | `xlsx` | Spreadsheets, .xlsx, .csv, .tsv, data analysis, financial models, or tabular data cleaning. |
| **PowerPoint** | `pptx` | Slide decks, presentations, pitch decks, .pptx files, or speaker notes. |
| **Scientific Slides** | `scientific-slides` | Scientific slide decks, presentations for research talks, conference presentations, thesis defense slides, or LaTeX Beamer. |
| **Scientific Writing** | `scientific-writing` | Scientific manuscripts, journal papers, IMRAD structure, academic prose, and citations. |
| **Research Posters** | `latex-posters` | Academic posters, conference posters, beamerposter, tikzposter, or baposter. |
| **PPTX Posters** | `pptx-posters` | PowerPoint posters (HTML-based), explicitly requested PPTX format. |
| **Doc Co-Authoring** | `doc-coauthoring` | Collaborative writing workflow, drafting proposals, specs, or complex documents. |

## Decision Guide

### 1. Identify the Format or Task
- **Is it a PDF?** Use the `pdf` skill. This is the best choice for text extraction from non-editable files, OCR, and form filling.
- **Is it a Word Document?** Use the `docx` skill. Best for high-fidelity document generation and editing XML-based Word files.
- **Is it a Spreadsheet?** Use the `xlsx` skill. Use this for anything involving rows, columns, formulas, and data analysis via pandas.
- **Is it a Presentation?** Use the `pptx` skill. Use this for creating and editing standard slide decks.
- **Is it a Scientific Slide Deck?** Use the `scientific-slides` skill. Optimized for research talks using LaTeX Beamer, focusing on visual engagement and research backing.
- **Is it a Scientific Manuscript?** Use the `scientific-writing` skill. Use for journal papers, following IMRAD structure and ensuring professional academic prose.
- **Is it a Research Poster?** 
    - **Standard/LaTeX**: Use `latex-posters`. This is the default for academic conferences (A0, beamerposter, etc.).
    - **PPTX Only**: Use `pptx-posters` ONLY if the user explicitly requests a PowerPoint format.
- **Is it a Complex/Collaborative Writing Task?** Use `doc-coauthoring`. This provides a structured 3-stage workflow (Context Gathering, Refinement, Reader Testing) to build high-quality documents from scratch.

### 2. Multi-Format & Advanced Workflows
If a task involves multiple formats or a deep research process, use this orchestrator to manage the sequence:
- **Research to Publication**: Use `scientific-writing` to draft a manuscript, then use `latex-posters` or `scientific-slides` to prepare the corresponding conference materials.
- **Collaborative Drafting**: Use `doc-coauthoring` to gather team context and iteratively build a technical specification or proposal.
- **Conversion to PDF**: Start with the source format skill (`docx`, `xlsx`, or `pptx`) and use the `soffice` scripts provided within those skills to generate the PDF.
- **Data to Document**: Use `xlsx` to process tabular data, then pass the findings to `scientific-writing` or `docx` to generate a report.

## Common Pitfalls
- **Don't use bullet points for manuscripts**: `scientific-writing` mandates full paragraphs for the final output.
- **Poster Font Sizes**: Always ensure text in AI-generated poster graphics is "poster-size" (GIANT bold fonts) as per the poster skills' mandates.
- **Validate Outputs**: Always use the validation scripts (e.g., `validate.py`, `recalc.py`) provided in the sub-skills after making modifications.
