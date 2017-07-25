#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_setter import AbstractSetter

class BrightnessSetter(AbstractSetter):
	"""
	Sets brightness according to the display used.
	"""
	
	def next(self):
		self._add_brightness(1)
		super(BrightnessSetter, self).next()
		
	def prev(self):
		self._add_brightness(-1)
		super(BrightnessSetter, self).prev()
		
	def _show_text(self):
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
