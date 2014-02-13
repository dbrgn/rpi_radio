# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from lcd import Lcd


class BitmapLcd(Lcd):
    def __init__(self, filename):
        self.im = Image.new("RGB", (128, 64))
        self.ctx = ImageDraw.Draw(self.im)
        self.filename = filename

    def draw_text(self, x, y, string):
        #self.ctx.text((x, y), string, font=font)
        print "[BitmapLCD]: " + string

    def draw_line(self, x_start, y_start, x_dest, y_dest):
        self.ctx.line(x_start, y_start, x_dest, y_dest)

    def flip(self):
        self.im.save(self.filename)