#!/usr/bin/python
# -*- coding: utf-8 -*-

class SoundSetter(object):
	"""
	Used to set volume.
	"""
	
	def __init__(self, disp, sounds, player):
		""" """
		self._player = player
		self._disp = disp
		self._sounds = sounds
		
		# indices
		self._current_idx = -1
		self._sound_key_list = []
		
		# create a list for keys
		for key, value in self._sounds.iteritems():
			self._sound_key_list.append(key)
			# getting the current index
			if (self._player.get_url() == value):
				self._current_idx = len(self._sound_key_list)-1

	def display(self):
		self._disp.show_text(self._sounds_text())
		
	def next(self):
		self.set_sound(1)
		self.display()
		
	def prev(self):
		self.set_sound(-1)
		self.display()
		
	def select(self):
		self._disp.show_text_blinking(self._sounds_text())
		return "back"
		
	def set_sound(self, add):
		indx = self._current_idx + add
		max_indx = len(self._sounds)-1
		if (indx > max_indx):
			indx = max_indx
		if (indx < 0):
			indx = 0
		self._current_idx = indx
		
		#set sound
		key = self._sound_key_list[self._current_idx]
		url = self._sounds[key]
		self._player.set_url(url)
				
	def _sounds_text(self):
		return self._sound_key_list[self._current_idx]
