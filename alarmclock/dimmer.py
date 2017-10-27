#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import dateutil.tz as tz
from dateutil import parser
import urllib2
import json
import logging
from apscheduler.triggers.cron import CronTrigger

class Dimmer(object):

	DIMMER_ID = "Dimmer"

	def __init__(self, scheduler, display):
		self._display = display
		self._scheduler = scheduler
		self._lat = None
		self._lon = None
		# default values
		self._night_percentage = 10
		self._day_percentage = 50
		
	def get_lat(self):
		return self._lat
		
	def set_lat(self, val):
		self._lat = val
		
	def get_lon(self):
		return self._lon
		
	def set_lon(self, val):
		self._lon = val
		
	def get_night_percentage(self):
		return self._night_percentage
		
	def set_night_percentage(self, val):
		self._night_percentage = val
		
	def get_day_percentage(self):
		return self._day_percentage
		
	def set_day_percentage(self, val):
		self._day_percentage = val
		
	def get_active(self):
		return (self._get_job() != None)
	
	def set_active(self, val):
		job = self._get_job()
		if (val is True) and (job == None):
			# Run every 5 minutes
			trig = CronTrigger(minute='*/5')
			self._scheduler.add_job(id=self.DIMMER_ID, func=self.update, trigger=trig)
		elif (val is False) and (job != None):
			self._scheduler.remove_job(job_id=self.DIMMER_ID)
		
	def _get_job(self):
		for job in self._scheduler.get_jobs():
			if (job.id == self.DIMMER_ID):
				return job
		return None
		
	def _cut_plus(self, str):
		last_occ = str.rfind("+")
		return str[:last_occ]
		
	def _cut_last_colon(self, str):
		last_occ = str.rfind(":")
		return str[:last_occ] + str[last_occ+1:]
		
	def update(self):
		# construct url
		url_a = "http://api.sunrise-sunset.org/json?lat="
		url_b = "&lng="
		url_c = "&formatted=0"
		url = url_a + str(self._lat) + url_b + str(self._lon) + url_c
		header = {}
		req = urllib2.Request(url, None, header)
		response = urllib2.urlopen(req)
		response_json = json.load(response)
		results = response_json['results']
		
		time_sunrise_str = results['sunrise']		
		time_sunset_str = results['sunset']
		
		time_sunrise = parser.parse(time_sunrise_str)
		time_sunset = parser.parse(time_sunset_str)
		
		time_now = datetime.utcnow()
		time_now = time_now.replace(tzinfo=tz.gettz("UTC"))
		
		# max brightness
		max = self._display.get_max_brightness()
		new_brightness = 0
		
		if (time_now > time_sunrise and time_now < time_sunset):
			# day
			logging.debug("It is day time")
			new_brightness = int((float(max) / 100) * self._day_percentage)
		else:
			# early morning or night
			logging.debug("It is night time")
			new_brightness = int((float(max) / 100) * self._night_percentage)
		
		self._display.set_brightness(new_brightness)
