# Import  dependencies
import time
import tweepy
import feedparser
from fake_useragent import UserAgent
from datetime import datetime, timedelta
from credentials import *
from website_list import *

# Access and authorize Twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Date parsing function
def dt_parse(t):
	ret = datetime.strptime(t[0:16],'%Y-%m-%dT%H:%M')
	if t[18]=='+':
		ret-=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
	elif t[18]=='-':
		ret+=timedelta(hours=int(t[19:22]),minutes=int(t[23:]))
	return ret

# Establish user agent
ua = UserAgent()

# Set initial time
testTime = dt_parse(datetime.utcnow().isoformat())

# Run Shopify website scrubber
while True:
	print(testTime)
	for site in shopify_website_list:
		feed = feedparser.parse(site, agent = ua.random)

		if (feed.status > 199 or feed.status < 300):

			for item in feed.entries:
				item_title = item["title"]
				item_URL = item["link"]
				item_time = dt_parse(item["published"])

				if item_time > testTime:
					api.update_status("%s %s" %(item_title, item_URL))
					print("Item: %s, Item URL: %s, Published: %s" %(item_title, item_URL, item_time))

			print("Site Checked!")

	testTime = dt_parse(datetime.utcnow().isoformat())
	time.sleep(15)