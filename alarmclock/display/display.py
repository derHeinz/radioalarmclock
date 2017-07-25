#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
import logging

class Display(threading.Thread):

	MODES = ["text", "time", "blank"]

	def __init__(self, dimmer):
		super(Display, self).__init__()
		self.setDaemon(True)
		self._dimmer = dimmer
		self._changed = False
		self._current_displaying = None
		self._current_mode = None
		self._signal1 = False # shows a signal like a flag
		self._signal2 = False
		
	def _draw(self):
		if (self._changed):
			self._output()
			self._changed = False
			
	def _output(self):
		# abstract overwrite point
		pass
		
	def _update_internal_state(self):
		# tick the time
		if self._current_mode == self.MODES[1]:
			current_time = time.strftime("%H:%M")
			if self._current_displaying != current_time:
				self._current_displaying = current_time
				self._changed = True

	def show_text(self, text):
		''' Displays the given text. '''
		if (self._current_mode != self.MODES[0] or self._current_displaying != text):
			self._changed = True
			self._current_mode = self.MODES[0]
			self._current_displaying = text
			
	def show_text_blinking(self, text):
		''' Blink between text and black screen. '''
		count = 10
		while count > 0:
			if (count % 2 == 0):
				self.show_text(text)
			else:
				self.black()
			count -= 1
			time.sleep(0.2)
		
	def black(self):
		''' Black out the screen e.g. show nothing '''
		self._current_mode = self.MODES[2]
		self._changed = True
		
		
	def show_time(self):
		if (self._current_mode is not self.MODES[1]):
			self._current_mode = self.MODES[1]
			self._changed = True
			
	def set_brightness(self, bright):
		pass
	
	def get_brightness(self):
		return self.get_max_brightness()
	
	def get_max_brightness(self):
		# default
		return 0
		
	def signal_first_on(self):
		self._signal1 = True
	
	def signal_first_off(self):
		self._signal1 = False
	
	def signal_second_on(self):
		self._signal2 = True
	
	def signal_second_off(self):
		self._signal2 = False
		
	def run(self):
		while True:
			self._update_internal_state()
			self._draw()
			time.sleep(0.2)
			#self._brightness = self._dimmer.brightness # TODO maybe this is also update interl state
			
