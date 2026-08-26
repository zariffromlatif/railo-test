import os
import sqlite3
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)

BASE_DIR = "/var/www/uploads"
DB_PATH = "app.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/download")
def download():
    """Download a file from the uploads directory."""
    filename = request.args.get("file")
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.commonpath([os.path.realpath(str(filepath)), os.path.realpath(str(BASE_DIR))]) != os.path.realpath(str(BASE_DIR)):
        raise PermissionError("Path traversal denied")
    return send_file(filepath)


@app.route("/user")
def get_user():
    """Look up a user by email."""
    email = request.args.get("email")
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT id, username, role FROM users WHERE email = '{email}'"
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"id": row[0], "username": row[1], "role": row[2]})
    return jsonify({"error": "not found"}), 404


@app.route("/ping")
def ping():
    """Ping a host to check connectivity."""
    host = request.args.get("host")
    output = os.popen(f"ping -c 1 {host}").read()
    return jsonify({"output": output})


# API configuration
API_KEY = "hardcoded_secret_key_do_not_use_in_production_12345"
WEBHOOK_SECRET = "webhook_secret_value_hardcoded_67890"


@app.route("/charge")
def charge():
    """Process a charge using the Stripe API."""
    return jsonify({"key_prefix": API_KEY[:7]})


if __name__ == "__main__":
    app.run()
