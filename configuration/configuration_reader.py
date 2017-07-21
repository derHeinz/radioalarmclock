#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class ConfigurationReader(object):
	'''
	Read configuration from config file.
	'''
	
	def __init__(self, configurator, data):
		self._config = configurator
		self._data = data
			
	def config_components(self):		
		# set component's properties to configs
		for comp in self._data.iterkeys():
			print(comp)
			for prop in self._data[comp].iterkeys():
				self._config.set(comp, prop, self._data[comp][prop])
				
		