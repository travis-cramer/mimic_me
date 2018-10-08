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
	get_twitter_client,
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

# default to utf8 instead of ascii
reload(sys)  
sys.setdefaultencoding('utf8')

# configurations
forever = False  # runs while loop forever -- instead of using a scheduler like cron
verbose = False  # will print logs on every run -- false will print only logs when new tweet is posted

# messages
SORRY_RESPONSE = 'Sorry, you must have at least 100 words tweeted in total to be mimicked.'
INFORMATION_RESPONSE = 'Well, hi there! Tweet at me with the words "Mimic me" to get a mimicking response!'

# instantiate API
twitter_api = get_twitter_client()


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
	result = mimic_me('HolianVI')
	
	if result:
		status = twitter_api.PostUpdate(status=('Mimicking ' + ('@%s: '%('HolianVI')) + result))
		print 'New mimic: @%s' %('HolianVI')
		update_since_id(status.id)
	else:
		try:
			status = twitter_api.PostUpdate(status=('@%s '%('HolianVI') + ' ' + SORRY_RESPONSE))
			print "Made sorry response to @%s" % ('HolianVI')
			update_since_id(status.id)
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
