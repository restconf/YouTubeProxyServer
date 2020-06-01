from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '%N$E#ug)wh$55Pd'
app.config.from_object('src.config')
db = SQLAlchemy(app)
import src.views