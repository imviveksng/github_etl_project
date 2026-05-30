import requests
import pandas as pd
import sqlite3
from datetime import datetime
import json

# ==========================================
# 1. EXTRACT STAGE
# ==========================================
def extract_github_data():
    print("--- Starting Extraction Stage ---")
    url = "https://api.github.com/search/repositories"
    
    all_items = []
    
    # Loop through 5 pages (5 pages x 100 items per page = 500 rows)
    for page in range(1, 6): 
        print(f"Fetching page {page} of data...")
        params = {
            "q": "language:python created:>2026-01-01",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,  # Always set to GitHub's maximum allowed limit
            "page": page      # Dynamically asks for page 1, then page 2, etc.
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            with open("data/github_raw_sample.json", "w", encoding="utf-8") as f:
             json.dump(data, f, indent=4)
            print("Raw JSON response successfully saved to data/github_raw_sample.json")
            
            items = data.get('items', [])
            if not items:
                print("No more data available.")
                break # Stop looping if we run out of records
                
            all_items.extend(items)
            
        except Exception as e:
            print(f"Error during extraction on page {page}: {e}")
            break
            
    print(f"Successfully extracted a total of {len(all_items)} repositories from GitHub API.")
    return all_items

# ==========================================
# 2. TRANSFORM STAGE
# ==========================================
def transform_data(raw_items):
    print("\n--- Starting Transformation Stage ---")
    if not raw_items:
        print("No data to transform.")
        return pd.DataFrame()
    
    extracted_records = []
    for repo in raw_items:
        extracted_records.append({
            "repo_id": repo['id'],
            "repo_name": repo['name'],
            "owner": repo['owner']['login'],
            "stars": repo['stargazers_count'],
            "forks": repo['forks_count'],
            "primary_language": repo['language'],
            "description": repo['description'],
            "created_at_raw": repo['created_at'],
            "url": repo['html_url']
        })
    
    # Load into DataFrame
    df = pd.DataFrame(extracted_records)
    
    # Transformation A: Clean missing values in description
    df['description'] = df['description'].fillna("No description provided")
    
    # Transformation B: Convert raw timestamp to standard YYYY-MM-DD Date format
    df['created_date'] = pd.to_datetime(df['created_at_raw']).dt.date
    df.drop(columns=['created_at_raw'], inplace=True)
    
    # Transformation C: Feature Engineering - Categorize repos by popularity tier
    def categorize_popularity(stars):
        if stars > 10000: return 'Tier 1 (Viral)'
        elif stars > 1000: return 'Tier 2 (High Growth)'
        else: return 'Tier 3 (Trending)'
        
    df['popularity_tier'] = df['stars'].apply(categorize_popularity)
    
    # Transformation D: Add a metadata column showing when this ETL job ran
    df['extracted_at_dt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"Transformation complete. Cleaned data shape: {df.shape}")
    return df

# ==========================================
# 3. LOAD STAGE (To SQL Database)
# ==========================================
def load_data_to_sqlite(df, db_name="github_metrics.db"):
    print("\n--- Starting Loading Stage ---")
    if df.empty:
        print("No data to load.")
        return
    
    try:
        # Establish connection to local SQLite Database file
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create a structured table if it doesn't already exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trending_repositories (
                repo_id INTEGER PRIMARY KEY,
                repo_name TEXT,
                owner TEXT,
                stars INTEGER,
                forks INTEGER,
                primary_language TEXT,
                description TEXT,
                url TEXT,
                created_date TEXT,
                popularity_tier TEXT,
                extracted_at_dt TEXT
            )
        """)
        
        # Load the dataframe into the SQLite table (Append mode so data stacks daily)
        # We use a staging logic or replace mode here to ensure fresh data
        df.to_sql("trending_repositories", conn, if_exists="replace", index=False)
        
        conn.commit()
        print(f"Successfully loaded data into database '{db_name}' table 'trending_repositories'!")
        
        # Verify Row Count
        cursor.execute("SELECT COUNT(*) FROM trending_repositories")
        total_rows = cursor.fetchone()[0]
        print(f"Total verified rows now in the DB: {total_rows}")
        
        conn.close()
    except Exception as e:
        print(f"Error during loading to database: {e}")

# ==========================================
# MAIN EXECUTION PIPELINE
# ==========================================
if __name__ == "__main__":
    print("=== PIPELINE INITIALIZED ===")
    raw_data = extract_github_data()
    cleaned_df = transform_data(raw_data)
    load_data_to_sqlite(cleaned_df)
    cleaned_df.to_csv("github_metrics.csv", index=False)
    print("\n=== PIPELINE RUN COMPLETED SUCCESSFULLY ===")