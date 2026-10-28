import sqlite3
from flask import Flask, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def get_db():
    return sqlite3.connect("users_fixed.db")

def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    existing_users = db.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    if existing_users == 0:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("admin", generate_password_hash("Admin123"))
        )

        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            ("student", generate_password_hash("Student123"))
        )

    db.commit()
    db.close()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        user = db.execute(
            "SELECT username, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        db.close()

        if user and check_password_hash(user[1], password):
            return "<h2>Login successful</h2>"

        return "<h2>Invalid username or password</h2>"

    return """
    <h1>Login</h1>
    <form method="POST">
        <label>Username:</label><br>
        <input type="text" name="username"><br><br>

        <label>Password:</label><br>
        <input type="password" name="password"><br><br>

        <button type="submit">Login</button>
    </form>

    <p>Test users:</p>
    <ul>
        <li>admin / Admin123</li>
        <li>student / Student123</li>
    </ul>
    """


@app.route("/")
def home():
    return """
    <h1>Secure Code Review Project</h1>
    <p>Sample 1 - Secure Login System</p>
    <a href="/login">Go to Login</a>
    """


if __name__ == "__main__":
    init_db()
    app.run(debug=False)