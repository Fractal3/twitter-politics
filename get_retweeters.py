from twython import Twython  # pip install twython
import time  # standard lib
import auth
import datetime
import os
import codecs

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

retweet_fields = "id,created_at,entities,favorite_count,lang,retweet_count,text,user".split(",")
# user_fields = "followers_count,friends_count,id,screen_name,name".split(",")
user_fields = "id,followers_count,statuses_count,friends_count,screen_name".split(",")
entities_field = "hashtags".split(",")

f = open("mostRecentRetweetId")
# Line counter for scrapping retweets
lastLineRead_top_down = long(f.readline())
f.close()
max_id = None

l = 1
counter = 1
lis = []
for line in open("data/tweets_{}.tsv".format(username)).readlines():
    if counter < lastLineRead_top_down:
        pass
    else:
        tweet_id = long(line.split("\t")[0])
        retweet_timeline = twitter.get_retweets(id=tweet_id, trim_user=0, count=15)
        f = codecs.open("data/retweets_{}.tsv".format(username), "a", encoding="utf-8")
        f2 = codecs.open("data/retweets_{}_{}.tsv".format(username, outfn), "a", encoding="utf-8")
        lis.append(tweet_id)
        for retweet in retweet_timeline:
            # id = retweet['id']
            # lis.append(id)  ## append tweet id's
            values = [str(tweet_id)]
            for x in retweet_fields:
                if x == "entities" or x == "user":
                    obj = retweet[x]
                    field_chooser = lambda l: entities_field if l == "entities" else user_fields
                    field = field_chooser(x)
                    for y in field:
                        values.append(obj[y])
                elif x == "text":
                    values.append(retweet['text'].replace('\n', ' '))
                else:
                    values.append(retweet[x])
            line = "\t".join(x if isinstance(x, unicode) else str(x) for x in values) +"\n"
            print(line)
            f.write(line)
            f2.write(line)
        f.close()
        f2.close()
        # could also make count % 74 == 0
        if l >= 74:
            print("INFO : Sleeping")
            time.sleep(900)  ## 15 minute rest between api calls
            l = 0
        else:
            print l
            l += 1
    counter += 1
    f = open('mostRecentRetweetId', 'w')
    f.write(str(counter))
    f.close()


