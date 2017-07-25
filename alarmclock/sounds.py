#!/usr/bin/python
# -*- coding: utf-8 -*-

class Sounds(object):
	
	def __init__(self):
		self._sounds = {}
		self._default = None
		
	def get_sounds(self):
		return self._sounds
		
	def set_sounds(self, value):
		self._sounds = value
		
	def get_default(self):
		return self._default
		
	def set_default(self, value):
		self._default = value
		
	def get_default_url(self):
		return self._sounds[self._default]
