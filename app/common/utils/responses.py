import json

from flask import jsonify, make_response


def response_with(response, value=None, message=None, error=None, headers={}, pagination=None):
    result = obj_to_dict(response)
    if value is not None:
        result.update(value)
    if error is not None:
        result.update({'errors': error})
    if message is not None:
        result.update({'message': message})
    if pagination is not None:
        result.update({'pagination': pagination})
    headers.update({'Access-Control-Allow-Origin': '*'})
    headers.update({'server': 'MSP Webhook'})
    return make_response(jsonify(result), 200, headers)


def response_without_body(response, headers={}):
    return make_response('', response['http_code'], headers)


def obj_to_dict(obj):
    if isinstance(obj, dict):
        return obj
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    elif hasattr(obj, '__slots__'):
        return {slot: getattr(obj, slot) for slot in obj.__slots__}
    else:
        return vars(obj)


def get_resp(response, html_status, **kwargs):
    json_text = json.dumps(response, ensure_ascii=False, default=obj_to_dict)
    resp = make_response(json_text, html_status)
    for key, value in kwargs.items():
        if key == 'data_type':
            resp.headers['X-datatype'] = value
        if key == 'content_type':
            resp.headers['Content-Type'] = value
    return resp


def get_resp_with_status(response, status):
    return get_resp(response, status, data_type='json', content_type='application/json')


INVALID_FIELD_NAME_SENT_422 = {
    'http_code': 422,
    'code': 'UNPROCESSABLE',
    'message': 'Invalid fields found'
}

INVALID_INPUT_422 = {
    'http_code': 422,
    'code': 'UNPROCESSABLE',
    'message': 'Invalid input'
}

MISSING_PARAMETERS_422 = {
    'http_code': 422,
    'code': 'UNPROCESSABLE',
    'message': 'Missing parameters.'
}

BAD_REQUEST_400 = {
    'http_code': 400,
    'code': 'BAD_REQUEST',
    'message': 'Bad request'
}

SERVER_ERROR_500 = {
    'http_code': 500,
    'code': 'INTERNAL_SERVER_ERROR',
    'message': 'Server error'
}

SERVER_ERROR_404 = {
    'http_code': 404,
    'code': 'NOT_FOUND',
    'message': 'Resource not found'
}

UNAUTHORIZED_401 = {
    'http_code': 401,
    'code': 'UNAUTHORIZED',
    'message': 'You are not authorized to execute this.'
}

UNAUTHORIZED_403 = {
    'http_code': 403,
    'code': 'FORBIDDEN',
    'message': 'You are not authorized to execute this.'
}
SUCCESS_200 = {
    'http_code': 200,
    'code': 'SUCCESS'
}

SUCCESS_201 = {
    'http_code': 201,
    'code': 'SUCCESS'
}

SUCCESS_204 = {
    'http_code': 204,
    'code': 'SUCCESS'
}
