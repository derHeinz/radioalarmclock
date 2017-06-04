#!/usr/bin/python
# -*- coding: utf-8 -*-


class TimeSetter(object):
	"""
	Time Setter acts as Menu item that is able to set time.
	"""
	
	# Default time when no time is set.
	DEFAULT_TIME = "8:00"

	def __init__(self, display, alarm):
		""" gimme display and a default time (20:15) and a function where I set the time."""
		self._display = display
		self._alarm = alarm
		
	def display(self):
		self._display.show_text(self._alarm_text())
		
	def next(self):
		self._add_minutes(10)
		self.display()
		
	def prev(self):
		self._add_minutes(-10)
		self.display()
		
	def select(self):
		# set wake time and return
		self._display.show_text_blinking(self._alarm_text())
		#self._alarm.set_alarm_time(self._time)
		return "back"
		
	def _alarm_text(self):
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