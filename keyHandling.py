from keyActions import *
from fileInteractions import *
import curses

def handlekeys(pad, pad_y, pad_x, stdscr, cursory, cursorx, screeny, screenx, linelength, eol, tabsize, filename, key, opperators):

	if key == 265: # F1
		exit() # exit without saving

	elif key == 266: # F2
		save_close(pad, pad_y, pad_x, filename) # Saves the file with the content to a user specified file.

	elif key == 267: # F3
		pass

	elif key == 268: # F4
		pass

	elif key == 263: # Backspace
	# Doesn't work with the default GNOME terminal //TODO make it universal
		delete(pad, pad_y, pad_x, stdscr, cursory, cursorx, screenx)

	elif key == 330: #Delete-key
		back_delete(pad, cursory, cursorx)

#==================================== Cursor keys ====================================#
	elif key == 260: # Left key
		left(pad, pad_y, pad_x, stdscr, cursory, cursorx, screenx)

	elif key == 261: # Right key
		right(pad, pad_y, pad_x, stdscr, cursory, cursorx, screenx)

	elif key == 259: # Up key
		up(pad, pad_y, pad_x, stdscr, cursory, cursorx, screeny)

	elif key == 258: # Down key
		down(pad, pad_y, pad_x, stdscr, cursory, cursorx, screeny)

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
		enter(pad, pad_y, pad_x, stdscr, cursory, screeny, eol)


	else:
		key_char = str(key)
		# scrolls pad to the right if cursor is at right edge
		if screenx == stdscr.getmaxyx()[1] - 1:
			pad_x += 1
		# expands pad if max x is reached
		if cursorx == pad.getmaxyx()[1] - 1:
			pad.resize(pad.getmaxyx()[0], pad.getmaxyx()[1] + 1)
		if cursorx + tabsize + linelength > pad.getmaxyx()[1] - 1:
			pad.resize(pad.getmaxyx()[0], cursorx + tabsize + linelength + 1)

		pad.insstr(key_char) # Add input to the screen

		if key_char == "\t":
			for x in range(0, tabsize):
				if (cursorx - x) % tabsize == 0:
					cursorx = cursorx + tabsize - x
		else:
			cursorx += + 1
		# syntaxHighlight(pad, cursory, cursorx, opperators)