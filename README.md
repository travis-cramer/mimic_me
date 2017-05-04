# mimic_me

This is the code behind the world-renowned twitter bot Mimic Me (@get_mimicked).

This bot responds to tweets containing "Mimic me @\<your handle\>" by mimicking the other user based on their twitter history.

The script main.py will take care of almost everything.

You just need two local text files:
  -A text file named 'passwords.txt' containing your twitter consumer key, twitter consumer secret, twitter access token,
    and twitter access secret for your Twitter REST API. 
  -A text file named 'past_mimics.txt' (just create it and leave it blank and main.py will take care of the rest) so that
    main.py can keep track of which mentions (tweet containing your twitter bot's handle) that your bot has already 
    responded to.
    
The only edit to main.py that you need to make is to reset the variable my_handle (at the top of the script).
