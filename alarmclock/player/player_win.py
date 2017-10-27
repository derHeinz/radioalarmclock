#!/usr/bin/python
# -*- coding: utf-8 -*-

import winsound
from player import Player
import logging

class PlayerWin(Player):
	''' A player stub for windows testing.'''

	def __init__(self, scheduler):
		super(PlayerWin, self).__init__(scheduler)
		self._volume = 0
		
	def is_running(self):
		return False
		
	def _stop(self):
		winsound.PlaySound(None, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

	def _play(self):
		logging.debug("attempting to play " + self._url)
		winsound.PlaySound(self._url, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
			
	def get_volume(self):
		return self._volume
		
	def set_volume(self, value):
		logging.info("setting volume to " + str(value))
		self._volume = value
		if (self._volume > 100):
			self._volume = 100
		elif (self._volume < 0):
			self._volume = 0
	
	def volume_up(self, by=5):
		current = self.get_volume()
		self.set_volume(current + by)
		
	def volume_down(self, by=5):
		current = self.get_volume()
		self.set_volume(current - by)
