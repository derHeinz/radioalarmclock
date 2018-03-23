#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import logging
from player import Player

class PlayerLinux(Player):
	"""
	The player for linux use.
	"""
	
	SOUNDCARD_NAME = "PCM"
	
	def __init__(self, scheduler):
		super(PlayerLinux, self).__init__(scheduler)
		self._process = None
		self._run_url = None
		
	def is_running(self):
		if self._process is None:
			return False
		self._process.poll()
		if self._process.returncode is None:
			return True
		return False
		
	def _stop(self):
		if self.is_running():
			self._process.terminate()
			self._run_url = None
			logging.debug("stop playing")
			
	def _play_url(self, url):
		"""
		cache - The cache size ink kbits.
		"""
		cache=320
		
		# prevent 2 processes
		if self.is_running():
			# check whether the same url ran
			if (self._run_url == url):
				return # issued to run the same thing again.
			self.stop()
		
		# -vo means the output driver
		execargs =['mplayer', '-softvol', '--slave', '--really-quiet', '-vo','null']
		
		if cache < 32: #mplayer requires cache>=32
			cache = 32
		execargs += ['-cache', str(cache)]

		# station URL
		execargs.append(url)
		
		self._process = subprocess.Popen(args=execargs)
		self._run_url = url
		logging.debug("playing: " + url)
	
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
		
	def set_volume(self, value):
		cmd = ["amixer", "-q", "sset", self.SOUNDCARD_NAME, str(value) + "%"]
		subprocess.call(cmd)
		