from functools import wraps
from flask import request

try:
    apiKey = os.environ['apiKey']
except:
    apiKey = 'default'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        if not token:
            return {'message': 'Token is missing.'}, 401
        if token != apiKey:
            return {'message': 'Your token is wrong, wrong, wrong!!!'}, 401
        return f(*args, **kwargs)

    return decorated