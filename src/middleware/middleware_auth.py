import os
from functools import wraps
from flask import request, jsonify
import jwt
from jwt import InvalidTokenError

from src.controller.userController import user_service
from src.service.userService import UserService
from src.utils.jwt_utils import ExpiredTokenError, SECRET_KEY
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Invalid token. Please log in again.')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            decode_token(token)
        except jwt.ExpiredSignatureError as e:
            return jsonify({'message': str(e)}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'message': str(e)}), 401

        return f(*args, **kwargs)

    return decorated



def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()  # Obtiene el ID del usuario del token
        user_service = UserService()
        user = user_service.get_user_by_id(user_id)
        if user and user.role_id == 8:  # Verifica si el rol del usuario es admin (rol 8)
            return f(*args, **kwargs)
        return jsonify({'message': '¡Se requiere acceso de administrador!'}), 403
    return decorated