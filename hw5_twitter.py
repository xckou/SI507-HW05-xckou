from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # uncomment line after you install nltk
from nltk.corpus import stopwords
import string

# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download('punkt')

## SI 206 - HW
## COMMENT WITH:
## Your section day/time:
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)

#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this

CACHE_FNAME = 'twitter_cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for key in alphabetized_keys:
        res.append("{}-{}".format(key, params[key]))
    return baseurl + "_".join(res)

def make_request_from_twitter(username, num_tweets):
    baseurl = " https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {"screen_name": username, "count": num_tweets}
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, auth=auth, params=params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() 
        return CACHE_DICTION[unique_ident]    

#Code for Part 1:Get Tweets


print("USER: ", username)
print("TWEETS ANALYZED: ", num_tweets)

response = make_request_from_twitter(username,num_tweets)

file = open("tweets.json" , "w")
# tweets_file = "tweets.json"
file.write(json.dumps(response, indent = 2))
file.close
# print(list_of_tweets[0]["text"])



#Code for Part 2:Analyze Tweets
list_all = []
for tweet in response:
	tokens = nltk.word_tokenize(tweet["text"])
	list_all.append(tokens)
# print(list_all)
# Step 4: Ignore stop words (1) ignore any words that do not start with an alphabetic character [a-zA-Z], 
# (2) ignore 'http', 'https', and 'RT' (these show up a lot in Twitter)
token1 = []
for a in list_all:
	for b in a:
		if b[0] in string.ascii_letters:
			token1.append(b)
# print(token1)


usable_tokens = []
ignore_lst = ["http","https","RT"]
for a in token1:
	if a not in ignore_lst:
		usable_tokens.append(a)
# print(usable_tokens)


usable_tokens_freq_dic = nltk.FreqDist(usable_tokens)
sorted_freq = sorted(usable_tokens_freq_dic.items(), key = lambda x: x[1], reverse = True)
# print(sorted_freq)

# Step 5: Print the 5 most frequently used words using the frequency distribution you just created.
print("5 MOST FREQUENT WORDS:")
for a in sorted_freq [0:5]:
    word, number = a
    print(word,"(",number,")") 


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
