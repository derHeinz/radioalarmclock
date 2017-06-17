#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import logging

class Player:
	"""
	The player for linux use.
	"""
	
	SOUNDCARD_NAME = "PCM"
	
	def __init__(self):
		self._process = None
		self._url = None
		self._run_url = None
		pass	
		
	def is_running(self):
		if self._process is None:
			return False
		self._process.poll()
		if self._process.returncode is None:
			return True
		return False
		
	def set_url(self, url):
		''' url - URL of the mp3 file or station. '''
		self._url = url
		
	def get_url(self):
		return self._url
		
	def stop(self):
		if self.is_running():
			self._process.terminate()
			self._run_url = None
			logging.info("stop playing")

	def play(self, cache=320):
		"""
		cache - The cache size ink kbits.
		"""
		
		# prevent 2 processes
		if self.is_running():
			# check whether the same url ran
			if (self._run_url == self._url):
				return # issued to run the same thing again.
			self.stop()
		
		# -vo means the output driver
		execargs =['mplayer', '-softvol', '--slave', '--really-quiet', '-vo','null']
		
		if cache < 32: #mplayer requires cache>=32
			cache = 32
		execargs += ['-cache', str(cache)]

		# station URL
		execargs.append(self._url)
		
		self._process = subprocess.Popen(args=execargs)
		self._run_url = self._url
		logging.info("playing: " + self._url)
	
	def get_volume(self):
		# the name of the soundcard is self.SOUNDCARD_NAME
		# in this example it's Master
		#awk -F"[][]" '/dB/ { print $2 }' <(amixer sget Master)
		cmd = ["amixer", "sget", self.SOUNDCARD_NAME]
		out = subprocess.check_output(cmd)
		lines = out.split('\n')
		words = lines[4].split()
		percentage_str = words[3].translate(None, '[%]')
		return int(percentage_str)
		
	def _set_volume(self, value):
		cmd = ["amixer", "-q", "sset", self.SOUNDCARD_NAME, str(value) + "%"]
		subprocess.call(cmd)
		
	def set_volume(self, value):
		self._set_volume(value)
	
	def volume_up(self, by=5):
		current = self.get_volume()
		self._set_volume(current + by)
		
	def volume_down(self, by=5):
		current = self.get_volume()
		self._set_volume(current - by)
		