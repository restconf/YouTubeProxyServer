import os
import hashlib
import uuid
import flask
import requests
from flask import request, session
from os.path import join, dirname
from dotenv import load_dotenv
from src import models, app, YouTube, Email, pytube_patch
import pytube

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
    query = models.Registered_User.query.filter_by(
        user_name=request.form['user_name'])
    if query.count() == 1:
        if query.first().password == hashlib.sha256(
                request.form["password"].encode()).hexdigest():
            session['user_name'] = request.form['user_name']
            return flask.redirect("/")
    return flask.redirect('/login')


@app.route("/login", methods=["GET"])
def login():
    if 'user_name' in session:
        return flask.redirect("/")
    return flask.render_template('login.html')


@app.route("/logout_manager", methods=["POST"])
def logout_manager():
    # Delete Cookie that shows server they are logged in
    session.pop('user_name', None)
    # redirect main Page
    return flask.redirect("/")


@app.route("/search", methods=["GET"])
def search():
    if 'user_name' in session:
        # Request Google YouTube API for getting video information
        search_query = request.args.get("search_query")
        result_amount = 5
        api_response = requests.get(
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={search_query}&maxResults={result_amount}&key={YOUTUBEAPIKEY}").text
        yt = YouTube.YouTube(api_response)
        return flask.render_template('result.html', list=yt.get_id_and_thumbnail())
    # if they aren't logged in
    return flask.redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    # if this is requested by POST
    if request.method == "POST":
        if models.Registered_User.query.filter_by(user_name=request.form['user_name']).count() == 0:
            UUID = str(uuid.uuid4())
            temp_user = models.Temp_User(
                user_name=request.form['user_name'], auth_uuid=UUID)
            models.db.session.add(temp_user)
            models.db.session.commit()
            Email.send_mail(Email.create_message(
                f"https://you-tube-proxy.herokuapp.com/validate?uuid={UUID}&user_name={request.form['user_name']}&password={request.form['password']}"))
            return flask.redirect("/login")
        else:
            # if the same account name already exists
            return flask.render_template('register.html', errormsg="Try Another Name")
    # if this is requested by GET
    elif request.method == "GET":
        return flask.render_template('register.html')


@app.route("/admin", methods=["GET"])
def admin_operate():
    if 'user_name' in session:
        if session["user_name"] == "admin":
            return flask.render_template('admin.html')
    return flask.redirect('/login')


@app.route("/delete_accounts", methods=["POST"])
def admin_operate_delete():
    if 'user_name' in session:
        if session["user_name"] == "admin":
            models.Registered_User.query.delete()
            models.Temp_User.query.delete()
            admin = models.Registered_User(user_name="admin",
                                           password=hashlib.sha256(os.environ.get("ADMINPASS").encode()).hexdigest())
            models.db.session.add(admin)
            models.db.session.commit()
            return flask.redirect('/login')
    return flask.redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return flask.render_template('500.html'), 500


@app.route("/validate", methods=["GET"])
def find_temp_user():
    uuid = request.args.get("uuid")
    name = request.args.get("user_name")
    password = request.args.get("password")
    query = models.Temp_User.query.filter_by(user_name=name)
    if query.count() == 1 and query.first().auth_uuid == uuid:
        new_user_info = models.Registered_User(
            user_name=name, password=hashlib.sha256(password.encode()).hexdigest())
        models.db.session.add(new_user_info)
        models.db.session.commit()
        return flask.redirect('/login')


@app.route("/watch", methods=["GET"])
def watch():
    video_id = request.args.get("video_id")
    thum_url = request.args.get("thum_url")
    if 'user_name' in session:
        return flask.render_template('watch.html', video_id=video_id, thum_url=thum_url)


@app.route("/find_url_by_id/<video_id>", methods=["GET"])
def find_url_by_id(video_id):
    itag_720p = 22
    itag_360p = 18
    itag_240p = 36
    itag_144p = 17
    pytube.__main__.apply_descrambler = pytube_patch.apply_descrambler
    yt = pytube.YouTube(f"https://www.youtube.com/watch?v={video_id}")
    try:
        url = yt.streams.get_by_itag(itag_144p).url
    except AttributeError:
        url = yt.streams.get_by_itag(itag_360p).url
    return url
