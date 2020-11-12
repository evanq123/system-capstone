import tweepy
import json

with open('config.json', 'r') as f:
    config = json.load(f)["TWITTER"]
consumer_key = config['CONSUMER_KEY']
consumer_secret = config['CONSUMER_SECRET']
access_token_key = config['ACCESS_TOKEN_KEY']
access_token_secret = config['ACCESS_TOKEN_SECRET']

n_tweets = 0

def main():
    print("Enter filename to store data in:")
    f = open(input(), "a")
    print("Enter word to filter tweets by:")
    filter_arg = input()
    print("Enter max number of tweets to store:")
    max_tweets = int(input())
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    tw_api = tweepy.API(auth)

    class MyStreamListener(tweepy.StreamListener):
        def on_status(self, status):
            print(status.text)

        def on_data(self, data):
            json_data = json.loads(data)
            # db_create(json_data, score_conv)
            f.write(json.dumps(json_data))
            f.write("\n")
            global n_tweets
            n_tweets += 1
            if(n_tweets >= max_tweets):
                print("Maximum number of tweets reached. Exiting..")
                exit()
            print("Added tweet id to db:{}".format(json_data['id']))

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = tw_api.auth, listener = myStreamListener)
    myStream.filter(track=["{}".format(filter_arg)])

if __name__ == "__main__":
    main()