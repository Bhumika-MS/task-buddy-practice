import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = "tasks.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL
            )
        """)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task = request.form.get("task", "").strip()

        if task:
            with sqlite3.connect(DATABASE) as conn:
                conn.execute(
                    "INSERT INTO tasks (title) VALUES (?)",
                    (task,)
                )

        return redirect(url_for("home"))

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

    return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)