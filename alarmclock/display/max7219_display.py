#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import max7219
from max7219.led import matrix as mat
from matrix_based_display import MatrixBasedDisplay
from matrix_based_display import SMALL_FONT
		
class Max7219Display(MatrixBasedDisplay):

	def __init__(self):
		super(Max7219Display, self).__init__()
		self._display_matrix = Display4x8x8(cascaded=4, vertical=True)

	# Brightness
	def set_brightness(self, bright):
		super(Max7219Display, self).set_brightness(bright)
		self._display_matrix.brightness(bright)
		
	# Display
	def _display_text(self, alignment):
		super(Max7219Display, self)._display_text(alignment)
		self._display_matrix.prepare_message_aligned(self._current_displaying, alignment, font=SMALL_FONT)
		
	def _display_special(self, alignment):
		super(Max7219Display, self)._display_special(alignment)
		self._display_matrix.prepare_aligned(self._get_special_matrix(),alignment)
		
	def _display_clear(self):
		super(Max7219Display, self)._display_clear()
		self._display_matrix.clear()
		
	def _display_flush(self):
		super(Max7219Display, self)._display_flush()
		self._display_matrix.flush()
		
	def _prepare_signal_1(self):
		super(Max7219Display, self)._prepare_signal_1()
		self._display_matrix.prepare_signal_1(self._signal1)
		
	def _prepare_signal_2(self):
		super(Max7219Display, self)._prepare_signal_2()
		self._display_matrix.prepare_signal_2(self._signal2)
		
	
	
class Display4x8x8(mat):

	def prepare_aligned(self, data, alignment):
		display_length = self.NUM_DIGITS * self._cascaded
		# How much margin we need on the left so it's centered
		# old margin to center:
		#margin = int((display_length - len(data))/2)
		# new margin to align right

		# default margin left:
		margin = None
		if alignment == 0:
			margin = 0
		elif alignment == 1:
			margin = int(display_length - len(data))
		elif alignment == 2:
			margin = int((display_length - len(data))/2)
			
		# Reset the buffer so no traces of the previous message are left
		self._buffer = [0] * display_length
		for pos, value in enumerate(data):
			self._buffer[margin+pos] = value

	def prepare_message_aligned(self, text, alignment=2, font=SMALL_FONT):
		"""
		Prepares the given message to be outputted to the device using flush().
		alignment=0: left, alignment=1: right, alignment=2: center
		"""

		src = [c for ascii_code in text for c in font[ord(ascii_code)]]
		self.prepare_aligned(src, alignment)
			
	def prepare_signal_1(self, value):
		self.pixel(0, 1, value, False)
		self.pixel(0, 2, value, False)
			
	def prepare_signal_2(self, value):
		self.pixel(0, 5, value, False)
		self.pixel(0, 6, value, False)
		