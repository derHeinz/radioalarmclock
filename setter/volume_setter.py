#!/usr/bin/python
# -*- coding: utf-8 -*-

class VolumeSetter(object):
	"""
	Used to set volume.
	"""
	
	def __init__(self, display, player):
		""" gimme display."""
		self._player = player
		self._display = display
		
	def display(self):
		self._display.show_text(self._volume_text())
		
	def next(self):
		self._player.volume_up()
		self.display()
		
	def prev(self):
		self._player.volume_down()
		self.display()
		
	def select(self):
		self._display.show_text_blinking(self._volume_text())
		return "back"
		
	def _volume_text(self):
		return "Volume: " + str(self._player.get_volume())
		