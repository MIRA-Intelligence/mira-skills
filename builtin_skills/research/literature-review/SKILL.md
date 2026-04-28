---
name: literature-review
description: "Execute autonomous multi-step deep research and write comprehensive literature reviews. Combines broad topic deep-dives with systematic medical imaging review capabilities. Triggers on 'deep research', 'literature review', 'survey paper', 'systematic review'."
metadata:
  version: "2.0.0"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - Task
  - mcp__arxiv-mcp-server__search_papers
  - mcp__pubmed-mcp-server__pubmed_search_articles
  - mcp__zotero__zotero_search_items
---

# Literature Review & Deep Research Skill

This skill acts as the analytical engine to read full texts, synthesize systematic reviews, or write deep research reports using a rigorous workflow. It handles both general deep-dive research and specialized academic review papers (e.g., Medical Imaging AI reviews).

## 1. Deep Research Strategy (General Topics)

Autonomous multi-step research that searches multiple sources, reads full content, synthesizes findings, and produces a structured report.

### Step 1: Query Decomposition
Break the research question into 3–5 sub-questions covering: Core definition, Current evidence, Debates/limitations, Clinical implications, and Recent developments.

### Step 2: Multi-Source Search
Use the `literature-search` skill or available MCP tools to gather sources:
1. PubMed (peer-reviewed evidence)
2. ArXiv MCP (latest methods, preprints)
3. Zotero (existing library)
4. Web search (guidelines, reviews)

### Step 3: Source Evaluation & Synthesis
- **Medical Evidence Hierarchy**: Systematic reviews > RCTs > Cohort studies > Case reports > Expert opinion.
- Synthesize across sources into a coherent narrative. Identify points of consensus, contradictions, knowledge gaps, and the strongest evidence.

### Step 4: Structured Report
Produce a well-formatted Markdown report with: Summary, Background, Current Evidence, Key Debates, Clinical Implications, Recent Developments, and Sources.

---

## 2. Systematic Academic Literature Review (e.g., Medical Imaging)

When writing formal survey papers, systematic reviews, or literature analyses on specific domains (like CT/MRI segmentation, pathology, etc.), use a highly structured 7-phase workflow.

### Quick Start
1. **Initialize project** with three core files:
   - `CLAUDE.md` - Writing guidelines and terminology
   - `IMPLEMENTATION_PLAN.md` - Staged execution plan
   - `manuscript_draft.md` - Main manuscript
2. **Follow the 7-phase workflow** (see `references/WORKFLOW.md` for details).

### Standard Review Structure
```markdown
# [Title]: State of the Art and Future Directions

## Key Points
- [3-5 bullets summarizing main findings]

## Abstract

## 1. Introduction
### 1.1 Clinical Background
### 1.2 Technical Challenges
### 1.3 Scope and Contributions

## 2. Datasets and Evaluation Metrics
### 2.1 Public Datasets (Table 1)
### 2.2 Evaluation Metrics

## 3. Deep Learning Methods
### 3.1 [Category 1]
### 3.2 [Category 2]
(Table 2: Method Comparison)

## 4. Downstream Applications

## 5. Commercial Products & Clinical Translation (Table 3)

## 6. Discussion
### 6.1 Current Limitations
### 6.2 Future Directions

## 7. Conclusion

## References
```

### Method Description Template
```markdown
### 3.X [Method Category]

[1-2 paragraph introduction with motivation]

**[Method Name]:** [Author] et al. [ref] proposed [method], which [innovation]:
- [Key component 1]
- [Key component 2]
Achieves Dice of X.XX on [dataset].

**Limitations:** Despite advantages, [category] methods face: (1) [limit 1]; (2) [limit 2].
```

## 3. Core Writing Principles

- **Writing Style**: Use hedging language ("may", "suggests", "has shown promising results"). Avoid absolutes ("X is the best method").
- **Paragraph Structure**: Topic sentence (main claim) → Supporting evidence (citations + data) → Analysis (critical evaluation) → Transition to next paragraph.
- **Visual Enhancements**: Always consider incorporating tables (e.g., Dataset Table, Method Comparison Table) and figures. Utilize the `visualization` skill to plot trend lines or pie charts of publication stats if needed.
- **Reporting Guidelines**: Always ensure compliance with PRISMA guidelines for systematic reviews and meta-analyses.

## 4. Reference Files
- `references/WORKFLOW.md`: Detailed 7-phase workflow.
- `references/TEMPLATES.md`: Templates for CLAUDE.md and IMPLEMENTATION_PLAN.md.
- `references/DOMAINS.md`: Domain-specific method categories (e.g., Coronary Artery, Brain Imaging, Pathology).
- `references/QUALITY_CHECKLIST.md`: Pre-submission quality checklist ensuring comprehensive coverage and standard language.