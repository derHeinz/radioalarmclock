# Alarm clock. #
Alarm clock using a raspberrypi, rotary knob switch and max7219 display. This way one can be alarmed by an audio stream or his/her favorite song.
![picture](https://user-images.githubusercontent.com/5774591/27263071-374e7136-5463-11e7-8708-2a9dcbfae9c8.jpg)
![picture](https://user-images.githubusercontent.com/5774591/27263072-37634200-5463-11e7-9252-192b698a5c82.jpg)


## Features ##
- Time
-- show and set current time
-- Automatically switch to show time after timeout (use as alarm clock)
-- Change this timeout
- Dsiplay
-- display menu or time
-- display max7219 displays
-- editing brightness of max7219 displays, for use in light or darker rooms
-- display on console
- Alarm 
-- on / off set and show current alarm time, so you can use it as an alarm clock
- Audio
-- play audio files and streams using mplayer
-- configurable audio for alarm 
-- change master Volume
- Input
-- use rotary knob like this one: https://www.amazon.de/gp/product/B011BHAQZE
-- use keyboard input (e.g. for debugging and testing)
- Exit application


## References ##
Inspired by: https://github.com/jeffkub/led-wall-clock

## Needed python libraries (install with pip install) ##
- daemonify (daemon process)
- ephem (astronomical calculation - for dimming)
- reachar (for keyboard controller)
- apscheduler (scheduleing)
- max7219 (for the led display)
- Flask (for the json remote API)

## Menu ##
References:
https://pypi.python.org/pypi/max7219
