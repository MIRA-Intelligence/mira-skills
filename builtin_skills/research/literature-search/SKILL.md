---
name: "literature-search"
description: "Comprehensive literature and web search engine. Integrates NCBI PubMed via BioPython Entrez and 17 general web search engines (Google, Bing, DuckDuckGo, WolframAlpha, etc.). Use this to find peer-reviewed papers, clinical guidelines, datasets, code repositories, or broad web knowledge without API keys."
metadata:
  aliases: ["pubmed search", "google scholar", "web search", "find papers"]
---

# Literature Search

This skill consolidates both academic database querying (PubMed) and broad web search strategies (Multi-Search Engine). It is the foundational step for any discovery or literature review task.

## 1. PubMed Search (Peer-Reviewed Medical Literature)

Search NCBI PubMed for scientific literature using BioPython's Entrez module. Use this when the user asks to find papers, search literature, look up research, find publications, or asks about recent studies on biomedical topics.

### Setup and Basic Search
```python
from Bio import Entrez
Entrez.email = "medclaw@freedomai.com"

# Search
handle = Entrez.esearch(db="pubmed", term="CRISPR delivery methods", retmax=20, sort="date")
record = Entrez.read(handle)
handle.close()

id_list = record["IdList"]
print(f"Found {record['Count']} results, showing top {len(id_list)}")

# Fetch details
handle = Entrez.efetch(db="pubmed", id=id_list, rettype="xml")
records = Entrez.read(handle)
handle.close()

for article in records['PubmedArticle']:
    medline = article['MedlineCitation']
    pmid = str(medline['PMID'])
    title = medline['Article']['ArticleTitle']
    print(f"PMID: {pmid} | Title: {title}")
```

### Advanced PubMed Operators
- `"CRISPR"[Title] AND "delivery"[Title]` — title-specific
- `"2026"[Date - Publication]` — date filter
- `"Nature"[Journal]` — journal filter
- `review[Publication Type]` — type filter

## 2. Multi-Search Engine (Broad Web & Gray Literature)

Integration of 17 search engines for web crawling without API keys. Use this to find guidelines, news, general information, or PDFs not indexed in PubMed.

### Search Engines available via `web_fetch`
- **Google**: `https://www.google.com/search?q={keyword}`
- **DuckDuckGo**: `https://duckduckgo.com/html/?q={keyword}`
- **Brave**: `https://search.brave.com/search?q={keyword}`
- **WolframAlpha**: `https://www.wolframalpha.com/input?i={keyword}`
- **Bing**: `https://cn.bing.com/search?q={keyword}&ensearch=1`

### Quick Examples
```javascript
// Basic search
web_fetch({"url": "https://www.google.com/search?q=python+tutorial"})

// Site-specific
web_fetch({"url": "https://www.google.com/search?q=site:github.com+react"})

// File type
web_fetch({"url": "https://www.google.com/search?q=machine+learning+filetype:pdf"})

// Time filter (past week)
web_fetch({"url": "https://www.google.com/search?q=ai+news&tbs=qdr:w"})

// DuckDuckGo Bangs
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+tensorflow"})

// Knowledge calculation
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})
```

### Advanced Search Operators
| Operator | Example | Description |
|----------|---------|-------------|
| `site:` | `site:github.com python` | Search within site |
| `filetype:` | `filetype:pdf report` | Specific file type |
| `""` | `"machine learning"` | Exact match |
| `-` | `python -snake` | Exclude term |

### Time Filters
- `tbs=qdr:h` (Past hour), `tbs=qdr:d` (Past day), `tbs=qdr:w` (Past week), `tbs=qdr:m` (Past month), `tbs=qdr:y` (Past year)

## 3. Integrated Search Strategy

When tasked with researching a topic:
1. **Define the Scope**: Is it purely academic, or does it include industry news and GitHub repos?
2. **Execute Parallel Searches**:
   - Use **PubMed** for clinical trials, RCTs, and peer-reviewed biology/medicine papers.
   - Use **Google/DuckDuckGo** for guidelines (e.g., WHO, AHA), technical tutorials, or PDF reports.
3. **Filter and Evaluate**: Identify the most authoritative sources.

For extensive topic analysis and report generation, pass the retrieved literature to the **`literature-review`** skill.
