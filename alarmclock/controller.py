#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
import sys
import threading
import socket
from common import stoppable

# own import
from menu import Menu, MenuItem, FunctionItem, GroupItem, BackItem, SubItem
from alarm import Alarm
from setter import *

class Controller(object):

	def _display_alarm_time(self):
		self._display.show_text(str(self._alarm.get_alarmtime()))
		
	def _display_ip_part(self):
		ip = socket.gethostbyname(socket.gethostname())
		self._display.show_text("IP " + ip.split(".")[3])
		
	def _connect_internet(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		s.close()
		
	def _timeout_occured(self):
		logging.info("timeout occured - switching to display time")
		self._set_mode(0)
		self._to_initial_menuitems()
		self._display.show_time()
		
	def _show_time(self):
		self._set_mode(0)
		self._display.show_time()
	
	def _set_mode(self, mode):
		'''
		Valid modes are:
		0 = show time
		1 = show text or other stuff
		'''
		self._mode = mode		
		
	def _exit(self):
		logging.info("exiting")
		
		# tear stuff down
		self._display.black()
		self._player.stop()
		self._scheduler.shutdown()
						
		# wait until teardown succeeded
		time.sleep(2)
		sys.exit()

	def __init__(self, display, alarm, sounds, player, timeout, scheduler):
		self._display = display
		self._alarm = alarm
		self._player = player
		self._scheduler = scheduler
		self._timeout = timeout
		self._timeout.set_timeout_function(self._timeout_occured)
		self._lock = threading.Lock()
		self._set_mode(1)
		
		# initial menu enty
		self._initial_menuitems = [
			FunctionItem("Time", True, self._show_time),
			FunctionItem("Exit", True, self._exit),
			GroupItem("Alm.", [ # Alarm
				FunctionItem("Show", True, self._display_alarm_time),
				SubItem("Set", time_setter.TimeSetter(display, alarm)),
				FunctionItem("Off", False, self._alarm.set_alarm, False)
				BackItem()]),
			GroupItem("Snd.", [ # Sounds
				SubItem("Prim", sound_setter.SoundSetter(display, sounds, player)),
				BackItem()]),
			GroupItem("Aud.", [ # Audio
				FunctionItem("Play", False, self._player.play),
				FunctionItem("Stop", False, self._player.stop),
				SubItem("Vol.", volume_setter.VolumeSetter(display, player)), # Volume
				BackItem()]),
			GroupItem("Oth.", [ # Other
				FunctionItem("IP", True, self._display_ip_part),
				FunctionItem("Inet", False, self._connect_internet),
				BackItem()]),
			SubItem("Tmot.", timeout_setter.TimeoutSetter(display, timeout)),
			SubItem("Brht.", brightness_setter.BrightnessSetter(display)) # Brightness
		]
		
		# controlled object
		self._to_initial_menuitems()
		# make interaction and activate to have a sync point since here
		self._interact_timeout()
		
	def _interact_timeout(self):
		self._timeout.interaction()
		self._timeout.activate()
		
	def _to_initial_menuitems(self):
		self._controlled_stack = []
		self._controlled_stack.append(Menu(self._display, self._initial_menuitems))
	
	def next(self):
		with self._lock:
			self._set_mode(1)
			self._interact_timeout()
			self._controlled_stack[-1].next()
	
	def prev(self):
		with self._lock:
			self._set_mode(1)
			self._interact_timeout()
			self._controlled_stack[-1].prev()
		
	def select(self):
		with self._lock:
			current_mode = self._mode
			self._set_mode(1)
			self._interact_timeout()
			if (current_mode == 0):
				# just deactivate sound
				self._player.stop()
			res = self._controlled_stack[-1].select()
			if res is not None:
				if (res == "back"):
					# throw away last item
					self._controlled_stack.pop()
				else:
					# stack next item
					self._controlled_stack.append(res)
				print(self._controlled_stack)
				self._controlled_stack[-1].display()
			