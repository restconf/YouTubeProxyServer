import os

SQLALCHEMY_DATABASE_URI_1 = os.environ.get('DATABASE_URL') or "sqlite:///userinfo.db"
SQLALCHEMY_DATABASE_URI_2 = os.environ.get('DATABASE_URL') or "sqlite:///tempuser.db"
SQLALCHEMY_BINDS = {"userinfo":SQLALCHEMY_DATABASE_URI_1, "temp_user":SQLALCHEMY_DATABASE_URI_2}
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY='%N$E#ug)wh$55Pd'