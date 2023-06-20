from app import db
from app.models.review import Review
from sqlalchemy import func

def get_all_review():
    result = Review.query.filter(
        Review.is_active == 1
    ).all()
    return result or None

def get_review_by_book_id(book_id):
    result = Review.query.filter(
        Review.book_id == book_id,
        Review.is_active == 1
    ).all()
    return result or None

def get_review_by_user_id(user_id):
    result = Review.query.filter(
        Review.user_id == user_id,
        Review.is_active == 1
    ).all()
    return result or None

def calculate_average_rating(book_id):
    average_rating = db.session.query(func.avg(Review._rating)).filter(Review._book_id == book_id).scalar()
    return average_rating if average_rating else 0 

def insert_review(id_,book_id_,user_id_,rating_,comment_,user_name):
    new_review = Review(
        _id = id_,
        _book_id = book_id_,
        _user_id = user_id_,
        _rating = rating_,
        _comment = comment_,
        _create_by = user_name,
        _modified_by = user_name
    )
    db.session.add(new_review)
    db.session.commit()

def delete_review_by_id(id,user_id):
    transaction_retrieved = Review.query.filter(
        Review.id == id,
        Review.user_id == user_id,
        Review.is_active == 1
    ).first()
    if transaction_retrieved is not None:
        transaction_retrieved.is_active = False
        db.session.add(transaction_retrieved)
        db.session.commit()