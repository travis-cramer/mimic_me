# Mimic Me ([@get_mimicked](https://twitter.com/get_mimicked))

This is the code behind the world-renowned twitter bot Mimic Me ([@get_mimicked](https://twitter.com/get_mimicked)).

This bot responds to mentions (tweets with the bot's handle tagged within) containing the words "Mimic me" by mimicking the tweeting user based on their twitter history using Markov Chains to randomly generate strings of words. Sometimes the results are grammatically correct. Most of the time, they're not. For entertainment purposes only.

You can create an exact relica of this twitter bot with this public repository.

The script main.py will take care of almost everything.

But some additions are needed:

* A text file named 'passwords.txt' containing your twitter consumer key, twitter consumer secret, twitter access token, twitter access secret (for your [Twitter REST API](https://dev.twitter.com/rest/public)), each on their own line in that order. An example of this document (which includes the optional MySQL db password) is in the repository as "passwords_example.txt".

* A text file called "past_mimics.txt" which the script will use to record all mentions that it has previously responded to. It uses this to check whether or not it needs to create a new mention.

* OR: A locally hosted [MySQL](https://www.mysql.com/) database named 'my_database' with a table named 'past_mimics' with columns (id INT, screen_name TEXT, date_time TEXT). If you choose to do this, you will have to edit the script to add your db credentials and add your db admin password to the passwords.txt file.                                                                                                                                         
    

