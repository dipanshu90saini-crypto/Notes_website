from flask import Flask, render_template, request

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
            "content": "Number Systems ke important notes yahan likhe jayenge."
        },
        2: {
            "title": "Polynomials",
            "content": "Polynomials ke important notes yahan likhe jayenge."
        },
        3: {
            "title": "Coordinate Geometry",
            "content": "Coordinate Geometry ke important notes yahan likhe jayenge."
        }
    }
}


@app.route("/")
def home():
    classes = [9, 10, 11, 12]
    return render_template("index.html", classes=classes)


@app.route("/class/<int:class_no>")
def subjects(class_no):
    return render_template(
        "subjects.html",
        class_no=class_no,
        subjects=subjects_data.get(class_no, [])
    )


@app.route("/class/<int:class_no>/subject/<subject>")
def chapters(class_no, subject):
    chapters = chapters_data.get(subject, [])

    return render_template(
        "chapters.html",
        class_no=class_no,
        subject=subject,
        chapters=chapters
    )


@app.route("/class/<int:class_no>/subject/<subject>/chapter/<int:chapter_no>")
def notes(class_no, subject, chapter_no):

    subject_notes = notes_data.get(subject, {})
    note = subject_notes.get(chapter_no)

    if note is None:
        return "Notes abhi available nahi hain."

    return render_template(
        "notes.html",
        class_no=class_no,
        subject=subject,
        note=note
    )


if __name__ == "__main__":
    app.run(debug=True)
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
