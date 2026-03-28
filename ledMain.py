import time

class LedMain():
    def __init__(self, num_leds):
        self.num_leds = num_leds

        # creates a list of vectors representing the r, g, b values of the leds
        self.pixels = [(0, 0, 0)] * num_leds

    def setPixel(self, i, color):
        """
        Description
        -----------
        This function sets the internal color of the provided led (i) to the provided color

        Args:
            i (int) : which led
            color (tuple[int, int, int]) : which color should be displayed

        Returns:
            bool : True if successful - False if out of bounds
        """
        if self._isInBounds(i):
            self.pixels[i] = (round(color[0]), round(color[1]), round(color[2]))
            return True
        return False

    def clear(self):
        self.pixels = [(0, 0, 0)] * self.num_leds

    def _isInBounds(self, i):
        return 0 <= i < self.num_leds

    def displaySimulation(self):

        text = ""
        for r, g, b in self.pixels:
            if (r, g, b) == (0, 0, 0):
                text += " "
            else:
                text += f"\033[48;2;{r};{g};{b}m \033[0m"
        
        print(f"|{text}|")
