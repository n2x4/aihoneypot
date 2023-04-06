import sqlite3
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login_attempts")
def login_attempts():
    conn = sqlite3.connect("login_attempts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_attempts ORDER BY timestamp DESC")
    data = cursor.fetchall()
    conn.close()

    login_attempts = []
    for entry in data:
        login_attempt = {
            "id": entry[0],
            "timestamp": entry[1],
            "username": entry[2],
            "password": entry[3],
            "ip_address": entry[4]
        }
        login_attempts.append(login_attempt)

    return jsonify(login_attempts)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
