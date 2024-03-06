# -*- coding: utf-8 -*-
# author: Madhav (https://github.com/madhav-mknc)

from configs import HOST, PORT
from utils import *

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for, 
    session, 
    flash, 
    jsonify
)

from functools import wraps
from flask_cors import CORS
from werkzeug.utils import secure_filename

import json

import os
from dotenv import load_dotenv
load_dotenv()

# Initialzing flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Change this to a strong random key in a production environment
# app.secret_key = str(unique_id()).replace("-","")


# only logged in access
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('authenticated'):
        return redirect(url_for("index"))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if is_authenticated(username, password):
            # Save the authenticated status in the session
            session['authenticated'] = True
            return redirect(url_for('index'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    
    return render_template('login.html')


# index
@app.route('/')
@login_required
def index():
    """
    Level 1
    """

    records = os.listdir('database')
    entries = []
    for id in records:
        with open(f'database/{id}/info.json', 'r') as file:
            info = json.load(file)
            name = info['title']
        entries.append({"id": id, "name": name})

    return render_template('dashboard.html', entries=entries)


# record new session
@app.route('/record_session')
@login_required
def record_session():
    """
    Level 2
    """
    
    return render_template('record_session.html')  


# record new session
@app.route('/submit_session', methods=['POST'])
@login_required
def submit_session():
    """
    Level 2
    """

    # check if the post request has the file part
    if 'audio_file' not in request.files:
        return redirect(request.url)

    file = request.files['audio_file']
    
    if file.filename == '':
        return redirect(request.url)

    if file and file.filename.split('.')[-1] in {'wav', 'mp3', 'ogg'}:
        filename = secure_filename(file.filename)
        file.save(os.path.join("uploads", filename))
        return 'File uploaded successfully'

    else:
        return 'Invalid file type'


@app.route('/record/<entry_id>')
@login_required
def record_entry(entry_id):
    """
    Level 3
    """
    
    db_directory = f"database/{entry_id}"
    if not os.path.exists(db_directory):
        return jsonify({"error": "Server side error"})
    
    transcript_filename = os.path.join(db_directory, 'transcript.json')
    with open(transcript_filename, 'r') as file:
        transcript_data = json.load(file)
    
    soap_filename = os.path.join(db_directory, 'soap.txt')
    with open(soap_filename, 'r') as file:
        soap_data = file.read().strip()

    return render_template("records.html", transcript=transcript_data, soap=soap_data)




# main
if __name__ == '__main__':
    app.run(
        host = HOST,
        port = PORT, 
        debug = True
    )

