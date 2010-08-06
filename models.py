from google.appengine.ext import db


class DonationSet(db.Model):
	url = db.StringProperty()
	online = db.FloatProperty()
	offline = db.FloatProperty()
	giftaid = db.FloatProperty()


class Donation(db.Model):
	keyhash = db.StringProperty()
	date = db.DateTimeProperty()
	amount = db.StringProperty()
	donor = db.StringProperty()
	url = db.StringProperty()


class NewsItem(db.Model):
	created_at = db.DateTimeProperty(auto_now_add=True)
	text = db.StringProperty()
	display = db.BooleanProperty(default=True)


class List(db.Model):
	list = db.StringListProperty()


class Tweet(db.Model):
	tweet_id = db.StringProperty()
	text = db.StringProperty()
	created_at = db.DateTimeProperty()
	display = db.BooleanProperty(default=True)


class Flickr(db.Model):
	flickr_secret = db.StringProperty()
	flickr_id = db.StringProperty()
	short_url = db.StringProperty()
	square = db.StringProperty()
	medium = db.StringProperty()
	title = db.StringProperty()
	created_at = db.DateTimeProperty()
	display = db.BooleanProperty(default=True)


class Location(db.Model):
	created_at = db.DateTimeProperty(auto_now_add=True)
	lat = db.StringProperty()	
	lng = db.StringProperty()
	note = db.TextProperty()


class Voice(db.Model):
	audio = db.BlobProperty()
	audio_url = db.StringProperty()
	created_at = db.DateTimeProperty(auto_now_add=True)


class SMS(db.Model):
	caller = db.StringProperty()
	message = db.StringProperty()
