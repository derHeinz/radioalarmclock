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

	#
	# First some functions called by menu items
	#

	def _display_alarm_time_1(self):
		self._display.show_text(str(self._alarm.get_alarmtime_1()))
		
	def _display_alarm_time_2(self):
		self._display.show_text(str(self._alarm.get_alarmtime_2()))
		
	def _display_ip_part(self):
		ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
		last_ip_segment = ip.split(".")[3]
		logging.debug("logging last ip segment " + last_ip_segment)
		self._display.show_text("I" + last_ip_segment)
		
	def _timeout_occured(self):
		logging.debug("timeout occured - switching to display time")
		self._to_initial_menuitems()
		self._display.show_time()
		
	def _show_time(self):
		self._display.show_time()
		
	def _weather_condition(self):
		if (self._weather.get_rain_today):
			return "nice_weather"
		else:
			return "rain"
		
	def _exit(self):
		logging.info("exiting")
		
		# tear stuff down
		self._display.black()
		self._player.stop()
		self._scheduler.shutdown()
						
		# wait until teardown succeeded
		time.sleep(2)
		sys.exit()
		
	#
	# End some functions called by menu items
	#

	#
	# Alarm related
	#
	
	def _alarm_function(self):
		logging.debug("alarm occured")
		if (not self._in_alarm):
			self._in_alarm = True
			# in here comes the stuff that should happen for alarm
			self._player.play()
			self._display.show_special(self._weather_condition())
			# end of stuff to happen for alarm
			self._interact_timeout() # start the interaction timeout in case one is in the menu at alarm
		
	def _anti_alarm_function(self):
		if (self._in_alarm):
			self._in_alarm = False
			# in here comes the stuff that should be kind of reset after alarm has been approved
			self._show_time()
			self._player.stop()
			
	#
	# End of Alarm related
	#

	def __init__(self, display, alarm, sounds, player, timeout, scheduler, weather):
		self._display = display
		self._alarm = alarm
		# defaulting both alarms to play
		self._alarm.set_alarm_function_1(self._alarm_function)
		self._alarm.set_alarm_function_2(self._alarm_function)
		self._player = player
		self._scheduler = scheduler
		self._weather = weather
		self._timeout = timeout
		self._timeout.set_timeout_function(self._timeout_occured)
		self._lock = threading.Lock()
		self._in_alarm = False # whether we are currently within an alarm
		
		# initial menu enty
		self._initial_menuitems = [
			FunctionItem("Time", True, self._show_time),
			FunctionItem("Exit", True, self._exit),
			GroupItem("Al1.", [ # Alarm 1
				FunctionItem("Show", True, self._display_alarm_time_1),
				SubItem("Set", time_setter_1.TimeSetter1(display, alarm)),
				FunctionItem("Off", False, self._alarm.set_alarm_1, False),
				BackItem()]),
			GroupItem("Al2.", [ # Alarm 2
				FunctionItem("Show", True, self._display_alarm_time_2),
				SubItem("Set", time_setter_2.TimeSetter2(display, alarm)),
				FunctionItem("Off", False, self._alarm.set_alarm_2, False),
				BackItem()]),
			GroupItem("Snd.", [ # Sounds
				SubItem("Prim", prim_sound_setter.PrimSoundSetter(display, sounds, player)),
				SubItem("Baku", backup_sound_setter.BackupSoundSetter(display, sounds, player)),
				BackItem()]),
			GroupItem("Aud.", [ # Audio
				FunctionItem("Play", False, self._player.play),
				FunctionItem("Stop", False, self._player.stop),
				SubItem("Vol.", volume_setter.VolumeSetter(display, player)), # Volume
				BackItem()]),
			GroupItem("Oth.", [ # Other
				FunctionItem("IP", True, self._display_ip_part),
				FunctionItem("Sun", True, self._display.show_special, "nice_weather"),
				FunctionItem("Cld", True, self._display.show_special, "rain"),
				FunctionItem("Chk", True, self._display.show_special, "check"),
				FunctionItem("O:W", True, self._display.show_text, str(len(self._weather_condition()))),
				BackItem()]),
			SubItem("Tmot.", timeout_setter.TimeoutSetter(display, timeout)),
			SubItem("Brht.", brightness_setter.BrightnessSetter(display)) # Brightness
		]
		
		# controlled object
		self._to_initial_menuitems()
		# make interaction and activate to have a sync point since here
		self._interact_timeout()
		
	def _interact_timeout(self):
		logging.debug("interact during timeout")
		self._timeout.interaction()
		self._timeout.activate()
		
	def _to_initial_menuitems(self):
		self._controlled_stack = []
		self._controlled_stack.append(Menu(self._display, self._initial_menuitems))
		
	def nearby(self):
		logging.debug("something is nearby")
		self._anti_alarm_function()
	
	def next(self):
		logging.debug("next triggered")
		with self._lock:
			self._anti_alarm_function()
			self._interact_timeout()
			self._controlled_stack[-1].next()
	
	def prev(self):
		logging.debug("previous triggered")
		with self._lock:
			self._anti_alarm_function()
			self._interact_timeout()
			self._controlled_stack[-1].prev()
		
	def select(self):
		logging.debug("select triggered")
		with self._lock:
			self._anti_alarm_function()
			self._interact_timeout()
			
			res = self._controlled_stack[-1].select()
			if res is not None:
				if (res == "back"):
					# throw away last item
					self._controlled_stack.pop()
				else:
					# stack next item
					self._controlled_stack.append(res)
				logging.debug("current element: "+ str(self._controlled_stack))
				self._controlled_stack[-1].display()
			