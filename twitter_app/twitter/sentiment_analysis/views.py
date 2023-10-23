from django.shortcuts import render
from django.http import *
from sentiment_analysis.forms import *
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
import string


class TwitterSentClass():
    def __init__(self):
        API_key = 'IEV8WxUSm4uYd6Rcfynrys2Ov'
        API_secret = '0lBsNrI6xCZrlpkGOtWIPtDFHiTWT2WlgVEKQFVmtG5vbxy9hW'
        access_token = '1613990303534354449-OpgPDAeOsLUlbtNhUMUjNyDRIOIdiD'
        access_token_secret = 'FHgjOYDf2ZWe87VlSN5XgleBcIW7tacWI40vmQTpG5MS1'
        try:
            self.auth = OAuthHandler(API_key, 
                                     API_secret)
            self.auth.set_access_token(access_token,
                                       access_token_secret)
            self.api = tweepy.API(self.auth)
            print('Authenticated')
        except:
            print("Sorry! Error in authentication!")
 
    def cleaning_process(self, tweet):
        text = tweet.lower()
        text = re.sub('\[.*?\]', '', tweet)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text
 
    def get_sentiment(self, tweet):
        analysis = TextBlob(self.cleaning_process(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count=1000):
        tweets = []
        try:
            fetched_tweets = self.api.search_tweets(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] =self.get_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
 
        except tweepy.errors.TweepyException as e:
            print("Error : " + str(e))

def show(request):
    form = TwitterForm()
    return render(request,'index.html',{'ff':form})
            
def prediction(request):
    arr_pred = []
    arr_pos_txt = []
    arr_neg_txt = []
    if request.method == 'POST' :
        api = TwitterSentClass()
        t = request.POST['tweeterid']
        tweets = api.get_tweets(query = t, count = 100)

        print(tweets)
        pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        pos = "Positive tweets percentage: {} %".format(100*len(pos_tweets)/len(tweets))

        neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        neg="Negative tweets percentage: {}%".format(100*len(neg_tweets)/len(tweets))                
        # adding the percentages to the prediction array to be shown in the html page.
        arr_pred.append(pos)
        arr_pred.append(neg)
        
        # storing first 5 positive tweets
        arr_pos_txt.append("Positive tweets:")
        for tweet in pos_tweets[:5]:
            arr_pos_txt.append(tweet['text'])

        # storing first 5 negative tweets
        arr_neg_txt.append("Negative tweets:")
        for tweet in neg_tweets[:5]:
            arr_neg_txt.append(tweet['text'])
   
        return render(request,'prediction.html',{'arr_pred':arr_pred
                                                ,'arr_pos_txt':arr_pos_txt,'arr_neg_txt':arr_neg_txt})