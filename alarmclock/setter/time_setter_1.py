#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_time_setter import AbstractTimeSetter

class TimeSetter1(AbstractTimeSetter):

	def _get_alarmtime(self):
		return self._alarm.get_alarmtime_1()

	def _set_alarmtime(self, time_s):
		self._alarm.set_alarmtime_1(time_s)
