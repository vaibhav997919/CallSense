from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from model_from_notebook import analyze_audio

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this in production
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy user for demonstration
USER = {'username': 'user', 'password': 'pass'}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('upload'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == USER['username'] and password == USER['password']:
        session['username'] = username
        return redirect(url_for('upload'))
    flash('Invalid credentials')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        if 'audiofile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['audiofile']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            result = analyze_audio(filepath)
            return render_template('result.html', result=result, filename=filename)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
