"""
@Author: Hizaoui Mohamed Abdelkader
@Email-1: hizaoui.ma@gmail.com
"""
import sys

from tweepy import OAuthHandler

from tweepy import Stream

from utils.config import conf
from utils.get_twitter_stream import CustomStreamListener
from utils.print_parsed_stream import PrintParsedStream

if __name__ == '__main__':
    try:
        keywords = sys.argv[1]
        keywords = [keyword.strip() for keyword in keywords.split(",")]
        print("Listening on twitter for: %r" % keywords)
    except IndexError:
        print("ERROR:\nUSAGE: python strap.py \"keyword1, keyword2, keyword3, keyword4\" [path/to/config.yml]")
        exit(1)
    l = CustomStreamListener()

    consumer_key = conf['consumer_key']
    consumer_secret = conf['consumer_secret']
    access_token = conf['access_token']
    access_token_secret = conf['access_token_secret']

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    printer = PrintParsedStream()
    try:
        printer.run()
        stream.filter(track=keywords)
    except KeyboardInterrupt:
        exit(0)