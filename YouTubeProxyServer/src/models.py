from src import db
from flask_sqlalchemy import SQLAlchemy


# class Entry(db.Model):
#     # __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     user_name = db.Column(db.Text, primary_key=True)
#     password= db.Column(db.Text, primary_key=True)
#
#     def __repr__(self):
#         return f"<Entry user_name={self.user_name} password={self.password}>"
#
#
# def init():
#     db.create_all()

class Entry(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)

def init_db():
    db.create_all()