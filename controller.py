#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import logging
import time

# own import
from menu import Menu, MenuItem, FunctionItem, GroupItem, BackItem, SubItem
from alarm import Alarm

from setter.time_setter import TimeSetter
from setter.volume_setter import VolumeSetter
from setter.brightness_setter import BrightnessSetter
from setter.sound_setter import SoundSetter


class Controller(object):

	def _display_alarm_time(self):
		self._display.show_text(str(self._alarm.get_alarm_time()))
		
	def _exit(self):
		logging.info("exiting")
		
		# tear stuff down
		self._display.show_text("")
		self._player.stop()
		# wait until teardown succeeded
		time.sleep(2)
		
		sys.exit()

	def __init__(self, display, alarm, sounds, player):
	
		self._display = display
		self._alarm = alarm
		self._player = player
		
		# initial menu enty
		initial_menuitems = [
			FunctionItem("Time", self._display.show_time, True),
			FunctionItem("Exit", self._exit, True),
			GroupItem("Alm.", [ # Alarm
				FunctionItem("Show", self._display_alarm_time, True),
				SubItem("Set", TimeSetter(display, alarm)), 
				BackItem()]),
			GroupItem("Snd.", [ # Sounds
				SubItem("Prim", SoundSetter(display, sounds, player)),
				BackItem()]),
			GroupItem("Aud.", [ # Audio
				FunctionItem("Play", player.play, False),
				FunctionItem("Stop", player.stop, False),
				SubItem("Vol.", VolumeSetter(display, player)), # Volume
				BackItem()]),
			SubItem("Brht.", BrightnessSetter(display)) # Brightness
		]
		
		# controlled object
		self._controlled_stack = []
		self._controlled_stack.append(Menu(display, initial_menuitems))
		
	
	def next(self):
		self._controlled_stack[-1].next()
	
	def prev(self):
		self._controlled_stack[-1].prev()
		
	def select(self):
		res = self._controlled_stack[-1].select()
		if res is not None:
			if (res == "back"):
				# throw away last item
				self._controlled_stack.pop()
			else:
				# stack next item
				self._controlled_stack.append(res)
			self._controlled_stack[-1].display()
			