from google.appengine.ext import webapp
from google.appengine.api import urlfetch

import models


class CacheHandler(webapp.RequestHandler):
	def get(self):
		voicekey = self.request.get("voice")
		self.response.out.write(voicekey)
		voice = models.Voice.get_by_key_name(voicekey)
		if voice:
			result = urlfetch.fetch(voice.audio_url + ".mp3")
			if result.status_code == 200:
				voice.audio = result.content
				voice.put()
				voicelist = models.List.get_or_insert("voicelist", list=[])
				if voicekey not in voicelist.list:
					voicelist.list.append(voicekey)
					message = "<a href='javascript:showAudio(\""+ voicekey +"\")'>New phone message from the team to listen to</a>"
					newsitem = models.NewsItem.get_or_insert(voice, text=message)


class PlayHandler(webapp.RequestHandler):
	def get(self, voicekey):
		voice = models.Voice.get_by_key_name(voicekey)
		if voice:
			self.response.headers['Content-Type'] = 'audio/x-mpeg'
			self.response.out.write(voice.audio)
		
