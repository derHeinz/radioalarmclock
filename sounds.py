#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

class Sounds(object):
	'''
	Put a list of sounds or soundstations into file sounds.json. Default directory is /sounds
	'''
	
	def __init__(self):
		with open('sounds.json') as data_file:    
			self.data = json.load(data_file)
		
	def get_sounds(self):
		return self.data
