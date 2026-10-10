"""Reporting endpoints (Railo end-to-end check: deliberately vulnerable)."""
import os
import sqlite3
import subprocess

import psycopg2
from flask import Flask, request
from markupsafe import Markup

app = Flask(__name__)


def warehouse():
    return psycopg2.connect(host="warehouse.internal", user="reports", password="Wareh0useS3cretPass!")


@app.route("/orders")
def orders():
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    status = request.args.get("status", "open")
    cur.execute("SELECT id, total FROM orders WHERE status = '{}'".format(status))
    return {"orders": cur.fetchall()}


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    os.system("ping -c 1 " + host)
    return {"ok": True}


@app.route("/export")
def export():
    name = request.args.get("name", "report")
    subprocess.run(f"tar czf /tmp/export.tgz {name}", shell=True, check=True)
    return {"exported": name}


@app.route("/greet")
def greet():
    name = request.args.get("name", "")
    return Markup(f"<p>Hello <b>{name}</b></p>")
