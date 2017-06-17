#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_setter import AbstractSetter

class TimeSetter(AbstractSetter):
	"""
	Sets the current time.
	"""
	
	# Default time when no time is set.
	DEFAULT_TIME = "8:00"

	def __init__(self, display, alarm):
		super(TimeSetter, self).__init__(display)
		self._alarm = alarm
		
	def next(self):
		self._add_minutes(10)
		super(TimeSetter, self).next()
		
	def prev(self):
		self._add_minutes(-10)
		super(TimeSetter, self).prev()
		
	def _show_text(self):
		return str(self._alarm.get_alarm_time())
	
	def _add_minutes(self, min):
		time = self._alarm.get_alarm_time()
		if (time == None):
			time = self.DEFAULT_TIME # default time
		splitted = time.split(":")
		hours_s = splitted[0]
		minutes_s = splitted[1]
		
		hours = int(hours_s)
		minutes = int(minutes_s)
		minutes += min
		
		# fix the minutes if the are over- or underrun
		if (minutes >= 60):
			minutes -= 60
			hours += 1
			if (hours > 23):
				hours = 0
			
		if (minutes < 0):
			minutes += 60
			hours -= 1
			if (hours < 0):
				hours = 23
		time_s = str(hours) + ":" + str("%02d" % minutes)
		# TODO: good idea to really set the time?
		self._alarm.set_alarm_time(time_s)
