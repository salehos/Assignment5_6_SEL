import datetime
import os

import jwt
from pymongo import MongoClient

mongo_servers = str(os.environ.get('MONGO_SERVERS'))
mongo_client = MongoClient(mongo_servers)

database = mongo_client.get_database(name="bidood")
user_col = database.get_collection(name="users")


def check_user_credential(username, password):
    username_check = user_col.find_one({"username": username, "password": password})
    if username_check is None:
        return {"res": "Unable to login with provided credential"}
    return None

def encode_auth_token(username):
    """
    Generate auth token
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'username': username,
        }
        return jwt.encode(
            payload,
            str(os.environ.get('JWT_SECRET_KEY')),
            alg='HS256'
        )
    except Exception as e:
        return e


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
            return func(*args, **kwargs, usernmae=username)
        except:
            return {"res": "Token has expired or is invalid, please login again"}

    return wrapper
