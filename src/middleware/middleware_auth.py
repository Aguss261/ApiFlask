from functools import wraps
from flask import request, jsonify
import jwt

from src.service.userService import UserService
from src.utils.jwt_utils import ExpiredTokenError, SECRET_KEY
from flask_jwt_extended import get_jwt_identity, jwt_required


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
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        user_service = UserService()
        user = user_service.get_user_by_id(user_id)
        if user and user.rol_id == 8:
            return f(*args, **kwargs)
        return jsonify({'message': '¡Se requiere acceso de administrador!'}), 403
    return decorated