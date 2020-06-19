## YouTubeProxyServer
This app is developed for my close friends.

## Notice 
1. If you watch a video through this app, the view count won't increase.

   So, watch a video on YouTube Site whenever you can.
  
2. This app will not work on the network which doesn't allow accessing to ~googlevideo.com/


## To run this app
1. create /src/.env and write like this 

~~~
YOUTUBEAPIKEY=your youtube api key 

VERIFICATION_EMAIL=gmail address 

PASSWORDFOREMAIL=google account password 
~~~

You should create new google account because 
you must disable your security. 

See this: https://support.google.com/a/answer/6260879?hl=en 

2. create database on heroku 

https://elements.heroku.com/addons/heroku-postgresql 
addon hobby-dev or better 

Run this command

~~~
heroku run python -c "import src.models; src.models.init_db()"
~~~
   
or

   open heroku console 
   run python code
   
   ~~~
   from src import models \
   models.init_db() 
   ~~~

3. add default account into database 

   ~~~
   user = models.Registered_User(user_name=[username], password=[hash256ed password]) 
   
   models.db.session.add(user) 
   
   models.db.session.commit()
   ~~~






