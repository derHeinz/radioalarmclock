#!/usr/bin/python
# -*- coding: utf-8 -*-

class AbstractSetter(object):
	"""
	Sets the timeout when menu is closed and system goes back to show time.
	"""
	
	def __init__(self, display):
		self._display = display
		
	def display(self):
		self._display.show_text(self._show_text())
		
	def next(self):
		# need to do what next does
		self.display()
		
	def prev(self):
		# need to do what prev does
		self.display()
		
	def select(self):
		self._display.show_text_blinking(self._show_text())
		return "back"
		
	def _show_text(self):
		# return the text of the current value state
		pass
		