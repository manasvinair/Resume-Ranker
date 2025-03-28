import sqlite3

def create_database():
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (            
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filename TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def storeResume(user_id,filename, text):
    conn = sqlite3.connect("resume.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resumes (user_id, filename, text) VALUES (?, ?, ?)",(user_id, filename, text))
    conn.commit()
    conn.close()

# Initialize database on first run
create_database()
