from ledMain import LedMain
import random as r

# create a constant null color Black/No Color for any time we need no color
NULL_COLOR = (0, 0, 0)

WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

PINK = (255, 0, 200)

GOOD_COLORS = [PINK, CYAN, MAGENTA, YELLOW, BLUE]

VOID_COLORS = [(29, 17, 53), (12, 22, 79), (186, 30, 104), (86, 67, 253), (118, 73, 254), (252, 251, 254)]
STAR_COLORS = [WHITE, (248, 225, 108), (108, 99, 255), YELLOW]


class BasePattern():
    """
    Description
    ----------
    This is the BasePattern class that simply defines the basic API
    
    Paramaters
    ----------
    led_strip : LedMain
        The led controller instance
    color : tuple[int, int, int], optional
        RGB color value. Defaults to (0, 0, 255) Blue
    """
    def __init__(self, led_strip=LedMain(50), color=(0, 0, 255)):
        self.led_strip = led_strip
        self.color = color
        self.instances = []

    def tryTriggerInstance(self, current_key_presses):
        """
        Attempts to trigger an instance of the pattern based on the given input.
        If it is successful the Pattern should add an instance to its respective datastructure then using update properly animate it.
        """
        pass

    def update(self):
        """
        This function updates the displayed pattern on the back end.
        This should be run every frame in order to properly animate the display.
        """
        pass

    def display(self):
        """
        Simply displays how the pattern would appear on the LEDs in the current frame.
        """
        self.led_strip.displaySimulation()

class baseOctavePattern(BasePattern):
    """
    Inherits from :class:`BasePattern`.

    This class Extends the BasePattern to add a method that detects If an octave is played when given a list of notes
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def isOctaveInNoteSet(self, key_presses):
        """
        Args:
            key_presses (list[note objects]) : The list of key presses you want to compare
        
        Returns:
            list[int] : the list of notes that had a note played an octave away
                (This should never return a list with one item in it)
        """
        notes = [msg.note for msg in key_presses]

        octaves = []

        for note in notes:
            if note + 12 in notes or note - 12 in notes:
                octaves.append(note)
        return octaves

class RipplePattern(BasePattern):
    def __init__(self, fade=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade = fade

    def tryTriggerInstance(self, current_key_presses):
        for key in current_key_presses:
            self.instances.extend(((key.note, 1), (key.note, 0)))
            self.led_strip.setPixel(key.note, self.color)


    def update(self):

        new_instances = []

        for instance in self.instances:

            led = instance[0]
            direction = instance[1]

            self.led_strip.setPixel(led, NULL_COLOR)

            if direction == 0:
                led += 1
            else:
                led -= 1
            
            if self.led_strip.setPixel(led, self.color):
                new_instances.append((led, direction))
        self.instances = new_instances

class SimpleOctaveRipple(baseOctavePattern):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = GOOD_COLORS

    def tryTriggerInstance(self, current_key_presses):
        for note in self.isOctaveInNoteSet(current_key_presses):

            # TODO: Change the color here in some way. Either modifiable or just keep random
            color = r.choice(self.colors)

            self.instances.append((0, color))
    
    def update(self):
        new_instances = []
        for instance in self.instances:

            self.led_strip.setPixel(instance[0], NULL_COLOR)
            new_instance = (instance[0] + 1, instance[1])

            if self.led_strip.setPixel(instance[0] + 1, instance[1]):
                new_instances.append(new_instance)
        
        self.instances = new_instances

class LEDFade(BasePattern):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colors = GOOD_COLORS

    def tryTriggerInstance(self, current_key_presses):
        """
        Description
        -----------
        For each key that is pressed we set some random LED to a random color choice listed above
        The color of the LED dims slowly until there is no color left in which the instance is removed.
        The dimming process is resolved in update.
        """
        for key in current_key_presses:

            which_led = r.randint(0, self.led_strip.num_leds - 1)
            which_color = r.choice(self.colors)
            decay = max(0.90, 0.98 - (key.velocity / 1270))

            self.instances.append((which_led, which_color, decay))


            self.led_strip.setPixel(which_led, which_color)
    
    def update(self):
        """
        Description
        -----------
        Dims each instance by some factor based on the stored velocity. IE. press the key harder the led will last longer.
        """
        new_instances = []
        for led, color, decay in self.instances:
            
            color = [c * decay for c in color]

            if any (c > 30 for c in color):
                new_instances.append([led, color, decay])
                self.led_strip.setPixel(led, tuple(map(int, color)))
            else:
                self.led_strip.setPixel(led, NULL_COLOR)
        
        self.instances = new_instances

class octaveFlash(baseOctavePattern):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_curve = [0.6, 0.7, 0.8, 0.9, 1, 0.9, 0.8, 0.7, 0.6]

    def tryTriggerInstance(self, current_key_presses):
        if self.isOctaveInNoteSet(current_key_presses):
            self.instances.append((-1, r.choice(VOID_COLORS)))
        
        notes = [msg.note for msg in current_key_presses]
        for note in notes:
            self.instances.append((round((note - 21) * (300/88)), r.choice(STAR_COLORS)))

    def update(self):
        new_instances = []
        for led, color in self.instances:
            color = [c * 0.95 for c in color]

            if led == -1: # if octave set all lights
                if any (c > 30 for c in color):
                    new_instances.append([led, color])

                    for i in range(300):
                        self.led_strip.setPixel(i, color)
                
                else:
                    for i in range(300):
                        self.led_strip.setPixel(i, NULL_COLOR)

            else: # if specific note then set just a couple leds
                if any (c > 30 for c in color):
                    new_instances.append([led, color])

                    for i in range(9):
                        temp_color = [c * (self.fade_curve[i]) for c in color]

                        self.led_strip.setPixel(led + i - 4, (temp_color[0], temp_color[1], temp_color[2]))

                else:
                    for i in range(9):
                        self.led_strip.setPixel(led + i - 4, NULL_COLOR)
        
        self.led_strip.setPixel(1, WHITE)
        
        self.instances = new_instances

class rippleOnNote(BasePattern):
    def __init__(self, led_strip=LedMain(50), color=(0, 0, 255)):
        super().__init__(led_strip, color)

    def _isOctaveInNoteSet(self, current_key_presses):
        octaves = []
        for note in current_key_presses:
            if note.velocity < 80: pass
            else:
                for note2 in current_key_presses:
                    if note2.velocity < 80: pass
                    else:
                        if note.note - 12 == note2.note or note.note + 12 == note2.note:
                            octaves.append(note)
                            octaves.append(note2)
            
        return octaves

    def tryTriggerInstance(self, current_key_presses):
        # 0-127 velocity scale
        notes = [msg.note for msg in current_key_presses]
        for note in current_key_presses:
            chosen_color = r.choice(GOOD_COLORS)
            self.instances.append((round((note.note - 21) * (300/88)), chosen_color, round(note.velocity / 5), 0))
            self.instances.append((round((note.note - 21) * (300/88)), chosen_color, round(note.velocity / 5), 1))

        octaves = self._isOctaveInNoteSet(current_key_presses)
        for note in octaves:
            chosen_color = r.choice(GOOD_COLORS)
            self.instances.append((round((note.note - 21) * (300/88)), chosen_color, 0, 2, 0))
            self.instances.append((round((note.note - 21) * (300/88)), chosen_color, 1, 2, 0))

    def update(self):
        
        self.led_strip.clear() # clear the backend leds

        new_instances = []
        for instance in self.instances:
            if instance[3] == 2: # if it is an octave
                if instance[4] >= 250: # if it has existed for longer than 250 frames don't add or do anything with it
                    pass
                else:
                    new_instances.append((instance[0] - 1 if instance[2] else instance[0] + 1, instance[1], instance[2], instance[3], instance[4] + 1))
                    for i in range(7):
                        self.led_strip.setPixel(instance[0] - i if instance[2] else instance[0] + i, instance[1])

            elif instance[2] <= 0: # don't add to new instances if velocity is expired
                pass

            else:
                # move direction based on instance[3]
                new_instances.append((instance[0] - 1 if instance[3] == 1 else instance[0] + 1, instance[1], instance[2] - 1, instance[3]))
                self.led_strip.setPixel(instance[0], instance[1])
                self.led_strip.setPixel(instance[0] - 1 if instance[3] else instance[0] + 1, instance[1])
        