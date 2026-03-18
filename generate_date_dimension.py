import pandas as pd
import pymysql

# -------------------------------
# 1. Connect to MySQL
# -------------------------------
connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',                # or another admin user
    passwd='7386163908',      # ← your actual password, as a string
    db='retail_dss0',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()

# -------------------------------
# 2. Generate the Dates DataFrame
# -------------------------------
start_date = pd.to_datetime('1990-01-01')
end_date   = pd.to_datetime('2100-01-01')
all_dates  = pd.date_range(start=start_date, end=end_date, freq='D')

df = pd.DataFrame({
    'Dates':       all_dates,
    'Day_name':    all_dates.day_name(),
    'Month_name':  all_dates.month_name(),
    'Year_name':   all_dates.year.astype(str)
})

# Create a sequential unique integer key
df['Date_key'] = range(1, len(df) + 1)

# -------------------------------
# 3. Drop & Create the dwh_date Table
# -------------------------------
cursor.execute("DROP TABLE IF EXISTS dwh_date;")
cursor.execute("""
CREATE TABLE dwh_date (
    Date_key    INT         NOT NULL PRIMARY KEY,
    Dates       DATE        NOT NULL,
    Day_name    VARCHAR(20) NOT NULL,
    Month_name  VARCHAR(20) NOT NULL,
    Year_name   VARCHAR(10) NOT NULL
) ENGINE=InnoDB;
""")

# -------------------------------
# 4. Insert All Rows Efficiently
# -------------------------------
# Prepare list of tuples in the correct order
records = list(zip(
    df['Date_key'],
    df['Dates'].dt.strftime('%Y-%m-%d'),
    df['Day_name'],
    df['Month_name'],
    df['Year_name']
))

insert_sql = """
INSERT INTO dwh_date
  (Date_key, Dates, Day_name, Month_name, Year_name)
VALUES (%s, %s, %s, %s, %s)
"""

# Execute all inserts in one batch
cursor.executemany(insert_sql, records)
connection.commit()

# -------------------------------
# 5. Cleanup & Confirmation
# -------------------------------
cursor.close()
connection.close()

print(f"Inserted {len(records)} rows into dwh_date successfully.")
