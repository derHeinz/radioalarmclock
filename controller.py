#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import time
import sys

# own import
from menu import Menu, MenuItem, FunctionItem, GroupItem, BackItem, SubItem
from alarm import Alarm
from setter import *

class Controller(object):

	def _display_alarm_time(self):
		self._display.show_text(str(self._alarm.get_alarm_time()))
		
	def _timeout_occured(self):
		logging.info("timeout occured - switching to display time")
		self._to_initial_menuitems()
		self._display.show_time()
		
	def _exit(self):
		logging.info("exiting")
		
		# tear stuff down
		self._display.black()
		self._player.stop()
		# wait until teardown succeeded
		time.sleep(2)
		
		sys.exit()

	def __init__(self, display, alarm, sounds, player, timeout):
		self._display = display
		self._alarm = alarm
		self._player = player
		self._timeout = timeout
		self._timeout.set_timeout_function(self._timeout_occured)
		
		# initial menu enty
		self._initial_menuitems = [
			FunctionItem("Time", self._display.show_time, True),
			FunctionItem("Exit", self._exit, True),
			GroupItem("Alm.", [ # Alarm
				FunctionItem("Show", self._display_alarm_time, True),
				SubItem("Set", time_setter.TimeSetter(display, alarm)),
				FunctionItem("Off", self._alarm.remove_alarm, False),
				BackItem()]),
			GroupItem("Snd.", [ # Sounds
				SubItem("Prim", sound_setter.SoundSetter(display, sounds, player)),
				BackItem()]),
			GroupItem("Aud.", [ # Audio
				FunctionItem("Play", player.play, False),
				FunctionItem("Stop", player.stop, False),
				SubItem("Vol.", volume_setter.VolumeSetter(display, player)), # Volume
				BackItem()]),
			SubItem("Tmot.", timeout_setter.TimeoutSetter(display, timeout)),
			SubItem("Brht.", brightness_setter.BrightnessSetter(display)) # Brightness
		]
		
		# controlled object
		self._to_initial_menuitems()
		# make interaction and activate to have a sync point since here
		self._timeout.interaction()
		self._timeout.activate()
		
	def _to_initial_menuitems(self):
		self._controlled_stack = []
		self._controlled_stack.append(Menu(self._display, self._initial_menuitems))
	
	def next(self):
		self._timeout.interaction()
		self._timeout.activate()
		self._controlled_stack[-1].next()
	
	def prev(self):
		self._timeout.interaction()
		self._timeout.activate()
		self._controlled_stack[-1].prev()
		
	def select(self):
		self._timeout.interaction()
		self._timeout.activate()
		res = self._controlled_stack[-1].select()
		if res is not None:
			if (res == "back"):
				# throw away last item
				self._controlled_stack.pop()
			else:
				# stack next item
				self._controlled_stack.append(res)
			self._controlled_stack[-1].display()
			