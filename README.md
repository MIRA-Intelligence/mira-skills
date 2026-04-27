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

---
*Developed for the MIRA Intelligence ecosystem.*
