#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_setter import AbstractSetter

class VolumeSetter(AbstractSetter):
	"""
	Used to set volume.
	"""
	
	def __init__(self, display, player):
		super(VolumeSetter, self).__init__(display)
		self._player = player
		
	def next(self):
		self._player.volume_up()
		super(VolumeSetter, self).next()
		
	def prev(self):
		self._player.volume_down()
		super(VolumeSetter, self).prev()
		
	def _show_text(self):
		return str(self._player.get_volume())
