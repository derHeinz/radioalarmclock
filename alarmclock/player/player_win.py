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
		winsound.PlaySound(None, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC | winsound.SND_NODEFAULT)

	def _play_url(self, url):
		logging.debug("attempting to play " + url)
		res = winsound.PlaySound(url, winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
		logging.debug("result " + str(res)) 
			
	def get_volume(self):
		return self._volume
		
	def set_volume(self, value):
		logging.info("setting volume to " + str(value))
		self._volume = value
		if (self._volume > 100):
			self._volume = 100
		elif (self._volume < 0):
			self._volume = 0
	