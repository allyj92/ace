# /client/flask_backend/routes.py
from flask import request, jsonify
from flask_backend import app

# Example login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Basic authentication logic (you can replace this with DB logic)
    if username == "user" and password == "password":
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Example signup route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Handle user registration logic
    return jsonify({"message": "Signup successful!"}), 200
