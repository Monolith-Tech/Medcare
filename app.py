# -*- coding: utf-8 -*-
# author: Madhav (https://github.com/madhav-mknc)

from configs import HOST, PORT
from utils.utils import *

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
# Change this to a strong random key in a production environment
app.secret_key = os.getenv("FLASK_SECRET_KEY")
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


# submit new session
@app.route('/submit_session', methods=['GET', 'POST'])
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
        filepath = os.path.join("uploads", filename)
        file.save(filepath)
        
        process_audio(audio_filepath=filepath)
        
        flash('File uploaded successfully')
        return redirect(url_for('index'))

    else:
        flash('Invalid file type', 'error')
        return redirect(request.url)


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

    # diagnosis_file = os.path.join(db_directory, 'DD.txt')
    # if os.path.exists(diagnosis_file):
    #     with open(diagnosis_file) as file:
    #         DD = file.read().strip()
    #     return render_template("records.html", transcript=transcript_data, soap=soap_data, diagnosis=DD)
    
    # return render_template("records.html", transcript=transcript_data, soap=soap_data)
    
    diff_diagnosis = request.args.get('diff_diagnosis', None)

    diagnosis_file = os.path.join(db_directory, 'DD.txt')
    if os.path.exists(diagnosis_file):
        with open(diagnosis_file) as file:
            diff_diagnosis = file.read().strip()

    return render_template(
        "records.html", 
        transcript = transcript_data, 
        soap = soap_data, 
        diff_diagnosis = diff_diagnosis, 
        entry_id = entry_id
    )


# upload reports
@app.route('/upload_reports/<entry_id>', methods=['POST'])
@login_required
def upload_reports(entry_id):
    if 'report_files' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    if not os.path.exists(f'database/{entry_id}/tests'):
        os.makedirs(f'database/{entry_id}/tests')

    files = request.files.getlist('report_files')
    for file in files:
        if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in {'pdf'}:
            filename = secure_filename(file.filename)
            file.save(f'database/{entry_id}/tests/{filename}')
    
    diff_diagnosis = perform_DD(id=entry_id)
    
    return redirect(url_for('record_entry', entry_id=entry_id, diff_diagnosis=diff_diagnosis))



# # differential diagnosis
# @app.route('/diagnosis/<entry_id>')
# @login_required
# def diagnosis(entry_id):
#     """
#     Level 4
#     """

#     return render_template('diagnosis.html')


# main
if __name__ == '__main__':
    app.run(
        host=HOST,
        port=PORT,
        debug=True
    )
