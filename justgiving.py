import hashlib

from google.appengine.ext import webapp
from google.appengine.api.labs import taskqueue

import initialdata
import helpers
import models




class JustGivingScraperQueue(webapp.RequestHandler):
	def get(self):
		climbers = initialdata.CLIMBERS
		for climber in climbers:
			if len(climber['justgiving']) > 0:
				taskqueue.add(url="/scrape/justgiving", params={"url": climber['justgiving']}, method='GET')


		
class JustGivingScraper(webapp.RequestHandler):
	def get(self):
		url = self.request.get("url")
		query = "select * from html where url=\"%s\" and (xpath=\"//table[@class='frp-totals']/tbody/tr/td/p\" or xpath=\"//table[@class='tbl-donations']/tbody/tr\")" % url
		results = helpers.do_yql(query)['query']['results']
		totals = results['p']
		donations = results['tr']
		online = float(totals[0][1:len(totals[0])].replace(",", ""))
		offline = float(totals[1][1:len(totals[1])].replace(",", ""))
		giftaid = float(totals[2][1:len(totals[2])].replace(",", ""))
		donationset = models.DonationSet.get_or_insert(url, url=url, online=online, offline=offline, giftaid=giftaid)
		donationlist = models.List.get_or_insert("donationlist", list=[])
		donationset.online = online
		donationset.offline = offline
		donationset.giftaid = giftaid
		donationset.put()
		self.response.out.write(online)
		self.response.out.write("<br />")
		self.response.out.write(offline)
		self.response.out.write("<br />")
		self.response.out.write(giftaid)
		self.response.out.write("<br />")
		self.response.out.write("<br />")
		for donation in donations:			
			donationdetails = donation['td'][1]['div']['p']['span']
			self.response.out.write(donationdetails)
			message = donationdetails[0]['content'].replace("\n", " ")
			try:
				donor = donationdetails[1]['strong'].strip().replace("\n", " ")
				date = helpers.convert_justgiving_datetime(donationdetails[2])
				rawdate = donationdetails[2]
			except:
				donor = "Anonymous"
				date = helpers.convert_justgiving_datetime(donationdetails[1])
				rawdate = donationdetails[1]
			try:
				rawamount = donation['td'][2]['strong']
				amount = rawamount
				#			amount = rawamount[1:len(rawamount)]
			except:
				amount = ""
			keyhash = hashlib.md5(str(url + donor + rawdate.replace("/", ""))).hexdigest()
			if keyhash not in donationlist.list:
				donation = models.Donation.get_or_insert(keyhash, keyhash=keyhash, date=date, amount=amount, donor=donor, message=message)
				donationlist.list.append(keyhash)
				donationlist.put()
				message = "<strong>" + donor + "</strong> has donated " + amount
				newsitem = models.NewsItem.get_or_insert(keyhash, text=message)
			self.response.out.write(message)
			self.response.out.write("<br />")
			self.response.out.write(donor)
			self.response.out.write("<br />")
			self.response.out.write(date)
			self.response.out.write("<br />")
			self.response.out.write(amount)
			self.response.out.write("<br />")
			self.response.out.write(keyhash)
			self.response.out.write("<br />")
			self.response.out.write("<br />")
