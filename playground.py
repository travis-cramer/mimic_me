import sys
import operator
import requests
import json
import twitter
import time
from markov_python.cc_markov import MarkovChain
import re


twitter_consumer_key = '9p2r4xxien2bw2DLruUmf4haP'
twitter_consumer_secret = 'Z14EtOPVxOaMqODk3OURP2bBkL4gLWa3ip8sgiJ3R1YQHAdqGr'
twitter_access_token = '851668423733985280-LXa5ly0Byt95WxkuMzQvafxP1tkFw26'
twitter_access_secret = 'zujkoOMqV0w530zJo2J5HoO2HAaJc9vgeWruETdgXZo1T'



twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

mentions = twitter_api.GetMentions(count = 20)

file = open('past_mimics.txt', 'w')

for mention in mentions:
	file.write(mention.user.screen_name + ' ' + mention.user.created_at + '\n')

file.close()

