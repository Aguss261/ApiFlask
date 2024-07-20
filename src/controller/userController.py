import bcrypt
from flask import request, jsonify
from src.service.userService import UserService
from src.utils.jwt_utils import generate_token

user_service = UserService()

def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    direccion = data.get('direccion')

    if user_service.get_user_by_username(username):
        return jsonify({'message': 'User already exists'}), 400

    user_id = user_service.create_user(username, email, password, direccion)
    if user_id:
        token = generate_token(user_id)
        return jsonify({'token': token}), 201
    return jsonify({'message': 'Failed to create user'}), 500

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = user_service.get_user_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        token = generate_token(user.id)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

