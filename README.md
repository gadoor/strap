# Introduction
This is a simple application that giving a set of keywords it listens to twitter streams and prints the trending tweets.

# Make it work
Running this application is really simple (make sure that `python-virtualenv` is installed):
```
$ virtualenv -p python3.4 venv
$ source venv/bin/activate
(venv)path/to/application/home$ pip install requirements.txt
```
Before running the application make sure to change the following required configuration values in `config.yml` file:
```
consumer_key: your_twitter_api_consumer_key
consumer_secret: your_twitter_api_consumer_secret
access_token: your_twitter_api_access_token
access_token_secret: your_twitter_api_access_token_secret
```
`config.yml` also has some optional values that you can set:
```
interval: interval in seconds to print the data, defaults to 60
port: zmq port, defaults to 1122
max_tweets: maximum number of tweets to print, defaults to 10
```
Run the app:
```
(venv)path/to/application/home$ python strap.py "keyword1, keyword2, ..." [path/to/config.yml]
```