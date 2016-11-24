from twython import Twython  # pip install twython
import time  # standard lib
import auth
import datetime
import os
import codecs

#  Trump, Clinton
user_ids = "25073877, 1339835893"

# Username used when writing the files
username = 'fr4ctal'


twitter = Twython(app_key=auth.api_key,
                  app_secret=auth.api_secret,
                  oauth_token=auth.access_token_key,
                  oauth_token_secret=auth.access_token_secret)
if not os.path.exists("data/"):
    os.makedirs("data/")
now = datetime.datetime.now()
fields = "id,created_at,text,user,lang,in_reply_to_user_id,retweeted,retweet_count,is_quote_status".split(",")
user_fields = "followers_count,friends_count,id,screen_name,name".split(",")
