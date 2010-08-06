import base64
import urllib

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from django.utils import simplejson

import helpers
import models


def urlencode_variable(variable):
	tmp = urllib.urlencode({'x':variable})
	variable = tmp[2:]
	return variable


def post_to_twitter(message):
	message = urlencode_variable(message)
	url = "http://twitter.com/statuses/update.json?status=" + message
	username = "childsiklimb"
	password = "kilimanjaro"
	base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
	headers = {'Authorization': "Basic %s" % base64string} 
	result = urlfetch.fetch(url, method=urlfetch.POST, headers=headers)
	json = simplejson.loads(result.content)
	return json



class TwitterPoster(webapp.RequestHandler):
	def get(self):
		if self.request.get("secret") == "k1lim4njar0":
			self.response.out.write(post_to_twitter(self.request.get("message")))



class TwitterScraper(webapp.RequestHandler):
	def get(self):
		query = "select guid, title, pubDate from rss where url='http://twitter.com/statuses/user_timeline/162386848.rss'"
		results = helpers.do_yql(query)['query']['results']['item']
		twitterlist = models.List.get_or_insert("twitterlist", list=[])
		for item in results:
			created_at = helpers.convert_twitter_rss_datetime(item['pubDate'])
			text = item['title'].replace("\n", " ")
			tweet_id = item['guid'].replace("http://twitter.com/childsiklimb/statuses/", "")
			if not tweet_id in twitterlist.list:
				twitterlist.list.append(tweet_id)
				twitterlist.put()
				tweet = models.Tweet.get_or_insert(tweet_id, tweet_id=tweet_id, text=text, created_at=created_at)
				message = "<span class='tweet'>" + text + "</span>"
				newsitem = models.NewsItem.get_or_insert(tweet_id, text=text, created_at=created_at)
			self.response.out.write(created_at)
			self.response.out.write("<br />")
			self.response.out.write(tweet_id)
			self.response.out.write("<br />")
			self.response.out.write(text)
			self.response.out.write("<br />")
			self.response.out.write("<br />")
			self.response.out.write("<br />")


