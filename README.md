## YouTubeProxyServer
This app is developed for my close friends.

## To work this perfectly
1. create /src/.env and write like this 
"""
YOUTUBEAPIKEY=your youtube api key 

VERIFICATION_EMAIL=gmail address 

PASSWORDFOREMAIL=accout password 

""" 
You should create new google account because 
you must disable your security. 

See this: https://support.google.com/a/answer/6260879?hl=en 

2. create database on heroku 

https://elements.heroku.com/addons/heroku-postgresql 
addon hobby-dev or better 

open heroku console 
run python code
> from src import models 
> models.init_db() 

3. add default account into database 

user = models.Registered_User(user_name=username, password=hash256ed password) 

models.db.session.add(user) 
models.db.session.add(user)

app will work well






