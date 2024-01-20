#!/usr/bin/env python3

from flask import Flask
from flask import jsonify


app = Flask('originstorebackend')

@app.route('/')
def index():
    return jsonify({"message": "/ endpoint"})


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, False)