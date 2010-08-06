import hashlib
import base64

from google.appengine.ext import webapp
from google.appengine.api import urlfetch

import helpers
import models



class FBScraper(webapp.RequestHandler):
	def get(self):
		url = "http://www.facebook.com/pages/Childs-i-Klimb/297046608283"
		result = urlfetch.fetch(url)
		if result.status_code == 200:
  			self.response.out.write(result.content)


		
class GMapScraper(webapp.RequestHandler):
	def get(self):
		url = self.request.get("url")
		query = "select script from html where url=\"http://maps.google.com/maps/ms?ie=UTF8&hl=en&msa=0&ll=-3.073324,37.411366&spn=0.126847,0.245819&t=h&z=13&msid=116890249293007182618.00048088bb3d7fc8d89e1\""
		results = helpers.do_yql(query)['query']['results']['body']
		for result in results:
			item = str(result['script']['content'])
			if "KEOB" in item:
				things = item.split("KEOB")
				geoelements = things[1].split("@")
				messageelements = things[3].split("@")
				latlng = geoelements[1][0:geoelements[1].find("\"")]
				lat = latlng.split(",")[0]
				lng = latlng.split(",")[1]
				messagebits = messageelements[1].replace("\",infoWindow:{title:\"", "").replace("\\", "").replace("x3c", "").replace("x3e", "").replace("/div", "").replace("\n", " ").split(":brbr")
				self.response.out.write(lat)
				self.response.out.write("<br />")			
				self.response.out.write(lng)
				self.response.out.write("<br />")			
				self.response.out.write("<br />")
				note = "<strong>From TeamKilimanjaro Guides</strong><br />" + messagebits[1].strip() + "<br />" + messagebits[0].strip()
				self.response.out.write(note)
				self.response.out.write("<br />")			
				self.response.out.write("<br />")
				keyhash = hashlib.md5(lat + lng).hexdigest();
				location = models.Location.get_or_insert(keyhash, lat=lat, lng=lng, note=note)
				geolist = models.List.get_or_insert("geolist", list=[])
				if keyhash not in geolist.list:
					geolist.list.append(keyhash)
					newsitem = models.NewsItem.get_or_insert(keyhash, text=note)

				
				
