#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from apscheduler.triggers.cron import CronTrigger
from datetime import timedelta
from datetime import datetime


class Player(object):
	''' A player stub that is able to fade in. '''

	FADE_IN_JOB_ID = "Player-Fade-In"
	CHECK_PLAYING_JOB_ID = "Player-Check-Playing"
	
	def __init__(self, scheduler):
		self._url = None
		self._backup_url = None
		self._scheduler = scheduler
		
		self._fadein = False
		self._fadein_steps = 5
		self._fadein_step_size = 8
		self._fadein_interval = 10
		self._fade_in_step = None
		self._fade_in_reset_counters()
		
	def is_running(self):
		return False
		
	# setter and getter for configuration
		
	def set_fadein_step_size(self, val):
		self._fadein_step_size = val
		
	def get_fadein_step_size(self):
		return self._fadein_step_size
	
	def set_fadein_steps(self, val):
		self._fadein_steps = val
		
	def get_fadein_steps(self):
		return self._fadein_steps
		
	def set_fadein_interval(self, val):
		self._fadein_interval = val
		
	def get_fadein_interval(self):
		return self._fadein_interval
		
	def set_fadein(self, val):
		self._fadein = val
		
	def get_fadein(self):
		return self._fadein
		
	def set_url(self, url):
		self._url = url
		
	def get_url(self):
		return self._url
		
	def set_backup_url(self, url):
		self._backup_url = url
		
	def get_backup_url(self):
		return self._backup_url
		
	# volume overrides
	
	def set_volume(self, val):
		pass
		
	def get_volume(self):
		return None
		
	# volume defaults
	
	def volume_up(self, by=5):
		current = self.get_volume()
		self.set_volume(current + by)
		
	def volume_down(self, by=5):
		current = self.get_volume()
		self.set_volume(current - by)
		
	# play feature
		
	def play(self):
		logging.debug("play() issued")
		if (self._fadein):
			self._play_fadein()
		else:
			self._play()
		
	def _play(self):
		self._prepare_check_playing()
		self._play_url(self._url)
		
	def _play_url(self, url):
		pass
		
	def _play_fadein(self):
		# schedule some fade-in
		trig = CronTrigger(second=("*/" + str(self._fadein_interval)))
		self._scheduler.add_job(id=self.FADE_IN_JOB_ID, func=self._fade_in, trigger=trig)
		
	def _fade_in(self):
		logging.debug("fade in")
		next_volume = None
		if (self._fade_in_step == 0):
			# calculate initial volume
			next_volume = self.get_volume() - (self._fadein_step_size * self._fadein_steps)
			self._fade_in_step = 1
		elif (self._fade_in_step == (self._fadein_steps)):
			# this is the last step
			# the last step is usually the same volume than the initial volume :)
			next_volume = self.get_volume() + self._fadein_step_size
			self._scheduler.remove_job(job_id=self.FADE_IN_JOB_ID)
			self._fade_in_reset_counters()
		elif (self._fade_in_step > 0):
			# steps between
			next_volume = self.get_volume() + self._fadein_step_size
			self._fade_in_step += 1
		self.set_volume(next_volume)
		# play if first invocation
		if (self._fade_in_step == 1):
			self._play()
			
	def _get_scheduler(self):
		for job in self._scheduler.get_jobs():
			if (job.id == self.FADE_IN_JOB_ID):
				return job
		
	def _fade_in_reset(self):
		# remove job
		if (self._get_scheduler() != None):
			self._scheduler.remove_job(job_id=self.FADE_IN_JOB_ID)
			# reset the volume to the initial volume
			next_volume = ((self._fadein_steps - (self._fade_in_step) + 1) *  self._fadein_step_size) + self.get_volume()
			self.set_volume(next_volume)
			
			self._fade_in_reset_counters()
			
	def _fade_in_reset_counters(self):
		# reset internal counters
		self._fade_in_step = 0
	
	# check whether it still is playing
	
	def _prepare_check_playing(self):
		logging.debug("start scheduler for checking whether playing")
		delta = timedelta(seconds=10)
		current = datetime.now()
		wake = current + delta
		self._scheduler.add_job(id=self.CHECK_PLAYING_JOB_ID, func=self._check_playing, run_date=wake)		
		
	def _check_playing(self):
		if not self.is_running():
			self.stop()
			logging.debug("playing backup url, main url not playable.")
			self._play_url(self._backup_url)
	
	# stop feature
		
	def stop(self):
		self._stop()
		self._fade_in_reset()
		
	def _stop(self):
		pass
		