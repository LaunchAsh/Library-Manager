from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from app import db
from flask_serialize import FlaskSerialize
fs_mixin = FlaskSerialize(db)

class Role(db.Model):

    __tablename__ = 'roles'
    _id = db.Column('id', db.String(50), primary_key=True)
    _name = db.Column('name', db.String(255))
    _is_active = db.Column('is_active', db.Boolean , default=True)

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
    def name(self, name_):
        self._name = name_

    @hybrid_property
    def is_active(self):
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        self._is_active = is_active
