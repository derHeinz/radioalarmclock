#!/usr/bin/python
# -*- coding: utf-8 -*-

from player import Player
import logging
import pyaudio
import wave

class PlayerPyAudio(Player):
	''' Another player stub for windows testing.'''

	CHUNK = 1024
	PlAY_JOB_ID = "Player-ToPlay"
	
	def __init__(self, scheduler):
		super(PlayerPyAudio, self).__init__(scheduler)
		# 
		self._run_url = None
		self._volume = 0
		# initialize runnables
		self._p = None
		self._wf = None
		self._stream = None
		self._please_stop = False
		
	def _play_url(self, url):
		# prevent 2 processes
		if self.is_running():
			# check whether the same url ran
			if (self._run_url == url):
				return # issued to run the same thing again.
			self.stop()
			
		self._p = pyaudio.PyAudio()
		logging.debug("pyaudio info: " + str(self._p.get_default_input_device_info()))
	
		self._wf = wave.open(url, 'rb')
		self._stream = self._p.open(format=self._p.get_format_from_width(self._wf.getsampwidth()),
                channels=self._wf.getnchannels(),
                rate=self._wf.getframerate(),
                output=True)
		self._run_url = url
		
		self._please_stop = False
		self._scheduler.add_job(id=self.PlAY_JOB_ID, func=self.run)
		
	def _stop(self):
		self._please_stop = True
		# unrun the job
		scheduled_run = None
		for job in self._scheduler.get_jobs():
			if (job.id == self.PlAY_JOB_ID):
				scheduled_run = job
		if (scheduled_run != None):
			scheduled_run.remove()
		
	def get_volume(self):
		return self._volume
		
	def set_volume(self, value):
		logging.debug("setting volume to " + str(value))
		self._volume = value
		if (self._volume > 100):
			self._volume = 100
		elif (self._volume < 0):
			self._volume = 0
			
	def is_running(self):
		return (self._stream != None)
		
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
		self._p = None
