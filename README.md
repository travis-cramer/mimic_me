# mimic_me

This is the code behind the world-renowned twitter bot Mimic Me (@get_mimicked).

This bot responds to tweets containing "Mimic me @\<your bot's handle\>" by mimicking the tweeting user based on their twitter history.

The script main.py will take care of almost everything.

But here is what additions you need:

* A text file named 'passwords.txt' containing your twitter consumer key, twitter consumer secret, twitter access token,
    twitter access secret (for your Twitter REST API), and your local administrative password. An example of this document is 
    in the repository as "passwords_example.txt".

* A locally hosted MySQL database named 'my_database' with a table named 'past_mimics' with columns 
    (id INT, screen_name TEXT, date_time TEXT). Of course, you may choose to name these things differently, just edit the 
    main.py script accordingly.

NOTE: If you do not wish to bother MySQL, another option for recording past mimics is in the code, it's just commented out.
You will need to uncomment the code responsible for opening the text file "past_mimics.txt" and for writing into it when a new 
mention is found.
