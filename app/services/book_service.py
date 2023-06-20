from app.dao import book_dao
from app.dao import review_dao
from app.services import review_service
import uuid
import os
import base64
from PIL import Image
from io import BytesIO


def save_image(image,namefile):
    try: 
        image_name = namefile+'.png'
        path = os.path.join(os.getcwd(),'app','images',image_name)
        print(path)
        image.save(path)
        image_path = '/img/'+image_name
        return image_path
    except:
        return None
def convert_base64_to_image(base64_string):

    # Chuyển đổi base64 thành dữ liệu nhị phân
    image_data = base64.b64decode(base64_string)

    # Tạo đối tượng hình ảnh từ dữ liệu nhị phân
    image = Image.open(BytesIO(image_data))

    return image

def get_all_book():
    books = book_dao.get_all_book()
    list_of_books = []
    for book in books:
        book_detail = {
            "id":book.id,
            "title":book.title,
            "quantity":book.quantity,
            "rating":book.rating,
            "isbn":book.isbn,
            "image_path":book.image_path,
            "description":book.description
        }
        list_of_books.append(book_detail)
    result = {"data":list_of_books}
    return result or None

def search_book(payload):
    title = payload.get("title") or None
    rating = payload.get("rating") or None
    quantity = payload.get("quantity") or None
    mode = payload.get("mode") or None
    books = book_dao.search_books(title,quantity,rating,mode)
    list_of_books = []
    if books : 
        for book in books:
            book_detail = {
                "id":book.id,
                "title":book.title,
                "quantity":book.quantity,
                "rating":book.rating,
                "isbn":book.isbn,
                "image_path":book.image_path,
                "description":book.description
            }
            list_of_books.append(book_detail)
    result = {"data":list_of_books}
    return result or None

def get_book_by_id(payload):
    id = payload.get("id") or None
    book = book_dao.get_book_by_id(id)
    review_book = review_service.get_all_review_by_book_id(id)
    book_detail = []
    if book : 
        book_detail = {
            "id":book.id,
            "title":book.title,
            "quantity":book.quantity,
            "rating":book.rating,
            "isbn":book.isbn,
            "image_path":book.image_path,
            "description":book.description,
            "reviews": review_book or None
        }
    result = {"data": book_detail}
    return result or None

def check_isbn_book(isbn):
    books = book_dao.get_all_book()
    for book in books :
        if book.isbn == isbn : return False
    return True

def insert_new_book(payload,session):
    id = str(uuid.uuid4())
    title = payload.get("title") or None
    isbn = payload.get("isbn") or None
    quantity = int(payload.get("quantity")) or None
    rating = float(payload.get("rating")) or None
    string_base64 = payload.get("image") or None
    image = convert_base64_to_image(string_base64)
    image_path = save_image(image,id)
    description = payload.get("description")
    user_name = session.name
    if check_isbn_book(isbn) is not True : return False , "Code of book is existed"
    book_dao.insert_book(id,title,isbn,quantity,rating,image_path,description,user_name)
    return True , "Successfully"

def edit_book(payload,session):
    id = payload.get("id") or None
    title = payload.get("title") or None
    isbn = payload.get("isbn") or None
    quantity = int(payload.get("quantity")) or None
    rating = float(payload.get("rating")) or None
    string_base64 = payload.get("image") or None
    image = convert_base64_to_image(string_base64) 
    image_path = save_image(image,id)
    description = payload.get("description") or None
    user_name = session.name or None
    book_dao.update_book(id,title,isbn,quantity,rating,image_path,description,user_name)
    return True , "Successfully"


def delete_book_by_id(payload,session):
    user_name = session.name
    book_id = payload.get("id") or None
    return book_dao.delete_book_by_id(book_id,user_name)
    
