# Last modified: September 29, 2018 4:20pm
# This script runs the @get_mimicked Twitter bot. 

import datetime as dt
import json
import operator
import sys
import time

import requests
import twitter

from markov_python.cc_markov import MarkovChain
from utils import (
	update_since_id,
	get_since_id,
	remove_last_word,
	remove_handles,
	remove_bad_chars,
	get_text,
	capitalize_first_word,
	add_period_to_the_end,
	list_of_words_to_string
)

HANDLE_TO_MIMIC = "Replace this string with someone's twitter handle"

# default to utf8 instead of ascii
reload(sys)  
sys.setdefaultencoding('utf8')

# configurations
forever = False  # runs while loop forever -- instead of using a scheduler like cron
verbose = False  # will print logs on every run -- false will print only logs when new tweet is posted

# messages
SORRY_RESPONSE = 'Sorry, you must have at least 100 words tweeted in total to be mimicked.'
INFORMATION_RESPONSE = 'Well, hi there! Tweet at me with the words "Mimic me" to get a mimicking response!'

# import passwords for Twitter REST API from local text file
passwords_file = open('passwords.txt', 'r')
passwords = passwords_file.readlines()
for password in passwords:
	passwords[passwords.index(password)] = password.replace('\n', '')

twitter_consumer_key = passwords[0]
twitter_consumer_secret = passwords[1]
twitter_access_token = passwords[2]
twitter_access_secret = passwords[3]

passwords_file.close()

# instantiate API
twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, 
					access_token_key=twitter_access_token, access_token_secret=twitter_access_secret,
					sleep_on_rate_limit=True)


def mimic_me(handle):
	# Takes in the other user's twitter handle and returns a tweet in the style of their tweets

	# get and analyze the past (up to) 1000 tweets made by the user-to-be-mimicked
	statuses = twitter_api.GetUserTimeline(screen_name=handle, count=1000, include_rts=False)

	text = get_text(statuses)
	text = remove_handles(text)  # take out all mentions
	text = remove_bad_chars(text)  # remove "bad" characters, like parentheses

	# cannot perform markov chain generation when there are less than 100 words in total to be analyzed
	if len(text.split(' ')) <= 100:
		return None

	# generate text using markov chains
	mc = MarkovChain()
	mc.add_string(text)
	result = mc.generate_text()

	# format the result
	result = capitalize_first_word(result)
	result = add_period_to_the_end(result)
	new_tweet = list_of_words_to_string(result)

	# ensure that new tweet is 240 characters or less
	while len(new_tweet) > 240:
		new_tweet = remove_last_word(new_tweet)

	return new_tweet


def main():
	result = mimic_me(HANDLE_TO_MIMIC)
	
	if result:
		status = twitter_api.PostUpdate(status=('Mimicking ' + ('@%s: '%(HANDLE_TO_MIMIC)) + result))
		print 'New mimic: @%s' %(HANDLE_TO_MIMIC)
	else:
		try:
			status = twitter_api.PostUpdate(status=('@%s '%(HANDLE_TO_MIMIC) + ' ' + SORRY_RESPONSE))
			print "Made sorry response to @%s" % (HANDLE_TO_MIMIC)
		except twitter.error.TwitterError:
			print "Duplicate SORRY_RESPONSE error"


if __name__ == "__main__":
	if forever:
		# infinitely loop while running script
		while True:
			if verbose:
				print '-----------------------------------------------------'
				print dt.datetime.now().strftime("%Y-%m-%d %H:%M")
			main()
			# sleep for 5~ minutes before checking twitter again for new mentions
			if verbose:
				print 'Now waiting 5 minutes...'
			time.sleep(300)
	else:
		main()
