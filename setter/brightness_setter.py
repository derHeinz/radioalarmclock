#!/usr/bin/python
# -*- coding: utf-8 -*-

class BrightnessSetter(object):
	"""
	Sets brightness according to the display used.
	"""
	
	def __init__(self, display):
		self._display = display
		
	def display(self):
		self._display.show_text(self._brightness_text())
		
	def next(self):
		self._add_brightness(1)
		self.display()
		
	def prev(self):
		self._add_brightness(-1)
		self.display()
		
	def select(self):
		self._display.show_text_blinking(self._brightness_text())
		return "back"
		
	def _brightness_text(self):
		return str(self._display.get_brightness())
	
	def _add_brightness(self, plus):
		bright = self._display.get_brightness()
		bright += plus
		max_bright = self._display.get_max_brightness()
		
		if (bright > max_bright):
			bright = max_bright
		if (bright < 0):
			bright = 0
		self._display.set_brightness(bright)
