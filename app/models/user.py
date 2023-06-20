from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app import db
from flask_serialize import FlaskSerialize
fs_mixin = FlaskSerialize(db)

class User(db.Model):

    __tablename__ = 'users'
    _id = db.Column('id', db.String(50), primary_key=True)
    _name = db.Column('name', db.String(255))
    _email = db.Column('email', db.String(255),unique=True)
    _password = db.Column('password', db.String(255))
    _role_id = db.Column('role_id', db.Integer)
    _phone_number = db.Column('phone_number', db.String(20), unique=True)
    _address = db.Column('address', db.String(255))
    _create_by = db.Column('create_by', db.String(255))
    _create_date = db.Column('create_date', db.TIMESTAMP,default=datetime.utcnow())
    _modified_by = db.Column('modified_by', db.String(255))
    _modified_date = db.Column('modified_date', db.TIMESTAMP,default=datetime.utcnow(),onupdate = datetime.utcnow)
    _is_active = db.Column('is_active', db.Boolean , default = True)

    @hybrid_property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_):
        self._id = id_

    @hybrid_property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @hybrid_property
    def role_id(self):
        return self._role_id

    @role_id.setter
    def role_id(self, role_id):
        self._role_id = role_id

    @hybrid_property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        self._phone_number = phone_number

    @hybrid_property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

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
        return {"id":self.id , "name": self.name , "email":self.email }