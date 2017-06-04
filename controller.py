#!/usr/bin/python
# -*- coding: utf-8 -*-

# sys imports
import threading
import readchar
import time

# own import
from menu import Menu, MenuItem, FunctionItem, GroupItem, BackItem, SubItem
from alarm import Alarm

from setter.time_setter import TimeSetter
from setter.volume_setter import VolumeSetter
from setter.brightness_setter import BrightnessSetter


class Controller(threading.Thread):

	def _display_alarm_time(self):
		self._display.show_text(str(self._alarm.get_alarm_time()))

	def __init__(self, display, alarm, player):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self._display = display
		self._alarm = alarm
		self._player = player
		
		# initial menu enty
		initial_menuitems = [
			GroupItem("Alrm.", [
				FunctionItem("Show", self._display_alarm_time),
				SubItem("Set.", TimeSetter(display, alarm)), 
				BackItem("<-.")]),
			GroupItem("Aud.", [
				FunctionItem("Play", player.play),
				FunctionItem("Stop", player.stop),
				SubItem("Vol.", VolumeSetter(display, player)), 
				BackItem("<-.")]),
			SubItem("Brht", BrightnessSetter(display)),
			FunctionItem("Time", self._display.show_time)
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
			
	# TODO very keyboard specific
	def _process_key(self, key):
		if (key == 'w'):
			self.up()
		if (key == 'a'):
			self.prev()
		if (key == 's'):
			self.down()
		if (key == 'd'):
			self.next()
		if (key == 'q'):
			self.select()
			
	def run(self):
		while True:
			# TODO very keyboard specific
			key = readchar.readchar()
			self._process_key(key)
			time.sleep(0.2)
