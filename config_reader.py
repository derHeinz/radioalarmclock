#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class ConfigReader(object):
	'''
	Put a list of sounds or soundstations into file sounds.json. Default directory is /sounds
	'''
	
	def __init__(self):
		with open('config.json') as data_file:    
			self.data = json.load(data_file)
			
	def _get(self, subtreename):
		return self.data[subtreename]
		
	def get_player(self):
		return self._get("sounds")
		
	def get_sounds(self):
		return self._get("sounds")
		
	def get_display(self):
		return self._get("display")
		
	def get_location(self):
		return self._get("location")
		
	def get_alarm(self):
		return self._get("alarm")