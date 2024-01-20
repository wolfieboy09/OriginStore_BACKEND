#!/usr/bin/env python3

from flask import Flask
from flask import jsonify
import json


app = Flask('originstorebackend')

@app.route('/')
def index():
    return "Hello!!"

@app.route('/applacations', methods=['GET'])
def applacations():
    with open('apps/applacations.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, False)