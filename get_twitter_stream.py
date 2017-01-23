"""
@Author: Hizaoui Mohamed Abdelkader
@Email-1: hizaoui.ma@gmail.com
"""
import json
from tweepy.streaming import StreamListener

from parse_twitter_stream import ParseTwitterStream


class CustomStreamListener(StreamListener):
    """
    My Custom StreamListener, it performs and action on an event:
        if it receives data
    """
    parser = ParseTwitterStream()

    def on_data(self, tweet):
        data = json.loads(tweet)
        try:
            t = {'text': data['text'],
                 'hashtags': data['entities']['hashtags'],
                 'coordinates': data['coordinates'],
                 'id': data['id']}
            self.parser.parse(t)
        except Exception as exp:
            pass
        return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        print(status)