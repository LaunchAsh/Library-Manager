from flask import request,g
from flask import Blueprint
from app.common.utils.responses import get_resp_with_status,response_with
import requests
from app.services import user_service
from app.common.utils.requires import token_required , admin_required

bp = Blueprint('acc', __name__)

class UserResponse:
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

    
@bp.route('/all', methods=['GET', 'OPTIONS'])
@admin_required
def get_all():
    try:
        result = user_service.get_all_user()
        return response_with(UserResponse().success_response(),result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(UserResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(UserResponse().failed_response(500), 500)

@bp.route('/', methods=['GET', 'OPTIONS'])
@token_required
def get_user():
    try:
        payload = g.token_data
        result = user_service.get_user_by_id(payload)
        return response_with(UserResponse().success_response(),result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(UserResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(UserResponse().failed_response(500), 500)

@bp.route('/', methods=['POST', 'OPTIONS'])
@admin_required
def insert_user_by_admin():
    try:
        payload = request.get_json(force=True)
        status ,result = user_service.insert_user(payload,None)
        if status :
            return response_with(UserResponse().success_response(),None)
        else:
            return response_with(UserResponse().failed_response(201), None,result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(UserResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(UserResponse().failed_response(500), 500)



@bp.route('/', methods=['PUT', 'OPTIONS'])
@admin_required
def change_user():
    try:
        payload = request.get_json(force=True)
        result = user_service.change_info_user(payload)
        return response_with(UserResponse().success_response(),result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(UserResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(UserResponse().failed_response(500), 500)

@bp.route('/', methods=['DELETE', 'OPTIONS'])
@admin_required
def delete_user():
    try:
        payload = request.get_json(force=True)
        result = user_service.delete_user(payload)
        return response_with(UserResponse().success_response(),result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(UserResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(UserResponse().failed_response(500), 500)