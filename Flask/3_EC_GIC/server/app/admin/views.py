from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from . import admin
from flask import Flask, jsonify, request

users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}
}

# file: server/app/admin/views.py
@admin.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@admin.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if username not in users or users[username]['password'] != password:
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

