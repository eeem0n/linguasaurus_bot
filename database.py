import sqlite3
from config import DATABASE_FILE

# Connect to database
conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT UNIQUE,
    file_name TEXT,
    category TEXT,
    semester INTEGER
)
""")
conn.commit()


# Get files by category & semester
def get_files_by_category(category):
    cursor.execute("SELECT file_name FROM files WHERE category=?", (category,))
    return [row[0] for row in cursor.fetchall()]


# Save file with keywords
def save_file(file_id, file_name, category, semester, keywords):
    full_category = f"{category}_semester_{semester}"
    cursor.execute("INSERT INTO files (file_id, file_name, category, semester, keywords) VALUES (?, ?, ?, ?, ?)", 
                   (file_id, file_name, full_category, semester, keywords))
    conn.commit()

# Search files by keyword
def search_files(keyword):
    cursor.execute("SELECT file_name FROM files WHERE keywords LIKE ? OR file_name LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
    return [row[0] for row in cursor.fetchall()]

# Delete file (Admin-only)
def delete_file(file_name):
    cursor.execute("DELETE FROM files WHERE file_name=?", (file_name,))
    conn.commit()

# Test database
def test_database():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='files'")
    return cursor.fetchone() is not None

