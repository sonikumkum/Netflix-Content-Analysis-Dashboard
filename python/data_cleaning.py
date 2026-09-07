import pandas as pd
import mysql.connector

# ==========================================
# 1. LOAD NETFLIX DATASET
# ==========================================

df = pd.read_csv("../dataset/netflix_titles.csv/netflix_titles.csv")

print("Original Shape:", df.shape)

# ==========================================
# 2. CHECK MISSING VALUES
# ==========================================

print("\nMissing Values:")
print(df.isnull().sum())

# ==========================================
# 3. REMOVE DUPLICATES
# ==========================================

df.drop_duplicates(inplace=True)

# ==========================================
# 4. CONVERT DATE COLUMN
# ==========================================

df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

# ==========================================
# 5. FILL MISSING VALUES
# ==========================================

df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Unknown")

# ==========================================
# 6. CREATE YEAR AND MONTH COLUMNS
# ==========================================

df["added_year"] = df["date_added"].dt.year
df["added_month"] = df["date_added"].dt.month

# ==========================================
# 7. SAVE CLEANED DATASET
# ==========================================

df.to_csv(
    "../dataset/netflix_titles_cleaned.csv",
    index=False
)

print("\nCleaned Shape:", df.shape)
print("\nCleaning completed successfully!")

# ==========================================
# 8. CONNECT TO MYSQL
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="netflix_analysis"
)

cursor = conn.cursor()

print("\nConnected to MySQL successfully!")

# ==========================================
# 9. REMOVE OLD DATA
# ==========================================

cursor.execute("TRUNCATE TABLE netflix_titles")

print("Old table data cleared!")

# ==========================================
# 10. PREPARE DATA FOR MYSQL
# ==========================================

df = df.where(pd.notnull(df), None)

insert_query = """
INSERT INTO netflix_titles
(
    show_id,
    type,
    title,
    director,
    cast,
    country,
    date_added,
    release_year,
    rating,
    duration,
    listed_in,
    description,
    added_year,
    added_month
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s
)
"""

# ==========================================
# 11. INSERT ALL RECORDS
# ==========================================

data = list(df.itertuples(index=False, name=None))

cursor.executemany(insert_query, data)

conn.commit()

print("Rows inserted:", len(data))

# ==========================================
# 12. VERIFY RECORD COUNT
# ==========================================

cursor.execute(
    "SELECT COUNT(*) FROM netflix_titles"
)

total_records = cursor.fetchone()[0]

print("Total records in MySQL:", total_records)

# ==========================================
# 13. CLOSE CONNECTION
# ==========================================

cursor.close()
conn.close()

print("\nMySQL import completed successfully!")