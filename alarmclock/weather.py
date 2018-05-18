#!/usr/bin/python
# -*- coding: utf-8 -*-
import pyowm
import datetime

class Weather(object):

	def __init__(self):
		self._owm_key = None
		self._location = None
		
	def set_owm_key(self, key):
		self._owm_key = key
		
	def set_location(self, location):
		self._location = location
		
	def get_rain_today():
		fc = owm.three_hours_forecast(location)
		n = self._cut_out_todays_forecaster(fc)
		return n.will_have_rain()
		
	def _cut_out_todays_forecaster(self, forecaster):
		"""
		Returns a forecaster containing forecast weather object for today only
		Provide a forecaster object from pyowm that contains data for today (and possibly other days).
		"""
		
		today_midnight = datetime.datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0)
		end_of_today = today_midnight + datetime.timedelta(days=1)
		return self._cut_out_forecaster(forecaster, today_midnight, end_of_today)
		
	def _cut_out_tomorrows_forecaster(self, forecaster):
		"""
		Returns a forecaster containing forecast weather object for only the day after today.
		Provide a forecaster object from pyowm that contains data for tomorrow.
		"""
	
		today_midnight = datetime.datetime.utcnow().replace(hour=0,minute=0,second=0,microsecond=0)
		tomorrow_start = today_midnight + datetime.timedelta(days=1)
		tomorrow_end =  tomorrow_start + datetime.timedelta(days=1)
		return self._cut_out_forecaster(forecaster, tomorrow_start, tomorrow_end)
		
	def _cut_out_forecaster(self, forecaster, start_date, end_date):
		"""
		Returns a forecaster containing forecast weather object for the given period.
		Provide a forecaster object from pyowm that contains data for tha period.
		"""
		
		forecast = fc.get_forecast()
		new_forecast_weathers = [w for w in forecast.get_weathers() if (w.get_reference_time('date').replace(tzinfo=None) > start_date and w.get_reference_time('date').replace(tzinfo=None) < end_date)]
		new_forecast = pyowm.webapi25.forecast.Forecast(forecast.get_interval(), forecast.get_reception_time(), forecast.get_location(), new_forecast_weathers)
		return pyowm.webapi25.forecaster.Forecaster(new_forecast)
	
	