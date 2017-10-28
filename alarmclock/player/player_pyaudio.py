#!/usr/bin/python
# -*- coding: utf-8 -*-

from player import Player
import logging
import pyaudio
import wave
import threading

class PlayerPyAudio(Player, threading.Thread):
	''' Another player stub for windows testing.'''

	CHUNK = 1024
	
	def __init__(self, scheduler):
		Player.__init__(self, scheduler)
		threading.Thread.__init__(self)
		self.setDaemon(True)
		# 
		self._run_url = None
		self._volume = 0
		# initialize runnables
		self._p = pyaudio.PyAudio()
		self._wf = None
		self._stream = None
		self._please_stop = False
		
	def _play(self):
		
		# prevent 2 processes
		if self.is_running():
			# check whether the same url ran
			if (self._run_url == self._url):
				return # issued to run the same thing again.
			self.stop()
	
		self._wf = wave.open(self._url, 'rb')
		self._stream = self._p.open(format=self._p.get_format_from_width(self._wf.getsampwidth()),
                channels=self._wf.getnchannels(),
                rate=self._wf.getframerate(),
                output=True)
		self._run_url = self._url
		self.start()
		
	def _stop(self):
		self._please_stop = True
		self.join()
		self._please_stop = False
		
	def get_volume(self):
		return self._volume
		
	def set_volume(self, value):
		logging.info("setting volume to " + str(value))
		self._volume = value
		if (self._volume > 100):
			self._volume = 100
		elif (self._volume < 0):
			self._volume = 0
			
	def is_running(self):
		return (self._stream =! None)
		
	def run(self):
		logging.debug("audio now playing")
		data = self._wf.readframes(self.CHUNK)
		while data != '' and not self._please_stop:
			self._stream.write(data)
			data = self._wf.readframes(self.CHUNK)
		self._wf = None
		self._run_url = None

		logging.debug("audio now stopping")
		self._stream.stop_stream()
		self._stream.close()
		self._stream = None

		self._p.terminate()
