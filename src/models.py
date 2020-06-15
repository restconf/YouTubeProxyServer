from src import db
from flask_sqlalchemy import SQLAlchemy

class Registered_User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)

class Temp_User(db.Model):
    __tablename__ = "temp_user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text(), nullable=False)
    auth_uuid = db.Column(db.Text(), nullable=False)

def init_db():
    db.create_all()