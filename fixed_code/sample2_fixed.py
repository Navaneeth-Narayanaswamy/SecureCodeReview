import os
import secrets
import hmac

from flask import (
    Flask,
    request,
    session,
    redirect,
    url_for,
    render_template_string,
    abort
)

app = Flask(__name__)  # NOSONAR - CSRF protection is implemented using a validated session token

# Secure secret key loaded from an environment variable
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY environment variable is not set.")

# Secure session-cookie configuration
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False
)

comments = []


def get_csrf_token():
    """Create a CSRF token for the current session."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)

    return session["csrf_token"]


def validate_csrf_token():
    """Validate the CSRF token submitted with a POST request."""
    submitted_token = request.form.get("csrf_token", "")
    session_token = session.get("csrf_token", "")

    if not session_token or not submitted_token:
        abort(403, description="CSRF validation failed.")

    if not hmac.compare_digest(submitted_token, session_token):
        abort(403, description="CSRF validation failed.")


@app.after_request
def add_security_headers(response):
    """Add browser security controls to every response."""

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'"
    )

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


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

        # Validate CSRF token before processing the request
        validate_csrf_token()

        comment = request.form.get("comment", "").strip()

        # Basic server-side input validation
        if not comment:
            return "<h2>Comment cannot be empty.</h2>"

        if len(comment) > 500:
            return "<h2>Comment is too long.</h2>"

        # Store the validated comment
        comments.append(comment)

        return redirect(url_for("comments_page"))

    csrf_token = get_csrf_token()

    page = """
    <h1>Comments</h1>

    <form method="POST">

        <input type="hidden"
               name="csrf_token"
               value="{{ csrf_token }}">

        <label>Comment:</label><br>

        <textarea name="comment"
                  maxlength="500"
                  required></textarea>

        <br><br>

        <button type="submit">Post Comment</button>

    </form>

    <h2>Comments</h2>

    {% for comment in comments %}

        <div>{{ comment|e }}</div>

        <hr>

    {% endfor %}

    <a href="/">Home</a>
    """

    return render_template_string(
        page,
        comments=comments,
        csrf_token=csrf_token
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "email" not in session:
        session["email"] = "student@example.com"

    if request.method == "POST":

        # Validate CSRF token before changing profile data
        validate_csrf_token()

        email = request.form.get("email", "").strip()

        # Basic server-side validation
        if not email or len(email) > 254 or "@" not in email:
            return "<h2>Invalid email address.</h2>"

        session["email"] = email

        return "<h2>Email updated successfully</h2>"

    csrf_token = get_csrf_token()

    page = """
    <h1>Profile</h1>

    <p>Current email: {{ email|e }}</p>

    <form method="POST" action="/profile">

        <input type="hidden"
               name="csrf_token"
               value="{{ csrf_token }}">

        <label>New email:</label><br>

        <input type="email"
               name="email"
               maxlength="254"
               required>

        <br><br>

        <button type="submit">Update Email</button>

    </form>

    <a href="/">Home</a>
    """

    return render_template_string(
        page,
        email=session["email"],
        csrf_token=csrf_token
    )


if __name__ == "__main__":
    app.run(debug=False, port=5000)