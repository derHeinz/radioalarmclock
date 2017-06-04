#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import readchar
import threading

class KeyboardInput(threading.Thread):
	
	def __init__(self, controller):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self._controller = controller

	# TODO very keyboard specific
	def _process_key(self, key):
		if (key == 'w'):
			self._controller.up()
		if (key == 'a'):
			self._controller.prev()
		if (key == 's'):
			self._controller.down()
		if (key == 'd'):
			self._controller.next()
		if (key == 'q'):
			self._controller.select()
			
	def run(self):
		while True:
			# TODO very keyboard specific
			key = readchar.readchar()
			self._process_key(key)
			time.sleep(0.2)
