#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_setter import AbstractSetter

class SoundSetter(AbstractSetter):
	"""
	Used to set volume.
	"""
	
	def __init__(self, display, sounds, player):
		super(SoundSetter, self).__init__(display)
		self._player = player
		self._sounds = sounds
		
		# indices
		self._current_idx = -1
		self._sound_key_list = []
		
		# create a list for keys
		for key, value in self._sounds.get_sounds().iteritems():
			self._sound_key_list.append(key)
			# getting the current index
			if (self._player.get_url() == value):
				self._current_idx = len(self._sound_key_list)-1

	def next(self):
		self._set_sound(1)
		super(SoundSetter, self).next()
		
	def prev(self):
		self._set_sound(-1)
		super(SoundSetter, self).prev()
		
	def _set_sound(self, add):
		indx = self._current_idx + add
		max_indx = len(self._sounds.get_sounds())-1
		if (indx > max_indx):
			indx = max_indx
		if (indx < 0):
			indx = 0
		self._current_idx = indx
		
		#set sound
		key = self._sound_key_list[self._current_idx]
		url = self._sounds.get_sounds()[key]
		self._player.set_url(url)
				
	def _show_text(self):
		return self._sound_key_list[self._current_idx]
