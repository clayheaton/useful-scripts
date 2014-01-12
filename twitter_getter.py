#################################################################
## YOU MUST CHANGE THESE VALUES TO MATCH YOUR TWITTER ACCOUNT ###
########### Create an 'application' at dev.twitter.com ##########
########### And then authenticate yourself to use it ############
######... the keys you need are listed on the app's page ########
#################################################################

APP_KEY            =  'YOUR APP_KEY'           
APP_SECRET         =  'YOUR APP_SECRET'        
OAUTH_TOKEN        =  'YOUR OAUTH_TOKEN'       
OAUTH_TOKEN_SECRET =  'YOUR OAUTH_TOKEN_SECRET'

# - Make sure you copy the keys correctly, with no extra spaces
# - and key them inside of quotes, as shown on the right above.

############ NOW RUN THE SCRIPT FROM A COMMAND LINE #############






#################################################################
######################### CHANGELOG #############################
#################################################################

# v.2
# FIXED Bug: when selecting both output types, CSV isn't saved in the proper directory.

# v.1
# Streaming only. CSV header error.

################################################################
########### BE CAREFUL CHANGING STUFF AFTER HERE ###############
################################################################

import sys

def no_creds():
    print "\nPlease edit the script and enter your credentials before use."
    print "Register at dev.twitter.com and create an app to get credentials.\n"
    sys.exit()

if APP_KEY == 'YOUR APP_KEY' or APP_SECRET == "YOUR APP_SECRET" or OAUTH_TOKEN == 'YOUR OAUTH_TOKEN' or OAUTH_TOKEN_SECRET == "YOUR OAUTH_TOKEN_SECRET":
    no_creds()

print "\n"

print " ==================================================================="
print " ||        .-. __ _ .-.                                           ||"
print " ||        |  `  / \  |                                           ||"
print " ||        /     '.()--\                                          ||"
print " ||       |         '._/                                          ||"
print " ||      _| O   _   O |_    PYTHON TWITTER GETTER                 ||"
print " ||      =\    '-'    /=    v.2                                   ||"
print " ||        '-._____.-'      11 JAN 2014                           ||"
print " ||        /`/\___/\`\                                            ||"
print " ||       /\/o     o\/\                                           ||"
print " ||      (_|         |_)                                          ||"
print " ||        |____,____|                                            ||"
print " ||        (____|____)                                            ||"
print " ||                                                               ||"
print " || This script uses the following nonstandard python libraries:  ||"
print " || required: twython, beautifulsoup4                             ||"
print " || optional: pymongo (and a local MongoDB server)                ||"
print " ||                                                               ||"
print " || See dev.twitter.com for additional API parameters             ||"
print " || and rules and rate limits. Anger Twitter at your own risk.    ||"
print " ||                                                               ||"
print " || Script provided as is. Feel free to fork, edit, etc.          ||"
print " || https://github.com/ccheaton/useful-scripts                    ||"
print " ==================================================================="

# If you want to capture additional fields in the .csv output, make 
# certain to include both a line for the header (near line 80) and
# a line for the actual value (near line 115). They must appear in 
# the same logical order or your headers will not be aligned with
# your data.

# Import the libraries that we need

try:
    from twython import Twython
    from twython import TwythonStreamer
except:
    print "========================= ERROR ================================="
    print "You must have the Twython library installed to use this script.\n"
    print "Try typing in your terminal or Powershell: easy_install twython"
    print "=================================================================\n"
    sys.exit()

try:
    from bs4 import BeautifulSoup
except:
    print "========================= ERROR ========================================"
    print "You must have the BeautifulSoup 4 script installed to use this script.\n"
    print "Try typing in your terminal or Powershell: easy_install beautifulsoup4"
    print "======================================================================\n"
    sys.exit()

import json
import csv
import re
import time
import os

# Establish some global variables
counter           = 0
header_done       = False
first_header_done = False
collection        = False
use_mongo         = False
use_json_files    = False
search_terms      = ""
keep_lang         = 'all'
output_dir        = ""

################################################################
########### GATHERING USER INPUT VARIABLES #####################
################################################################

print "\n"
search_type = raw_input("Do you want to catch a Twitter stream (1) get a user timeline (2) or perform a search (3)? ")
print "\n"
try:
    search_type = abs(int(search_type))
except:
    print "You entered an invalid type."
    sys.exit()

if not search_type in (1,2,3):
    print "You entered an invalid type."
    sys.exit()

if search_type == 1:
    while search_terms == "":
        search_terms = raw_input("Enter filter terms or 'sample' to get a sample of the full 'firehose': ")
        print "\n"

if search_type == 3:
    print "----------------------------------------------------------------------------------------------------"
    print "NOTE: Twitter limits search API calls to 15 per rate cycle, for a max of 1500 tweets per rate cycle.\n \
    Each call is limited to 100 tweets, max. That means that if you request 550 tweets on the search API\n \
    that you are making 6 search API calls. See dev.twitter.com for more information.\n"
    print "----------------------------------------------------------------------------------------------------\n"
    while search_terms == "":
        search_terms = raw_input("Enter search terms: ")
        print "\n"

if search_type == 2:
    print "NOTE: Twitter restricts results to approximately 200 per request when you fetch a user timeline.\n"
    name_of_twit = ""
    while name_of_twit == "":
        name_of_twit = raw_input("What is the @screen_name of the user whose timeline you want to get? ")
        print "\n"

if search_type == 1:
    print "You can filter by language. Enter 'all' (without quotes) to keep all languages. "
    print "'en' for English, 'fr' for French, 'es' for Spanish, etc."
    print "If you want to keep two or more, but not all, then enter them with a comma separating them, such as: en,fr,es \n"
    keep_lang = raw_input("What language(s) of tweets do you want to collect? ")
    print "\n"

    keep_lang = keep_lang.strip()

    if keep_lang == "" or len(keep_lang) == 0:
        keep_lang = "all"
        print "Keeping all languages by default."
        print "\n"

    if keep_lang != "all":
        keep_lang = keep_lang.split(",")
        for index,lang in enumerate(keep_lang):
            keep_lang[index] = keep_lang[index].strip()
else:
    keep_lang = "all"

if search_type in (1,3):
    keep_tweets = raw_input("How many tweets do you want to collect? ")
    print "\n"
    try:
        keep_tweets = abs(int(keep_tweets))
    except:
        print "You entered an invalid number. Collecting 50 tweets."
        print "\n"
        keep_tweets = 50

    if keep_tweets is None or keep_tweets == "" or keep_tweets == 0:
        keep_tweets = 50

    if search_type == 3 and keep_tweets > 1500:
        keep_tweets = 1500
else:
    keep_tweets = 200

print "-----------------------------------------------------------------------------------------"
print "NOTE: saving as .csv currently only saves a subset of the data available with each tweet.\n"
print "... Also, the .csv (and .json) files are encoded with UTF-8. If you want to open the .csv"
print "files in Excel, you need to 'import' them as text using Unicode (UTF-8) encoding or you will"
print "not see all of the funky and/or foreign characters that people use in their tweets."
print "-----------------------------------------------------------------------------------------\n"


output_format    = raw_input("Do you want LIMITED .csv files (1), complete JSON (2), or both (3)? ")
print "\n"
try:
    output_format = abs(int(output_format))
except:
    print "Invalid answer. Saving only .csv files.\n"
    output_format = 1



# Directory
if output_format in (1,2,3):
    output_dir = raw_input("In which EXISTING directory do you want to save the output files (return/enter for default)? ")
    output_dir = output_dir.strip().replace('\\','/')
    if not output_dir == "" and not os.path.isdir(output_dir):
        if not output_dir[-1] == "/":
            output_dir += "/"
        if not os.path.isdir(output_dir):
            print "\nThat directory does not exist. Defaulting to script directory."
            output_dir = ""

    if not output_dir == "" and not output_dir[-1] == "/":
        output_dir += "/"

    if output_dir == "":
        print "\nOutputting to script directory."
    else:
        print "\nOutputting to",output_dir,"\n"






# Additional setup options related to JSON
if output_format in (2,3):
    try:
        from pymongo import MongoClient
        capture = raw_input("Do you want to save the JSON to Mongo (1), as .json files (2), or both (3)? ").replace("(","").replace(")","")
        print "\n"
        try:
            capture = abs(int(capture))
        except:
            print "Invalid answer. Saving only .json files."
            print "\n"
            capture = 2


        if capture in (1,3):
            use_mongo = True

        if capture in (2,3):
            use_json_files = True

        if capture not in (1,2,3):
            print "Invalid answer. Saving only .json files."
            print "\n"
            use_mongo = False
            use_json_files = True

        if use_mongo:
            try:
                client   = MongoClient()
                database_name = raw_input("What name do you want to use (or create) for the MongoDB database? (default is 'twitter') ")
                print "\n"

                if database_name == "":
                    database_name = "twitter"
                database = client[database_name]

                collection_name = raw_input("What name do you want to use (or create) for the MongoDB collection in the '" + database_name + "' database? (default is 'tweets') ")
                print "\n"

                if collection_name == "":
                    collection_name = "tweets"
                else:
                    collection_name = "_".join(collection_name.split())

                collection = database[collection_name]

                print "Ok, I'll push tweets into the MongoDB database called '" + database_name + "' and collection called '" + collection_name + "'."
                print "\n"

            except:
                print "========================= WARNING =========================================="
                print "There was a problem with pymongo or MongoDB. Gonna save .json files instead."
                print "==========================================================================\n"
                use_mongo      = False
                use_json_files = True
    except:
        print "-- Install MongoDB and pymongo if you want to save tweets straight to a database. MongoDB must be running. --"
        print "\n"
        use_mongo = False
        use_json_files = True

if output_format == 2 and use_mongo == True and use_json_files == False:
    filename_prefix  = ""
    file_name_suffix = 1
else:
    if output_format in (1,3) or use_json_files == True:
        if output_format in (1,3) or (output_format == 2 and use_json_files is True):
            tweets_per_file  = raw_input("How many tweets do you want per output .csv/.json file? ")
            print "\n"
            try:
                tweets_per_file = abs(int(tweets_per_file))
            except:
                print "You entered an invalid number. Storing 5000 tweets per output file."
                print "\n"
                tweets_per_file = 5000

            if tweets_per_file is None or tweets_per_file == "" or tweets_per_file == 0:
                tweets_per_file = 5000

            # Additional setup options related to .csv files
            if keep_tweets > tweets_per_file:
                if output_format in (1,3):
                    include_header_in_each_file = raw_input("Do you want headers only in the first .csv file (1) or in all .csv files (2)? ")
                    print "\n"
                    try:
                        include_header_in_each_file = abs(int(include_header_in_each_file))
                    except:
                        print "Invalid answer. Only putting headers in the first file."
                        include_header_in_each_file = 1

                    if include_header_in_each_file == 1:
                        include_header_in_each_file = False
                    elif include_header_in_each_file == 2:
                        include_header_in_each_file = True
                    else:
                        include_header_in_each_file = False
            else:
                include_header_in_each_file = False

        else:
            tweets_per_file = 5000

        print "-----------------------------------------------------------------------------------------"
        print "File names will be in the form 'prefix_csv_tweets_1.csv' or 'prefix_json_tweets_1.csv'."
        print "Additional files generated while the script is running will increment the suffix number."
        print "-----------------------------------------------------------------------------------------\n"

        file_name_suffix = raw_input("What integer do you want to use as the suffix for the first file generated? ")
        print "\n"
        try:
            file_name_suffix = abs(int(file_name_suffix))
        except:
            print "You entered an invalid number. Setting the initial suffix to 1.\n"
            file_name_suffix = 1
    else:
        file_name_suffix = 1

    # We're writing a file, so get the prefix for the file.
    filename_prefix  = raw_input("Enter a prefix for your output file(s) (or 'return' for blank): ")
    print "\n"


# Prettyfy the prefix for output files
if filename_prefix is None:
    filename_prefix = ""
elif len(filename_prefix) > 0 and filename_prefix[-1] != "_":
    filename_prefix = filename_prefix + "_"






# Start the timer
start = time.time()

################################################################
######################### DEFINING CLASSES #####################
################################################################


# The DasTweetMaker class processes tweets for output to csv.
class DasTweetMaker():
    def clean(self,text):
        text = text.replace("\n"," ").replace("\r"," ") # Remove newline characters
        text = text.replace('"', "'") # Convert double-quotes to single quotes
        text = text.replace(','," ")  # Remove commas
        text = " ".join(text.split()) # Remove extra spaces and tabs
        return text

    def fix_source(self,a_href):
        soup = BeautifulSoup(a_href)
        src  = soup.find('a')
        if src is not None:
            return src.text.encode("utf-8","replace")
        else:
            return ""

    def create_header(self):
        global file_name_suffix

        header = []
        tweets = open(output_dir + filename_prefix + "csv_tweets_" + str(file_name_suffix) + ".csv", 'ab+')
        wr     = csv.writer(tweets, dialect='excel')

        header.append("created_at")
        header.append("tweet_id")
        header.append("lang")
        header.append("is_retweet")
        header.append("screen_name")
        header.append("tweet")
        header.append("source")
        header.append("in_reply_to_status_id")
        header.append("in_reply_to_screen_name")
        header.append("geo")
        wr.writerow(header)

        tweets.close()

    def process(self, tweet):
        global first_header_done
        global header_done
        global file_name_suffix
        global counter

        if first_header_done is False or (header_done is False and include_header_in_each_file is True):
            self.create_header()
            first_header_done = True
            header_done       = True

        # Create the file or append to the existing
        theOutput = []

        # Hi kids. We're writing UTF-8 which can be a pain in the ass. You shouldn't get encoding errors.
        # If you do, then for the love all all holy, don't ask me about it. Just kidding. Just don't ask
        # me about it until you have a few drinks and search StackOverflow.com for the error messages
        # And don't try to READ a csv file with Unicode/UTF-8 characters using the standard
        # python csv library.

        theOutput.append(tweet['created_at'])
        theOutput.append(tweet['id'])
        theOutput.append(tweet['lang'].encode('utf-8', 'replace'))

        if "retweeted_status" in tweet:
            theOutput.append(1)
        else:
            theOutput.append(0)

        uname = tweet['user']['screen_name'].encode('utf-8', 'replace')
        newuname = re.sub('\n','',uname)
        theOutput.append(newuname)

        twt = self.clean(tweet['text']).encode('utf-8', 'replace')
        newtwt = re.sub('\n','',twt)
        theOutput.append(newtwt)
        
        theOutput.append(self.fix_source(tweet['source']))
        theOutput.append(tweet['in_reply_to_status_id'])
        theOutput.append(tweet['in_reply_to_screen_name'])

        if tweet['geo'] is not None:
            if tweet['geo']['type'] == 'Point':
                lat = str(tweet['geo']['coordinates'][0]) + " "
                lon = str(tweet['geo']['coordinates'][1])
                theOutput.append(lat + lon)
            else:
                theOutput.append(tweet['geo'])
        else:
            theOutput.append(tweet['geo'])

        tweets = open(output_dir + filename_prefix + "csv_tweets_" + str(file_name_suffix) + ".csv", 'ab+')
        wr     = csv.writer(tweets, dialect='excel')
        wr.writerow(theOutput)
        tweets.close()

# APSS parallelized

class TweetSaver():
    def __init__(self):
        self.writer = DasTweetMaker()

    def handleTweet(self,data):
        global file_name_suffix
        global output_format
        global use_mongo
        global use_json_files
        global collection
        global client
        global counter
        global tweets_per_file
        global header_done

        # Increment the counter
        counter += 1

        if counter % tweets_per_file == 0:
            # Increment the file name
            header_done       = False
            file_name_suffix += 1

        if output_format in (2,3):
            if use_json_files:
                # Keep the JSON files
                g = open(output_dir + filename_prefix + "json_tweets_" + str(file_name_suffix) + ".json", "ab+")
                json.dump(data,g)
                g.write("\n")
                g.close()
            if use_mongo:
                # Push the JSON into MongoDB
                collection.insert(data)

        if output_format in (1,3):
            # Keep the CSV
            self.writer.process(data)   



# This is the class that handles the streaming.
# Stream on, stream on, stream until your stream comes true...
class MyStreamer(TwythonStreamer):
    def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
        super( MyStreamer, self ).__init__(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.saver = TweetSaver()

    def on_success(self, data):
        global counter
        global keep_lang
        global keep_tweets
        global include_header_in_each_file
        global header_done
        global tweets_per_file
        global file_name_suffix
        global output_format
        global use_mongo
        global use_json_files
        global collection
        global client
        global start

        if 'text' in data:
            if not 'lang' in data or (keep_lang == 'all' or data['lang'] in keep_lang):

                end = time.time()
                elapsed = end - start
                if int(elapsed) % 60 == 0:
                    rate = float(counter) / (elapsed/60)
                    print counter,"tweets at a rate of",int(rate),"per minute after",int(elapsed/60),"minutes."

                # The saver object handles the saving of the data
                self.saver.handleTweet(data)

                if not output_format in (1,2,3):
                    print "You entered an invalid output format."
                    self.disconnect()

        # Disconnect if we've gathered all of the tweets requested
        if counter >= keep_tweets:
            self.disconnect()
            if use_mongo:
                client.disconnect()

    # Something went wrong... oh noes
    def on_error(self, status_code, data):
        global use_mongo
        print status_code, data
        print "---- END WITH ERROR ----\n\n"
        if use_mongo:
            client.disconnect()

#########################################################
########## Function needed for search API results #######
#########################################################

def processTweetsSaveAPI(results):
    saver = TweetSaver()
    init_maxid = True

    # Make sure maxid is defined
    try:
        maxid
    except:
        maxid = "x"

    for res in results['statuses']:
        if init_maxid is True:
            maxid = int(res['id_str']) - 1
            init_maxid = False
        else:
            if int(res['id_str']) < maxid:
                maxid = int(res['id_str']) - 1
        saver.handleTweet(res)
    return maxid


#########################################################
########## This is where things start to happen #########
#########################################################

print "Talking to Twitter. Wait patiently and monitor your output directory."




# For the streaming API -- implement TweetSaver()
if search_type == 1:
    # Create the Twython object and authenticate
    stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    # Open the socket to Twitter and receive the stream
    if search_terms == "sample":
        stream.statuses.sample()
    else:
        stream.statuses.filter(track=search_terms)




# For the user timeline search
elif search_type == 2:
    twitter       = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    timeline      = twitter.get_user_timeline(screen_name=name_of_twit,count=200,include_rts=1)
    saver         = TweetSaver()
    for tweet in timeline:
        saver.handleTweet(tweet)




# For the search API
elif search_type == 3:
    # tweet search 
    twitter       = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    t_keep_tweets = keep_tweets
    # Hi there. You are wondering if you can use more search parameters. Yes, yes you can.
    # Read about them here: https://dev.twitter.com/docs/api/1.1/get/search/tweets

    results = twitter.cursor(twitter.search,q=search_terms)

    maxid = "x" # Do not change this

    while t_keep_tweets > 100:
        if maxid == "x":
            # print "while loop initial search without maxid"
            results = twitter.search(q=search_terms,count=100)
            maxid = processTweetsSaveAPI(results) # Why is this a problem?
        else:
            # print "while loop paginated search maxid:",maxid
            results = twitter.search(q=search_terms,max_id=maxid,count=100)
            maxid = processTweetsSaveAPI(results)
        t_keep_tweets -= 100

    if t_keep_tweets <= 100:
        # print "\n LESS THAN 100 TO FETCH"
        if maxid == "x":
            # print "initial lt 100 search without maxid"
            results = twitter.search(q=search_terms,count=t_keep_tweets)
        else:
            # print "paginated lt 100 search:",maxid
            results = twitter.search(q=search_terms,max_id=maxid,count=t_keep_tweets)

        processTweetsSaveAPI(results)

print "\nOk all done. Bye bye.\n"