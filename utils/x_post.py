import tweepy
from typing import List
import os

class TwitterClient:
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
            consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
            access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
        )

    def create_thread(self, tweets: List[str]) -> None:
        previous_tweet_id = None
        for tweet in tweets:
            response = self.client.create_tweet(
                text=tweet, 
                in_reply_to_tweet_id=previous_tweet_id
            )
            previous_tweet_id = response.data['id']
            
    def send_post(self, text: str) -> None:
        self.client.create_tweet(text=text)