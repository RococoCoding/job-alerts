import sqlite3

# Connect to the SQLite database (creates a new one if not exists)
conn = sqlite3.connect('database/jobs.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Define a migration to create the jobs table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        CONSTRAINT unique_job_company UNIQUE (title, company)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
