import curses
import re 
from globalDefinitions import PadPos
# TODO: deleting past the current line
def delete(pad, padposition, stdscr, cursory, cursorx, screenx): # Doesn't work with the default GNOME terminal
	if cursorx > 0: # preventing crash
		if screenx == 0:
			if padposition.x > 1:
				padposition.x -= 2
				pad.refresh(padposition.y, padposition.x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
			elif padposition.x > 0:
				padposition.x -= 1
				pad.refresh(padposition.y, padposition.x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
		pad.delch(cursory, cursorx - 1) # Delete the character that is one to the
	return padposition.x

def back_delete(pad, cursory, cursorx):
	pad.delch(cursory, cursorx) # Delete the character to the righ. This also
	# moves the other characters on that line one closer to the cursor

def left(pad, padposition, stdscr, cursory, cursorx, screenx):
	if cursorx > 0:
		if screenx == 0:
			if padposition.x > 0:
				padposition.x -= 1
				pad.refresh(padposition.y, padposition.x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
		newx = cursorx - 1
		pad.move(cursory, newx)
	return padposition.x

def right(pad, padposition, stdscr, cursory, cursorx, screenx):
	if screenx == stdscr.getmaxyx()[1] - 1:
		padposition.x += 1
	if cursorx == pad.getmaxyx()[1] - 1:
		pad.resize(pad.getmaxyx()[0], pad.getmaxyx()[1] + 1)
	newx = cursorx + 1
	pad.move(cursory, newx)
	pad.refresh(padposition.y, padposition.x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
	return padposition.x

def up(pad, padposition, stdscr, cursory, cursorx, screeny):
	if cursory != 0:
		if screeny == 0:
			if padposition.y != 0:
				padposition.y -= 1
				pad.refresh(padposition.y, padposition.x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
		newy = cursory - 1
		pad.move(newy, cursorx)
	return padposition.y

def down(pad, padposition, stdscr, cursory, cursorx, screeny):
	if screeny == stdscr.getmaxyx()[0] - 1:
		padposition.y += 1
	if cursory == pad.getmaxyx()[0] - 1:
		pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
	newy = cursory + 1
	pad.move(newy, cursorx)
	pad.refresh(padposition.y, padposition.x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
	return padposition.y

def enter(pad, padposition, stdscr, cursory, screeny, eol):
	pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
	pad.clrtoeol()
	if screeny == stdscr.getmaxyx()[0] - 1:
		padposition.y += 1
		pad.refresh(padposition.y, padposition.x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
	pad.move(cursory + 1, 0)
	pad.insertln()
	pad.insstr(eol)
	return padposition.y

def syntaxHighlight(pad, padposition, stdscr, cursory, cursorx, operators): 
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
	if operators[0] != None:
		if cursory == pad.getmaxyx()[0] - 1:
			pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
			pad.refresh(padposition.y, padposition.x, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)

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
		# regex time! 
		pad.move(cursory, 0)
		funcs = re.findall("\w*\(.*\)", currline)
		for f in funcs:
			p = re.compile("(\w*)\([^\)]*\)")
			m = p.findall(f)
			for i in m: 
				for x in range(eol):
					foundx = currline.find(i + "(", x, eol) # Hacky fix for detecting just a word as a function. TODO: actually fix 
					if foundx != -1: 
						pad.move(cursory, foundx) 
						pad.addstr(i, curses.color_pair(3))
	pad.move(cursory, cursorx)

def fileSyntax(pad, operators):
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	if operators[0] != None:
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
