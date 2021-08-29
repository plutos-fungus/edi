from keyActions import *
from fileInteractions import *
import curses
from globalDefinitions import *
def handlekeys(pad, myPad, stdscr, cursor, linelength, eol, tabsize, filename, key, opperators):

	if key == 265: # F1
		exit() # exit without saving

	elif key == 266: # F2
		save_close(pad, myPad, filename) # Saves the file with the content to a user specified file.

	elif key == 267: # F3
		pass

	elif key == 268: # F4
		pass

	elif key == 263: # Backspace
	# Doesn't work with the default GNOME terminal //TODO make it universal
		myPad.x = delete(pad, myPad, stdscr, cursor)

	elif key == 330: #Delete-key
		back_delete(pad, cursor)

#==================================== Cursor keys ====================================#
	elif key == 260: # Left key
		myPad.x = left(pad, myPad, stdscr, cursor)

	elif key == 261: # Right key
		myPad.x = right(pad, myPad, stdscr, cursor)

	elif key == 259: # Up key
		myPad.y = up(pad, myPad, stdscr, cursor)

	elif key == 258: # Down key
		myPad.y = down(pad, myPad, stdscr, cursor)

	elif key == 410: # Resize event
		stdscr.refresh()
		curses.update_lines_cols()
		if curses.LINES > pad.getmaxyx()[0]:
			pad.resize(curses.LINES, pad.getmaxyx()[1])
		if curses.COLS > pad.getmaxyx()[1]:
			pad.resize(pad.getmaxyx()[0], curses.COLS)

	elif key == -1: # No key has been registered
		pass

	elif str(key) == None:
		pass

	elif str(key) == "\n":
		myPad.y = enter(pad, myPad, stdscr, cursor, eol)

	else:
		key_char = str(key)
		# scrolls pad to the right if cursor is at right edge
		if cursor.sx == stdscr.getmaxyx()[1] - 1:
			myPad.x += 1
		# expands pad if max x is reached
		if cursor.px == pad.getmaxyx()[1] - 1:
			pad.resize(pad.getmaxyx()[0], pad.getmaxyx()[1] + 1)
		if cursor.px + tabsize + linelength > pad.getmaxyx()[1] - 1:
			pad.resize(pad.getmaxyx()[0], cursor.px + tabsize + linelength + 1)

		pad.insstr(key_char) # Add input to the screen

		if key_char == "\t":
			for x in range(0, tabsize):
				if (cursor.px - x) % tabsize == 0:
					cursor.px = cursor.px + tabsize - x
		else:
			cursor.px += + 1
		syntaxHighlight(pad, myPad, stdscr, cursor, opperators)