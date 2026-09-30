from database import get_db

conn = get_db()

conn.execute("""
    INSERT INTO notes
    (class_no, subject, chapter, title, content)
    VALUES (?, ?, ?, ?, ?)
""", (
    9,
    "Maths",
    "Chapter 1 - Number Systems",
    "Number Systems",
    "Number Systems ke important notes yahan hain."
))

conn.commit()
conn.close()

print("Note successfully added!")
