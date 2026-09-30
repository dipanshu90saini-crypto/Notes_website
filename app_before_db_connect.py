from flask import Flask, render_template, request
from database import get_db

app = Flask(__name__)

subjects_data = {
    9: ["Maths", "Science", "English", "Hindi", "Social Science"],
    10: ["Maths", "Science", "English", "Hindi", "Social Science"],
    11: ["Physics", "Chemistry", "Maths", "Biology", "English"],
    12: ["Physics", "Chemistry", "Maths", "Biology", "English"]
}

chapters_data = {
    "Maths": [
        "Chapter 1 - Number Systems",
        "Chapter 2 - Polynomials",
        "Chapter 3 - Coordinate Geometry"
    ],
    "Science": [
        "Chapter 1 - Matter in Our Surroundings",
        "Chapter 2 - Is Matter Around Us Pure?",
        "Chapter 3 - Atoms and Molecules"
    ],
    "English": [
        "Chapter 1 - Reading",
        "Chapter 2 - Writing",
        "Chapter 3 - Literature"
    ]
}

notes_data = {
    "Maths": {
        1: {
            "title": "Number Systems",
            "content": "Number Systems ke important notes yahan hain."
        },
        2: {
            "title": "Polynomials",
            "content": "Polynomials ke important notes yahan hain."
        },
        3: {
            "title": "Coordinate Geometry",
            "content": "Coordinate Geometry ke important notes yahan hain."
        }
    }
}


@app.route("/")
def home():
    return render_template("index.html", classes=[9, 10, 11, 12])


@app.route("/class/<int:class_no>")
def subjects(class_no):
    return render_template(
        "subjects.html",
        class_no=class_no,
        subjects=subjects_data.get(class_no, [])
    )


@app.route("/class/<int:class_no>/subject/<subject>")
def chapters(class_no, subject):
    return render_template(
        "chapters.html",
        class_no=class_no,
        subject=subject,
        chapters=chapters_data.get(subject, [])
    )


@app.route("/class/<int:class_no>/subject/<subject>/chapter/<int:chapter_no>")
def notes(class_no, subject, chapter_no):
    note = notes_data.get(subject, {}).get(chapter_no)

    if note is None:
        return "Notes abhi available nahi hain."

    return render_template(
        "notes.html",
        class_no=class_no,
        subject=subject,
        note=note
    )


@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()
    results = []

    for class_no, subjects in subjects_data.items():
        for subject in subjects:

            if query in subject.lower():
                results.append({
                    "class_no": class_no,
                    "subject": subject,
                    "chapter": None
                })

            for chapter in chapters_data.get(subject, []):
                if query in chapter.lower():
                    results.append({
                        "class_no": class_no,
                        "subject": subject,
                        "chapter": chapter
                    })

    return render_template(
        "search.html",
        query=query,
        results=results
    )


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
        (class_no, subject, chapter, title, content)
    )

    conn.commit()
    conn.close()

    return "Note successfully added! <br><br><a href='/admin'>Add another note</a>"


if __name__ == "__main__":
    app.run(debug=True)
