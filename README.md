# Automated Open-Source Intelligence Tool (API-to-SQL ETL Pipeline) 🚀

An enterprise-grade data pipeline that extracts, transforms, and stores real-time software development metrics from the GitHub REST API into a relational SQLite database, featuring an connected live reporting layer in Power BI.

---

## 🛠️ Architecture & Data Flow

1. **Extract**: Queries the GitHub API utilizing dynamic chronological windowing (weekly intervals) to bypass the native 1,000-record query threshold, using programmatic back-off delays (`time.sleep`) to strictly adhere to platform rate limits.
2. **Transform**: Leverages `Pandas` for data cleansing, automated date normalization, handling null fields, and feature engineering categorical data (`popularity_tier`).
3. **Load**: Establishes a connection to a local SQLite relational database instance, staging and committing structured records into clean, indexable tables.
4. **Visualize**: Bypasses traditional flat file constraints by serving relational database tables directly into an executive Power BI analytical layer.

---

## 📦 Repository Structure

```text
├── data/           # Raw JSON API sample payloads
├── docs/           # Database schema details and data dictionary
├── files/          # Production Python scripts, .csv, and .db files
├── screenshots/    # Power BI Dashboard views and execution logs
└── README.md       # Project documentation
🚀 Getting Started
Prerequisites
Bash
pip install requests pandas
Execution
Run the core script to trigger the extraction sequence and refresh the database:

Bash
python files/etl_pipeline.py
📊 Analytics Deep-Dive (Power BI Layer)
The dashboard connected to this pipeline tracks engineering metrics via three specific core perspectives:

Volume & Scale: Distinct count of trending repositories categorized by primary language framework.

Engagement Insights: Custom DAX measures tracking the Fork-to-Star Engagement Ratio to calculate true project depth over pure viral hype.

Velocity: Distribution of project creation velocity across engineered popularity tiers (Tiers 1, 2, and 3).


---

## 🔄 Step 3: Update Your Main Profile README

To feature this on your main GitHub profile layout (`imviveksng`), copy and paste this new project block directly underneath your **Featured Projects** section:

```markdown
### ⚙️ [Automated GitHub Metrics ETL Pipeline](https://github.com/imviveksng/github-metrics-etl-pipeline)
End-to-end Python pipeline extracting live open-source metrics using the GitHub REST API.  
Bypassed strict API deep-paging barriers via custom **query windowing blocks** and loaded clean records directly into an **SQLite relational database** connected directly to an analytical Power BI report.  
`Python` `Pandas` `REST API` `SQLite` `Power BI` `Data Engineering`
