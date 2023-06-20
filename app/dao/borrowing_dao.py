from app import db
from app.models.borrowing import Borrowing
from datetime import timedelta
from datetime import datetime
from datetime import datetime, date

def get_all_borrowing():
    result = Borrowing.query.filter(
        Borrowing.is_active == 1
    ).all()
    return result or None

def get_borrowing_by_id(id):
    result = Borrowing.query.filter(
        Borrowing.id == id,
        Borrowing.is_active == 1
    ).first()
    return result or None

def get_borrowing_by_book_id(book_id):
    result = Borrowing.query.filter(
        Borrowing.book_id == book_id,
        Borrowing.returned_date == None,
        Borrowing.is_active == 1
    ).first()
    return result or None

def find_borrowing_by_book_id(book_id,today):
    result = Borrowing.query.filter(
        Borrowing.book_id == book_id,
        Borrowing.borrowed_date <= today,
        Borrowing.due_date >= today,
        Borrowing.returned_date == None,
        Borrowing.is_active == 1
    ).first()
    return result or None

def search_borrowing(user_id,borrow_name,book_id,borrowed_date,due_date):
    borrow_date = datetime.strptime(borrowed_date, "%Y-%m-%d").date()
    result = Borrowing.query.filter(
        Borrowing.borrower_name.ilike(f"%{borrow_name}%"),
        Borrowing.book_id.ilike(f"%{book_id}%"),
        Borrowing.user_id.ilike(f"%{user_id}%"),
        Borrowing.borrowed_date == borrow_date,
        Borrowing.due_date == due_date,
        Borrowing.is_active == 1
    ).all()
    return result or None

def get_borrowing_in_date(date):
    date = datetime.strptime(date, "%Y-%m-%d").date()
    result = Borrowing.query.filter(
        Borrowing.borrowed_date == date,
        Borrowing.returned_date.is_(None),
        Borrowing.is_active == 1
    ).all()
    return result or None

def insert_borrowing(id,book_id,user_id,borrower_name,borrowed_date,due_date,user_name):
    new_borrowing = Borrowing(
        _id = id,
        _book_id = book_id,
        _user_id = user_id,
        _borrower_name = borrower_name,
        _borrowed_date = borrowed_date,
        _due_date = due_date,
        _create_by = user_name,
        _modified_by = user_name
    )
    db.session.add(new_borrowing)
    db.session.commit()

def check_give_book(id,user_name):
    transaction_retrieved = Borrowing.query.filter(
        Borrowing.id == id,
        Borrowing.is_active == 1,
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.is_given = True
        transaction_retrieved.modified_by = user_name
        db.session.add(transaction_retrieved)
        db.session.commit()


def check_borrow_date(book_id, borrowed_date, due_date):
    borrowed_date = datetime.strptime(borrowed_date, "%Y-%m-%d").date()
    due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    start_date = datetime.combine(borrowed_date, datetime.min.time())
    end_date = datetime.combine(due_date, datetime.max.time())

    transaction_retrieved = Borrowing.query.filter(
        Borrowing.book_id == book_id,
        Borrowing.returned_date == None,
        Borrowing.is_active == 1
    ).all()

    for borrow in transaction_retrieved:
        if (borrow.borrowed_date <= end_date.date() and borrow.due_date >= start_date.date()) or \
           (start_date.date() <= borrow.due_date and end_date.date() >= borrow.borrowed_date):
            return True

    return False
def check_return_book(id,return_date,user_name):
    transaction_retrieved = Borrowing.query.filter(
        Borrowing.id == id,
        Borrowing.is_active == 1
    ).first()
    print(return_date)
    if transaction_retrieved is not None:
        transaction_retrieved.is_given = False
        transaction_retrieved.returned_date = return_date
        transaction_retrieved.modified_by = user_name
        db.session.add(transaction_retrieved)
        db.session.commit()

def delete_borrowing(id,user_name):
    transaction_retrieved = Borrowing.query.filter(
        Borrowing.id == id,
        Borrowing.is_active == 1
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.is_active = False
        db.session.add(transaction_retrieved)
        db.session.commit()