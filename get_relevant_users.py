from twython import Twython  # pip install twython
import twython
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
result_file = open('data/rt_ratio.tsv', 'w')
with open("data/frequent_retweeters.tsv", 'r') as ru:
    header = ru.readline()
    print header
    for r in ru.readlines():
        user_id = r.split('\t')[1]
        try:
            user_timeline = twitter.get_user_timeline(user_id=user_id, count=100, include_retweets=False)
        except twython.exceptions.TwythonError:
            print 'Not Found user'
            continue

        rt_count = 0
        tweet_count = 0
        for tweet in user_timeline:
            print tweet['retweet_count']
            rt_count += tweet['retweet_count']
            tweet_count += 1
        ratio = float(rt_count)/float(tweet_count)
        line = r.rstrip() + '\t' + str(ratio) + '\n'
        result_file.write(line)
result_file.close()
