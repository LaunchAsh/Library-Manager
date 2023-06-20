from app import db
from app.models.token import Token


def get_refresh_token_by_user_id(user_id):
    result = Token.query.filter(
        Token._user_id == user_id,
        Token.is_active == 1
    ).first()
    return result or None

def get_token_by_id(id):
    result = Token.query.filter(
        Token.id == id,
        Token.is_active == 1
    ).first()
    return result or None

def delete_token_by_id(id):
    transaction_retrieved = Token.query.filter(
        Token.id == id,
        Token.is_active == 1
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.is_active = False
        db.session.add(transaction_retrieved)
        db.session.commit()

def store_refresh_token( token,user_id,user_name,due_date):
    new_token = Token(
        _id = token,
        _user_id = user_id,
        _due_date = due_date,
        _create_by = user_name,
        _modified_by = user_name)
    db.session.add(new_token)
    db.session.commit()
