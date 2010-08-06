import os
import datetime

from google.appengine.ext.webapp import template

import yql


def do_yql(query):
	y = yql.Public()
	result = y.execute(query)
	return result


def convert_justgiving_datetime(theirdatetime):
	thisdatetime = datetime.datetime(int("20" + theirdatetime[6: 8]), int(theirdatetime[3: 5]), int(theirdatetime[0: 2]))
	return thisdatetime


def monthname_to_month(monthname):
	if monthname == "Jan":
		month = 1
	if monthname == "Feb":
		month = 2
	if monthname == "Mar":
		month = 3
	if monthname == "Apr":
		month = 4
	if monthname == "May":
		month = 5
	if monthname == "Jun":
		month = 6
	if monthname == "Jul":
		month = 7
	if monthname == "Aug":
		month = 8
	if monthname == "Sep":
		month = 9
	if monthname == "Oct":
		month = 10
	if monthname == "Nov":
		month = 11
	if monthname == "Dec":
		month = 12
	return month



def convert_twitter_rss_datetime(theirdatetime):
	thisdatetime = datetime.datetime(int(theirdatetime[12:16]), monthname_to_month(theirdatetime[8:11]), int(theirdatetime[5:8]), int(theirdatetime[17:19]), int(theirdatetime[20:22]), int(theirdatetime[23:25]))
	return thisdatetime



def render_template(self, end_point, template_values):
	path = os.path.join(os.path.dirname(__file__), "templates/" + end_point)
	response = template.render(path, template_values)
	self.response.out.write(response)
