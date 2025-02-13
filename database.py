import psycopg2
from config import DATABASE_URL

# connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    file_id TEXT UNIQUE,
    file_name TEXT,
    category TEXT,  -- Books, Notes, Questions, etc.
    course_code TEXT, 
    keywords TEXT
)
""")
conn.commit()

# cave file metadata
def save_file(file_id, file_name, category, course_code, keywords):
    try:
        cursor.execute("""
            INSERT INTO files (file_id, file_name, category, course_code, keywords)
            VALUES (%s, %s, %s, %s, %s)
        """, (file_id, file_name, category, course_code, keywords))
        conn.commit()
        return True
    except psycopg2.IntegrityError:
        return False

# get files by category & course code
def get_files_by_course(category, course_code):
    cursor.execute("SELECT file_name, file_id FROM files WHERE category=%s AND course_code=%s", (category, course_code))
    return cursor.fetchall()

# get all files by course, grouped by category
def get_all_files_by_course(course_code):
    cursor.execute("SELECT category, file_name, file_id FROM files WHERE course_code=%s ORDER BY category", (course_code,))
    files = cursor.fetchall()
    
    # Group files by category
    categorized_files = {}
    for category, file_name, file_id in files:
        if category not in categorized_files:
            categorized_files[category] = []
        categorized_files[category].append((file_name, file_id))

    return categorized_files

# search files by keyword
def search_files(keyword):
    cursor.execute("SELECT file_name, file_id FROM files WHERE keywords ILIKE %s OR file_name ILIKE %s",
                   (f"%{keyword}%", f"%{keyword}%"))
    return cursor.fetchall()

# delete a file
def delete_file(file_name):
    cursor.execute("DELETE FROM files WHERE file_name=%s", (file_name,))
    conn.commit()
