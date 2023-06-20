from app.dao import user_dao , token_dao
from datetime import datetime, timedelta
import jwt 
import secrets
from datetime import datetime, timedelta

SECRET_KEY = 'LIBRARYAPP'

def generate_access_token(user_id,user_name):
    payload = {
        'user_id': user_id,
        'user_name':user_name,
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'iat': datetime.utcnow()
    } 
    access_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return access_token

def generate_refresh_token(user_id,user_name):
    refresh_token_length = 100  # Đặt chiều dài token mong muốn
    refresh_token = secrets.token_urlsafe(refresh_token_length)
    current_time = datetime.now()
    due_date = current_time + timedelta(days=30)
    token_dao.store_refresh_token(refresh_token,user_id,user_name,due_date)
    return refresh_token

def login_service(payload):
    email = payload.get("email")
    password = payload.get("password")
    resp = user_dao.get_user_by_email(email)
    if resp:
        for user in resp:
            if user.password == password :
                result = { 
                    "access_token": generate_access_token(user.id,user.name),
                    "refresh_token": generate_refresh_token(user.id,user.name),
                    "user": {
                        "id":user.id,
                        "name":user.name,
                        "email":user.email,
                        "role":user.role_id
                    }
                }
                return True, result
    return False, 'Invalid credentials'

def reset_access_token(payload):
    refresh_token = payload.get("refresh_token")
    token = token_dao.get_token_by_id(refresh_token)
    user = user_dao.get_user_by_id(token.user_id)
    current_time = datetime.now()
    result = 'The token dont exist!'
    if token:
        if token.due_date >= current_time :
            access_token = generate_access_token(user.id,user.name)
            result = {
                "access_token":access_token
            }
            return True , result
    return False , result

def logout_service(payload):
    refresh_token = payload.get("refresh_token")
    print(refresh_token)
    token_dao.delete_token_by_id(refresh_token)