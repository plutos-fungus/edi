import curses
# TODO: deleting past the current line
def delete(pad, pad_y, pad_x, stdscr, cursory, cursorx, screenx): # Doesn't work with the default GNOME terminal
	if cursorx > 0: # preventing crash
		if screenx == 0:
			if pad_x > 1:
				pad_x -= 2
				pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
			elif pad_x > 0:
				pad_x -= 1
				pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
		pad.delch(cursory, cursorx - 1) # Delete the character that is one to the

def back_delete(pad, cursory, cursorx):
	pad.delch(cursory, cursorx) # Delete the character to the righ. This also
	# moves the other characters on that line one closer to the cursor

def left(pad, pad_y, pad_x, stdscr, cursory, cursorx, screenx):
	if cursorx > 0:
		if screenx == 0:
			if pad_x > 0:
				pad_x -= 1
				pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
		newx = cursorx - 1
		pad.move(cursory, newx)

def right(pad, pad_y, pad_x, stdscr, cursory, cursorx, screenx):
	if screenx == stdscr.getmaxyx()[1] - 1:
		pad_x += 1
	if cursorx == pad.getmaxyx()[1] - 1:
		pad.resize(pad.getmaxyx()[0], pad.getmaxyx()[1] + 1)
	newx = cursorx + 1
	pad.move(cursory, newx)
	pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)

def up(pad, pad_y, pad_x, stdscr, cursory, cursorx, screeny):
	if cursory != 0:
		if screeny == 0:
			if pad_y != 0:
				pad_y -= 1
				pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
		newy = cursory - 1
		pad.move(newy, cursorx)

def down(pad, pad_y, pad_x, stdscr, cursory, cursorx, screeny):
	if screeny == stdscr.getmaxyx()[0] - 1:
		pad_y += 1
	if cursory == pad.getmaxyx()[0] - 1:
		pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
	newy = cursory + 1
	pad.move(newy, cursorx)
	pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)

def enter(pad, pad_y, pad_x, stdscr, cursory, screeny, eol):
	pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
	pad.clrtoeol()
	if screeny == stdscr.getmaxyx()[0] - 1:
		pad_y += 1
		pad.refresh(pad_y, pad_x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
	pad.move(cursory + 1, 0)
	pad.insertln()
	pad.insstr(eol)

def syntaxHighlight(pad, cursory, cursorx, operators): 
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	currline = pad.instr(cursory, 0).decode("utf-8") # Get contents of current line 
	eol = len(currline)
	pad.move(cursory, 0)
	pad.addstr(currline)
	for o in operators:
		oposes = []
		for x in range(eol):
			foundx = currline.find(o, x, eol)
			if foundx != -1: 
				oposes.append(foundx)
			else: 
				break
		if len(oposes) != 0:
			for xpos in oposes:
				pad.move(cursory, xpos)
				pad.addstr(o, curses.color_pair(2))
	pad.move(cursory, cursorx)

def fileSyntax(pad, operators):
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	for y in range(pad.getmaxyx()[0] - 1):
		currline = pad.instr(y, 0).decode("utf-8")
		eol = len(currline)
		for o in operators:
			oposes = []
			for x in range(eol):
				foundx = currline.find(o, x, eol)
				if foundx != -1: 
					oposes.append(foundx)
				else:
					break
			if len(oposes) != 0:
				for xpos in oposes:
					pad.move(y, xpos)
					pad.addstr(o, curses.color_pair(2))
		pad.move(0, 0)


	# orposes = []
	# for x in range(eol):
	# 	foundx = currline.find(" or ", x, eol)
	# 	if foundx != -1:
	# 		orposes.append(foundx)
	# 	else:
	# 		break
	# pad.move(cursory, 0)
	# pad.addstr(currline)	
	# if len(orposes) != 0:
	# 	for xpos in orposes:
	# 		pad.move(cursory, xpos)
	# 		pad.addstr(" or ", curses.color_pair(2))
	# pad.move(cursory, cursorx)






