import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "sqlite:///userinfo.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY='%N$E#ug)wh$55Pd'