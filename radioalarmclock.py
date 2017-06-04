#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from daemonify import Daemon

from inputs.keyboard_input import KeyboardInput
from inputs.rotary_knob_input import RotaryKnobInput

from dimmer import Dimmer
from controller import Controller
from alarm import Alarm

# use this for cosole
from display.console_display import ConsoleDisplay
# use this for LED out
from display.max7219_display import Max7219Display

# todo use this for windows
#from player.player_win import Player 
# use this for linux
from player.player import Player

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

	def run(self):
		self.setup_logging()

		scheduler = BlockingScheduler()
		player = Player()
		# configure default sound
		player.set_url('sounds/tada.wav')
		
		dimmer = Dimmer(scheduler)
		alarm = Alarm(scheduler, player.play)
		display = Max7219Display(dimmer)
		#ConsoleDisplay(dimmer)
		
		controller = Controller(display, alarm, player)
		
		input = RotaryKnobInput(controller)
		#KeyboardInput(controller)

		#print("start display")
		display.start()
		#print("start controller")
		#input.start()
		#print("start scheduler")
		scheduler.start()


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
