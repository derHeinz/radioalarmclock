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
		self.app.add_url_rule(rule="/v1.0/fadein", endpoint="get_fadein", view_func=self.get_fadein, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/fadein", endpoint="set_fadein", view_func=self.set_fadein, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/fadeinsteps", endpoint="get_fadeinsteps", view_func=self.get_fadeinsteps, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/fadeinsteps", endpoint="set_fadeinsteps", view_func=self.set_fadeinsteps, methods=['POST'])
		self.app.add_url_rule(rule="/v1.0/fadeinstepsize", endpoint="get_fadeinstepsize", view_func=self.get_fadeinstepsize, methods=['GET'])
		self.app.add_url_rule(rule="/v1.0/fadeinstepsize", endpoint="set_fadeinstepsize", view_func=self.set_fadeinstepsize, methods=['POST'])

		
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

	# alarmtime set, get
	def get_alarmtime(self):
		return self._get_simple("alarm", "alarmtime")
		
	def set_alarmtime(self):
		return self._set_simple("alarm", "alarmtime")
		
	# alarm set, get
	def get_alarm(self):
		return self._get_simple("alarm", "alarm")
		
	def set_alarm(self):
		return self._set_simple_bool("alarm", "alarm")
		
	# volume set, get
	def get_volume(self):
		return self._get_simple("player", "volume")
	
	def set_volume(self):
		return self._set_simple("player", "volume")
		
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
		
	# brightness set, get
	def get_brightness(self):
		return self._get_simple("display", "brightness")
		
	def set_brightness(self):
		return self._set_simple("display", "brightness")
		
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
		
	