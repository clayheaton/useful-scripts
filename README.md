## useful-scripts
==============

#### twitter_getter.py

v.2 on 11 JAN 2014

This script connects to the free Twitter API and allows you to gather tweets through a persistent stream, through the search API, or from a specified user's profile.

You can save the tweets that you collect either as .csv files, as raw .json files, or push them directly into a local instance of [MongoDB](http://www.mongodb.com/). 

At the moment, if you elect to save .csv files, you will not get all of the metadata that comes along with each tweet -- only a subset of the most important data. This was done to save space on a large project, where the script tracked a stream for 2 months and collected ~ 15 million tweets.

The scripts is provided as-is, with no warranty, and is free to the public domain. Please feel free to take it, use it, modify it, redistribute it, etc. If you make improvements or clean it up, I'll accept pull requests.

*Requirements*

- You must have a Twitter account.
- You must register your Twitter account as a developer at [dev.twitter.com](http://dev.twitter.com).
- You must create an app at dev.twitter.com.
- You must authenticate yourself to use the app that you create.
- You must copy you app's key/secret and your Oauth key/secret and paste them in the top of the `twitter_getter.py` file.
- You must have the pymongo and beautifulsoup4 libraries installed on your computer.
- Developed and tested with python 2.7.5 (Anaconda) and Twython 3.1.2

*Known Issues*

- There are bugs with the new cursor functions in Twython 3.1.2, which is why the search API parts of this script use the "old" search syntax instead of the new cursor syntax.


