#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO

import time
import readchar

# PIN definitions
PIN_CLK = 17
PIN_DT = 27
BUTTON_PIN = 22
 

class RotaryKnobInput():
	
	def __init__(self, controller):
		self._controller = controller

		# GPIO setup
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(PIN_CLK, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(PIN_DT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		
		# variable declartion
		self.PIN_CLK_LETZTER = 0
		self.PIN_CLK_AKTUELL = 0
		# Initiales Auslesen des Pin_CLK
		self.PIN_CLK_LETZTER = GPIO.input(PIN_CLK)
		
		# Um einen Debounce direkt zu integrieren, werden die Funktionen zur Ausgabe mittels
		# CallBack-Option vom GPIO Python Modul initialisiert
		GPIO.add_event_detect(PIN_CLK, GPIO.BOTH, callback=self.turned, bouncetime=150)
		GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=self.switched, bouncetime=150)
		
	def switched(self, null):
		self._controller.select()
		
	def turned(self, null):
		self.PIN_CLK_AKTUELL = GPIO.input(PIN_CLK)
 
		if self.PIN_CLK_AKTUELL != self.PIN_CLK_LETZTER:
 
			if GPIO.input(PIN_DT) != self.PIN_CLK_AKTUELL:
				self._controller.next()
			else:
				self._controller.prev()
