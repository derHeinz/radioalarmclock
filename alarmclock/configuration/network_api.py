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
		self.app.add_url_rule(rule="/v1.0/alarmtime", endpoint="get_alarmtime", view_func=self.get_alarmtime, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/alarmtime", endpoint="set_alarmtime", view_func=self.set_alarmtime, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/alarm", endpoint="get_alarm", view_func=self.get_alarm, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/alarm", endpoint="set_alarm", view_func=self.set_alarm, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/volume", endpoint="get_volume", view_func=self.get_volume, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/volume", endpoint="set_volume", view_func=self.set_volume, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/sounds", endpoint="get_sounds", view_func=self.get_sounds, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/sound", endpoint="add_sound", view_func=self.add_sound, methods=['PUT'])
		self.app.add_url_rule(rule="/v1.0/brightness", endpoint="get_brightness", view_func=self.get_brightness, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/brightness", endpoint="set_brightness", view_func=self.set_brightness, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/timeout", endpoint="get_timeout", view_func=self.get_timeout, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/timeout", endpoint="set_timeout", view_func=self.set_timeout, methods=['POST'])
		
		# register default error handler
		self.app.register_error_handler(code_or_exception=404, f=self.not_found)
	
	def run(self):
		self._server.serve_forever()
						
	def wrong_request(self, error="Internal Error"):
		return make_response(jsonify({'error': error}), 400)
		
	def not_found(self, error):
		return make_response(jsonify({'error': 'Not found'}), 404)
		
	# set alarm, get alarm
	def get_alarmtime(self):
		return jsonify({'alarmtime': self._config.get("alarm", "alarmtime")})
		
	def set_alarmtime(self):
		if not request.json or not 'alarmtime' in request.json:
			self.wrong_request()
		alarmtime = request.json['alarmtime']
		self._config.set("alarm", "alarmtime", alarmtime)
		return jsonify({'result': True})
		
	# set alarm, get alarm
	def get_alarm(self):
		return jsonify({'alarm': self._config.get("alarm", "alarm")})
		
	def set_alarm(self):
		if not request.json or not 'alarm' in request.json:
			self.wrong_request()
		alarm = request.json['alarm']
		if not type(alarm) == bool:
			self.wrong_request()
		self._config.set("alarm", "alarm", alarm)
		return jsonify({'result': True})
		
	# set volume, get volume
	def get_volume(self):
		return jsonify({'volume': self._config.get("player", "volume")})	
	
	def set_volume(self):
		if not request.json or not 'volume' in request.json:
			self.wrong_request()
		volume = int(request.json['volume'])
		self._config.set("player", "volume", volume)
		return jsonify({'result': True})
		
	# get sounds, add sound
	def get_sounds(self):
		return jsonify({'sounds': self._config.get("sounds", "sounds")})	

	def add_sound(self):
		if not request.json or not 'title' in request.json or not 'url' in request.json:
			self.wrong_request()
		title = request.json['title']
		url = request.json['url']
		self._config.get("sounds", "sounds")[title] = url
		return jsonify({'result': True})
		
	# set get brightness
	def get_brightness(self):
		return jsonify({'brightness': self._config.get("display", "brightness")})	
		
	def set_brightness(self):
		if not request.json or not 'brightness' in request.json:
			self.wrong_request()
		brightness = int(request.json['brightness'])
		self._config.set("display", "brightness", brightness)
		return jsonify({'result': True})
		
	# set, get timeout
	def get_timeout(self):
		return jsonify({'timeout': self._config.get("timeout", "timeout")})	
		
	def set_timeout(self):
		if not request.json or not 'timeout' in request.json:
			self.wrong_request()
		timeout = int(request.json['timeout'])
		self._config.get("timeout", "timeout", timeout)
		return jsonify({'result': True})

# only for test
if __name__ == '__main__':
	nw_api = NetworkAPI(None)
	nw_api.start()
	
	import time
	starttime=time.time()
	while True:
		print "tick"
		time.sleep(60.0 - ((time.time() - starttime) % 60.0))
		
	