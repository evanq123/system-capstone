import twitter
import tweepy
import json
from database import MySQLDB as mysqldb
from database import db_create, db_read, db_delete, db_range, db_kvstore
from datetime import datetime

consumer_key = "***REMOVED***"
consumer_secret = "***REMOVED***"
access_token_key = "***REMOVED***"
access_token_secret = "***REMOVED***"

def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    tw_api = tweepy.API(auth)
    
    score_conv = { 'created_at': score_date }

    class MyStreamListener(tweepy.StreamListener):

        def on_status(self, status):
            print(status.text)

        def on_data(self, data):
            json_data = json.loads(data)
            db_create(json_data, score_conv)
            #db_delete(2000)
            #db_read(5, "text")
            #db_range("created_at", "text", "Wed Nov 11 22:33:40 +0000 2020", "Wed Nov 11 22:34:16 +0000 2020")
            print("Added tweet id to db:{}".format(json_data['id']))


    myStreamListener = MyStreamListener()

    myStream = tweepy.Stream(auth = tw_api.auth, listener = myStreamListener)

    myStream.filter(track=['python'])

def score_date(date):
    # calculate numeric value of date for sorting. Note, some dates have
    # same score, so we might not be able to use sets, or we can store list
    # of uid that have same score in same key.
    return int(datetime.strptime(date,'%a %b %d %H:%M:%S %z %Y').timestamp());


if __name__ == "__main__":
    main()