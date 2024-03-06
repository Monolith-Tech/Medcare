# utilties / helper functions for app.py

import os
import json
import sys
import hashlib


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




