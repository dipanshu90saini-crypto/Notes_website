import sqlite3

DB_NAME = "notes.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_no INTEGER NOT NULL,
            subject TEXT NOT NULL,
            chapter TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chapter_extras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_no INTEGER NOT NULL,
            subject TEXT NOT NULL,
            chapter_no INTEGER NOT NULL,
            important_points TEXT,
            examples TEXT,
            practice_questions TEXT
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database ready!")
