#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import json
import hashlib
import os


app = Flask('originstorebackend')
CORS(app)

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Dummy user for demonstration purposes
users = {
    'username': 'password'
}

def checkCreditentions(username, password) -> bool:
     ...
     
def doesAccountAlreadyExist(username) -> bool:
    with open('users/users.json', 'r') as f:
        data = json.load(f)
    for user_info in data:
        if user_info.get("username") == username: return True
    return False


@app.route('/')
def index():
    return "Hello!!"

@app.route('/applications', methods=['GET'])
def applications():
    with open('apps/applications.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/account/new', methods=['POST'])
def newAccount():
    username = request.json.get('username')
    password = request.json.get('password')

    if not doesAccountAlreadyExist(username):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password.encode('utf-8'))
        hashed_password = sha256_hash.hexdigest()

        with open('users/users.json', 'r') as f:
            data = json.load(f)

        data.append({"username": username, "password": hashed_password})

        with open('users/users.json', 'w') as f:
            json.dump(data, f, indent=2)

        return jsonify({"message": "ACCOUNT_CREATED"}), 201
    else:
        return jsonify({"error": "ACCOUNT_ALREADY_EXISTS"}), 409

@app.route('/app/new', methods=['POST'])
@jwt_required()
def newApp():
    username = request.json.get('username')
    password = request.json.get('password')
    if checkCreditentions(username, password):
        with open('apps/applications.json', 'r') as f:
            data = json.load(f)
        data['apps'].append(request.headers.get('App-Data'))
        with open('apps/applications.json', 'w') as f:
            json.dump(data, f)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080, False)
