from app import db
from app.models.book import Book

def get_all_book():
    result = Book.query.filter(
        Book.is_active == 1
    ).all()
    return result or None

def get_book_by_id(id):
    result = Book.query.filter(
        Book.id == id,
        Book.is_active == 1
    ).first()
    return result or None

def get_book_by_id_in_admin(id):
    result = Book.query.filter(
        Book.id == id
    ).first()
    return result or None

def get_all_book_by_user():
    result = Book.query.filter(
        Book.is_active == 1
    ).all()
    return result or None

def search_name_books(query):
    result = Book.queryfilter(
        Book.is_active == 1,
        Book.title.ilike(f"%{query}%")
    ).all()
    return result or None

def search_books(title, quantity, rating, mode):
    query = Book.query.filter(Book.is_active == 1,Book.is_borrowed == 0)

    if title is not None:
        query = query.filter( Book.title.ilike(f"%{title}%"))

    if quantity is not None:
        query = query.filter(Book.quantity == quantity)

    if rating is not None:
        query = query.filter(round(Book.rating) == rating)

    if mode == 0 or mode is None: 
        query = query.order_by(Book.modified_date.desc())
    elif mode == 1:
        query = query.order_by(Book.rating.desc())
    elif mode == 2:
        query = query.order_by(Book.quantity.desc())

    result = query.all()
    return result or None

def get_book_by_isbn(isbn):
    result = Book.query.filter(
        Book.is_active == 1,
        Book.isbn == isbn
    ).first()
    return result or None

def update_book(id,_title,_isbn,_quantity,_rating,_image_path,_description,user_name):
    transaction_retrieved = Book.query.filter(
        Book.id == id,
        Book.is_active == 1
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.title = _title if _title else transaction_retrieved.title
        transaction_retrieved.isbn = _isbn if _isbn else transaction_retrieved.isbn
        transaction_retrieved.quantity = _quantity if _quantity else transaction_retrieved.quantity
        transaction_retrieved.rating = _rating if _rating else transaction_retrieved.rating
        transaction_retrieved.image_path = _image_path if _image_path else transaction_retrieved.image_path
        transaction_retrieved.description = _description if _description else transaction_retrieved.description
        transaction_retrieved.modified_by = user_name
        db.session.add(transaction_retrieved)
        db.session.commit()

def change_status_book(id):
    transaction_retrieved = Book.query.filter(
        Book.id == id,
        Book.is_active == 1
    ).first()
    status_book = not transaction_retrieved.is_borrowed
    if transaction_retrieved is not None:
        transaction_retrieved.is_borrowed = status_book
        db.session.add(transaction_retrieved)
        db.session.commit()

def update_rating_book(id,rate_avg):
    transaction_retrieved = Book.query.filter(
        Book.id == id,
        Book.is_active == 1
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.rating = rate_avg
        db.session.add(transaction_retrieved)
        db.session.commit()

def insert_book(id_,title_,isbn_,quantity_,rating_,image_path_,description_,user_name):
    new_book = Book(
        _id = id_,
        _title = title_,
        _isbn = isbn_,
        _quantity = quantity_,
        _rating = rating_,
        _image_path = image_path_,
        _description = description_,
        _create_by = user_name,
        _modified_by = user_name)
    db.session.add(new_book)
    db.session.commit()

def delete_book_by_id(id,user_name):
    transaction_retrieved = Book.query.filter(
        Book.id == id
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.is_active = False
        transaction_retrieved.modified_by = user_name
        db.session.add(transaction_retrieved)
        db.session.commit()