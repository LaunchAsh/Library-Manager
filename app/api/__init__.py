from flask import Flask
from app import login_manager
from app.api import notify
from app.api import authorize_api
from app.api import image_api
from app.api import book_api
from app.api import review_api
from app.api import user_api
from app.api import borrowing_api
from app.models.user import User

def register_blueprints(app: Flask):
    app.register_blueprint(notify.bp, url_prefix='/api')
    app.register_blueprint(authorize_api.bp, url_prefix='/auth')
    app.register_blueprint(image_api.bp, url_prefix='/img')
    app.register_blueprint(book_api.bp, url_prefix='/bok')
    app.register_blueprint(review_api.bp, url_prefix='/rev')
    app.register_blueprint(user_api.bp, url_prefix='/acc')
    app.register_blueprint(borrowing_api.bp, url_prefix='/borrow')

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

import app.dao.admin