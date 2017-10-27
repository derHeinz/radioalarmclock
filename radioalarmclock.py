#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import logging
import json
import socket
from logging.handlers import RotatingFileHandler
from daemonify import Daemon

from alarmclock.dimmer import Dimmer
from alarmclock.sounds import Sounds
from alarmclock.controller import Controller
from alarmclock.alarm import Alarm
from alarmclock.configuration.configurator import Configurator
from alarmclock.configuration.configuration_reader import ConfigurationReader
from alarmclock.configuration.network_api import NetworkAPI
from alarmclock.timeout import Timeout
from apscheduler.triggers.cron import CronTrigger


from apscheduler.schedulers.blocking import BlockingScheduler


class LedClockDaemon(Daemon):
	def __init__(self, args):
		super(LedClockDaemon, self).__init__(pidfile=args["pidfile"])
		self._args = args

	def setup_logging(self):
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

		handler = RotatingFileHandler(self._args['logfile'], maxBytes=153600, backupCount=3)
		handler.setFormatter(formatter)

		root_logger = logging.getLogger()
		root_logger.setLevel(logging.DEBUG)
		root_logger.addHandler(handler)

	def _connect_internet(self):
		logging.info("connecting internet")
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		s.close()
		
	def run(self):
		self.setup_logging()
		
		# configuration
		config = Configurator()
		network_api = NetworkAPI(config)

		scheduler = BlockingScheduler()
		sounds = Sounds()
		config.register_component(sounds, "sounds")
		
		# trigger a connect to I-net
		trig = CronTrigger(minute="*/15")
		scheduler.add_job(id="internet-call", func=self._connect_internet, trigger=trig)
		
		
		# Player
		try:
			# use this for windows
			from alarmclock.player.player_win import PlayerWin as Player 
		except ImportError:
			# use this for linux
			from alarmclock.player.player_linux import PlayerLinux as Player
		player = Player(scheduler)
		config.register_component(player, "player")
		
		# Display
		try:
			from alarmclock.display.max7219_display import Max7219Display
			display = Max7219Display(None)
		except ImportError:
			logging.info("Cannot import Max display, switching to console display.")
			from alarmclock.display.console_display import ConsoleDisplay
			display = ConsoleDisplay(None)
		config.register_component(display, "display")
		
		# Alarm
		alarm = Alarm(scheduler, display)
		config.register_component(alarm, "alarm")
		
		# Timeout
		timeout = Timeout(None, None)
		config.register_component(timeout, "timeout")
		
		# Dimmer
		dimmer = Dimmer(scheduler, display)
		config.register_component(dimmer, "dimmer")
		
		# load configuration from config file
		with open('config.json') as data_file:    
			data = json.load(data_file)
			cr = ConfigurationReader(config, data)
			cr.config_components()
		
		controller = Controller(display, alarm, sounds, player, timeout, scheduler)
		
		# dependently load input
		try:
			from alarmclock.inputs.rotary_knob_input import RotaryKnobInput
			input = RotaryKnobInput(controller)
		except ImportError:
			logging.info("Cannot import rotary knob, switching to keyboard.")
			from alarmclock.inputs.keyboard_input import KeyboardInput
			input = KeyboardInput(controller)
			
		# dependently load nearby sensor
		try:
			from alarmclock.inputs.ir_distance_input import IRDistanceInput
			distance_input = IRDistanceInput(controller)
		except ImportError:
			logging.info("Cannot import distance_input leaving that out.")
		
		display.start()
		network_api.start()
		timeout.start()
		scheduler.start() # blocking scheduler than this blocks!		


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pidfile", help="PID file name", type=str, default="/var/run/ledclock.pid")
    parser.add_argument("-l", "--logfile", help="Log file name", type=str, default="/var/log/ledclock.log")
    parser.add_argument("-d", "--daemon", help="start stop restart", type=str)

    return vars(parser.parse_args())


# Main function
if __name__ == "__main__":
    # Process command line arguments
    args = process_args()

    # Verify running as root.  Unfortunately, this is required to access /dev/mem by the rgbmatrix lib
    #if os.getuid() != 0:
    #    print "Must run as root!"
    #    sys.exit(-1)

    daemon = LedClockDaemon(args)

    if args['daemon'] is None:
        try:
            print("Starting RadioalarmClock\nPress CTRL-C to exit")
            daemon.run()
        except KeyboardInterrupt:
            print "Exiting\n"
            sys.exit(0)
    elif args['daemon'] == 'start':
        daemon.start()
    elif args['daemon'] == 'stop':
        daemon.stop()
    elif args['daemon'] == 'restart':
        daemon.restart()
    else:
		print "Invalid daemon action"
