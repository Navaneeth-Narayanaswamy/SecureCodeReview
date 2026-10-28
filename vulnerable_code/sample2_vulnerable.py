from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = "sample2-secret-key"

comments = []

@app.route("/")
def home():
    return """
    <h1>Sample 2 - Comments and Profile</h1>
    <a href="/comments">Comments</a><br>
    <a href="/profile">Profile</a>
    """

@app.route("/comments", methods=["GET", "POST"])
def comments_page():
    if request.method == "POST":
        comment = request.form["comment"]
        comments.append(comment)
        return redirect(url_for("comments_page"))

    page = """
    <h1>Comments</h1>

    <form method="POST">
        <label>Comment:</label><br>
        <textarea name="comment"></textarea><br><br>
        <button type="submit">Post Comment</button>
    </form>

    <h2>Comments</h2>

    {% for comment in comments %}
        <div>{{ comment|safe }}</div>
        <hr>
    {% endfor %}

    <a href="/">Home</a>
    """

    return render_template_string(page, comments=comments)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "email" not in session:
        session["email"] = "student@example.com"

    if request.method == "POST":
        session["email"] = request.form["email"]
        return "<h2>Email updated successfully</h2>"

    return """
    <h1>Profile</h1>

    <p>Current email: {}</p>

    <form method="POST" action="/profile">
        <label>New email:</label><br>
        <input type="email" name="email"><br><br>
        <button type="submit">Update Email</button>
    </form>

    <a href="/">Home</a>
    """.format(session["email"])


if __name__ == "__main__":
    app.run(debug=True, port=5000)