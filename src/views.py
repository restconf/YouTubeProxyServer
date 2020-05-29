import datetime
import os
from pytube import YouTube, extract
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
            f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={request.form['keyword']}&maxResults=10&key={YOUTUBEAPIKEY}").text
        return flask.render_template('movie.html', link=get_url(api_response))
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

# These will remove after pytube updates
import urllib
from typing import Dict

def custom_apply_descrambler(stream_data: Dict, key: str) -> None:
    """Apply various in-place transforms to YouTube's media stream data.

    Creates a ``list`` of dictionaries by string splitting on commas, then
    taking each list item, parsing it as a query string, converting it to a
    ``dict`` and unquoting the value.

    :param dict stream_data:
        Dictionary containing query string encoded values.
    :param str key:
        Name of the key in dictionary.

    **Example**:

    >>> d = {'foo': 'bar=1&var=test,em=5&t=url%20encoded'}
    >>> apply_descrambler(d, 'foo')
    >>> print(d)
    {'foo': [{'bar': '1', 'var': 'test'}, {'em': '5', 't': 'url encoded'}]}

    """
    otf_type = "FORMAT_STREAM_TYPE_OTF"

    if key == "url_encoded_fmt_stream_map" and not stream_data.get(
            "url_encoded_fmt_stream_map"
    ):
        formats = json.loads(stream_data["player_response"])["streamingData"]["formats"]
        formats.extend(
            json.loads(stream_data["player_response"])["streamingData"][
                "adaptiveFormats"
            ]
        )
        try:
            stream_data[key] = [
                {
                    "url": format_item["url"],
                    "type": format_item["mimeType"],
                    "quality": format_item["quality"],
                    "itag": format_item["itag"],
                    "bitrate": format_item.get("bitrate"),
                    "is_otf": (format_item.get("type") == otf_type),
                }
                for format_item in formats
            ]
        except KeyError:
            cipher_url = []
            for data in formats:
                cipher = data.get("cipher") or data["signatureCipher"]
                cipher_url.append(urllib.parse.parse_qs(cipher))
            stream_data[key] = [
                {
                    "url": cipher_url[i]["url"][0],
                    "s": cipher_url[i]["s"][0],
                    "type": format_item["mimeType"],
                    "quality": format_item["quality"],
                    "itag": format_item["itag"],
                    "bitrate": format_item.get("bitrate"),
                    "is_otf": (format_item.get("type") == otf_type),
                }
                for i, format_item in enumerate(formats)
            ]
    else:
        stream_data[key] = [
            {k: urllib.parse.unquote(v) for k, v in urllib.parse.parse_qsl(i)}
            for i in stream_data[key].split(",")
        ]
#

def get_url(response: str):
    i = 0
    try:
        jsonObj = json.loads(response)
        extract.apply_descrambler = custom_apply_descrambler
        link = YouTube(f"https://www.youtube.com/watch?v={jsonObj['items'][0]['id']['videoId']}")
    except:
        if i >= 5:
            return flask.render_template('search.html')
        get_url(response)
    return link.streams.get_by_itag(18).url