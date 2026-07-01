from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database
def create_database():
    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    issue TEXT,
    description TEXT,
    map_link TEXT,
    status TEXT
)
""")

    conn.commit()
    conn.close()

create_database()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Report Page
@app.route("/report")
def report():
    return render_template("report.html")


# Submit Complaint
@app.route("/submit", methods=["POST"])
def submit():

    name = request.form["name"]
    location = request.form["location"]
    issue = request.form["issue"]
    description = request.form["description"]
    map_link = request.form["map_link"]

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO complaints
    (name, location, issue, description, map_link, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        location,
        issue,
        description,
        map_link,
        "Pending"
    ))

    conn.commit()
    conn.close()

    return redirect("/")
# Admin Dashboard
@app.route("/admin")
def admin():

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()

    conn.close()

    return render_template("admin.html", complaints=complaints)
@app.route("/resolve/<int:id>")
def resolve(id):

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE complaints SET status=? WHERE id=?",
        ("Resolved", id)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)