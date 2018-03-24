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
			
	def _stop(self):
		logging.debug("stopping player")

	def _play(self):
		# do not really play anything - this is a test
		logging.debug("playing player")
		

class PlayerTestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		# setting up logging
		#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		#handler = StreamHandler()
		#handler.setFormatter(formatter)
		#root_logger = logging.getLogger()
		#root_logger.setLevel(logging.DEBUG)
		#root_logger.addHandler(handler)

		# setting up the scheduler
		cls._scheduler = BackgroundScheduler()
		cls._scheduler.start()
		
	def tearDown(self):
		PlayerTestCase._scheduler.remove_all_jobs()
		
	def create_new_player(self):
		p = PlayerTest(PlayerTestCase._scheduler)
		p.set_url("bell.wav")
		return p
		
	def test_simple_fadein(self):
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
		p.set_fadein_steps(3)
		p.set_fadein_interval(10)

		# start
		p.play()
		
		# wait time but not until finished but abort before
		time.sleep(22)
		
		# test player's values
		size3_or_4 = (len(p.get_stored_volumes()) == 3) or (len(p.get_stored_volumes()) == 4)
		self.assertTrue(size3_or_4)
		
		self.assertEquals(p.get_stored_volumes()[0], 50)
		self.assertEquals(p.get_stored_volumes()[1], 35)
		self.assertEquals(p.get_stored_volumes()[2], 40)
		
		#self.assertEquals(p.get_stored_volumes()[0], 50, 35, 40, 45])
		
	def test_fadein_volume_back(self):
		p = self.create_new_player()

		# configure
		original_volume = 67
		p.set_volume(original_volume)
		p.set_fadein(True)
		p.set_fadein_step_size(2)
		p.set_fadein_steps(28)
		p.set_fadein_interval(1)

		# start
		p.play()
		# wait such that in the middle of nowhere
		time.sleep(10)
		# stop playing
		p.stop()
		
		# check it resetted to orignal volume
		self.assertEquals(original_volume, p.get_volume())
		

if __name__ == '__main__':
    unittest.main()