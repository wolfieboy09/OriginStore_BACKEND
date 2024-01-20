#!/usr/bin/env python3

from flask import Flask
from flask import jsonify
from flask_cors import CORS

import json


app = Flask('originstorebackend')
CORS(app)

@app.route('/')
def index():
    return "Hello!!"

@app.route('/applications', methods=['GET'])
def applications():
    with open('apps/applications.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, False)