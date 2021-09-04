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
	red = 0
	green = 0
	yellow = 0
	cyan = 0
	magenta = 0
	white = 0
	black = 0
	blue = 0

	def __init__(self, themes_files, theme):
		for i in theme:
			if i is not None: 
				with open(themes_files + i, 'r') as themes:
					themes = yaml.load(themes, Loader=SafeLoader)
					self.red = themes['red'][0]
					self.green = themes['green'][0]
					self.yellow = themes['yellow'][0]
					self.cyan = themes['cyan'][0]
					self.magenta = themes['magenta'][0]
					self.white = themes['white'][0]
					self.black = themes['black'][0]
					self.blue = themes['blue'][0]
	
	def parseColors(self):
		m = interp1d([0,255],[0,1000])
		black_rgb = [int(m(int(str(self.black[0:2]), 16))), int(m(int(str(self.black[2:4]), 16))), int(m(int(str(self.black[4:6]), 16)))]
		red_rgb = [int(m(int(str(self.red[0:2]), 16))), int(m(int(str(self.red[2:4]), 16))), int(m(int(str(self.red[4:6]), 16)))]
		green_rgb = [int(m(int(str(self.green[0:2]), 16))), int(m(int(str(self.green[2:4]), 16))), int(m(int(str(self.green[4:6]), 16)))]
		yellow_rgb = [int(m(int(str(self.yellow[0:2]), 16))), int(m(int(str(self.yellow[2:4]), 16))), int(m(int(str(self.yellow[4:6]), 16)))]
		blue_rgb = [int(m(int(str(self.blue[0:2]), 16))), int(m(int(str(self.blue[2:4]), 16))), int(m(int(str(self.blue[4:6]), 16)))]
		magenta_rgb = [int(m(int(str(self.magenta[0:2]), 16))), int(m(int(str(self.magenta[2:4]), 16))), int(m(int(str(self.magenta[4:6]), 16)))]
		cyan_rgb = [int(m(int(str(self.cyan[0:2]), 16))), int(m(int(str(self.cyan[2:4]), 16))), int(m(int(str(self.cyan[4:6]), 16)))]
		white_rgb = [int(m(int(str(self.white[0:2]), 16))), int(m(int(str(self.white[2:4]), 16))), int(m(int(str(self.white[4:6]), 16)))]
		# red_rgb = [int(m(int(self.red[0:1], 16))), int(m(int(self.red[2:3], 16))), int(m(int(self.red[4:5], 16)))]
		# green_rgb = [int(m(int(self.green[0:1], 16))), int(m(int(self.green[2:3], 16))), int(m(int(self.green[4:5], 16)))]
		# yellow_rgb = [int(m(int(self.yellow[0:1], 16))), int(m(int(self.yellow[2:3], 16))), int(m(int(self.yellow[4:5], 16)))]
		# blue_rgb = [int(m(int(self.blue[0:1], 16))), int(m(int(self.blue[2:3], 16))), int(m(int(self.blue[4:5], 16)))]
		# cyan_rgb = [int(m(int(self.cyan[0:1], 16))), int(m(int(self.cyan[2:3], 16))), int(m(int(self.cyan[4:5], 16)))]
		# magenta_rgb = [int(m(int(self.magenta[0:1], 16))), int(m(int(self.magenta[2:3], 16))), int(m(int(self.magenta[4:5], 16)))]
		# white_rgb = [int(m(int(self.white[0:1], 16))), int(m(int(self.white[2:3], 16))), int(m(int(self.white[4:5], 16)))]

		colors_list = [black_rgb, red_rgb, green_rgb, yellow_rgb, blue_rgb, magenta_rgb, cyan_rgb, white_rgb]
		return colors_list