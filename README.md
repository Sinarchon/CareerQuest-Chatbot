# CareerQuest — Research Knowledge Base

A compact, versioned research dataset for the CareerQuest student-facing chatbot. This is **not** a model or an API on its own. A server-side retrieval step must find relevant records and pass them to an LLM, along with their source metadata.

## Contents

| File | Data | Geographic / temporal scope |
| --- | --- | --- |
| `data/onet/occupation_profiles.jsonl` | Occupational descriptions, top O*NET essential and transferable skills, education, tasks, knowledge, RIASEC interest scores, job zone, related careers, software examples, and matched BLS figures | U.S., O*NET 31.0 (2026), BLS 2025–35 |
| `data/bls/occupational_outlook_2025_2035.jsonl` | Detailed occupation employment projections, job openings, wages and entry education | U.S. projections 2025–2035 |
| `data/anthropic/occupation_ai_exposure.jsonl` | Anthropic observed AI exposure estimates by SOC code | Dataset-specific observational estimates |
| `data/anthropic/task_ai_penetration.jsonl` | Anthropic task penetration estimates | Dataset-specific observational estimates |
| `data/pbs/lfs_2024_25_facts.jsonl` | Selected independently verified PBS labour statistics with PDF page references | Pakistan, 2024–25 |
| `data/wef/future_jobs_2025_facts.jsonl` | Brief original factual notes with PDF page references | Global employer forecasts to 2030 |
| `metadata/sources.json` | Publisher links, rights notes, coverage and source keys | — |
| `metadata/manifest.json` | Data counts and caveats | — |
| `scripts/search_knowledge.py` | Local demonstration of file-based source retrieval (no paid service) | — |

## Data format and citations

Each `.jsonl` file consists of **one valid JSON object per line**. Do **not** upload this entire file as one LLM prompt. Search the data first, return the relevant objects, and ask the model to cite `source_url`, `source_id`, and PDF page where applicable.

**Important:** O*NET job titles and task data refer to U.S. occupations. BLS wages and growth are **U.S.-only forecasts** in USD and percent. The Pakistan Bureau of Statistics figures are historical **Pakistan** survey data. WEF projections are **global** and scenario-/survey-based. Anthropic exposure is **not** the likelihood an occupation will be automated or displaced.

The PBS 2024–25 report has an important methodology distinction: `7.1%` unemployment under the 19th ICLS approach versus `6.9%` under a comparable 13th ICLS series. Never silently interchange them. All source publication dates and units must be retained.

## Quick offline test

Run (Python 3, no third-party packages):

```bash
python scripts/search_knowledge.py "software developer"
python scripts/search_knowledge.py "Pakistan unemployment rate"
```

This keyword search is **a starting example**, not a production-scale semantic vector index. A later CareerQuest API route can use the same JSONL records in a better-ranked retrieval function.

## GitHub upload (Sinarchon)

1. Extract the delivered ZIP on your computer.
2. Sign into the Sinarchon account and open `Sinarchon/CareerQuest-Chatbot`.
3. Choose **Add file → Upload files** and drag the extracted `data`, `metadata`, and `scripts` directories, plus `README.md`, into the upload page. If your browser won't accept directories, drag their files while preserving the intended paths, or use GitHub Desktop.
4. Commit the upload. Do **not** upload the original downloaded PDF bundle, API keys, `.env` files or earlier broken Google File Search scripts.

## Source licenses and attribution

### O*NET 31.0 database

Contains information derived from the **O*NET 31.0 Database** by the U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). Used under the [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/). O*NET® is a trademark of USDOL/ETA. CareerQuest has modified the source database into compact occupation records, sorted attributes and merged BLS fields. USDOL/ETA has not approved, endorsed or tested these modifications. [Source / official database license](https://www.onetcenter.org/license_db.html).

### Other publishers

- **BLS:** U.S. Bureau of Labor Statistics. The workbook's Table 1.2 describes employment in 2025 and projections for 2035. [Official employment-projections page](https://www.bls.gov/emp/data.htm).
- **PBS:** Pakistan Bureau of Statistics, Labour Force Survey 2024–25, official research tables. Only short factual extracts and attribution are included; full reports are not republished. [Source](https://www.pbs.gov.pk/labour-force-statistics/).
- **WEF:** World Economic Forum, *Future of Jobs Report 2025*. The PDF expressly restricts reproduction; only short independent factual summaries and links are included. [Source](https://www.weforum.org/reports/the-future-of-jobs-report-2025/).
- **Anthropic:** Anthropic Economic Index dataset; Hugging Face dataset card lists MIT license. These observational statistics do not establish automation risk. [Source](https://huggingface.co/datasets/Anthropic/EconomicIndex).

Please check each publisher's terms before distributing updated, expanded, or modified datasets commercially.

## Project integration

For a Vercel-hosted frontend, keep the knowledge database on the **server side**, not embedded in the client JavaScript bundle. If using a Git submodule, Vercel can fetch a **public HTTPS submodule** at build time. A submodule reference is pinned to a commit; updates in the knowledge repository require updating the pointer in the main app repository. Do not expose API keys.
