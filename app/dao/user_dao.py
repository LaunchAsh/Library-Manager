from app import db
from app.models.user import User

def get_all_user():
    result = User.query.filter(
        User.is_active == True
    ).all()
    return result or None

def get_user_by_email(email):
    result = User.query.filter(
        User.email == email ,
        User.is_active == True
    ).all()
    return result or None

def get_user_by_id(id):
    result = User.query.filter(
        User.id == id ,
        User.is_active == True
    ).first()
    return result or None

def get_user_by_id_in_admin(id):
    result = User.query.filter(
        User.id == id 
    ).first()
    return result or None

def insert_user(id,name,email,password,phone,address,role_id):
    new_user = User(
        _id = id,
        _name = name,
        _email = email,
        _phone_number = phone,
        _password = password,
        _address = address,
        _role_id = role_id,
        _create_by = name,
        _modified_by = name
    )
    db.session.add(new_user)
    db.session.commit()
    
def update_user(id,name,email,phone,address):
    transaction_retrieved = User.query.filter(
        User.id == id,
        User.is_active == 1
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.name = name
        transaction_retrieved.email = email
        transaction_retrieved.phone_number = phone
        transaction_retrieved.address = address
        db.session.add(transaction_retrieved)
        db.session.commit()

def change_password_user(id,name,password):
    transaction_retrieved = User.query.filter(
        User.id == id,
        User.is_active == 1
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.password = password
        transaction_retrieved.modified_by = name
        db.session.add(transaction_retrieved)
        db.session.commit()

def update_user_by_admin(id,name,email,password,phone,address,role_id):
    transaction_retrieved = User.query.filter(
        User.id == id,
        User.is_active == 1
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.name = name
        transaction_retrieved.email = email
        transaction_retrieved.password = password
        transaction_retrieved.role_id = role_id
        transaction_retrieved.phone_number = phone
        transaction_retrieved.address = address
        db.session.add(transaction_retrieved)
        db.session.commit()

def delete_user_by_id(id):
    transaction_retrieved = User.query.filter(
        User.id == id,
        User.is_active == 1
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.is_active = False
        db.session.add(transaction_retrieved)
        db.session.commit()