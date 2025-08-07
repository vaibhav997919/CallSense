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
        files = request.files.getlist('audiofile')
        if not files or all(f.filename == '' for f in files):
            flash('No selected file')
            return redirect(request.url)
        issue_counts = {}
        file_results = []
        issue_suggestions = {
            'Billing Issue': 'This issue seems related to payment or billing. Please check your payment method or contact billing support.',
            'Delivery Issue': 'This issue is related to delivery. Please verify the shipping address or contact the delivery provider.',
            'Technical Issue': 'This appears to be a technical problem. Try basic troubleshooting or contact technical support.',
            'Refund Issue': 'This is a refund-related issue. Please check the refund policy or contact customer service for assistance.',
            'Password Issue': 'This is related to password or login. Try resetting your password or contact support.',
            'Networking Issue': 'This may be a networking or connectivity problem. Please check your internet connection or try again later.',
            'Account Suspension Issue': 'Your account appears to be suspended. Please contact support to resolve this issue.',
            'Product Inquiry Issue': 'This is a product inquiry. Please visit our product FAQ or contact sales for more information.',
            'Other Issue': 'This issue does not fit common categories. Please provide more details to support.'
        }
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                result = analyze_audio(filepath)
                transcription = result.get('transcription', '').lower()
                if 'billing' in transcription or 'payment' in transcription or 'invoice' in transcription:
                    issue = 'Billing Issue'
                elif 'delivery' in transcription or 'shipment' in transcription or 'shipping' in transcription:
                    issue = 'Delivery Issue'
                elif 'technical' in transcription or 'error' in transcription or 'bug' in transcription or 'crash' in transcription:
                    issue = 'Technical Issue'
                elif 'refund' in transcription or 'return' in transcription:
                    issue = 'Refund Issue'
                elif 'password' in transcription or 'login' in transcription or 'account' in transcription:
                    issue = 'Password Issue'
                elif 'network' in transcription or 'connectivity' in transcription or 'internet' in transcription:
                    issue = 'Networking Issue'
                elif 'suspend' in transcription or 'suspended' in transcription or 'account locked' in transcription:
                    issue = 'Account Suspension Issue'
                elif 'product' in transcription or 'item' in transcription or 'inquiry' in transcription or 'information' in transcription:
                    issue = 'Product Inquiry Issue'
                else:
                    issue = 'Other Issue'
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
                suggestion = issue_suggestions.get(issue, issue_suggestions['Other Issue'])
                file_results.append({'filename': filename, 'result': result, 'issue': issue, 'suggestion': suggestion})
        return render_template('result.html', file_results=file_results, issue_counts=issue_counts)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
