
from datetime import datetime
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from config import bcrypt 

db=SQLAlchemy()

class Note(db.Model,SerializerMixin):

    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def note_serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S') if self.date else None
            }

   
    def __repr__(self):
        return f'<Note {self.id} {self.title}{self.content} {self.tags}{self.date}>'
class User(db.Model,SerializerMixin):
    __tablename__='users'

    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,nullable=False)
    _password_hash=db.Column(db.String,nullable=False)


    @hybrid_property
    def password_hash(self):
        raise AttributeError("Cannot access password")
    @password_hash.setter
    def password_hash(self,password):
        password_hash=bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash=password_hash.decode('utf-8')

    def authenticate(self,password):
        return bcrypt.check_password_hash(self._password_hash.encode('utf-8'), password.encode('utf-8'))


