from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app import db
from flask_serialize import FlaskSerialize
fs_mixin = FlaskSerialize(db)

class Borrowing(db.Model):

    __tablename__ = 'borrowings'
    _id = db.Column('id', db.String(50), primary_key=True)
    _book_id = db.Column('book_id', db.String(50))
    _user_id = db.Column('user_id', db.String(50))
    _borrower_name = db.Column('borrower_name', db.String(255))
    _is_given = db.Column('is_given', db.Boolean, default = False)
    _borrowed_date = db.Column('borrowed_date', db.Date)
    _due_date = db.Column('due_date', db.Date)
    _returned_date = db.Column('returned_date', db.Date)
    _create_by = db.Column('create_by', db.String(255))
    _create_date = db.Column('create_date', db.TIMESTAMP , default=datetime.utcnow())
    _modified_by = db.Column('modified_by', db.String(255))
    _modified_date = db.Column('modified_date', db.TIMESTAMP, default=datetime.utcnow(),onupdate = datetime.utcnow)
    _is_active = db.Column('is_active', db.Boolean , default = True)

    @hybrid_property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_):
        self._id = id_

    @hybrid_property
    def book_id(self):
        return self._book_id

    @book_id.setter
    def name(self, book_id):
        self._book_id = book_id

    @hybrid_property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    @hybrid_property
    def borrower_name(self):
        return self._borrower_name

    @borrower_name.setter
    def borrower_name(self, borrower_name):
        self._borrower_name = borrower_name

    @hybrid_property
    def borrowed_date(self):
        return self._borrowed_date

    @borrowed_date.setter
    def borrowed_date(self, borrowed_date):
        self._borrowed_date = borrowed_date
    
    @hybrid_property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, due_date):
        self._due_date = due_date
    
    @hybrid_property
    def returned_date(self):
        return self._returned_date

    @returned_date.setter
    def returned_date(self, returned_date):
        self._returned_date = returned_date

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

    @hybrid_property
    def is_given(self):
        return self._is_given

    @is_given.setter
    def is_given(self, is_given):
        self._is_given = is_given

    def __repr__(self):
        return '<id - book_id - user_id : {} - {} - {} >'.format(self.id, self.book_id, self.user_id)