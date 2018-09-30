# Last modified: September 29, 2018 4:20pm
# This script runs the @get_mimicked Twitter bot. 

import datetime as dt
import json
import operator
import re
import sys
import time

import requests
import twitter

from markov_python.cc_markov import MarkovChain

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


def update_since_id(since_id):
	# record latest status.id that mimic me has made (this is to search for mentions only after this status was made)
	file = open('since_id.txt', 'w')
	file.write(str(since_id))
	file.close()


def get_since_id():
	# get previous status.id of our bot's last mimic (we call it since_id)
	try:
		file = open('since_id.txt', 'r')
		since_id = int(file.readline())
		file.close()
	except IOError:
		since_id = None
	return since_id


def remove_last_word(sentence):
	# Removes the last word of a sentence (and keeps the period).
	# split sentence into a list of all the words, call it post
	post = sentence.split(' ')
	# remove the last word from post
	post = post.remove(post[-1])
	# iterate from list into string again
	new_sentence = ''
	for i in range(len(post)):
		new_sentence = new_sentence + post[i] + ' '
	# Remove extra space and add a period back onto the end of the new sentence.
	new_sentence = new_sentence[:-1] + '.'
	return new_sentence


def mimic_me(handle):
	# Takes in the other user's twitter handle and returns a tweet in the style of their tweets
	statuses = twitter_api.GetUserTimeline(screen_name=handle, count=1000, include_rts=False)
	text = ""
	for status in statuses:
		if status.lang == 'en':
			text += status.text.encode('utf-8') + ' '
	# remove handles # take out all mentions in the generated tweet. (maybe so that random friends don't get mad)
	handles = re.findall('@[^ ]*', text)
	for handle in handles:
		text = text.replace(handle, '')
	#remove parentheses
	bad_characters = re.findall('\(', text) + re.findall('\)', text)
	for character in bad_characters:
		text = text.replace(character, '')
	if len(text.split(' ')) <= 100:
		return 0
	else:
		pass
	mc = MarkovChain()
	mc.add_string(text)
	result = mc.generate_text()
	# Capitalize the first word in the generated sentence.
	letter = result[0][0]
	rest_of_word = result[0][1:]
	capped_word = letter.upper() + rest_of_word
	result[0] = capped_word
	# Put a period at the end of the last word in the generated sentence.
	result[len(result) - 1] = result[len(result) - 1] + '.'
	new_tweet = ''
	for i in range(len(result)):
		new_tweet = new_tweet + result[i] + ' '
		# ensure that new tweet is 140 characters or less
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
			# generate mimicking tweet
			result = mimic_me(mention.user.screen_name)
			
			if result != 0:
				status = twitter_api.PostUpdate(status=('Mimicking ' + ('@%s: '%(mention.user.screen_name)) + result),
									   			in_reply_to_status_id=mention.id)
				print 'New mimic: @%s' %(mention.user.screen_name)
				update_since_id(status.id)
			elif result == 0:
				try:
					status = twitter_api.PostUpdate(status=('@%s '%(mention.user.screen_name) + ' ' + SORRY_RESPONSE),
										   			in_reply_to_status_id=mention.id)
					print "Made sorry response to @%s" % (mention.user.screen_name)
					update_since_id(status.id)
				except twitter.error.TwitterError:
					pass
		else:
			try:
				status = twitter_api.PostUpdate(status=('@%s '%(mention.user.screen_name) + ' ' + INFORMATION_RESPONSE),
									   			in_reply_to_status_id=mention.id)
				print "Made an informational response to @%s" %(mention.user.screen_name)
				update_since_id(status.id)
			except twitter.error.TwitterError:
				pass

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
		main()
