#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from dimmer import Dimmer


class TestDimmer(unittest.TestCase):
	
	def test_calc_brightness_simple(self):
		dim = Dimmer(None, None)
		
		max = 100
		dim._day_percentage = 10
		dim._night_percentage = 20
		
		# this mocks before sunrise and before sunset
		br = dim._calculate_brightness(max, 0, 1, 2)
		self.assertEquals(20, br)
		
		# this mocks after sunrise and before sunset
		br = dim._calculate_brightness(max, 1, 0, 2)
		self.assertEquals(10, br)
		
		# this mocks after sunrise and after sunset
		br = dim._calculate_brightness(max, 2, 0, 1)
		self.assertEquals(20, br)
		
	def test_calc_brightness_special(self):
		dim = Dimmer(None, None)
		
		max = 15
		dim._day_percentage = 25
		dim._night_percentage = 5
		
		# this mocks after sunrise and before sunset
		br = dim._calculate_brightness(max, 1, 0, 2)
		self.assertEquals(3, br)
		
		# this mocks after sunrise and after sunset
		br = dim._calculate_brightness(max, 2, 0, 1)
		self.assertEquals(0, br)
		
if __name__ == '__main__':
	unittest.main()