#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from display import Display

class ConsoleDisplay(Display):

	def __init__(self, dimmer):
		Display.__init__(self, dimmer)
		self._brightness = 7
	
	def _output(self):
		
		signal = ""
		if self._signal1 and self._signal2:
			signal = "="
		elif self._signal1:
			signal = "-"
		elif self._signal2:
			signal = "_"
		else:
			signal = " "
		
		rest = "(" + str(self._brightness) + ") "
		
		if self._current_mode == self.MODES[2]: # blank 
			rest += ""
		elif self._current_mode == self.MODES[1]: # time
			rest += "Time: " + self._current_displaying
		elif self._current_mode == self.MODES[0]: # text
			rest += "Text: " + self._current_displaying
		print(signal + " " + rest)
			
	def signal_first_on(self):
		super(ConsoleDisplay, self).signal_first_on()
		logging.debug("signal 1 on")
	
	def signal_first_off(self):
		super(ConsoleDisplay, self).signal_first_off()
		logging.debug("signal 1 off")
	
	def signal_second_on(self):
		super(ConsoleDisplay, self).signal_second_on()
		logging.debug("signal 2 on")
	
	def signal_second_off(self):
		super(ConsoleDisplay, self).signal_second_off()
		logging.debug("signal 2 off")
	
	def set_brightness(self, bright):
		self._brightness = bright
		
	def get_brightness(self):
		return self._brightness 
	
	def get_max_brightness(self):
		return 15
	