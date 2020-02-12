#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
import logging
from threading import Thread
from matrix_based_display import MatrixBasedDisplay
from matrix_based_display import SMALL_FONT
from matrix_based_display import NERD_FONT
from matrix_based_display import ICONIC_FONT_SMALL
from matrix_based_display import ICONIC_FONT_BIG

def _create_circle(self, x, y, r, **kwargs):
	return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
	
class TKinterDisplay(MatrixBasedDisplay):

	DISPLAY_SIZE = 8
	DISPLAY_AMOUNT = 4
	DISPLAY_LENGTH = DISPLAY_AMOUNT * DISPLAY_SIZE

	def __init__(self):
		super(TKinterDisplay, self).__init__()
		
		# init processing stuff
		self._data = [0] * self.DISPLAY_LENGTH # 32 ints field
		self._circles = None
		self._nerd = False
		
		# init ui
		self._root = tk.Tk()
		self._canvas = None
		self._init_internal()
		
	def set_nerd(self, val):
		self._nerd = val
		
	def get_nerd(self):
		return self._nerd
		
	def _init_internal(self):
		
		self._canvas = tk.Canvas(self._root, width=490, height=130, borderwidth=0, highlightthickness=0, bg="black")
		self._canvas.grid()
		tk.Canvas.create_circle = _create_circle
		
		self._draw_circles()
		self._canvas.pack()
		
		# title
		self._root.wm_title("Dot Matrix")
				
		# start threaded
		def mainloop():
			self._root.mainloop()
		thread = Thread(target = mainloop)
		thread.start()
	
	def _calc_color(self):
		switcher = {
			0: "#400700",
			1: "#400700",
			2: "#500800",
			3: "#500800",
			4: "#600A00",
			5: "#600A00",
			6: "#700B00",
			7: "#700B00",
			8: "#800D00",
			9: "#800D00",
			10: "#900E00",
			11: "#900E00",
			12: "#A01000",
			13: "#A01000",
			14: "#AF1100",
			15: "#AF1100"
		}
		return switcher.get(self._brightness)
	
	# Display
	def _display(self, alignment, data):
		
		# copy of max7219
		# default margin left:
		margin = None
		if alignment == 0:
			margin = 0
		elif alignment == 1:
			margin = int(self.DISPLAY_LENGTH - len(data))
		elif alignment == 2:
			margin = int((self.DISPLAY_LENGTH - len(data))/2)
			
		# Reset the buffer so no traces of the previous message are left
		self._data = [0] * self.DISPLAY_LENGTH
		for pos, value in enumerate(data):
			self._data[margin+pos] = value
	
	def _display_text(self, alignment):
		super(TKinterDisplay, self)._display_text(alignment)
		data = [c for ascii_code in self._current_displaying for c in SMALL_FONT[ord(ascii_code)]]
		self._display(alignment, data)
		
	def _display_time(self):
		# do not inherit from above as we wanna
		if (self._nerd):
			logging.debug("nerdy")
			data = [c for ascii_code in self._current_displaying for c in ICONIC_FONT_SMALL[ord(ascii_code)]]
			self._display(alignment=1, data=data)
		else:
			super(TKinterDisplay, self)._display_time()
			
	def _display_special(self, alignment):
		super(TKinterDisplay, self)._display_special(alignment)
		src = self._get_special_matrix()
		self._display(alignment, src)
		
	def _display_clear(self):
		super(TKinterDisplay, self)._display_clear()
		self._data = [0] * self.DISPLAY_LENGTH
		self._draw_circles()
		
	def _display_flush(self):
		super(TKinterDisplay, self)._display_flush()
		self._draw_circles()
		
	def _prepare_signal_1(self):
		super(TKinterDisplay, self)._prepare_signal_1()
		if (self._signal1):
			self._data[0] = self._data[0] ^ 6
		else:
			self._data[0] = self._data[0] & 153
		
	def _prepare_signal_2(self):
		super(TKinterDisplay, self)._prepare_signal_2()
		pass # not yet implemented
				
			
	# Internal
	
	def _draw_circles(self, show_dots=True):
		
		# whether this is the initial call to draw
		initial = False
		if (self._circles == None):
			initial = True
			
		if (initial):
			self._canvas.delete(tk.ALL)
			self._circles = [0] * self.DISPLAY_LENGTH
		# create 1: 8x8 matrix
		dist = 15
		initial_dist = 10
		radius = 5
		
		# colors
		color1="#0E0B16"
		color2=self._calc_color() #"red"
		
		for i in range(self.DISPLAY_LENGTH):
			data = self._data[i]
			if (initial):
				self._circles[i] = [0] * self.DISPLAY_SIZE
			for j in range(self.DISPLAY_SIZE):
				d = data>>j

				#fg color
				col = color1
				#bg color
				outl = "#373737"
				
				if (d&1):
					col = color2
				else:
					if (not show_dots):
						col = "black"
						outl = "black"
				
				# either create circles
				if (initial):
					self._circles[i][j] = self._canvas.create_circle(initial_dist+dist*i, initial_dist+dist*j, radius, fill=col, outline=outl, width=1)
				else:
					# or just update them
					self._canvas.itemconfig(self._circles[i][j], fill=col)
	