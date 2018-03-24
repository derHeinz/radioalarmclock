#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from player import Player
import logging
import time
from apscheduler.triggers.cron import CronTrigger
from logging import StreamHandler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

class PlayerTest(Player):
	
	def __init__(self, scheduler):
		super(PlayerTest, self).__init__(scheduler)
		self._volume = 0
		self._stored_volumes = []
		
	def get_stored_volumes(self):
		return self._stored_volumes
		
	def get_volume(self):
		return self._volume
		
	def set_volume(self, value):
		self._volume = value
		logging.debug("setting value to " + str(self._volume))
		self._stored_volumes.append(value)
			
	def stop(self):
		logging.debug("stopping player")

	def _play(self):
		logging.debug("playing player")
		

class PlayerTestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		# setting up logging

		# setting up the scheduler
		cls._scheduler = BackgroundScheduler()
		cls._scheduler.start()
		
	def tearDown(self):
		PlayerTestCase._scheduler.remove_all_jobs()
		
	def create_new_player(self):
		p = PlayerTest(PlayerTestCase._scheduler)
		p.set_url("bell.wav")
		return p
		
	def test_simple_schedule(self):
		p = self.create_new_player()

		# configure
		p.set_volume(100)
		p.set_fadein(True)
		p.set_fadein_step_size(10)
		p.set_fadein_steps(5)
		p.set_fadein_interval(1)

		# start
		p.play()
		
		# wait until finished
		time.sleep(10)
		
		# test player's values (initially set to 100, than the 5 steps with the size occure until it is set back to initial value
		self.assertEquals(p.get_stored_volumes(), [100, 50, 60, 70, 80, 90 ,100])

	def test_crazy_numbers(self):
		p = self.create_new_player()

		# configure
		p.set_volume(93)
		p.set_fadein(True)
		p.set_fadein_step_size(7)
		p.set_fadein_steps(11)
		p.set_fadein_interval(1)

		# start
		p.play()
		
		# wait until finished
		time.sleep(20)
		
		# test player's values
		self.assertEquals(p.get_stored_volumes(), [93, 16, 23, 30, 37, 44, 51, 58, 65, 72, 79, 86, 93])
		
	def test_scheduler_still_runs(self):
		p = self.create_new_player()

		# configure
		p.set_volume(50)
		p.set_fadein(True)
		p.set_fadein_step_size(5)
		p.set_fadein_steps(2)
		p.set_fadein_interval(10)

		# start
		p.play()
		
		# wait until finished
		time.sleep(22)
		
		# test player's values
		self.assertEquals(p.get_stored_volumes(), [50, 40, 45])
		
		

if __name__ == '__main__':
    unittest.main()