#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import memcache


import helpers
import initialdata
import models
import justgiving
import flickr
import twitter
import twilio
import api
import audio
import geo


def get_total():
	total = memcache.get("total")
	if not total:
		donationsets = models.DonationSet.all()
		total = 0.0
		for donationset in donationsets:
			total += donationset.online
			total += donationset.offline
			total += donationset.giftaid
		memcache.add("total", total, 300)
	return total


def get_news(number):
#	newsitems = models.NewsItem.all().order('-created_at').filter('display =', True).fetch(number)
	newsitems = models.NewsItem.all().order('-created_at').fetch(number)
	return newsitems


def get_images(number):
#	images = models.Flickr.all().order('-created_at').filter('display =', True).fetch(number)
	images = models.Flickr.all().order('-created_at').fetch(number)
	return images
	


def get_locations(number):
	locations = models.Location.all().order('-created_at').fetch(number)
	return locations

class MainHandler(webapp.RequestHandler):
	def get(self):
		template_values = {
			"climbers": initialdata.CLIMBERS,
			"total": get_total(),
			"newsitems": get_news(5),
			"images": get_images(10),
			"locations": get_locations(10),
		}
		helpers.render_template(self, "index.html", template_values)
		


class ImageDetailsHandler(webapp.RequestHandler):
	def get(self, imagekey):
		image = models.Flickr.get_by_key_name(imagekey)
		template_values = {
			"image": image
		}
		helpers.render_template(self, "image.html", template_values)


class AudioDetailsHandler(webapp.RequestHandler):
	def get(self, voicekey):
		voice = models.Voice.get_by_key_name(voicekey)
		template_values = {
			"voice": voice,
			"voicekey": voicekey,
		}
		helpers.render_template(self, "audio.html", template_values)



class GeoHandler(webapp.RequestHandler):
	def get(self):
		template_values = {
		}
		helpers.render_template(self, "geoclient.html", template_values)


class MigrateHandler(webapp.RequestHandler):
	def get(self):
		newsitems = models.NewsItem.all()
		for newsitem in newsitems:
			newsitem.display = True
			newsitem.put()


def main():
    application = webapp.WSGIApplication([
		('/', MainHandler),
		('/geo', GeoHandler),
		('/api/geo', api.GeoHandler),
		('/migrate', MigrateHandler),
		('/image/(.*)', ImageDetailsHandler),
		('/scrape/justgiving/queue', justgiving.JustGivingScraperQueue),
		('/scrape/justgiving', justgiving.JustGivingScraper),
		('/scrape/flickr', flickr.FlickrScraper),
		('/scrape/flickrshortner', flickr.FlickrShortner),
		('/scrape/twitter', twitter.TwitterScraper),
		('/twitter/post', twitter.TwitterPoster),
		('/scrape/gmap', geo.GMapScraper),
		('/scrape/fb', geo.FBScraper),
		('/sms', twilio.SMSHandler),
		('/phone', twilio.AudioHandler),
		('/phone/record', twilio.AudioRecordingHandler),
		('/audio/play/(.*).mp3', audio.PlayHandler),
		('/audio/(.*)', AudioDetailsHandler),
		('/audio/cache', audio.CacheHandler),
	], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
