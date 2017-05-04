# Last modified: May 3, 2017 11:33pm
# This script, using a Twitter API, operates the @get_mimicked Twitter acount. 


import sys
import operator
import requests
import json
import twitter
import time
from markov_python.cc_markov import MarkovChain
import re
import datetime as dt


# import passwords for Twitter REST API from local text file
passwords_file = open('passwords.txt', 'r')
passwords = passwords_file.readlines()
for password in passwords:
	passwords[passwords.index(password)] = password.replace('\n', '')



twitter_consumer_key = passwords[0]
twitter_consumer_secret = passwords[1]
twitter_access_token = passwords[2]
twitter_access_secret = passwords[3]


# instantiate API
twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

def remove_last_word(sentence):
	# Removes the last word of the sentence (and keeps the period).

	# split sentence into a list of all the words, call it post
		post = sentence.split(' ')

		# remove the last word from post
		post = post.remove(post[-1])
		print post

		# iterate from list into string again
		new_sentence = ''
		for i in range(len(post)):
			new_sentence = new_sentence + post[i] + ' '

		# Remove extra space and add a period back onto the end of the new sentence.
		new_sentence = new_sentence[:-1] + '.'

		return new_sentence


def mimic_me(handle):
	statuses = twitter_api.GetUserTimeline(screen_name = handle, count = 1000, include_rts = False)
	text = ""
	for status in statuses:
		if status.lang == 'en':
			text += status.text.encode('utf-8') + ' '


	# remove handles
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
	while len(new_tweet) > 140:
		new_tweet = remove_last_word(new_tweet)

	return new_tweet



# infinitely loop while running script
while True:
	# print datetime before each check for new mentions
	print dt.datetime.now().strftime("%Y-%m-%d %H:%M")

	# open past_mimics for reading and appending to read past mimics and to potentially add new mimics
	file_1 = open('past_mimics.txt', 'r')
	file_2 = open('past_mimics.txt', 'a')

	# convert past_mimics into list
	past_mimics = file_1.readlines()
	for mimic in past_mimics:
		past_mimics[past_mimics.index(mimic)] = mimic.replace('\n', '')

	

	# collect 20 most recent mentions

	mentions = twitter_api.GetMentions(count = 20)



	# check if new mention, check if 'mimic me' is in tweet, then create mimic and post mimic of mentioner

	for mention in mentions:
		mention_simple = mention.user.screen_name + ' ' + mention.created_at
		print mention_simple
		if mention_simple not in past_mimics:
			if ('mimic me' in mention.text) or ('Mimic me' in mention.text) or ('Mimic Me' in mention.text) or ('Mimic me.' in mention.text):
				
				file_2.write(mention_simple + '\n')

				

				their_handle = mention.user.screen_name

				result = mimic_me(their_handle)
				

				if result != 0:
					# take out all mentions in the generated tweet. (maybe so that friends don't get mad)
					twitter_api.PostUpdates('Mimicking ' + ('@%s: ' % (their_handle)) + result)
					print 'New mimic: %s' %(their_handle)
				elif result == 0:
					try:
						twitter_api.PostUpdates('@%s ' % (their_handle) + 'Sorry, you must have at least 100 words tweeted in total to be mimicked.')
					except twitter.error.TwitterError:
						pass

	file_1.close()
	file_2.close()
	print 'Now waiting 5 minutes...'
	print '-----------------------------------------------------'

	# sleep for 5~ minutes before checking twitter again for new mentions
	time.sleep(600)

