#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
import logging

class Display(threading.Thread):

	MODES = ["text", "time", "blank", "special"]

	def __init__(self):
		super(Display, self).__init__()
		self.setDaemon(True)
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
			if (current_time.startswith("0")):
				current_time = current_time.replace("0", " ", 1)
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
			
	def show_special(self, special):
		''' Displays the given text. '''
		if (self._current_mode != self.MODES[3] or self._current_displaying != special):
			self._changed = True
			self._current_mode = self.MODES[3]
			self._current_displaying = special
			
	def set_brightness(self, bright):
		pass
	
	def get_brightness(self):
		return self.get_max_brightness()
	
	def get_max_brightness(self):
		# default
		return 0
		
	def set_alarm_1(self, value):
		self._set_alarm(value, "_signal1")
		
	def set_alarm_2(self, value):
		self._set_alarm(value, "_signal2")
		
	def _set_alarm(self, value, signal_str):
		if not type(value) == bool:
			logging.error("Error calling set alarm.")
			return
		signal = getattr(self, signal_str)
		if (value == signal):
			# no change
			logging.debug("No alarm value change for the display.")
			return
		logging.debug("Setting signal " + signal_str + " to " + str(value))
		setattr(self, signal_str, value)
		#signal = value
		self._changed = True
		self._draw()
		
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
			
