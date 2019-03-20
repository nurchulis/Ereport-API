from run import app
from flask import jsonify
@app.route('/')
def index():
    return ('API OK :D')