#!/usr/bin/python
# -*- coding: utf-8 -*-

from abstract_time_setter import AbstractTimeSetter

class TimeSetter2(AbstractTimeSetter):

	def _get_alarmtime(self):
		return self._alarm.get_alarmtime_2()

	def _set_alarmtime(self, time_s):
		self._alarm.set_alarmtime_2(time_s)