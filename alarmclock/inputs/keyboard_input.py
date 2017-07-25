#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import readchar
import logging
import threading

class KeyboardInput(threading.Thread):
	
	def __init__(self, controller):
		super(KeyboardInput, self).__init__()
		self.setDaemon(True)
		self._controller = controller
		self.start()

	def _process_key(self, key):
		if (key == 'a'):
			self._controller.prev()
		if (key == 'd'):
			self._controller.next()
		if (key == 'q'):
			self._controller.select()
			
	def run(self):
		while True:
			key = readchar.readchar()
			self._process_key(key)
			time.sleep(0.2)
			