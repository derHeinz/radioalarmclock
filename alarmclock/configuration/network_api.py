#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
import threading
from flask import Flask, jsonify, request, make_response
from configurator import Configurator
from multiprocessing import Process
from werkzeug.serving import make_server

class NetworkAPI(threading.Thread):
	
	def __init__(self, config):
		super(NetworkAPI, self).__init__()
		self.setDaemon(True)
		self.app = Flask(__name__)
		self._config = config
		self._server = make_server(host='0.0.0.0', port=5000, app=self.app, threaded=True)
		self.ctx = self.app.app_context()
		self.ctx.push()

		# register some endpoints
		
		# alarm 1
		self.app.add_url_rule(rule="/v1.0/alarmtime_1", endpoint="get_alarmtime_1", view_func=self.get_alarmtime_1, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/alarmtime_1", endpoint="set_alarmtime_1", view_func=self.set_alarmtime_1, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/alarm_1", endpoint="get_alarm_1", view_func=self.get_alarm_1, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/alarm_1", endpoint="set_alarm_1", view_func=self.set_alarm_1, methods=['POST'])
		# alarm 2
		self.app.add_url_rule(rule="/v1.0/alarmtime_2", endpoint="get_alarmtime_2", view_func=self.get_alarmtime_2, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/alarmtime_2", endpoint="set_alarmtime_2", view_func=self.set_alarmtime_2, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/alarm_2", endpoint="get_alarm_2", view_func=self.get_alarm_2, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/alarm_2", endpoint="set_alarm_2", view_func=self.set_alarm_2, methods=['POST'])
		
		# player
		self.app.add_url_rule(rule="/v1.0/volume", endpoint="get_volume", view_func=self.get_volume, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/volume", endpoint="set_volume", view_func=self.set_volume, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/fadein", endpoint="get_fadein", view_func=self.get_fadein, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/fadein", endpoint="set_fadein", view_func=self.set_fadein, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/fadeinsteps", endpoint="get_fadeinsteps", view_func=self.get_fadeinsteps, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/fadeinsteps", endpoint="set_fadeinsteps", view_func=self.set_fadeinsteps, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/fadeinstepsize", endpoint="get_fadeinstepsize", view_func=self.get_fadeinstepsize, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/fadeinstepsize", endpoint="set_fadeinstepsize", view_func=self.set_fadeinstepsize, methods=['POST'])
		
		# sounds
		self.app.add_url_rule(rule="/v1.0/sounds", endpoint="get_sounds", view_func=self.get_sounds, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/sound", endpoint="add_sound", view_func=self.add_sound, methods=['PUT'])
		
		# display
		self.app.add_url_rule(rule="/v1.0/brightness", endpoint="get_brightness", view_func=self.get_brightness, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/brightness", endpoint="set_brightness", view_func=self.set_brightness, methods=['POST'])
		
		# timeout
		self.app.add_url_rule(rule="/v1.0/timeout", endpoint="get_timeout", view_func=self.get_timeout, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/timeout", endpoint="set_timeout", view_func=self.set_timeout, methods=['POST'])
		
		# dimmer
		self.app.add_url_rule(rule="/v1.0/dimmer_active", endpoint="get_dimmer_active", view_func=self.get_dimmer_active, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/dimmer_active", endpoint="set_dimmer_active", view_func=self.set_dimmer_active, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/latitude", endpoint="get_latitude", view_func=self.get_latitude, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/latitude", endpoint="set_latitude", view_func=self.set_latitude, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/longitude", endpoint="get_longitude", view_func=self.get_longitude, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/longitude", endpoint="set_longitude", view_func=self.set_longitude, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/night_percentage", endpoint="get_night_percentage", view_func=self.get_night_percentage, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/night_percentage", endpoint="set_night_percentage", view_func=self.set_night_percentage, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/day_percentage", endpoint="get_day_percentage", view_func=self.get_day_percentage, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/day_percentage", endpoint="set_day_percentage", view_func=self.set_day_percentage, methods=['POST'])
		
		# register default error handler
		self.app.register_error_handler(code_or_exception=404, f=self.not_found)
	
	def run(self):
		self._server.serve_forever()
						
	def wrong_request(self, error="Internal Error"):
		return make_response(jsonify({'error': error}), 400)
		
	def not_found(self, error):
		return make_response(jsonify({'error': 'Not found'}), 404)
		
	# some methods for simple processing.	
	
	def _get_simple(self, component, property):
		return jsonify({property: self._config.get(component, property)})
		
	def _set_simple(self, component, property):
		if not request.json or not property in request.json:
			self.wrong_request()
			return
		value = request.json[property]
		self._config.set(component, property, value)
		return jsonify({'result': True})
		
	def _set_simple_bool(self, component, property):
		if not request.json or not property in request.json:
			self.wrong_request()
			return
		# mapping from false->False, true->True
		value = request.json[property]
		if (value == 'true'):
			value = True
		elif (value == 'false'):
			value = False
		else:
			self.wrong_request()
			return
		self._config.set(component, property, value)
		return jsonify({'result': True})	
	
	#
	# Dimmer
	#
	def get_dimmer_active(self):
		return self._get_simple("dimmer", "active")
		
	def set_dimmer_active(self):
		return self._set_simple_bool("dimmer", "active")
		
	def get_night_percentage(self):
		return self._get_simple("dimmer", "night_percentage")
		
	def set_night_percentage(self):
		return self._set_simple("dimmer", "night_percentage")
		
	def get_day_percentage(self):
		return self._get_simple("dimmer", "day_percentage")
		
	def set_day_percentage(self):
		return self._set_simple("dimmer", "day_percentage")
	
	def get_latitude(self):
		return self._get_simple("dimmer", "lat")
		
	def set_latitude(self):
		return self._set_simple("dimmer", "lat")
		
	def get_longitude(self):
		return self._get_simple("dimmer", "lon")
		
	def set_longitude(self):
		return self._set_simple("dimmer", "lon")
		
	#
	# Player
	#
	
	# fadeinstepsize set, get
	def get_fadeinstepsize(self):
		return self._get_simple("player", "fadein_step_size")
		
	def set_fadeinstepsize(self):
		return self._set_simple("player", "fadein_step_size")
	
	# fadeinsteps set, get
	def get_fadeinsteps(self):
		return self._get_simple("player", "fadein_steps")
		
	def set_fadeinsteps(self):
		return self._set_simple("player", "fadein_steps")
	
	# fadein set, get
	def get_fadein(self):
		return self._get_simple("player", "fadein")
		
	def set_fadein(self):
		return self._set_simple_bool("player", "fadein")

	# volume set, get
	def get_volume(self):
		return self._get_simple("player", "volume")
	
	def set_volume(self):
		return self._set_simple("player", "volume")
		
	#
	# Alarm
	#
		
	# alarmtime_1 set, get
	def get_alarmtime_1(self):
		return self._get_simple("alarm", "alarmtime_1")
		
	def set_alarmtime_1(self):
		return self._set_simple("alarm", "alarmtime_1")
		
	# alarm_1 set, get
	def get_alarm_1(self):
		return self._get_simple("alarm", "alarm_1")
		
	def set_alarm_1(self):
		return self._set_simple_bool("alarm", "alarm_1")
		
	# alarmtime_2 set, get
	def get_alarmtime_2(self):
		return self._get_simple("alarm", "alarmtime_2")
		
	def set_alarmtime_2(self):
		return self._set_simple("alarm", "alarmtime_2")
		
	# alarm_2 set, get
	def get_alarm_2(self):
		return self._get_simple("alarm", "alarm_2")
		
	def set_alarm_2(self):
		return self._set_simple_bool("alarm", "alarm_2")
		
	#
	# Sounds
	#	
	
	# sounds set, get
	def get_sounds(self):
		return self._get_simple("sounds", "sounds")

	def add_sound(self):
		if not request.json or not 'title' in request.json or not 'url' in request.json:
			self.wrong_request()
			return
		title = request.json['title']
		url = request.json['url']
		self._config.get("sounds", "sounds")[title] = url
		return jsonify({'result': True})
		
		
	#
	# Display
	#
		
	# brightness set, get
	def get_brightness(self):
		return self._get_simple("display", "brightness")
		
	def set_brightness(self):
		return self._set_simple("display", "brightness")
		
	#
	# Timeout
	#
		
	# timeout set, get
	def get_timeout(self):
		return self._get_simple("timeout", "timeout")
		
	def set_timeout(self):
		return self._set_simple("timeout", "timeout")

# only for test
if __name__ == '__main__':
	nw_api = NetworkAPI(None)
	nw_api.start()
	
	import time
	starttime=time.time()
	while True:
		print "tick"
		time.sleep(60.0 - ((time.time() - starttime) % 60.0))
		
	