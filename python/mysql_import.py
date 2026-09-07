import pandas as pd
import mysql.connector

# ==========================================
# 1. LOAD CLEANED DATASET
# ==========================================

df = pd.read_csv("../dataset/netflix_titles_cleaned.csv")

print("Cleaned dataset loaded!")
print("Total rows:", len(df))

# Replace NaN values with None
df = df.where(pd.notnull(df), None)

# ==========================================
# 2. CONNECT TO MYSQL
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="netflix_analysis"
)

cursor = conn.cursor()

print("Connected to MySQL successfully!")

# ==========================================
# 3. CLEAR OLD DATA
# ==========================================

cursor.execute("TRUNCATE TABLE netflix_titles")

print("Old data cleared!")

# ==========================================
# 4. INSERT DATA
# ==========================================

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

data = list(df.itertuples(index=False, name=None))

cursor.executemany(insert_query, data)

conn.commit()

print("Rows inserted:", len(data))

# ==========================================
# 5. VERIFY DATA
# ==========================================

cursor.execute("SELECT COUNT(*) FROM netflix_titles")

total_records = cursor.fetchone()[0]

print("Total records in MySQL:", total_records)

# ==========================================
# 6. CLOSE CONNECTION
# ==========================================

cursor.close()
conn.close()

print("MySQL import completed successfully!")