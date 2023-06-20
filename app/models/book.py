from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app import db
from flask_serialize import FlaskSerialize
fs_mixin = FlaskSerialize(db)

class Book(db.Model):

    __tablename__ = 'books'
    _id = db.Column('id', db.String(50), primary_key=True)
    _title = db.Column('title', db.String(255))
    _author_id = db.Column('author_id', db.String(50))
    _publisher_id = db.Column('publisher_id', db.String(50))
    _isbn = db.Column('isbn', db.String(50))
    _quantity = db.Column('quantity', db.Integer)
    _rating = db.Column('rating', db.Float)
    _image_path = db.Column('image_path', db.String(255))
    _is_borrowed = db.Column('is_borrowed', db.Boolean , default = False)
    _description = db.Column('description', db.Text)
    _create_by = db.Column('create_by', db.String(255))
    _create_date = db.Column('create_date', db.TIMESTAMP , default=datetime.utcnow())
    _modified_by = db.Column('modified_by', db.String(255))
    _modified_date = db.Column('modified_date', db.TIMESTAMP , default=datetime.utcnow(),onupdate = datetime.utcnow)
    _is_active = db.Column('is_active', db.Boolean , default = True)

    @hybrid_property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_):
        self._id = id_

    @hybrid_property
    def title(self):
        return self._title

    @title.setter
    def title(self, title_):
        self._title = title_
    
    @hybrid_property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, author_id):
        self._author_id = author_id
    
    @hybrid_property
    def publisher_id(self):
        return self._publisher_id

    @publisher_id.setter
    def publisher_id(self, publisher_id):
        self._publisher_id = publisher_id

    @hybrid_property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, isbn):
        self._isbn = isbn

    @hybrid_property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity

    @hybrid_property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        self._rating = rating

    @hybrid_property
    def image_path(self):
        return self._image_path

    @image_path.setter
    def image_path(self, image_path):
        self._image_path = image_path
    
    @hybrid_property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description
    

    @hybrid_property
    def is_borrowed(self):
        return self._is_borrowed

    @is_borrowed.setter
    def is_borrowed(self, is_borrowed):
        self._is_borrowed = is_borrowed


    @hybrid_property
    def create_by(self):
        return self._create_by

    @create_by.setter
    def create_by(self, create_by):
        self._create_by = create_by

    @hybrid_property
    def create_date(self):
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        self._create_date = create_date

    @hybrid_property
    def modified_by(self):
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        self._modified_by = modified_by

    @hybrid_property
    def modified_date(self):
        return self._modified_date

    @modified_date.setter
    def modified_date(self, modified_date):
        self._modified_date = modified_date

    @hybrid_property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        self._is_active = is_active

    def __repr__(self):
        return '<id - title: {} - {}>'.format(self.id, self.title)