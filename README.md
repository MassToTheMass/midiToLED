# MIDI-to-LED Visualizer

[▶ Watch Demo](https://youtu.be/0IN3lGUjR1I)

## Overview
This project converts live MIDI input into real-time LED output using a variety of visual patterns.

Different LED behaviors are implemented as pattern classes, allowing MIDI attributes such as pitch and velocity to drive dynamic lighting effects.

---

## Requirements
- Python
- Libraries:
  - board
  - neopixel
  - mido
- A controller device (e.g., Raspberry Pi)
- Addressable LED strip (e.g., WS2812 / NeoPixel)

---

## Setup

1. Clone the repository onto your controller device:
   ```bash
   git clone https://github.com/MassToTheMass/midiToLED
