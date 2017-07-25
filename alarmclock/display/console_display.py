#!/usr/bin/python
# -*- coding: utf-8 -*-

from display import Display

class ConsoleDisplay(Display):
	
	def _output(self):
		print(self._current_displaying)
		
	def signal_first_on(self):
		print("signal 1 on")
	
	def signal_first_off(self):
		print("signal 1 off")
	
	def signal_second_on(self):
		print("signal 2 on")
	
	def signal_second_off(self):
		print("signal 2 off")
	