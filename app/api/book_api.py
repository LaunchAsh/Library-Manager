from flask import request , g
from flask import Blueprint
from app.common.utils.responses import get_resp_with_status,response_with
from app.services import book_service
import requests
from app.common.utils.requires import admin_required

bp = Blueprint('bok', __name__)

class BookResponse:
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
def get_all():
    try:
        result = book_service.get_all_book()
        return response_with(BookResponse().success_response(), result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BookResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BookResponse().failed_response(500), 500)

@bp.route('/search', methods=['POST', 'OPTIONS'])
def search_by_user():
    try:
        payload = request.get_json(force=True)
        result = book_service.search_book(payload)
        return response_with(BookResponse().success_response(), result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BookResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BookResponse().failed_response(500), 500)

@bp.route('/get', methods=['POST', 'OPTIONS'])
def get_book():
    try:
        payload = request.get_json(force=True)
        result = book_service.get_book_by_id(payload)
        return response_with(BookResponse().success_response(), result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BookResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BookResponse().failed_response(500), 500)

@bp.route('/add', methods=['PUT', 'OPTIONS'])
@admin_required
def add_book():
    try:
        session = g.user_info
        payload = request.get_json(force=True)
        status , result  = book_service.insert_new_book(payload,session)
        if status :
            return response_with(BookResponse().success_response(),None)
        else:
            return response_with(BookResponse().failed_response(201), None,result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BookResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BookResponse().failed_response(500), 500)

@bp.route('/edit', methods=['POST', 'OPTIONS'])
@admin_required
def edit_book():
    try:
        session = g.user_info
        payload = request.get_json(force=True)
        status , result  = book_service.edit_book(payload,session)
        if status :
            return response_with(BookResponse().success_response(),None)
        else:
            return response_with(BookResponse().failed_response(201), None,result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BookResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BookResponse().failed_response(500), 500)
@bp.route('/delete', methods=['POST', 'OPTIONS'])
@admin_required
def delete_book():
    try:
        session = g.user_info
        payload = request.get_json(force=True)
        book_service.delete_book_by_id(payload,session)
        return response_with(BookResponse().success_response())
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(BookResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(BookResponse().failed_response(500), 500)
