#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from display import Display

# Special Animations
NICE_WEATHER = [
	[ 0x00, 0x00, 0x08, 0x1C, 0x08, 0x00, 0x00 ],
	[ 0x00, 0x00, 0x08, 0x1C, 0x08, 0x00, 0x00 ],
	[ 0x00, 0x00, 0x08, 0x1C, 0x08, 0x00, 0x00 ],
	
	[ 0x00, 0x14, 0x08, 0x3E, 0x08, 0x14, 0x00 ],
	[ 0x00, 0x14, 0x08, 0x3E, 0x08, 0x14, 0x00 ],
	[ 0x00, 0x14, 0x08, 0x3E, 0x08, 0x14, 0x00 ],
	[ 0x00, 0x14, 0x08, 0x3E, 0x08, 0x14, 0x00 ],
	[ 0x00, 0x14, 0x08, 0x3E, 0x08, 0x14, 0x00 ],
			
	[ 0x22, 0x14, 0x08, 0x7F, 0x08, 0x14, 0x22 ],
	[ 0x22, 0x14, 0x08, 0x7F, 0x08, 0x14, 0x22 ],
	[ 0x22, 0x14, 0x08, 0x7F, 0x08, 0x14, 0x22 ]
]
RAIN = [
	[ 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0C ],
	[ 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0C ],
	[ 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0C ],

	[ 0x18, 0x16, 0x12, 0x31, 0x11, 0x12, 0x0C ],
	[ 0x18, 0x16, 0x12, 0x31, 0x11, 0x12, 0x0C ],
	[ 0x18, 0x16, 0x12, 0x31, 0x11, 0x12, 0x0C ],
	
	[ 0x18, 0x36, 0x12, 0x71, 0x11, 0x32, 0x0C ],
	[ 0x18, 0x36, 0x12, 0x71, 0x11, 0x32, 0x0C ],
	[ 0x18, 0x36, 0x12, 0x71, 0x11, 0x32, 0x0C ],
			
	[ 0x18, 0x76, 0x12, 0xF1, 0x11, 0x72, 0x0C ],
	[ 0x18, 0x76, 0x12, 0xF1, 0x11, 0x72, 0x0C ],
	[ 0x18, 0x76, 0x12, 0xF1, 0x11, 0x72, 0x0C ]
]
CLOUDS = [
	[0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0xc, 0x00, 0x00],
	[0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0xc, 0x00, 0x00],
	[0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0xc, 0x00, 0x00],
	
	[0x00, 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0c, 0x00],
	[0x00, 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0c, 0x00],
	[0x00, 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0c, 0x00],
	
	[0x00, 0x00, 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0c],
	[0x00, 0x00, 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0c],
	[0x00, 0x00, 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0c],
	
	[0x00, 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0c, 0x00],
	[0x00, 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0c, 0x00],
	[0x00, 0x18, 0x16, 0x12, 0x11, 0x11, 0x12, 0x0c, 0x00]
]

SNOW = [
	[0x0, 0x0, 0xa, 0x1b, 0x4, 0x1b, 0xa, 0x0],
	[0x0, 0x0, 0xa, 0x1b, 0x4, 0x1b, 0xa, 0x0],
	[0x0, 0x0, 0xa, 0x1b, 0x4, 0x1b, 0xa, 0x0],
	
	[0x0, 0x0, 0x14, 0x36, 0x8, 0x36, 0x14, 0x0],
	[0x0, 0x0, 0x14, 0x36, 0x8, 0x36, 0x14, 0x0],
	[0x0, 0x0, 0x14, 0x36, 0x8, 0x36, 0x14, 0x0],
	
	[0x0, 0x0, 0x28, 0x6c, 0x10, 0x6c, 0x28, 0x0],
	[0x0, 0x0, 0x28, 0x6c, 0x10, 0x6c, 0x28, 0x0],
	[0x0, 0x0, 0x28, 0x6c, 0x10, 0x6c, 0x28, 0x0],
	
	[0x0, 0x0, 0x50, 0xd8, 0x20, 0xd8, 0x50, 0x0],
	[0x0, 0x0, 0x50, 0xd8, 0x20, 0xd8, 0x50, 0x0],
	[0x0, 0x0, 0x50, 0xd8, 0x20, 0xd8, 0x50, 0x0]
]


PLUG = [
	[0x0, 0x1c, 0x3f, 0xfc, 0xfc, 0x3f, 0x1c, 0x0]
]

TV = [
	[0xfc, 0xfc, 0xcc, 0x84, 0x85, 0xce, 0xfd, 0xfc]
]
HUMAN = [
	[0x0, 0x80, 0xcc, 0xde, 0xde, 0xcc, 0x80, 0x0]
]
SND = [
	[0x18, 0x0, 0x18, 0x3c, 0x7e, 0x0, 0x5a, 0x99]
]
KEY = [
	[0x18, 0x24, 0x24, 0x18, 0x8, 0x18, 0x8, 0x18]
]
RUNNER = [
	[0x24, 0x22, 0x1a, 0x1c, 0x27, 0xcb, 0x8, 0x0]
]
SIGNAL_LOW = [
	[0xc0, 0x0, 0xc0, 0x0, 0xc0, 0x0, 0xc0, 0x0]
]
SIGNAL_MED = [
	[0xc0, 0x0, 0xf0, 0x0, 0xfc, 0x0, 0xc0, 0x0]
]
SIGNAL_HIGH = [
	[0xc0, 0x0, 0xf0, 0x0, 0xfc, 0x0, 0xff, 0x0]
]
SUN2 = [
	[0x91, 0x42, 0x18, 0x3d, 0xbc, 0x18, 0x42, 0x89]
]
HEART = [
	[0x0, 0x1c, 0x3e, 0x7c, 0xf8, 0x7c, 0x3e, 0x1c]
]
NOTE1 = [
	[0x0, 0xc0, 0xe0, 0x7e, 0x2, 0x4, 0x0, 0x0]
]
NOTE2 = [
	[0x0, 0xc0, 0xe0, 0x7c, 0x6, 0x62, 0x72, 0x3e]
]


SPECIALS = {
			"sun": NICE_WEATHER,
			"rain": RAIN,
			"clouds": CLOUDS,
			"snow": SNOW,
			"plug": PLUG,
			"tv": TV,
			"human": HUMAN,
			"snd": SND,
			"key": KEY,
			"runner": RUNNER,
			"heart": HEART,
			"note1": NOTE1,
			"note2": NOTE2,
			"signal_low": SIGNAL_LOW,
			"signal_med": SIGNAL_MED,
			"signal_high": SIGNAL_HIGH,
}


# FONT
SMALL_FONT = [
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ],
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ], # SPACE
			[ 0x00, 0x00, 0x00, 0x4F, 0x00, 0x00 ], # !
			[ 0x00, 0x00, 0x07, 0x00, 0x07, 0x00 ], # "
			[ 0x00, 0x14, 0x7F, 0x14, 0x7F, 0x14 ], # #
			[ 0x00, 0x24, 0x2A, 0x7F, 0x2A, 0x12 ], # $
			[ 0x00, 0x23, 0x13, 0x08, 0x64, 0x62 ], # %
			[ 0x00, 0x36, 0x49, 0x55, 0x22, 0x50 ], # &
			[ 0x00, 0x00, 0x05, 0x03, 0x00, 0x00 ], # '
			[ 0x00, 0x00, 0x1C, 0x22, 0x41, 0x00 ], # (
			[ 0x00, 0x00, 0x41, 0x22, 0x1C, 0x00 ], # )
			[ 0x00, 0x14, 0x08, 0x3E, 0x08, 0x14 ], # *
			[ 0x00, 0x08, 0x08, 0x3E, 0x08, 0x08 ], # +
			[ 0x00, 0x00, 0x50, 0x30, 0x00, 0x00 ], # ,
			[ 0x00, 0x08, 0x08, 0x08, 0x08, 0x08 ], # -
			[ 0x00, 0x00, 0x60, 0x60, 0x00, 0x00 ], # .
			[ 0x00, 0x20, 0x10, 0x08, 0x04, 0x02 ], # /
			[ 0x00, 0x3E, 0x51, 0x49, 0x45, 0x3E ], # 0
			[ 0x00, 0x00, 0x42, 0x7F, 0x40, 0x00 ], # 1
			[ 0x00, 0x42, 0x61, 0x51, 0x49, 0x46 ], # 2
			[ 0x00, 0x21, 0x41, 0x45, 0x4B, 0x31 ], # 3
			[ 0x00, 0x18, 0x14, 0x12, 0x7F, 0x10 ], # 4
			[ 0x00, 0x27, 0x45, 0x45, 0x45, 0x39 ], # 5
			[ 0x00, 0x3C, 0x4A, 0x49, 0x49, 0x30 ], # 6
			[ 0x00, 0x01, 0x71, 0x09, 0x05, 0x03 ], # 7
			[ 0x00, 0x36, 0x49, 0x49, 0x49, 0x36 ], # 8
			[ 0x00, 0x06, 0x49, 0x49, 0x29, 0x1E ], # 9
			[ 0x00, 0x00, 0x36, 0x36, 0x00, 0x00 ], # :
			[ 0x00, 0x56, 0x36, 0x00, 0x00, 0x00 ], # ;
			[ 0x00, 0x08, 0x14, 0x22, 0x41, 0x00 ], # <
			[ 0x00, 0x14, 0x14, 0x14, 0x14, 0x14 ], # =
			[ 0x00, 0x00, 0x41, 0x22, 0x14, 0x08 ], # >
			[ 0x00, 0x02, 0x01, 0x51, 0x09, 0x06 ], # ?
			[ 0x00, 0x30, 0x49, 0x79, 0x41, 0x3E ], # @
			[ 0x00, 0x7E, 0x11, 0x11, 0x11, 0x7E ], # A
			[ 0x00, 0x7F, 0x49, 0x49, 0x49, 0x36 ], # B
			[ 0x00, 0x3E, 0x41, 0x41, 0x41, 0x22 ], # C
			[ 0x00, 0x7F, 0x41, 0x41, 0x22, 0x1C ], # D
			[ 0x00, 0x7F, 0x49, 0x49, 0x49, 0x41 ], # E
			[ 0x00, 0x7F, 0x09, 0x09, 0x09, 0x01 ], # F
			[ 0x00, 0x3E, 0x41, 0x49, 0x49, 0x7A ], # G
			[ 0x00, 0x7F, 0x08, 0x08, 0x08, 0x7F ], # H
			[ 0x00, 0x00, 0x41, 0x7F, 0x41, 0x00 ], # I
			[ 0x00, 0x20, 0x40, 0x41, 0x3F, 0x01 ], # J
			[ 0x00, 0x7F, 0x08, 0x14, 0x22, 0x41 ], # K
			[ 0x00, 0x7F, 0x40, 0x40, 0x40, 0x40 ], # L
			[ 0x00, 0x7F, 0x02, 0x0C, 0x02, 0x7F ], # M
			[ 0x00, 0x7F, 0x04, 0x08, 0x10, 0x7F ], # N
			[ 0x00, 0x3E, 0x41, 0x41, 0x41, 0x3E ], # O
			[ 0x00, 0x7F, 0x09, 0x09, 0x09, 0x06 ], # P
			[ 0x00, 0x3E, 0x41, 0x51, 0x21, 0x5E ], # Q
			[ 0x00, 0x7F, 0x09, 0x19, 0x29, 0x46 ], # R
			[ 0x00, 0x46, 0x49, 0x49, 0x49, 0x31 ], # S
			[ 0x00, 0x01, 0x01, 0x7F, 0x01, 0x01 ], # T
			[ 0x00, 0x3F, 0x40, 0x40, 0x40, 0x3F ], # U
			[ 0x00, 0x1F, 0x20, 0x40, 0x20, 0x1F ], # V
			[ 0x00, 0x3F, 0x40, 0x30, 0x40, 0x3F ], # W
			[ 0x00, 0x63, 0x14, 0x08, 0x14, 0x63 ], # X
			[ 0x00, 0x07, 0x08, 0x70, 0x08, 0x07 ], # Y
			[ 0x00, 0x61, 0x51, 0x49, 0x45, 0x43 ], # Z
			[ 0x00, 0x00, 0x7F, 0x41, 0x41, 0x00 ], # [
			[ 0x00, 0x02, 0x04, 0x08, 0x10, 0x20 ], # backslash
			[ 0x00, 0x00, 0x41, 0x41, 0x7F, 0x00 ], # ]
			[ 0x00, 0x04, 0x02, 0x01, 0x02, 0x04 ], # ^
			[ 0x00, 0x40, 0x40, 0x40, 0x40, 0x40 ], # _
			[ 0x00, 0x04, 0x0A, 0x04, 0x00, 0x00 ], # `
			[ 0x00, 0x20, 0x54, 0x54, 0x54, 0x78 ], # a
			[ 0x00, 0x7F, 0x50, 0x48, 0x48, 0x30 ], # b
			[ 0x00, 0x38, 0x44, 0x44, 0x44, 0x00 ], # c
			[ 0x00, 0x38, 0x44, 0x44, 0x48, 0x7F ], # d
			[ 0x00, 0x38, 0x54, 0x54, 0x54, 0x18 ], # e
			[ 0x00, 0x08, 0x7E, 0x09, 0x01, 0x02 ], # f
			[ 0x00, 0x0C, 0x52, 0x52, 0x52, 0x3E ], # g
			[ 0x00, 0x7F, 0x08, 0x04, 0x04, 0x78 ], # h
			[ 0x00, 0x00, 0x44, 0x7D, 0x40, 0x00 ], # i
			[ 0x00, 0x20, 0x40, 0x44, 0x3D, 0x00 ], # j
			[ 0x00, 0x7F, 0x10, 0x28, 0x44, 0x00 ], # k
			[ 0x00, 0x00, 0x41, 0x7F, 0x40, 0x00 ], # l
			[ 0x00, 0x78, 0x04, 0x78, 0x04, 0x78 ], # m
			[ 0x00, 0x7C, 0x08, 0x04, 0x04, 0x78 ], # n
			[ 0x00, 0x38, 0x44, 0x44, 0x44, 0x38 ], # o
			[ 0x00, 0x7C, 0x14, 0x14, 0x14, 0x08 ], # p
			[ 0x00, 0x08, 0x14, 0x14, 0x18, 0x7C ], # q
			[ 0x00, 0x7C, 0x08, 0x04, 0x04, 0x08 ], # r
			[ 0x00, 0x48, 0x54, 0x54, 0x54, 0x20 ], # s
			[ 0x00, 0x04, 0x3F, 0x44, 0x40, 0x20 ], # t
			[ 0x00, 0x3C, 0x40, 0x40, 0x20, 0x7C ], # u
			[ 0x00, 0x1C, 0x20, 0x40, 0x20, 0x1C ], # v
			[ 0x00, 0x3C, 0x40, 0x30, 0x40, 0x3C ], # w
			[ 0x00, 0x44, 0x28, 0x10, 0x28, 0x44 ], # x
			[ 0x00, 0x0C, 0x50, 0x50, 0x50, 0x3C ], # y
			[ 0x00, 0x44, 0x64, 0x54, 0x4C, 0x44 ], # z
			[ 0x00, 0x00, 0x08, 0x36, 0x41, 0x00 ], # [
			[ 0x00, 0x00, 0x00, 0x7F, 0x00, 0x00 ], # |
			[ 0x00, 0x00, 0x41, 0x36, 0x08, 0x00 ], # ]
			[ 0x00, 0x0C, 0x02, 0x0C, 0x10, 0x0C ], # ~
			[ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ], # DEL
		]

class MatrixBasedDisplay(Display):

	def __init__(self):
		Display.__init__(self)
		self._brightness = 7 # default brightness
		self._special_index = 0
		
	#
	# Brightness section
	#
		
	def set_brightness(self, bright):
		self._brightness = bright
	
	def get_max_brightness(self):
		# default
		return 15
		
	def get_brightness(self):
		return self._brightness
		
	#
	# Display section
	#
	
	def _display_text(self, alignment):
		pass
		
	def _display_clear(self):
		pass
		
	def _display_flush(self):
		pass
		
	def _prepare_signal_1(self):
		pass
		
	def _prepare_signal_2(self):
		pass
		
	#
	# Special Function ability
	#
	
	def _display_special(self, alignment):
		pass
		
	def _update_internal_state(self):
		super(MatrixBasedDisplay, self)._update_internal_state()
		if self._current_mode == self.MODES[3]:
			self._special_index = ( self._special_index + 1) % len(SPECIALS[self._current_displaying])
			self._changed = True
		
	def show_special(self, special):
		# reset
		self._special_index = 0
		super(MatrixBasedDisplay, self).show_special(special)
	
	def _get_special_matrix(self):
		return SPECIALS[self._current_displaying][self._special_index]
	
	#
	# Output section
	#
	
	def _output(self):
		if self._current_mode == self.MODES[2]: # blank 
			self._display_clear()
			return # make sure to not do anything else
		if self._current_mode == self.MODES[1]:
			self._display_text(alignment=1) # time displayed aligned right
		elif self._current_mode == self.MODES[0]:
			self._display_text(alignment=2) # text displayed centered
		elif self._current_mode == self.MODES[3]:
			self._display_special(alignment=2) # special displayed centered
			
		self._prepare_signal_1()
		self._prepare_signal_2()
		self._display_flush() # using double buffering