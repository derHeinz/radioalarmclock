#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging
from apscheduler.triggers.cron import CronTrigger

class Alarm(object):
	''' Manages the alarm time(s).'''

	ALARM_JOB_ID = "alarm1"
	
	def __init__(self, scheduler, display):
		self._scheduler = scheduler
		self._display = display
		self._alarm_function = None
		
	def set_alarm_function(self, alarm_function):
		self._alarm_function = alarm_function

	def _run_alarm(self):
		logging.info("alarm: running alarm")
		self._alarm_function()

	def get_alarmtime(self):
		alarm = self._get_alarm()
		if (alarm == None):
			return None
		else:
			return  alarm.next_run_time.strftime("%H:%M")
			
	def get_alarm(self):
		if self.get_alarmtime() is None:
			return False
		return True
		
	def set_alarm(self, value):
		if value is True:
			raise ValueError("illegal value given.")
		if value is False:
			self.remove_alarm()
		self._display.set_alarm(value)

	def _get_alarm(self):
		for job in self._scheduler.get_jobs():
			if (job.id == self.ALARM_JOB_ID):
				return job
				
	def remove_alarm(self):
		if (self._get_alarm() != None):
			self._scheduler.remove_job(job_id=self.ALARM_JOB_ID)
			logging.info("setting alarm to: off")

	def set_alarmtime(self, time):
		logging.info("setting alarm to: " + time)
		# split time hour and min
		splitted = time.split(":")
		hours_s = splitted[0]
		minutes_s = splitted[1]
		
		# however create new trigger
		trig = CronTrigger(hour=int(hours_s), minute=int(minutes_s))

		self.remove_alarm()
		self._scheduler.add_job(id=self.ALARM_JOB_ID, func=self._run_alarm, trigger=trig)
		self._display.set_alarm(True)
