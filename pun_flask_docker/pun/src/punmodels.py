from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pun(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pun_text = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, unique=True)

    def __init__(self, pun_text: str, user_id: int):
        self.pun_text = pun_text
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'pun_text': self.pun_text,
            'author': self.user_id
        }