import sqlite3


def drop_all_entries():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    # Drop all entries in the jobs table
    cursor.execute('''
        DELETE FROM jobs
    ''')

    conn.commit()
    conn.close()


drop_all_entries()