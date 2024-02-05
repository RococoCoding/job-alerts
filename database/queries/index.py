def insert_job(conn, title, company):
    cursor = conn.cursor()

    # Insert job into the jobs table
    cursor.execute('''
        INSERT INTO jobs (title, company) VALUES (?, ?)
    ''', (title, company))

    conn.commit()


def query_jobs_by_title_and_company(conn, title, company):
    cursor = conn.cursor()

    # Query jobs by job_title and company
    cursor.execute('''
        SELECT * FROM jobs WHERE title = ? AND company = ?
    ''', (title, company))

    jobs = cursor.fetchall()

    return jobs
