from flask import Flask, request, render_template, send_from_directory
import requests
import os
import sqlite3

app = Flask(__name__, template_folder='.')

SECRET_KEY =""

# -------------------------
# CREATE DATABASE IF NOT EXISTS
# -------------------------
def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        year TEXT,
        department TEXT,
        email TEXT,
        password TEXT,
        phone TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# -------------------------
# HOME PAGE (GET)
# -------------------------
@app.route('/')
def home():
    return render_template('StudentSignUp.html')

# -------------------------
# SERVE LOGO IMAGE
# -------------------------
@app.route('/TCE_COLLAB_HUB_LOGO.png')
def logo():
    return send_from_directory(os.getcwd(), 'TCE_COLLAB_HUB_LOGO.png')

# -------------------------
# SIGNUP + CAPTCHA VERIFY (POST)
# -------------------------
@app.route('/signup', methods=['POST'])
def signup():

    # Get form data
    name = request.form['name']
    year = request.form['year']
    department = request.form['department']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    recaptcha_response = request.form['g-recaptcha-response']

    # Verify reCAPTCHA
    data = {
        'secret': SECRET_KEY,
        'response': recaptcha_response
    }

    r = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data=data
    )

    result = r.json()

    if not result['success']:
        return "CAPTCHA Failed ❌ Try again"

    # If captcha success → store in DB
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students(name, year, department, email, password, phone)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, year, department, email, password, phone))

    conn.commit()
    conn.close()

    return "Registration Successful — Human Verified ✅"

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)