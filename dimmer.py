#!/usr/bin/python
# -*- coding: utf-8 -*-

import ephem
import logging

class Dimmer(object):
	def __init__(self, scheduler, display):
		self._observer = ephem.Observer()
		
		self._observer.pressure = 0
		self._observer.horizon = '-6'

		self._display = display

		self.update()

		# Run every 5 minutes
		scheduler.add_job(self.update, 'cron', minute='*/5')

	def set_location(self, lat, lon):
		self._observer.lat = lat
		self._observer.lon = lon
		
	def update(self):
		self._observer.date = ephem.now()

		morning = self._observer.next_rising(ephem.Sun(), use_center=True)
		night = self._observer.next_setting(ephem.Sun(), use_center=True)

		bright = 0
		if morning < night:
			# Morning is sooner, so it must be night
			logging.info("It is night time: min brightness")
			bright = 0
		else:
			logging.info("It is day time. max brightness")
			bright = self._display.get_max_brightness()
		self._display.set_brightness(bright)
