from flask import request , g
from flask import Blueprint
from app.common.utils.requires import token_required
from app.common.utils.responses import get_resp_with_status,response_with
from app.services import review_service
import requests
bp = Blueprint('rev', __name__)

class ReviewResponse:
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
@bp.route('/get', methods=['POST', 'OPTIONS'])
def get_review():
    try:
        payload = request.get_json(force=True)
        result = review_service.get_review_by_book_id(payload)
        return response_with(ReviewResponse().success_response(),result)
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(ReviewResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(ReviewResponse().failed_response(500), 500)
    
@bp.route('/add', methods=['POST', 'OPTIONS'])
@token_required
def insert_review():
    try:
        session = g.data_token
        payload = request.get_json(force=True)
        review_service.add_new_review(payload,session)
        return response_with(ReviewResponse().success_response())
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(ReviewResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(ReviewResponse().failed_response(500), 500)

@bp.route('/delete', methods=['POST', 'OPTIONS'])
@token_required
def delete_review():
    try:
        session = g.token_data
        payload = request.get_json(force=True)
        review_service.delete_review(payload,session)
        return response_with(ReviewResponse().success_response())
    except requests.exceptions.Timeout as err:
        return get_resp_with_status(ReviewResponse().failed_response(504), 504)
    except Exception as err:
        return get_resp_with_status(ReviewResponse().failed_response(500), 500)