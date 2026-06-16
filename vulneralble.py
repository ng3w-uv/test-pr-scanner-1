import hashlib
import os
import pickle
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)

# --- Hardcoded secrets (secrets/credentials category) ---
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
API_TOKEN = "sk_live_51H8xQp2eZvKYlo2C0123456789abcdef"
DB_PASSWORD = "SuperSecret123!"


# --- SQL injection (injection category) ---
@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    # Unsanitized input concatenated straight into the query
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"
    cursor.execute(query)
    return str(cursor.fetchall())


# --- Command injection (injection category) ---
@app.route("/ping")
def ping():
    host = request.args.get("host")
    # User input passed to a shell
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    return output


# --- Use of eval on user input (insecure code pattern) ---
@app.route("/calc")
def calc():
    expression = request.args.get("expr")
    # Arbitrary code execution
    result = eval(expression)
    return str(result)


# --- Unsafe deserialization (insecure code pattern) ---
@app.route("/load")
def load_data():
    blob = request.args.get("data")
    # pickle on untrusted input = remote code execution
    obj = pickle.loads(bytes.fromhex(blob))
    return str(obj)


# --- Weak cryptography (insecure code pattern) ---
def hash_password(password):
    # MD5 is cryptographically broken for passwords
    return hashlib.md5(password.encode()).hexdigest()


# --- Insecure default / debug mode in production ---
if __name__ == "__main__":
    # Binding to all interfaces with debug on exposes the Werkzeug debugger
    app.run(host="0.0.0.0", debug=True)
