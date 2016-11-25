from twython import Twython  # pip install twython
import time  # standard lib
import auth
import datetime
import os
import codecs

#  Trump, Clinton
user_ids = "25073877, 1339835893"

# Username used when writing the files
username = 'pi3rrick'


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

f = open("mostRecentId")
startId = long(f.readline())
mostRecentId = startId
f.close()
max_id = None

textBuffer = []

for i in range(1):
    retweet_timeline = twitter.get_retweets(id=long(795710386855088129),trim_user=0, count=10)
    f = codecs.open("data/retweets_{}.tsv".format(username), "a", encoding="utf-8")
    f2 = codecs.open("data/retweets_{}_{}.tsv".format(username, outfn), "a", encoding="utf-8")
    lis = []
    for retweet in retweet_timeline:
        id = retweet['id']
        lis.append(id)  ## append tweet id's
        values = []
        for x in retweet_fields:
            if x == "entities" or x == "user":
                obj = retweet[x]
                field_chooser = lambda l: entities_field if l == "entities" else user_fields
                print obj
                field = field_chooser(x)
                for y in field:
                    print y
                    print obj[y]
                    values.append(obj[y])
            elif x == "text":
                values.append(retweet['text'].replace('\n', ' '))
            else:
                values.append(retweet[x])
        print retweet['text']
        line = "\t".join(x if isinstance(x, unicode) else str(x) for x in values) + "\n"
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

# f = open('mostRecentId', 'w')
# f.write(str(mostRecentId))
# f.close()


