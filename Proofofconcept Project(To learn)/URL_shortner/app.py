import json
import os
import string
import random
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "urls.json")
BASE_URL = "http://localhost:5000/"


# -----------------------------------
# Load & Save Database
# -----------------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------
# Generate Short Code
# -----------------------------------
def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


# -----------------------------------
# Create Short URL
# -----------------------------------
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL required"}), 400

    db = load_data()

    code = generate_code()

    # ensure uniqueness
    while code in db:
        code = generate_code()

    db[code] = original_url
    save_data(db)

    short_url = BASE_URL + code

    return jsonify({
        "short_url": short_url
    })


# -----------------------------------
# Redirect Route
# -----------------------------------
@app.route("/<code>")
def redirect_url(code):
    db = load_data()

    if code in db:
        return redirect(db[code])
    else:
        return jsonify({"error": "URL not found"}), 404


# -----------------------------------
# Home Route
# -----------------------------------
@app.route("/")
def home():
    return "URL Shortener Running"


# -----------------------------------
# Run Server
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)
