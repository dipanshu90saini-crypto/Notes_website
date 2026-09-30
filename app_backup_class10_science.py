from flask import Flask, render_template, request
from database import get_db

app = Flask(__name__)


# =========================
# SUBJECTS
# =========================

subjects_data = {
    9: ["Maths", "Science", "English", "Hindi", "Social Science"],
    10: ["Maths", "Science", "English", "Hindi", "Social Science"],
    11: ["Physics", "Chemistry", "Maths", "Biology", "English"],
    12: ["Physics", "Chemistry", "Maths", "Biology", "English"]
}


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template(
        "index.html",
        classes=[9, 10, 11, 12]
    )


# =========================
# CLASS → SUBJECTS
# =========================

@app.route("/class/<int:class_no>")
def subjects(class_no):

    subjects = subjects_data.get(class_no)

    if subjects is None:
        return "Invalid class", 404

    return render_template(
        "subjects.html",
        class_no=class_no,
        subjects=subjects
    )


# =========================
# SUBJECT → CHAPTERS
# =========================

@app.route("/class/<int:class_no>/subject/<subject>")
def subject(class_no, subject):

    conn = get_db()

    chapters = conn.execute(
        """
        SELECT DISTINCT chapter
        FROM notes
        WHERE class_no = ?
        AND subject = ?
        ORDER BY id ASC
        """,
        (class_no, subject)
    ).fetchall()

    conn.close()

    return render_template(
        "chapters.html",
        class_no=class_no,
        subject=subject,
        chapters=chapters
    )


# =========================
# CHAPTER → NOTES
# =========================
@app.route("/class/<int:class_no>/subject/<subject>/chapter/<int:chapter_no>")
def notes(class_no, subject, chapter_no):

    conn = get_db()

    note = conn.execute(
        """
        SELECT title, content
        FROM notes
        WHERE class_no = ?
        AND subject = ?
        AND chapter LIKE ?
        ORDER BY id ASC
        LIMIT 1
        """,
        (
            class_no,
            subject,
            f"Chapter {chapter_no}%"
        )
    ).fetchone()

    extras = conn.execute(
        """
        SELECT important_points, examples, practice_questions
        FROM chapter_extras
        WHERE class_no = ?
        AND subject = ?
        AND chapter_no = ?
        LIMIT 1
        """,
        (
            class_no,
            subject,
            chapter_no
        )
    ).fetchone()

    conn.close()

    if note is None:
        return "Is chapter ke notes abhi available nahi hain."

    return render_template(
        "notes.html",
        class_no=class_no,
        subject=subject,
        note=note,
        extras=extras
    )


# =========================
# SEARCH
# =========================
# =========================
@app.route("/search")
def search():

    query = request.args.get("q", "").strip()

    results = []

    if query:

        conn = get_db()

        results = conn.execute(
            """
            SELECT id, class_no, subject, chapter, title
            FROM notes
            WHERE title LIKE ?
            OR chapter LIKE ?
            OR subject LIKE ?
            ORDER BY class_no ASC, id ASC
            """,
            (
                f"%{query}%",
                f"%{query}%",
                f"%{query}%"
            )
        ).fetchall()

        conn.close()

    return render_template(
        "search.html",
        query=query,
        results=results
    )


# =========================
# DATABASE NOTES
# =========================

@app.route("/database-notes")
def database_notes():

    conn = get_db()

    notes = conn.execute(
        "SELECT * FROM notes ORDER BY class_no, id"
    ).fetchall()

    conn.close()

    return render_template(
        "database_notes.html",
        notes=notes
    )


# =========================
# ADMIN
# =========================

@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/admin/add", methods=["POST"])
def admin_add():

    class_no = request.form["class_no"]
    subject = request.form["subject"]
    chapter = request.form["chapter"]
    title = request.form["title"]
    content = request.form["content"]

    conn = get_db()

    conn.execute(
        """
        INSERT INTO notes
        (class_no, subject, chapter, title, content)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            class_no,
            subject,
            chapter,
            title,
            content
        )
    )

    conn.commit()
    conn.close()

    return """
    Note successfully added!
    <br><br>
    <a href="/admin">Add another note</a>
    """


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)
