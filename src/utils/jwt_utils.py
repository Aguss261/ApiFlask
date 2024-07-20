import os

import jwt
import datetime

from jwt import InvalidTokenError

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_secret_key')

def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, os.environ.get('JWT_SECRET_KEY', 'default_secret_key'), algorithm='HS256')


class ExpiredTokenError:
    pass


def decode_token(token):
    try:
        payload = jwt.decode(token, os.environ.get('SECRET_KEY', "default_secret_key"), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenError('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise InvalidTokenError('Invalid token. Please log in again.')