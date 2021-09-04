import yaml
from yaml.loader import SafeLoader

class Pad:
	posy = 0
	posx = 0

class Cursor: 
	sy = 0
	sx = 0
	py = 0
	px = 0

class Themecolors:
	red = 0
	orange = 0
	green = 0
	yellow = 0
	purple = 0
	cyan = 0
	magenta = 0
	white = 0
	black = 0

	foreground = 0
	background = 0
	def getcolors(themes_files, theme):
		if i is not None:
			with open(themes_files + i, 'r') as themes:
				themes = yaml.load(themes, Loader=SafeLoader)
				this.red = themes['red']
				this.orange = themes['orange']
				this.green = themes['green']
				this.yellow = themes['yellow']
				this.purple = themes['purple']
				this.cyan = themes['cyan']
				this.magenta = themes['magenta']
				this,white = themes['white']
				themes.black = themes['black']
				themes.foreground = themes['foreground']
				themes.background = themes['background']
