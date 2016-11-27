from twython import Twython  # pip install twython
import time  # standard lib
import auth
import datetime
import os
import codecs

#  Trump, Clinton
user_ids = "25073877, 1339835893"

# Username used when writing the files
username = auth.username

twitter = Twython(app_key=auth.api_key,
                  app_secret=auth.api_secret,
                  oauth_token=auth.access_token_key,
                  oauth_token_secret=auth.access_token_secret)

if not os.path.exists("data/"):
    os.makedirs("data/")
now = datetime.datetime.now()
outfn = "%i.%i.%i" % (now.month, now.day, now.year)

fields = "id,created_at,text,user,lang,in_reply_to_user_id,retweeted,retweet_count,is_quote_status".split(",")
user_fields = "followers_count,friends_count,user_id,screen_name,name".split(",")

f = open("mostRecentId")
startId = long(f.readline())
mostRecentId = startId
f.close()
max_id = None

textBuffer = []

for i in range(0, 16):  ## iterate through all tweets
    ## tweet extract method with the last list item as the max_id
    user_timeline = twitter.get_user_timeline(user_id=auth.scrapped_id, count=200, include_retweets=False, max_id=max_id,
                                              since_id=startId)
    f = codecs.open("data/tweets_{}.csv".format(username), "a", encoding="utf-8")
    f2 = codecs.open("data/tweets_{}_{}.csv".format(username,outfn), "a", encoding="utf-8")
    lis = []
    for tweet in user_timeline:
        id = tweet['id']
        lis.append(id)  ## append tweet id's
        values = []

        values.append(id)
        values.append(tweet['created_at'])
        values.append(tweet['text'].replace('\n', ' '))
        values.append(tweet['lang'])
        values.append(tweet['in_reply_to_user_id'])
        values.append(tweet['retweeted'])
        values.append(tweet['retweet_count'])
        values.append(tweet['is_quote_status'])

        user = tweet['user']
        values.append(user['followers_count'])
        values.append(user['friends_count'])
        values.append(user['id'])
        values.append(user['screen_name'])
        values.append(user['name'])

        line = ""+str(values[0])
        print tweet['text']
        for j in range(1,len(values)):
            # print val
            val = values[j]
            if(isinstance(val, unicode)):
                line += "\t" + val
            else:
                line += "\t" + str(val)

        line += "\n"
        f.write(line)
        f2.write(line)

    f.close()
    f2.close()

    #No new tweets from the timeline, stop the process
    if len(lis) > 0:
        if i==0:
            mostRecentId = lis[0]
        max_id = min(lis) - 1
    else:
        break

    #Less than 200 tweets, we scrapped all, we stop the process
    if len(lis) < 200:
        break

    if i < 15:
        print("INFO : Sleeping")
        time.sleep(300)  ## 5 minute rest between api calls

f = open('mostRecentId', 'w')
f.write(str(mostRecentId))
f.close()
