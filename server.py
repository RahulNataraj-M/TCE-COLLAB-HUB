from flask import Flask, request, render_template, send_from_directory
import requests
import os
app = Flask(__name__, template_folder='.')

SECRET_KEY = "6LcCJ20sAAAAABdLlF8UGun1Da9vuurPYDiqUHgf"

# HOME PAGE
@app.route('/')
def home():
    return render_template('StudentSignUp.html')

# route to serve image manually
@app.route('/TCE_COLLAB_HUB_LOGO.png')
def logo():
    return send_from_directory(os.getcwd(), 'TCE_COLLAB_HUB_LOGO.png')

# CAPTCHA VERIFY
@app.route('/verify', methods=['POST'])
def verify():
    recaptcha_response = request.form['g-recaptcha-response']

    data = {
        'secret': SECRET_KEY,
        'response': recaptcha_response
    }

    r = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data=data
    )

    result = r.json()

    if result['success']:
        return "Login Successful — Human Verified ✅"
    else:
        return "CAPTCHA Failed ❌ Try again"

app.run(debug=True)
