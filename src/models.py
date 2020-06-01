from src import db
from flask_sqlalchemy import SQLAlchemy

class Entry(db.Model):
    __bind_key__ = "userinfo"
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)

class Entry_Temp(db.Model):
    __bind_key__ = "temp_user"
    __tablename__ = "temp_user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text(), nullable=False)
    auth_uuid = db.Column(db.Text(), nullable=False)

def init_db():
    db.create_all()