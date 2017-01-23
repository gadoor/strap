"""
@Author: Hizaoui Mohamed Abdelkader
@Email-1: hizaoui.ma@gmail.com
"""
import hashlib
import json
import time
import zmq

from config import conf


class ParseTwitterStream(object):
    """
    Twitter Stream Parser
    """
    def __init__(self):
        """
        initializing attributes
        :md5_store: stores the md5 hashes of a existing tweets
        :tweets: stores tweets information
        :begin: to keep track of the time
        :interval: period to wait before changing printed tweets
        :port: zmq publisher port
        :pub: zmq publisher socket
        :return:
        """
        self.md5_store = []
        self.tweets = {}
        self.begin = time.time()
        self.interval = conf.get('interval', 60)
        if type(self.interval) != int and type(self.interval) != float:
            print("Interval is not an int or a float, using default value")
            self.interval = 60
        self.port = conf.get('port', 1122)
        if type(self.port) != int:
            print("Port is not an int, using default value")
        self.pub = self.__get_zmq_pub()

    def __get_zmq_pub(self):
        """
        initialize zmq publisher socket
        :return: zmq publisher socket
        """
        print("Publishing to tcp://127.0.0.1:%d channel: tweets" % self.port)
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://127.0.0.1:%d" % self.port)
        return socket

    def parse(self, tweet):
        """
        parse a tweet: increase a counter (trending index) if it already exists in tweets or append it if it doesn't
        :param tweet: dict returned from twitter
        :return: None
        """
        m = hashlib.md5()
        m.update(tweet['text'].encode('utf-8'))
        md5sum = m.hexdigest()
        if md5sum in self.md5_store:
            self.tweets[md5sum]['count'] += 1
        else:
            self.md5_store.append(m.hexdigest())
            self.tweets[md5sum] = tweet
            self.tweets[md5sum]['count'] = 1
        if time.time() - self.begin >= self.interval:
            self.pub.send_string('tweets<->%s' % json.dumps(self.tweets))
            self.begin = time.time()