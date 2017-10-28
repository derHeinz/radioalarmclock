#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_sound_setter import AbstractSoundSetter

class PrimSoundSetter(AbstractSoundSetter):
	"""
	Used to set main sound.
	"""
	
	def __init__(self, display, sounds, player):
		super(PrimSoundSetter, self).__init__(display, sounds, player)
	
	def _get_url(self):
		return self._player.get_url()
		
	def _set_url(self, url):
		self._player.set_url(url)
