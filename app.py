#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_limiter import Limiter

import json
import hashlib
import os
import LOGGER


app = Flask('originstorebackend')
CORS(app)

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
RATE_LIMIT = 100
jwt = JWTManager(app)
limiter = Limiter(app)


def checkCreditentions(username, password) -> bool:
    LOGGER.debug(f"Checking Creditentions of {username}")
    with open('users/users.json', 'r') as f:
         data = json.load(f)
    for user in data:
        if user.get("username") == username and user.get('password') == password: 
            LOGGER.debug(f"User {username} VALIDATED")
            return True
    LOGGER.debug(f"User {username} NOT VALIDATED")
    return False
     
def doesAccountAlreadyExist(username) -> bool:
    with open('users/users.json', 'r') as f:
        data = json.loads(f.read())
    for user_info in data:
        if isinstance(user_info, dict) and user_info.get("username") == username:
            return True
    return False




@app.errorhandler(400)
def bad_request(error):
    response = jsonify({'error': 'BAD_REQUEST', "message": str(error.description)})
    return response, 400

@app.errorhandler(401)
def unauthorized(error):
    response = jsonify({'error': 'UNAUTHORIZED', "message": str(error.description)})
    return response, 401

@app.errorhandler(403)
def forbidden(error):
    response = jsonify({'error': 'FORBIDDEN', "message": str(error.description)})
    return response, 403

@app.errorhandler(404)
def page_not_found(error):
     return jsonify({"error": "PAGE_NOT_FOUND", "message": str(error.description)}), 404

@app.errorhandler(405)
def method_not_allowd(error):
    return jsonify({'error': 'METHOD_NOT_ALLOWED', 'message': str(error.description)}), 405

@app.errorhandler(406)
def not_acceptable(error):
    return jsonify({'error': 'NOT_ACCEPTABLE', 'message': str(error.description)}), 406

@app.errorhandler(408)
def timeout(error):
    return jsonify({'error': 'REQUEST_TIMEOUT', 'message': str(error.description)}), 408

@app.errorhandler(409)
def conflict(error):
    return jsonify({'error': 'CONFLICT', 'message': str(error.description)}), 409

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify({"error": "RATELIMIT_EXCEEDED", "message": str(e.description), "extra": f"limit of {RATE_LIMIT} per minute"}), 429

@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify({'error': 'INTERNAL_SERVER_ERROR', "message": str(error.description)})
    return response, 500

@app.route('/')
def index():
    return jsonify({"message": "Hello! This is the API for >> https://origin-store-app.vercel.app/ <<"})

@limiter.limit("100 per minute")
@app.route('/applications', methods=['GET'])
def applications():
    with open('apps/applications.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/DEBUGGING/USERS')
def users():
    LOGGER.info("Got DEBUG")
    with open('users/users.json', 'r') as f:
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
        if 'accounts' not in data:
            data['accounts'] = []
        data['accounts'].append({"username": username, "password": hashed_password})

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
        return jsonify({"message": "APP_CREATED"}), 201
    else:
        return jsonify({"error": "INVALID_CREDENTIALS"}), 401  
    
if __name__ == '__main__':
    app.run('0.0.0.0', 8080, False)
