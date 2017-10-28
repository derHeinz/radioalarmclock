#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_sound_setter import AbstractSoundSetter

class BackupSoundSetter(AbstractSoundSetter):
	"""
	Used to set main sound.
	"""
	
	def __init__(self, display, sounds, player):
		super(BackupSoundSetter, self).__init__(display, sounds, player)
	
	def _get_url(self):
		return self._player.get_backup_url()
		
	def _set_url(self, url):
		self._player.set_backup_url(url)
