import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from flask import Flask, request, jsonify,session, render_template,redirect,url_for

class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'ILS67Ta7A2ZytAEQdexR4L29Z'
        consumer_secret = 'sb2W6yVsbDLisH6G5tigFvIL70HHsc6OvRUg6qZoNZXFIGnUPV'
        access_token = '910900174368714753-Q6kBmqJy5KpeqJ1qdEspMa1LppO2jGd'
        access_token_secret = '1PuM2YOtCEFtFMN5JZj4iHJpzye5Cae6A7kN2xKPFeYmj'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 400): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    tweets = api.get_tweets(query = 'cnn', count = 400)
     
  
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    # percentage of positive tweets 
    print("Positive tweets percentage: {}%".format(100*len(ptweets)/len(tweets))) 
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    # percentage of negative tweets 
    print("Negative tweets percentage: {}%".format(100*len(ntweets)/len(tweets))) 
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {}%".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 
    
    return "Positive tweets percentage: {}%"
    # printing first 5 positive tweets 
#     print("\n\nPositive tweets:") 
#     for tweet in ptweets: 
#         print(ptweets) 
  
#     # printing first 5 negative tweets 
#     print("\n\nNegative tweets:") 
#     for tweet in ntweets: 
#         print(ntweets) 
  
# #if __name__ == "__main__": 
#     # calling main function 
app = Flask(__name__)
@app.route('/')
def index():
    return """<form action='/test' method='POST'>
    <input type='text' name='i1'>
    <input type='submit'  >    
    <form/>
    """
@app.route('/test', methods=['GET','POST'])
def index1():
    api = TwitterClient() 
    # calling function to get tweets 
    q=request.form['i1']

    tweets = api.get_tweets(query = q, count = 400)
     
    if len(tweets)>0:
        # picking positive tweets from tweets 
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
        # percentage of positive tweets 
        print("Positive tweets percentage: {}%".format(100*len(ptweets)/len(tweets))) 
        # picking negative tweets from tweets 
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
        # percentage of negative tweets 
        print("Negative tweets percentage: {}%".format(100*len(ntweets)/len(tweets))) 
        # percentage of neutral tweets 
        print("Neutral tweets percentage: {}%".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 
        temp=''
        temp1=''
        for t in ptweets:
            a=str(t['text'].encode('utf8'))+'<br>'+''
            temp=temp+a
        for i in ntweets:
            b=str(i['text'].encode('utf8'))+'<br>'+''
            temp1=temp1+b
        return "Positive tweets percentage: {}%".format(100*len(ptweets)/len(tweets))+'<br>'+"Negative tweets percentage: {}%".format(100*len(ntweets)/len(tweets))+'<br>'+"Neutral tweets percentage: {}%".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))+'<br>'+"<b>Positive Tweets</b><br>"+temp+"<b>Negative Tweets</b><br>"+temp1
    else:
        return 'no tweet with this text found'
app.run(debug=True)


