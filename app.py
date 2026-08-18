import os
from flask import Flask, request, send_file

app = Flask(__name__)
BASE_DIR = "/var/www/uploads"

@app.route("/download")
def download():
    filename = request.args.get("file")
    filepath = os.path.join(BASE_DIR, filename)
    return send_file(filepath)
