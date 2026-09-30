import sqlite3

conn = sqlite3.connect("notes.db")

conn.execute("""
INSERT INTO chapter_extras
(class_no, subject, chapter_no, important_points, examples, practice_questions)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    9,
    "Maths",
    1,
    """• Rational numbers ko p/q form mein likha ja sakta hai.
• Irrational numbers p/q form mein nahi likhe ja sakte.
• Rational aur irrational numbers milkar real numbers banate hain.
• Har integer ek rational number hota hai.""",

    """Example 1: 1/2 = 0.5
Example 2: 1/3 = 0.333...
Example 3: √2 ek irrational number hai.""",

    """1. Rational number ki definition likho.
2. √3 rational hai ya irrational?
3. 5 ko p/q form mein likho.
4. Rational aur irrational numbers mein difference batao."""
))

conn.commit()
conn.close()

print("Chapter 1 data added!")
