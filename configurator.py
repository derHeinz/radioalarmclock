#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class Configurator(object):
	'''
	Used to configure the program.
	'''
	
	def __init__(self):
		with open('config.json') as data_file:    
			self.data = json.load(data_file)
			
	def _get(self, subtreename):
		return self.data[subtreename]
		
	
	def get_sounds(self):
		return self._get("sounds")	
		
	def config_player(self, player):
		conf = self._get("player")
		player.set_volume(conf["volume"])
		player.set_url(self.get_sounds()[conf["default"]])
	
	def config_display(self, display):
		conf = self._get("display")
		display.set_brightness(conf["brightness"])
		
	def config_alarm(self, alarm):
		conf = self._get("alarm")
		alarm.set_alarm_time(conf["time"])
		
	def config_dimmer(self, dimmer):
		conf = self._get("location")
		dimmer.set_location(conf["lat"], conf["lon"])
		