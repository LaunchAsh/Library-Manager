from app.dao import review_dao , user_dao,book_dao
from app.classify import rating_for_comment
import uuid
import os

def get_all_review_by_book_id(book_id):
    reviews = review_dao.get_review_by_book_id(book_id)
    list_review = []
    order = 0 
    if reviews :
        for review in reviews:
            user = user_dao.get_user_by_id(review.user_id)
            detail = {
                "order":order,
                "id":review.id,
                "book_id":review.book_id,
                "user_name": "Anonymous" if not user else user.name,
                "rating": review.rating,
                "comment":review.comment
            }
            order+=1
            list_review.append(detail)
    result = list_review
    return result or None

def get_review_by_book_id(payload):
    book_id = payload.get("book_id")
    reviews = review_dao.get_review_by_book_id(book_id)
    list_review = []
    order = 0 
    if reviews :
        for review in reviews:
            user = user_dao.get_user_by_id(review.user_id)
            detail = {
                "order":order,
                "id":review.id,
                "book_id":review.book_id,
                "user_name": "Anonymous" if not user else user.name,
                "rating": review.rating,
                "comment":review.comment
            }
            order+=1
            list_review.append(detail)
    result = {"data":list_review}
    return result or None

def add_new_review(payload,session):
    id = str(uuid.uuid4())
    book_id = payload.get("book_id")
    user_id = session.get("user_id")
    user_name = session.get("user_name")
    comment = payload.get("comment")
    rating = rating_for_comment(comment)
    review_dao.insert_review(id,book_id,user_id,rating,comment,user_name)
    review_avg = review_dao.calculate_average_rating(book_id)
    book_dao.update_rating_book(book_id,review_avg)

def delete_review(payload,session):
    id = payload.get("id")
    user_id = session.get("user_id")
    review_dao.delete_review_by_id(id,user_id)