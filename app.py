from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input

# Load model
model = load_model('signature_model.h5')
IMG_SIZE = (224, 224)

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
DATABASE = 'users.db'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize DB
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

# Helper: Get user by username or email
def get_user(identifier):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? OR email=?", (identifier, identifier))
        return cur.fetchone()

# Route: Home
@app.route('/')
def home():
    return render_template('home.html')

# Route: Sign Up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if get_user(username) or get_user(email):
            flash('Username or Email already exists. Please try a different one.', 'danger')
            return render_template('signup.html')

        hashed_password = generate_password_hash(password)

        with sqlite3.connect(DATABASE) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
            conn.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']

        user = get_user(identifier)

        if user and check_password_hash(user[3], password):
            session['email'] = user[2]
            session['username'] = user[1]
            flash(f'Welcome back, {user[1]}!', 'success')
            return redirect(url_for('index'))

        flash('Invalid username/email or password.', 'danger')
        return render_template('login.html')

    return render_template('login.html')

# Route: Logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Route: Upload + Predict
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'email' not in session:
        flash("Please login to access predictions.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'warning')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        img = load_img(filepath, target_size=IMG_SIZE)
        img_array = img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)[0][0]
        confidence = prediction if prediction > 0.5 else 1 - prediction  # Confidence calculation
        result = "Genuine Signature ✅" if prediction > 0.5 else "Forged Signature ❌"

        return render_template('result.html', filename=filename, result=result, confidence=confidence)

    return render_template('index.html')

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return url_for('static', filename='uploads/' + filename)

# Route: Predict (API)
@app.route('/predict', methods=['POST'])
def predict():
    if 'email' not in session:
        flash("Please login to access predictions.", "warning")
        return redirect(url_for('login'))

    if 'file' not in request.files:
        flash('No file part.', 'warning')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file.', 'warning')
        return redirect(request.url)

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    img = load_img(filepath, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0][0]
    confidence = prediction if prediction > 0.5 else 1 - prediction  # Confidence calculation
    result = "Genuine Signature ✅" if prediction > 0.5 else "Forged Signature ❌"

    return render_template('result.html', filename=filename, result=result, confidence=confidence)

# Run App
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
