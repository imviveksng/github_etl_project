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
