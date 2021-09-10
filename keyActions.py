import curses
import re 
from globalDefinitions import *
# TODO: deleting past the current line
def delete(pad, myPad, stdscr, cursor): # Doesn't work with the default GNOME terminal
	if cursor.px > 0: # preventing crash
		if cursor.sx == 0:
			if myPad.posx > 1:
				myPad.posx -= 2
				pad.refresh(myPad.posy, myPad.posx, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
			elif myPad.posx > 0:
				myPad.posx -= 1
				pad.refresh(myPad.posy, myPad.posx, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
		pad.delch(cursor.py, cursor.px - 1) # Delete the character that is one to the
	return myPad.posx

def back_delete(pad, cursor):
	pad.delch(cursor.py, cursor.px) # Delete the character to the right. This also
	# moves the other characters on that line one closer to the cursor

def left(pad, myPad, stdscr, cursor):
	if cursor.px > 0:
		if cursor.sx == 0:
			if myPad.posx > 0:
				myPad.posx -= 1
				pad.refresh(myPad.posy, myPad.posx, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
		newx = cursor.px - 1
		pad.move(cursor.py, newx)
	return myPad.posx

def right(pad, myPad, stdscr, cursor):
	if cursor.sx == stdscr.getmaxyx()[1] - 1:
		myPad.posx += 1
	if cursor.px == pad.getmaxyx()[1] - 1:
		pad.resize(pad.getmaxyx()[0], pad.getmaxyx()[1] + 1)
	newx = cursor.px + 1
	pad.move(cursor.py, newx)
	pad.refresh(myPad.posy, myPad.posx, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
	return myPad.posx


def up(pad, myPad, stdscr, cursor):
	if cursor.py != 0:
		if cursor.sy == 0:
			if myPad.posy != 0:
				myPad.posy -= 1
				pad.refresh(myPad.posy, myPad.posx, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
		newy = cursor.py - 1
		pad.move(newy, cursor.px)
	return myPad.posy

def down(pad, myPad, stdscr, cursor):
	if cursor.sy == stdscr.getmaxyx()[0] - 1:
		myPad.posy += 1
	if cursor.py == pad.getmaxyx()[0] - 1:
		pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
	newy = cursor.py + 1
	pad.move(newy, cursor.px)
	pad.refresh(myPad.posy, myPad.posx, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
	return myPad.posy

def enter(pad, myPad, stdscr, cursor, eol):
	pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
	pad.clrtoeol()
	if cursor.sy == stdscr.getmaxyx()[0] - 1:
		myPad.posy += 1
		pad.refresh(myPad.posy, myPad.posx, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)
	pad.move(cursor.py + 1, 0)
	pad.insertln()
	pad.insstr(eol)
	return myPad.posy

def syntaxHighlight(pad, myPad, stdscr, cursor, operators): 
	# Getting operators 
	if operators[0] != None:
		if cursor.py == pad.getmaxyx()[0] - 1:
			pad.resize(pad.getmaxyx()[0] + 1, pad.getmaxyx()[1])
			pad.refresh(myPad.posy, myPad.posx, 0, 0, stdscr.getmaxyx()[0] - 1, stdscr.getmaxyx()[1] - 1)

		currline = pad.instr(cursor.py, 0).decode("utf-8") # Get contents of current line 
		eol = len(currline)
		pad.move(cursor.py, 0)
		pad.addstr(currline, curses.color_pair(1))
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
					pad.move(cursor.py, xpos)
					pad.addstr(o, curses.color_pair(2))
		# functions. Should be done as part of language config file somehow 
		pad.move(cursor.py, 0)
		funcs = re.findall("\w*\(.*\)", currline)
		for f in funcs:
			p = re.compile("(\w*)\([^\)]*\)")
			m = p.findall(f)
			for i in m: 
				for x in range(eol):
					foundx = currline.find(i + "(", x, eol) # Hacky fix for detecting just a word as a function. TODO: actually fix 
					if foundx != -1: 
						pad.move(cursor.py, foundx) 
						pad.addstr(i, curses.color_pair(3))
	pad.move(cursor.py, cursor.px)

def fileSyntax(pad, operators):
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

	for y in range(pad.getmaxyx()[0] - 1):
		currline = pad.instr(y, 0).decode("utf-8")
		eol = len(currline)
		funcs = re.findall("\w*\(.*\)", currline)
		for f in funcs:
			p = re.compile("(\w*)\([^\)]*\)")
			m = p.findall(f)
			for i in m: 
				for x in range(eol):
					foundx = currline.find(i + "(", x, eol) # Hacky fix for detecting just a word as a function. TODO: actually fix 
					if foundx != -1: 
						pad.move(y, foundx) 
						pad.addstr(i, curses.color_pair(3))
	pad.move(0, 0)
