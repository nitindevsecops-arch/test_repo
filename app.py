from flask import Flask, request, render_template_string
import sqlite3
import os
import pickle

app = Flask(__name__)

# Hardcoded secret key (bad)
app.secret_key = "supersecretkey"

@app.route("/")
def index():
    return "Vulnerable Flask App"

# --- SQL Injection ---
@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Vulnerable SQL query (string concatenation)
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()
