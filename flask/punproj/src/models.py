from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pun(db.Model):
    __tablename__ = "puns"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pun_text = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)

    def __init__(self, pun_text: str, user_id: int):
        self.pun_text = pun_text
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'pun_text': self.pun_text,
            'author': self.user_id
        }
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, user_name: str, password: str):
        self.user_name = user_name
        self.password = password

    def serialize(self):
        return {
            'id': self.id,
            'user_name': self.user_name
        }
    

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, category_name: str):
        self.category_name = category_name

    def serialize(self):
        return {
            'id': self.id,
            'category_name': self.category_name
        }
    
puns_categories_table = db.Table(
    'puns_categories',
    db.Column(
        'pun_id', db.Integer,
        db.ForeignKey('puns.id'),
        primary_key=True
    ),

    db.Column(
        'category_id', db.Integer,
        db.ForeignKey('categories.id'),
        primary_key=True
    )
)