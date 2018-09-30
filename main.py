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

	print("here 1")
	text = get_text(statuses)
	print("here 2")
	text = remove_handles(text)  # take out all mentions
	print("here 3")
	text = remove_bad_chars(text)  # remove "bad" characters, like parentheses
	print("here 4")

	# cannot perform markov chain generation when there are less than 100 words in total to be analyzed
	if len(text.split(' ')) <= 100:
		return None

	# generate text using markov chains
	mc = MarkovChain()
	mc.add_string(text)
	result = mc.generate_text()

	print("here 5")

	# format the result
	result = capitalize_first_word(result)
	print("here 6")
	result = add_period_to_the_end(result)
	print("here 7")
	new_tweet = list_of_words_to_string(result)
	print("here 8")

	# ensure that new tweet is 240 characters or less
	while len(new_tweet) > 240:
		new_tweet = remove_last_word(new_tweet)

	return new_tweet


def main():
	new_mention = False
	since_id = get_since_id()
	mentions = twitter_api.GetMentions(since_id=since_id)  # defaults to 20 most recent since status with id since_id

	# for each new mention, either reply with mimic, SORRY_RESPONSE, or INFORMATION_RESPONSE
	for mention in mentions:
		# there exists new mention(s)
		new_mention = True

		if ('mimic me' in mention.text.lower()):

			print("Saw a mimic request")

			# generate mimicking tweet
			result = mimic_me(mention.user.screen_name)
			
			if result:
				status = twitter_api.PostUpdate(status=('Mimicking ' + ('@%s: '%(mention.user.screen_name)) + result),
									   			in_reply_to_status_id=mention.id)
				print 'New mimic: @%s' %(mention.user.screen_name)
				update_since_id(status.id)
			elif result == 0:
				print("making sorry response")
				try:
					status = twitter_api.PostUpdate(status=('@%s '%(mention.user.screen_name) + ' ' + SORRY_RESPONSE),
										   			in_reply_to_status_id=mention.id)
					print "Made sorry response to @%s" % (mention.user.screen_name)
					update_since_id(status.id)
				except twitter.error.TwitterError:
					print("Duplicate Sorry response error")
		else:
			try:
				status = twitter_api.PostUpdate(status=('@%s '%(mention.user.screen_name) + ' ' + INFORMATION_RESPONSE),
									   			in_reply_to_status_id=mention.id)
				print "Made an informational response to @%s" %(mention.user.screen_name)
				update_since_id(status.id)
			except twitter.error.TwitterError:
				print("Duplicate informational response error")

	if verbose and not new_mention:
			print 'No new mentions.'


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
		print("Made it into __main__ block")
		main()
