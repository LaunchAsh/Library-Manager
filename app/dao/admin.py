from app import db, admin
from app.models.author import Author
from app.models.book import Book
from app.models.borrowing import Borrowing
from app.models.category import Category
from app.models.publisher import Publisher
from app.models.review import Review
from app.models.role import Role
from app.models.token import Token
from app.models.user import User

from flask_admin.contrib.sqla import ModelView
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Borrowing, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Publisher, db.session))
admin.add_view(ModelView(Review, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Token, db.session))
admin.add_view(ModelView(Author, db.session))
