import board
import neopixel
import mido
import time

from ledPatterns import octaveFlash, rippleOnNote
from ledMain import LedMain

# ----- 1. Setup LED strip -----
NUM_LEDS = 300
LED_PIN = board.D18

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=1.0,
    auto_write=False
)

# ----- 2. Setup your LED controller -----
led_ctrl = rippleOnNote(led_strip=LedMain(300))

# ----- 3. Setup MIDI input -----
midi_input_name = 'Clavinova MIDI 1'

connected_midi = False
while not connected_midi:
    try:
        midi_port = mido.open_input(midi_input_name)
        connected_midi = True
    
    except:
        connected_midi = False
        time.sleep(3) # wait 3 seconds before trying to connect again

# ----- 4. Main loop -----
try:
    while True:
        # --- Handle MIDI messages ---
        notes_this_frame = []
        for msg in midi_port.iter_pending():
            if msg.type == 'note_on':
                notes_this_frame.append(msg)
        led_ctrl.tryTriggerInstance(notes_this_frame)

        # --- Update LEDs ---
        led_ctrl.update()  # your existing update method

        # --- Write to physical strip ---

        pixels[:] = led_ctrl.led_strip.pixels
        pixels.show()

        # --- Optional: small delay to reduce CPU usage ---
        time.sleep(0.001)

except KeyboardInterrupt:
    # Turn off all LEDs on exit
    for i in range(NUM_LEDS):
        pixels[i] = (0, 0, 0)
    pixels.show()
