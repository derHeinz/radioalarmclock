#!/usr/bin/python
# -*- coding: utf-8 -*-

from display import Display

class ConsoleDisplay(Display):
	
	def _output(self):
		print(self._current_displaying)