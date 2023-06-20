from flask import request , g
from flask import Blueprint
from app.common.utils.responses import get_resp_with_status,response_with
from app.services import borrowing_service
import requests
from app.common.utils.requires import admin_required, token_required

bp = Blueprint('borrow', __name__)

class BorrowResponse:
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
def get_all_borrow():
    try:
        result = borrowing_service.get_all_borrowing()
        return response_with(BorrowResponse().success_response(), result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BorrowResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BorrowResponse().failed_response(500), 500)

@bp.route('/add', methods=['POST', 'OPTIONS'])
@token_required
def add_my_borrow():
    try:
        session = g.data_token
        payload = request.get_json(force=True)
        status , result = borrowing_service.add_new_borrowing(payload,session)
        if status :
            return response_with(BorrowResponse().success_response(),None)
        else:
            return response_with(BorrowResponse().failed_response(201), None,result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BorrowResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BorrowResponse().failed_response(500), 500)

@bp.route('/delete', methods=['POST', 'OPTIONS'])
@admin_required
def get_borrow_my():
    try:
        session = g.data_token
        payload = request.get_json(force=True)
        result = borrowing_service.delete_borrowing(payload,session)
        return response_with(BorrowResponse().success_response(), result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BorrowResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BorrowResponse().failed_response(500), 500)


@bp.route('/search', methods=['POST', 'OPTIONS'])
@token_required
def get_borrow_user():
    try:
        session = g.data_token
        payload = request.get_json(force=True)
        result = borrowing_service.search_borrowing_by_user(payload,session)
        return response_with(BorrowResponse().success_response(), result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BorrowResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BorrowResponse().failed_response(500), 500)

@bp.route('/search', methods=['PUT', 'OPTIONS'])
@admin_required
def get_borrow_admin():
    try:
        payload = request.get_json(force=True)
        result = borrowing_service.search_borrowing_in_date(payload)
        return response_with(BorrowResponse().success_response(), result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BorrowResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BorrowResponse().failed_response(500), 500)
    

@bp.route('/return', methods=['POST', 'OPTIONS'])
@admin_required
def check_return_book():
    try:
        session = g.data_token
        payload = request.get_json(force=True)
        status = borrowing_service.check_return_book(payload,session)
        if status :
            return response_with(BorrowResponse().success_response(),None)
        else:
            return response_with(BorrowResponse().failed_response(201), None,"THIS BORROWING IS NOT EXIST")
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BorrowResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BorrowResponse().failed_response(500), 500)
    
@bp.route('/given', methods=['POST', 'OPTIONS'])
@admin_required
def check_given():
    try:
        session = g.data_token
        payload = request.get_json(force=True)
        borrowing_service.check_give_book(payload,session)
        return response_with(BorrowResponse().success_response())
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BorrowResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BorrowResponse().failed_response(500), 500)

@bp.route('/find', methods=['POST', 'OPTIONS'])
@admin_required
def find_borrow():
    try:
        payload = request.get_json(force=True)
        status,result,message = borrowing_service.find_return_borrow_by_book_isbn(payload)
        if status :
            return response_with(BorrowResponse().success_response(),result,message)
        else:
            return response_with(BorrowResponse().failed_response(201), result,message)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BorrowResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BorrowResponse().failed_response(500), 500)