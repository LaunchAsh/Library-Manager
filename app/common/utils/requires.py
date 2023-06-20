from flask import jsonify, request
import jwt 
from functools import wraps
from flask import Blueprint, request , g
from app.dao import user_dao
from app.common.utils.responses import response_with
SECRET_KEY = 'LIBRARYAPP'

class Response:
    def __init__(self):
        self.status = True
        self.status_code = 200
    @classmethod
    def success_response(cls):
        response = cls()
        response.status = True
        response.status_code = 200
        return response

    @classmethod
    def failed_response(cls, status_code):
        response = cls()
        response.status = False
        response.status_code = status_code
        return response

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        bearer  = request.headers.get('Authorization')
        if not bearer :
            return response_with(Response().failed_response(403), None,'Token is missing')
        try:
            token = bearer.split()[1]
            data = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
            g.data_token = data
        except:
            return response_with(Response().failed_response(403), None,'Token is invalid')
        
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        bearer  = request.headers.get('Authorization')
        if not bearer :
            return response_with(Response().failed_response(403), None,'Token is missing')
        try:
            token = bearer.split()[1]
            data = jwt.decode(token,SECRET_KEY, algorithms=["HS256"])
            user_id = data.get("user_id")
            user = user_dao.get_user_by_id(user_id)
            if user and user.role_id == '1': 
                g.data_token = data
                g.user_info = user
            else : response_with(Response().failed_response(403), None,'No permission')
        except:
            return response_with(Response().failed_response(403), None,'Token is invalid')
        return f(*args, **kwargs)
    return decorated