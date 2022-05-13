import os

import jwt


def decode_auth_token(auth_token):
    """
    Validates the auth token
    """
    try:
        payload = jwt.decode(auth_token, str(os.environ.get('JWT_SECRET_KEY')))
        return payload['username']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def auth_decorator(func):
    def wrapper(*args, **kwargs):
        from flask import request
        authorization = request.headers.environ['HTTP_AUTHORIZATION']
        try:
            jwt_token = authorization.split()[1]
            username = decode_auth_token(jwt_token)
            return func(*args, **kwargs, username=username)
        except Exception as e:
            return {"res": "Token has expired or is invalid, please login again", "error": str(e)}

    return wrapper
