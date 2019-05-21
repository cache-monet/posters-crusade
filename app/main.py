from flask import Flask, jsonify, request
from errors import InvalidUsage 
from collection import collect

app = Flask(__name__)

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def home():
    return "Welcome poster!"

@app.route('/posts', methods=['GET'])
def collection():
    data = request.get_json()
    if not data:
        raise InvalidUsage("ERROR: Empty request body", status_code=400)

    users = data.get('users') or []
    limit = data.get('limit') or 10
    return jsonify(collect(users, limit))
