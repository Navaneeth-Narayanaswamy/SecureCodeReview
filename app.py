import sqlite3
from flask import Flask, request

app = Flask(__name__)


def get_db():
    return sqlite3.connect("users.db")


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    existing_users = db.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    if existing_users == 0:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", "Admin123")
        )

        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("student", "Student123")
        )

    db.commit()
    db.close()


@app.route("/")
def home():
    return """
    <h1>Secure Code Review Project</h1>
    <p>Sample 1 - Login System</p>
    <a href="/login">Go to Login</a>
    """


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db()

        # VULNERABLE: direct concatenation of user input
        query = (
            "SELECT username FROM users "
            "WHERE username = '" + username +
            "' AND password = '" + password + "'"
        )

        user = db.execute(query).fetchone()

        db.close()

        if user:
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


if __name__ == "__main__":
    init_db()
    app.run(debug=True)