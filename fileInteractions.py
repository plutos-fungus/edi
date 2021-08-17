import os 
import curses
import re

def loadfile(pad, pad_y, pad_x, args):
	filename = ""
	files = os.listdir()
	if len(args) > 2: 
		exit("Error: Too many arguments")
	elif len(args) == 2:
		filename = args[1]
		if filename in files:
			f = open(filename)
			contents = f.readlines()
			f.close()
			maxlen = 0
			for i in contents:
				if len(i) > pad.getmaxyx()[1] - 1: # x handling
					if len(i) > maxlen:
						maxlen = len(i)
						pad.resize(pad.getmaxyx()[0], maxlen)
				if curses.getsyx()[0] == curses.LINES - 1: #y handling
					pad_y += 1
					pad.resize(pad.getmaxyx()[0] + pad_y, pad.getmaxyx()[1])
				pad.addstr(i)
				pad.refresh(pad_y, pad_x, 0, 0, curses.LINES - 1, curses.COLS - 1)
			pad_y = 0
			pad.refresh(pad_y, pad_x, 0, 0, curses.LINES - 1, curses.COLS - 1)
			pad.move(0, 0)
		else:
			create = open(filename, "w")
			create.close()             
	return filename 

def save_close(pad, pad_y, pad_x, filename):
	contents = []
	for y in range (pad.getmaxyx()[0]):
		contents.append(pad.instr(y,0).decode("utf-8"))
			# instr doesn't really work for more than one line and is quite impractical
	pad.clear()
	pad.refresh(pad_y, pad_x, 0, 0, curses.LINES - 1, curses.COLS - 1)
	curses.endwin()

	if filename == "": # Ask about the name of the file if the file isn't one that has been opened
		nameFound = False
		while not nameFound:
			tempfilename = input("Which file name/path do you want? ")
			validAnswer = False
			while not validAnswer:
				answer = input("Are you sure? (y/n) ")
				if answer == "y" or answer == "Y":
					filename = tempfilename
					nameFound = True
					validAnswer = True
				elif answer == "n" or answer == "N":
					print("Enter another name")
					validAnswer = True
				else:
					print("Invalid answer. Try again")

	create = open(filename, "w")
	create.close()
	save = open(filename, "a")

	index = 0 # Marks the index after the last index that holds a non-blank string
	curindex = 0
	for s in contents: # Find EOF by finding last non-blank string
		if not re.search("^\s*$", s): # If the string isn't only white space
			# Update index so it becomes the index after the non-empty string
			index = curindex + 1
		curindex += 1 # Update current index for next iteration

	for x in range(index, len(contents)):
		del contents[index] # Remove all the strings after EOF

	for s in contents:
		noTrailingWhitespace = re.sub("\s*$", "", s)
		s = noTrailingWhitespace + "\n"
		save.write(s)

	save.close()
	exit()