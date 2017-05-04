# mimic_me

This is the code behind the world-renowned twitter bot Mimic Me (@get_mimicked).

This bot responds to tweets containing "Mimic me @\<your bot's handle\>" by mimicking the tweeting user based on their twitter history.

The script main.py will take care of almost everything.

You just need two local text files:

-A text file named 'passwords.txt' containing your twitter consumer key, twitter consumer secret, twitter access token,
    and twitter access secret for your Twitter REST API. 
    
-A text file named 'past_mimics.txt' (just create it and leave it blank and main.py will take care of the rest) so that
    main.py can keep track of which mentions (tweets containing your twitter bot's handle) that your bot has already 
    responded to.
    
Have fun!
