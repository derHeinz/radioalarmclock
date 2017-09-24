#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import logging

PIN_INP = 12

class IRDistanceInput(object):
	
	def __init__(self, controller):
		super(IRDistanceInput, self).__init__()
		self._function = controller.nearby
		
		# GPIO setup
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIN_INP, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.add_event_detect(PIN_INP, GPIO.FALLING, callback=self._occured, bouncetime=50)
		
	def _occured(self, null):
		logging.info("nearby sensor triggered")
		if (self._function != None):
			self._function()
