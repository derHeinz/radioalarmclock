#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_setter import AbstractSetter

class TimeoutSetter(AbstractSetter):
	"""
	Sets the timeout when menu is closed and system goes back to show time.
	"""
	
	def __init__(self, display, timeout):
		super(TimeoutSetter, self).__init__(display)
		self._timeout = timeout
		
	def next(self):
		current_timeout = self._timeout.get_timeout()
		current_timeout += 1
		self._timeout.set_timeout(current_timeout)
		super(TimeoutSetter, self).next()
		
	def prev(self):
		current_timeout = self._timeout.get_timeout()
		current_timeout -= 1
		self._timeout.set_timeout(current_timeout)
		super(TimeoutSetter, self).prev()
		
	def _show_text(self):
		return str(self._timeout.get_timeout())
