import yaml
import curses 
from yaml.loader import SafeLoader
from scipy.interpolate import interp1d

class Pad:
	posy = 0
	posx = 0

class Cursor: 
	sy = 0
	sx = 0
	py = 0
	px = 0

class Themergb:
	color_list = []

	def __init__(self, themes_files, theme):
		for i in theme:
			if i is not None: 
				with open(themes_files + i, 'r') as themes:
					themes = yaml.load(themes, Loader=SafeLoader)
					for c in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']:
						self.color_list.append(themes[c][0])
	
	def parseColors(self):
		m = interp1d([0,255],[0,1000])
		color_rgb = [None] * 8
		for x in range(8):
			color_rgb[x] = [int(m(int(str(self.color_list[x][0:2]), 16))), int(m(int(str(self.color_list[x][2:4]), 16))), int(m(int(str(self.color_list[x][4:6]), 16)))]

		return color_rgb