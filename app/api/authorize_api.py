from flask import request , g
from flask import Blueprint
from app.common.utils.responses import get_resp_with_status,response_with
import requests
from app.services import auth_service, user_service
from app.common.utils.requires import token_required

bp = Blueprint('authorize', __name__)

class AuthResponse:
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
    
@bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    try:
        payload = request.get_json(force=True)
        status, result = auth_service.login_service(payload)
        if status : 
            return response_with(AuthResponse().success_response(), result,'Login Successfully')
        else : 
            return response_with(AuthResponse().failed_response(201),None,'Invalid Information')
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(AuthResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(AuthResponse().failed_response(500), 500)

@bp.route('/refresh', methods=['POST', 'OPTIONS'])
def refresh():
    try: 
        payload = request.get_json(force=True)
        status , result = auth_service.reset_access_token(payload)
        if status : 
            return response_with(AuthResponse().success_response(), result)
        else : 
            return response_with(AuthResponse().failed_response(201), result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(AuthResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(AuthResponse().failed_response(500), 500)
    
@bp.route('/logout', methods=['POST', 'OPTIONS'])
@token_required
def logout():
    try: 
        payload = request.get_json(force=True)
        auth_service.logout_service(payload)
        return get_resp_with_status(AuthResponse().success_response(), 200)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(AuthResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(AuthResponse().failed_response(500), 500)
    
@bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    try:
        payload = request.get_json(force=True)
        status, result = user_service.insert_user(payload,'2')
        if status :
            return response_with(AuthResponse().success_response(),None)
        else:
            return response_with(AuthResponse().failed_response(201), None,result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(AuthResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(AuthResponse().failed_response(500), 500)

@bp.route('/password', methods=['PUT', 'OPTIONS'])
@token_required
def change_pass():
    try:
        session = g.data_token
        payload = request.get_json(force=True)
        status, result = user_service.change_password(payload,session)
        if status :
            return response_with(AuthResponse().success_response(),None)
        else:
            return response_with(AuthResponse().failed_response(201), None,result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(AuthResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(AuthResponse().failed_response(500), 500)

@bp.route('/', methods=['DELETE', 'OPTIONS'])
@token_required
def delete_account():
    try:
        session = g.data_token
        user_service.delete_user(session)
        return response_with(AuthResponse().success_response(),None)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(AuthResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(AuthResponse().failed_response(500), 500)
