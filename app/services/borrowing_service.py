from app.dao import borrowing_dao , book_dao, user_dao
import uuid
import datetime
from firebase_admin import db


def get_all_borrowing():
    borrowings = borrowing_dao.get_all_borrowing()
    list_borrowing = []
    if borrowings :
        for borrowing in borrowings :
            detail = {
                "id": borrowing.id,
                "user_id": borrowing.user_id,
                "book_id": borrowing.book_id,
                "borrower_name": borrowing.borrower_name,
                "borrowed_date": borrowing.borrowed_date,
                "due_date": borrowing.due_date,
                "return_date": borrowing.returned_date
            }
            list_borrowing.append(detail)
    result = {"data" : list_borrowing}
    return result or None

def search_borrowing_by_user(payload,session):
    user_id = session.get("user_id")
    book_id = payload.get("book_id") or None 
    borrower_name = payload.get("borrower_name") or None 
    borrowed_date = payload.get("borrowing_date") or None
    due_date = payload.get("due_date") or None
    borrowings = borrowing_dao.search_borrowing(user_id,borrower_name,book_id,borrowed_date,due_date)
    list_borrowing = []
    if borrowings :
        for borrowing in borrowings :
            detail = {
                "id": borrowing.id,
                "user_id": borrowing.user_id,
                "book_id": borrowing.book_id,
                "borrower_name": borrowing.borrower_name,
                "borrowed_date": borrowing.borrowed_date,
                "due_date": borrowing.due_date,
                "return_date": borrowing.returned_date
            }
            list_borrowing.append(detail)
    result = {"data" : list_borrowing}
    return result or None

def search_borrowing_in_date(payload):
    date = payload.get("date") or None
    borrowings = borrowing_dao.get_borrowing_in_date(date)
    list_borrowing = []
    if borrowings : 
        for borrowing in borrowings :
            detail = {
                "id": borrowing.id,
                "user_id": borrowing.user_id,
                "book_id": borrowing.book_id,
                "borrower_name": borrowing.borrower_name,
                "borrowed_date": borrowing.borrowed_date,
                "due_date": borrowing.due_date,
                "return_date": borrowing.returned_date
            }
            list_borrowing.append(detail)
    result = {"data" : list_borrowing}
    return result or None

def check_borrowing(book_id):
    book = book_dao.get_book_by_id(book_id)
    if book is None : return False , "This book is not exist"
    elif book.is_borrowed == True : return False, "This book is borrrowed"
    else : return True , None 

def add_new_borrowing(payload,session):
    id = str(uuid.uuid4())
    user_id = session.get("user_id")
    book_id = payload.get("book_id")
    borrower_name = session.get("user_name")
    borrowed_date = payload.get("borrowed_date")
    due_date = payload.get("due_date")
    user_name = session.get("user_name")
    status, message =  check_borrowing(book_id) 
    if status is not True : return False , message
    if borrowing_dao.check_borrow_date(book_id,borrowed_date,due_date) : return False , "ERROR INVALID DATE"
    borrowing_dao.insert_borrowing(id,book_id,user_id,borrower_name,borrowed_date,due_date,user_name)
    save_borrow_in_firebase(id,book_id,user_id,borrower_name,borrowed_date,due_date)
    return True , "Successfully"

def save_borrow_in_firebase(id,book_id,user_id,borrower_name,borrowed_date,due_date):
    book = book_dao.get_book_by_id(book_id)
    ref = db.reference('borrows')
    data = {
    'id': id,
    'book_id': book_id,
    'user_id': user_id,
    'book_title': book.title,
    'book_image': book.image_path,
    'borrower_name': borrower_name,
    'borrowed_date':borrowed_date,
    'due_date': due_date,
    'is_status': 0
    }
    ref.push(data)


def check_give_book(payload,session):
    id = payload.get("id")
    user_name = session.get("user_name")
    book_id = payload.get("book_id")
    user_id = payload.get("user_id")
    borrowing_dao.check_give_book(id,user_name)
    book_dao.change_status_book(book_id)
    edit_borrow_in_firebase(id)

def check_return_book(payload,session):
    id = payload.get("id")
    book_id = payload.get("book_id")
    user_id = payload.get("user_id")
    user_name = session.get("user_name")
    return_date = datetime.date.today()
    borrow = borrowing_dao.get_borrowing_by_id(id)
    if borrow and borrow.returned_date != None : return False
    borrowing_dao.check_return_book(id,return_date,user_name)
    book_dao.change_status_book(book_id)
    defuse_borrow_in_firebase(id)
    return True

def delete_borrow_in_firebase(id):
    ref = db.reference('borrows')
    query = ref.order_by_child('id').equal_to(id)
    result = query.get()
    if result:
        for key in result.keys():
            ref.child(key).delete()

def defuse_borrow_in_firebase(id):
    ref = db.reference('borrows')
    query = ref.order_by_child('id').equal_to(id)
    result = query.get()

    if result:
        for key in result.keys():
            borrow_ref = ref.child(key)
            borrow_ref.update({'is_status': 1})

def edit_borrow_in_firebase(id):
    ref = db.reference('borrows')
    query = ref.order_by_child('id').equal_to(id)
    result = query.get()

    if result:
        for key in result.keys():
            borrow_ref = ref.child(key)
            borrow_ref.update({'is_status': 2})

def find_return_borrow_by_book_isbn(payload):
    book_isbn = payload.get("isbn")
    book = book_dao.get_book_by_isbn(book_isbn)
    today = datetime.date.today()
    if book is None : return False , None, 'THIS BOOK IS NOT EXIST'
    borrow = borrowing_dao.find_borrowing_by_book_id(book.id,today)
    if borrow is None : return False , None , 'THIS BOOK IS NOT BORROWED TODAY'
    if borrow.returned_date != None :  return False , None , 'THIS BORROWING IS RETURNED'
    user = user_dao.get_user_by_id_in_admin(borrow.user_id)
    if user is None : return False , None , 'THIS USER IS NOT EXIST'
    detail = {
            "id":borrow.id,
            "book_id": book.id,
            "book_image":book.image_path,
            "title":book.title,
            "quantity":book.quantity,
            "rating":book.rating,
            "isbn":book.isbn,
            "image_path":book.image_path,
            "description":book.description,
            "user_id": user.id,
            "user_name":user.name,
            "user_email":user.email,
            "user_phone":user.phone_number,
            "user_address":user.address,
            "borrowed_date": borrow.borrowed_date,
            "due_date": borrow.due_date,
            "return_date": borrow.returned_date,
            "is_given":borrow.is_given
        }
    result = {"data":detail}
    return True , result , None


def delete_borrowing(payload,session):
    id = payload.get("id")
    user_name = session.get("user_name")
    borrowing_dao.delete_borrowing(id,user_name)