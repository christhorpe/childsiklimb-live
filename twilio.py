import hashlib

from google.appengine.ext import webapp
from google.appengine.api.labs import taskqueue

import initialdata
import models
import helpers



class SMSHandler(webapp.RequestHandler):
	def post(self):
		self.get()
	def get(self):
		caller = self.request.get("From")
		message = self.request.get("Body")
		if caller in initialdata.PHONES:
			sms = models.SMS(caller=caller, message=message).put()
			taskqueue.add(url="/twitter/post", params={"secret": "k1lim4njar0", "message": message}, method='GET')
			self.response.out.write(sms)



class AudioHandler(webapp.RequestHandler):
	def post(self):
		self.get()
	def get(self):
		caller = self.request.get("Caller")
		template_values = {}
		if caller in initialdata.PHONES:
			helpers.render_template(self, "index.twml", template_values)
		else:
			helpers.render_template(self, "error.twml", template_values)



class AudioRecordingHandler(webapp.RequestHandler):
	def get(self):
		template_values = {}
		caller = self.request.get("Caller")
		if caller in initialdata.PHONES:
			audio_url = self.request.get("RecordingUrl")
			keyhash = hashlib.md5(caller + audio_url).hexdigest();
			voice = models.Voice.get_or_insert(keyhash, audio_url=audio_url)
			helpers.render_template(self, "end.twml", template_values)
			voicelist = models.List.get_or_insert("voicelist", list=[])
			if keyhash not in voicelist.list:
				voicelist.list.append(keyhash)
				message = "<a href='javascript:showAudio(\""+ keyhash +"\")'>New phone message from the team to listen to</a>"
				newsitem = models.NewsItem.get_or_insert(keyhash, text=message)
				taskqueue.add(url="/audio/cache", params={"voice":keyhash}, method='GET')
