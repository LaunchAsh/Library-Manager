from app.dao import user_dao, role_dao
import uuid
import os
import string
import re

def check_password(password):
    # Kiểm tra độ dài mật khẩu
    if len(password) < 8 or len(password) > 50:
        return False
    
    # Kiểm tra xem mật khẩu chỉ chứa chữ và số
    if not re.match("^[a-zA-Z0-9]+$", password):
        return False
    
    return True

def check_email(email):
    users = user_dao.get_all_user()
    for user in users :
        if user.email == email : return True
    return False

def get_all_user():
    users = user_dao.get_all_user()
    list_of_users = []
    for user in users :
        role = role_dao.get_role_by_id(user.role_id)
        detail = {
            "id" : user.id,
            "name" : user.name,
            "email": user.email,
            "password": user.password,
            "role": role.name or None,
            "phone_number": user.phone_number,
            "address" : user.address
        }
        list_of_users.append(detail)
    result = {"data": list_of_users}
    return result or None

def get_user_by_id(payload):
    id = payload.get("user_id")
    user = user_dao.get_user_by_id(id)
    role = role_dao.get_role_by_id(user.role_id)
    detail = {
            "id" : user.id,
            "name" : user.name,
            "email": user.email,
            "password": user.password,
            "role" : role.name or None,
            "phone_number": user.phone_number,
            "address" : user.address
        }
    result = {"data": detail}
    return result or None 

def insert_user(payload,role_id):
    id = str(uuid.uuid4())
    name = payload.get("name")
    email = payload.get("email")
    password = payload.get("password")
    role = role_id if role_id else payload.get("role_id")
    phone = payload.get("phone_number")
    address = payload.get("address")
    users = user_dao.get_user_by_email(email)
    if check_email(email) : return False , "Email is existed"
    if check_password(password) is not True : return False , "Invalid password."
    if users : 
        return False , "Account is existed"
    else : 
        user_dao.insert_user(id,name,email,password,phone,address,role)
        return True , "Successfully"


def change_info_user(payload):
    id = payload.get("id")
    name = payload.get("name")
    email = payload.get("email")
    password = payload.get("password")
    role = payload.get("role_id")
    phone = payload.get("phone_number")
    address = payload.get("address")
    if check_password(password) is not True: return False , "Invalid password."
    user_dao.update_user_by_admin(id,name,email,password,phone,address,role)
    return True , "Successfully"

def change_my_info(payload,session):
    id = session.get("user_id")
    name = payload.get("name")
    email = payload.get("email")
    phone = payload.get("phone_number")
    address = payload.get("address")
    user_dao.update_user(id,name,email,phone,address)

def change_password(payload,session):
    id = session.get("user_id")
    name = session.get("user_name")
    password  = payload.get("password")
    print(password)
    if check_password(password) is not True : return False , "Invalid password."
    user_dao.change_password_user(id,name,password)
    return True , "Successfully"

def delete_user(payload):
    id  = payload.get("user_id")
    user_dao.delete_user_by_id(id)
