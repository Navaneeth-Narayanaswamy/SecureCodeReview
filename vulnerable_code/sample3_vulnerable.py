from flask import Flask, request

app = Flask(__name__)

users = {
    "101": {
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "admin"
    },
    "102": {
        "name": "Student User",
        "email": "student@example.com",
        "role": "student"
    }
}


@app.route("/profile")
def profile():
    user_id = request.args.get("id")

    user = users.get(user_id)

    if not user:
        return "<h2>User not found</h2>", 404

    return f"""
    <h1>User Profile</h1>
    <p>Name: {user['name']}</p>
    <p>Email: {user['email']}</p>
    <p>Role: {user['role']}</p>
    """


if __name__ == "__main__":
    app.run(debug=False, port=5002)