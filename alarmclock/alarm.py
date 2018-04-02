#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging
from apscheduler.triggers.cron import CronTrigger

class Alarm(object):
	''' Manages the alarm time(s).'''

	ALARM_JOB_ID_1 = "alarm1"
	ALARM_JOB_ID_2 = "alarm2"
	
	# ##############
	# API Functions
	# ##############
	
	def __init__(self, scheduler, display):
		self._scheduler = scheduler
		self._display = display
		self._alarm_function_1 = None
		self._alarm_function_2 = None
		
	def set_alarm_function_1(self, alarm_function):
		self._alarm_function_1 = alarm_function
	
	def set_alarm_function_2(self, alarm_function):
		self._alarm_function_2 = alarm_function
		
	def get_alarmtime_1(self):
		return self._get_alarmtime(self.ALARM_JOB_ID_1)
		
	def get_alarmtime_2(self):
		return self._get_alarmtime(self.ALARM_JOB_ID_2)
		
	def set_alarmtime_1(self, time):
		self._set_alarmtime(time, self.ALARM_JOB_ID_1, self._run_alarm_1)
	
	def set_alarmtime_2(self, time):
		self._set_alarmtime(time, self.ALARM_JOB_ID_2, self._run_alarm_2)
		
	def get_alarm_1(self):	
		return self._get_alarm_activated(self.ALARM_JOB_ID_1)
		
	def get_alarm_2(self):
		return self._get_alarm_activated(self.ALARM_JOB_ID_2)
		
	def set_alarm_1(self, value):
		self._set_alarm(value, self.ALARM_JOB_ID_1)
	
	def set_alarm_2(self, value):
		self._set_alarm(value, self.ALARM_JOB_ID_2)
	
	def remove_alarm_1(self):
		self._remove_alarm(self.ALARM_JOB_ID_1)
		
	def remove_alarm_2(self):
		self._remove_alarm(self.ALARM_JOB_ID_2)
	
	# ###################
	# Internal Functions
	# ###################
	
	def _run_alarm_1(self):
		self._run_alarm(self.ALARM_JOB_ID_1, self._alarm_function_1())
		
	def _run_alarm_2(self):
		self._run_alarm(self.ALARM_JOB_ID_2, self._alarm_function_2())
		
	def _run_alarm(self, alarm_job, method_to_run):
		logging.debug(alarm_job + ": running alarm")
		method_to_run()

	def _get_alarmtime(self, alarm_job):
		alarm = self._get_alarm(alarm_job)
		if (alarm == None):
			return None
		else:
			result = alarm.next_run_time.strftime("%H:%M")
			if result.startswith("0"):
				return result.replace("0", " ", 1)
			return result
			
	def _get_alarm_activated(self, alarm_job):
		if self._get_alarmtime(alarm_job) is None:
			return False
		return True
		
	def _get_alarm(self, alarm_job):
		for job in self._scheduler.get_jobs():
			if (job.id == alarm_job):
				return job
		
	def _set_alarm(self, value, alarm_job):
		if value is True:
			raise ValueError("illegal value given.")
		if value is False:
			self._remove_alarm(alarm_job)
		
		self._set_display_alarm(value, alarm_job)
		
	def _remove_alarm(self, alarm_job):
		if (self._get_alarm(alarm_job) != None):
			self._scheduler.remove_job(job_id=alarm_job)
			logging.debug("setting alarm " + alarm_job + " to: off")

	def _set_alarmtime(self, time, alarm_job, method_to_run):
		logging.debug("setting alarm " + alarm_job + " to: " + time)
		# split time hour and min
		splitted = time.split(":")
		hours_s = splitted[0]
		minutes_s = splitted[1]
		
		# however create new trigger
		trig = CronTrigger(hour=int(hours_s), minute=int(minutes_s))

		self._remove_alarm(alarm_job)
		self._scheduler.add_job(id=alarm_job, func=method_to_run, trigger=trig)
		self._set_display_alarm(True, alarm_job)
		
	def _set_display_alarm(self, value, alarm_job):
		# TODO only because we don't want to propagate the dualism of alarms any further
		if (alarm_job == self.ALARM_JOB_ID_1):
			self._display.set_alarm_1(value)	
		elif (alarm_job == self.ALARM_JOB_ID_2):
			self._display.set_alarm_2(value)
