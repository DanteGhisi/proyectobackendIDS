from flask import Flask, render_template, jsonify, request
from db import execute

app = Flask(__name__)

from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

BACKEND_URL = 'http://localhost:5000'

@app.route('/', methods=['GET'])
def saludar():
    return {'mensaje': 'hola mundo'}
