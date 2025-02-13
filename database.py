import psycopg2
from config import DATABASE_URL

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

#  Create the table if it doesn’t exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    file_id TEXT UNIQUE,
    file_name TEXT,
    course_code TEXT,
    category TEXT,
    keywords TEXT
)
""")
conn.commit()

#  Save file metadata
def save_file(file_id, file_name, course_code, category, keywords):
    try:
        cursor.execute("""
            INSERT INTO files (file_id, file_name, course_code, category, keywords)
            VALUES (%s, %s, %s, %s, %s)
        """, (file_id, file_name, course_code, category, keywords))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        return False

#  Get files by course code & category (books, notes, etc.)
def get_files_by_course(course_code, category):
    cursor.execute("SELECT file_name, file_id FROM files WHERE course_code=%s AND category=%s", (course_code, category))
    return cursor.fetchall()

# Search files by keyword
def search_files(keyword):
    cursor.execute("SELECT file_name, file_id FROM files WHERE keywords ILIKE %s OR file_name ILIKE %s",
                   (f"%{keyword}%", f"%{keyword}%"))
    return cursor.fetchall()

#  Delete a file
def delete_file(file_name):
    cursor.execute("DELETE FROM files WHERE file_name=%s", (file_name,))
    conn.commit()
