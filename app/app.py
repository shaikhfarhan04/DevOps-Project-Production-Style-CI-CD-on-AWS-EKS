from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/version")
def version():
    return jsonify({
        "application": "DevOps Demo Application",
        "version": "1.0.1",
        "environment": "development"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)