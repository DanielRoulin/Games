import os
from huscii.utilities import *
from PIL import Image, ImageOps


# Make a numpy array with a rectangle in the middle
# data = np.zeros((32, 32), np.uint32)
# data[8:32-8, 8:32-8] = 1
class HUSCIIRenderer:
    def __init__(self, width=80, height=25):
        """The one and only HUSCII renderer"""

        self.WIDTH = width
        self.HEIGHT = height
        self.CHARS = ' .:-=+*#%@'

        self.fill_char = self.CHARS[-1]
        self.bg_char = self.CHARS[1]

        self.reset_translate()

        self.chars = [[self.bg_char] * self.WIDTH for i in range(self.HEIGHT)]

    @round_inputs
    def point(self, x, y, char):
        """Sets the point x, y to the character char."""

        x += self.x_offset
        y += self.y_offset

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

        # self.clear()
        print(screen)

        self.chars = [[self.bg_char] * self.WIDTH for i in range(self.HEIGHT)]
        self.reset_translate()

    @round_inputs
    def rect(self, x, y, w, h):
        """Draws a rectangle whose top left corner is at <x, y> and of width w and height h."""
        for i in range(h):
            for j in range(w):
                self.point(x + j, y + i, self.fill_char)

    @round_inputs
    def ellipse(self, x, y, w, h=None):
        """
        Draws an ellipse of center <x; y> and of width h and height h.
        If no height is specified, draws a circle of diameter w.
        """
        if not h:
            h = w/2
        for i in range(-h, h + 1):
            for j in range(-w, w + 1):
                if j*j * h*h + i*i * w*w <= h*h * w*w:
                    self.point(x + j, y + i, self.fill_char)

    @round_inputs
    def text(self, x, y, string):
        """Write the text "string" at the x, y location on the screen."""
        w = len(string)
        for i in range(w):
            self.point(x + i, y, string[i])
    
    @round_inputs
    def line(self, x1, y1, x2, y2):
        length = max(abs(x1 - x2), abs(y1 - y2))
        for i in range(length):
            p = i/length
            x = lerp(x1, x2, p)
            y = lerp(y1, y2, p)
            self.point(x, y, self.fill_char)

    @round_inputs
    def translate(self, x, y):
        """
        Offsets all subsequent drawing operations by the specified amount.
        Note that translations are cumulative: translate(10, 10) + translate(15, 15) = translate(25, 25)
        """
        self.x_offset += x
        self.y_offset += y

    def reset_translate(self):
        """Resets the current translation to zero."""
        self.x_offset = 0
        self.y_offset = 0

    def sprite(self, path):
        """Returns a sprite object, which can be drawn by calling .draw() on it."""
        return self._Sprite(self, path)

    class _Sprite():
        def __init__(self, renderer, path):
            self.r = renderer
            self.img = Image.open(path)
            self.default_width, self.default_height = self.img.size
            self.chars_width, self.chars_height = 0, 0

        def generate_chars(self, width, height):
            self.chars_width = width
            self.chars_height = height

            temp_img = self.img.resize((width, height))
            temp_img = ImageOps.grayscale(temp_img)
            img_pixels = temp_img.load()

            self.chars = [[""] * width for i in range(height)]
            for y in range(height):
                for x in range(width):
                    len_chars = len(self.r.CHARS)
                    color = min(
                        int(img_pixels[x, y]/255 * len_chars), len_chars - 1)
                    char = self.r.CHARS[color]
                    self.chars[y][x] = char
        
        @round_inputs
        def draw(self, x, y, w=None, h=None):
            """Draws the sprite to the screen."""
            if not w:
                w = self.default_width
            if not h:
                h = self.default_height

            if not self.chars_width == w or not self.chars_height == h:
                self.generate_chars(w, h)

            for i in range(h):
                for j in range(w):
                    self.r.point(x + j, y + i, self.chars[i][j])