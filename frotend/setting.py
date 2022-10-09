from tkinter import *


class Setting:

    def __init__(self, window, canvas, window_width, window_height, padding):
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.padding = padding
        self.setting_canvas = canvas
        self.setting_canvas.config(highlightthickness=2)
