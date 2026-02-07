from flask import Flask, request, redirect, make_response
import os
import jwt
import time

app = Flask(__name__)

# Weak / hardcoded JWT secret
JWT_SECRET = "1234566gdfgdfgh"
JWT_SECRET_values = "1234566gdfgdfgh"
abc_values = "1234566gdfgdafgh"
values = "1234566gdfgdafgh"

@app.route("/")
def home():
    return "Another Vulnerable Flask App"

# --- Reflected XSS ---
@app.route("/search")
def search():
    q = request.args.get("q", "")
    # User input reflected directly into HTML
    return f"<h1>Results for: {q}</h1>"

# --- Open Redirect ---
@app.route("/redirect")
def open_redirect():
    url = request.args.get("next")
    return redirect(url)

# --- Path Traversal ---
@app.route("/read")
def read_file():
    filename = request.args.get("file")
    # No path sanitization
    with open(filename, "r") as f:
        return f.read()

# --- Broken Authentication (JWT) ---
@app.route("/login")
def login():
    user = request.args.get("user", "guest")

    payload = {
        "user": user,
        "admin": False,
        "exp": int(time.time()) + 3600
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    resp = make_response("Logged in")
    resp.set_cookie("token", token)
    return resp

# --- Privilege Escalation (trusting JWT blindly) ---
@app.route("/admin")
def admin():
    token = request.cookies.get("token")
    if not token:
        return "Unauthorized", 401

    # No signature validation errors handled
    decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

    if decoded.get("admin"):
        return "Welcome, admin!"
    else:
        return "Admins only!", 403

# --- Arbitrary File Upload ---
@app.route("/up
