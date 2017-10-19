#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from apscheduler.triggers.cron import CronTrigger

class Player(object):
	''' A player stub.'''
	
	FADE_IN_STEP_SIZE = 8
	FADE_IN_STEPS = 5
	FADE_IN_JOB_ID = "Player-Fade-In"
	
	def __init__(self, scheduler):
		self._url = None
		self._scheduler = scheduler
		
		self._fadein = False
		self._fadeout = False
		self._fade_in_step = None
		self._fade_in_reset_counters()
		
	def is_running(self):
		return False
		
	# setter and getter for configuration
		
	def set_fadein(self, val):
		self._fadein = val
		
	def get_fadein(self):
		return self._fadein
		
	def set_fadeout(self, val):
		self._fadeout = val
		
	def get_fadeout(self):
		return self._fadeout
		
	def set_url(self, url):
		self._url = url
		
	def get_url(self):
		return self._url
		
	def set_volume(self, val):
		pass
		
	def get_volume(self):
		return None
		
	# play feature
		
	def play(self):
		logging.debug("play() issued")
		if (self._fadein):
			self._play_fadein()
		else:
			self._play()
		
	def _play(self):
		pass
		
	def _play_fadein(self):
		# schedule some fade-in
		trig = CronTrigger(second="*/10")
		self._scheduler.add_job(id=self.FADE_IN_JOB_ID, func=self._fade_in, trigger=trig)
		
	def _fade_in(self):
		logging.debug("fade in")
		next_volume = None
		if (self._fade_in_step == 0):
			# calculate initial volume
			next_volume = self.get_volume() - (self.FADE_IN_STEP_SIZE * self.FADE_IN_STEPS)
			self._fade_in_step = 1
		elif (self._fade_in_step == (self.FADE_IN_STEPS)):
			# this is the last step
			# the last step is usually the same volume than the initial volume :)
			next_volume = self.get_volume() + self.FADE_IN_STEP_SIZE
			self._scheduler.remove_job(job_id=self.FADE_IN_JOB_ID)
		elif (self._fade_in_step > 0):
			# steps between
			next_volume = self.get_volume() + self.FADE_IN_STEP_SIZE
			self._fade_in_step += 1
		self.set_volume(next_volume)
		# play if first invocation
		if (self._fade_in_step == 1):
			self._play()
		
	def _fade_in_reset(self):
		# remove job
		self._scheduler.remove_job(job_id=self.FADE_IN_JOB_ID)
		self._fade_in_reset_volume()
		self._fade_in_reset_counters()
			
	def _fade_in_reset_counters(self):
		# reset internal counters
		self._fade_in_step = 0
		
	def _fade_in_reset_volume(self):
		# reset the volume to the initial volume
		next_volume = ((self.FADE_IN_STEPS - self._fade_in_step) *  self.FADE_IN_STEP_SIZE) + self.get_volume()
		self.set_volume(next_volume)
		
	# stop feature
		
	def stop(self):
		self._fade_in_reset()
		self._stop()
		
	def _stop(self):
		pass
		