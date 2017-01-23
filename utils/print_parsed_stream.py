"""
@Author: Hizaoui Mohamed Abdelkader
@Email-1: hizaoui.ma@gmail.com
"""
import json
import subprocess as sp
from multiprocessing import Process

import shutil
import zmq

from utils.config import conf


class PrintParsedStream(object):
    """
    Parsed Stream Printer
    """
    def __init__(self):
        """
        initializing attributes
        :max_tweets: maximum number of tweets to show
        :port: zmq publisher port (for the subscriber to listen on)
        :cols: number of terminal columns
        :return:
        """
        self.max_tweets = conf.get('max_tweets', 10)
        if type(self.max_tweets) != int:
            print("Max tweets is not and int, using default value")
            self.max_tweets = 10
        self.port = conf.get('port', 1122)
        if type(self.port) != int:
            print("Port is not an int, using default value")
            self.port = 1122
        self.cols = shutil.get_terminal_size().columns

    def __get_zmq_sub(self):
        """
        initialize zmq subscriber
        :return: zmq subscriber socket
        """
        print("Subscribing to tcp://127.0.0.1:%d channel: tweets" % self.port)
        context = zmq.Context()
        sub = context.socket(zmq.SUB)
        sub.connect("tcp://127.0.0.1:%d" % self.port)
        sub.setsockopt_string(zmq.SUBSCRIBE, "tweets")
        return sub

    def __pretty_print(self, tweet):
        """
        pretty prints a tweet: prints the trending index, text and hashtags and coordinates
        :param tweet: dict of tweet to print
        :return: None
        """
        print("Trendiness: %(count)d\nText:\n\t%(text)s" % tweet)
        if tweet['hashtags']:
            print("Hashtags: ")
            print(end="\t")
            print(", ".join([hashtag['text'] for hashtag in tweet['hashtags']]))
        if tweet['coordinates']:
            print("Coordinates", end=": ")
            print(", ".join(["%.2f" % coordinate for coordinate in tweet['coordinates']['coordinates']]))
        print("******".center(self.cols))

    def __printer(self):
        """
        Receives tweets then prints them
        :return: None
        """
        print("Started PrintParsedStream...")
        sub = self.__get_zmq_sub()
        while True:
            try:
                message = sub.recv_string()
            except KeyboardInterrupt as ki:
                print(ki)
                sub.close()
                exit(1)
            except Exception as exp:
                print(exp)
                sub.close()
                exit(1)
            _, msg = message.split("tweets<->")
            data = json.loads(msg)
            sorted_tweets = sorted(list(data.values()), key=lambda k: k['count'], reverse=True)
            try:
                _ = sp.call("clear", shell=True)
            except Exception as exp:
                _ = sp.call("cls", shell=True)
            finally:
                pass
            for tweet in sorted_tweets[:self.max_tweets]:
                self.__pretty_print(tweet)

    def run(self):
        """
        Starts the __printer as spawned process
        :return: None
        """
        process = Process(target=self.__printer)
        process.start()
