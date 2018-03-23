#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import logging
import threading

class Timeout(threading.Thread):
	
	def __init__(self, timeout_amount, timeout_func):
		super(Timeout, self).__init__()
		self.setDaemon(True)
		self.interaction()
		self.set_timeout(timeout_amount)
		self.set_timeout_function(timeout_func)
		self._activated = False
		
	def activate(self):
		if not self._activated:
			self._activated = True
			logging.debug("activated timeout")
		
	def deactivate(self):
		if self._activated:
			self._activated = False
			logging.debug("deactivated timeout")
	
	def interaction(self):
		self._lasttime = datetime.datetime.now()
		#logging.debug("interaction")
		
	def set_timeout(self, amount):
		self._timeout = amount
		
	def get_timeout(self):
		return self._timeout
		
	def set_timeout_function(self, func):
		self._timeout_func = func
		
	def _timeout_occured(self):
		logging.debug("timeout occured")
		self.deactivate()
		self._timeout_func()
	
	def run(self):
		while True:
			if (self._activated):
				current_time = datetime.datetime.now()
				break_time = self._lasttime + datetime.timedelta(seconds=self._timeout)
				if (current_time > break_time):
					self._timeout_occured()
			time.sleep(2)
