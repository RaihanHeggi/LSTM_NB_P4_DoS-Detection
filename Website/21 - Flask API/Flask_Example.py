from flask import Flask, render_template


def main():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("form.html")

    # Example with parameters
    @app.route("/nama/<nama>")
    def index_nama(nama):
        return f"Hai {nama}, ini testing"

    @app.route("/submit", methods=["POST"])
    def submit():
        return "Hi, User"

    app.run(host="localhost", port="5000")


if __name__ == "__main__":
    main()
