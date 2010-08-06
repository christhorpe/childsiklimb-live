import datetime

from google.appengine.ext import webapp
from google.appengine.api.labs import taskqueue


import helpers
import models





class FlickrShortner(webapp.RequestHandler):
	def get(self):
		flickr = models.Flickr.get_by_key_name(self.request.get("flickr_secret"))
		query = "select content from html where url=\"http://www.timparenti.com/dev/flickr/shortlink/?id=%s\" and xpath=\"//a[@id='shortLink']\"" % flickr.flickr_id
		results = helpers.do_yql(query)['query']['results']['a']
		if not flickr.short_url:
			flickr.short_url = results
			flickr.put()
			taskqueue.add(url="/twitter/post", params={"secret": "k1lim4njar0", "message": flickr.title + " : " + flickr.short_url}, method='GET')
		self.response.out.write(results)



class FlickrScraper(webapp.RequestHandler):
	def get(self):
		query = "SELECT * FROM flickr.people.publicphotos(0,10) WHERE user_id='51711675@N02' AND extras='url_sq, date_upload, url_m'"
		results = helpers.do_yql(query)['query']['results']['photo']
		flickrlist = models.List.get_or_insert("flickrlist", list=[])
		for photo in results:
			created_at = datetime.datetime.fromtimestamp(float(photo['dateupload']))
			flickr_id = photo['id']
			flickr_secret = photo['secret']
			square = photo['url_sq']
			medium = photo['url_m']
			title = photo['title']
			if flickr_secret not in flickrlist.list:
				flickrlist.list.append(flickr_secret)
				flickrlist.put()
				flickr = models.Flickr.get_or_insert(flickr_secret, flickr_secret=flickr_secret, created_at=created_at, flickr_id=flickr_id, square=square, medium=medium, title=title)
				taskqueue.add(url="/scrape/flickrshortner", params={"flickr_secret": flickr_secret}, method='GET')
				message = "<span class='newsimg'><img src='"+ square +"' height='45' width='45' alt='"+ title +"'/></span>" + "<a href='javascript:showImage(\""+ flickr_secret +"\")'>" + title + "</a>"
				newsitem = models.NewsItem.get_or_insert(flickr_secret, text=message, created_at=created_at)
			self.response.out.write(created_at)
			self.response.out.write("<br />")
			self.response.out.write(square)
			self.response.out.write("<br />")
			self.response.out.write(medium)
			self.response.out.write("<br />")
			self.response.out.write(title)
			self.response.out.write("<br />")
			self.response.out.write(flickr_id)
			self.response.out.write("<br />")
			self.response.out.write("<br />")
