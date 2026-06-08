# 🔍 Automated GitHub Metrics ETL Pipeline

> An enterprise-grade, end-to-end data pipeline that extracts, transforms, and loads real-time open-source software development metrics from the **GitHub REST API** into a relational **SQLite** database — served directly into an interactive **Power BI** analytical reporting layer.

---

## 📌 Project Overview

This project implements a fully automated **Open-Source Intelligence (OSINT)** data pipeline targeting the GitHub public REST API. It overcomes native platform constraints (1,000-record query caps, rate limiting) through custom **chronological query windowing** and programmatic **back-off strategies**, delivering clean, structured repository metrics ready for executive-level analysis.

The pipeline is designed around three core engineering principles:
- **Reliability** — automated pagination and rate-limit handling for uninterrupted data extraction
- **Scalability** — modular ETL architecture decoupled across extract, transform, and load phases
- **Insight** — a normalized relational schema feeding live Power BI dashboards for real-time decision-making

---

## 🛠️ Architecture & Data Flow

```
GitHub REST API  ──►  Python ETL Script  ──►  Pandas Transform  ──►  SQLite DB  ──►  Power BI Dashboard
      │                      │                        │                   │                   │
  Raw JSON              Windowed Query           Data Cleansing      Structured         Executive
  Payloads              + Rate-Limiting         + Normalization      Indexed Tables      Analytics
                        + Pagination            + Feature Eng.
```

### Phase Breakdown

| Phase | Component | Key Actions |
|---|---|---|
| **Extract** | `requests` + GitHub REST API | Dynamic chronological windowing (weekly intervals), back-off delays (`time.sleep`), pagination bypass |
| **Transform** | `Pandas` | Data cleansing, date normalization, null handling, categorical feature engineering (`popularity_tier`) |
| **Load** | `SQLite3` | Schema creation, staging, and committing records into clean, indexable relational tables |
| **Visualize** | Power BI | DAX measures, live relational DB connection, executive dashboards across 3 analytical perspectives |

---

## 📦 Repository Structure

```text
github-metrics-etl-pipeline/
│
├── data/                    # Raw JSON API sample payloads
│
├── docs/                    # Database schema details and data dictionary
│
├── files/                   # Production Python scripts, .csv exports, and .db files
│   └── etl_pipeline.py      # Core ETL execution script
│
├── screenshots/             # Power BI dashboard views and execution logs
│
└── README.md                # Project documentation
```

---

## ⚙️ Getting Started

### Prerequisites

Ensure the following Python packages are installed before execution:

```bash
pip install requests pandas
```

> SQLite3 is included in the Python standard library — no additional installation required.

### Execution

Run the core script to trigger the full extraction sequence and refresh the database:

```bash
python files/etl_pipeline.py
```

The script will:
1. Authenticate against the GitHub REST API
2. Execute windowed chronological queries across weekly date intervals
3. Transform and normalize raw JSON payloads via Pandas
4. Stage and commit clean records into the local SQLite database

---

## 🔧 Technical Deep-Dive

### API Extraction Strategy

The GitHub Search API enforces a hard **1,000-record result cap** per query. To overcome this, the pipeline implements a **chronological windowing** technique — splitting the extraction range into discrete **weekly time intervals** and issuing one targeted API query per window. This approach:

- Bypasses the native deep-paging barrier entirely
- Ensures full dataset coverage without record loss
- Respects platform rate limits via `time.sleep` back-off delays between requests

### Data Transformation Layer

Raw nested JSON responses are processed through a structured Pandas pipeline:

- **Date Normalization** — ISO 8601 timestamps parsed and standardized
- **Null Handling** — Missing fields imputed or flagged consistently across all records
- **Feature Engineering** — A custom `popularity_tier` categorical variable (Tiers 1, 2, 3) is computed based on star count thresholds, enabling segmented trend analysis

### Database Schema

Records are committed into a normalized SQLite schema optimized for analytical querying:

- **Repository table** — core metadata (name, language, stars, forks, creation date, popularity tier)
- Indexed columns on `language`, `popularity_tier`, and `created_at` for fast filter and aggregation operations

---

## 📊 Power BI Analytics Layer

The Power BI report connects **directly to the SQLite `.db` file**, bypassing flat-file (.csv) export limitations to enable live, relational data access.

The dashboard tracks engineering metrics across **three analytical perspectives**:

### 1. 📦 Volume & Scale
> *How is open-source activity distributed across language ecosystems?*

- Distinct count of trending repositories categorized by primary programming language framework
- Horizontal bar chart ranking languages by repository volume

### 2. 💡 Engagement Insights
> *Which projects reflect true community depth vs. viral hype?*

- Custom **DAX measure** computing the **Fork-to-Star Engagement Ratio**
  ```
  Engagement Ratio = DIVIDE([Total Forks], [Total Stars], 0)
  ```
- Surfaces projects with genuine contributor engagement beyond surface-level star counts

### 3. 🚀 Velocity & Growth
> *How fast are new projects gaining traction across popularity segments?*

- Distribution of project creation velocity segmented across engineered **Popularity Tiers (1, 2, 3)**
- Tracks the rate at which repositories move across tier thresholds over time

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Data Extraction | `requests`, GitHub REST API v3 |
| Data Transformation | `Pandas` |
| Data Storage | SQLite3 |
| Visualization | Microsoft Power BI |
| Key Techniques | API Pagination, Query Windowing, Rate-Limit Handling, DAX |

---

## 🏗️ Key Engineering Decisions

- **Query Windowing over Pagination** — Windowed date-range queries solve the hard 1,000-record API cap more reliably than cursor-based pagination, which breaks at deep offsets
- **SQLite over Flat Files** — Relational storage enables JOIN-capable queries, indexed lookups, and a direct live Power BI connection — removing manual CSV refresh cycles
- **Feature Engineering at Transform Time** — Computing `popularity_tier` during the transform phase keeps the load layer clean and the database immediately query-ready without post-load processing

---

## 📸 Screenshots

> Power BI dashboard views and Python execution logs are available in the [`/screenshots`](./screenshots/) directory.

---

## 👤 Author

**Vivek**
- GitHub: [@imviveksng](https://github.com/imviveksng)
- Project: [github-metrics-etl-pipeline](https://github.com/imviveksng/github-metrics-etl-pipeline)

---

## 📄 License

This project is open-source and available under the [MIT License](./LICENSE).
