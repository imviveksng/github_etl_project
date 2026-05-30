# Data Dictionary: trending_repositories

**Target Table Name:** `trending_repositories`  
**Database Engine:** SQLite / Flat CSV Target  
**Pipeline Source:** GitHub REST API v3 (Search Repositories Endpoint)  
**Last Updated Documentation:** May 2026

---

## 📊 Schema Overview

| Column Name | Data Type (SQL) | Pandas Dtype | Source Type | Description |
| :--- | :--- | :--- | :--- | :--- |
| **repo_id** | INTEGER | int64 | Raw API | Unique identification key provided by GitHub for the repository (Primary Key). |
| **repo_name** | TEXT | object | Raw API | The public name of the repository. |
| **owner** | TEXT | object | Raw API | The GitHub username/organization handle of the repository creator. |
| **stars** | INTEGER | int64 | Raw API | The total count of stargazers (`stargazers_count`) at the time of extraction. |
| **forks** | INTEGER | int64 | Raw API | The total count of project forks (`forks_count`) at the time of extraction. |
| **primary_language** | TEXT | object | Raw API | The dominant programming language framework detected (Filtered to 'Python'). |
| **description** | TEXT | object | Transformed | Short description of the project. Imputed during transformation if missing. |
| **url** | TEXT | object | Raw API | Direct hyperlink to the GitHub repository web page. |
| **created_date** | TEXT | object | Engineered | Normalized calendar date when the repository was created. |
| **popularity_tier** | TEXT | object | Engineered | Categorical classification tracking market velocity and project scale. |
| **extracted_at_dt** | TEXT | object | Metadata | System execution timestamp mapping exactly when the ETL run occurred. |

---

## ⚙️ Transformation & Feature Engineering Business Logic

This section details the transformation logic applied using the `Pandas` processing layer before staging the data into production.

### 1. Column Imputation (`description`)
* **Logic:** The raw API payload occasionally passes a null value (`None`) if the repository developer leaves the description blank. To prevent downstream BI indexing issues or empty dashboard cells, missing entries are filled.
* **Python Expression:** ```python
  df['description'] = df['description'].fillna("No description provided")
2. Date Normalization (created_date)
Logic: The API outputs an ISO 8601 string combined timestamp (e.g., 2026-04-05T14:22:01Z). To optimize query filtering and support clean chronological relationships in BI data modeling, this is stripped down to a basic YYYY-MM-DD standard date entity.

Python Expression:

Python
df['created_date'] = pd.to_datetime(df['created_at_raw']).dt.date
3. Categorical Feature Engineering (popularity_tier)
Logic: A segmentation rule designed to separate viral, high-growth, and baseline trending repositories based on cumulative developer stars. This classification reduces visual data clutter in dashboard reporting slabs.

Conditional Rules Matrix:

Tier 1 (Viral): Stars > 10,000

Tier 2 (High Growth): Stars > 1,000 and <= 10,000

Tier 3 (Trending): Stars <= 1,000

Python Implementation:

Python
def categorize_popularity(stars):
    if stars > 10000: 
        return 'Tier 1 (Viral)'
    elif stars > 1000: 
        return 'Tier 2 (High Growth)'
    else: 
        return 'Tier 3 (Trending)'

df['popularity_tier'] = df['stars'].apply(categorize_popularity)
4. System Operational Metadata (extracted_at_dt)
Logic: Generates an extraction record timestamp captured from the system runtime clock (YYYY-MM-DD HH:MM:SS). This column enables historic delta comparisons and data tracking over time if the staging pattern changes from data replacement to chronological append sequences.

Python Expression:

Python
df['extracted_at_dt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
