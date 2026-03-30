# Overview

The project converts MIDI input to LED output. There are several LED patterns in the pattern file. Which output different patterns to the LEDs.

# Usage

Download the 3 files onto a controller device with board, neopixel, and mido libraries installed. The controller must have a pin connected to the the LEDs on the data wire. The following changes must be made to [main](main.py):

 - NUM_LEDS: the number of LEDs on your LED strip (line 10)
 - LED_PIN: the pin on your controller board you are outputting your LED data (line 11)
 - led_ctrl: select a pattern class and pass in led_strip=LedMain(NUM_LEDS) to the pattern class (line 21)
 - midi_input_name: change this to the name of your midi input device name. You may want to just look your's up (line 24)

After the appropriate changes have been made run main.py on the device while everything is powered. When an input is received by your controller it should light up.

## Example
[Youtube Demonstration Video](https://youtu.be/0IN3lGUjR1I)
