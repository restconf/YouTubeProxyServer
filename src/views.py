import os
import hashlib
import json
import flask
import requests
from flask import request, session
from os.path import join, dirname
from dotenv import load_dotenv
from src import models, app, YouTube

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

YOUTUBEAPIKEY = os.environ.get("YOUTUBEAPIKEY")

@app.route('/')
def show_entries():
    if 'user_name' in session:
        return flask.render_template('root.html')
    # if they aren't logged in
    return flask.render_template('login.html')


@app.route("/login_manager", methods=["POST"])
def login_manager():
    if models.Entry.query.filter_by(user_name=request.form['user_name']).first().password == hashlib.sha256(
            request.form["password"].encode()).hexdigest():
        session['user_name'] = request.form['user_name']
        return flask.render_template('root.html')
    return flask.render_template('login.html')


@app.route("/logout_manager", methods=["POST"])
def logout_manager():
    # Delete Cookie that shows server they are logged in
    session.pop('user_name', None)
    # redirect main Page
    return flask.render_template('login.html')


@app.route("/search", methods=["POST"])
def search():
    if 'user_name' in session:
        # Request Google YouTube API for getting video information
        api_response = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={request.form['keyword']}&maxResults=15&key={YOUTUBEAPIKEY}").text
        yt = YouTube.YouTube(api_response)
        return flask.render_template('movie.html', links=yt.get_ids())
    # if they aren't logged in
    return flask.render_template('login.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    # if this is requested by POST
    if request.method == "POST":
        if models.Entry.query.filter_by(user_name=request.form['user_name']).count() == 0:
            user = models.Entry(user_name=request.form['user_name'],
                                password=hashlib.sha256(request.form['password'].encode()).hexdigest())
            models.db.session.add(user)
            models.db.session.commit()
            return flask.render_template('login.html')
        else:
            # if the same account name already exists
            return flask.render_template('register.html')
    # if this is requested by GET
    elif request.method == "GET":
        return flask.render_template('register.html')


@app.route("/admin", methods=["GET"])
def admin_operate():
    if 'user_name' in session:
        if session["user_name"] == "admin":
            return flask.render_template('admin.html')
    return flask.render_template('login.html')


@app.route("/delete_accounts", methods=["POST"])
def admin_operate_delete():
    if 'user_name' in session:
        if session["user_name"] == "admin":
            models.Entry.query.delete()
            user = models.Entry(user_name="admin",
                                password=hashlib.sha256(os.environ.get("ADMINPASS").encode()).hexdigest())
            models.db.session.add(user)
            models.db.session.commit()
            return flask.render_template('login.html')
    return flask.render_template('login.html')
