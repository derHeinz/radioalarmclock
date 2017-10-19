#!/usr/bin/python
# -*- coding: utf-8 -*-

from player import Player
from player_win import PlayerWin
import logging

class PlayerTest(Player):
	
	def __init__(self, scheduler):
		super(PlayerTest, self).__init__(scheduler)
		self._volume = 0
		
	def get_volume(self):
		return self._volume
		
	def set_volume(self, value):
		self._volume = value
		if (self._volume > 100):
			self._volume = 100
		elif (self._volume < 0):
			self._volume = 0
		logging.info("setting value to " + str(self._volume))
			
	def stop(self):
		logging.info("stopping player")

	def _play(self):
		logging.info("playing player")

		
#from apscheduler.triggers.cron import CronTrigger
#from logging.handlers import RotatingFileHandler
#from apscheduler.schedulers.blocking import BlockingScheduler
# setting up logging
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#handler = RotatingFileHandler('player_test.log', maxBytes=153600, backupCount=3)
#handler.setFormatter(formatter)

#root_logger = logging.getLogger()
#root_logger.setLevel(logging.DEBUG)
#root_logger.addHandler(handler)

#scheduler = BlockingScheduler()
#p = PlayerWin(scheduler)
#p.set_url("bell.wav")
#p.set_volume(95)
#p.play_fadein()
#p.play()
#scheduler.start() # blocking scheduler than this blocks!