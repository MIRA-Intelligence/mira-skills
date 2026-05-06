# Data Compliance & Bilingual Alignment

Use this reference to ensure your data package meets FAIR standards and aligns Chinese author intent with international publication terminology.

## 1. Bilingual Terminology Alignment
Translate intent, not wording. Nature-family journals prefer precise institutional/repository routes.

| 中文 (Chinese) | Preferred English | Note |
|----------------|-------------------|------|
| 数据可用性声明 | Data Availability | Standard journal heading |
| 原始数据 | Raw data | Avoid calling processed tables "raw" |
| 源数据 | Source data | Underlying data for figures/tables |
| 补充材料 | Supplementary Information | Use exact file/table names |
| 公共数据库 | Public repository | Name the database and identifier |
| 受限数据 | Restricted data | Explain reason (privacy, commercial) |
| 脱敏数据 | De-identified data | "Anonymous" implies zero re-id risk |
| 合理请求 | Reasonable request | Must add route, eligibility, conditions |
| 通讯作者 | Corresponding author | Do not make email the ONLY access route |

## 2. FAIR Metadata Checklist
Ensure your dataset is Findable, Accessible, Interoperable, and Reusable.

| Principle | Check |
|-----------|-------|
| **Findable** | Dataset has a persistent identifier (DOI/Accession), rich keywords, and searchable metadata. |
| **Accessible** | Identifier resolves through standard protocol; access conditions are explicit. |
| **Interoperable** | Files use community formats (CSV/TSV/H5); metadata use shared vocabulary and units. |
| **Reusable** | License (CC-BY/CC0), provenance (how data were generated), and quality-control notes are clear. |

## 3. DataCite Core Fields (Mandatory for DOIs)
- Identifier (DOI)
- Creator (Authors)
- Title (Dataset name)
- Publisher (Repository)
- Publication Year
- Resource Type (Dataset, Software, Image)

## 4. Repository Selection Decision Tree
1. Use a **Mandated Repository** if the data type requires it (e.g., GEO for sequencing, PDB for structures).
2. Use a **Discipline-Specific Repository** if no mandate applies.
3. Use a **Generalist Repository** (Zenodo, Figshare, Dryad) or Institutional Repository as fallback.
4. **Never** use personal/lab websites or ad-hoc cloud folders (Google Drive/Baidu Netdisk) as the primary route.
