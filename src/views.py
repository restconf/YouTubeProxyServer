import datetime
import os
from pytube import YouTube
import hashlib
import json
import flask
import requests
from flask import request
from flask import session
from os.path import join, dirname
from dotenv import load_dotenv
from src import models
from src import app

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YOUTUBEAPIKEY = os.environ.get("YOUTUBEAPIKEY")
PASSWORDHASH = os.environ.get("PASSWORDHASH")
TESTHASH = os.environ.get("TESTHASH")

@app.route('/')
def show_entries():
    if 'user_name' in session:
        return flask.render_template('root.html')
    return flask.render_template('login.html')

@app.route("/login_manager", methods=["POST"])
def login_manager():
    if models.Entry.query.filter_by(user_name=request.form['user_name']).first().password == hashlib.sha256(request.form["password"].encode()).hexdigest():
        session['user_name'] = request.form['user_name']
        return flask.render_template('root.html')
    return "That account is not registered"

@app.route("/logout_manager", methods=["POST"])
def logout_manager():
    session.pop('user_name', None)
    return flask.render_template('login.html')

@app.route("/search", methods=["POST"])
def search():
    if 'user_name' in session:
        api_response = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={request.form['keyword']}&key={YOUTUBEAPIKEY}").text
        return flask.render_template('movie.html', link=get_url(api_response))
    return flask.render_template('login.html')

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        if models.Entry.query.filter_by(user_name=request.form['user_name']).count() == 0:
            user = models.Entry(user_name=request.form['user_name'], password=hashlib.sha256(request.form['password'].encode()).hexdigest())
            models.db.session.add(user)
            models.db.session.commit()
            return flask.render_template('login.html')
        else:
            return flask.render_template('register.html')
    else:
        return flask.render_template('register.html')

def get_url(response:str):
    try:
        jsonObj = json.loads(response)
        link = YouTube(f"https://www.youtube.com/watch?v={jsonObj['items'][0]['id']['videoId']}")
    except:
        get_url(response)
    return link.streams.get_by_itag(18).url
