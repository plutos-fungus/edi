import yaml
import curses 
from yaml.loader import SafeLoader
from scipy.interpolate import interp1d
import os.path
from os import path

class Pad:
	posy = 0
	posx = 0

class Cursor: 
	sy = 0
	sx = 0
	py = 0
	px = 0

class Themergb:
	hasColorTheme = False
	color_list = []

	def __init__(self, theme_file):
		if path.exists(theme_file):
			self.hasColorTheme = True 
			with open(theme_file, 'r') as themes:
				themes = yaml.load(themes, Loader=SafeLoader)
				for c in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']:
					self.color_list.append(themes[c][0])
	
	def parseColors(self):
		if self.hasColorTheme:
			m = interp1d([0,255],[0,1000])
			color_rgb = [None] * 8
			for x in range(8):
				color_rgb[x] = [int(m(int(str(self.color_list[x][0:2]), 16))), int(m(int(str(self.color_list[x][2:4]), 16))), int(m(int(str(self.color_list[x][4:6]), 16)))]

			return color_rgb
		else: 
			return None 
