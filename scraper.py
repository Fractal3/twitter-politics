from twython import Twython # pip install twython
import time # standard lib
import auth
import datetime
import os
import codecs

#  Trump, Clinton
user_ids = "25073877, 1339835893"

#Username used when writing the files
username = 'fr4ctal'

twitter = Twython(app_key=auth.api_key,
            app_secret=auth.api_secret,
            oauth_token=auth.access_token_key,
            oauth_token_secret=auth.access_token_secret)

if not os.path.exists("data/"):
    os.makedirs("data/")
file = codecs.open("data/tweets_{}.csv".format(username), "a", encoding="utf-8")
now = datetime.datetime.now()

lis = [738177801556217855,786281218945982465] ## oldest, newest tweet
# fields = "id,created_at,text,user,in_reply_to_screen_name,in_reply_to_status_id,in_reply_to_user_id_str,lang,favorite_count\
# ,place,entities,contributors,truncated,id_str,in_reply_to_user_id,source,geo,in_reply_to_status_id_str\
# ,retweeted,retweet_count,is_quote_status,favorited,coordinates".split(",")

fields = "id,created_at,text,user,in_reply_to_screen_name,in_reply_to_status_id,in_reply_to_user_id_str,lang,favorite_count\
,id_str,in_reply_to_user_id,source,geo,in_reply_to_status_id_str\
,retweeted,retweet_count,is_quote_status,favorited".split(",")


# INITIALIZE OUTPUT FILE AND WRITE HEADER ROW
outfn = "data/tweets_%i.%i.%i.csv" % (now.month, now.day, now.year)
outfp = codecs.open(outfn, "w", encoding="utf-8")
outfp.write(str.join(",", fields) + "\n")  # .encode("utf-8"))

for i in range(0, 16): ## iterate through all tweets
## tweet extract method with the last list item as the max_id
    user_timeline = twitter.get_user_timeline(user_id="1339835893", count=200, include_retweets=False,max_id=None,since_id=lis[1])
    for tweet in user_timeline:
        print(tweet['text']) ## print the tweet
        lis.append(tweet['id']) ## append tweet id's
        lst = []
        for f in fields:
            if isinstance(tweet[f], unicode):
                lst.append(tweet[f])
            else:
                lst.append(str(tweet[f]))
        line = ("".join(e+"," for e in lst) + "\n")
        outfp.write(line)#.encode("utf-8"))
        file.write(line)
    time.sleep(300) ## 5 minute rest between api calls

outfp.close()
file.close()