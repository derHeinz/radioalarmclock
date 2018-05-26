# Alarm clock. #
Alarm clock using a raspberrypi, rotary knob switch and max7219 display. This way one can be alarmed by an audio stream or his/her favorite song.
![picture](https://user-images.githubusercontent.com/5774591/27263071-374e7136-5463-11e7-8708-2a9dcbfae9c8.jpg)
![picture](https://user-images.githubusercontent.com/5774591/27263072-37634200-5463-11e7-9252-192b698a5c82.jpg)


## Features ##
- Time
  - show current time (get from system time)
  - Automatically switch and show time after timeout (use as alarm clock)
  - Change this timeout
- Display
  - display menu or time, or functions
  - display max7219 displays like this: http://www.ebay.com/itm/Dot-Matrix-Modul-4x-8x8-3mm-MAXIM-MAX7219-Arduino-STM32-473-/322337412484
  - editing brightness of max7219 displays, for use in light or darker rooms
  - display to TKinter (for testing)
  - display on console (for testing)
- Dimmer
  - set brightness based day / night
  - calculate day night by astronomical means of sunrise and sunset
- Alarm 
  - on / off set and show current alarm time, so you can use it as an alarm clock
  - 2 different alarms available
- Audio
  - play audio files and streams
  - support mplayer for linux, pyaudio, and winsound for windows
  - configurable audio for alarm
  - configurable fade-in for alarm
  - backup to local audio file in case of unavailable stream
  - change master Volume
- Input
  - use rotary knob like this one: https://www.amazon.de/gp/product/B011BHAQZE
  - use keyboard input (e.g. for debugging and testing)
  - use IR detector (TCRT5000) to contactless deactivate running alarm (like: http://www.ebay.de/itm/TCRT5000-IR-Infrarot-Infrared-Lichtschranke-Sensor-Modul-Arduino-Raspberry-Pi-/112288305305?hash=item1a24e79099)
- Network JSON API
  - get/set all important settings
- Weather
  - Using pyowm https://github.com/csparpa/pyowm
  - get weather forecast and present on display
- Exit application


## References ##
Inspired by: https://github.com/jeffkub/led-wall-clock
Further ideas: https://github.com/caternuson/rpi-weather

## Needed python libraries (install with pip install) ##
- daemonify (daemon process)
- ephem (astronomical calculation - for dimming)
- apscheduler (scheduleing)
- max7219 (for the led display)
- Flask (for the json remote API)
- pyowm https://github.com/csparpa/pyowm for weather forecast

## Optional python libraries (nice for development without real hardware) ##
- reachar (for keyboard controller) instead of rotary knob
- tkinter (for windows/linux) replaces led display

## Menu ##
The application provides a simple menu to interface with the different features. 
The menu is operated using some keys or the the rotary switch and displays to the console or the MAX7219 display.
There are three operations (left, right and select). By turning the rotary to the left and right one selects the menu options. Pushing the rotary switch selects the current menu item.
Menu items may be items that allow to change a value or may be sub menus. Changeing a value ends in immmediately editing this value. To exit the value change push the select button.
Sub menu items are identified by a '>' at the end, push select on a sub menu item to get to the submenu. To get back to the menu from a submenu select the back itm identified by '<'.

## Network API ##
The network API uses Flask http://flask.pocoo.org/ to provide a JSON API. 

The API is bound to port 5000 on all network interfaces. Following methods are currently available.

|Path|HTTP Method|Description|
|---|---|---|
|/v1.0/alarmtime_1|GET/POST|Get and set alarm time for alarm 1.|
|/v1.0/alarm_1|GET/POST|Get and set the alarm 1 (active, inactive).|
|/v1.0/alarmtime_2|GET/POST|Get and set alarm time for alarm 2.|
|/v1.0/alarm_2|GET/POST|Get and set the alarm 2 (active, inactive).|
|/v1.0/fadein|GET/POST|Whether to use fade-in for audio files or not.|
|/v1.0/volume|GET/POST|Get and set the master volume.|
|/v1.0/play|GET/POST|Play or stop playing.|
|/v1.0/sounds|GET|Get currently configured sounds (Streams, MP3s, etc).|
|/v1.0/sound|PUT|Add another sound (Stream, MP3, etc).|
|/v1.0/brightness|GET/POST|Get and set the current brightness of the display.|
|/v1.0/timeout|GET/POST|Get and set the timeout (after which period of inactivity to switch from menu to show time).|
|/v1.0/dimmer_active|GET/POST|Use auto dimming (switch brightness of display between night and daytime).|
|/v1.0/night_percentage|GET/POST|Set brightness during night, in percentage of max.|
|/v1.0/day_percentage|GET/POST|Set brightness during day, in percentage of max.|

## Hardware ##
- Rotary Switch Layout

This describes the connections between the rotary switch and the pins of a raspberrypi.

|Rotary Switch|Raspberrypi|
|---|---|
|GND|GND/Pin9|
|VCC|3.3V/Pin1|
|SW|GPIO22/Pin15|
|Data|GPIO27/Pin13|
|CLK|GPIO17/Pin11|

- Max7219 Display Layout

This describes the connection between the MAX7219 https://pypi.python.org/pypi/max7219 and the pins of a raspberrypi.
You need to activate SPI in raspi-config/Interface options in order to use it.

|4x Max7219|Raspberrypi|
|---|---|
|GND|GND/Pin14|
|VCC|3.3V/Pin17|
|DIN|GPIO10/Pin19|
|CS|GPIO8/SPI C0/Pin24|
|CLK|GPIO11/SPI CLK/Pin23|

- TCRT5000 IR Detector

This describes the connection between the TCRT5000 IR Detector and the raspberrypi.

|TCRT5000|Raspberrypi|
|---|---|
|GND|GND/Pin39|
|VCC|3.3V/Pin1|
|D0|not connected|
|A0|GPIO23/Pin16|