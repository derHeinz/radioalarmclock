#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import winsound

class Player(object):
	''' A player stub for windows testing.'''

	def __init__(self):
		self._url = None
		self._volume = 0
		pass	
		
	def is_running(self):
		return False
		
	def set_url(self, url):
		self._url = url
		
	def get_url(self):
		return self._url
		
	def stop(self):
		winsound.PlaySound(None, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

	def play(self):
		winsound.PlaySound(self._url, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
		
	def get_volume(self):
		return self._volume
		
	def _set_volume(self, value):
		self._volume = value
		if (self._volume > 100):
			self._volume = 100
		elif (self._volume < 0):
			self._volume = 0
	
	def volume_up(self, by=5):
		current = self.get_volume()
		self._set_volume(current + by)
		
	def volume_down(self, by=5):
		current = self.get_volume()
		self._set_volume(current - by)
