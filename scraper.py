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

# lis = [738177801556217855,786281218945982465] ## oldest, newest tweet
# fields = "id,created_at,text,user,in_reply_to_screen_name,in_reply_to_status_id,in_reply_to_user_id_str,lang,favorite_count\
# ,place,entities,contributors,truncated,id_str,in_reply_to_user_id,source,geo,in_reply_to_status_id_str\
# ,retweeted,retweet_count,is_quote_status,favorited,coordinates".split(",")

fields = "id,created_at,text,user,lang,in_reply_to_user_id,retweeted,retweet_count,is_quote_status".split(",")
user_fields = "followers_count,friends_count,id,screen_name,name".split(",")

# INITIALIZE OUTPUT FILE AND WRITE HEADER ROW
# outfp.write(str.join("\t", fields) + "\n")  # .encode("utf-8"))

mostRecentId = None
max_id = None
lis = []

for i in range(0, 16):  ## iterate through all tweets
    file = codecs.open("data/tweets_{}.csv".format(username), "a", encoding="utf-8")
    # outfn = "data/tweets_%i.%i.%i.tsv" % (now.month, now.day, now.year)
    outfp = codecs.open("data/raw_{}.csv".format(username), "a", encoding="utf-8")

    ## tweet extract method with the last list item as the max_id
    user_timeline = twitter.get_user_timeline(user_id="25073877", count=200, include_retweets=False, max_id=max_id,
                                              since_id=mostRecentId)
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
        for i in range(1,len(values)):
            # print val
            val = values[i]
            if(isinstance(val, unicode)):
                line += "\t" + val
            else:
                line += "\t" + str(val)

        line += "\n"

        # line = ("".join(str(e) + "\t" for e in values) + "\n")

        # for f in fields:
        #     if isinstance(tweet[f], unicode):
        #         lst.append(tweet[f])
        #     else:
        #         lst.append(str(tweet[f]))
        # line = ("".join(e + "\t" for e in lst) + "\n")
        # print line
        outfp.write(str(tweet)+"\n")  # .encode("utf-8"))
        file.write(line)

    outfp.close()
    file.close()
    max_id = min(lis)-1

    # if len(lis) > 0:
    #     newMostRecentId = max(lis)
    #     if newMostRecentId == mostRecentId:
    #         break
    #     mostRecentId = newMostRecentId
    # else:
    #     break
    print("INFO : Sleeping")
    time.sleep(300)  ## 5 minute rest between api calls
