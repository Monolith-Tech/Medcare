# utilties / helper functions for app.py

import os
import json
import sys
import hashlib
from uuid import uuid4 as unique_id

from transcript import read_conversation
from soap_generation import generate_SOAP


# Load admin users from the JSON file
USERS_FILE = 'users.json'
USERS = []

if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as file:
        USERS = json.load(file)

else:
    print(f"[error] {USERS_FILE} NOT FOUND")
    sys.exit()

# Check if the provided username and password match any admin user
def is_authenticated(username, password):
    for admin_user in USERS:
        if admin_user['username'] == username and hashlib.sha256(admin_user['password'].encode()).hexdigest() == hashlib.sha256(password.encode()).hexdigest():
            return True
    return False


def process_audio(audio_filepath: str) -> str:
    """
    Converts audio -> Transcript -> Structured conversation -> SOAP
    """
    
    id = unique_id()
    
    conversation = read_conversation(
        audio_file_input = audio_filepath,
        verbose = True,
        save_to_file = f"database/{id}/transcript.json"
    )
    
    soap = generate_SOAP(
        conversation = conversation,
        verbose = True,
        save_to_file = f"database/{id}/soap.txt"
    )
    
    info = {
        "title" : audio_filepath.split('/')[-1].split('.')[0].lower().strip()
    }
    with open(f"database/{id}/info.txt", 'w') as file:
        json.dump(info, file)

    
