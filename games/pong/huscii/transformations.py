import os
from utilities import *
import numpy as np


class HUSCIIRenderer:
    def __init__(self, width=80, height=25):
        """The one and only HUSCII renderer"""

        self.WIDTH = width
        self.HEIGHT = height
        self.CHARS = ' .:-=+*#%@'

        self.fill_char = self.CHARS[-1]
        self.bg_char = self.CHARS[1]

        self.translate_matrix = np.array()

        self.chars = [[self.bg_char] * self.WIDTH for i in range(self.HEIGHT)]

    
    def _apply_transform(x, y):
        return x, y

    def translate(x, y):
        

    @round_inputs
    def point(self, x, y, char):
        """Sets the point x, y to the character char."""
        x, y = self._apply_transform(x, y)
        if (y < self.HEIGHT
            and x < self.WIDTH
            and y >= 0
                and x >= 0):

            self.chars[y][x] = char

    def clear(self):
        """Clears the console."""
        if os.name in ("nt", "dos"):
            os.system("cls")
        else:
            os.system("clear")

    def draw(self):
        """Prints the scene."""
        screen = ""
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                screen += self.chars[y][x]
            screen += "\n"

        self.clear()
        print(screen)
        self.chars = [[self.bg_char] * self.WIDTH for i in range(self.HEIGHT)]

    @round_inputs
    def rect(self, x, y, w, h):
        """Draws a rectangle whose top left corner is at <x, y> and of width w and height h."""
        for i in range(h):
            for j in range(w):
                tx, ty = self._apply_transform(x + j, y + i)
                self.point(tx, ty, self.fill_char)

if __name__=="__main__":
    r = HUSCIIRenderer(40, 20)
    
    r.rect(10, 5, 20, 10)
    r.draw()