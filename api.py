import hashlib
import datetime

from google.appengine.ext import webapp

import models


class GeoHandler(webapp.RequestHandler):
	def get(self):
		keyhash = hashlib.md5(self.request.get("lat") + self.request.get("lng")).hexdigest();
		message = False
		timenow = datetime.datetime.now()
		timestamp = timenow.strftime(" %H:%M UTC on %A %eord %B %Y").replace(":", "")
		# Suffix with the ordinal (e.g., "1st", "2nd" or "3rd", "4th").
		if 4 <= timenow.day <= 20 or 24 <= timenow.day <= 30:
			timestamp = timestamp.replace("ord", "th")
		else:
			if timenow.day == 1 or timenow.day == 21 or timenow.day == 31:
				timestamp = timestamp.replace("ord", "st")
			if timenow.day == 2 or timenow.day == 22:
				timestamp = timestamp.replace("ord", "nd")
			if timenow.day == 3 or timenow.day == 23:
				timestamp = timestamp.replace("ord", "nd")
		if self.request.get("note"):
			note = self.request.get("note")
			if len(note) > 0:
				message = "<strong>From the team</strong><br />" + note + "<br />" + timestamp
		if not message:
			message = "<strong>From the team</strong><br />Latest position at<br />" + timestamp
#		self.response.out.write(message)
		location = models.Location.get_or_insert(keyhash, lat=self.request.get("lat"), lng=self.request.get("lng"), note=message)
		self.response.out.write("Location logged<br /><a href='/geo'>Click here to refresh.")
		geolist = models.List.get_or_insert("geolist", list=[])
		if keyhash not in geolist.list:
			geolist.list.append(keyhash)
			newsitem = models.NewsItem.get_or_insert(keyhash, text=message)
